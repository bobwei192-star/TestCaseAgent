# [Issue]: hsa_queue_create causes GPU page fault on gfx1151 APU (Ryzen AI Max+ 395, Radeon 8060S)

> **Issue #6118**
> **状态**: closed
> **创建时间**: 2026-04-04T11:26:17Z
> **更新时间**: 2026-04-08T06:41:46Z
> **关闭时间**: 2026-04-08T06:41:46Z
> **作者**: tomasthoresen
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6118

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

## Environment
- APU: AMD Ryzen AI Max+ 395 (Strix Halo)
- GPU: Radeon 8060S (gfx1151, RDNA 3.5, Chip ID 0x1586)
- ROCm: 7.2.1 (hsa-rocr 1.18.0.70201-81)
- Driver: amdgpu-dkms 6.19.0 (31.20 series)
- Kernel: 6.17.0-20-generic (Ubuntu 24.04)
- Also tested: amdgpu-dkms 6.16.13 (30.30), kernel 6.17.0-19

## Problem
hsa_queue_create() on the gfx1151 GPU agent causes an immediate
GPU memory access fault and crashes:

  Memory access fault by GPU node-1 (Agent handle: 0x5b19b86e7090) 
  on address 0x767500478000. 
  Reason: Page not present or supervisor privilege.

dmesg shows:
  amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8)
  GCVM_L2_PROTECTION_FAULT_STATUS: 0x00800932
  Faulty UTCL2 client ID: CPF (0x4)
  WALKER_ERROR: 0x1, PERMISSION_FAULTS: 0x3, MAPPING_ERROR: 0x1

This blocks ALL GPU compute: hipStreamCreate, hipMalloc, 
hipModuleLoadData all hang because they go through hsa_queue_create.

## What works
- rocminfo detects the GPU correctly (gfx1151, 40 CUs, KERNEL_DISPATCH)
- rocm-smi shows healthy GPU (32°C, 23W)
- hipInit, hipHostMalloc, hipDeviceSynchronize all work
- hiprtcCompileProgram produces valid code objects
- Display output works fine

## Minimal reproducer (Python)
```python
import ctypes

hsa = ctypes.CDLL('/opt/rocm/lib/libhsa-runtime64.so')

class hsa_agent_t(ctypes.Structure):
    _fields_ = [('handle', ctypes.c_uint64)]

hsa.hsa_init()

AGENT_CB = ctypes.CFUNCTYPE(ctypes.c_int, hsa_agent_t, ctypes.c_void_p)
gpu = hsa_agent_t()

def find_gpu(agent, data):
    dev = ctypes.c_uint32()
    hsa.hsa_agent_get_info(agent, 17, ctypes.byref(dev))
    if dev.value == 1:
        gpu.handle = agent.handle
    return 0

hsa.hsa_iterate_agents(AGENT_CB(find_gpu), None)
queue = ctypes.c_void_p()
# This line crashes with page fault:
hsa.hsa_queue_create(gpu, 1024, 0, None, None, 
    ctypes.c_uint32(0xFFFFFFFF), ctypes.c_uint32(0xFFFFFFFF),
    ctypes.byref(queue))
```

## Impact
Completely blocks GPU compute on Ryzen AI Max+ 395.

## rocminfo GPU output
  Name: gfx1151
  Marketing Name: Radeon 8060S Graphics
  Feature: KERNEL_DISPATCH
  Max Queue Number: 128
  Chip ID: 5510 (0x1586)
  Compute Unit: 40
  Wavefront Size: 32

### Operating System

24.04.4 LTS (Noble Numbat)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon™ 8060S × 32

### GPU

Radeon™ 8060S Graphics

### ROCm Version

7.2.1 (hsa-rocr 1.18.0.70201-81)

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — janchk (2026-04-06T22:29:25Z)

And here we are asking why cuda is winning..

---

### 评论 #2 — amd-nicknick (2026-04-07T09:13:18Z)

Hi @tomasthoresen, the reproducer you provided works correctly on my system.
For Strix Halo, try to use the OEM kernel instead of DKMS. Follow the instructions here: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html
Specifically, you should remove all DKMS and firmware package installed, and make sure you're using 24.04 OEM kernel.

Could you please help clarify what you're trying to achieve here? I recommend using the hip APIs as that is easier, portable and better documented compared to interfacing with hsa.

---

### 评论 #3 — tomasthoresen (2026-04-08T03:45:00Z)

@amd-nicknick - Thank you for testing and for the guidance. I can confirm that using the OEM kernel I am able to progress. Thx!

---

### 评论 #4 — amd-nicknick (2026-04-08T06:41:46Z)

@tomasthoresen, no problem at all. If you encounter any further problem, feel free to create a new issue and we'll take a look. Thanks!

---
