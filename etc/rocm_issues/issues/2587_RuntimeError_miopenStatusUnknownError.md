# RuntimeError: miopenStatusUnknownError

> **Issue #2587**
> **状态**: closed
> **创建时间**: 2023-10-19T22:52:46Z
> **更新时间**: 2024-07-22T18:22:18Z
> **关闭时间**: 2024-07-22T18:22:18Z
> **作者**: rasemailcz
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2587

## 描述

### Using

[rocm/pytorch:rocm5.7_ubuntu20.04_py3.9_pytorch_2.0.1](https://hub.docker.com/layers/rocm/pytorch/rocm5.7_ubuntu20.04_py3.9_pytorch_2.0.1/images/sha256-4dd86046e5f777f53ae40a75ecfc76a5e819f01f3b2d40eacbb2db95c2f971d4?context=explore) 

`uname -a`

`Linux nid005131 5.14.21-150400.24.46_12.0.73-cray_shasta_c #1 SMP Thu May 18 23:03:34 UTC 2023 (9c4698c) x86_64 x86_64 x86_64 GNU/Linux`

`rocminfo`

```[37mROCk module is loaded[0m
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          NO

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
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
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131320684(0x7d3cb6c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131320684(0x7d3cb6c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131320684(0x7d3cb6c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    132112468(0x7dfe054) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132112468(0x7dfe054) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132112468(0x7dfe054) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        2                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    132112468(0x7dfe054) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132112468(0x7dfe054) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132112468(0x7dfe054) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 4                  
*******                  
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        3                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    132090576(0x7df8ad0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132090576(0x7df8ad0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132090576(0x7df8ad0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 5                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-a98e0d77ca91cb4a               
  Marketing Name:          AMD Instinct MI250X                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    4                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29704(0x7408)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   53504                              
  Internal Node ID:        4                                  
  Compute Unit:            110                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 63                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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

`error:`

```MIOpen Error: /long_pathname_so_that_rpms_can_package_the_debug_info/src/extlibs/MLOpen/src/hip/handlehip.cpp:643: Failed getting available memory: invalid argument
MIOpen Error: /long_pathname_so_that_rpms_can_package_the_debug_info/src/extlibs/MLOpen/src/hip/handlehip.cpp:643: Failed getting available memory: invalid argument
Traceback (most recent call last):
  File "/users/petlikra/ddpmst/scripts/image_train_nodiff.py", line 528, in <module>
    main(conf_arg)
  File "/users/petlikra/ddpmst/scripts/image_train_nodiff.py", line 148, in main
    frame_blurred_tm1_m1p1 = torchvision.transforms.functional.gaussian_blur(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torchvision-0.15.2a0+fa99a53-py3.9-linux-x86_64.egg/torchvision/transforms/functional.py", line 1386, in gaussian_blur
    output = F_t.gaussian_blur(t_img, kernel_size, sigma)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torchvision-0.15.2a0+fa99a53-py3.9-linux-x86_64.egg/torchvision/transforms/_functional_tensor.py", line 761, in gaussian_blur
    img = conv2d(img, kernel, groups=img.shape[-3])
RuntimeError: miopenStatusUnknownError```

---

## 评论 (7 条)

### 评论 #1 — nartmada (2024-04-07T21:15:26Z)

Hi @rasemailcz, apologies for the lack of response.  Can you please try latest ROCm 6.0.2 and see if your issue has been resolved?  Thanks.

---

### 评论 #2 — nartmada (2024-04-07T21:17:01Z)

Hi @yanbosmu, please refer to https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html for installation guide.  Thanks.

---

### 评论 #3 — rasemailcz (2024-04-08T10:23:41Z)

@nartmada Just to be sure that I understand you correctly - you propose that I install ROCm 6.0.2 and then compile torch and torchvision from source?

---

### 评论 #4 — nartmada (2024-04-08T14:43:24Z)

@rasemailcz, let's rewind a bit.  Can you please share your repro steps?  We can try to repro the issue here.  Thanks.



---

### 评论 #5 — rasemailcz (2024-04-09T11:59:05Z)

@nartmada I shared the repro steps at the beginning. The thing is that I used the [rocm/pytorch:rocm5.7_ubuntu20.04_py3.9_pytorch_2.0.1 docker image](https://hub.docker.com/layers/rocm/pytorch/rocm5.7_ubuntu20.04_py3.9_pytorch_2.0.1/images/sha256-4dd86046e5f777f53ae40a75ecfc76a5e819f01f3b2d40eacbb2db95c2f971d4?context=explore) ...

---

### 评论 #6 — v-iashin (2024-04-14T08:09:58Z)

it happened to me as well. MWE:
```
import torch
proj = torch.nn.Conv3d(10, 16, kernel_size=(2, 16, 16), stride=(2, 16, 16)).cuda()
a = torch.randn(2, 10, 16, 224, 224).cuda()
print(proj(a).shape)
# RuntimeError: miopenStatusUnknownError
```

torch+rocm was installed through `pip`: `torch==2.2.1+rocm5.7`

downgrading `rocm` and `torch` appropriately helped:
```
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/rocm5.6
```

---

### 评论 #7 — harkgill-amd (2024-07-22T18:22:18Z)

Hi @rasemailcz, I was unable to reproduce your issue with the latest Pytorch on ROCm image found at [rocm/pytorch](https://hub.docker.com/r/rocm/pytorch). 

In my experiments, I ran rocminfo and also tried the example shared by @v-iashin. I tried both of these using the [docker image with PyTorch pre-installed](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/3rd-party/pytorch-install.html#using-a-docker-image-with-pytorch-pre-installed) and [using a wheels package](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/3rd-party/pytorch-install.html#using-a-wheels-package). Neither of these tests resulted in the `RuntimeError: miopenStatusUnknownError`.

If you are still encountering this issue after following the steps at [Installing PyTorch for ROCm](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/3rd-party/pytorch-install.html), please re-open this issue. Thanks!

---
