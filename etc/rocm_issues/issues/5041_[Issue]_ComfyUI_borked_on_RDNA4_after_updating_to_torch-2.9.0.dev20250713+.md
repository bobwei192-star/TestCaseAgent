# [Issue]:  ComfyUI borked on RDNA4 after updating to torch-2.9.0.dev20250713+

> **Issue #5041**
> **状态**: closed
> **创建时间**: 2025-07-14T21:39:29Z
> **更新时间**: 2025-07-17T19:17:42Z
> **关闭时间**: 2025-07-17T19:17:42Z
> **作者**: B4rr3l-Rid3r
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5041

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

ComfyUi Borked after updating Torch from torch-2.9.0.dev20250711+rocm6.4.dist-info to  torch-2.9.0.dev20250713+rocm6.4.dist-info or newer

terminate called after throwing an instance of 'c10::Error'
  what():  backend:hipMallocAsync requires PyTorch to be built with HIP 11.4 or newer, but TORCH_HIP_VERSION is 604
Exception raised from parseAllocatorConfig at /pytorch/c10/hip/HIPAllocatorConfig.cpp:58 (most recent call first):
frame #0: c10::Error::Error(c10::SourceLocation, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >) + 0x88 (0x7f9eb4f7e0b8 in /home/bull3t/comfy/venv/lib64/python3.12/site-packages/torch/lib/libc10.so)
frame #1: c10::detail::torchCheckFail(char const*, char const*, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) + 0x55 (0x7f9eb4f15837 in /home/bull3t/comfy/venv/lib64/python3.12/site-packages/torch/lib/libc10.so)
frame #2: c10::hip::HIPCachingAllocator::HIPAllocatorConfig::parseAllocatorConfig(c10::CachingAllocator::ConfigTokenizer const&, unsigned long) + 0x580 (0x7f9eb52f3970 in /home/bull3t/comfy/venv/lib64/python3.12/site-packages/torch/lib/libc10_hip.so)
frame #3: c10::hip::HIPCachingAllocator::HIPAllocatorConfig::parseArgs(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) + 0x7d (0x7f9eb52f43fd in /home/bull3t/comfy/venv/lib64/python3.12/site-packages/torch/lib/libc10_hip.so)
frame #4: <unknown function> + 0xcf0d (0x7f9eb52f4f0d in /home/bull3t/comfy/venv/lib64/python3.12/site-packages/torch/lib/libc10_hip.so)
frame #5: <unknown function> + 0xaf5c (0x7f9eb52f2f5c in /home/bull3t/comfy/venv/lib64/python3.12/site-packages/torch/lib/libc10_hip.so)
frame #6: <unknown function> + 0x531e (0x7f9eb865231e in /lib64/ld-linux-x86-64.so.2)
frame #7: <unknown function> + 0x53fc (0x7f9eb86523fc in /lib64/ld-linux-x86-64.so.2)
frame #8: _dl_catch_exception + 0x11b (0x7f9eb864f549 in /lib64/ld-linux-x86-64.so.2)
frame #9: <unknown function> + 0xc158 (0x7f9eb8659158 in /lib64/ld-linux-x86-64.so.2)
frame #10: _dl_catch_exception + 0x88 (0x7f9eb864f4b6 in /lib64/ld-linux-x86-64.so.2)
frame #11: <unknown function> + 0xc5c9 (0x7f9eb86595c9 in /lib64/ld-linux-x86-64.so.2)
frame #12: <unknown function> + 0x9649c (0x7f9eb7a9649c in /lib64/libc.so.6)
frame #13: _dl_catch_exception + 0x88 (0x7f9eb864f4b6 in /lib64/ld-linux-x86-64.so.2)
frame #14: <unknown function> + 0x25f3 (0x7f9eb864f5f3 in /lib64/ld-linux-x86-64.so.2)
frame #15: <unknown function> + 0x95ef4 (0x7f9eb7a95ef4 in /lib64/libc.so.6)
frame #16: dlopen + 0x7b (0x7f9eb7a96569 in /lib64/libc.so.6)
<omitting python frames>
frame #49: <unknown function> + 0x2b37b (0x7f9eb7a2b37b in /lib64/libc.so.6)
frame #50: __libc_start_main + 0x8d (0x7f9eb7a2b44b in /lib64/libc.so.6)

Aborted (core dumped)





### Operating System

OpenSUSE Tumbleweed

### CPU

Ryzen 9 9900X

### GPU

Radeon RX 9070

### ROCm Version

ROCm 6.4.1

### ROCm Component

AMDMIGraphX

### Steps to Reproduce

update from torch-2.9.0.dev20250711+rocm6.4.dist-info to  torch-2.9.0.dev20250713+rocm6.4.dist-info or newer

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
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
      Size:                    65404656(0x3e5fef0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65404656(0x3e5fef0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65404656(0x3e5fef0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65404656(0x3e5fef0) KB             
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
  Uuid:                    GPU-9fde5482590eb830               
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
    L1:                      32(0x20) KB                        
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2120                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            56                                 
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***  

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2025-07-15T13:54:34Z)

Hi @B4rr3l-Rid3r. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — B4rr3l-Rid3r (2025-07-17T19:17:42Z)

fixed on torch-2.9.0.dev20250716+rocm6.4
thank you.

---
