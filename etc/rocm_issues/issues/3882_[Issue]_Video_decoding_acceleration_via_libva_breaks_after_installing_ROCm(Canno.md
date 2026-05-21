# [Issue]: Video decoding acceleration via libva breaks after installing ROCm(Cannot find target for triple amdgcn-- Unable to find target for this triple (no targets are registered))

> **Issue #3882**
> **状态**: closed
> **创建时间**: 2024-10-10T09:52:43Z
> **更新时间**: 2024-10-15T14:30:47Z
> **关闭时间**: 2024-10-11T14:30:53Z
> **作者**: brlin-tw
> **标签**: Under Investigation, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3882

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

**NOTE:** The GPU field of this form was originally wrongly selected as no applicable model is enumerated.

After installing rocm 6.2.2 I can no longer play local video files using VA-API decoding acceleration.

The application crashed shortly after launching:

```
$ gst-play-1.0 --videosink vaapidecodebin /path/to/video.mp4
Press 'k' to see a list of keyboard shortcuts.
Now playing /home/brlin/??/Animation_ New recruit learns military customs from his sergeant ? Saka(23_sakapicdora_ENG).mp4
Redistribute latency...
Redistribute latency...
ac: Unknown GPU, using 0 for raster_config
Cannot find target for triple amdgcn-- Unable to find target for this triple (no targets are registered)
Segmentation fault (core dumped)
```

### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen 7 7840U w/ Radeon  780M Graphics

### GPU

Radeon  780M Graphics

```
c1:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Phoenix1 (rev c4)
```

### ROCm Version

ROCm 6.2.0

### ROCm Component

ROCm

### Steps to Reproduce

1. Install ROCm via the [Quick start installation guide — ROCm installation (Linux)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html).
2. Play any video which decoding is hardware-accelerable using libva:

    ```bash
    totem /path/to/video.mp4
    ```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.8.5 is loaded
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
  Name:                    AMD Ryzen 7 7840U w/ Radeon  780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7840U w/ Radeon  780M Graphics
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
  Max Clock Freq. (MHz):   5132                               
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
      Size:                    61515984(0x3aaa8d0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    61515984(0x3aaa8d0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    61515984(0x3aaa8d0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1103                            
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
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           7(0x7)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   49408                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 39                                 
  SDMA engine uCode::      18                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    30757992(0x1d55468) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    30757992(0x1d55468) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1103         
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

System: Framework Laptop 13(AMD 7040 series)

---

## 评论 (11 条)

### 评论 #1 — brlin-tw (2024-10-10T10:17:14Z)

Please help remove the invalid [AMD Instinct MI300X](https://github.com/ROCm/ROCm/labels/AMD%20Instinct%20MI300X) tag, thanks!

---

### 评论 #2 — frzb (2024-10-11T08:42:44Z)

## Similar situation here

Similar situation here, Framework laptop, gfx1103, similar software setup.
Applications that need  VA-API or VDPAU support abort during start with the mentioned error message.

## Work-around for me

```
$ LIBVA_DRIVER_NAME="vdpau" <application>
```
or 

```
$ LIBVA_DRIVER_NAME="vaapi" <application>
```
Looks like a detection error of existing video hardware acceleration. 
I guess a system-wide export of this variable could work as well, but unclear if there are some side effects.

---

### 评论 #3 — brlin-tw (2024-10-11T08:45:24Z)

@harkgill-amd

After re-installing ROCm I can no longer reproduce this issue, I would say that the workaround you enumerated doesn't work IIRC, though.

---

### 评论 #4 — harkgill-amd (2024-10-11T13:24:02Z)

Was there any difference in your installation? We were not able to reproduce this issue either after adding the graphics use case to our installation i.e
```
sudo amdgpu-install --usecase=graphics,rocm
```
Adding this use case is recommended for graphical workloads such as hardware video acceleration. @frzb and @brlin-tw, could you please give this a try and let me know if it resolves your issue?

---

### 评论 #5 — brlin-tw (2024-10-11T13:36:30Z)

> Was there any difference in your installation? We were not able to reproduce this issue either after adding the graphics use case to our installation i.e
> ```
> sudo amdgpu-install --usecase=graphics,rocm
> ```
> Adding this use case is recommended for graphical workloads such as hardware video acceleration. @frzb and @brlin-tw, could you please give this a try and let me know if it resolves your issue?

I believe I was using the package installation(e.g. by following the quickstart guide) when I reproduced the issue.

The second installation attempt I'm using the exact command you mentioned and it worked.


---

### 评论 #6 — harkgill-amd (2024-10-11T14:30:53Z)

I'm glad to hear that it's now working on your side!

---

### 评论 #7 — frzb (2024-10-11T19:22:59Z)

@harkgill-amd  Thanks a lot for your hints!

Using `sudo amdgpu-install --usecase=graphics` which reflects to  ` sudo apt install amdgpu-lib amdgpu-lib32`  made hardware video acceleration for the application work again without  setting `LIBVA_DRIVER_NAME=...` manually. 

Case closed for me. :smiley: 

Only  left-over remark from my side is that the official _Quick start installation guide_ for ROCm should not break `libva` hardware acceleration in the first place, or I am wrong? :wink:  

---

### 评论 #8 — schung-amd (2024-10-11T21:04:36Z)

Technically these releases are meant for headless configurations, which is why the quick start guide can cause some issues with graphical applications when physical displays are involved. We also have official ROCm on Radeon releases (such as 6.1.3) which are specifically intended for and tested on such configurations, as pointed out above the quick start instructions:

> If you’re using ROCm with AMD Radeon or Radeon Pro GPUs for graphics workloads, see the [Use ROCm on Radeon GPU](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html) documentation for installation instructions .

That being said, the regular releases with graphics usecase tend to work on these systems as well, so you shouldn't need to downgrade to the Radeon-specific version unless you run into further issues. Thanks for your input!

---

### 评论 #9 — frzb (2024-10-12T01:51:36Z)

> Technically these releases are meant for headless configurations, which is why the quick start guide can cause some issues with graphical applications when physical displays are involved. We also have official ROCm on Radeon releases (such as 6.1.3) which are specifically intended for and tested on such configurations, as pointed out above the quick start instructions:

@schung-amd Oh yes, I see!  RTFM :+1: 
Would a simple heuristic guess checking  in `amdgpu-install` if `$XDG_SESSION_TYPE` contains a value and if so picking or recommending  `--usecase=graphics` make sense to improve the UX?

**Reasoning behind this**
I thought about **why** I missed this documentation from a UX perspective.
And I think it is caused by the misalignment between AMD product brand naming and the technical naming. Radeon™ is used as brand name but abandoned as software name on a technical level in Linux since some time. In my perception `radeon` was  percepted as this legacy software. This is confusing and misleading.



---

### 评论 #10 — schung-amd (2024-10-15T14:19:51Z)

> Would a simple heuristic guess checking in amdgpu-install if $XDG_SESSION_TYPE contains a value and if so picking or recommending --usecase=graphics make sense to improve the UX?

Thanks for your feedback! Ultimately, I think the issue lies in a lack of visibility and clarity about when the graphics usecase (or equivalently the ROCm on Radeon release) is required. While the graphics usecase is required for some graphical workloads with a physical display attached, ROCm still functions in most other cases with a physical display even without the graphics usecase, so it would be helpful if we could be more specific about when `--usecase=graphics` is warranted (versus, say, the multimedia usecase, or no additional usecases).

> And I think it is caused by the misalignment between AMD product brand naming and the technical naming. Radeon™ is used as brand name but abandoned as software name on a technical level in Linux since some time. In my perception radeon was percepted as this legacy software. This is confusing and misleading.

This is interesting, and I'll bring this up to the internal team. We're working on improving the installation methods and documentation, so your feedback is greatly appreciated. 

---

### 评论 #11 — brlin-tw (2024-10-15T14:30:45Z)

IMHO the quick start guide should simply instruct the user to use the `amdgpu-install` script instead of:

```
sudo apt install amdgpu-dkms rocm
```

As the script is essentially a wrapper of package installation there's little reason to instruct the users to run the package installation command.

---
