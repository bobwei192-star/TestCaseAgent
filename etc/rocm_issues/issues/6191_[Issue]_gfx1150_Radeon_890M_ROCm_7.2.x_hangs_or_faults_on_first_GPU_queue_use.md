# [Issue]: gfx1150 / Radeon 890M: ROCm 7.2.x hangs or faults on first GPU queue use

> **Issue #6191**
> **状态**: closed
> **创建时间**: 2026-04-29T10:19:27Z
> **更新时间**: 2026-04-29T13:19:01Z
> **关闭时间**: 2026-04-29T13:19:01Z
> **作者**: tastynoob
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6191

## 描述

### Problem Description

## Summary

On a Ryzen AI 9 HX 370 system with Radeon 890M (`gfx1150`), ROCm 7.2.x hangs or faults when creating the first real GPU queue / command submission path.

This is not JAX-specific. I can reproduce the same low-level failure with:

- JAX at `jax.devices()`
- a minimal HIP program
- PyTorch ROCm

## System

- OS: Ubuntu 24.04.4 LTS
- Kernel tested: `6.17.0-1017-oem` and generic HWE kernel
- GPU: Radeon 890M (`gfx1150`, device id `0x150e`)
- ROCm: 7.2.x
- `hipconfig --version`: `7.2.53211-671d39a71e`
- PyTorch: `2.11.0+rocm7.2`
- JAX: `0.8.2`

`rocminfo` shows the GPU, but also reports:

- `Coherent Host Access: FALSE`
- `IOMMU Support:: None`
- `DMAbuf Support: YES`
- `VMM Support: YES`

### Operating System

Ubuntu 24.04 lts

### CPU

AMD Ryzen Ai 9 hx 370

### GPU

890m iGPU

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

## Repro

### Minimal HIP repro

```cpp
#include <hip/hip_runtime.h>
#include <cstdio>

static int check(hipError_t err, const char* label) {
  if (err != hipSuccess) {
    fprintf(stderr, "%s failed: %s\n", label, hipGetErrorString(err));
    return 1;
  }
  printf("%s ok\n", label);
  fflush(stdout);
  return 0;
}

int main() {
  setvbuf(stdout, nullptr, _IONBF, 0);
  setvbuf(stderr, nullptr, _IONBF, 0);

  int count = 0;
  if (check(hipGetDeviceCount(&count), "hipGetDeviceCount")) return 1;
  printf("device_count=%d\n", count);

  if (check(hipSetDevice(0), "hipSetDevice")) return 1;

  float* dev = nullptr;
  printf("before hipMalloc\n");
  if (check(hipMalloc(&dev, 64), "hipMalloc")) return 1;

  printf("before hipMemset\n");
  if (check(hipMemset(dev, 0, 64), "hipMemset")) return 1;

  printf("done\n");
  return 0;
}
```

Observed behavior:

- `hipGetDeviceCount` and `hipMalloc` succeed
- `hipMemset` hangs
- with `HSA_ENABLE_VM_FAULT_MESSAGE=1 HIP_SKIP_ABORT_ON_GPU_ERROR=0`, the process aborts with:

```text
Memory access fault by GPU node-1 ... Reason: Page not present or supervisor privilege.
```

Kernel log also shows:

```text
amdgpu ... [gfxhub] page fault
GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
Faulty UTCL2 client ID: CPF (0x4)
WALKER_ERROR: 0x1
PERMISSION_FAULTS: 0x3
MAPPING_ERROR: 0x1
```

The fault address maps into a `/dev/dri/renderD128` mapping.

### PyTorch repro

PyTorch sees the GPU:

```text
cuda_available: True
device_count: 1
device[0]: name=AMD Radeon 890M
```

But the first real GPU allocation/initialization hangs:

```python
import torch
x = torch.zeros((1,), device="cuda")
```

`torch.empty((1,), device="cuda")` succeeds, but `torch.zeros(...)`, H2D copy, or synchronization hangs.

## What I tried

I already tested the usual workarounds and they did not fix the issue:

- `amdgpu.cwsr_enable=0`
- `iommu=pt`
- OEM kernel and generic kernel
- `amdgpu-dkms` removal / reinstall
- firmware update
- `HSA_ENABLE_SDMA=0`
- `HSA_XNACK=0/1`
- `HSA_FORCE_FINE_GRAIN_PCIE=1`
- `HSA_ALLOCATE_QUEUE_DEV_MEM=1`
- `AMD_DIRECT_DISPATCH=0`
- other common ROCm env vars related to queueing / dispatch / memory

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
*******                  
Agent 2                  
*******                  
  Name:                    gfx1150                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon 890M Graphics           
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 5390(0x150e)                       
  ASIC Revision:           4(0x4)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50176                              
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12103188(0xb8ae14) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    12103188(0xb8ae14) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1150         
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
```

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — tastynoob (2026-04-29T11:57:56Z)

Resolved:
reinstall dkms by this version:
 https://repo.radeon.com/amdgpu/30.20.1/ubuntu/pool/main/a/amdgpu-dkms/amdgpu-dkms_6.16.6.30200100-2255209.24.04_all.deb
https://repo.radeon.com/amdgpu/30.20.1/ubuntu/pool/main/a/amdgpu-dkms-firmware/amdgpu-dkms-firmware_30.20.1.0.30200100-2255209.24.04_all.deb


---
