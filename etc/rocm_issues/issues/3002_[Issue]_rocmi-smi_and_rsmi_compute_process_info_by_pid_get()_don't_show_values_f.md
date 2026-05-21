# [Issue]: rocmi-smi and rsmi_compute_process_info_by_pid_get() don't show values for processes that don't have access to all installed GPUs (Linux)

> **Issue #3002**
> **状态**: closed
> **创建时间**: 2024-04-10T10:09:23Z
> **更新时间**: 2024-10-09T13:29:03Z
> **关闭时间**: 2024-10-09T13:29:02Z
> **作者**: maxweiss
> **标签**: Under Investigation, ROCm 5.7.1, AMD Instinct MI210
> **URL**: https://github.com/ROCm/ROCm/issues/3002

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Instinct MI210** (颜色: #ededed)

## 描述

### Problem Description

The example host has four GPUs:

```
$ rocm-smi
========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU  Temp (DieEdge)  AvgPwr  SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
0    50.0c           42.0W   800Mhz  1600Mhz  0%   auto  300.0W    0%   0%    
1    47.0c           40.0W   800Mhz  1600Mhz  0%   auto  300.0W    0%   0%    
2    42.0c           42.0W   800Mhz  1600Mhz  0%   auto  300.0W    0%   0%    
3    50.0c           43.0W   800Mhz  1600Mhz  0%   auto  300.0W    0%   0%    
====================================================================================
=============================== End of ROCm SMI Log ================================
```


rocm-smi --showpids works fine as long as the GPU process has access to all GPUs, e.g.:

We start a work binary that does some calculations on the GPU:
```
$ ./work 
[09:49:03] Forked PID: 2254756
[09:49:03][2254756] Working for 100 seconds
[09:49:03][2254756] Using OpenCL device gfx90a:sramecc+:xnack- (allocating 200M)
```

And call rocm-smi in a different shell:
```
$ rocm-smi --showpids
========================= ROCm System Management Interface =========================
================================== KFD Processes ===================================
KFD process information:
PID    	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
2254756	work        	1     	356581376	0        	9           	
====================================================================================
=============================== End of ROCm SMI Log ================================
```

But when the GPU process doesn't have access to all GPUs (see description below), rocm-smi doesn't show any values for the process.
In this case, the work binary is started inside a container that only has access to one GPU and rocm-smi is called from the host, outside of the container:

```
$ rocm-smi --showpids
========================= ROCm System Management Interface =========================
================================== KFD Processes ===================================
get_compute_process_info_by_pid, Not supported on the given system
KFD process information:
PID    	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
2674551	work        	1     	UNKNOWN  	UNKNOWN  	UNKNOWN     	
====================================================================================
=============================== End of ROCm SMI Log ================================
```

The same happens when we use the API function rsmi_compute_process_info_by_pid_get(). It doesn't report any values for the process.

### Operating System

Ubuntu 22.04.4 LTS

### CPU

AMD EPYC 7763

### GPU

AMD Instinct MI210

### ROCm Version

ROCm 5.7.1

### ROCm Component

rocm_smi_lib

### Steps to Reproduce

In two cases the GPU process doesn't have access to all GPUs:

1. Access to the GPUs is blocked via cgroups. We want to ensure that the process cannot access GPUs that are used by other processes, so we only allow access to device-files for one GPU and block the others (/dev/dri/cardX and /dev/dri/renderDX in cgroups devices.deny/devices.allow)

2. The process is running inside a container and not all GPUs were mounted into the container:

`docker run --rm -it -v /opt/work:/opt/work --device=/dev/dri/card1 --device=/dev/dri/renderD128 --device=/dev/kfd  amdopencl /bin/bash`

It looks like there are files missing in /sys/devices/virtual/kfd/kfd/proc/<pid> when the process doesn't have access to all installed GPUs:

```
$ ls /sys/devices/virtual/kfd/kfd/proc/2674551/
counters_9354  pasid  queues  sdma_9354  stats_9354  vram_9354
```

As long as the process has access to all GPUs, one file for each value/GPU is created in /sys/devices/virtual/kfd/kfd/proc/<pid>:

```
$ ls /sys/devices/virtual/kfd/kfd/proc/2254756/
counters_25466  counters_46764  counters_64925  counters_9354  pasid  queues  sdma_25466  sdma_46764  sdma_64925  sdma_9354  stats_25466  stats_46764  stats_64925  stats_9354  vram_25466  vram_46764  vram_64925  vram_9354
```

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
  Name:                    AMD EPYC 7763 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7763 64-Core Processor    
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
  Max Clock Freq. (MHz):   2450                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            128                                
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    263993980(0xfbc3a7c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    263993980(0xfbc3a7c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    263993980(0xfbc3a7c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 7763 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7763 64-Core Processor    
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
  Max Clock Freq. (MHz):   2450                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            128                                
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    264145100(0xfbe88cc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    264145100(0xfbe88cc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    264145100(0xfbe88cc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-74e9455f63e4f48f               
  Marketing Name:          AMD Instinct MI210                 
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
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   25344                              
  Internal Node ID:        2                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 78                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    67092480(0x3ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
Agent 4                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-6de8c605c2212805               
  Marketing Name:          AMD Instinct MI210                 
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   17152                              
  Internal Node ID:        3                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 78                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    67092480(0x3ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
Agent 5                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-600c883acb6a35a8               
  Marketing Name:          AMD Instinct MI210                 
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    4                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   33536                              
  Internal Node ID:        4                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 78                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    67092480(0x3ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
Agent 6                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-850e4e3c316d4738               
  Marketing Name:          AMD Instinct MI210                 
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    5                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   41728                              
  Internal Node ID:        5                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 78                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    67092480(0x3ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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

## 评论 (7 条)

### 评论 #1 — maxweiss (2024-04-10T10:16:58Z)

It looks like the function `amd::smi::GetProcessInfoForPID` returns too early when the files are missing in /sys/devices/virtual/kfd/kfd/proc/. But I'm not sure if changing this function to just ignore the missing files would have any side effects.

---

### 评论 #2 — nartmada (2024-04-11T15:51:09Z)

Internal ticket has been created for investigation.

---

### 评论 #3 — akondrat-amd (2024-04-19T02:02:27Z)

Can you try the latest ROCm 6.1.0? It seems that this issue was just fixed. From CHANGELOG.md:

* Fixed `--showpids` reporting `[PID] [PROCESS NAME] 1 UNKNOWN UNKNOWN UNKNOWN`.
  Output was failing because `cu_occupancy debugfs` method is not provided on some graphics cards
  by design. `get_compute_process_info_by_pid` was updated to reflect this and returns with the output
  needed by the CLI.

---

### 评论 #4 — maxweiss (2024-04-21T16:35:24Z)

Unfortunately, ROCm 6.1.0 has the same issue.

The host has four GPUs, but we mount only one into the container:

```
$ docker run --rm -it -v /opt/work:/opt/work --device=/dev/dri/card1 --device=/dev/dri/renderD128 --device=/dev/kfd  amdopencl /bin/bash
root@e9a753b3895f:/tmp/amd-opencl# /opt/work/work_amd 
[16:31:28][9] Could not load CUDA library libcuda.so
[16:31:28][9] Successfully loaded OpenCL library libOpenCL.so.1
[16:31:28] Forked PID: 11
[16:31:28][11] Working for 100 seconds (GPU 0)
[16:31:28][11] Using OpenCL device gfx90a:sramecc+:xnack- (allocating 200M)
```

Called from outside the container, `rocm-smi --showpids` shows "UNKNOWN" for most values:

```
$ rocm-smi --version
ROCM-SMI version: 2.0.0+8e78352
ROCM-SMI-LIB version: 7.0.0
$ rocm-smi --showpids


============================ ROCm System Management Interface ============================
===================================== KFD Processes ======================================
get_compute_process_info_by_pid, Not supported on the given system
KFD process information:
PID   	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
846909	work_amd    	1     	UNKNOWN  	UNKNOWN  	UNKNOWN     	
==========================================================================================
================================== End of ROCm SMI Log ===================================
```
`rsmi_compute_process_info_by_pid_get()` for the PID returns `RSMI_STATUS_NOT_SUPPORTED`.

As mentioned in the initial problem description, `rocm-smi --showpids` works fine if we mount all available GPUs into the container:

```
$ docker run --rm -it -v /opt/work:/opt/work --device=/dev/dri/ --device=/dev/kfd  amdopencl /bin/bash
root@ccdad0890ca0:/tmp/amd-opencl# /opt/work/work_amd 
[16:33:26][9] Could not load CUDA library libcuda.so
[16:33:26][9] Successfully loaded OpenCL library libOpenCL.so.1
[16:33:26] Forked PID: 11
[16:33:26][11] Working for 100 seconds (GPU 0)
[16:33:26][11] Using OpenCL device gfx90a:sramecc+:xnack- (allocating 200M)
```

Called from outside the container:

```
$ rocm-smi --showpids


============================ ROCm System Management Interface ============================
===================================== KFD Processes ======================================
KFD process information:
PID   	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
858113	work_amd    	1     	356581376	0        	14          	
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

(The same happens when we block access to some GPUs via cgroups)

---

### 评论 #5 — yx-lamini (2024-08-24T01:02:31Z)

6.2.0 also have the same issue https://github.com/ROCm/ROCm/issues/2595#issuecomment-2307966592

I'd like to emphasize that the ability to monitor CU occupancy is critical for almost all of the AI use cases on GPUs. It's been many releases already, and this issue still lingers.

Please consider fix

---

### 评论 #6 — jamesxu2 (2024-08-28T20:11:07Z)

Hi @maxweiss , I was able to reproduce your issue and confirm this theory:
> It looks like the function amd::smi::GetProcessInfoForPID returns too early when the files are missing in /sys/devices/virtual/kfd/kfd/proc/. But I'm not sure if changing this function to just ignore the missing files would have any side effects.

Thanks for the lead and for the meticulous issue report. [A PR has been made](https://github.com/ROCm/rocm_smi_lib/pull/194) to resolve this issue.

---

### 评论 #7 — jamesxu2 (2024-10-09T13:29:03Z)

Just an update @maxweiss and @yx-lamini , this issue has been resolved and the above PR has been merged internally. The content of the change is available in the public PR for reference.

This fix will be available in a future version of ROCm. Thanks for your help @maxweiss!



---
