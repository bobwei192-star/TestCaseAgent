# [Issue]: RX6750GRE12G SCLK Very low

> **Issue #3157**
> **状态**: closed
> **创建时间**: 2024-05-24T08:39:43Z
> **更新时间**: 2024-05-27T20:36:15Z
> **关闭时间**: 2024-05-27T20:36:15Z
> **作者**: liuyang6055
> **标签**: AMD Radeon RX 7900 XTX, AMD Radeon Pro VII, AMD Radeon VII, AMD Radeon RX 7900 XT, ROCm 5.7.0
> **URL**: https://github.com/ROCm/ROCm/issues/3157

## 标签

- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **AMD Radeon Pro VII** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 5.7.0** (颜色: #ededed)

## 描述

### Problem Description

hello
My environment is Ubuntu 22.04+RX 6750GRE 12G graphics card，and

(py39e) liuyang@liuyang-MS-7D20:~$ rocm-smi -s


========================= ROCm System Management Interface =========================
=========================== Supported clock frequencies ============================
GPU[0] : Supported dcefclk frequencies on GPU0
GPU[0] : 0: 417Mhz
GPU[0] : 1: 480Mhz *
GPU[0] : 2: 1200Mhz
GPU[0] :
GPU[0] : Supported fclk frequencies on GPU0
GPU[0] : 0: 500Mhz
GPU[0] : 1: 1176Mhz *
GPU[0] : 2: 1941Mhz
GPU[0] :
GPU[0] : Supported mclk frequencies on GPU0
GPU[0] : 0: 96Mhz *
GPU[0] : 1: 456Mhz
GPU[0] : 2: 675Mhz
GPU[0] : 3: 1124Mhz
GPU[0] :
GPU[0] : Supported sclk frequencies on GPU0
GPU[0] : 0: 500Mhz *
GPU[0] : 1: 500Mhz
GPU[0] :
GPU[0] : Supported socclk frequencies on GPU0
GPU[0] : 0: 480Mhz
GPU[0] : 1: 800Mhz *
GPU[0] : 2: 1200Mhz
GPU[0] :
GPU[0] : Supported PCIe frequencies on GPU0
GPU[0] : 0: 16.0GT/s x16 *
GPU[0] : 1: 16.0GT/s x16
GPU[0] :

 

this SCLK only 500MHZ  ，this is too low, can I change it?

### Operating System

ubuntu22.04

### CPU

11th Gen Intel(R) Core(TM) i5-11500 @ 2.70GHz

### GPU

AMD Radeon Pro VII, AMD Radeon RX 7900 XTX, AMD Radeon RX 7900 XT, AMD Radeon VII

### ROCm Version

ROCm 5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

grapic is RX 6750GRE 12G  

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
  Name:                    11th Gen Intel(R) Core(TM) i5-11500 @ 2.70GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          11th Gen Intel(R) Core(TM) i5-11500 @ 2.70GHz
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
  Max Clock Freq. (MHz):   4600                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16261332(0xf820d4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16261332(0xf820d4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16261332(0xf820d4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1031                            
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
    L2:                      3072(0xc00) KB                     
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29663(0x73df)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   500                                
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 94                                 
  SDMA engine uCode::      79                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12566528(0xbfc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    12566528(0xbfc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1031         
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

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2024-05-27T20:36:15Z)

@liuyang6055 RX 6750 GRE graphics is not supported. Thanks!

---
