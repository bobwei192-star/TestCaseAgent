# [Issue]: WSL2 ROCm6.2.3+vllm0.6.4 Failed to infer device type error message is reported when the model is started

> **Issue #4055**
> **状态**: closed
> **创建时间**: 2024-11-26T08:32:54Z
> **更新时间**: 2024-12-10T06:14:33Z
> **关闭时间**: 2024-11-26T15:01:35Z
> **作者**: githust66
> **标签**: ROCm 6.2.3, 7900xt
> **URL**: https://github.com/ROCm/ROCm/issues/4055

## 标签

- **ROCm 6.2.3** (颜色: #ededed)
- **7900xt** (颜色: #ededed)

## 描述

### Problem Description

WSL2 ROCm6.2.3+vllm0.6.4 Failed to infer device type error message is reported when the model is started
![image](https://github.com/user-attachments/assets/257f394d-6f87-4e12-810d-2f604dcc9fa9)


### Operating System

WSL2 Ubuntu 22.04

### CPU

7700

### GPU

7900xt

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

root@DESKTOP-ESRGKIB:~/miniconda3/envs/xinf/lib/python3.10/site-packages/amdsmi# /opt/rocm/bin/rocminfo --support
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    CPU                                
  Uuid:                    CPU-XX                             
  Marketing Name:          CPU                                
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
  Chip ID:                 0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    20486160(0x1389810) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20486160(0x1389810) KB             
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
  Marketing Name:          AMD Radeon RX 7900 XT              
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        16(0x10)                           
  Queue Min Size:          4096(0x1000)                       
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      6144(0x1800) KB                    
    L3:                      81920(0x14000) KB                  
  Chip ID:                 29772(0x744c)                      
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2219                               
  Internal Node ID:        1                                  
  Compute Unit:            84                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 2280                               
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20885672(0x13eb0a8) KB             
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

## 评论 (5 条)

### 评论 #1 — githust66 (2024-11-26T08:35:15Z)

For more information about VLLM, please click here, https://github.com/vllm-project/vllm/issues/10653

---

### 评论 #2 — harkgill-amd (2024-11-26T15:01:35Z)

Hi @githust66, amd-smi is not expected to work in a WSL environment due to architectural limitations. Specifically, WSL uses the Windows KMD driver than the native Linux driver implementation which will causes some form of "driver not loaded" errors for both rocm-smi and amd-smi. For more information on this, please see the [ROCm support in WSL environments ](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#rocm-support-in-wsl-environments)section in the documentation. 

As for the issue you're seeing with vLLM, the same issue has already been reported over at https://github.com/ROCm/ROCm/issues/3914#issuecomment-2480800758. We are currently looking into the vLLM+WSL usecase internally and will continue to use that thread to provide any relevant updates. I'll close out this thread for now but feel free to leave a comment if you have any questions.

---

### 评论 #3 — githust66 (2024-11-26T17:19:04Z)

> Hi @githust66, amd-smi is not expected to work in a WSL environment due to architectural limitations. Specifically, WSL uses the Windows KMD driver than the native Linux driver implementation which will causes some form of "driver not loaded" errors for both rocm-smi and amd-smi. For more information on this, please see the [ROCm support in WSL environments ](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#rocm-support-in-wsl-environments)section in the documentation.
> 
> As for the issue you're seeing with vLLM, the same issue has already been reported over at [#3914 (comment)](https://github.com/ROCm/ROCm/issues/3914#issuecomment-2480800758). We are currently looking into the vLLM+WSL usecase internally and will continue to use that thread to provide any relevant updates. I'll close out this thread for now but feel free to leave a comment if you have any questions.

OK,  you mean rocm + vllm is not currently supported on wsl?

---

### 评论 #4 — jamesxu2 (2024-12-06T15:40:11Z)

Hi @githust66 , please see my response to your question to a related ticket: https://github.com/ROCm/ROCm/issues/3914#issuecomment-2523518918

---

### 评论 #5 — githust66 (2024-12-10T06:14:33Z)

> Hi @githust66 , please see my response to your question to a related ticket: [#3914 (comment)](https://github.com/ROCm/ROCm/issues/3914#issuecomment-2523518918)

ok, thanks

---
