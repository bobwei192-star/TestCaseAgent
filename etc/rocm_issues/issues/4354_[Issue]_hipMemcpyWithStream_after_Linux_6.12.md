# [Issue]: hipMemcpyWithStream after Linux 6.12

> **Issue #4354**
> **状态**: closed
> **创建时间**: 2025-02-07T07:46:49Z
> **更新时间**: 2025-02-18T17:14:23Z
> **关闭时间**: 2025-02-18T16:41:23Z
> **作者**: waltercool
> **标签**: Under Investigation, ROCm 6.2.4
> **URL**: https://github.com/ROCm/ROCm/issues/4354

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.4** (颜色: #ededed)

## 描述

### Problem Description

Hi there,

I been seeing this error for a while, and only happens at Linux 6.12, 6.13 and current 6.14-rc1. It works fine while using Linux 6.10.

When using ComfyUI or Stable Diffussion Forge, both will crash with a same hipMemcpyWithStream call.

Example from Stable Diffussion Forge:

```
:3:hip_device_runtime.cpp   :644 : 1326120773 us: [pid:8976  tid:0x7f8c5a889f80] hipGetDevice: Returned hipSuccess : 
:3:hip_graph.cpp            :866 : 1326120781 us: [pid:8976  tid:0x7f8c5a889f80]  hipStreamIsCapturing ( stream:<null>, 0x7ffe58b192a0 ) 
:3:hip_graph.cpp            :867 : 1326120784 us: [pid:8976  tid:0x7f8c5a889f80] hipStreamIsCapturing: Returned hipSuccess : 
:3:hip_memory.cpp           :615 : 1326120791 us: [pid:8976  tid:0x7f8c5a889f80]  hipMalloc ( 0x7ffe58b19390, 2097152 ) 
:3:rocdevice.cpp            :2418: 1326120905 us: [pid:8976  tid:0x7f8c5a889f80] Device=0x55e868b90800, freeMem_ = 0x1fee00000
:3:hip_memory.cpp           :617 : 1326120914 us: [pid:8976  tid:0x7f8c5a889f80] hipMalloc: Returned hipSuccess : 0x7f87de200000: duration: 123 us
:3:hip_device_runtime.cpp   :666 : 1326120928 us: [pid:8976  tid:0x7f8c5a889f80]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :670 : 1326120930 us: [pid:8976  tid:0x7f8c5a889f80] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :666 : 1326120932 us: [pid:8976  tid:0x7f8c5a889f80]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :670 : 1326120933 us: [pid:8976  tid:0x7f8c5a889f80] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 1326120996 us: [pid:8976  tid:0x7f8c5a889f80]  hipGetDevice ( 0x7ffe58b199e4 ) 
:3:hip_device_runtime.cpp   :644 : 1326121000 us: [pid:8976  tid:0x7f8c5a889f80] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 1326121003 us: [pid:8976  tid:0x7f8c5a889f80]  hipGetDevice ( 0x7ffe58b197fc ) 
:3:hip_device_runtime.cpp   :644 : 1326121005 us: [pid:8976  tid:0x7f8c5a889f80] hipGetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :701 : 1326121016 us: [pid:8976  tid:0x7f8c5a889f80]  hipMemcpyWithStream ( 0x7f87de200000, 0x55e86938bd00, 4, hipMemcpyHostToDevice, stream:<null> ) 
:3:rocdevice.cpp            :3030: 1326121023 us: [pid:8976  tid:0x7f8c5a889f80] Number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
./webui.sh: line 304:  8976 Segmentation fault      (core dumped) "${python_cmd}" -u "${LAUNCH_SCRIPT}" "$@"
```

Any idea what could be the issue or any lead to this, would be very appreciated.

A small discussion happened at https://github.com/comfyanonymous/ComfyUI/issues/5756, but I did recommended for now to stay into 6.10 because that works for me.

### Operating System

Gentoo

### CPU

AMD Ryzen 7 7840HS w/ Radeon 780M Graphics

### GPU

AMD Radeon RX 7700S

### ROCm Version

6.2.4 (current Pytorch)

### ROCm Component

HIP

### Steps to Reproduce

Use Kernel 6.12+
Install ComfyUI or Stable Diffusion Forge
Create a venv folder and activate it.
Install latest stable Pytorch for ROCM
Install requirements.py for ComfyUI or run webui.sh for Stable Diffusion Forge.

On ComfyUI, this is easy to reproduce by executing a Flux.1 operation
On Stable Diffusion Forge, it crashes by start

While running ComfyUI or SD Forge, I'm using the following env variables:
- HSA_OVERRIDE_GFX_VERSION=11.0.0
- HIP_VISIBLE_DEVICES=0

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.4
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
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5137                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    96627696(0x5c26bf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    96627696(0x5c26bf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    96627696(0x5c26bf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 7700S                
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2208                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 462                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8372224(0x7fc000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1103                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon 780M                    
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
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           9(0x9)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   50432                              
  Internal Node ID:        2                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 40                                 
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    48313848(0x2e135f8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    48313848(0x2e135f8) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1103         
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

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — tcgu-amd (2025-02-07T21:26:04Z)

Hi @waltercool, thanks for raising the issue! We appreciate your efforts on trying ROCm on cutting edge Linux versions. However, we currently [only support kernel versions up to 6.11 HWE](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#os-kernel-versions), which could explain why 6.12 is causing problems. 

I would still be happy to take a look at your issue to see if I can find any hints, but the default logs you provided do not reveal much information at lower levels. Would you be able run the test with AMD_LOG_LEVEL=5, and HSAKMT_DEBUG_INFO=5 separately and upload the resulting logs? 

Figuring out issues in an unsupported kernel is difficult, and even with these logs we might not be able to figure out what's going on. Even if we did, a patch will likely not be made until the newer version is supported by ROCm anyways. I would personally suggest to refrain from upgrading the kernel and just stick with the version that works for now. 

Thanks! 

---

### 评论 #2 — tcgu-amd (2025-02-18T16:41:23Z)

Hi, I will be closing this issue for now due to inactivity. Please feel free to follow-up/reopen. Thanks! 

---

### 评论 #3 — waltercool (2025-02-18T17:14:22Z)

No worries, since I'm already avoiding those Linux distributions. I do understand debugging from your side will get lot more difficult. So far, 6.10 an 6.11 seems to work OK, and I'm already sticking on those.

Just concerned because those versions are no longer supported by the Linux Kernel team.

If you think adding extra logs from 6.13 or 6.14 can be useful, I can do it.

---
