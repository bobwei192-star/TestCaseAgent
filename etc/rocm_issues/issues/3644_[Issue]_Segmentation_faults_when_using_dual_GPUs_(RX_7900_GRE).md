# [Issue]: Segmentation faults when using dual GPUs (RX 7900 GRE)

> **Issue #3644**
> **状态**: closed
> **创建时间**: 2024-08-27T02:27:31Z
> **更新时间**: 2025-03-10T17:13:15Z
> **关闭时间**: 2024-08-28T14:51:31Z
> **作者**: han-minhee
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3644

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

#2804 
When using dual RX 7900 GRE setup, accessing the second GPU yields seg faults.

I tried reinstalling Ubuntu or ROCm but to no avail

### Operating System

NAME="Ubuntu" VERSION="24.04 LTS (Noble Numbat)"

### CPU

AMD Ryzen 9 7900 12-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Have a dual GPU setup that works as PCIe 5.0 X8 for each (ProArt X670E-CREATOR WIFI)
2. Clean install of Ubuntu 24.04
3. Install ROCm according to [the official document](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)
4. Do anything that works with the second GPU, and it will give segmentation fault

For pytorch,
`
>>> import torch
>>> X = torch.rand(2,3).cuda(0)
>>> Y = torch.rand(2,3).cuda(1)
Segmentation fault (core dumped)
`
[For rocHPCG](https://github.com/ROCm/rocHPCG/issues/80),
`
Memory access fault by GPU node-1 (Agent handle: 0x2308090) on address 0x77525e362000. Reason: Page not present or supervisor privilege. Aborted (core dumped)
`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.8.5 is loaded
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
  Name:                    AMD Ryzen 9 7900 12-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7900 12-Core Processor 
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
  Max Clock Freq. (MHz):   5482                               
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
      Size:                    98562356(0x5dff134) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98562356(0x5dff134) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98562356(0x5dff134) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-71be6bf20576cf7f               
  Marketing Name:          Radeon RX 7900 GRE                 
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
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1927                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 232                                
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
  Name:                    gfx1100                            
  Uuid:                    GPU-2a5814ccdc518719               
  Marketing Name:          Radeon RX 7900 GRE                 
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
    L2:                      6144(0x1800) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1927                               
  BDFID:                   1792                               
  Internal Node ID:        2                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 232                                
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
*** Done ***             

### Additional Information

I've also
1. disabled integrated GPU
2. enabled resizable bar
3. enabled above 4G decoding

---

## 评论 (6 条)

### 评论 #1 — han-minhee (2024-08-27T04:01:58Z)

When I launch some kernels by myself, it works without (seemingly) no problems.
I confirmed that [torch nightly](https://download.pytorch.org/whl/nightly/rocm6.2) works without the above issue.
So it might not be the problem with the rocm itself, but maybe a compatibility issue

---

### 评论 #2 — harkgill-amd (2024-08-27T14:34:01Z)

Hi @han-minhee, you mentioned launching kernels by yourself and testing using the ROCm 6.2  PyTorch wheel was successful. How were you initially installing torch when you ran into this error? 
```
import torch
X = torch.rand(2,3).cuda(0)
Y = torch.rand(2,3).cuda(1)
Segmentation fault (core dumped)
Memory access fault by GPU node-1 (Agent handle: 0x2308090) on address 0x77525e362000. Reason: Page not present or supervisor privilege. Aborted (core dumped)
```


---

### 评论 #3 — han-minhee (2024-08-27T14:38:08Z)

> How were you initially installing torch when you ran into this error? 

I was using torch 2.4 with rocm 6.1 installed by `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1`

---

### 评论 #4 — harkgill-amd (2024-08-27T18:06:28Z)

This is most likely a compatibility issue as only ROCm 6.2.0 is supported on Ubuntu 24.04. Please refer to the [compatibility matrix ](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#compatibility-matrix)for more information on this.

I was not able to reproduce this issue after installing PyTorch using the ROCm 6.1 wheel on Ubuntu 22.04. If possible, can you also give this a try?

---

### 评论 #5 — han-minhee (2024-08-28T01:45:21Z)

As my initial report says, I'm using ROCm 6.2 with Ubuntu 24.04. It was just that I was able to install torch with ROCm 6.1 without any apparent problem. So I guess the issue will be gone by the next release of PyTorch. Or just a subtle notice that the current torch version isn't compatible with 6.2 would do.

 And could you add GRE to the selectable device when opening a new issue? 

---

### 评论 #6 — harkgill-amd (2024-08-28T14:51:31Z)

@han-minhee, apologies for the confusion. To use torch with your ROCm 6.2.0 installation, it would be best to continue with the [6.2 nightly build](https://download.pytorch.org/whl/nightly/rocm6.2). The documentation will also be updated to reflect the new installation command shortly.
```
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.2/
```

The mismatch in your original configuration between the 6.2 installed on your system and the 6.1 torch installation is the most likely culprit for the seg faults as I was not able to reproduce them in my testing. If you do encounter them again, please leave a comment and I will re-open this issue to further investigate.

I have added the AMD Radeon RX 7900 GRE to the issue template, thanks for the heads up. 

---
