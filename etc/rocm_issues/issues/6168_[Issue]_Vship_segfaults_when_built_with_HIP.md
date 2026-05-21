# [Issue]: Vship segfaults when built with HIP

> **Issue #6168**
> **状态**: open
> **创建时间**: 2026-04-21T11:39:36Z
> **更新时间**: 2026-05-15T19:24:46Z
> **作者**: Line-fr
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6168

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

Hi, I am the developper of https://codeberg.org/Line-fr/Vship/releases
Since around 6 months, I have seen reports on issues on my repo that did not exist before, with gpu segfault. This was at first specific to some configurations of OS and HW. However, This has now been spreading over every configurations and more specifically windows even. It seems to be related to amd driver updates. Countless errors of that type have been happening on the ROCm repo. I believe Vship is a nice case study here because it is directly written in HIP, no ROCm library call or python intermediate or anything.
Recently I have also seens errors that do not result in crash but the program always return perfect score.

Reasons why I am convinced it's not an issue in vship:
- The vulkan implementation (which is sort of copy pasted from the hip one) works like a charm
- The cuda version which is litteraly a C preprocessed version of the hip code works and pass every cuda memcheck tests/synccheck or anything with success
- It works on machine using relatively older amd drivers versions like my ubuntu 24

This is getting out of hand and I believe in my next release I will actively discourage people from using the HIP version (even though it is faster than the vulkan version). I hope that you will be able to resolve this issue.

### Operating System

Windows & Linux (arch, cachyOS, ...)

### CPU

Any

### GPU

Any, but specifically observed on RX 7900XTX, RX 9070XT for example

### ROCm Version

Observed at first on ROCm 7 but also on ROCm 6.2 (it seems to come from a driver and not ROCm)

### ROCm Component

HIP

### Steps to Reproduce

- Use relatively recent amd drivers (or even eventually a windows)
- install ffvship HIP backend
there is a good chance you'll get issues (running ffvship on 2 different videos may give > 99 SSIMULACRA2 or might segfault and crash the graphical driver)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

This is a following on a previous issue that I posted accompagnied by one of the first case of this, now it happens to so many people I am redoing this issue.

Vship uses relatively simple HIP features, most notably Streams if it matters here.

---

## 评论 (52 条)

### 评论 #1 — schung-amd (2026-04-22T15:45:26Z)

Thanks for the report @Line-fr, happy to look into this and get things working for you and your users. Will try to repro on my end and see how consistent the failures are. Can you link a couple of the user segfault reports?

---

### 评论 #2 — HAL703 (2026-04-22T18:02:45Z)

> Thanks for the report @Line-fr, happy to look into this and get things working for you and your users. Will try to repro on my end and see how consistent the failures are. Can you link a couple of the user segfault reports?

Hi @schung-amd, I am a user of vship and these problems happen to me and are related to ROCm/HIP. This has been happening basically ever since I started using vship. Here is one such report using the latest ROCm 7.2.2 suite: 

`Memory access fault by GPU node-1 (Agent handle: 0x3dea2690) on address 0x7f3838202000. Reason: Page not present or supervisor privilege.
[1]    138053 IOT instruction (core dumped)`

Notably, this problem seems to be quite random. Vship may work for a while or even fully complete, but this error can seemingly occur at _any_ time, causing a segfault. But it also appears to be quite regular at the same time, preventing usage of vship. On all versions of ROCm 7+ this problem exists. I am pretty sure it also exists on the last release of ROCm 6, but beyond that I'm personally unsure.

I am using libvship with `xav` for target quality encoding primarily. To reproduce this issue, I have a 7900XT (the card doesn't seem to really matter here though), and I simply run xav as intended on any video with libvship built with `make build` (the HIP/ROCm version of it).

Output of `rocminfo --support`:

```❯ /opt/rocm/bin/rocminfo --support
ROCk module is loaded
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
  Name:                    AMD Ryzen 9 9950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 9950X 16-Core Processor
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
  Max Clock Freq. (MHz):   5756                               
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
      Size:                    32450852(0x1ef2924) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32450852(0x1ef2924) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32450852(0x1ef2924) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32450852(0x1ef2924) KB             
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
  Uuid:                    GPU-fa75d5f7e663ee22               
  Marketing Name:          AMD Radeon RX 7900 XT              
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
    L3:                      81920(0x14000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2075                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            84                                 
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 632                                
  SDMA engine uCode::      27                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20955136(0x13fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    20955136(0x13fc000) KB             
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
*** Done ***             
```

---

### 评论 #3 — schung-amd (2026-04-22T18:49:45Z)

Having trouble installing this on Ubuntu 24 to test, the available libffms2 does not seem to have a compatible libavutil associated with it.

---

### 评论 #4 — Line-fr (2026-04-22T18:55:31Z)

Only libavutil header is required
Eventually you may just take manually the libavutil header folder and modify the compilation command (it s a single command for ffvship)

---

### 评论 #5 — schung-amd (2026-04-22T19:02:12Z)

Thanks, replaced the header with upstream and it built. Is there a specific workload that exhibits issues more commonly than others?

---

### 评论 #6 — Line-fr (2026-04-22T19:06:51Z)

As there are 2 options
I suggest putting 2 different videos as input that are not too short. If you get a score > 99 then a problem happened
If you get a segfault well the problem is there too

---

### 评论 #7 — HAL703 (2026-04-22T20:39:46Z)

> Thanks, replaced the header with upstream and it built. Is there a specific workload that exhibits issues more commonly than others?

There doesn't appear to be any specific workload that causes it. No matter the video's specifications (resolution, frames per second, etc.), it can happen and does. I've had it happen on 720p five second videos.

---

### 评论 #8 — schung-amd (2026-04-22T20:59:50Z)

Ok, thanks. I've done about 30 runs on two ~200MB video files on ROCm 7.2.1 + 9070 for a while without seeing an issue, but I'll keep trying. Will also try to source some other samples to test with.

---

### 评论 #9 — HAL703 (2026-04-22T21:28:32Z)

> Ok, thanks. I've done about 30 runs on two ~200MB video files on ROCm 7.2.1 + 9070 for a while without seeing an issue, but I'll keep trying. Will also try to source some other samples to test with.

If I can reproduce it again, which I'm sure I can, is there anything I should do either beforehand or after it happens?

I'm opening to debugging if that is an option or anything else. Oh! And I'm using Linux, if that helps.

---

### 评论 #10 — schung-amd (2026-04-23T14:24:00Z)

Ideally I'd like to find a somewhat consistent reproducer. Whenever an issue is seen, if we log info about the video files that caused it and the app being used (i.e. the FFVship executable itself or an app that uses libffvship) we could build a better idea of what might affect this. dmesg output would also help, the error messages when segfaults occur can be a bit generic but might help to match against known issues.

I've sourced more video samples and will be trying to repro with those as well. Let me know if/when you find a consistent reproducer.

---

### 评论 #11 — HAL703 (2026-04-23T16:24:17Z)

> Ideally I'd like to find a somewhat consistent reproducer. Whenever an issue is seen, if we log info about the video files that caused it and the app being used (i.e. the FFVship executable itself or an app that uses libffvship) we could build a better idea of what might affect this. dmesg output would also help, the error messages when segfaults occur can be a bit generic but might help to match against known issues.
> 
> I've sourced more video samples and will be trying to repro with those as well. Let me know if/when you find a consistent reproducer.

I have a free example video right here that reproduces the `Memory access fault by GPU node-1` practically every time. It doesn't happen every time, but out of the four times I have tried, 3 have resulted in a segfault. I simply compared it to two other random free source videos and it results in the error lightning fast. Note that this is true regardless if using FFVShip or libvship with xav. For FFVShip, I used the following command: `FFVship 11264605-hd_1080_1920_60fps.mp4 13885756_3840_2160_60fps.mp4 -m cvvdp`. The second video can be seemingly any other video and it will still happen.

https://github.com/user-attachments/assets/03b8756b-0475-4daa-98e0-d3e61e25eab8 <-- Video in question

I used FFVShip with this video, and here are stats about FFVship: 

<img width="450" height="140" alt="Image" src="https://github.com/user-attachments/assets/e5f2bc93-0cc9-4b4e-b7a3-84269b6b84be" />

Here is an example error message: `Memory access fault by GPU node-1 (Agent handle: 0x5639aee881d0) on address 0x7ff864e02000. Reason: Page not present or supervisor privilege. [1]    606598 IOT instruction (core dumped)`

Here is a screenshot showing this happening in a terminal (**mind you, 33.mp4 is a 720p 30fps video that is 5 seconds long, and the result isn't a pass, rather an error that is likely caused by the same gpu memory access fault and it also results in a segfault according to `dmesg`**—thus it certainly isn't 2160p videos that are the culprit): 

<img width="1006" height="494" alt="Image" src="https://github.com/user-attachments/assets/563ac343-5462-40ee-897d-b14fbb8f66cc" />

This also happens when using `libvship` with `xav`, but since it happens with FFVship and that is more accessible and easier to use to reproduce this issue, I won't bother with it.

Relevant `sudo dmesg` output: 

>  [97028.328892] amdgpu 0000:03:00.0: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 6, simd_id 0, wgp_id 0
> 
> [97028.328897] amdgpu 0000:03:00.0: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 2, simd_id 0, wgp_id 0
> [97028.328899] amdgpu 0000:03:00.0: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 10, simd_id 0, wgp_id 0
> [97028.329096] amdgpu 0000:03:00.0: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:1861)
> [97028.329099] amdgpu 0000:03:00.0:  Process FFVship pid 606975 thread FFVship pid 606975
> [97028.329100] amdgpu 0000:03:00.0:   in page starting at address 0x00007f789ee02000 from client 10
> [97028.329101] amdgpu 0000:03:00.0: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
> [97028.329102] amdgpu 0000:03:00.0:      Faulty UTCL2 client ID: TCP (0x8)
> [97028.329103] amdgpu 0000:03:00.0:      MORE_FAULTS: 0x1
> [97028.329103] amdgpu 0000:03:00.0:      WALKER_ERROR: 0x0
> [97028.329104] amdgpu 0000:03:00.0:      PERMISSION_FAULTS: 0x3
> [97028.329104] amdgpu 0000:03:00.0:      MAPPING_ERROR: 0x0
> [97028.329104] amdgpu 0000:03:00.0:      RW: 0x0
> [97028.329108] amdgpu 0000:03:00.0: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:1861)
> [97028.329108] amdgpu 0000:03:00.0:  Process FFVship pid 606975 thread FFVship pid 606975
> [97028.329109] amdgpu 0000:03:00.0:   in page starting at address 0x00007f789ee02000 from client 10
> [97028.329112] amdgpu 0000:03:00.0: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:1861)
> [97028.329112] amdgpu 0000:03:00.0:  Process FFVship pid 606975 thread FFVship pid 606975
> [97028.329113] amdgpu 0000:03:00.0:   in page starting at address 0x00007f789ee02000 from client 10


---

### 评论 #12 — schung-amd (2026-04-23T20:40:37Z)

Doesn't appear to repro on 9070, I'll rebuild on a 7900 and try there.

---

### 评论 #13 — Line-fr (2026-04-23T20:51:37Z)

It seems to not depends on hw as much as driver versions/rocm versions
I have had a case of someone updating their drivers and suddenly getting it
Typically, I do not have the bug on my ubuntu 24 Lts

---

### 评论 #14 — schung-amd (2026-04-23T21:02:14Z)

Might be related to kernel version then, a major difference between Ubuntu 24 and "exotic" distros is that our mainline support is tied to an older kernel. @HAL703 what distro are you on, what's your kernel version, and do you have the DKMS driver installed?

---

### 评论 #15 — HAL703 (2026-04-23T23:10:23Z)

> Might be related to kernel version then, a major difference between Ubuntu 24 and "exotic" distros is that our mainline support is tied to an older kernel. [@HAL703](https://github.com/HAL703) what distro are you on, what's your kernel version, and do you have the DKMS driver installed?

Distro is EndeavourOS (Arch Linux). Kernel version is linux-cachyos-7.0.0. I am unsure of what you mean by dkms driver (I do not have dkms installed in the `extra` repo, but I have amdgpu, mesa, as well as linux-firmware-amdgpu installed with the most recent versions available. Please note that I have tried linux-lts and regular linux kernel versions in the past and they also did not work (yes, I tried linux 6.12 and that did not work either with the old lts). I do believe it could be related to linux-firmware-amdgpu, as it weirdly worked for a brief window a few months ago before it broke again after installing a new version (or perhaps a new ROCm version). Or perhaps that was a red herring, and I am mis-remembering. If I recall correctly, @Line-fr also had users of 9070 XT experience this bug, too. It's all very confusing. 

---

### 评论 #16 — schung-amd (2026-04-24T14:40:20Z)

If you installed ROCm according to our docs (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html), the amdgpu-dkms driver is installed which can cause issues on newer kernel versions. If you installed through your distro's package manager you probably don't have it (especially since you don't have `dkms` installed in the first place), but you can check with `dkms status`.

Firmware version could be a culprit as well if it's beyond what we're testing extensively for. I'll try to repro on a fresh install of Arch. In the meanwhile, have you or any other Vship users tried TheRock? It's a more agile release channel for ROCm that may have needed fixes.

---

### 评论 #17 — Line-fr (2026-04-24T14:43:55Z)

On the DKMS note, I have indeed encountered issues with ROCm dkms install on my ubuntu. My PC refused to boot completely and I had to chroot from a live ubuntu and remove ROCm SDK completely from my machine to fix it. However I do not believe it to be linked to the issue at hand.

I have not heard previously of TheRock from anyone at all, not in the case of vship in regard to this issue. Is there something you may wish us to try?

---

### 评论 #18 — schung-amd (2026-04-24T16:52:10Z)

https://github.com/ROCm/TheRock is our new, modernized build system; you can try building it or installing a nightly and see if it's more stable than mainline/in-box ROCm, but that is a big time/storage commitment so I'd say the best option is for me to check if it helps once I have a reproducer on my end. There's nothing specific about this issue I know about yet which would indicate TheRock would solve these problems, this is more speculative/curiosity, but if I do see stability improvements with TheRock I'll let you know and you can try it out then. 

---

### 评论 #19 — schung-amd (2026-04-27T21:47:55Z)

Got an arch system to repro on and it does seem to consistently segfault (with TheRock as well, so no need to try that on your end). Thanks for all the info, looking into it now.

---

### 评论 #20 — HAL703 (2026-04-27T21:52:15Z)

Great! Thank you so much. We were losing hope.

---

### 评论 #21 — schung-amd (2026-04-28T17:48:17Z)

Think this might be an issue with the ffms2 package; not seeing any segfaults after building it from source on the Arch reproducer. If users on affected systems could try that and report that would be great. My reproducer system is using TheRock to provide ROCm rather than getting it from AUR, which does involve some extra steps, so it would be ideal if this addresses the issue with in-box ROCm distributions as well.

---

### 评论 #22 — Line-fr (2026-04-28T17:50:23Z)

How would that cause gpu segfaults (or even gpu wrong scores / complete amd driver crash) if that were the case?

---

### 评论 #23 — Line-fr (2026-04-28T17:55:36Z)

Apparently, it can't be the issue. As it also happens with "xav" which can also use libvship C api and does not use ffms2 at all when feeding frames to vship.
So at that point I see 2 options:

- either the bug you observed is not the one we currently observe which would seem to indicate the initial reproducer was not actually reproducing the expected bug
- eventually it would mean the issue is not in therock

---

### 评论 #24 — schung-amd (2026-04-28T18:42:44Z)

Hm, good point. I'll see if I can repro with xav.

---

### 评论 #25 — schung-amd (2026-04-28T21:10:51Z)

I can't repro any issues with xav with TheRock, so either: 

- xav issues are more sporadic and I just haven't seen them yet
- These issues are fixed in TheRock and will be fixed in an upcoming mainline release, with the ffms2 incompatibility being a separate issue that can be worked around with a build from source
- My reproducer system differs from other users in some way, I'm on a fresh install of Arch however so not sure what that would be

Here are the steps I took to get things working with TheRock on Arch, not including most dependencies:

1. Install TheRock via pip wheel (preferably in a venv); see https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-rocm-python-packages
2. Set some environment variables so we can build with the pip wheel ROCm components; see https://github.com/ROCm/TheRock/issues/1658#issuecomment-3359869071
3. Install ffmpeg and ffms2 via pacman
4. Build ffms2 from source, then remove the libffms2 files in /usr/lib and copy the new libffms2 objects (the default ffms2 build writes them to /usr/local/lib)
5. Build Vship library, make install, build the executable

For xav, system clang needs to be used so the environment variables should NOT be set when building; we currently have a known issue where tools are unable to invoke TheRock-packaged clang from the pip wheels. With TheRock I don't see a segfault with xav with or without the libffms2 replacement.

---

### 评论 #26 — HAL703 (2026-04-29T14:24:16Z)

I have a question. Can you give the commands you used with xav?

---

### 评论 #27 — schung-amd (2026-04-29T14:44:07Z)

To repro? I'm just running `xav <input video> <output path>`; I didn't see any instructions indicating passing an option was necessary to enable Vship in xav, is there something I should be setting?

---

### 评论 #28 — HAL703 (2026-04-29T14:50:15Z)

> To repro? I'm just running `xav <input video> <output path>`; I didn't see any instructions indicating passing an option was necessary to enable Vship in xav, is there something I should be setting?

Yes, it means you were not using libvship at all, so it makes sense why you were not able to reproduce. Please try the following, also downloading this cvvdp.json file necessary for encoding with CVVDP (the file is required): 
`xav -e svt-av1 -t 9.44-9.55 -d ~/Videos/cvvdp.json input.mp4 output.mp4` You can put the cvvdp file wherever, just make sure you specify the location. You do not need to worry about the details in the cvvdp.json file, it shouldn't cause problems even if the characteristics are wrong. 

**Also, please make sure you built xav with target quality support when you built it! If not, this won't work.**

[cvvdp.json](https://github.com/user-attachments/files/27206288/cvvdp.json)

---

### 评论 #29 — schung-amd (2026-04-29T15:38:09Z)

Thanks. Is the segfault consistent with xav in your experience?

> Also, please make sure you built xav with target quality support when you built it! If not, this won't work.

I'm selecting the build dynamic with TQ option which says it uses the system Vship library, I assume that is sufficient?

---

### 评论 #30 — HAL703 (2026-04-29T16:05:01Z)

Yes, it is. Sometimes it may go through for whatever reason, but it seems random. It's that GPU memory access bug I almost always get. If xav segfaults with no output or errors, it probably isn't related and might be because your system gets too hot or overloaded.

---

### 评论 #31 — schung-amd (2026-04-29T16:20:30Z)

Ok, not seeing any issues with your cvvdp.json and command with or without the libffms2 replacement on Arch + TheRock nightly. Where did you get ROCm from on your system, the AUR?

---

### 评论 #32 — HAL703 (2026-04-29T16:28:13Z)

The AUR, yes. Do you think ROCm on the AUR isn't very compatible with current kernel versions for this type of work? I guess that couldn't be it because LTS didn't work either when I tried it. Reminder that xav does not rely on ffms2 at all, so you don't have to worry about that, only with FFVship.

Is it possible for you to try this with a non-TheRock ROCm build to see if it reproduces? I think it would be quite clear that the issue would be with the AUR ROCm then. I'm just surprised because I thought that the current version, 7.2.2, would be fine for everything? Does TheRock do something fundamentally different?

---

### 评论 #33 — schung-amd (2026-04-29T16:57:56Z)

Mainly double-checking. I don't expect the AUR-provided ROCm to have much deviation from our official ROCm releases, but we also don't really have control over that.

> Does TheRock do something fundamentally different?

In this context TheRock nightlies are just more current than mainline, so this may have been fixed between releases. There is actually an AUR package that appears to be based off TheRock nightlies: https://aur.archlinux.org/packages/rocm-nightly-gfx120x-all-bin (and associated packages for other hardware). I'm going to see if I can repro your issue with ROCm provided via https://aur.archlinux.org/packages/opencl-amd-dev first, then if so I'll check whether the nightly package works.

---

### 评论 #34 — Line-fr (2026-04-29T17:07:01Z)

As I said at the beginning of the issue, the bug also happens on windows now since about a month. That offers a more stable way to obtain it in.. theory ...

---

### 评论 #35 — schung-amd (2026-04-29T17:40:42Z)

Can indeed repro xav segfaults with ROCm provided via https://aur.archlinux.org/packages/opencl-amd-dev. Testing the nightly package.

---

### 评论 #36 — HAL703 (2026-04-29T17:46:05Z)

Have you tried reproducing using the ROCm suite made in the Extra Arch repo? I currently have that installed along with everything needed for ROCm to function (specifically HIP is probably the problem here since that is what vship uses.) This is what I use and what causes the issue. https://archlinux.org/packages/extra/x86_64/rocm-core/

This is what most users would be using in Arch.

---

### 评论 #37 — schung-amd (2026-04-29T17:51:57Z)

I can try that if you'd like, was mainly interested in seeing if I could repro an xav segfault at all. As mentioned I don't expect much deviation from our official releases so I'd assume these are all kosher.

---

### 评论 #38 — schung-amd (2026-04-29T17:58:17Z)

No segfaults with https://aur.archlinux.org/packages/rocm-nightly-gfx120x-all-bin.

---

### 评论 #39 — ReaNMeTheFool (2026-04-29T18:12:10Z)

Hi, I just saw this and I can constantly reproduce an issue. It's not a segfault, but it's certainly giving wrong scores. When I was on Windows I was getting perfect scores almost every time, even if I gave a completely different video with the same frame count.
Right now I'm on CachyOS:
- Kernel: 7.0.1-1-cachyos
- GPU: RX 7600S
- HIP: 7.2.53211-9999
 when i run `dkms status` it gives 
```
openrazer-driver/3.12.2, 6.18.24-1-cachyos-lts, x86_64: installed
openrazer-driver/3.12.2, 7.0.1-1-cachyos, x86_64: installed
```
and right now when I give the same video to ffvship

<img width="1180" height="367" alt="Image" src="https://github.com/user-attachments/assets/d4dbd8f1-ece4-4995-9344-6ba8a7ac7a17" />
it gives score like this and hip version is wrong **every time** and vulkan version is perfectly fine and As an additional note the HIP version works perfectly fine when I use Ubuntu 24 with Distrobox.

---

### 评论 #40 — schung-amd (2026-04-29T18:14:12Z)

I do see segfaults with https://archlinux.org/packages/extra/any/rocm-ml-sdk/ (which pulls in the rocm-core package and all the ROCm components). So for Arch I'd recommend using the rocm-nightly-gfx*-all-bin packages at the moment (or TheRock via build from source/nightly wheels) to address the xav segfault.

---

### 评论 #41 — schung-amd (2026-04-29T18:20:20Z)

@ReaNMeTheFool How is ROCm acquired on Cachy, is it the same as Arch? If so, please try the rocm-nightly packages based on TheRock. I haven't checked FFVship itself with those packages, but with a nightly TheRock wheel I wasn't seeing those incorrect scores. Also unsure if this is related to the ffms2 incompatibility I saw as that was producing segfaults and not wrong scores.

Will need to test all of this on Windows as well. A lot of our Windows issues involve Windows-specific details so I want to make sure everything is working on the Linux side of things first.

---

### 评论 #42 — ReaNMeTheFool (2026-04-29T18:37:20Z)

@schung-amd I installed ROCm with pacman, same as Arch I think, since CachyOS is Arch-based too. My ROCm version was 7.2.2 and I'm not very experienced, but I don't think this is related to ffms2 since I'm using the same ffms2 on Distrobox too.
I've also had a lot of driver issues with my GPU on both Windows and Linux.
On my end, Windows has the perfect score problem and Linux has the absurdly wrong score problem — they are completely different and I don't know why.

And i will test with rocm-nightly too

---

### 评论 #43 — schung-amd (2026-04-30T17:54:09Z)

@Line-fr What are the Windows issues seen, also segfaults? I'm not seeing any segfaults myself running FFVShip and the results look correct (consistent and the trivial test passing the same file twice scores ~100), although the driver is reporting a timeout after it finishes running.

e: After further testing the timeout is a fault and not happening on termination, there's just a delay between when it happens and the software reporting. Looking into it.

---

### 评论 #44 — ReaNMeTheFool (2026-04-30T18:25:17Z)

@schung-amd when i was on windows i was getting perfect score for everything. i encoded a video with h264_amf qp 51 and video was like a pixel art and ssimulacra2 gave 97 score 

<img width="1915" height="1002" alt="Image" src="https://github.com/user-attachments/assets/63577303-e6a0-4b4f-8aab-f40fa5c8e61b" />

---

### 评论 #45 — Line-fr (2026-04-30T18:40:50Z)

The issue seems to manifest differently depending on the machine it seems (may it be sw or hw)
I do not have it myself as I do not possess a potent amd gpu

---

### 评论 #46 — schung-amd (2026-04-30T19:23:02Z)

I can at least look into the issue I'm seeing on my repro system for now then, although as mentioned it doesn't seem to be affecting scores. May also be related to GPU support on Windows as it is not as extensive as on Linux. Might also be tied to the driver, as the Adrenalin software ships its own HIP dlls which are prioritized by Windows since they live in system32.

---

### 评论 #47 — schung-amd (2026-04-30T19:46:02Z)

Looks like it's just the drivers shipped with Adrenalin. I copied amdhip64_7.dll and amd_comgr0713.dll from ROCm 7.13 via TheRock nightlies into the Vship folder to preempt the system32 dll search and it runs without issue. This also required setting other environment variables (i.e. those in https://github.com/ROCm/TheRock/issues/1658#issuecomment-3359869071) to utilize the ROCm components from the nightly. Unfortunately adding the ROCm files to PATH does not provide the dlls due to the Windows dll search order.

e: My assumption is that the dlls living in system32 are from Adrenalin, however they could be leftover from a previous HIP SDK installation as well. In any case they would be outdated compared to the nightlies.

---

### 评论 #48 — schung-amd (2026-04-30T19:56:06Z)

@ReaNMeTheFool Let me know when you've had a chance to try ROCm via TheRock nightlies, either through the AUR packages or via pip wheel. I think we can close this on our end as it will work in the future and there are workarounds available for now, assuming the scores on Cachy are good.

---

### 评论 #49 — ReaNMeTheFool (2026-05-01T09:42:43Z)

@schung-amd i tried "rocm-nightly-gfx110x-bin" from aur since  i have rx 7600s (gfx1102) and it didnt fix plus it started crashing my gpu randomly like middle of test my second monitors half became random colored pixels and my some workspaces became random colored pixels too the one i was testing ffvship too when i opened a new workspace but it was becaming random colored pixels when i opened terminal or do anything so i uninstalled nightly 

---

### 评论 #50 — schung-amd (2026-05-01T14:58:32Z)

Ok, thanks for trying. I'll have to set up a Cachy system to test when I get time.

---

### 评论 #51 — ReaNMeTheFool (2026-05-15T19:07:37Z)

@schung-amd Hi, I found out that replacing` hipMallocAsync` and `hipFreeAsync` with `hipMalloc` and `hipFree` fixes my -2m average score problem, but it's slowing down compute speed.

---

### 评论 #52 — schung-amd (2026-05-15T19:24:46Z)

Thanks for the update. I still haven't had the time/resources to set up a Cachy system but will hopefully get a chance next week. 

aync memory management being the issue smells like improper barrier synchronization to me, which could indicate a driver or firmware issue. Can you try running some other code that uses `hipMallocAsync` and `hipFreeAsync` on your system to see if we can isolate the issue to those? You can write your own, or https://github.com/ROCm/rocm-examples should have some examples.

---
