# [Issue]: error type not found - 780M, Model IBM granite3-dense:8b , ROCm enabled, VRAM 16GB

> **Issue #5452**
> **状态**: closed
> **创建时间**: 2025-10-01T01:15:34Z
> **更新时间**: 2026-04-07T18:41:50Z
> **关闭时间**: 2026-04-07T18:40:24Z
> **作者**: reywang18
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5452

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- darren-amd

## 描述

### Problem Description

NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU: 
model name      : AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
GPU:
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Name:                    gfx1102                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1102         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    aie2                               
  Marketing Name:          AIE-ML           
 
       
Sep 28 20:18:13 U24 ollama[25793]: time=2025-09-28T20:18:13.707-04:00 level=DEBUG source=ggml.go:276 msg="key with type not found" key=general.alignment default=32
Issue - related to "key with type not found", possible AMD driver issue



### Operating System

24.04.3 LTS

### CPU

 AMD Ryzen 7 7840HS w/ Radeon 780M Graphics

### GPU

780M iGPU

### ROCm Version

6.12.12

### ROCm Component

_No response_

### Steps to Reproduce

With Linux ollama set,  Model IBM granite3-dense:8b and with modelfile I added a model with num_gpu = 0
Run both models same time in Open WebUI.
Notice original with VRAM, it prompts back 44444444444.
And ollama log shows error type not found.

With create modelfile option, I added a model for testing, set num_gpu = 0. I ran both models with Open WebUI, clearly it has issue with VRAM (ROCm) active. Noticed token rates are worsen in model num_gpu = 0, such 7 tokens vs 23 tokens. A ROCm driver issue I think.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5137                               
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
      Size:                    49115692(0x2ed722c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49115692(0x2ed722c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49115692(0x2ed722c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    49115692(0x2ed722c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
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
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           7(0x7)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   50688                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 40                                 
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16777216(0x1000000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16777216(0x1000000) KB             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
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
      Size:                    49115692(0x2ed722c) KB             
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
      Size:                    49115692(0x2ed722c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***            

### Additional Information

_No response_

---

## 评论 (25 条)

### 评论 #1 — ppanchad-amd (2025-10-01T14:18:21Z)

Hi @reywang18. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — reywang18 (2025-10-01T18:23:32Z)

It is easy for to do a repro. I wonder is there a better way to collect more ROCm error messages for trouble shooting.

---

### 评论 #3 — darren-amd (2025-10-15T15:34:49Z)

Hi @reywang18,

Could you please provide the full logs for the error, as well as the dmesg logs? The displayed error seems to be more of a warning than an error message so the full logs should be more informative. Thanks!

---

### 评论 #4 — reywang18 (2025-10-16T14:39:49Z)

[

[rocm.tar.gz](https://github.com/user-attachments/files/22952323/rocm.tar.gz)

](url)

Here is the file

---

### 评论 #5 — darren-amd (2025-12-01T15:54:48Z)

Thanks @reywang18,

Would you mind trying on the latest ROCm/amdgpu by following the instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) and seeing if the issue persists? Also I noticed from your `rocminfo` output that your device is being displayed as `gfx1102`, have you overridden this with an environment variable or do you have another GPU?

---

### 评论 #6 — darren-amd (2025-12-22T16:54:49Z)

Closing due to inactivity, please feel free to reopen or create a new ticket if the issue persists, thanks!

---

### 评论 #7 — reywang18 (2025-12-22T20:04:09Z)

output that your device is being displayed as gfx1102
This is a built-in GPU, no other GPU in it.
So what setting I should do, ( not gfx1102 ) ?

---

### 评论 #8 — darren-amd (2025-12-22T21:12:05Z)

That's a bit strange, could you verify that `HSA_OVERRIDE_GFX_VERSION` is not set somewhere? A 780M should be displayed as `gfx1103` and not `gfx1102`.

---

### 评论 #9 — reywang18 (2025-12-22T23:40:29Z)

Based on this blog, https://blog.syddel.uk/?p=625
I set HSA_OVERRIDE_GFX_VERSION to 11.0.2.

From the above, my GPU is a gfx1103_r1, which equates to LLVM target 11.0.3 (which isn’t listed as a supported AMD GPU on the Ollama github page).

$ ollama ps
NAME                                            ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
granite3-dense:8b                               199456d876ee    6.7 GB    100% GPU     4096       4 minutes from now    
hf.co/unsloth/granite-4.0-h-tiny-GGUF:latest    51a1639bd554    5.1 GB    100% GPU     4096       4 minutes from now    

I run tests thru  open-webui setup.
It seems no gibbish here few queries started with granite-4.0-h-tiny-GGUF:latest, then I switched over grantie3.
So Ollama ps, shows 2 models are loaded.

Then run 1 query against granite3, I got.
granite3-dense:8b
Today at 6:31 PM
4444444444444444444444444444444

I continue to use model granite-4.0-h-tiny, it seems no issues.

$ ollama -v
ollama version is 0.12.3

---

### 评论 #10 — reywang18 (2026-01-07T00:34:35Z)

ru@U24:~/ollama/model$ ollama show  hf.co/unsloth/granite-4.0-h-tiny-GGUF    **## perfect, no issue**
  Model
    architecture        granitehybrid    
    parameters          6.94B            
    context length      1048576          
    embedding length    1536             
    quantization        unknown          

  Capabilities
    completion    
    tools         

ru@U24:~/ollama/model$ ollama show  granite3-dense:8b   **## has issue on this model**
  Model
    architecture        granite    
    parameters          8.2B       
    context length      4096       
    embedding length    4096       
    quantization        Q4_K_M     

  Capabilities
    completion    
    tools         

  System
    You are Granite, an AI language model developed by IBM in 2024.    

  License
    Apache License               
    Version 2.0, January 2004    
    ...                          

ru@U24:~/ollama/model$ ollama ps
NAME                                            ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
hf.co/unsloth/granite-4.0-h-tiny-GGUF:latest    51a1639bd554    5.1 GB    100% GPU     4096       4 minutes from now    
granite3-dense:8b                                                   199456d876ee    6.7 GB    100% GPU     4096       4 minutes from now    

After more than 4+ chat requests, granite3 has gebbish replies. And granite4.0-h is still showed perfect.

---

### 评论 #11 — darren-amd (2026-02-04T19:36:00Z)

Hi @reywang18,

I got a hold of a `gfx1103` system and gave this a try without the override via `HSA_OVERRIDE_GFX_VERSION` and was unable to reproduce the issue. Could you please try installing the latest ollama version and giving it another try?

My steps:
```
curl -fsSL https://ollama.com/install.sh | sh
ollama run granite3-dense:8b
```

---

### 评论 #12 — reywang18 (2026-02-04T21:52:31Z)

I did the step; and system is rebooted here. And I checked with '$ amdgpu_top' .
And noticed VRAM and GTT, no usages at all.

I have this in settings.
$ env | grep 11
HSA_OVERRIDE_GFX_VERSION=11.0.2

Should I remove it and try it again ?

---

### 评论 #13 — darren-amd (2026-02-04T21:55:24Z)

Hi,

Just to clarify, are you observing no VRAM usage while running the model or are you unable to run the model? Also yes, I was able to get the workload running without the overridden GFX version.

---

### 评论 #14 — reywang18 (2026-02-04T22:18:43Z)

Able to run model (without 4444 errors), very slow though. 
We want a fix, run fast VRAM/GTT. It is a 64GB box.
My previous setup, it ables to use VRAM properly.

---

### 评论 #15 — darren-amd (2026-02-06T19:55:48Z)

Hi,

Glad to hear that the model is running now. For the performance related issues you are reporting, would you mind creating a new ticket to track it? Please include more details on the performance issues you are experiencing, thanks!

---

### 评论 #16 — reywang18 (2026-02-06T20:29:29Z)

Nope, we can't close this. Then why we are buying 780M, and GPU can't be enabled here.
Please update the setup ROCm. I need the GPU running with ollama model and get back its high performance.

---

### 评论 #17 — darren-amd (2026-02-06T20:55:37Z)

Hi,

I have reopened the ticket. Could you elaborate more on what you mean by "GPU can't be enabled here"? What kind of performance issues are you experiencing?

---

### 评论 #18 — reywang18 (2026-02-06T21:01:28Z)

Linux tool amdgpu_top shows no GPU, VRAM not active, 0 usage.
So it is not fixed.  Before I saw VRAM usages are high, and I got 44444 errors.

Your step,
curl -fsSL https://ollama.com/install.sh | sh
ollama run granite3-dense:8b
Seems GPU/VRAM is disabled here.

---

### 评论 #19 — reywang18 (2026-02-06T23:15:38Z)

Found this error, ollama log.
Feb 06 18:10:34 U24 ollama[22382]: time=2026-02-06T18:10:34.891-05:00 level=INFO source=runner.go:464 msg="failure during GPU discovery" OLLAMA_LIBRARY_PATH="[/usr/local/lib/ollama /usr/local/lib/ollama/rocm]" extra_envs="map[GGML_CUDA_INIT:1 ROCR_VISIBLE_DEVICES:0]" error="runner crashed"

Should I set ollama service file as 11.0.3? Before I did re-install and GPU/VRAM has high usages, I did set to 11.0.2.

 [Service]
**Environment="HSA_OVERRIDE_GFX_VERSION=11.0.3"**

---

### 评论 #20 — darren-amd (2026-02-07T00:17:46Z)

Hi,

I was able to reproduce this error and it looks like the bundled ROCm libraries with Ollama don't yet have `gfx1103` rocBLAS support:
```
rocBLAS error: Cannot read /usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary.dat: Illegal seek for GPU arch : gfx1103
 List of available TensileLibrary Files :
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx942.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1101.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1201.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1100.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1200.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx90a.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx908.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1010.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1151.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1102.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1030.dat"
"/usr/local/lib/ollama/rocm/rocblas/library/TensileLibrary_lazy_gfx1012.dat"
time=2026-02-06T18:51:06.257-05:00 level=INFO source=runner.go:464 msg="failure during GPU discovery" OLLAMA_LIBRARY_PATH="[/usr/local/lib/ollama /usr/local/lib/ollama/rocm]" extra_envs="map[GGML_CUDA_INIT:1 ROCR_VISIBLE_DEVICES:0]" error="runner crashed"
```

So on my end it was defaulting to the CPU errantly which I didn't catch. We have rocBLAS support within TheRock wheels which I'll give a try but I'm running into some unrelated system issues right now. Please give the HSA override (1102) a try and let me know if it works.

---

### 评论 #21 — reywang18 (2026-02-07T02:51:59Z)

A similar issue reported - https://github.com/ROCm/ROCm/issues/5890

[   17.338061] amdgpu 0000:c6:00.0: **amdgpu: [gfxhub] page fault (src_id:0 ring:153** vmid:8 pasid:32770)
[   17.338074] amdgpu 0000:c6:00.0: amdgpu:  Process ollama pid 3622 thread ollama pid 3626
[   17.338081] amdgpu 0000:c6:00.0: amdgpu:   in page starting at address 0x00007298d922e000 from client 10
[   17.338086] amdgpu 0000:c6:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932

---

### 评论 #22 — darren-amd (2026-02-09T19:49:28Z)

Hi @reywang18.

I was able to reproduce a similar issue with amdgpu-dkms installed. I did not encounter the issue on `6.14.0-37-generic` nor `6.14.0-1020-oem`. Could you please uninstall dkms with `sudo apt autoremove amdgpu-dkms` and see if the issue persists? If it does, could you also try installing the oem kernel with `sudo apt install linux-oem-24.04c` followed by a reboot? 

I then ran:
```
HSA_OVERRIDE_GFX_VERSION=11.0.2 OLLAMA_DEBUG=2 OLLAMA_LLM_LIBRARY=rocm ollama serve
ollama run granite3-dense:8b
```
And it is correctly using the GPU now. Please give that a try and let me know if you run into any issues, thanks!

---

### 评论 #23 — darren-amd (2026-02-23T19:41:59Z)

Hi @reywang18,

Just checking in if the above fixed the issue?

---

### 评论 #24 — reywang18 (2026-02-25T02:06:34Z)

Give me a couple days.
I will check it.

On Mon, Feb 23, 2026 at 2:42 PM darren-amd ***@***.***> wrote:

> *darren-amd* left a comment (ROCm/ROCm#5452)
> <https://github.com/ROCm/ROCm/issues/5452#issuecomment-3946918103>
>
> Hi @reywang18 <https://github.com/reywang18>,
>
> Just checking in if the above fixed the issue?
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5452#issuecomment-3946918103>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ABEDXIS33XSF2ETXZ4CGI4L4NNJZ3AVCNFSM6AAAAACH6Q5K3GVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSNBWHEYTQMJQGM>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #25 — darren-amd (2026-04-07T18:41:50Z)

Closing as this is fixed on my end, please feel free to reopen or create a new ticket if the issue persists.

---
