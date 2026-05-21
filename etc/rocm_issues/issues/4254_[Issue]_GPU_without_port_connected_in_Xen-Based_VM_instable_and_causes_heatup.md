# [Issue]: GPU without port connected in Xen-Based VM instable and causes heatup

> **Issue #4254**
> **状态**: closed
> **创建时间**: 2025-01-13T21:38:55Z
> **更新时间**: 2025-01-14T20:53:42Z
> **关闭时间**: 2025-01-14T20:53:41Z
> **作者**: rsta79
> **标签**: Under Investigation, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4254

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

passing a GPU without port connected to a monitor into a Xen-HVM causes the GPU heats up and the fan goes full speed without any workload, also the VM might crash in the meantime, or the device disappeared in rocminfo. I don't think its highly-related to ROCm itself though, but probably ROCm is the only feature that users will probably use the GPU without connecting to a monitor.

the problem can be fixed by connect the GPU to a monitor.

not tested in non-Xen environments yet. it's probably not a Xen specific problem.

### Operating System

QubesOS(debian-12-xfce+testing/firmware-amd-graphics, fedora-40-xfce)

### CPU

Intel Core i7-14700K

### GPU

AMD Radeon RX7800XT

### ROCm Version

ROCm 6.3.0

### ROCm Component

ROCK-Kernel-Driver, ROCm

### Steps to Reproduce

pass GPU with any ports connected into a HVM qube. start and wait about 10-20 minutes, then GPU will starts heats up and fan goes full speed without any workload or randomly crashes the VM.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
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
DMAbuf Support:          NO

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    Intel(R) Core(TM) i7-14700K        
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i7-14700K        
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
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16004616(0xf43608) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16004616(0xf43608) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16004616(0xf43608) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16004616(0xf43608) KB              
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
  Uuid:                    GPU-7570dd6500000000               
  Marketing Name:          AMD Radeon RX 7800 XT              
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
  Max Clock Freq. (MHz):   2213                               
  BDFID:                   48                                 
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
  Packet Processor uCode:: 462                                
  SDMA engine uCode::      27                                 
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
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
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

### Additional Information

sometimes the rocminfo failure with following message:
```
long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1306 Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events. 
```

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2025-01-14T15:26:37Z)

Hi @rsta79. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-01-14T16:22:49Z)

Hey @rsta79, thanks for reaching out! Just to confirm, is this issue related to https://github.com/ROCm/ROCm/issues/4253 or should we treat them as separate ones? Thanks!

---

### 评论 #3 — tcgu-amd (2025-01-14T16:50:43Z)

@rsta79, please keep in mind that for both #4253 and this issue, ROCm is not officially supported for Zen HVM (please refer to our [official support matrix for virtualization](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#virtualization-support). If the workload runs fine on bare metal, then the lack of support is likely the reason. 

---

### 评论 #4 — rsta79 (2025-01-14T17:11:08Z)

> Hey [@rsta79](https://github.com/rsta79), thanks for reaching out! Just to confirm, is this issue related to [#4253](https://github.com/ROCm/ROCm/issues/4253) or should we treat them as separate ones? Thanks!

@tcgu-amd I believe its two separate issue. cause I remember I once using bare metal archlinux setup without dGPU connect to the monitor, and its heating up and fan also goes full speed without any workloads. but I'm not testing it for this release of ROCm yet. and I'll try out using KVM to see if its working. but I believe that Xen-HVM is using qemu as backend though. 

I'll give the test results here once I finished testing.

---

### 评论 #5 — rsta79 (2025-01-14T17:20:03Z)

> [@rsta79](https://github.com/rsta79), please keep in mind that for both [#4253](https://github.com/ROCm/ROCm/issues/4253) and this issue, ROCm is not officially supported for Zen HVM (please refer to our [official support matrix for virtualization](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#virtualization-support). If the workload runs fine on bare metal, then the lack of support is likely the reason.

One thing I want to mention is that connect the GPU with monitor can make it stable and work as normal (not heating up). and the rocminfo is also stable when its connected. and torch can also recognize the device, but putting any workload on it will causes the terminal hangs. just as mentioned in  #4253 .

---

### 评论 #6 — rsta79 (2025-01-14T20:32:45Z)

> > [@rsta79](https://github.com/rsta79), please keep in mind that for both [#4253](https://github.com/ROCm/ROCm/issues/4253) and this issue, ROCm is not officially supported for Zen HVM (please refer to our [official support matrix for virtualization](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#virtualization-support). If the workload runs fine on bare metal, then the lack of support is likely the reason.
> 
> One thing I want to mention is that connect the GPU with monitor can make it stable and work as normal (not heating up). and the rocminfo is also stable when its connected. and torch can also recognize the device, but putting any workload on it will causes the terminal hangs. just as mentioned in [#4253](https://github.com/ROCm/ROCm/issues/4253) .

After testing. ROCm in QEMU/KVM on archlinux works just fine. even without ports connected. and unfortunately, it seems to be problem specific to ROCm in Xen environments. Guess I'm out of luck here :( 

---

### 评论 #7 — tcgu-amd (2025-01-14T20:47:34Z)

@rsta79 Yeah...Really sorry about the lack of support, but unfortunately this is the current state of where ROCm is at :( 





---

### 评论 #8 — tcgu-amd (2025-01-14T20:53:41Z)

@rsta79, thanks for opening a feature request. I will bring the request to the attention of internal dev teams and I will close this and #4253 for now to avoid redundancy. Thanks! 

---
