# [Issue]: darktable crashing on rocm 5.7.1 __pthread_kill_implementation

> **Issue #3039**
> **状态**: closed
> **创建时间**: 2024-04-18T13:21:12Z
> **更新时间**: 2024-07-10T21:01:41Z
> **关闭时间**: 2024-07-10T21:01:41Z
> **作者**: Germano0
> **标签**: AMD Instinct MI300X, AMD Instinct MI300A, AMD Instinct MI250X, ROCm 5.7.1, AMD Instinct MI100, AMD Radeon RX 7900 XTX, AMD Radeon Pro W6800, AMD Radeon Pro VII, AMD Radeon VII, AMD Radeon RX 7900 XT, AMD Radeon Pro W7900, AMD Instinct MI250, AMD Instinct MI210, AMD Radeon Pro V620
> **URL**: https://github.com/ROCm/ROCm/issues/3039

## 标签

- **AMD Instinct MI300X** (颜色: #ededed)
- **AMD Instinct MI300A** (颜色: #ededed)
- **AMD Instinct MI250X** (颜色: #ededed)
- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Instinct MI100** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **AMD Radeon Pro W6800** (颜色: #ededed)
- **AMD Radeon Pro VII** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **AMD Instinct MI250** (颜色: #ededed)
- **AMD Instinct MI210** (颜色: #ededed)
- **AMD Radeon Pro V620** (颜色: #ededed)

## 描述

### Problem Description

Disclaimer: the GPU is a Radeon 680M, which is not listed in the limited-options-list in the issue form
darktable Fedora package maintainer here.
When exporting photos, rocm crashed, causing darktable crash.

- kernel 6.8.5-201.fc39.x86_64
- amd-gpu-firmware-20240410-1.fc39.noarch
- darktable-4.6.1-5.fc39.x86_64
- rocm-opencl 5.7.1

**Attaching GDB trace here:**
[darktable_gdb.txt](https://github.com/ROCm/ROCm/files/15025458/darktable_gdb.txt)


### Operating System

Fedora 39 KDE

### CPU

AMD Ryzen 7 PRO 6850U

### GPU

AMD Instinct MI300X, AMD Instinct MI300A, AMD Instinct MI250X, AMD Instinct MI250, AMD Instinct MI210, AMD Instinct MI100, AMD Radeon Pro W7900, AMD Radeon Pro W6800, AMD Radeon Pro V620, AMD Radeon Pro VII, AMD Radeon RX 7900 XTX, AMD Radeon RX 7900 XT, AMD Radeon VII

### ROCm Version

ROCm 5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

enable OpenCL in darktable and export some photos
Advanced Micro Devices, Inc. [AMD/ATI] Rembrandt [Radeon 680M] (rev d1)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
  Name:                    AMD Ryzen 7 PRO 6850U with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 PRO 6850U with Radeon Graphics
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
  Max Clock Freq. (MHz):   4768                               
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
      Size:                    31585928(0x1e1f688) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31585928(0x1e1f688) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31585928(0x1e1f688) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1035                            
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 5761(0x1681)                       
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   13056                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
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
  Packet Processor uCode:: 116                                
  SDMA engine uCode::      47                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    1048576(0x100000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    1048576(0x100000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx1035         
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

### 评论 #1 — nartmada (2024-04-19T03:38:43Z)

@Germano0, thanks for reporting the issue.  Can you please try ROCm 6.1.0 to see if your issue has been resolved?  Thanks.

---

### 评论 #2 — Germano0 (2024-04-23T16:43:59Z)

Hello, concerning 6.1.0, I am waiting for it [to be released in Fedora](https://bugzilla.redhat.com/show_bug.cgi?id=2276678). For the moment I can provide a newer trace made with rocm 6.0
[darktable_gdb_rocm_6.txt](https://github.com/ROCm/ROCm/files/15080065/darktable_gdb_rocm_6.txt)


I would like also to attach two screenshots of radeontop:

darktable closed (after a darktable crash), Firefox running, Plasma 6.0.3 running

![radeontop_idle](https://github.com/darktable-org/darktable/assets/5477747/5e9dafd3-7996-46c5-8904-46e30cc46464)

darktable exporting, Firefox running, Plasma 6.0.3 running

![radeontop_darktable_exporting](https://github.com/darktable-org/darktable/assets/5477747/d9b58897-750f-476c-ab72-60625e03cd69)


---

### 评论 #3 — Germano0 (2024-04-30T14:07:03Z)

In [this darktable issue](https://github.com/darktable-org/darktable/issues/16641) I filled related to this crash, darktable developers found out some interesting quirks about the video RAM amount exposed to the system. There maybe a driver issue too? See in particular from [this comment](https://github.com/darktable-org/darktable/issues/16641#issuecomment-2080858563) onwards

---

### 评论 #4 — Germano0 (2024-06-27T10:41:39Z)

The crash is no longer happening on rocm 6.1.0 and 6.9.5-200.fc40.x86_64 kernel.
I leave to you the decision to close this bugreport.
Concerning the RAM amount exposed to the system, I will open a ticket to amdgpu developers to better investigate it.
Cheers

---

### 评论 #5 — harkgill-amd (2024-07-10T21:01:41Z)

Hi @Germano0, let's close this ticket for now. If you encounter this issue again, please re-open the ticket, Thanks!

---
