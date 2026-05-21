# [Issue]: Arch Linux RX 7600 using CPU instead of GPU

> **Issue #2708**
> **状态**: closed
> **创建时间**: 2023-12-14T05:57:21Z
> **更新时间**: 2023-12-14T22:14:29Z
> **关闭时间**: 2023-12-14T22:14:29Z
> **作者**: 0xGingi
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2708

## 描述

### Problem Description

I am attempting to use PyTorch with ROCM, I have tried both the opencl-amd/opencl-amd-dev packages in the AUR as well as the rocm packages in the arch extra repository. I am using the pytorch packages from https://repo.radeon.com/rocm/manylinux/rocm-rel-5.7

I have tried the following exports:

PYTORCH_ROCM_ARCH=gfx1102 HSA_OVERRIDE_GFX_VERSION=11.0.0 HCC_AMDGPU_TARGET=gfx1102
PYTORCH_ROCM_ARCH=gfx1100 HSA_OVERRIDE_GFX_VERSION=11.0.0 HCC_AMDGPU_TARGET=gfx1100

It seems to only be using CPU and not touching the GPU

### Operating System

Arch Linux

### CPU

AMD Ryzen 5 5600X

### GPU

RX 7600

### ROCm Version

5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

PYTORCH_ROCM_ARCH=gfx1102 HSA_OVERRIDE_GFX_VERSION=11.0.0 HCC_AMDGPU_TARGET=gfx1102 python index.py

### Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen 5 5600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5600X 6-Core Processor 
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
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32783864(0x1f43df8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32783864(0x1f43df8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32783864(0x1f43df8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 7600                 
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
  Max Clock Freq. (MHz):   2250                               
  BDFID:                   11520                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
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
  Packet Processor uCode:: 528                                
  SDMA engine uCode::      16                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    8372224(0x7fc000) KB               
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

---

## 评论 (3 条)

### 评论 #1 — danielzgtg (2023-12-14T06:51:00Z)

What's the output of `python3 -c 'import torch; print(torch.cuda.is_available(), torch.version.git_version, torch.version.hip)'; pip freeze | grep torch` ?

---

### 评论 #2 — 0xGingi (2023-12-14T06:54:48Z)

True d28dbc840346b2e33ac3040677087aebf6992c39 5.7.31921-d1770ee1b
pytorch-triton-rocm==2.0.2
torch @ file:///home/gingi/github/yuna-ai/torch-2.0.1%2Brocm5.7-cp311-cp311-linux_x86_64.whl#sha256=8783088eb6bde0775a94068ca38fe656c2b56ba47f725b84b056b42120183d8e
torchaudio==2.2.0.dev20231213+rocm5.7
torchvision @ file:///home/gingi/github/yuna-ai/torchvision-0.15.2%2Brocm5.7-cp311-cp311-linux_x86_64.whl#sha256=46e1f92053d3dbd53438babc720ba1cdf2c143aa03ca3cd2922acf167b01a8a2

---

### 评论 #3 — 0xGingi (2023-12-14T07:01:38Z)

I have narrowed it down to ctransformers (which I also followed their guide for installing for rocm) instead of torch itself, I added some checks and torch is logging my GPU

---
