# [Issue]: ROCm 7.1.0 incorrectly reports 8060S as GFX1201 when system uses RDNA4 eGPU

> **Issue #5696**
> **状态**: closed
> **创建时间**: 2025-11-26T05:50:43Z
> **更新时间**: 2026-02-14T05:11:31Z
> **关闭时间**: 2025-12-04T05:45:15Z
> **作者**: Soddentrough
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5696

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

System:

```
NAME="Fedora Linux"
VERSION="43 (Workstation Edition)"
CPU: model name	: AMD RYZEN AI MAX+ 395 w/ 
GPU: Radeon 8060S + R9700 Pro (eGPU)
```

```
$ sudo dmesg |grep gfx
[    4.190763] amdgpu 0000:c7:00.0: amdgpu: detected ip block number 6 <gfx_v12_0>
[    4.855272] amdgpu 0000:c7:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[    4.891410] amdgpu 0000:c8:00.0: amdgpu: detected ip block number 6 <gfx_v11_0>
[    5.587877] amdgpu 0000:c8:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
```

amdgpu driver finds the correct architectures.

ROCm details:
```
$ rocminfo 
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.14
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    130996836(0x7ceda64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130996836(0x7ceda64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    130996836(0x7ceda64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    130996836(0x7ceda64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-173c2096e6ab4d91               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   50944                              
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 108                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33406976(0x1fdc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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
  Name:                    gfx1201                            
  Uuid:                    GPU-XX                             
  Marketing Name:          Radeon 8060S Graphics              
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
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   51200                              
  Internal Node ID:        2                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65498416(0x3e76d30) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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
Agent 4                  
*******                  
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
  Vendor Name:             AMD                                
  Feature:                 AGENT_DISPATCH                     
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        1(0x1)                             
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          64(0x40)                           
  Queue Type:              SINGLE                             
  Node:                    0                                  
  Device Type:             DSP                                
  Cache Info:              
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          0(0x0)                             
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            0                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:0                                  
  Memory Properties:       
  Features:                AGENT_DISPATCH
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    130996836(0x7ceda64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536(0x10000) KB                  
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    130996836(0x7ceda64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done *** 
```

### Operating System

Fedora 43

### CPU

AMD RYZEN AI MAX+ 395 

### GPU

Radeon 8060S + R9700 Pro (eGPU/OcuLink)

### ROCm Version

7.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

```
rocm-runtime-7.1.0-1.fc44.x86_64
rocminfo-7.1.0-1.fc44.x86_64
rocm-runtime-devel-7.1.0-1.fc44.x86_64
rocm-core-7.1.0-1.fc44.x86_64
hipblas-common-devel-7.1.0-1.fc44.noarch
rocm-origami-7.1.0-1.fc44.x86_64
rocm-core-devel-7.1.0-1.fc44.x86_64
rocm-smi-7.1.0-1.fc44.x86_64
hipblaslt-7.1.0-1.fc44.x86_64
hipblaslt-devel-7.1.0-1.fc44.x86_64
rocm-llvm-filesystem-20-7.rocm7.1.0.fc44.x86_64
rocm-libc++-20-7.rocm7.1.0.fc44.x86_64
rocm-llvm-libs-20-7.rocm7.1.0.fc44.x86_64
rocm-clang-libs-20-7.rocm7.1.0.fc44.x86_64
rocm-lld-20-7.rocm7.1.0.fc44.x86_64
rocm-llvm-20-7.rocm7.1.0.fc44.x86_64
rocm-llvm-devel-20-7.rocm7.1.0.fc44.x86_64
rocm-llvm-static-20-7.rocm7.1.0.fc44.x86_64
rocm-libc++-devel-20-7.rocm7.1.0.fc44.x86_64
rocm-comgr-20-7.rocm7.1.0.fc44.x86_64
rocm-clang-runtime-devel-20-7.rocm7.1.0.fc44.x86_64
rocm-clang-20-7.rocm7.1.0.fc44.x86_64
rocm-clang-devel-20-7.rocm7.1.0.fc44.x86_64
rocm-device-libs-20-7.rocm7.1.0.fc44.x86_64
hipcc-20-7.rocm7.1.0.fc44.x86_64
rocm-comgr-devel-20-7.rocm7.1.0.fc44.x86_64
rocm-opencl-7.1.0-2.fc44.x86_64
rocm-hip-7.1.0-2.fc44.x86_64
rocm-hip-devel-7.1.0-2.fc44.x86_64
rocm-opencl-devel-7.1.0-2.fc44.x86_64
hipsparse-7.1.0-2.fc44.x86_64
hiprand-7.1.0-3.fc44.x86_64
hipblas-7.1.0-4.fc44.x86_64
hipblas-devel-7.1.0-4.fc44.x86_64
hiprand-devel-7.1.0-3.fc44.x86_64
hipsparse-devel-7.1.0-2.fc44.x86_64
hipcub-devel-7.1.0-2.fc44.x86_64

```

---

## 评论 (5 条)

### 评论 #1 — Soddentrough (2025-11-29T01:07:02Z)

Vulkan (25.2.7-3.fc4) sees things as they are:
```
		GPU id = 0 (AMD Radeon AI PRO R9700 (RADV GFX1201))
		GPU id = 1 (Radeon 8060S Graphics (RADV GFX1151))
```

But ROCm/HIP applications, including llama.cpp, display this issue. And interestingly I also see this same behavior with OpenCL.

```
$ /usr/bin/rocm-clinfo|grep -P 'Board|gfx'
  Board name:					 AMD Radeon AI PRO R9700
  Name:						 gfx1201
  Board name:					 Radeon 8060S Graphics
  Name:						 gfx1201
```


---

### 评论 #2 — schung-amd (2025-12-01T20:28:50Z)

Thanks for the report, I'll take a look once I source hardware to repro this on.

---

### 评论 #3 — Soddentrough (2025-12-04T05:45:15Z)

Well now I feel like a total goose. I updated to 7.1.1 and in doing so noticed my .bashrc had 
```
export HSA_OVERRIDE_GFX_VERSION=12.0.1
```
This was forcing the override (hence the name). Removing that and we are back to:
```
$ rocminfo |grep gfx
  Name:                    gfx1201                            
      Name:                    amdgcn-amd-amdhsa--gfx1201         
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
  Name:                    gfx1151                            
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
```
Dear oh dear. 

---

### 评论 #4 — Geramy (2026-02-14T04:22:54Z)

> Well now I feel like a total goose. I updated to 7.1.1 and in doing so noticed my .bashrc had
> 
> ```
> export HSA_OVERRIDE_GFX_VERSION=12.0.1
> ```
> 
> This was forcing the override (hence the name). Removing that and we are back to:
> 
> ```
> $ rocminfo |grep gfx
>   Name:                    gfx1201                            
>       Name:                    amdgcn-amd-amdhsa--gfx1201         
>       Name:                    amdgcn-amd-amdhsa--gfx12-generic   
>   Name:                    gfx1151                            
>       Name:                    amdgcn-amd-amdhsa--gfx1151         
>       Name:                    amdgcn-amd-amdhsa--gfx11-generic   
> ```
> 
> Dear oh dear.

What hardware do you have that is the gfx1151 and supports oculink? I have the MS-S1 and R9700 but I cant get the oculink to work.

---

### 评论 #5 — Soddentrough (2026-02-14T05:11:31Z)

I am using a "FEVM FAEX9". 

---
