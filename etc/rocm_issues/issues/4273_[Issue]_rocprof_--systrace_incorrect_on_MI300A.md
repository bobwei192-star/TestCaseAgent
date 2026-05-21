# [Issue]: rocprof --systrace incorrect on MI300A

> **Issue #4273**
> **状态**: closed
> **创建时间**: 2025-01-19T21:40:09Z
> **更新时间**: 2025-07-09T18:57:19Z
> **关闭时间**: 2025-07-09T18:48:49Z
> **作者**: fluidnumericsJoe
> **标签**: Under Investigation, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4273

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

iIn working with a rather [simple example](https://github.com/FluidNumerics/Hipfort_Course/blob/main/course_material/L5_hipFORT_Examples/tensoradd_hip_fptr.f90) wherein

* Three host pointers are allocated (system allocator - Fortran `allocate`)
* Three device pointers are allocated (`hipMalloc`)
* Host pointers are initialized with random values
* Host data is copied to device for two of the pointers (`hipMemcpy`)
* A kernel is launched to add two arrays and populate the fields for the third array
* Device data for the result array is copied back to the host pointer (`hipMemcpy`)
* Result is checked for correctness.


The point of this exercise is to learn how existing HIP code for discrete GPU systems would work on MI300A hardware. The code appears to run correctly and obtain the correct results. As a part of this exercise, I looked into a trace profile using `rocprof --sys-trace`. A screenshot of the visualized trace profile (with ui.perfetto.dev) is shown below. I've also attached the corresponding `results.json` generated from the trace profile.

![Image](https://github.com/user-attachments/assets/eb5dbb8c-3c21-4e5e-a67a-da7bab9d4e90)

The trace profile shows the kernel is launched before two host-to-device memcpy's are executed and the final device-to-host memcpy is not shown. Indeed, digging through the `results.json` trace profile, I see the following

```
$ grep hipMemcpy results.json 
,{"ph":"X","name":"hipMemcpy","pid":2,"tid":1539475,"ts":"692706293048","dur":"269063",
    "Name":"hipMemcpy",
,{"ph":"X","name":"hipMemcpy","pid":2,"tid":1539475,"ts":"692706562129","dur":"1010",
    "Name":"hipMemcpy",
,{"ph":"X","name":"hipMemcpy","pid":2,"tid":1539475,"ts":"692706564173","dur":"27838",
    "Name":"hipMemcpy",
```

```
$ grep Copy results.json
,{"ph":"X","name":"CopyHostToDevice","pid":1,"tid":0,"ts":"692706620838","dur":"4",
    "Name":"CopyHostToDevice",
,{"ph":"X","name":"CopyHostToDevice","pid":1,"tid":0,"ts":"692706621993","dur":"3",
    "Name":"CopyHostToDevice",
,{"ph":"X","name":"CopyDeviceToHost","pid":1,"tid":0,"ts":"692706650780","dur":"4",
    "Name":"CopyDeviceToHost",
```

```
$ grep tensor results.json
    "args":"( kernel(tensoradd_2D(float*, float*, float*, int, int)) function_address(0x206dc0) numBlocks({z(1) y(2) x(2}) dimBlocks({z(1) y(8) x(8}) args(0x7ffd1c522b88) sharedMemBytes(0) stream(1))",
,{"ph":"X","name":"tensoradd_2D(float*, float*, float*, int, int)","pid":10,"tid":1,"ts":"692706564056","dur":"2",
    "Name":"tensoradd_2D(float*, float*, float*, int, int)",
```

From the timestamps, indeed, we see that the `tensoradd_2D` kernel is observed by rocprof to launch before the `CopyHostToDevice` calls. This doesn't quite make sense, given that the executed code obtains the correct results.

There's a couple things here to resolve

* Why is the order of operations seemingly not captured correctly with `rocprof --sys-trace` ? Please tell me I'm missing something obvious.
* Why is the `CopyDeviceToHost` call shown in the `results.json` file but not showing up on perfetto at all ?


[results.json](https://github.com/user-attachments/files/18470510/results.json)
[results.stats.csv](https://github.com/user-attachments/files/18470511/results.stats.csv)

### Operating System

Rocky Linux 9.5

### CPU

AMD MI300A

### GPU

AMD MI300A

### ROCm Version

ROCm 6.3.1

### ROCm Component

rocprofiler

### Steps to Reproduce

If you'd like to reproduce this on an MI300A platform, you will need to build the code in the [HIPFort_Course Repository](https://github.com/FluidNumerics/Hipfort_Course/). You will need ROCm 6.3.1 and `cmake` and to do the following

```
export FC=$(which amdflang)
export CC=$(which amdclang)
export CXX=$(which amdclang++)
export HIP_PLATFORM=amd
export GPU_ARCH=gfx942
export HIPFORT_COMPILER=$(which amdflang)

git clone https://github.com/fluidnumerics/HIPFort_Course ~/HIPFort_Course
mkdir -p ~/HIPFort_Course/build 
cd ~/HIPFort_Course/build
cmake ../ -DCMAKE_INSTALL_PREFIX=~/HIPFort_Course/install
make
make install
cd ~/HIPFort_Course/install/bin
rocprof --sys-trace ./tensoradd_hip_fptr
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.10.5 is loaded
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
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
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
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    130753312(0x7cb2320) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130753312(0x7cb2320) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    130753312(0x7cb2320) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    130753312(0x7cb2320) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131809008(0x7db3ef0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131809008(0x7db3ef0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131809008(0x7db3ef0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131809008(0x7db3ef0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        2                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131765224(0x7da93e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131765224(0x7da93e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131765224(0x7da93e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131765224(0x7da93e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 4                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        3                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131795444(0x7db09f4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131795444(0x7db09f4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131795444(0x7db09f4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131795444(0x7db09f4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 5                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-b8e0078991ff9d4d               
  Marketing Name:          AMD Instinct MI300A                
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
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   256                                
  Internal Node ID:        4                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
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
  Packet Processor uCode:: 166                                
  SDMA engine uCode::      22                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98648060(0x5e13ffc) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
  Name:                    gfx942                             
  Uuid:                    GPU-eaa69826c47efb9c               
  Marketing Name:          AMD Instinct MI300A                
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
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   16640                              
  Internal Node ID:        5                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
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
  Packet Processor uCode:: 166                                
  SDMA engine uCode::      22                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98648060(0x5e13ffc) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
Agent 7                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-b88af96f2664a354               
  Marketing Name:          AMD Instinct MI300A                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    6                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   33024                              
  Internal Node ID:        6                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
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
  Packet Processor uCode:: 166                                
  SDMA engine uCode::      22                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98648060(0x5e13ffc) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
Agent 8                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-1aa50edc8434308c               
  Marketing Name:          AMD Instinct MI300A                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    7                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   49408                              
  Internal Node ID:        7                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
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
  Packet Processor uCode:: 166                                
  SDMA engine uCode::      22                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98648060(0x5e13ffc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98648060(0x5e13ffc) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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

_No response_

---

## 评论 (21 条)

### 评论 #1 — harkgill-amd (2025-01-20T17:22:00Z)

Hi @fluidnumerics-joe, thanks for the report and providing concise steps to reproduce. An internal ticket has been opened to further investigate this issue.

---

### 评论 #2 — tcgu-amd (2025-01-20T21:06:21Z)

Hi @fluidnumerics-joe, thanks for reaching out! We are in the process of reproducing your issue right now. 

While reproducing, I noticed a small issue; in your script, you seem to have 

```
export GPU_ARCH=gfx90a
```

But you seem to be using MI300A, which should correspond to LLVM target of gfx942. If you are experiencing unexpected behaviors, this could partially contribute to it. 

Thanks! 

Edit: Here is a [helpful link](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus) for all the gpu llvm targets. 

---

### 评论 #3 — fluidnumericsJoe (2025-01-20T21:40:07Z)

Hey @tcgu-amd , when we ran this on our system, we use a [build script](https://github.com/FluidNumerics/Hipfort_Course/blob/main/install.sh) that sources this [env file](
https://github.com/FluidNumerics/Hipfort_Course/blob/main/env). 

The system name is `nicholson` where we have set the environment variable for the architecture code to `gfx942` (See https://github.com/FluidNumerics/Hipfort_Course/blob/main/env#L42 )

I manually typed up the steps to reproduce after spending hours trying to understand what could possibly be wrong with code released by AMD. Thanks for sharing the GPU  LLVM targets; I'm quite aware of the architecture codes but made a simple mistake in attempting to write up steps for you to reproduce.


---

### 评论 #4 — tcgu-amd (2025-01-20T21:42:11Z)

> Hey [@tcgu-amd](https://github.com/tcgu-amd) , when we ran this on our system, we use a [build script](https://github.com/FluidNumerics/Hipfort_Course/blob/main/install.sh) that sources this [env file](https://github.com/FluidNumerics/Hipfort_Course/blob/main/env).
> 
> The system name is `nicholson` where we have set the environment variable for the architecture code to `gfx942` (See https://github.com/FluidNumerics/Hipfort_Course/blob/main/env#L42 )
> 
> I manually typed up the steps to reproduce after spending hours trying to understand what could possibly be wrong with code released by AMD. Thanks for sharing the GPU LLVM targets; I'm quite aware of the architecture codes but made a simple mistake in attempting to write up steps for you to reproduce.

Ah, got it! That makes more sense now. Thanks for clarifying! :)

---

### 评论 #5 — tcgu-amd (2025-01-21T16:57:58Z)

Hi @fluidnumerics-joe, bit of an update: we tried but cannot seem to reproduce your issue. 

Edit: Clarification, the following was done on a **MI300X**. We will continue to investigate the issue on MI300A.

Here is the steps we took: 

1. We ran the instruction you provided with slight modifications (mostly for directory handling)
```
export FC=$(which amdflang)
export CC=$(which amdclang)
export CXX=$(which amdclang++)
export HIP_PLATFORM=amd
export GPU_ARCH=gfx942
export HIPFORT_COMPILER=$(which amdflang)

git clone https://github.com/fluidnumerics/Hipfort_Course ./Hipfort_Course
mkdir -p Hipfort_Course/build
cd Hipfort_Course/build
cmake ../ -DCMAKE_INSTALL_PREFIX=$(pwd)/../install -DCMAKE_PREFIX_PATH=/opt/rocm
make
make install
cd $(pwd)/../install/bin
rocprof --sys-trace ./tensoradd_hip_fptr
```

1. We obtained the following results
  hipMemcpy:
  
  ,{"ph":"X","name":"hipMemcpy","pid":2,"tid":356321,"ts":"149351969936","dur":"185230",
      "Name":"hipMemcpy",
  ,{"ph":"X","name":"hipMemcpy","pid":2,"tid":356321,"ts":"149352155177","dur":"221",
      "Name":"hipMemcpy",
  ,{"ph":"X","name":"hipMemcpy","pid":2,"tid":356321,"ts":"149352158992","dur":"838",
      "Name":"hipMemcpy",
  
  Copy: 
  
  ,{"ph":"X","name":"CopyHostToDevice","pid":1,"tid":0,"ts":"149352155112","dur":"8",
      "Name":"CopyHostToDevice",
  ,{"ph":"X","name":"CopyHostToDevice","pid":1,"tid":0,"ts":"149352155372","dur":"7",
      "Name":"CopyHostToDevice",
  ,{"ph":"X","name":"CopyDeviceToHost","pid":1,"tid":0,"ts":"149352159770","dur":"8",
      "Name":"CopyDeviceToHost",
  
  tensor: 
  
      "args":"( kernel(tensoradd_2D(float*, float*, float*, int, int)) function_address(0x201f00) numBlocks({z(1) y(2) x(2}) dimBlocks({z(1) y(8) x(8}) args(0x7ffe718c2ae8) sharedMemBytes(0) stream(1))",
  ,{"ph":"X","name":"tensoradd_2D(float*, float*, float*, int, int)","pid":9,"tid":1,"ts":"149352158681","dur":"294",
      "Name":"tensoradd_2D(float*, float*, float*, int, int)",
  
  Which translates to the call order:
  
  hipMemcpy -> CopyHostToDevice -> hipMemcpy -> CopyHostToDevice -> tensoradd_2D -> hipMemcpy -> CopyDeviceToHost

 Which appears to be correct.

3. we capture the following (zoomed in) screenshot from perfetto
![Image](https://github.com/user-attachments/assets/8f148c61-836c-4d20-ae11-cf63c8c340e9)

*I think the reason why perfectto is not showing some events could be that they are too short -- you might need to zoom in a little.

Currently, we are not quite sure what might be causing the discrepancy. We will continue to investigate to see if there's anything else we can find. Please keep us posted on new discoveries as well. Thanks! 

---

### 评论 #6 — tcgu-amd (2025-01-21T17:07:30Z)

Hi @fluidnumerics-joe, would you be able to run rocprof with HSA_ENABLE_SDMA=0 and see if the issue persists? Thanks!

---

### 评论 #7 — tcgu-amd (2025-01-24T15:11:51Z)

Hi @fluidnumerics-joe, this seems like an known issue with MI300A. A fix has been made and will be available in the future. For now, please see if using HSA_ENABLE_SDMA=0 will fix the issue. Thanks!

---

### 评论 #8 — fluidnumericsJoe (2025-01-24T15:53:26Z)

Hey @tcgu-amd ; I'll give this a go today and get back to you this afternoon.

---

### 评论 #9 — fluidnumericsJoe (2025-01-24T15:53:59Z)

Are you able to comment on this issue a bit more ? I was not aware that this was "known"

---

### 评论 #10 — tcgu-amd (2025-01-24T16:13:14Z)

> Are you able to comment on this issue a bit more ? I was not aware that this was "known"

@fluidnumerics-joe, sorry, I should have clarified "known" means we are aware of the bug internally. Unfortunately, since the fix involves lower level drivers outside the scope for ROCm itself, I am unable to provide too much details at the moment. 

---

### 评论 #11 — fluidnumericsJoe (2025-01-24T18:26:23Z)

Can confirm that setting `HSA_ENABLE_SDMA=0` fixes the issue. What is it about the MI300A SDMA engine that causes a problem ? 

![Image](https://github.com/user-attachments/assets/36e39ce1-1ff9-44f5-8afb-77607c00b68f)

---

### 评论 #12 — tcgu-amd (2025-01-27T15:29:58Z)

@fluidnumerics-joe, I would love to provide more details; however, since the issue does not originate from the ROCm stack, I do not have a lot of information at hand either. That being said, once the patch becomes available, more information should come along. 

---

### 评论 #13 — ruizhe-ops (2025-01-29T07:11:52Z)

The issues you encountered with `rocprof --sys-trace` on the MI300A platform can be analyzed as follows:

### 1. **Incorrect Order of Operations in the Trace**  
The trace shows the kernel (`tensoradd_2D`) launching before the `CopyHostToDevice` operations, even though the code executes correctly. This discrepancy likely stems from:  
- **Asynchronous Execution and Queueing**:  
  In ROCm, kernel launches and memory copies are asynchronous by default. The HIP runtime may enqueue kernel execution commands before completing all preceding `hipMemcpy` operations, especially if they are not explicitly synchronized. The `rocprof` tool records events based on when they are submitted to queues (e.g., HSA queues), not necessarily their actual execution order on hardware.  
  - For example, the kernel launch command might be submitted to a compute queue while memory copies are handled by a separate DMA engine, leading to overlapping timelines in the trace.  

- **Timestamp Synchronization Issues**:  
  The `results.json` timestamps indicate the kernel (`ts=692706564056`) starts slightly before the first `CopyHostToDevice` (`ts=692706620838`). This could result from clock domain differences between the CPU and GPU or synchronization gaps in the profiling tool itself.  

- **Tool Limitations in MI300A**:  
  ROCm 6.3.1’s `rocprof` (V1) might not fully account for the MI300A’s APU architecture, which integrates CPU and GPU on the same die. The unified memory model could lead to non-intuitive tracing behavior compared to discrete GPUs.  

### 2. **Missing `CopyDeviceToHost` in Perfetto Visualization**  
The `CopyDeviceToHost` event exists in `results.json` but does not appear in Perfetto due to:  
- **Event Filtering or Rendering Artifacts**:  
  Perfetto might collapse very short-duration events (e.g., `dur=4` in `CopyDeviceToHost`) if the zoom level is too wide or if the UI filters out low-duration events.  
  - **Solution**: Zoom into the timeline around `ts=692706650780` or check if the event is categorized under a different track (e.g., a separate thread or process).  

- **Metadata Mismatch**:  
  The `CopyDeviceToHost` event in `results.json` has `pid=1` and `tid=0`, while the kernel runs on `pid=10` and `tid=1`. Perfetto might group events by process/thread, causing the copy operation to appear in a less visible track.  

### Recommendations  
1. **Explicit Synchronization**:  
   Add `hipDeviceSynchronize()` or `hipStreamSynchronize()` after memory copies to enforce execution order and validate if the trace aligns with the code logic.  

2. **Upgrade to ROCm 6.3.1+ or rocprofv2**:  
   ROCm 6.3.1 includes updates for MI300A support, and `rocprofv2` (beta) offers improved tracing accuracy. Try reprofiling with:  
   ```bash
   rocprof --tool-version 2 --sys-trace ./tensoradd_hip_fptr
   ```  
   .  

3. **Inspect Raw Timestamps**:  
   Use `results.json` timestamps directly to verify event ordering, as visualization tools like Perfetto might abstract temporal relationships.  

4. **Check for Known Issues**:  
   The MI300A’s APU architecture may require specific OS settings (e.g., GRUB `pci=realloc=off`, NUMA balancing disabled) to ensure proper profiling.  

If the issue persists, consider filing a bug report with AMD ROCm, including the `results.json` and environment details.

---

### 评论 #14 — fluidnumericsJoe (2025-01-29T09:20:47Z)

@ruizhe-ops - this reaks of AI generated slop based on the first post and none of the discussion beneath.


> In ROCm, kernel launches and memory copies are asynchronous by default. The HIP runtime may enqueue kernel execution commands before completing all preceding hipMemcpy operations, especially if they are not explicitly synchronized. The rocprof tool records events based on when they are submitted to queues (e.g., HSA queues), not necessarily their actual execution order on hardware.

Since when are kernel launches and `hipMemcpy` on the default stream asynchronous be default? `rocprof` records HSA, HIP API call, and kernel start and duration. In every other GPU I've used from AMD these details have been recorded in the correct/expected order. This explanation appears to be an attempt to sidestep admission of a major bug in rocprof on AMD's flagship hardware on El Capitan.


---

### 评论 #15 — tcgu-amd (2025-01-29T14:53:09Z)

Hi @fluidnumerics-joe, @ruizhe-ops is a recognized spam user that has been posting AI-generated answers across multiple issues part of ROCm. Please disregard their answers. Thanks. 

---

### 评论 #16 — fluidnumericsJoe (2025-03-10T18:57:44Z)

Hey @tcgu-amd - Can you comment on where this issue originates from ? Is this within the AMDGPU driver ?

---

### 评论 #17 — fluidnumericsJoe (2025-03-27T14:03:32Z)

Giving this a bump. @tcgu-amd @harkgill-amd , While using the blit kernels is a fine work-around,  is there currently an ETA expected for a fix on this issue ?

---

### 评论 #18 — fluidnumericsJoe (2025-04-03T19:26:48Z)

Giving this another bump. @tcgu-amd @harkgill-amd , While using the blit kernels is a fine work-around, is there currently an ETA expected for a fix on this issue ?

If you need reliable access to an MI300A system to help resolve this issue, Fluid Numerics can provide time on our system

---

### 评论 #19 — tcgu-amd (2025-07-09T18:48:49Z)

@fluidnumerics-joe, the fix is scheduled to be available soon. Moving on, we will be tracking the release schedule through this issue https://github.com/ROCm/ROCm/issues/4079. 

The current issue will be closed. Thanks! 

---

### 评论 #20 — fluidnumericsJoe (2025-07-09T18:52:36Z)

I wouldn't say that this is closed if a fix hasn't been released. Is this something that will come from AMD via ROCm or from Supermicro as a firmware fix ?

---

### 评论 #21 — tcgu-amd (2025-07-09T18:57:07Z)

> I wouldn't say that this is closed if a fix hasn't been released. Is this something that will come from AMD via ROCm or from Supermicro as a firmware fix ?

The fix is going to be delivered via an SBIO update. 

And yes -- we just have a bunch of tickets that all underpins the same issue, so right now we are just trying to remove duplicates. Thanks for understanding! 

---
