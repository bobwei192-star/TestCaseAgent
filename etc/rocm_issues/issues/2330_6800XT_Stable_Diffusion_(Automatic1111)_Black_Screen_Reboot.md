# 6800XT Stable Diffusion (Automatic1111) Black Screen Reboot

> **Issue #2330**
> **状态**: closed
> **创建时间**: 2023-07-22T17:54:42Z
> **更新时间**: 2024-08-01T15:32:04Z
> **关闭时间**: 2024-08-01T15:32:04Z
> **作者**: Walaryne
> **标签**: application:pytorch, aimodel:stablediffusion
> **URL**: https://github.com/ROCm/ROCm/issues/2330

## 标签

- **application:pytorch** (颜色: #bfdadc)
- **aimodel:stablediffusion** (颜色: #c2e0c6)

## 描述

I'm on ROCm 5.6.0
Linux kernel 6.5.0-1-MANJARO

ROCm info output:


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

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 7700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   5573                               
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
      Size:                    31974820(0x1e7e5a4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31974820(0x1e7e5a4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31974820(0x1e7e5a4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-e0ce170bfa1769dd               
  Marketing Name:          AMD Radeon RX 6800 XT              
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2575                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            72                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   28160                              
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
*** Done ***`
```

System will freeze, go to a black screen, wait, then attempt a reboot shortly. Reboot will succeed but VGA will not reinitialize. 
Hard poweroff is required to power down card and reset VGA.
I've done stress testing to try and rule out RAM overclocking, CPU undervolting, etc.
None of these things seem to factor into whether it crashes.
GPU temperatures seem stable (junction around 90C max, everything else below 70C).
Issue does not occur during gaming, or even heavy gaming workloads.
Tested Linux 6.1.39, 6.2.0, 6.3.13, 6.4.4, and 6.5.0, issue occurs on all versions.

Steps to reproduce:
Run Automatic1111 Stable Diffusion until issue occurs.

---

## 评论 (23 条)

### 评论 #1 — xuhuisheng (2023-07-22T23:06:10Z)

try pytroch 1.13

---

### 评论 #2 — lenhone (2023-07-26T01:08:03Z)

I get the same crashes with a RX6800 within a minute with PyTorch rocm5.42 and PyTorch rocm5.5 (nightly) running stable diffusion or whisper. However PyTorch rocm5.2 runs without issue, you can install from the [previous-versions](https://pytorch.org/get-started/previous-versions/) page but be aware there is no python 3.11 version so installing it can be a pain.

After the crash, power off, power on, running `journactl -b-1` shows an error about 50% of the time (shown below). Machine learning on RDNA2 is a no go for the foreseeable future.

```
May 11 13:59:42 crash kernel: i2c-designware-pci 0000:08:00.3: Unable to change power state from D3hot to D0, device inaccessible
May 11 13:59:53 crash kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma0 timeout, signaled seq=5509, emitted seq=5512
May 11 13:59:53 crash kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process  pid 0 thread  pid 0
May 11 13:59:53 crash kernel: amdgpu 0000:08:00.0: amdgpu: GPU reset begin!
May 11 13:59:53 crash kernel: amdgpu: Failed to suspend process 0x8007
May 11 13:59:53 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:41 param:0x00000000 message:DisallowGfxOff?
May 11 13:59:53 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to disable gfxoff!
```

```
Jun 14 10:47:36 crash kernel: i2c-designware-pci 0000:08:00.3: Unable to change power state from D3hot to D0, device inaccessible
```

```
Jun 21 21:43:48 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to export SMU metrics table!
Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to export SMU metrics table!
Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to export SMU metrics table!
```

---

### 评论 #3 — serhii-nakon (2023-07-27T21:05:28Z)

Try disable integrated graphic, I had the similar problem when it was active while I used HIP

---

### 评论 #4 — Walaryne (2023-07-31T02:27:25Z)

> Try disable integrated graphic, I had the similar problem when it was active while I used HIP

Doesn't work, it's another thing I tried

---

### 评论 #5 — Walaryne (2023-07-31T02:28:20Z)

> I get the same crashes with a RX6800 within a minute with PyTorch rocm5.42 and PyTorch rocm5.5 (nightly) running stable diffusion or whisper. However PyTorch rocm5.2 runs without issue, you can install from the [previous-versions](https://pytorch.org/get-started/previous-versions/) page but be aware there is no python 3.11 version so installing it can be a pain.
> 
> After the crash, power off, power on, running `journactl -b-1` shows an error about 50% of the time (shown below). Machine learning on RDNA2 is a no go for the foreseeable future.
> 
> ```
> May 11 13:59:42 crash kernel: i2c-designware-pci 0000:08:00.3: Unable to change power state from D3hot to D0, device inaccessible
> May 11 13:59:53 crash kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma0 timeout, signaled seq=5509, emitted seq=5512
> May 11 13:59:53 crash kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process  pid 0 thread  pid 0
> May 11 13:59:53 crash kernel: amdgpu 0000:08:00.0: amdgpu: GPU reset begin!
> May 11 13:59:53 crash kernel: amdgpu: Failed to suspend process 0x8007
> May 11 13:59:53 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:41 param:0x00000000 message:DisallowGfxOff?
> May 11 13:59:53 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to disable gfxoff!
> ```
> 
> ```
> Jun 14 10:47:36 crash kernel: i2c-designware-pci 0000:08:00.3: Unable to change power state from D3hot to D0, device inaccessible
> ```
> 
> ```
> Jun 21 21:43:48 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
> Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to export SMU metrics table!
> Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
> Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to export SMU metrics table!
> Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
> Jun 21 21:43:49 crash kernel: amdgpu 0000:08:00.0: amdgpu: Failed to export SMU metrics table!
> ```

Glad to know I'm not crazy and someone else is experiencing this. PyTorch workloads are the only workloads I've seen this happen under.

EDIT: Also you mentioned Torch 1.13.1? Or perhaps 1.13.0. I tried 1.13.1 while running system ROCm 5.6, and still experienced the same crash. Do you happen to remember the system ROCm version you used while it was stable?

---

### 评论 #6 — serhii-nakon (2023-08-02T10:05:54Z)

ROCm 5.4 doesn't support your video card. And I think Pytorch 1.13 also not support you card 

You should use at least ROCm 5.6 and rebuild Pytorch 1.13 with support you card.

---

### 评论 #7 — serhii-nakon (2023-08-02T10:11:02Z)

Or if it possible you can use Pytorch from this Docker container that already built with support you card ( https://hub.docker.com/layers/rocm/pytorch/rocm5.6_ubuntu20.04_py3.8_pytorch_1.13.1/images/sha256-267e5045f7c51b7ae252d429f664dca83a5fa8d99100c45ca736a26758748ee2?context=explore)

---

### 评论 #8 — serhii-nakon (2023-08-02T10:16:38Z)

And I think that better to use latest stable release of Linux kernel with this Docker.

---

### 评论 #9 — Walaryne (2023-08-02T11:33:31Z)

I'm pretty sure this is a firmware bug considering the nature of it. But I can try playing with the versions again. Frankly I really don't think the version of Torch, a userspace program, should have the slightest bearing on crashing the entire system. I might give that Docker image a try, but I'm not hopeful.

---

### 评论 #10 — lenhone (2023-08-03T07:13:35Z)

> ROCm 5.4 doesn't support your video card.

Currently AMD [does not support](https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html) any RDNA2 consumer hardware with Rocm on Linux. However some RDNA2 chips sometimes work due to similarity with the supported "Radeon Pro W6800". I have no issues with the following torch version regardless of system Rocm version 5.2 through 5.6.
```
# ROCM 5.2 (Linux only)
pip install torch==1.13.1+rocm5.2 torchvision==0.14.1+rocm5.2 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/rocm5.2
```

> I'm pretty sure this is a firmware bug considering the nature of it. But I can try playing with the versions again. Frankly I really don't think the version of Torch, a userspace program, should have the slightest bearing on crashing the entire system. I might give that Docker image a try, but I'm not hopeful.

AMD GPUs crashing the system from user-space is often reported at the [DRM repo](https://gitlab.freedesktop.org/drm/amd/-/issues), unfortunately it is rare to see issues closed successfully.

There are however [34 entries](https://vladmandic.github.io/sd-extension-system-info/pages/benchmark.html) of 6800/XT users using Stable Diffusion with Torch 2.0+, weather they did this between crashes I don't know.

---

### 评论 #11 — Walaryne (2023-08-03T11:54:34Z)

@lenhone I guess perhaps we might just have "bad" silicon or some other hardware issue going on. I've tried power limiting the card so I doubt it's power related. But at the same time, considering the crash only happens when running AI, and only AI, I must assume it's an issue with ROCm/Linux Kernel DRM. Considering the card's blatant refusal to reset itself after this failure, maybe it's even the VBIOS, or some random PCIe issue on my motherboard. I guess that's the very unfortunate part, that it could be so many things going wrong.

In a major turn of misfortune, I did in fact use that exact version of Torch like you specified, and still managed a crash.

Also if you don't mind my prying, do you happen to have the Linux kernel version you're using, and are you using the PRO version of the amdgpu driver? Also to clarify, your card does refuse to reinitialize VGA after the hard crash then reboot (black screen but Linux boots underneath, card is completely locked up)? I do want to isolate variables so I can maybe reproduce your success.

Sidenote: You don't happen to *also* be using Ryzen 7000 and an X670E motherboard, do you? (with your GPU made by XFX?) 😬 

EDIT: Would also like to point out:
I haven't ever seen this in my own personal logs from my memory, but i2c-designware-pci is the I2C bus interface on the actual card. It is, from my understanding, locking up so hard that it doesn't even respond to I2C communication. That's frankly insane.

EDIT again: More research done. Lots of people reporting issues with I2C on an AMD card were in fact, having BIOS issues. I'm pretty disheartened this might never get fixed since my board is from Asus. There's a new BIOS update out, so I guess I can try doing that. Perhaps you could try the same.

It'd be absolutely amazing if someone at AMD could mention how to sniff the I2C comms to the card, as it would likely be very very enlightening.

EDIT 3: Found this incredibly eerily similar DRM issue report.
https://gitlab.freedesktop.org/drm/amd/-/issues/1871

I did attempt the patch contained, no luck whatsoever.

---

### 评论 #12 — serhii-nakon (2023-08-05T10:38:14Z)

> I'm pretty sure this is a firmware bug considering the nature of it. But I can try playing with the versions again. Frankly I really don't think the version of Torch, a userspace program, should have the slightest bearing on crashing the entire system. I might give that Docker image a try, but I'm not hopeful.

PyTorch should be built with support you card, I mean that I not sure that official PyTorch rebuild with support you card but I sure that Docker container that i sent support it (see screenshot)

PS: I had DRM/AMDGPU errors with official PyTorch and after rebuild it fixed.
 
![image](https://github.com/RadeonOpenCompute/ROCm/assets/57632032/b5c0e574-9cf8-472c-a687-216640c886ff)
  

---

### 评论 #13 — Kademo15 (2023-08-07T18:51:14Z)

@Walaryne Try using the 5.19 kernel for my rx7900xtx it works without an issue. [testes kernels](https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html#supported-distributions)

---

### 评论 #14 — Walaryne (2023-08-07T18:52:46Z)

> @Walaryne Try using the 5.19 kernel for my rx7900xtx it works without an issue. [testes kernels](https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html#supported-distributions)

I could try it, hopefully that's not too old of a kernel for my AM5 system though.

---

### 评论 #15 — Kademo15 (2023-08-07T20:48:54Z)

im on am5 too it works for me

---

### 评论 #16 — Walaryne (2023-08-08T14:52:28Z)

@Kademo15 Were you experiencing the same crashes described here? (Card stuck in unrecoverable state till force poweroff?)

Because if this works, we have a jumping off point for bisecting the kernel/firmware.

---

### 评论 #17 — lenhone (2023-08-08T14:53:18Z)

> Also if you don't mind my prying, do you happen to have the Linux kernel version you're using, and are you using the PRO version of the amdgpu driver? Also to clarify, your card does refuse to reinitialize VGA after the hard crash then reboot (black screen but Linux boots underneath, card is completely locked up)? I do want to isolate variables so I can maybe reproduce your success.

Hi Walaryne, answers to you questions below.

- Current kernel is 6.4.7-arch1-2
- I use opencl-amd from the AUR which installs the .deb packaged rocm stuff from repo.radeon. For example https://repo.radeon.com/rocm/apt/5.6/pool/main/h/hip-runtime-amd/hip-runtime-amd_5.6.31061.50600-67~22.04_amd64.deb. 
- My system also refuse to reinitialize VGA after the hard crash. I am left with a black screen until I power off and power on again.
-  My GPU is a Sapphire RX6800 reference model.

There are many variables that may cause the crash. Unfortunately I have not crossed any off the list as I don't have any duplicate hardware.
- GPU - Overheating / defective silicone / defective bios
- Mother board - Power delivery (does the mother board prevent the GPU powering up after crash)
- CPU - MCE / Power issues with C-state

Best of luck with your investigations, report back if you stop the crashes!



---

### 评论 #18 — Walaryne (2023-08-08T15:09:40Z)

@lenhone Thank you so much for the info. It's going to help a lot at deciphering this. VBIOS seems unlikely considering our cards are from different manufacturers. If I was crazy I'd try a W6800 VBIOS. My best guess considering the otherwise perfect function of our cards (to the best of my knowledge) points to either:

A: An SMU issue.
B: Invalid register state.

But regardless the issue seems to lie in the linux-firmware, or the DRM/amdgpu components of the kernel itself. But I still have not confirmed a working kernel/linux-firmware for myself.

---

### 评论 #19 — Kademo15 (2023-08-08T16:33:44Z)

@Walaryne no not these but i had my share of compiling issues when i was on the 6.x kernels

---

### 评论 #20 — lenhone (2023-08-09T02:11:59Z)

Looks like this issue is similar to https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/11155#issuecomment-1589973562

I have installed CoreCtl and have access to the "advanced" voltage offset / GPU clock / Memory clock. Hopefully I get some time in the near future to play with these settings to see if stability improves.

---

### 评论 #21 — Walaryne (2023-08-09T12:57:15Z)

> Looks like this issue is similar to [AUTOMATIC1111/stable-diffusion-webui#11155 (comment)](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/11155#issuecomment-1589973562)
> 
> I have installed CoreCtl and have access to the "advanced" voltage offset / GPU clock / Memory clock. Hopefully I get some time in the near future to play with these settings to see if stability improves.

I was able to give your suggestion a try last night, sadly no dice for me. At least not on Torch 2.0. Still doing more research though, trying not to give up. Let me know how it works for you.

---

### 评论 #22 — ppanchad-amd (2024-05-14T15:06:47Z)

@Walaryne  Can you please test with latest ROCm 6.1.1 to see if it resolve your issues. Thanks!

---

### 评论 #23 — ppanchad-amd (2024-08-01T15:32:04Z)

@Walaryne Closing ticket since we haven't heard from you in a while. Please re-open if you still encounter the issue with the latest ROCm software. Thanks!

---
