# [Issue]: RCCL 2.27.7 / ROCm 7.2.1 dual-GPU collectives fail on 2x Radeon RX 7900 XTX

> **Issue #6074**
> **状态**: open
> **创建时间**: 2026-03-28T17:27:22Z
> **更新时间**: 2026-05-07T16:46:08Z
> **作者**: msembinelli
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6074

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

## Context

I originally hit this while trying to get **vLLM nightlies** working for tensor-parallel multi-GPU inference. The container I was using was:

- `vllm/vllm-openai-rocm:nightly-148a5c1226f8668cb52c4900b5ff2c80344e78f2`

However, after reducing the problem, this reproduces **outside vLLM** using a minimal `torch.distributed` script on the host. So this does not appear to be a vLLM-specific issue.

## Problem Description

Dual-GPU collectives fail on a host system with **2x Radeon RX 7900 XTX** on **ROCm 7.2.1 / RCCL 2.27.7**.

Each GPU works individually. The failure only occurs when both GPUs participate in the same collective. The public `ROCm/rccl` repository appears deprecated/moved, so I am filing this in `ROCm/ROCm` for triage.

## System Information

### OS

```text
NAME="Ubuntu"
VERSION="24.04.4 LTS (Noble Numbat)"
```

### CPU

```text
AMD Ryzen 7 7800X3D 8-Core Processor
```

### GPU

```text
Name:                    AMD Ryzen 7 7800X3D 8-Core Processor
Marketing Name:          AMD Ryzen 7 7800X3D 8-Core Processor
Name:                    gfx1100
Marketing Name:          Radeon RX 7900 XTX
    Name:                    amdgcn-amd-amdhsa--gfx1100
    Name:                    amdgcn-amd-amdhsa--gfx11-generic
Name:                    gfx1100
Marketing Name:          Radeon RX 7900 XTX
    Name:                    amdgcn-amd-amdhsa--gfx1100
    Name:                    amdgcn-amd-amdhsa--gfx11-generic
Name:                    gfx1100
Marketing Name:          AMD Radeon Graphics
    Name:                    amdgcn-amd-amdhsa--gfx1100
    Name:                    amdgcn-amd-amdhsa--gfx11-generic
```

### Software Versions

- ROCm: `7.2.1`
- RCCL: `2.27.7-HEAD:96a25b5`
- PyTorch: `2.9.1+rocm7.2.0.git7e1940d4`
- Kernel: `6.17.0-19-generic`

## Expected Behavior

A minimal 2-rank `torch.distributed` program should successfully complete:

- `dist.barrier()`
- `dist.all_reduce()`

## Actual Behavior

The process group initializes and RCCL communicator initialization completes on both GPUs, but the first collective fails with:

- `HIP failure: 'the operation cannot be performed in the present state'`
- `torch.distributed.DistBackendError`
- `NCCL version 2.27.7`

This happens in a minimal host-side PyTorch repro, so this does **not** appear to be a vLLM-specific issue.

## Topology Observation

RCCL reports the two discrete GPUs on a `PHB` path with bandwidth `6.0`, and the second GPU is the chipset-side device (`busId d000`). The failure occurs only when a collective spans both GPUs.

## Minimal Reproduction Script

Save as `rccl_smoke.py`:

```python
#!/usr/bin/env python3
import os
import sys
import torch
import torch.distributed as dist


def log(msg: str) -> None:
    rank = int(os.environ.get("RANK", "-1"))
    local_rank = int(os.environ.get("LOCAL_RANK", "-1"))
    print(f"[rank={rank} local_rank={local_rank}] {msg}", flush=True)


def main() -> int:
    print("HIP_VISIBLE_DEVICES =", os.environ.get("HIP_VISIBLE_DEVICES"), flush=True)
    print("ROCR_VISIBLE_DEVICES =", os.environ.get("ROCR_VISIBLE_DEVICES"), flush=True)

    if not torch.cuda.is_available():
        print("torch.cuda.is_available() is False", file=sys.stderr, flush=True)
        return 2

    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])

    log(f"torch={torch.__version__}")
    log(f"cuda/HIP available={torch.cuda.is_available()} device_count={torch.cuda.device_count()}")

    torch.cuda.set_device(local_rank)
    dev = torch.device(f"cuda:{local_rank}")
    props = torch.cuda.get_device_properties(dev)
    log(f"using device {local_rank}: {props.name}")

    dist.init_process_group(
        backend="nccl",
        init_method="env://",
        world_size=world_size,
        rank=rank,
        device_id=dev,
    )
    log("process group initialized")

    x = torch.tensor([rank + 1.0], device=dev, dtype=torch.float32)
    log(f"before barrier: {x.item()}")

    # Fails here on the affected setup
    dist.barrier()
    torch.cuda.synchronize()
    log("barrier passed")

    dist.all_reduce(x, op=dist.ReduceOp.SUM)
    torch.cuda.synchronize()
    log(f"after all_reduce: {x.item()}")

    dist.destroy_process_group()
    log("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Reproduction Command

```bash
export HIP_VISIBLE_DEVICES=0,1
unset ROCR_VISIBLE_DEVICES

export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,P2P,GRAPH,ENV
export NCCL_DMABUF_ENABLE=1
export NCCL_P2P_DISABLE=1
export NCCL_MIN_NCHANNELS=1
export NCCL_MAX_NCHANNELS=1
export RCCL_CHANNEL_TUNING_ENABLE=0
export RCCL_P2P_BATCH_ENABLE=0
export HSA_FORCE_FINE_GRAIN_PCIE=1

torchrun --nproc_per_node=2 rccl_smoke.py
```

## Result

The 2-rank run fails on the first collective. A representative error is:

```text
[rank1]: torch.distributed.DistBackendError: NCCL error in:
... ProcessGroupNCCL.cpp ...
unhandled cuda error, NCCL version 2.27.7

[FATAL ERROR]: HIP failure: 'the operation cannot be performed in the present state'
```

Host-side repro logs show:

- both GPUs visible and selected correctly
- process group initialized
- communicator init completed on both ranks
- `NCCL_P2P_DISABLE=1` was honored
- transport was `via SHM/direct/direct`
- failure still occurred on the first collective on rank 1 / `busId d000`

## Additional Validation

### Single GPU: first 7900 XTX works

This passes with only the first discrete GPU exposed:

```bash
unset ROCR_VISIBLE_DEVICES
export HIP_VISIBLE_DEVICES=0
export NCCL_DEBUG=INFO
torchrun --nproc_per_node=1 rccl_smoke.py
```

### Single GPU: second 7900 XTX works

This also passes with only the second discrete GPU exposed:

```bash
unset ROCR_VISIBLE_DEVICES
export HIP_VISIBLE_DEVICES=1
export NCCL_DEBUG=INFO
torchrun --nproc_per_node=1 rccl_smoke.py
```

### Interpretation

This suggests:

- GPU 0 alone is healthy
- GPU 1 alone is healthy
- communicator initialization across both GPUs is healthy
- the failure is specific to the **first dual-GPU collective** on this topology

## Notes

- This issue reproduces both inside and outside containers, but the host-side PyTorch repro is the cleanest evidence that the failure is below vLLM.
- I previously observed this setup working on an earlier RCCL generation around `2.26.x` on the same machine, though I do not currently have a minimized side-by-side repro attached for that older version.
- The machine also has an AMD iGPU present, but the failure reproduces with only the two discrete GPUs exposed to the repro.

## Attachments

I can attach, if helpful:

1. `rccl_smoke.py`
2. full 2-GPU failing host log
3. single-GPU passing log for GPU 0
4. single-GPU passing log for GPU 1
5. equivalent vLLM failure log showing the same first-collective failure pattern

### Operating System

24.04.4 LTS (Noble Numbat)

### CPU

7800X3D

### GPU

2 x AMD Radeon 7900XTX

### ROCm Version

7.2.1

### ROCm Component

rccl

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (35 条)

### 评论 #1 — msembinelli (2026-03-28T17:44:37Z)

Same smoke test on rocm 7.2

both ranks initialize successfully
communicator init completes on both GPUs
barrier passed on both ranks
after all_reduce: 3.0 appears, which is the key success condition for the smoke test

So the important takeaway is:

ROCm 7.2.0 on host passes the dual-GPU smoke test on your topology, while 7.2.1 failed.

A few nuanced points from the log:

This is still RCCL 2.27.7-HEAD, but it is a different build than the failing one:
working: 2.27.7-HEAD:0d2c4fd
failing before: 2.27.7-HEAD:96a25b5 / similar 7.2.1-era build lineage
The working run is on:
ROCm version : 7.2.0.0-43
Librccl path : /opt/rocm-7.2.0/lib/librccl.so.1
It even works on the exact same weak topology:
GPU 3000 ↔ GPU d000
PHB
bw 6.0

```
$ unset ROCR_VISIBLE_DEVICES
export HIP_VISIBLE_DEVICES=0,1

unset NCCL_P2P_DISABLE
unset NCCL_MIN_NCHANNELS
unset NCCL_MAX_NCHANNELS
unset RCCL_CHANNEL_TUNING_ENABLE
unset RCCL_P2P_BATCH_ENABLE
unset HSA_FORCE_FINE_GRAIN_PCIE
unset NCCL_ALGO
unset NCCL_PROTO
unset NCCL_SOCKET_IFNAME
unset NCCL_RINGS
unset RCCL_TREES

export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,P2P,GRAPH,ENV,COLL,SHM

torchrun --nproc_per_node=2 rccl_smoke.py
W0328 11:41:53.835000 829457 torch/distributed/run.py:803] 
W0328 11:41:53.835000 829457 torch/distributed/run.py:803] *****************************************
W0328 11:41:53.835000 829457 torch/distributed/run.py:803] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
W0328 11:41:53.835000 829457 torch/distributed/run.py:803] *****************************************
[rank=0 local_rank=0] torch=2.9.1+rocm7.2.0.git7e1940d4
[rank=1 local_rank=1] torch=2.9.1+rocm7.2.0.git7e1940d4
[rank=0 local_rank=0] cuda/HIP available=True device_count=2
[rank=1 local_rank=1] cuda/HIP available=True device_count=2
[rank=0 local_rank=0] using device 0: Radeon RX 7900 XTX[rank=1 local_rank=1] using device 1: Radeon RX 7900 XTX

TARS:829507:829507 [0] NCCL INFO [rocprofiler-sdk-rccl][ = 829507 ] rocprofiler-register returned code = 1 : rocprofiler-register found no tools
TARS:829508:829508 [1] NCCL INFO [rocprofiler-sdk-rccl][ = 829508 ] rocprofiler-register returned code = 1 : rocprofiler-register found no tools
[rank=0 local_rank=0] process group initialized
[rank=1 local_rank=1] process group initialized
[rank=0 local_rank=0] before all_reduce: 1.0
[rank=1 local_rank=1] before all_reduce: 2.0
/home/matt/lib/python3.12/site-packages/torch/distributed/distributed_c10d.py:4876: UserWarning: barrier(): using the device under current context. You can specify `device_id` in `init_process_group` to mute this warning.
  warnings.warn(  # warn only once
[rank0]:[W328 11:41:55.224844091 ProcessGroupNCCL.cpp:5072] Guessing device ID based on global rank. This can cause a hang if rank to GPU mapping is heterogeneous. You can specify device_id in init_process_group()
TARS:829507:829507 [0] NCCL INFO Kernel version: 6.17.0-19-generic
TARS:829507:829507 [0] NCCL INFO Hipruntime version: 70226015, firmware version: 2650
TARS:829507:829507 [0] NCCL INFO ROCr version 1.18
TARS:829507:829507 [0] NCCL INFO Dmabuf feature disabled without NCCL_DMABUF_ENABLE=1
TARS:829507:829507 [0] NCCL INFO Kernel version: 6.17.0-19-generic
TARS:829507:829507 [0] NCCL INFO RCCL version : 2.27.7-HEAD:0d2c4fd
HIP version  : 7.2.26015-fc0010cf6a
ROCm version : 7.2.0.0-43-fc0010cf6a
Hostname     : TARS
Librccl path : /opt/rocm-7.2.0/lib/librccl.so.1
TARS:829507:829507 [0] NCCL INFO Comm config Blocking set to 1
TARS:829508:829508 [1] NCCL INFO ROCr version 1.18
TARS:829508:829508 [1] NCCL INFO Dmabuf feature disabled without NCCL_DMABUF_ENABLE=1
TARS:829508:829508 [1] NCCL INFO Kernel version: 6.17.0-19-generic
TARS:829508:829508 [1] NCCL INFO Hipruntime version: 70226015, firmware version: 2650
TARS:829508:829508 [1] NCCL INFO RCCL version : 2.27.7-HEAD:0d2c4fd
HIP version  : 7.2.26015-fc0010cf6a
ROCm version : 7.2.0.0-43-fc0010cf6a
Hostname     : TARS
Librccl path : /opt/rocm-7.2.0/lib/librccl.so.1
TARS:829508:829508 [1] NCCL INFO Comm config Blocking set to 1
TARS:829507:829550 [0] NCCL INFO NET/Plugin: Could not find: libnccl-net.so. 
TARS:829507:829550 [0] NCCL INFO NET/IB : No device found.
TARS:829507:829550 [0] NCCL INFO NET/IB : Using [RO]; OOB eno1:10.0.20.2<0>
TARS:829507:829550 [0] NCCL INFO NET/Socket : Using [0]eno1:10.0.20.2<0> [1]br-66f6c8282949:172.19.0.1<0> [2]br-93c7b977d333:172.18.0.1<0> [3]veth99b071a:fe80::c078:68ff:fed4:88c6%veth99b071a<0> [4]veth1395e36:fe80::8007:daff:fe9f:5ad2%veth1395e36<0>
TARS:829507:829550 [0] NCCL INFO Initialized NET plugin Socket
TARS:829507:829550 [0] NCCL INFO Assigned NET plugin Socket to comm
TARS:829507:829550 [0] NCCL INFO Using network Socket
TARS:829507:829550 [0] NCCL INFO [node_id = 3; gpu_id = 4479; unique_id = 0; location_id = 5632; bdf = 5632; domain = 0; partition = 0], 
TARS:829507:829550 [0] NCCL INFO [node_id = 2; gpu_id = 25016; unique_id = 6668021157319683351; location_id = 3328; bdf = 3328; domain = 0; partition = 0], 
TARS:829507:829550 [0] NCCL INFO [node_id = 1; gpu_id = 22753; unique_id = 10080792926504095258; location_id = 768; bdf = 768; domain = 0; partition = 0], 
TARS:829507:829550 [0] NCCL INFO initialized internal alternative rsmi functionality
TARS:829508:829551 [1] NCCL INFO NET/Plugin: Could not find: libnccl-net.so. 
TARS:829508:829551 [1] NCCL INFO NET/IB : No device found.
TARS:829508:829551 [1] NCCL INFO NET/IB : Using [RO]; OOB eno1:10.0.20.2<0>
TARS:829508:829551 [1] NCCL INFO NET/Socket : Using [0]eno1:10.0.20.2<0> [1]br-66f6c8282949:172.19.0.1<0> [2]br-93c7b977d333:172.18.0.1<0> [3]veth99b071a:fe80::c078:68ff:fed4:88c6%veth99b071a<0> [4]veth1395e36:fe80::8007:daff:fe9f:5ad2%veth1395e36<0>
TARS:829508:829551 [1] NCCL INFO Initialized NET plugin Socket
TARS:829508:829551 [1] NCCL INFO Assigned NET plugin Socket to comm
TARS:829508:829551 [1] NCCL INFO Using network Socket
TARS:829508:829551 [1] NCCL INFO [node_id = 3; gpu_id = 4479; unique_id = 0; location_id = 5632; bdf = 5632; domain = 0; partition = 0], 
TARS:829508:829551 [1] NCCL INFO [node_id = 2; gpu_id = 25016; unique_id = 6668021157319683351; location_id = 3328; bdf = 3328; domain = 0; partition = 0], 
TARS:829508:829551 [1] NCCL INFO [node_id = 1; gpu_id = 22753; unique_id = 10080792926504095258; location_id = 768; bdf = 768; domain = 0; partition = 0], 
TARS:829508:829551 [1] NCCL INFO initialized internal alternative rsmi functionality
TARS:829507:829550 [0] NCCL INFO ncclCommInitRankConfig_impl comm 0x2bc1f840 rank 0 nranks 2 cudaDev 0 nvmlDev 0 busId 3000 commId 0xcde2ea451c75c2ba - Init START
TARS:829508:829551 [1] NCCL INFO ncclCommInitRankConfig_impl comm 0x3ab1b680 rank 1 nranks 2 cudaDev 1 nvmlDev 1 busId d000 commId 0xcde2ea451c75c2ba - Init START
TARS:829508:829551 [1] NCCL INFO RAS client listening socket at 127.0.0.1<28028>
TARS:829507:829550 [0] NCCL INFO RAS client listening socket at 127.0.0.1<28028>
TARS:829507:829550 [0] NCCL INFO initialized internal alternative rsmi functionality
TARS:829507:829550 [0] NCCL INFO TOPO/NET : Importing network plugins to topology
TARS:829507:829550 [0] NCCL INFO Retrieving state for Socket
TARS:829507:829550 [0] NCCL INFO Initialized state 0 for Socket
TARS:829508:829551 [1] NCCL INFO initialized internal alternative rsmi functionality
TARS:829508:829551 [1] NCCL INFO TOPO/NET : Importing network plugins to topology
TARS:829508:829551 [1] NCCL INFO Retrieving state for Socket
TARS:829508:829551 [1] NCCL INFO Initialized state 0 for Socket
TARS:829507:829550 [0] NCCL INFO ncclTopoPopulateNics : Filled eno1 in topo with pciPath=/sys/devices/pci0000:00/0000:00:02.1/0000:05:00.0/0000:06:08.0/0000:09:00.0/0000:0a:04.0/0000:0e:00.0 keep=1 coll=(null)
TARS:829507:829550 [0] NCCL INFO ncclTopoPopulateNics : Filled br-66f6c8282949 in topo with pciPath=(null) keep=1 coll=(null)
TARS:829507:829550 [0] NCCL INFO ncclTopoPopulateNics : Filled br-93c7b977d333 in topo with pciPath=(null) keep=1 coll=(null)
TARS:829507:829550 [0] NCCL INFO ncclTopoPopulateNics : Filled veth99b071a in topo with pciPath=(null) keep=1 coll=(null)
TARS:829507:829550 [0] NCCL INFO ncclTopoPopulateNics : Filled veth1395e36 in topo with pciPath=(null) keep=1 coll=(null)
TARS:829508:829551 [1] NCCL INFO ncclTopoPopulateNics : Filled eno1 in topo with pciPath=/sys/devices/pci0000:00/0000:00:02.1/0000:05:00.0/0000:06:08.0/0000:09:00.0/0000:0a:04.0/0000:0e:00.0 keep=1 coll=(null)
TARS:829508:829551 [1] NCCL INFO ncclTopoPopulateNics : Filled br-66f6c8282949 in topo with pciPath=(null) keep=1 coll=(null)
TARS:829508:829551 [1] NCCL INFO ncclTopoPopulateNics : Filled br-93c7b977d333 in topo with pciPath=(null) keep=1 coll=(null)
TARS:829508:829551 [1] NCCL INFO ncclTopoPopulateNics : Filled veth99b071a in topo with pciPath=(null) keep=1 coll=(null)
TARS:829508:829551 [1] NCCL INFO ncclTopoPopulateNics : Filled veth1395e36 in topo with pciPath=(null) keep=1 coll=(null)
TARS:829507:829550 [0] NCCL INFO === System : maxBw 6.0 totalBw 24.0 ===
TARS:829507:829550 [0] NCCL INFO CPU/0-0 (1/2/6)
TARS:829507:829550 [0] NCCL INFO + PCI[5000.0] - NIC/0-0
TARS:829507:829550 [0] NCCL INFO + PCI[24.0] - PCI/0-1000 (1002147800000000)
TARS:829507:829550 [0] NCCL INFO               + PCI[24.0] - GPU/0-3000 (0)
TARS:829507:829550 [0] NCCL INFO + PCI[6.0] - PCI/0-5000 (102243f41b213328)
TARS:829507:829550 [0] NCCL INFO              + PCI[6.0] - PCI/0-9000 (102243f41b213328)
TARS:829507:829550 [0] NCCL INFO                           + PCI[6.0] - PCI/0-b000 (1002147800000000)
TARS:829507:829550 [0] NCCL INFO                                        + PCI[24.0] - GPU/0-d000 (1)
TARS:829507:829550 [0] NCCL INFO                           + PCI[0.4] - NIC/0-e000
TARS:829507:829550 [0] NCCL INFO ==========================================
TARS:829507:829550 [0] NCCL INFO GPU/0-3000 :GPU/0-3000 (0/5000.0/LOC) GPU/0-d000 (6/6.0/PHB) CPU/0-0 (2/24.0/PHB) 
TARS:829507:829550 [0] NCCL INFO GPU/0-d000 :GPU/0-3000 (6/6.0/PHB) GPU/0-d000 (0/5000.0/LOC) CPU/0-0 (4/6.0/PHB) 
TARS:829507:829550 [0] NCCL INFO Setting affinity for GPU 0 to 0-15
TARS:829507:829550 [0] NCCL INFO Pattern 4, crossNic 0, nChannels 1, bw 6.000000/6.000000, type PHB/PIX, sameChannels 1
TARS:829507:829550 [0] NCCL INFO  0 : GPU/0-3000 GPU/0-d000
TARS:829507:829550 [0] NCCL INFO Pattern 1, crossNic 0, nChannels 1, bw 6.000000/6.000000, type PHB/PIX, sameChannels 1
TARS:829507:829550 [0] NCCL INFO  0 : GPU/0-3000 GPU/0-d000
TARS:829507:829550 [0] NCCL INFO GFX9 cheap fence is OFF
TARS:829508:829551 [1] NCCL INFO === System : maxBw 6.0 totalBw 24.0 ===
TARS:829508:829551 [1] NCCL INFO CPU/0-0 (1/2/6)
TARS:829508:829551 [1] NCCL INFO + PCI[5000.0] - NIC/0-0
TARS:829508:829551 [1] NCCL INFO + PCI[24.0] - PCI/0-1000 (1002147800000000)
TARS:829508:829551 [1] NCCL INFO               + PCI[24.0] - GPU/0-3000 (0)
TARS:829508:829551 [1] NCCL INFO + PCI[6.0] - PCI/0-5000 (102243f41b213328)
TARS:829508:829551 [1] NCCL INFO              + PCI[6.0] - PCI/0-9000 (102243f41b213328)
TARS:829508:829551 [1] NCCL INFO                           + PCI[6.0] - PCI/0-b000 (1002147800000000)
TARS:829508:829551 [1] NCCL INFO                                        + PCI[24.0] - GPU/0-d000 (1)
TARS:829508:829551 [1] NCCL INFO                           + PCI[0.4] - NIC/0-e000
TARS:829508:829551 [1] NCCL INFO ==========================================
TARS:829508:829551 [1] NCCL INFO GPU/0-3000 :GPU/0-3000 (0/5000.0/LOC) GPU/0-d000 (6/6.0/PHB) CPU/0-0 (2/24.0/PHB) 
TARS:829508:829551 [1] NCCL INFO GPU/0-d000 :GPU/0-3000 (6/6.0/PHB) GPU/0-d000 (0/5000.0/LOC) CPU/0-0 (4/6.0/PHB) 
TARS:829508:829551 [1] NCCL INFO Setting affinity for GPU 1 to 0-15
TARS:829508:829551 [1] NCCL INFO Pattern 4, crossNic 0, nChannels 1, bw 6.000000/6.000000, type PHB/PIX, sameChannels 1
TARS:829508:829551 [1] NCCL INFO  0 : GPU/0-3000 GPU/0-d000
TARS:829508:829551 [1] NCCL INFO Pattern 1, crossNic 0, nChannels 1, bw 6.000000/6.000000, type PHB/PIX, sameChannels 1
TARS:829508:829551 [1] NCCL INFO  0 : GPU/0-3000 GPU/0-d000
TARS:829508:829551 [1] NCCL INFO GFX9 cheap fence is OFF
TARS:829507:829550 [0] NCCL INFO comm 0x2bc1f840 rank 0 nRanks 2 nNodes 1 localRanks 2 localRank 0 MNNVL 0
TARS:829508:829551 [1] NCCL INFO comm 0x3ab1b680 rank 1 nRanks 2 nNodes 1 localRanks 2 localRank 1 MNNVL 0
TARS:829507:829550 [0] NCCL INFO [RINGS]      00
TARS:829508:829551 [1] NCCL INFO Tree 0 : 0 -> 1 -> -1/-1/-1
TARS:829507:829550 [0] NCCL INFO [RINGS]  00->01
TARS:829508:829551 [1] NCCL INFO Tree 1 : 0 -> 1 -> -1/-1/-1
TARS:829507:829550 [0] NCCL INFO Tree 0 : -1 -> 0 -> 1/-1/-1
TARS:829507:829550 [0] NCCL INFO Tree 1 : -1 -> 0 -> 1/-1/-1
TARS:829508:829551 [1] NCCL INFO Ring 0 : 0 -> 1 -> 0 comm 0x3ab1b680 nRanks 02 busId d000
TARS:829508:829551 [1] NCCL INFO Ring 1 : 0 -> 1 -> 0 comm 0x3ab1b680 nRanks 02 busId d000
TARS:829507:829550 [0] NCCL INFO Channel 00/02 : 0 1
TARS:829508:829551 [1] NCCL INFO Trees [0] -1/-1/-1->1->0 [1] -1/-1/-1->1->0 comm 0x3ab1b680 nRanks 02 busId d000
TARS:829507:829550 [0] NCCL INFO Channel 01/02 : 0 1
TARS:829508:829551 [1] NCCL INFO P2P Chunksize set to 131072
TARS:829507:829550 [0] NCCL INFO Ring 0 : 1 -> 0 -> 1 comm 0x2bc1f840 nRanks 02 busId 3000
TARS:829507:829550 [0] NCCL INFO Ring 1 : 1 -> 0 -> 1 comm 0x2bc1f840 nRanks 02 busId 3000
TARS:829507:829550 [0] NCCL INFO Trees [0] 1/-1/-1->0->-1 [1] 1/-1/-1->0->-1 comm 0x2bc1f840 nRanks 02 busId 3000
TARS:829507:829550 [0] NCCL INFO P2P Chunksize set to 131072
TARS:829508:829551 [1] NCCL INFO PROFILER/Plugin: Could not find: librccl-profiler.so. 
TARS:829507:829550 [0] NCCL INFO PROFILER/Plugin: Could not find: librccl-profiler.so. 
TARS:829507:829550 [0] NCCL INFO Check P2P Type isAllDirectP2p 1 directMode 0
TARS:829507:829620 [0] NCCL INFO [Proxy Service UDS] Device 0 CPU core 15
TARS:829508:829619 [1] NCCL INFO [Proxy Service UDS] Device 1 CPU core 13
TARS:829507:829618 [0] NCCL INFO [Proxy Service] Device 0 CPU core 10
TARS:829508:829617 [1] NCCL INFO [Proxy Service] Device 1 CPU core 10
TARS:829507:829618 [0] NCCL INFO Allocated shareable buffer 0x7973a2400000 size 6291456 ipcDesc 0x79737c004f40
TARS:829508:829617 [1] NCCL INFO Allocated shareable buffer 0x7a196f800000 size 6291456 ipcDesc 0x7a1944004f40
TARS:829507:829618 [0] NCCL INFO Allocated shareable buffer 0x7973a2e00000 size 6291456 ipcDesc 0x79737c004f40
TARS:829507:829550 [0] NCCL INFO Channel 00/0 : 0[3000] -> 1[d000] via P2P/IPC comm 0x2bc1f840 nRanks 02
TARS:829508:829617 [1] NCCL INFO Allocated shareable buffer 0x7a1970200000 size 6291456 ipcDesc 0x7a1944004f40
TARS:829508:829551 [1] NCCL INFO Channel 00/0 : 1[d000] -> 0[3000] via P2P/IPC comm 0x3ab1b680 nRanks 02
TARS:829507:829618 [0] NCCL INFO Allocated shareable buffer 0x797384800000 size 2097152 ipcDesc 0x79737c004f40
TARS:829507:829550 [0] NCCL INFO Channel 01/0 : 0[3000] -> 1[d000] via P2P/IPC comm 0x2bc1f840 nRanks 02
TARS:829508:829617 [1] NCCL INFO Allocated shareable buffer 0x7a196e200000 size 2097152 ipcDesc 0x7a1944004f40
TARS:829508:829551 [1] NCCL INFO Channel 01/0 : 1[d000] -> 0[3000] via P2P/IPC comm 0x3ab1b680 nRanks 02
TARS:829507:829618 [0] NCCL INFO Allocated shareable buffer 0x797384400000 size 2097152 ipcDesc 0x79737c004f40
TARS:829508:829617 [1] NCCL INFO Allocated shareable buffer 0x7a1951a00000 size 2097152 ipcDesc 0x7a1944004f40
TARS:829508:829551 [1] NCCL INFO Imported shareable buffer device 1 size 6291456 ptr 0x7a196f000000
TARS:829507:829550 [0] NCCL INFO Imported shareable buffer device 0 size 6291456 ptr 0x797385600000
TARS:829508:829551 [1] NCCL INFO Imported shareable buffer device 1 size 2097152 ptr 0x7a1970c00000
TARS:829507:829550 [0] NCCL INFO Imported shareable buffer device 0 size 2097152 ptr 0x7973a3800000
TARS:829508:829551 [1] NCCL INFO Imported shareable buffer device 1 size 6291456 ptr 0x7a196e800000
TARS:829508:829551 [1] NCCL INFO Imported shareable buffer device 1 size 2097152 ptr 0x7a1951600000
TARS:829507:829550 [0] NCCL INFO Imported shareable buffer device 0 size 6291456 ptr 0x797384e00000
TARS:829507:829550 [0] NCCL INFO Imported shareable buffer device 0 size 2097152 ptr 0x797377c00000
TARS:829508:829551 [1] NCCL INFO Connected all rings, use ring PXN 0 GDR 1
TARS:829507:829550 [0] NCCL INFO Connected all rings, use ring PXN 0 GDR 1
TARS:829507:829550 [0] NCCL INFO Connected all trees
TARS:829508:829551 [1] NCCL INFO Connected all trees
TARS:829508:829624 [1] NCCL INFO [Proxy Progress] Device 1 CPU core 0
TARS:829507:829623 [0] NCCL INFO [Proxy Progress] Device 0 CPU core 2
TARS:829507:829550 [0] NCCL INFO threadThresholds 8/8/64 | 16/8/64 | 256 | 256
TARS:829507:829550 [0] NCCL INFO comm:0x2bc1f840, nRanks:2, nNodes:1, coll channels:2 collnet channels:2, nvls channels:0, p2p channels:2, p2p channels per peer:2
TARS:829507:829550 [0] NCCL INFO CC Off, workFifoBytes 4194304
TARS:829508:829551 [1] NCCL INFO threadThresholds 8/8/64 | 16/8/64 | 256 | 256
TARS:829508:829551 [1] NCCL INFO comm:0x3ab1b680, nRanks:2, nNodes:1, coll channels:2 collnet channels:2, nvls channels:0, p2p channels:2, p2p channels per peer:2
TARS:829507:829550 [0] NCCL INFO RCCL Unroll Factor (pre-set): 4
TARS:829508:829551 [1] NCCL INFO RCCL Unroll Factor (pre-set): 4
TARS:829508:829551 [1] NCCL INFO TUNER/Plugin: Could not find: libnccl-tuner.so. Using internal tuner plugin.
TARS:829507:829550 [0] NCCL INFO TUNER/Plugin: Could not find: libnccl-tuner.so. Using internal tuner plugin.
TARS:829507:829550 [0] NCCL INFO ncclCommInitRankConfig_impl comm 0x2bc1f840 rank 0 nranks 2 cudaDev 0 nvmlDev 0 busId 3000 commId 0xcde2ea451c75c2ba - Init COMPLETE
TARS:829507:829550 [0] NCCL INFO Init timings - ncclCommInitRankConfig_impl: rank 0 nranks 2 total 4.66 (kernels 4.32, alloc 0.07, bootstrap 0.02, allgathers 0.00, topo 0.14, graphs 0.00, connections 0.11, rest 0.00)
TARS:829508:829551 [1] NCCL INFO ncclCommInitRankConfig_impl comm 0x3ab1b680 rank 1 nranks 2 cudaDev 1 nvmlDev 1 busId d000 commId 0xcde2ea451c75c2ba - Init COMPLETE
TARS:829508:829551 [1] NCCL INFO Init timings - ncclCommInitRankConfig_impl: rank 1 nranks 2 total 4.65 (kernels 4.33, alloc 0.07, bootstrap 0.00, allgathers 0.00, topo 0.14, graphs 0.00, connections 0.11, rest 0.00)
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 0 sendbuff 0x7973d6e00400 recvbuff 0x7973d6e00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 0 sendbuff 0x7a1bf0a00400 recvbuff 0x7a1bf0a00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=1 local_rank=1] barrier passed
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 1 sendbuff 0x7a1bf0a00000 recvbuff 0x7a1bf0a00000 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=0 local_rank=0] barrier passed
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 1 sendbuff 0x7973d6e00000 recvbuff 0x7973d6e00000 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=0 local_rank=0] after all_reduce: 3.0
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 2 sendbuff 0x7973d6e00400 recvbuff 0x7973d6e00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=1 local_rank=1] after all_reduce: 3.0
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 2 sendbuff 0x7a1bf0a00400 recvbuff 0x7a1bf0a00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=1 local_rank=1] loop 0: all_reduce ok, value=2.0
[rank=0 local_rank=0] loop 0: all_reduce ok, value=2.0
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 3 sendbuff 0x7a1bf0a00600 recvbuff 0x7a1bf0a00600 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 3 sendbuff 0x7973d6e00600 recvbuff 0x7973d6e00600 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=0 local_rank=0] loop 1: all_reduce ok, value=2.0
[rank=1 local_rank=1] loop 1: all_reduce ok, value=2.0
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 4 sendbuff 0x7a1bf0a00400 recvbuff 0x7a1bf0a00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 4 sendbuff 0x7973d6e00400 recvbuff 0x7973d6e00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=0 local_rank=0] loop 2: all_reduce ok, value=2.0
[rank=1 local_rank=1] loop 2: all_reduce ok, value=2.0
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 5 sendbuff 0x7a1bf0a00600 recvbuff 0x7a1bf0a00600 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 5 sendbuff 0x7973d6e00600 recvbuff 0x7973d6e00600 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=0 local_rank=0] loop 3: all_reduce ok, value=2.0
[rank=1 local_rank=1] loop 3: all_reduce ok, value=2.0
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 6 sendbuff 0x7a1bf0a00400 recvbuff 0x7a1bf0a00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 6 sendbuff 0x7973d6e00400 recvbuff 0x7973d6e00400 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=0 local_rank=0] loop 4: all_reduce ok, value=2.0
[rank=1 local_rank=1] loop 4: all_reduce ok, value=2.0
TARS:829507:829507 [0] NCCL INFO AllReduce: opCount 7 sendbuff 0x7973d6e00200 recvbuff 0x7973d6e00200 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x2bc1f840 [nranks=2] stream (nil) task 0 globalrank 0
TARS:829508:829508 [1] NCCL INFO AllReduce: opCount 7 sendbuff 0x7a1bf0a00200 recvbuff 0x7a1bf0a00200 acc (nil) count 1 datatype 7 op 0 root 0 comm 0x3ab1b680 [nranks=2] stream (nil) task 0 globalrank 1
TARS:829507:829507 [0] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829508:829508 [1] NCCL INFO pre-adjustment threadThreshold:16 nBytes:4 nc:2
TARS:829507:829507 [0] NCCL INFO minNChannels:-2
TARS:829508:829508 [1] NCCL INFO minNChannels:-2
TARS:829507:829507 [0] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
TARS:829508:829508 [1] NCCL INFO post-adjustment based on threadThreshold:16 nBytes:4 nc:1
[rank=0 local_rank=0] final barrier passed
[rank=1 local_rank=1] final barrier passed
TARS:829508:829508 [1] NCCL INFO Memory used = 34132136
TARS:829507:829507 [0] NCCL INFO Memory used = 34132136
TARS:829508:829627 [1] NCCL INFO comm 0x3ab1b680 rank 1 nranks 2 cudaDev 1 busId d000 - Destroy COMPLETE
TARS:829507:829628 [0] NCCL INFO comm 0x2bc1f840 rank 0 nranks 2 cudaDev 0 busId 3000 - Destroy COMPLETE
[rank=1 local_rank=1] done
[rank=0 local_rank=0] done
```

---

### 评论 #2 — madisondigitalservice-gif (2026-03-28T22:44:18Z)

OK, I have been on this quest with rocm 7.2 and torch 2.11 for several weeks. Tried vllm, sglang. Deepspeed and others. The underlying issue is the complex PagedAttention and continuous batching create high communication overhead that ROCm's consumer GPU drivers handle poorly. They were never made for that.

Need to take the TCP/IP versus Class of Service networking perspective.

The only way you will find peace of mind and very good performance is with llama.CPP . I run 3-5 multiple GPUs of 7900 xtx. I run AMD Pro 9700 as well before in similar configurations. 

The only way you can get stability and any real inference performance is with that engine. I do use rocm runtime versus vulkan. They are about the same as a performance experience.

My firm and I are AMD advocates.

Believe me when I say we spent hours trying to overcome the the issues of Tensor Parallelism Instability: Users report that vLLM fails with tensor-parallel-size values like 2, 4, or 6 on ROCm, even when 1 or 8 GPUs work.  This is due to unreliable NCCL/RoCCL communication and lack of robust P2P (peer-to-peer) memory access between consumer Radeon cards, causing hangs and assertion errors. 

Try to run a query and get a decent response ...will not happen. Maybe never returns and you need to kill the http server. 

That is because this comm was made for data center networking not PCI bus or oculink. We found the llama.CPP will deliver good performance as I can run 32B qwen models on our GPU clusters of Radeon 7900 xtx cards. Our AI agents that access this edge solution have no issues. Coding, agents, and inference all running at the edge. All with a extremely lower TCO.

The Radeon cards are indeed awesome, but some of the AI related software being used or even promoted with them is not viable in many cases. I finished writing about this on x today on the very subject. Until the software matches the use case and their is true support for edge deployment, and AMD , you will be in this endless hype and doom loop. Llama.CPP and don't look back.

---

### 评论 #3 — msembinelli (2026-03-29T16:46:30Z)

Thanks for the response @madisondigitalservice-gif 

Totally hear you on that. I feel like I'm getting close to something that is usable though, a simple downgrade to rocm 7.2 seems to get past this point fine.

Having much better results with these vllm serve params, vllm nightly `0.18.1rc1.dev218+gfafca38ad`

```
docker run -d --rm \
  --name "${CONTAINER}" \
  --group-add=video \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --device /dev/kfd \
  --device /dev/dri \
  -v "${HF_CACHE_HOST}:/root/.cache/huggingface" \
  --env "HF_TOKEN=${HF_TOKEN:-}" \
  --env "GCN_ARCH_NAME=gfx1100" \
  --env "HSA_ENABLE_IPC_MODE_LEGACY=0" \
  --env PYTORCH_ALLOC_CONF=graph_capture_record_stream_reuse:True,expandable_segments:True \
  -p "${HOST_PORT}:8000" \
  --ipc=host \
  "${IMAGE}" \
  --model "cyankiwi/Qwen3.5-27B-AWQ-BF16-INT4" \
  --dtype float16 \
  --tensor-parallel-size 2 \
  --max-model-len 65536 \
  --max-num-seqs 8 \
  --block-size 32 \
  --max-num-batched-tokens 2048 \
  --gpu-memory-utilization 0.90 \
  --attention-backend TRITON_ATTN \
  --enable-prefix-caching \
  --enable-prompt-tokens-details \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3 \
  --chat-template-content-format string \
  --language-model-only \
  --mamba-cache-mode align \
  --quantization compressed-tensors \
```

---

### 评论 #4 — JartX (2026-03-30T22:50:14Z)

Hi guys, same bug here
https://github.com/vllm-project/vllm/issues/38587

---

### 评论 #5 — JartX (2026-03-31T16:24:23Z)

Hi @msembinelli can you check it ?

I'm using the 7.2.1 commit here; I’d say the problem lies with the amdclang compiler because if use the amdclang of 7.2.0 to build the code of rccl 7.2.1 works for me, but if use the amdclang of 7.2.1 same problem.

`wget "[https://repo.radeon.com/rocm/apt/7.2/pool/main/r/rocm-llvm/rocm-llvm_22.0.0.26014.70200-43~22.04_amd64.deb](https://repo.radeon.com/rocm/apt/7.2/pool/main/r/rocm-llvm/rocm-llvm_22.0.0.26014.70200-43~22.04_amd64.deb)" -O /tmp/llvm720.deb && mkdir -p /tmp/llvm720 && dpkg -x /tmp/llvm720.deb /tmp/llvm720 && git clone --branch rocm-7.2.1 --depth 1 [https://github.com/ROCm/rccl.git](https://github.com/ROCm/rccl.git) /tmp/rccl && cd /tmp/rccl && CXX=/tmp/llvm720/opt/rocm-7.2.0/llvm/bin/amdclang++ CC=/tmp/llvm720/opt/rocm-7.2.0/llvm/bin/amdclang CXXFLAGS="--rocm-path=/opt/rocm" CFLAGS="--rocm-path=/opt/rocm" ./install.sh --amdgpu_targets "gfx1100" && rm -f /opt/rocm/lib/librccl.so.1.0* /opt/rocm/lib/librccl.so.1 /opt/rocm/lib/librccl.so && cp /tmp/rccl/build/release/librccl.so.1.0 /opt/rocm/lib/librccl.so.1.0 && ln -sf librccl.so.1.0 /opt/rocm/lib/librccl.so.1 && ln -sf librccl.so.1 /opt/rocm/lib/librccl.so && ln -sf /opt/rocm/lib/librccl.so.1.0 /opt/rocm-7.2.1/lib/librccl.so.1.0.70201 && ldconfig && rm -rf /tmp/llvm720.deb /tmp/llvm720 /tmp/rccl`

---

### 评论 #6 — JartX (2026-03-31T16:27:54Z)

@msembinelli 

My DockerFile for gfx1100
```
ARG REMOTE_VLLM="0"
ARG COMMON_WORKDIR=/app
ARG BASE_IMAGE=rocm/vllm-dev:base_custom_rocm_7.2.1_torch_triton_0330_vllm018

ARG USE_SCCACHE
ARG SCCACHE_DOWNLOAD_URL
ARG SCCACHE_ENDPOINT
ARG SCCACHE_BUCKET_NAME=vllm-build-sccache
ARG SCCACHE_REGION_NAME=us-west-2
ARG SCCACHE_S3_NO_CREDENTIALS=0

FROM ${BASE_IMAGE} AS base

ARG ARG_PYTORCH_ROCM_ARCH
ENV PYTORCH_ROCM_ARCH=${ARG_PYTORCH_ROCM_ARCH:-${PYTORCH_ROCM_ARCH}}
ENV RAY_EXPERIMENTAL_NOSET_ROCR_VISIBLE_DEVICES=1
ENV RAY_EXPERIMENTAL_NOSET_HIP_VISIBLE_DEVICES=1
ENV PYTORCH_ROCM_ARCH="gfx1100"
RUN apt-get update -q -y && apt-get install -q -y \
    sqlite3 libsqlite3-dev libfmt-dev libmsgpack-dev libsuitesparse-dev \
    apt-transport-https ca-certificates wget curl git
RUN python3 -m pip install --upgrade pip

ARG USE_SCCACHE
RUN if [ "$USE_SCCACHE" != "1" ]; then \
        apt-get purge -y sccache || true; \
        python3 -m pip uninstall -y sccache || true; \
        rm -f "$(which sccache)" || true; \
    fi

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

ENV UV_HTTP_TIMEOUT=500
ENV UV_INDEX_STRATEGY="unsafe-best-match"
ENV UV_LINK_MODE=copy

ARG USE_SCCACHE
ARG SCCACHE_DOWNLOAD_URL
ARG SCCACHE_ENDPOINT
ARG SCCACHE_BUCKET_NAME
ARG SCCACHE_REGION_NAME
ARG SCCACHE_S3_NO_CREDENTIALS
RUN if [ "$USE_SCCACHE" = "1" ]; then \
        if command -v sccache >/dev/null 2>&1; then \
            echo "sccache already installed, skipping installation"; \
            sccache --version; \
        else \
            echo "Installing sccache..." \
            && SCCACHE_ARCH="x86_64" \
            && SCCACHE_VERSION="v0.8.1" \
            && SCCACHE_DL_URL="${SCCACHE_DOWNLOAD_URL:-https://github.com/mozilla/sccache/releases/download/${SCCACHE_VERSION}/sccache-${SCCACHE_VERSION}-${SCCACHE_ARCH}-unknown-linux-musl.tar.gz}" \
            && curl -L -o /tmp/sccache.tar.gz ${SCCACHE_DL_URL} \
            && tar -xzf /tmp/sccache.tar.gz -C /tmp \
            && mv /tmp/sccache-${SCCACHE_VERSION}-${SCCACHE_ARCH}-unknown-linux-musl/sccache /usr/bin/sccache \
            && chmod +x /usr/bin/sccache \
            && rm -rf /tmp/sccache.tar.gz /tmp/sccache-${SCCACHE_VERSION}-${SCCACHE_ARCH}-unknown-linux-musl \
            && sccache --version; \
        fi; \
    fi

ARG USE_SCCACHE
ENV SCCACHE_BUCKET=${USE_SCCACHE:+${SCCACHE_BUCKET_NAME}}
ENV SCCACHE_REGION=${USE_SCCACHE:+${SCCACHE_REGION_NAME}}
ENV SCCACHE_S3_NO_CREDENTIALS=${USE_SCCACHE:+${SCCACHE_S3_NO_CREDENTIALS}}
ENV SCCACHE_IDLE_TIMEOUT=${USE_SCCACHE:+0}

ENV FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
ENV GPU_AI'm using the 7.2.1 commit here; I’d say the problem lies with the amdclang compiler.RCHS="gfx1100"
RUN git clone --single-branch --branch main_perf https://github.com/ROCm/flash-attention.git \
    && cd flash-attention \
    && python3 setup.py install \
    && cd .. \
    && rm -rf flash-attention

ARG COMMON_WORKDIR
WORKDIR ${COMMON_WORKDIR}

# Build RCCL 7.2.1 with ROCm 7.2.0 compiler (7.2.1 compiler generates broken code for gfx1100)
FROM base AS build_rccl
RUN wget "https://repo.radeon.com/rocm/apt/7.2/pool/main/r/rocm-llvm/rocm-llvm_22.0.0.26014.70200-43~22.04_amd64.deb" -O /tmp/llvm720.deb \
    && mkdir -p /tmp/llvm720 && dpkg -x /tmp/llvm720.deb /tmp/llvm720 \
    && git clone --branch rocm-7.2.1 --depth 1 https://github.com/ROCm/rccl.git /tmp/rccl \
    && cd /tmp/rccl \
    && CXX=/tmp/llvm720/opt/rocm-7.2.0/llvm/bin/amdclang++ \
       CC=/tmp/llvm720/opt/rocm-7.2.0/llvm/bin/amdclang \
       CXXFLAGS="--rocm-path=/opt/rocm" \
       CFLAGS="--rocm-path=/opt/rocm" \
       ./install.sh --amdgpu_targets "gfx1100" \
    && rm -rf /tmp/llvm720.deb /tmp/llvm720

FROM base AS fetch_vllm_0
ONBUILD COPY ./ vllm/
FROM base AS fetch_vllm_1
ARG VLLM_REPO="https://github.com/vllm-project/vllm.git"
ARG VLLM_BRANCH="main"
ENV VLLM_REPO=${VLLM_REPO}
ENV VLLM_BRANCH=${VLLM_BRANCH}
ONBUILD RUN git clone ${VLLM_REPO} \
        && cd vllm \
        && git fetch -v --prune -- origin ${VLLM_BRANCH} \
        && git checkout FETCH_HEAD \
        && if [ ${VLLM_REPO} != "https://github.com/vllm-project/vllm.git" ] ; then \
               git remote add upstream "https://github.com/vllm-project/vllm.git" \
               && git fetch upstream ; fi
FROM fetch_vllm_${REMOTE_VLLM} AS fetch_vllm

FROM fetch_vllm AS build_vllm
RUN cd vllm \
    && python3 -m pip install -r requirements/rocm.txt \
    && python3 setup.py clean --all  \
    && python3 setup.py bdist_wheel --dist-dir=dist
FROM scratch AS export_vllm
ARG COMMON_WORKDIR
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/dist/*.whl /
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/requirements /requirements
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/benchmarks /benchmarks
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/tests /tests
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/examples /examples
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/docker/Dockerfile.rocm /docker/
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/.buildkite /.buildkite
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm/vllm/v1 /vllm_v1

FROM base AS build_rixl
ARG RIXL_BRANCH="f33a5599"
ARG RIXL_REPO="https://github.com/ROCm/RIXL.git"
ARG UCX_BRANCH="da3fac2a"
ARG UCX_REPO="https://github.com/ROCm/ucx.git"
ENV ROCM_PATH=/opt/rocm
ENV UCX_HOME=/usr/local/ucx
ENV RIXL_HOME=/usr/local/rixl
ENV RIXL_BENCH_HOME=/usr/local/rixl_bench

RUN apt-get -y update && apt-get -y install autoconf libtool pkg-config \
    libgrpc-dev \
    libgrpc++-dev \
    libprotobuf-dev \
    protobuf-compiler-grpc \
    libcpprest-dev \
    libaio-dev \
    librdmacm1 \
    librdmacm-dev \
    libibverbs1 \
    libibverbs-dev \
    ibverbs-utils \
    rdmacm-utils \
    ibverbs-providers \
    && rm -rf /var/lib/apt/lists/*

RUN uv pip install --system meson auditwheel patchelf tomlkit

RUN cd /usr/local/src && \
    git clone ${UCX_REPO} &&  \
    cd ucx  && \
    git checkout ${UCX_BRANCH} && \
    ./autogen.sh && \
    mkdir build && cd build && \
    ../configure \
        --prefix=/usr/local/ucx \
        --enable-shared \
        --disable-static \
        --disable-doxygen-doc \
        --enable-optimizations \
        --enable-devel-headers \
        --with-rocm=/opt/rocm \
        --with-verbs \
        --with-dm \
        --enable-mt && \
    make -j && \
    make install

ENV PATH=/usr/local/ucx/bin:$PATH
ENV LD_LIBRARY_PATH=${UCX_HOME}/lib:${LD_LIBRARY_PATH}

RUN git clone ${RIXL_REPO} /opt/rixl && \
    cd /opt/rixl && \
    git checkout ${RIXL_BRANCH} && \
    meson setup build --prefix=${RIXL_HOME} \
                      -Ducx_path=${UCX_HOME} \
                      -Drocm_path=${ROCM_PATH} && \
    cd build && \
    ninja && \
    ninja install

RUN cd /opt/rixl && mkdir -p /app/install && \
    ./contrib/build-wheel.sh \
        --output-dir /app/install \
        --rocm-dir ${ROCM_PATH} \
        --ucx-plugins-dir ${UCX_HOME}/lib/ucx \
        --nixl-plugins-dir ${RIXL_HOME}/lib/x86_64-linux-gnu/plugins


FROM fetch_vllm AS build_vllm_wheel_release

ARG COMMON_WORKDIR

RUN mkdir -p /install

COPY docker/context/base-wheels/ /tmp/base-wheels/
RUN if [ -n "$(ls /tmp/base-wheels/*.whl 2>/dev/null)" ]; then \
        echo "Found custom wheels - copying to /install"; \
        cp /tmp/base-wheels/*.whl /install/ && \
        echo "Copied custom wheels:"; \
        ls -lh /install/; \
    else \
        echo "ERROR: No custom wheels found in docker/context/base-wheels/"; \
        echo "Wheel releases require pre-built ROCm wheels."; \
        exit 1; \
    fi

ARG GIT_REPO_CHECK=0
RUN if [ "$GIT_REPO_CHECK" != "0" ]; then \
        echo "Running repository checks..."; \
        cd vllm && bash tools/check_repo.sh; \
    fi

RUN --mount=type=bind,source=.git,target=vllm/.git \
    cd vllm \
    && pip install setuptools_scm regex \
    && VLLM_VERSION=$(python3 -c "import setuptools_scm; print(setuptools_scm.get_version())") \
    && echo "Detected vLLM version: ${VLLM_VERSION}" \
    && echo "${VLLM_VERSION}" > /tmp/vllm_version.txt

RUN echo "Checking for git-based packages in requirements files..." \
    && echo "Checking common.txt for git-based packages:" \
    && if grep -q 'git+' ${COMMON_WORKDIR}/vllm/requirements/common.txt; then \
         echo "ERROR: Git-based packages found in common.txt:"; \
         grep 'git+' ${COMMON_WORKDIR}/vllm/requirements/common.txt; \
         echo "Please publish these packages to PyPI instead of using git dependencies."; \
         exit 1; \
       else \
         echo "  ✓ No git-based packages found in common.txt"; \
       fi \
    && echo "Checking rocm.txt for git-based packages:" \
    && if grep -q 'git+' ${COMMON_WORKDIR}/vllm/requirements/rocm.txt; then \
         echo "ERROR: Git-based packages found in rocm.txt:"; \
         grep 'git+' ${COMMON_WORKDIR}/vllm/requirements/rocm.txt; \
         echo "Please publish these packages to PyPI instead of using git dependencies."; \
         exit 1; \
       else \
         echo "  ✓ No git-based packages found in rocm.txt"; \
       fi \
    && echo "All requirements files are clean - no git-based packages found"

COPY tools/vllm-rocm/pin_rocm_dependencies.py /tmp/pin_rocm_dependencies.py
RUN echo "Pinning vLLM dependencies to custom wheel versions..." \
    && python3 /tmp/pin_rocm_dependencies.py /install ${COMMON_WORKDIR}/vllm/requirements/rocm.txt

RUN cd vllm \
    && echo "Building vLLM with custom wheels from /install" \
    && python3 -m pip install --find-links /install -r requirements/rocm.txt \
    && python3 setup.py clean --all

RUN --mount=type=bind,source=.git,target=vllm/.git \
    cd vllm \
    && export SETUPTOOLS_SCM_PRETEND_VERSION=$(cat /tmp/vllm_version.txt) \
    && echo "Building wheel with version: ${SETUPTOOLS_SCM_PRETEND_VERSION}" \
    && python3 setup.py bdist_wheel --dist-dir=dist

FROM scratch AS export_vllm_wheel_release
ARG COMMON_WORKDIR
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/dist/*.whl /
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/requirements /requirements
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/benchmarks /benchmarks
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/tests /tests
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/examples /examples
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/docker/Dockerfile.rocm /docker/
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/.buildkite /.buildkite
COPY --from=build_vllm_wheel_release ${COMMON_WORKDIR}/vllm/vllm/v1 /vllm_v1

FROM base AS test

RUN python3 -m pip install --upgrade pip && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,from=export_vllm,src=/,target=/install \
    --mount=type=cache,target=/root/.cache/uv \
    cd /install \
    && uv pip install --system -r requirements/rocm.txt \
    && uv pip install --system -r requirements/rocm-test.txt \
    && pip uninstall -y vllm \
    && uv pip install --system *.whl

RUN --mount=type=bind,from=build_rixl,src=/app/install,target=/rixl_install \
    uv pip install --system /rixl_install/*.whl

WORKDIR /vllm-workspace
ARG COMMON_WORKDIR
COPY --from=build_vllm ${COMMON_WORKDIR}/vllm /vllm-workspace

RUN cd /vllm-workspace \
    && python3 -m pip install -e tests/vllm_test_utils \
    && python3 -m pip install pytest-shard

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system hf_transfer
ENV HF_HUB_ENABLE_HF_TRANSFER=1

COPY tools/install_torchcodec_rocm.sh /tmp/install_torchcodec.sh
RUN bash /tmp/install_torchcodec.sh \
    && rm /tmp/install_torchcodec.sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=export_vllm /vllm_v1 /usr/local/lib/python${PYTHON_VERSION}/dist-packages/vllm/v1

RUN mkdir src && mv vllm src/vllm

FROM base AS final

RUN python3 -m pip install --upgrade pip && rm -rf /var/lib/apt/lists/*

RUN rm -f /usr/bin/sccache || true \
    && rm -rf /opt/sccache-wrappers || true

ENV SCCACHE_BUCKET=
ENV SCCACHE_REGION=
ENV SCCACHE_S3_NO_CREDENTIALS=
ENV SCCACHE_IDLE_TIMEOUT=

RUN case "$(which python3)" in \
        *"/opt/conda/envs/py_3.9"*) \
            rm -rf /opt/conda/envs/py_3.9/lib/python3.9/site-packages/numpy-1.20.3.dist-info/;; \
        *) ;; esac

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --upgrade huggingface-hub[cli]

RUN --mount=type=bind,from=export_vllm,src=/,target=/install \
    --mount=type=cache,target=/root/.cache/uv \
    cd /install \
    && uv pip install --system -r requirements/rocm.txt \
    && pip uninstall -y vllm \
    && uv pip install --system *.whl \
    && python3 -m pip install "vllm[audio]"

ARG COMMON_WORKDIR
ARG BASE_IMAGE

COPY --from=export_vllm /benchmarks ${COMMON_WORKDIR}/vllm/benchmarks
COPY --from=export_vllm /examples ${COMMON_WORKDIR}/vllm/examples
COPY --from=export_vllm /docker ${COMMON_WORKDIR}/vllm/docker

ENV TOKENIZERS_PARALLELISM=false

ENV SAFETENSORS_FAST_GPU=1

ENV HIP_FORCE_DEV_KERNARG=1

RUN echo "ROCTRACER_MAX_EVENTS=10000000" > ${COMMON_WORKDIR}/libkineto.conf
ENV KINETO_CONFIG="${COMMON_WORKDIR}/libkineto.conf"
RUN echo "VLLM_BASE_IMAGE=${BASE_IMAGE}" >> ${COMMON_WORKDIR}/versions.txt

# Replace RCCL 7.2.1 with 7.2.1 compiled using ROCm 7.2.0 compiler
# (7.2.1 amdclang++ generates broken code for gfx1100)
COPY --from=build_rccl /tmp/rccl/build/release/librccl.so.1.0 /opt/rocm/lib/librccl.so.1.0
RUN rm -f /opt/rocm/lib/librccl.so.1 /opt/rocm/lib/librccl.so \
    && ln -sf librccl.so.1.0 /opt/rocm/lib/librccl.so.1 \
    && ln -sf librccl.so.1 /opt/rocm/lib/librccl.so \
    && ln -sf /opt/rocm/lib/librccl.so.1.0 /opt/rocm-7.2.1/lib/librccl.so.1.0.70201 \
    && ldconfig

CMD ["/bin/bash"]

FROM final AS vllm-openai
ENTRYPOINT ["vllm", "serve"]
```

---

### 评论 #7 — msembinelli (2026-03-31T20:03:25Z)

Thank you @JartX , trying this right now, will report back

---

### 评论 #8 — msembinelli (2026-03-31T20:23:08Z)

@JartX I can confirm that your workaround is running smoothly, no more startup issues!

Thank you!!

---

### 评论 #9 — JartX (2026-03-31T20:27:43Z)

@msembinelli We're not finished yet; we still need to see at what point the compiler broke

This has only bought us some time

---

### 评论 #10 — madisondigitalservice-gif (2026-03-31T21:34:13Z)

As your working away I am using three to four models across my latest LM
Studio (lllmster instances | headless) for coding, data analytics, and
general inference. I run these instances in docker containers, each with
their own isolated reference of Radeoon AMD GPU's for the specific
workloads. SOme will have 2-3 mGPU's, some will be a singleton. Our plan
will be to create our applications called rocmWare and rocShare to manage
and instrument this environment.
With the coding model,  we are building our Centurion AI agents. One of
those agent workloads will be using a RoCm native M/L, which we will
dedicate to one of the GPU's ( docker containers/ llmster) in our system.
 Like most now are finding that Radeon GPU's and RocM 7.2, PyTorch 2.11 is
indeed stable for a single card, but never mGPU has it is currently written
mainly for data centers usein that configuration. PFJ

On Tue, Mar 31, 2026 at 3:28 PM JartX ***@***.***> wrote:

> *JartX* left a comment (ROCm/ROCm#6074)
> <https://github.com/ROCm/ROCm/issues/6074#issuecomment-4165305430>
>
> @msembinelli <https://github.com/msembinelli> We're not finished yet; we
> still need to see at what point the compiler broke
>
> This has only bought us some time
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/6074?email_source=notifications&email_token=B5W7BNBAQ5BTD2XGRRN3X234TQS5LA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTIMJWGUZTANJUGMYKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-4165305430>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/B5W7BNHURV3RIKAXZAIJH7L4TQS5LAVCNFSM6AAAAACXDLRZGOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHM2DCNRVGMYDKNBTGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #11 — JartX (2026-03-31T22:03:35Z)

@darren-amd Besides the different versions in the repository, do you have any other suggestions on how we could narrow it down? Thank you so much for your time.

---

### 评论 #12 — darren-amd (2026-04-02T19:19:48Z)

Hi @msembinelli @JartX,

Thanks for reporting the issue and the work on debugging! I got a similar dual-GPU system setup and gave your workload a try inside of the latest [`rocm/vllm-dev:nightly`](https://hub.docker.com/layers/rocm/vllm-dev/nightly/images/sha256-04b8e97fee531a55a38372b698c98f3353f35553571f848c5e31f40427b8bbe3) container and was unable to reproduce the issue:
```
RCCL version : 2.27.7-HEAD:96a25b5
HIP version  : 7.2.53211-e1a6bc5663
ROCm version : 7.2.1.0-81-e1a6bc5663
Librccl path : /opt/rocm/lib/librccl.so.1
Torch version: torch=2.10.0+git8514f05
```
I also tried compiling the tagged 7.2.1 release of RCCL with the 7.2.1 compiler which also passed for me. Would you mind giving that container a try and seeing if the issue persists?

Another thing I wanted to mention if you're interested is that we do have nightly [TheRock](https://github.com/ROCm/TheRock) builds that are available to download [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#torch-for-gfx110x-all), which bundle RCCL built from latest develop.

---

### 评论 #13 — JartX (2026-04-06T10:17:18Z)

Hi @darren-amd 
It keeps failing, and with the latest builds, vllm won't even start, giving the same error. If I compile with the amdclang compiler you see in the Dockerfile, everything works. If I use the one from 7.2.1, it crashes. Did you compile the compiler yourself, or did you download it from the Dockerfile?

Thanks a lot!

---

### 评论 #14 — JartX (2026-04-06T13:45:12Z)

@darren-amd 
Could you please post the image you're using? That way we all have the same code and the tests are more reproducible :)

---

### 评论 #15 — darren-amd (2026-04-06T15:41:59Z)

Hi @JartX,

I gave this a try inside of the: [04-01 nightly](https://hub.docker.com/layers/rocm/vllm-dev/nightly_main_20260401/images/sha256-a2a5187f28bb1d5111ecc6d8ea7e218dff89c4ce1f881bd73af984be6bb029a4). Were you using the latest vllm-dev/nightly from yesterday? I can give it a try inside of that container as well. 

---

### 评论 #16 — JartX (2026-04-06T22:21:25Z)

Yes, that's correct, I tried yesterday's version. And the same thing happens; if I don't compile with the amdclang from 7.2.0, I get the same error. It only happens when compiling with the 7.2.1 version. Hmm, there must be something that changed in the compiler, adding a flag or variable that's breaking the behavior. I'm thinking it could be the one PCIe Gen 4 x16 GPU and another PCIe Gen 4 x4 GPU, but that setup configuration has always worked for me until this version. Could you please change the PCIe bandwidth values on the motherboard? Or force the second GPU to go through the PCH?
Many thanks for your time @darren-amd 

---

### 评论 #17 — JartX (2026-04-06T22:29:38Z)

@darren-amd What kernel version?

---

### 评论 #18 — cjrolo (2026-04-08T15:32:07Z)

Having the exact same issue on gfx1201.

4x R9700 AI PRO. All in PCI 5. Some 16x, some 8x. Always worked until now.

---

### 评论 #19 — darren-amd (2026-04-08T19:32:18Z)

Hi @JartX,

Thanks for giving it a try. I gave all the mentioned configurations a try as well as the container you linked and was unable to reproduce the issue. Lets standardize the container that we try as [04-01 nightly vLLM](https://hub.docker.com/layers/rocm/vllm-dev/nightly_main_20260401/images/sha256-a2a5187f28bb1d5111ecc6d8ea7e218dff89c4ce1f881bd73af984be6bb029a4) just to limit the number of variables. I'm on Ubuntu 22.04 `5.15.0-173-generic`. I'm on the latest amdgpu release available [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#amd-gpu-driver-installation), could you please try uninstalling the older driver and installing this latest one?

Also to clarify, are you saying that the default `/opt/rocm/lib/librccl.so` bundled in the container is reproducing the failure along with 7.2.1 RCCL built with the 7.2.1 compiler from [this link](https://repo.radeon.com/rocm/apt/7.2.1/pool/main/r/rocm-llvm/), but the 7.2.0 compiler works? 

Could you try using a fresh container with the above image and running the reproducer script with `NCCL_DEBUG=INFO` from above and give me the full logs for each of the three librccl versions mentioned above:
```
#!/usr/bin/env python3
import os
import sys
import torch
import torch.distributed as dist


def log(msg: str) -> None:
    rank = int(os.environ.get("RANK", "-1"))
    local_rank = int(os.environ.get("LOCAL_RANK", "-1"))
    print(f"[rank={rank} local_rank={local_rank}] {msg}", flush=True)


def main() -> int:
    print("HIP_VISIBLE_DEVICES =", os.environ.get("HIP_VISIBLE_DEVICES"), flush=True)
    print("ROCR_VISIBLE_DEVICES =", os.environ.get("ROCR_VISIBLE_DEVICES"), flush=True)

    if not torch.cuda.is_available():
        print("torch.cuda.is_available() is False", file=sys.stderr, flush=True)
        return 2

    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])

    log(f"torch={torch.__version__}")
    log(f"cuda/HIP available={torch.cuda.is_available()} device_count={torch.cuda.device_count()}")

    torch.cuda.set_device(local_rank)
    dev = torch.device(f"cuda:{local_rank}")
    props = torch.cuda.get_device_properties(dev)
    log(f"using device {local_rank}: {props.name}")

    dist.init_process_group(
        backend="nccl",
        init_method="env://",
        world_size=world_size,
        rank=rank,
        device_id=dev,
    )
    log("process group initialized")

    x = torch.tensor([rank + 1.0], device=dev, dtype=torch.float32)
    log(f"before barrier: {x.item()}")

    # Fails here on the affected setup
    dist.barrier()
    torch.cuda.synchronize()
    log("barrier passed")

    dist.all_reduce(x, op=dist.ReduceOp.SUM)
    torch.cuda.synchronize()
    log(f"after all_reduce: {x.item()}")

    dist.destroy_process_group()
    log("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Also could you provide me with the output of: 

1. `rocminfo`
2. `rocm_agent_enumerator`
3. 
```
amd-smi
amd-smi topology
amd-smi static --driver
amd-smi firmware
amd-smi xgmi
```
4. `dkms status`
5. `lspci -d ::0300 -vvv 2>&1 | grep -iE "Region|Resize"`

Additionally, could you check your Resizable BAR status and try enabling it?

Thanks!

EDIT: Another thing that may be worth trying is our nightly TheRock wheels available [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#torch-for-gfx1151). These are built nightly and contain the latest RCCL built with our latest compiler.

---

### 评论 #20 — madisondigitalservice-gif (2026-04-09T14:52:48Z)

Most consumer-grade MB's have one x16 (first slot) and another x4 (second slot) — so, dual-GPU setups are indeed possible. The amount of chatter and communication due to vllm's use of RCCL makes it impracticable with the Radeon GPU's as the chattering communication introduces latency and instability if inference tasks run across mGPU's (on the MB's PCI bus). 

That is why llama.cpp works, just a bit slower, much less communication. 

Still useful work can be accomplished with rocm 7.2, and pytorch when using larger models across mGPU's. 

Now if there are two x16 PCI slots available on various "consumer" MBs, I would be very curious if this is better handled on the PCI rails between the mGPU's using vllm ( RCCL). 

Note: Two x16 slots's offer bandwidth distribution (x8/x8) or primary slot priority (x16/x4). 

Why x8/x8 is usually "Best"

For dual-GPU setups, an x8/x8 configuration is almost always superior to x16/x4. This is because:

    Direct CPU Connection: On high-end boards (like those listed below), both x8 slots connect directly to the CPU.
    Latency: An x4 slot is often connected through the chipset (PCH), which adds latency and can bottleneck your second card.
    Minimal Loss: In real-world benchmarks, running a modern GPU at x8 (especially PCIe 4.0 or 5.0) typically results in only a 1–3% performance hit compared to x16.

Options:

ASUS ProArt X870E-CREATOR WIFI
	AMD (AM5)	Dual PCIe 5.0 x8 slots; ideal for creative multi-GPU workloads.
MSI MPG X870E CARBON WIFI
	AMD (AM5)	Reliable lane bifurcation (x8/x8) for the top two slots.
ASUS ROG Maximus Z890 APEX
	Intel (LGA1851)	Extreme overclocking board that supports x8/x8 Gen 5.
ASRock X870E Taichi
	AMD (AM5)	High-end power delivery with native support for dual-slot splitting.

Otherwise: Your heading into Threadripper MB territory and that is expensive for most individuals and small businesses. It will run full x16 slot bandwidth for each GPU. Most ppl can use the consumer level boards to pull of inference or fine tuning even across MGPU's. Just need to set expectations.

---

### 评论 #21 — JartX (2026-04-10T09:30:24Z)

@darren-amd 
I'm creating this comment to add historical information.

**rocminfo**

```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.15
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
Agent 1                  
*******                  
  Name:                    13th Gen Intel(R) Core(TM) i9-13900K
  Uuid:                    CPU-XX                             
  Marketing Name:          13th Gen Intel(R) Core(TM) i9-13900K
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
  Max Clock Freq. (MHz):   5800                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131655876(0x7d8e8c4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131655876(0x7d8e8c4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131655876(0x7d8e8c4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131655876(0x7d8e8c4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-4fe81514950cd6cd               
  Marketing Name:          AMD Radeon RX 7900 XTX             
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
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 632                                
  SDMA engine uCode::      27                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
*******                  
Agent 3                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-4aca8d870a6af8f4               
  Marketing Name:          AMD Radeon RX 7900 XTX             
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
    L2:                      6144(0x1800) KB                    
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   3072                               
  Internal Node ID:        2                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 632                                
  SDMA engine uCode::      27                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
*** Done ***             
```

**amd-smi**
```

+------------------------------------------------------------------------------+
| AMD-SMI 26.2.2+unknown       amdgpu version: Linuxver ROCm version: N/A      |
| VBIOS version: 00070987                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:03:00.0 AMD Radeon RX 7900 XTX | 29 %     93 °C   0           280/327 W |
|   0       0     N/A             N/A | 100 %   51.76            7608/24560 MB |
|-------------------------------------+----------------------------------------|
| 0000:0c:00.0 AMD Radeon RX 7900 XTX | 0 %      43 °C   0            20/327 W |
|   1       1     N/A             N/A | 0 %      0.0 %             30/24560 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|    0     250235  python3.12             7.9 MB    3.8 GB     4.1 GB  N/A     |
|    0     250236  python3.12             7.9 MB    2.6 GB     2.8 GB  N/A     |
|    1     250235  python3.12             7.9 MB    3.8 GB     4.1 GB  N/A     |
|    1     250236  python3.12             7.9 MB    2.6 GB     2.8 GB  N/A     |
+------------------------------------------------------------------------------+
```
**amd-smi topology**

```
ACCESS TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 ENABLED      DISABLED
0000:0c:00.0 DISABLED     ENABLED
WEIGHT TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 0            40
0000:0c:00.0 40           0
HOPS TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 0            2
0000:0c:00.0 2            0
LINK TYPE TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 SELF         PCIE
0000:0c:00.0 PCIE         SELF
NUMA BW TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 N/A          N/A
0000:0c:00.0 N/A          N/A
CACHE COHERANCY TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 SELF         N/A
0000:0c:00.0 N/A          SELF
ATOMICS TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 SELF         N/A
0000:0c:00.0 N/A          SELF
DMA TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 SELF         N/A
0000:0c:00.0 N/A          SELF
BI-DIRECTIONAL TABLE:
             0000:03:00.0 0000:0c:00.0
0000:03:00.0 SELF         N/A
0000:0c:00.0 N/A          SELF


Legend:
  SELF = Current GPU
  ENABLED / DISABLED = Link is enabled or disabled
  N/A = Not supported
  T/F = True / False
  C/NC = Coherant / Non-Coherant io links
  64,32 = 64 bit and 32 bit atomic support
  <BW from>-<BW to>
```

**amd-smi static --driver**

```
GPU: 0
    DRIVER:
        NAME: amdgpu
        VERSION: Linuxversion6.19.11(nixbld@localhost)(gcc(GCC)15.2.0,GNUld(GNUBinutils)2.44)#1-NixOSSMPPREEMPT_DYNAMICThuApr211:25:57UTC2026

GPU: 1
    DRIVER:
        NAME: amdgpu
        VERSION: Linuxversion6.19.11(nixbld@localhost)(gcc(GCC)15.2.0,GNUld(GNUBinutils)2.44)#1-NixOSSMPPREEMPT_DYNAMICThuApr211:25:57UTC2026
```

**amd-smi firmware**

```
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_PFP
            FW_VERSION: 2640
        FW 1:
            FW_ID: CP_ME
            FW_VERSION: 2470
        FW 2:
            FW_ID: CP_MEC1
            FW_VERSION: 2680
        FW 3:
            FW_ID: RLC
            FW_VERSION: 128
        FW 4:
            FW_ID: SDMA0
            FW_VERSION: 27
        FW 5:
            FW_ID: SDMA1
            FW_VERSION: 27
        FW 6:
            FW_ID: VCN
            FW_VERSION: 09.11.80.10
        FW 7:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.31.00.35
        FW 8:
            FW_ID: ASD
            FW_VERSION: 553648393
        FW 9:
            FW_ID: TA_RAS
            FW_VERSION: 1B.00.02.05
        FW 10:
            FW_ID: PM
            FW_VERSION: 00.78.131.00

GPU: 1
    FW_LIST:
        FW 0:
            FW_ID: CP_PFP
            FW_VERSION: 2640
        FW 1:
            FW_ID: CP_ME
            FW_VERSION: 2470
        FW 2:
            FW_ID: CP_MEC1
            FW_VERSION: 2680
        FW 3:
            FW_ID: RLC
            FW_VERSION: 128
        FW 4:
            FW_ID: SDMA0
            FW_VERSION: 27
        FW 5:
            FW_ID: SDMA1
            FW_VERSION: 27
        FW 6:
            FW_ID: VCN
            FW_VERSION: 09.11.80.10
        FW 7:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.31.00.35
        FW 8:
            FW_ID: ASD
            FW_VERSION: 553648393
        FW 9:
            FW_ID: TA_RAS
            FW_VERSION: 1B.00.02.05
        FW 10:
            FW_ID: PM
            FW_VERSION: 00.78.131.00
```

**amd-smi xgmi**

```
LINK METRIC TABLE:
       bdf           bit_rate  max_bandwidth  link_type  GPU0         GPU1
GPU0   0000:03:00.0  65535 Gb/s4294967295 Gb/sN/A
 Read                                                    N/A          N/A
 Write                                                   N/A          N/A
GPU1   0000:0c:00.0  65535 Gb/s4294967295 Gb/sN/A
 Read                                                    N/A          N/A
 Write                                                   N/A          N/A

GPU LINK PORT STATUS:
       bdf           port_num            
GPU0   0000:03:00.0  X  X  X  X  X  X  X  X
GPU1   0000:0c:00.0  X  X  X  X  X  X  X  X

XGMI LINK STATUS:
        bdf            GPU0          GPU1          
GPU0	0000:03:00.0   SELF          N/A
GPU1	0000:0c:00.0   N/A           SELF


Legend:
  SELF = Current GPU
  N/A = Not supported
  U / D / X = Link is Up / Down / Disabled
  Read / Write = GPU Metric Accumulated Read / Write
```

---

### 评论 #22 — msembinelli (2026-04-14T21:59:04Z)

This could also be related: https://github.com/ROCm/ROCm/issues/6148

---

### 评论 #23 — JartX (2026-04-14T23:10:16Z)

hi @darren-amd @msembinelli 

Same problem in the last nightly

https://hub.docker.com/layers/rocm/vllm-dev/nightly/images/sha256-30d01b3b198c7f94f2d62fcd337775593135df5b3cbcf5f58058cf2e7565097e

I can only get inference to work with my Dockerfile

---

### 评论 #24 — big-yellow-duck (2026-04-16T07:56:03Z)

I tested the rock latest pip install method  as of 2026-04-16 on gfx1201 @msembinelli  you can try this dockerfile if it helps
note that you need to update your env vars using `rocm-env.sh` below

```dockerfile
FROM ubuntu:24.04

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -y ca-certificates git cmake build-essential python3-dev pkg-config
  
WORKDIR /app

RUN uv venv .venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# based on the rock releases
#https://github.com/ROCm/TheRock/blob/main/RELEASES.md#torch-for-gfx120x-all
#https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx120x-all

RUN uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx110X-all/ "rocm[libraries,devel]"
RUN uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx110X-all/ torch torchaudio torchvision

# for gfx120x
# RUN uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ "rocm[libraries,devel]"
# RUN uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ torch torchaudio torchvision

# dependency for vllm
RUN uv pip install setuptools_scm


```

# setup env
* in the image create the script called rocm-env.sh this is to fix the rocm libs not linking correctly.

```bash
#!/usr/bin/env bash

# Source this before building or running vLLM on this machine:
#   source ./rocm-env.sh

_rocm_prepend() {
  local var_name="$1"
  local value="$2"
  local current="${!var_name:-}"

  if [[ -z "$value" || ! -e "$value" ]]; then
    return 0
  fi

  case ":$current:" in
    *":$value:"*) ;;
    *)
      if [[ -n "$current" ]]; then
        export "${var_name}=${value}:${current}"
      else
        export "${var_name}=${value}"
      fi
      ;;
  esac
}

_rocm_set_if_exists() {
  local var_name="$1"
  local value="$2"

  if [[ -n "$value" && -e "$value" ]]; then
    export "${var_name}=${value}"
  fi
}

_rocm_first_existing() {
  local candidate

  for candidate in "$@"; do
    if [[ -n "$candidate" && -e "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  return 1
}

_rocm_find_root() {
  local candidate

  if command -v rocm-sdk >/dev/null 2>&1; then
    candidate="$(rocm-sdk path --root 2>/dev/null || true)"
    if [[ -n "$candidate" && -d "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  fi

  for candidate in \
    "${ROCM_ROOT:-}" \
    "${ROCM_PATH:-}" \
    "${ROCM_HOME:-}" \
    /opt/rocm/core-7.13 \
    /opt/rocm/core-7.12 \
    /opt/rocm \
    /opt/rocm-*; do
    if [[ -n "$candidate" && -d "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  return 1
}

_rocm_detect_gpu_arch() {
  local candidate

  if command -v rocm_agent_enumerator >/dev/null 2>&1; then
    while IFS= read -r candidate; do
      if [[ "$candidate" =~ ^gfx[0-9a-z]+$ && "$candidate" != "gfx000" ]]; then
        printf '%s\n' "$candidate"
        return 0
      fi
    done < <(rocm_agent_enumerator 2>/dev/null | sort -u)
  fi

  if command -v rocminfo >/dev/null 2>&1; then
    while IFS= read -r candidate; do
      if [[ "$candidate" =~ ^gfx[0-9][0-9a-z]+$ ]]; then
        printf '%s\n' "$candidate"
        return 0
      fi
    done < <(rocminfo 2>/dev/null | rg -o 'gfx[0-9a-z]+' | sort -u)
  fi

  return 1
}

ROCM_ROOT="$(_rocm_find_root)" || {
  echo "ROCm root not found. Set ROCM_ROOT or install rocm-sdk." >&2
  return 1 2>/dev/null || exit 1
}

if command -v rocm-sdk >/dev/null 2>&1; then
  ROCM_BIN_PATH="$(rocm-sdk path --bin 2>/dev/null || true)"
  ROCM_CMAKE_PATH="$(rocm-sdk path --cmake 2>/dev/null || true)"
else
  ROCM_BIN_PATH=""
  ROCM_CMAKE_PATH=""
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AOTRITON_PATH="${AOTRITON_PATH:-$SCRIPT_DIR/aotriton/build/install_dir}"
ROCM_LIB_DIR="$(_rocm_first_existing "$ROCM_ROOT/lib" "$ROCM_ROOT/lib64" || true)"
ROCM_SYSDEPS_ROOT="$(_rocm_first_existing "$ROCM_ROOT/lib/rocm_sysdeps" "$ROCM_ROOT/lib64/rocm_sysdeps" || true)"
ROCM_SYSDEPS_LIB_DIR="$(_rocm_first_existing "$ROCM_SYSDEPS_ROOT/lib" "$ROCM_SYSDEPS_ROOT/lib64" || true)"
GPU_ARCH_FALLBACK="gfx1201"
GPU_ARCH_DETECTED="$(_rocm_detect_gpu_arch || true)"
GPU_ARCH_DEFAULT="${GPU_ARCH_DETECTED:-$GPU_ARCH_FALLBACK}"
GPU_ARCH_RESOLVED="${GPU_ARCH:-${PYTORCH_ROCM_ARCH:-${HIP_ARCH:-$GPU_ARCH_DEFAULT}}}"

export ROCM_ROOT
export ROCM_HOME="$ROCM_ROOT"
export ROCM_PATH="$ROCM_ROOT"
export HIP_PLATFORM="${HIP_PLATFORM:-amd}"
export HIP_PATH="$ROCM_ROOT"
export HIP_ROOT_DIR="$ROCM_ROOT"
export HSA_PATH="$ROCM_ROOT"
export HIP_INCLUDE_PATH="${HIP_INCLUDE_PATH:-$ROCM_ROOT/include}"
export HIP_LIB_PATH="${HIP_LIB_PATH:-${ROCM_LIB_DIR:-$ROCM_ROOT/lib}}"
export GPU_ARCH="$GPU_ARCH_RESOLVED"
export HIP_ARCH="$GPU_ARCH"
export PYTORCH_ROCM_ARCH="$GPU_ARCH"
export AMD_SERIALIZE_KERNEL="${AMD_SERIALIZE_KERNEL:-3}"
if [[ -n "$ROCM_SYSDEPS_ROOT" ]]; then
  export ROCM_SYSDEPS_ROOT
fi
if [[ -n "$ROCM_SYSDEPS_LIB_DIR" ]]; then
  export LIBDRM_ROOT="$ROCM_SYSDEPS_ROOT"
fi

_rocm_set_if_exists HIP_CLANG_PATH "$ROCM_ROOT/lib/llvm/bin"
_rocm_set_if_exists HIP_DEVICE_LIB_PATH "$ROCM_ROOT/lib/llvm/amdgcn/bitcode"
_rocm_set_if_exists TRITON_HIP_LLD_PATH "$ROCM_ROOT/llvm/bin/ld.lld"
if [[ -z "${TRITON_HIP_LLD_PATH:-}" ]]; then
  _rocm_set_if_exists TRITON_HIP_LLD_PATH "$ROCM_ROOT/lib/llvm/bin/ld.lld"
fi

if [[ -n "${VIRTUAL_ENV:-}" && -d "${VIRTUAL_ENV}/bin" ]]; then
  _rocm_prepend PATH "${VIRTUAL_ENV}/bin"
fi
_rocm_prepend PATH "${ROCM_BIN_PATH:-$ROCM_ROOT/bin}"
_rocm_prepend PATH "$ROCM_SYSDEPS_ROOT/bin"
_rocm_prepend LD_LIBRARY_PATH "$ROCM_LIB_DIR"
_rocm_prepend LD_LIBRARY_PATH "$ROCM_ROOT/lib64"
_rocm_prepend LD_LIBRARY_PATH "$ROCM_SYSDEPS_LIB_DIR"
_rocm_prepend LD_LIBRARY_PATH "$AOTRITON_PATH/lib"
_rocm_prepend LIBRARY_PATH "$ROCM_LIB_DIR"
_rocm_prepend LIBRARY_PATH "$ROCM_ROOT/lib64"
_rocm_prepend LIBRARY_PATH "$ROCM_SYSDEPS_LIB_DIR"
_rocm_prepend CPATH "$ROCM_ROOT/include"
_rocm_prepend CPATH "$ROCM_SYSDEPS_ROOT/include"
_rocm_prepend PKG_CONFIG_PATH "$ROCM_LIB_DIR/pkgconfig"
_rocm_prepend PKG_CONFIG_PATH "$ROCM_SYSDEPS_LIB_DIR/pkgconfig"
_rocm_prepend CMAKE_PREFIX_PATH "$ROCM_ROOT"
if [[ -n "$ROCM_CMAKE_PATH" ]]; then
  _rocm_prepend CMAKE_PREFIX_PATH "$ROCM_CMAKE_PATH"
fi
_rocm_prepend CMAKE_MODULE_PATH "$ROCM_ROOT/lib/cmake/hip"

# ROCm package metadata may reference a Fortran hipsolver shim that is not
# shipped in some container builds. Provide a compatibility symlink so CMake
# package validation can succeed.
if [[ -f "$ROCM_ROOT/lib/libhipsolver.so.1.0" && ! -e "$ROCM_ROOT/lib/libhipsolver_fortran.so.1.0" && ! -L "$ROCM_ROOT/lib/libhipsolver_fortran.so.1.0" ]]; then
  ln -s libhipsolver.so.1.0 "$ROCM_ROOT/lib/libhipsolver_fortran.so.1.0"
fi
if [[ -e "$ROCM_ROOT/lib/libhipsolver_fortran.so.1.0" && ! -e "$ROCM_ROOT/lib/libhipsolver_fortran.so.1" && ! -L "$ROCM_ROOT/lib/libhipsolver_fortran.so.1" ]]; then
  ln -s libhipsolver_fortran.so.1.0 "$ROCM_ROOT/lib/libhipsolver_fortran.so.1"
fi
if [[ -e "$ROCM_ROOT/lib/libhipsolver_fortran.so.1" && ! -e "$ROCM_ROOT/lib/libhipsolver_fortran.so" && ! -L "$ROCM_ROOT/lib/libhipsolver_fortran.so" ]]; then
  ln -s libhipsolver_fortran.so.1 "$ROCM_ROOT/lib/libhipsolver_fortran.so"
fi

cat <<EOF
ROCm runtime environment loaded:
  ROCM_ROOT=$ROCM_ROOT
  ROCM_PATH=$ROCM_PATH
  GPU_ARCH=$GPU_ARCH
  HIP_PLATFORM=$HIP_PLATFORM
  HIP_PATH=$HIP_PATH
  HIP_ARCH=$HIP_ARCH
  PYTORCH_ROCM_ARCH=$PYTORCH_ROCM_ARCH
  HIP_CLANG_PATH=${HIP_CLANG_PATH:-<not found>}
  HIP_DEVICE_LIB_PATH=${HIP_DEVICE_LIB_PATH:-<not found>}
  TRITON_HIP_LLD_PATH=${TRITON_HIP_LLD_PATH:-<not found>}
  ROCM_SYSDEPS_ROOT=${ROCM_SYSDEPS_ROOT:-<not found>}
  LIBDRM_ROOT=${LIBDRM_ROOT:-<not found>}
  LD_LIBRARY_PATH=$LD_LIBRARY_PATH

Set GPU arch before sourcing if you want to override auto-detection, for example:
  export GPU_ARCH=gfx1201
  source ./rocm-env.sh

Arch selection order:
  GPU_ARCH -> PYTORCH_ROCM_ARCH -> HIP_ARCH -> detected arch -> $GPU_ARCH_FALLBACK

Leave HIP_VISIBLE_DEVICES/ROCR_VISIBLE_DEVICES/CUDA_VISIBLE_DEVICES unset
unless you specifically need to mask GPUs. On this stack, forcing them to "0"
can make torch.cuda.device_count() report 0 even when the HIP runtime sees 1.
EOF
```


```bash
# for gfx1100 
EXPORT GPU_ARCH=gfx1100
source rocm-env.sh
```
 `rccl_smoke.py` mentioned above works.
## Output
```
ROCm runtime environment loaded:
  ROCM_ROOT=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel
  ROCM_PATH=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel
  GPU_ARCH=gfx1201
  HIP_PLATFORM=amd
  HIP_PATH=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel
  HIP_ARCH=gfx1201
  PYTORCH_ROCM_ARCH=gfx1201
  HIP_CLANG_PATH=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel/lib/llvm/bin
  HIP_DEVICE_LIB_PATH=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel/lib/llvm/amdgcn/bitcode
  TRITON_HIP_LLD_PATH=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel/llvm/bin/ld.lld
  ROCM_SYSDEPS_ROOT=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel/lib/rocm_sysdeps
  LIBDRM_ROOT=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel/lib/rocm_sysdeps
  LD_LIBRARY_PATH=/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel/lib/rocm_sysdeps/lib:/app/.venv/lib/python3.12/site-packages/_rocm_sdk_devel/lib

Set GPU arch before sourcing if you want to override auto-detection, for example:
  export GPU_ARCH=gfx1201
  source ./rocm-env.sh

Arch selection order:
  GPU_ARCH -> PYTORCH_ROCM_ARCH -> HIP_ARCH -> detected arch -> gfx1201

Leave HIP_VISIBLE_DEVICES/ROCR_VISIBLE_DEVICES/CUDA_VISIBLE_DEVICES unset
unless you specifically need to mask GPUs. On this stack, forcing them to "0"
can make torch.cuda.device_count() report 0 even when the HIP runtime sees 1.
W0416 07:48:22.387000 63536 torch/distributed/run.py:851] 
W0416 07:48:22.387000 63536 torch/distributed/run.py:851] *****************************************
W0416 07:48:22.387000 63536 torch/distributed/run.py:851] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
W0416 07:48:22.387000 63536 torch/distributed/run.py:851] *****************************************
HIP_VISIBLE_DEVICES = 0,1
ROCR_VISIBLE_DEVICES = None
[rank=0 local_rank=0] torch=2.11.0+rocm7.13.0a20260415
[rank=0 local_rank=0] cuda/HIP available=True device_count=2
[rank=0 local_rank=0] using device 0: AMD Radeon AI PRO R9700
intelbro:63720:63720 [0] NCCL INFO Kernel version: 6.18.16-200.fc43.x86_64

[2026-04-16 07:48:24] intelbro:63720:63720 [0] /home/runner/_work/TheRock/TheRock/output/build/comm-libs/rccl/build/hipify/src/init.cc:283 NCCL WARN Missing "iommu=pt" from kernel command line which can lead to system instablity or hang!
intelbro:63720:63720 [0] NCCL INFO Hipruntime version: 71361040, firmware version: 0
intelbro:63720:63720 [0] NCCL INFO ROCr version 1.21
intelbro:63720:63720 [0] NCCL INFO Kernel version 6.18
intelbro:63720:63720 [0] NCCL INFO NCCL_DMABUF_ENABLE set by environment to 1.
intelbro:63720:63720 [0] NCCL INFO Skipping /proc/config.gz (zcat available, file not found)
intelbro:63720:63720 [0] NCCL INFO Could not open kernel conf file, trying /proc/kallsyms fallback
intelbro:63720:63720 [0] NCCL INFO DMA_BUF Support Enabled via /proc/kallsyms (dma_buf_move_notify + pci_p2pdma)
intelbro:63720:63720 [0] NCCL INFO Kernel version: 6.18.16-200.fc43.x86_64

[2026-04-16 07:48:24] intelbro:63720:63720 [0] /home/runner/_work/TheRock/TheRock/output/build/comm-libs/rccl/build/hipify/src/init.cc:283 NCCL WARN Missing "iommu=pt" from kernel command line which can lead to system instablity or hang!
intelbro:63720:63720 [0] NCCL INFO RCCL version : 2.28.3-HEAD:8017ffe+
HIP version  : 7.13.61040-8017ffed34
ROCm version : 7.13.0.0-9999-8017ffed34
Hostname     : intelbro
Librccl path : /app/.venv/lib/python3.12/site-packages/_rocm_sdk_libraries_gfx120X_all/lib/librccl.so.1
intelbro:63720:63720 [0] NCCL INFO Comm config Blocking set to 1
HIP_VISIBLE_DEVICES = 0,1
ROCR_VISIBLE_DEVICES = None
[rank=1 local_rank=1] torch=2.11.0+rocm7.13.0a20260415
[rank=1 local_rank=1] cuda/HIP available=True device_count=2
[rank=1 local_rank=1] using device 1: AMD Radeon AI PRO R9700
intelbro:63721:63721 [1] NCCL INFO ROCr version 1.21
intelbro:63721:63721 [1] NCCL INFO Kernel version 6.18
intelbro:63721:63721 [1] NCCL INFO NCCL_DMABUF_ENABLE set by environment to 1.
intelbro:63721:63721 [1] NCCL INFO Skipping /proc/config.gz (zcat available, file not found)
intelbro:63721:63721 [1] NCCL INFO Could not open kernel conf file, trying /proc/kallsyms fallback
intelbro:63721:63721 [1] NCCL INFO DMA_BUF Support Enabled via /proc/kallsyms (dma_buf_move_notify + pci_p2pdma)
intelbro:63721:63721 [1] NCCL INFO Kernel version: 6.18.16-200.fc43.x86_64

[2026-04-16 07:48:24] intelbro:63721:63721 [1] /home/runner/_work/TheRock/TheRock/output/build/comm-libs/rccl/build/hipify/src/init.cc:283 NCCL WARN Missing "iommu=pt" from kernel command line which can lead to system instablity or hang!
intelbro:63721:63721 [1] NCCL INFO Hipruntime version: 71361040, firmware version: 0
intelbro:63721:63721 [1] NCCL INFO RCCL version : 2.28.3-HEAD:8017ffe+
HIP version  : 7.13.61040-8017ffed34
ROCm version : 7.13.0.0-9999-8017ffed34
Hostname     : intelbro
Librccl path : /app/.venv/lib/python3.12/site-packages/_rocm_sdk_libraries_gfx120X_all/lib/librccl.so.1
intelbro:63721:63721 [1] NCCL INFO Comm config Blocking set to 1
intelbro:63720:63720 [0] NCCL INFO RCCL: Detected 0 IB devices, primary type: 0 (count: 0)
intelbro:63720:63720 [0] NCCL INFO NET/Plugin: Could not find: librccl-net.so
intelbro:63720:63720 [0] NCCL INFO Failed to open libibverbs.so[.1]
intelbro:63720:63720 [0] NCCL INFO Failed to initialize NET plugin IB
intelbro:63720:63720 [0] NCCL INFO NET/Socket : Using [0]eno2:192.168.50.137<0> [1]tun0:192.168.224.182<0> [2]tun1:192.168.222.170<0>
intelbro:63720:63720 [0] NCCL INFO Initialized NET plugin Socket
intelbro:63720:63720 [0] NCCL INFO Assigned NET plugin Socket to comm
intelbro:63720:63720 [0] NCCL INFO Using network Socket
intelbro:63720:63720 [0] NCCL INFO [node_id = 1; gpu_id = 41977; unique_id = 14101013936730803355; location_id = 21504; bdf = 21504; domain = 0; partition = 0], 
intelbro:63720:63720 [0] NCCL INFO [node_id = 2; gpu_id = 55651; unique_id = 16576701947199271179; location_id = 29184; bdf = 29184; domain = 0; partition = 0], 
intelbro:63720:63720 [0] NCCL INFO initialized internal alternative rsmi functionality
intelbro:63720:63720 [0] NCCL INFO ncclCommInitRankConfig_impl comm 0x3befb570 rank 0 nranks 2 cudaDev 0 nvmlDev 0 busId 54000 commId 0xa362a61828935194 - Init START
intelbro:63721:63721 [1] NCCL INFO RCCL: Detected 0 IB devices, primary type: 0 (count: 0)
intelbro:63721:63721 [1] NCCL INFO NET/Plugin: Could not find: librccl-net.so
intelbro:63721:63721 [1] NCCL INFO Failed to open libibverbs.so[.1]
intelbro:63721:63721 [1] NCCL INFO Failed to initialize NET plugin IB
intelbro:63721:63721 [1] NCCL INFO NET/Socket : Using [0]eno2:192.168.50.137<0> [1]tun0:192.168.224.182<0> [2]tun1:192.168.222.170<0>
intelbro:63721:63721 [1] NCCL INFO Initialized NET plugin Socket
intelbro:63721:63721 [1] NCCL INFO Assigned NET plugin Socket to comm
intelbro:63721:63721 [1] NCCL INFO Using network Socket
intelbro:63721:63721 [1] NCCL INFO [node_id = 1; gpu_id = 41977; unique_id = 14101013936730803355; location_id = 21504; bdf = 21504; domain = 0; partition = 0], 
intelbro:63721:63721 [1] NCCL INFO [node_id = 2; gpu_id = 55651; unique_id = 16576701947199271179; location_id = 29184; bdf = 29184; domain = 0; partition = 0], 
intelbro:63721:63721 [1] NCCL INFO initialized internal alternative rsmi functionality
intelbro:63721:63721 [1] NCCL INFO ncclCommInitRankConfig_impl comm 0x42d42620 rank 1 nranks 2 cudaDev 1 nvmlDev 1 busId 72000 commId 0xa362a61828935194 - Init START
intelbro:63721:63721 [1] NCCL INFO RAS client listening socket at ::1<28028>
intelbro:63720:63720 [0] NCCL INFO RAS client listening socket at ::1<28028>
intelbro:63721:63721 [1] NCCL INFO UALoE fabric detection skipped: RCCL_USE_AMD_SMI_LIB not set
intelbro:63720:63720 [0] NCCL INFO UALoE fabric detection skipped: RCCL_USE_AMD_SMI_LIB not set
intelbro:63721:63721 [1] NCCL INFO NCCL_P2P_DISABLE set by environment to 1
intelbro:63720:63720 [0] NCCL INFO NCCL_P2P_DISABLE set by environment to 1
intelbro:63721:63721 [1] NCCL INFO TOPO/NET : Importing network plugins to topology
intelbro:63720:63720 [0] NCCL INFO TOPO/NET : Importing network plugins to topology
intelbro:63720:63720 [0] NCCL INFO ncclTopoPopulateNics : Filled eno2 in topo with pciPath=/sys/devices/pci0000:00/0000:00:1c.7/0000:06:00.0 keep=1 coll=(null)
intelbro:63721:63721 [1] NCCL INFO ncclTopoPopulateNics : Filled eno2 in topo with pciPath=/sys/devices/pci0000:00/0000:00:1c.7/0000:06:00.0 keep=1 coll=(null)
intelbro:63720:63720 [0] NCCL INFO ncclTopoPopulateNics : Filled tun0 in topo with pciPath=(null) keep=1 coll=(null)
intelbro:63721:63721 [1] NCCL INFO ncclTopoPopulateNics : Filled tun0 in topo with pciPath=(null) keep=1 coll=(null)
intelbro:63720:63720 [0] NCCL INFO ncclTopoPopulateNics : Filled tun1 in topo with pciPath=(null) keep=1 coll=(null)
intelbro:63721:63721 [1] NCCL INFO ncclTopoPopulateNics : Filled tun1 in topo with pciPath=(null) keep=1 coll=(null)
intelbro:63721:63721 [1] NCCL INFO Tuning index set to: 7
intelbro:63721:63721 [1] NCCL INFO === System : maxBw 48.0 totalBw 48.0 ===
intelbro:63721:63721 [1] NCCL INFO CPU/0-0 (1/1/3)
intelbro:63721:63721 [1] NCCL INFO + PCI[5000.0] - NIC/0-0
intelbro:63721:63721 [1] NCCL INFO + PCI[48.0] - PCI/0-52000 (10021478148c1478)
intelbro:63721:63721 [1] NCCL INFO               + PCI[48.0] - GPU/0-54000 (0)
intelbro:63721:63721 [1] NCCL INFO + PCI[48.0] - PCI/0-70000 (10021478148c1478)
intelbro:63721:63721 [1] NCCL INFO               + PCI[48.0] - GPU/0-72000 (1)
intelbro:63721:63721 [1] NCCL INFO + PCI[0.4] - NIC/0-6000
intelbro:63721:63721 [1] NCCL INFO ==========================================
intelbro:63721:63721 [1] NCCL INFO GPU/0-54000 :GPU/0-54000 (0/5000.0/LOC) GPU/0-72000 (4/48.0/PHB) CPU/0-0 (2/48.0/PHB) 
intelbro:63721:63721 [1] NCCL INFO GPU/0-72000 :GPU/0-54000 (4/48.0/PHB) GPU/0-72000 (0/5000.0/LOC) CPU/0-0 (2/48.0/PHB) 
intelbro:63721:63721 [1] NCCL INFO ncclTopoGetCpuAffinity: Affinity for GPU 1 is 0-63. (GPU affinity = 0-63 ; CPU affinity = 0-63).
intelbro:63721:63721 [1] NCCL INFO Pattern 4, crossNic 0, nChannels 2, bw 20.000000/20.000000, type PHB/PIX, sameChannels 1
intelbro:63721:63721 [1] NCCL INFO  0 : GPU/0-54000 GPU/0-72000
intelbro:63721:63721 [1] NCCL INFO  1 : GPU/0-54000 GPU/0-72000
intelbro:63721:63721 [1] NCCL INFO Pattern 1, crossNic 0, nChannels 2, bw 24.000000/24.000000, type PHB/PIX, sameChannels 0
intelbro:63721:63721 [1] NCCL INFO  0 : GPU/0-54000 GPU/0-72000
intelbro:63721:63721 [1] NCCL INFO  1 : GPU/0-72000 GPU/0-54000
intelbro:63721:63721 [1] NCCL INFO GFX9 cheap fence is OFF
intelbro:63720:63720 [0] NCCL INFO Tuning index set to: 7
intelbro:63720:63720 [0] NCCL INFO === System : maxBw 48.0 totalBw 48.0 ===
intelbro:63720:63720 [0] NCCL INFO CPU/0-0 (1/1/3)
intelbro:63720:63720 [0] NCCL INFO + PCI[5000.0] - NIC/0-0
intelbro:63720:63720 [0] NCCL INFO + PCI[48.0] - PCI/0-52000 (10021478148c1478)
intelbro:63720:63720 [0] NCCL INFO               + PCI[48.0] - GPU/0-54000 (0)
intelbro:63720:63720 [0] NCCL INFO + PCI[48.0] - PCI/0-70000 (10021478148c1478)
intelbro:63720:63720 [0] NCCL INFO               + PCI[48.0] - GPU/0-72000 (1)
intelbro:63720:63720 [0] NCCL INFO + PCI[0.4] - NIC/0-6000
intelbro:63720:63720 [0] NCCL INFO ==========================================
intelbro:63720:63720 [0] NCCL INFO GPU/0-54000 :GPU/0-54000 (0/5000.0/LOC) GPU/0-72000 (4/48.0/PHB) CPU/0-0 (2/48.0/PHB) 
intelbro:63720:63720 [0] NCCL INFO GPU/0-72000 :GPU/0-54000 (4/48.0/PHB) GPU/0-72000 (0/5000.0/LOC) CPU/0-0 (2/48.0/PHB) 
intelbro:63720:63720 [0] NCCL INFO ncclTopoGetCpuAffinity: Affinity for GPU 0 is 0-63. (GPU affinity = 0-63 ; CPU affinity = 0-63).
intelbro:63720:63720 [0] NCCL INFO Pattern 4, crossNic 0, nChannels 2, bw 20.000000/20.000000, type PHB/PIX, sameChannels 1
intelbro:63720:63720 [0] NCCL INFO  0 : GPU/0-54000 GPU/0-72000
intelbro:63720:63720 [0] NCCL INFO  1 : GPU/0-54000 GPU/0-72000
intelbro:63720:63720 [0] NCCL INFO Pattern 1, crossNic 0, nChannels 2, bw 24.000000/24.000000, type PHB/PIX, sameChannels 0
intelbro:63720:63720 [0] NCCL INFO  0 : GPU/0-54000 GPU/0-72000
intelbro:63720:63720 [0] NCCL INFO  1 : GPU/0-72000 GPU/0-54000
intelbro:63720:63720 [0] NCCL INFO GFX9 cheap fence is OFF
intelbro:63721:63721 [1] NCCL INFO comm 0x42d42620 rank 1 nRanks 2 nNodes 1 localRanks 2 localRank 1 MNNVL 0
intelbro:63720:63720 [0] NCCL INFO comm 0x3befb570 rank 0 nRanks 2 nNodes 1 localRanks 2 localRank 0 MNNVL 0
intelbro:63721:63721 [1] NCCL INFO Tree 0 : 0 -> 1 -> -1/-1/-1
intelbro:63720:63720 [0] NCCL INFO [RINGS]      00     01
intelbro:63721:63721 [1] NCCL INFO Tree 2 : 0 -> 1 -> -1/-1/-1
intelbro:63720:63720 [0] NCCL INFO [RINGS]  00->01 00->01
intelbro:63721:63721 [1] NCCL INFO Tree 1 : -1 -> 1 -> 0/-1/-1
intelbro:63720:63720 [0] NCCL INFO Tree 0 : -1 -> 0 -> 1/-1/-1
intelbro:63721:63721 [1] NCCL INFO Tree 3 : -1 -> 1 -> 0/-1/-1
intelbro:63720:63720 [0] NCCL INFO Tree 2 : -1 -> 0 -> 1/-1/-1
intelbro:63721:63721 [1] NCCL INFO NCCL_MAX_NCHANNELS set by environment to 1.
intelbro:63720:63720 [0] NCCL INFO Tree 1 : 1 -> 0 -> -1/-1/-1
intelbro:63721:63721 [1] NCCL INFO NCCL_MIN_NCHANNELS set by environment to 1.
intelbro:63720:63720 [0] NCCL INFO Tree 3 : 1 -> 0 -> -1/-1/-1
intelbro:63721:63721 [1] NCCL INFO Ring 0 : 0 -> 1 -> 0 comm 0x42d42620 nRanks 02 busId 72000
intelbro:63720:63720 [0] NCCL INFO NCCL_MAX_NCHANNELS set by environment to 1.
intelbro:63721:63721 [1] NCCL INFO Trees [0] -1/-1/-1->1->0 comm 0x42d42620 nRanks 02 busId 72000
intelbro:63720:63720 [0] NCCL INFO NCCL_MIN_NCHANNELS set by environment to 1.
intelbro:63720:63720 [0] NCCL INFO Channel 00/01 : 0 1
intelbro:63721:63721 [1] NCCL INFO P2P Chunksize set to 131072
intelbro:63720:63720 [0] NCCL INFO Ring 0 : 1 -> 0 -> 1 comm 0x3befb570 nRanks 02 busId 54000
intelbro:63720:63720 [0] NCCL INFO Trees [0] 1/-1/-1->0->-1 comm 0x3befb570 nRanks 02 busId 54000
intelbro:63720:63720 [0] NCCL INFO P2P Chunksize set to 131072
intelbro:63721:63721 [1] NCCL INFO PROFILER/Plugin: Could not find: librccl-profiler.so
intelbro:63720:63720 [0] NCCL INFO PROFILER/Plugin: Could not find: librccl-profiler.so
intelbro:63720:63720 [0] NCCL INFO Check P2P Type isAllDirectP2p 0 directMode 0
intelbro:63721:63766 [0] NCCL INFO [Proxy Service] Device 1 CPU core 27
intelbro:63720:63768 [0] NCCL INFO [Proxy Service] Device 0 CPU core 62
intelbro:63721:63767 [0] NCCL INFO [Proxy Service UDS] Device 1 CPU core 29
intelbro:63720:63769 [0] NCCL INFO [Proxy Service UDS] Device 0 CPU core 0
intelbro:63720:63720 [0] NCCL INFO Channel 00 : 0[54000] -> 1[72000] via SHM/direct/direct comm 0x3befb570 nRanks 02
intelbro:63721:63721 [1] NCCL INFO Channel 00 : 1[72000] -> 0[54000] via SHM/direct/direct comm 0x42d42620 nRanks 02
intelbro:63721:63721 [1] NCCL INFO Connected all rings, use ring PXN 0 GDR 1
intelbro:63720:63720 [0] NCCL INFO Connected all rings, use ring PXN 0 GDR 1
intelbro:63721:63721 [1] NCCL INFO Connected all trees
intelbro:63720:63720 [0] NCCL INFO Connected all trees
intelbro:63720:63770 [0] NCCL INFO [Proxy Progress] Device 0 CPU core 35
intelbro:63720:63720 [0] NCCL INFO TUNER/Plugin: Could not find: libnccl-tuner.so. Using internal tuner plugin.
intelbro:63720:63720 [0] NCCL INFO RCCL Tuning index:7
intelbro:63720:63720 [0] NCCL INFO threadThresholds 8/8/64 | 16/8/64 | 256 | 256
intelbro:63720:63720 [0] NCCL INFO comm:0x3befb570, nRanks:2, nNodes:1, coll channels:1 collnet channels:1, nvls channels:0, p2p channels:8, p2p channels per peer:8, shiftSize:-1
intelbro:63720:63720 [0] NCCL INFO CC Off, workFifoBytes 4194304
intelbro:63721:63771 [0] NCCL INFO [Proxy Progress] Device 1 CPU core 36
intelbro:63721:63721 [1] NCCL INFO TUNER/Plugin: Could not find: libnccl-tuner.so. Using internal tuner plugin.
intelbro:63721:63721 [1] NCCL INFO RCCL Tuning index:7
intelbro:63721:63721 [1] NCCL INFO threadThresholds 8/8/64 | 16/8/64 | 256 | 256
intelbro:63721:63721 [1] NCCL INFO comm:0x42d42620, nRanks:2, nNodes:1, coll channels:1 collnet channels:1, nvls channels:0, p2p channels:8, p2p channels per peer:8, shiftSize:-1
intelbro:63720:63720 [0] NCCL INFO RCCL Unroll Factor (pre-set): 4
intelbro:63721:63721 [1] NCCL INFO RCCL Unroll Factor (pre-set): 4
intelbro:63720:63720 [0] NCCL INFO ncclCommInitRankConfig_impl comm 0x3befb570 rank 0 nranks 2 cudaDev 0 nvmlDev 0 busId 54000 commId 0xa362a61828935194 - Init COMPLETE
intelbro:63721:63721 [1] NCCL INFO ncclCommInitRankConfig_impl comm 0x42d42620 rank 1 nranks 2 cudaDev 1 nvmlDev 1 busId 72000 commId 0xa362a61828935194 - Init COMPLETE
intelbro:63720:63720 [0] NCCL INFO Init timings - ncclCommInitRankConfig_impl: rank 0 nranks 2 total 1.04 (kernels 0.66, alloc 0.02, bootstrap 0.17, allgathers 0.00, topo 0.15, graphs 0.00, connections 0.03, rest 0.00)
intelbro:63721:63721 [1] NCCL INFO Init timings - ncclCommInitRankConfig_impl: rank 1 nranks 2 total 0.85 (kernels 0.65, alloc 0.02, bootstrap 0.00, allgathers 0.00, topo 0.14, graphs 0.00, connections 0.03, rest 0.00)
[rank=1 local_rank=1] process group initialized[rank=0 local_rank=0] process group initialized

[rank=1 local_rank=1] before barrier: 2.0
[rank=0 local_rank=0] before barrier: 1.0
[rank=0 local_rank=0] barrier passed
[rank=1 local_rank=1] barrier passed
[rank=0 local_rank=0] after all_reduce: 3.0
[rank=1 local_rank=1] after all_reduce: 3.0
intelbro:63720:63720 [0] NCCL INFO Memory used = 33620232
intelbro:63721:63721 [1] NCCL INFO Memory used = 33620232
intelbro:63721:63721 [1] NCCL INFO comm 0x42d42620 rank 1 nranks 2 cudaDev 1 busId 72000 - Destroy COMPLETE
[rank=1 local_rank=1] done
intelbro:63720:63720 [0] NCCL INFO comm 0x3befb570 rank 0 nranks 2 cudaDev 0 busId 54000 - Destroy COMPLETE
[rank=0 local_rank=0] done
```
the rock nightly build does not work for vllm yet I got this error:
```
(Worker_TP0 pid=48686) ERROR 04-16 07:24:53 [v1/executor/multiproc_executor.py:971] torch.AcceleratorError: CUDA error: device kernel image is invalid
```
at least it might help you out.

---

### 评论 #25 — JartX (2026-04-25T23:01:05Z)

Hi @darren-amd any news about it?

---

### 评论 #26 — JartX (2026-05-04T12:02:59Z)

@msembinelli @ppanchad-amd @darren-amd  hi guys, any news?

---

### 评论 #27 — madisondigitalservice-gif (2026-05-04T14:11:25Z)

We have noticed that when we expand the context window beyond 32k-64K per session caused RoCM to crash across mGPU's with Radeon cards (7900 XTX). This is using llama.cpp. Otherwise its stable. For higher context, the only option that is compatible for higher context  is moving over to Vulkan ( 85K -166K). Would like to see this solved with vllm and the context window support higher capacities to allow for longer sessions. We built from source and found that is the only way we could make RoCM behave reasonable for mGPU use to run larger models requiring more vRAM. 

---

### 评论 #28 — tcgu-amd (2026-05-04T14:14:51Z)

Hi @JartX, sorry for the lack of updates. We had a few more tries to reproduce the issue but everything was working normally, which makes debugging kind of tricky... I have a few hypotheses and am currently combing through the source code diff to try to see what might have contributed to the bug. Thanks!

---

### 评论 #29 — JartX (2026-05-04T14:19:16Z)

Hi @tcgu-amd, thanks for replying. I know it's an amdclang issue; please check the Dockerfile, because if I compile it from a certain version of Clang, it no longer works.

---

### 评论 #30 — tcgu-amd (2026-05-04T21:21:59Z)

@JartX Managed to setup a different system with two 9700 system and was able to reproduce it! Thanks for the pointer, will look into amdclang.

---

### 评论 #31 — JartX (2026-05-04T21:24:58Z)

@tcgu-amd 

I'm here for whatever you need. I'm also still looking into the reasons why. Let me know if you need any testing or development. I'll keep you updated.

---

### 评论 #32 — JartX (2026-05-06T17:39:12Z)

Hi @tcgu-amd check this dockerfile please:
```
=============================================================================
# Dockerfile: vLLM with amdclang + RCCL built entirely from source
# Base: rocm/vllm-dev:nightly (ROCm 7.2.1 + PyTorch + vLLM)
# Compiler: ROCm LLVM rocm-7.2.2 built from source
# RCCL: rocm-7.2.1 branch built with our self-built compiler
# =============================================================================

FROM rocm/vllm-dev:nightly AS build_amdclang

# Install build deps for LLVM
RUN apt-get update -q -y && apt-get install -q -y \
    cmake ninja-build python3-dev libncurses-dev zlib1g-dev libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Build amdclang from source (only AMDGPU + X86 backends, clang + lld)
RUN git clone --branch rocm-7.2.2 --depth 1 \
        https://github.com/ROCm/llvm-project.git /tmp/llvm-project \
    && cd /tmp/llvm-project \
    && cmake -G Ninja -B build \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/amdclang \
        -DLLVM_ENABLE_PROJECTS="clang;lld" \
        -DLLVM_TARGETS_TO_BUILD="AMDGPU;X86" \
        -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
        -DCLANG_DEFAULT_LINKER=lld \
        -DLLVM_ENABLE_ASSERTIONS=OFF \
        -DLLVM_OPTIMIZED_TABLEGEN=ON \
        -DLLVM_PARALLEL_LINK_JOBS=4 \
        llvm \
    && ninja -C build -j32 \
    && ninja -C build install \
    && rm -rf /tmp/llvm-project

# =============================================================================
# Build RCCL from source with our self-built amdclang
# =============================================================================
FROM build_amdclang AS build_rccl

RUN git clone --branch rocm-7.2.1 --depth 1 https://github.com/ROCm/rccl.git /tmp/rccl \
    && cd /tmp/rccl \
    && CXX=/opt/amdclang/bin/clang++ \
       CC=/opt/amdclang/bin/clang \
       CXXFLAGS="--rocm-path=/opt/rocm" \
       CFLAGS="--rocm-path=/opt/rocm" \
       ./install.sh --amdgpu_targets "gfx1100" \
    && rm -rf /opt/amdclang

# =============================================================================
# Final image: nightly with broken RCCL replaced by our from-source build
# =============================================================================
FROM rocm/vllm-dev:nightly AS final

ENV PYTORCH_ROCM_ARCH="gfx1100"
ENV TOKENIZERS_PARALLELISM=false
ENV SAFETENSORS_FAST_GPU=1
ENV HIP_FORCE_DEV_KERNARG=1

# Remove the broken official RCCL and replace from-source build
COPY --from=build_rccl /tmp/rccl/build/release/librccl.so.1.0 /opt/rocm/lib/librccl.so.1.0
RUN rm -f /opt/rocm/lib/librccl.so.1 /opt/rocm/lib/librccl.so /opt/rocm/lib/librccl.so.1.0.70201 \
    && ln -sf librccl.so.1.0 /opt/rocm/lib/librccl.so.1 \
    && ln -sf librccl.so.1 /opt/rocm/lib/librccl.so \
    && ldconfig

CMD ["/bin/bash"] 
```

---

### 评论 #33 — JartX (2026-05-07T15:54:04Z)

@msembinelli can you check the dockerfile please?

---

### 评论 #34 — tcgu-amd (2026-05-07T16:42:59Z)

Hi @JartX Thanks for the docker file. I currently trying to track down what changed in LLVM to cause this. Thanks


---

### 评论 #35 — JartX (2026-05-07T16:46:08Z)

@tcgu-amd Hi! Could it be the compilation flags? Because from what I'm seeing, if I compile the latest amdclang and rccl, it also works correctly.

That's why I'm also asking @msembinelli if you've checked it; does it start correctly for you with this Dockerfile?

---
