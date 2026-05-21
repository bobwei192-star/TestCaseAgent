# [Issue]: Unable to compile ROCm5.7 on recent Ubuntu (InvokeAI + fp16 + RX7600 incompatibility)

> **Issue #4358**
> **状态**: closed
> **创建时间**: 2025-02-08T15:26:02Z
> **更新时间**: 2025-02-18T20:10:16Z
> **关闭时间**: 2025-02-18T20:08:37Z
> **作者**: mcondarelli
> **标签**: Under Investigation, ROCm 5.7.0
> **URL**: https://github.com/ROCm/ROCm/issues/4358

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 5.7.0** (颜色: #ededed)

## 描述

### Problem Description

I am trying to compile the oldish version ROCm5.7 because it seems it's the last one fully working on my hardware (any update on this would be *much* appreciated).

Compilation fails on "`aqlprofile started due to rocr`" probably due to my OS (`Ubuntu 24.04`).
Is there a way around?
I need this just to run `PyTorch`-based applications (i.e.: `InvokeAI` and related suites).
Do I even need it (it seems to have been dropped)?
Can I just comment it out in `rocr` dependencies?

### Operating System

OS: NAME="Linux Mint" VERSION="22.1 (Xia)" UBUNTU_CODENAME="noble"

### CPU

CPU:  model name	: AMD Ryzen 9 5950X 16-Core Processor

### GPU

GPU:   Name:                    AMD Ryzen 9 5950X 16-Core Processor   Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor   Name:                    gfx1102                               Marketing Name:          AMD Radeon™ RX 7600 XT                  Name:                    amdgcn-amd-amdhsa--gfx1102         

### ROCm Version

ROCm 5.7

### ROCm Component

_No response_

### Steps to Reproduce

I am following instructions [here](https://github.com/ROCm/ROCm?tab=readme-ov-file#build-rocm-from-source) and I'm using the `Docker` method.
Apparently problem is `aqlprofile` is supported only for older Ubuntu releases (I see just v20.04 and v22.04 on repo).
```
mcon@ikea:~/ROCm$ export ROCM_VERSION=5.7.2
mcon@ikea:~/ROCm$ repo sync
Fetching: 100% (64/64), done in 0.853s
info: A new version of repo is available
warning: repo is not tracking a remote branch, so it will not receive updates
info: Restarting repo with latest version
Checking out: 100% (63/63), done in 3.127s
repo sync has finished successfully.
mcon@ikea:~/ROCm$ docker pull rocm/rocm-build-ubuntu-24.04:6.3
6.3: Pulling from rocm/rocm-build-ubuntu-24.04
de44b265507a: Pull complete 
d70eae50cadc: Pull complete 
5f1f94851a67: Pull complete 
03fa6a4a986c: Pull complete 
2d76206028dc: Pull complete 
f3cb47b6e45f: Pull complete 
98fd60208a5a: Pull complete 
Digest: sha256:b9b8b84a8c5f5d083e9da50e3cfc231dd35e5a061cc3137031719802f2e92b02
Status: Downloaded newer image for rocm/rocm-build-ubuntu-24.04:6.3
docker.io/rocm/rocm-build-ubuntu-24.04:6.3
mcon@ikea:~/ROCm$ docker run -ti \
    -e ROCM_VERSION=${ROCM_VERSION} \
    -e CCACHE_DIR=$HOME/.ccache \
    -e CCACHE_ENABLED=true \
    -e DOCK_WORK_FOLD=/src \
    -w /src \
    -v $PWD:/src \
    -v /etc/passwd:/etc/passwd \
    -v /etc/shadow:/etc/shadow \
    -v ${HOME}/.ccache:${HOME}/.ccache \
    -u $(id -u):$(id -g) \
    rocm/rocm-build-ubuntu-24.04:6.3 bash
mcon@6afbab97987b:/src$ export GPU_ARCHS="gfx1100,gfx1102"
mcon@6afbab97987b:/src$ make -f ROCm/tools/rocm-build/ROCm.mk -j ${NPROC:-$(nproc)} all
OUT_DIR=/src/out/ubuntu-24.04/24.04
ROCM_INSTALL_PATH=/opt/rocm-5.7.2
sudo mkdir -p -m 775 "/opt/rocm-5.7.2" && \
sudo chown -R "1000:1000" "/opt"
0dino!
sudo chown -R "1000:1000" "/home/mcon"
mkdir -p "/src/out/ubuntu-24.04/24.04/logs"
mkdir -p /home/mcon/.ccache
amd_smi_lib started due to
rocm_smi_lib started due to
lightning started due to
hipcc started due to
rocprofiler-register started due to
rocm-cmake started due to
rocprofiler-compute started due to
rocm-core started due to
half started due to rocm-cmake
:              rocm-cmake built
:              rocm-core built
:              half built
:              rocprofiler-compute built
:              hipcc built
:              rocprofiler-register built
:              amd_smi_lib built
:              rocm_smi_lib built
:              lightning built
devicelibs started due to lightning
hipblas-common started due to lightning
miopen-deps started due to lightning hipcc
:              hipblas-common built
:              devicelibs built
rocr started due to lightning rocm_smi_lib devicelibs rocprofiler-register
comgr started due to lightning devicelibs
:              rocr built
openmp_extras started due to lightning devicelibs rocr
aqlprofile started due to rocr
rocminfo started due to rocr
rocm_bandwidth_test started due to rocr
make: *** [ROCm/tools/rocm-build/ROCm.mk:209: /src/out/ubuntu-24.04/24.04/logs/aqlprofile] Error 1
make: *** Waiting for unfinished jobs....
mcon@6afbab97987b:/src$ make -f ROCm/tools/rocm-build/ROCm.mk -j ${NPROC:-$(nproc)} all
OUT_DIR=/src/out/ubuntu-24.04/24.04
ROCM_INSTALL_PATH=/opt/rocm-5.7.2
:              amd_smi_lib built
:              comgr built
:              devicelibs built
:              half built
:              hipblas-common built
:              hipcc built
:              lightning built
:              miopen-deps built
opencl_on_rocclr started due to rocr comgr
dbgapi started due to rocr comgr
aqlprofile started due to rocr
hip_on_rocclr started due to rocr comgr hipcc rocprofiler-register
:              openmp_extras built
:              rocm-cmake built
:              rocm-core built
:              rocm_bandwidth_test built
:              rocm_smi_lib built
:              rocminfo built
:              rocprofiler-compute built
:              rocprofiler-register built
:              rocr built
rpp started due to half lightning hipcc openmp_extras
make: *** [ROCm/tools/rocm-build/ROCm.mk:209: /src/out/ubuntu-24.04/24.04/logs/aqlprofile] Error 1
make: *** Waiting for unfinished jobs....
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

on Docker container I have:
```
mcon@6afbab97987b:/src/out/ubuntu-24.04/24.04/logs$ /opt/rocm-5.7.2/bin/rocminfo --support
ROCk module version 6.10.5 is loaded
Unable to open /dev/kfd read-write: No such file or directory
Failed to get user name to check for video group membership
```
while on host I have:
```
mcon@ikea:~$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.10.5 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
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
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
  Max Clock Freq. (MHz):   3400                               
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
      Size:                    32781080(0x1f43318) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32781080(0x1f43318) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32781080(0x1f43318) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32781080(0x1f43318) KB             
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
  Marketing Name:          AMD Radeon™ RX 7600 XT           
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2493                               
  BDFID:                   11520                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 412                                
  SDMA engine uCode::      21                                 
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
*** Done ***             
```

### Additional Information

_No response_

---

## 评论 (28 条)

### 评论 #1 — briansp2020 (2025-02-08T17:41:13Z)

Why don't you just install the latest? It seems compiling ROCm from source is not a simple task, especially older versions.

---

### 评论 #2 — mcondarelli (2025-02-08T18:47:23Z)

> Why don't you just install the latest? It seems compiling ROCm from source is not a simple task, especially older versions.

I know.
Problem is ROCm5.7 seems to be the last version supporting AMD Radeon™ RX 7600 XT.
Later versions dropped support and **don't** fully work (e.g.: fp16 usage results in core dump).

---

### 评论 #3 — mcondarelli (2025-02-09T18:04:48Z)

Update: Besides above error I also experience a very strange behavior: when compiling certain models (currently `make -f ROCm/tools/rocm-build/ROCm.mk -j 31 T_rocprim`,  `[ 30%] Linking CXX executable test_basic`) system becomes completely unresponsive (not blocked) and can take several minutes to process a simple `ls` command on another terminal; not even `ctrl-alt-Fn` given at console is honored. Interrupting compilation with `ctrl-C` **does** work... after a loooooooong time.

Note: this machine has 32 CPUs, 32Gb RAM and 300+GB free disk.

---

### 评论 #4 — mcondarelli (2025-02-10T09:30:06Z)

Further Update: Apparently unresponsiveness problem is due to memory consumption: after a while compilation ate up all my 32Gb real RAM and all my 33Gb swap and then `kswapd0` process started running at 100% CPU.

NOTE: apparently `make -f ROCm/tools/rocm-build/ROCm.mk -j 1 ...` does **not** honor the `-j 1` flag as I can see 32 instances of `clang-18` process, each eating 1+Gb RAM.
Perhaps flag is not passed correctly to sub-makefiles?

---

### 评论 #5 — ppanchad-amd (2025-02-10T15:14:48Z)

Hi @mcondarelli. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #6 — schung-amd (2025-02-10T17:26:10Z)

Hi @mcondarelli, sorry you're having trouble with this. While newer versions of ROCm are not officially supported on the 7600XT, you should be able to use them with `HSA_OVERRIDE_GFX_VERSION=11.0.0`. `fp16`-related crashes are not unheard of, but I need some more information. Are you only seeing these crashes with certain applications and in certain contexts? It may be the case that your crashes are in line with some of our known issues and not caused by the lack of official support for the 7600XT.

Regarding the issue you're seeing with `aqlprofile`, this is probably because ROCm 5.7 is not supported on Ubuntu 24.04 (see: https://rocm.docs.amd.com/en/docs-5.7.0/release/gpu_os_support.html); we didn't add support for Ubuntu 24.04 until ROCm 6.2.0 so I'm not surprised that there are missing packages for older releases. `aqlprofile` is closed-source so I don't think there's a way around this at the moment, but we are working on eventually making this open source.

I'll look into the `make` process issue you're seeing. In the meanwhile, I don't have experience with Linux Mint, but as 22.1 is based on Ubuntu 24.04 you may be able to follow https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html rather than building from source.

---

### 评论 #7 — mcondarelli (2025-02-10T18:04:21Z)

> Hi [@mcondarelli](https://github.com/mcondarelli), sorry you're having trouble with this. While newer versions of ROCm are not officially supported on the 7600XT, you should be able to use them with `HSA_OVERRIDE_GFX_VERSION=11.0.0`. `fp16`-related crashes are not unheard of, but I need some more information. Are you only seeing these crashes with certain applications and in certain contexts? It may be the case that your crashes are in line with some of our known issues and not caused by the lack of official support for the 7600XT.

I was trying to use latest version but I got into deep troubles involving bad and repeatable core-dumps.
My test system is currently in a rather messy status because of many attempts to overcome problem, but I'm fully willing to do a complete reinstall from scratch if that is deemed useful.
I am a long time Debian user and I would like to avoid Ubuntu (**_if possible_**) due to recent switch to SNAP, but I'm open to suggestions.

> Regarding the issue you're seeing with `aqlprofile`, this is probably because ROCm 5.7 is not supported on Ubuntu 24.04 (see: https://rocm.docs.amd.com/en/docs-5.7.0/release/gpu_os_support.html); we didn't add support for Ubuntu 24.04 until ROCm 6.2.0 so I'm not surprised that there are missing packages for older releases. `aqlprofile` is closed-source so I don't think there's a way around this at the moment, but we are working on eventually making this open source.

My attempt to compile from source is **_only_** because I understood ROCm5.7 was last version fully working (i.e.: including fp16) on my hardware.
I would be happy to use "standard install" if at all possible.

> I'll look into the `make` process issue you're seeing. In the meanwhile, I don't have experience with Linux Mint, but as 22.1 is based on Ubuntu 24.04 you may be able to follow https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html rather than building from source.

As said reason for this attempt was crashes of applications, manly when using `fp16` which is almost-required when using medium-large models.

I am tinkering with A.I. and my current target is using `InvokeAI`, but I will want to expand to other technologies (and I would hate to need to buy another GPU).

I will cleanup my installation and I will try to follow https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html 
I will report here any trouble I may get with application.

Help solving (if needed, of course) will be highly appreciated.
Please feel free to ask specific questions and/or tests.

Many thanks, for the time being.

---

### 评论 #8 — schung-amd (2025-02-10T19:29:56Z)

> I am a long time Debian user and I would like to avoid Ubuntu (if possible) due to recent switch to SNAP, but I'm open to suggestions.

We have recently added Debian 12 support, but only for kernel version 6.1. A possible alternative would be to downgrade to Mint 21.x since that's based on Ubuntu 22.04, which ROCm 5.7 did have support for. Again, I don't have experience with ROCm on Mint, but I'll provide support in any way I can.

I'm not sure this would solve the fp16 crashes though, as I suspect this isn't just due to lack of official support. I've personally seen crashes on a 7900XTX with fp16-enabled A1111 (somewhat of a known issue with various AMD hardware according to their documentation). Still, if you can get ROCm 5.7 up and running, we might as well try that to see if it resolves your issues.

> My attempt to compile from source is only because I understood ROCm5.7 was last version fully working (i.e.: including fp16) on my hardware.
I would be happy to use "standard install" if at all possible.

There are instructions for installing ROCm 5.7.0 at https://rocm.docs.amd.com/en/docs-5.7.0/deploy/linux/quick_start.html, which I believe are still functional. This won't address the incompatibility issue however, so you'll either have to downgrade your distro version or use a more recent ROCm version.

> As said reason for this attempt was crashes of applications, manly when using fp16 which is almost-required when using medium-large models.

Is your main issue with full precision a lack of VRAM? The low VRAM mode in `InvokeAI` may help with this.

---

### 评论 #9 — mcondarelli (2025-02-10T21:18:58Z)

I post below full script of what I did to install `ROCm6.3`, `InvokeAI` and `bitsandbytes`.
Besides a few nuances due to `bitsandbytes` being compiled for `ROCm6.2` problem is always the same:
```
:0:rocdevice.cpp            :3020: 7262982208d us:  Callback: Queue 0x77ec42100000 aborting with error : HSA_STATUS_ERROR_INVALID_ISA: The instruction set architecture is invalid. code: 0x100f
Aborted (core dumped)
```
Enabling `precision: float32` flag in `invokeai.yaml` (i.e.: disabling `fp16` usage) error disappears but I'm no longer able to use SDXL models due to OoM error:
```
(.venv) mcon@ikea:~/AMD$ ./start-web 
+ export HCC_AMDGPU_TARGET=gfx1100
+ export HSA_OVERRIDE_GFX_VERSION=11.0.0
+ export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True
+ export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
+ export INVOKEAI_ROOT=/home/mcon/invokeai
+ .venv/bin/invokeai-web
g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

[2025-02-10 21:42:16,812]::[InvokeAI]::INFO --> Loading node pack latent-upscale
[2025-02-10 21:42:16,974]::[InvokeAI]::INFO --> Loaded 1 node packs from /home/mcon/invokeai/nodes
[2025-02-10 21:42:18,162]::[InvokeAI]::INFO --> Patchmatch initialized
[2025-02-10 21:42:18,686]::[InvokeAI]::INFO --> Using torch device: AMD Radeon™ RX 7600 XT
[2025-02-10 21:42:19,063]::[InvokeAI]::INFO --> cuDNN version: 3003000
[2025-02-10 21:42:19,073]::[InvokeAI]::INFO --> InvokeAI version 5.6.0
[2025-02-10 21:42:19,073]::[InvokeAI]::INFO --> Root directory = /home/mcon/invokeai
[2025-02-10 21:42:19,074]::[InvokeAI]::INFO --> Initializing database at /home/mcon/invokeai/databases/invokeai.db
[2025-02-10 21:42:19,076]::[ModelManagerService]::INFO --> [MODEL CACHE] Calculated model RAM cache size: 13958.38 MB. Heuristics applied: [1].
[2025-02-10 21:42:19,093]::[InvokeAI]::INFO --> Pruned 1 finished queue items
[2025-02-10 21:42:19,304]::[InvokeAI]::INFO --> Cleaned database (freed 0.01MB)
[2025-02-10 21:42:19,304]::[InvokeAI]::INFO --> Invoke running on http://0.0.0.0:9090 (Press CTRL+C to quit)
[2025-02-10 21:42:29,624]::[InvokeAI]::INFO --> Executing queue item 261, session 18f998d3-635e-40cf-add0-eb500c4af8e3
[2025-02-10 21:42:29,752]::[InvokeAI]::WARNING --> Loading 0.146484375 MB into VRAM, but only -4991.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/cached_model/cached_model_with_partial_load.py:219: UserWarning: expandable_segments not supported on this platform (Triggered internally at /pytorch/c10/hip/HIPAllocatorConfig.h:29.)
  state_dict[key] = state_dict[key].to(target_device)
[2025-02-10 21:42:29,949]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.20s. Total model size: 469.44MB, VRAM: 0.15MB (0.0%)
[2025-02-10 21:42:30,001]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:42:30,991]::[InvokeAI]::WARNING --> Loading 0.634765625 MB into VRAM, but only -5206.75 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:42:31,005]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.02s. Total model size: 2649.92MB, VRAM: 0.63MB (0.0%)
[2025-02-10 21:42:31,047]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:42:32,511]::[InvokeAI]::WARNING --> Loading 0.146484375 MB into VRAM, but only -5208.75 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:42:32,516]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.02s. Total model size: 469.44MB, VRAM: 0.15MB (0.0%)
[2025-02-10 21:42:32,520]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:42:32,701]::[InvokeAI]::WARNING --> Loading 0.634765625 MB into VRAM, but only -5208.75 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:42:32,715]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.02s. Total model size: 2649.92MB, VRAM: 0.63MB (0.0%)
[2025-02-10 21:42:32,717]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:42:35,091]::[InvokeAI]::WARNING --> Loading 1.904296875 MB into VRAM, but only -5208.75 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:42:35,145]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:unet' (UNet2DConditionModel) onto cuda device in 0.08s. Total model size: 9794.10MB, VRAM: 1.90MB (0.0%)
[2025-02-10 21:42:35,152]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:scheduler' (DDPMScheduler) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 30/30 [06:57<00:00, 13.93s/it]
[2025-02-10 21:49:36,148]::[InvokeAI]::WARNING --> Loading 0.0 MB into VRAM, but only -5320.75 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:49:36,149]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:vae' (AutoencoderKL) onto cuda device in 0.04s. Total model size: 319.11MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:49:50,303]::[InvokeAI]::ERROR --> Error while invoking session 18f998d3-635e-40cf-add0-eb500c4af8e3, invocation fffe4dcd-c763-4a53-85e6-bd23ae48bbc0 (l2i): HIP out of memory. Tried to allocate 4.50 GiB. GPU 0 has a total capacity of 15.98 GiB of which 1.40 GiB is free. Of the allocated memory 1.26 GiB is allocated by PyTorch, and 152.50 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
[2025-02-10 21:49:50,303]::[InvokeAI]::ERROR --> Traceback (most recent call last):
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/app/services/session_processor/session_processor_default.py", line 129, in run_node
    output = invocation.invoke_internal(context=context, services=self._services)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/app/invocations/baseinvocation.py", line 308, in invoke_internal
    return self.invoke(context)
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/utils/_contextlib.py", line 116, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/app/invocations/latents_to_image.py", line 153, in invoke
    image = vae.decode(latents, return_dict=False)[0]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/diffusers/utils/accelerate_utils.py", line 46, in wrapper
    return method(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/diffusers/models/autoencoders/autoencoder_kl.py", line 326, in decode
    decoded = self._decode(z).sample
              ^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/diffusers/models/autoencoders/autoencoder_kl.py", line 297, in _decode
    dec = self.decoder(z)
          ^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1751, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1762, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/diffusers/models/autoencoders/vae.py", line 337, in forward
    sample = up_block(sample, latent_embeds)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1751, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1762, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/diffusers/models/unets/unet_2d_blocks.py", line 2750, in forward
    hidden_states = upsampler(hidden_states)
                    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1751, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1762, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/diffusers/models/upsampling.py", line 180, in forward
    hidden_states = self.conv(hidden_states)
                    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1751, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1762, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/torch_module_autocast/custom_modules/custom_conv2d.py", line 41, in forward
    return self._autocast_forward(input)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/torch_module_autocast/custom_modules/custom_conv2d.py", line 35, in _autocast_forward
    return self._conv_forward(input, weight, bias)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/nn/modules/conv.py", line 549, in _conv_forward
    return F.conv2d(
           ^^^^^^^^^
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 4.50 GiB. GPU 0 has a total capacity of 15.98 GiB of which 1.40 GiB is free. Of the allocated memory 1.26 GiB is allocated by PyTorch, and 152.50 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

[2025-02-10 21:49:50,346]::[InvokeAI]::INFO --> Graph stats: 18f998d3-635e-40cf-add0-eb500c4af8e3
                          Node   Calls   Seconds  VRAM Used
             sdxl_model_loader       1    0.015s     0.000G
            sdxl_compel_prompt       2    4.070s     0.238G
                       collect       2    0.001s     0.001G
                         noise       1    0.001s     0.001G
               denoise_latents       1  422.129s     1.012G
                 core_metadata       1    0.000s     0.003G
                           l2i       1   14.432s     2.469G
TOTAL GRAPH EXECUTION TIME: 440.648s
TOTAL GRAPH WALL TIME: 440.655s
RAM used by InvokeAI process: 15.36G (+13.724G)
RAM used to load models: 12.92G
VRAM in use: 0.000G
RAM cache statistics:
   Model cache hits: 11
   Model cache misses: 7
   Models cached: 7
   Models cleared from cache: 0
   Cache high water mark: 12.92/0.00G
```
downgrading to some SD.1 model I finally get requested image:
```
[2025-02-10 21:51:56,774]::[InvokeAI]::INFO --> Executing queue item 262, session 30e1b6e9-dfec-49a3-9b65-7f21079de530
(…)ature_extractor/preprocessor_config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 342/342 [00:00<00:00, 2.69MB/s]
tokenizer/special_tokens_map.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 472/472 [00:00<00:00, 3.64MB/s]
scheduler/scheduler_config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 308/308 [00:00<00:00, 2.23MB/s]
tokenizer/tokenizer_config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 806/806 [00:00<00:00, 6.34MB/s]
model_index.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 541/541 [00:00<00:00, 5.16MB/s]
safety_checker/config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4.72k/4.72k [00:00<00:00, 32.3MB/s]
text_encoder/config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 617/617 [00:00<00:00, 4.81MB/s]
unet/config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 743/743 [00:00<00:00, 8.07MB/s]
tokenizer/merges.txt: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 525k/525k [00:00<00:00, 1.75MB/s]
tokenizer/vocab.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.06M/1.06M [00:00<00:00, 3.36MB/s]
vae/config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 547/547 [00:00<00:00, 4.63MB/s]
Fetching 11 files: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 11/11 [00:01<00:00,  9.29it/s]
Loading pipeline components...: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6/6 [00:02<00:00,  2.81it/s]
[2025-02-10 21:52:01,741]::[InvokeAI]::WARNING --> Loading 0.146484375 MB into VRAM, but only -5321.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:52:01,747]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '97f484a5-7842-4949-b788-f4a0c2d54ab9:text_encoder' (CLIPTextModel) onto cuda device in 0.01s. Total model size: 469.44MB, VRAM: 0.15MB (0.0%)
[2025-02-10 21:52:01,754]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '97f484a5-7842-4949-b788-f4a0c2d54ab9:tokenizer' (CLIPTokenizer) onto cuda device in 0.01s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:52:01,960]::[InvokeAI]::WARNING --> Loading 0.0 MB into VRAM, but only -5321.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:52:01,961]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '97f484a5-7842-4949-b788-f4a0c2d54ab9:text_encoder' (CLIPTextModel) onto cuda device in 0.01s. Total model size: 469.44MB, VRAM: 0.15MB (0.0%)
[2025-02-10 21:52:01,967]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '97f484a5-7842-4949-b788-f4a0c2d54ab9:tokenizer' (CLIPTokenizer) onto cuda device in 0.01s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:52:02,177]::[InvokeAI]::WARNING --> Loading 0.28564453125 MB into VRAM, but only -5321.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:52:02,194]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '97f484a5-7842-4949-b788-f4a0c2d54ab9:unet' (UNet2DConditionModel) onto cuda device in 0.03s. Total model size: 3278.81MB, VRAM: 0.29MB (0.0%)
[2025-02-10 21:52:02,199]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '97f484a5-7842-4949-b788-f4a0c2d54ab9:scheduler' (PNDMScheduler) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 30/30 [03:25<00:00,  6.85s/it]
[2025-02-10 21:55:27,601]::[InvokeAI]::WARNING --> Loading 0.0 MB into VRAM, but only -5325.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:55:27,603]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '97f484a5-7842-4949-b788-f4a0c2d54ab9:vae' (AutoencoderKL) onto cuda device in 0.02s. Total model size: 319.11MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:57:40,970]::[InvokeAI]::INFO --> Graph stats: 30e1b6e9-dfec-49a3-9b65-7f21079de530
                          Node   Calls   Seconds  VRAM Used
             main_model_loader       1    0.003s     0.000G
                     clip_skip       1    0.001s     0.000G
                        compel       2    5.363s     0.142G
                       collect       2    0.000s     0.000G
                         noise       1    0.001s     0.000G
               denoise_latents       1  205.417s     2.549G
                 core_metadata       1    0.000s     0.001G
                           l2i       1  133.358s     2.941G
TOTAL GRAPH EXECUTION TIME: 344.144s
TOTAL GRAPH WALL TIME: 344.151s
RAM used by InvokeAI process: 14.95G (-0.409G)
RAM used to load models: 3.97G
VRAM in use: 0.001G
RAM cache statistics:
   Model cache hits: 7
   Model cache misses: 1
   Models cached: 7
   Models cleared from cache: 2
   Cache high water mark: 4.28/0.00G
```
but build took almost 6 minutes which seems too much.

I am pretty desperate because I'm pretty sure I managed to make this work *without* "Low VRAM" (and I have imagest that prove I dod not allucinate), but then I tried to add also LoRA training (which I need) and I did break something and I'm unable to recreate previous situation.

Note: using docker containers would be preferred because of repeteability but I'm open to suggestions.

TiA!

Here is full log of what I did:
```
mcon@ikea:~$ sudo apt purge amd
amd64-microcode       amdgpu-core           amdgpu-dkms           amdgpu-dkms-firmware  amdgpu-install        amdgpu-lib            amdgpu-lib32          amdgpu-multimedia     amd-smi-lib           
mcon@ikea:~$ sudo apt purge amdgpu*
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package amdgpu-install_6.3.60302-1_all.deb
mcon@ikea:~$ sudo apt purge amdgpu\*
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'amdgpu-install' for glob 'amdgpu*'
Note, selecting 'amdgpu-multimedia' for glob 'amdgpu*'
Note, selecting 'amdgpu-dkms' for glob 'amdgpu*'
Note, selecting 'amdgpu-doc' for glob 'amdgpu*'
Note, selecting 'amdgpu-lib32' for glob 'amdgpu*'
Note, selecting 'amdgpu-lib' for glob 'amdgpu*'
Note, selecting 'amdgpu-pro' for glob 'amdgpu*'
Note, selecting 'amdgpu-pro-core' for glob 'amdgpu*'
Note, selecting 'amdgpu-pro-lib32' for glob 'amdgpu*'
Note, selecting 'amdgpu-pro-oglp' for glob 'amdgpu*'
Note, selecting 'amdgpu-dkms-firmware' for glob 'amdgpu*'
Note, selecting 'amdgpu-dkms-headers' for glob 'amdgpu*'
Note, selecting 'amdgpu' for glob 'amdgpu*'
Note, selecting 'amdgpu-pro-oglp:i386' for glob 'amdgpu*'
Note, selecting 'amdgpu-core' for glob 'amdgpu*'
Note, selecting 'amdgpu-pro-oglp:i386' instead of 'amdgpu-pro-oglp:i386'
Package 'amdgpu-pro' is not installed, so not removed
Package 'amdgpu' is not installed, so not removed
Package 'amdgpu-pro-core' is not installed, so not removed
Package 'amdgpu-pro-oglp' is not installed, so not removed
Package 'amdgpu-pro-lib32' is not installed, so not removed
Package 'amdgpu-dkms-headers' is not installed, so not removed
Package 'amdgpu-doc' is not installed, so not removed
The following package was automatically installed and is no longer required:
  valgrind
Use 'sudo apt autoremove' to remove it.
The following packages will be REMOVED:
  amdgpu-core* amdgpu-dkms* amdgpu-dkms-firmware* amdgpu-install* amdgpu-lib* amdgpu-lib32* amdgpu-multimedia* libdrm-amdgpu-amdgpu1* libdrm-amdgpu-amdgpu1:i386* libdrm-amdgpu-common* libdrm-amdgpu-dev* libdrm-amdgpu-radeon1*
  libdrm-amdgpu-radeon1:i386* libdrm2-amdgpu* libdrm2-amdgpu:i386* libegl1-amdgpu-mesa* libegl1-amdgpu-mesa:i386* libegl1-amdgpu-mesa-drivers* libegl1-amdgpu-mesa-drivers:i386* libgbm1-amdgpu* libgbm1-amdgpu:i386* libgl1-amdgpu-mesa-dri*
  libgl1-amdgpu-mesa-dri:i386* libgl1-amdgpu-mesa-glx* libgl1-amdgpu-mesa-glx:i386* libglapi-amdgpu-mesa* libglapi-amdgpu-mesa:i386* libllvm19.1-amdgpu* libllvm19.1-amdgpu:i386* libwayland-amdgpu-client0* libwayland-amdgpu-client0:i386*
  libwayland-amdgpu-egl1:i386* libwayland-amdgpu-server0* libwayland-amdgpu-server0:i386* libxatracker2-amdgpu* libxatracker2-amdgpu:i386* mesa-amdgpu-libgallium* mesa-amdgpu-libgallium:i386* mesa-amdgpu-va-drivers*
  mesa-amdgpu-va-drivers:i386* mesa-amdgpu-vdpau-drivers* xserver-xorg-amdgpu-video-amdgpu*
0 upgraded, 0 newly installed, 42 to remove and 0 not upgraded.
After this operation, 907 MB disk space will be freed.
Do you want to continue? [Y/n] 
(Reading database ... 532772 files and directories currently installed.)
Removing amdgpu-lib32 (1:6.3.60302-2109964.24.04) ...
Removing amdgpu-lib (1:6.3.60302-2109964.24.04) ...
Removing xserver-xorg-amdgpu-video-amdgpu (1:22.0.0.60302-2109964.24.04) ...
Removing libegl1-amdgpu-mesa-drivers:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing libegl1-amdgpu-mesa:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing libgl1-amdgpu-mesa-dri:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing mesa-amdgpu-va-drivers:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing libxatracker2-amdgpu:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing amdgpu-multimedia (1:6.3.60302-2109964.24.04) ...
Removing mesa-amdgpu-vdpau-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libgbm1-amdgpu:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing libwayland-amdgpu-server0:i386 (1.23.0.60302-2109964.24.04) ...
Removing amdgpu-dkms (1:6.10.5.60302-2109964.24.04) ...
Module amdgpu-6.10.5-2109964.24.04 for kernel 6.8.0-52-generic (amd64).
Before uninstall, this module version was ACTIVE on this kernel.

amdgpu.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.8.0-52-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amdttm.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.8.0-52-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amdkcl.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.8.0-52-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amd-sched.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.8.0-52-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amddrm_ttm_helper.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.8.0-52-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amddrm_buddy.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.8.0-52-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amdxcp.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.8.0-52-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.
depmod....
Deleting module amdgpu-6.10.5-2109964.24.04 completely from the DKMS tree.
update-initramfs: Generating /boot/initrd.img-6.8.0-52-generic
I: The initramfs will attempt to resume from /dev/nvme0n1p3
I: (UUID=b8ddbe21-2dc9-4ae9-b190-2a13150b5035)
I: Set the RESUME variable to override this.
Removing amdgpu-dkms-firmware (1:6.10.5.60302-2109964.24.04) ...
Removing amdgpu-install (6.3.60302-2109964.24.04) ...
Removing libdrm-amdgpu-dev:amd64 (1:2.4.123.60302-2109964.24.04) ...
Removing libegl1-amdgpu-mesa-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libegl1-amdgpu-mesa:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libxatracker2-amdgpu:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libgl1-amdgpu-mesa-glx:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libgl1-amdgpu-mesa-dri:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libgbm1-amdgpu:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libgl1-amdgpu-mesa-glx:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing libwayland-amdgpu-client0:amd64 (1.23.0.60302-2109964.24.04) ...
Removing libwayland-amdgpu-client0:i386 (1.23.0.60302-2109964.24.04) ...
Removing libwayland-amdgpu-egl1:i386 (1.23.0.60302-2109964.24.04) ...
Removing libwayland-amdgpu-server0:amd64 (1.23.0.60302-2109964.24.04) ...
Removing mesa-amdgpu-va-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing mesa-amdgpu-libgallium:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing libdrm-amdgpu-amdgpu1:i386 (1:2.4.123.60302-2109964.24.04) ...
Removing mesa-amdgpu-libgallium:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libdrm-amdgpu-amdgpu1:amd64 (1:2.4.123.60302-2109964.24.04) ...
Removing libdrm-amdgpu-common (1.0.0.60302-2111876.22.04) ...
Removing libdrm-amdgpu-radeon1:i386 (1:2.4.123.60302-2109964.24.04) ...
Removing libdrm-amdgpu-radeon1:amd64 (1:2.4.123.60302-2109964.24.04) ...
Removing libdrm2-amdgpu:amd64 (1:2.4.123.60302-2109964.24.04) ...
Removing libglapi-amdgpu-mesa:amd64 (1:24.3.0.60302-2109964.24.04) ...
Removing libglapi-amdgpu-mesa:i386 (1:24.3.0.60302-2109964.24.04) ...
Removing libllvm19.1-amdgpu:amd64 (1:19.1.60302-2109964.24.04) ...
Removing libllvm19.1-amdgpu:i386 (1:19.1.60302-2109964.24.04) ...
Removing libdrm2-amdgpu:i386 (1:2.4.123.60302-2109964.24.04) ...
Removing amdgpu-core (1:6.3.60302-2109964.24.04) ...
Processing triggers for libc-bin (2.39-0ubuntu8.4) ...
(Reading database ... 528404 files and directories currently installed.)
Purging configuration files for amdgpu-dkms (1:6.10.5.60302-2109964.24.04) ...
Purging configuration files for amdgpu-install (6.3.60302-2109964.24.04) ...
mcon@ikea:~$ sudo apt autoremove
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages will be REMOVED:
  valgrind
0 upgraded, 0 newly installed, 1 to remove and 3 not upgraded.
After this operation, 78,8 MB disk space will be freed.
Do you want to continue? [Y/n] 
(Reading database ... 528395 files and directories currently installed.)
Removing valgrind (1:3.22.0-0ubuntu3) ...
Processing triggers for man-db (2.12.0-4build2) ...
mcon@ikea:~$ sudo reboot

Broadcast message from root@ikea on pts/3 (Mon 2025-02-10 19:10:18 CET):

The system will reboot now!

mcon@ikea:~$ Read from remote host ikea.lan: Connection reset by peer
Connection to ikea.lan closed.
client_loop: send disconnect: Broken pipe
mcon@cinderella:~/Documents/Mauro$ ssh ikea 

Last login: Mon Feb 10 19:05:19 2025 from 192.168.7.12
mcon@ikea:~$ mkdir AMD
mcon@ikea:~$ cd AMD
mcon@ikea:~/AMD$ sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.2/ubuntu/noble/amdgpu-install_6.3.60302-1_all.deb
sudo apt install ./amdgpu-install_6.3.60302-1_all.deb
Hit:1 https://ubuntu.mirror.garr.it/ubuntu noble InRelease
Hit:2 https://ubuntu.mirror.garr.it/ubuntu noble-updates InRelease
Hit:3 https://ubuntu.mirror.garr.it/ubuntu noble-backports InRelease
Ign:4 https://linuxmint.mirror.garr.it/linuxmint/packages xia InRelease
Hit:5 https://linuxmint.mirror.garr.it/linuxmint/packages xia Release
Get:6 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
Get:8 http://security.ubuntu.com/ubuntu noble-security/main amd64 Components [8.984 B]
Get:9 http://security.ubuntu.com/ubuntu noble-security/restricted amd64 Components [208 B]
Get:10 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Components [51,9 kB]
Get:11 http://security.ubuntu.com/ubuntu noble-security/multiverse amd64 Components [208 B]
Fetched 187 kB in 1s (201 kB/s)             
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
3 packages can be upgraded. Run 'apt list --upgradable' to see them.
--2025-02-10 19:26:46--  https://repo.radeon.com/amdgpu-install/6.3.2/ubuntu/noble/amdgpu-install_6.3.60302-1_all.deb
Resolving repo.radeon.com (repo.radeon.com)... 2.21.14.178, 2.21.14.224, 2001:41a8:28:5::214:fc63, ...
Connecting to repo.radeon.com (repo.radeon.com)|2.21.14.178|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 16988 (17K) [application/octet-stream]
Saving to: ‘amdgpu-install_6.3.60302-1_all.deb’

amdgpu-install_6.3.60302-1_all.deb                           100%[==============================================================================================================================================>]  16,59K  --.-KB/s    in 0s      

2025-02-10 19:26:46 (55,4 MB/s) - ‘amdgpu-install_6.3.60302-1_all.deb’ saved [16988/16988]

Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'amdgpu-install' instead of './amdgpu-install_6.3.60302-1_all.deb'
The following NEW packages will be installed:
  amdgpu-install
0 upgraded, 1 newly installed, 0 to remove and 3 not upgraded.
Need to get 0 B/17,0 kB of archives.
After this operation, 74,8 kB of additional disk space will be used.
Get:1 /home/mcon/AMD/amdgpu-install_6.3.60302-1_all.deb amdgpu-install all 6.3.60302-2109964.24.04 [17,0 kB]
Selecting previously unselected package amdgpu-install.
(Reading database ... 528023 files and directories currently installed.)
Preparing to unpack .../amdgpu-install_6.3.60302-1_all.deb ...
Unpacking amdgpu-install (6.3.60302-2109964.24.04) ...
Setting up amdgpu-install (6.3.60302-2109964.24.04) ...
mcon@ikea:~/AMD$ sudo amdgpu-install --list-usecase
If --usecase option is not present, the default selection is
"dkms,graphics,opencl,hip"
Available use cases:
dkms            (to only install the kernel mode driver)
  - Kernel mode driver (included in all usecases)
graphics        (for users of graphics applications)
  - Open source Mesa 3D graphics and multimedia libraries
multimedia      (for users of open source multimedia)
  - Open source Mesa 3D multimedia libraries
workstation     (for users of legacy WS applications)
  - Open source multimedia libraries
  - Closed source (legacy) OpenGL
rocm            (for users and developers requiring full ROCm stack)
  - OpenCL (ROCr/KFD based) runtime
  - HIP runtimes
  - Machine learning framework
  - All ROCm libraries and applications
wsl             (for using ROCm in a WSL context)
  - ROCr WSL runtime library (Ubuntu 22.04 only)
rocmdev         (for developers requiring ROCm runtime and
                profiling/debugging tools)
  - HIP runtimes
  - OpenCL runtime
  - Profiler, Tracer and Debugger tools
rocmdevtools    (for developers requiring ROCm profiling/debugging tools)
  - Profiler, Tracer and Debugger tools
amf             (for users of AMF based multimedia)
  - AMF closed source multimedia library
lrt             (for users of applications requiring ROCm runtime)
  - ROCm Compiler and device libraries
  - ROCr runtime and thunk
opencl          (for users of applications requiring OpenCL on Vega or later
                products)
  - ROCr based OpenCL
  - ROCm Language runtime
openclsdk       (for application developers requiring ROCr based OpenCL)
  - ROCr based OpenCL
  - ROCm Language runtime
  - development and SDK files for ROCr based OpenCL
hip             (for users of HIP runtime on AMD products)
  - HIP runtimes
hiplibsdk       (for application developers requiring HIP on AMD products)
  - HIP runtimes
  - ROCm math libraries
  - HIP development libraries
openmpsdk       (for users of openmp/flang on AMD products)
  - OpenMP runtime and devel packages
mllib           (for users executing machine learning workloads)
  - MIOpen hip/tensile libraries
  - Clang OpenCL
  - MIOpen kernels
mlsdk           (for developers executing machine learning workloads)
  - MIOpen development libraries
  - Clang OpenCL development libraries
  - MIOpen kernels
asan            (for users of ASAN enabled ROCm packages)
  - ASAN enabled OpenCL (ROCr/KFD based) runtime
  - ASAN enabled HIP runtimes
  - ASAN enabled Machine learning framework
  - ASAN enabled ROCm libraries

mcon@ikea:~/AMD$ amdgpu-install -y --usecase=graphics,rocm
Get:1 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble InRelease [5.465 B]
Hit:2 https://ubuntu.mirror.garr.it/ubuntu noble InRelease                                             
Ign:3 https://linuxmint.mirror.garr.it/linuxmint/packages xia InRelease
Get:4 https://repo.radeon.com/rocm/apt/6.3.2 noble InRelease [2.605 B]
Hit:5 https://ubuntu.mirror.garr.it/ubuntu noble-updates InRelease                                     
Hit:6 https://linuxmint.mirror.garr.it/linuxmint/packages xia Release
Hit:7 https://ubuntu.mirror.garr.it/ubuntu noble-backports InRelease
Get:8 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main amd64 Packages [14,6 kB]
Hit:9 http://security.ubuntu.com/ubuntu noble-security InRelease     
Get:10 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main i386 Packages [12,3 kB]
Get:11 https://repo.radeon.com/rocm/apt/6.3.2 noble/main amd64 Packages [60,0 kB]
Fetched 94,9 kB in 1s (167 kB/s)
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
rocm is already the newest version (6.3.2.60302-66~24.04).
linux-headers-6.8.0-52-generic is already the newest version (6.8.0-52.53).
The following additional packages will be installed:
  amdgpu-core amdgpu-dkms-firmware amdgpu-multimedia libdrm-amdgpu-amdgpu1 libdrm-amdgpu-amdgpu1:i386 libdrm-amdgpu-common libdrm-amdgpu-radeon1 libdrm-amdgpu-radeon1:i386 libdrm2-amdgpu libdrm2-amdgpu:i386 libegl1-amdgpu-mesa
  libegl1-amdgpu-mesa:i386 libegl1-amdgpu-mesa-drivers libegl1-amdgpu-mesa-drivers:i386 libgbm1-amdgpu libgbm1-amdgpu:i386 libgl1-amdgpu-mesa-dri libgl1-amdgpu-mesa-dri:i386 libgl1-amdgpu-mesa-glx libgl1-amdgpu-mesa-glx:i386
  libglapi-amdgpu-mesa libglapi-amdgpu-mesa:i386 libllvm19.1-amdgpu libllvm19.1-amdgpu:i386 libwayland-amdgpu-client0 libwayland-amdgpu-client0:i386 libwayland-amdgpu-server0 libwayland-amdgpu-server0:i386 libxatracker2-amdgpu
  libxatracker2-amdgpu:i386 mesa-amdgpu-libgallium mesa-amdgpu-libgallium:i386 mesa-amdgpu-va-drivers mesa-amdgpu-va-drivers:i386 mesa-amdgpu-vdpau-drivers xserver-xorg-amdgpu-video-amdgpu
The following NEW packages will be installed:
  amdgpu-core amdgpu-dkms amdgpu-dkms-firmware amdgpu-lib amdgpu-lib32 amdgpu-multimedia libdrm-amdgpu-amdgpu1 libdrm-amdgpu-amdgpu1:i386 libdrm-amdgpu-common libdrm-amdgpu-radeon1 libdrm-amdgpu-radeon1:i386 libdrm2-amdgpu libdrm2-amdgpu:i386
  libegl1-amdgpu-mesa libegl1-amdgpu-mesa:i386 libegl1-amdgpu-mesa-drivers libegl1-amdgpu-mesa-drivers:i386 libgbm1-amdgpu libgbm1-amdgpu:i386 libgl1-amdgpu-mesa-dri libgl1-amdgpu-mesa-dri:i386 libgl1-amdgpu-mesa-glx
  libgl1-amdgpu-mesa-glx:i386 libglapi-amdgpu-mesa libglapi-amdgpu-mesa:i386 libllvm19.1-amdgpu libllvm19.1-amdgpu:i386 libwayland-amdgpu-client0 libwayland-amdgpu-client0:i386 libwayland-amdgpu-server0 libwayland-amdgpu-server0:i386
  libxatracker2-amdgpu libxatracker2-amdgpu:i386 mesa-amdgpu-libgallium mesa-amdgpu-libgallium:i386 mesa-amdgpu-va-drivers mesa-amdgpu-va-drivers:i386 mesa-amdgpu-vdpau-drivers xserver-xorg-amdgpu-video-amdgpu
0 upgraded, 39 newly installed, 0 to remove and 0 not upgraded.
Need to get 15,3 MB/97,7 MB of archives.
After this operation, 906 MB of additional disk space will be used.
Get:1 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main i386 libdrm2-amdgpu i386 1:2.4.123.60302-2109964.24.04 [39,2 kB]
Get:2 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main i386 libdrm-amdgpu-amdgpu1 i386 1:2.4.123.60302-2109964.24.04 [25,0 kB]
Get:3 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main i386 libdrm-amdgpu-radeon1 i386 1:2.4.123.60302-2109964.24.04 [25,1 kB]
Get:4 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main amd64 libdrm2-amdgpu amd64 1:2.4.123.60302-2109964.24.04 [37,7 kB]
Get:5 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main amd64 libdrm-amdgpu-amdgpu1 amd64 1:2.4.123.60302-2109964.24.04 [21,5 kB]
Get:6 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main amd64 libdrm-amdgpu-radeon1 amd64 1:2.4.123.60302-2109964.24.04 [24,4 kB]
Get:7 https://repo.radeon.com/amdgpu/6.3.2/ubuntu noble/main amd64 amdgpu-dkms-firmware all 1:6.10.5.60302-2109964.24.04 [15,1 MB]
Fetched 15,3 MB in 0s (33,6 MB/s)              
Extracting templates from packages: 100%
Selecting previously unselected package amdgpu-core.
(Reading database ... 528041 files and directories currently installed.)
Preparing to unpack .../00-amdgpu-core_1%3a6.3.60302-2109964.24.04_all.deb ...
Unpacking amdgpu-core (1:6.3.60302-2109964.24.04) ...
Selecting previously unselected package libdrm2-amdgpu:i386.
Preparing to unpack .../01-libdrm2-amdgpu_1%3a2.4.123.60302-2109964.24.04_i386.deb ...
Unpacking libdrm2-amdgpu:i386 (1:2.4.123.60302-2109964.24.04) ...
Selecting previously unselected package libdrm-amdgpu-common.
Preparing to unpack .../02-libdrm-amdgpu-common_1.0.0.60302-2111876.22.04_all.deb ...
Unpacking libdrm-amdgpu-common (1.0.0.60302-2111876.22.04) ...
Selecting previously unselected package libdrm-amdgpu-amdgpu1:i386.
Preparing to unpack .../03-libdrm-amdgpu-amdgpu1_1%3a2.4.123.60302-2109964.24.04_i386.deb ...
Unpacking libdrm-amdgpu-amdgpu1:i386 (1:2.4.123.60302-2109964.24.04) ...
Selecting previously unselected package libdrm-amdgpu-radeon1:i386.
Preparing to unpack .../04-libdrm-amdgpu-radeon1_1%3a2.4.123.60302-2109964.24.04_i386.deb ...
Unpacking libdrm-amdgpu-radeon1:i386 (1:2.4.123.60302-2109964.24.04) ...
Selecting previously unselected package libglapi-amdgpu-mesa:i386.
Preparing to unpack .../05-libglapi-amdgpu-mesa_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking libglapi-amdgpu-mesa:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libllvm19.1-amdgpu:i386.
Preparing to unpack .../06-libllvm19.1-amdgpu_1%3a19.1.60302-2109964.24.04_i386.deb ...
Unpacking libllvm19.1-amdgpu:i386 (1:19.1.60302-2109964.24.04) ...
Selecting previously unselected package mesa-amdgpu-libgallium:i386.
Preparing to unpack .../07-mesa-amdgpu-libgallium_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking mesa-amdgpu-libgallium:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package mesa-amdgpu-va-drivers:i386.
Preparing to unpack .../08-mesa-amdgpu-va-drivers_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking mesa-amdgpu-va-drivers:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libwayland-amdgpu-server0:i386.
Preparing to unpack .../09-libwayland-amdgpu-server0_1.23.0.60302-2109964.24.04_i386.deb ...
Unpacking libwayland-amdgpu-server0:i386 (1.23.0.60302-2109964.24.04) ...
Selecting previously unselected package libgbm1-amdgpu:i386.
Preparing to unpack .../10-libgbm1-amdgpu_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking libgbm1-amdgpu:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up amdgpu-core (1:6.3.60302-2109964.24.04) ...
Setting up libdrm2-amdgpu:i386 (1:2.4.123.60302-2109964.24.04) ...
Setting up libdrm-amdgpu-common (1.0.0.60302-2111876.22.04) ...
Setting up libdrm-amdgpu-amdgpu1:i386 (1:2.4.123.60302-2109964.24.04) ...
Setting up libdrm-amdgpu-radeon1:i386 (1:2.4.123.60302-2109964.24.04) ...
Setting up libglapi-amdgpu-mesa:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up libllvm19.1-amdgpu:i386 (1:19.1.60302-2109964.24.04) ...
Setting up mesa-amdgpu-libgallium:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up mesa-amdgpu-va-drivers:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libgl1-amdgpu-mesa-dri:i386.
(Reading database ... 528108 files and directories currently installed.)
Preparing to unpack .../0-libgl1-amdgpu-mesa-dri_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking libgl1-amdgpu-mesa-dri:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libdrm2-amdgpu:amd64.
Preparing to unpack .../1-libdrm2-amdgpu_1%3a2.4.123.60302-2109964.24.04_amd64.deb ...
Unpacking libdrm2-amdgpu:amd64 (1:2.4.123.60302-2109964.24.04) ...
Selecting previously unselected package libdrm-amdgpu-amdgpu1:amd64.
Preparing to unpack .../2-libdrm-amdgpu-amdgpu1_1%3a2.4.123.60302-2109964.24.04_amd64.deb ...
Unpacking libdrm-amdgpu-amdgpu1:amd64 (1:2.4.123.60302-2109964.24.04) ...
Selecting previously unselected package libdrm-amdgpu-radeon1:amd64.
Preparing to unpack .../3-libdrm-amdgpu-radeon1_1%3a2.4.123.60302-2109964.24.04_amd64.deb ...
Unpacking libdrm-amdgpu-radeon1:amd64 (1:2.4.123.60302-2109964.24.04) ...
Selecting previously unselected package libglapi-amdgpu-mesa:amd64.
Preparing to unpack .../4-libglapi-amdgpu-mesa_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking libglapi-amdgpu-mesa:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libllvm19.1-amdgpu:amd64.
Preparing to unpack .../5-libllvm19.1-amdgpu_1%3a19.1.60302-2109964.24.04_amd64.deb ...
Unpacking libllvm19.1-amdgpu:amd64 (1:19.1.60302-2109964.24.04) ...
Selecting previously unselected package mesa-amdgpu-libgallium:amd64.
Preparing to unpack .../6-mesa-amdgpu-libgallium_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking mesa-amdgpu-libgallium:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package mesa-amdgpu-va-drivers:amd64.
Preparing to unpack .../7-mesa-amdgpu-va-drivers_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking mesa-amdgpu-va-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libwayland-amdgpu-server0:amd64.
Preparing to unpack .../8-libwayland-amdgpu-server0_1.23.0.60302-2109964.24.04_amd64.deb ...
Unpacking libwayland-amdgpu-server0:amd64 (1.23.0.60302-2109964.24.04) ...
Selecting previously unselected package libgbm1-amdgpu:amd64.
Preparing to unpack .../9-libgbm1-amdgpu_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking libgbm1-amdgpu:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libdrm2-amdgpu:amd64 (1:2.4.123.60302-2109964.24.04) ...
Setting up libdrm-amdgpu-amdgpu1:amd64 (1:2.4.123.60302-2109964.24.04) ...
Setting up libdrm-amdgpu-radeon1:amd64 (1:2.4.123.60302-2109964.24.04) ...
Setting up libglapi-amdgpu-mesa:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libllvm19.1-amdgpu:amd64 (1:19.1.60302-2109964.24.04) ...
Setting up mesa-amdgpu-libgallium:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up mesa-amdgpu-va-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libgl1-amdgpu-mesa-dri:amd64.
(Reading database ... 528150 files and directories currently installed.)
Preparing to unpack .../00-libgl1-amdgpu-mesa-dri_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking libgl1-amdgpu-mesa-dri:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package mesa-amdgpu-vdpau-drivers:amd64.
Preparing to unpack .../01-mesa-amdgpu-vdpau-drivers_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking mesa-amdgpu-vdpau-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package amdgpu-dkms-firmware.
Preparing to unpack .../02-amdgpu-dkms-firmware_1%3a6.10.5.60302-2109964.24.04_all.deb ...
Unpacking amdgpu-dkms-firmware (1:6.10.5.60302-2109964.24.04) ...
Selecting previously unselected package amdgpu-dkms.
Preparing to unpack .../03-amdgpu-dkms_1%3a6.10.5.60302-2109964.24.04_all.deb ...
Unpacking amdgpu-dkms (1:6.10.5.60302-2109964.24.04) ...
Selecting previously unselected package amdgpu-multimedia.
Preparing to unpack .../04-amdgpu-multimedia_1%3a6.3.60302-2109964.24.04_amd64.deb ...
Unpacking amdgpu-multimedia (1:6.3.60302-2109964.24.04) ...
Selecting previously unselected package libwayland-amdgpu-client0:amd64.
Preparing to unpack .../05-libwayland-amdgpu-client0_1.23.0.60302-2109964.24.04_amd64.deb ...
Unpacking libwayland-amdgpu-client0:amd64 (1.23.0.60302-2109964.24.04) ...
Selecting previously unselected package libxatracker2-amdgpu:amd64.
Preparing to unpack .../06-libxatracker2-amdgpu_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking libxatracker2-amdgpu:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libegl1-amdgpu-mesa:amd64.
Preparing to unpack .../07-libegl1-amdgpu-mesa_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking libegl1-amdgpu-mesa:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libegl1-amdgpu-mesa-drivers:amd64.
Preparing to unpack .../08-libegl1-amdgpu-mesa-drivers_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking libegl1-amdgpu-mesa-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libgl1-amdgpu-mesa-glx:amd64.
Preparing to unpack .../09-libgl1-amdgpu-mesa-glx_1%3a24.3.0.60302-2109964.24.04_amd64.deb ...
Unpacking libgl1-amdgpu-mesa-glx:amd64 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package xserver-xorg-amdgpu-video-amdgpu.
Preparing to unpack .../10-xserver-xorg-amdgpu-video-amdgpu_1%3a22.0.0.60302-2109964.24.04_amd64.deb ...
Unpacking xserver-xorg-amdgpu-video-amdgpu (1:22.0.0.60302-2109964.24.04) ...
Selecting previously unselected package amdgpu-lib.
Preparing to unpack .../11-amdgpu-lib_1%3a6.3.60302-2109964.24.04_amd64.deb ...
Unpacking amdgpu-lib (1:6.3.60302-2109964.24.04) ...
Selecting previously unselected package libwayland-amdgpu-client0:i386.
Preparing to unpack .../12-libwayland-amdgpu-client0_1.23.0.60302-2109964.24.04_i386.deb ...
Unpacking libwayland-amdgpu-client0:i386 (1.23.0.60302-2109964.24.04) ...
Selecting previously unselected package libxatracker2-amdgpu:i386.
Preparing to unpack .../13-libxatracker2-amdgpu_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking libxatracker2-amdgpu:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libegl1-amdgpu-mesa:i386.
Preparing to unpack .../14-libegl1-amdgpu-mesa_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking libegl1-amdgpu-mesa:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libegl1-amdgpu-mesa-drivers:i386.
Preparing to unpack .../15-libegl1-amdgpu-mesa-drivers_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking libegl1-amdgpu-mesa-drivers:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package libgl1-amdgpu-mesa-glx:i386.
Preparing to unpack .../16-libgl1-amdgpu-mesa-glx_1%3a24.3.0.60302-2109964.24.04_i386.deb ...
Unpacking libgl1-amdgpu-mesa-glx:i386 (1:24.3.0.60302-2109964.24.04) ...
Selecting previously unselected package amdgpu-lib32.
Preparing to unpack .../17-amdgpu-lib32_1%3a6.3.60302-2109964.24.04_amd64.deb ...
Unpacking amdgpu-lib32 (1:6.3.60302-2109964.24.04) ...
Setting up libxatracker2-amdgpu:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libxatracker2-amdgpu:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up libwayland-amdgpu-server0:amd64 (1.23.0.60302-2109964.24.04) ...
Setting up libwayland-amdgpu-server0:i386 (1.23.0.60302-2109964.24.04) ...
Setting up libgbm1-amdgpu:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libgbm1-amdgpu:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up mesa-amdgpu-vdpau-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up amdgpu-multimedia (1:6.3.60302-2109964.24.04) ...
Setting up amdgpu-dkms-firmware (1:6.10.5.60302-2109964.24.04) ...
Setting up xserver-xorg-amdgpu-video-amdgpu (1:22.0.0.60302-2109964.24.04) ...
Setting up libwayland-amdgpu-client0:amd64 (1.23.0.60302-2109964.24.04) ...
Setting up libwayland-amdgpu-client0:i386 (1.23.0.60302-2109964.24.04) ...
Setting up libgl1-amdgpu-mesa-glx:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libgl1-amdgpu-mesa-glx:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up libgl1-amdgpu-mesa-dri:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libgl1-amdgpu-mesa-dri:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up amdgpu-dkms (1:6.10.5.60302-2109964.24.04) ...
Loading new amdgpu-6.10.5-2109964.24.04 DKMS files...
Building for 6.8.0-52-generic
Building for architecture amd64
Building initial module for 6.8.0-52-generic
Done.
Forcing installation of amdgpu

amdgpu.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.8.0-52-generic/updates/dkms/

amdttm.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.8.0-52-generic/updates/dkms/

amdkcl.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.8.0-52-generic/updates/dkms/

amd-sched.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.8.0-52-generic/updates/dkms/

amddrm_ttm_helper.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.8.0-52-generic/updates/dkms/

amddrm_buddy.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.8.0-52-generic/updates/dkms/

amdxcp.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.8.0-52-generic/updates/dkms/
depmod....
update-initramfs: Generating /boot/initrd.img-6.8.0-52-generic
I: The initramfs will attempt to resume from /dev/nvme0n1p3
I: (UUID=b8ddbe21-2dc9-4ae9-b190-2a13150b5035)
I: Set the RESUME variable to override this.
Setting up libegl1-amdgpu-mesa:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libegl1-amdgpu-mesa:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up libegl1-amdgpu-mesa-drivers:amd64 (1:24.3.0.60302-2109964.24.04) ...
Setting up libegl1-amdgpu-mesa-drivers:i386 (1:24.3.0.60302-2109964.24.04) ...
Setting up amdgpu-lib (1:6.3.60302-2109964.24.04) ...
Setting up amdgpu-lib32 (1:6.3.60302-2109964.24.04) ...
Processing triggers for libc-bin (2.39-0ubuntu8.4) ...
mcon@ikea:~/AMD$ sudo reboot

Broadcast message from root@ikea on pts/1 (Mon 2025-02-10 19:31:20 CET):

The system will reboot now!

mcon@ikea:~/AMD$ Read from remote host ikea.lan: Connection reset by peer
Connection to ikea.lan closed.
client_loop: send disconnect: Broken pipe
mcon@cinderella:~/Documents/Mauro$ ssh ikea 

Last login: Mon Feb 10 19:25:27 2025 from 192.168.7.12
mcon@ikea:~$ id
uid=1000(mcon) gid=1000(mcon) groups=1000(mcon),4(adm),24(cdrom),27(sudo),30(dip),44(video),46(plugdev),100(users),105(lpadmin),125(sambashare),127(docker),992(render)
mcon@ikea:~$ dkms status
amdgpu/6.10.5-2109964.24.04, 6.8.0-52-generic, amd64: installed
amdgpu/6.2.4-1664922.22.04: added
mcon@ikea:~$ rocminfo
ROCk module version 6.10.5 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
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
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
  Max Clock Freq. (MHz):   3400                               
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
      Size:                    32781072(0x1f43310) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32781072(0x1f43310) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32781072(0x1f43310) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32781072(0x1f43310) KB             
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
  Marketing Name:          AMD Radeon™ RX 7600 XT           
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2493                               
  BDFID:                   11520                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 412                                
  SDMA engine uCode::      21                                 
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
*** Done ***             
mcon@ikea:~$ clinfo
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 1
  Device Type:					 CL_DEVICE_TYPE_GPU
  Vendor ID:					 1002h
  Board name:					 AMD Radeon™ RX 7600 XT
  Device Topology:				 PCI[ B#45, D#0, F#0 ]
  Max compute units:				 16
  Max work items dimensions:			 3
    Max work items[0]:				 1024
    Max work items[1]:				 1024
    Max work items[2]:				 1024
  Max work group size:				 256
  Preferred vector width char:			 4
  Preferred vector width short:			 2
  Preferred vector width int:			 1
  Preferred vector width long:			 1
  Preferred vector width float:			 1
  Preferred vector width double:		 1
  Native vector width char:			 4
  Native vector width short:			 2
  Native vector width int:			 1
  Native vector width long:			 1
  Native vector width float:			 1
  Native vector width double:			 1
  Max clock frequency:				 2493Mhz
  Address bits:					 64
  Max memory allocation:			 14588628168
  Image support:				 Yes
  Max number of images read arguments:		 128
  Max number of images write arguments:		 8
  Max image 2D width:				 16384
  Max image 2D height:				 16384
  Max image 3D width:				 16384
  Max image 3D height:				 16384
  Max image 3D depth:				 8192
  Max samplers within kernel:			 16
  Max size of kernel argument:			 1024
  Alignment (bits) of base address:		 2048
  Minimum alignment (bytes) for any datatype:	 128
  Single precision floating point capability
    Denorms:					 Yes
    Quiet NaNs:					 Yes
    Round to nearest even:			 Yes
    Round to zero:				 Yes
    Round to +ve and infinity:			 Yes
    IEEE754-2008 fused multiply-add:		 Yes
  Cache type:					 Read/Write
  Cache line size:				 64
  Cache size:					 32768
  Global memory size:				 17163091968
  Constant buffer size:				 14588628168
  Max number of constant args:			 8
  Local memory type:				 Local
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 1703726280
  Max global variable size:			 14588628168
  Max global variable preferred total size:	 17163091968
  Max read/write image args:			 64
  Max on device events:				 1024
  Queue on device max size:			 8388608
  Max on device queues:				 1
  Queue on device preferred size:		 262144
  SVM capabilities:				 
    Coarse grain buffer:			 Yes
    Fine grain buffer:				 Yes
    Fine grain system:				 No
    Atomics:					 No
  Preferred platform atomic alignment:		 0
  Preferred global atomic alignment:		 0
  Preferred local atomic alignment:		 0
  Kernel Preferred work group size multiple:	 32
  Error correction support:			 0
  Unified memory for Host and Device:		 0
  Profiling timer resolution:			 1
  Device endianess:				 Little
  Available:					 Yes
  Compiler available:				 Yes
  Execution capabilities:				 
    Execute OpenCL kernels:			 Yes
    Execute native function:			 No
  Queue on Host properties:				 
    Out-of-Order:				 No
    Profiling :					 Yes
  Queue on Device properties:				 
    Out-of-Order:				 Yes
    Profiling :					 Yes
  Platform ID:					 0x78d4efff0ff0
  Name:						 gfx1102
  Vendor:					 Advanced Micro Devices, Inc.
  Device OpenCL C version:			 OpenCL C 2.0 
  Driver version:				 3635.0 (HSA1.1,LC)
  Profile:					 FULL_PROFILE
  Version:					 OpenCL 2.0 
  Extensions:					 cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 


mcon@ikea:~$ cd AMD
mcon@ikea:~/AMD$ python3.10 -m venv .venv
mcon@ikea:~/AMD$ source .venv/bin/activate
(.venv) mcon@ikea:~/AMD$ 
logout
Connection to ikea.lan closed.
mcon@cinderella:~/Documents/Mauro$ ssh ikea 

Last login: Mon Feb 10 19:43:46 2025 from 192.168.7.12
mcon@ikea:~$ cd AMD
mcon@ikea:~/AMD$ rm -r venv
rm: cannot remove 'venv': No such file or directory
mcon@ikea:~/AMD$ rm -r .venv
mcon@ikea:~/AMD$ python3.11 -m venv .venv
Command 'python3.11' not found, but can be installed with:
sudo apt install python3.11
mcon@ikea:~/AMD$ sudo apt install python3.11
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package python3.11
E: Couldn't find any package by glob 'python3.11'
mcon@ikea:~/AMD$ python3.11 -m venv .venv
mcon@ikea:~/AMD$ source .venv/bin/activate
(.venv) mcon@ikea:~/AMD$ pip install invokeai --extra-index-url https://download.pytorch.org/whl/nightly/rocm6.3
Looking in indexes: https://pypi.org/simple, https://download.pytorch.org/whl/nightly/rocm6.3
Collecting invokeai
  Using cached InvokeAI-5.6.0-py3-none-any.whl.metadata (24 kB)
Collecting accelerate==1.0.1 (from invokeai)
  Using cached accelerate-1.0.1-py3-none-any.whl.metadata (19 kB)
Collecting bitsandbytes==0.45.0 (from invokeai)
  Using cached bitsandbytes-0.45.0-py3-none-manylinux_2_24_x86_64.whl.metadata (2.9 kB)
Collecting clip_anytorch==2.6.0 (from invokeai)
  Using cached clip_anytorch-2.6.0-py3-none-any.whl.metadata (8.4 kB)
Collecting compel==2.0.2 (from invokeai)
  Using cached compel-2.0.2-py3-none-any.whl.metadata (12 kB)
Collecting controlnet-aux==0.0.7 (from invokeai)
  Using cached controlnet_aux-0.0.7-py3-none-any.whl
Collecting diffusers==0.31.0 (from diffusers[torch]==0.31.0->invokeai)
  Using cached diffusers-0.31.0-py3-none-any.whl.metadata (18 kB)
Collecting gguf==0.10.0 (from invokeai)
  Using cached gguf-0.10.0-py3-none-any.whl.metadata (3.5 kB)
Collecting invisible-watermark==0.2.0 (from invokeai)
  Using cached invisible_watermark-0.2.0-py3-none-any.whl.metadata (8.2 kB)
Collecting mediapipe==0.10.14 (from invokeai)
  Using cached mediapipe-0.10.14-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.7 kB)
Collecting numpy<2.0.0 (from invokeai)
  Using cached https://download.pytorch.org/whl/nightly/numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (18.3 MB)
Collecting onnx==1.16.1 (from invokeai)
  Using cached onnx-1.16.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (16 kB)
Collecting onnxruntime==1.19.2 (from invokeai)
  Using cached onnxruntime-1.19.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (4.5 kB)
Collecting opencv-python==4.9.0.80 (from invokeai)
  Using cached opencv_python-4.9.0.80-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (20 kB)
Collecting pytorch-lightning==2.1.3 (from invokeai)
  Using cached pytorch_lightning-2.1.3-py3-none-any.whl.metadata (21 kB)
Collecting safetensors==0.4.3 (from invokeai)
  Using cached https://download.pytorch.org/whl/nightly/safetensors-0.4.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
Collecting sentencepiece==0.2.0 (from invokeai)
  Using cached https://download.pytorch.org/whl/nightly/sentencepiece-0.2.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.3 MB)
Collecting spandrel==0.3.4 (from invokeai)
  Using cached spandrel-0.3.4-py3-none-any.whl.metadata (14 kB)
Collecting timm==0.6.13 (from invokeai)
  Using cached timm-0.6.13-py3-none-any.whl.metadata (38 kB)
Collecting torch<2.5.0 (from invokeai)
  Using cached torch-2.4.1-cp311-cp311-manylinux1_x86_64.whl.metadata (26 kB)
Collecting torchmetrics (from invokeai)
  Using cached torchmetrics-1.6.1-py3-none-any.whl.metadata (21 kB)
Collecting torchsde (from invokeai)
  Using cached torchsde-0.2.6-py3-none-any.whl.metadata (5.3 kB)
Collecting torchvision (from invokeai)
  Downloading torchvision-0.21.0-cp311-cp311-manylinux1_x86_64.whl.metadata (6.1 kB)
Collecting transformers==4.46.3 (from invokeai)
  Using cached transformers-4.46.3-py3-none-any.whl.metadata (44 kB)
Collecting fastapi-events==0.11.1 (from invokeai)
  Using cached fastapi_events-0.11.1-py3-none-any.whl.metadata (19 kB)
Collecting fastapi==0.111.0 (from invokeai)
  Using cached fastapi-0.111.0-py3-none-any.whl.metadata (25 kB)
Collecting huggingface-hub==0.26.1 (from invokeai)
  Using cached huggingface_hub-0.26.1-py3-none-any.whl.metadata (13 kB)
Collecting pydantic-settings==2.2.1 (from invokeai)
  Using cached pydantic_settings-2.2.1-py3-none-any.whl.metadata (3.1 kB)
Collecting pydantic==2.7.2 (from invokeai)
  Using cached pydantic-2.7.2-py3-none-any.whl.metadata (108 kB)
Collecting python-socketio==5.11.1 (from invokeai)
  Using cached python_socketio-5.11.1-py3-none-any.whl.metadata (3.2 kB)
Collecting uvicorn==0.28.0 (from uvicorn[standard]==0.28.0->invokeai)
  Using cached uvicorn-0.28.0-py3-none-any.whl.metadata (6.3 kB)
Collecting albumentations (from invokeai)
  Using cached albumentations-2.0.3-py3-none-any.whl.metadata (38 kB)
Collecting blake3 (from invokeai)
  Downloading blake3-1.0.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.2 kB)
Collecting click (from invokeai)
  Using cached click-8.1.8-py3-none-any.whl.metadata (2.3 kB)
Collecting datasets (from invokeai)
  Using cached datasets-3.2.0-py3-none-any.whl.metadata (20 kB)
Collecting Deprecated (from invokeai)
  Using cached Deprecated-1.2.18-py2.py3-none-any.whl.metadata (5.7 kB)
Collecting dnspython (from invokeai)
  Using cached dnspython-2.7.0-py3-none-any.whl.metadata (5.8 kB)
Collecting dynamicprompts (from invokeai)
  Using cached dynamicprompts-0.31.0-py3-none-any.whl.metadata (18 kB)
Collecting einops (from invokeai)
  Downloading einops-0.8.1-py3-none-any.whl.metadata (13 kB)
Collecting facexlib (from invokeai)
  Using cached facexlib-0.3.0-py3-none-any.whl.metadata (4.6 kB)
Collecting matplotlib!=3.9.1 (from invokeai)
  Using cached matplotlib-3.10.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
Collecting npyscreen (from invokeai)
  Using cached npyscreen-4.10.5-py3-none-any.whl
Collecting omegaconf (from invokeai)
  Using cached https://download.pytorch.org/whl/nightly/omegaconf-2.3.0-py3-none-any.whl (79 kB)
Collecting picklescan (from invokeai)
  Using cached picklescan-0.0.19-py3-none-any.whl.metadata (6.2 kB)
Collecting pillow (from invokeai)
  Using cached pillow-11.1.0-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (9.1 kB)
Collecting prompt-toolkit (from invokeai)
  Using cached prompt_toolkit-3.0.50-py3-none-any.whl.metadata (6.6 kB)
Collecting pympler (from invokeai)
  Using cached Pympler-1.1-py3-none-any.whl.metadata (3.6 kB)
Collecting pypatchmatch (from invokeai)
  Using cached PyPatchMatch-1.0.0-py3-none-any.whl.metadata (4.8 kB)
Collecting pyperclip (from invokeai)
  Using cached pyperclip-1.9.0-py3-none-any.whl
Collecting pyreadline3 (from invokeai)
  Using cached pyreadline3-3.5.4-py3-none-any.whl.metadata (4.7 kB)
Collecting python-multipart (from invokeai)
  Using cached python_multipart-0.0.20-py3-none-any.whl.metadata (1.8 kB)
Collecting requests (from invokeai)
  Using cached https://download.pytorch.org/whl/nightly/requests-2.32.3-py3-none-any.whl (64 kB)
Collecting rich~=13.3 (from invokeai)
  Using cached rich-13.9.4-py3-none-any.whl.metadata (18 kB)
Collecting scikit-image (from invokeai)
  Downloading scikit_image-0.25.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (14 kB)
Collecting semver~=3.0.1 (from invokeai)
  Using cached semver-3.0.4-py3-none-any.whl.metadata (6.8 kB)
Collecting test-tube (from invokeai)
  Using cached test_tube-0.7.5-py3-none-any.whl
Collecting packaging>=20.0 (from accelerate==1.0.1->invokeai)
  Using cached packaging-24.2-py3-none-any.whl.metadata (3.2 kB)
Collecting psutil (from accelerate==1.0.1->invokeai)
  Using cached psutil-6.1.1-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (22 kB)
Collecting pyyaml (from accelerate==1.0.1->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (762 kB)
Collecting typing_extensions>=4.8.0 (from bitsandbytes==0.45.0->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/typing_extensions-4.12.2-py3-none-any.whl (37 kB)
Collecting ftfy (from clip_anytorch==2.6.0->invokeai)
  Using cached ftfy-6.3.1-py3-none-any.whl.metadata (7.3 kB)
Collecting regex (from clip_anytorch==2.6.0->invokeai)
  Using cached regex-2024.11.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (40 kB)
Collecting tqdm (from clip_anytorch==2.6.0->invokeai)
  Using cached tqdm-4.67.1-py3-none-any.whl.metadata (57 kB)
Collecting pyparsing~=3.0 (from compel==2.0.2->invokeai)
  Using cached pyparsing-3.2.1-py3-none-any.whl.metadata (5.0 kB)
Collecting importlib_metadata (from controlnet-aux==0.0.7->invokeai)
  Using cached importlib_metadata-8.6.1-py3-none-any.whl.metadata (4.7 kB)
Collecting scipy (from controlnet-aux==0.0.7->invokeai)
  Using cached scipy-1.15.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
Collecting filelock (from controlnet-aux==0.0.7->invokeai)
  Using cached filelock-3.17.0-py3-none-any.whl.metadata (2.9 kB)
Collecting starlette<0.38.0,>=0.37.2 (from fastapi==0.111.0->invokeai)
  Using cached starlette-0.37.2-py3-none-any.whl.metadata (5.9 kB)
Collecting fastapi-cli>=0.0.2 (from fastapi==0.111.0->invokeai)
  Using cached fastapi_cli-0.0.7-py3-none-any.whl.metadata (6.2 kB)
Collecting httpx>=0.23.0 (from fastapi==0.111.0->invokeai)
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting jinja2>=2.11.2 (from fastapi==0.111.0->invokeai)
  Using cached jinja2-3.1.5-py3-none-any.whl.metadata (2.6 kB)
Collecting ujson!=4.0.2,!=4.1.0,!=4.2.0,!=4.3.0,!=5.0.0,!=5.1.0,>=4.0.1 (from fastapi==0.111.0->invokeai)
  Using cached ujson-5.10.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.3 kB)
Collecting orjson>=3.2.1 (from fastapi==0.111.0->invokeai)
  Using cached orjson-3.10.15-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (41 kB)
Collecting email_validator>=2.0.0 (from fastapi==0.111.0->invokeai)
  Using cached email_validator-2.2.0-py3-none-any.whl.metadata (25 kB)
Collecting fsspec>=2023.5.0 (from huggingface-hub==0.26.1->invokeai)
  Using cached fsspec-2025.2.0-py3-none-any.whl.metadata (11 kB)
Collecting PyWavelets>=1.1.1 (from invisible-watermark==0.2.0->invokeai)
  Using cached pywavelets-1.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.0 kB)
Collecting absl-py (from mediapipe==0.10.14->invokeai)
  Using cached absl_py-2.1.0-py3-none-any.whl.metadata (2.3 kB)
Collecting attrs>=19.1.0 (from mediapipe==0.10.14->invokeai)
  Using cached attrs-25.1.0-py3-none-any.whl.metadata (10 kB)
Collecting flatbuffers>=2.0 (from mediapipe==0.10.14->invokeai)
  Using cached flatbuffers-25.1.24-py2.py3-none-any.whl.metadata (875 bytes)
Collecting jax (from mediapipe==0.10.14->invokeai)
  Using cached jax-0.5.0-py3-none-any.whl.metadata (22 kB)
Collecting jaxlib (from mediapipe==0.10.14->invokeai)
  Using cached jaxlib-0.5.0-cp311-cp311-manylinux2014_x86_64.whl.metadata (978 bytes)
Collecting opencv-contrib-python (from mediapipe==0.10.14->invokeai)
  Using cached opencv_contrib_python-4.11.0.86-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (20 kB)
Collecting protobuf<5,>=4.25.3 (from mediapipe==0.10.14->invokeai)
  Using cached protobuf-4.25.6-cp37-abi3-manylinux2014_x86_64.whl.metadata (541 bytes)
Collecting sounddevice>=0.4.4 (from mediapipe==0.10.14->invokeai)
  Using cached sounddevice-0.5.1-py3-none-any.whl.metadata (1.4 kB)
Collecting coloredlogs (from onnxruntime==1.19.2->invokeai)
  Using cached coloredlogs-15.0.1-py2.py3-none-any.whl.metadata (12 kB)
Collecting sympy (from onnxruntime==1.19.2->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/sympy-1.13.3-py3-none-any.whl (6.2 MB)
Collecting annotated-types>=0.4.0 (from pydantic==2.7.2->invokeai)
  Using cached annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.18.3 (from pydantic==2.7.2->invokeai)
  Using cached pydantic_core-2.18.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.5 kB)
Collecting python-dotenv>=0.21.0 (from pydantic-settings==2.2.1->invokeai)
  Using cached python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
Collecting bidict>=0.21.0 (from python-socketio==5.11.1->invokeai)
  Using cached bidict-0.23.1-py3-none-any.whl.metadata (8.7 kB)
Collecting python-engineio>=4.8.0 (from python-socketio==5.11.1->invokeai)
  Using cached python_engineio-4.11.2-py3-none-any.whl.metadata (2.2 kB)
Collecting lightning-utilities>=0.8.0 (from pytorch-lightning==2.1.3->invokeai)
  Using cached lightning_utilities-0.12.0-py3-none-any.whl.metadata (5.6 kB)
Collecting tokenizers<0.21,>=0.20 (from transformers==4.46.3->invokeai)
  Using cached tokenizers-0.20.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
Collecting h11>=0.8 (from uvicorn==0.28.0->uvicorn[standard]==0.28.0->invokeai)
  Using cached h11-0.14.0-py3-none-any.whl.metadata (8.2 kB)
Collecting httptools>=0.5.0 (from uvicorn[standard]==0.28.0->invokeai)
  Using cached httptools-0.6.4-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (3.6 kB)
Collecting uvloop!=0.15.0,!=0.15.1,>=0.14.0 (from uvicorn[standard]==0.28.0->invokeai)
  Using cached uvloop-0.21.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
Collecting watchfiles>=0.13 (from uvicorn[standard]==0.28.0->invokeai)
  Using cached watchfiles-1.0.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
Collecting websockets>=10.4 (from uvicorn[standard]==0.28.0->invokeai)
  Using cached websockets-14.2-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.8 kB)
Collecting contourpy>=1.0.1 (from matplotlib!=3.9.1->invokeai)
  Using cached contourpy-1.3.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.4 kB)
Collecting cycler>=0.10 (from matplotlib!=3.9.1->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/cycler-0.12.1-py3-none-any.whl (8.3 kB)
Collecting fonttools>=4.22.0 (from matplotlib!=3.9.1->invokeai)
  Downloading fonttools-4.56.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (101 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 101.9/101.9 kB 2.4 MB/s eta 0:00:00
Collecting kiwisolver>=1.3.1 (from matplotlib!=3.9.1->invokeai)
  Using cached kiwisolver-1.4.8-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.2 kB)
Collecting python-dateutil>=2.7 (from matplotlib!=3.9.1->invokeai)
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting markdown-it-py>=2.2.0 (from rich~=13.3->invokeai)
  Using cached markdown_it_py-3.0.0-py3-none-any.whl.metadata (6.9 kB)
Collecting pygments<3.0.0,>=2.13.0 (from rich~=13.3->invokeai)
  Using cached pygments-2.19.1-py3-none-any.whl.metadata (2.5 kB)
Collecting networkx (from torch<2.5.0->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/networkx-3.4.2-py3-none-any.whl (1.7 MB)
Collecting nvidia-cuda-nvrtc-cu12==12.1.105 (from torch<2.5.0->invokeai)
  Using cached nvidia_cuda_nvrtc_cu12-12.1.105-py3-none-manylinux1_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cuda-runtime-cu12==12.1.105 (from torch<2.5.0->invokeai)
  Using cached nvidia_cuda_runtime_cu12-12.1.105-py3-none-manylinux1_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cuda-cupti-cu12==12.1.105 (from torch<2.5.0->invokeai)
  Using cached nvidia_cuda_cupti_cu12-12.1.105-py3-none-manylinux1_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-cudnn-cu12==9.1.0.70 (from torch<2.5.0->invokeai)
  Using cached nvidia_cudnn_cu12-9.1.0.70-py3-none-manylinux2014_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-cublas-cu12==12.1.3.1 (from torch<2.5.0->invokeai)
  Using cached nvidia_cublas_cu12-12.1.3.1-py3-none-manylinux1_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cufft-cu12==11.0.2.54 (from torch<2.5.0->invokeai)
  Using cached nvidia_cufft_cu12-11.0.2.54-py3-none-manylinux1_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-curand-cu12==10.3.2.106 (from torch<2.5.0->invokeai)
  Using cached nvidia_curand_cu12-10.3.2.106-py3-none-manylinux1_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cusolver-cu12==11.4.5.107 (from torch<2.5.0->invokeai)
  Using cached nvidia_cusolver_cu12-11.4.5.107-py3-none-manylinux1_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-cusparse-cu12==12.1.0.106 (from torch<2.5.0->invokeai)
  Using cached nvidia_cusparse_cu12-12.1.0.106-py3-none-manylinux1_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-nccl-cu12==2.20.5 (from torch<2.5.0->invokeai)
  Using cached nvidia_nccl_cu12-2.20.5-py3-none-manylinux2014_x86_64.whl.metadata (1.8 kB)
Collecting nvidia-nvtx-cu12==12.1.105 (from torch<2.5.0->invokeai)
  Using cached nvidia_nvtx_cu12-12.1.105-py3-none-manylinux1_x86_64.whl.metadata (1.7 kB)
Collecting triton==3.0.0 (from torch<2.5.0->invokeai)
  Using cached triton-3.0.0-1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.3 kB)
Collecting nvidia-nvjitlink-cu12 (from nvidia-cusolver-cu12==11.4.5.107->torch<2.5.0->invokeai)
  Using cached nvidia_nvjitlink_cu12-12.8.61-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl.metadata (1.7 kB)
INFO: pip is looking at multiple versions of albumentations to determine which version is compatible with other requirements. This could take a while.
Collecting albumentations (from invokeai)
  Using cached albumentations-2.0.2-py3-none-any.whl.metadata (38 kB)
  Using cached albumentations-2.0.1-py3-none-any.whl.metadata (38 kB)
  Using cached albumentations-2.0.0-py3-none-any.whl.metadata (38 kB)
  Using cached albumentations-1.4.24-py3-none-any.whl.metadata (37 kB)
  Using cached albumentations-1.4.23-py3-none-any.whl.metadata (36 kB)
  Using cached albumentations-1.4.22-py3-none-any.whl.metadata (33 kB)
  Using cached albumentations-1.4.21-py3-none-any.whl.metadata (31 kB)
Collecting albucore==0.0.20 (from albumentations->invokeai)
  Using cached albucore-0.0.20-py3-none-any.whl.metadata (5.3 kB)
Collecting eval-type-backport (from albumentations->invokeai)
  Using cached eval_type_backport-0.2.2-py3-none-any.whl.metadata (2.2 kB)
Collecting opencv-python-headless>=4.9.0.80 (from albumentations->invokeai)
  Using cached opencv_python_headless-4.11.0.86-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (20 kB)
Collecting stringzilla>=3.10.4 (from albucore==0.0.20->albumentations->invokeai)
  Using cached stringzilla-3.11.3-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_28_x86_64.whl.metadata (80 kB)
Collecting simsimd>=5.9.2 (from albucore==0.0.20->albumentations->invokeai)
  Using cached simsimd-6.2.1-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (66 kB)
Collecting pyarrow>=15.0.0 (from datasets->invokeai)
  Using cached pyarrow-19.0.0-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (3.3 kB)
Collecting dill<0.3.9,>=0.3.0 (from datasets->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/dill-0.3.8-py3-none-any.whl (116 kB)
Collecting pandas (from datasets->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/pandas-2.2.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (13.1 MB)
Collecting xxhash (from datasets->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/xxhash-3.5.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (194 kB)
Collecting multiprocess<0.70.17 (from datasets->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/multiprocess-0.70.16-py311-none-any.whl (143 kB)
Collecting fsspec>=2023.5.0 (from huggingface-hub==0.26.1->invokeai)
  Using cached fsspec-2024.9.0-py3-none-any.whl.metadata (11 kB)
Collecting aiohttp (from datasets->invokeai)
  Downloading aiohttp-3.11.12-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.7 kB)
Collecting charset-normalizer<4,>=2 (from requests->invokeai)
  Using cached charset_normalizer-3.4.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (35 kB)
Collecting idna<4,>=2.5 (from requests->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/idna-3.10-py3-none-any.whl (70 kB)
Collecting urllib3<3,>=1.21.1 (from requests->invokeai)
  Using cached urllib3-2.3.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests->invokeai)
  Using cached certifi-2025.1.31-py3-none-any.whl.metadata (2.5 kB)
Collecting wrapt<2,>=1.10 (from Deprecated->invokeai)
  Using cached wrapt-1.17.2-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.4 kB)
Collecting filterpy (from facexlib->invokeai)
  Using cached filterpy-1.4.5-py3-none-any.whl
Collecting numba (from facexlib->invokeai)
  Using cached numba-0.61.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.8 kB)
Collecting antlr4-python3-runtime==4.9.* (from omegaconf->invokeai)
  Using cached antlr4_python3_runtime-4.9.3-py3-none-any.whl
Collecting wcwidth (from prompt-toolkit->invokeai)
  Using cached wcwidth-0.2.13-py2.py3-none-any.whl.metadata (14 kB)
Collecting imageio!=2.35.0,>=2.33 (from scikit-image->invokeai)
  Using cached imageio-2.37.0-py3-none-any.whl.metadata (5.2 kB)
Collecting tifffile>=2022.8.12 (from scikit-image->invokeai)
  Using cached tifffile-2025.1.10-py3-none-any.whl.metadata (31 kB)
Collecting lazy-loader>=0.4 (from scikit-image->invokeai)
  Using cached lazy_loader-0.4-py3-none-any.whl.metadata (7.6 kB)
Collecting tensorboard>=1.15.0 (from test-tube->invokeai)
  Using cached tensorboard-2.18.0-py3-none-any.whl.metadata (1.6 kB)
Collecting future (from test-tube->invokeai)
  Using cached future-1.0.0-py3-none-any.whl.metadata (4.0 kB)
Collecting trampoline>=0.1.2 (from torchsde->invokeai)
  Using cached trampoline-0.1.2-py3-none-any.whl.metadata (10 kB)
INFO: pip is looking at multiple versions of torchvision to determine which version is compatible with other requirements. This could take a while.
Collecting torchvision (from invokeai)
  Using cached torchvision-0.20.1-cp311-cp311-manylinux1_x86_64.whl.metadata (6.1 kB)
  Using cached torchvision-0.20.0-cp311-cp311-manylinux1_x86_64.whl.metadata (6.1 kB)
  Using cached torchvision-0.19.1-cp311-cp311-manylinux1_x86_64.whl.metadata (6.0 kB)
Collecting typer>=0.12.3 (from fastapi-cli>=0.0.2->fastapi==0.111.0->invokeai)
  Using cached typer-0.15.1-py3-none-any.whl.metadata (15 kB)
Collecting rich-toolkit>=0.11.1 (from fastapi-cli>=0.0.2->fastapi==0.111.0->invokeai)
  Using cached rich_toolkit-0.13.2-py3-none-any.whl.metadata (999 bytes)
Collecting aiohappyeyeballs>=2.3.0 (from aiohttp->datasets->invokeai)
  Using cached aiohappyeyeballs-2.4.6-py3-none-any.whl.metadata (5.9 kB)
Collecting aiosignal>=1.1.2 (from aiohttp->datasets->invokeai)
  Using cached aiosignal-1.3.2-py2.py3-none-any.whl.metadata (3.8 kB)
Collecting frozenlist>=1.1.1 (from aiohttp->datasets->invokeai)
  Using cached frozenlist-1.5.0-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (13 kB)
Collecting multidict<7.0,>=4.5 (from aiohttp->datasets->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/multidict-6.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (129 kB)
Collecting propcache>=0.2.0 (from aiohttp->datasets->invokeai)
  Using cached propcache-0.2.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.2 kB)
Collecting yarl<2.0,>=1.17.0 (from aiohttp->datasets->invokeai)
  Using cached yarl-1.18.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (69 kB)
Collecting anyio (from httpx>=0.23.0->fastapi==0.111.0->invokeai)
  Using cached anyio-4.8.0-py3-none-any.whl.metadata (4.6 kB)
Collecting httpcore==1.* (from httpx>=0.23.0->fastapi==0.111.0->invokeai)
  Using cached httpcore-1.0.7-py3-none-any.whl.metadata (21 kB)
Collecting MarkupSafe>=2.0 (from jinja2>=2.11.2->fastapi==0.111.0->invokeai)
  Using cached MarkupSafe-3.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.0 kB)
Requirement already satisfied: setuptools in ./.venv/lib/python3.11/site-packages (from lightning-utilities>=0.8.0->pytorch-lightning==2.1.3->invokeai) (65.5.0)
Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich~=13.3->invokeai)
  Using cached mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Collecting pytz>=2020.1 (from pandas->datasets->invokeai)
  Using cached pytz-2025.1-py2.py3-none-any.whl.metadata (22 kB)
Collecting tzdata>=2022.7 (from pandas->datasets->invokeai)
  Using cached tzdata-2025.1-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting six>=1.5 (from python-dateutil>=2.7->matplotlib!=3.9.1->invokeai)
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting simple-websocket>=0.10.0 (from python-engineio>=4.8.0->python-socketio==5.11.1->invokeai)
  Using cached simple_websocket-1.1.0-py3-none-any.whl.metadata (1.5 kB)
Collecting CFFI>=1.0 (from sounddevice>=0.4.4->mediapipe==0.10.14->invokeai)
  Using cached cffi-1.17.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.5 kB)
Collecting grpcio>=1.48.2 (from tensorboard>=1.15.0->test-tube->invokeai)
  Downloading grpcio-1.70.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (3.9 kB)
Collecting markdown>=2.6.8 (from tensorboard>=1.15.0->test-tube->invokeai)
  Using cached Markdown-3.7-py3-none-any.whl.metadata (7.0 kB)
Collecting tensorboard-data-server<0.8.0,>=0.7.0 (from tensorboard>=1.15.0->test-tube->invokeai)
  Using cached tensorboard_data_server-0.7.2-py3-none-manylinux_2_31_x86_64.whl.metadata (1.1 kB)
Collecting werkzeug>=1.0.1 (from tensorboard>=1.15.0->test-tube->invokeai)
  Using cached werkzeug-3.1.3-py3-none-any.whl.metadata (3.7 kB)
Collecting humanfriendly>=9.1 (from coloredlogs->onnxruntime==1.19.2->invokeai)
  Using cached humanfriendly-10.0-py2.py3-none-any.whl.metadata (9.2 kB)
Collecting zipp>=3.20 (from importlib_metadata->controlnet-aux==0.0.7->invokeai)
  Using cached zipp-3.21.0-py3-none-any.whl.metadata (3.7 kB)
Collecting ml_dtypes>=0.4.0 (from jax->mediapipe==0.10.14->invokeai)
  Using cached ml_dtypes-0.5.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (21 kB)
Collecting opt_einsum (from jax->mediapipe==0.10.14->invokeai)
  Using cached opt_einsum-3.4.0-py3-none-any.whl.metadata (6.3 kB)
Collecting llvmlite<0.45,>=0.44.0dev0 (from numba->facexlib->invokeai)
  Using cached llvmlite-0.44.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.8 kB)
Collecting mpmath<1.4,>=1.1.0 (from sympy->onnxruntime==1.19.2->invokeai)
  Using cached https://download.pytorch.org/whl/nightly/mpmath-1.3.0-py3-none-any.whl (536 kB)
Collecting sniffio>=1.1 (from anyio->httpx>=0.23.0->fastapi==0.111.0->invokeai)
  Using cached sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting pycparser (from CFFI>=1.0->sounddevice>=0.4.4->mediapipe==0.10.14->invokeai)
  Using cached pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
Collecting wsproto (from simple-websocket>=0.10.0->python-engineio>=4.8.0->python-socketio==5.11.1->invokeai)
  Using cached wsproto-1.2.0-py3-none-any.whl.metadata (5.6 kB)
Collecting shellingham>=1.3.0 (from typer>=0.12.3->fastapi-cli>=0.0.2->fastapi==0.111.0->invokeai)
  Using cached shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
Using cached InvokeAI-5.6.0-py3-none-any.whl (8.2 MB)
Using cached accelerate-1.0.1-py3-none-any.whl (330 kB)
Using cached bitsandbytes-0.45.0-py3-none-manylinux_2_24_x86_64.whl (69.1 MB)
Using cached clip_anytorch-2.6.0-py3-none-any.whl (1.4 MB)
Using cached compel-2.0.2-py3-none-any.whl (30 kB)
Using cached diffusers-0.31.0-py3-none-any.whl (2.9 MB)
Using cached fastapi-0.111.0-py3-none-any.whl (91 kB)
Using cached fastapi_events-0.11.1-py3-none-any.whl (28 kB)
Using cached gguf-0.10.0-py3-none-any.whl (71 kB)
Using cached huggingface_hub-0.26.1-py3-none-any.whl (447 kB)
Using cached invisible_watermark-0.2.0-py3-none-any.whl (1.6 MB)
Using cached mediapipe-0.10.14-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (35.7 MB)
Using cached onnx-1.16.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (15.9 MB)
Using cached onnxruntime-1.19.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (13.2 MB)
Using cached opencv_python-4.9.0.80-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (62.2 MB)
Using cached pydantic-2.7.2-py3-none-any.whl (409 kB)
Using cached pydantic_settings-2.2.1-py3-none-any.whl (13 kB)
Using cached python_socketio-5.11.1-py3-none-any.whl (75 kB)
Using cached pytorch_lightning-2.1.3-py3-none-any.whl (777 kB)
Using cached spandrel-0.3.4-py3-none-any.whl (268 kB)
Using cached timm-0.6.13-py3-none-any.whl (549 kB)
Using cached transformers-4.46.3-py3-none-any.whl (10.0 MB)
Using cached uvicorn-0.28.0-py3-none-any.whl (60 kB)
Using cached pydantic_core-2.18.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.0 MB)
Using cached click-8.1.8-py3-none-any.whl (98 kB)
Using cached matplotlib-3.10.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (8.6 MB)
Using cached pillow-11.1.0-cp311-cp311-manylinux_2_28_x86_64.whl (4.5 MB)
Using cached python_multipart-0.0.20-py3-none-any.whl (24 kB)
Using cached rich-13.9.4-py3-none-any.whl (242 kB)
Using cached semver-3.0.4-py3-none-any.whl (17 kB)
Using cached torch-2.4.1-cp311-cp311-manylinux1_x86_64.whl (797.1 MB)
Using cached nvidia_cublas_cu12-12.1.3.1-py3-none-manylinux1_x86_64.whl (410.6 MB)
Using cached nvidia_cuda_cupti_cu12-12.1.105-py3-none-manylinux1_x86_64.whl (14.1 MB)
Using cached nvidia_cuda_nvrtc_cu12-12.1.105-py3-none-manylinux1_x86_64.whl (23.7 MB)
Using cached nvidia_cuda_runtime_cu12-12.1.105-py3-none-manylinux1_x86_64.whl (823 kB)
Using cached nvidia_cudnn_cu12-9.1.0.70-py3-none-manylinux2014_x86_64.whl (664.8 MB)
Using cached nvidia_cufft_cu12-11.0.2.54-py3-none-manylinux1_x86_64.whl (121.6 MB)
Using cached nvidia_curand_cu12-10.3.2.106-py3-none-manylinux1_x86_64.whl (56.5 MB)
Using cached nvidia_cusolver_cu12-11.4.5.107-py3-none-manylinux1_x86_64.whl (124.2 MB)
Using cached nvidia_cusparse_cu12-12.1.0.106-py3-none-manylinux1_x86_64.whl (196.0 MB)
Using cached nvidia_nccl_cu12-2.20.5-py3-none-manylinux2014_x86_64.whl (176.2 MB)
Using cached nvidia_nvtx_cu12-12.1.105-py3-none-manylinux1_x86_64.whl (99 kB)
Using cached triton-3.0.0-1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (209.4 MB)
Using cached torchmetrics-1.6.1-py3-none-any.whl (927 kB)
Using cached albumentations-1.4.21-py3-none-any.whl (227 kB)
Using cached albucore-0.0.20-py3-none-any.whl (12 kB)
Downloading blake3-1.0.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (376 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 376.2/376.2 kB 8.9 MB/s eta 0:00:00
Using cached datasets-3.2.0-py3-none-any.whl (480 kB)
Using cached Deprecated-1.2.18-py2.py3-none-any.whl (10.0 kB)
Using cached dnspython-2.7.0-py3-none-any.whl (313 kB)
Using cached dynamicprompts-0.31.0-py3-none-any.whl (53 kB)
Downloading einops-0.8.1-py3-none-any.whl (64 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.4/64.4 kB 5.7 MB/s eta 0:00:00
Using cached facexlib-0.3.0-py3-none-any.whl (59 kB)
Using cached picklescan-0.0.19-py3-none-any.whl (12 kB)
Using cached prompt_toolkit-3.0.50-py3-none-any.whl (387 kB)
Using cached Pympler-1.1-py3-none-any.whl (165 kB)
Using cached PyPatchMatch-1.0.0-py3-none-any.whl (20 kB)
Using cached pyreadline3-3.5.4-py3-none-any.whl (83 kB)
Downloading scikit_image-0.25.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (14.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.8/14.8 MB 61.4 MB/s eta 0:00:00
Using cached torchsde-0.2.6-py3-none-any.whl (61 kB)
Using cached torchvision-0.19.1-cp311-cp311-manylinux1_x86_64.whl (7.0 MB)
Using cached annotated_types-0.7.0-py3-none-any.whl (13 kB)
Using cached attrs-25.1.0-py3-none-any.whl (63 kB)
Using cached bidict-0.23.1-py3-none-any.whl (32 kB)
Using cached certifi-2025.1.31-py3-none-any.whl (166 kB)
Using cached charset_normalizer-3.4.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (143 kB)
Using cached contourpy-1.3.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (326 kB)
Using cached email_validator-2.2.0-py3-none-any.whl (33 kB)
Using cached fastapi_cli-0.0.7-py3-none-any.whl (10 kB)
Using cached flatbuffers-25.1.24-py2.py3-none-any.whl (30 kB)
Downloading fonttools-4.56.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.9/4.9 MB 67.0 MB/s eta 0:00:00
Using cached fsspec-2024.9.0-py3-none-any.whl (179 kB)
Downloading aiohttp-3.11.12-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 57.1 MB/s eta 0:00:00
Using cached h11-0.14.0-py3-none-any.whl (58 kB)
Using cached httptools-0.6.4-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (459 kB)
Using cached httpx-0.28.1-py3-none-any.whl (73 kB)
Using cached httpcore-1.0.7-py3-none-any.whl (78 kB)
Using cached imageio-2.37.0-py3-none-any.whl (315 kB)
Using cached jinja2-3.1.5-py3-none-any.whl (134 kB)
Using cached kiwisolver-1.4.8-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.4 MB)
Using cached lazy_loader-0.4-py3-none-any.whl (12 kB)
Using cached lightning_utilities-0.12.0-py3-none-any.whl (28 kB)
Using cached markdown_it_py-3.0.0-py3-none-any.whl (87 kB)
Using cached opencv_python_headless-4.11.0.86-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (50.0 MB)
Using cached orjson-3.10.15-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (130 kB)
Using cached packaging-24.2-py3-none-any.whl (65 kB)
Using cached protobuf-4.25.6-cp37-abi3-manylinux2014_x86_64.whl (294 kB)
Using cached pyarrow-19.0.0-cp311-cp311-manylinux_2_28_x86_64.whl (42.1 MB)
Using cached pygments-2.19.1-py3-none-any.whl (1.2 MB)
Using cached pyparsing-3.2.1-py3-none-any.whl (107 kB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Using cached python_engineio-4.11.2-py3-none-any.whl (59 kB)
Using cached pywavelets-1.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.5 MB)
Using cached regex-2024.11.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (792 kB)
Using cached scipy-1.15.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (40.6 MB)
Using cached sounddevice-0.5.1-py3-none-any.whl (32 kB)
Using cached starlette-0.37.2-py3-none-any.whl (71 kB)
Using cached tensorboard-2.18.0-py3-none-any.whl (5.5 MB)
Using cached absl_py-2.1.0-py3-none-any.whl (133 kB)
Using cached tifffile-2025.1.10-py3-none-any.whl (227 kB)
Using cached tokenizers-0.20.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
Using cached tqdm-4.67.1-py3-none-any.whl (78 kB)
Using cached trampoline-0.1.2-py3-none-any.whl (5.2 kB)
Using cached ujson-5.10.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (53 kB)
Using cached urllib3-2.3.0-py3-none-any.whl (128 kB)
Using cached uvloop-0.21.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.0 MB)
Using cached watchfiles-1.0.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (452 kB)
Using cached websockets-14.2-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (169 kB)
Using cached wrapt-1.17.2-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (83 kB)
Using cached coloredlogs-15.0.1-py2.py3-none-any.whl (46 kB)
Using cached eval_type_backport-0.2.2-py3-none-any.whl (5.8 kB)
Using cached filelock-3.17.0-py3-none-any.whl (16 kB)
Using cached ftfy-6.3.1-py3-none-any.whl (44 kB)
Using cached future-1.0.0-py3-none-any.whl (491 kB)
Using cached importlib_metadata-8.6.1-py3-none-any.whl (26 kB)
Using cached jax-0.5.0-py3-none-any.whl (2.3 MB)
Using cached jaxlib-0.5.0-cp311-cp311-manylinux2014_x86_64.whl (102.0 MB)
Using cached numba-0.61.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (3.8 MB)
Using cached opencv_contrib_python-4.11.0.86-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (69.1 MB)
Using cached psutil-6.1.1-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (287 kB)
Using cached wcwidth-0.2.13-py2.py3-none-any.whl (34 kB)
Using cached aiohappyeyeballs-2.4.6-py3-none-any.whl (14 kB)
Using cached aiosignal-1.3.2-py2.py3-none-any.whl (7.6 kB)
Using cached anyio-4.8.0-py3-none-any.whl (96 kB)
Using cached cffi-1.17.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (467 kB)
Using cached frozenlist-1.5.0-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (274 kB)
Downloading grpcio-1.70.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (5.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.9/5.9 MB 50.6 MB/s eta 0:00:00
Using cached humanfriendly-10.0-py2.py3-none-any.whl (86 kB)
Using cached llvmlite-0.44.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (42.4 MB)
Using cached Markdown-3.7-py3-none-any.whl (106 kB)
Using cached MarkupSafe-3.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (23 kB)
Using cached mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Using cached ml_dtypes-0.5.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.7 MB)
Using cached propcache-0.2.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (231 kB)
Using cached pytz-2025.1-py2.py3-none-any.whl (507 kB)
Using cached rich_toolkit-0.13.2-py3-none-any.whl (13 kB)
Using cached simple_websocket-1.1.0-py3-none-any.whl (13 kB)
Using cached simsimd-6.2.1-cp311-cp311-manylinux_2_28_x86_64.whl (632 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Using cached stringzilla-3.11.3-cp311-cp311-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_28_x86_64.whl (307 kB)
Using cached tensorboard_data_server-0.7.2-py3-none-manylinux_2_31_x86_64.whl (6.6 MB)
Using cached typer-0.15.1-py3-none-any.whl (44 kB)
Using cached tzdata-2025.1-py2.py3-none-any.whl (346 kB)
Using cached werkzeug-3.1.3-py3-none-any.whl (224 kB)
Using cached yarl-1.18.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (344 kB)
Using cached zipp-3.21.0-py3-none-any.whl (9.6 kB)
Using cached nvidia_nvjitlink_cu12-12.8.61-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl (39.2 MB)
Using cached opt_einsum-3.4.0-py3-none-any.whl (71 kB)
Using cached shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Using cached sniffio-1.3.1-py3-none-any.whl (10 kB)
Using cached pycparser-2.22-py3-none-any.whl (117 kB)
Using cached wsproto-1.2.0-py3-none-any.whl (24 kB)
Installing collected packages: wcwidth, trampoline, stringzilla, simsimd, sentencepiece, pytz, pyperclip, npyscreen, mpmath, flatbuffers, blake3, antlr4-python3-runtime, zipp, xxhash, wrapt, websockets, uvloop, urllib3, ujson, tzdata, typing_extensions, tqdm, tensorboard-data-server, sympy, sniffio, six, shellingham, semver, safetensors, regex, pyyaml, python-multipart, python-dotenv, pyreadline3, pyparsing, pympler, pygments, pycparser, pyarrow, psutil, protobuf, propcache, prompt-toolkit, pillow, picklescan, packaging, orjson, opt_einsum, nvidia-nvtx-cu12, nvidia-nvjitlink-cu12, nvidia-nccl-cu12, nvidia-curand-cu12, nvidia-cufft-cu12, nvidia-cuda-runtime-cu12, nvidia-cuda-nvrtc-cu12, nvidia-cuda-cupti-cu12, nvidia-cublas-cu12, numpy, networkx, multidict, mdurl, MarkupSafe, markdown, llvmlite, kiwisolver, idna, humanfriendly, httptools, h11, grpcio, future, ftfy, fsspec, frozenlist, fonttools, filelock, fastapi-events, eval-type-backport, einops, dnspython, dill, cycler, click, charset-normalizer, certifi, bidict, attrs, annotated-types, aiohappyeyeballs, absl-py, yarl, wsproto, werkzeug, uvicorn, triton, tifffile, scipy, requests, PyWavelets, python-dateutil, pypatchmatch, pydantic-core, opencv-python-headless, opencv-python, opencv-contrib-python, onnx, omegaconf, nvidia-cusparse-cu12, nvidia-cudnn-cu12, numba, multiprocess, ml_dtypes, markdown-it-py, lightning-utilities, lazy-loader, jinja2, importlib_metadata, imageio, httpcore, gguf, email_validator, Deprecated, contourpy, coloredlogs, CFFI, anyio, aiosignal, watchfiles, tensorboard, starlette, sounddevice, simple-websocket, scikit-image, rich, pydantic, pandas, onnxruntime, nvidia-cusolver-cu12, matplotlib, jaxlib, huggingface-hub, httpx, dynamicprompts, albucore, aiohttp, typer, torch, tokenizers, rich-toolkit, python-engineio, pydantic-settings, jax, filterpy, diffusers, albumentations, transformers, torchvision, torchsde, torchmetrics, test-tube, python-socketio, mediapipe, invisible-watermark, fastapi-cli, datasets, bitsandbytes, accelerate, timm, spandrel, pytorch-lightning, fastapi, facexlib, compel, clip_anytorch, controlnet-aux, invokeai
Successfully installed CFFI-1.17.1 Deprecated-1.2.18 MarkupSafe-3.0.2 PyWavelets-1.8.0 absl-py-2.1.0 accelerate-1.0.1 aiohappyeyeballs-2.4.6 aiohttp-3.11.12 aiosignal-1.3.2 albucore-0.0.20 albumentations-1.4.21 annotated-types-0.7.0 antlr4-python3-runtime-4.9.3 anyio-4.8.0 attrs-25.1.0 bidict-0.23.1 bitsandbytes-0.45.0 blake3-1.0.4 certifi-2025.1.31 charset-normalizer-3.4.1 click-8.1.8 clip_anytorch-2.6.0 coloredlogs-15.0.1 compel-2.0.2 contourpy-1.3.1 controlnet-aux-0.0.7 cycler-0.12.1 datasets-3.2.0 diffusers-0.31.0 dill-0.3.8 dnspython-2.7.0 dynamicprompts-0.31.0 einops-0.8.1 email_validator-2.2.0 eval-type-backport-0.2.2 facexlib-0.3.0 fastapi-0.111.0 fastapi-cli-0.0.7 fastapi-events-0.11.1 filelock-3.17.0 filterpy-1.4.5 flatbuffers-25.1.24 fonttools-4.56.0 frozenlist-1.5.0 fsspec-2024.9.0 ftfy-6.3.1 future-1.0.0 gguf-0.10.0 grpcio-1.70.0 h11-0.14.0 httpcore-1.0.7 httptools-0.6.4 httpx-0.28.1 huggingface-hub-0.26.1 humanfriendly-10.0 idna-3.10 imageio-2.37.0 importlib_metadata-8.6.1 invisible-watermark-0.2.0 invokeai-5.6.0 jax-0.5.0 jaxlib-0.5.0 jinja2-3.1.5 kiwisolver-1.4.8 lazy-loader-0.4 lightning-utilities-0.12.0 llvmlite-0.44.0 markdown-3.7 markdown-it-py-3.0.0 matplotlib-3.10.0 mdurl-0.1.2 mediapipe-0.10.14 ml_dtypes-0.5.1 mpmath-1.3.0 multidict-6.1.0 multiprocess-0.70.16 networkx-3.4.2 npyscreen-4.10.5 numba-0.61.0 numpy-1.26.4 nvidia-cublas-cu12-12.1.3.1 nvidia-cuda-cupti-cu12-12.1.105 nvidia-cuda-nvrtc-cu12-12.1.105 nvidia-cuda-runtime-cu12-12.1.105 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.0.2.54 nvidia-curand-cu12-10.3.2.106 nvidia-cusolver-cu12-11.4.5.107 nvidia-cusparse-cu12-12.1.0.106 nvidia-nccl-cu12-2.20.5 nvidia-nvjitlink-cu12-12.8.61 nvidia-nvtx-cu12-12.1.105 omegaconf-2.3.0 onnx-1.16.1 onnxruntime-1.19.2 opencv-contrib-python-4.11.0.86 opencv-python-4.9.0.80 opencv-python-headless-4.11.0.86 opt_einsum-3.4.0 orjson-3.10.15 packaging-24.2 pandas-2.2.3 picklescan-0.0.19 pillow-11.1.0 prompt-toolkit-3.0.50 propcache-0.2.1 protobuf-4.25.6 psutil-6.1.1 pyarrow-19.0.0 pycparser-2.22 pydantic-2.7.2 pydantic-core-2.18.3 pydantic-settings-2.2.1 pygments-2.19.1 pympler-1.1 pyparsing-3.2.1 pypatchmatch-1.0.0 pyperclip-1.9.0 pyreadline3-3.5.4 python-dateutil-2.9.0.post0 python-dotenv-1.0.1 python-engineio-4.11.2 python-multipart-0.0.20 python-socketio-5.11.1 pytorch-lightning-2.1.3 pytz-2025.1 pyyaml-6.0.2 regex-2024.11.6 requests-2.32.3 rich-13.9.4 rich-toolkit-0.13.2 safetensors-0.4.3 scikit-image-0.25.1 scipy-1.15.1 semver-3.0.4 sentencepiece-0.2.0 shellingham-1.5.4 simple-websocket-1.1.0 simsimd-6.2.1 six-1.17.0 sniffio-1.3.1 sounddevice-0.5.1 spandrel-0.3.4 starlette-0.37.2 stringzilla-3.11.3 sympy-1.13.3 tensorboard-2.18.0 tensorboard-data-server-0.7.2 test-tube-0.7.5 tifffile-2025.1.10 timm-0.6.13 tokenizers-0.20.3 torch-2.4.1 torchmetrics-1.6.1 torchsde-0.2.6 torchvision-0.19.1 tqdm-4.67.1 trampoline-0.1.2 transformers-4.46.3 triton-3.0.0 typer-0.15.1 typing_extensions-4.12.2 tzdata-2025.1 ujson-5.10.0 urllib3-2.3.0 uvicorn-0.28.0 uvloop-0.21.0 watchfiles-1.0.4 wcwidth-0.2.13 websockets-14.2 werkzeug-3.1.3 wrapt-1.17.2 wsproto-1.2.0 xxhash-3.5.0 yarl-1.18.3 zipp-3.21.0

[notice] A new release of pip is available: 24.0 -> 25.0.1
[notice] To update, run: pip install --upgrade pip
(.venv) mcon@ikea:~/AMD$ pip install --upgrade pip
Requirement already satisfied: pip in ./.venv/lib/python3.11/site-packages (24.0)
Collecting pip
  Downloading pip-25.0.1-py3-none-any.whl.metadata (3.7 kB)
Downloading pip-25.0.1-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 15.1 MB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed pip-25.0.1
(.venv) mcon@ikea:~/AMD$ python PyTorch_test.py 
PyTorch version: 2.4.1+cu121
CUDA is not available. PyTorch will use the CPU.
(.venv) mcon@ikea:~/AMD$ pip uninstall -y torch torchvision
Found existing installation: torch 2.4.1
Uninstalling torch-2.4.1:
  Successfully uninstalled torch-2.4.1
Found existing installation: torchvision 0.19.1
Uninstalling torchvision-0.19.1:
  Successfully uninstalled torchvision-0.19.1
(.venv) mcon@ikea:~/AMD$ pip install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/rocm6.3
Looking in indexes: https://download.pytorch.org/whl/nightly/rocm6.3
Collecting torch
  Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torch-2.7.0.dev20250210%2Brocm6.3-cp311-cp311-manylinux_2_28_x86_64.whl (4324.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.3/4.3 GB 36.9 MB/s eta 0:00:00
Collecting torchvision
  Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torchvision-0.22.0.dev20250210%2Brocm6.3-cp311-cp311-linux_x86_64.whl.metadata (6.2 kB)
Requirement already satisfied: filelock in ./.venv/lib/python3.11/site-packages (from torch) (3.17.0)
Requirement already satisfied: typing-extensions>=4.10.0 in ./.venv/lib/python3.11/site-packages (from torch) (4.12.2)
Collecting sympy==1.13.1 (from torch)
  Using cached https://download.pytorch.org/whl/nightly/sympy-1.13.1-py3-none-any.whl (6.2 MB)
Requirement already satisfied: networkx in ./.venv/lib/python3.11/site-packages (from torch) (3.4.2)
Requirement already satisfied: jinja2 in ./.venv/lib/python3.11/site-packages (from torch) (3.1.5)
Requirement already satisfied: fsspec in ./.venv/lib/python3.11/site-packages (from torch) (2024.9.0)
Collecting pytorch-triton-rocm==3.2.0+git4b3bb1f8 (from torch)
  Downloading https://download.pytorch.org/whl/nightly/pytorch_triton_rocm-3.2.0%2Bgit4b3bb1f8-cp311-cp311-linux_x86_64.whl.metadata (1.3 kB)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./.venv/lib/python3.11/site-packages (from sympy==1.13.1->torch) (1.3.0)
Requirement already satisfied: numpy in ./.venv/lib/python3.11/site-packages (from torchvision) (1.26.4)
Collecting torch
  Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torch-2.7.0.dev20250209%2Brocm6.3-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (27 kB)
Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in ./.venv/lib/python3.11/site-packages (from torchvision) (11.1.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./.venv/lib/python3.11/site-packages (from jinja2->torch) (3.0.2)
Downloading https://download.pytorch.org/whl/nightly/pytorch_triton_rocm-3.2.0%2Bgit4b3bb1f8-cp311-cp311-linux_x86_64.whl (265.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 265.1/265.1 MB 95.2 MB/s eta 0:00:00
Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torchvision-0.22.0.dev20250210%2Brocm6.3-cp311-cp311-linux_x86_64.whl (2.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 66.2 MB/s eta 0:00:00
Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torch-2.7.0.dev20250209%2Brocm6.3-cp311-cp311-manylinux_2_28_x86_64.whl (4324.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.3/4.3 GB 36.7 MB/s eta 0:00:00
Installing collected packages: pytorch-triton-rocm, sympy, torch, torchvision
  Attempting uninstall: sympy
    Found existing installation: sympy 1.13.3
    Uninstalling sympy-1.13.3:
      Successfully uninstalled sympy-1.13.3
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
invokeai 5.6.0 requires torch<2.5.0, but you have torch 2.7.0.dev20250209+rocm6.3 which is incompatible.
Successfully installed pytorch-triton-rocm-3.2.0+git4b3bb1f8 sympy-1.13.1 torch-2.7.0.dev20250209+rocm6.3 torchvision-0.22.0.dev20250210+rocm6.3
(.venv) mcon@ikea:~/AMD$ python PyTorch_test.py 
PyTorch version: 2.7.0.dev20250209+rocm6.3
CUDA is available! PyTorch can use the GPU.
GPU: AMD Radeon™ RX 7600 XT
(.venv) mcon@ikea:~/AMD$ pip install --force-reinstall 'https://github.com/bitsandbytes-foundation/bitsandbytes/releases/download/continuous-release_multi-backend-refactor/bitsandbytes-0.44.1.dev0-py3-none-manylinux_2_24_x86_64.whl' --no-deps
Collecting bitsandbytes==0.44.1.dev0
  Downloading https://github.com/bitsandbytes-foundation/bitsandbytes/releases/download/continuous-release_multi-backend-refactor/bitsandbytes-0.44.1.dev0-py3-none-manylinux_2_24_x86_64.whl (1.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 22.7 MB/s eta 0:00:00
Installing collected packages: bitsandbytes
  Attempting uninstall: bitsandbytes
    Found existing installation: bitsandbytes 0.45.0
    Uninstalling bitsandbytes-0.45.0:
      Successfully uninstalled bitsandbytes-0.45.0
Successfully installed bitsandbytes-0.44.1.dev0+9315692
(.venv) mcon@ikea:~/AMD$ python PyTorch_test.py 
PyTorch version: 2.7.0.dev20250209+rocm6.3
CUDA is available! PyTorch can use the GPU.
GPU: AMD Radeon™ RX 7600 XT
(.venv) mcon@ikea:~/AMD$ ./start-web 
+ export HCC_AMDGPU_TARGET=gfx1100
+ export HSA_OVERRIDE_GFX_VERSION=11.0.0
+ export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True
+ export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
+ export INVOKEAI_ROOT=/home/mcon/invokeai
+ .venv/bin/invokeai-web
Could not find the bitsandbytes ROCm binary at PosixPath('/home/mcon/AMD/.venv/lib/python3.11/site-packages/bitsandbytes/libbitsandbytes_rocm63.so')
g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

[2025-02-10 21:28:39,419]::[InvokeAI]::INFO --> Loading node pack latent-upscale
[2025-02-10 21:28:39,580]::[InvokeAI]::INFO --> Loaded 1 node packs from /home/mcon/invokeai/nodes
[2025-02-10 21:28:40,768]::[InvokeAI]::INFO --> Patchmatch initialized
[2025-02-10 21:28:41,297]::[InvokeAI]::INFO --> Using torch device: AMD Radeon™ RX 7600 XT
[2025-02-10 21:28:41,672]::[InvokeAI]::INFO --> cuDNN version: 3003000
[2025-02-10 21:28:41,682]::[InvokeAI]::INFO --> InvokeAI version 5.6.0
[2025-02-10 21:28:41,682]::[InvokeAI]::INFO --> Root directory = /home/mcon/invokeai
[2025-02-10 21:28:41,683]::[InvokeAI]::INFO --> Initializing database at /home/mcon/invokeai/databases/invokeai.db
[2025-02-10 21:28:41,685]::[ModelManagerService]::INFO --> [MODEL CACHE] Calculated model RAM cache size: 13958.38 MB. Heuristics applied: [1].
[2025-02-10 21:28:41,702]::[InvokeAI]::INFO --> Pruned 1 finished queue items
[2025-02-10 21:28:41,920]::[InvokeAI]::INFO --> Cleaned database (freed 0.01MB)
[2025-02-10 21:28:41,920]::[InvokeAI]::INFO --> Invoke running on http://0.0.0.0:9090 (Press CTRL+C to quit)
[2025-02-10 21:29:59,496]::[InvokeAI]::INFO --> Executing queue item 258, session 6e768a0e-4098-4218-b0b1-5487e8572a7e
/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/cached_model/cached_model_only_full_load.py:77: UserWarning: expandable_segments not supported on this platform (Triggered internally at /pytorch/c10/hip/HIPAllocatorConfig.h:29.)
  new_state_dict[k] = v.to(self._compute_device, copy=True)
[2025-02-10 21:29:59,910]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.35s. Total model size: 234.72MB, VRAM: 234.72MB (100.0%)
[2025-02-10 21:29:59,960]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:01,176]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.81s. Total model size: 1324.96MB, VRAM: 1324.96MB (100.0%)
[2025-02-10 21:30:01,212]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:01,314]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.00s. Total model size: 234.72MB, VRAM: 234.72MB (100.0%)
[2025-02-10 21:30:01,315]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:01,393]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.00s. Total model size: 1324.96MB, VRAM: 1324.96MB (100.0%)
[2025-02-10 21:30:01,395]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:04,306]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:unet' (UNet2DConditionModel) onto cuda device in 2.62s. Total model size: 4897.05MB, VRAM: 4897.05MB (100.0%)
[2025-02-10 21:30:04,310]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:scheduler' (DDPMScheduler) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
:0:rocdevice.cpp            :3020: 7098718447d us:  Callback: Queue 0x77f8c4700000 aborting with error : HSA_STATUS_ERROR_INVALID_ISA: The instruction set architecture is invalid. code: 0x100f
^CAborted (core dumped)

(.venv) mcon@ikea:~/AMD$ ./start-web 
+ export HCC_AMDGPU_TARGET=gfx1100
+ export HSA_OVERRIDE_GFX_VERSION=11.0.0
+ export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True
+ export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
+ export INVOKEAI_ROOT=/home/mcon/invokeai
+ .venv/bin/invokeai-web
g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

[2025-02-10 21:30:42,123]::[InvokeAI]::INFO --> Loading node pack latent-upscale
[2025-02-10 21:30:42,288]::[InvokeAI]::INFO --> Loaded 1 node packs from /home/mcon/invokeai/nodes
[2025-02-10 21:30:43,477]::[InvokeAI]::INFO --> Patchmatch initialized
[2025-02-10 21:30:44,011]::[InvokeAI]::INFO --> Using torch device: AMD Radeon™ RX 7600 XT
[2025-02-10 21:30:44,392]::[InvokeAI]::INFO --> cuDNN version: 3003000
[2025-02-10 21:30:44,402]::[InvokeAI]::INFO --> InvokeAI version 5.6.0
[2025-02-10 21:30:44,402]::[InvokeAI]::INFO --> Root directory = /home/mcon/invokeai
[2025-02-10 21:30:44,403]::[InvokeAI]::INFO --> Initializing database at /home/mcon/invokeai/databases/invokeai.db
[2025-02-10 21:30:44,405]::[ModelManagerService]::INFO --> [MODEL CACHE] Calculated model RAM cache size: 13958.38 MB. Heuristics applied: [1].
[2025-02-10 21:30:44,445]::[InvokeAI]::INFO --> Pruned 1 finished queue items
[2025-02-10 21:30:44,668]::[InvokeAI]::INFO --> Cleaned database (freed 0.01MB)
[2025-02-10 21:30:44,668]::[InvokeAI]::INFO --> Invoke running on http://0.0.0.0:9090 (Press CTRL+C to quit)
[2025-02-10 21:30:53,287]::[InvokeAI]::INFO --> Executing queue item 259, session 7a0f98ee-8669-46e2-813b-5dfe27cf7f81
/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/cached_model/cached_model_only_full_load.py:77: UserWarning: expandable_segments not supported on this platform (Triggered internally at /pytorch/c10/hip/HIPAllocatorConfig.h:29.)
  new_state_dict[k] = v.to(self._compute_device, copy=True)
[2025-02-10 21:30:53,755]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.40s. Total model size: 234.72MB, VRAM: 234.72MB (100.0%)
[2025-02-10 21:30:53,807]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:55,104]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.87s. Total model size: 1324.96MB, VRAM: 1324.96MB (100.0%)
[2025-02-10 21:30:55,140]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:55,311]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.06s. Total model size: 234.72MB, VRAM: 234.72MB (100.0%)
[2025-02-10 21:30:55,312]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:55,512]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.14s. Total model size: 1324.96MB, VRAM: 1324.96MB (100.0%)
[2025-02-10 21:30:55,514]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:30:57,655]::[ModelManagerService]::WARNING --> [MODEL CACHE] Insufficient GPU memory to load model. Aborting
[2025-02-10 21:30:57,655]::[ModelManagerService]::WARNING --> [MODEL CACHE] Insufficient GPU memory to load model. Aborting
[2025-02-10 21:30:57,659]::[InvokeAI]::ERROR --> Error while invoking session 7a0f98ee-8669-46e2-813b-5dfe27cf7f81, invocation c00a3cd6-9fea-4ed0-be56-0dbb08a1ecaa (denoise_latents): HIP out of memory. Tried to allocate 26.00 MiB. GPU 0 has a total capacity of 15.98 GiB of which 0 bytes is free. Of the allocated memory 3.28 GiB is allocated by PyTorch, and 132.00 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
[2025-02-10 21:30:57,659]::[InvokeAI]::ERROR --> Traceback (most recent call last):
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/app/services/session_processor/session_processor_default.py", line 129, in run_node
    output = invocation.invoke_internal(context=context, services=self._services)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/app/invocations/baseinvocation.py", line 300, in invoke_internal
    output = self.invoke(context)
             ^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/app/invocations/denoise_latents.py", line 824, in invoke
    return self._old_invoke(context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/torch/utils/_contextlib.py", line 116, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/contextlib.py", line 81, in inner
    return func(*args, **kwds)
           ^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/app/invocations/denoise_latents.py", line 1011, in _old_invoke
    with (
  File "/usr/local/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/load_base.py", line 75, in model_on_device
    self._cache.lock(self._cache_record, working_mem_bytes)
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/model_cache.py", line 232, in lock
    self._load_locked_model(cache_entry, working_mem_bytes)
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/model_cache.py", line 303, in _load_locked_model
    model_bytes_loaded = self._move_model_to_vram(cache_entry, vram_available + MB)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/model_cache.py", line 325, in _move_model_to_vram
    return cache_entry.cached_model.full_load_to_vram()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/cached_model/cached_model_only_full_load.py", line 77, in full_load_to_vram
    new_state_dict[k] = v.to(self._compute_device, copy=True)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 26.00 MiB. GPU 0 has a total capacity of 15.98 GiB of which 0 bytes is free. Of the allocated memory 3.28 GiB is allocated by PyTorch, and 132.00 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

[2025-02-10 21:30:57,958]::[InvokeAI]::INFO --> Graph stats: 7a0f98ee-8669-46e2-813b-5dfe27cf7f81
                          Node   Calls   Seconds  VRAM Used
             sdxl_model_loader       1    0.016s     0.000G
            sdxl_compel_prompt       2    2.280s     1.375G
                       collect       2    0.001s     1.294G
                         noise       1    0.003s     1.294G
               denoise_latents       1    2.049s     3.279G
TOTAL GRAPH EXECUTION TIME:   4.348s
TOTAL GRAPH WALL TIME:   4.353s
RAM used by InvokeAI process: 6.82G (+5.178G)
RAM used to load models: 6.31G
RAM cache statistics:
   Model cache hits: 9
   Model cache misses: 5
   Models cached: 5
   Models cleared from cache: 0
   Cache high water mark: 6.31/0.00G

^C[2025-02-10 21:32:12,443]::[ModelInstallService]::INFO --> Installer thread 125693553804992 exiting
/usr/local/lib/python3.11/tempfile.py:934: ResourceWarning: Implicitly cleaning up <TemporaryDirectory '/tmp/tmptxnex3t_'>
  _warnings.warn(warn_message, ResourceWarning)

(.venv) mcon@ikea:~/AMD$ ./start-web 
+ export HCC_AMDGPU_TARGET=gfx1100
+ export HSA_OVERRIDE_GFX_VERSION=11.0.0
+ export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True
+ export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
+ export INVOKEAI_ROOT=/home/mcon/invokeai
+ .venv/bin/invokeai-web
g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

[2025-02-10 21:32:25,779]::[InvokeAI]::INFO --> Loading node pack latent-upscale
[2025-02-10 21:32:25,941]::[InvokeAI]::INFO --> Loaded 1 node packs from /home/mcon/invokeai/nodes
[2025-02-10 21:32:27,159]::[InvokeAI]::INFO --> Patchmatch initialized
[2025-02-10 21:32:27,694]::[InvokeAI]::INFO --> Using torch device: AMD Radeon™ RX 7600 XT
[2025-02-10 21:32:28,079]::[InvokeAI]::INFO --> cuDNN version: 3003000
[2025-02-10 21:32:28,089]::[InvokeAI]::INFO --> InvokeAI version 5.6.0
[2025-02-10 21:32:28,089]::[InvokeAI]::INFO --> Root directory = /home/mcon/invokeai
[2025-02-10 21:32:28,090]::[InvokeAI]::INFO --> Initializing database at /home/mcon/invokeai/databases/invokeai.db
[2025-02-10 21:32:28,091]::[ModelManagerService]::INFO --> [MODEL CACHE] Calculated model RAM cache size: 13958.38 MB. Heuristics applied: [1].
[2025-02-10 21:32:28,109]::[InvokeAI]::INFO --> Pruned 1 finished queue items
[2025-02-10 21:32:28,312]::[InvokeAI]::INFO --> Cleaned database (freed 0.04MB)
[2025-02-10 21:32:28,312]::[InvokeAI]::INFO --> Invoke running on http://0.0.0.0:9090 (Press CTRL+C to quit)
[2025-02-10 21:32:45,415]::[InvokeAI]::INFO --> Executing queue item 260, session d5549fbb-15ec-4006-924c-1b9afbc3eb6f
[2025-02-10 21:32:45,499]::[InvokeAI]::WARNING --> Loading 0.0732421875 MB into VRAM, but only -4607.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
/home/mcon/AMD/.venv/lib/python3.11/site-packages/invokeai/backend/model_manager/load/model_cache/cached_model/cached_model_with_partial_load.py:219: UserWarning: expandable_segments not supported on this platform (Triggered internally at /pytorch/c10/hip/HIPAllocatorConfig.h:29.)
  state_dict[key] = state_dict[key].to(target_device)
[2025-02-10 21:32:45,693]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.20s. Total model size: 234.72MB, VRAM: 0.07MB (0.0%)
[2025-02-10 21:32:45,746]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:32:46,397]::[InvokeAI]::WARNING --> Loading 0.3173828125 MB into VRAM, but only -4820.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:32:46,412]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.02s. Total model size: 1324.96MB, VRAM: 0.32MB (0.0%)
[2025-02-10 21:32:46,450]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:32:47,646]::[InvokeAI]::WARNING --> Loading 0.0732421875 MB into VRAM, but only -4822.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:32:47,651]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder' (CLIPTextModel) onto cuda device in 0.02s. Total model size: 234.72MB, VRAM: 0.07MB (0.0%)
[2025-02-10 21:32:47,655]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:32:47,809]::[InvokeAI]::WARNING --> Loading 0.3173828125 MB into VRAM, but only -4822.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:32:47,823]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:text_encoder_2' (CLIPTextModelWithProjection) onto cuda device in 0.02s. Total model size: 1324.96MB, VRAM: 0.32MB (0.0%)
[2025-02-10 21:32:47,826]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:tokenizer_2' (CLIPTokenizer) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
[2025-02-10 21:32:48,509]::[InvokeAI]::WARNING --> Loading 0.9521484375 MB into VRAM, but only -4822.0 MB were requested. This is the minimum set of weights in VRAM required to run the model.
[2025-02-10 21:32:48,561]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:unet' (UNet2DConditionModel) onto cuda device in 0.08s. Total model size: 4897.05MB, VRAM: 0.95MB (0.0%)
[2025-02-10 21:32:48,568]::[ModelManagerService]::INFO --> [MODEL CACHE] Loaded model '683c44e2-927a-45f6-87da-67b90642e5bf:scheduler' (DDPMScheduler) onto cuda device in 0.00s. Total model size: 0.00MB, VRAM: 0.00MB (0.0%)
:0:rocdevice.cpp            :3020: 7262982208d us:  Callback: Queue 0x77ec42100000 aborting with error : HSA_STATUS_ERROR_INVALID_ISA: The instruction set architecture is invalid. code: 0x100f
Aborted (core dumped)
(.venv) mcon@ikea:~/AMD$ 
```

---

### 评论 #10 — schung-amd (2025-02-11T20:28:27Z)

Thanks for the details! I'll take a look and get back to you on this.

---

### 评论 #11 — schung-amd (2025-02-12T19:17:34Z)

Hi @mcondarelli, can you start invokeai-web with AMD_LOG_LEVEL=7 and provide some of the output leading up to the error? I've reproduced your issue on similar hardware and want to make sure we're seeing the same thing. It seems that, on my system at least, `HSA_OVERRIDE_GFX_VERSION=11.0.0` on its own is not enough to enable this workload on gfx1102, but I'll try to find a workaround.

---

### 评论 #12 — mcondarelli (2025-02-12T20:20:44Z)

Thanks, I assume relevant part is this (but I attach whole file "just in case..."):
```
:3:rocvirtual.cpp           :807 : 78415276251d us: [pid:110451 tid: 7c422ea006c0] Arg0:  BATCHSIZE = val:2
:3:rocvirtual.cpp           :807 : 78415276253d us: [pid:110451 tid: 7c422ea006c0] Arg1:  C = val:4
:3:rocvirtual.cpp           :807 : 78415276256d us: [pid:110451 tid: 7c422ea006c0] Arg2:  H = val:128
:3:rocvirtual.cpp           :807 : 78415276259d us: [pid:110451 tid: 7c422ea006c0] Arg3:  W = val:128
:3:rocvirtual.cpp           :807 : 78415276262d us: [pid:110451 tid: 7c422ea006c0] Arg4:  K = val:320
:3:rocvirtual.cpp           :807 : 78415276264d us: [pid:110451 tid: 7c422ea006c0] Arg5:  n_groups = val:32
:3:rocvirtual.cpp           :807 : 78415276267d us: [pid:110451 tid: 7c422ea006c0] Arg6:  flags = val:17920
:3:rocvirtual.cpp           :807 : 78415276269d us: [pid:110451 tid: 7c422ea006c0] Arg7:  reserved = val:0
:3:rocvirtual.cpp           :731 : 78415276272d us: [pid:110451 tid: 7c422ea006c0] Arg8:  in = ptr:0x7c4193db0000 obj:[0x7c4193c00000-0x7c4193e00000]
:3:rocvirtual.cpp           :731 : 78415276277d us: [pid:110451 tid: 7c422ea006c0] Arg9:  weights = ptr:0x7c41a89f5e00 obj:[0x7c41a8800000-0x7c41a8a00000]
:3:rocvirtual.cpp           :731 : 78415276280d us: [pid:110451 tid: 7c422ea006c0] Arg10:  out = ptr:0x7c40cf200000 obj:[0x7c40cf200000-0x7c40d3e00000]
:3:rocvirtual.cpp           :227 : 78415276275d us: [pid:110451 tid: 7c422d6006c0] Handler: value(0), timestamp(0x7c42101802e0), handle(0x7c43ccbff780)
:3:rocvirtual.cpp           :168 : 78415276300d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbfd800), Translated start/end = 78415275810252 / 78415276170970, Elapsed = 360718 ns, ticks start/end = 7843800667734 / 7843800703806, Ticks elapsed = 36072
:4:command.cpp              :167 : 78415276310d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c42110312b8 complete (Wall: 204005, CPU: 0, GPU: 360 us)
:3:rocvirtual.cpp           :168 : 78415276319d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff780), Translated start/end = 78415276260650 / 78415276272290, Elapsed = 11640 ns, ticks start/end = 7843800712774 / 7843800713938, Ticks elapsed = 1164
:4:command.cpp              :167 : 78415276326d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c4211031ab0 complete (Wall: 204106, CPU: 0, GPU: 11 us)
:3:rocvirtual.cpp           :807 : 78415276284d us: [pid:110451 tid: 7c422ea006c0] Arg12:  R = val:3
:3:rocvirtual.cpp           :807 : 78415276339d us: [pid:110451 tid: 7c422ea006c0] Arg13:  S = val:3
:3:rocvirtual.cpp           :807 : 78415276342d us: [pid:110451 tid: 7c422ea006c0] Arg14:  pad_h = val:1
:3:rocvirtual.cpp           :807 : 78415276344d us: [pid:110451 tid: 7c422ea006c0] Arg15:  pad_w = val:1
:3:rocvirtual.cpp           :807 : 78415276347d us: [pid:110451 tid: 7c422ea006c0] Arg16:  out_h = val:128
:3:rocvirtual.cpp           :807 : 78415276350d us: [pid:110451 tid: 7c422ea006c0] Arg17:  out_w = val:128
:3:rocvirtual.cpp           :807 : 78415276352d us: [pid:110451 tid: 7c422ea006c0] Arg19:  alpha = val:0
:3:rocvirtual.cpp           :807 : 78415276355d us: [pid:110451 tid: 7c422ea006c0] Arg20:  beta = val:0
:3:rocvirtual.cpp           :807 : 78415276357d us: [pid:110451 tid: 7c422ea006c0] Arg21:  d_offset = val:0
:3:rocvirtual.cpp           :807 : 78415276360d us: [pid:110451 tid: 7c422ea006c0] Arg22:  f_offset = val:0
:3:rocvirtual.cpp           :807 : 78415276362d us: [pid:110451 tid: 7c422ea006c0] Arg23:  o_offset = val:0
:3:rocvirtual.cpp           :807 : 78415276365d us: [pid:110451 tid: 7c422ea006c0] Arg24:  b_offset = val:0
:3:rocvirtual.cpp           :807 : 78415276368d us: [pid:110451 tid: 7c422ea006c0] Arg25:  d_N_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415276370d us: [pid:110451 tid: 7c422ea006c0] Arg26:  d_C_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415276373d us: [pid:110451 tid: 7c422ea006c0] Arg27:  d_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415276376d us: [pid:110451 tid: 7c422ea006c0] Arg28:  d_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415276378d us: [pid:110451 tid: 7c422ea006c0] Arg29:  f_K_stride = val:36
:3:rocvirtual.cpp           :807 : 78415276381d us: [pid:110451 tid: 7c422ea006c0] Arg30:  f_C_stride = val:9
:3:rocvirtual.cpp           :807 : 78415276384d us: [pid:110451 tid: 7c422ea006c0] Arg31:  f_R_stride = val:3
:3:rocvirtual.cpp           :807 : 78415276386d us: [pid:110451 tid: 7c422ea006c0] Arg32:  f_S_stride = val:1
:3:rocvirtual.cpp           :807 : 78415276389d us: [pid:110451 tid: 7c422ea006c0] Arg33:  o_N_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415276392d us: [pid:110451 tid: 7c422ea006c0] Arg34:  o_K_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415276395d us: [pid:110451 tid: 7c422ea006c0] Arg35:  o_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415276397d us: [pid:110451 tid: 7c422ea006c0] Arg36:  o_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415276400d us: [pid:110451 tid: 7c422ea006c0] Arg37:  G = val:1
:3:rocvirtual.cpp           :807 : 78415276402d us: [pid:110451 tid: 7c422ea006c0] Arg38:  d_G_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415276405d us: [pid:110451 tid: 7c422ea006c0] Arg39:  f_G_stride = val:11520
:3:rocvirtual.cpp           :807 : 78415276408d us: [pid:110451 tid: 7c422ea006c0] Arg40:  o_G_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415276410d us: [pid:110451 tid: 7c422ea006c0] Arg41:  activation_mode = val:
:3:rocvirtual.cpp           :3056: 78415276412d us: [pid:110451 tid: 7c422ea006c0] ShaderName : miopenSp3AsmConv_v30_3_1_gfx11_fp16_dot2_f2x3_stride1
:4:rocvirtual.cpp           :930 : 78415276418d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[8192, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=65536, kernel_obj=0x7c4261e312c0, kernarg_address=0x7c4216d07680, completion_signal=0x7c43ccbff700, correlation_id=0, rptr=2139, wptr=2139
:3:hip_module.cpp           :489 : 78415276424d us: [pid:110451 tid: 7c422ea006c0] hipExtModuleLaunchKernel: Returned hipSuccess : 
:3:hip_event.cpp            :434 : 78415276428d us: [pid:110451 tid: 7c422ea006c0]  hipEventSynchronize ( event:0x7c40d6412ed0 ) 
:3:rocvirtual.hpp           :67  : 78415276431d us: [pid:110451 tid: 7c422ea006c0] Host active wait for Signal = (0x7c43ccbff700) for -1 ns
:3:hip_event.cpp            :454 : 78415276812d us: [pid:110451 tid: 7c422ea006c0] hipEventSynchronize: Returned hipSuccess : 
:3:hip_event.cpp            :372 : 78415276815d us: [pid:110451 tid: 7c422ea006c0]  hipEventElapsedTime ( 0x7c40d47ec464, event:0x7c40d46e0f20, event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :389 : 78415276820d us: [pid:110451 tid: 7c422ea006c0] hipEventElapsedTime: Returned hipSuccess : Elapsed Time = , 0.360799
:3:hip_event.cpp            :348 : 78415276824d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :368 : 78415276827d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_event.cpp            :348 : 78415276830d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d46e0f20 ) 
:3:hip_event.cpp            :368 : 78415276834d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :664 : 78415276836d us: [pid:110451 tid: 7c422ea006c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :668 : 78415276839d us: [pid:110451 tid: 7c422ea006c0] hipSetDevice: Returned hipSuccess : 
:3:hip_event.cpp            :338 : 78415276842d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9dd8 ) 
:3:hip_event.cpp            :344 : 78415276845d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d46e0f20
:3:hip_event.cpp            :338 : 78415276849d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9dd8 ) 
:3:hip_event.cpp            :344 : 78415276852d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d6412ed0
:3:hip_module.cpp           :477 : 78415276857d us: [pid:110451 tid: 7c422ea006c0]  hipExtModuleLaunchKernel ( 0x0x7c40d55dd0b0, 8192, 1, 1, 256, 1, 1, 0, stream:<null>, char array:<null>, 0x7c422e9f9d30, event:0x7c40d46e0f20, event:0x7c40d6412ed0, 0 ) 
:4:command.cpp              :352 : 78415276865d us: [pid:110451 tid: 7c422ea006c0] Command (InternalMarker) enqueued: 0x7c4211032000
:3:rocvirtual.cpp           :480 : 78415276871d us: [pid:110451 tid: 7c422ea006c0] Set Handler: handle(0x7c43ccbff680), timestamp(0x7c42101f5e20)
:4:rocvirtual.cpp           :1103: 78415276875d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7c43ccbff680
:4:command.cpp              :352 : 78415276880d us: [pid:110451 tid: 7c422ea006c0] Command (KernelExecution) enqueued: 0x7c4211031d58
:3:rocvirtual.cpp           :807 : 78415276883d us: [pid:110451 tid: 7c422ea006c0] Arg0:  BATCHSIZE = val:2
:3:rocvirtual.cpp           :807 : 78415276886d us: [pid:110451 tid: 7c422ea006c0] Arg1:  C = val:4
:3:rocvirtual.cpp           :807 : 78415276889d us: [pid:110451 tid: 7c422ea006c0] Arg2:  H = val:128
:3:rocvirtual.cpp           :807 : 78415276892d us: [pid:110451 tid: 7c422ea006c0] Arg3:  W = val:128
:3:rocvirtual.cpp           :807 : 78415276895d us: [pid:110451 tid: 7c422ea006c0] Arg4:  K = val:320
:3:rocvirtual.cpp           :807 : 78415276897d us: [pid:110451 tid: 7c422ea006c0] Arg5:  n_groups = val:32
:3:rocvirtual.cpp           :807 : 78415276901d us: [pid:110451 tid: 7c422ea006c0] Arg6:  flags = val:17920
:3:rocvirtual.cpp           :807 : 78415276903d us: [pid:110451 tid: 7c422ea006c0] Arg7:  reserved = val:0
:3:rocvirtual.cpp           :731 : 78415276906d us: [pid:110451 tid: 7c422ea006c0] Arg8:  in = ptr:0x7c4193db0000 obj:[0x7c4193c00000-0x7c4193e00000]
:3:rocvirtual.cpp           :731 : 78415276911d us: [pid:110451 tid: 7c422ea006c0] Arg9:  weights = ptr:0x7c41a89f5e00 obj:[0x7c41a8800000-0x7c41a8a00000]
:3:rocvirtual.cpp           :731 : 78415276914d us: [pid:110451 tid: 7c422ea006c0] Arg10:  out = ptr:0x7c40cf200000 obj:[0x7c40cf200000-0x7c40d3e00000]
:3:rocvirtual.cpp           :807 : 78415276918d us: [pid:110451 tid: 7c422ea006c0] Arg12:  R = val:3
:3:rocvirtual.cpp           :807 : 78415276921d us: [pid:110451 tid: 7c422ea006c0] Arg13:  S = val:3
:3:rocvirtual.cpp           :807 : 78415276924d us: [pid:110451 tid: 7c422ea006c0] Arg14:  pad_h = val:1
:3:rocvirtual.cpp           :807 : 78415276928d us: [pid:110451 tid: 7c422ea006c0] Arg15:  pad_w = val:1
:3:rocvirtual.cpp           :807 : 78415276930d us: [pid:110451 tid: 7c422ea006c0] Arg16:  out_h = val:128
:3:rocvirtual.cpp           :807 : 78415276935d us: [pid:110451 tid: 7c422ea006c0] Arg17:  out_w = val:128
:3:rocvirtual.cpp           :807 : 78415276937d us: [pid:110451 tid: 7c422ea006c0] Arg19:  alpha = val:0
:3:rocvirtual.cpp           :807 : 78415276942d us: [pid:110451 tid: 7c422ea006c0] Arg20:  beta = val:0
:3:rocvirtual.cpp           :807 : 78415276944d us: [pid:110451 tid: 7c422ea006c0] Arg21:  d_offset = val:0
:3:rocvirtual.cpp           :227 : 78415276908d us: [pid:110451 tid: 7c422d6006c0] Handler: value(0), timestamp(0x7c40d5167a70), handle(0x7c43ccbff680)
:3:rocvirtual.cpp           :168 : 78415276956d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff700), Translated start/end = 78415276445849 / 78415276806648, Elapsed = 360799 ns, ticks start/end = 7843800731294 / 7843800767374, Ticks elapsed = 36080
:4:command.cpp              :167 : 78415276966d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c4211031808 complete (Wall: 204641, CPU: 0, GPU: 360 us)
:3:rocvirtual.cpp           :168 : 78415276974d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff680), Translated start/end = 78415276894058 / 78415276905658, Elapsed = 11600 ns, ticks start/end = 7843800776115 / 7843800777275, Ticks elapsed = 1160
:4:command.cpp              :167 : 78415276982d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c4211032000 complete (Wall: 204740, CPU: 0, GPU: 11 us)
:3:rocvirtual.cpp           :807 : 78415276946d us: [pid:110451 tid: 7c422ea006c0] Arg22:  f_offset = val:0
:3:rocvirtual.cpp           :807 : 78415276994d us: [pid:110451 tid: 7c422ea006c0] Arg23:  o_offset = val:0
:3:rocvirtual.cpp           :807 : 78415276997d us: [pid:110451 tid: 7c422ea006c0] Arg24:  b_offset = val:0
:3:rocvirtual.cpp           :807 : 78415277004d us: [pid:110451 tid: 7c422ea006c0] Arg25:  d_N_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415277006d us: [pid:110451 tid: 7c422ea006c0] Arg26:  d_C_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415277010d us: [pid:110451 tid: 7c422ea006c0] Arg27:  d_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415277013d us: [pid:110451 tid: 7c422ea006c0] Arg28:  d_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415277015d us: [pid:110451 tid: 7c422ea006c0] Arg29:  f_K_stride = val:36
:3:rocvirtual.cpp           :807 : 78415277018d us: [pid:110451 tid: 7c422ea006c0] Arg30:  f_C_stride = val:9
:3:rocvirtual.cpp           :807 : 78415277021d us: [pid:110451 tid: 7c422ea006c0] Arg31:  f_R_stride = val:3
:3:rocvirtual.cpp           :807 : 78415277023d us: [pid:110451 tid: 7c422ea006c0] Arg32:  f_S_stride = val:1
:3:rocvirtual.cpp           :807 : 78415277026d us: [pid:110451 tid: 7c422ea006c0] Arg33:  o_N_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415277029d us: [pid:110451 tid: 7c422ea006c0] Arg34:  o_K_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415277032d us: [pid:110451 tid: 7c422ea006c0] Arg35:  o_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415277034d us: [pid:110451 tid: 7c422ea006c0] Arg36:  o_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415277037d us: [pid:110451 tid: 7c422ea006c0] Arg37:  G = val:1
:3:rocvirtual.cpp           :807 : 78415277040d us: [pid:110451 tid: 7c422ea006c0] Arg38:  d_G_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415277042d us: [pid:110451 tid: 7c422ea006c0] Arg39:  f_G_stride = val:11520
:3:rocvirtual.cpp           :807 : 78415277045d us: [pid:110451 tid: 7c422ea006c0] Arg40:  o_G_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415277048d us: [pid:110451 tid: 7c422ea006c0] Arg41:  activation_mode = val:
:3:rocvirtual.cpp           :3056: 78415277050d us: [pid:110451 tid: 7c422ea006c0] ShaderName : miopenSp3AsmConv_v30_3_1_gfx11_fp16_dot2_f2x3_stride1
:4:rocvirtual.cpp           :930 : 78415277057d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[8192, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=65536, kernel_obj=0x7c4261e312c0, kernarg_address=0x7c4216d07780, completion_signal=0x7c43ccbff600, correlation_id=0, rptr=2141, wptr=2141
:3:hip_module.cpp           :489 : 78415277063d us: [pid:110451 tid: 7c422ea006c0] hipExtModuleLaunchKernel: Returned hipSuccess : 
:3:hip_event.cpp            :434 : 78415277067d us: [pid:110451 tid: 7c422ea006c0]  hipEventSynchronize ( event:0x7c40d6412ed0 ) 
:3:rocvirtual.hpp           :67  : 78415277071d us: [pid:110451 tid: 7c422ea006c0] Host active wait for Signal = (0x7c43ccbff600) for -1 ns
:3:hip_event.cpp            :454 : 78415277451d us: [pid:110451 tid: 7c422ea006c0] hipEventSynchronize: Returned hipSuccess : 
:3:hip_event.cpp            :372 : 78415277455d us: [pid:110451 tid: 7c422ea006c0]  hipEventElapsedTime ( 0x7c40d47ec464, event:0x7c40d46e0f20, event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :389 : 78415277461d us: [pid:110451 tid: 7c422ea006c0] hipEventElapsedTime: Returned hipSuccess : Elapsed Time = , 0.360919
:3:hip_event.cpp            :348 : 78415277465d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :368 : 78415277468d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_event.cpp            :348 : 78415277471d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d46e0f20 ) 
:3:hip_event.cpp            :368 : 78415277475d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :664 : 78415277478d us: [pid:110451 tid: 7c422ea006c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :668 : 78415277480d us: [pid:110451 tid: 7c422ea006c0] hipSetDevice: Returned hipSuccess : 
:3:hip_event.cpp            :338 : 78415277483d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9dd8 ) 
:3:hip_event.cpp            :344 : 78415277486d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d46e0f20
:3:hip_event.cpp            :338 : 78415277489d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9dd8 ) 
:3:hip_event.cpp            :344 : 78415277492d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d6412ed0
:3:hip_module.cpp           :477 : 78415277498d us: [pid:110451 tid: 7c422ea006c0]  hipExtModuleLaunchKernel ( 0x0x7c40d55dd0b0, 8192, 1, 1, 256, 1, 1, 0, stream:<null>, char array:<null>, 0x7c422e9f9d30, event:0x7c40d46e0f20, event:0x7c40d6412ed0, 0 ) 
:4:command.cpp              :352 : 78415277504d us: [pid:110451 tid: 7c422ea006c0] Command (InternalMarker) enqueued: 0x7c4211032550
:3:rocvirtual.cpp           :480 : 78415277511d us: [pid:110451 tid: 7c422ea006c0] Set Handler: handle(0x7c43ccbff580), timestamp(0x7c42116ddcb0)
:4:rocvirtual.cpp           :1103: 78415277515d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7c43ccbff580
:4:command.cpp              :352 : 78415277520d us: [pid:110451 tid: 7c422ea006c0] Command (KernelExecution) enqueued: 0x7c42110322a8
:3:rocvirtual.cpp           :807 : 78415277524d us: [pid:110451 tid: 7c422ea006c0] Arg0:  BATCHSIZE = val:2
:3:rocvirtual.cpp           :807 : 78415277526d us: [pid:110451 tid: 7c422ea006c0] Arg1:  C = val:4
:3:rocvirtual.cpp           :807 : 78415277529d us: [pid:110451 tid: 7c422ea006c0] Arg2:  H = val:128
:3:rocvirtual.cpp           :807 : 78415277532d us: [pid:110451 tid: 7c422ea006c0] Arg3:  W = val:128
:3:rocvirtual.cpp           :807 : 78415277534d us: [pid:110451 tid: 7c422ea006c0] Arg4:  K = val:320
:3:rocvirtual.cpp           :807 : 78415277537d us: [pid:110451 tid: 7c422ea006c0] Arg5:  n_groups = val:32
:3:rocvirtual.cpp           :807 : 78415277540d us: [pid:110451 tid: 7c422ea006c0] Arg6:  flags = val:17920
:3:rocvirtual.cpp           :807 : 78415277542d us: [pid:110451 tid: 7c422ea006c0] Arg7:  reserved = val:0
:3:rocvirtual.cpp           :731 : 78415277545d us: [pid:110451 tid: 7c422ea006c0] Arg8:  in = ptr:0x7c4193db0000 obj:[0x7c4193c00000-0x7c4193e00000]
:3:rocvirtual.cpp           :227 : 78415277548d us: [pid:110451 tid: 7c422d6006c0] Handler: value(0), timestamp(0x7c40d5167b40), handle(0x7c43ccbff580)
:3:rocvirtual.cpp           :168 : 78415277565d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff600), Translated start/end = 78415277085107 / 78415277446026, Elapsed = 360919 ns, ticks start/end = 7843800795220 / 7843800831312, Ticks elapsed = 36092
:4:command.cpp              :167 : 78415277576d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c4211031d58 complete (Wall: 205280, CPU: 0, GPU: 360 us)
:3:rocvirtual.cpp           :168 : 78415277585d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff580), Translated start/end = 78415277533675 / 78415277545315, Elapsed = 11640 ns, ticks start/end = 7843800840077 / 7843800841241, Ticks elapsed = 1164
:4:command.cpp              :167 : 78415277592d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c4211032550 complete (Wall: 205380, CPU: 0, GPU: 11 us)
:3:rocvirtual.cpp           :731 : 78415277565d us: [pid:110451 tid: 7c422ea006c0] Arg9:  weights = ptr:0x7c41a89f5e00 obj:[0x7c41a8800000-0x7c41a8a00000]
:3:rocvirtual.cpp           :731 : 78415277606d us: [pid:110451 tid: 7c422ea006c0] Arg10:  out = ptr:0x7c40cf200000 obj:[0x7c40cf200000-0x7c40d3e00000]
:3:rocvirtual.cpp           :807 : 78415277609d us: [pid:110451 tid: 7c422ea006c0] Arg12:  R = val:3
:3:rocvirtual.cpp           :807 : 78415277612d us: [pid:110451 tid: 7c422ea006c0] Arg13:  S = val:3
:3:rocvirtual.cpp           :807 : 78415277614d us: [pid:110451 tid: 7c422ea006c0] Arg14:  pad_h = val:1
:3:rocvirtual.cpp           :807 : 78415277617d us: [pid:110451 tid: 7c422ea006c0] Arg15:  pad_w = val:1
:3:rocvirtual.cpp           :807 : 78415277620d us: [pid:110451 tid: 7c422ea006c0] Arg16:  out_h = val:128
:3:rocvirtual.cpp           :807 : 78415277622d us: [pid:110451 tid: 7c422ea006c0] Arg17:  out_w = val:128
:3:rocvirtual.cpp           :807 : 78415277624d us: [pid:110451 tid: 7c422ea006c0] Arg19:  alpha = val:0
:3:rocvirtual.cpp           :807 : 78415277627d us: [pid:110451 tid: 7c422ea006c0] Arg20:  beta = val:0
:3:rocvirtual.cpp           :807 : 78415277630d us: [pid:110451 tid: 7c422ea006c0] Arg21:  d_offset = val:0
:3:rocvirtual.cpp           :807 : 78415277633d us: [pid:110451 tid: 7c422ea006c0] Arg22:  f_offset = val:0
:3:rocvirtual.cpp           :807 : 78415277635d us: [pid:110451 tid: 7c422ea006c0] Arg23:  o_offset = val:0
:3:rocvirtual.cpp           :807 : 78415277638d us: [pid:110451 tid: 7c422ea006c0] Arg24:  b_offset = val:0
:3:rocvirtual.cpp           :807 : 78415277641d us: [pid:110451 tid: 7c422ea006c0] Arg25:  d_N_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415277644d us: [pid:110451 tid: 7c422ea006c0] Arg26:  d_C_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415277647d us: [pid:110451 tid: 7c422ea006c0] Arg27:  d_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415277650d us: [pid:110451 tid: 7c422ea006c0] Arg28:  d_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415277652d us: [pid:110451 tid: 7c422ea006c0] Arg29:  f_K_stride = val:36
:3:rocvirtual.cpp           :807 : 78415277655d us: [pid:110451 tid: 7c422ea006c0] Arg30:  f_C_stride = val:9
:3:rocvirtual.cpp           :807 : 78415277658d us: [pid:110451 tid: 7c422ea006c0] Arg31:  f_R_stride = val:3
:3:rocvirtual.cpp           :807 : 78415277660d us: [pid:110451 tid: 7c422ea006c0] Arg32:  f_S_stride = val:1
:3:rocvirtual.cpp           :807 : 78415277662d us: [pid:110451 tid: 7c422ea006c0] Arg33:  o_N_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415277665d us: [pid:110451 tid: 7c422ea006c0] Arg34:  o_K_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415277668d us: [pid:110451 tid: 7c422ea006c0] Arg35:  o_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415277670d us: [pid:110451 tid: 7c422ea006c0] Arg36:  o_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415277673d us: [pid:110451 tid: 7c422ea006c0] Arg37:  G = val:1
:3:rocvirtual.cpp           :807 : 78415277676d us: [pid:110451 tid: 7c422ea006c0] Arg38:  d_G_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415277678d us: [pid:110451 tid: 7c422ea006c0] Arg39:  f_G_stride = val:11520
:3:rocvirtual.cpp           :807 : 78415277681d us: [pid:110451 tid: 7c422ea006c0] Arg40:  o_G_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415277684d us: [pid:110451 tid: 7c422ea006c0] Arg41:  activation_mode = val:
:3:rocvirtual.cpp           :3056: 78415277687d us: [pid:110451 tid: 7c422ea006c0] ShaderName : miopenSp3AsmConv_v30_3_1_gfx11_fp16_dot2_f2x3_stride1
:4:rocvirtual.cpp           :930 : 78415277692d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[8192, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=65536, kernel_obj=0x7c4261e312c0, kernarg_address=0x7c4216d07880, completion_signal=0x7c43ccbff500, correlation_id=0, rptr=2143, wptr=2143
:3:hip_module.cpp           :489 : 78415277699d us: [pid:110451 tid: 7c422ea006c0] hipExtModuleLaunchKernel: Returned hipSuccess : 
:3:hip_event.cpp            :434 : 78415277703d us: [pid:110451 tid: 7c422ea006c0]  hipEventSynchronize ( event:0x7c40d6412ed0 ) 
:3:rocvirtual.hpp           :67  : 78415277707d us: [pid:110451 tid: 7c422ea006c0] Host active wait for Signal = (0x7c43ccbff500) for -1 ns
:3:hip_event.cpp            :454 : 78415278085d us: [pid:110451 tid: 7c422ea006c0] hipEventSynchronize: Returned hipSuccess : 
:3:hip_event.cpp            :372 : 78415278088d us: [pid:110451 tid: 7c422ea006c0]  hipEventElapsedTime ( 0x7c40d47ec464, event:0x7c40d46e0f20, event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :389 : 78415278094d us: [pid:110451 tid: 7c422ea006c0] hipEventElapsedTime: Returned hipSuccess : Elapsed Time = , 0.360718
:3:hip_event.cpp            :348 : 78415278098d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :368 : 78415278101d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_event.cpp            :348 : 78415278104d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d46e0f20 ) 
:3:hip_event.cpp            :368 : 78415278109d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :664 : 78415278112d us: [pid:110451 tid: 7c422ea006c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :668 : 78415278115d us: [pid:110451 tid: 7c422ea006c0] hipSetDevice: Returned hipSuccess : 
:3:hip_event.cpp            :338 : 78415278118d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9dd8 ) 
:3:hip_event.cpp            :344 : 78415278121d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d46e0f20
:3:hip_event.cpp            :338 : 78415278124d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9dd8 ) 
:3:hip_event.cpp            :344 : 78415278127d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d6412ed0
:3:hip_module.cpp           :477 : 78415278133d us: [pid:110451 tid: 7c422ea006c0]  hipExtModuleLaunchKernel ( 0x0x7c40d55dd0b0, 8192, 1, 1, 256, 1, 1, 0, stream:<null>, char array:<null>, 0x7c422e9f9d30, event:0x7c40d46e0f20, event:0x7c40d6412ed0, 0 ) 
:4:command.cpp              :352 : 78415278139d us: [pid:110451 tid: 7c422ea006c0] Command (InternalMarker) enqueued: 0x7c4211032aa0
:3:rocvirtual.cpp           :480 : 78415278145d us: [pid:110451 tid: 7c422ea006c0] Set Handler: handle(0x7c43ccbff480), timestamp(0x7c421014e240)
:4:rocvirtual.cpp           :1103: 78415278149d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7c43ccbff480
:4:command.cpp              :352 : 78415278155d us: [pid:110451 tid: 7c422ea006c0] Command (KernelExecution) enqueued: 0x7c42110327f8
:3:rocvirtual.cpp           :807 : 78415278158d us: [pid:110451 tid: 7c422ea006c0] Arg0:  BATCHSIZE = val:2
:3:rocvirtual.cpp           :807 : 78415278161d us: [pid:110451 tid: 7c422ea006c0] Arg1:  C = val:4
:3:rocvirtual.cpp           :807 : 78415278164d us: [pid:110451 tid: 7c422ea006c0] Arg2:  H = val:128
:3:rocvirtual.cpp           :807 : 78415278166d us: [pid:110451 tid: 7c422ea006c0] Arg3:  W = val:128
:3:rocvirtual.cpp           :807 : 78415278169d us: [pid:110451 tid: 7c422ea006c0] Arg4:  K = val:320
:3:rocvirtual.cpp           :807 : 78415278171d us: [pid:110451 tid: 7c422ea006c0] Arg5:  n_groups = val:32
:3:rocvirtual.cpp           :807 : 78415278174d us: [pid:110451 tid: 7c422ea006c0] Arg6:  flags = val:17920
:3:rocvirtual.cpp           :807 : 78415278176d us: [pid:110451 tid: 7c422ea006c0] Arg7:  reserved = val:0
:3:rocvirtual.cpp           :731 : 78415278179d us: [pid:110451 tid: 7c422ea006c0] Arg8:  in = ptr:0x7c4193db0000 obj:[0x7c4193c00000-0x7c4193e00000]
:3:rocvirtual.cpp           :227 : 78415278182d us: [pid:110451 tid: 7c422d6006c0] Handler: value(0), timestamp(0x7c41d5a6e3d0), handle(0x7c43ccbff480)
:3:rocvirtual.cpp           :731 : 78415278183d us: [pid:110451 tid: 7c422ea006c0] Arg9:  weights = ptr:0x7c41a89f5e00 obj:[0x7c41a8800000-0x7c41a8a00000]
:3:rocvirtual.cpp           :731 : 78415278201d us: [pid:110451 tid: 7c422ea006c0] Arg10:  out = ptr:0x7c40cf200000 obj:[0x7c40cf200000-0x7c40d3e00000]
:3:rocvirtual.cpp           :807 : 78415278205d us: [pid:110451 tid: 7c422ea006c0] Arg12:  R = val:3
:3:rocvirtual.cpp           :807 : 78415278209d us: [pid:110451 tid: 7c422ea006c0] Arg13:  S = val:3
:3:rocvirtual.cpp           :807 : 78415278211d us: [pid:110451 tid: 7c422ea006c0] Arg14:  pad_h = val:1
:3:rocvirtual.cpp           :807 : 78415278215d us: [pid:110451 tid: 7c422ea006c0] Arg15:  pad_w = val:1
:3:rocvirtual.cpp           :807 : 78415278218d us: [pid:110451 tid: 7c422ea006c0] Arg16:  out_h = val:128
:3:rocvirtual.cpp           :807 : 78415278221d us: [pid:110451 tid: 7c422ea006c0] Arg17:  out_w = val:128
:3:rocvirtual.cpp           :807 : 78415278224d us: [pid:110451 tid: 7c422ea006c0] Arg19:  alpha = val:0
:3:rocvirtual.cpp           :807 : 78415278228d us: [pid:110451 tid: 7c422ea006c0] Arg20:  beta = val:0
:3:rocvirtual.cpp           :807 : 78415278230d us: [pid:110451 tid: 7c422ea006c0] Arg21:  d_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278234d us: [pid:110451 tid: 7c422ea006c0] Arg22:  f_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278237d us: [pid:110451 tid: 7c422ea006c0] Arg23:  o_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278240d us: [pid:110451 tid: 7c422ea006c0] Arg24:  b_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278243d us: [pid:110451 tid: 7c422ea006c0] Arg25:  d_N_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415278246d us: [pid:110451 tid: 7c422ea006c0] Arg26:  d_C_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415278249d us: [pid:110451 tid: 7c422ea006c0] Arg27:  d_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415278252d us: [pid:110451 tid: 7c422ea006c0] Arg28:  d_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415278255d us: [pid:110451 tid: 7c422ea006c0] Arg29:  f_K_stride = val:36
:3:rocvirtual.cpp           :807 : 78415278258d us: [pid:110451 tid: 7c422ea006c0] Arg30:  f_C_stride = val:9
:3:rocvirtual.cpp           :168 : 78415278196d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff500), Translated start/end = 78415277718335 / 78415278079053, Elapsed = 360718 ns, ticks start/end = 7843800858543 / 7843800894615, Ticks elapsed = 36072
:4:command.cpp              :167 : 78415278271d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c42110322a8 complete (Wall: 205913, CPU: 0, GPU: 360 us)
:3:rocvirtual.cpp           :168 : 78415278280d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff480), Translated start/end = 78415278168013 / 78415278179653, Elapsed = 11640 ns, ticks start/end = 7843800903511 / 7843800904675, Ticks elapsed = 1164
:4:command.cpp              :167 : 78415278288d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c4211032aa0 complete (Wall: 206014, CPU: 0, GPU: 11 us)
:3:rocvirtual.cpp           :807 : 78415278261d us: [pid:110451 tid: 7c422ea006c0] Arg31:  f_R_stride = val:3
:3:rocvirtual.cpp           :807 : 78415278300d us: [pid:110451 tid: 7c422ea006c0] Arg32:  f_S_stride = val:1
:3:rocvirtual.cpp           :807 : 78415278303d us: [pid:110451 tid: 7c422ea006c0] Arg33:  o_N_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415278306d us: [pid:110451 tid: 7c422ea006c0] Arg34:  o_K_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415278308d us: [pid:110451 tid: 7c422ea006c0] Arg35:  o_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415278311d us: [pid:110451 tid: 7c422ea006c0] Arg36:  o_W_stride = val:1
:3:rocvirtual.cpp           :807 : 78415278313d us: [pid:110451 tid: 7c422ea006c0] Arg37:  G = val:1
:3:rocvirtual.cpp           :807 : 78415278316d us: [pid:110451 tid: 7c422ea006c0] Arg38:  d_G_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415278318d us: [pid:110451 tid: 7c422ea006c0] Arg39:  f_G_stride = val:11520
:3:rocvirtual.cpp           :807 : 78415278321d us: [pid:110451 tid: 7c422ea006c0] Arg40:  o_G_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415278323d us: [pid:110451 tid: 7c422ea006c0] Arg41:  activation_mode = val:
:3:rocvirtual.cpp           :3056: 78415278326d us: [pid:110451 tid: 7c422ea006c0] ShaderName : miopenSp3AsmConv_v30_3_1_gfx11_fp16_dot2_f2x3_stride1
:4:rocvirtual.cpp           :930 : 78415278332d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[8192, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=65536, kernel_obj=0x7c4261e312c0, kernarg_address=0x7c4216d07980, completion_signal=0x7c43ccbff400, correlation_id=0, rptr=2145, wptr=2145
:3:hip_module.cpp           :489 : 78415278339d us: [pid:110451 tid: 7c422ea006c0] hipExtModuleLaunchKernel: Returned hipSuccess : 
:3:hip_event.cpp            :434 : 78415278342d us: [pid:110451 tid: 7c422ea006c0]  hipEventSynchronize ( event:0x7c40d6412ed0 ) 
:3:rocvirtual.hpp           :67  : 78415278346d us: [pid:110451 tid: 7c422ea006c0] Host active wait for Signal = (0x7c43ccbff400) for -1 ns
:3:hip_event.cpp            :454 : 78415278727d us: [pid:110451 tid: 7c422ea006c0] hipEventSynchronize: Returned hipSuccess : 
:3:hip_event.cpp            :372 : 78415278730d us: [pid:110451 tid: 7c422ea006c0]  hipEventElapsedTime ( 0x7c40d47ec464, event:0x7c40d46e0f20, event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :389 : 78415278735d us: [pid:110451 tid: 7c422ea006c0] hipEventElapsedTime: Returned hipSuccess : Elapsed Time = , 0.361159
:3:hip_event.cpp            :348 : 78415278739d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d6412ed0 ) 
:3:hip_event.cpp            :368 : 78415278742d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_event.cpp            :348 : 78415278745d us: [pid:110451 tid: 7c422ea006c0]  hipEventDestroy ( event:0x7c40d46e0f20 ) 
:3:hip_event.cpp            :368 : 78415278749d us: [pid:110451 tid: 7c422ea006c0] hipEventDestroy: Returned hipSuccess : 
:3:hip_module.cpp           :74  : 78415278758d us: [pid:110451 tid: 7c422ea006c0]  hipModuleGetFunction ( 0x7c422e9fa0c8, 0x7c40d49d96c0, miopenSp3AsmConvFury_v2_4_1_gfx11_1536vgprs_fp16_fp16acc_f2x3_c16_stride1 ) 
:3:hip_module.cpp           :88  : 78415278764d us: [pid:110451 tid: 7c422ea006c0] hipModuleGetFunction: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :664 : 78415278767d us: [pid:110451 tid: 7c422ea006c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :668 : 78415278770d us: [pid:110451 tid: 7c422ea006c0] hipSetDevice: Returned hipSuccess : 
:3:hip_event.cpp            :338 : 78415278775d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9d28 ) 
:3:hip_event.cpp            :344 : 78415278778d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d46e0f20
:3:hip_event.cpp            :338 : 78415278781d us: [pid:110451 tid: 7c422ea006c0]  hipEventCreate ( 0x7c422e9f9d28 ) 
:3:hip_event.cpp            :344 : 78415278784d us: [pid:110451 tid: 7c422ea006c0] hipEventCreate: Returned hipSuccess : event:0x7c40d6412ed0
:3:hip_module.cpp           :477 : 78415278790d us: [pid:110451 tid: 7c422ea006c0]  hipExtModuleLaunchKernel ( 0x0x7c40d49e88b0, 12288, 1, 1, 384, 1, 1, 0, stream:<null>, char array:<null>, 0x7c422e9f9c80, event:0x7c40d46e0f20, event:0x7c40d6412ed0, 0 ) 
:4:command.cpp              :352 : 78415278797d us: [pid:110451 tid: 7c422ea006c0] Command (InternalMarker) enqueued: 0x7c4211032ff0
:3:rocvirtual.cpp           :480 : 78415278803d us: [pid:110451 tid: 7c422ea006c0] Set Handler: handle(0x7c43ccbff380), timestamp(0x7c42101edca0)
:4:rocvirtual.cpp           :1103: 78415278807d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7c43ccbff380
:4:command.cpp              :352 : 78415278812d us: [pid:110451 tid: 7c422ea006c0] Command (KernelExecution) enqueued: 0x7c4211032d48
:3:rocvirtual.cpp           :807 : 78415278816d us: [pid:110451 tid: 7c422ea006c0] Arg0:  N_ = val:2
:3:rocvirtual.cpp           :807 : 78415278818d us: [pid:110451 tid: 7c422ea006c0] Arg1:  C = val:4
:3:rocvirtual.cpp           :807 : 78415278821d us: [pid:110451 tid: 7c422ea006c0] Arg2:  H = val:128
:3:rocvirtual.cpp           :807 : 78415278824d us: [pid:110451 tid: 7c422ea006c0] Arg3:  W = val:128
:3:rocvirtual.cpp           :807 : 78415278827d us: [pid:110451 tid: 7c422ea006c0] Arg4:  K = val:320
:3:rocvirtual.cpp           :807 : 78415278830d us: [pid:110451 tid: 7c422ea006c0] Arg5:  n_groups = val:32
:3:rocvirtual.cpp           :807 : 78415278833d us: [pid:110451 tid: 7c422ea006c0] Arg6:  flags64 = val:57856
:3:rocvirtual.cpp           :731 : 78415278836d us: [pid:110451 tid: 7c422ea006c0] Arg7:  data_addr = ptr:0x7c4193db0000 obj:[0x7c4193c00000-0x7c4193e00000]
:3:rocvirtual.cpp           :731 : 78415278839d us: [pid:110451 tid: 7c422ea006c0] Arg8:  filter_addr = ptr:0x7c41a89f5e00 obj:[0x7c41a8800000-0x7c41a8a00000]
:3:rocvirtual.cpp           :731 : 78415278844d us: [pid:110451 tid: 7c422ea006c0] Arg9:  output_addr = ptr:0x7c40cf200000 obj:[0x7c40cf200000-0x7c40d3e00000]
:3:rocvirtual.cpp           :807 : 78415278848d us: [pid:110451 tid: 7c422ea006c0] Arg10:   = val:0
:3:rocvirtual.cpp           :227 : 78415278841d us: [pid:110451 tid: 7c422d6006c0] Handler: value(0), timestamp(0x7c40d62f0ca0), handle(0x7c43ccbff380)
:3:rocvirtual.cpp           :168 : 78415278862d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff400), Translated start/end = 78415278360222 / 78415278721381, Elapsed = 361159 ns, ticks start/end = 7843800922732 / 7843800958848, Ticks elapsed = 36116
:4:command.cpp              :167 : 78415278872d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c42110327f8 complete (Wall: 206556, CPU: 0, GPU: 361 us)
:3:rocvirtual.cpp           :168 : 78415278880d us: [pid:110451 tid: 7c422d6006c0] Signal = (0x7c43ccbff380), Translated start/end = 78415278826660 / 78415278838300, Elapsed = 11640 ns, ticks start/end = 7843800969376 / 7843800970540, Ticks elapsed = 1164
:4:command.cpp              :167 : 78415278888d us: [pid:110451 tid: 7c422d6006c0] Command 0x7c4211032ff0 complete (Wall: 206673, CPU: 0, GPU: 11 us)
:3:rocvirtual.cpp           :807 : 78415278850d us: [pid:110451 tid: 7c422ea006c0] Arg11:  R = val:3
:3:rocvirtual.cpp           :807 : 78415278901d us: [pid:110451 tid: 7c422ea006c0] Arg12:  S = val:3
:3:rocvirtual.cpp           :807 : 78415278904d us: [pid:110451 tid: 7c422ea006c0] Arg13:  pad_h = val:1
:3:rocvirtual.cpp           :807 : 78415278906d us: [pid:110451 tid: 7c422ea006c0] Arg14:  pad_w = val:1
:3:rocvirtual.cpp           :807 : 78415278909d us: [pid:110451 tid: 7c422ea006c0] Arg15:  out_h = val:128
:3:rocvirtual.cpp           :807 : 78415278912d us: [pid:110451 tid: 7c422ea006c0] Arg16:  out_w = val:128
:3:rocvirtual.cpp           :807 : 78415278915d us: [pid:110451 tid: 7c422ea006c0] Arg18:  alpha = val:0
:3:rocvirtual.cpp           :807 : 78415278918d us: [pid:110451 tid: 7c422ea006c0] Arg19:  beta = val:0
:3:rocvirtual.cpp           :807 : 78415278921d us: [pid:110451 tid: 7c422ea006c0] Arg20:  d_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278923d us: [pid:110451 tid: 7c422ea006c0] Arg21:  f_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278925d us: [pid:110451 tid: 7c422ea006c0] Arg22:  o_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278928d us: [pid:110451 tid: 7c422ea006c0] Arg23:  b_offset = val:0
:3:rocvirtual.cpp           :807 : 78415278931d us: [pid:110451 tid: 7c422ea006c0] Arg24:  d_N_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415278934d us: [pid:110451 tid: 7c422ea006c0] Arg25:  d_C_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415278936d us: [pid:110451 tid: 7c422ea006c0] Arg26:  d_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415278939d us: [pid:110451 tid: 7c422ea006c0] Arg27:   = val:0
:3:rocvirtual.cpp           :807 : 78415278942d us: [pid:110451 tid: 7c422ea006c0] Arg28:  f_K_stride = val:36
:3:rocvirtual.cpp           :807 : 78415278945d us: [pid:110451 tid: 7c422ea006c0] Arg29:  f_C_stride = val:9
:3:rocvirtual.cpp           :807 : 78415278948d us: [pid:110451 tid: 7c422ea006c0] Arg30:  f_R_stride = val:3
:3:rocvirtual.cpp           :807 : 78415278951d us: [pid:110451 tid: 7c422ea006c0] Arg31:   = val:0
:3:rocvirtual.cpp           :807 : 78415278953d us: [pid:110451 tid: 7c422ea006c0] Arg32:  o_N_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415278955d us: [pid:110451 tid: 7c422ea006c0] Arg33:  o_K_stride = val:16384
:3:rocvirtual.cpp           :807 : 78415278958d us: [pid:110451 tid: 7c422ea006c0] Arg34:  o_H_stride = val:128
:3:rocvirtual.cpp           :807 : 78415278961d us: [pid:110451 tid: 7c422ea006c0] Arg35:   = val:0
:3:rocvirtual.cpp           :807 : 78415278964d us: [pid:110451 tid: 7c422ea006c0] Arg36:  G = val:1
:3:rocvirtual.cpp           :807 : 78415278967d us: [pid:110451 tid: 7c422ea006c0] Arg37:  d_G_stride = val:65536
:3:rocvirtual.cpp           :807 : 78415278970d us: [pid:110451 tid: 7c422ea006c0] Arg38:  f_G_stride = val:11520
:3:rocvirtual.cpp           :807 : 78415278973d us: [pid:110451 tid: 7c422ea006c0] Arg39:  o_G_stride = val:5242880
:3:rocvirtual.cpp           :807 : 78415278975d us: [pid:110451 tid: 7c422ea006c0] Arg40:  activation_mode = val:
:3:rocvirtual.cpp           :807 : 78415278978d us: [pid:110451 tid: 7c422ea006c0] Arg41:  sync_limit = val:
:3:rocvirtual.cpp           :807 : 78415278981d us: [pid:110451 tid: 7c422ea006c0] Arg42:  sync_period = val:
:3:rocvirtual.cpp           :807 : 78415278983d us: [pid:110451 tid: 7c422ea006c0] Arg43:   = val:
:3:rocvirtual.cpp           :807 : 78415278986d us: [pid:110451 tid: 7c422ea006c0] Arg44:   = val:0
:3:rocvirtual.cpp           :807 : 78415278988d us: [pid:110451 tid: 7c422ea006c0] Arg47:  a_offset = val:0
:3:rocvirtual.cpp           :3056: 78415278991d us: [pid:110451 tid: 7c422ea006c0] ShaderName : miopenSp3AsmConvFury_v2_4_1_gfx11_1536vgprs_fp16_fp16acc_f2x3_c16_stride1
:4:rocvirtual.cpp           :930 : 78415278996d us: [pid:110451 tid: 7c422ea006c0] SWq=0x7c441ee02000, HWq=0x7c4217d00000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[12288, 1, 1], workgroup=[384, 1, 1], private_seg_size=0, group_seg_size=65536, kernel_obj=0x7c4261e10f80, kernarg_address=0x7c4216d07a80, completion_signal=0x7c43ccbff300, correlation_id=0, rptr=2147, wptr=2147
:3:hip_module.cpp           :489 : 78415279007d us: [pid:110451 tid: 7c422ea006c0] hipExtModuleLaunchKernel: Returned hipSuccess : 
:3:hip_event.cpp            :434 : 78415279011d us: [pid:110451 tid: 7c422ea006c0]  hipEventSynchronize ( event:0x7c40d6412ed0 ) 
:3:rocvirtual.hpp           :67  : 78415279014d us: [pid:110451 tid: 7c422ea006c0] Host active wait for Signal = (0x7c43ccbff300) for -1 ns
:0:rocdevice.cpp            :3020: 78415286347d us: [pid:110451 tid: 7c422d6006c0] Callback: Queue 0x7c4217d00000 aborting with error : HSA_STATUS_ERROR_INVALID_ISA: The instruction set architecture is invalid. code: 0x100f
Aborted (core dumped)
mcon@ikea:~/AMD$ :3:hip_device_runtime.cpp   :618 : 78431257135d us: [pid:110493 tid: 7f84fa2ba740]  hipDeviceSynchronize (  ) 
:3:hip_device_runtime.cpp   :622 : 78431257161d us: [pid:110493 tid: 7f84fa2ba740] hipDeviceSynchronize: Returned hipSuccess : 
:3:hip_fatbin.cpp           :66  : 78431260649d us: [pid:110493 tid: 7f84fa2ba740] ~FatBinaryInfo(0x579887a5aad0) will delete binary_image_ 0x579885e25360
:3:hip_fatbin.cpp           :66  : 78431261385d us: [pid:110493 tid: 7f84fa2ba740] ~FatBinaryInfo(0x5798818dfe90) will delete binary_image_ 0x5798818a1210
:3:hip_fatbin.cpp           :66  : 78431261955d us: [pid:110493 tid: 7f84fa2ba740] ~FatBinaryInfo(0x57987eed5cf0) will delete binary_image_ 0x5798806d0510
:3:hip_fatbin.cpp           :66  : 78431262484d us: [pid:110493 tid: 7f84fa2ba740] ~FatBinaryInfo(0x57987f003500) will delete binary_image_ 0x57987f58ae70
```

[requested_log.gz](https://github.com/user-attachments/files/18773591/requested_log.gz)

---

### 评论 #13 — schung-amd (2025-02-13T20:45:54Z)

Thanks! It does seem to be the same issue I'm seeing. torch is trying to launch a pre-compiled kernel for fp16 which uses 1536 VGPRs; this is correct for gfx1100 and gfx1101, but gfx1102 does not have enough registers. Unfortunately, as we don't officially support gfx1102, we don't seem to provide an appropriate kernel here.

There is a possibility that this will be addressed in the near future. We're working on support for a generic gfx11 architecture which does not assume a large amount of registers, so kernels compiled for that architecture would work for the 7600 and similar GPUs. This seems like it would address this issue, as an appropriate kernel would be provided through the generic architecture, but I'll have to reach out to internal teams involved in this for more details.

I've also tried using a ROCm 5.7 + Ubuntu 22 docker for this, but other components are not supported there (InvokeAI itself states a ROCm 6.1 requirement to begin with), so I haven't had much luck. I'll look a bit more into seeing if there's some workaround to build ROCm 5.7 on Ubuntu 24, but I suspect there might be other incompatibilities anyway.

---

### 评论 #14 — mcondarelli (2025-02-13T21:15:46Z)

Thanks.

Do you have some vague idea about which is the time frame we are speaking about ?
Please bear in mind I am fully willing to get beta (or even pre-alpha) code to test and I can provide reasonable test reports.

I don't think it's worthwhile to pursue ROCm6.7 road at this point, unless there's some hope to piggyback the old precompiled fp6 kernel (but I'm out of my depth here).

I assume it's not possible just to change some preprocessor constant and recompile the krenel, right?
I am not scared by self compilation (and I upgraded my machine to 64GB RAM so I shouldn't have problems there).

Please keep me in the loop.
Many Thanks in Advance

---

### 评论 #15 — cbayle (2025-02-13T22:47:29Z)

Got the exact same problem on a RX7600XT Board using standart debian package and precompiled pytorch with either 5.7 or 6.2 rocm
the core dump doesn't occur when I set 
precision: float32 in invokeai.yaml confirming the fp16 issue
I'm using debian Trixie and would be happy to make some tests too


---

### 评论 #16 — schung-amd (2025-02-14T15:02:33Z)

> Do you have some vague idea about which is the time frame we are speaking about ?

There is already related code in staging (e.g. https://github.com/ROCm/ROCR-Runtime/commit/0c18ff22e1b666d94d111686de1a0c8b5b98e1ac), and basic/initial functionality for this should be in the next minor version. This is being enabled on a component-by-component basis, so I don't have a clear picture of when this will work with pytorch applications. I'll update if I get more information on this.

> I don't think it's worthwhile to pursue ROCm6.7 road at this point, 

Agreed, I don't think it's likely that add support for ROCm 5.7 on Ubuntu 24 and it seems like there are other obstacles to building InvokeAI and its related components on ROCm 5.7 + Ubuntu 22.

> unless there's some hope to piggyback the old precompiled fp6 kernel (but I'm out of my depth here).

I think this might be possible but there's a lot of moving parts here and I suspect this is out of the scope of our support. I'll see if there's an easy workaround along these lines.

@cbayle Thanks for the corroborating report. You can run with AMD_LOG_LEVEL=7 to verify if you wish, but this is probably the same issue as it will affect all gfx1102 cards.

For now, fp32 + low vram mode may be required on this hardware, sorry for the inconvenience. Hopefully we can have these cards supported again in the near future.

---

### 评论 #17 — schung-amd (2025-02-14T15:30:32Z)

@cbayle @mcondarelli One thing I didn't think of; you could try bf16 instead of fp16 (i.e. set precision to bfloat16). This seems to run fine for me on a 7500 with HSA_OVERRIDE_GFX_VERSION=11.0.0 on ROCm 6.3.2 + torch 2.4.0 from repo.radeon.com, but I'm testing on a smaller model since this card only has 8gb of vram.

---

### 评论 #18 — cbayle (2025-02-14T21:13:03Z)

I got this with AMD_LOG_LEVEL=7

With ROCm 6.3:

`
...
:4:rocvirtual.cpp           :930 : 1176046695771d us: [pid:2017286 tid: 7f68718f96c0] SWq=0x7f69cf71c000, HWq=0x7f6870100000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[12288, 1, 1], workgroup=[384, 1, 1], private_seg_size=0, group_seg_size=65536, kernel_obj=0x7f6879d48f80, kernarg_address=0x7f684e603d80, completion_signal=0x7f69cd1ff580, correlation_id=0, rptr=5538, wptr=5538
:3:hip_module.cpp           :489 : 1176046695777d us: [pid:2017286 tid: 7f68718f96c0] hipExtModuleLaunchKernel: Returned hipSuccess : 
:3:hip_event.cpp            :434 : 1176046695781d us: [pid:2017286 tid: 7f68718f96c0]  hipEventSynchronize ( event:0x7f68542ae020 ) 
:3:rocvirtual.hpp           :67  : 1176046695785d us: [pid:2017286 tid: 7f68718f96c0] Host active wait for Signal = (0x7f69cd1ff580) for -1 ns
:0:rocdevice.cpp            :3020: 1176046695937d us: [pid:2017286 tid: 7f684fbff6c0] Callback: Queue 0x7f6870100000 aborting with error : HSA_STATUS_ERROR_OUT_OF_REGISTERS: Kernel has requested more VGPRs than are available on this agent code: 0x2d
./run.sh : ligne 4 : 2017286 Abandon                 (core dumped)invokeai-web --root ~/invokeai
`

bf16 makes the crash happen later with HIP memory issues

`
...
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 9.13 GiB. GPU 0 has a total capacity of 15.98 GiB of which 5.72 GiB is free. Of the allocated memory 9.50 GiB is allocated by PyTorch, and 330.58 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)`


No problem with ROCm 5.7:

---

### 评论 #19 — mcondarelli (2025-02-14T21:19:19Z)

FYI:
I went ahead and tried to recompile from sources using the `Docker` compilation container.
I found several errors in the process, mainly due to directories created as root and unwritable by the installer or attempts to create subdirectories failing because `root` privileges were needed.
If you deem it useful I can prepare a detailed bug report (here or a new one).
***Almost*** all problems are "setup problems", meaning that after fixing permissions recompilation will keep working forever (or until a new place is selected, of course).
One problem is of a different kind and I attach here logs, if you think it's worthwhile to have a look.
Of course I can open a new bug report, if you think that's the right thing to do.
I am available to do whatever test might seem useful.

[hipsparselt.errors.gz](https://github.com/user-attachments/files/18804660/hipsparselt.errors.gz)

---

### 评论 #20 — schung-amd (2025-02-14T22:03:31Z)

@cbayle Thanks! Looks like the same issue to me, although the error message is different. I'm surprised bf16 is using so much VRAM; does it also cause OOM errors on ROCm 5.7?

@mcondarelli Sure, I'll take a look and will try again to get this running in a Docker with ROCm 5.7.

---

### 评论 #21 — mcondarelli (2025-02-14T22:18:20Z)

> [@mcondarelli](https://github.com/mcondarelli) Sure, I'll take a look and will try again to get this running in a Docker with ROCm 5.7.

I was unclear.
The errors I'm speaking about happen while compiling current HEAD (RCOm6.3.2).

---

### 评论 #22 — mcondarelli (2025-02-14T22:23:29Z)

> No problem with ROCm 5.7:

Hi @cbayle, 
Can you share exactly how you managed to install InvokeAI with ROCm5.7?
I **know** it can be done because I did it, but I clobbered my working install and I've been unable to replicate.
I must be missing something really stupid, but...
Complete instructions (including precisely which version of `amdgpu` you uesed and where you downloaded it) could be useful to many people.

TiA!

---

### 评论 #23 — mcondarelli (2025-02-15T10:09:49Z)

> [@cbayle](https://github.com/cbayle) Thanks! Looks like the same issue to me, although the error message is different. I'm surprised bf16 is using so much VRAM; does it also cause OOM errors on ROCm 5.7?

I m unsure about what's happening here.
I tried using `precision: bfloat16` and it *did* succeed with a smallish (sd1.x) model, then I switched to `Juggernaut XL` (SDXL) and it failed on last pass, *after* denoising.

Switching to `precision: float32` held very similar results: free VRAM is a bit less, but final pass requests the dame (large) amount of VRAM (9.00 GiB).

Here follows the errors (full log is in attachment).
Might it be `invokeAI` is not honoring `precision` in the last pass?

I will dig deeper.

using `bfloqt16`:
```
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 9.00 GiB. GPU 0 has a total capacity of 15.98 GiB of which 6.64 GiB is free. Of the allocated memory 8.64 GiB is allocated by PyTorch, and 287.49 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
```

using `float32`:
```
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 9.00 GiB. GPU 0 has a total capacity of 15.98 GiB of which 4.47 GiB is free. Of the allocated memory 9.83 GiB is allocated by PyTorch, and 1.25 GiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
```

[full-log.tar.gz](https://github.com/user-attachments/files/18809617/full-log.tar.gz)

---

### 评论 #24 — cbayle (2025-02-15T15:54:52Z)

Hello, 

not taht easy to describe all what i did

I commited what i use to build and run on debian/trixie using uv virtualenv
here https://github.com/cbayle/InvokeAI/tree/uv

you have for 5.7
```
cd uv
./build-backend.sh
./build-frontend.sh
./run.sh
```
you can add as a parameter 6.3 to each shell  to have the same thing running with rocm6.3
should also work with 6.2

I don't use any extra amd driver/firmware other than (no amdgpu install indeed, the lib are probably retrieved by php:
ii  firmware-amd-graphics               20241210-1                        all          Binary firmware for AMD/ATI graphics chips
ii  libdrm-amdgpu1:amd64                2.4.123-1                         amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  linux-headers-6.1.0-28-amd64        6.1.119-1                         amd64        Header files for Linux 6.1.0-28-amd64
ii  linux-image-6.1.0-28-amd64          6.1.119-1                         amd64        Linux 6.1 for 64-bit PCs (signed)

you will probably have to install uv as decribed in the invokeai documentation
and at least node-corepack package to be able to build frontend

I probably did some more, don't hesitate if you encounter problems


I think that probable invokeai is doing something wrong in the last part that requires to much memory, but could't find any parameter to workaround yet.

At least  precision: bfloat16 seems to fix the first part of image generation problem, like float32




> > No problem with ROCm 5.7:
> 
> Hi [@cbayle](https://github.com/cbayle), Can you share exactly how you managed to install InvokeAI with ROCm5.7? I **know** it can be done because I did it, but I clobbered my working install and I've been unable to replicate. I must be missing something really stupid, but... Complete instructions (including precisely which version of `amdgpu` you uesed and where you downloaded it) could be useful to many people.
> 
> TiA!



---

### 评论 #25 — mcondarelli (2025-02-18T09:06:19Z)

@cbayle : FYI :

Problem with huge VMEM spike (9.0GiB, in my case) happens because `Latents to Image` simply can't understand `bfloat16` so it falls back to `float32`.

Workaround is to enable `force_tiled_decode: true`, but that doesn't work either unless you force default `tile_size` in code
see: https://github.com/invoke-ai/InvokeAI/issues/7650
This has solved for me.

Note: you can make that change in your specific `venv`, no need to meddle with upstream.

---

### 评论 #26 — schung-amd (2025-02-18T16:24:14Z)

@mcondarelli Glad you got it working! I guess the VAE decoder for that model does not support bf16 even though the model itself does. Are you still interested in trying to get ROCm 5.7 working? If not, we can probably rename this issue and close it off for now. While I'm speculating that we can re-enable fp16 support for the 7600 indirectly through the generic architecture, I don't have a clear idea of when this will be.

---

### 评论 #27 — mcondarelli (2025-02-18T18:11:34Z)

We can surely close this.
I won't try anymore to install ROCm6.7.
Many Thanks for your help.

A side question while I have your attention:
I am having problems with another related piece of code [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes/) dies with error "`undefined symbol: _Z36__device_stub__kOptimizer32bit1StateI12hip_bfloat16Li2EEvPT_S2_PfS3_ffffffiffbi`".
If I read code correctly that symbol is automatically generated inside ROCm code (in `.../lib/CodeGen/CodeGenModule.cpp:getMangledNameImpl()`) and is nowhere present in `bitsandbytes` code.
I opened a ticket there (https://github.com/bitsandbytes-foundation/bitsandbytes/issues/1519); should I open one also here?
Code there is quite convoluted and I'm unsure.

Many thanks in advance.

---

### 评论 #28 — schung-amd (2025-02-18T20:08:37Z)

Yes, please open a ticket in our fork (https://github.com/ROCm/bitsandbytes) with details and a link to the upstream ticket and we'll take a look, thanks!

Feel free to comment here as well if you need any further guidance related to this issue and we can reopen if necessary.

---
