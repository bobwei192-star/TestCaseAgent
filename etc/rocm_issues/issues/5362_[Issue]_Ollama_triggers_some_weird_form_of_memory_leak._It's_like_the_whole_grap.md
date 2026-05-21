# [Issue]: Ollama triggers some weird form of memory leak. It's like the whole graphic stack has the ability to unload VRAM disabled.

> **Issue #5362**
> **状态**: closed
> **创建时间**: 2025-09-17T08:37:31Z
> **更新时间**: 2025-12-28T09:18:20Z
> **关闭时间**: 2025-12-26T06:53:01Z
> **作者**: ghost
> **标签**: Under Investigation, ROCm 6.3.1
> **URL**: https://github.com/ROCm/ROCm/issues/5362

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.1** (颜色: #ededed)

## 负责人

- amd-nicknick

## 描述

### Problem Description

I load and unload the model.
I launch the model via an app "alpaca"(from flathub) and there's an option to unload after use.
And sometimes I pick the wrong model stop the generation mid-way and change the model, if you do it like 2-3 times it can make the graphic stack be incapable of freeing VRAM.
I use a non-managed by alpaca instance of ollama. Ollama: 0.11.11
Ollama reports no model being loaded, stopping ollama process doesn't help, rocm-smi isn't aware of any process using up memory etc.
For whatever reason, Firefox is capable of freeing VRAM once it runs out of VRAM to use. Don't ask me why I don't get it either. 
I closed firefox and memory usage was 5.5 GB, now it shoots up slowly again, but I launched a game stopped it, went on irc stopped that as well so after half an hour I'm at 14GB of VRAM.

I used qwen3-30B-MoE and GPT-OSS-20B probably of little relevance.
I doesn't feel like a kinda fixable issue from ollama POV, or for it to be anywhere in the API.

### Operating System

Fedora Linux 42 (Workstation Edition)

### CPU

AMD Ryzen 7 5700X3D 8-Core Processor

### GPU

AMD Radeon RX 7800 XT

### ROCm Version

ROCm 6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

1. Load, unload the model and stop generation midway on ollama via the web http interface.
2. Suddenly the whole graphic stack cannot free VRAM memory space and it's only firefox which manages to free up VRAM. For whatever reason, firefox is capable of freeing VRAM once it runs out of VRAM to use. Don't ask me why I don't get it either. Rebooting helps.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[37mROCk module is loaded[0m
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
  Name:                    AMD Ryzen 7 5700X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5700X3D 8-Core Processor
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
  Max Clock Freq. (MHz):   4151                               
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
      Size:                    32773604(0x1f415e4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32773604(0x1f415e4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32773604(0x1f415e4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32773604(0x1f415e4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1101                            
  Uuid:                    GPU-d28993d3a7a1642a               
  Marketing Name:          AMD Radeon RX 7800 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29822(0x747e)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2124                               
  BDFID:                   2304                               
  Internal Node ID:        1                                  
  Compute Unit:            60                                 
  SIMDs per CU:            2                                  
  Shader Engines:          3                                  
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
  Packet Processor uCode:: 552                                
  SDMA engine uCode::      27                                 
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
      Name:                    amdgcn-amd-amdhsa--gfx1101         
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

[dmesg.txt](https://github.com/user-attachments/files/22380266/dmesg.txt)

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2025-09-17T13:58:08Z)

Hi @esperanza-esperanza. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — rsolvang (2025-09-18T20:03:48Z)

I have experienced the exact same issue for a couple of weeks on a similar setup.

- Fedora Silverblue 42
- AMD Ryzen 7 5800X3D × 16
- AMD Radeon RX 7900 XTX

I have run Ollama and Open WebUI in podman containers and as quadlets, and both methods have suffered from the same problem; Ollama suddenly stops generating tokens, usually after 5-7 prompts. I have had the problem both with and without switching between models.

Some ~minutes later, the screen freezes. I can still access the shell via SSH, but I cannot _really_ stop or kill Ollama. A restart is the only solution.  Here is my compose.yaml-file:

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:rocm
    container_name: ollama
    devices:
      - /dev/kfd
      - /dev/dri
    volumes:
      - ./ollama:/root/.ollama:z
    environment:
      - OLLAMA_FLASH_ATTENTION=1
      - OLLAMA_KV_CACHE_TYPE=q8_0
      - OLLAMA_KEEP_ALIVE=15
      - OLLAMA_CONTEXT_LENGTH=16384
    security_opt:
      - label=disable
    ports:
      - 11434:11434
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - 3000:8080
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./open-webui:/app/backend/data:z
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: always

```

I keep the containers up-to-date with the latest version of Ollama. I have had FLASH_ATTENTION active since the start, but I am currently testing my setup right now when it is disabled.

EDIT: Computer crashed hard again, possibly faster than before with FLASH_ATTENTION disabled. Would make sense, as the VRAM use is greater. My guess is that this is an AMD specific issue somehow.

---

### 评论 #3 — seevee (2025-09-23T21:45:38Z)

I have also experienced this, similar situation as above. `rocm-smi` reports ever-increasing VRAM usage despite model unloading, container stoppage, etc.

~This behavior does not seem to occur when there is no active graphical user session (`loginctl kill-session 1` in my case). In this case, VRAM is freed as expected.~

Without a graphical session, behavior is improved, but these problems can still occur.

Ollama invocation:
```bash
docker run -d \
  --device /dev/kfd \
  --device /dev/dri \
  -v ~/docker/ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama:rocm
```

<details>
  <summary>inxi</summary>

```
CPU: 8-core AMD Ryzen 7 3800X (-MT MCP-) speed/min/max: 3855/577/4560 MHz
Kernel: 6.16.8-arch3-1 x86_64 Up: 31m Mem: 3.02/62.71 GiB (4.8%)
Storage: 2.96 TiB (36.9% used) Procs: 469 Shell: Zsh inxi: 3.3.39
```

</details>

<details>
  <summary>/opt/rocm/bin/rocminfo --support</summary>

```
[37mROCk module is loaded[0m
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
  Name:                    AMD Ryzen 7 3800X 8-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 3800X 8-Core Processor
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
  Max Clock Freq. (MHz):   4560
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
      Size:                    65757876(0x3eb62b4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65757876(0x3eb62b4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65757876(0x3eb62b4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65757876(0x3eb62b4) KB
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
  Uuid:                    GPU-961271c74aef45a0
  Marketing Name:          AMD Radeon RX 7900 XTX
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
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2431
  BDFID:                   12032
  Internal Node ID:        1
  Compute Unit:            96
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
  Packet Processor uCode:: 602
  SDMA engine uCode::      27
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB
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
*** Done ***
```

</details>


---

### 评论 #4 — rsolvang (2025-11-03T19:34:42Z)

Spun up the latest version of Ollama again, and this problem is persisting :/

---

### 评论 #5 — amd-nicknick (2025-11-21T07:30:12Z)

Hmm. I tried a couple of cases, different model combination, interrupting during generation, different memory utilization... I cannot seem to repro this issue? Is there a step-by-step method that I can follow to duplicate this?

Ollama doesn't free up VRAM unless the model is unloaded, is the model still present in `ollama ps`? What happens if the Ollama process is killed? Will the VRAM be released? Also to align, are you using `rocm-smi` or other ways to capture VRAM usage?

---

### 评论 #6 — rsolvang (2025-11-22T16:49:54Z)

For me, killing the Ollama process has not been possible, so maybe this is a kernel related problem? Something seems to crash _really_ hard.

I have been using vLLM lately without trouble, and haven't tested Ollama in a while.

---

### 评论 #7 — amd-nicknick (2025-12-26T06:53:01Z)

Hi @rsolvang, well received. If you encounter any further issues, feel free to open new issues so we could take a look.
If you encounter the crashes with Ollama again, please reopen this issue so we can further isolate the potential problem.

---

### 评论 #8 — rsolvang (2025-12-28T09:18:20Z)

@amd-nicknick I tried the latest version a week ago and it worked flawlessly, so whatever caused the crash has been fix 👍 

---
