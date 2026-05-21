# [Issue]: Davinci Resolve 18.6.2 crashes on kernel 6.6.2 and Rocm 5.7.1

> **Issue #2672**
> **状态**: closed
> **创建时间**: 2023-11-24T17:57:25Z
> **更新时间**: 2024-06-25T03:52:06Z
> **关闭时间**: 2024-06-25T03:52:06Z
> **作者**: helloworld1
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2672

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

On Kernel 6.6.2 and Rocm 5.7.1. When I launch Davinci Resolve it crashes with the following trace
```
/opt/resolve/bin/resolve() [0x487ffe9]
/opt/resolve/bin/resolve() [0x487f3d0]
/usr/lib/libc.so.6(+0x3e710) [0x7fd7d085c710]
/usr/lib/libc.so.6(+0x158337) [0x7fd7d0976337]
/usr/lib/dri/radeonsi_dri.so(+0x8a4c16) [0x7fd668ca4c16]
/usr/lib/dri/radeonsi_dri.so(+0x8165cc) [0x7fd668c165cc]
/usr/lib/dri/radeonsi_dri.so(+0x81c24b) [0x7fd668c1c24b]
/usr/lib/dri/radeonsi_dri.so(amdgpu_winsys_create+0x628) [0x7fd668cd1d88]
/usr/lib/dri/radeonsi_dri.so(+0xe392a) [0x7fd6684e392a]
/usr/lib/dri/radeonsi_dri.so(+0x6c6d03) [0x7fd668ac6d03]
/usr/lib/dri/radeonsi_dri.so(+0xe0c62) [0x7fd6684e0c62]
/usr/lib/dri/radeonsi_dri.so(+0xce815) [0x7fd6684ce815]
/usr/lib/libGLX_mesa.so.0(+0x5474c) [0x7fd7c506474c]
/usr/lib/libGLX_mesa.so.0(+0x38109) [0x7fd7c5048109]
/usr/lib/libGLX_mesa.so.0(+0x386c4) [0x7fd7c50486c4]
/usr/lib/libGLX_mesa.so.0(+0x3f063) [0x7fd7c504f063]
/opt/resolve/libs/plugins/xcbglintegrations/libqxcb-glx-integration.so(+0x982b) [0x7fd7c700f82b]
/opt/resolve/libs/libQt5XcbQpa.so.5(_ZN10QXcbWindow6createEv+0x7b6) [0x7fd799325cf6]
/opt/resolve/libs/libQt5XcbQpa.so.5(_ZNK15QXcbIntegration20createPlatformWindowEP7QWindow+0xad) [0x7fd7993188dd]
/opt/resolve/bin/../libs/libQt5Gui.so.5(_ZN14QWindowPrivate6createEby+0x1f6) [0x7fd7b612e6a6]
/opt/resolve/bin/../libs/libQt5Widgets.so.5(_ZN14QWidgetPrivate6createEv+0x589) [0x7fd7e458fbd9]
/opt/resolve/bin/../libs/libQt5Widgets.so.5(_ZN7QWidget6createEybb+0x142) [0x7fd7e458e862]
/opt/resolve/bin/../libs/libQt5Widgets.so.5(_ZN14QWidgetPrivate10setVisibleEb+0x1b5) [0x7fd7e45a25b5]
/opt/resolve/bin/resolve() [0x24ccd58]
/opt/resolve/bin/resolve() [0x24d022c]
/opt/resolve/bin/resolve() [0x24ca6ce]
/usr/lib/libc.so.6(+0x27cd0) [0x7fd7d0845cd0]
/usr/lib/libc.so.6(__libc_start_main+0x8a) [0x7fd7d0845d8a]
/opt/resolve/bin/resolve() [0x24c8d6b]
```

Downgrading to kernel 6.5.9 works fine without this issue.
If I uninstall rocm packages, davinci reseolve can start normally but videos cannot playback.

### Operating System

Arch

### CPU

AMD Ryzon 5900x

### GPU

AMD 6950xt

### ROCm Version

5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### Output of /opt/rocm/bin/rocminfo --support

```ROCk module is loaded
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
  Name:                    AMD Ryzen 9 5900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5900X 12-Core Processor
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65746380(0x3eb35cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65746380(0x3eb35cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65746380(0x3eb35cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-7a2c2ab825bf6831               
  Marketing Name:          AMD Radeon RX 6950 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      131072(0x20000) KB                 
  Chip ID:                 29605(0x73a5)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2720                               
  BDFID:                   2816                               
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 115                                
  SDMA engine uCode::      83                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    16760832(0xffc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1030         
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
*** Done ***   ```

---

## 评论 (5 条)

### 评论 #1 — ryan-ronnander (2023-12-05T23:38:40Z)

I am also seeing this problem on kernel 6.6.4 and ROCm 5.7.2. 

---

### 评论 #2 — helloworld1 (2024-01-13T04:15:41Z)

Also crashes on kernel 6.7 and ROCm 6.0.0 with the same error.

---

### 评论 #3 — harkgill-amd (2024-06-20T19:50:20Z)

Hi @helloworld1, an internal ticket has been created to investigate this issue. Are you seeing any issues with DaVinci Resolve on kernel 6.5?

---

### 评论 #4 — harkgill-amd (2024-06-20T20:32:23Z)

@helloworld1, could you also please provide the exact OS details. Also, is this being run in a virtual machine?

---

### 评论 #5 — helloworld1 (2024-06-25T03:52:06Z)

I have tested kernel 6.7, 6.8 and 6.9. All 3 versions works fine now. Seems like 6.6 just have a regression.

---
