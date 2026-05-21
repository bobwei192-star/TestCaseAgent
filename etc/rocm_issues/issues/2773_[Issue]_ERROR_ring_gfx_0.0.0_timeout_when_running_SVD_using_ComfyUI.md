# [Issue]: *ERROR* ring gfx_0.0.0 timeout when running SVD using ComfyUI

> **Issue #2773**
> **状态**: closed
> **创建时间**: 2024-01-02T11:30:44Z
> **更新时间**: 2024-01-07T10:58:18Z
> **关闭时间**: 2024-01-07T10:58:18Z
> **作者**: lubosz
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2773

## 描述

## Problem Description

I am experiencing GPU lockups when running Stable Video Diffusion using ComfyUI on ROCm 5.7.1.

```
[drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring gfx_0.0.0 timeout, signaled seq=43270, emitted seq=43271
[drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process gnome-shell pid 11025 thread gnome-shel:cs0 pid 11072
amdgpu 0000:0d:00.0: amdgpu: GPU reset begin!
```

When reducing the settings (like resolution) and with some luck I am able to complete the workflow with low performance (~70s/it).

A RX 7900 XT user has reported the same issue and was able to overcome it by most likely upgrading from ROCm 5.6 -> 5.7, avoiding the lockup and improving performance.

Related ComfyUI issue: https://github.com/comfyanonymous/ComfyUI/issues/2304

### dmesg

<details>
  <summary>Click to expand</summary>

```
[  711.453529] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring gfx_0.0.0 timeout, signaled seq=43270, emitted seq=43271
[  711.454066] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process gnome-shell pid 11025 thread gnome-shel:cs0 pid 11072
[  711.454568] amdgpu 0000:0d:00.0: amdgpu: GPU reset begin!
[  711.454596] amdgpu: Failed to suspend process 0x8001
[  711.837294] amdgpu 0000:0d:00.0: amdgpu: MODE1 reset
[  711.837298] amdgpu 0000:0d:00.0: amdgpu: GPU mode1 reset
[  711.837373] amdgpu 0000:0d:00.0: amdgpu: GPU smu mode1 reset
[  712.349872] amdgpu 0000:0d:00.0: amdgpu: GPU reset succeeded, trying to resume
[  712.350059] [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
[  712.350133] [drm] VRAM is lost due to GPU reset!
[  712.350134] [drm] PSP is resuming...
[  712.430342] [drm] reserve 0xa00000 from 0x83fd000000 for PSP TMR
[  712.571285] amdgpu 0000:0d:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  712.571287] amdgpu 0000:0d:00.0: amdgpu: SMU is resuming...
[  712.571290] amdgpu 0000:0d:00.0: amdgpu: smu driver if version = 0x00000040, smu fw if version = 0x00000041, smu fw program = 0, version = 0x003a5800 (58.88.0)
[  712.571292] amdgpu 0000:0d:00.0: amdgpu: SMU driver if version not matched
[  712.571324] amdgpu 0000:0d:00.0: amdgpu: use vbios provided pptable
[  712.646897] amdgpu 0000:0d:00.0: amdgpu: SMU is resumed successfully!
[  712.648165] [drm] DMUB hardware initialized: version=0x02020020
[  713.202199] [drm] kiq ring mec 2 pipe 1 q 0
[  713.207827] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  713.208082] [drm] JPEG decode initialized successfully.
[  713.208098] amdgpu 0000:0d:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  713.208099] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  713.208100] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  713.208101] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  713.208102] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  713.208103] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  713.208103] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  713.208104] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  713.208105] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  713.208106] amdgpu 0000:0d:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  713.208107] amdgpu 0000:0d:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  713.208108] amdgpu 0000:0d:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  713.208108] amdgpu 0000:0d:00.0: amdgpu: ring sdma2 uses VM inv eng 14 on hub 0
[  713.208109] amdgpu 0000:0d:00.0: amdgpu: ring sdma3 uses VM inv eng 15 on hub 0
[  713.208110] amdgpu 0000:0d:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  713.208110] amdgpu 0000:0d:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  713.208111] amdgpu 0000:0d:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  713.208112] amdgpu 0000:0d:00.0: amdgpu: ring vcn_dec_1 uses VM inv eng 5 on hub 8
[  713.208112] amdgpu 0000:0d:00.0: amdgpu: ring vcn_enc_1.0 uses VM inv eng 6 on hub 8
[  713.208113] amdgpu 0000:0d:00.0: amdgpu: ring vcn_enc_1.1 uses VM inv eng 7 on hub 8
[  713.208114] amdgpu 0000:0d:00.0: amdgpu: ring jpeg_dec uses VM inv eng 8 on hub 8
[  713.216941] amdgpu 0000:0d:00.0: amdgpu: recover vram bo from shadow start
[  713.221446] amdgpu 0000:0d:00.0: amdgpu: recover vram bo from shadow done
[  713.221475] amdgpu 0000:0d:00.0: amdgpu: GPU reset(8) succeeded!
[  713.221485] [drm] Skip scheduling IBs!
[  713.221494] [drm] Skip scheduling IBs!
[  713.229972] [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!
[  714.731815] [drm] Skip scheduling IBs!
[  714.731822] [drm] Skip scheduling IBs!
[  714.731823] [drm] Skip scheduling IBs!
[  714.731825] [drm] Skip scheduling IBs!
[  714.731836] [drm] Skip scheduling IBs!
[  714.731843] [drm] Skip scheduling IBs!
[  714.731844] [drm] Skip scheduling IBs!
[  714.731845] [drm] Skip scheduling IBs!
```
</details>

## System

### Operating System

Arch Linux

### CPU

AMD Ryzen 9 3900X
RAM 64202 MB

### GPU

AMD Radeon RX 6900 XT / gfx1030
VRAM 16368 MB

### Kernel

Linux 6.6.8-arch1-1

### ComfyUI Version

git master at `60fafb5`

### ROCm Version

ROCm 5.7.1

### Steps to Reproduce

https://comfyanonymous.github.io/ComfyUI_examples/video/

* Model
https://huggingface.co/stabilityai/stable-video-diffusion-img2vid/blob/main/svd.safetensors

* Workflow
https://comfyanonymous.github.io/ComfyUI_examples/video/workflow_image_to_video.json

* Init Image
https://comfyanonymous.github.io/ComfyUI_examples/unclip/mountains.png

### Output of `/opt/rocm/bin/rocminfo --support`

<details>
  <summary>Click to expand</summary>


```
ROCk module is loaded
/usr/share/libdrm/amdgpu.ids version: 1.0.0
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
  Name:                    AMD Ryzen 9 3900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 3900X 12-Core Processor
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
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65742604(0x3eb270c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65742604(0x3eb270c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65742604(0x3eb270c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-acfa08f5f8ea8075               
  Marketing Name:          AMD Radeon RX 6900 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      131072(0x20000) KB                 
  Chip ID:                 29631(0x73bf)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2660                               
  BDFID:                   3328                               
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 115                                
  SDMA engine uCode::      83                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    16760832(0xffc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1030         
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
</details>

---

## 评论 (1 条)

### 评论 #1 — lubosz (2024-01-07T10:58:18Z)

I was able to resolve the issue by upgrading to `ROCm 6.0.0`.

---
