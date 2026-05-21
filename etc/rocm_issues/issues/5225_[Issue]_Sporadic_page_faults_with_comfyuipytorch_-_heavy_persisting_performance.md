# [Issue]: Sporadic page faults with comfyui/pytorch - heavy persisting performance drop afterwards

> **Issue #5225**
> **状态**: closed
> **创建时间**: 2025-08-23T11:39:46Z
> **更新时间**: 2026-01-14T19:21:20Z
> **关闭时间**: 2026-01-14T19:21:20Z
> **作者**: kaubonbon
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5225

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

With comfyui image generation generally works very good (5s/it on an sdxl model) and then on a sporadic base (sometimes after 2 image generations, sometimes after ~15) I get this:

 35%|███████████████▍                            | 7/20 [00:47<01:27,  6.77s/it]Memory access fault by GPU node-1 (Agent handle: 0xeea28e0) on address 0x7a6eedb80000. Reason: Page not present or supervisor privilege.
Failed to fetch queues snapshot.
GPU core dump failed
Aborted (core dumped)

In dmesg:
```
[  499.707618] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  499.707632] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3710 thread python3 pid 3710
[  499.707639] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007a6e20839000 from client 0x1b (UTCL2)
[  499.707646] amdgpu 0000:74:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  499.707651] amdgpu 0000:74:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  499.707656] amdgpu 0000:74:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  499.707661] amdgpu 0000:74:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  499.707665] amdgpu 0000:74:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  499.707669] amdgpu 0000:74:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  499.707673] amdgpu 0000:74:00.0: amdgpu: 	 RW: 0x0
[  499.707689] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  499.707696] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3710 thread python3 pid 3710
[  499.707701] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007a6efabbb000 from client 0x1b (UTCL2)
```

... a lot of those ...

```
[  499.707838] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  499.707843] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3710 thread python3 pid 3710
[  499.707848] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007a6e086a0000 from client 0x1b (UTCL2)
```


After that event, the performance drops heavily and the image generation usually is 3 or 4 times as slow as before.
Interestingly, this state persists until a system cold restart. Then it's back to "normal".

I couldn't find any differences in metrics or settings that are different before or after this event. Hence, I could need some advice on either the problem source, how to dig in into this issue further, or some workaround.
I also did another install with Ubuntu 25, built TheRock rocm version from scratch for my gpu model. **Complete same issue.**

It's a fresh ubuntu 24LTS installation. Drivers from default ubuntu repositories. Pytorch install from their website. Extensive system info below.

Please let me know, if you need more logs/info.



### Operating System

Ubuntu 24.04.3 LTS

### CPU

AMD Ryzen 7 6800H with Radeon Graphics

### GPU

AMD Radeon 680M

### ROCm Version

ROCm 5.7.0 ?

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
  Name:                    AMD Ryzen 7 6800H with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 6800H with Radeon Graphics
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
  Max Clock Freq. (MHz):   4787                               
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
      Size:                    32077704(0x1e97788) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32077704(0x1e97788) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32077704(0x1e97788) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon 680M                    
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 5761(0x1681)                       
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   29696                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
  Packet Processor uCode:: 116                                
  SDMA engine uCode::      47                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16038852(0xf4bbc4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    16038852(0xf4bbc4) KB              
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


--------------------------------------- *** ---------------------------------------
SYSTEM INFO:
```
OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU: 
model name	: AMD Ryzen 7 6800H with Radeon Graphics
GPU:
  Name:                    AMD Ryzen 7 6800H with Radeon Graphics
  Marketing Name:          AMD Ryzen 7 6800H with Radeon Graphics
  Name:                    gfx1030                            
  Marketing Name:          AMD Radeon 680M                    
      Name:                    amdgcn-amd-amdhsa--gfx1030 
```

--------------------------------------- *** ---------------------------------------
environment:

```
HSA_OVERRIDE_GFX_VERSION=10.3.0
USE_CUDA=0
```



--------------------------------------- *** ---------------------------------------
rocminfo:
```

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
  Name:                    AMD Ryzen 7 6800H with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 6800H with Radeon Graphics
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
  Max Clock Freq. (MHz):   4787                               
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
      Size:                    32077704(0x1e97788) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32077704(0x1e97788) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32077704(0x1e97788) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon 680M                    
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 5761(0x1681)                       
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   29696                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
  Packet Processor uCode:: 116                                
  SDMA engine uCode::      47                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16038852(0xf4bbc4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    16038852(0xf4bbc4) KB              
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

```

--------------------------------------- *** ---------------------------------------

rocm-smi


```
========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU[0]		: get_power_avg, Not supported on the given system
Exception caught: map::at
ERROR: GPU[0]	: sclk clock is unsupported
====================================================================================
GPU[0]		: get_power_cap, Not supported on the given system
GPU  Temp (DieEdge)  AvgPwr  SCLK  MCLK     Fan  Perf  PwrCap       VRAM%  GPU%  
0    45.0c           N/A     None  2400Mhz  0%   auto  Unsupported   83%   0%    
====================================================================================
=============================== End of ROCm SMI Log ================================
```


--------------------------------------- *** ---------------------------------------

rocm-smi --showdriverversion

```
========================= ROCm System Management Interface =========================
=========================== Version of System Component ============================
Driver version: 6.14.0-28-generic
====================================================================================
=============================== End of ROCm SMI Log ================================

--------------------------------------- *** ---------------------------------------

```
pip list
```
Package                    Version
-------------------------- --------------
aiofiles                   24.1.0
aiohappyeyeballs           2.6.1
aiohttp                    3.12.15
aiohttp_socks              0.10.1
aiosignal                  1.4.0
alembic                    1.16.4
annotated-types            0.7.0
attrs                      25.3.0
av                         15.0.0
certifi                    2025.8.3
cffi                       1.17.1
chardet                    5.2.0
charset-normalizer         3.4.3
click                      8.2.1
comfyui-embedded-docs      0.2.6
comfyui_frontend_package   1.25.9
comfyui_workflow_templates 0.1.65
cryptography               45.0.6
einops                     0.8.1
filelock                   3.13.1
frozenlist                 1.7.0
fsspec                     2025.7.0
gitdb                      4.0.12
GitPython                  3.1.45
greenlet                   3.2.4
h11                        0.16.0
h2                         4.2.0
hf-xet                     1.1.8
hpack                      4.1.0
huggingface-hub            0.34.4
hyperframe                 6.1.0
idna                       3.10
Jinja2                     3.1.4
jsonschema                 4.25.1
jsonschema-specifications  2025.4.1
kornia                     0.8.1
kornia_rs                  0.1.9
Mako                       1.3.10
markdown-it-py             4.0.0
MarkupSafe                 2.1.5
matrix-nio                 0.25.2
mdurl                      0.1.2
mpmath                     1.3.0
multidict                  6.6.4
networkx                   3.3
numpy                      2.1.2
packaging                  25.0
piexif                     1.1.3
pillow                     11.0.0
pip                        24.0
propcache                  0.3.2
psutil                     7.0.0
pycparser                  2.22
pycryptodome               3.23.0
pydantic                   2.11.7
pydantic_core              2.33.2
pydantic-settings          2.10.1
PyGithub                   2.7.0
Pygments                   2.19.2
PyJWT                      2.10.1
PyNaCl                     1.5.0
python-dotenv              1.1.1
python-socks               2.7.2
pytorch-triton-rocm        3.4.0
PyYAML                     6.0.2
referencing                0.36.2
regex                      2025.7.34
requests                   2.32.5
rich                       14.1.0
rpds-py                    0.27.0
safetensors                0.6.2
scipy                      1.16.1
sentencepiece              0.2.1
setuptools                 70.2.0
shellingham                1.5.4
smmap                      5.0.2
soundfile                  0.13.1
spandrel                   0.4.1
SQLAlchemy                 2.0.43
sympy                      1.13.3
tokenizers                 0.21.4
toml                       0.10.2
torch                      2.8.0+rocm6.4
torchaudio                 2.8.0
torchsde                   0.2.6
torchvision                0.23.0+rocm6.4
tqdm                       4.67.1
trampoline                 0.1.2
transformers               4.55.4
typer                      0.16.1
typing_extensions          4.12.2
typing-inspection          0.4.1
unpaddedbase64             2.1.0
urllib3                    2.5.0
uv                         0.8.13
yarl                       1.20.1
```

--------------------------------------- *** ---------------------------------------
comfyui-startup:

```
python3 main.py --fp16-unet --cpu-vae --preview-method none --fp16-text-enc --disable-smart-memory --async-offload
[START] Security scan
Using Python 3.12.3 environment at: venv
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** ComfyUI startup time: 2025-08-23 12:45:48.511
** Platform: Linux
** Python version: 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0]
...
Using Python 3.12.3 environment at: venv
Using Python 3.12.3 environment at: venv

Prestartup times for custom nodes:
   0.5 seconds: /home/*/ComfyUI/custom_nodes/comfyui-manager

Checkpoint files will always be loaded safely.
Total VRAM 15663 MB, total RAM 31326 MB
pytorch version: 2.8.0+rocm6.4
AMD arch: gfx1030
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Disabling smart memory management
Device: cuda:0 AMD Radeon 680M : native
Using async weight offloading with 2 streams
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
torchaudio missing, ACE model will be broken
torchaudio missing, ACE model will be broken
Python version: 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0]
ComfyUI version: 0.3.51
ComfyUI frontend version: 1.25.9
```

--------------------------------------- *** ---------------------------------------

rocm-smi -a:
```
========================= ROCm System Management Interface =========================
=========================== Version of System Component ============================
Driver version: 6.14.0-28-generic
====================================================================================
======================================== ID ========================================
GPU[0]		: GPU ID: 0x1681
====================================================================================
==================================== Unique ID =====================================
GPU[0]		: Unique ID: N/A
====================================================================================
====================================== VBIOS =======================================
GPU[0]		: VBIOS version: 113-REMBRANDT-X37
====================================================================================
=================================== Temperature ====================================
GPU[0]		: Temperature (Sensor edge) (C): 44.0
====================================================================================
============================ Current clock frequencies =============================
Exception caught: map::at
GPU[0]		: fclk clock level: 1: (1800Mhz)
GPU[0]		: mclk clock level: 1: (2400Mhz)
GPU[0]		: sclk clock level: 1: (400Mhz)
GPU[0]		: socclk clock level: 0: (400Mhz)
====================================================================================
================================ Current Fan Metric ================================
GPU[0]		: Unable to detect fan speed for GPU 0
====================================================================================
============================== Show Performance Level ==============================
GPU[0]		: Performance Level: auto
====================================================================================
================================= OverDrive Level ==================================
GPU[0]		: get_overdrive_level_sclk, Not supported on the given system
====================================================================================
================================= OverDrive Level ==================================
GPU[0]		: get_mem_overdrive_level_mclk, Not supported on the given system
====================================================================================
==================================== Power Cap =====================================
GPU[0]		: get_power_cap, Not supported on the given system
GPU[0]		: Max Graphics Package Power Unsupported
====================================================================================
=============================== Show Power Profiles ================================
GPU[0]		: get_power_profiles, Not supported on the given system
====================================================================================
================================ Power Consumption =================================
, Not supported on the given system
GPU[0]		: get_power_avg, Not supported on the given system
GPU[0]		: get_power_avg, Not supported on the given system
GPU[0]		: Average Graphics Package Power (W): N/A
====================================================================================
=========================== Supported clock frequencies ============================
GPU[0]		: Supported fclk frequencies on GPU0
GPU[0]		: 0: 500Mhz
GPU[0]		: 1: 1800Mhz *
GPU[0]		: 
GPU[0]		: Supported mclk frequencies on GPU0
GPU[0]		: 0: 1000Mhz
GPU[0]		: 1: 2400Mhz *
GPU[0]		: 
GPU[0]		: Supported sclk frequencies on GPU0
GPU[0]		: 0: 200Mhz
GPU[0]		: 1: 533Mhz *
GPU[0]		: 2: 2200Mhz
GPU[0]		: 
GPU[0]		: Supported socclk frequencies on GPU0
GPU[0]		: 0: 400Mhz
GPU[0]		: 1: 600Mhz
GPU[0]		: 2: 720Mhz
GPU[0]		: 3: 800Mhz
GPU[0]		: 4: 900Mhz
GPU[0]		: 5: 1028Mhz
GPU[0]		: 6: 1028Mhz
GPU[0]		: 7: 1200Mhz *
GPU[0]		: 
------------------------------------------------------------------------------------
====================================================================================
================================ % time GPU is busy ================================
GPU[0]		: GPU use (%): 0
====================================================================================
================================ Current Memory Use ================================
GPU[0]		: % memory use, Not supported on the given system
GPU[0]		: Memory Activity: N/A
====================================================================================
================================== Memory Vendor ===================================
GPU[0]		: get_vram_vendor, Not supported on the given system
====================================================================================
=============================== PCIe Replay Counter ================================
GPU[0]		: PCIe Replay Count: 0
====================================================================================
================================== Serial Number ===================================
GPU[0]		: get_serial_number, Not supported on the given system
GPU[0]		: Serial Number: N/A
====================================================================================
================================== KFD Processes ===================================
No KFD PIDs currently running
====================================================================================
=============================== GPUs Indexed by PID ================================
No KFD PIDs currently running
====================================================================================
==================== GPU Memory clock frequencies and voltages =====================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
================================= Current voltage ==================================
GPU[0]		: Voltage (mV): 885
====================================================================================
==================================== PCI Bus ID ====================================
GPU[0]		: PCI Bus: 0000:74:00.0
====================================================================================
=============================== Firmware Information ===============================
GPU[0]		: ASD firmware version: 	0x210000c7
GPU[0]		: CE firmware version: 		37
GPU[0]		: get_firmware_version_DMCU, Not supported on the given system
GPU[0]		: get_firmware_version_MC, Not supported on the given system
GPU[0]		: ME firmware version: 		64
GPU[0]		: MEC firmware version: 	116
GPU[0]		: MEC2 firmware version: 	116
GPU[0]		: PFP firmware version: 	97
GPU[0]		: RLC firmware version: 	83
GPU[0]		: RLC SRLC firmware version: 	1
GPU[0]		: RLC SRLG firmware version: 	1
GPU[0]		: RLC SRLS firmware version: 	1
GPU[0]		: SDMA firmware version: 	47
GPU[0]		: get_firmware_version_SDMA2, Not supported on the given system
GPU[0]		: SMC firmware version: 	04.69.61.00
GPU[0]		: get_firmware_version_SOS, Not supported on the given system
GPU[0]		: get_firmware_version_TA RAS, Not supported on the given system
GPU[0]		: get_firmware_version_TA XGMI, Not supported on the given system
GPU[0]		: get_firmware_version_UVD, Not supported on the given system
GPU[0]		: get_firmware_version_VCE, Not supported on the given system
GPU[0]		: VCN firmware version: 	0x0311e004
====================================================================================
=================================== Product Info ===================================
GPU[0]		: Card series: 		Rembrandt [Radeon 680M]
GPU[0]		: Card model: 		0x1001
GPU[0]		: Card vendor: 		Advanced Micro Devices, Inc. [AMD/ATI]
GPU[0]		: Card SKU: 		REMBRANDT
====================================================================================
==================================== Pages Info ====================================
GPU[0]		: ras, Not supported on the given system
============================== Show Valid sclk Range ===============================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
============================== Show Valid mclk Range ===============================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
============================= Show Valid voltage Range =============================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
=============================== Voltage Curve Points ===============================
GPU[0]		: get_od_volt_info, Requested function is not implemented on this setup
====================================================================================
================================= Consumed Energy ==================================
GPU[0]		: % Energy Counter, Not supported on the given system
====================================================================================
============================ Current Compute Partition =============================
GPU[0]		: Not supported on the given system
====================================================================================
================================= Current NPS Mode =================================
GPU[0]		: Not supported on the given system
====================================================================================
=============================== End of ROCm SMI Log ================================

```
```
dpkg -l | grep rocm
ii  librocm-smi64-1                               5.7.0-1                                  amd64        ROCm System Management Interface (ROCm SMI) library
ii  rocm-device-libs-17                           6.0+git20231212.5a852ed-2                amd64        AMD specific device-side language runtime libraries
ii  rocm-smi                                      5.7.0-1                                  amd64        ROCm System Management Interface (ROCm SMI) command-line interface
ii  rocminfo                                      5.7.1-3build1                            amd64        ROCm Application for Reporting System Info
```

---

## 评论 (36 条)

### 评论 #1 — kaubonbon (2025-08-23T15:35:12Z)

The bad state seems to persist even after a reboot of the system. Only a hard reset will clear the bad state.
Error happens at the sampling stage of the processing always.

---

### 评论 #2 — kaubonbon (2025-08-23T22:07:31Z)

Sorry for spamming, this is the kernel log containing the GPU reset:

`Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3416 thread python3 pid 3416
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007bf2f3408000 from client 0x1b (UTCL2)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841051
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          MORE_FAULTS: 0x1
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          WALKER_ERROR: 0x0
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          MAPPING_ERROR: 0x0
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          RW: 0x1
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3416 thread python3 pid 3416
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007bf2f3410000 from client 0x1b (UTCL2)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3416 thread python3 pid 3416
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007bf2f3418000 from client 0x1b (UTCL2)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3416 thread python3 pid 3416
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007bf2f3440000 from client 0x1b (UTCL2)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3416 thread python3 pid 3416
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007bf2f3448000 from client 0x1b (UTCL2)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3416 thread python3 pid 3416
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007bf2f3450000 from client 0x1b (UTCL2)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 3416 thread python3 pid 3416
Aug 23 23:38:11 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x00007bf2f3458000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b09429c000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          MORE_FAULTS: 0x1
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          WALKER_ERROR: 0x0
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          MAPPING_ERROR: 0x0
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          RW: 0x0
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b094d50000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b092447000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b0921c7000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b0924f2000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b091750000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b093ebb000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b09092e000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b092c50000 from client 0x1b (UTCL2)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4856 thread python3 pid 4856
Aug 23 23:40:30 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000072b08fe31000 from client 0x1b (UTCL2)
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: Queue preemption failed for queue with doorbell_id: 80004008
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: Failed to evict process queues
Aug 23 23:47:33 jo-A6 kernel: amdgpu: Failed to quiesce KFD
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GPU reset begin!
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: Dumping IP State
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: Dumping IP State Completed
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: MODE2 reset
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GPU reset succeeded, trying to resume
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: PSP is resuming...
Aug 23 23:47:33 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: reserve 0xa00000 from 0xf41e000000 for PSP TMR
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: RAS: optional ras ta ucode is not available
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: RAP: optional rap ta ucode is not available
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: SMU is resuming...
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: SMU is resumed successfully!
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
Aug 23 23:47:34 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GPU reset(1) succeeded!
Aug 23 23:47:34 jo-A6 kernel: workqueue: kfd_process_wq_release [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
`

---

### 评论 #3 — kaubonbon (2025-08-24T10:28:08Z)

I compared all the sys-fs values before and after the crash and I could not find a difference.
The performance mode on the gpu is always 'auto' and changing it will do no difference.
I did google searches for "performance drop after gpureset" but so far I came up with nothing.
I don't understand that this behaviour should be so exotic, since my whole setup is really vanilla, I think.

---

### 评论 #4 — kaubonbon (2025-08-24T10:32:08Z)

These values from #5195 unfortunately don't  help in my setup
export MIOPEN_DEBUG_CONV_GEMM=0
export MIOPEN_DEBUG_CONV_WINOGRAD=0

---

### 评论 #5 — kaubonbon (2025-08-24T12:48:17Z)

Euler Ancestral seems to trigger more crashes than DP2m++ /Karras.

---

### 评论 #6 — kaubonbon (2025-08-24T12:52:29Z)

With some loglevel at "export AMD_LOG_LEVEL=2", I always get a lot of these on startup of comfyUI:

`:1:hip_fatbin.cpp           :761 : 5643807211 us:  Cannot find CO in the bundle /home/jo/ComfyUI/venv/lib/python3.12/site-packages/torch/lib/libMIOpen.so for ISA: amdgcn-amd-amdhsa--gfx1030
...
:1:hip_fatbin.cpp           :115 : 5644900815 us:  Missing CO for these ISAs - 
:1:hip_fatbin.cpp           :118 : 5644900817 us:       spirv64-amd-amdhsa--amdgcnspirv
:1:hip_fatbin.cpp           :118 : 5644900819 us:       amdgcn-amd-amdhsa--gfx1030
`

And then on generation, a lot of these, for various hip modules and functions:
`:1:hip_module.cpp           :86  : 5712191458 us:  Cannot find the function: Cijk_Ailk_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS3_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA4_GLVWB4_GRCGA1_GRCGB1_GRPM1_GRVW4_GSU1_GSUASB_GLS0_ISA1030_IU1_K1_KLA_LBSPPA0_LBSPPB0_LPA0_LPB0_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV0_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR1_PLR1_PKA0_SIA1_SLW1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO0_SVW4_SNLL0_TSGRA0_TSGRB0_TT8_8_TLDS0_UMLDSA0_UMLDSB0_U64SL1_USFGROn1_VAW1_VSn1_VW4_VWB4_VFLRP0_WSGRA0_WSGRB0_WS32_WG8_8_1_WGM1 for module: 0x7f0f5350
`

However, this is always the case, whether the performance is high or low.

---

### 评论 #7 — kaubonbon (2025-08-24T15:19:32Z)

Same with kernel 6.8 instead of 6.12
Same with rocm-packages from your repo https://repo.radeon.com/rocm/apt/6.4.3  instead of default ubuntu repos.
It's getting really tiring... I really wanted to get this to work with this amd card. well...

---

### 评论 #8 — ppanchad-amd (2025-08-25T14:00:01Z)

Hi @kaubonbon. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #9 — tcgu-amd (2025-08-25T18:16:42Z)

Hi @kaubonbon, thanks you for reaching out to us! And I'm sorry that you are experience this issue with AMD devices. It does look like your device has an iGPU along a dGPU. There have been known issues when both are enabled. I would try disabling iGPU in the BIOS and give it a try again. 

---

### 评论 #10 — kaubonbon (2025-08-25T18:22:07Z)

@tcgu-amd : no it's just a AMD Ryzen 7 6800H with an iGPU. you may have misinterpreted the logs.

---

### 评论 #11 — tcgu-amd (2025-08-25T18:33:11Z)

> [@tcgu-amd](https://github.com/tcgu-amd) : no it's just a AMD Ryzen 7 6800H with an iGPU. you may have misinterpreted the logs.

Ah I see, I indeed misread. Let me try digging deeper. 

---

### 评论 #12 — tcgu-amd (2025-08-25T18:39:39Z)

@kaubonbon, is your IOMMU enabled?

---

### 评论 #13 — kaubonbon (2025-08-25T18:52:10Z)

I have no IOMMU options in my bios, but is the following output enough to make a conclusion regarding this?


```
dmesg | grep -i iommu

[    0.407353] iommu: Default domain type: Translated
[    0.407353] iommu: DMA domain TLB invalidation policy: lazy mode
[    0.453155] pci 0000:00:00.2: AMD-Vi: IOMMU performance counters supported
[    0.453205] pci 0000:00:01.0: Adding to iommu group 0
[    0.453231] pci 0000:00:02.0: Adding to iommu group 1
[    0.453247] pci 0000:00:02.1: Adding to iommu group 2
[    0.453263] pci 0000:00:02.3: Adding to iommu group 3
[    0.453279] pci 0000:00:02.4: Adding to iommu group 4
[    0.453307] pci 0000:00:03.0: Adding to iommu group 5
[    0.453321] pci 0000:00:03.1: Adding to iommu group 5
[    0.453341] pci 0000:00:04.0: Adding to iommu group 6
[    0.453371] pci 0000:00:08.0: Adding to iommu group 7
[    0.453387] pci 0000:00:08.1: Adding to iommu group 8
[    0.453403] pci 0000:00:08.3: Adding to iommu group 9
[    0.453431] pci 0000:00:14.0: Adding to iommu group 10
[    0.453446] pci 0000:00:14.3: Adding to iommu group 10
[    0.453516] pci 0000:00:18.0: Adding to iommu group 11
[    0.453531] pci 0000:00:18.1: Adding to iommu group 11
[    0.453547] pci 0000:00:18.2: Adding to iommu group 11
[    0.453562] pci 0000:00:18.3: Adding to iommu group 11
[    0.453576] pci 0000:00:18.4: Adding to iommu group 11
[    0.453591] pci 0000:00:18.5: Adding to iommu group 11
[    0.453606] pci 0000:00:18.6: Adding to iommu group 11
[    0.453621] pci 0000:00:18.7: Adding to iommu group 11
[    0.453642] pci 0000:01:00.0: Adding to iommu group 12
[    0.453657] pci 0000:02:00.0: Adding to iommu group 13
[    0.453673] pci 0000:03:00.0: Adding to iommu group 14
[    0.453699] pci 0000:74:00.0: Adding to iommu group 15
[    0.453715] pci 0000:74:00.1: Adding to iommu group 16
[    0.453731] pci 0000:74:00.2: Adding to iommu group 17
[    0.453748] pci 0000:74:00.3: Adding to iommu group 18
[    0.453764] pci 0000:74:00.4: Adding to iommu group 19
[    0.453780] pci 0000:74:00.6: Adding to iommu group 20
[    0.453797] pci 0000:74:00.7: Adding to iommu group 21
[    0.453813] pci 0000:75:00.0: Adding to iommu group 22
[    0.453829] pci 0000:75:00.3: Adding to iommu group 23
[    0.453845] pci 0000:75:00.4: Adding to iommu group 24
[    0.453861] pci 0000:75:00.5: Adding to iommu group 25
[    0.456484] perf/amd_iommu: Detected AMD IOMMU #0 (2 banks, 4 counters/bank).
```

---

### 评论 #14 — kaubonbon (2025-08-25T19:15:41Z)

Also the 'svm' cpu flag is there. So I guess, it is enabled?

---

### 评论 #15 — tcgu-amd (2025-08-25T20:11:34Z)

@kaubonbon, yes, looks like it is enabled. I am wondering if turning it off will change the behavior. Do you know the version of BIOS you are running? Thanks!

---

### 评论 #16 — kaubonbon (2025-08-25T20:40:11Z)

It is a AMI Bios Version 2.22.1289

I'll try with kernel parameters iommu=off and iommu=pt, and give feedback.

---

### 评论 #17 — kaubonbon (2025-08-26T20:45:00Z)

Both modes won't change the overall demeanor. Using iommu=off, I still get some hangs:

```
journalctl -b | grep -i iommu
Aug 26 22:21:59 jo-A6 kernel: Command line: BOOT_IMAGE=/boot/vmlinuz-6.14.0-28-generic root=UUID=319da759-eb4c-4fe5-82c9-a62167c7f62a ro quiet splash iommu=off vt.handoff=7
Aug 26 22:21:59 jo-A6 kernel: Kernel command line: BOOT_IMAGE=/boot/vmlinuz-6.14.0-28-generic root=UUID=319da759-eb4c-4fe5-82c9-a62167c7f62a ro quiet splash iommu=off vt.handoff=7
Aug 26 22:21:59 jo-A6 kernel: iommu: Default domain type: Translated
Aug 26 22:21:59 jo-A6 kernel: iommu: DMA domain TLB invalidation policy: lazy mode
```

```
[  275.757285] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  275.757299] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4726 thread python3 pid 4726
[  275.757304] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x0000717e0fb08000 from client 0x1b (UTCL2)
[  275.757309] amdgpu 0000:74:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  275.757312] amdgpu 0000:74:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  275.757316] amdgpu 0000:74:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  275.757319] amdgpu 0000:74:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  275.757321] amdgpu 0000:74:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  275.757324] amdgpu 0000:74:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  275.757327] amdgpu 0000:74:00.0: amdgpu: 	 RW: 0x0
[  275.757359] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  275.757363] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4726 thread python3 pid 4726
[  275.757366] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x0000717e13d58000 from client 0x1b (UTCL2)
[  275.757371] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  275.757375] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4726 thread python3 pid 4726
[  275.757378] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x0000717e01086000 from client 0x1b (UTCL2)
[  275.757383] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  275.757386] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4726 thread python3 pid 4726
[  275.757390] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x0000717e01011000 from client 0x1b (UTCL2)
[  275.757394] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  275.757397] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4726 thread python3 pid 4726
[  275.757401] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x0000717e0bd07000 from client 0x1b (UTCL2)
[  275.757406] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[  275.757410] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4726 thread python3 pid 4726
[  275.757413] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x0000717e0130f000 from client 0x1b (UTCL2)
[  276.961679] amdgpu: Freeing queue vital buffer 0x717baba00000, queue evicted
[  276.961686] amdgpu: Freeing queue vital buffer 0x717bb0e00000, queue evicted
```

In this state, for example, the system operates normally, but the comfy process is hanging at:

```
loaded completely 11467.69392578125 4897.0483474731445 True
  5%|██▍                                             | 1/20 [00:05<01:39,  5.25s/it]
```

Then if I kill the python process the screen goes black for one second and I am back at my WM with all my windows still open. In dmesg I get this:

```
[  635.700115] amdgpu 0000:74:00.0: amdgpu: Queue preemption failed for queue with doorbell_id: 80004008
[  635.700124] amdgpu 0000:74:00.0: amdgpu: Failed to evict process queues
[  635.700126] amdgpu: Failed to quiesce KFD
[  635.700149] amdgpu 0000:74:00.0: amdgpu: GPU reset begin!
[  635.700206] amdgpu 0000:74:00.0: amdgpu: Dumping IP State
[  635.702853] amdgpu 0000:74:00.0: amdgpu: Dumping IP State Completed
[  635.733416] amdgpu: Freeing queue vital buffer 0x757762a00000, queue evicted
[  635.733422] amdgpu: Freeing queue vital buffer 0x7577b0400000, queue evicted
[  635.786702] amdgpu 0000:74:00.0: amdgpu: MODE2 reset
[  635.795696] amdgpu 0000:74:00.0: amdgpu: GPU reset succeeded, trying to resume
[  635.795811] [drm] PCIE GART of 1024M enabled (table at 0x000000F41FC00000).
[  635.795880] amdgpu 0000:74:00.0: amdgpu: PSP is resuming...
[  635.817960] amdgpu 0000:74:00.0: amdgpu: reserve 0xa00000 from 0xf41e000000 for PSP TMR
[  636.115058] amdgpu 0000:74:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  636.124952] amdgpu 0000:74:00.0: amdgpu: RAP: optional rap ta ucode is not available
[  636.124956] amdgpu 0000:74:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  636.124961] amdgpu 0000:74:00.0: amdgpu: SMU is resuming...
[  636.125812] amdgpu 0000:74:00.0: amdgpu: SMU is resumed successfully!
[  636.126146] [drm] kiq ring mec 2 pipe 1 q 0
[  636.131660] [drm] DMUB hardware initialized: version=0x04000045
[  636.286647] amdgpu 0000:74:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  636.286653] amdgpu 0000:74:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
[  636.286655] amdgpu 0000:74:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
[  636.286657] amdgpu 0000:74:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
[  636.286659] amdgpu 0000:74:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  636.286660] amdgpu 0000:74:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  636.286662] amdgpu 0000:74:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  636.286664] amdgpu 0000:74:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  636.286666] amdgpu 0000:74:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  636.286668] amdgpu 0000:74:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  636.286670] amdgpu 0000:74:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
[  636.286672] amdgpu 0000:74:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
[  636.286674] amdgpu 0000:74:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  636.286676] amdgpu 0000:74:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  636.286677] amdgpu 0000:74:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  636.286679] amdgpu 0000:74:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  636.294464] amdgpu 0000:74:00.0: amdgpu: GPU reset(1) succeeded!
```


Then after the reset - the usual. System is much slower.

`40%|███████████████████▏                            | 8/20 [02:03<03:05, 15.43s/it]
`

And while the system draws around 40-50W power and has 80°C in it's 'normal' state - after the gpu reset those values usually run around that:

```
========================================= ROCm System Management Interface =========================================
=================================================== Concise Info ===================================================
Device  Node  IDs              Temp    Power     Partitions          SCLK  MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Socket)  (Mem, Compute, ID)                                                 
====================================================================================================================
0       1     0x1681,   61049  60.0°C  33.041W   N/A, N/A, 0         N/A   2400Mhz  0%   auto  N/A     85%    100%  
====================================================================================================================
=============================================== End of ROCm SMI Log ================================================

```

So for these two issues, where one is apparently a faulty driver and the other is a ... general system malfunction, I can't understand for the latter, why such a massive and persisting performance change isn't visible somewhere.

Are there some environment variables that I can change to see more of what is happening?

---

### 评论 #18 — tcgu-amd (2025-08-26T21:07:18Z)

Thanks for the update. It seems like despite disabling iommu, the logs still show `iommu: Default domain type: Translated`. But yeah, regardless, I agree the error shouldn't leave the system at a degraded state. To get more logs, I think you can try setting "HSAKMT_DEBUG_LEVEL=7". This won't directly give you driver logs but will show lower level ROCR runtime logs which interfaces with the driver. Hopefully it will show us something that might have gone wrong. 

---

### 评论 #19 — tcgu-amd (2025-08-26T21:16:27Z)

You can also try enabling amdgpu kernel debug output by adding amdgpu.debug_mask=1 to your kernel parameters. This should show more details in dmesg. 

---

### 评论 #20 — kaubonbon (2025-08-26T21:22:33Z)

> It seems like despite disabling iommu, the logs still show iommu: Default domain type: Translated.

That's true, but the following output regarding iommu in dmesg still differs from the one mentioned in former posts, where it was:
```
...
[    0.453845] pci 0000:75:00.4: Adding to iommu group 24
[    0.453861] pci 0000:75:00.5: Adding to iommu group 25
[    0.456484] perf/amd_iommu: Detected AMD IOMMU #0 (2 banks, 4 counters/bank).
```
But I'm by no means fit to understand, if that means that iommu is really off.

I will try your two suggesions.

---

### 评论 #21 — kaubonbon (2025-08-27T18:48:26Z)

So with these two settings you suggested it looks like this - in ComfyUI:


```
...
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a90200000 size 20971520 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a90200000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a8d800000 size 41943040 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a8d800000 number of nodes 1
[hsaKmtUnmapMemoryToGPU] address 0x796a99000000
[hsaKmtFreeMemory] address 0x796a99000000
[hsaKmtUnmapMemoryToGPU] address 0x796a78a00000
[hsaKmtFreeMemory] address 0x796a78a00000
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a9a200000 size 2097152 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a9a200000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796ed1280000 size 135168 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796ed1280000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x796ed1240000 flags 0x40 size 0x21000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x796ed1240000 size 135168 from host
[hsaKmtMapMemoryToGPUNodes] address 0x796ed1240000 number of nodes 1
  5%|██▉                                                        | 1/20 [00:05<01:35,  5.05s/it][hsaKmtAvailableMemory] node 1
[hsaKmtQueryPointerInfo] pointer 0x796a888fcbc0
[hsaKmtQueryPointerInfo] pointer 0x796a888fcbc0
[hsaKmtQueryPointerInfo] pointer 0x796a888fcbc0
[hsaKmtQueryPointerInfo] pointer 0x796a888fcbc0
[hsaKmtQueryPointerInfo] pointer 0x796a888fcbc0
[hsaKmtRegisterMemoryWithFlags] address 0x796a888fc000 size 3788800
Registering to SVM 0x796a888fc000 size: 3788800
[hsaKmtMapMemoryToGPUNodes] address 0x796a888fc000 number of nodes 1
_fmm_map_to_gpu_userptr Mapping Address 0x796a888fc000 size aligned: 3788800 offset: 0
[hsaKmtUnmapMemoryToGPU] address 0x796a888fc000
[hsaKmtDeregisterMemory] address 0x796a888fc000
[hsaKmtQueryPointerInfo] pointer 0x796a88779a40
[hsaKmtQueryPointerInfo] pointer 0x796a88779a40
[hsaKmtQueryPointerInfo] pointer 0x796a88779a40
[hsaKmtQueryPointerInfo] pointer 0x796a88779a40
[hsaKmtQueryPointerInfo] pointer 0x796a88779a40
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a8c200000 size 20971520 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a8c200000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a86a00000 size 20971520 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a86a00000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a99600000 size 10485760 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a99600000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a85e00000 size 10485760 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a85e00000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a85200000 size 10485760 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a85200000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x796a84600000 size 10485760 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a84600000 number of nodes 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAllocMemoryAlign] node 1
Memory exception on virtual address 0x8ec04000, node id 1 : Page not present
op get range attrs failed Bad address
Address does not belong to a known buffer
Memory access fault by GPU node-1 (Agent handle: 0x459b42f0) on address 0x8ec04000. Reason: Page not present or supervisor privilege.
[hsaKmtAllocMemoryAlign] node 1 address 0x796a5c400000 size 671088640 from device
[hsaKmtMapMemoryToGPUNodes] address 0x796a5c400000 number of nodes 1
Failed to fetch queues snapshot.
GPU core dump failed
Aborted (core dumped)
```

And in kernel logs:

```
[  449.246835] amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32771)
[  449.246878] amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4864 thread python3 pid 4864
[  449.246885] amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000000008ec04000 from client 0x1b (UTCL2)
[  449.246890] amdgpu 0000:74:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841050
[  449.246893] amdgpu 0000:74:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  449.246897] amdgpu 0000:74:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  449.246900] amdgpu 0000:74:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  449.246903] amdgpu 0000:74:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
[  449.246906] amdgpu 0000:74:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  449.246909] amdgpu 0000:74:00.0: amdgpu: 	 RW: 0x1
[  450.397648] amdgpu: Freeing queue vital buffer 0x796a9fa00000, queue evicted
[  450.397695] amdgpu: Freeing queue vital buffer 0x796cec600000, queue evicted
```



---

### 评论 #22 — kaubonbon (2025-08-27T18:55:15Z)

Most of the times, it fails directly after the _fmm_map function:

```
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
 15%|█████████████                                                                          | 3/20 [00:13<01:17,  4.56s/it][hsaKmtAvailableMemory] node 1
[hsaKmtQueryPointerInfo] pointer 0x743360a641c0
[hsaKmtQueryPointerInfo] pointer 0x743360a641c0
[hsaKmtQueryPointerInfo] pointer 0x743360a641c0
[hsaKmtQueryPointerInfo] pointer 0x743360a641c0
[hsaKmtQueryPointerInfo] pointer 0x743360a641c0
[hsaKmtRegisterMemoryWithFlags] address 0x743360a64000 size 3788800
Registering to SVM 0x743360a64000 size: 3788800
[hsaKmtMapMemoryToGPUNodes] address 0x743360a64000 number of nodes 1
_fmm_map_to_gpu_userptr Mapping Address 0x743360a64000 size aligned: 3788800 offset: 0
Memory exception on virtual address 0x7433805bc000, node id 1 : Page not present
op get range attrs failed Bad address
Address does not belong to a known buffer
Memory access fault by GPU node-1 (Agent handle: 0x1a2792a0) on address 0x7433805bc000. Reason: Page not present or supervisor privilege.
Failed to fetch queues snapshot.
GPU core dump failed
Aborted (core dumped)

```

---

### 评论 #23 — kaubonbon (2025-08-27T18:59:51Z)

Sometimes it also hangs there, for several minutes, with a lot of gpu usage:

```
[hsaKmtAllocMemoryAlign] node 0 address 0x768de6c80000 size 135168 from host
[hsaKmtMapMemoryToGPUNodes] address 0x768de6c80000 number of nodes 1
  5%|████▎                                                                                  | 1/20 [00:15<04:57, 15.67s/it][hsaKmtAvailableMemory] node 1
[hsaKmtQueryPointerInfo] pointer 0x3ddb15c0
[hsaKmtQueryPointerInfo] pointer 0x3ddb15c0
[hsaKmtQueryPointerInfo] pointer 0x3ddb15c0
[hsaKmtQueryPointerInfo] pointer 0x3ddb15c0
[hsaKmtQueryPointerInfo] pointer 0x3ddb15c0
[hsaKmtRegisterMemoryWithFlags] address 0x3ddb1000 size 3788800
Registering to SVM 0x3ddb1000 size: 3788800
[hsaKmtMapMemoryToGPUNodes] address 0x3ddb1000 number of nodes 1
_fmm_map_to_gpu_userptr Mapping Address 0x3ddb1000 size aligned: 3788800 offset: 0

```

before that:

```
HW Exception by GPU node-1 (Agent handle: 0x12e78350) reason :GPU Hang
Aborted (core dumped)
```


---

### 评论 #24 — tcgu-amd (2025-08-27T19:27:16Z)

Thanks @kaubonbon, that's really helpful! It definitely seems like there's some sort of memory-race going on. Can you try disabling sdma with HSA_ENABLE_SDMA=0? It might help reduce the chance of the race. I will try to take a look where the race could have happened. Thanks! 

---

### 评论 #25 — kaubonbon (2025-08-27T19:41:22Z)

I will try.
Interestingly the euler_a/normal sampler will almost always fail early with iommu=off.
The dpm++_2m/karras with iomm=off, will fail in later stages with a slightly different behaviour.
In ComfyUI:

```
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
 35%|███████████████████████▍                                           | 7/20 [00:32<00:59,  4.55s/it][hsaKmtAvailableMemory] node 1
[hsaKmtQueryPointerInfo] pointer 0x7631a7840280
[hsaKmtQueryPointerInfo] pointer 0x7631a7840280
[hsaKmtQueryPointerInfo] pointer 0x7631a7840280
[hsaKmtQueryPointerInfo] pointer 0x7631a7840280
[hsaKmtQueryPointerInfo] pointer 0x7631a7840280
[hsaKmtRegisterMemoryWithFlags] address 0x7631a7840000 size 3788800
Registering to SVM 0x7631a7840000 size: 3788800
[hsaKmtMapMemoryToGPUNodes] address 0x7631a7840000 number of nodes 1
_fmm_map_to_gpu_userptr Mapping Address 0x7631a7840000 size aligned: 3788800 offset: 0
[hsaKmtUnmapMemoryToGPU] address 0x7631a7840000
[hsaKmtDeregisterMemory] address 0x7631a7840000
[hsaKmtQueryPointerInfo] pointer 0x7631448aa7c0
[hsaKmtQueryPointerInfo] pointer 0x7631448aa7c0
[hsaKmtQueryPointerInfo] pointer 0x7631448aa7c0
[hsaKmtQueryPointerInfo] pointer 0x7631448aa7c0
[hsaKmtQueryPointerInfo] pointer 0x7631448aa7c0
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
[hsaKmtAvailableMemory] node 1
Memory exception on virtual address 0x76301bf72000, node id 1 : Page not present
GPU address 0x76301bf72000, is Unified memory
Preferred location for address 0x76301bf72000 is Node id -1
Prefetch location for address 0x76301bf72000 is Node id -1
Node id 1 has no access to address 0x76301bf72000
Fine grained coherency between devices
Memory access fault by GPU node-1 (Agent handle: 0xa2ca1a0) on address 0x76301bf72000. Reason: Page not present or supervisor privilege.
Failed to fetch queues snapshot.
GPU core dump failed
```

In kernel log:

```
Aug 27 21:33:33 jo-A6 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076301bf74000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          MORE_FAULTS: 0x1
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          WALKER_ERROR: 0x0
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          MAPPING_ERROR: 0x0
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:          RW: 0x0
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076301bf75000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076301bfd1000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076301bf50000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076301abd0000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076300bb6c000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076300bbd4000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076300bb60000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076300af6c000 from client 0x1b (UTCL2)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:  in process python3 pid 4655 thread python3 pid 4655
Aug 27 21:34:13 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu:   in page starting at address 0x000076301bf52000 from client 0x1b (UTCL2)
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: Queue preemption failed for queue with doorbell_id: 80004008
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GPU reset begin!
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: Dumping IP State
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: Dumping IP State Completed
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: MODE2 reset
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GPU reset succeeded, trying to resume
Aug 27 21:34:17 jo-A6 kernel: [drm] PCIE GART of 1024M enabled (table at 0x000000F41FC00000).
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: PSP is resuming...
Aug 27 21:34:17 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: reserve 0xa00000 from 0xf41e000000 for PSP TMR
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: RAS: optional ras ta ucode is not available
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: RAP: optional rap ta ucode is not available
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: SMU is resuming...
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: SMU is resumed successfully!
Aug 27 21:34:18 jo-A6 kernel: [drm] kiq ring mec 2 pipe 1 q 0
Aug 27 21:34:18 jo-A6 kernel: [drm] DMUB hardware initialized: version=0x04000045
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
Aug 27 21:34:18 jo-A6 kernel: amdgpu 0000:74:00.0: amdgpu: GPU reset(1) succeeded!

```

---

### 评论 #26 — kaubonbon (2025-08-27T19:42:27Z)

With iommu=pt I could at least sometimes get complete runs with dpm++_2m. Also never with euler_a.

---

### 评论 #27 — tcgu-amd (2025-08-27T20:17:09Z)

> With iommu=pt I could at least sometimes get complete runs with dpm++_2m. Also never with euler_a.

Yeah with memory races different code paths can lead to different behaviors that may not always be expected...


---

### 评论 #28 — kaubonbon (2025-08-27T20:41:35Z)

So with 'HSA_ENABLE_SDMA=0' things are worse than before, in that I can't get a complete rendering at all.
However how it fails is different. No more exceptions. It just hangs there, two Core's are at 100% and the gpu does something... but it will just hang.

<img width="1488" height="1176" alt="Image" src="https://github.com/user-attachments/assets/ad8428d0-5b28-419e-8845-6a29e4bd3298" />

If I kill the process then it takes forever to free the memory:

```
^C
Stopped server
[hsaKmtUnmapMemoryToGPU] address 0x7176d0100000
[hsaKmtFreeMemory] address 0x7176d0100000
[hsaKmtUnmapMemoryToGPU] address 0x71768a700000
[hsaKmtFreeMemory] address 0x71768a700000
[hsaKmtUnmapMemoryToGPU] address 0x717634400000
[hsaKmtFreeMemory] address 0x717634400000
[hsaKmtUnmapMemoryToGPU] address 0x71762d600000
[hsaKmtFreeMemory] address 0x71762d600000
[hsaKmtUnmapMemoryToGPU] address 0x717639600000
[hsaKmtFreeMemory] address 0x717639600000
[hsaKmtUnmapMemoryToGPU] address 0x717638600000
[hsaKmtFreeMemory] address 0x717638600000

```

---

### 评论 #29 — kaubonbon (2025-08-27T20:43:26Z)

Then when I issue a ctrl+c again it manages sometimes manages to free the memory:

```
Aug 27 22:42:01 jo-A6 kernel: amdgpu: Freeing queue vital buffer 0x717444800000, queue evicted
Aug 27 22:42:01 jo-A6 kernel: amdgpu: Freeing queue vital buffer 0x71763aa00000, queue evicted

```

But often it just dies and results in a GPU-Reset.

---

### 评论 #30 — kaubonbon (2025-08-27T21:36:29Z)

I think, I located the problem. In the bios there is an option for 'UMA Frame Buffer Size' which was on 16G.
I changed it to 2G and now all the problems seem to be gone.

Maybe some of the environment variables that are currently there in this system are essential for this to work. I will do more tests and report back.

Surprisingly, I had some wifi card issues (sporadic disconnects under high load) which are now also gone........................



Some spam again - current environment:
```

$ uname -r
6.8.0-78-generic


$ cat /etc/debian_version 
trixie/sid


$ env
SHELL=/bin/bash
XDG_SESSION_DESKTOP=ubuntu
XDG_SESSION_TYPE=wayland
USE_CUDA=0
XDG_CURRENT_DESKTOP=ubuntu:GNOME
HSAKMT_DEBUG_LEVEL=7
HIP_VISIBLE_DEVICES=0
HSA_ENABLE_SDMA=0
SHLVL=1
VIRTUAL_ENV_PROMPT=(venv) 
PATH=/home/jo/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin
HSA_OVERRIDE_GFX_VERSION=10.3.0


$ pip list
Package                    Version
-------------------------- --------------
aiohappyeyeballs           2.6.1
aiohttp                    3.12.15
aiosignal                  1.4.0
alembic                    1.16.4
annotated-types            0.7.0
argcomplete                3.1.4
attrs                      23.2.0
av                         15.0.0
Babel                      2.10.3
bcc                        0.29.1
blinker                    1.7.0
Brlapi                     0.8.5
certifi                    2023.11.17
cffi                       1.17.1
chardet                    5.2.0
click                      8.1.6
cloud-init                 25.1.4
colorama                   0.4.6
comfyui-embedded-docs      0.2.6
comfyui_frontend_package   1.25.10
comfyui_workflow_templates 0.1.65
command-not-found          0.3
configobj                  5.0.8
cryptography               41.0.7
cupshelpers                1.0
dbus-python                1.3.2
defer                      1.0.6
distro                     1.9.0
distro-info                1.7+build1
einops                     0.8.1
filelock                   3.13.1
frozenlist                 1.7.0
fsspec                     2024.6.1
greenlet                   3.2.4
hf-xet                     1.1.8
httplib2                   0.20.4
huggingface-hub            0.34.4
idna                       3.6
Jinja2                     3.1.2
jsonpatch                  1.32
jsonpointer                2.0
jsonschema                 4.10.3
kornia                     0.8.1
kornia_rs                  0.1.9
language-selector          0.1
launchpadlib               1.11.0
lazr.restfulclient         0.14.6
lazr.uri                   1.0.6
louis                      3.29.0
Mako                       1.3.10
markdown-it-py             3.0.0
MarkupSafe                 2.1.5
mdurl                      0.1.2
mpmath                     1.3.0
multidict                  6.6.4
netaddr                    0.8.0
netifaces                  0.11.0
networkx                   3.3
numpy                      2.1.2
oauthlib                   3.2.2
olefile                    0.46
packaging                  25.0
pexpect                    4.9.0
pillow                     10.2.0
pip                        24.0
propcache                  0.3.2
psutil                     7.0.0
ptyprocess                 0.7.0
pycairo                    1.25.1
pycparser                  2.22
pycups                     2.0.1
pydantic                   2.11.7
pydantic_core              2.33.2
pydantic-settings          2.10.1
Pygments                   2.17.2
PyGObject                  3.48.2
PyJWT                      2.7.0
pyparsing                  3.1.1
pyrsistent                 0.20.0
pyserial                   3.5
python-apt                 2.7.7+ubuntu5
python-dateutil            2.8.2
python-debian              0.1.49+ubuntu2
python-dotenv              1.1.1
pytorch-triton-rocm        3.4.0
pytz                       2024.1
pyxdg                      0.28
PyYAML                     6.0.1
regex                      2025.7.34
requests                   2.31.0
rich                       13.7.1
safetensors                0.6.2
scipy                      1.16.1
sentencepiece              0.2.1
setuptools                 70.2.0
six                        1.16.0
soundfile                  0.13.1
spandrel                   0.4.1
SQLAlchemy                 2.0.43
sympy                      1.13.3
systemd-python             235
tokenizers                 0.21.4
torch                      2.8.0+rocm6.4
torchaudio                 2.8.0
torchsde                   0.2.6
torchvision                0.23.0+rocm6.4
tqdm                       4.67.1
trampoline                 0.1.2
transformers               4.55.4
typing_extensions          4.15.0
typing-inspection          0.4.1
ubuntu-drivers-common      0.0.0
ubuntu-pro-client          8001
ufw                        0.36.2
unattended-upgrades        0.1
urllib3                    2.0.7
wadllib                    1.3.6
wheel                      0.42.0
xdg                        5
xkit                       0.0.0
yarl                       1.20.1


$ cat /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.debug_mask=1"



$ sudo apt list | grep -i amdgpu | grep -i installed
amdgpu-core/noble,noble,now 1:6.4.60402-2187269.24.04 all [installed,automatic]
amdgpu-install/now 6.4.60402-2198586.24.04 all [installed,local]
libdrm-amdgpu-amdgpu1/noble,now 1:2.4.124.60402-2187269.24.04 amd64 [installed,automatic]
libdrm-amdgpu-common/noble,noble,now 1.0.0.60403-2194681.24.04 all [installed,automatic]
libdrm-amdgpu1/noble-updates,now 2.4.122-1~ubuntu0.24.04.1 amd64 [installed,automatic]
libdrm2-amdgpu/noble,now 1:2.4.124.60402-2187269.24.04 amd64 [installed,automatic]
xserver-xorg-video-amdgpu/noble,now 23.0.0-1build1 amd64 [installed,automatic]

```

---

### 评论 #31 — tcgu-amd (2025-08-28T15:02:48Z)

@kaubonbon Nice! I am glad you found a solution. Decreasing the UMA Frame buffer size can indeed reduce mapping pressure and lower the chance of a mem race. I am definitely still interested in seeing how the env variables affect the things. 

---

### 评论 #32 — kaubonbon (2025-08-29T10:17:41Z)

Unfortunately, the good system state couldn't be contained.
I think I might have just had a sweet spot, off all configurations combined (environment flags, kernel parameters, driver version, pytorch version, sd model, lora's), where it worked 'better'.
What I definitely can say:
- with the rocm libraries from the adm repos (with the amd guide) the generation process was really unstable.
- the rocm libraries from the default ubuntu 24 repos are mandatory
- The iommu kernel parameters didn't do much in the end
- HSA_ENABLE_SDMA may be helpful, but I am unsure after all.

Overall the process is way too fiddly to be fun, so I will stop experimenting with it for now. Thank you @tcgu-amd for your help.

---

### 评论 #33 — virtualuk (2025-08-31T02:19:06Z)

I've also got the same issues with the same setup (slightly different hardware, running a AMD Strix Halo with a 8060S, 128GB memory with 96GB allocated to the iGPU in the BIOS). Happy to help in any way I can in debugging as it's infuriating to get so far with a ComfyUI task for it to get nuked. 

---

### 评论 #34 — tcgu-amd (2025-09-02T20:14:18Z)

> I've also got the same issues with the same setup (slightly different hardware, running a AMD Strix Halo with a 8060S, 128GB memory with 96GB allocated to the iGPU in the BIOS). Happy to help in any way I can in debugging as it's infuriating to get so far with a ComfyUI task for it to get nuked.

Huh interesting, Strix Halo is a bit different since it's an APU and has official support from, unlike 680M iGPU. Have you tried the suggestions above? 

---

### 评论 #35 — tcgu-amd (2025-09-18T20:33:56Z)

Hi @virtualuk did you find a solution to your issue or opened another issue somewhere else? Thanks! 

---

### 评论 #36 — virtualuk (2025-09-18T20:50:03Z)

I managed to get to a state where it's stable with the combination of Docker files attached to this thread.  I would say it's "mostly stable", stable enough that I've stopped tinkering with it.  I can't help with the contents, full disclosure, the files were vibed.

[comfyui_docker-compose.yml](https://github.com/user-attachments/files/22414698/comfyui_docker-compose.yml)
[comfyUI_Dockerfile.txt](https://github.com/user-attachments/files/22414697/comfyUI_Dockerfile.txt)

---
