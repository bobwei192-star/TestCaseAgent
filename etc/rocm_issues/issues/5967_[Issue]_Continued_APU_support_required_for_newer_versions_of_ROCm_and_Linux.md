# [Issue]: Continued APU support required for newer versions of ROCm and Linux

> **Issue #5967**
> **状态**: open
> **创建时间**: 2026-02-15T08:28:06Z
> **更新时间**: 2026-05-04T23:58:24Z
> **作者**: nav9
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5967

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Latest ROCm versions (6 & 7) [do not appear to work](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html) on Linux Mint 22 / Ubuntu 24 for the GPU/APU integrated with the CPU. The last known working version was version 5.4.5, on Linux Mint 21. There have been some complaints about it mentioned in [this thread](https://github.com/ROCm/ROCm/issues/2216#issuecomment-2001933917) too.
  
**Problems:**  
* I had to switch back to using Mint 21 because of this. It prevents me from making use of the newest features and security updates of the newer operating systems.
* High-profile third party frameworks like Mojo struggle to provide support for such APU's as mentioned [here](https://forum.modular.com/t/how-to-get-mojo-to-detect-amd-integrated-gpu-apu/2727). This is a systemic technical hurdle.  
* GPU prices have skyrocketed, and for various segments of users it is uneconomical to purchase a new GPU, so it would help to be able to continue to use the integrated GPU which we spent our hard earned money to purchase. Especially for hobby projects and basic machine learning and even gaming, it is useful.
  
Could AMD ensure that such hardware is supported with software updates for at least 10 to 15 years? Would it be possible for y'all to put forward such a request to your managers and obtain approval? Or would it help if users like me send an email to perhaps `rocm-feedback@amd.com` regarding this to request for support?

### Operating System

Linux Mint 21.3 (Virginia)

### CPU

AMD Ryzen 5 5600G with Radeon Graphics

### GPU

gfx90c amdgcn-amd-amdhsa--gfx90c:xnack- AMD Ryzen 5 5600G with Radeon Graphics

### ROCm Version

6 or 7 (the last working version was 5.4.5. Even 5.5.5 didn't work on my hardware (gets installed but pytorch was unable to use the GPU, if I remember correctly))

### ROCm Component

_No response_

### Steps to Reproduce

Install Linux Mint 22. Try installing ROCm versions compatible with Linux Mint 22. Then try running PyTorch and see if it can detect and use the GPU like in [this page](https://github.com/ROCm/ROCm/issues/2216#issuecomment-1637054248).

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

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 5 5600G with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5600G with Radeon Graphics
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
  Max Clock Freq. (MHz):   3900                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    28619192(0x1b4b1b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    28619192(0x1b4b1b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    28619192(0x1b4b1b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx90c                             
  Uuid:                    GPU-XX                             
  Marketing Name:                                             
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
    L2:                      1024(0x400) KB                     
  Chip ID:                 5688(0x1638)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1900                               
  BDFID:                   12288                              
  Internal Node ID:        1                                  
  Compute Unit:            7                                  
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    4194304(0x400000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx90c:xnack-   
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

### Additional Information

_No response_

---

## 评论 (17 条)

### 评论 #1 — alpharder (2026-02-23T00:36:22Z)

No dude just buy Intel instead, that's what I learned with AMD drivers. They won't let you use your hardware. Go buy Ryzen AI and it will also be dropped in a year or two.

---

### 评论 #2 — harkgill-amd (2026-03-05T17:29:19Z)

Hey @nav9, we've been working on expanding our HW support as much as possible, with a focus on enabling older architectures that previously lacked support. For example, architecture families such as `gfx101X` and `gfx90X` now have nightly builds available at https://rocm.nightlies.amd.com/v2. 

In terms of APUs, we provide builds for the majority of newer APUs such as Phoenix/Strix Halo and are working towards posting builds for `gfx103X` APUs/iGPUs (Radeon 680M, Ryzen 7000 iGPUs.etc) as well. While official support can be difficult for older hardware, especially iGPUs, we're committed to help maintain as much functionality as possible, see the following [discussion ](https://github.com/ROCm/ROCm/discussions/4276#discussioncomment-15164487)for more info on this. if you are experiencing a regression in this aspect, this is something that needs to be investigated. 

I'll try getting my hands on a 5600G to see if I can reproduce the PyTorch detection failures on my end. 

---

### 评论 #3 — nav9 (2026-03-05T19:46:08Z)

Thank you @harkgill-amd. I'm assuming the `X` in `gfx90X` is a placeholder, so hoping my `gfx90c` would be supported.  
1. Glad to see that nightly builds are available (though I get a `The specified key does not exist` error for [this](https://rocm.nightlies.amd.com/gfx90X-dcgpu/) link (Update: As the user nikelborm [mentioned below](https://github.com/ROCm/ROCm/issues/5967#issuecomment-4335404197), the correct link may be [this](https://rocm.nightlies.amd.com/tarball/))). If it's currently accessible only to AMD employees, perhaps relevant links and info could be added [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html) and [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) too in due time?  
2. [Owen suggested](https://forum.modular.com/t/how-to-get-mojo-to-detect-amd-integrated-gpu-apu/2727/13) that it might simply be a matter of adding a target in the build. I'm mentioning this out of curiosity of whether the solution may actually be as simple as that.
3. I have the option of uninstalling ROCm 5.4.5 from my SSD to try installing the latest ROCm (but this is on Linux Mint 21). I also have the option of disconnecting the SSD and connecting a spare hard disk onto which I could install Linux Mint 22.2 and try various versions of ROCm and mention what errors I encountered. Do let me know if my input is required, though I guess the easier option is what you mentioned about finding a 5600G.  
4. I did wonder if it'd be possible for AMD to build emulators or digital twins of hardware to be able to automate various aspects of testing, but I guess the hardware-software interaction requires the actual thing.
I'm grateful that you and your team are looking into this. Please do let me know if my help/input/feedback is required at any stage.

---

### 评论 #4 — harkgill-amd (2026-03-06T20:06:41Z)

We don't have gfx90c builds published in TheRock _yet_ though gfx906 is also based off the same GCN 5.1 architecture, which we do have builds available for. I was able to get a 5700G up and running with torch using these builds + overriding the gfx90c to gfx906 with the following steps,
```
python3 -m venv .venv
source .venv/bin/activate
pip install   --extra-index-url https://rocm.nightlies.amd.com/v2-staging/gfx906/   torch torchaudio torchvision
export HSA_OVERRIDE_GFX_VERSION=9.0.6
```
After this, not only did the [test script](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533) you shared pass, but I also went ahead and generated a much more detailed sanity test which is also passing for all cases. I'll share it here so you can give it a try as well with the 5600G - [test_gfx_support.py](https://github.com/user-attachments/files/25803284/test_gfx_support.py).

We'd obviously rather have targeted builds for gfx90c rather than having users HSA Override to different architectures so I've also opened https://github.com/ROCm/TheRock/issues/3818 to get the ball rolling on this. 

---

### 评论 #5 — nav9 (2026-03-07T19:29:56Z)

Thank you @harkgill-amd. I tried with a fresh install of Linux Mint 21 and 22 as per [these steps](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html). There are two issues that are essentially installation-related rather than ROCm related, but like how Matt Damon's character in `The Martian` said: _"At some point, everything's gonna go south on you... You just begin. You do the math. You solve one problem... and you solve the next one... and then the next"_. 
    
**Issue1 on Linux Mint 21 (Ubuntu 22):**  
On installing, it shows a `permission denied` error at the end of the last line which can make Users think the installation failed, when in reality I realized it actually was successful (but there's still Issue 2 below):  
 ```
sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
[sudo] password for nav:                  
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'amdgpu-install' instead of './amdgpu-install_7.2.70200-1_all.deb'
The following NEW packages will be installed:
  amdgpu-install
0 upgraded, 1 newly installed, 0 to remove and 624 not upgraded.
Need to get 0 B/17.0 kB of archives.
After this operation, 73.7 kB of additional disk space will be used.
Get:1 /home/nav/amdgpu-install_7.2.70200-1_all.deb amdgpu-install all 30.30.0.0.30300000-2278356.22.04 [17.0 kB]
Selecting previously unselected package amdgpu-install.
(Reading database ... 537476 files and directories currently installed.)
Preparing to unpack .../amdgpu-install_7.2.70200-1_all.deb ...
Unpacking amdgpu-install (30.30.0.0.30300000-2278356.22.04) ...
Setting up amdgpu-install (30.30.0.0.30300000-2278356.22.04) ...
N: Download is performed unsandboxed as root as file '/home/nav/amdgpu-install_7.2.70200-1_all.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
```  
The permission denied issue does not happen on Linux Mint 22 though.  
  
**Issue 2 on Linux Mint 21 (Ubuntu 22) and 22 (Ubuntu 24):**  
* Mint 21: `sudo apt install rocm` requires downloading 6.7GB of archives which after installation takes up 27.8GB of disk space.
* Mint 22: `sudo apt install rocm` requires downloading 6.9GB of archives which after installation takes up 28.1GB of disk space. Running `amdgpu-install` by itself requires downloading 891MB of archives which takes 1.6GB disk space, and running `amdgpu-install --usecase=hiplibsdk,rocm,dkms` would require downloading 6.9GB of archives which will take up 28.7GB disk space.  
  
**Why it's an issue:**  
Various people (like me, [this person](https://github.com/flutter/flutter/issues/89000#issuecomment-909208366) and [this person](https://github.com/flutter/flutter/issues/102040#issue-1206425591)) work on connections that have a daily usage limit (2GB in my case) or flaky internet. A first step would be to ensure that Users would be able to download rocm and install it. So would there be ways to eventually:
1. Use any flag to install only what is necessary? (6GB for rocm seems like overkill)
2. Download a large deb file via a single seeded torrent?

---

### 评论 #6 — JohnLoveJoy (2026-03-08T13:23:57Z)

> Thank you [@harkgill-amd](https://github.com/harkgill-amd). I tried with a fresh install of Linux Mint 21 and 22 as per [these steps](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html). There are two issues that are essentially installation-related rather than ROCm related, but like how Matt Damon's character in `The Martian` said: _"At some point, everything's gonna go south on you... You just begin. You do the math. You solve one problem... and you solve the next one... and then the next"_.
> 
> **Issue1 on Linux Mint 21 (Ubuntu 22):** On installing, it shows a `permission denied` error at the end of the last line which can make Users think the installation failed, when in reality I realized it actually was successful (but there's still Issue 2 below):
> 
> ```
> sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
> [sudo] password for nav:                  
> Reading package lists... Done
> Building dependency tree... Done
> Reading state information... Done
> Note, selecting 'amdgpu-install' instead of './amdgpu-install_7.2.70200-1_all.deb'
> The following NEW packages will be installed:
>  amdgpu-install
> 0 upgraded, 1 newly installed, 0 to remove and 624 not upgraded.
> Need to get 0 B/17.0 kB of archives.
> After this operation, 73.7 kB of additional disk space will be used.
> Get:1 /home/nav/amdgpu-install_7.2.70200-1_all.deb amdgpu-install all 30.30.0.0.30300000-2278356.22.04 [17.0 kB]
> Selecting previously unselected package amdgpu-install.
> (Reading database ... 537476 files and directories currently installed.)
> Preparing to unpack .../amdgpu-install_7.2.70200-1_all.deb ...
> Unpacking amdgpu-install (30.30.0.0.30300000-2278356.22.04) ...
> Setting up amdgpu-install (30.30.0.0.30300000-2278356.22.04) ...
> N: Download is performed unsandboxed as root as file '/home/nav/amdgpu-install_7.2.70200-1_all.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
> ```
> 
> The permission denied issue does not happen on Linux Mint 22 though.
> 
> **Issue 2 on Linux Mint 21 (Ubuntu 22) and 22 (Ubuntu 24):**
> 
> * Mint 21: `sudo apt install rocm` requires downloading 6.7GB of archives which after installation takes up 27.8GB of disk space.
> *** Mint 22: `sudo apt install rocm` requires downloading 6.9GB of archives which after installation takes up 28.1GB of disk space.** Running `amdgpu-install` by itself requires downloading 891MB of archives which takes 1.6GB disk space, and running `amdgpu-install --usecase=hiplibsdk,rocm,dkms` would require downloading 6.9GB of archives which will take up 28.7GB disk space.
> 
> **Why it's an issue:** Various people (like me, [this person](https://github.com/flutter/flutter/issues/89000#issuecomment-909208366) and [this person](https://github.com/flutter/flutter/issues/102040#issue-1206425591)) work on connections that have a daily usage limit (2GB in my case) or flaky internet. A first step would be to ensure that Users would be able to download rocm and install it. So would there be ways to eventually:
> 
> 1. Use any flag to install only what is necessary? (6GB for rocm seems like overkill)
> 2. Download a large deb file via a single seeded torrent?

ROCm is still somewhat bloated. 

---

### 评论 #7 — IMbackK (2026-03-08T21:45:22Z)

@harkgill-amd gfx90c dosent support all instructions that gfx906 supports, so gfx900 is the safe override.

---

### 评论 #8 — harkgill-amd (2026-03-09T15:23:57Z)

@nav9 - so we currently offer a couple different installation pathways for ROCm. You're trying the generic package manager based installation that relies on amdgpu-install/apt whereas the instructions I shared provide targeted ROCm installations using TheRock/pip. The latter is what'll give you functionality with gfx90c and also partially addresses your concern of installing only what's necessary - the expanded ROCm packages for gfx906 come out to a little less than 12GB on my end.

@IMbackK - Yup, though we're still waiting on https://github.com/ROCm/TheRock/pull/3564 for gfx900 nightlies. Hopefully we can get the gfx90c nightlies in around the same time as well.

---

### 评论 #9 — IMbackK (2026-03-09T16:26:47Z)

@harkgill-amd yeah the return of gfx900 is a great thing, esp since the list of gfx900 derivatives is so long. Hopefully some time soon you guys will be at the point where you can just build for gfx9-generic and have one build for all of these gfx9 variants besides gfx906 and CDNA.

---

### 评论 #10 — nav9 (2026-03-10T19:25:44Z)

@harkgill-amd : Good news! It works on my computer ([script1](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533) and [script2](https://github.com/user-attachments/files/25803284/test_gfx_support.py)). I tried it on the partition where I did a fresh install of Linux Mint 22 (Ubuntu 24), so there are a few additions to the steps you mentioned. It took around 1.6GB of internet download to do this installation.
```
sudo apt update
sudo apt install python3-pip
sudo apt install python3.12-venv
python3 -m venv .venv
source .venv/bin/activate
pip install   --extra-index-url https://rocm.nightlies.amd.com/v2-staging/gfx906/   torch torchaudio torchvision
export HSA_OVERRIDE_GFX_VERSION=9.0.6
sudo usermod -a -G video $USER
sudo usermod -a -G render $USER
```
Now reboot the computer.
```
amd-smi version #shows the rocm version
python3 rocm_test.py
python3 test_gfx_support.py
``` 
Output of script 1:  
```
Checking ROCM support...
GOOD: ROCM devices found:  2
Checking PyTorch...
GOOD: PyTorch is working fine.
Checking user groups...
GOOD: The user nav is in RENDER and VIDEO groups.
GOOD: PyTorch ROCM support found.
Testing PyTorch ROCM support...
Everything fine! You can run PyTorch code inside of: 
--->  AMD Ryzen 5 5600G with Radeon Graphics  
--->  gfx906
```
Output of script 2:
```
============================================================
  Level 1 — CPU Basics
============================================================
  [PASS] Import torch  (v2.10.0+rocm7.12.0a20260310)
  [PASS] Tensor creation
  [PASS] Element-wise add
  [PASS] CPU matmul (64x64)
  [PASS] Autograd (dy/dx of x²)

============================================================
  Level 2 — Device Detection
============================================================
  [PASS] GPU available (torch.cuda)  (ROCm/HIP)
  [PASS] Device count  (1)
  [PASS] GPU 0 properties  (AMD Radeon Graphics — 13.7 GB, SM/CU 7)
  [PASS] Runtime version  (7.12.60610)

============================================================
  Level 3 — GPU Fundamentals
============================================================
  [PASS] Tensor on GPU
  [PASS] CPU→GPU transfer
  [PASS] GPU→CPU transfer
  [PASS] GPU arithmetic (512x512)
  [PASS] GPU memory alloc/free  (peak 19.2 MB → 3.2 MB)

============================================================
  Level 4 — Intermediate Compute
============================================================
  [PASS] Large matmul (1024x1024)  (902.13 ms)
  [PASS] Batched matmul (8x512x512)
  [PASS] Einsum (bij,bjk->bik)
  [PASS] NN forward pass (MLP)
  [PASS] NN backward pass  (loss=0.0000)
  [PASS] Float16 matmul (1024²)
  [PASS] BFloat16 matmul (1024²)

============================================================
  Level 5 — Intermediate System
============================================================
  [PASS] CUDA streams
  [PASS] Stream synchronization
  [PASS] Pinned memory transfer  (7.60 ms)
  [PASS] DNN backend available  (MIOpen)
  [SKIP] Multi-GPU P2P access  (single GPU)
  [PASS] Conv2d forward (DNN backend)  (8659.32 ms)
  [PASS] torch.compile

============================================================
  Summary
============================================================
  Total : 28
  PASS  : 27
  FAIL  : 0
  SKIP  : 1

```
I hadn't quite understood how the rocm installation works with a virtual environment. A few questions:
* I didn't have to install the AMD GPU driver. From what I understand, the GPU driver is the base kernel-level driver for display and power management and rocm is a higher level software for compute tasks like AI. How did rocm work without AMD GPU installation?
* From what I understand, the rocm installed via apt is a lower level kernel driver and rocm installed via pip inside the venv is installed in the user space in the virtual environment. So if I need to use Modular Mojo or a raw C++ program that uses the GPU, I would need the apt installation of rocm. Am I correct? 
* If I decide to install rocm in a virtual environment on my Linux Mint 21 which already has rocm 5.4 installed via apt, I reckon I won't have to uninstall rocm 5.4 because rocm 7.2 will be installed in the virtual environment?
  
I'm impressed at how y'all have [got rocm working for llama.cpp](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/llama-cpp-install.html) via Docker. Although I hoped to be able to install rocm as a low level driver that allows any program to use it (even for llama-cpp, and also for games that require some GPU usage). For the rocm 5.4 (installed via apt) I have on Linux Mint 21, I've seen via radeontop, how even applications like three.js are able to use the GPU. Perhaps the simplest way to do this installation would be to have a large deb file (or multiple deb files) which can be downloaded via a torrent and during installation it could ask the User which components to install.

---

### 评论 #11 — harkgill-amd (2026-03-12T18:30:55Z)

Happy to hear it's working on your end!

> How did rocm work without AMD GPU installation?

So with the virtual environment install, you didn't install the amdgpu driver (`amdgpu-dkms`) that you'd normally find in a regular ROCm installation but you'd still have the inbox kernel driver that comes with your Linux distro up and running. See https://rocm.blogs.amd.com/ecosystems-and-partners/instinct-gpu-driver/README.html for some more information on how we're working towards separating the driver install from the user level ROCm install - it's an older blog so the naming has changed a bit but the premise is the same. TL;DR you don't need the amdgpu-dkms package for your usecase and the inbox kernel driver will work just fine. 

> From what I understand, the rocm installed via apt is a lower level kernel driver and rocm installed via pip inside the venv is installed in the user space in the virtual environment. So if I need to use Modular Mojo or a raw C++ program that uses the GPU, I would need the apt installation of rocm. Am I correct?

The previous link on ROCm modularity should help clear up this question as well but in essence - the `amdgpu` driver is the lower level driver. For the user level ROCm install, you can get that from either the apt installation or the venv based installation but both provide the same functionality. 

> If I decide to install rocm in a virtual environment on my Linux Mint 21 which already has rocm 5.4 installed via apt, I reckon I won't have to uninstall rocm 5.4 because rocm 7.2 will be installed in the virtual environment?

They should be able to coexist, with the ROCm 7.2 libraries getting picked up when you're working in the virtual environment. You could even have newer versions of ROCm in separate virtual environments for a real Muti-ROCm installation :). The only recommendation I'd have here is to uninstall the amdgpu-dkms package that you'd have picked up with your 5.4 ROCm install `sudo apt remove amdgpu-dkms`. This is on the older side and uninstalling should put you back to the inbox kernel driver after a reboot.

---

### 评论 #12 — IMbackK (2026-03-12T18:49:29Z)

@nav9 I would second @harkgill-amd's recommendation for people to use the mainline "inbox" kernel modules, which i think is a good idea for almost all rocm users, but i would mention that for some features the undocumented envvar HSA_ENABLE_IPC_MODE_LEGACY=0 is required, sutch as rccl or upcoming parallel multigpu support in llamacpp/GGML. 

Currently the combination of ROCM and the mainline kernel will otherwise fail with very unhelpful error messages as it will attempt to use ioctls that dont exist.

---

### 评论 #13 — nav9 (2026-03-13T15:12:16Z)

@harkgill-amd : I think it's brilliant to be able to have a Multi-ROCm installation. There is however one problem I ran into with Mojo's [vector addition program](https://docs.modular.com/mojo/manual/gpu/intro-tutorial/) on Linux Mint 22 which had the latest rocm installed in the venv. The Mojo program output "_No compatible GPU found_" (I think Mojo and the Modular MAX engine rely on ROCm's lower-level HIP/HSA runtimes). But running an OpenCL program (which used the GPU) outside the venv worked fine. So maybe a system-wide installation of rocm might help for wider support of various frameworks and languages. It could potentially help a much wider userbase...especially students or people who are not software engineers but are trying out machine learning.  
Nice to know that the amdgpu driver is not really required. Humble suggestion: It could be mentioned on the [install page](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) and/or if anyone does not read it and downloads and installs it, the installer itself could be programmed to examine the User's hardware and inform them that the installation can be aborted.  
  
@IMbackK : Ok then, I guess I'll stick to Linux 21 and rocm 5.4 until full compatibility is implemented for the newer versions. Sadly this means I won't be able to try running Mojo's [Build an LLM from scratch](https://llm.modular.com/). I've [welcomed their input](https://forum.modular.com/t/how-to-get-mojo-to-detect-amd-integrated-gpu-apu/2727/17) to this thread too.
  
I'm grateful that y'all are extending support for hardware like mine too. As you proceed with it, if y'all ever need any help from me in running any software and providing feedback on whether it works or not, I'll be happy to help!

---

### 评论 #14 — harkgill-amd (2026-03-25T17:53:21Z)

Hey @nav9, apologies for the delay in response. Mojo can work by patching the [info.mojo](https://github.com/modular/modular/blob/main/mojo/stdlib/std/gpu/host/info.mojo) with `gfx906` support (Still overriding to this for now). Calling on this custom build stdlib with `MODULAR_MOJO_MAX_IMPORT_PATH` resulted in the vector addition sample program correctly enumerating the iGPU, 
```
MODULAR_MOJO_MAX_IMPORT_PATH=bazel-bin/mojo/stdlib/std mojo ~/vector_addition.mojo
Found GPU: AMD Radeon Graphics
```
This is obviously just a POC and it might fail for more complex operations downstream but it's a good starting point for Vega support there. 

>  So maybe a system-wide installation of rocm might help for wider support of various frameworks and languages.

We'll still offer the package manager based installation option in future releases as well, though it'll likely be limited to officially supported SKUs - see [ROCm 7.11](https://rocm.docs.amd.com/en/7.11.0-preview/install/rocm.html?fam=ryzen&gpu=max-pro-395&os=ubuntu&os-version=24.04&i=pkgman#install-amd-rocm-rocm-version) for example

> Nice to know that the amdgpu driver is not really required. Humble suggestion: It could be mentioned on the [install page](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)

Similiary, with 7.11 and future docs releases, we are starting to make this distinction clearer for which devices require amdgpu-dkms vs which ones can proceed with the inbox kernel driver ([example](https://rocm.docs.amd.com/en/7.11.0-preview/install/rocm.html?fam=ryzen&gpu=max-pro-395&os=ubuntu&os-version=24.04&i=pkgman#about-the-kernel-driver-fam-ryzen-os-ubuntu)).

We're making progress on https://github.com/ROCm/TheRock/issues/3818, will ping you there if we need any help with testing!

---

### 评论 #15 — nikelborm (2026-04-28T12:51:40Z)

@nav9
> Glad to see that nightly builds are available (though I get a The specified key does not exist error for [this](https://rocm.nightlies.amd.com/gfx90X-dcgpu/) link)

Not sure if this is what you're looking for, but I was able to find gfx90X-dcgpu entries here by scrolling to the bottom and then using search on the page:
https://rocm.nightlies.amd.com/tarball/

---

### 评论 #16 — nav9 (2026-04-28T15:10:05Z)

@nikelborm : Hey thanks a lot. That does indeed seem to be the right place to look for the tar files. I've [updated my earlier comment now](https://github.com/ROCm/ROCm/issues/5967#issuecomment-4007338731) so that anyone who needs that info would be able to find it. Anyway, as per what @harkgill-amd replied, they are continuing with the updates, so it'll probably take a while until it's ready.

---

### 评论 #17 — cdanis (2026-05-04T23:58:24Z)

Watching for Strix Halo ROCm fixes.

---
