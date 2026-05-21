# [Issue]: Stall / hang in comfyUI gfx1201 above 6.4.4 (7.1 / 7.0.2 / 7.0.0 / nightlies) on Ubuntu 25.04 (pytorch Docker images)

> **Issue #5581**
> **状态**: closed
> **创建时间**: 2025-10-28T03:55:14Z
> **更新时间**: 2025-11-25T00:19:25Z
> **关闭时间**: 2025-11-24T21:02:31Z
> **作者**: Phezzan
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5581

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

ComfyUI eventually stalls generating images (1-30 generations)

GPU% remains 100% forever, but power / heat drop over the course of dozens of minutes until it is clear the card is not doing work.
even after hours, no progress is observed and temps remain low (50-65C, GPU fans cycle on/off)

problem is **not observed** in ROCm 6.4.4 w/ torch 2.7.1

docker images tested: 

rocm7.1_ubuntu24.04_py3.12_pytorch_release_2.8.0
rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.8.0
rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.7.1
rocm7.0_ubuntu24.04_py3.12_pytorch_release_2.7.1
rocm7.0_ubuntu24.04_py3.12_pytorch_release_2.8.0
rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1



### Operating System

25.04 (Plucky Puffin)

### CPU

5700 X3D

### GPU

9070xt

### ROCm Version

everything since 7.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Download rocm/pytorch
Install comfyUI requirements (using existing modules as constraints to prevent breaking rocm-torch compatibility)

generate 10-50 SDXL illustrious images.



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.14.14 is loaded
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
      Size:                    49252724(0x2ef8974) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49252724(0x2ef8974) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49252724(0x2ef8974) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    49252724(0x2ef8974) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-939d3c9fc1d5f803               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2400                               
  BDFID:                   11520                              
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 1012                               
  SDMA engine uCode::      838                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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

### Additional Information

```
/home/USER/comfy
├── base
│   ├── custom_nodes
│   ├── disabled_custom_nodes
│   ├── input
│   ├── models -> /mnt/ai/models
│   ├── output
│   ├── temp
│   └── user
├── build
├── ComfyUI
│   ├── alembic_db
│   ├── api_server
│   ├── app
...
└── user
    ├── default
    └── huggingface

```

``` Dockerfile
ARG ROCM_MAJOR=6.4
ARG ROCM_MINOR=.4
FROM rocm/pytorch:rocm${ROCM_MAJOR}${ROCM_MINOR}_ubuntu24.04_py3.12_pytorch_release_2.7.1
#FROM rocm/pytorch:rocm7.0_ubuntu24.04_py3.12_pytorch_release_2.7.1
#FROM rocm/pytorch:rocm7.0_ubuntu24.04_py3.12_pytorch_release_2.8.0
#FROM rocm/pytorch:rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.8.0
#FROM rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1
 
# 7.0 and up use /opt/venv
#ENV UV_VENV=/opt/venv
# 6.4.4 uses conda
ENV UV_VENV=/opt/conda/envs/py_3.12
 
 
ENV ROCM_VERSION=${ROCM_MAJOR}${ROCM_MINOR}
ENV UV_INDEX="https://repo.radeon.com/rocm/manylinux/rocm-rel-${ROCM_VERSION}/ https://download.pytorch.org/whl/nightly/rocm${ROCM_MAJOR}"
 
ENV UV_CACHE_DIR=/.cache/uv
ENV UV_BREAK_SYSTEM_PACKAGES=true
ENV UV_SYSTEM_PYTHON=true
 
ENV CUSTOM_NODES=/comfy/base/custom_nodes
ENV COMFY_DIR=/comfy/ComfyUI
 
RUN apt-get install --yes libcairo2-dev &&\
mkdir -p /mnt
 
WORKDIR /build
 
RUN pip install uv

# host contains up-to-date comfyUI
# ~/comfy/ComfyUI
RUN --mount=type=bind,source=.,target=/comfy                            \
uv pip freeze | sed 's/==\([^+]\+\)$/>=\1/' > frozen                    &&\
grep -hvP "^\s*(#.*)?$|\btorch\b|\btorchvision\b|\bpytorch-triton-rocm\b" $COMFY_DIR/requirements.txt $CUSTOM_NODES/*/requirements.txt | sort | uniq > all_requirements.txt
 
# unsafe-best-match is required to resolve ? opencv ?
RUN --mount=type=cache,target=/.cache                                   \
uv pip install --index-strategy unsafe-best-match -r  all_requirements.txt -c frozen
 
WORKDIR /comfy
```

```
services:
  comfy_srv:
    container_name: "comfy_srv"
    image: "rocm644-torch271"
    restart: unless-stopped
    working_dir: /comfy
    volumes:
      - .:/comfy
      - /mnt/ai:/mnt/ai
    env_file: "comfy.env"
    environment:
      - HOST_DIR=$PWD
      - WORKING_DIR=/comfy
      - COMFY_DIR=/comfy/ComfyUI
      - COMFY_PORT=12345
    command: ["./run_comfy.sh"]
    ports:
      - 12345:12345
    group_add:
      - video
      - 105
    devices:
      - "/dev/dri"
      - "/dev/kfd"
    security_opt: 
      - seccomp=unconfined
    cap_add: 
      - SYS_PTRACE
    network_mode: host
    ipc: host
    shm_size: 12G
```

PS:
rocm644-torch280 (2025-10-26 build) eventually runs out of ... something and wreaks havoc on usability with this:
```
 2025-10-27T21:01:36.451881-04:00 tv kernel: [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
 2025-10-27T21:01:40.153879-04:00 tv kernel: amdgpu 0000:2d:00.0: amdgpu: 00000000caf88e41 pin failed
```

---

## 评论 (12 条)

### 评论 #1 — Hubert97 (2025-10-28T09:41:00Z)

check number of kworkers in D state. Maybe its the same issue as https://github.com/ROCm/ROCm/issues/5536

---

### 评论 #2 — Phezzan (2025-10-30T13:18:40Z)

dmesg during infinite hang 
rocm702-torch271
```
[13668.340285] workqueue: dm_irq_work_func [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
[13669.490279] workqueue: dm_irq_work_func [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
[13699.150122] workqueue: dm_irq_work_func [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
[17097.352734] workqueue: dm_irq_work_func [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
[25224.644795] workqueue: dm_irq_work_func [amdgpu] hogged CPU for >10000us 19 times, consider switching to WQ_UNBOUND
[33162.985209] workqueue: dm_irq_work_func [amdgpu] hogged CPU for >10000us 35 times, consider switching to WQ_UNBOUND

```

---

### 评论 #3 — Phezzan (2025-10-30T13:29:56Z)

$ amd-smi firmware
```
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_PFP
            FW_VERSION: 2840
        FW 1:
            FW_ID: CP_ME
            FW_VERSION: 2780
        FW 2:
            FW_ID: CP_MEC1
            FW_VERSION: 3060
        FW 3:
            FW_ID: RLC
            FW_VERSION: 12484000
        FW 4:
            FW_ID: SDMA0
            FW_VERSION: 7289670
        FW 5:
            FW_ID: SDMA1
            FW_VERSION: 7289670
        FW 6:
            FW_ID: VCN
            FW_VERSION: 09.10.70.13
        FW 7:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.3A.0B.14
        FW 8:
            FW_ID: ASD
            FW_VERSION: 553648366
        FW 9:
            FW_ID: TA_RAS
            FW_VERSION: 1B.3A.00.01
        FW 10:
            FW_ID: PM
            FW_VERSION: 00.104.74.00
```

amd-smi - comfy is running VAE decode (infinite) - rocm702-torch271 built from 
rocm/pytorch:rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.7.1
```
+------------------------------------------------------------------------------+
| AMD-SMI 26.0.2+39589fda      amdgpu version: 6.14.14  ROCm version: 7.0.2    |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:2d:00.0  AMD Radeon RX 9070 XT | 6 %      62 °C   0           189/266 W |
|   0       0     N/A             N/A | 100 %   29.8 %          11541/16304 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|    0      36750  python3.12             2.0 MB    9.3 GB     9.5 GB  N/A     |
+------------------------------------------------------------------------------+
```

Yes, I reduce power max with amd-smi:
sudo amd-smi set -g 0 -o 266


---

### 评论 #4 — Phezzan (2025-10-30T13:54:00Z)

> check number of kworkers in D state. Maybe its the same issue as [#5536](https://github.com/ROCm/ROCm/issues/5536)

I see one come and go every few seconds (rocm702 - torch 271, Linux 6.14.0-35-generic #35-Ubuntu SMP PREEMPT_DYNAMIC)

---

### 评论 #5 — Phezzan (2025-10-30T20:04:53Z)

rocm 702 torch 271 after running VAE decode for... a very very long time
```
...
comfy_srv  | model weight dtype torch.float16, manual cast: None
comfy_srv  | model_type EPS
comfy_srv  | FETCH ComfyRegistry Data [DONE]
comfy_srv  | [ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
comfy_srv  | FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json [DONE]
comfy_srv  | [ComfyUI-Manager] All startup tasks have been completed.
comfy_srv  | Using split attention in VAE
comfy_srv  | Using split attention in VAE
comfy_srv  | VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
comfy_srv  | Requested to load SDXLClipModel
comfy_srv  | loaded completely 9.5367431640625e+25 1560.802734375 True
comfy_srv  | CLIP/text encoder model load device: cpu, offload device: cpu, current: cpu, dtype: torch.float16
comfy_srv  | Requested to load SDXL
comfy_srv  | loaded completely 13441.59951171875 4897.0483474731445 True
100%|██████████| 20/20 [08:37<00:00, 25.89s/it]  
comfy_srv  | Requested to load AutoencoderKL
comfy_srv  | loaded completely 5376.335546875001 159.55708122253418 True
comfy_srv  | Memory access fault by GPU node-1 (Agent handle: 0x284d0a60) on address 0x754e67e57000. Reason: Page not present or supervisor privilege.
comfy_srv exited with code 0
```

```
[58751.149919] kauditd_printk_skb: 2266 callbacks suppressed
[58751.149921] audit: type=1400 audit(1761854208.614:3076): apparmor="DENIED" operation="open" class="file" profile="ubuntu_pro_apt_news" name="/opt/rocm-7.0.2/lib/" pid=69458 comm="python3" requested_mask="r" denied_mask="r" fsuid=0 ouid=0
[58751.150318] audit: type=1400 audit(1761854208.614:3077): apparmor="DENIED" operation="open" class="file" profile="ubuntu_pro_esm_cache" name="/opt/rocm-7.0.2/lib/" pid=69459 comm="python3" requested_mask="r" denied_mask="r" fsuid=0 ouid=0
[58751.227583] audit: type=1400 audit(1761854208.691:3078): apparmor="DENIED" operation="capable" class="cap" profile="ubuntu_pro_esm_cache" pid=69459 comm="python3" capability=24  capname="sys_resource"
[58755.052813] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
[58755.077813] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
[58755.151814] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
[58755.291179] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32796)
[58755.291189] amdgpu 0000:2d:00.0: amdgpu:  in process python3 pid 65605 thread python3 pid 65605)
[58755.291193] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000754e67e57000 from client 10
[58755.291197] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x0080113A
[58755.291200] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[58755.291203] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x0
[58755.291206] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x5
[58755.291209] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[58755.291212] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x1
[58755.291214] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[58755.292100] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32796)
[58755.292107] amdgpu 0000:2d:00.0: amdgpu:  in process python3 pid 65605 thread python3 pid 65605)
[58755.292111] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000754d6130a000 from client 10
[58755.292115] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[58755.292119] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[58755.292122] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[58755.292125] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[58755.292128] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[58755.292131] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[58755.292134] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[58755.292146] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32796)
[58755.292150] amdgpu 0000:2d:00.0: amdgpu:  in process python3 pid 65605 thread python3 pid 65605)
[58755.292154] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000754d6120a000 from client 10
[58755.292166] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32796)
[58755.292170] amdgpu 0000:2d:00.0: amdgpu:  in process python3 pid 65605 thread python3 pid 65605)
[58755.292174] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000754d6220a000 from client 10
[58755.292185] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32796)
[58755.292190] amdgpu 0000:2d:00.0: amdgpu:  in process python3 pid 65605 thread python3 pid 65605)
[58755.292193] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000754d63a0a000 from client 10
[58755.292205] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32796)
[58755.292209] amdgpu 0000:2d:00.0: amdgpu:  in process python3 pid 65605 thread python3 pid 65605)
[58755.292212] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000754d6230a000 from client 10
[58755.292224] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32796)
[58755.292228] amdgpu 0000:2d:00.0: amdgpu:  in process python3 pid 65605 thread python3 pid 65605)
[58755.292231] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000754d63b0a000 from client 10
[58947.697357] show_signal: 23 callbacks suppressed
[58947.697360] traps: python3[65649] general protection fault ip:7552a25149a2 sp:7551597fec50 error:0 in libc.so.6[289a2,7552a2514000+188000]
[58947.840661] amdgpu: Freeing queue vital buffer 0x754e16200000, queue evicted
[58947.840665] amdgpu: Freeing queue vital buffer 0x754e1c200000, queue evicted
```

---

### 评论 #6 — Phezzan (2025-10-31T23:31:56Z)

7.1 ... is better.
The system remains fairly usable, though it repeatedly halts momentarily
This halting coincides with memory usage jumping up and instantly back down ~10G repeatedly during image generation.

This squeezes almost all the disk cache out of my 48GB of RAM.

a few images do successfully generate, and when they fail you get a simple memory error:
```
comfy_srv  | Prompt executed in 68.29 seconds
comfy_srv  | EasyCache enabled - threshold: 0.2, start_percent: 0.15, end_percent: 0.95
comfy_srv  | Requested to load SDXL
comfy_srv  | Requested to load ControlNet
comfy_srv  | loaded completely 10792.81044921875 4897.0483474731445 True
comfy_srv  | loaded completely 5859.9115234375 2386.120147705078 True
 41%|████▏     | 12/29 [00:05<00:07,  2.25it/s]Memory access fault by GPU node-1 (Agent handle: 0x3158d740) on address 0x731276071000. Reason: Page not present or supervisor privilege.
comfy_srv  | Failed to create GPU coredump: File exists
comfy_srv  | GPU core dump failed
comfy_srv exited with code 0
```

meanwhile over in dmesg
```
...
[20146.621557] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20146.890079] amdgpu 0000:2d:00.0: amdgpu: 0000000076584ecb pin failed
[20146.890085] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20147.054691] amdgpu 0000:2d:00.0: amdgpu: 0000000076584ecb pin failed
[20147.054696] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20147.218258] amdgpu 0000:2d:00.0: amdgpu: 000000005fb32cc8 pin failed
[20147.218266] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20147.856913] amdgpu 0000:2d:00.0: amdgpu: 00000000c6d4f2b6 pin failed
[20147.856921] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20148.044451] amdgpu 0000:2d:00.0: amdgpu: 0000000076584ecb pin failed
[20148.044457] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20148.214739] amdgpu 0000:2d:00.0: amdgpu: 00000000c6d4f2b6 pin failed
[20148.214744] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20148.223224] amdgpu 0000:2d:00.0: amdgpu: 00000000c82e792a pin failed
[20148.223230] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20148.470580] amdgpu 0000:2d:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[20148.472229] amdgpu 0000:2d:00.0: amdgpu: 0000000076584ecb pin failed
[20148.472443] amdgpu 0000:2d:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[20148.472235] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20152.828878] amdgpu 0000:2d:00.0: amdgpu: 00000000c6d4f2b6 pin failed
[20152.828885] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
[20708.622603] gmc_v12_0_process_interrupt: 1433 callbacks suppressed
[20708.622607] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622614] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622618] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000731294698000 from client 10
[20708.622622] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841051
[20708.622625] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[20708.622629] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[20708.622632] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[20708.622634] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x5
[20708.622637] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[20708.622640] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x1
[20708.622651] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622656] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622660] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000731287ce3000 from client 10
[20708.622672] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622676] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622680] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000073127b9e1000 from client 10
[20708.622691] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622695] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622699] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000073128c409000 from client 10
[20708.622710] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:173 vmid:8 pasid:32784)
[20708.622715] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622719] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000731290b2a000 from client 10
[20708.622729] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622734] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622738] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000731287ce3000 from client 10
[20708.622748] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622753] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622757] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000073127b9e1000 from client 10
[20708.622768] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622772] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622776] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000731294698000 from client 10
[20708.622787] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622791] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622795] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000731294738000 from client 10
[20708.622807] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32784)
[20708.622812] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 44913 thread python3 pid 44913
[20708.622816] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x00007312b2a66000 from client 10
[20709.963248] amdgpu: Freeing queue vital buffer 0x73168d800000, queue evicted
[20709.963253] amdgpu: Freeing queue vital buffer 0x73168f600000, queue evicted
[20709.963255] amdgpu: Freeing queue vital buffer 0x731690000000, queue evicted
[20711.588111] workqueue: kfd_process_wq_release [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
```

Since this crashes comfyUI, it has the added benefit that docker restarts the container and service is restored 👍 

---

### 评论 #7 — Phezzan (2025-11-01T02:43:40Z)

rocm/pytorch 7.1 docker - got a hang in comfy... 

dmesg
```
... [older messages]
[30509.777575] gmc_v12_0_process_interrupt: 662 callbacks suppressed
[30509.777580] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777595] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777600] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b507008000 from client 10
[30509.777603] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[30509.777606] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[30509.777611] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[30509.777614] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[30509.777618] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[30509.777620] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[30509.777622] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[30509.777632] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777636] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777641] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b507009000 from client 10
[30509.777644] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[30509.777646] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[30509.777648] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[30509.777651] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[30509.777653] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[30509.777662] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[30509.777664] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[30509.777675] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777678] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777680] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b50700a000 from client 10
[30509.777684] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[30509.777688] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[30509.777691] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[30509.777693] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[30509.777695] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[30509.777697] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[30509.777699] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[30509.777712] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777716] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777718] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b50700b000 from client 10
[30509.777722] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[30509.777724] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[30509.777726] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[30509.777728] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[30509.777732] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[30509.777735] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[30509.777737] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[30509.777746] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777749] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777754] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b50700b000 from client 10
[30509.777762] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[30509.777766] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[30509.777768] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[30509.777773] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[30509.777783] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[30509.777787] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[30509.777789] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[30509.777798] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777805] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777810] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b50700c000 from client 10
[30509.777813] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[30509.777815] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[30509.777817] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[30509.777820] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[30509.777822] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[30509.777824] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[30509.777826] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[30509.777838] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777841] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777844] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b507019000 from client 10
[30509.777846] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[30509.777848] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[30509.777851] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x1
[30509.777853] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[30509.777855] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[30509.777857] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[30509.777859] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
[30509.777871] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777874] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777877] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b496beb000 from client 10
[30509.777889] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777892] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777894] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b496bec000 from client 10
[30509.777907] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32784)
[30509.777910] amdgpu 0000:2d:00.0: amdgpu:  Process python3 pid 55798 thread python3 pid 55798
[30509.777912] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x000076b496bed000 from client 10
[30511.290853] amdgpu: Freeing queue vital buffer 0x76b80cc00000, queue evicted
[30511.290858] amdgpu: Freeing queue vital buffer 0x76b80ea00000, queue evicted
[30511.290861] amdgpu: Freeing queue vital buffer 0x76b810000000, queue evicted
[30683.595703] systemd-journald[697]: Under memory pressure, flushing caches.
[30685.644687] systemd-journald[697]: Under memory pressure, flushing caches.
```

---

### 评论 #8 — tcgu-amd (2025-11-04T21:42:31Z)

Hi @Phezzan, this might be related to a known bug in hipblaslt specific to gfx12. Forcing Pytorch to use rocblas instead for torch was known to temporarily resolve this, but unfortunately this requires patching pytorch and rebuilding it, which is not trivial (please feel free to give it a try though). We are currently working on a patch for hipblaslt, and once we are done we will try to get it out of the gate ASAP. 

The fact that you said it used to work with rocm 6.4.4 + torch 2.7.1 seems to match it pretty well. This issue pretty much will only affect rocm > 6.4 and pytorch versions higher than somewhere between 2.7.x to 2.8 (not sure exactly when) because of this change in torch to set hipblaslt as perferred backend https://github.com/pytorch/pytorch/blob/7f0e9321360cb13563a11bf9c720464c3dbf1ece/aten/src/ATen/Context.cpp#L437. 

To patch it, you just want to remove the gfx1200 and gfx1201 targets from the file linked above, then build and install torch (you can try using TheRock if that helps). Then, export the following env vars before running your workload

`export ROCBLAS_USE_HIPBLASLT=0 ROCBLAS_USE_HIPBLASLT_BATCHED=0 MIOPEN_USE_HIPBLASLT=0`

Please let me know if you have any additional questions. Thanks! 

---

### 评论 #9 — Phezzan (2025-11-06T05:07:48Z)

Thanks - it makes sense that some execution provider has a bug/incompatibility that hangs execution.

Tried compiling pytorch 2.9.0 (current release), but it died complaining

```
  In file included from /home/jk/comfy/src/torch/release/2.9/test/cpp/aoti_abi_check/test_headeronlyarrayref.cpp:3:
  /home/jk/comfy/src/torch/release/2.9/torch/headeronly/util/HeaderOnlyArrayRef.h: In member function ‘constexpr bool c10::HeaderOnlyArrayRef<T>::allMatch(const std::function<bool(const T&)>&) const’:
  /home/jk/comfy/src/torch/release/2.9/torch/headeronly/util/HeaderOnlyArrayRef.h:134:17: error: ‘all_of’ is not a member of ‘std’
    134 |     return std::all_of(cbegin(), cend(), pred);
```

I'll try 2.8.0 later.

PS: 
I found information about ubuntu choosing 'linux-firmware' over 'amdgpu-dkms-firmware' 
It was confusing to understand, and I was unfamiliar with the whole 'pinning' system which didn't appear to do anything until I issued `apt reinstall amdgpu-dkms-firmware`

While that appears to have worked, It seems gaming performance dropped a bit... but I have no reliable test data.

---

### 评论 #10 — Phezzan (2025-11-06T18:16:37Z)

So 2.8 also fails... I've got some .. incompatible header problem ... 

```
  In file included from /home/jk/comfy/src/torch/release/2.8/test/cpp/aoti_abi_check/test_headeronlyarrayref.cpp:3:
  /home/jk/comfy/src/torch/release/2.8/torch/headeronly/util/HeaderOnlyArrayRef.h: In member function ‘constexpr bool c10::HeaderOnlyArrayRef<T>::allMatch(const std::function<bool(const T&)>&) const’:
  /home/jk/comfy/src/torch/release/2.8/torch/headeronly/util/HeaderOnlyArrayRef.h:134:17: error: ‘all_of’ is not a member of ‘std’
    134 |     return std::all_of(cbegin(), cend(), pred);
        |                 ^~~~~~
```

Ok - I added 
```
#include <algorithm>
```

Now I see 
```
      Removing file or directory /home/jk/.pyenv/versions/3.12.11/envs/comfy12/lib/python3.12/site-packages/torchgen/
      Successfully uninstalled torch-2.8.0+rocm7.1.0.lw.git7a520360
  changing mode of /home/jk/.pyenv/versions/comfy12/bin/torchfrtrace to 775
  changing mode of /home/jk/.pyenv/versions/comfy12/bin/torchrun to 775
Successfully installed torch-2.10.0a0+git2005b5f
```
🤞 
```
Traceback (most recent call last):
  File "/home/jk/comfy/ComfyUI/main.py", line 147, in <module>
    import comfy.utils
  File "/home/jk/comfy/ComfyUI/comfy/utils.py", line 24, in <module>
    import safetensors.torch
  File "/home/jk/.pyenv/versions/comfy12/lib/python3.12/site-packages/safetensors/torch.py", line 12, in <module>
    def storage_ptr(tensor: torch.Tensor) -> int:
                            ^^^^^^^^^^^^
AttributeError: module 'torch' has no attribute 'Tensor'
```
⚰️ 

---

### 评论 #11 — tcgu-amd (2025-11-24T21:02:31Z)

Hi all, just a quick update, the official patch did not make it to 7.1.1. We are currently looking at a ROCm 7.2. 

For easier tracking purposes, I will be closing this issue since it has the same root cause as https://github.com/ROCm/ROCm/issues/5245. Please use that ticket for future updates. In the meantime, feel free to continue to use this issue as a forum for discussions. 

Thanks! 

---

### 评论 #12 — Phezzan (2025-11-25T00:19:00Z)

Just to be clear - 6.4.4 / 2.7.1 works

7.1 works once or twice, then hangs in a busy loop.

---
