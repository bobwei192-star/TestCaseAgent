# [Issue]: 100% GPU usage and high power draw during idle after memcpy/memset with HIP streams on RDNA3

> **Issue #2625**
> **状态**: closed
> **创建时间**: 2023-11-02T16:07:24Z
> **更新时间**: 2026-05-03T02:09:29Z
> **关闭时间**: 2024-10-02T14:00:32Z
> **作者**: Googulator
> **标签**: Under Investigation, 5.7.1
> **URL**: https://github.com/ROCm/ROCm/issues/2625

## 标签

- **Under Investigation** (颜色: #0052cc)
- **5.7.1** (颜色: #b60205)

## 描述

### Problem Description

When running llama.cpp's server example on ROCm, using an RDNA3 GPU, GPU usage is shown as 100% and a high power consumption is measured at the wall outlet, even with the server at idle.

Investigating further, it seems that the issue is related to HIP stream usage: GPU usage first shoots up to persistent 100% when llama.cpp tries to create its second HIP stream. If I limit llama.cpp to use only a single stream, then GPU load behaves normally until it begins writing into GPU memory using hipMemcpy or hipMemset, at which point it permanently jumps up to 100%, and stays there until llama.cpp is closed.

In minimal testcases, the following scenarios all yielded 100% GPU usage, despite never actually executing any user code on the GPU:

- Creating a HIP stream while another HIP stream is open. Once triggered, closing the HIP streams doesn't help. (If I open a stream and close it, then open another one, with no overlap in time between the 2 streams, the issue isn't seen.)
- Writing to GPU memory while a HIP stream is open. Once triggered, neither closing the HIP stream nor deallocating the memory previously written will cause the GPU load to come down, only killing the process helps. (If I close the stream before writing to GPU memory, the issue isn't seen, even if that memory was allocated before or during the stream's lifetime.)
- Creating a HIP stream after **any** GPU memory write has taken place, _even if the previously written memory is freed_ before the stream is created. Once triggered, closing the HIP stream doesn't help.

I've attached minimal testcases, as well as strace logs for each of them.

### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 5 4500 6-Core Processor

### GPU

Radeon RX 7900 XT (gfx1100)

### ROCm Version

5.7.1

### ROCm Component

hipBLAS, rocBLAS or amdgpu kernel driver(?)

### Steps to Reproduce

Execute any of the reproX.cpp testcases like this:
`hipcc reproX.cpp; ./a.out`
and watch the output of rocm-smi, or a physical power meter.

Using the noreproX.cpp testcases, normal behavior (no persistent 100% GPU load) is observed.

(The files are renamed to a ".txt" extension because of GitHub's extension filter.)

[norepro1.cpp](https://github.com/RadeonOpenCompute/ROCm/files/13242036/norepro1.cpp.txt)
[norepro1.strace](https://github.com/RadeonOpenCompute/ROCm/files/13242037/norepro1.strace.txt)
[norepro2.cpp](https://github.com/RadeonOpenCompute/ROCm/files/13242038/norepro2.cpp.txt)
[norepro2.strace](https://github.com/RadeonOpenCompute/ROCm/files/13242039/norepro2.strace.txt)
[repro1.cpp](https://github.com/RadeonOpenCompute/ROCm/files/13242040/repro1.cpp.txt)
[repro1.strace](https://github.com/RadeonOpenCompute/ROCm/files/13242041/repro1.strace.txt)
[repro2.cpp](https://github.com/RadeonOpenCompute/ROCm/files/13242042/repro2.cpp.txt)
[repro2.strace](https://github.com/RadeonOpenCompute/ROCm/files/13242043/repro2.strace.txt)
[repro3.cpp](https://github.com/RadeonOpenCompute/ROCm/files/13242044/repro3.cpp.txt)
[repro3.strace](https://github.com/RadeonOpenCompute/ROCm/files/13242045/repro3.strace.txt)


### Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 5 4500 6-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 5 4500 6-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   4208
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            12
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32722432(0x1f34e00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32722432(0x1f34e00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32722432(0x1f34e00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1100
  Uuid:                    GPU-22a3388da1ef8d2a
  Marketing Name:          Radeon RX 7900 XT
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      6144(0x1800) KB
    L3:                      81920(0x14000) KB
  Chip ID:                 29772(0x744c)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2025
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            84
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 546
  SDMA engine uCode::      19
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    20955136(0x13fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS:
      Size:                    20955136(0x13fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1100
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***

---

## 评论 (12 条)

### 评论 #1 — Googulator (2023-11-10T14:39:45Z)

Found a workaround: by loading the amdgpu kernel module with the option "sched_policy=2", the power draw stays low both in llama.cpp and the attached examples. Unfortunately, this causes a slight increase of true idle power draw, i.e. when no ROCm program is running at all.

modinfo describes sched_policy as follows:

> parm:           sched_policy:Scheduling policy (0 = HWS (Default), 1 = HWS without over-subscription, 2 = Non-HWS (Used for debugging only) (int)

which has me a bit worried about deploying this workaround in production.

---

### 评论 #2 — Googulator (2023-11-10T16:33:31Z)

Debugging this further, it seems that excessive power usage starts when the offending operation (memory write or stream creation) creates a new HW queue. On RDNA3, this always uses MES, even when mes=0 is specified in the module parameters.

Within the MES code, mes_v11_0_add_hw_queue then calls mes_v11_0_submit_pkt_and_poll_completion, which calls amdgpu_ring_commit. As soon as amdgpu_ring_commit returns, GPU usage spikes to 100%, and remains there, using about 100W of excess power. 

---

### 评论 #3 — kentrussell (2023-11-14T18:27:19Z)

Will use https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver/issues/153 for updates

---

### 评论 #4 — 65a (2024-01-01T06:13:46Z)

`GPU_MAX_HW_QUEUES=1` in the environment seems to be a workaround. This should receive an upstream fix, but hopefully that helps ROCm developers narrow the problem.

---

### 评论 #5 — spitzenidee (2024-01-14T17:01:01Z)

Thank you for suggesting `GPU_MAX_HW_QUEUES=1`! I can confirm that it drops power usage for llama.cpp from ~30W power draw at the wall socket while waiting "idle" for prompts (without the env var) to 5-7W with the env var (7B Mistral with all layers offloaded to the iGPU / APU: `server --mlock -to 60000 --host 0.0.0.0 --port 9980 -b 4096 -c 16384 -n -1 -t 14 -ngl 35 -m /usr/local/lib/llm_gguf/speechless-code-mistral-7b-v1.0.Q5_K_M.gguf`).

I measure and log power draw using a smart wall Zigbee plug in Home Assistant, so I see the sum of power drawn by the CPU / GPU (in my case a AMD 7940HS) including, mainboard, power supply etc.

---

### 评论 #6 — Googulator (2024-01-15T09:24:48Z)

Thank you, GPU_MAX_HW_QUEUES=1 is indeed a viable workaround with fewer side effects than disabling hardware scheduling altogether.

---

### 评论 #7 — ppanchad-amd (2024-05-16T18:12:17Z)

@Googulator Can we close this ticket? Thanks!

---

### 评论 #8 — kentrussell (2024-05-17T14:01:55Z)

@ppanchad-amd We've got an internal JIRA for this. The RLC guys had a FW fix, but we want to check it out before closing this off. There's a workaround which is nice, but it's not resolved properly yet. Ping me if you want to consolidate this with the internal JIRA

---

### 评论 #9 — kentrussell (2024-06-20T20:17:20Z)

We've got an RLC FW fix coming in ROCm 6.2 that should also work to address this issue.



---

### 评论 #10 — harkgill-amd (2024-10-02T14:00:33Z)

@Googulator, the fix was implemented in ROCm 6.2 and I can no longer reproduce the 100% GPU usage when compiling the samples provided. Closing this ticket out, if you have any questions or are still experiencing the reported issues, please leave a comment and I will re-open this ticket. Thanks!

---

### 评论 #11 — thxCode (2025-01-10T04:05:29Z)

@kentrussell , @Googulator PTAL. after some testing, this issue still exists. am I missing something? thanks.

#### process info

llama-box is based on llama.cpp and using the ggml.

#### host info: 6.2.4

<img width="916" alt="image" src="https://github.com/user-attachments/assets/130c5a32-f099-4965-a263-6d6272bb69f6" />

```shell
$  rocminfo --support
ROCk module version 6.8.5 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.14
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    Intel(R) Core(TM) i5-14600KF
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i5-14600KF
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5300
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            20
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65616716(0x3e93b4c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65616716(0x3e93b4c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65616716(0x3e93b4c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1101
  Uuid:                    GPU-5c88007d760374f3
  Marketing Name:
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      65536(0x10000) KB
  Chip ID:                 29822(0x747e)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2254
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            60
  SIMDs per CU:            2
  Shader Engines:          3
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 232
  SDMA engine uCode::      22
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1101
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***
```

#### backend build with rocm/hip 6.2.4

1. without `GPU_MAX_HW_QUEUES=1`, running 3 instances cause the GPU utilization to reach 100%.

<img width="1891" alt="image" src="https://github.com/user-attachments/assets/137978c4-ff74-49af-bf28-0a66de54996d" />

2. with `GPU_MAX_HW_QUEUES=1`, running 3 instances is fine, but running 5 instances gets the same result as without `GPU_MAX_HW_QUEUES=1`.

<img width="1971" alt="image" src="https://github.com/user-attachments/assets/0635b3b3-3919-4d3e-bb0e-a1c3d49b77f7" />

3. with `GPU_MAX_HW_QUEUES=1`, and modify drm/amdgpu with `sched_policy=2`, we can only run up to 3 instances.

<img width="1974" alt="image" src="https://github.com/user-attachments/assets/42bd3927-13c2-49ad-ab38-63e98c696584" />



---

### 评论 #12 — oxidworks (2026-05-03T02:09:28Z)

Still occurring after the ROCm 6.2 RLC FW fix. @thxCode already noted this in January 2025 with no follow-up. Confirming on a current stack:

System:
- GPU: Radeon RX 7900 XTX (gfx1100)
- ROCm: 7.2.1
- PyTorch: 2.10.0.dev nightly with HIP 6.4.4
- Kernel: 6.17.0-14
- Distro: Linux Mint 22.2

Reproducer: PyTorch+ROCm SDXL inference, cancelled mid-sampling. Polling sysfs once per second:

- During sampling: gpu_busy_percent fluctuates 4-97%, mem_busy_percent 0-48% (correlated, real load).
- ~4 seconds after the job ends: gpu_busy_percent snaps to 100% and stays there. mem_busy_percent stays at 0%, \`rocm-smi --showmemuse\` reports Avg. Memory Bandwidth = 0. Restarting the Python process resets it.

Tested GPU_MAX_HW_QUEUES=1: makes it worse. With the workaround set, gpu_busy_percent pins to 100% from the very first compute call, mem_busy_percent stays near 0 even during active sampling.

1. Is the ROCm 6.2 RLC FW fix still active in 7.2.1, or bound to a code path the current HIP 6.4.4 PyTorch build doesn't take?
2. Is the Linux 7.0 MES-firmware fix from #5706 portable to RDNA3?

Happy to provide additional logs or test patches.

---
