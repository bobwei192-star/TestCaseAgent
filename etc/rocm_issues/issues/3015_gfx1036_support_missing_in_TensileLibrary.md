# gfx1036 support missing in TensileLibrary

> **Issue #3015**
> **状态**: closed
> **创建时间**: 2024-04-15T21:53:06Z
> **更新时间**: 2024-04-19T19:39:31Z
> **关闭时间**: 2024-04-19T19:39:31Z
> **作者**: tim-janik
> **标签**: ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/3015

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

I am trying to use llama.cpp with my integrated AMD graphics card, but I am getting:
```
rocBLAS error: Cannot read /opt/rocm/lib/rocblas/library/TensileLibrary.dat: No such file or directory for GPU arch : gfx1036
 List of available TensileLibrary Files : 
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1030.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1100.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1101.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1102.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx900.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx906.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx908.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx90a.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx940.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx941.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx942.dat"
Aborted (core dumped)
```

Where can I find `TensileLibrary*gfx1036.dat` ? 
FWIW, adding `HSA_OVERRIDE_GFX_VERSION=10.3.0` does *not* fix the issue, that sometimes produces either segfaults or CUDA errors like `ggml_cuda_compute_forward: ADD failed\nCUDA error: shared object initialization failed`


ROCM installed via:
```sh
$ wget https://repo.radeon.com/amdgpu-install/6.0.3/ubuntu/jammy/amdgpu-install_6.0.60003-1_all.deb && apt install ./amdgpu-install_6.0.60003-1_all.deb && amdgpu-install --usecase=graphics,rocm
[...]
rocm-utils is already the newest version (6.0.3.60003-131~22.04).
0 upgraded, 0 newly installed, 0 to remove and 48 not upgraded.
Error! Could not locate dkms.conf file.
File: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/source/dkms.conf does not exist.
WARNING: amdgpu dkms failed for running kernel

# OS INFO
OS:
NAME="Ubuntu"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
CPU: 
model name	: AMD Ryzen 9 7950X3D 16-Core Processor
GPU:
  Name:                    AMD Ryzen 9 7950X3D 16-Core Processor
  Marketing Name:          AMD Ryzen 9 7950X3D 16-Core Processor
  Name:                    gfx1036                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1036         
```

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 7950X3D 16-Core Processor GPU:

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Use any ROCM program on gfx1036 that needs `/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1036.dat`.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
[37mROCk module is loaded[0m
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
  Name:                    AMD Ryzen 9 7950X3D 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X3D 16-Core Processor
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
  Max Clock Freq. (MHz):   5714                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    94433972(0x5a0f2b4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    94433972(0x5a0f2b4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    94433972(0x5a0f2b4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1036                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
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
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   4608                               
  Internal Node ID:        1                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 20                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    4194304(0x400000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    4194304(0x400000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — nartmada (2024-04-16T15:42:43Z)

Hi @tim-janik, gfx1036 is not supported.

Please refer to the below link for the supported GPUs.
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

---
