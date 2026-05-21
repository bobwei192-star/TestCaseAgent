# [Issue]: Poor performance with float32, good performance with float16 gfx1151

> **Issue #5807**
> **状态**: open
> **创建时间**: 2025-12-22T09:29:14Z
> **更新时间**: 2026-05-09T17:11:12Z
> **作者**: jrhip
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5807

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

float32 performance is unexpectedly low compared to float16 on gfx1151

Torch:

float16: 35.0 TFLOPS ✅
float32: 3.1 TFLOPS ❌

JAX:

float16: 29.7 TFLOPS ~✅
float32: 4.6 TFLOPS ❌

Related: https://github.com/ROCm/ROCm/issues/4499

### Operating System

Fedora 43

### CPU

AMD RYZEN AI MAX+ 395

### GPU

Radeon 8060S

### ROCm Version

Varies: 
Torch: 2.11.0a0+rocm7.11.0a20251221
JAX: 0.8.0, rocm 7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

```
import torch

a = torch.randn(4096, 4096, device='cuda', dtype=torch.float32)
b = torch.randn(4096, 4096, device='cuda', dtype=torch.float32)

# Warmup
for _ in range(10):
    c = a @ b
torch.cuda.synchronize()

import time
torch.cuda.synchronize()
start = time.perf_counter()
for _ in range(100):
    c = a @ b
torch.cuda.synchronize()
elapsed = time.perf_counter() - start

flops = 100 * 2 * 4096**3 / elapsed / 1e12
print(f"{flops:.1f} TFLOPS")
```

```
import jax
import jax.numpy as jnp
import time

a = jax.random.normal(jax.random.key(0), (4096, 4096), dtype=jnp.float32)
b = jax.random.normal(jax.random.key(1), (4096, 4096), dtype=jnp.float32)

# Warmup
for _ in range(10):
    c = a @ b
c.block_until_ready()

start = time.perf_counter()
for _ in range(100):
    c = a @ b
c.block_until_ready()
elapsed = time.perf_counter() - start

flops = 100 * 2 * 4096**3 / elapsed / 1e12
print(f"{flops:.1f} TFLOPS")
```

Note: To run JAX without a crash I had to build with gfx1151 added to targets https://github.com/ROCm/rocm-jax/issues/234
Easier to test in Pytorch, but I needed to check if it was a Pytorch-specific issue or not. 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
      Size:                    131151708(0x7d1375c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131151708(0x7d1375c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131151708(0x7d1375c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131151708(0x7d1375c) KB            
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
  Marketing Name:          Radeon 8060S Graphics              
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
  BDFID:                   49664                              
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
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65575852(0x3e89bac) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65575852(0x3e89bac) KB             
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
*******                  
Agent 3                  
*******                  
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
  Vendor Name:             AMD                                
  Feature:                 AGENT_DISPATCH                     
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        1(0x1)                             
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          64(0x40)                           
  Queue Type:              SINGLE                             
  Node:                    0                                  
  Device Type:             DSP                                
  Cache Info:              
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          0(0x0)                             
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            0                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:0                                  
  Memory Properties:       
  Features:                AGENT_DISPATCH
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    131151708(0x7d1375c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536(0x10000) KB                  
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131151708(0x7d1375c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:     

### Additional Information

OS:
NAME="Fedora Linux"
VERSION="43 (Workstation Edition)"
CPU: 
model name	: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151                            
  Marketing Name:          Radeon 8060S Graphics              
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    aie2                               
  Marketing Name:          AIE-ML

---

## 评论 (7 条)

### 评论 #1 — vladbelous (2025-12-23T05:26:28Z)

FWIW, I've also observed very poor fp32 performance on gfx1151, but found that it **_wildly_** varies by ROCm version and/or installation method.

I've done a custom LLM-like model benchmark with pytorch 2.9.1. The numbers are ms for forward pass time (lower is better).
- rocm 7.11.0a (installed via TheRock) -- 965ms
- rocm 7.1.1 (torch from repo.radeon.com/rocm/manylinux) -- 606ms
- rocm 7.1.x (torch from pytorch.org nightly) -- 536ms
- rocm 7.1.x (torch from pytorch.org nightly) with `HSA_OVERRIDE_GFX_VERSION=11.0.0` -- 243ms (!)
- rocm 6.4.x (torch from pytorch.org - must use `HSA_OVERRIDE_GFX_VERSION=11.0.0`) -- 242ms (!)

On Nvidia 3060 Ti - I'm getting 224ms, so Strix Halo has the potential to be competitive. Hopefully AMD can sort this out.

(performance for bf16 varies a bit as well, but nowhere near this significantly, and is slightly better on 7.11.0 and 7.1.1)


---

### 评论 #2 — Only8Bits (2026-01-04T15:11:33Z)

This also seems to affect gfx1100:

Torch:

FP32: 2.6 TFLOPS (even slower than gfx1151)
FP16: 65.7 TFLOPS
BF16: 66.3 TFLOPS

Kubuntu 24.04, Ryzen 5800X3D + Radeon 7900XT, Torch: 2.9.1+rocm7.1.1.lw.git351ff442

Tested FP32 with HSA_OVERRIDE_GFX_VERSION=11.0.0 (just in case), TORCH_BLAS_PREFER_HIPBLASLT=1 and 0, no changes.

---

### 评论 #3 — vladbelous (2026-01-05T20:09:22Z)

I've found that running my pytorch benchmarks with `PYTORCH_TUNABLEOP_ENABLED=1` makes the f32 performance much better and bf16 slightly better too, but more importantly, it becomes much more consistent between ROCm versions / installation methods.

Note that the first iteration will be extremely slow (could be 1-10 minutes, so make your test small-ish), but subsequent runs will be faster.
I don't see it as a viable solution, but seems quite informative -- it suggests the potential is there, but pytorch/ROCm is not picking the right kernels, by a big margin.

---

### 评论 #4 — LuXuxue (2026-01-07T05:02:31Z)

torch-2.11.0a0+rocm7.11.0a20260106-cp313-cp313-win_amd64 test on gfx1103 (using comfyui, sdxl, fp16 model+bf16 tiled vae):
PYTORCH_TUNABLEOP_ENABLED=1 does make better performance, speed up about 8%.

---

### 评论 #5 — vladbelous (2026-01-19T05:50:59Z)

@darren-amd , it's been almost a month and still no action taken here. Anything you can share?

---

### 评论 #6 — darren-amd (2026-01-19T16:49:12Z)

Thanks for checking in! We are aware of the performance issues with fp32 on gfx1151 and are actively looking into it. For gfx1100, there is a fix available here: https://github.com/ROCm/ROCm/issues/5725 that improves performance.

---

### 评论 #7 — jrhip (2026-05-09T17:11:12Z)

A more scientific test with more than one matmul size: 
(https://github.com/stas00/ml-engineering/blob/master/compute/accelerator/benchmarks/mamf-finder.py)

float16 is ~30 TFLOPS as before ✅
float32 is a little bit faster, 8.7 TFLOPS. But still a way off ~14-15. 

float16:

```
python mamf-finder.py --dtype float16 --m_range 0 20480 256 --n 4096 --k 4096 --output_file=2026-05-09-14:01:43.txt

** Dtype: torch.float16

** Platform/Device info:
- Linux fedora 7.0.4-200.fc44.x86_64 #1 SMP PREEMPT_DYNAMIC Fri May  8 16:02:43 UTC 2026 x86_64 
- _CudaDeviceProperties(name='Radeon 8060S Graphics', major=11, minor=5, gcnArchName='gfx1151', total_memory=64038MB, multi_processor_count=20, uuid=58580000-0000-0000-0000-000000000000, pci_bus_id=194, pci_device_id=0, pci_domain_id=0, L2_cache_size=2MB)

** Critical software versions:
- torch=2.11.0+rocm7.13.0a20260505
- hip=7.13.26176, cuda=None

** Critical environment variables:
- PYTORCH_TUNABLEOP_ENABLED=1

** Additional notes:
- benchmark version: 2

Across 79 shapes in range: m=[0, 20480, 256] | n=[4096] | k=[4096] in this run:
arithmetic mean: 32.3 TFLOPS
geometric mean:  31.9 TFLOPS

```

float32 (had to ctrl+c, was taking hours):

```
python mamf-finder.py --dtype float32 --m_range 0 20480 256 --n 4096 --k 4096 --output_file=2026-05-09-15:28:58.txt

** Dtype: torch.float32

** Platform/Device info:
- Linux fedora 7.0.4-200.fc44.x86_64 #1 SMP PREEMPT_DYNAMIC Fri May  8 16:02:43 UTC 2026 x86_64 
- _CudaDeviceProperties(name='Radeon 8060S Graphics', major=11, minor=5, gcnArchName='gfx1151', total_memory=64038MB, multi_processor_count=20, uuid=58580000-0000-0000-0000-000000000000, pci_bus_id=194, pci_device_id=0, pci_domain_id=0, L2_cache_size=2MB)

** Critical software versions:
- torch=2.11.0+rocm7.13.0a20260505
- hip=7.13.26176, cuda=None

** Critical environment variables:
- PYTORCH_TUNABLEOP_ENABLED=1

** Additional notes:
- benchmark version: 2

8.7(mean)    8.7(median)    8.9(max) TFLOPS
```

---
