# [Issue]: clCreateCommandQueueWithProperties returning CL_OUT_OF_HOST_MEMORY error on WSL

> **Issue #5675**
> **状态**: closed
> **创建时间**: 2025-11-18T03:26:36Z
> **更新时间**: 2026-01-05T16:04:40Z
> **关闭时间**: 2026-01-05T16:04:40Z
> **作者**: Tilroe
> **标签**: ROCm on WSL, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5675

## 标签

- **ROCm on WSL** (颜色: #7CE964)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

First of all, apologies if this is considered a duplicate issue post. I've posted this in the [ROCm/clr](https://github.com/ROCm/clr) repo as well ROCm/clr#261, but since that repo is marked as retired, I wasn't sure if anyone was keeping track of issues over there. 

clCreateCommandQueueWithProperties is returning CL_OUT_OF_HOST_MEMORY in the error code on my WSL toolchain (gcc/gdb). No such error when done locally on Windows toolchain (minGW). Additionally, this issue only seems to happen under the debug configuration, leading me to believe that the issue is some interference with gdb.

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat) (WSL)

### CPU

AMD Ryzen 9 7950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.4.2

### ROCm Component

clr

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
WSL environment detected.
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.7
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
  Name:                    AMD Ryzen 9 7950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X 16-Core Processor
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
  Cacheline Size:          64(0x40)                           
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    15931524(0xf31884) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15931524(0xf31884) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    15931524(0xf31884) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15931524(0xf31884) KB              
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
  Marketing Name:          AMD Radeon RX 7900 XTX             
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2371                               
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 552                                
  SDMA engine uCode::      24                                 
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***
```

### Additional Information

Compiled libraries were installed following [this page](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html)

---

## 评论 (16 条)

### 评论 #1 — schung-amd (2025-11-19T15:50:03Z)

Hi @Tilroe, thanks for the report. No problem having duplicated issues across different repos IMO, we can always tidy things up if necessary.

What version of the Adrenalin driver do you have? Also, can you provide the output of `clinfo` in both your native Windows environment and your WSL environment? 

---

### 评论 #2 — Tilroe (2025-11-19T17:42:16Z)

> Hi [@Tilroe](https://github.com/Tilroe), thanks for the report. No problem having duplicated issues across different repos IMO, we can always tidy things up if necessary.
> 
> What version of the Adrenalin driver do you have? Also, can you provide the output of `clinfo` in both your native Windows environment and your WSL environment?

### Adrenalin Driver Version
25.11.1

### Windows clinfo output
```
Number of platforms:                             2
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3661.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_khr_d3d10_sharing cl_khr_d3d11_sharing cl_khr_dx9_media_sharing cl_amd_event_callback cl_amd_offline_devices
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3652.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_khr_d3d10_sharing cl_khr_d3d11_sharing cl_khr_dx9_media_sharing cl_amd_event_callback cl_amd_offline_devices


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon RX 7900 XTX
  Device Topology:                               PCI[ B#3, D#0, F#0 ]
  Max compute units:                             48
  Max work items dimensions:                     3
    Max work items[0]:                           1024
    Max work items[1]:                           1024
    Max work items[2]:                           1024
  Max work group size:                           256
  Preferred vector width char:                   4
  Preferred vector width short:                  2
  Preferred vector width int:                    1
  Preferred vector width long:                   1
  Preferred vector width float:                  1
  Preferred vector width double:                 1
  Native vector width char:                      4
  Native vector width short:                     2
  Native vector width int:                       1
  Native vector width long:                      1
  Native vector width float:                     1
  Native vector width double:                    1
  Max clock frequency:                           2371Mhz
  Address bits:                                  64
  Max memory allocation:                         21890072576
  Image support:                                 Yes
  Max number of images read arguments:           128
  Max number of images write arguments:          64
  Max image 2D width:                            16384
  Max image 2D height:                           16384
  Max image 3D width:                            2048
  Max image 3D height:                           2048
  Max image 3D depth:                            2048
  Max samplers within kernel:                    16
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              2048
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     Yes
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               Yes
    Round to +ve and infinity:                   Yes
    IEEE754-2008 fused multiply-add:             Yes
  Cache type:                                    Read/Write
  Cache line size:                               64
  Cache size:                                    16384
  Global memory size:                            25753026560
  Constant buffer size:                          21890072576
  Max number of constant args:                   8
  Local memory type:                             Local
  Local memory size:                             32768
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          415236096
  Max global variable size:                      19701065216
  Max global variable preferred total size:      25753026560
  Max read/write image args:                     64
  Max on device events:                          1024
  Queue on device max size:                      8388608
  Max on device queues:                          1
  Queue on device preferred size:                262144
  SVM capabilities:
    Coarse grain buffer:                         Yes
    Fine grain buffer:                           Yes
    Fine grain system:                           No
    Atomics:                                     No
  Preferred platform atomic alignment:           0
  Preferred global atomic alignment:             0
  Preferred local atomic alignment:              0
  Kernel Preferred work group size multiple:     32
  Error correction support:                      0
  Unified memory for Host and Device:            0
  Profiling timer resolution:                    1
  Device endianess:                              Little
  Available:                                     Yes
  Compiler available:                            Yes
  Execution capabilities:
    Execute OpenCL kernels:                      Yes
    Execute native function:                     No
  Queue on Host properties:
    Out-of-Order:                                No
    Profiling :                                  Yes
  Queue on Device properties:
    Out-of-Order:                                Yes
    Profiling :                                  Yes
  Platform ID:                                   00007FFC928FE490
  Name:                                          gfx1100
  Vendor:                                        Advanced Micro Devices, Inc.
  Device OpenCL C version:                       OpenCL C 2.0
  Driver version:                                3661.0 (PAL,LC)
  Profile:                                       FULL_PROFILE
  Version:                                       OpenCL 2.0 AMD-APP (3661.0)
  Extensions:                                    cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_d3d10_sharing cl_khr_d3d11_sharing cl_khr_dx9_media_sharing cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_gl_event cl_khr_depth_images cl_khr_mipmap_image cl_khr_mipmap_image_writes cl_amd_copy_buffer_p2p cl_amd_planar_yuv


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               2
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon RX 7900 XTX
  Device Topology:                               PCI[ B#3, D#0, F#0 ]
  Max compute units:                             48
  Max work items dimensions:                     3
    Max work items[0]:                           1024
    Max work items[1]:                           1024
    Max work items[2]:                           1024
  Max work group size:                           256
  Preferred vector width char:                   4
  Preferred vector width short:                  2
  Preferred vector width int:                    1
  Preferred vector width long:                   1
  Preferred vector width float:                  1
  Preferred vector width double:                 1
  Native vector width char:                      4
  Native vector width short:                     2
  Native vector width int:                       1
  Native vector width long:                      1
  Native vector width float:                     1
  Native vector width double:                    1
  Max clock frequency:                           2371Mhz
  Address bits:                                  64
  Max memory allocation:                         21890072576
  Image support:                                 Yes
  Max number of images read arguments:           128
  Max number of images write arguments:          64
  Max image 2D width:                            16384
  Max image 2D height:                           16384
  Max image 3D width:                            2048
  Max image 3D height:                           2048
  Max image 3D depth:                            2048
  Max samplers within kernel:                    16
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              2048
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     Yes
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               Yes
    Round to +ve and infinity:                   Yes
    IEEE754-2008 fused multiply-add:             Yes
  Cache type:                                    Read/Write
  Cache line size:                               64
  Cache size:                                    16384
  Global memory size:                            25753026560
  Constant buffer size:                          21890072576
  Max number of constant args:                   8
  Local memory type:                             Local
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          415236096
  Max global variable size:                      19701065216
  Max global variable preferred total size:      25753026560
  Max read/write image args:                     64
  Max on device events:                          1024
  Queue on device max size:                      8388608
  Max on device queues:                          1
  Queue on device preferred size:                262144
  SVM capabilities:
    Coarse grain buffer:                         Yes
    Fine grain buffer:                           Yes
    Fine grain system:                           No
    Atomics:                                     No
  Preferred platform atomic alignment:           0
  Preferred global atomic alignment:             0
  Preferred local atomic alignment:              0
  Kernel Preferred work group size multiple:     32
  Error correction support:                      0
  Unified memory for Host and Device:            0
  Profiling timer resolution:                    1
  Device endianess:                              Little
  Available:                                     Yes
  Compiler available:                            Yes
  Execution capabilities:
    Execute OpenCL kernels:                      Yes
    Execute native function:                     No
  Queue on Host properties:
    Out-of-Order:                                No
    Profiling :                                  Yes
  Queue on Device properties:
    Out-of-Order:                                Yes
    Profiling :                                  Yes
  Platform ID:                                   00007FFC90041000
  Name:                                          gfx1100
  Vendor:                                        Advanced Micro Devices, Inc.
  Device OpenCL C version:                       OpenCL C 2.0
  Driver version:                                3652.0 (PAL,LC)
  Profile:                                       FULL_PROFILE
  Version:                                       OpenCL 2.0 AMD-APP (3652.0)
  Extensions:                                    cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_d3d10_sharing cl_khr_d3d11_sharing cl_khr_dx9_media_sharing cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_gl_event cl_khr_depth_images cl_khr_mipmap_image cl_khr_mipmap_image_writes cl_amd_copy_buffer_p2p cl_amd_planar_yuv


  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon(TM) Graphics
  Device Topology:                               PCI[ B#26, D#0, F#0 ]
  Max compute units:                             1
  Max work items dimensions:                     3
    Max work items[0]:                           1024
    Max work items[1]:                           1024
    Max work items[2]:                           1024
  Max work group size:                           256
  Preferred vector width char:                   4
  Preferred vector width short:                  2
  Preferred vector width int:                    1
  Preferred vector width long:                   1
  Preferred vector width float:                  1
  Preferred vector width double:                 1
  Native vector width char:                      4
  Native vector width short:                     2
  Native vector width int:                       1
  Native vector width long:                      1
  Native vector width float:                     1
  Native vector width double:                    1
  Max clock frequency:                           2200Mhz
  Address bits:                                  64
  Max memory allocation:                         10661759385
  Image support:                                 Yes
  Max number of images read arguments:           128
  Max number of images write arguments:          64
  Max image 2D width:                            16384
  Max image 2D height:                           16384
  Max image 3D width:                            2048
  Max image 3D height:                           2048
  Max image 3D depth:                            2048
  Max samplers within kernel:                    16
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              2048
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     Yes
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               Yes
    Round to +ve and infinity:                   Yes
    IEEE754-2008 fused multiply-add:             Yes
  Cache type:                                    Read/Write
  Cache line size:                               64
  Cache size:                                    16384
  Global memory size:                            13080117248
  Constant buffer size:                          10661759385
  Max number of constant args:                   8
  Local memory type:                             Local
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          2071824793
  Max global variable size:                      9595583232
  Max global variable preferred total size:      13080117248
  Max read/write image args:                     64
  Max on device events:                          1024
  Queue on device max size:                      8388608
  Max on device queues:                          1
  Queue on device preferred size:                262144
  SVM capabilities:
    Coarse grain buffer:                         Yes
    Fine grain buffer:                           Yes
    Fine grain system:                           No
    Atomics:                                     No
  Preferred platform atomic alignment:           0
  Preferred global atomic alignment:             0
  Preferred local atomic alignment:              0
  Kernel Preferred work group size multiple:     32
  Error correction support:                      0
  Unified memory for Host and Device:            1
  Profiling timer resolution:                    1
  Device endianess:                              Little
  Available:                                     Yes
  Compiler available:                            Yes
  Execution capabilities:
    Execute OpenCL kernels:                      Yes
    Execute native function:                     No
  Queue on Host properties:
    Out-of-Order:                                No
    Profiling :                                  Yes
  Queue on Device properties:
    Out-of-Order:                                Yes
    Profiling :                                  Yes
  Platform ID:                                   00007FFC90041000
  Name:                                          gfx1036
  Vendor:                                        Advanced Micro Devices, Inc.
  Device OpenCL C version:                       OpenCL C 2.0
  Driver version:                                3652.0 (PAL,LC)
  Profile:                                       FULL_PROFILE
  Version:                                       OpenCL 2.0 AMD-APP (3652.0)
  Extensions:                                    cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_d3d10_sharing cl_khr_d3d11_sharing cl_khr_dx9_media_sharing cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_gl_event cl_khr_depth_images cl_khr_mipmap_image cl_khr_mipmap_image_writes cl_amd_copy_buffer_p2p cl_amd_planar_yuv
```

### WSL clinfo output
```
Number of platforms                               1
  Platform Name                                   AMD Accelerated Parallel Processing
  Platform Vendor                                 Advanced Micro Devices, Inc.
  Platform Version                                OpenCL 2.1 AMD-APP (3649.0)
  Platform Profile                                FULL_PROFILE
  Platform Extensions                             cl_khr_icd cl_amd_event_callback
  Platform Extensions function suffix             AMD
  Platform Host timer resolution                  1ns

  Platform Name                                   AMD Accelerated Parallel Processing
Number of devices                                 1
  Device Name                                     gfx1100
  Device Vendor                                   Advanced Micro Devices, Inc.
  Device Vendor ID                                0x1002
  Device Version                                  OpenCL 2.0
  Driver Version                                  3649.0 (HSA1.1,LC)
  Device OpenCL C Version                         OpenCL C 2.0
  Device Type                                     GPU
  Device Board Name (AMD)                         AMD Radeon RX 7900 XTX
  Device PCI-e ID (AMD)                           0x744c
  Device Topology (AMD)                           PCI-E, 0000:03:00.0
  Device Profile                                  FULL_PROFILE
  Device Available                                Yes
  Compiler Available                              Yes
  Linker Available                                Yes
  Max compute units                               48
  SIMD per compute unit (AMD)                     4
  SIMD width (AMD)                                32
  SIMD instruction width (AMD)                    1
  Max clock frequency                             2371MHz
  Graphics IP (AMD)                               11.0
  Device Partition                                (core)
    Max number of sub-devices                     48
    Supported partition types                     None
    Supported affinity domains                    (n/a)
  Max work item dimensions                        3
  Max work item sizes                             1024x1024x1024
  Max work group size                             256
  Preferred work group size (AMD)                 256
  Max work group size (AMD)                       1024
  Preferred work group size multiple (kernel)     32
  Wavefront width (AMD)                           32
  Preferred / native vector sizes
    char                                                 4 / 4
    short                                                2 / 2
    int                                                  1 / 1
    long                                                 1 / 1
    half                                                 1 / 1        (cl_khr_fp16)
    float                                                1 / 1
    double                                               1 / 1        (cl_khr_fp64)
  Half-precision Floating-point support           (cl_khr_fp16)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
  Single-precision Floating-point support         (core)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
    Correctly-rounded divide and sqrt operations  Yes
  Double-precision Floating-point support         (cl_khr_fp64)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
  Address bits                                    64, Little-Endian
  Global memory size                              25753026560 (23.98GiB)
  Global free memory (AMD)                        22574712 (21.53GiB) 22574712 (21.53GiB)
  Global memory channels (AMD)                    12
  Global memory banks per channel (AMD)           4
  Global memory bank width (AMD)                  256 bytes
  Error Correction support                        No
  Max memory allocation                           21890072576 (20.39GiB)
  Unified memory for Host and Device              No
  Shared Virtual Memory (SVM) capabilities        (core)
    Coarse-grained buffer sharing                 Yes
    Fine-grained buffer sharing                   Yes
    Fine-grained system sharing                   No
    Atomics                                       No
  Minimum alignment for any data type             128 bytes
  Alignment of base address                       2048 bits (256 bytes)
  Preferred alignment for atomics
    SVM                                           0 bytes
    Global                                        0 bytes
    Local                                         0 bytes
  Max size for global variable                    21890072576 (20.39GiB)
  Preferred total size of global vars             25753026560 (23.98GiB)
  Global Memory cache type                        Read/Write
  Global Memory cache size                        32768 (32KiB)
  Global Memory cache line size                   64 bytes
  Image support                                   No
    Base address alignment for 2D image buffers   0 bytes
    Pitch alignment for 2D image buffers          0 pixels
  Max number of pipe args                         16
  Max active pipe reservations                    16
  Max pipe packet size                            415236096 (396MiB)
  Local memory type                               Local
  Local memory size                               65536 (64KiB)
  Local memory size per CU (AMD)                  65536 (64KiB)
  Local memory banks (AMD)                        32
  Max number of constant args                     8
  Max constant buffer size                        21890072576 (20.39GiB)
  Preferred constant buffer size (AMD)            16384 (16KiB)
  Max size of kernel argument                     1024
  Queue properties (on host)
    Out-of-order execution                        No
    Profiling                                     Yes
  Queue properties (on device)
    Out-of-order execution                        Yes
    Profiling                                     Yes
    Preferred size                                262144 (256KiB)
    Max size                                      8388608 (8MiB)
  Max queues on device                            1
  Max events on device                            1024
  Prefer user sync for interop                    Yes
  Number of P2P devices (AMD)                     0
  Profiling timer resolution                      1ns
  Profiling timer offset since Epoch (AMD)        0ns (Wed Dec 31 17:00:00 1969)
  Execution capabilities
    Run OpenCL kernels                            Yes
    Run native kernels                            No
    Thread trace supported (AMD)                  No
    Number of async queues (AMD)                  8
    Max real-time compute queues (AMD)            8
    Max real-time compute units (AMD)             48
  printf() buffer size                            4194304 (4MiB)
  Built-in kernels                                (n/a)
  Device Extensions                               cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program

NULL platform behavior
  clGetPlatformInfo(NULL, CL_PLATFORM_NAME, ...)  AMD Accelerated Parallel Processing
  clGetDeviceIDs(NULL, CL_DEVICE_TYPE_ALL, ...)   Success [AMD]
  clCreateContext(NULL, ...) [default]            Success [AMD]
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_DEFAULT)  Success (1)
    Platform Name                                 AMD Accelerated Parallel Processing
    Device Name                                   gfx1100
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_CPU)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_GPU)  Success (1)
    Platform Name                                 AMD Accelerated Parallel Processing
    Device Name                                   gfx1100
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_ACCELERATOR)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_CUSTOM)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_ALL)  Success (1)
    Platform Name                                 AMD Accelerated Parallel Processing
    Device Name                                   gfx1100

ICD loader properties
  ICD loader Name                                 OpenCL ICD Loader
  ICD loader Vendor                               OCL Icd free software
  ICD loader Version                              2.3.2
  ICD loader Profile                              OpenCL 3.0
```

---

### 评论 #3 — schung-amd (2025-11-19T18:38:42Z)

Thanks! I haven't repro'd yet, but first thing that sticks out is

> Adrenalin Driver Version
25.11.1

ROCm on WSL requires a specific driver version with WSL compatibility; the latest according to the [install docs](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html) is 25.8.1. This might not be the root cause of your issue but I'd give that a shot first.

---

### 评论 #4 — Tilroe (2025-11-19T20:20:46Z)

I downgraded to 25.8.1. Still facing the same `CL_OUT_OF_HOST_MEMORY` issue.

---

### 评论 #5 — schung-amd (2025-11-19T21:29:08Z)

Thanks for verifying, will let you know when I have more info.

---

### 评论 #6 — schung-amd (2025-11-24T19:15:59Z)

@Tilroe I haven't been able to reproduce this on our WSL test machines. How much memory is available to WSL on your system?

My reproducer is:

- 7900XTX, Windows 11, ROCm on WSL installed per https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html
- Copied your reproducer code from the linked issue as test.cpp
- `sudo apt install ocl-icd-opencl-dev`
- `gcc test.cpp -g -I/opt/rocm/include -lOpenCL`

I don't see any issues running the executable alone or in `gdb`.

I do see some discrepancies between `clinfo` output in your WSL environment and mine, not sure what's causing that at the moment and whether it might be related.

---

### 评论 #7 — Tilroe (2025-11-25T03:08:46Z)

@schung-amd Thanks for the response. I'll take a second look on my end. Out of curiousity, what sort of discrepancies did you see between your `clinfo` output and mine?

Also, just for some added context (even though as far as I can tell it should be equivalent), I've included the [OpenCL-ICD-Loader](https://github.com/KhronosGroup/OpenCL-ICD-Loader) for the ICD loader (instead of `ocl-icd-opencl-dev` providing `libOpenCL.so`) and [OpenCL-Headers](https://github.com/KhronosGroup/OpenCL-Headers) (instead of the headers distributed with ROCm) repositories directly from Khronos Group in my project as git submodules. I'm also using CMake to manage my project.

Again, seeing as the first few OpenCL calls worked fine, I think this should be roughly equivalent, but I thought I'd mention it at least.

EDIT: I also tried the ICD from `ocl-icd-opencl-dev`, no luck.

> How much memory is available to WSL on your system?

Around 16 GB

---

### 评论 #8 — schung-amd (2025-11-25T15:30:27Z)

> Out of curiousity, what sort of discrepancies did you see between your clinfo output and mine?

I'll try to paste the whole output when I get access to a WSL system again, but it was closer to the native Windows output; specifically sections like

>   Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               2
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon RX 7900 XTX

which I don't see in your WSL clinfo output. I didn't see any immediate red flags in the actual data though, so it could just be a different output format related to our environment differences.

Speaking of which,

> Also, just for some added context (even though as far as I can tell it should be equivalent), I've included the [OpenCL-ICD-Loader](https://github.com/KhronosGroup/OpenCL-ICD-Loader) for the ICD loader (instead of ocl-icd-opencl-dev providing libOpenCL.so) and [OpenCL-Headers](https://github.com/KhronosGroup/OpenCL-Headers) (instead of the headers distributed with ROCm) repositories directly from Khronos Group in my project as git submodules. I'm also using CMake to manage my project.

I'm not entirely sure these are fully equivalent, so please do try this with the OpenCL that we distribute. We have our own OpenCL implementation that may differ from Khronos under the hood. As for CMake, I don't think this should cause an issue, but could you provide the CMakeLists for your reproducer?

> Around 16 GB

Thanks for checking, this should be sufficient; was seeing some segfaults with the reproducer in low memory (<4GB) environments.



---

### 评论 #9 — Tilroe (2025-11-25T17:25:32Z)

> I'm not entirely sure these are fully equivalent, so please do try this with the OpenCL that we distribute. We have our own OpenCL implementation that may differ from Khronos under the hood. As for CMake, I don't think this should cause an issue, but could you provide the CMakeLists for your reproducer?

Correct me if I'm wrong, but I thought the point of the Installable Client Driver (ICD) (i.e. `libOpenCL.so`) was to find the vendor's implementation of OpenCL ("under the hood" implementation) at runtime? After all, OpenCL is just a standard defined by Khronos Group, and its up to chip vendors to implement it for their hardware. The way my executable is created is that it links with the static library `libOpenCL.a` from OpenCL-ICD-Loader, instead of the shared object `libOpenCL.so` from `ocl-icd-opencl-dev`. 

Running the executable with `strace` to track the system calls, it looks as if the ICD correctly finds AMD's vendored `.icd` file

```
[pid 13193] newfstatat(AT_FDCWD, "/etc/OpenCL/vendors/amdocl64_60402_120.icd", {st_mode=S_IFREG|0644, st_size=15, ...}, 0) = 0
[pid 13193] openat(AT_FDCWD, "/etc/OpenCL/vendors/amdocl64_60402_120.icd", O_RDONLY) = 20
```
which point to AMD's actual vendored library
```
[pid 13193] read(20, "libamdocl64.so\n", 15) = 15
[pid 13193] openat(AT_FDCWD, "/opt/rocm-6.4.2/lib/libamdocl64.so", O_RDONLY|O_CLOEXEC) = 2
```

> As for CMake, I don't think this should cause an issue, but could you provide the CMakeLists for your reproducer?

Rather than provide my project piecemeal, its probably best to just provide the whole thing to observe: [rubiks-cube-gl](https://github.com/Tilroe/rubiks-cube-gl)

---

### 评论 #10 — schung-amd (2025-11-25T20:45:07Z)

On paper, yes, but sometimes things are wonky; that being said, your strace output does show the correct library being found. I'll check that against what I see on my end.

Thanks for linking to the full project!

---

### 评论 #11 — schung-amd (2025-11-27T18:21:27Z)

When/how are you seeing this error with your project? I built it and am not seeing any issues when running the rubix_cube executable.

---

### 评论 #12 — Tilroe (2025-11-27T19:20:02Z)

I see the error under the debug configuration of my IDE (CLion) on my WSL toolchain, which reports as using `gdb` for the debugger. When running on my native Windows, the bundled CLion `gdb` for Windows works fine.

### WSL toolchain
<img width="1475" height="478" alt="Image" src="https://github.com/user-attachments/assets/e27b14b3-227a-4d88-82d8-7b9d8bea3f44" />

### MinGW Windows toolchain

<img width="1457" height="490" alt="Image" src="https://github.com/user-attachments/assets/a6714466-e422-4588-b5b4-cc015be0bb9c" />

### Problem WSL debug configuration

<img width="1863" height="652" alt="Image" src="https://github.com/user-attachments/assets/80377123-030c-4bd4-8a4d-fdf414f2fb29" />

### Before / After queue creation
Before
<img width="1420" height="334" alt="Image" src="https://github.com/user-attachments/assets/4ba87994-7fea-4512-9cde-3a5ec349a631" />
After
<img width="1586" height="332" alt="Image" src="https://github.com/user-attachments/assets/f583d247-0790-4d5e-b9ae-47d71ebe2d3d" />

---

### 评论 #13 — Tilroe (2025-12-03T20:04:10Z)

Hi, just wanted to reach out to see if this is still an open issue at AMD's end. If there's any additional diagnostic info you want me to provide, let me know.

---

### 评论 #14 — schung-amd (2025-12-03T20:17:12Z)

Thanks for checking in. I'm still looking into it, but I haven't been able to reproduce this yet unfortunately. I suspect this is something to do with your environment and not something more fundamental; that doesn't mean we're not interested in fixing it for you and other users who may run into this issue, but makes it a bit tricky to debug, and it's not clear whether this issue is emerging from our end.

The next thing I need to try for this is using CLion's WSL workflow, there might be an issue with the WSL integration on that side of things. Hopefully I'll be able to reproduce your issue there, and I'll update accordingly.

---

### 评论 #15 — schung-amd (2025-12-16T19:24:21Z)

Sorry for the delay on this, I still haven't been able to repro the issue. Building and debugging in WSL via CLion works fine on my system. I'll keep trying to repro this as bandwidth allows, but will probably close this next week if I'm still unable to as it doesn't seem like the issues you're seeing are on our end.

---

### 评论 #16 — schung-amd (2026-01-05T16:04:40Z)

Closing for now as I'm still unable to repro, we can reopen this in the future if this changes.

---
