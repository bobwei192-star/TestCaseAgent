# [Issue]: CMake is not identifying hipcc

> **Issue #3660**
> **状态**: closed
> **创建时间**: 2024-08-30T16:55:13Z
> **更新时间**: 2024-09-06T12:42:32Z
> **关闭时间**: 2024-09-06T12:42:31Z
> **作者**: Vomartins
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3660

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

I just moved to Ubuntu 24.04 and installed ROCm on it with amdgpu-install. No errors reported. Now I would like to use hipcc to compile a program that use CMake as a build assistant. Thus, I used the CMake configuration command `cmake .. -DCMAKE_CXX_COMPILER=hipcc` and got the following error:
![Screenshot from 2024-08-30 18-50-43](https://github.com/user-attachments/assets/aa7d3804-1d9f-46fa-a185-52eb94eaea32)



### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 7900 12-Core Processor

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.2.0

### ROCm Component

HIPCC

### Steps to Reproduce

_No response_

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
  Name:                    AMD Ryzen 9 7900 12-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7900 12-Core Processor 
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
  Max Clock Freq. (MHz):   5482                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65536748(0x3e802ec) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65536748(0x3e802ec) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536748(0x3e802ec) KB             
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
  Uuid:                    GPU-07071a9c2b9e8ff7               
  Marketing Name:          AMD Radeon PRO W7900               
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
  Chip ID:                 29768(0x7448)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1760                               
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
  Packet Processor uCode:: 232                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    47169536(0x2cfc000) KB             
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

HIP version: 6.2.41133-dd7f95766
AMD clang version 18.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-6.2.0 24292 26466ce804ac523b398608f17388eb6d605a3f09)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.2.0/lib/llvm/bin
Configuration file: /opt/rocm-6.2.0/lib/llvm/bin/clang++.cfg

---

## 评论 (6 条)

### 评论 #1 — Wintoplay (2024-09-02T17:57:22Z)

I also ran into trouble on Ubuntu 24.04.1 LTS.
However, it is rocminfo.

rocminfo
ROCk module is NOT loaded, possibly no GPU devices

I guess the newest version of Ubuntu is the cause of the problem.

---

### 评论 #2 — harkgill-amd (2024-09-03T13:54:53Z)

Hi @Vomartins, could you please try installing libstdc++ with `sudo apt install libstdc++-12-dev` and then recompile the program? For reference, this looks to be the same as [Issue #4: C++ libraries](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/install-faq.html#issue-4-c-libraries).




---

### 评论 #3 — Vomartins (2024-09-03T14:58:48Z)

HI @harkgill-amd . I'll do it on Friday. Unfortunately, I don't have access to the machine before then.

---

### 评论 #4 — Vomartins (2024-09-06T10:55:09Z)

@harkgill-amd I installed the package but nothing changed.
![Screenshot from 2024-09-06 12-45-42](https://github.com/user-attachments/assets/2d4574c2-4ee7-4ced-a9a5-c818ca194848)


---

### 评论 #5 — Vomartins (2024-09-06T11:51:12Z)

Obs.: I tried using hipcc without CMake I got the same error (`fatal error: 'cmath' file not found`).

---

### 评论 #6 — Vomartins (2024-09-06T12:42:32Z)

I updated libstdc++-13 to libstdc++-14 and the problem was solved.

---
