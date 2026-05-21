# [Issue]: When installing ROCm from nightly - rccl wont compile.

> **Issue #5817**
> **状态**: closed
> **创建时间**: 2025-12-26T16:06:31Z
> **更新时间**: 2025-12-30T15:23:43Z
> **关闭时间**: 2025-12-30T15:23:43Z
> **作者**: Geramy
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5817

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

I'm not sure exactly whats happening, because I havn't dug into the cmakes, but it seems like the rccl library is trying to use the /opt/rocm and the /opt/rocm library, which is your nightly build, and my install location for a easier life haha, which is fine but it seems the cmake files are confusing rccl or basically causing it not to build.

-- HIP_CONTIGUOUS_MEMORY enabled
-- HIP_UNCACHED_MEMORY enabled
-- HIP_HOST_UNCACHED_MEMORY enabled
-- --offload-compress enabled - ROCm version >= 6.2.0
-- Fault injection enabled
-- Found rocprofiler-register: /opt/rocm (found version "0.6.0")  
cat: /sys/fs/cgroup/memory.max: No such file or directory
-- Use 8 jobs for linking
-- Building shared RCCL library
Building rccl RAS client executable
-- rocm-cmake: Set license file to /home/geramyl/Documents/Programming/rccl/LICENSE.txt.
-- Configuring done (15.4s)
CMake Error in CMakeLists.txt:
  Imported target "rocm_smi64" includes non-existent path

    "/therock/output/build/third-party/sysdeps/linux/libdrm/build/stage/lib/rocm_sysdeps/lib/pkgconfig/../../include"

  in its INTERFACE_INCLUDE_DIRECTORIES.  Possible reasons include:

  * The path was deleted, renamed, or moved to another location.

  * An install or uninstall procedure did not complete successfully.

  * The installation package was faulty and references files it does not
  provide.



-- Generating done (0.0s)
CMake Warning:
  Manually-specified variables were not used by the project:

    BUILD_ROCM_SMI


### Operating System

Ubuntu Linux geramyl-MS-S1-MAX 6.14.0-1018-oem #18-Ubuntu SMP PREEMPT_DYNAMIC Wed Dec 10 09:33:29 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux

### CPU

Ryzen AI 395+ Max

### GPU

GFX1151

### ROCm Version

7.11 - nightly

### ROCm Component

rccl

### Steps to Reproduce

Install rocm nightly in /opt/rocm, set paths accordingly if needed.
Download rccl and build it.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.15
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
      Size:                    131015868(0x7cf24bc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131015868(0x7cf24bc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131015868(0x7cf24bc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131015868(0x7cf24bc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
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
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   62464                              
  Internal Node ID:        1                                  
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
      Size:                    65507932(0x3e7925c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65507932(0x3e7925c) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
*** Done ***             


### Additional Information

I am trying to work on a rccl plugin for tb5 on the gfx1151

---

## 评论 (6 条)

### 评论 #1 — huanrwan-amd (2025-12-29T20:36:06Z)

Hi @Geramy, At the moment, we do not have plans to support Strix Halo (gfx1151) for RCCL. Please stay tuned for future updates.

---

### 评论 #2 — Geramy (2025-12-29T20:40:28Z)

@huanrwan-amd right, how about the compiling problems with trying to compile rocm and rccl library as I did? 

---

### 评论 #3 — huanrwan-amd (2025-12-29T20:48:55Z)

Hi @Geramy, have you checked the build instructions? https://rocmdocs.amd.com/projects/rccl/en/latest/install/building-installing.html and the docker image here: https://github.com/ROCm/rccl/tree/develop/docker 
rccl can be compiled to other GPU architecture as here: https://github.com/ROCm/rccl/blob/develop/CMakeLists.txt

---

### 评论 #4 — Geramy (2025-12-29T20:53:02Z)

I will double check those links, thank you!
Is it possible to make PRs to add rccl support for gfx1151, or are there stoppers for the open source community such as myself to work on implementations?

---

### 评论 #5 — huanrwan-amd (2025-12-29T21:03:42Z)

Hi @Geramy, thanks for the message. In general, the open-source community contribution is welcome and be reviewed.  
To work on some specific features, e.g. supporting gfx1151, you may need AMD's IP which would not be released to open-source community. 

---

### 评论 #6 — Geramy (2025-12-29T23:45:14Z)

@huanrwan-amd right that would make sense.

---
