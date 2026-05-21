# [Issue]: HIP error on rocm/pytorch docker (gfx 1100) for float tensors

> **Issue #2950**
> **状态**: closed
> **创建时间**: 2024-03-06T19:38:38Z
> **更新时间**: 2024-05-14T04:04:42Z
> **关闭时间**: 2024-05-14T04:04:42Z
> **作者**: yash-s20
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon Pro W7900
> **URL**: https://github.com/ROCm/ROCm/issues/2950

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon Pro W7900** (颜色: #ededed)

## 描述

### Problem Description

I'm trying to use my AMD Radeon Pro W7900 to train ML models. I'm using the latest docker image provided to run rocm smoothly with python, despite rocm-smi and rocminfo identifying the gpu connected, python throws the following error when loading and printing a tensor from the gpu.

```
RuntimeError: HIP error: the operation cannot be performed in the present state
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```
What's odd is that int64 tensors work perfectly fine.

The host is Ubuntu 22.04 but the docker image is Ubuntu 20.04.

see how to reproduce the error below.

### Operating System

Ubuntu 20.04 LTS (Focal Fossa)

### CPU

12th Gen Intel Core i7-1260P

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Pulling and running the latest rocm/pytorch docker container as of 03/06/2024.
```
$ python
>>> import torch
>>> x = torch.tensor([34, 5, 20, 3], dtype=torch.int64, device='cuda')
>>> x # works fine
tensor([34,  5, 20,  3], device='cuda:0')
>>> x = torch.tensor([34, 5, 20, 3], dtype=torch.float32, device='cuda')
>>> x # breaks
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/_tensor.py", line 431, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/_tensor_str.py", line 664, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/_tensor_str.py", line 595, in _str_intern
    tensor_str = _tensor_str(self, indent)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/_tensor_str.py", line 347, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/_tensor_str.py", line 137, in __init__
    nonzero_finite_vals = torch.masked_select(
RuntimeError: HIP error: the operation cannot be performed in the present state
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

```

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
  Name:                    12th Gen Intel(R) Core(TM) i7-1260P
  Uuid:                    CPU-XX                             
  Marketing Name:          12th Gen Intel(R) Core(TM) i7-1260P
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
  Max Clock Freq. (MHz):   4700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32474808(0x1ef86b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32474808(0x1ef86b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32474808(0x1ef86b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-75ef8983826798b1               
  Marketing Name:          AMD Radeon PRO W7900               
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
  Chip ID:                 29768(0x7448)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1760                               
  BDFID:                   2304                               
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
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    47169536(0x2cfc000) KB             
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

The gpu is connected to the system using a egpu (enclosure): Razer Core X Chroma.

---

## 评论 (9 条)

### 评论 #1 — yash-s20 (2024-03-06T19:46:24Z)

Additionally, I tried the solutions on #2536 which seemed the closest issue but to no success.

---

### 评论 #2 — yash-s20 (2024-03-06T20:19:37Z)

not sure what's wrong, but I followed the bare metal pytorch-nightly installation instructions on https://rocm.docs.amd.com/projects/install-on-linux/en/develop/how-to/3rd-party/pytorch-install.html and that seems to work. If I have issues I will let you know on this thread! Keeping the issue open since docker is the recommended approach and that still doesn't work.

---

### 评论 #3 — nartmada (2024-03-06T22:20:03Z)

Internal ticket has been created for investigation.

---

### 评论 #4 — hongxiayang (2024-03-18T14:53:15Z)

@yash-s20 If you prefer docker, can you try rocm/pytorch-nightly:latest docker?

---

### 评论 #5 — alexxu-amd (2024-04-26T14:27:31Z)

In the latest rocm 6.1 docker image, this error can be solved by upgrading torch 2.1 to 2.3. Can you check if it works for you?@yash-s20 

---

### 评论 #6 — yash-s20 (2024-04-26T15:15:04Z)

Thank you for the replies! I was caught up in other threads but I will try both these methods out soon! 

---

### 评论 #7 — hongxiayang (2024-04-26T16:37:21Z)

@yash-s20  The fix is in pytorch 2.2+. You can also try this pytorch official wheels as below:
```
pip3 install torch --index-url https://download.pytorch.org/whl/rocm6.0
```

---

### 评论 #8 — rti (2024-04-26T19:30:07Z)

I can confirm that on a similar setup (Radeon RX 7900 XT/7900 XTX via Thunderbold 3 eGPU) the pytorch nightly fixes the problem:

#### ⛔ Failure on: rocm/pytorch:rocm6.1_ubuntu22.04_py3.10_pytorch_2.1.2 python
```
❱ echo "import torch\nprint(torch.randn(1, device='cuda'))" | docker run --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri -i --rm rocm/pytorch:rocm6.1_ubuntu22.04_py3.10_pytorch_2.1.2 python
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/_tensor.py", line 431, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/_tensor_str.py", line 664, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/_tensor_str.py", line 595, in _str_intern
    tensor_str = _tensor_str(self, indent)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/_tensor_str.py", line 347, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/_tensor_str.py", line 137, in __init__
    nonzero_finite_vals = torch.masked_select(
RuntimeError: HIP error: the operation cannot be performed in the present state
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```
#### ✅ Works on rocm/pytorch-nightly:latest
```
❱ echo "import torch\nprint(torch.randn(1, device='cuda'))" | docker run --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri -i --rm rocm/pytorch-nightly:latest python                       
tensor([-0.3552], device='cuda:0')
```

Thanks a lot for your work on that! ❤️ 

---

### 评论 #9 — yash-s20 (2024-05-14T04:04:42Z)

Can confirm W7900 works for `rocm/pytorch:latest` (which wasn't working prior) and native on ubuntu 22.04 LTS (without docker, as was already working). The docker images are too big (60+GB all layers combined) so I was not able to make enough space to test the nightly image.

Thank you for the fixes! Closing the issue.

---
