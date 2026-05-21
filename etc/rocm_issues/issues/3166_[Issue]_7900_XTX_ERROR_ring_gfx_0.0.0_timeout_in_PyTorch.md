# [Issue]: 7900 XTX *ERROR* ring gfx_0.0.0 timeout in PyTorch

> **Issue #3166**
> **状态**: closed
> **创建时间**: 2024-05-28T04:12:14Z
> **更新时间**: 2024-07-04T13:34:20Z
> **关闭时间**: 2024-07-04T13:34:20Z
> **作者**: madness742
> **标签**: Under Investigation, ROCm 5.7.1, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3166

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

### Brief summary:
When generating a picture in [A1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui), [ComfyUI](https://github.com/comfyanonymous/ComfyUI) or [SD.Next](https://github.com/vladmandic/automatic). The whole computer will freeze. If I switch to a different TTY at the same time it freezes, I'm able to see that the GPU has timed out. If I do not switch to a different TTY the system becomes non responsive to all my inputs. This requires me to hit the reset button on the case.

Version 6.1 crashes near instantaneous, but `clinfo` doesn't cause my second monitor to crash.
Version 5.7.3 has a workaround (see at the bottom), but `clinfo` crashes my second monitor on KDE with a message `KWin has restarted`.

Running Blender with either ROCm versions seems to be fine on this machine. It seems to only affect PyTorch.

### Systems affected by it:
Systems running under Podman container:
- Fedora 40
- Arch Linux
- Ubuntu 22.04

Systems without a container:
- OpenSUSE Tumbleweed (Kernel: 6.9.1-1) <-- this system was running the containers.
- Ubuntu 22.04.4 LTS (ROCm 6.1.1 with PyTorch 6.1) <-- clean install to isolate the issue.

### Versions affected by it:
I have tested version[ 6.1.1](https://repo.radeon.com/amdgpu-install/6.1.1/ubuntu/jammy/amdgpu-install_6.1.60101-1_all.deb).
I have tested version [5.7.3](https://repo.radeon.com/amdgpu-install/5.7.3/ubuntu/jammy/amdgpu-install_5.7.50703-1_all.deb).

### Workarounds:
- Connecting *all* monitors to the motherboard video output so that nothing else gets rendered on the dedicated gpu (7900 XTX). This prevents my PC from getting frozen down, but it will still hang my gpu from time to time. This only requires me to restart stable diffusion from the terminal.
- With version 5.7.3 if I only have Firefox with a tab showing me the page of Stable Diffusion, and a terminal in the background, I can run it with much less crashes. Once I start opening up more tabs and specifically going to discord.com/app, the pc will freeze once again.


![error_output](https://github.com/ROCm/ROCm/assets/170082508/9e2dd8d3-8d8f-4207-86a2-37dd6552b186)

### Operating System

22.04.4 LTS (Jammy Jellyfish) [Podman Container]

### CPU

AMD Ryzen 9 7950X3D 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0, ROCm 5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

1. `git clone https://github.com/vladmandic/automatic`
2.  `cd automatic`
3.  `python3.11 -m venv venv`
4.  `source venv/bin/activate`
5.  `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1`
6. `./webui.sh --debug`
7. Copy [Pony V6 SDXL Model](https://civitai.com/api/download/models/290640?type=Model&format=SafeTensor&size=pruned&fp=fp16) to `/models/Stable-diffusion/`.
8. Copy [Pony S6 SDXL VAE](https://civitai.com/api/download/models/290640?type=VAE&format=SafeTensor) to `/models/VAE/`. 
9. Refresh and select new model in the webui.
10. Set resolution to `1024x1024` and generate a picture.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```HSA System Attributes    
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
      Size:                    64992428(0x3dfb4ac) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    64992428(0x3dfb4ac) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    64992428(0x3dfb4ac) KB             
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
  Uuid:                    GPU-[censored]               
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
  Packet Processor uCode:: 102                                
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
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   4864                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 21                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    524288(0x80000) KB                 
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
*** Done ***             ```

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2024-06-26T15:45:33Z)

@madness742 Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — madness742 (2024-06-26T17:05:55Z)

Hi @ppanchad-amd! I'd like to add that, in addition to the configuration I mentioned in my steps to reproduce section, enabling a upscaler (RealESGRAN 4x+ Anime6B) (Rescale by 1.5 - 2, depending on available VRAM) **combined** with Force HiRes (20 steps) enabled will cause a system freeze much more frequently. These options can be found under "Refine". 

![image](https://github.com/ROCm/ROCm/assets/170082508/55030e3f-d005-4425-9f84-27cfd2febcff)

I have updated `kernel-firmware-amdgpu` after reading a [comment by Alex Deucher ](https://gitlab.freedesktop.org/drm/amd/-/issues/3220#note_2463104). Currently on `Version: 20240618-1.1`. I have also updated to ROCm 6.1.3, but even when following the suggestion of trying to keep some VRAM available the freezes will occur.

Much less often, but they still occur nonetheless. It even occurred once after waking up the system after it successfully generated a batch (count) of 100 images and went into sleep mode. 

I hope this additional information can be of use during the investigation! 

---

### 评论 #3 — jamesxu2 (2024-06-28T14:55:22Z)

Hello @madness742 , thanks for expanding on your configuration. I used your original issue to attempt to reproduce https://github.com/ROCm/ROCm/issues/2935 and have retried it by enabling the Upscaler + Force HiRes option, using SD.Next.

I do notice frequent out-of-memory errors and am running the automatic SD.Next webui with the --lowvram option as a result. With your configuration, I generated 100+ images continuously over a course of several hours and didn't encounter your crash. 

System Configuration:
- RX7900XT
- Ubuntu 22.04
- Both Torch2.5.0+rocm6.1 and Torch 2.3.1+rocm5.7 

I have some follow-ups:
1. Assuming this issue may be VRAM related, have you tried running with the --lowvram option?
2. What's the approximate frequency that crashes occur on your machine? How many images with the upscaler + ForceHiRes option are generated before encountering a crash?

---

### 评论 #4 — madness742 (2024-07-01T08:04:19Z)

Hi @jamesxu2, I've been extensively using SD.Next since your message.

1. I tried lowering the VRAM usage by setting different generation parameters. It was on average using 72% of the total VRAM during a 100 batch count generation. Even tried generating 10 pictures (1024x1024) at the same time using the batch ***size*** option. Haven't encountered a crash/freeze so far on this configuration after updating SD.Next and the host system (openSUSE Tumbleweed). Currently on [snapshot 20240629](https://lists.opensuse.org/archives/list/factory@lists.opensuse.org/message/22XKK7N3J5QPF2OVXAOXFQBOAMYQLGP3/). 
2. With the mentioned configuration (1024x1024, Forced HiRes, Upscaler) it would either crash instantly upon hitting generate, or within 10 minutes. I was generating one picture at a time. It's very random to when it crashes the whole system.

The GPU stats during the 100 batch count generation:
![image](https://github.com/ROCm/ROCm/assets/170082508/11508412-51b8-48cb-afc5-269351ddf1f1)

The logs after the systems runs out of VRAM and hard freezes:
```bash
Jul 01 07:23:51 localhost.localdomain kwin_wayland[127968]: kwin_core: Cannot grant a token to KWin::ClientConnection(0x5618130c52a0)
Jul 01 07:24:35 localhost.localdomain kwin_wayland[127968]: kwin_libinput: Libinput: event2  - Compx Pulsar Xlite Wireless: client bug: event processing lagging behind by 30ms, your system is too slow
Jul 01 07:24:40 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:24:40 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:24:40 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:24:46 localhost.localdomain kwin_wayland[127968]: kwin_wayland_drm: Page flip failed: Cannot allocate memory
Jul 01 07:24:46 localhost.localdomain kernel: amdgpu 0000:03:00.0: amdgpu: 00000000591fde63 pin failed
Jul 01 07:24:46 localhost.localdomain kernel: [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
Jul 01 07:24:46 localhost.localdomain kwin_wayland[127968]: kwin_wayland_drm: Presentation failed! Cannot allocate memory
Jul 01 07:24:48 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:24:48 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:24:48 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:08 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
Jul 01 07:25:59 localhost.localdomain kwin_wayland[127968]: kwin_wayland_drm: Page flip failed: Cannot allocate memory
Jul 01 07:25:59 localhost.localdomain kwin_wayland[127968]: kwin_wayland_drm: Presentation failed! Cannot allocate memory
Jul 01 07:25:59 localhost.localdomain kernel: amdgpu 0000:03:00.0: amdgpu: 00000000591fde63 pin failed
Jul 01 07:25:59 localhost.localdomain kernel: [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
Jul 01 07:25:59 localhost.localdomain kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
```

Last week SD.Next received a fix for [memory exceptions on ROCm](https://github.com/vladmandic/automatic/blob/master/CHANGELOG.md#fixes). I have updated to that version a couple days ago, and it has made a big difference. Other changes I've made was to set the GPU power profile to `COMPUTE` (from `BOOTUP_DEFAULT`) and raise the power limit to `402000000` (from `339000000`). I've also changed the vBios on the GPU to overclock mode by pushing a physical switch on my GPU.

I have not tested if these changes above also help on Ubuntu 22.04 when installed as a host. I also haven't tested A111/ComfyUI.

Host configuration:
- openSUSE Tumbleweed
- Kernel: 6.9.7-1-default
- AMD Sapphire 7900 XTX Nitro+

Container configuration: 
- Ubuntu 22.04
- Python: 3.11.9  
- Torch 2.5.0.dev20240621
- ROCm 6.1 (6.1.60103-1)
- SD.Next (2024-06-24)

It hasn't crashed once since I made all those changes in combination of not exceeding 16-17gb of VRAM usage. In the past it would still randomly crash despite the relatively moderate VRAM usage.


```bash
cat /sys/class/drm/card1/device/pp_power_profile_mode 
PROFILE_INDEX(NAME) CLOCK_TYPE(NAME) FPS MinActiveFreqType MinActiveFreq BoosterFreqType BoosterFreq PD_Data_limit_c PD_Data_error_coeff PD_Data_error_rate_coeff
 0 BOOTUP_DEFAULT :
                    0(       GFXCLK)       0       1       0       4     800 4587520  -65536       0
                    1(         FCLK)       0       3       0       1       0 3276800  -65536   -6553
 1 3D_FULL_SCREEN :
                    0(       GFXCLK)       0       0    1200       4     650 3932160   -3276  -65536
                    1(         FCLK)       0       3       0       3       0 1310720   -6553   -6553
 2   POWER_SAVING :
                    0(       GFXCLK)       0       1       0       3       0 5898240  -65536       0
                    1(         FCLK)       0       1       0       1       0 3407872  -65536   -6553
 3          VIDEO :
                    0(       GFXCLK)       0       1       0       4     500 4587520  -65536       0
                    1(         FCLK)       0       3       0       3       0 3473408  -65536   -6553
 4             VR :
                    0(       GFXCLK)       0       2    1000       1       0 3276800       0       0
                    1(         FCLK)       0       3       0       3       0 1310720   -6553   -6553
 5        COMPUTE*:
                    0(       GFXCLK)       0       2    1000       1       0 3932160       0       0
                    1(         FCLK)       0       3       0       3       0 1310720   -6553   -6553
 6         CUSTOM :
                    0(       GFXCLK)       0       0    1200       4       0  655360   -3276  -65536
                    1(         FCLK)       0       3       0       3       0 1310720   -6553   -6553
 7      WINDOW_3D :
                    0(       GFXCLK)       0       0    1200       4     650 5242880   -3276  -65536
                    1(         FCLK)       0       3       0       3       0 1310720   -6553   -6553
```


---

### 评论 #5 — jamesxu2 (2024-07-03T20:48:58Z)

@madness742  I'm glad to hear those changes have mitigated your crashes. Given that you aren't seeing any more crashes in your current configuration, can this issue be closed? 

---

### 评论 #6 — madness742 (2024-07-04T13:34:20Z)

Hi @jamesxu2, i'll go ahead and close this issue. 

ComfyUI is working fine as well (generated 300 pics) after the power plan and power limit adjustment, as long as it doesn't spike my VRAM which causes me to get OOM and freeze. I was unable to test A1111 as it required much more VRAM than the other two and I had trouble loading a SDXL model at the recommended 1024x1024 resolutions.

Interestingly setting it to `COMPUTE` also solves [this issue](https://gitlab.freedesktop.org/drm/amd/-/issues/1500) in a specific game when it comes to VRR on a dual monitor setup. Probably not related, but might be worth mentioning.

---
