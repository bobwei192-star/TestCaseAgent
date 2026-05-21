# [Issue]: Unable to create even a single tensor on Pytorch 

> **Issue #3040**
> **状态**: closed
> **创建时间**: 2024-04-18T13:25:48Z
> **更新时间**: 2024-06-24T13:56:32Z
> **关闭时间**: 2024-06-24T13:56:32Z
> **作者**: kjhanjee
> **标签**: ROCm 6.0.0, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/3040

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

Hi All,

I'm trying to use ROCm 6.0 with Pytorch for some deep learning experiments. 

My system config is - 

NAME="Ubuntu"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
CPU: 
model name	: AMD Ryzen 5 7600X 6-Core Processor
GPU:
  Name:                    AMD Ryzen 5 7600X 6-Core Processor 
  Marketing Name:          AMD Ryzen 5 7600X 6-Core Processor 
  Name:                    gfx1100                            
  Marketing Name:          Radeon RX 7900 XTX                 
      Name:                    amdgcn-amd-amdhsa--gfx1100         
  Name:                    gfx1036                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1036 

The code that I'm trying 
tensor = torch.zeros(1).cuda()
tensor

The error that I'm getting: 
HIP error: shared object initialization failed
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

What I've tried until now:
1. Uninstalling and Reinstalling ROCm and Related Packages from Ubuntu
2. Uninstalling complete amdgpu package (including rocm, and amdgpu-install)
3. Reinstalling Ubuntu from scratch and following the instructions provided for rocm installation from scratch
4. Following instructions as is from here(https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/install-radeon.html) including prerequisites, installation, and post install checks. I followed the amdgpu-install package manager method


Also, I installed pytorch using the wheels in AMD repo
https://repo.radeon.com/rocm/manylinux/rocm-rel-6.0.2/torch-2.1.2+rocm6.0-cp310-cp310-linux_x86_64.whl
https://repo.radeon.com/rocm/manylinux/rocm-rel-6.0.2/torchvision-0.16.1+rocm6.0-cp310-cp310-linux_x86_64.whl
pip3 install --force-reinstall torch-2.1.2+rocm6.0-cp310-cp310-linux_x86_64.whl torchvision-0.16.1+rocm6.0-cp310-cp310-linux_x86_64.whl


I am not really sure what to do now to get this working. Any help is appreciated


### Operating System

UBUNTU 22.04 LTS Jammy

### CPU

7600X

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.0.0

### ROCm Component

hipTensor

### Steps to Reproduce

1. Download UBUNTU image from their website
2. Install UBUNTU 22.04 LTS
3. Install ROCM as per the documentation above
4. Install the pytorch wheels from the above links
5. try creating a tensor

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
  Name:                    AMD Ryzen 5 7600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 7600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   5453                               
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
      Size:                    32013344(0x1e87c20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32013344(0x1e87c20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32013344(0x1e87c20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-9e3333f65b92c1b9               
  Marketing Name:          Radeon RX 7900 XTX                 
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
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      19                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   4864                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 20                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    524288(0x80000) KB                 
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32 

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — Engininja2 (2024-04-18T22:32:13Z)

Try setting HIP_VISIBLE_DEVICES to hide your gfx1036 gpu from pytorch
```sh
export HIP_VISIBLE_DEVICES="0"
```

---

### 评论 #2 — kjhanjee (2024-04-19T06:36:57Z)

> Try setting HIP_VISIBLE_DEVICES to hide your gfx1036 gpu from pytorch
> ```sh
> export HIP_VISIBLE_DEVICES="0"
> ```

I have tried this as well to no avail.

---

### 评论 #3 — kjhanjee (2024-04-19T06:37:43Z)

> Try setting HIP_VISIBLE_DEVICES to hide your gfx1036 gpu from pytorch
> ```sh
> export HIP_VISIBLE_DEVICES="0"
> ```

I will try and see if I can disable the igpu from bios and see if that works 

---

### 评论 #4 — kjhanjee (2024-04-19T08:54:12Z)

This worked after disabling the igpu. In the documentation it talks about x670 chipset for disabling igpu but I think the same process will have to be followed by all AM5 chipsets

---

### 评论 #5 — IMbackK (2024-04-19T11:40:14Z)

can you try ROCR_VISIBLE_DEVICES=0 ? this is the same as HIP_VISIBLE_DEVICES but one layer down so could work where disableing the igpu dose and HIP_VISIBLE_DEVICES dose not

---

### 评论 #6 — kjhanjee (2024-04-19T16:03:25Z)

> can you try ROCR_VISIBLE_DEVICES=0 ? this is the same as HIP_VISIBLE_DEVICES but one layer down so could work where disableing the igpu dose and HIP_VISIBLE_DEVICES dose not

Will try this and let you know

---

### 评论 #7 — ppanchad-amd (2024-06-21T18:58:51Z)

@kjhanjee Did you have a chance to try ROCR_VISIBLE_DEVICES=0? If your issue is resolved, please close the ticket. Thanks!

---

### 评论 #8 — kjhanjee (2024-06-22T11:24:17Z)

I did but what worked for me was disabling igpu from the bios

---
