# [Issue]: llama.cpp Vulkan outperforms ROCm backend

> **Issue #4883**
> **状态**: open
> **创建时间**: 2025-06-04T21:55:12Z
> **更新时间**: 2026-01-07T19:38:38Z
> **作者**: Matthew-Jenkins
> **标签**: Under Investigation, hardware:Radeon, ROCm 6.3.1
> **URL**: https://github.com/ROCm/ROCm/issues/4883

## 标签

- **Under Investigation** (颜色: #0052cc)
- **hardware:Radeon** (颜色: #2B113F)
- **ROCm 6.3.1** (颜色: #ededed)

## 负责人

- schung-amd

## 描述

### Problem Description

After upgrading to Fedora 42, llamacpp vulkan is anywhere from at least as fast, to 50% faster than rocm. I'm glad I received a bunch of performance for free, but seems odd, don't it?

Using  with on lm studio 0.3.16, warm response with empty context
mungert/fairyr1-32b@iq2_m lm studio runtime vulkan v1.33.0, mesa-vulkan-drivers-20.0.6-1:
28.04 tok/sec
2188 tokens
0.06s to first token
Stop reason: EOS Token Found

mungert/fairyr1-32b@iq2_m lm studio runtime rocm v1.33.0:
20.29 tok/sec
861 tokens
0.05s to first token
Stop reason: User Stopped

mungert/qwen3-16b-a3b@iq2_m lm studio runtime vulkan v1.33.0, mesa-vulkan-drivers-20.0.6-1:
83.19 tok/sec
1480 tokens
0.14s to first token
Stop reason: User Stopped

mungert/qwen3-16b-a3b@iq2_m lm studio runtime rocm v1.33.0:
57.45 tok/sec
838 tokens
0.10s to first token
Stop reason: User Stopped

unsloth/gemma-3-27b-it-qat@iq4_xs lm studio runtime vulkan v1.33.0, mesa-vulkan-drivers-20.0.6-1:
20.67 tok/sec
534 tokens
2.16s to first token
Stop reason: User Stopped

unsloth/gemma-3-27b-it-qat@iq4_xs lm studio runtime rocm v1.33.0:
21.41 tok/sec
566 tokens
0.07s to first token
Stop reason: User Stopped

lmstudio-community/qwen3-0.b@q8_0 lm studio runtime vulkan v1.33.0, mesa-vulkan-drivers-20.0.6-1:
193.74 tok/sec
818 tokens
0.07s to first token
Stop reason: EOS Token Found

lmstudio-community/qwen3-0.b@q8_0 lm studio runtime rocm v1.33.0:
133.23 tok/sec
1314 tokens
0.01s to first token
Stop reason: EOS Token Found

NAME="Fedora Linux"
VERSION="42 (Workstation Edition)"
CPU: 
model name	: AMD Ryzen 7 5700X 8-Core Processor
GPU:
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
  Name:                    AMD Ryzen 7 5700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   4665                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-9065db9c627c65bd               
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
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2660                               
  BDFID:                   2560                               
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
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
  Packet Processor uCode:: 130                                
  SDMA engine uCode::      85                                 
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


### Operating System

Fedora 42

### CPU

AMD Ryzen 7 5700X 8-Core Processor

### GPU

AMD Radeon RX 6900 XT

### ROCm Version

ROCm 6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

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
  Name:                    AMD Ryzen 7 5700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   4665                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65757064(0x3eb5f88) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-9065db9c627c65bd               
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
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2660                               
  BDFID:                   2560                               
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
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
  Packet Processor uCode:: 130                                
  SDMA engine uCode::      85                                 
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


### Additional Information

_No response_

---

## 评论 (14 条)

### 评论 #1 — ppanchad-amd (2025-06-05T14:03:07Z)

Hi @Matthew-Jenkins. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-06-09T21:17:55Z)

Hi @Matthew-Jenkins, thanks for reporting this, I'll take a look. I'm seeing something similar with llama.cpp outside of lm studio on Ubuntu 24.04 + ROCm 6.4.1 + 7900XTX + default settings, although the performance gap is not as large as you're seeing.

---

### 评论 #3 — schung-amd (2025-06-11T16:04:49Z)

What are you setting for the number of GPU offload layers? I see significantly increased performance on the HIP build by increasing this; for example, with fairyr1-32b I'm seeing similar performance between the HIP and Vulkan builds without explicitly setting `-ngl`, but with `-ngl 100` the HIP backend is about twice as fast as Vulkan.

---

### 评论 #4 — Matthew-Jenkins (2025-06-13T05:09:44Z)

fairy is fully gpu offloaded. Are you using the IQ2_M quant? 100 isn't a valid number of layers for fairy 32B. It only has 64 layers. 

![Image](https://github.com/user-attachments/assets/e9348276-1027-41c5-b849-0d82711a4926)

on a compiled llamacpp using tag b5648 and compile command:
HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)"     cmake -S . -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1030 -DCMAKE_BUILD_TYPE=Release  -DLLAMA_CURL=OFF   && cmake --build build --config Release -- -j 16

and command
echo 'say hello' | ./llama-cli -fa -m ~/.lmstudio/models/Mungert/FairyR1-32B-GGUF/FairyR1-32B-iq2_m.gguf -ngl 64 -c 4096 -t 16 --mlock -co

llama_perf_sampler_print:    sampling time =      58.20 ms /   652 runs   (    0.09 ms per token, 11202.56 tokens per second)
llama_perf_context_print:        load time =    1652.55 ms
llama_perf_context_print: prompt eval time =     177.30 ms /     5 tokens (   35.46 ms per token,    28.20 tokens per second)
llama_perf_context_print:        eval time =   44259.88 ms /   647 runs   (   68.41 ms per token,    14.62 tokens per second)
llama_perf_context_print:       total time =   44590.40 ms /   652 tokens



Using the vulkan build from tag b5648 downloaded from their releases, same command:
llama_perf_sampler_print:    sampling time =      86.72 ms /   943 runs   (    0.09 ms per token, 10873.83 tokens per second)
llama_perf_context_print:        load time =    3678.36 ms
llama_perf_context_print: prompt eval time =     152.64 ms /     5 tokens (   30.53 ms per token,    32.76 tokens per second)
llama_perf_context_print:        eval time =   54150.19 ms /   938 runs   (   57.73 ms per token,    17.32 tokens per second)
llama_perf_context_print:       total time =   54600.82 ms /   943 tokens


Hip build:
echo 'say hello' | ./llama-cli -fa -m ~/.lmstudio/models/Mungert/FairyR1-32B-GGUF/FairyR1-32B-iq2_m.gguf -ngl 999 -c 4096 -t 16 --mlock -co

llama_perf_sampler_print:    sampling time =      17.59 ms /   375 runs   (    0.05 ms per token, 21322.57 tokens per second)
llama_perf_context_print:        load time =    1691.73 ms
llama_perf_context_print: prompt eval time =     120.87 ms /     5 tokens (   24.17 ms per token,    41.37 tokens per second)
llama_perf_context_print:        eval time =   16472.58 ms /   370 runs   (   44.52 ms per token,    22.46 tokens per second)
llama_perf_context_print:       total time =   16648.72 ms /   375 tokens


vulkan:
llama_perf_sampler_print:    sampling time =      20.02 ms /   329 runs   (    0.06 ms per token, 16431.10 tokens per second)
llama_perf_context_print:        load time =    3972.70 ms
llama_perf_context_print: prompt eval time =      99.50 ms /     5 tokens (   19.90 ms per token,    50.25 tokens per second)
llama_perf_context_print:        eval time =   10743.61 ms /   324 runs   (   33.16 ms per token,    30.16 tokens per second)
llama_perf_context_print:       total time =   10899.35 ms /   329 tokens


I'm not sure why ngl=999 improves performance. Seems like a bug to me since there are only 64 layers. But ok. In any event, ngl=64 there is a very slight vulkan lead. ngl=999 vulkan is much better.

---

### 评论 #5 — Matthew-Jenkins (2025-06-13T05:12:43Z)

testing with ngl=100
hip:
llama_perf_sampler_print:    sampling time =      17.23 ms /   344 runs   (    0.05 ms per token, 19969.81 tokens per second)
llama_perf_context_print:        load time =    1664.86 ms
llama_perf_context_print: prompt eval time =     120.19 ms /     5 tokens (   24.04 ms per token,    41.60 tokens per second)
llama_perf_context_print:        eval time =   15054.10 ms /   339 runs   (   44.41 ms per token,    22.52 tokens per second)
llama_perf_context_print:       total time =   15227.70 ms /   344 tokens


vulkan:
llama_perf_sampler_print:    sampling time =      16.64 ms /   304 runs   (    0.05 ms per token, 18271.43 tokens per second)
llama_perf_context_print:        load time =    3947.57 ms
llama_perf_context_print: prompt eval time =      82.86 ms /     5 tokens (   16.57 ms per token,    60.34 tokens per second)
llama_perf_context_print:        eval time =    9864.54 ms /   299 runs   (   32.99 ms per token,    30.31 tokens per second)
llama_perf_context_print:       total time =    9996.41 ms /   304 tokens


---

### 评论 #6 — schung-amd (2025-06-13T15:22:40Z)

Thanks for checking! After testing again today, I'm unable to reproduce the speedup I saw vs. Vulkan on 7900XTX; with my reproducer, the metrics are generally similar to

HIP:
llama_perf_sampler_print:    sampling time =      38.14 ms /   499 runs   (    0.08 ms per token, 13084.41 tokens per second)
llama_perf_context_print: prompt eval time =      74.42 ms /     8 tokens (    9.30 ms per token,   107.50 tokens per second)
llama_perf_context_print:        eval time =   18150.01 ms /   490 runs   (   37.04 ms per token,    27.00 tokens per second)

Vulkan:
llama_perf_sampler_print:    sampling time =      42.81 ms /   401 runs   (    0.11 ms per token,  9367.85 tokens per second)
llama_perf_context_print: prompt eval time =      62.84 ms /     8 tokens (    7.86 ms per token,   127.30 tokens per second)
llama_perf_context_print:        eval time =    9282.18 ms /   392 runs   (   23.68 ms per token,    42.23 tokens per second)

> Seems like a bug to me since there are only 64 layers

The max is actually 65 according to the output; with `-ngpu 64`,
```
load_tensors: offloading 64 repeating layers to GPU
load_tensors: offloaded 64/65 layers to GPU
```
I don't know if this is a bug or intentional behavior by llama.cpp. Regardless, setting `-ngl` unnecessarily high (like 100 or 999) will max it out. 

Based on some internal tickets it seems like poor performance in llama.cpp is a known issue, and we have several folks working on it. For now I'd suggest using a different framework such as vLLM if possible or just use the Vulkan backend, I don't see any workarounds or parameter settings for llama.cpp that give a performance gain for HIP over Vulkan at the moment.

---

### 评论 #7 — Matthew-Jenkins (2025-06-13T16:14:09Z)

I don't think the 6900 xt is compatible with vllm?

---

### 评论 #8 — zeFresk (2025-06-20T16:37:04Z)

Hello, I just wanted to post some stats I collected two months ago with my 9070XT on rocm 6.4. I compared the vulkan and rocm backends for llama.cpp using the same benchmarks. The results are aggregated across a lot of runs, so the error bars may be too small to be visible. The graph shows the average token/s across all runs.

![Image](https://github.com/user-attachments/assets/9dfcb845-2ace-4619-9808-14fb743342e8)

Overall, the rocm 6.4 backend was slower than the vulkan backend on all models, even with flash attention enabled.

For now, I would suggest sticking to the vulkan backend if you have a 9070 XT. Otherwise, I got very good results using the vLLM docker image from this tutorial: [https://docs.vllm.ai/en/v0.6.5/getting_started/amd-installation.html](https://docs.vllm.ai/en/v0.6.5/getting_started/amd-installation.html), and quantizing the models myself.

---

### 评论 #9 — SimSonic (2025-10-13T09:05:29Z)

Hi! I'm measured LM Studio's new beta ROCm-based llama.cpp backend and it is slower than Vulkan on 15%.

Is any information about issue?

---

### 评论 #10 — FengZi-lv (2025-12-04T10:42:01Z)

> Hi! I'm measured LM Studio's new beta ROCm-based llama.cpp backend and it is slower than Vulkan on 15%.你好！我测试了 LM Studio 新发布的基于 ROCm 的 llama.cpp 后端，发现其速度比 Vulkan 慢了 15%。
> 
> Is any information about issue?有关这个问题的任何信息？

same here.

---

### 评论 #11 — GreenShadows (2025-12-05T10:16:54Z)

> Hi! I'm measured LM Studio's new beta ROCm-based llama.cpp backend and it is slower than Vulkan on 15%.
> 
> Is any information about issue?

The effect of Vulkan API being the focus of Llama.cpp's optimization strategy, fine-tuning performance almost daily. AMD does not seem to have anyone working on their Llama.cpp Git, and ROCm is also not moving as fast as they are.

---

### 评论 #12 — skewty (2026-01-07T16:17:53Z)

At CES a few days ago AMD just pretended ROCm 7.2 is the best strategy to do AI workloads on AMD GPUs. Issues such as this one show a very different story. Why would any corporation trust AMD in AI when issues like this linger in silence? I am looking to draft up a proposal to buy some AI hardware for the corporation I work for and this issue will likely be a decisive factor.

---

### 评论 #13 — schung-amd (2026-01-07T19:28:53Z)

If llama.cpp is going to be your main usecase and you're restricted to Radeon cards, then yes, you would be better served using Vulkan or other hardware (although I haven't seen a comparison between Vulkan and CUDA with llama.cpp, Vulkan may still be the winner there). 

In general though I think taking this specific issue as a catch-all for AI workloads is a bit disingenuous, as llama.cpp is only one of many AI frameworks. Obviously we'd like to be highly performant for all users in all usecases, but with limited resources we can't have all of the bases covered all the time, and taking marketing presentations like that as engineering truth will always result in a negative impression.

As for progress on this issue, Radeon performance in general has been a hot topic over the last couple months, especially in the context of MIOpen kernel improvement. It's possible that these improvements may also help llama.cpp, but I don't think we're quite at the stage to benchmark yet. When we've made some strides on that front, we may have the bandwidth to drill down llama.cpp performance specifically.

---

### 评论 #14 — GreenShadows (2026-01-07T19:38:38Z)

This argument about limited resources is a joke, and this mentality is what is holding AMD back.

AMD is not a corner store—it’s a multi‑billion‑dollar corporation. And it would already be a trillion-dollar company if it weren't for the software problems.

If additional capital is required, they could issue $5-10 billion in shares and direct those funds toward solving the software challenges that are critical to maintaining and expanding their consumer base.  

Meanwhile, llama.cpp stands out as one of the most widely adopted tools among general consumers. But please ignore that and continue to embarrass yourselves in every review.

---
