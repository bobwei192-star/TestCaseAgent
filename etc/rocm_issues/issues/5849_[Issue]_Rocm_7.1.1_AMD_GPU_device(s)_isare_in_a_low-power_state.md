# [Issue]: Rocm 7.1.1 AMD GPU device(s) is/are in a low-power state.

> **Issue #5849**
> **状态**: closed
> **创建时间**: 2026-01-11T19:07:22Z
> **更新时间**: 2026-04-27T04:49:38Z
> **关闭时间**: 2026-03-25T18:01:32Z
> **作者**: mrmorganschneider
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5849

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- darren-amd

## 描述

### Problem Description

Hello,
After installing rocm version 7.1.1, I'm getting the following warning message in the rocm-smi interface:

"~/Desktop$ rocm-smi

```
WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

=========================================== ROCm System Management Interface ===========================================
===================================================== Concise Info =====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK     MCLK     Fan     Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                       
========================================================================================================================
0       1     0x7550,   45211  54.0°C  41.0W  N/A, N/A, 0         1626Mhz  1124Mhz  0%      high  330.0W  6%     33%   
1       2     0x7551,   43088  45.0°C  48.0W  N/A, N/A, 0         41Mhz    1124Mhz  24.71%  high  300.0W  61%    3%    
========================================================================================================================
================================================= End of ROCm SMI Log =================================================="
```

I've set the Ubuntu power settings to performance and have also installed CoreCtrl and set all settings to performance as well, but the issue remains. Not sure what else I can do at this point

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 9950X3D 16-Core Processor

### GPU

AMD Radeon RX 9070 XT x AMD Radeon AI PRO R9700

### ROCm Version

7.1.1.70101-38~24.04

### ROCm Component

_No response_

### Steps to Reproduce

Run rocm-smi command. Issue happens regardless of system state.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

/Desktop$ /opt/rocm/bin/rocminfo --support
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
  Name:                    AMD Ryzen 9 9950X3D 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 9950X3D 16-Core Processor
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
  Max Clock Freq. (MHz):   5756                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32464112(0x1ef5cf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32464112(0x1ef5cf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32464112(0x1ef5cf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32464112(0x1ef5cf0) KB             
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
  Uuid:                    GPU-1e1da31fa1a40123               
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
  Max Clock Freq. (MHz):   2520                               
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
  Packet Processor uCode:: 68                                 
  SDMA engine uCode::      662                                
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
  Name:                    gfx1201                            
  Uuid:                    GPU-a38e51c7e81a37be               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L1:                      32(0x20) KB                        
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   1792                               
  Internal Node ID:        2                                  
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
  Packet Processor uCode:: 68                                 
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31309824(0x1ddc000) KB             
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


### Additional Information

_No response_

---

## 评论 (20 条)

### 评论 #1 — ca1ic0 (2026-01-13T14:41:38Z)

Meet the same problem with 9070xt
```bash
calico@calico-System-Product-Name:~/blas$ rocm-smi


WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

======================================== ROCm System Management Interface ========================================
================================================== Concise Info ==================================================
Device  Node  IDs              Temp    Power   Partitions          SCLK  MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)   (Mem, Compute, ID)                                                 
==================================================================================================================
0       1     0x7550,   3197   39.0°C  74.0W   N/A, N/A, 0         0Mhz  456Mhz   0%   auto  340.0W  2%     0%    
1       2     0x13c0,   43534  46.0°C  0.012W  N/A, N/A, 0         N/A   3000Mhz  0%   auto  N/A     3%     0%    
==================================================================================================================
============================================== End of ROCm SMI Log ===============================================
```

```bash
calico@calico-System-Product-Name:~/blas$ sudo rocminfo
ROCk module version 6.16.6 is loaded
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
  Name:                    AMD Ryzen 5 9600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 9600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   5486                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    31994964(0x1e83454) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31994964(0x1e83454) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31994964(0x1e83454) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31994964(0x1e83454) KB             
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
  Uuid:                    GPU-33cdcaebba902e5f               
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
  Max Clock Freq. (MHz):   2570                               
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
  Packet Processor uCode:: 108                                
  SDMA engine uCode::      662                                
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
  BDFID:                   3584                               
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
  Packet Processor uCode:: 121                                
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15997480(0xf41a28) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15997480(0xf41a28) KB              
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

```

While a simple gemm benchmark using rocblas show low performance , only 800GFLOPS(mnk=4096)


---

### 评论 #2 — darren-amd (2026-01-13T19:53:41Z)

Hi @mrmorganschneider,

Thanks for the report! I was able to reproduce this issue on the latest ROCm. We have a fix available that I verified fixes the issue: https://github.com/ROCm/rocm-systems/pull/2510. This will be included in a future release, but in the meantime you either build from source or patch the change into `/opt/rocm/libexec/rocm_smi/rocm_smi.py`.

---

### 评论 #3 — ca1ic0 (2026-01-14T06:21:37Z)

> Hi [@mrmorganschneider](https://github.com/mrmorganschneider),
> 
> Thanks for the report! I was able to reproduce this issue on the latest ROCm. We have a fix available that I verified fixes the issue: [ROCm/rocm-systems#2510](https://github.com/ROCm/rocm-systems/pull/2510). This will be included in a future release, but in the meantime you either build from source or patch the change into `/opt/rocm/libexec/rocm_smi/rocm_smi.py`.

Will this patch influence performance?  
which official tools could do a quick benchmark of flops and bandwidth?

---

### 评论 #4 — jnolck (2026-01-16T02:06:05Z)

Good catch! I'm on Fedora and was wondering why my performance had dropped so much. 

---

### 评论 #5 — darren-amd (2026-01-16T16:02:16Z)

> > Hi [@mrmorganschneider](https://github.com/mrmorganschneider),
> > Thanks for the report! I was able to reproduce this issue on the latest ROCm. We have a fix available that I verified fixes the issue: [ROCm/rocm-systems#2510](https://github.com/ROCm/rocm-systems/pull/2510). This will be included in a future release, but in the meantime you either build from source or patch the change into `/opt/rocm/libexec/rocm_smi/rocm_smi.py`.
> 
> Will this patch influence performance? which official tools could do a quick benchmark of flops and bandwidth?

Hi @ca1ic0, This change will not have an impact on performance. What kind of workload/benchmark are you trying to run?

Hi @jnolck, would you mind creating a separate ticket with details on the performance difference you are experiencing? That should help us to further investigate.

---

### 评论 #6 — ca1ic0 (2026-01-17T00:50:15Z)

> > > Hi [@mrmorganschneider](https://github.com/mrmorganschneider),
> > > Thanks for the report! I was able to reproduce this issue on the latest ROCm. We have a fix available that I verified fixes the issue: [ROCm/rocm-systems#2510](https://github.com/ROCm/rocm-systems/pull/2510). This will be included in a future release, but in the meantime you either build from source or patch the change into `/opt/rocm/libexec/rocm_smi/rocm_smi.py`.
> > 
> > 
> > Will this patch influence performance? which official tools could do a quick benchmark of flops and bandwidth?
> 
> Hi [@ca1ic0](https://github.com/ca1ic0), This change will not have an impact on performance. What kind of workload/benchmark are you trying to run?
> 
> Hi [@jnolck](https://github.com/jnolck), would you mind creating a separate ticket with details on the performance difference you are experiencing? That should help us to further investigate.

I create a issue about low gemm performace https://github.com/ROCm/ROCm/issues/5861.

---

### 评论 #7 — jnolck (2026-01-17T06:06:21Z)

> > > Hi [@mrmorganschneider](https://github.com/mrmorganschneider),
> > > Thanks for the report! I was able to reproduce this issue on the latest ROCm. We have a fix available that I verified fixes the issue: [ROCm/rocm-systems#2510](https://github.com/ROCm/rocm-systems/pull/2510). This will be included in a future release, but in the meantime you either build from source or patch the change into `/opt/rocm/libexec/rocm_smi/rocm_smi.py`.
> > 
> > 
> > Will this patch influence performance? which official tools could do a quick benchmark of flops and bandwidth?
> 
> Hi [@ca1ic0](https://github.com/ca1ic0), This change will not have an impact on performance. What kind of workload/benchmark are you trying to run?
> 
> Hi [@jnolck](https://github.com/jnolck), would you mind creating a separate ticket with details on the performance difference you are experiencing? That should help us to further investigate.

I would but if this isn't it I have no idea what caused it. I usually use one of the docker containers you provide to test since I know neither pytorch/rocm is affected when messing with that, but even that is slower than usual. Let me apply his patch and retest, this being it makes sense to me. 

His patch fixed this issue. I'll open up my own if I can pinpoint where the drop in performance is coming from. 

---

### 评论 #8 — mrmorganschneider (2026-01-22T02:10:17Z)

All,
I patched the code provided into the python file as described in the issue resolution but am still seeing the error. Are there any additional steps I need to take to complete the patching other than just copy-pasting the code into the file?

---

### 评论 #9 — darren-amd (2026-01-22T15:28:45Z)

Hi @mrmorganschneider,

No, there shouldn't be any necessary additional steps, manually patching the file is sufficient. Could you please make sure that the right `rocm-smi` is being run? Try running `/opt/rocm/bin/rocm-smi` manually and see if the issue persists.

---

### 评论 #10 — mrmorganschneider (2026-01-25T03:23:00Z)

Hi Darren,
Followed your recommendation to run rocm-smi from the opt directory and am still getting the same error:

<img width="1185" height="310" alt="Image" src="https://github.com/user-attachments/assets/fa58074d-3b70-4c13-a5dc-fe9dcec7ea8a" />

---

### 评论 #11 — darren-amd (2026-01-27T15:28:50Z)

Hi @mrmorganschneider,

Could you double check that the change is in `/opt/rocm/libexec/rocm_smi/rocm_smi.py`? If that doesn't work, could you try building from source by following the instructions [here](https://rocm.docs.amd.com/projects/amdsmi/en/latest/install/build.html#building-amd-smi) and let me know if you run into any issues? I also spoke with the team and the fix will be included in the next release.

---

### 评论 #12 — marifamd (2026-02-04T17:54:33Z)

Resolved in https://github.com/ROCm/rocm-systems/pull/2510 should be in the 7.2.1 release and TheRock 7.11+ releases.

---

### 评论 #13 — RedactedHosting (2026-03-07T03:39:00Z)

same issue as of 3/6/2026 9700xtx fresh install ubuntu 

---

### 评论 #14 — thor171 (2026-03-07T14:44:35Z)

I can confirm, same issue as of 7/3/2026 with MI50 on Ubuntu 24.04

---

### 评论 #15 — Poisonsting (2026-03-08T00:49:01Z)

Also still having this issue with a 7900 XTX on NixOS Unstable

---

### 评论 #16 — yipinghuang1991 (2026-03-24T16:38:27Z)

Still having this with 9700XT on latest Arch

---

### 评论 #17 — darren-amd (2026-03-25T18:01:32Z)

Hi everyone,

Thanks for reporting the issue!

This has been fixed in ROCm 7.2.1, which you can update to by following the instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html). 

---

### 评论 #18 — opticblu (2026-04-26T02:52:20Z)

yeah this issue is back for sure, arch, new kernels, full rocm stack, latest

I think it's actually getting worse, clocks seem even lower

---

### 评论 #19 — opticblu (2026-04-26T02:52:45Z)

Also tried on ubuntu 26.04, same problem, can't get the clocks high

---

### 评论 #20 — general-rishkin (2026-04-27T04:49:38Z)

I am having this problem right now too!
My OS is Ubuntu 26.04.

---
