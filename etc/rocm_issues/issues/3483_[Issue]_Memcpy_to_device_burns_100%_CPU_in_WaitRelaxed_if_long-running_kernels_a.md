# [Issue]: Memcpy to device burns 100% CPU in WaitRelaxed if long-running kernels are present

> **Issue #3483**
> **状态**: closed
> **创建时间**: 2024-08-01T21:59:34Z
> **更新时间**: 2024-08-12T16:13:12Z
> **关闭时间**: 2024-08-09T21:56:29Z
> **作者**: FeepingCreature
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3483

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

**Edit** for future readers who find this on Google:

# This is intentional behavior!

CUDA does the same thing. Google `hipSetDeviceFlags(hipDeviceScheduleBlockingSync)` for how to turn it off.

## Previous text:

### Problem Description

I've run into this with ComfyUI, but there's been variants of this issue a few times already (just search the issues for `WaitRelaxed`), but there's usually been some other issue that was fixed eventually, so I want to go ahead and file a bug for *just* `WaitRelaxed` burning 100% CPU.

As far as I can tell, this goes back to `DmaBlitManager::hsaCopyStaged` calling `releaseMemoryFence`, which, via `CpuWaitForSignal`, goes into a `HSA_WAIT_STATE_ACTIVE` `WaitRelaxed` call, which then spends 80% of CPU load on the `now()` call in the loop. To add insult to injury, `g_enable_mwaitx` has somehow become `false` even though my CPU definitely supports it.

So it just hot-busyloops for many milliseconds waiting for the kernel to finish.

### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen 7950X3D

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

clr

### Steps to Reproduce

- Launch ComfyUI
- Set latent size to 2048x2048 to ensure some nice long-running kernels
- Queue Prompt
- Observe high CPU load.
- Observe `rdtsc` taking >80% in profiler.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.13
Runtime Ext Version:     1.4
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
  Name:                    AMD Ryzen 9 7950X3D 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X3D 16-Core Processor
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
  Max Clock Freq. (MHz):   5759                               
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
      Size:                    32568860(0x1f0f61c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32568860(0x1f0f61c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32568860(0x1f0f61c) KB             
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
  Uuid:                    GPU-7b8755ac387dcb5c               
  Marketing Name:          Radeon RX 7900 XTX                 
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2526                               
  BDFID:                   768                                
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
  Packet Processor uCode:: 202                                
  SDMA engine uCode::      20                                 
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
*** Done ***          

### Additional Information

_No response_

---

## 评论 (17 条)

### 评论 #1 — ppanchad-amd (2024-08-02T14:31:18Z)

@FeepingCreature Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2024-08-08T18:10:17Z)

Hi @FeepingCreature, are you able to reproduce this on ROCm 6.2? Also, to clarify, does your kernel proceed while the CPU is spinning or are you getting a hang? We're currently investigating some other issues with DMA and this might be related. Thanks!

---

### 评论 #3 — FeepingCreature (2024-08-08T22:46:43Z)

It's proceeding fine, the Python process is just additionally sitting on high CPU. Yes this happens  on 6.2, the dropdown just didn't have that as an option when I filed the bug.

edit: Re-confirmed it happens with `libhsa-runtime64.so.1.14.60200` loaded in pytorch. (Note pytorch ships a vendor version of that lib for some reason ... replaced it to be safe, but I see CPU load with either.)

---

### 评论 #4 — schung-amd (2024-08-09T14:14:54Z)

Thanks for the quick response! A few follow-up questions: Is this a new issue you're running into, or have you experienced this CPU spin with multiple configurations (i.e. on other distros, older versions, or on other hardware)? Is the CPU usage constantly high throughout? Does this issue appear only on large workloads like the one you've provided, or are you seeing the CPU spin on smaller tasks as well?

---

### 评论 #5 — FeepingCreature (2024-08-09T14:49:58Z)

I've always seen Python at high CPU load with ComfyUI, but I never looked at it in a profiler before so I can't confirm it's the same function. Also to be safe I just reproed the issue on a clean ComfyUI install with AnythingXL. Also, the issue seems constant no matter how big I make the tasks, ie. if I run 256x256 for 200 steps, rdtsc still dominates the profiler, though a lot more is burned in pure Python: in that one, rdtsc sits at 18%. Which is still a lot! I suspect the 80% are burnt by Python before Rocm gets a chance to burn it - since it's a busyloop waiting for a GPU event, it doesn't matter too much _where_ the CPU goes. Only thing I could do to make it cleaner is boot into a Liveimage so I can have a clean rocm install, does that seem worthwhile? Also, do you want me to just upload a perf capture somewhere?

---

### 评论 #6 — schung-amd (2024-08-09T16:57:26Z)

I think a clean install could be helpful just to cover all the bases, but I don't think it's likely to fix your problem, so that's up to your discretion. A configuration issue is possible since high CPU usage doesn't seem to be commonly reported for this workflow, but that could manifest from sources outside of the ROCm install. What settings are you using in ComfyUI, so I can try to reproduce your exact issue?

---

### 评论 #7 — FeepingCreature (2024-08-09T17:17:15Z)

It happens with the default workflow. ("Load Default" on the right.) No commandline args, just `python3 main.py`. I've had it happen with AutismMix (PonyV6 variant) and AnythingXL, but I really doubt it depends on which SDXL checkpoint you use. I'm trying to set up a clean 22.04 boot and rocm/pytorch install in a chroot off the 22.04.2 livecd on my end currently, will report back how that behaves. It's taking a while to download. :)

I kind of suspect it happens a lot, but isn't usually _reported_. After all, who would be surprised that a process is busy when it's performing work? 

---

### 评论 #8 — FeepingCreature (2024-08-09T18:04:48Z)

Yep, reproduced on a livecd chroot. I haven't done these *exact* steps, but that suggests this should work (mostly it's straight from my `history`):

1. Install Ubuntu 22.04.4
2. `apt update`
3. `apt full-upgrade`
4. `apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"`
5. `usermod -a -G render,video $LOGNAME`
6. `wget https://repo.radeon.com/amdgpu-install/6.2/ubuntu/jammy/amdgpu-install_6.2.60200-1_all.deb`
7. `apt install ./amdgpu-install_6.2.60200-1_all.deb`
8. `apt update`
9. `apt install amdgpu-dkms rocm`
10. `modprobe amdgpu`
11. `apt install linux-tools-common linux-tools-5.15.0-94-generic # for perf`
12. `apt install python3-pip`
13. `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1`
14. `git clone https://github.com/comfyanonymous/ComfyUI.git`
15. `cd ComfyUI`
16. `pip3 install -r requirements.txt`
17. download a model such as SDXL or https://civitai.com/models/9409/or-anything-xl to `models/checkpoints`
18. `python3 main.py --listen`
19. confirm that running with 1024x1024 evinces 100% CPU load in `htop` while the KSampler in the default workflow is running, and that `libhsa-runtime64.so` tops the chart in `perf top`
20. `apt install hsa-rocr-dbgsym`
21. give torch the system libhsa runtime so we can profile it
22. `rm $HOME/.local/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so`
23. `ln -s /opt/rocm-6.2.0/lib/libhsa-runtime64.so.1.14.60200 $HOME/.local/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so`
24. observe that `rocr::core::InterruptSignal::WaitRelaxed` leads the chart (85% at sampler 1024x1024) while ComfyUI runs.

---

### 评论 #9 — schung-amd (2024-08-09T20:09:18Z)

Thanks for the detailed reproduction instructions! My setup is on Ubuntu 22.04 with ROCm 6.2, with a 7900XTX and 5995WX. I set up ComfyUI with Anything XL and ran it with latent size 1024x1024. Instead of using the nightly torch builds, however, I used specific versions of torch, torchvision, and triton confirmed for ROCm 6.2 support:
```
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/torch-2.3.0%2Brocm6.2.0-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/torchvision-0.18.0%2Brocm6.2.0-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/pytorch_triton_rocm-2.3.0%2Brocm6.2.0.1540b42334-cp310-cp310-linux_x86_64.whl
pip3 uninstall torch torchvision pytorch-triton-rocm numpy
pip3 install torch-2.3.0+rocm6.2.0-cp310-cp310-linux_x86_64.whl torchvision-0.18.0+rocm6.2.0-cp310-cp310-linux_x86_64.whl pytorch_triton_rocm-2.3.0+rocm6.2.0.1540b42334-cp310-cp310-linux_x86_64.whl numpy==1.26.4
```
With this setup, single CPU threads occasionally spin up to 100%, but only one thread at a time. After looking into the source code in our stack where you've pointed (i.e. the `WaitRelaxed` call), I believe this is intended behavior, as the thread is spinlocking waiting for a memory transfer to complete. If you're observing more than one thread spinning, try those versions of torch, torchvision, and triton.

---

### 评论 #10 — FeepingCreature (2024-08-09T20:24:00Z)

Nope, that's what I'm seeing as well. It does seem like intended behavior, in the sense that the code is doing what it says it does. It just seems a bit wild. Like, surely waiting for the GPU to change state should be able to proceed in a better fashion than "spin the CPU until the address changes value". Don't you guys have interrupts? ;-)

In hindsight saying "100% CPU" may have been misleading; if that's the case I apologize. Linux (top and co) uses "100%" to refer to "one core".

---

### 评论 #11 — FeepingCreature (2024-08-09T20:45:39Z)

It sort of looks like WaitRelaxed is supposed to be switching to an event-based sleep. I'm not sure why it doesn't happen.

To clarify, I've attached a breakpoint to `hsaKmtWaitOnEvent_Ext` and it's literally never called.

---

### 评论 #12 — FeepingCreature (2024-08-09T21:13:15Z)

The matter is starting to clear up. Apparently `hipSetDeviceFlags` lets you deliberately opt in to this behavior. Trying to figure out who sets this and why.

edit: Apparently it's on by default...?

---

### 评论 #13 — FeepingCreature (2024-08-09T21:20:41Z)

Resolution! Apparently this is behavior that's been copied from CUDA, where it also occurs. https://github.com/pytorch/pytorch/issues/28224 So I just have to figure out how to `hipSetDeviceFlags(hipDeviceScheduleBlockingSync)` from Python somehow.

For skimming future readers:

# This is intentional behavior.


---

### 评论 #14 — FeepingCreature (2024-08-09T21:29:35Z)

```
import ctypes

# hipSetDeviceFlags(hipDeviceScheduleBlockingSync)
assert ctypes.CDLL('libamdhip64.so').hipSetDeviceFlags(4) == 0
```

I dropped this code (thanks Claude 3.5 Sonnet!) at the top of main.py, and CPU load drops to 10% with 1024x1024. Problem solved. Sorry for wasting your time.

edit: Though at least the docs are wrong! :) https://github.com/ROCm/HIP/blob/amd-staging/include/hip/hip_runtime_api.h#L2083 says "On ROCm platform, this is a synonym for hipDeviceScheduleYield", and no it isn't. To be fair, I don't think it sees much use. I can only find two occurrences of `hipSetDeviceFlags(hipDeviceScheduleBlockingSync)` on Github, and one is in AMD tests. :)

edit: FWIW this has measurable effect on my CPU's power use, to the tune of +-20W when using ROCM. IMO blocking mode should really be default, but I understand it'd be hard to change now.

---

### 评论 #15 — schung-amd (2024-08-12T14:25:21Z)

Thanks for the deep dive! I'm glad you found a workaround for your system, and for future readers who also find this to be an issue. I'll make a note of this internally so we can take a closer look if/when it becomes higher priority.

As for the documentation issue, do you mean that you've tried setting hipDeviceScheduleYield and it doesn't have the same function, or hipDeviceScheduleYield is being set internally somewhere when hipDeviceScheduleBlockingSync should be set, or something else?

---

### 评论 #16 — FeepingCreature (2024-08-12T16:05:51Z)

No, the docs currently say that BlockingSync does not have any effect other than Yield. BlockingSync does a blocking sync, because it sets `device->setActiveWait(false)`. `Yield` and `Spin` are the ones that have the same effect. See [hip_device_runtime.cpp](https://github.com/ROCm/clr/blob/develop/hipamd/src/hip_device_runtime.cpp#L707-L715), and if you check the ROCR runtime you'll see [hsa_wait_state_t doesn't even have the option to differentiate](https://github.com/ROCm/ROCR-Runtime/blob/master/src/core/runtime/interrupt_signal.cpp#L146), and `g_enable_mwaitx` can only be disabled by a [lack of CPU support or an env var](https://github.com/ROCm/ROCR-Runtime/blob/master/src/core/util/flag.h#L229). Unless Spin (vs Yield) turns `g_enable_mwaitx` off through some mechanism I don't see right now.

---

### 评论 #17 — schung-amd (2024-08-12T16:11:44Z)

I see, I'll bring that up to the internal team, thanks!

---
