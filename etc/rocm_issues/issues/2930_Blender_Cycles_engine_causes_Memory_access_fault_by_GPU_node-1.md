#  Blender Cycles engine causes "Memory access fault by GPU node-1"

> **Issue #2930**
> **状态**: closed
> **创建时间**: 2024-02-26T21:42:41Z
> **更新时间**: 2025-03-05T12:12:37Z
> **关闭时间**: 2024-10-21T14:33:20Z
> **作者**: widarr
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon Pro W7900
> **URL**: https://github.com/ROCm/ROCm/issues/2930

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon Pro W7900** (颜色: #ededed)

## 描述

### Problem Description

Error:
Blender crashes with `Memory access fault by GPU node-1 (Agent handle: 0x7c1aea898400) on address 0x5fd000. Reason: Page not present or supervisor privilege.`




### Operating System

6.7.4-2-MANJARO Linux

### CPU

AMD Ryzen 9 5950X

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Reproducing error: Just opening Blender (tested 4.0-4.1), switching Render Engine to Cycles (Feature Set: Supported, Device: GPU compute) Activate Viewport shading (and maybe rotate the camera around the default cube a few times) causes the crash. Also  trying to render anything instantly crashes Blender.

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
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131808628(0x7db3d74) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131808628(0x7db3d74) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131808628(0x7db3d74) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-9e8b159eef31d025               
  Marketing Name:          AMD Radeon Pro W7900               
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
  Chip ID:                 29768(0x7448)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1760                               
  BDFID:                   3584                               
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 528                                
  SDMA engine uCode::      19                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    47169536(0x2cfc000) KB             
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
*** Done ***

### Additional Information

OS:
NAME="Manjaro Linux"

CPU: 
model name	: AMD Ryzen 9 5950X 16-Core Processor

GPU:
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
  Name:                    gfx1100                            
  Marketing Name:          AMD Radeon Pro W7900               
      Name:                    amdgcn-amd-amdhsa--gfx1100

Mobo: ASUSTeK model: ROG STRIX X570-E GAMING WIFI II

Graphics:
  Device-1: AMD Navi 31 [Radeon Pro W7900] driver: amdgpu v: kernel
  Display: x11 server: X.Org v: 21.1.11 with: Xwayland v: 23.2.4 driver: X:
    loaded: amdgpu unloaded: modesetting,radeon dri: radeonsi gpu: amdgpu
    resolution: 3840x2160~144Hz
  API: EGL v: 1.5 drivers: radeonsi,swrast platforms: x11,surfaceless,device
  API: OpenGL v: 4.6 compat-v: 4.5 vendor: amd mesa v: 23.3.5-manjaro1.1
    renderer: AMD Radeon Pro W7900 (radeonsi navi31 LLVM 16.0.6 DRM 3.57
    6.7.4-2-MANJARO)
  API: Vulkan v: 1.3.276 drivers: amd surfaces: xcb,xlib

RAM (DDR4)
Memory: total: 128 GiB

PSU: 1000W

Case: EATX with 9 Fans


---

## 评论 (37 条)

### 评论 #1 — twoexem (2024-03-05T13:39:56Z)

I have this issue too on my AMD RX6600XT.

---

### 评论 #2 — Jmvars (2024-03-07T06:09:23Z)

I have this issue on my RX 7900 XT. Viewport shading works fine, Rendered View or trying to render anything causes instant crash with this error message.

---

### 评论 #3 — Kagukara (2024-03-07T17:35:17Z)

Getting the same on 7900 XTX, ran `gdb blender-4.2` and it gave me:
```
Thread 130 "blender-4.2" received signal SIGABRT, Aborted.
__pthread_kill_implementation (threadid=<optimized out>, signo=signo@entry=6, no_tid=no_tid@entry=0) at pthread_kill.c:44
44	     return INTERNAL_SYSCALL_ERROR_P (ret) ? INTERNAL_SYSCALL_ERRNO (ret) : 0;
```
backtrace:
```
#0  __pthread_kill_implementation (threadid=<optimized out>, signo=signo@entry=6, no_tid=no_tid@entry=0) at pthread_kill.c:44
#1  0x00007fffe98ab393 in __pthread_kill_internal (signo=6, threadid=<optimized out>) at pthread_kill.c:78
#2  0x00007fffe985a6c8 in __GI_raise (sig=sig@entry=6) at ../sysdeps/posix/raise.c:26
#3  0x00007fffe98424b8 in __GI_abort () at abort.c:79
#4  0x00007fff1f023514 in rocr::core::Runtime::VMFaultHandler (val=<optimized out>, arg=<optimized out>)
    at /usr/src/debug/hsa-rocr/ROCR-Runtime-rocm-6.0.0/src/core/runtime/runtime.cpp:1429
#5  0x00007fff1f07f642 in rocr::core::Runtime::AsyncEventsLoop () at /usr/include/c++/13.2.1/bits/stl_vector.h:1125
#6  0x00007fff1f027a6c in rocr::os::ThreadTrampoline (arg=<optimized out>) at /usr/src/debug/hsa-rocr/ROCR-Runtime-rocm-6.0.0/src/core/util/lnx/os_linux.cpp:80
#7  0x00007fffe98a955a in start_thread (arg=<optimized out>) at pthread_create.c:447
#8  0x00007fffe9926a3c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78
```

---

### 评论 #4 — fililip (2024-03-08T00:21:41Z)

Does running Blender with `HSA_ENABLE_SDMA=0` work?

---

### 评论 #5 — Kagukara (2024-03-08T00:24:36Z)

Running `HSA_ENABLE_SDMA=0 blender-4.2` gives me the same result.

```
Memory access fault by GPU node-1 (Agent handle: 0x7c32f76c4e00) on address 0x7c315dde2000. Reason: Page not present or supervisor privilege.
Aborted (core dumped)
```

---

### 评论 #6 — twoexem (2024-03-08T22:32:24Z)

Yeah, same here:
`Memory access fault by GPU node-1 (Agent handle: 0x76eb18475600) on address 0x984000. Reason: Page not present or supervisor privilege.
`

---

### 评论 #7 — twoexem (2024-03-08T22:42:36Z)

My dmesg output shows the following:

```
[18786.415357] amdgpu 0000:2d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32799, for process blender pid 36725 thread blender:cs0 pid 36744)
[18786.415359] amdgpu 0000:2d:00.0: amdgpu:   in page starting at address 0x0000000000989000 from client 0x1b (UTCL2)
[18786.415361] amdgpu 0000:2d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[18786.415362] amdgpu 0000:2d:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[18786.415364] amdgpu 0000:2d:00.0: amdgpu:      MORE_FAULTS: 0x0
[18786.415365] amdgpu 0000:2d:00.0: amdgpu:      WALKER_ERROR: 0x0
[18786.415366] amdgpu 0000:2d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[18786.415367] amdgpu 0000:2d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[18786.415369] amdgpu 0000:2d:00.0: amdgpu:      RW: 0x0
```

---

### 评论 #8 — TNT3530 (2024-03-28T12:38:24Z)

Can confirm this also happens on Ubuntu 22.04 with kernels 6.5.0-14, 6.5.0-28, 6.8.1-060801, 6.7.10-060710, and 6.6.22-060622 when using Instinct MI100s and ROCm 6.0

---

### 评论 #9 — GZGavinZhao (2024-03-30T17:39:29Z)

Hi, I think this may be a compiler bug, further investigation still needed: https://projects.blender.org/blender/blender/issues/112084#issuecomment-1157532

---

### 评论 #10 — GZGavinZhao (2024-04-03T19:33:19Z)

If you're getting this only on ROCm 6, `git bisect` shows it's likely a compiler bug. Filed ROCm/llvm-project#58.

---

### 评论 #11 — alexxu-amd (2024-04-18T15:49:49Z)

Hi all, can you check if this issue can still be reproduced with the latest ROCm 6.1?

---

### 评论 #12 — GZGavinZhao (2024-04-19T16:03:08Z)

You can still reproduce the crash with a slight caveat. The reproducing step with Docker is as follows:

1. Pull the `rocm/rocm-terminal:6.1` docker image.
2. Enter the docker image: `podman run -it --device=/dev/kfd --device=/dev/dri --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined rocm/rocm-terminal:6.1`. I personally use `podman`, if you use `docker` replace `podman` with `sudo docker`.
3. Create a `work` directory for convenience. `mkdir work && cd work`
4. Install runtime dependencies for Blender: `sudo apt-get update && sudo apt-get install build-essential git git-lfs subversion cmake libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libegl-dev libwayland-dev wayland-protocols libxkbcommon-dev libdbus-1-dev linux-libc-dev unzip libsm6 libxext6 -y`. (yes, not all of these dependencies are needed, I'm just being safe here)
5. Fetch the Blender 4.1 binary: `curl -O https://download.blender.org/release/Blender4.1/blender-4.1.0-linux-x64.tar.xz`
6. Extract Blender: `tar xf blender-4.1.0-linux-x64.tar.xz`. You should now have a `blender-4.1.0-linux-x64` directory in you current directory.
7. Fetch the BMW27 blender project for testing: `curl -O https://download.blender.org/demo/test/BMW27.blend.zip`
8. `unzip BMW27.blend.zip`. You should now have a `BMW27.blend` file in your current directory.
9. Render the file. `blender-4.1.0-linux-x64/blender -b BMW27.blend -f 0 -- --cycles-device HIP`. Note that by default Blender will use your GPU with id 0 to render; if you want to use another GPU, run `export HIP_VISIBLE_DEVICES=<gpu-id-you-want-to-use>` before rendering with Blender. You can find the available GPU ids by running `rocm-smi` (under the `Device` column).
10. You should now almost immediately get `Memory access fault by GPU node-1 (Agent handle: 0x7f5f2af98000) on address 0x7f5afa7cb000. Reason: Page not present or supervisor privilege.`

The caveat is that this issue is probably on the compiler side, not ROCm's runtime. Blender ships pre-compiled GPU fatbins that is compiled with some ROCm version that I don't know (I suspect the fatbins that come with 4.1 are compiled with ROCm 6.0, but even the Blender folks aren't sure). To verify that it's probably a compiler issue, continue:

11. Clone Blender. To save space and ensure consistency, we're just going to clone the 4.1.0 version: `git clone https://projects.blender.org/blender/blender.git --depth 1 --branch v4.1.0`
12. Enter the Blender folder and compile the fatbins with ROCm 6.1: `pushd blender && hipcc --offload-arch=$arch --genco intern/cycles/kernel/device/hip/kernel.cpp -D CCL_NAMESPACE_BEGIN= -D CCL_NAMESPACE_END= -D HIPCC -I intern/cycles/kernel/.. -I intern/cycles/kernel/device/hip -ffast-math -o kernel_$arch.fatbin && popd`. Replace `$arch` with the architecture of the GPU you want to run on, e.g. `gfx900`. If you want to compile against multiple architectures, you must repeat step 12 and 13 for each architecture.
13. Put the `blender/kernel_$arch.fatbin` file at `blender-4.1.0-linux-x64/4.1/scripts/addons/cycles/lib/kernel_$arch.fatbin`. Once again, replace `$arch` with your desired GPU architecture.
14. Now run step 9 again. Blender shouldn't crash anymore.

If you're unable to reproduce the crash with the BMW27 example, try any one of the demo files under the "Cycles" section on the [Blender demos page](https://www.blender.org/download/demo-files/#cycles). One common test file we used was the Classroom example.

---

### 评论 #13 — alexxu-amd (2024-04-22T14:07:03Z)

@GZGavinZhao Thanks for the detailed description. We will look into it

---

### 评论 #14 — jeancf (2024-05-14T13:26:57Z)

I am affected by this bug also with 6.8.8-2-MANJARO + ROCm 6.0.2 + Blender 4.0 + Radeon RX 6800XT

```
inxi -SCG
System:
  Host: desktop1 Kernel: 6.8.8-2-MANJARO arch: x86_64 bits: 64
  Desktop: KDE Plasma v: 5.27.11 Distro: Manjaro Linux
CPU:
  Info: quad core model: Intel Core i7-6700K bits: 64 type: MT MCP cache:
    L2: 1024 KiB
  Speed (MHz): avg: 800 min/max: 800/4200 cores: 1: 800 2: 800 3: 800 4: 800
    5: 800 6: 800 7: 800 8: 800
Graphics:
  Device-1: AMD Navi 21 [Radeon RX 6800/6800 XT / 6900 XT] driver: amdgpu
    v: kernel
  Display: x11 server: X.Org v: 21.1.12 driver: X: loaded: amdgpu
    unloaded: modesetting,radeon dri: radeonsi gpu: amdgpu resolution:
    1: 2560x1440 2: 1280x1024
  API: EGL v: 1.5 drivers: kms_swrast,radeonsi,swrast
    platforms: gbm,x11,surfaceless,device
  API: OpenGL v: 4.6 compat-v: 4.5 vendor: amd mesa v: 24.0.2-manjaro1.1.1
    renderer: AMD Radeon RX 6800 XT (radeonsi navi21 LLVM 16.0.6 DRM 3.57
    6.8.8-2-MANJARO)
  API: Vulkan v: 1.3.279 drivers: radv,llvmpipe surfaces: xcb,xlib
```

---

### 评论 #15 — Jmvars (2024-05-23T23:26:12Z)

This seems to be fixed for me on my 7900 XT, Blender 4.1.1, ROCm 6.0.2, Arch Linux-zen 6.9.1

Important to note I had to reinstall the entire OS due to drive dying.

---

### 评论 #16 — jeancf (2024-05-24T09:54:21Z)

I confirm that the scenes that I have tested no longer crash for me with this combination of versions: Blender 4.1, ROCm 6.0.2, Linux-MANJARO 6.9.0

---

### 评论 #17 — ppanchad-amd (2024-06-20T14:28:29Z)

@widarr Can you please re-test with the following combination to see if you still see the issue: Blender 4.1.1, ROCm 6.1.2, Linux-MANJARO 6.9.0. Thanks!

---

### 评论 #18 — ppanchad-amd (2024-07-17T19:15:45Z)

Closing as there is no response from reporter and issue seems to be fixed with Blender 4.1.1 + ROCm 6.0.2. Thanks!

---

### 评论 #19 — NerosTie (2024-09-08T11:43:32Z)

Blender 4.2.1 + ROCm 6.0.2 (tested with 6.2.0 too) + 6600 XT + Mesa 24.2.2 and the issue is still here...

```
Memory access fault by GPU node-1 (Agent handle: 0x769ca033ac00) on address 0x76b5cc934000. Reason: Page not present or supervisor privilege.
fish: Job 1, 'blender' terminated by signal SIGABRT (Abandon)
```

---

### 评论 #20 — ppanchad-amd (2024-09-08T23:18:13Z)

@NerosTie Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #21 — schung-amd (2024-09-09T17:36:40Z)

Hi @NerosTie, what distro are you seeing this on? Did some testing on Ubuntu 22.04 with Blender 4.2.1 LTS + ROCm 6.2 + mesa 24.2.2 from `kisak-mesa` PPA (AMD mesa drivers from ROCm 6.2 are 24.2.0) + 7900XTX and was unable to reproduce the issue with the steps in the original post as well as rendering the BMW27 and classroom examples as suggested by @GZGavinZhao. The steps in the original post also did not result in a crash when using the mesa version that ships with Ubuntu 22.04, although I didn't try rendering BMW27 or classroom with these drivers.

---

### 评论 #22 — NerosTie (2024-09-09T17:44:59Z)

@schung-amd Arch
I test with Classroom and [White Lands](https://cloud.blender.org/p/gallery/629f23f908e12d4ff15241d3).

You say you have an 7900XTX and I have an 6600XT, maybe that's why?

A year ago it was working with previous versions of Blender.

---

### 评论 #23 — schung-amd (2024-09-09T18:48:56Z)

Thanks for the quick response! This was reported fixed on a 6800XT earlier in this thread, but you can try rendering with `HSA_OVERRIDE_GFX_VERSION=11.0.0` (e.g. `HSA_OVERRIDE_GFX_VERSION=11.0.0 blender-4.2.1-linux-x64/blender -b classroom.blend -f 0 -- --cycles-device HIP`). If that doesn't help I'll try to find a 6600 to repro on.

---

### 评论 #24 — NerosTie (2024-09-09T18:59:17Z)

```HSA_OVERRIDE_GFX_VERSION=11.0.0 blender```

Well, it freezes the GPU when rendering and I had to reboot, so, not a good thing.

---

### 评论 #25 — schung-amd (2024-09-09T20:07:09Z)

I don't have a 6600XT on hand at the moment, but I was able to render `classroom` on an RX 6400 (which has a similar architecture) without issue. I can also render the scene without crashing when passing `HSA_OVERRIDE_GFX_VERSION=10.3.0`, which is similar to the actual architecture of the RX 6400 (gfx1034). 

Interestingly, I was able to reproduce a segfault trying to render from the command line with `HSA_OVERRIDE_GFX_VERSION=11.0.0` which emits a similar error to what was originally reported: 
```
Memory access fault by GPU node-1 (Agent handle: 0x73b8a8453e00) on address 0x73b967802000. Reason: Page not present or supervisor privilege.
Aborted (core dumped)
```
I'll have to see if I can reproduce the issue on Arch. We don't officially support Arch (see https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html) so I can't guarantee a solution, but I may be able to at least find a workaround for you. Out of curiosity, have you tried steps 11 through 14 posted by @GZGavinZhao? 

---

### 评论 #26 — schung-amd (2024-09-09T20:26:16Z)

Also, according to https://projects.blender.org/blender/blender/issues/100353 this was solved for several users with RDNA2 cards on Arch with a kernel/firmware update, so you can try that as well. 

---

### 评论 #27 — schung-amd (2024-09-25T20:57:37Z)

I can reproduce this on Arch with an RX6400, but only on a few tests; Classroom and Lone Monk crash early, while BMW27 and Italian Flat render fine, among others. Also, there are no issues when using a 7900XTX. The workaround posted by @GZGavinZhao didn't work on my end, and this might be a completely separate issue, but I recommend trying it anyway just in case it solves your problem. 

It's not clear to me why there are only issues on less powerful hardware and only for certain tests; normally this would point to a load issue, but it's hard to say whether the problematic tests place more of a load on the GPU than the others. I'm not a Blender user and can't tell if there's an obvious difference between these tests; let me know if you can see any differences in the settings of these tests that may be related to the cause of this issue.

---

### 评论 #28 — schung-amd (2024-10-04T15:29:10Z)

@NerosTie Still not sure of the underlying cause, but this is fixed on my end on the 6400 with Blender 4.4 (built from source with WITH_CYCLES_HIP_BINARIES enabled) and ROCm 6.2.1 (provided via opencl-amd and opencl-amd-dev in AUR). With these versions I can render both Classroom and Lone Monk without running into that memory access fault. Give these versions a try and let me know if you still experience the issue.

---

### 评论 #29 — schung-amd (2024-10-08T14:48:37Z)

Closing as I can't reproduce on latest software versions. If you're still experiencing this issue with latest Blender and ROCm, feel free to comment and we can reopen this.

---

### 评论 #30 — NerosTie (2024-10-08T15:16:28Z)

Tested with Blender 4.4 and ROCm 6.0.2 (I'm waiting for an update in Arch for a long time now...):
- Classroom: it works!
- Lone Monk: it works!
- [White Lands](https://cloud.blender.org/p/gallery/629f23f908e12d4ff15241d3): crash with the same error

So yes, it's going better, but there is still an issue somewhere.

---

### 评论 #31 — schung-amd (2024-10-08T15:32:03Z)

Can you try ROCm 6.2.1 (provided via opencl-amd and opencl-amd-dev in AUR)? I'll see if I can reproduce on my end with White Lands. Ultimately however these issues aren't on our end, as we don't officially support Arch and don't control what is provided there. In addition since updated Blender has resolved some of your issues I assume this is on Blender's end as well.

It would probably also be helpful to find out what is different about the files that are failing to render. If you can find a specific feature or workload that is causing your failures we can look into why these failures might be occurring.

---

### 评论 #32 — schung-amd (2024-10-11T16:10:03Z)

I can reproduce the crash with Blender 4.4 + ROCm 6.2.1 (via AUR) on Arch for White Lands with a 6400 (as a stand-in for the 6600XT as they are similarly unsupported). However, on Ubuntu 22.04 + Blender 4.4 + ROCm 6.2.2 (latest release as of this comment) it renders fine on the 6400. 

As stated, we don't officially support Arch, so everything is working as intended on our end. Whatever is causing your issues is either on Blender's end, on the Arch package's end, or there is something specifically wrong with your configuration. I am willing to continue investigating this issue to try and provide as much support as we can, but I suggest you reach out to Blender and the Arch package maintainer for ROCm regarding this as we do not control the software you are using.

---

### 评论 #33 — schung-amd (2024-10-11T20:40:22Z)

@NerosTie After some tweaking I found that I was able to render White Lands when the water's volumetric shading was disabled, so I suspected that this was raytracing-related. With Blender 4.4 built from source with WITH_CYCLES_HIP_BINARIES and WITH_CYCLES_DEVICE_HIPRT both enabled, I'm able to render the scene without a crash on Arch + ROCm 6.2.1 (via AUR) + 6400. Try building Blender with both the Cycles binaries and Cycles HIPRT enabled and see if that fixes the problem on your end.

---

### 评论 #34 — schung-amd (2024-10-21T14:33:20Z)

Closing this again, as can't reproduce the issue with the configuration above. Feel free to comment if you still run into issues with Cycles HIPRT enabled or if you run into issues rendering other files and we can reopen this. Ultimately these issues don't seem to be on our end (as everything has been working fine on Ubuntu), but I'll try to provide as much support as I can.

---

### 评论 #35 — leucome (2025-01-20T02:55:14Z)

On Manjaro I do get the error "Memory access fault by GPU node-1 (Agent handle: 0x7f2569666900) on address 0x7f23daa1e000. Reason: Page not present or supervisor privilege"

It is only happening when HIPRT and motion blur  is turned on.  I dont know if this clue can help find what is the difference on Arch based distro.    

This seem to fit with this statement. "Classroom and Lone Monk crash early, while BMW27 and Italian Flat render fine".  I am pretty sure BMW27 and Italian Flat  do not use motion blur.  

---

### 评论 #36 — schung-amd (2025-01-20T14:39:56Z)

Hi @leucome, can you open a new issue for this with more details about your configuration? You can link this in but it's not clear if your issue is a duplicate of this one, as that error message is not very specific.

---

### 评论 #37 — NerosTie (2025-03-05T12:12:36Z)

Rocm has been updated to 6.3.2 in Arch and now, finally, it doesn't crash anymore with the scene "White Lands" with my RX 6600 XT, the issue is fixed!

---
