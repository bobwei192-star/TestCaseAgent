# [Issue]: mesa-amdgpu-va-drivers crashing google chrome/vs code but not chromium/codium

> **Issue #4056**
> **状态**: closed
> **创建时间**: 2024-11-26T15:45:45Z
> **更新时间**: 2024-11-26T18:25:15Z
> **关闭时间**: 2024-11-26T18:25:15Z
> **作者**: keejkrej
> **标签**: Under Investigation, ROCm 6.2.3, Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4056

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

I have a fresh installation of rocm 6.2.4 on linux mint 22 (based on ubuntu 24.04), google chrome will crash on startup, firefox and chromium runs fine. 
Error: Cannot find target for triple amdgcn-- Unable to find target for this triple (no targets are registered)
When I remove the mesa-amdgpu-va-drivers, problem solved. But rocm depends on mesa-amdgpu-va-drivers and apt will try to remove rocm as a whole.

### Operating System

Linux Mint 22 / Ubuntu 24.04

### CPU

12th Gen Intel(R) Core(TM) i7-12700K

### GPU

Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

Install Ubuntu 24.04
Follow installation instructions on [installation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)
Reboot
Follow post installation instructions on [post installation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/post-install.html)
Run google-chrome/vs code (in terminal)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    12th Gen Intel(R) Core(TM) i7-12700K
  Uuid:                    CPU-XX                             
  Marketing Name:          12th Gen Intel(R) Core(TM) i7-12700K
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
  Max Clock Freq. (MHz):   4900                               
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
      Size:                    65631852(0x3e9766c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65631852(0x3e9766c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65631852(0x3e9766c) KB             
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
  Uuid:                    GPU-97823e6593efd99c               
  Marketing Name:          Radeon RX 7900 XTX                 
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2431                               
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 342                                
  SDMA engine uCode::      21                                 
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done *** 

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2024-11-26T16:39:43Z)

Hi @keejkrej. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2024-11-26T17:16:49Z)

Hi @keejkrej, can you try installing ROCm with the AMDGPU installer (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html) using `--usecase=graphics,rocm`? The quick start instructions are not compatible with some graphical workloads and applications. If this doesn't resolve the issue with ROCm 6.2.4 you can also try the ROCm on Radeon release which is specifically intended for this usecase: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html.

---

### 评论 #3 — keejkrej (2024-11-26T17:40:47Z)

Thank you! `sudo amdgpu-install --usecase=graphics, rocm` works!
Please add this to the "quick start" page if possible, since most people will copy the code in quick start and be frustrated when google chrome won't launch.

---

### 评论 #4 — schung-amd (2024-11-26T18:25:15Z)

Glad to hear it works!

Regarding the quick start instructions, I understand your (and many other users') frustrations. The mainline ROCm releases are really intended for headless configurations and not for graphics workloads, and we have a warning (albeit commonly overlooked) pointing this out:

> If you’re using ROCm with AMD Radeon or Radeon Pro GPUs for graphics workloads, see the [Use ROCm on Radeon GPU](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html) documentation for installation instructions .

From one perspective, the quick start is intended to be a minimal default installation, so it makes sense not to include the graphics components as the mainline release stream is intended for non-graphical configurations; users who do want these components are directed to the ROCm on Radeon release stream which is specifically tested for graphical workloads.

However, users will naturally want to use the latest ROCm version, and the ROCm on Radeon releases are not updated as frequently as the mainline releases. In my experience I have had no issues with mainline + `--usecase=graphics`, but we don't test graphics workloads on these releases as extensively as with the ROCm on Radeon release stream, so the latter is our default recommendation.

I agree with you that there is a disconnect here. In my view a common/intuitive path to getting ROCm as a new user is just searching "install ROCm", finding the quick start instructions, and copy-pasting the commands, and unfortunately as you have observed there will be problems for "regular" users (i.e. those with consumer GPUs who use their system for gaming/multimedia/etc. and just want to try ROCm). For the moment we don't have the best support or guidance for such users, but I am hopeful that we will improve on this in the future.

Thanks for your interest in ROCm!

---
