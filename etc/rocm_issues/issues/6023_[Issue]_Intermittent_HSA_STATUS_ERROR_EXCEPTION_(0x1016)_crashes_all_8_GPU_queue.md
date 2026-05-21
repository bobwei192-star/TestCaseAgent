# [Issue]: Intermittent HSA_STATUS_ERROR_EXCEPTION (0x1016) crashes all 8 GPU queues serving Qwen3.5-397B-A17B on 8×MI325X (TP8)

> **Issue #6023**
> **状态**: open
> **创建时间**: 2026-03-07T22:10:35Z
> **更新时间**: 2026-05-12T15:56:01Z
> **作者**: ianschenck
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6023

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

**Intermittent HSA_STATUS_ERROR_EXCEPTION (0x1016) crashes all 8 GPU queues serving Qwen3.5-397B-A17B on 8×MI325X (TP8)**

During tensor-parallel inference serving Qwen3.5-397B-A17B on 8×MI325X (XGMI fully-connected), GPU queues intermittently crash with `HSA_STATUS_ERROR_EXCEPTION` code `0x1016` (memory aperture violation). The fault cascades across all 8 GPUs within ~600ms, aborting all scheduler processes. The crash occurs during normal decode batches with no preceding application-level error.

**This reproduces on both ROCm 7.0.0 and ROCm 7.2.0** using AMD's officially recommended Docker images and configuration for this model.

## Crash Signature

```
:0:rocdevice.cpp:3586: Callback: Queue 0x7f78cb400000 aborting with error : HSA_STATUS_ERROR_EXCEPTION: An HSAIL operation resulted in a hardware exception. code: 0x1016
```

All 8 GPU queues crash in rapid succession (~600ms total):

| Time (μs offset) | Queue Address | Delta |
|---|---|---|
| 74339723890 | 0x7f78cb400000 | — |
| 74339844633 | 0x7ed480c00000 | +121ms |
| 74339965489 | 0x7edc9ec00000 | +121ms |
| 74340015890 | 0x7ecb76e00000 | +50ms |
| 74340034649 | 0x7f27d6a00000 | +19ms |
| 74340198441 | 0x7f4fdec00000 | +164ms |
| 74340274680 | 0x7edd6ee00000 | +76ms |
| 74340311292 | 0x7ef66a400000 | +37ms |

Each crash is preceded by a failed GPU coredump attempt:
```
GPU coredump: execvp failed: No such file or directory
Failed to write program header to pipe: Broken pipe
GPU core dump failed
```

## Environment

| Component | Version |
|-----------|---------|
| **GPU** | 8× AMD Instinct MI325X (gfx942, 262 GB HBM3e each) |
| **Interconnect** | XGMI fully-connected, 1 hop, weight 15 |
| **Host OS** | Ubuntu 22.04.5 LTS, kernel 5.15.0-171-generic |
| **Host driver** | amdgpu-dkms 6.14.14.30100100 |
| **Host ROCm** | rocm-core 7.0.1.70001 |
| **Docker image** | `rocm/sgl-dev:v0.5.8.post1-rocm720-mi30x-20260215` (AMD recommended) |
| **Container ROCm** | 7.2.0 (HIP 7.2.26015-fc0010cf6a) |
| **PyTorch** | 2.9.1+rocm7.2.0.git7e1940d4 |
| **RCCL** | 2.27.7 |
| **SGLang** | 0.5.8.post1.dev20260215 |
| **aiter** | Built-in (JIT compiled, `SGLANG_USE_AITER=1`) |
| **VBIOS** | 113-M3250101-100 |
| **HSA Runtime** | 1.18 |

**Also reproduced on**: ROCm 7.0.0 image (`rocm/sgl-dev:v0.5.9-rocm700-mi30x-20260306`) with RCCL 2.26.6, SGLang 0.5.9.

## Workload

Following AMD's official deployment guide: [Day 0 Support for Qwen 3.5 on AMD Instinct GPUs](https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-qwen-3-5-on-amd-instinct-gpus.html)

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen3.5-397B-A17B \
  --tp 8 \
  --attention-backend triton \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder \
  --served-model-name Qwen3.5-397B-A17B \
  --port 8081 --host 0.0.0.0
```

- **Model**: Qwen3.5-397B-A17B (hybrid Mamba+Attention MoE, 304 experts, 10 active/token)
- **TP**: 8 (one rank per GPU)
- **Attention backend**: triton (required — hybrid Mamba model, wave backend crashes)
- **MoE backend**: aiter fused_moe (CK 2-stage)
- **All-reduce**: AiterCustomAllreduce (AMD default, loaded from `/sgl-workspace/aiter/aiter/jit/module_custom_all_reduce.so`)
- **CUDA graphs**: enabled (52 batch sizes)
- **KV cache**: bf16 (default)
- **Memory per GPU**: ~93 GB weights + ~55 GB Mamba cache + KV cache, ~39 GB free

## Symptoms

1. Server operates normally for minutes to hours under light-to-moderate load (~65 tok/s decode throughput)
2. During a normal decode batch, one GPU queue hits 0x1016
3. Within ~600ms, all 8 GPU queues cascade-fail with the same error
4. All 8 scheduler processes abort (`Fatal Python error: Aborted`)
5. Crash call stack: `scheduler.py:event_loop_normal` → `scheduler.py:process_batch_result` → `scheduler_output_processor_mixin.py:process_batch_result_decode` (line 430)
6. The main FastAPI process survives but becomes unresponsive (serves HTTP 503, heartbeat frozen)
7. No error in application logs before the fault — last entries are normal 200 OK responses
8. dmesg shows only `amdgpu: Freeing queue vital buffer ..., queue evicted` (cleanup, not the fault itself)

## Hardware Diagnostics at Crash Time

All captured by automated watchdog within seconds of the crash:

| Signal | Finding |
|--------|---------|
| **RAS counters** | All zeros on all 8 GPUs — no UMC, GFX, MMHUB, SDMA, XGMI_WAFL correctable or uncorrectable errors |
| **VRAM usage** | ~105 GB / 275 GB per GPU — well within limits |
| **dmesg** | No vm_fault, page_fault, poison, or GPU reset messages |
| **PCIe AER** | No uncorrectable errors |
| **XGMI** | `rocm-smi --showxgmierr` returns "Invalid arguments provided" (not implemented?) |
| **Process state** | All 8 scheduler processes in `R (running)` state at capture time |
| **Host memory** | ~350 GB free of 1.5 TB |
| **GPU temperature** | Normal operating range |

## What We've Ruled Out

| Hypothesis | How Ruled Out |
|---|---|
| **Hardware ECC errors** | RAS counters all zero across all blocks on all 8 GPUs |
| **OOM** | ~39 GB free per GPU, no OOM in logs |
| **Thermal** | GPUs within normal operating range |
| **PCIe/XGMI transport errors** | No AER errors, no XGMI_WAFL RAS counts |
| **ROCm version-specific** | Tested two different Docker images: `rocm/sgl-dev:v0.5.9-rocm700-mi30x-20260306` (ROCm 7.0, RCCL 2.26.6) and `rocm/sgl-dev:v0.5.8.post1-rocm720-mi30x-20260215` (ROCm 7.2, RCCL 2.27.7). Crash reproduces on both. |

## What We've Tested

| Configuration | Result |
|---|---|
| `--disable-cuda-graph` | No crash observed in brief test, but 3.1× slower (18 vs 57 tok/s) — not viable |
| ROCm 7.0.0 → 7.2.0 upgrade | Crash still occurs, 15% better throughput |

## Hypothesis

0x1016 is `HSA_STATUS_ERROR_MEMORY_APERTURE_VIOLATION` — a bad GPU virtual address access. Given that hardware diagnostics are completely clean, this is likely a software bug. Possible causes:

1. **Stale pointer in CUDA graph replay**: A buffer address captured during graph recording becomes invalid when the buffer pool is rearranged between recordings, and a specific batch size triggers replay of a graph with a stale pointer.
2. **aiter JIT kernel bug**: AiterCustomAllreduce or fused_moe accesses an out-of-bounds offset for certain tensor shapes that only occur under specific batch compositions.
3. **CUDA graph + aiter custom all-reduce interaction**: The custom all-reduce kernel uses shared memory IPC handles that may become stale when replayed inside a CUDA graph.

The fact that `--disable-cuda-graph` didn't crash in brief testing (but is 3× slower) makes CUDA graph replay a strong suspect, but we haven't been able to run it long enough to confirm.


### Operating System

Ubuntu 22.04.5 LTS (host), Docker container based on ROCm 7.2.0

### CPU

2× AMD EPYC (256 threads, 1.5 TB RAM)

### GPU

8× AMD Instinct MI325X (gfx942)

### ROCm Version

Host: 7.0.1 (amdgpu-dkms 6.14.14), Container: 7.2.0 (rocm/sgl-dev:v0.5.8.post1-rocm720-mi30x-20260215)

### ROCm Component

HSA Runtime, aiter, RCCL

### Steps to Reproduce

1. Pull AMD-recommended image: `docker pull rocm/sgl-dev:v0.5.8.post1-rocm720-mi30x-20260215`
2. Launch with the command shown in the Workload section on 8×MI325X
3. Send sustained inference traffic (chat completions API)
4. Wait — crash occurs intermittently (minutes to hours)

We do not yet have a minimal reproducer outside of SGLang. The crash appears to require:
- TP8 across 8 GPUs with XGMI
- CUDA graphs enabled
- AiterCustomAllreduce
- Sustained decode batches of varying sizes

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.14.14 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 3 (first GPU — all 8 are identical)
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-b39adaf836600b31               
  Marketing Name:          AMD Instinct MI325X                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29861(0x74a5)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   29952                              
  Internal Node ID:        2                                  
  Compute Unit:            304                                
  SIMDs per CU:            4                                  
  Shader Engines:          32                                 
  Shader Arrs. per Eng.:   1                                  
  Coherent Host Access:    FALSE                              
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Packet Processor uCode:: 177                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1: GLOBAL; COARSE GRAINED   268419072 KB
    Pool 2: GLOBAL; EXTENDED FINE GRAINED   268419072 KB
    Pool 3: GLOBAL; FINE GRAINED   268419072 KB
    Pool 4: GROUP   64 KB
  ISA Info:                
    ISA 1: amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
    ISA 2: amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
```
(Showing 1 of 8 identical GPU agents. 2 CPU agents: AMD EPYC 9575F 64-Core Processor. Full 1125-line output available on request.)

### Additional Information

**Crash frequency**: Multiple times per day under normal traffic. The dmesg `queue evicted` pattern shows 79 distinct crash timestamps in 20 hours of uptime, though many are from the container auto-restarting and crashing again.

**Automated diagnostics**: We have a watchdog script that auto-captures `dmesg`, `rocm-smi --showall`, `rocm-smi --showrasinfo`, `rocm-smi --showmeminfo vram`, PCIe AER state, XGMI errors, process state, and container logs within seconds of detecting an unresponsive server. Full capture archives available on request.

**AMD guide reference**: We are following https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-qwen-3-5-on-amd-instinct-gpus.html exactly.


---

## 评论 (3 条)

### 评论 #1 — ianschenck (2026-03-08T21:14:12Z)

Turning off the custom all-reduce (`--disable-custom-all-reduce`) has been stable (at the cost of throughput).

---

### 评论 #2 — huanrwan-amd (2026-03-24T14:40:01Z)

Hi @ianschenck, internal team found there is an issue on Aiter for this. I will let you know when it is fixed. 

---

### 评论 #3 — huanrwan-amd (2026-05-12T15:56:01Z)

@ianschenck , https://github.com/ROCm/aiter/pull/2324 seems fix this. Let us know if you still see the issue. 

---
