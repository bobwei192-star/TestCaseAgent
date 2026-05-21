# [Issue]: Decrease in generation speed on stable-diffusion-webui-forge with ROCM 6.3

> **Issue #5027**
> **状态**: open
> **创建时间**: 2025-07-10T12:21:25Z
> **更新时间**: 2025-07-23T14:27:22Z
> **作者**: RadeonVega-56
> **标签**: Under Investigation, ROCm 6.3.1
> **URL**: https://github.com/ROCm/ROCm/issues/5027

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.1** (颜色: #ededed)

## 描述

### Problem Description

I use a Radeon Vega 56 to generate images with stable-diffusion-webui-forge on Nobara Linux 42. I had generation speed of 3 to 5 it/sec with Euler scheduler. With the latest ROCM update from 6.2 to 6.3 my generation speed decreased to 1.25 it/sec. Generation with other schedulers also decreased.



### Operating System

Nobara Linux 42

### CPU

Ryzen 9 9950X

### GPU

Asus STRIX Radeon Vega 56 OC

### ROCm Version

6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

I followed this guide: https://www.youtube.com/watch?v=vCm6K7GEAMM
I use this repo: https://github.com/lllyasviel/stable-diffusion-webui-forge

Install Nobara 42 from Image,
install Rocm in nobara driver manager,
edit .bashrc: add "export HSA_OVERRIDE_GFX_VERSION=9.0.0",
reboot,
install python 3.10: sudo dnf install python3.10,
create venv: python3.10 -m venv my_venv,
activate venv: source/my_venv/bin/activate,
install pytorch 2.6.0 to venv: pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/rocm6.2.4,
deactivate venv: deactivate,
clone stable-diffusion-webui-forge repo with git: cd, git clone https://github.com/lllyasviel/stable-diffusion-webui-forge.git,
cd stable-diffusion-webui-forge,
copy venv to stable-diffusion-webui-forge folder: cp -r /home/"username"/my_venv/ stable-diffusion-webui-forge/,
activate venv: source/my_venv/bin/activate,
install software: pip install -r requirements_version.txt,
edit webui-user.sh: 

export COMMANDLINE_ARGS="--all-in-fp16 --disable-gpu-warning --disable-nan-check --opt-split-attention-v1 --upcast-sampling --use-cpu interrogate gfpgan scunet codeformer"
export SAFETENSORS_FAST_GPU=1

run the software with "./webui.sh"



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Max Clock Freq. (MHz):   5756                               
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
      Size:                    98449352(0x5de37c8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98449352(0x5de37c8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98449352(0x5de37c8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98449352(0x5de37c8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx900                             
  Uuid:                    GPU-0213f2d6874e1844               
  Marketing Name:          AMD Radeon RX Vega                 
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
  Chip ID:                 26751(0x687f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1590                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            56                                 
  SIMDs per CU:            4                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 472                                
  SDMA engine uCode::      434                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8372224(0x7fc000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx900:xnack-   
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

stable-diffusion-webui-forge was very fast with ROCM versions prior to 6.3.

<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/e2eef312-f8ff-41de-8904-8c50d3eef7ac" />

With the latest Nobara ROCM package 6.3 the speed decreased by almost 30 to 50 percent using DPM++2M scheduler. Speed decrease with Euler scheduler is dramatic, it went down from 3 to 5 it/sec to 1.25 it/sec.

I also installed a brand new Rhino Linux with latest ROCM 6.4.1 to verify and the speed decrease is the same.

Before i was able to generate 10 images in roughly 50 seconds as you can see in my screenshot above. Now with the latest update i am no longer able to generate 10 images per minute because generation speed dropped. It takes 20 to 30 seconds longer to generate 10 images.

The screenshot was taken after i updated from Nobara 41 to Nobara 42 to test the speed of the new linux version.

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-07-10T18:02:19Z)

Hi @RadeonVega-56. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — RadeonVega-56 (2025-07-14T13:05:18Z)

Another thing i noticed is that when you generate an image, the first iteration is faster. For example the first iteration runs and is displayed with 2.x it/second. All of the follwing iterations are displayed with 1.2x it/second and VAE encoding takes longer. This was not the case with the previous ROCM version. It stayed at 2.x it/second until the image was finished and VAE encoding was faster.

---

### 评论 #3 — RadeonVega-56 (2025-07-23T14:27:22Z)

Generation speed after todays updates to Nobara 42 is almost back to the level where it was before i opened this ticket. VAE encding is faster. The EULER scheduler runs with 2.5x it/seconds. About double speed than before. There where no updates to ROCM, just kernel and driver updates.

Maybe the problem is related to kernel or driver issues of the rolling release Nobara Linux.

<img width="2560" height="1123" alt="Image" src="https://github.com/user-attachments/assets/23af5cf0-99c9-4323-be40-fddad9e84622" />

FHD generation is back to less than 2 min per image. This has been my main issue. These images took much longer.

<img width="2550" height="959" alt="Image" src="https://github.com/user-attachments/assets/8084bdf2-51a4-4716-83e2-cb6726522233" />


---
