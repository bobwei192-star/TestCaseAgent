# [Issue]: ROCm Issue Report - AMDGPU Page Fault Error

> **Issue #5670**
> **状态**: closed
> **创建时间**: 2025-11-16T10:25:44Z
> **更新时间**: 2025-12-01T14:43:56Z
> **关闭时间**: 2025-12-01T14:43:56Z
> **作者**: wwxxyy-zz
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5670

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

# ROCm Issue Report - AMDGPU Page Fault Error

## Environment Information

### System Information
- **Operating System**: Ubuntu 24.04.3 LTS (Noble Numbat)
- **Kernel Version**: 6.14.0-35-generic
- **CPU**: AMD Ryzen 7 5700X3D 8-Core Processor

### GPU Information
- **GPU Model**: AMD Radeon RX 7800 XT
- **Card Series**: AMD Radeon RX 7800 XT
- **Card Model**: 0x747e
- **Card Vendor**: Advanced Micro Devices, Inc. [AMD/ATI]
- **Card SKU**: D7120201
- **Subsystem ID**: 0x475d
- **Device Rev**: 0xc8
- **GFX Version**: gfx1101
- **Node ID**: 1
- **GUID**: 62813

### ROCm Information
- **ROCm Version**: 7.1.0 (70100-20~24.04)
- **ROCm Core**: 7.1.0.70100-20~24.04
- **ROCm HIP**: 7.1.0.70100-20~24.04
- **ROCm LLVM**: 20.0.0.25425.70100-20~24.04
- **ROCm Device Libraries**: 1.0.0.70100-20~24.04

### Python Environment
- **Conda Environment**
- **Python Version**: 3.12.12
- **ONNX Version**: 1.19.1
- **ONNXRuntime**: onnxruntime-migraphx 1.23.1

### Project Dependencies
```
gradio-rangeslider==0.0.8
gradio
numpy==1.26.4
opencv-python
psutil==7.1.2
tqdm==4.67.1
scipy==1.16.3
```

## Error Description

### Error Log
```
[10265.148838] amdgpu 0000:28:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[10265.148846] amdgpu 0000:28:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[10265.148849] amdgpu 0000:28:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[10265.148851] amdgpu 0000:28:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[10265.148854] amdgpu 0000:28:00.0: amdgpu:      MORE_FAULTS: 0x0
[10265.148856] amdgpu 0000:28:00.0: amdgpu:      WALKER_ERROR: 0x1
[10265.148858] amdgpu 0000:28:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[10265.148860] amdgpu 0000:28:00.0: amdgpu:      MAPPING_ERROR: 0x1
[10265.148862] amdgpu 0000:28:00.0: amdgpu:      RW: 0x0
```

### Error Analysis
- **Error Type**: AMDGPU Page Fault (GCVM_L2_PROTECTION_FAULT)
- **Fault Address**: 0x0000000000000000 (NULL pointer)
- **Faulty Client**: CPC (Compute Pipe Controller - 0x5)
- **Ring ID**: 153
- **WALKER_ERROR**: 0x1 (Page table walker error)
- **PERMISSION_FAULTS**: 0x3 (Permission violation)
- **MAPPING_ERROR**: 0x1 (Memory mapping error)
- **RW**: 0x0 (Read operation)

### Additional Warning
```
WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status
```


## Expected Behavior
GPU compute operations should execute without page faults or memory access violations.

## Actual Behavior
AMDGPU driver reports page fault with NULL pointer access (0x0000000000000000) from the Compute Pipe Controller, indicating a potential issue with:
- Memory allocation/mapping in ROCm stack
- GPU kernel memory access patterns
- ONNXRuntime-MIGraphX backend memory management
- Driver compatibility with gfx1101 architecture



### Operating System

Ubuntu 24.04.3 LTS

### CPU

AMD Ryzen 7 5700X3D 8-Core Processor

### GPU

AMD Radeon RX 7800 XT

### ROCm Version

ROCm Version: 7.1.0 (70100-20~24.04)

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
  Name:                    AMD Ryzen 7 5700X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5700X3D 8-Core Processor
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
  Max Clock Freq. (MHz):   4151                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16296880(0xf8abb0) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16296880(0xf8abb0) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16296880(0xf8abb0) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16296880(0xf8abb0) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1101                            
  Uuid:                    GPU-6a830e83a9827f8a               
  Marketing Name:          AMD Radeon RX 7800 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29822(0x747e)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2124                               
  BDFID:                   10240                              
  Internal Node ID:        1                                  
  Compute Unit:            60                                 
  SIMDs per CU:            2                                  
  Shader Engines:          3                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 550                                
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
      Name:                    amdgcn-amd-amdhsa--gfx1101         
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

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-11-17T18:10:37Z)

Hi @wwxxyy-zz, could you share more information on the workload you were running prior to hitting the page fault? Steps to reproduce would also be helpful in further debugging this.

---

### 评论 #2 — BillyOutlast (2025-11-24T06:15:04Z)

any update?

---

### 评论 #3 — harkgill-amd (2025-12-01T14:43:56Z)

Closing this out for now. @wwxxyy-zz, please share more info/repro steps when you get a chance and I'll re-open this ticket.

---
