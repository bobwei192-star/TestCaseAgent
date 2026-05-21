# [Issue]: ROCm runtime crashes after system suspension

> **Issue #4548**
> **状态**: closed
> **创建时间**: 2025-03-31T22:44:35Z
> **更新时间**: 2026-02-21T19:19:54Z
> **关闭时间**: 2025-06-06T16:24:24Z
> **作者**: Equiel-1703
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4548

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Hey everyone!

Recently, I created a simple Mandelbrot fractal generator using GPU kernels. The generator was originally written in CUDA C and then converted to HIP code using the `hipify-clang` tool. After that, I compiled the final binary with `hipcc`, and everything worked fine. The program runs as expected and is highly efficient!

The problem occurs when I suspend my computer. When I first run the program after booting the system, everything works perfectly. However, if I suspend the machine, wake it up, and then try to run the program again, the system crashes. The process becomes unresponsive, and if I attempt to abort it using Ctrl + C, my machine completely freezes, forcing me to force shut down. I recorded a video demonstrating exactly this (please forgive my terrible English—I'm still working on it 😅): [VIDEO](https://youtu.be/MRfmHzUqkGY).

I remember that when I first installed ROCm, my machine already struggled with system suspension. After waking up, the screen would flash frantically. The "solution" to this was changing my battery mode from "Balanced" to "Performance" ([here](https://www.reddit.com/r/Fedora/comments/1hk5wmi/fedora_41_screen_blinks_and_turns_off_when_waking/) is the post I read about this "fix"). After switching to Performance mode, the flashing screen issue disappeared, but now the screen brightness is set to maximum every time the computer wakes up from suspension, and the ROCm runtime breaks as described above. Perhaps this is a driver issue?

Thanks in advance for any help!

### Operating System

Linux Mint 22.1 (Xia)

### CPU

AMD Ryzen 5 5500U

### GPU

AMD Radeon Graphics gfx90c

### ROCm Version

ROCm 6.3.3

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
  Name:                    AMD Ryzen 5 5500U with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5500U with Radeon Graphics
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
  Max Clock Freq. (MHz):   4056                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    5906004(0x5a1e54) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    5906004(0x5a1e54) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    5906004(0x5a1e54) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    5906004(0x5a1e54) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx90c                             
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
    L1:                      16(0x10) KB                        
    L2:                      1024(0x400) KB                     
  Chip ID:                 5708(0x164c)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1800                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            7                                  
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
  Packet Processor uCode:: 472                                
  SDMA engine uCode::      40                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    2953000(0x2d0f28) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    2953000(0x2d0f28) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx90c:xnack+   
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

I'm using the 6.8.0-57-generic linux kernel, and the code for the fractal generator I created can be found [here](https://github.com/Equiel-1703/mandelbrot-fractal).

**UPDATE**: I tried the 6.11.0-21-generic kernel, but I got exactly the same issues.

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-04-01T14:01:00Z)

Hi @Equiel-1703. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-05-26T15:46:22Z)

Hi @Equiel-1703, sorry for the delay on this. We don't currently have official support for gfx90c and other integrated graphics; see the compatibility matrices at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html.

---

### 评论 #3 — schung-amd (2025-06-06T16:24:24Z)

Closing for now as gfx90c is unsupported. Feel free to comment and we can reopen if necessary.

---

### 评论 #4 — Leokuma (2026-02-21T18:53:49Z)

I was having a similar problem on Mint 22.3 with AMD Radeon RX 7600 (which apparently is not officially supported, but works for me). In my case, the PC wouldn't wake up from suspension at all: the screen was blank.

When I installed ROCm with the command `amdgpu-install --usecase=rocm`, suspension stopped working and I also had to run Blender as `sudo` for it to be able to detect HIP.

Then I formatted my PC and followed the instructions from the following page, **but I didn't install the AMDGPU driver**: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html:

```
wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/jammy/amdgpu-install_7.2.70200-1_all.deb
sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
sudo apt update
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm
```

Now everything works fine. I can even use Blender with hardware raytracing, and it detects HIP without `sudo`. I can also suspend and wake up the machine without any problems.

---

### 评论 #5 — Equiel-1703 (2026-02-21T19:19:11Z)

Hey @Leokuma! Thanks for the info! After @schung-amd explained that ROCm doesn't officialy supports my iGPU I started using Mesa drivers and got very good results! I specifically needed OpenCL support, and worked very fine. I installed the `mesa-opencl-icd` package and set `rusticl` as the main implementation.

I'm very glad that you shared this solution, though! I may give this a try sometime. It's a shame that Blender is dropping support on OpenCL, we could get the most out of older hardware this way (and more easily). [But looks like the standard is not that great for rendering anymore](https://blender.stackexchange.com/questions/221683/cycles-opencl-and-mesa-driver-support).

---
