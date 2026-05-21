# [Issue]: Pytorch for rocm (6.1) doesn't work correctly.  Ubuntu 20.04 with AMD GPU

> **Issue #3485**
> **状态**: closed
> **创建时间**: 2024-08-02T09:15:08Z
> **更新时间**: 2024-08-07T13:09:08Z
> **关闭时间**: 2024-08-07T13:09:08Z
> **作者**: DragonOV12341
> **标签**: Under Investigation, AMD Radeon VII, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3485

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Hi，I met the problem of 'torch.cuda.is_available()' returns 'False'.  
My ROCm version is 6.1, and I installed pytorch for rocm through official website of pytorch. I checked my installed torch through `pip list` and returns:
```
torch                    2.4.0+rocm6.1
torchaudio               2.4.0+rocm6.1
torchvision              0.19.0+rocm6.1
```
My ROCM is installed in local system, and pytorch is installed in Anaconda virtual env I created. 
'rocminfo' returns:
```
ROCk module version 6.7.0 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.13
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
  Name:                    Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz
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
  Max Clock Freq. (MHz):   3000                               
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
      Size:                    32836212(0x1f50a74) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32836212(0x1f50a74) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32836212(0x1f50a74) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3000                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32976488(0x1f72e68) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32976488(0x1f72e68) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32976488(0x1f72e68) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx906                             
  Uuid:                    GPU-3866388172dc76e5               
  Marketing Name:          AMD Radeon VII                     
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
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 26287(0x66af)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1801                               
  BDFID:                   768                                
  Internal Node ID:        2                                  
  Compute Unit:            60                                 
  SIMDs per CU:            4                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 471                                
  SDMA engine uCode::      145                                
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
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
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
Check of `import torch;torch.tensor[1,1]` works fine. But the output of 'torch.cuda.is_available()' is False. How can I solve the problem? Thx

### Operating System

Ubuntu 20.04

### CPU

Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2024-08-02T15:05:40Z)

@DragonOV12341 Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — jamesxu2 (2024-08-06T15:47:21Z)

Hello @DragonOV12341, I'm not able to reproduce your issue with a Radeon VII card. I've done a clean install of ROCm 6.1.0 and pytorch 2.4+rocm6.1 and my torch.cuda.is_available() returns true. 

Have you added your user to the render/video groups? 
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#setting-permissions-for-groups

---

### 评论 #3 — DragonOV12341 (2024-08-07T07:27:58Z)

Thanks! I checked the group settings and add myself to render and video group, then it returns True. Helps me a lot, thx :)



---Original---
From: ***@***.***&gt;
Date: Tue, Aug 6, 2024 23:47 PM
To: ***@***.***&gt;;
Cc: ***@***.******@***.***&gt;;
Subject: Re: [ROCm/ROCm] [Issue]: Pytorch for rocm (6.1) doesn't workcorrectly.  Ubuntu 20.04 with AMD GPU (Issue #3485)




 
Hello @DragonOV12341, I'm not able to reproduce your issue with a Radeon VII card. I've done a clean install of ROCm 6.1.0 and pytorch 2.4+rocm6.1 and my torch.cuda.is_available() returns true.
 
Have you added your user to the render/video groups?
 https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#setting-permissions-for-groups
 
—
Reply to this email directly, view it on GitHub, or unsubscribe.
You are receiving this because you were mentioned.Message ID: ***@***.***&gt;

---
