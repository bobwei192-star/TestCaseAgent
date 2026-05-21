# [Issue]: Coredump while generating image with InvokeAI/FLUX Dev (Quantized)

> **Issue #4394**
> **状态**: open
> **创建时间**: 2025-02-19T18:13:26Z
> **更新时间**: 2025-02-25T19:58:28Z
> **作者**: mcondarelli
> **标签**: Under Investigation, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4394

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

While generating images with InvokeAI I  repeatably get the following error:
```
...
:4:command.cpp              :352 : 7270505876d us: [pid:21983 tid: 7f316f4006c0] Command (KernelExecution) enqueued: 0x7f2e1c055840
:3:rocvirtual.cpp           :807 : 7270505882d us: [pid:21983 tid: 7f316f4006c0] Arg0:   = val:8
:3:rocvirtual.cpp           :807 : 7270505886d us: [pid:21983 tid: 7f316f4006c0] Arg1:   = val:
:3:rocvirtual.cpp           :3056: 7270505890d us: [pid:21983 tid: 7f316f4006c0] ShaderName : _ZN2at6native18elementwise_kernelILi128ELi4EZNS0_15gpu_kernel_implIZZZNS0_12_GLOBAL__N_124pow_tensor_tensor_kernelERNS_18TensorIteratorBaseEENKUlvE_clEvENKUlvE4_clEvEUlddE_EEvS5_RKT_EUliE0_EEviT1_
:4:rocvirtual.cpp           :930 : 7270505900d us: [pid:21983 tid: 7f316f4006c0] SWq=0x7f3342202000, HWq=0x7f316c300000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[128, 1, 1], workgroup=[128, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x7f30e189d240, kernarg_address=0x7f3162f02600, completion_signal=0x0, correlation_id=0, rptr=10769, wptr=10780
:3:hip_module.cpp           :687 : 7270505909d us: [pid:21983 tid: 7f316f4006c0] hipLaunchKernel: Returned hipSuccess : 
:3:hip_error.cpp            :36  : 7270505913d us: [pid:21983 tid: 7f316f4006c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :664 : 7270505917d us: [pid:21983 tid: 7f316f4006c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :668 : 7270505922d us: [pid:21983 tid: 7f316f4006c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :664 : 7270505927d us: [pid:21983 tid: 7f316f4006c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :668 : 7270505931d us: [pid:21983 tid: 7f316f4006c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :634 : 7270505943d us: [pid:21983 tid: 7f316f4006c0]  hipGetDevice ( 0x7f316f3fd71c ) 
:3:hip_device_runtime.cpp   :642 : 7270505948d us: [pid:21983 tid: 7f316f4006c0] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :634 : 7270505952d us: [pid:21983 tid: 7f316f4006c0]  hipGetDevice ( 0x7f316f3fd404 ) 
:3:hip_device_runtime.cpp   :642 : 7270505956d us: [pid:21983 tid: 7f316f4006c0] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :634 : 7270505962d us: [pid:21983 tid: 7f316f4006c0]  hipGetDevice ( 0x7f316f3fd0ac ) 
:3:hip_device_runtime.cpp   :642 : 7270505966d us: [pid:21983 tid: 7f316f4006c0] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :664 : 7270505972d us: [pid:21983 tid: 7f316f4006c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :668 : 7270505976d us: [pid:21983 tid: 7f316f4006c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :634 : 7270505985d us: [pid:21983 tid: 7f316f4006c0]  hipGetDevice ( 0x7f316f3fd4dc ) 
:3:hip_device_runtime.cpp   :642 : 7270505989d us: [pid:21983 tid: 7f316f4006c0] hipGetDevice: Returned hipSuccess : 
:3:hip_platform.cpp         :230 : 7270505994d us: [pid:21983 tid: 7f316f4006c0]  __hipPushCallConfiguration ( {1,1,1}, {256,1,1}, 0, stream:<null> ) 
:3:hip_platform.cpp         :234 : 7270506009d us: [pid:21983 tid: 7f316f4006c0] __hipPushCallConfiguration: Returned hipSuccess : 
Memory access fault by GPU node-1 (Agent handle: 0x5a11cce11a10) on address 0x7f2cbb000000. Reason: Page not present or supervisor privilege.
:3:hip_platform.cpp         :239 : 7270506016d us: [pid:21983 tid: 7f316f4006c0]  __hipPopCallConfiguration ( {458753,9175040,1866456168}, {3437859327,32564,1866456784}, 0x7f316f3fd710, 0x7f316f3fd720 ) 
:3:hip_platform.cpp         :248 : 7270506032d us: [pid:21983 tid: 7f316f4006c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :686 : 7270506037d us: [pid:21983 tid: 7f316f4006c0]  hipLaunchKernel ( 0x7f34d2a31a90, {1,1,1}, {256,1,1}, 0x7f316f3fd770, 0, stream:<null> ) 
./invokeai: line 33: 21983 Aborted                 (core dumped) $SUDO $VENV/bin/invokeai-web $REDIRECT
```
I attach full log below.

[full.log.gz](https://github.com/user-attachments/files/18869944/full.log.gz)

### Operating System

OS: NAME="Linux Mint" VERSION="22.1 (Xia)" UBUNTU_CODENAME=noble

### CPU

CPU:  model name	: AMD Ryzen 9 5950X 16-Core Processor

### GPU

GPU:   Name:                    gfx1102                               Marketing Name:          AMD Radeon™ RX 7600 XT                  Name:                    amdgcn-amd-amdhsa--gfx1102         

### ROCm Version

rocm-6.3.2

### ROCm Component

_No response_

### Steps to Reproduce

- install and run InvokeAI
- Load `FLUX Dev (Quantized)` (`fluxFusionV24StepsGGUFNF4_V2GGUFQ3KS.gguf` actually seems to work) model
- try to build any image

Note: problem seems to be linked to "Quantized" models.

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
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
  Max Clock Freq. (MHz):   3400                               
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
      Size:                    65762048(0x3eb7300) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65762048(0x3eb7300) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65762048(0x3eb7300) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65762048(0x3eb7300) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon™ RX 7600 XT           
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2493                               
  BDFID:                   11520                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 412                                
  SDMA engine uCode::      21                                 
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
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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

Note: problem seems to be linked to "Quantized" models.
I did several tests and all "Quantized" had the problem and none of the others showed it.

---

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2025-02-19T21:39:53Z)

Hi @mcondarelli. Internal ticket has been created to investigate this issue. Thanks!

---
