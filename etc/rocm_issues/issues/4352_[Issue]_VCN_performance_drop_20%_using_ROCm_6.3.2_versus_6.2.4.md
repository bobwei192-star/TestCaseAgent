# [Issue]: VCN performance drop 20% using ROCm 6.3.2 versus 6.2.4

> **Issue #4352**
> **状态**: closed
> **创建时间**: 2025-02-06T20:57:35Z
> **更新时间**: 2025-03-11T20:56:10Z
> **关闭时间**: 2025-03-11T20:56:10Z
> **作者**: Geoknysis
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4352

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

Handbrake encode of DVD ISO using AMD VCN (h.264) drops 20% when using ROCm 6.3.2 versus using 6.2.4. In particular:

ROCm 6.2.4
`sudo apt install '/home/<user>/Downloads/amdgpu-install_6.2.60204-1_all.deb' && sudo apt update && sudo amdgpu-install -y --usecase=dkms,workstation,hiplibsdk,rocm,amf --vulkan=pro`

encode start: 16:13:42
encode end: 16:16:13
total encode time: 00:02:31
encode fps avg: 1067.38671
encode bitrate: 2448.87 kbps
[Activity.log.\[ROCm624\].txt](https://github.com/user-attachments/files/18697765/Activity.log.ROCm624.txt)

ROCm 6.3.2
`sudo apt install '/home/<user>/Downloads/amdgpu-install_6.3.60302-1_all.deb' && sudo apt update && sudo amdgpu-install -y --usecase=dkms,workstation,hiplibsdk,rocm,amf --vulkan=pro`

encode start: 16:24:35
encode end: 16:27:37
total encode time: 00:03:02
encode fps avg: 882.762451
encode bitrate: 2448.87 kbps
[Activity.log.\[ROCm632\].txt](https://github.com/user-attachments/files/18697764/Activity.log.ROCm632.txt)

Note: `amdgpu-install` usecase `graphics` or `workstation` have no impact on performance degradation. 
Note: `sudo nano /etc/apt/sources.list.d/amdgpu-proprietary.list` is required to enable proprietary repo access.

### Operating System
Ubuntu 24.04.1
Kernel 6.8.0-060800.202403131158

### CPU
7800X 3D

### GPU
7900XTX

### ROCm Version
ROCm 6.2.4 and ROCm 6.3.2

### ROCm Component
_No response_

### Steps to Reproduce

`git clone https://github.com/HandBrake/HandBrake.git && cd Handbrake && ./configure --launch-jobs=$(nproc) --launch --enable-vice && sudo make --directory=build install`

`sudo apt install '/home/<user>/Downloads/amdgpu-install_6.2.60204-1_all.deb' && sudo apt update && sudo amdgpu-install -y --usecase=dkms,workstation,hiplibsdk,rocm,amf --vulkan=pro`
Encode performance was ~1,050fps.

`sudo apt install '/home/<user>/Downloads/amdgpu-install_6.3.60302-1_all.deb' && sudo apt update && sudo amdgpu-install -y --usecase=dkms,workstation,hiplibsdk,rocm,amf --vulkan=pro`
Encode performance was ~850fps.

Note: `amdgpu-install` usecase `graphics` or `workstation` have no impact on performance degradation. 
Note: `sudo nano /etc/apt/sources.list.d/amdgpu-proprietary.list` is required to enable proprietary repo access.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

//////////////////////////////////////////////////////////////
//////////////////////// ROCm 6.2.4 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\ [see below for ROCm 6.3.2 output] \\\\\\\\\\\\\\\\
///////////////////////////////////////////////////////////////

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
  Name:                    AMD Ryzen 7 7800X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7800X3D 8-Core Processor
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
  Max Clock Freq. (MHz):   5050                               
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
      Size:                    65485188(0x3e73984) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65485188(0x3e73984) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65485188(0x3e73984) KB             
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
  Uuid:                    GPU-f33e7ed1f4d234a7               
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
  Max Clock Freq. (MHz):   2371                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 342                                
  SDMA engine uCode::      21                                 
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

//////////////////////////////////////////////////////////////
//////////////////////// ROCm 6.3.2 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

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
  Name:                    AMD Ryzen 7 7800X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7800X3D 8-Core Processor
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
  Max Clock Freq. (MHz):   5050                               
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
      Size:                    65485188(0x3e73984) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65485188(0x3e73984) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65485188(0x3e73984) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65485188(0x3e73984) KB             
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
  Uuid:                    GPU-f33e7ed1f4d234a7               
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
  Max Clock Freq. (MHz):   2371                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 412                                
  SDMA engine uCode::      24                                 
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

## 评论 (6 条)

### 评论 #1 — Geoknysis (2025-02-07T04:27:08Z)

It would be important to note that Handbrake doesn't support AMD hardware decoding using an AMD GPU. It only supports hardware encoding with an AMD GPU. Since the encode bitrate in the Handbrake logs are identical between the two ROCm versions, it would appear that the encode aspect (hardware GPU) is functioning well, leaving the CPU decode function as a potential culprit for performance degredation. 

Looking at the `ROCm info` logs, I note a difference in `Agent 1` pools. In particular, it appears ROCm 6
2.4 `Pool 3 Segment: GLOBAL; FLAGS: COARSE GRAINED` has been changed in ROCm 6
3.2 to `Pool 3 Segment: GLOBAL; FLAGS: KERNARG, FINE GRAINED`. However, under ROCm 6.3.2, the characteristics of Pool 4 are identical to ROCm 6.2.4 Pool 3.

---

### 评论 #2 — harkgill-amd (2025-02-07T18:48:01Z)

Hi @Geoknysis, an internal ticket has been created to further investigate this issue. 

---

### 评论 #3 — sohaibnd (2025-03-04T21:11:52Z)

Hi @Geoknysis, sorry for the delay. Can you please provide steps to reproduce this after installing Handbrake? 

> It would be important to note that Handbrake doesn't support AMD hardware decoding using an AMD GPU. It only supports hardware encoding with an AMD GPU. Since the encode bitrate in the Handbrake logs are identical between the two ROCm versions, it would appear that the encode aspect (hardware GPU) is functioning well, leaving the CPU decode function as a potential culprit for performance degredation.

Are you sure it's a decoding issue? The logs seem to point to encoding taking longer, correct me if I'm wrong.

![Image](https://github.com/user-attachments/assets/a327344e-3929-4fe1-b06e-5d98ff751ba0)

Also, if the performance degradation does lie in the decoding and that is happening on the CPU, that would mean the problem isn't related to ROCm or AMD GPUs.



---

### 评论 #4 — Geoknysis (2025-03-05T14:41:09Z)

Hi @sohaibnd, thanks for taking the time to investigate! 

I first brought to the attention of HandBrake devs [here](https://github.com/HandBrake/HandBrake/issues/6610). The [recommendation](https://github.com/HandBrake/HandBrake/issues/6610#issuecomment-2638026760) was that since the encode bitrate (see picture below) was identical between the two instances of ROCm, that it was potentially something AMD changed or potentially a bug in HandBrake.
![Image](https://github.com/user-attachments/assets/200c63c2-1995-4539-b3bb-d214bc296f11)

To reproduce the issue, please follow these steps:

1. Install ROCm 6.2.4: `sudo apt install '/home/<user>/Downloads/amdgpu-install_6.2.60204-1_all.deb' && sudo apt update && sudo amdgpu-install -y --usecase=dkms,workstation,hiplibsdk,rocm,amf --vulkan=pro`
2. [Build Handbrake from source](https://handbrake.fr/docs/en/1.9.0/developer/build-linux.html) with [VCE enabled](https://handbrake.fr/docs/en/1.9.0/technical/video-vcn.html): `git clone https://github.com/HandBrake/HandBrake.git && cd Handbrake && ./configure --launch-jobs=$(nproc) --launch --enable-vce && sudo make --directory=build install`
3. Open HandBrake.
4. Load a DVD iso file by dragging it onto the HandBrake window. If no DVD iso is available, try any video file.
5. Navigate to the `Video` tab.
6. Select the `H.264 VCN Hardware Preset` from the profiles menu.
7. Begin the encode.
8. Upon encode completion, encode logs are available in `~/.config/ghb`
9. Purge ROCm 6.2.4: `amdgpu-uninstall && sudo apt purge amdgpu-install && sudo apt update && sudo apt autoremove`
10. Install ROCm 6.3.2: `sudo apt install '/home/<user>/Downloads/amdgpu-install_6.3.60302-1_all.deb' && sudo apt update && sudo amdgpu-install -y --usecase=dkms,workstation,hiplibsdk,rocm,amf --vulkan=pro`
11. Open HandBrake.
12. Load a DVD iso file by dragging it onto the HandBrake window. If no DVD iso is available, try any video file.
13. Navigate to the `Video` tab.
14. Select the `H.264 VCN Hardware Preset` from the profiles menu.
15. Begin the encode.
16. Upon encode completion, encode logs are available in `~/.config/ghb`

If you find that this is not a ROCm related issue, could you please help direct me in the right direction as to which team I should reach to for further investigation? Thanks!

---

### 评论 #5 — sohaibnd (2025-03-11T16:17:51Z)

@Geoknysis Thanks for providing the steps to reproduce. I did not find a `H.264 VCN Hardware Preset`, only `H.265 VCN 2160P 4K` and `H.265 VCN 1080p` under Presets->Hardware. Based on your logs, it looks like you're using a custom preset. Anyways, I tried to run a custom preset to use the H.264 AMD VCE encoder and got similar results between ROCm 6.2.4 and ROCm 6.3.2 (logs attached).

[rocm-6.2.4-H264 Encoding-Horizon.txt](https://github.com/user-attachments/files/19191809/rocm-6.2.4-H264.Encoding-Horizon.txt)
[rocm-6.3.2-H264 Encoding-Horizon.txt](https://github.com/user-attachments/files/19191808/rocm-6.3.2-H264.Encoding-Horizon.txt)

---

### 评论 #6 — Geoknysis (2025-03-11T20:56:06Z)

Thanks for verifying. I'll investigate further on my end. 

---
