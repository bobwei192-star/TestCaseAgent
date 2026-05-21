# [Issue]: Rocm7 Pytorch Docker: AOTriton not available for gfx1151

> **Issue #5404**
> **状态**: closed
> **创建时间**: 2025-09-20T21:10:27Z
> **更新时间**: 2025-11-01T00:13:18Z
> **关闭时间**: 2025-11-01T00:13:18Z
> **作者**: waltercool
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5404

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Using official latest docker: https://hub.docker.com/layers/rocm/pytorch/latest/images/sha256-f6095568e49a2d2f808188920e45f8270a15b9c3f1a7ee49cadb2420e5cf3543

This issue have been reported into TheRock, but seems like it also happens at official release.

Issue reported at TheRock: https://github.com/ROCm/TheRock/issues/1364
Test: https://github.com/lhl/strix-halo-testing/blob/main/torch-therock/test-pytorch-flashattention.py

```
# python test-pytorch-flashattention.py 
=== PyTorch Installation Check ===
PyTorch version: 2.8.0+rocm7.0.0.git64359f59
PyTorch ROCm version: 7.0.51831-a3e329ad8
CUDA available: True
Device count: 1
Device name: AMD Radeon Graphics

=== Flash Attention Support Check ===
/usr/lib/python3.12/contextlib.py:105: FutureWarning: `torch.backends.cuda.sdp_kernel()` is deprecated. In the future, this context manager will be removed. Please see `torch.nn.attention.sdpa_kernel()` for the new context manager, with updated signature.
  self.gen = func(*args, **kwds)
Available SDP backends: <contextlib._GeneratorContextManager object at 0x7f9317be7260>
Flash Attention backend enabled
Test tensors created on cuda
/mnt/test-pytorch-flashattention.py:40: UserWarning: Memory efficient kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:859.)
  output = F.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:40: UserWarning: Memory Efficient attention has been runtime disabled. (Triggered internally at /pytorch/aten/src/ATen/native/transformers/sdp_utils_cpp.h:552.)
  output = F.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:40: UserWarning: Flash attention kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:861.)
  output = F.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:40: UserWarning: Flash attention was not compiled for current AMD GPU architecture. Attempting to run on architecture gfx1151 (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:241.)
  output = F.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:40: UserWarning: CuDNN attention kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:863.)
  output = F.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:40: UserWarning: Torch was not compiled with cuDNN attention. (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:618.)
  output = F.scaled_dot_product_attention(q, k, v)
Flash Attention test failed: No available kernel. Aborting execution.

=== AOTriton Check ===
AOTriton not available: No module named 'pyaotriton'

=== Environment Variables ===
ROCM_PATH: Not set
HIP_PATH: Not set
HIP_PLATFORM: Not set
HIP_ARCH: Not set
HSA_OVERRIDE_GFX_VERSION: Not set

=== Testing GFX Version Override ===
Set HSA_OVERRIDE_GFX_VERSION=11.0.0 to test gfx110x mapping
/mnt/test-pytorch-flashattention.py:78: UserWarning: Memory efficient kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:859.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:78: UserWarning: Memory Efficient attention has been runtime disabled. (Triggered internally at /pytorch/aten/src/ATen/native/transformers/sdp_utils_cpp.h:552.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:78: UserWarning: Flash attention kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:861.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:78: UserWarning: Flash attention was not compiled for current AMD GPU architecture. Attempting to run on architecture gfx1151 (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:241.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:78: UserWarning: CuDNN attention kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:863.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:78: UserWarning: Torch was not compiled with cuDNN attention. (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:618.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
✗ Flash Attention still failed with override: No available kernel. Aborting execution.

=== Flash Attention Backend Detection ===
/mnt/test-pytorch-flashattention.py:107: UserWarning: Memory efficient kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:859.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:107: UserWarning: Memory Efficient attention has been runtime disabled. (Triggered internally at /pytorch/aten/src/ATen/native/transformers/sdp_utils_cpp.h:552.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:107: UserWarning: Flash attention kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:861.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:107: UserWarning: Flash attention was not compiled for current AMD GPU architecture. Attempting to run on architecture gfx1151 (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:241.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:107: UserWarning: CuDNN attention kernel not used because: (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:863.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:107: UserWarning: Torch was not compiled with cuDNN attention. (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:618.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
✗ flash backend failed: No available kernel. Aborting execution.
/mnt/test-pytorch-flashattention.py:107: UserWarning: Mem Efficient attention was not compiled for current AMD GPU architecture. Attempting to run on architecture gfx1151 (Triggered internally at /pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:292.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
/mnt/test-pytorch-flashattention.py:107: UserWarning: Flash attention has been runtime disabled. (Triggered internally at /pytorch/aten/src/ATen/native/transformers/sdp_utils_cpp.h:540.)
  output = torch.nn.functional.scaled_dot_product_attention(q, k, v)
✗ mem_efficient backend failed: No available kernel. Aborting execution.
✓ math backend works
```

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

docker.io/rocm/pytorch:rocm7.0_ubuntu24.04_py3.12_pytorch_release_2.8.0

### ROCm Component

_No response_

### Steps to Reproduce

Just run ComfyUI and try any video with WAN 2.2. The memory requirements will be over 100GB for 2-3s video

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    131004020(0x7cef674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131004020(0x7cef674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131004020(0x7cef674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131004020(0x7cef674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
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
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50176                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 31                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    125829120(0x7800000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    125829120(0x7800000) KB            
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — harkgill-amd (2025-09-24T18:15:15Z)

Hi @waltercool, checking for AOTriton with `import pyaotriton` is incorrect in this case. The `pyaotriton` module is reserved for development use only and wouldn't be available in the docker images. A more appropriate check to see if AOTriton is installed is to confirm if libtorch_hip.so is linked against libaotriton.so - this is true in the case of the rocm/pytorch:latest image with it being linked against `libaotriton_v2.so.0.10.0`.

As for the errors, the docker image is using 0.10b which is missing commits that enable `gfx1151`, including https://github.com/ROCm/aotriton/commit/0e7d518e83e6ada6a41cbb8b8b48f50c652fdeeb. 

---

### 评论 #2 — waltercool (2025-09-24T18:21:53Z)

Many thanks @harkgill-amd for your kind response, please keep us posted once aotriton gets merged into the Docker for proper testing.

I do understand this may take a while from the official release.

---

### 评论 #3 — harkgill-amd (2025-09-29T18:12:05Z)

@waltercool, I think there's been a little misunderstanding here - the latest `rocm/pytorch` docker image already ships with aotriton `0.10b`. 
```
root@ba66843d22fa:/opt/venv/lib/python3.12/site-packages/torch/lib# ls -la
total 1795672
drwxr-xr-x  5 root root       4096 Sep 20 05:58 .
drwxr-xr-x 65 root root       4096 Sep 20 05:58 ..
drwxr-xr-x  7 root root       4096 Sep 20 05:58 aotriton.images
-rwxr-xr-x  1 root root     353992 Sep 20 05:58 libaoti_custom_ops.so
-rwxr-xr-x  1 root root   11154233 Sep 20 05:58 libaotriton_v2.so
-rwxr-xr-x  1 root root   11154233 Sep 20 05:58 libaotriton_v2.so.0.10.0
```

What we'd be waiting for is a newer image which bumps aotriton to `0.11`. This would introduce experimental support for gfx115x though I don't have a timeline on when this would be. 

---

### 评论 #4 — waltercool (2025-09-29T18:43:26Z)

Hi @harkgill-amd, I do understand that, this ticket is about gfx1151 and stating the current aotriton doesn't work for it, leading to an unoptimized use of memory with PyTorch until 0.11b gets released. 

Apologies if my comment was misunderstood. 

---

### 评论 #5 — hammmmy (2025-10-31T22:32:54Z)

Docker image option is now added in 7.1: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html#option-b-docker-installation and it supports AOTriton. This issue can now be closed.

---

### 评论 #6 — hammmmy (2025-10-31T22:35:17Z)

Need to 'export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1' before you run your scripts.

---

### 评论 #7 — waltercool (2025-11-01T00:13:18Z)

Thank you very much everyone! Hope this can help many users doing torch operations with the AI 300 series de devices!

---
