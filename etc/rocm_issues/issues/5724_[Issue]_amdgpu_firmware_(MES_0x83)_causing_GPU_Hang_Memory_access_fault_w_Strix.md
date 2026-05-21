# [Issue]: amdgpu firmware (MES 0x83) causing GPU Hang / Memory access fault w/ Strix Halo

> **Issue #5724**
> **状态**: closed
> **创建时间**: 2025-11-29T00:14:14Z
> **更新时间**: 2026-03-04T14:51:11Z
> **关闭时间**: 2026-01-15T09:56:23Z
> **作者**: ianbmacdonald
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5724

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

### Problem Description

--> Jump right to the bottom for ROCm 7.2 + 24.04-oem kernels https://github.com/ROCm/ROCm/issues/5724#issuecomment-3821014371

This new firmware causes a GPU fault in known working scenarios.   This was the case for ROCm 7.1.0, and the problem persists after the release of ROCm 7.1.1 just a few days ago. 

TDLR;  Stick to the amdgpu-dkms-firmware package and keep the `cwsr_enable=0` workaround in place.  Older MES 0x80 does not cause this issue.

A new [amdgpu firmware ](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/log/?qt=grep&q=amdgpu) appeared upstream for the Strix Halo (gfx1151).   It can be seen upstream in ubuntu-proposed [linux-firmware](https://code.launchpad.net/ubuntu/+source/linux-firmware/20251125.gitff6418d1-0ubuntu1).  It is just a matter of time before this firmware lands on users with recent linux kernels that may opt not to use the amdgpu-dkms* packages, as the amdgpu stack ships with newer kernels and ABI compatibility with the newest kernels is not baked into the shipped dkms modules.  Additionally the upstream Ubuntu firmware bundle carries new firmware for MT7925 bluetooth and wifi components integrated into most Strix Halo SoCs currently pulling more Strix Halo users in this direction because of other quirks. 

One simple way to reproduce is to use an AMD ROCm vLLM build and serve the smallest of the IBM granite4 hybrid Mamba models.  The result a terminal error similar to the following. 

`Memory access fault by GPU node-1 (Agent handle: 0x43578c10) on address 0x7f58f8001000. Reason: Page not present or supervisor privilege.`

Additionally, the kernel dmesg emits a page fault
```
[  651.971687] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32771)
[  651.971715] amdgpu 0000:c5:00.0: amdgpu:  Process VLLM::EngineCor pid 2419 thread VLLM::EngineCor pid 2419
[  651.971725] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f58f8001000 from client 10
[  651.971734] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[  651.971741] amdgpu 0000:c5:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPF (0x4)
[  651.971748] amdgpu 0000:c5:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  651.971754] amdgpu 0000:c5:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[  651.971761] amdgpu 0000:c5:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  651.971769] amdgpu 0000:c5:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  651.971774] amdgpu 0000:c5:00.0: amdgpu: 	 RW: 0x0
[  652.292990] amdgpu: Freeing queue vital buffer 0x7f56f8a00000, queue evicted
```

Some additional notes:
- sticking with default kernels, ROCm 7.1.1 and amdgpu 30.20.1 packages will not trip on this as amdgpu-dkms-firmware overrides linux-firmware on Ubuntu by default.  You still need the cwsr workaround in #5590 to avoid that separate GPU hang issue on ROCm 7.1.1. 

- The amdgpu instinct 30.20.1 amdgpu-dkms-firmware was released a few days ago, but ships the older MES 0x80 firmware, possibly indicating a known issue at the time of release.  Also, another RDNA 3 firmware, the gfx1101 updates, were rolled back as seen in the amdgpu linux-firmware commits linked above. 

- As noted earlier, the previous MES hang in #5590 must still be worked around with the `amdgpu.cwsr_enable=0` kernel flag.  Without that flag enabled, ROCm 7.1.1 and amdgpu 30.20.1 on Ubuntu 24.04.3 will still cause a separate known GPU hang, and so the workaround in #5590 must still be enabled.


### Operating System

Ubuntu 24.04.3

### CPU

Strix Halo

### GPU

Strix Halo

### ROCm Version

ROCm 7.1.1

### ROCm Component

_No response_

### Steps to Reproduce


Grab an AMD vllm image;  Either the most recent stable (built against ROCm 7.0) or current nightly (built against ROCm 7.1) will do or [build your own](https://github.com/ROCm/aiter/issues/900#issuecomment-3523554029). 

`docker pull rocm/vllm:rocm7.0.0_vllm_0.11.1_20251103` 
or
`docker pull rocm/vllm-dev:nightly`

Fire up docker 
```
 docker run -it \
    --network host \
    --ipc host \
    --privileged \
    --cap-add=CAP_SYS_ADMIN \
    --cap-add=SYS_PTRACE \
    --device=/dev/kfd \
    --device=/dev/dri \
    --device=/dev/mem \
    --security-opt seccomp=unconfined \
    --shm-size 4G \
    -e TERM=xterm-256color \
    -v /mnt/models/huggingface/:/root/.cache/huggingface/ \
    --name vllm-strixhalohang \
    rocm/vllm:rocm7.0.0_vllm_0.11.1_20251103
```
Serve the model

```
root@ai2:/app# vllm serve ibm-granite/granite-4.0-h-350m
INFO 11-28 23:05:28 [__init__.py:225] Automatically detected platform rocm.
(APIServer pid=13) INFO 11-28 23:05:33 [api_server.py:1876] vLLM API server version 0.11.1rc2.dev141+g38f225c2a
(APIServer pid=13) INFO 11-28 23:05:33 [utils.py:243] non-default args: {'model_tag': 'ibm-granite/granite-4.0-h-350m', 'model': 'ibm-granite/granite-4.0-h-350m'}
(APIServer pid=13) INFO 11-28 23:05:41 [model.py:658] Resolved architecture: GraniteMoeHybridForCausalLM
(APIServer pid=13) INFO 11-28 23:05:41 [model.py:1745] Using max model len 32768
(APIServer pid=13) INFO 11-28 23:05:42 [scheduler.py:225] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=13) INFO 11-28 23:05:42 [config.py:323] Disabling cascade attention since it is not supported for hybrid models.
(APIServer pid=13) INFO 11-28 23:05:42 [config.py:439] Setting attention block size to 400 tokens to ensure that attention page size is >= mamba page size.
(APIServer pid=13) INFO 11-28 23:05:42 [config.py:463] Padding mamba page size by 1.39% to ensure that mamba page size and attention page size are exactly equal.
INFO 11-28 23:05:43 [__init__.py:225] Automatically detected platform rocm.
(EngineCore_DP0 pid=178) INFO 11-28 23:05:46 [core.py:730] Waiting for init message from front-end.
(EngineCore_DP0 pid=178) INFO 11-28 23:05:46 [core.py:97] Initializing a V1 LLM engine (v0.11.1rc2.dev141+g38f225c2a) with config: model='ibm-granite/granite-4.0-h-350m', speculative_config=None, tokenizer='ibm-granite/granite-4.0-h-350m', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=32768, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser=''), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=0, served_model_name=ibm-granite/granite-4.0-h-350m, enable_prefix_caching=False, chunked_prefill_enabled=True, pooler_config=None, compilation_config={'level': None, 'mode': 3, 'debug_dump_path': None, 'cache_dir': '', 'backend': 'inductor', 'custom_ops': ['+rms_norm', '+silu_and_mul', '+quant_fp8', 'none', '+rms_norm'], 'splitting_ops': [], 'use_inductor': None, 'compile_sizes': [], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL: 2>, 'use_cudagraph': True, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [512, 504, 496, 488, 480, 472, 464, 456, 448, 440, 432, 424, 416, 408, 400, 392, 384, 376, 368, 360, 352, 344, 336, 328, 320, 312, 304, 296, 288, 280, 272, 264, 256, 248, 240, 232, 224, 216, 208, 200, 192, 184, 176, 168, 160, 152, 144, 136, 128, 120, 112, 104, 96, 88, 80, 72, 64, 56, 48, 40, 32, 24, 16, 8, 4, 2, 1], 'cudagraph_copy_inputs': False, 'full_cuda_graph': True, 'use_inductor_graph_partition': False, 'pass_config': {}, 'max_capture_size': 512, 'local_cache_dir': None}
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
(EngineCore_DP0 pid=178) INFO 11-28 23:05:47 [parallel_state.py:1325] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, TP rank 0, EP rank 0
Memory access fault by GPU node-1 (Agent handle: 0x43578c10) on address 0x7f58f8001000. Reason: Page not present or supervisor privilege.
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Same observations on Debian 13. 

---

## 评论 (52 条)

### 评论 #1 — ianbmacdonald (2025-12-02T20:25:13Z)

And just like that, looks like it was reverted https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/commit/?id=c092c7487eb7c3d58697f490ff605bc38f4cc947

---

### 评论 #2 — huyndao (2025-12-03T01:41:09Z)

Hello, I'm running into the same page fault, using the latest commit, post the above reversion, `68517135613717f550f8eb8170656d98a9929ab3` from upstream linux-firmware repo.  OS is Debian, upstream kernel 6.18.0.


# dmesg 

```shell
root@null:~# dmesg | grep -i amdgpu
[    4.042962] amdgpu 0000:63:00.0: amdgpu: [drm] Optional firmware "amdgpu/isp_4_1_0.bin" was not found
[    4.043665] amdgpu 0000:63:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x09003500
[    4.043822] amdgpu 0000:63:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 27

[  593.942278] amdgpu 0000:63:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32803)
[  593.942302] amdgpu 0000:63:00.0: amdgpu:  Process ipython pid 5923 thread ipython pid 5923
[  593.942308] amdgpu 0000:63:00.0: amdgpu:   in page starting at address 0x00007fc56129d000 from client 10
```

# what I ran

```python
import torch
if torch.cuda.is_available():
     x = torch.rand(1000, 1000).cuda()
     y = torch.rand(1000, 1000).cuda()
     z = torch.mm(x, y)
     print("GPU computation successful!")
elif torch.version.hip:
     x = torch.rand(1000, 1000).to("cuda")
     y = torch.rand(1000, 1000).to("cuda")
     z = torch.mm(x, y)
     print("ROCm GPU computation successful!")
else:
     print("Running on CPU only.")
```

## torch version

```python
import torch

In [2]: torch.cuda.is_available()
Out[2]: True

In [3]: torch.version.hip
Out[3]: '7.1.25424'
```

# rocminfo

```shell

[37mROCk module is loaded[0m
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
  Name:                    AMD Ryzen AI 9 HX 370 w/ Radeon 890M
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen AI 9 HX 370 w/ Radeon 890M
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
  Max Clock Freq. (MHz):   5157                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    24221800(0x1719868) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24221800(0x1719868) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24221800(0x1719868) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24221800(0x1719868) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1150                            
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
  Chip ID:                 5390(0x150e)                       
  ASIC Revision:           4(0x4)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   25344                              
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
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
      Size:                    12110900(0xb8cc34) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    12110900(0xb8cc34) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1150         
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
      Size:                    24221800(0x1719868) KB             
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
      Size:                    24221800(0x1719868) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             
```

# dpkg

```shell
root@null:~# dpkg -l | grep amdgpu
ii  amdgpu-core                                        1:7.1.70101-2255337.24.04                 all          Core meta package for unified amdgpu driver.
ii  amdgpu-install                                     30.20.1.0.30200100-2255209.24.04          all          AMDGPU driver repository and installer
ii  amdgpu-lib                                         1:7.1.70101-2255337.24.04                 amd64        Meta package to install amdgpu userspace components.
ii  amdgpu-multimedia                                  1:7.1.70101-2255337.24.04                 amd64        Meta package to install mesa multimedia components.
ii  libdrm-amdgpu-amdgpu1:amd64                        1:2.4.125.70101-2255337.24.04             amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm-amdgpu-common                               1.0.0.70101-2255337.24.04                 all          List of AMD/ATI cards' device IDs, revision IDs and marketing names
ii  libdrm-amdgpu-dev:amd64                            1:2.4.125.70101-2255337.24.04             amd64        Userspace interface to kernel DRM services -- development files
ii  libdrm-amdgpu-radeon1:amd64                        1:2.4.125.70101-2255337.24.04             amd64        Userspace interface to radeon-specific kernel DRM services -- runtime
ii  libdrm-amdgpu1:amd64                               2.4.129-1                                 amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm2-amdgpu:amd64                               1:2.4.125.70101-2255337.24.04             amd64        Userspace interface to kernel DRM services -- runtime
ii  libegl1-amdgpu-mesa:amd64                          1:25.3.0.70101-2255337.24.04              amd64        free implementation of the EGL API -- Mesa vendor library
ii  libegl1-amdgpu-mesa-drivers:amd64                  1:25.3.0.70101-2255337.24.04              amd64        free implementation of the EGL API -- hardware drivers
ii  libgbm1-amdgpu:amd64                               1:25.3.0.70101-2255337.24.04              amd64        generic buffer management API -- runtime
ii  libgl1-amdgpu-mesa-dri:amd64                       1:25.3.0.70101-2255337.24.04              amd64        free implementation of the OpenGL API -- DRI modules
ii  libgl1-amdgpu-mesa-glx:amd64                       1:25.3.0.70101-2255337.24.04              amd64        free implementation of the OpenGL API -- GLX runtime
ii  libllvm20.1-amdgpu:amd64                           1:20.1.70101-2255337.24.04                amd64        Modular compiler and toolchain technologies, runtime library
ii  mesa-amdgpu-libgallium:amd64                       1:25.3.0.70101-2255337.24.04              amd64        shared infrastructure for Mesa drivers
ii  mesa-amdgpu-va-drivers:amd64                       1:25.3.0.70101-2255337.24.04              amd64        Mesa VA-API video acceleration drivers
ii  xserver-xorg-video-amdgpu                          25.0.0-1                                  amd64        X.Org X server -- AMDGPU display driver
```


---

### 评论 #3 — ghost (2025-12-03T16:24:40Z)

I was able to get MES 0x83 to work with gfx 1151 under Ubuntu 24.04 by compiling a 6.16.0 kernel from the amdgpu source (rocm-7.1.1 tag). 
(see https://github.com/ROCm/amdgpu/issues/201.)   Maybe the solution is to release a new linux-image-eom-24.04 kernel?  

---

### 评论 #4 — huyndao (2025-12-03T22:09:53Z)

Looks like this has been addressed for gfx 1150 and 1151, see:

https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/commit/?id=a0f0e52138e5f77fb0f358ff952447623ae0a7c4

https://gitlab.freedesktop.org/drm/amd/-/issues/4751

I can confirm that it's working with my setup (referenced in previous comment above).


---

### 评论 #5 — ianbmacdonald (2025-12-04T17:21:10Z)

> I was able to get MES 0x83 to work with gfx 1151 under Ubuntu 24.04 by compiling a 6.16.0 kernel from the amdgpu source (rocm-7.1.1 tag). (see [ROCm/amdgpu#201](https://github.com/ROCm/amdgpu/issues/201).) Maybe the solution is to release a new linux-image-eom-24.04 kernel?

It works for many scenarios, except the ones that fault.  Are you saying you tested the use case described in the issue?  My testing included a variety of kernels from 6.12 through 6.18, some packaged, some built locally with the upstream cwsr fixes.  At 6.16, you can use in-kernel or amdgpu-dkms .. I didn't see a change with any of these permutations. 

---

### 评论 #6 — ianbmacdonald (2025-12-04T17:22:00Z)

> Hello, I'm running into the same page fault, using the latest commit, post the above reversion, `68517135613717f550f8eb8170656d98a9929ab3` from upstream linux-firmware repo. OS is Debian, upstream kernel 6.18.0.

There is no commit post reversion :) .. the reversion is the latest, back to MES 0x80 :)

---

### 评论 #7 — huyndao (2025-12-04T20:12:00Z)

> > Hello, I'm running into the same page fault, using the latest commit, post the above reversion, `68517135613717f550f8eb8170656d98a9929ab3` from upstream linux-firmware repo. OS is Debian, upstream kernel 6.18.0.
> 
> There is no commit post reversion :) .. the reversion is the latest, back to MES 0x80 :)

That comment was in response to this comment from you:

> And just like that, looks like it was reverted https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/commit/?id=c092c7487eb7c3d58697f490ff605bc38f4cc947

As can be seen from the following git log graph of linux-firmware repo: commit `6851713` is after (post) the reverted commit that you linked `c092c74`.

I used `6851713` and it had no effect on my hardware: gfx1150, which meant that `c092c74` had no effect on my hardware.  The most recent commit `a0f0e52` is what is relevant for gfx1150.

<img width="204" height="1388" alt="Image" src="https://github.com/user-attachments/assets/513d7c03-03e8-47ed-891f-5d072b218a48" />

---

### 评论 #8 — amd-nicknick (2025-12-08T09:59:07Z)

Hi @ianbmacdonald, @huyndao, the MES FW 0x83 is causing this regression you're seeing. It looks like a change introduced discrepancy between KFD and MES. I am checking the plans for a future fix.
In the meantime, please revert to MES 0x80. Thanks for reporting this issue!

---

### 评论 #9 — ianbmacdonald (2025-12-09T00:09:27Z)

> it had no effect on my hardware: gfx1150

This issue is for the Strix Halo (gfx1151), which was fixed when the firmware 0x83 was reverted back to 0x80 on 2025-12-01 04:03:22. 

@huyndao  If you are still having issues with your Strix Point, you should open another issue. 

The simplest way to determine what you are running is just to check `amdgpu_firmware_info`
```
# cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
```

---

### 评论 #10 — ndrewpj (2025-12-09T11:43:35Z)

I can confirm that the _amdgpu.cwsr_enable=0_ added to the kernel line in GRUB helped in preventing the hangs on CachyOS (Arch based) with latest linux firmware (with MES v. ... 080)


---

### 评论 #11 — jalberto (2025-12-10T13:35:57Z)

the `amdgpu.cwsr_enable=0` doesn't work with 0x83

---

### 评论 #12 — ndrewpj (2025-12-10T17:56:21Z)

> the `amdgpu.cwsr_enable=0` doesn't work with 0x83

Did you run update-grub after editing the config file?

---

### 评论 #13 — jalberto (2025-12-11T09:19:05Z)

I am on Fedora Silverblue, no need for that

---

### 评论 #14 — amd-nicknick (2025-12-11T15:39:56Z)

@jalberto, you **have to** be on MES 0x80. The `cwsr_enable` has nothing to do with the firmware issue in 0x83.

# TLDR For anyone stumbled onto this thread looking for hang/fault solution:
* If you're on MES 0x83 (Check with `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info`):
  * Rollback to MES 0x80, check the `linux-firmware` package from your distro.
  * Upstream kernel firmware **after** https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/commit/?id=3d5c8135206cef364e7d353711b3e7358a90d152
* If you're on MES 0x80
  * Try disabling CWSR: Kernel parameter `amdgpu.cwsr_enable=0`
* If you're on MES <0x80
  * Update your kernel and firmware. For Ubuntu ensure you're on the OEM kernel **without** amdgpu DKMS.

# Detail & Background Information
* MES 0x80 and onwards supports a flag `cwsr_enable`
  * The feature is called "Compute Wave Save Restore", which supports detaching compute queue on the fly to process 3D queues. The goal is to relief 3D queue even if intensive compute task is in progress, to maintain UI responsiveness.
  * If `amdgpu.cwsr_enable=0` is set, it **disables** this CWSR feature.
  * In order to "swap" the in-flight compute wave, a save space is needed to store the state for later restore. However, there is a bug where Strix Halo (gfx1151) was given a space too small to capture all context. This causes fault when the compute queue is reattached, as the state is essentially corrupted.
  * ~~Fixes are available, but requires nightlies + latest kernel~~ 
    **TheRock Nightly does not contain the fix yet. Thanks @mgehre-amd & @superm1!**
    * ~~ROCm, allocate more space for gfx1151: https://github.com/ROCm/rocm-systems/pull/1807~~ 
      **Rolled back for better fix: https://github.com/ROCm/rocm-systems/pull/2200/files**
    * ~~Kernel, relax checks for over allocation of save area: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?h=v6.18&id=d15deafab5d722afb9e2f83c5edcdef9d9d98bd1~~
      **New kernel fix: 1. https://lore.kernel.org/amd-gfx/20251205195730.1266877-1-jonathan.kim@amd.com/ 2. https://lore.kernel.org/amd-gfx/20251205184158.2261400-1-mario.limonciello@amd.com/**
* MES 0x83 introduced a regression when the queue is created.
  * This regression is unrelated to CWSR. It affects all queue created regardless of if CWSR is enabled.
  * During queue creation, the FW receives the virtual address range of the process. Previously, this was consumed from firmware as page range of 4KB. 0x83 FW changed this to consume as actual address range due to how our Windows driver supplied them. This change breaks Linux driver as KFD still supplies page range. 
  * We have rolled-back the upstream firmware & code change in internal development branch.

---

### 评论 #15 — mgehre-amd (2025-12-11T16:23:29Z)

>   * Fixes are available, but requires nightlies + latest kernel

ROCm nightly does not contain the fix, it was [reverted](https://github.com/ROCm/TheRock/blob/main/patches/amd-mainline/rocm-systems/0002-Revert-hsakmt-bump-vgpr-count-for-gfx1151-1807.patch). We are waiting for https://github.com/ROCm/rocm-systems/pull/2200 to land, and then a rocm-systems bump into TheRock, before the fix is in the nightlies. This fix will also require a newer kernel.

---

### 评论 #16 — superm1 (2025-12-11T16:32:51Z)

> This fix will also require a newer kernel.

To be transparent - these are the two patches that will be needed.

* https://lore.kernel.org/amd-gfx/20251205195730.1266877-1-jonathan.kim@amd.com/
* https://lore.kernel.org/amd-gfx/20251205184158.2261400-1-mario.limonciello@amd.com/

They should go to 6.19-rc2.


---

### 评论 #17 — jalberto (2025-12-12T09:54:32Z)

@amd-nicknick Does that means I need to downgrade every firmware in the system? (as linux-firmware contains more than just AMD ones)

---

### 评论 #18 — amd-nicknick (2025-12-12T10:12:57Z)

@jalberto, no, just MES, try updating the firmware package from your distro. 
If the latest is still not yet rolled back, you could download the firmware directly: https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amdgpu/gc_11_5_0_mes_2.bin?id=3d5c8135206cef364e7d353711b3e7358a90d152
Place the firmware in `/lib/firmware/updates/amdgpu/` with the name `gc_11_5_0_mes_2.bin`, reboot and check with `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info` to see if it's loaded. Do not forget to delete it after your distro has provided the rolled-back package.

---

### 评论 #19 — jalberto (2025-12-12T10:14:39Z)

Thanks!

On Fri, 12 Dec 2025 at 11:13, Nick Kuo ***@***.***> wrote:

> *amd-nicknick* left a comment (ROCm/ROCm#5724)
> <https://github.com/ROCm/ROCm/issues/5724#issuecomment-3645828920>
>
> @jalberto <https://github.com/jalberto>, no, just MES, try updating the
> firmware package from your distro.
> If the latest is still not yet rolled back, you could download the
> firmware directly:
> https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amdgpu/gc_11_5_0_mes_2.bin?id=3d5c8135206cef364e7d353711b3e7358a90d152
> Place the firmware in /lib/firmware/updates/amdgpu/ with the name
> gc_11_5_0_mes_2.bin, reboot and check with cat
> /sys/kernel/debug/dri/1/amdgpu_firmware_info to see if it's loaded. Do
> not forget to delete it after your distro has provided the rolled-back
> package.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5724#issuecomment-3645828920>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AAAYMV74R24FLQM2LXPYTNL4BKIMBAVCNFSM6AAAAACNQL6BBKVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTMNBVHAZDQOJSGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #20 — laichiaheng (2025-12-13T11:45:54Z)

Is Arch using the old firmware? I keep having this issue, some of the thing in comfyui only works with rocm6.5 and above.

---

### 评论 #21 — BillFleming (2025-12-16T10:14:24Z)

FYI Arch has reverted the firmware already: https://gitlab.archlinux.org/archlinux/packaging/packages/linux-firmware/-/commit/be3cd595d357a4166f5d8adff37e362882d3f12c
I have managed to trigger the "amdgpu: MES ring buffer is full" on my Framework 16 with Radeon 780M with MES 0x80, Mesa 25.3.1 and Kernel 6.18. Will come back if "amdgpu.cwsr_enable=0" and full arch update doesn't fix the problem.
Also FYI the "[PATCH] drm/amdkfd: Export the cwsr_size and ctl_stack_size to userspace" applies easily on 6.18.1 and just finished a rebuild to go on the laptop. That is the "generic patch", the other is specifically only for GFX1151.

---

### 评论 #22 — bondwell79 (2025-12-18T21:26:44Z)

Hi,

If somenone need fedora 43 script to downgrade amdgpu easy, this can help:

sudo dnf downgrade amd-gpu-firmware
sudo dnf versionlock add amd-gpu-firmware
sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
sudo dracut -f

With this I can run comfyui already.

---

### 评论 #23 — amd-nicknick (2025-12-26T03:30:09Z)

> FYI Arch has reverted the firmware already: https://gitlab.archlinux.org/archlinux/packaging/packages/linux-firmware/-/commit/be3cd595d357a4166f5d8adff37e362882d3f12c I have managed to trigger the "amdgpu: MES ring buffer is full" on my Framework 16 with Radeon 780M with MES 0x80, Mesa 25.3.1 and Kernel 6.18. Will come back if "amdgpu.cwsr_enable=0" and full arch update doesn't fix the problem. Also FYI the "[PATCH] drm/amdkfd: Export the cwsr_size and ctl_stack_size to userspace" applies easily on 6.18.1 and just finished a rebuild to go on the laptop. That is the "generic patch", the other is specifically only for GFX1151.

It would be great if you could test out the fix on your workload. Feel free to report back any defects discovered with the fix.

For anyone else stumbled onto this: The kernel change alone is not enough, you need both kfd and ROCm (hsakmt) change for it to be effective. Remember to remove `amdgpu_cwsr_enable=0`.

---

### 评论 #24 — amd-nicknick (2025-12-29T01:03:11Z)

Hi @KL1RL, for gfx1150 it was reverted by this commit: https://gitlab.com/kernel-firmware/linux-firmware/-/commit/3d5c8135206cef364e7d353711b3e7358a90d152

---

### 评论 #25 — morini3andahalf (2026-01-01T21:04:58Z)

> [@jalberto](https://github.com/jalberto), no, just MES, try updating the firmware package from your distro. If the latest is still not yet rolled back, you could download the firmware directly: https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amdgpu/gc_11_5_0_mes_2.bin?id=3d5c8135206cef364e7d353711b3e7358a90d152 Place the firmware in `/lib/firmware/updates/amdgpu/` with the name `gc_11_5_0_mes_2.bin`, reboot and check with `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info` to see if it's loaded. Do not forget to delete it after your distro has provided the rolled-back package.

I am running into this issue and have tried following this advice. I copied the firmware bin file into the location given, rebooted but still have MES 0x83. This is a Fedora 43 laptop, is there something else I need to do?

---

### 评论 #26 — amd-nicknick (2026-01-02T06:56:39Z)

Hi @morini3andahalf, for FC43, try rolling back to `amd-gpu-firmware-20251111-1.fc43` RPM package.

---

### 评论 #27 — morini3andahalf (2026-01-02T08:43:34Z)

> Hi [@morini3andahalf](https://github.com/morini3andahalf), for FC43, try rolling back to `amd-gpu-firmware-20251111-1.fc43` RPM package.

Many thanks, that worked. For the benefit of others I had to

sudo dnf install fedora-repos-archive
sudo dnf --enablerepo=updates-archive downgrade amd-gpu-firmware-20251111

I can run darktable again without it crashing on startup.

---

### 评论 #28 — bondwell79 (2026-01-03T15:44:20Z)

Does anyone know if Fedora intends to resolve this issue, or whoever is responsible for it? Because the solution should be general, not a rollback to previous versions.

---

### 评论 #29 — adamskrodzki (2026-01-04T19:47:07Z)

Under Fedora (Nobara to be exact)

this script:

````
# Downgrade ALL firmware packages to 20251021 (the version with MES 0x80)
sudo dnf downgrade \
  amd-gpu-firmware-20251021-1.fc42 \
  linux-firmware-20251021-1.fc42 \
  linux-firmware-whence-20251021-1.fc42 \
  atheros-firmware-20251021-1.fc42 \
  brcmfmac-firmware-20251021-1.fc42 \
  cirrus-audio-firmware-20251021-1.fc42 \
  intel-audio-firmware-20251021-1.fc42 \
  intel-gpu-firmware-20251021-1.fc42 \
  intel-vsc-firmware-20251021-1.fc42 \
  iwlegacy-firmware-20251021-1.fc42 \
  iwlwifi-dvm-firmware-20251021-1.fc42 \
  libertas-firmware-20251021-1.fc42 \
  mt7xxx-firmware-20251021-1.fc42 \
  nvidia-gpu-firmware-20251021-1.fc42 \
  nxpwireless-firmware-20251021-1.fc42 \
  realtek-firmware-20251021-1.fc42 \
  tiwilink-firmware-20251021-1.fc42

# Rebuild initramfs
sudo dracut -f

# Reboot
sudo reboot
````

worked for me



---

### 评论 #30 — X-Ryl669 (2026-01-08T15:51:02Z)

I've the same issue but on a gfx1152 (Krakan point) Ryzen AI 9 HX. 

I'm running on CachyOS (Arch linux based). I have the latest linux-firmware 20251125-2 package.

The firmware I have is MES 0x82 **not 0x83**:
```
$ sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x00000079
MES feature version: 1, firmware version: 0x00000082
```

I've the command line to disable CWSR:
```
$ cat /proc/cmdline
quiet zswap.enabled=0 nowatchdog splash rw root=UUID=something amdgpu.cwsr_enable=0 initrd=\initramfs-linux-cachyos.img
```

I've tried to put the given firmware earlier in the thread but either it doesn't load or it's ignored (I don't have any message about this file in dmesg). Notice that I don't have a /lib/firmware/updates, but only a /lib/firmware/ folder, so I've put the file in the amdgpu folder, **replacing** the file with the same name (after zstd compressing it, like the previous one).

```
$ sudo dmesg | grep -i amd | grep -i firm
[    3.560271] amdgpu 0000:04:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x09003500
[    3.560531] amdgpu 0000:04:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 27
```

Maybe I did something wrong?

As the side note, the [posted patch](https://github.com/ROCm/ROCm/issues/5724#issuecomment-3642759910) don't account for this gpu type, only for gfx1151 (Strix Halo), IIUC. Maybe it's missing the gfx1152 and gfx1153 GPU type too? @amd-nicknick or @mgehre-amd, can you confirm?



---

### 评论 #31 — adamskrodzki (2026-01-10T08:31:48Z)

@X-Ryl669 I'm not an expert in Linux but i fixed this problem and one line In my post (directly above) I do not see you mentioning anything about is
````
# Rebuild initramfs
sudo dracut -f
````

my understanding is that gpu firmware loads on boot and therefore needs to be "baked in" to the boot image/ram disk (that is what dracut does)

Also You may want to check in your GRUB what image do you use and what is being baked into that image.

---

### 评论 #32 — X-Ryl669 (2026-01-10T09:35:08Z)

I'm not on a Fedora distribution, so I don't have dracut. You are right, maybe I've missed the part that needs rebuilding the initramfs, but I have a doubt about the version to use. 

The loaded firmware for me is MES 0x82 (not 0x83) and I think it's linked with the fact that I have a gfx1152 (not gfx1151). If the system loaded that firmware (0x82) instead of 0x83 while the 0x83 is already in the /lib/firmware tree, it means that it's deciding that 0x83 isn't working for my setup. 

So, when I reverted the firmware to 0x80, it's likely that I've changed the wrong file (that is, the file that a gfx1151 would have use). I've no idea what firmware file to use (is it 0x79?, what's its name? Did AMD released another firmware before 0x82 for gfx1152?).

I've started another issue #5844 about this, since I'm not 100% sure the solution in this thread would work on my setup (and, in fact, on any Krakan Point system). I'm waiting for a nice fellow at AMD to answer this problem.



---

### 评论 #33 — amd-nicknick (2026-01-12T02:13:54Z)

> I've the same issue but on a gfx1152 (Krakan point) Ryzen AI 9 HX.
> 
> I'm running on CachyOS (Arch linux based). I have the latest linux-firmware 20251125-2 package.
> 
> The firmware I have is MES 0x82 **not 0x83**:
> 
> ```
> $ sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
> MES_KIQ feature version: 6, firmware version: 0x00000079
> MES feature version: 1, firmware version: 0x00000082
> ```
> 
> I've the command line to disable CWSR:
> 
> ```
> $ cat /proc/cmdline
> quiet zswap.enabled=0 nowatchdog splash rw root=UUID=something amdgpu.cwsr_enable=0 initrd=\initramfs-linux-cachyos.img
> ```
> 
> I've tried to put the given firmware earlier in the thread but either it doesn't load or it's ignored (I don't have any message about this file in dmesg). Notice that I don't have a /lib/firmware/updates, but only a /lib/firmware/ folder, so I've put the file in the amdgpu folder, **replacing** the file with the same name (after zstd compressing it, like the previous one).
> 
> ```
> $ sudo dmesg | grep -i amd | grep -i firm
> [    3.560271] amdgpu 0000:04:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x09003500
> [    3.560531] amdgpu 0000:04:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 27
> ```
> 
> Maybe I did something wrong?
> 
> As the side note, the [posted patch](https://github.com/ROCm/ROCm/issues/5724#issuecomment-3642759910) don't account for this gpu type, only for gfx1151 (Strix Halo), IIUC. Maybe it's missing the gfx1152 and gfx1153 GPU type too? [@amd-nicknick](https://github.com/amd-nicknick) or [@mgehre-amd](https://github.com/mgehre-amd), can you confirm?

FW 0x82 is not affected by this issue, in other words, the failure is only introduced after FW 0x83.
If anyone is seeing failures with FW != 0x83, please raise a new issue. Thanks!

---

### 评论 #34 — AnhNhan (2026-01-13T09:44:28Z)

Update: Comment is moot, see below. `linux-firmware-20260110-1` works!

Original:

~~I have tested `linux-firmware-20260110-1.fc43` that is available for Fedora 43 in the testing branch.~~

~~MES version is still `0x83` and I could still reproduce this issue (with kernel version `6.18.4-200.fc43.x86_64`), so not fixed yet!~~

~~I advise anyone encountering this issue to stay downgraded to `linux-firmware-20251111-1` with the `amdgpu.cwsr_enable=0` kargs.~~

---

### 评论 #35 — morini3andahalf (2026-01-13T11:12:35Z)

> I have tested `linux-firmware-20260110-1.fc43` that is available for Fedora 43 in the testing branch.
> 
> MES version is still `0x83` and I could still reproduce this issue (with kernel version `6.18.4-200.fc43.x86_64`), so not fixed yet!
> 
> I advise anyone encountering this issue to stay downgraded to `linux-firmware-20251111-1` with the `amdgpu.cwsr_enable=0` kargs.

That is disappointing. Running on the downgraded firmware with recent kernels gives  "RDSEED32 is broken" in dmesg. Do the fedora devs know about this? I guess https://bugzilla.redhat.com/show_bug.cgi?id=2420062 would be the correct place to mention it but I don't have an account.

---

### 评论 #36 — superm1 (2026-01-13T12:23:13Z)

The F/W package in Fedora definitely has the expected reverts now.  Did you make sure that you've rebuilt your initramfs after changing packages?

---

### 评论 #37 — AnhNhan (2026-01-13T12:43:00Z)

This is embarassing! I had assumed Fedora Silverblue did this automatically. Looks like I can regenerate it explicitly.

```sh
$ rpm-ostree initramfs --enable -r
$ rpm-ostree kargs --delete=amdgpu.cwsr_enable=0
```

I have also disabled the `amdgpu.cwsr_enable=0` kernel argument.

And ComfyUI works! Thanks for the heads up. My notice above is moot, I have updated it.

---

### 评论 #38 — amd-nicknick (2026-01-15T09:55:42Z)

Hi all, the FW rollback should be present in all major distros now `20260110-1` package. If you had previously manually replaced the firmware or rollback + pinned the package, please try removing the pin and upgrade the firmware package. 

---

### 评论 #39 — ianbmacdonald (2026-01-29T20:08:10Z)

Not sure why somebody decided to close this bug without any comment or reproduction;  Looks like it is still present on Ubuntu 24.04 running the current ROCm/AMDGPU stack on the leading edge OEM kernels without the cwsr workaround. 

Anyways, for anyone still tracking this issue on the Strix Halo, using the supported Ubuntu 24.04 pattern, some details follow on current state without any workaround.   The 0x83 firmware is shipping now with `amdgpu-dkms-firmware`;  I have not confirmed all the required patches are backported and in place with Ubuntu kernels, but I am seeing the same on my Debian 13 box with packaged 6.19~rc6-1~exp1 which should have everything merged from 6.18.4 where the above mentioned patches were applied. 

I am guessing VPGR is still absent https://github.com/ROCm/TheRock/issues/2991#issuecomment-3768808325

```bash
imac@ai2:~$ uname -a
Linux ai2 6.17.0-1009-oem #9-Ubuntu SMP PREEMPT_DYNAMIC Thu Dec 18 05:48:19 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
imac@ai2:~$ sudo dmesg | head -5
[    0.000000] Linux version 6.17.0-1009-oem (buildd@lcy02-amd64-099) (x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, GNU ld (GNU Binutils for Ubuntu) 2.42) #9-Ubuntu SMP PREEMPT_DYNAMIC Thu Dec 18 05:48:19 UTC 2025 (Ubuntu 6.17.0-1009.9-oem 6.17.2)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.17.0-1009-oem root=UUID=2e992352-6f78-4f9b-aa68-1b771d43e2b0 ro transparent_hugepage=always numa_balancing=disable ttm.pages_limit=32768000 ttm.page_pool_size=32768000 amdttm.pages_limit=32768000 amdttm.page_pool_size=32768000
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
imac@ai2:~$ dpkg -l | grep linux-oem-24.04d
ii  linux-oem-24.04d                     6.17.0-1009.9                           amd64        Complete OEM Linux kernel and headers
imac@ai2:~$ dpkg -l | grep amdgpu-dkms-firmware
ii  amdgpu-dkms-firmware                 30.30.0.0.30300000-2278356.24.04        all          firmware blobs used by amdgpu driver in DKMS format
imac@ai2:~$ sudo dkms status | grep amdgpu
amdgpu/6.16.13-2278356.24.04, 6.17.0-1009-oem, x86_64: installed
imac@ai2:~$ sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000083
imac@ai2:~$ sudo dmesg | grep amdgpu | grep memory
[    3.634911] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 512M of VRAM memory ready
[    3.634913] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 128000M of GTT memory ready.
imac@ai2:~$ sudo amd-smi
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.1+fc0010cf6a    amdgpu version: 6.16.13  ROCm version: 7.2.0    |
| VBIOS version: 00107962                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0    AMD Radeon Graphics | N/A        N/A   0                 N/A |
|   0       0     N/A             N/A | N/A        N/A              147/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+

```

Updated reproduction with the latest ROCM 7.2 vllm 0.15 builds from AMD to match the ROCM 7.2 AMDGPU 30.30 which ships MES 0x83 for Strix Halo (11.5.1)

Pull the image, run it linked to your local HF cache, launch the mamba MoE model

`docker pull rocm/vllm-dev:prerelease_72_releases_v0.15.0_20260129`

```bash
 docker run -it \
    --network host \
    --ipc host \
    --privileged \
    --cap-add=CAP_SYS_ADMIN \
    --cap-add=SYS_PTRACE \
    --device=/dev/kfd \
    --device=/dev/dri \
    --device=/dev/mem \
    --security-opt seccomp=unconfined \
    --shm-size 4G \
    -e TERM=xterm-256color \
    -v /mnt/models/huggingface/:/root/.cache/huggingface/ \
    --name vllm-strixhalo-mes-cwsr \
    rocm/vllm-dev:prerelease_72_releases_v0.15.0_20260129
```

```bash
root@ai2:/app# vllm serve ibm-granite/granite-4.0-h-350m
(APIServer pid=83) INFO 01-29 19:47:16 [utils.py:325] 
(APIServer pid=83) INFO 01-29 19:47:16 [utils.py:325]        █     █     █▄   ▄█
(APIServer pid=83) INFO 01-29 19:47:16 [utils.py:325]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.15.0rc3
(APIServer pid=83) INFO 01-29 19:47:16 [utils.py:325]   █▄█▀ █     █     █     █  model   ibm-granite/granite-4.0-h-350m
(APIServer pid=83) INFO 01-29 19:47:16 [utils.py:325]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=83) INFO 01-29 19:47:16 [utils.py:325] 
(APIServer pid=83) INFO 01-29 19:47:16 [utils.py:261] non-default args: {'model_tag': 'ibm-granite/granite-4.0-h-350m', 'api_server_count': 1, 'model': 'ibm-granite/granite-4.0-h-350m'}
(APIServer pid=83) INFO 01-29 19:47:22 [model.py:541] Resolved architecture: GraniteMoeHybridForCausalLM
(APIServer pid=83) INFO 01-29 19:47:22 [model.py:1561] Using max model len 32768
(APIServer pid=83) INFO 01-29 19:47:23 [scheduler.py:226] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=83) INFO 01-29 19:47:23 [config.py:504] Setting attention block size to 400 tokens to ensure that attention page size is >= mamba page size.
(APIServer pid=83) INFO 01-29 19:47:23 [config.py:535] Padding mamba page size by 1.39% to ensure that mamba page size and attention page size are exactly equal.
(APIServer pid=83) INFO 01-29 19:47:23 [vllm.py:624] Asynchronous scheduling is enabled.
(EngineCore_DP0 pid=196) INFO 01-29 19:47:28 [core.py:96] Initializing a V1 LLM engine (v0.15.0rc3) with config: model='ibm-granite/granite-4.0-h-350m', speculative_config=None, tokenizer='ibm-granite/granite-4.0-h-350m', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=32768, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=ibm-granite/granite-4.0-h-350m, enable_prefix_caching=False, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none', '+sparse_attn_indexer'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_split_points': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'eliminate_noops': True, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 512, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': True}, 'local_cache_dir': None}
(EngineCore_DP0 pid=196) INFO 01-29 19:47:28 [parallel_state.py:1212] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://192.168.79.18:48943 backend=nccl
(EngineCore_DP0 pid=196) INFO 01-29 19:47:28 [parallel_state.py:1423] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A
Memory access fault by GPU node-1 (Agent handle: 0x4511c7f0) on address 0x7beb01001000. Reason: Page not present or supervisor privilege.
```

```
[ 1200.356630] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32771)
[ 1200.356652] amdgpu 0000:c5:00.0: amdgpu:  Process python pid 2792 thread python pid 2792
[ 1200.356657] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007beb01001000 from client 10
[ 1200.356662] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[ 1200.356666] amdgpu 0000:c5:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPF (0x4)
[ 1200.356668] amdgpu 0000:c5:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[ 1200.356671] amdgpu 0000:c5:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[ 1200.356673] amdgpu 0000:c5:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[ 1200.356675] amdgpu 0000:c5:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[ 1200.356677] amdgpu 0000:c5:00.0: amdgpu: 	 RW: 0x0
```

---

### 评论 #40 — ianbmacdonald (2026-01-29T21:52:04Z)

So the VPGR patch is in, so looks like it isn't that.  Maybe @amd-nicknick knows, as he did close this issue.

```bash
root@ai2:/usr/local/src# cd /usr/local/src/linux-oem-6.17-6.17.0

# show the exact line(s) that prove the patch
grep -nE 'gfxv == 110501|GFX_VERSION_GFX1151' \
  drivers/gpu/drm/amd/amdkfd/kfd_queue.c || echo "NOT FOUND"

# show the whole conditional block around it (for context)
grep -nE 'kfd_get_vgpr_size_per_cu|vgpr_size|110501|110000|120000' \
  drivers/gpu/drm/amd/amdkfd/kfd_queue.c
412:		 gfxv == 110501 ||		/* GFX_VERSION_GFX1151 */
401:static u32 kfd_get_vgpr_size_per_cu(u32 gfxv)
403:	u32 vgpr_size = 0x40000;
409:		vgpr_size = 0x80000;
410:	else if (gfxv == 110000 ||		/* GFX_VERSION_PLUM_BONITO */
412:		 gfxv == 110501 ||		/* GFX_VERSION_GFX1151 */
413:		 gfxv == 120000 ||		/* GFX_VERSION_GFX1200 */
415:		vgpr_size = 0x60000;
417:	return vgpr_size;
421:	(kfd_get_vgpr_size_per_cu(gfxv) + SGPR_SIZE_PER_CU +\
root@ai2:/usr/local/src/linux-oem-6.17-6.17.0# 
```

---

### 评论 #41 — ianbmacdonald (2026-01-29T23:54:45Z)

The new workaround is pretty straightforward; No need for the `cwsr_enable=0` kernel flag, that seems to be resolved in the current amdgpu / kernel / rocm stack, independent of the buggy firmware.  Just remove amdgpu-dkms-firmware; This purges the new 0x83 firmware, falling back on linux-firmware from noble, which at the time of this post contains 0x80. 

6.17+ ship with amdgpu, so no need for the dkms module either. 

```bash
root@ai2:~# apt remove amdgpu-dkms-firmware amdgpu-dkms
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  dkms dwarves linux-headers-6.8.0-90 linux-headers-6.8.0-90-generic linux-image-6.8.0-90-generic linux-modules-6.8.0-90-generic linux-modules-extra-6.8.0-90-generic linux-tools-6.8.0-90 linux-tools-6.8.0-90-generic pahole
Use 'apt autoremove' to remove them.
The following packages will be REMOVED:
  amdgpu-dkms* amdgpu-dkms-firmware*
0 upgraded, 0 newly installed, 2 to remove and 24 not upgraded.
After this operation, 632 MB disk space will be freed.
Do you want to continue? [Y/n] 
(Reading database ... 270527 files and directories currently installed.)
Removing amdgpu-dkms (1:6.16.13.30300000-2278356.24.04) ...
Module amdgpu-6.16.13-2278356.24.04 for kernel 6.8.0-94-generic (x86_64).
Before uninstall, this module version was ACTIVE on this kernel.
...
reboot
```
```bash
root@ai2:~# cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
root@ai2:~# uname -a
Linux ai2 6.17.0-1010-oem #10-Ubuntu SMP PREEMPT_DYNAMIC Thu Jan 15 03:39:57 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
root@ai2:~# dpkg -l | grep linux-firmware
ii  linux-firmware                       20240318.git3b128b60-0ubuntu2.23        amd64        Firmware for Linux kernel drivers
root@ai2:~# dmesg | head -5
[    0.000000] Linux version 6.17.0-1010-oem (buildd@lcy02-amd64-028) (x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, GNU ld (GNU Binutils for Ubuntu) 2.42) #10-Ubuntu SMP PREEMPT_DYNAMIC Thu Jan 15 03:39:57 UTC 2026 (Ubuntu 6.17.0-1010.10-oem 6.17.2)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.17.0-1010-oem root=UUID=2e992352-6f78-4f9b-aa68-1b771d43e2b0 ro transparent_hugepage=always numa_balancing=disable ttm.pages_limit=32768000 ttm.page_pool_size=32768000 amdttm.pages_limit=32768000 amdttm.page_pool_size=32768000
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
root@ai2:~# docker ps -a
CONTAINER ID   IMAGE                                                   COMMAND       CREATED          STATUS                      PORTS     NAMES
88951e5b7e28   rocm/vllm-dev:prerelease_72_releases_v0.15.0_20260129   "/bin/bash"   48 minutes ago   Exited (1) 47 minutes ago             vllm-strixhalo-mes-cwsr
root@ai2:~# docker start -ai 88951e5b7e28
root@ai2:/app# vllm serve ibm-granite/granite-4.0-h-350m
(APIServer pid=13) INFO 01-29 23:48:46 [utils.py:325] 
(APIServer pid=13) INFO 01-29 23:48:46 [utils.py:325]        █     █     █▄   ▄█
(APIServer pid=13) INFO 01-29 23:48:46 [utils.py:325]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.15.0rc3
(APIServer pid=13) INFO 01-29 23:48:46 [utils.py:325]   █▄█▀ █     █     █     █  model   ibm-granite/granite-4.0-h-350m
(APIServer pid=13) INFO 01-29 23:48:46 [utils.py:325]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=13) INFO 01-29 23:48:46 [utils.py:325] 
(APIServer pid=13) INFO 01-29 23:48:46 [utils.py:261] non-default args: {'model_tag': 'ibm-granite/granite-4.0-h-350m', 'api_server_count': 1, 'model': 'ibm-granite/granite-4.0-h-350m'}
(APIServer pid=13) INFO 01-29 23:48:46 [model.py:541] Resolved architecture: GraniteMoeHybridForCausalLM
(APIServer pid=13) INFO 01-29 23:48:46 [model.py:1561] Using max model len 32768
(APIServer pid=13) INFO 01-29 23:48:46 [scheduler.py:226] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=13) INFO 01-29 23:48:46 [config.py:504] Setting attention block size to 400 tokens to ensure that attention page size is >= mamba page size.
(APIServer pid=13) INFO 01-29 23:48:46 [config.py:535] Padding mamba page size by 1.39% to ensure that mamba page size and attention page size are exactly equal.
(APIServer pid=13) INFO 01-29 23:48:46 [vllm.py:624] Asynchronous scheduling is enabled.
(EngineCore_DP0 pid=90) INFO 01-29 23:48:51 [core.py:96] Initializing a V1 LLM engine (v0.15.0rc3) with config: model='ibm-granite/granite-4.0-h-350m', speculative_config=None, tokenizer='ibm-granite/granite-4.0-h-350m', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=32768, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=ibm-granite/granite-4.0-h-350m, enable_prefix_caching=False, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none', '+sparse_attn_indexer'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_split_points': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'eliminate_noops': True, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 512, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': True}, 'local_cache_dir': None}
(EngineCore_DP0 pid=90) INFO 01-29 23:48:51 [parallel_state.py:1212] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://192.168.79.18:47243 backend=nccl
(EngineCore_DP0 pid=90) INFO 01-29 23:48:51 [parallel_state.py:1423] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A
(EngineCore_DP0 pid=90) INFO 01-29 23:48:52 [gpu_model_runner.py:4021] Starting to load model ibm-granite/granite-4.0-h-350m...
(EngineCore_DP0 pid=90) INFO 01-29 23:48:52 [rocm.py:338] Using Triton Attention backend.
(EngineCore_DP0 pid=90) WARNING 01-29 23:48:53 [compilation.py:1047] Op 'sparse_attn_indexer' not present in model, enabling with '+sparse_attn_indexer' has no effect
(EngineCore_DP0 pid=90) INFO 01-29 23:48:53 [weight_utils.py:567] No model.safetensors.index.json found in remote.
Loading safetensors checkpoint shards:   0% Completed | 0/1 [00:00<?, ?it/s]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:00<00:00,  1.29it/s]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:00<00:00,  1.29it/s]
(EngineCore_DP0 pid=90) 
(EngineCore_DP0 pid=90) INFO 01-29 23:48:54 [default_loader.py:291] Loading weights took 0.80 seconds
(EngineCore_DP0 pid=90) INFO 01-29 23:48:54 [gpu_model_runner.py:4118] Model loading took 0.84 GiB memory and 1.169840 seconds
(EngineCore_DP0 pid=90) INFO 01-29 23:48:57 [backends.py:805] Using cache directory: /root/.cache/vllm/torch_compile_cache/7c429e2847/rank_0_0/backbone for vLLM's torch.compile
(EngineCore_DP0 pid=90) INFO 01-29 23:48:57 [backends.py:865] Dynamo bytecode transform time: 2.94 s
(EngineCore_DP0 pid=90) INFO 01-29 23:49:00 [backends.py:302] Cache the graph of compile range (1, 8192) for later use
(EngineCore_DP0 pid=90) INFO 01-29 23:49:21 [backends.py:319] Compiling a graph for compile range (1, 8192) takes 21.67 s
(EngineCore_DP0 pid=90) INFO 01-29 23:49:21 [monitor.py:34] torch.compile takes 24.61 s in total
(EngineCore_DP0 pid=90) INFO 01-29 23:49:23 [gpu_worker.py:356] Available KV cache memory: 107.5 GiB
(EngineCore_DP0 pid=90) INFO 01-29 23:49:23 [kv_cache_utils.py:1307] GPU KV cache size: 3,522,400 tokens
(EngineCore_DP0 pid=90) INFO 01-29 23:49:23 [kv_cache_utils.py:1312] Maximum concurrency for 32,768 tokens per request: 791.58x
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 51/51 [00:01<00:00, 40.59it/s]
Capturing CUDA graphs (decode, FULL): 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 51/51 [00:04<00:00, 11.19it/s]
(EngineCore_DP0 pid=90) INFO 01-29 23:49:34 [gpu_model_runner.py:5051] Graph capturing finished in 7 secs, took 0.33 GiB
(EngineCore_DP0 pid=90) INFO 01-29 23:49:34 [core.py:272] init engine (profile, create kv cache, warmup model) took 40.11 seconds
(EngineCore_DP0 pid=90) INFO 01-29 23:49:35 [vllm.py:624] Asynchronous scheduling is enabled.
(APIServer pid=13) INFO 01-29 23:49:36 [api_server.py:665] Supported tasks: ['generate']
(APIServer pid=13) INFO 01-29 23:49:36 [serving.py:177] Warming up chat template processing...
(APIServer pid=13) INFO 01-29 23:49:36 [hf.py:310] Detected the chat template content format to be 'openai'. You can set `--chat-template-content-format` to override this.
(APIServer pid=13) INFO 01-29 23:49:36 [serving.py:212] Chat template warmup completed in 592.5ms
(APIServer pid=13) INFO 01-29 23:49:36 [api_server.py:946] Starting vLLM API server 0 on http://0.0.0.0:8000
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:38] Available routes are:
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /openapi.json, Methods: HEAD, GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /docs, Methods: HEAD, GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /docs/oauth2-redirect, Methods: HEAD, GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /redoc, Methods: HEAD, GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /scale_elastic_ep, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /is_scaling_elastic_ep, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /tokenize, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /detokenize, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /pause, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /resume, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /is_paused, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /metrics, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /health, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/chat/completions, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/chat/completions/render, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/responses, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/responses/{response_id}, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/responses/{response_id}/cancel, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/audio/transcriptions, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/audio/translations, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/completions, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/completions/render, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/messages, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/models, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /load, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /version, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /ping, Methods: GET
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /ping, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /invocations, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /classify, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/embeddings, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /score, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/score, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /rerank, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v1/rerank, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /v2/rerank, Methods: POST
(APIServer pid=13) INFO 01-29 23:49:36 [launcher.py:46] Route: /pooling, Methods: POST
(APIServer pid=13) INFO:     Started server process [13]
(APIServer pid=13) INFO:     Waiting for application startup.
(APIServer pid=13) INFO:     Application startup complete.


---

### 评论 #42 — amd-nicknick (2026-01-30T05:34:31Z)

@ianbmacdonald you shouldn't be on amdgpu packages with Strix Halo. You should use in-tree driver & firmware.
I closed the issue as all major distros have rolled back the 0x83 FW release.

The FW 0x83 problem really doesn't have anything to do with the VGPR or CWSR. For that, the latest ROCm + RC kernel (6.19 RC1) will resolve that, when the kernel is available, the `cwsr_enable=0` workaround could be removed.

---

### 评论 #43 — ianbmacdonald (2026-01-31T16:38:20Z)

I don't use amdgpu; Just here to match the typical patterm for the graphics,rocm flags on the scripted package wrapper that does pull amdgpu.   I am curious  if you are saying 0x83 is legit for furture kernels, or is a *problem*.

FW 0x83 actually appears upstream in in-tree firmware for the distros as well.   My testing on packaged 6.19~rc6-1 (https://packages.debian.org/experimental/linux-source-6.19) indicates no resolution for this fault when paired with the matching upstream 0x83 firmware .. @amd-nicknick is that what you are suggesting FW 0x83 works with >6.19 rc1?



---

### 评论 #44 — amd-nicknick (2026-02-01T09:41:47Z)

No, FW 0x83 will not work with any kernel.
The whole problem with the 0x83 FW was due to a fix targeting Windows driver, the corresponding change never made it to amdgpu. We later found the fix was not optimal anyway and reverted, but during that period, 0x83 got released on kernel-firmware.

Do you have the `firmware-amd-graphics` package installed? I'm guessing you either have incorrect firmware package installed (From our dkms pkg maybe?), or the FW is embedded by Debian during build. 
Check if files `/usr/lib/firmware/amdgpu/gc_11_5_1*.bin` exist, if they do, find out who supplied them by `dpkg -S`.
The firmware is also likely included in the initramfs, so you might need to regenerate that. On Debian do `update-initramfs -u`

For all Debian suite, the package should contain the correct FW. https://packages.debian.org/search?lang=en&keywords=firmware-amd-graphics
Let me know if I misunderstood you, I can reopen this if there is somewhere I missed still carry the 0x83 FW.

---

### 评论 #45 — zw963 (2026-02-03T13:33:30Z)

Hello, I am trying to run ComfyUI use 6.18.8 kernal with rOCm 7.2.0 use 780M, but still system crash (iGpu reset) and force login out if remove `amdgpu.cwsr_enable=0` 

```
 ╰──➤ $ uname -a
Linux mingfan 6.18.8-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Sat, 31 Jan 2026 05:51:47 +0000 x86_64 GNU/Linux
```

```
 ╰──➤ $ \cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap sysrq_always_enabled=1 amdgpu.gpu_recovery=1 amdgpu.gttsize=24576 ttm.pages_limit=6291456 initrd=\boot\initramfs-linux-xanmod.img
```

Following is the dmesg broken log:

```
[  292.487846] userif-5: sent link down event.
[  292.487856] userif-5: sent link up event.
[  950.818166] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  950.818171] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1802
[  950.818174] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  950.818177] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[  950.818179] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[  950.818199] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[  950.818212] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 5
[  950.818215] amdgpu: Failed to suspend process pid 14368
[  950.818218] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 64667
[  950.818245] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[  950.820337] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[  952.916113] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  952.916120] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[  953.391196] amdgpu: Freeing queue vital buffer 0x7f2e70800000, queue evicted
[  953.391202] amdgpu: Freeing queue vital buffer 0x7f2e9da00000, queue evicted
[  953.391204] amdgpu: Freeing queue vital buffer 0x7f340c400000, queue evicted
[  953.391207] amdgpu: Freeing queue vital buffer 0x7f340fa00000, queue evicted
[  953.391209] amdgpu: Freeing queue vital buffer 0x7f3414400000, queue evicted
[  954.920081] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  954.920088] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[  956.924070] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  956.924077] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[  957.131282] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[  957.132772] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[  957.165393] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[  957.166061] [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
[  957.166190] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[  957.166192] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[  957.166195] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[  957.167841] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[  957.173995] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[  957.296277] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  957.296286] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  957.296288] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  957.296290] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  957.296291] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  957.296293] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  957.296294] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  957.296295] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  957.296297] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  957.296300] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  957.296301] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  957.296303] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[  957.296305] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  957.298461] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[  957.298474] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[  958.892620] rfkill: input handler enabled
[  959.357038] userif-5: sent link down event.
[  959.357044] userif-5: sent link up event.
[  961.343114] amdgpu: Freeing queue vital buffer 0x7f4e7ca00000, queue evicted
[  961.343128] amdgpu: Freeing queue vital buffer 0x7f4ec8600000, queue evicted
[  961.343133] amdgpu: Freeing queue vital buffer 0x7f4f03600000, queue evicted
[  961.343135] amdgpu: Freeing queue vital buffer 0x7f4f04400000, queue evicted
[  961.480700] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  961.480930] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1800
[  961.481136] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  961.481177] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[  961.481200] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[  961.481201] amdgpu: Resetting wave fronts (cpsch) on dev 000000000ff73c32
[  961.481203] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[  961.481250] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[  961.484928] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[  961.583988] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[  961.617548] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[  961.618214] [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
```

Following is new installed rocm related package version:


```
composable-kernel-7.2.0-1-x86_64 1557.0 MiB 16.6 MiB/s 01:34 [###########################################] 100%
hipblaslt-7.2.0-1-x86_64 1525.6 MiB 12.7 MiB/s 02:01 [###########################################] 100%
rocm-llvm-2:7.2.0-1-x86_64 956.8 MiB 14.0 MiB/s 01:08 [###########################################] 100%
rocsolver-7.2.0-1-x86_64 690.6 MiB 17.9 MiB/s 00:39 [###########################################] 100%
rccl-7.2.0-1-x86_64 423.2 MiB 18.8 MiB/s 00:22 [###########################################] 100%
rocblas-7.2.0-1-x86_64 331.3 MiB 16.7 MiB/s 00:20 [###########################################] 100%
miopen-hip-7.2.0-1-x86_64 251.1 MiB 17.2 MiB/s 00:15 [###########################################] 100%
rocfft-7.2.0-1-x86_64 120.8 MiB 17.4 MiB/s 00:07 [###########################################] 100%
rocsparse-7.2.0-1-x86_64 72.1 MiB 16.2 MiB/s 00:04 [###########################################] 100%
comgr-2:7.2.0-1-x86_64 42.1 MiB 16.5 MiB/s 00:03 [###########################################] 100%
hipsparselt-7.2.0-1-x86_64 41.6 MiB 18.5 MiB/s 00:02 [###########################################] 100%
rocrand-7.2.0-1-x86_64 22.5 MiB 15.9 MiB/s 00:01 [###########################################] 100%
rocalution-7.2.0-1-x86_64 8.3 MiB 19.2 MiB/s 00:00 [###########################################] 100%
hip-runtime-amd-7.2.0-1-x86_64 7.3 MiB 20.1 MiB/s 00:00 [###########################################] 100%
rocm-smi-lib-7.2.0-1-x86_64 1052.3 KiB 1253 KiB/s 00:01 [###########################################] 100%
hsa-rocr-7.2.0-1-x86_64 856.7 KiB 1727 KiB/s 00:00 [###########################################] 100%
rocm-opencl-runtime-7.2.0-1-x86_64 580.5 KiB 2044 KiB/s 00:00 [###########################################] 100%
rocm-device-libs-2:7.2.0-1-x86_64 537.9 KiB 2.29 MiB/s 00:00 [###########################################] 100%
roctracer-7.2.0-2-x86_64 526.5 KiB 2.62 MiB/s 00:00 [###########################################] 100%
rocthrust-7.2.0-1-x86_64 426.2 KiB 2.42 MiB/s 00:00 [###########################################] 100%
rocprim-7.2.0-1-any 307.8 KiB 2.21 MiB/s 00:00 [###########################################] 100%
hipblas-7.2.0-1-x86_64 165.5 KiB 1724 KiB/s 00:00 [###########################################] 100%
hipsparse-7.2.0-1-x86_64 116.3 KiB 1264 KiB/s 00:00 [###########################################] 100%
rocprofiler-register-7.2.0-1-x86_64 105.4 KiB 1054 KiB/s 00:00 [###########################################] 100%
hipcub-7.2.0-1-x86_64 93.8 KiB 1117 KiB/s 00:00 [###########################################] 100%
hipsolver-7.2.0-1-x86_64 83.1 KiB 989 KiB/s 00:00 [###########################################] 100%
hipfft-7.2.0-1-x86_64 66.1 KiB 870 KiB/s 00:00 [###########################################] 100%
rocm-core-7.2.0-1-x86_64 29.5 KiB 388 KiB/s 00:00 [###########################################] 100%
rocminfo-7.2.0-1-x86_64 28.8 KiB 400 KiB/s 00:00 [###########################################] 100%
hiprand-7.2.0-1-x86_64 28.6 KiB 376 KiB/s 00:00 [###########################################] 100%
rocm-cmake-7.2.0-1-any 28.1 KiB 369 KiB/s 00:00 [###########################################] 100%
hipblas-common-7.2.0-1-any 8.1 KiB 107 KiB/s 00:00 [###########################################] 100%
rocm-hip-sdk-7.2.0-1-any 2.2 KiB 30.8 KiB/s 00:00 [###########################################] 100%
rocm-hip-libraries-7.2.0-1-any 2.2 KiB 24.9 KiB/s 00:00 [###########################################] 100%
rocm-hip-runtime-7.2.0-1-any 2.1 KiB 31.5 KiB/s 00:00 [###########################################] 100%
rocm-opencl-sdk-7.2.0-1-any 2.1 KiB 26.6 KiB/s 00:00 [###########################################] 100%
rocm-language-runtime-7.2.0-1-any 2.1 KiB 27.8 KiB/s 00:00 [###########################################] 100%
```

---

### 评论 #46 — John-Gee (2026-02-08T21:49:49Z)

> No, FW 0x83 will not work with any kernel. The whole problem with the 0x83 FW was due to a fix targeting Windows driver, the corresponding change never made it to amdgpu. We later found the fix was not optimal anyway and reverted, but during that period, 0x83 got released on kernel-firmware.
> 

Is 0x84 supposed to be correct then?
I don't have the message handy right now, but I think when my computer boots amdgpu complains that the fw is < 0x82 and so it can't apply some kind of workaround, even though 84 > 82.


---

### 评论 #47 — amd-nicknick (2026-02-09T01:10:26Z)

@John-Gee, which device are you using? For Strix Halos you should not use DKMS. Are you using Halo or desktop GPUs?

---

### 评论 #48 — John-Gee (2026-02-10T10:59:37Z)

> [@John-Gee](https://github.com/John-Gee), which device are you using? For Strix Halos you should not use DKMS. Are you using Halo or desktop GPUs?

Ooops I did not notice this topic was Strix only, sorry. I'm using a 9070.

---

### 评论 #49 — amd-nicknick (2026-02-10T11:14:48Z)

Cool haha, for 9070 that is correct. The MES FW is on different codebase for Halo vs 9070, so version numbers are not directly comparable (ie. 0x84 does not carry the bug in 0x83 on Halo).
I could check the boot msg you mentioned if you share the dmesg log with me :)

---

### 评论 #50 — John-Gee (2026-02-10T11:45:16Z)

> Cool haha, for 9070 that is correct. The MES FW is on different codebase for Halo vs 9070, so version numbers are not directly comparable (ie. 0x84 does not carry the bug in 0x83 on Halo). I could check the boot msg you mentioned if you share the dmesg log with me :)

The line I mentioned:
[ 4.921347] amdgpu 0000:09:00.0: amdgpu: MES FW version must be >= 0x82 to enable LR compute workaround

yet:
cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES

MES_KIQ feature version: 1, firmware version: 0x00000084

MES feature version: 1, firmware version: 0x00000084 

the rest of amdgpu to limit spamming: https://gist.github.com/John-Gee/5353902ab2f99adae5e34af499d60172

Thanks a lot!

---

### 评论 #51 — zw963 (2026-02-25T16:08:24Z)

> Hello, I am trying to run ComfyUI use 6.18.8 kernal with rOCm 7.2.0 use 780M, but still system crash (iGpu reset) and force login out if remove `amdgpu.cwsr_enable=0`
> 
> ```
>  ╰──➤ $ uname -a
> Linux mingfan 6.18.8-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Sat, 31 Jan 2026 05:51:47 +0000 x86_64 GNU/Linux
> ```
> 
> ```
>  ╰──➤ $ \cat /proc/cmdline
> root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap sysrq_always_enabled=1 amdgpu.gpu_recovery=1 amdgpu.gttsize=24576 ttm.pages_limit=6291456 initrd=\boot\initramfs-linux-xanmod.img
> ```
> 
> Following is the dmesg broken log:
> 
> ```
> [  292.487846] userif-5: sent link down event.
> [  292.487856] userif-5: sent link up event.
> [  950.818166] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> [  950.818171] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1802
> [  950.818174] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
> [  950.818177] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
> [  950.818179] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
> [  950.818199] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
> [  950.818212] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 5
> [  950.818215] amdgpu: Failed to suspend process pid 14368
> [  950.818218] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 64667
> [  950.818245] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
> [  950.820337] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
> [  952.916113] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> [  952.916120] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
> [  953.391196] amdgpu: Freeing queue vital buffer 0x7f2e70800000, queue evicted
> [  953.391202] amdgpu: Freeing queue vital buffer 0x7f2e9da00000, queue evicted
> [  953.391204] amdgpu: Freeing queue vital buffer 0x7f340c400000, queue evicted
> [  953.391207] amdgpu: Freeing queue vital buffer 0x7f340fa00000, queue evicted
> [  953.391209] amdgpu: Freeing queue vital buffer 0x7f3414400000, queue evicted
> [  954.920081] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> [  954.920088] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
> [  956.924070] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> [  956.924077] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
> [  957.131282] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
> [  957.132772] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
> [  957.165393] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
> [  957.166061] [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
> [  957.166190] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> [  957.166192] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> [  957.166195] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
> [  957.167841] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
> [  957.173995] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
> [  957.296277] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
> [  957.296286] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
> [  957.296288] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
> [  957.296290] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
> [  957.296291] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
> [  957.296293] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
> [  957.296294] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
> [  957.296295] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
> [  957.296297] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
> [  957.296300] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
> [  957.296301] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
> [  957.296303] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
> [  957.296305] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
> [  957.298461] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
> [  957.298474] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
> [  958.892620] rfkill: input handler enabled
> [  959.357038] userif-5: sent link down event.
> [  959.357044] userif-5: sent link up event.
> [  961.343114] amdgpu: Freeing queue vital buffer 0x7f4e7ca00000, queue evicted
> [  961.343128] amdgpu: Freeing queue vital buffer 0x7f4ec8600000, queue evicted
> [  961.343133] amdgpu: Freeing queue vital buffer 0x7f4f03600000, queue evicted
> [  961.343135] amdgpu: Freeing queue vital buffer 0x7f4f04400000, queue evicted
> [  961.480700] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> [  961.480930] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1800
> [  961.481136] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
> [  961.481177] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
> [  961.481200] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
> [  961.481201] amdgpu: Resetting wave fronts (cpsch) on dev 000000000ff73c32
> [  961.481203] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
> [  961.481250] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
> [  961.484928] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
> [  961.583988] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
> [  961.617548] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
> [  961.618214] [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
> ```
> 
> Following is new installed rocm related package version:
> 
> ```
> composable-kernel-7.2.0-1-x86_64 1557.0 MiB 16.6 MiB/s 01:34 [###########################################] 100%
> hipblaslt-7.2.0-1-x86_64 1525.6 MiB 12.7 MiB/s 02:01 [###########################################] 100%
> rocm-llvm-2:7.2.0-1-x86_64 956.8 MiB 14.0 MiB/s 01:08 [###########################################] 100%
> rocsolver-7.2.0-1-x86_64 690.6 MiB 17.9 MiB/s 00:39 [###########################################] 100%
> rccl-7.2.0-1-x86_64 423.2 MiB 18.8 MiB/s 00:22 [###########################################] 100%
> rocblas-7.2.0-1-x86_64 331.3 MiB 16.7 MiB/s 00:20 [###########################################] 100%
> miopen-hip-7.2.0-1-x86_64 251.1 MiB 17.2 MiB/s 00:15 [###########################################] 100%
> rocfft-7.2.0-1-x86_64 120.8 MiB 17.4 MiB/s 00:07 [###########################################] 100%
> rocsparse-7.2.0-1-x86_64 72.1 MiB 16.2 MiB/s 00:04 [###########################################] 100%
> comgr-2:7.2.0-1-x86_64 42.1 MiB 16.5 MiB/s 00:03 [###########################################] 100%
> hipsparselt-7.2.0-1-x86_64 41.6 MiB 18.5 MiB/s 00:02 [###########################################] 100%
> rocrand-7.2.0-1-x86_64 22.5 MiB 15.9 MiB/s 00:01 [###########################################] 100%
> rocalution-7.2.0-1-x86_64 8.3 MiB 19.2 MiB/s 00:00 [###########################################] 100%
> hip-runtime-amd-7.2.0-1-x86_64 7.3 MiB 20.1 MiB/s 00:00 [###########################################] 100%
> rocm-smi-lib-7.2.0-1-x86_64 1052.3 KiB 1253 KiB/s 00:01 [###########################################] 100%
> hsa-rocr-7.2.0-1-x86_64 856.7 KiB 1727 KiB/s 00:00 [###########################################] 100%
> rocm-opencl-runtime-7.2.0-1-x86_64 580.5 KiB 2044 KiB/s 00:00 [###########################################] 100%
> rocm-device-libs-2:7.2.0-1-x86_64 537.9 KiB 2.29 MiB/s 00:00 [###########################################] 100%
> roctracer-7.2.0-2-x86_64 526.5 KiB 2.62 MiB/s 00:00 [###########################################] 100%
> rocthrust-7.2.0-1-x86_64 426.2 KiB 2.42 MiB/s 00:00 [###########################################] 100%
> rocprim-7.2.0-1-any 307.8 KiB 2.21 MiB/s 00:00 [###########################################] 100%
> hipblas-7.2.0-1-x86_64 165.5 KiB 1724 KiB/s 00:00 [###########################################] 100%
> hipsparse-7.2.0-1-x86_64 116.3 KiB 1264 KiB/s 00:00 [###########################################] 100%
> rocprofiler-register-7.2.0-1-x86_64 105.4 KiB 1054 KiB/s 00:00 [###########################################] 100%
> hipcub-7.2.0-1-x86_64 93.8 KiB 1117 KiB/s 00:00 [###########################################] 100%
> hipsolver-7.2.0-1-x86_64 83.1 KiB 989 KiB/s 00:00 [###########################################] 100%
> hipfft-7.2.0-1-x86_64 66.1 KiB 870 KiB/s 00:00 [###########################################] 100%
> rocm-core-7.2.0-1-x86_64 29.5 KiB 388 KiB/s 00:00 [###########################################] 100%
> rocminfo-7.2.0-1-x86_64 28.8 KiB 400 KiB/s 00:00 [###########################################] 100%
> hiprand-7.2.0-1-x86_64 28.6 KiB 376 KiB/s 00:00 [###########################################] 100%
> rocm-cmake-7.2.0-1-any 28.1 KiB 369 KiB/s 00:00 [###########################################] 100%
> hipblas-common-7.2.0-1-any 8.1 KiB 107 KiB/s 00:00 [###########################################] 100%
> rocm-hip-sdk-7.2.0-1-any 2.2 KiB 30.8 KiB/s 00:00 [###########################################] 100%
> rocm-hip-libraries-7.2.0-1-any 2.2 KiB 24.9 KiB/s 00:00 [###########################################] 100%
> rocm-hip-runtime-7.2.0-1-any 2.1 KiB 31.5 KiB/s 00:00 [###########################################] 100%
> rocm-opencl-sdk-7.2.0-1-any 2.1 KiB 26.6 KiB/s 00:00 [###########################################] 100%
> rocm-language-runtime-7.2.0-1-any 2.1 KiB 27.8 KiB/s 00:00 [###########################################] 100%
> ```

Hi, this fixed on my 7840hs mini pc without need set `amdgpu.cwsr_enable=0` in boot cmdline, check https://github.com/ROCm/ROCm/issues/5180#issuecomment-3946430208

---

### 评论 #52 — zw963 (2026-03-04T14:51:11Z)

probably still not fixed on 780M ?

```
[73314.889668] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73314.889675] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[73314.889677] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73314.889681] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[73314.889682] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[73314.889684] amdgpu: Failed to quiesce KFD
[73314.889701] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73314.891684] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 49700
[73314.891708] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73314.893432] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73316.994500] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73316.994507] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.998481] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73318.998487] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.999856] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73319.031470] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73319.031938] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73319.032193] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73319.032198] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73319.032202] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73319.033702] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73319.039404] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73319.185138] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73319.185150] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73319.185153] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73319.185155] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73319.185157] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73319.185158] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73319.185160] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73319.185162] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73319.185163] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73319.185165] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73319.185167] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73319.185169] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73319.185171] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73319.187263] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[73319.187276] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[73327.541061] amdgpu: Freeing queue vital buffer 0x7f2e27400000, queue evicted
[73327.541067] amdgpu: Freeing queue vital buffer 0x7f3041200000, queue evicted
[73327.541070] amdgpu: Freeing queue vital buffer 0x7f3047400000, queue evicted
[73327.541071] amdgpu: Freeing queue vital buffer 0x7f3047a00000, queue evicted
[73327.541075] amdgpu: Freeing queue vital buffer 0x7f3196600000, queue evicted
[73327.649199] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73327.649205] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[73327.649207] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73327.649211] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[73327.649212] amdgpu: Resetting wave fronts (cpsch) on dev 0000000058c303b6
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73327.649312] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73327.652804] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73327.758867] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73327.793270] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73327.793923] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73327.793983] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73327.793985] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73327.793988] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73327.796093] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73327.803519] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73328.541797] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73328.541804] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73328.541807] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73328.541808] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73328.541810] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73328.541811] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73328.541813] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73328.541814] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73328.541815] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73328.541817] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73328.541819] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73328.541820] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73328.541822] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73328.543914] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[73328.543927] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
```

---
