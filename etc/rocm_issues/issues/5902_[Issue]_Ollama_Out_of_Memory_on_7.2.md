# [Issue]: Ollama Out of Memory on 7.2

> **Issue #5902**
> **状态**: closed
> **创建时间**: 2026-01-26T12:23:44Z
> **更新时间**: 2026-03-09T13:23:40Z
> **关闭时间**: 2026-03-09T13:23:40Z
> **作者**: winmutt
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5902

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

ROCm is ooming under ollama with a model that fits easily in memory in ROCm 7.1:

qwen3:14b-q8_0                                             304bf7349c71    15 GB 

### Operating System

NAME="Ubuntu" VERSION="24.04.3 LTS (Noble Numbat)"

### CPU

model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S   Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S   Name:                    gfx1151                               Marketing Name:          AMD Radeon Graphics                       Name:                    amdgcn-amd-amdhsa--gfx1151                Name:                    amdgcn-amd-amdhsa--gfx11-generic      Name:                    aie2p                                 Marketing Name:          RyzenAI-npu5   

### ROCm Version

ROCm 7.2

### ROCm Component

rocm-core

### Steps to Reproduce

amdgpu reports 96G available (I'd love it if someone can tell me how to increase this to 112G avail).
```
kernel: [drm] amdgpu: 98304M of VRAM memory ready
```
amd-smi:
```
amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.1+fc0010cf6a    amdgpu version: Linuxver ROCm version: 7.2.0    |
| VBIOS version: 023.011.000.039.000001                                        |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0    AMD Radeon Graphics | N/A        N/A   0                 N/A |
|   0       0     N/A             N/A | N/A        N/A            161/98304 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+

```

ROCm appears to report 112G
```
ollama[1297]: time=2026-01-26T12:06:56.209Z level=INFO source=types.go:42 msg="inference compute" id=0 filter_id=0 library=ROCm compute=gfx1151 name=ROCm0 description="AMD Radeon Graphics" libdirs=ollama,rocm driver=60342.13 pci_id=0000:c5:00.0 type=iGPU total="111.5 GiB" available="111.3 GiB"
```

OOM
```
ollama[1297]: ROCm error: out of memory
ollama[1297]:   current device: 0, in function stream at //ml/backend/ggml/ggml/src/ggml-cuda/common.cuh:1248
ollama[1297]:   hipStreamCreateWithFlags(&streams[device][stream], 0x01)
ollama[1297]: //ml/backend/ggml/ggml/src/ggml-cuda/ggml-cuda.cu:94: ROCm error
ollama[1297]: /usr/local/lib/ollama/libggml-base.so.0(+0x1bae8)[0x7dd72c301ae8]
ollama[1297]: /usr/local/lib/ollama/libggml-base.so.0(ggml_print_backtrace+0x1e6)[0x7dd72c301eb6]
ollama[1297]: /usr/local/lib/ollama/libggml-base.so.0(ggml_abort+0x11d)[0x7dd72c30203d]
ollama[1297]: /usr/local/lib/ollama/rocm/libggml-hip.so(+0x1bd1c2)[0x7dd6c2dbd1c2]
ollama[1297]: /usr/local/lib/ollama/rocm/libggml-hip.so(+0x1c2b27)[0x7dd6c2dc2b27]
ollama[1297]: /usr/local/bin/ollama(+0x11fd64e)[0x55661b13164e]
ollama[1297]: /usr/local/bin/ollama(+0x1200430)[0x55661b134430]
ollama[1297]: /usr/local/bin/ollama(+0x119aaff)[0x55661b0ceaff]
ollama[1297]: /usr/local/bin/ollama(+0x3a4841)[0x55661a2d8841]
ollama[1297]: SIGABRT: abort
ollama[1297]: PC=0x7dd77709eb2c m=14 sigcode=18446744073709551610
ollama[1297]: signal arrived during cgo execution
ollama[1297]: goroutine 15 gp=0xc000703180 m=14 mp=0xc000701008 [syscall]:
ollama[1297]: runtime.cgocall(0x55661b0ceac8, 0xc0000490d8)
ollama[1297]:         runtime/cgocall.go:167 +0x4b fp=0xc0000490b0 sp=0xc000049078 pc=0x55661a2cd8ab
ollama[1297]: github.com/ollama/ollama/ml/backend/ggml._Cfunc_ggml_backend_sched_reserve(0x7dd6f4d031b0, 0x7dd5402be210)
```



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ESC[37mROCk module is loadedESC[0m
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.15
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
      Size:                    32484672(0x1efad40) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32484672(0x1efad40) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32484672(0x1efad40) KB             
      Allocatable:             TRUE                               
:
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32484672(0x1efad40) KB             
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
  BDFID:                   50432                              
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
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    100663296(0x6000000) KB            
      Allocatable:             TRUE                               
     Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    100663296(0x6000000) KB            
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
  Name:                    aie2p                              
  Uuid:                    AIE-XX                             
  Marketing Name:          RyzenAI-npu5                       
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
      Size:                    32484672(0x1efad40) KB             
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
      Size:                    32484672(0x1efad40) KB             
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

## 评论 (23 条)

### 评论 #1 — boyvanamstel (2026-01-28T08:01:05Z)

Same device. Same issue.

[After some research](https://www.youtube.com/watch?v=Hdg7zL3pcIs)  (video by @kyuz0) I discovered that it's due to a few components causing issues when they don't exactly match the expected version.

---

### 评论 #2 — winmutt (2026-01-28T10:18:40Z)

I tried adjusting the bios enabling and disabling the reserved memory allocation, all with the same result. 

Disabled in BIOS
```
kernel: [drm] amdgpu: 31965M of GTT memory ready.
```

Set to 512M
```
kernel: [drm] amdgpu: 512M of VRAM memory ready
kernel: [drm] amdgpu: 63969M of GTT memory ready.
```

I had missed the new amd-ttm instructions. After setting the video allocation to 512M and using amd-ttm I was able to achieve what appears to be a good configuration:

amd-ttm
```
kernel: [drm] amdgpu: 512M of VRAM memory ready
kernel: [drm] amdgpu: 110592M of GTT memory ready.
ollama[1293]: time=2026-01-28T10:12:52.482Z level=INFO source=types.go:42 msg="inference compute" id=0 filter_id=0 library=ROCm compute=gfx1151 name=ROCm0 description="AMD Radeon Graphics" libdirs=ollama,rocm driver=60342.13 pci_id=0000:c5:00.0 type=iGPU total="108.5 GiB" available="108.3 GiB"

# amd-ttm 
💻 Current TTM pages limit: 28311552 pages (108.00 GB)
💻 Total system memory: 124.94 GB
```










---

### 评论 #3 — winmutt (2026-01-29T12:03:17Z)

This appears to be an ollama problem as I am able to get rocm 7.2 working with lemonade-server.

---

### 评论 #4 — amd-nicknick (2026-01-29T12:06:12Z)

Hi @winmutt, but you mentioned it was working on ROCm 7.1 before? I'm looking into this now and tracking down possible regression.
The lemonade-server works differently so I'm afraid it's not quite comparable, but if that will suffice your use-case, I can lower the priority a bit?

---

### 评论 #5 — winmutt (2026-01-29T12:58:15Z)

@amd-nicknick works for my use case, feel free to adjust priority! Thanks for all the hard work you do!

Ollama was working on 7.1 before, or atleast not OOMing.

---

### 评论 #6 — amd-nicknick (2026-01-29T13:48:52Z)

Thanks for confirming, this helps me to narrow-down the issue. I'll still check on what happened with ollama. Keeping this issue open & will update with my findings.
Since ollama does some memory usage calculation on its own, it might be basing calculation on something we change between 7.1 and 7.2.

---

### 评论 #7 — BenjaminBenetti (2026-02-05T05:59:44Z)

I'm also getting this no matter the model size. on my `AMD RYZEN AI MAX+ 395` .

tried configuring memory in BIOS and with `amd-ttm`
```
💻 Current TTM pages limit: 26214400 pages (100.00 GB)
💻 Total system memory: 125.08 GB
```
but no change.

Switching to the Vulkan backend gets things working as a work around in the mean time, though I look forward to a ROCm fix.

For any one reading you can switch to Vulkan by setting these environment variables
```
OLLAMA_VULKAN=1
ROCR_VISIBLE_DEVICES=-1
```

---

### 评论 #8 — stratmm (2026-02-05T10:53:44Z)

Same here, just rebuild last night with latest rocm nightly and latest ollama.

---

### 评论 #9 — bh1rio (2026-02-07T10:48:56Z)

Same error when i run offical docker images of ollama on my archlinux.

But ollama pkg of archlinux is ok, and rocm is 7.2.

So I think that the docker images is build by early version rocm.

---

### 评论 #10 — mcurtis789 (2026-02-18T17:03:03Z)

I am running MS-S1 MAX and I appear to be encountering the same issue. The following does seem to act as a workaround. 

```
OLLAMA_VULKAN=1
ROCR_VISIBLE_DEVICES=-1
````

journalctl 
```
found" key=tokenizer.ggml.add_eos_token default=false
Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.202Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=tokenizer.ggml.eos_token_ids default="&{size:0 values:[]}"
Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.rope.scaling.type default=""
Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.rope.scaling.factor default=1
Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.rope.scaling.original_context_length default=0
Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.norm_top_k_prob default=true
Feb 18 16:56:30 ms-s1-max ollama[27678]: ROCm error: out of memory
Feb 18 16:56:30 ms-s1-max ollama[27678]:   current device: 0, in function stream at //ml/backend/ggml/ggml/src/ggml-cuda/common.cuh:1248
Feb 18 16:56:30 ms-s1-max ollama[27678]:   hipStreamCreateWithFlags(&streams[device][stream], 0x01)
Feb 18 16:56:30 ms-s1-max ollama[27678]: //ml/backend/ggml/ggml/src/ggml-cuda/ggml-cuda.cu:94: ROCm error
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/libggml-base.so.0(+0x1bae8) [0x71bdd5cffae8]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/libggml-base.so.0(ggml_print_backtrace+0x1e6) [0x71bdd5cffeb6]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/libggml-base.so.0(ggml_abort+0x11d) [0x71bdd5d0003d]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/rocm/libggml-hip.so(+0x1bd1c2) [0x71bdaadbd1c2]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/rocm/libggml-hip.so(+0x1c2b27) [0x71bdaadc2b27]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x1338b4e) [0x57fd74fe3b4e]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x133b930) [0x57fd74fe6930]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x12b271b) [0x57fd74f5d71b]
Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x3cdb41) [0x57fd74078b41]
Feb 18 16:56:30 ms-s1-max ollama[27678]: SIGABRT: abort
```

ENV Vars
```
Environment="OLLAMA_CONTEXT_LENGTH=64000"
Environment="HSA_OVERRIDE_GFX_VERSION=11.5.1"
#Environment="OLLAMA_VULKAN=1"
#Environment="ROCR_VISIBLE_DEVICES=-1"
Environment="OLLAMA_DEBUG=1"
```

rocminfo
```
*******
Agent 2
*******
  Name:                    gfx1151
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon Graphics
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
```

amd-smi
```
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.1+fc0010cf6a    amdgpu version: 6.18.7-061807 ROCm version: 7.2.0    |
| VBIOS version: 00107962                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:f4:00.0    AMD Radeon Graphics | N/A        N/A   0                 N/A |
|   0       0     N/A             N/A | N/A        N/A             151/1024 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```

amd-ttm
```
💻 Current TTM pages limit: 26214400 pages (100.00 GB)
💻 Total system memory: 122.20 GB
```

radeontop
```
                                         Graphics pipe   0.00% x
qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
                                          Event Engine   0.00% x
                                                               x
                           Vertex Grouper + Tesselator   0.00% x
                                                               x
                                     Texture Addresser   0.00% x
                                         Texture Cache   0.00% x
                                                               x
                                         Shader Export   0.00% x
                           Sequencer Instruction Cache   0.00% x
                                   Shader Interpolator   0.00% x
                                Shader Memory Exchange   0.00% x
                                                               x
                                        Scan Converter   0.00% x
                                    Primitive Assembly   0.00% x
                                                               x
                                           Depth Block   0.00% x
                                           Color Block   0.00% x
                                        Clip Rectangle   0.00% x
                                                               x
                                      151M / 865M VRAM  17.49% x
                                     18M / 102382M GTT   0.02% x
                            0.55G / 1.00G Memory Clock  54.90% x
                            0.60G / 2.90G Shader Clock  20.74% x
```

---

### 评论 #11 — stratmm (2026-02-18T23:18:52Z)

> I am running MS-S1 MAX and I appear to be encountering the same issue. The following does seem to act as a workaround.
> 
> ```
> OLLAMA_VULKAN=1
> ROCR_VISIBLE_DEVICES=-1
> ```
> 
> journalctl
> 
> ```
> found" key=tokenizer.ggml.add_eos_token default=false
> Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.202Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=tokenizer.ggml.eos_token_ids default="&{size:0 values:[]}"
> Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.rope.scaling.type default=""
> Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.rope.scaling.factor default=1
> Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.rope.scaling.original_context_length default=0
> Feb 18 16:56:30 ms-s1-max ollama[27678]: time=2026-02-18T16:56:30.203Z level=DEBUG source=ggml.go:300 msg="key with type not found" key=qwen3moe.norm_top_k_prob default=true
> Feb 18 16:56:30 ms-s1-max ollama[27678]: ROCm error: out of memory
> Feb 18 16:56:30 ms-s1-max ollama[27678]:   current device: 0, in function stream at //ml/backend/ggml/ggml/src/ggml-cuda/common.cuh:1248
> Feb 18 16:56:30 ms-s1-max ollama[27678]:   hipStreamCreateWithFlags(&streams[device][stream], 0x01)
> Feb 18 16:56:30 ms-s1-max ollama[27678]: //ml/backend/ggml/ggml/src/ggml-cuda/ggml-cuda.cu:94: ROCm error
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/libggml-base.so.0(+0x1bae8) [0x71bdd5cffae8]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/libggml-base.so.0(ggml_print_backtrace+0x1e6) [0x71bdd5cffeb6]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/libggml-base.so.0(ggml_abort+0x11d) [0x71bdd5d0003d]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/rocm/libggml-hip.so(+0x1bd1c2) [0x71bdaadbd1c2]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/lib/ollama/rocm/libggml-hip.so(+0x1c2b27) [0x71bdaadc2b27]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x1338b4e) [0x57fd74fe3b4e]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x133b930) [0x57fd74fe6930]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x12b271b) [0x57fd74f5d71b]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: /usr/local/bin/ollama(+0x3cdb41) [0x57fd74078b41]
> Feb 18 16:56:30 ms-s1-max ollama[27678]: SIGABRT: abort
> ```
> 
> ENV Vars
> 
> ```
> Environment="OLLAMA_CONTEXT_LENGTH=64000"
> Environment="HSA_OVERRIDE_GFX_VERSION=11.5.1"
> #Environment="OLLAMA_VULKAN=1"
> #Environment="ROCR_VISIBLE_DEVICES=-1"
> Environment="OLLAMA_DEBUG=1"
> ```
> 
> rocminfo
> 
> ```
> *******
> Agent 2
> *******
>   Name:                    gfx1151
>   Uuid:                    GPU-XX
>   Marketing Name:          AMD Radeon Graphics
>   Vendor Name:             AMD
>   Feature:                 KERNEL_DISPATCH
> ```
> 
> amd-smi
> 
> ```
> +------------------------------------------------------------------------------+
> | AMD-SMI 26.2.1+fc0010cf6a    amdgpu version: 6.18.7-061807 ROCm version: 7.2.0    |
> | VBIOS version: 00107962                                                      |
> | Platform: Linux Baremetal                                                    |
> |-------------------------------------+----------------------------------------|
> | BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
> | GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
> |=====================================+========================================|
> | 0000:f4:00.0    AMD Radeon Graphics | N/A        N/A   0                 N/A |
> |   0       0     N/A             N/A | N/A        N/A             151/1024 MB |
> +-------------------------------------+----------------------------------------+
> +------------------------------------------------------------------------------+
> | Processes:                                                                   |
> |  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
> |==============================================================================|
> |  No running processes found                                                  |
> +------------------------------------------------------------------------------+
> ```
> 
> amd-ttm
> 
> ```
> 💻 Current TTM pages limit: 26214400 pages (100.00 GB)
> 💻 Total system memory: 122.20 GB
> ```
> 
> radeontop
> 
> ```
>                                          Graphics pipe   0.00% x
> qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
>                                           Event Engine   0.00% x
>                                                                x
>                            Vertex Grouper + Tesselator   0.00% x
>                                                                x
>                                      Texture Addresser   0.00% x
>                                          Texture Cache   0.00% x
>                                                                x
>                                          Shader Export   0.00% x
>                            Sequencer Instruction Cache   0.00% x
>                                    Shader Interpolator   0.00% x
>                                 Shader Memory Exchange   0.00% x
>                                                                x
>                                         Scan Converter   0.00% x
>                                     Primitive Assembly   0.00% x
>                                                                x
>                                            Depth Block   0.00% x
>                                            Color Block   0.00% x
>                                         Clip Rectangle   0.00% x
>                                                                x
>                                       151M / 865M VRAM  17.49% x
>                                      18M / 102382M GTT   0.02% x
>                             0.55G / 1.00G Memory Clock  54.90% x
>                             0.60G / 2.90G Shader Clock  20.74% x
> ```

You seem to just be eneabling the vulkan drvier and therefore disabling the use of ROCM?

---

### 评论 #12 — mcurtis789 (2026-02-19T10:19:03Z)

I am currently using OLLAMA_VULKAN=1 and ROCR_VISIBLE_DEVICES=-1 as a work around. If i just just HSA_OVERRIDE_GFX_VERSION=11.5.1 I get the out of memory error.

---

### 评论 #13 — amd-nicknick (2026-02-23T13:19:14Z)

Hi all, I spent some time looking into this. This is a Ollama integration issue with ROCm.

Ollama packages all ROCm dependency in an effort to make itself portable, but this means system installed ROCm will not be used.
In order to use Ollama with ROCm 7, you must rebuild Ollama with ROCm 7 toolchain. Since Ollama only supports ROCm 6.3.3, you also need to patch it.

I did a quick test, and I could run llama3.2 + Ollama + ROCm 7 without any errors.
@winmutt, @mcurtis789, @bh1rio, could you please try rebuilding Ollama + ROCm 7.2 toolchain? I used the Docker build + `rocm/dev-almalinux-8:7.2-complete` image.

---

### 评论 #14 — BenjaminBenetti (2026-02-24T04:46:28Z)

Hey @amd-nicknick I know you didn't tag me but I've been following this closely. 

I did as you asked and rebuilt Ollama with ROCm 7.2, and it works perfectly! 

My system: 
```
OS: Fedora Linux 43 (Workstation Edition) x86_64
Host: Desktop (AMD Ryzen AI Max 300 Series) (A6)
Kernel: Linux 6.18.10-200.fc43.x86_64
CPU: AMD RYZEN AI MAX+ 395 (32) @ 5.19 GHz
GPU: AMD Radeon 8060S Graphics [Integrated]
Memory: 53.51 GiB / 125.08 GiB (43%)
```

I had to modify the following files to get ollama building 

```
+++ b/CMakePresets.json
@@ -73,7 +73,7 @@
       "inherits": [ "ROCm" ],
       "cacheVariables": {
         "CMAKE_HIP_FLAGS": "-parallel-jobs=4",
-        "AMDGPU_TARGETS": "gfx940;gfx941;gfx942;gfx1010;gfx1012;gfx1030;gfx1100;gfx1101;gfx1102;gfx1151;gfx1200;gfx1201;gfx908:xnack-;gfx90a:xnack+;gfx90a:xnack-",
+        "AMDGPU_TARGETS": "gfx942;gfx1010;gfx1012;gfx1030;gfx1100;gfx1101;gfx1102;gfx1151;gfx1200;gfx1201;gfx908:xnack-;gfx90a:xnack+;gfx90a:xnack-",
```
and 
```
+++ b/Dockerfile
@@ -3,7 +3,7 @@
 ARG FLAVOR=${TARGETARCH}
 ARG PARALLEL=8
 
-ARG ROCMVERSION=6.3.3
+ARG ROCMVERSION=7.2
```
finally
```
+++ CMakeLists.txt
@@ -148,7 +148,7 @@ if(CMAKE_HIP_COMPILER)
         )
         install(RUNTIME_DEPENDENCY_SET rocm
                 DIRECTORIES ${HIP_BIN_INSTALL_DIR} ${HIP_LIB_INSTALL_DIR}
-                PRE_INCLUDE_REGEXES hipblas rocblas amdhip64 rocsolver amd_comgr hsa-runtime64 rocsparse tinfo rocprofiler-register drm drm_amdgpu numa elf
+                PRE_INCLUDE_REGEXES hipblas rocblas amdhip64 rocsolver amd_comgr hsa-runtime64 rocsparse tinfo rocprofiler-register drm drm_amdgpu numa elf roctx64 rocroller
```

The first 2 changes where pretty obvious. But for the last edit, not gonna lie, Claude bailed me out, had no idea the shared libraries where missing (it booted fine but would only use CPU).

I built with 
```
docker build --build-arg FLAVOR=rocm . -t ollama:rocm-7.2
```

Then to run 
```
docker run --rm --device /dev/kfd --device /dev/dri  -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama:rocm-7.2
```

Bam, working ollama with ROCm 7.2 
```
time=2026-02-24T04:41:24.130Z level=INFO source=runner.go:67 msg="discovering available GPUs..."
time=2026-02-24T04:41:24.130Z level=INFO source=server.go:431 msg="starting runner" cmd="/usr/bin/ollama runner --ollama-engine --port 45627"
time=2026-02-24T04:41:24.185Z level=INFO source=server.go:431 msg="starting runner" cmd="/usr/bin/ollama runner --ollama-engine --port 39647"
time=2026-02-24T04:41:24.736Z level=INFO source=types.go:42 msg="inference compute" id=0 filter_id=0 library=ROCm compute=gfx1151 name=ROCm0 description="Radeon 8060S Graphics" libdirs=ollama,rocm driver=70226.1 pci_id=0000:c2:00.0 type=iGPU total="100.5 GiB" available="98.2 GiB"
time=2026-02-24T04:41:24.736Z level=INFO source=routes.go:1768 msg="vram-based default context" total_vram="100.5 GiB" default_num_ctx=262144

```


---

### 评论 #15 — amd-nicknick (2026-02-24T06:21:30Z)

@BenjaminBenetti That's great news, thanks for confirming!
I have been talking to a few folks internally; we had actually submitted a PR upstream to Ollama to add ROCm7 support.
https://github.com/ollama/ollama/pull/14328
@winmutt, @stratmm, @bh1rio, @mcurtis789, could you please give this a try as well?

---

### 评论 #16 — mcurtis789 (2026-02-24T12:08:42Z)

@amd-nicknick  are you able to provide the steps you followed? I tried following the step that @BenjaminBenetti  shared but I am running into issues building the image. 
```
Step 16/138 : RUN yum install -y yum-utils epel-release     && dnf install -y clang ccache git     && yum-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/sbsa/cuda-rhel8.repo
 ---> [Warning] The requested image's platform (linux/arm64/v8) does not match the detected host platform (linux/amd64/v4) and no specific platform was requested
 ---> Running in f417c8a5e207
exec /bin/sh: exec format error
The command '/bin/sh -c yum install -y yum-utils epel-release     && dnf install -y clang ccache git     && yum-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/sbsa/cuda-rhel8.repo' returned a non-zero code: 255
```


---

### 评论 #17 — amd-nicknick (2026-02-24T14:47:24Z)

@mcurtis789, try these steps:
1. Clone ~~https://github.com/superm1/ollama/tree/main~~ https://github.com/dhiltgen/ollama/tree/rocm_bump, this contains the ROCm 7 bump changes altogether, and is open to review in ~~https://github.com/ollama/ollama/pull/14328~~ https://github.com/ollama/ollama/pull/14391
2.  Build
`docker build --build-arg FLAVOR=rocm --tag ollama-rocm7.2 --platform=linux/amd64 .`

For some reason it seems like Docker is attempting to build ARM image on your system. Specifying the platform flag should resolve this.

EDIT: PR dropped in favor for https://github.com/ollama/ollama/pull/14391

---

### 评论 #18 — mcurtis789 (2026-02-24T23:10:59Z)

Turns out I was missing docker-buildx. I can confirm that rocm 7.2 + ollama is working for me now. Thank you!

---

### 评论 #19 — james-bq (2026-03-02T22:42:17Z)

Any idea when https://github.com/ollama/ollama/pull/14391 is getting merged?

---

### 评论 #20 — cvocvo (2026-03-02T22:52:20Z)

> Any idea when [ollama/ollama#14391](https://github.com/ollama/ollama/pull/14391) is getting merged?

Unclear ETA + probably a question for the Ollama maintainers instead of ROCm. We've been following this PR for a few months https://github.com/ollama/ollama/pull/13000 and using this variant that the PR is based on in the meantime: https://github.com/rjmalagon/ollama-linux-amd-apu/
There isn't a _release_ version of 17.x for ollama-linux-amd-apu however 17.4 is merged; https://github.com/rjmalagon/ollama-linux-amd-apu/activity
We just pulled/compiled it and it seems to be running fine with an R9700.

---

### 评论 #21 — cocofhu (2026-03-07T22:49:22Z)

After I updated the kernel, I started having this issue.
sudo apt update && sudo apt install linux-oem-24.04c
According to the ROCm 7.2 installation guide:
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html

---

### 评论 #22 — amd-nicknick (2026-03-09T09:44:20Z)

@cocofhu, you'd need to provide further information so I could assess the issue you're encountering. 
What error message? Any log files you could provide? Are you using self-built ollama?

---

### 评论 #23 — amd-nicknick (2026-03-09T13:23:40Z)

Closing this issue as resolved.

---
