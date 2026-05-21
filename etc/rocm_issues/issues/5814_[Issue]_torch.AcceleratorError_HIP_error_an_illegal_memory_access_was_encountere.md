# [Issue]: torch.AcceleratorError: HIP error: an illegal memory access was encountered

> **Issue #5814**
> **状态**: closed
> **创建时间**: 2025-12-25T11:30:26Z
> **更新时间**: 2026-01-23T09:26:22Z
> **关闭时间**: 2026-01-23T09:26:22Z
> **作者**: Jayson-du
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5814

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

hello everyone. When I used vllm built based on ROCm7.0 and ran the official example of vllm for deploying Qwen3-0.6B (vllm/examples/offline_inference/context_extension.py);
vllm informed me that "torch.AcceleratorError: HIP error: an illegal memory access was encountered";
I used this issue's(https://github.com/ROCm/ROCm/issues/2536) addvise, 
export PYTORCH_ROCM_ARCH="gfx1201"

Both hip errors and kernel errors still exist.

kernel error:
[  +0.000012] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32781)
[  +0.000006] amdgpu 0000:03:00.0: amdgpu:  in process python3 pid 5748 thread python3 pid 5748)
[  +0.000002] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000796073ed4000 from client 10
[  +0.000002] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841051
[  +0.000002] amdgpu 0000:03:00.0: amdgpu:       Faulty UTCL2 client ID: TCP (0x8)
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       MORE_FAULTS: 0x1
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       WALKER_ERROR: 0x0
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       PERMISSION_FAULTS: 0x5
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       MAPPING_ERROR: 0x0
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       RW: 0x1
[  +0.000007] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32781)
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:  in process python3 pid 5748 thread python3 pid 5748)
[  +0.000002] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007963a2a21000 from client 10
[  +0.000007] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32781)
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:  in process python3 pid 5748 thread python3 pid 5748)
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007963a6433000 from client 10
[12月25 19:09] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32785)
[  +0.000008] amdgpu 0000:03:00.0: amdgpu:  in process python3 pid 6318 thread python3 pid 6318)
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x000074adb5565000 from client 10
[  +0.000002] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841051
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       Faulty UTCL2 client ID: TCP (0x8)
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       MORE_FAULTS: 0x1
[  +0.000000] amdgpu 0000:03:00.0: amdgpu:       WALKER_ERROR: 0x0
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       PERMISSION_FAULTS: 0x5
[  +0.000001] amdgpu 0000:03:00.0: amdgpu:       MAPPING_ERROR: 0x0
[  +0.000000] amdgpu 0000:03:00.0: amdgpu:       RW: 0x1

Who can tell me what the problem is?

### Operating System

Ubuntu 22.04.5 LTS

### CPU

AMD Ryzen 9 9950X 16-Core Processor

### GPU

gfx1201

### ROCm Version

ROCm 7.0

### ROCm Component

_No response_

### Steps to Reproduce

cd path/vllm/examples/offline_inference && python3 ./context_extension.py

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.14.14 is loaded
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
  Name:                    AMD Ryzen 9 9950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 9950X 16-Core Processor
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
  Max Clock Freq. (MHz):   5752                               
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
      Size:                    129372352(0x7b610c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    129372352(0x7b610c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    129372352(0x7b610c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    129372352(0x7b610c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-2b09110b94528d60               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2460                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 58                                 
  SDMA engine uCode::      380                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5056(0x13c0)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   30208                              
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 22                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    64686176(0x3db0860) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    64686176(0x3db0860) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic 
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

my vllm's  version is v0.11.2

---

## 评论 (9 条)

### 评论 #1 — c0rb4c (2025-12-29T08:50:45Z)

Same here using Radeon AI Pro R9700 (gfx1201) on ComfyUI (ROCm 7.1):

**!!! Exception during processing !!! HIP error: an illegal memory access was encountered**

System is pretty much unusable now as the error triggers almost on every AI inference :(

Seems to be linked to the last linux-firmware update on Arch (amdgpu 20251125-2). Tried to downgrade the firmware but I got other errors.

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
  Name:                    AMD Ryzen 9 9900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 9900X 12-Core Processor
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
  Max Clock Freq. (MHz):   5662                               
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
      Size:                    65472724(0x3e708d4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65472724(0x3e708d4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65472724(0x3e708d4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65472724(0x3e708d4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-06a2adab67bf131c               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33406976(0x1fdc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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

---

### 评论 #2 — amd-nicknick (2026-01-07T13:46:14Z)

Hi @Jayson-du, @c0rb4c, let's clear up some further information first.
Could you please help confirm which version of firmware you're on? Provide the output of `sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info`.

@Jayson-du, are you using any Docker images to run? if so, could you provide the image tag so I could check the stack?

---

### 评论 #3 — c0rb4c (2026-01-10T20:27:09Z)

> Hi [@Jayson-du](https://github.com/Jayson-du), [@c0rb4c](https://github.com/c0rb4c), let's clear up some further information first. Could you please help confirm which version of firmware you're on? Provide the output of `sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info`.
> 
> [@Jayson-du](https://github.com/Jayson-du), are you using any Docker images to run? if so, could you provide the image tag so I could check the stack?

Hello @amd-nicknick, here are the output:

```
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b40
PFP feature version: 29, firmware version: 0x00000b86
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000c80
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3805204, firmware version: 0x003a1014
ASD feature version: 553648388, firmware version: 0x21000104
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684b00 (104.75.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x0910b001
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x0a000601
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x00000084
MES feature version: 1, firmware version: 0x00000084
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-APM107573-101
```

---

### 评论 #4 — c0rb4c (2026-01-11T10:36:54Z)

I don't know if there is any link or so, but using:

- WHL ROCm PyTorch 2.9.1+rocm7.10.0 (the ones from there https://repo.amd.com/rocm/whl/gfx120X-all not the nightlies from there https://rocm.nightlies.amd.com/v2/gfx120X-all which have poor performances on clippers), installed in the venv using "pip install torch torchvision torchaudio --index-url https://repo.amd.com/rocm/whl/gfx120X-all)
-  Python 3.12.12 on the last GIT version of ComfyUI (no launch param like --force-fp16 or any --high-vram stuff even with 32 Go of VRAM, and no HSA_OVERRIDE_GFX_VERSION override, gfx1201 is detected by the soft)
- HSA runtime version 1.18 ext version 1.14
- Last kernel 6.18.3-2
- Last firmware distributed on Manjaro (linux-firmware-meta 20251125-2)

Seems to be way more stable (still got some "HIP illegal memory access" and some "Memory access fault by GPU node-1" from time to time, but now at least I can work for a few long minutes straight... and restart it maybe once an hour of full GPU usage) and performance is there as well. Any other combination is unusable for me, and I think I tried a lot of them during the last weeks... maybe all of them ;)

---

### 评论 #5 — amd-nicknick (2026-01-12T03:21:53Z)

Hi @c0rb4c, I'm a little surprised you could get FW 0x84, are you sure the firmware came from the package you mentioned (Check version of linux-firmware-amdgpu).
FW 0x84 is affected by a known MES issue. I'm also surprised it works on your system. Could you confirm your current FW version?

@Jayson-du, pinging you to check on your original VLLM report, are you still reproducing?

---

### 评论 #6 — c0rb4c (2026-01-12T05:43:46Z)

```
sudo pacman -Q linux-firmware-amdgpu
linux-firmware-amdgpu 20251125-2
```

I didn't say it works flawlessly ;-) it did crash for example during this night batch (Memory access fault by GPU node-1 ("Agent handle: 0x555f9d52f230) on address 0x7fd7d0246000. Reason: Page not present or supervisor privilege.") but this is the versions association being the more stable on my R9700. On some older versions, it crashes almost every time a model is loaded or unloaded (mainly the big ones like FLUX), or during any VAE decoding, ... with this combination, I can trigger 400 to 500 workflows before random crashes.

Thanks for the help!

---

### 评论 #7 — jyggen (2026-01-12T20:35:21Z)

Running into similar issues with pytorch and rocm after a handful of generations while using ComfyUI or SD.Next. 

```
Memory access fault by GPU node-1 (Agent handle: 0x55ed71f0e400) on address 0x7fed0e205000. Reason: Page not present or supervisor privilege.
```

It started happening around early/mid December (iirc), around the time linux, linux-firmware and rocm all had recently released new versions, so it's hard to pinpoint the exact cause. I've tried rolling linux-firmware back to as far as 20251011 (since rolling back seemed to fix similar issues on gfx1151), but that didn't change anything - so it's likely breaking by some change introduced in Linux 6.18. An interesting side-effect is that after this error occurs, launching most games will usually yield a white screen and soon after completely freeze my PC.

ComfyUI output:
```
pytorch version: 2.11.0.dev20260111+rocm7.1
AMD arch: gfx1201
ROCm version: (7, 1)
Device: cuda:0 AMD Radeon RX 9070 XT : native
```

Firmware version:
```
❯ cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 1, firmware version: 0x00000084
MES feature version: 1, firmware version: 0x00000084
```

Relevant package versions (archlinux):
```
linux 6.18.4.arch1-1
linux-firmware-amdgpu 20251125-2
rocm-cmake 7.1.1-1
rocm-core 7.1.1-1
rocm-device-libs 2:7.1.1-2
rocm-hip-runtime 7.1.1-1
rocminfo 7.1.1-1
rocm-language-runtime 7.1.1-1
rocm-llvm 2:7.1.1-2
rocm-smi-lib 7.1.1-1
```

I also got a GPU core dump from ComfyUI that I can upload  somewhere if it's of any help.

---

### 评论 #8 — FR-Mister-T (2026-01-13T18:26:47Z)

> Running into similar issues with pytorch and rocm after a handful of generations while using ComfyUI or SD.Next.
> 
> ```
> Memory access fault by GPU node-1 (Agent handle: 0x55ed71f0e400) on address 0x7fed0e205000. Reason: Page not present or supervisor privilege.
> ```
> 
> It started happening around early/mid December (iirc), around the time linux, linux-firmware and rocm all had recently released new versions, so it's hard to pinpoint the exact cause. I've tried rolling linux-firmware back to as far as 20251011 (since rolling back seemed to fix similar issues on gfx1151), but that didn't change anything - so it's likely breaking by some change introduced in Linux 6.18. An interesting side-effect is that after this error occurs, launching most games will usually yield a white screen and soon after completely freeze my PC.
> 
> ComfyUI output:
> 
> ```
> pytorch version: 2.11.0.dev20260111+rocm7.1
> AMD arch: gfx1201
> ROCm version: (7, 1)
> Device: cuda:0 AMD Radeon RX 9070 XT : native
> ```
> 
> Firmware version:
> 
> ```
> ❯ cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
> MES_KIQ feature version: 1, firmware version: 0x00000084
> MES feature version: 1, firmware version: 0x00000084
> ```
> 
> Relevant package versions (archlinux):
> 
> ```
> linux 6.18.4.arch1-1
> linux-firmware-amdgpu 20251125-2
> rocm-cmake 7.1.1-1
> rocm-core 7.1.1-1
> rocm-device-libs 2:7.1.1-2
> rocm-hip-runtime 7.1.1-1
> rocminfo 7.1.1-1
> rocm-language-runtime 7.1.1-1
> rocm-llvm 2:7.1.1-2
> rocm-smi-lib 7.1.1-1
> ```
> 
> I also got a GPU core dump from ComfyUI that I can upload somewhere if it's of any help.

Hello I manage to get back my system into "working condition" (but not fast) with the setup in this link
I hope it will help  https://github.com/ROCm/ROCm/issues/5742#issuecomment-3706570596

---

### 评论 #9 — amd-nicknick (2026-01-23T09:26:22Z)

Closing this issue for now due to inactivity, if you are still facing the same issue, please reopen this issue and attach latest information. Thanks!

---
