# [Issue]: The 780M GPU fails to run any model using comfyui

> **Issue #4557**
> **状态**: closed
> **创建时间**: 2025-04-03T00:55:31Z
> **更新时间**: 2025-10-15T03:36:55Z
> **关闭时间**: 2025-07-08T20:47:39Z
> **作者**: leioukupo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4557

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

The 780m kernel is a failure to run comfyui in fedora41 with any model
Log display
HW Exception by GPU node-1 (Agent handle: 0x11dd2220) reason :GPU Hang
core dumped

### Operating System

fedora 41

### CPU

8845h with 780m

### GPU

780m

### ROCm Version

rocm6.3

### ROCm Component

_No response_

### Steps to Reproduce

Download comfyui, and then follow the README to set up the environment and run it
AI drawing using arbitrary models

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    AMD Ryzen 7 8845HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 8845HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5100                               
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
      Size:                    49088700(0x2ed08bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49088700(0x2ed08bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    49088700(0x2ed08bc) KB             
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
  Chip ID:                 6400(0x1900)                       
  ASIC Revision:           12(0xc)                            
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   50432                              
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
  Packet Processor uCode:: 40                                 
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24544348(0x176845c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24544348(0x176845c) KB             
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

### Additional Information

_No response_

---

## 评论 (15 条)

### 评论 #1 — ppanchad-amd (2025-04-03T15:06:22Z)

Hi @leioukupo. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-04-03T15:21:21Z)

Hi @leioukupo, can you post a dmesg log around where you get the exception? ROCm doesn't officially support gfx1103 so this might just not work, but I'll take a look anyway.

---

### 评论 #3 — leioukupo (2025-04-06T11:14:11Z)

> Hi [@leioukupo](https://github.com/leioukupo), can you post a dmesg log around where you get the exception? ROCm doesn't officially support gfx1103 so this might just not work, but I'll take a look anyway.

[1.txt](https://github.com/user-attachments/files/19620993/1.txt)

---

### 评论 #4 — fonix232 (2025-04-06T23:36:47Z)

I am getting this exact same issue (down to the Python segfault code) on my 8945HS node, however, only with pytorch based AI models - ollama/llama.cpp works flawlessly.

Relevant dmesg:

```
[Apr 6 23:35] python[20514]: segfault at 18 ip 00007f108c0af9bd sp 00007ffda0f33e20 error 4 in libamdhip64.so[2af9bd,7f108be00000+439000] likely on CPU 11 (core 3, socket 0)
[  +0.000010] Code: 00 31 f6 48 83 c5 08 e8 51 04 00 00 49 39 ec 75 ec 48 8b 83 48 01 00 00 48 8b a8 a0 01 00 00 48 8b 05 87 05 39 00 64 48 8b 10 <48> 8b 45 18 4c 8d 6d 18 a8 01 0f 85 8b 03 00 00 48 89 c1 48 83 c9
[Apr 6 23:38] python[21193]: segfault at 18 ip 00007f9c624af9bd sp 00007ffc3ff4ea20 error 4 in libamdhip64.so[2af9bd,7f9c62200000+439000] likely on CPU 11 (core 3, socket 0)
[  +0.000009] Code: 00 31 f6 48 83 c5 08 e8 51 04 00 00 49 39 ec 75 ec 48 8b 83 48 01 00 00 48 8b a8 a0 01 00 00 48 8b 05 87 05 39 00 64 48 8b 10 <48> 8b 45 18 4c 8d 6d 18 a8 01 0f 85 8b 03 00 00 48 89 c1 48 83 c9
```

A few observations:

- Using gfx1103 results in a number of `invalid device function` HIP errors in runtime
- Using gfx1102/gfx1101/gfx1100 results in the above segfault
- Using gfx1030 causes a kernel crash that reboots the host

This behaviour was observed on ROCm versions 6.2.4, 6.3.0, 6.3.3, and 6.3.4 (which does not seem to be tagged, yet it's the latest rocm/pytorch image available?), on PyTorch 2.4, 2.5, 2.6 and 2.8.

---

### 评论 #5 — schung-amd (2025-04-07T12:55:51Z)

@fonix232 What OS are you on? And when you refer to using gfx1103, gfx1102, etc. do you mean via `HSA_OVERRIDE_GFX_VERSION`?

---

### 评论 #6 — fonix232 (2025-04-07T17:50:04Z)

Small update: after hours of tinkering, I found the Radeon repo for pytorch. Using that in combination with Ubuntu 24.04, ROCm 6.3.4, and the Radeon PyTorch 2.4.0 builds (enforcing gfx1101/gfx1100) fixes the segfault issue seen above - however I've run into GPU hang issues using this combination.

For said GPU hang, I believe it might be my system causing an issue, as I'm running TrueNAS SCALE 25.04-RC.1 (based on Debian 12 but with kernel 6.12.15, which as far as I know is unsupported at the moment by the ROCm stack). Unfortunately PyTorch has no way of recovering from these GPU hangs.

The full log of this event:

```
[17954.089070] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[17954.092089] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[17954.095627] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[17954.099061] amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 1
[17954.101464] amdgpu 0000:c6:00.0: amdgpu: Failed to evict process queues
[17954.104101] amdgpu: Failed to quiesce KFD
[17954.106236] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[17954.106251] amdgpu 0000:c6:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 0 for dev 2065
[17954.109982] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State
[17954.111854] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State Completed
[17956.206957] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[17956.209952] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[17958.217450] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[17958.220455] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[17958.225472] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[17958.255229] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[17958.255710] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[17958.255866] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[17958.257641] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[17958.263794] [drm] DMUB hardware initialized: version=0x08003D00
[17958.472573] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[17958.472586] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[17958.472590] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[17958.472594] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[17958.472597] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[17958.472600] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[17958.472602] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[17958.472605] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[17958.472608] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[17958.472612] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[17958.472615] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[17958.472618] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[17958.472621] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[17958.509781] amdgpu 0000:c6:00.0: amdgpu: GPU reset(6) succeeded!
[17959.325394] usb 7-1: USB disconnect, device number 14
[17959.325403] usb 7-1.1: USB disconnect, device number 15
[17959.577235] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[17959.580325] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[17959.583920] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[17959.587431] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 0
[17959.587433] amdgpu: Resetting wave fronts (cpsch) on dev 000000009472e026
[17959.587435] amdgpu 0000:c6:00.0: amdgpu: no vmid pasid mapping supported
[17959.590282] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[17959.595428] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State
[17959.598711] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State Completed
[17959.695462] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[17959.727467] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[17959.728127] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[17959.728201] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[17959.729821] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[17959.737245] [drm] DMUB hardware initialized: version=0x08003D00
[17959.863054] usb 7-1: new high-speed USB device number 16 using xhci_hcd
[17959.952983] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[17959.952993] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[17959.952996] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[17959.952998] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[17959.953000] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[17959.953001] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[17959.953003] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[17959.953004] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[17959.953006] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[17959.953008] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[17959.953009] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[17959.953011] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[17959.953013] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[17960.001680] usb 7-1: New USB device found, idVendor=1a40, idProduct=0101, bcdDevice= 1.00
[17960.001685] usb 7-1: New USB device strings: Mfr=0, Product=1, SerialNumber=0
[17960.001686] usb 7-1: Product: USB2.0 HUB
[17960.006288] amdgpu 0000:c6:00.0: amdgpu: GPU reset(7) succeeded!
```

This, according to [this thread on the Linux Kernel mail-list](https://lore.kernel.org/lkml/c12d7952-b05e-4ea7-bedc-7a1d5da3e3cf@amd.com/) is caused by a MES firmware issue on the 11.0.3 devices. 

@schung-amd as per above, TrueNAS SCALE 25.04-RC.1, running PyTorch in a Docker container (base Ubuntu 24.04, but I've also tried the official rocm/pytorch containers).

Yes, when I say using gfx1103/1102/1101/1030, I meant setting it via the following env vars:

```
export HSA_OVERRIDE_GFX_VERSION="11.0.1"
export PYTORCH_ROCM_ARCH="gfx1101"
export HIP_VISIBLE_DEVICES=0
```

---

### 评论 #7 — schung-amd (2025-04-07T18:14:52Z)

@fonix232 Thanks for the update! Running with AMD_LOG_LEVEL=7 may reveal more but it sounds like this is a symptom of `gfx1103` not being supported by ROCm at the moment.

Unrelated to the hang, but regarding `HSA_OVERRIDE_GFX_VERSION` and `gfx1103` specifically: there are some issues on `gfx1102` and `gfx1103` when overriding to `gfx1100` or `gfx1101`. Although the ISA is compatible, these architectures have less VGPRs than `gfx1100` and `gfx1101`. The kernels we ship for `gfx1100` are tuned to take full advantage of the hardware, so if you override a `gfx1103` card to `gfx1100` some workloads may invoke a kernel which requires more VGPRs than are available. I've only seen this in the wild with `fp16` precision so far, but this may exist elsewhere as well.

---

### 评论 #8 — fonix232 (2025-04-07T21:23:15Z)

@schung-amd that might be the reason for the hangs! Unfortunately, `gfx1102` and `gfx1103` override targets, I get the unknown HIP function (or something akin, haven't saved those logs sadly, basically model execution fails from the get-go).

`AMD_LOG_LEVEL=7` seems to have the unintended side effect of flooding logs so quickly, the GPU can't be properly utilised - while my test script (simply using pyannote-audio for speaker diarization on 30min+ audio files) would usually nearly max out GPU usage (as per rocm-smi), with log level set to 7, I barely hit 7% on average (10% max, 3-4% most of the time).

Is there a way to redirect all that logging to a separate pipe instead of my current stout? It makes monitoring my Python script impossible as it spams 30-50 lines per ROCm task execution (which happens multiple times per second).

---

### 评论 #9 — schung-amd (2025-04-08T14:14:46Z)

> Is there a way to redirect all that logging to a separate pipe instead of my current stout?

You can use AMD_LOG_LEVEL_FILE="foo" to redirect the log output to a file.

---

### 评论 #10 — denzilferreira (2025-04-13T20:08:46Z)

 > The kernels we ship for `gfx1100` are tuned to take full advantage of the hardware, so if you override a `gfx1103` card to `gfx1100` some workloads may invoke a kernel which requires more VGPRs than are available. I've only seen this in the wild with `fp16` precision so far, but this may exist elsewhere as well.

Is there a way to limit how many VGPRs are requested? I'm facing the same issue with 780M with 8GB allocated on a T14Gen5. It will run for a while until it doesn't, just hanging the laptop altogether 😬 

---

### 评论 #11 — schung-amd (2025-04-14T14:31:17Z)

I'll try to find a workaround to do that. In my experience the VGPR issue causes crashes rather than hangs, so I'd suggest getting AMD_LOG_LEVEL=7 output to verify that it is a noncompatible kernel launch causing your issue.

---

### 评论 #12 — Nan-Do (2025-05-29T08:38:36Z)

I have experienced the same problem on my 780 when using pytorch or any other app that relies on rocm. The log is the similar as the one previously posted on this thread.

```
[117875.114139] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[117875.114146] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[117876.620535] amdgpu 0000:c6:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[117876.620540] amdgpu 0000:c6:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[117876.620543] amdgpu 0000:c6:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
[117876.620545] amdgpu 0000:c6:00.0: amdgpu:     Faulty UTCL2 client ID: CPC (0x5)
[117876.620547] amdgpu 0000:c6:00.0: amdgpu:     MORE_FAULTS: 0x1
[117876.620549] amdgpu 0000:c6:00.0: amdgpu:     WALKER_ERROR: 0x1
[117876.620550] amdgpu 0000:c6:00.0: amdgpu:     PERMISSION_FAULTS: 0x5
[117876.620552] amdgpu 0000:c6:00.0: amdgpu:     MAPPING_ERROR: 0x1
[117876.620553] amdgpu 0000:c6:00.0: amdgpu:     RW: 0x1
[117876.620557] amdgpu 0000:c6:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[117876.620560] amdgpu 0000:c6:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[117877.813807] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[117877.813812] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[117882.633682] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[117882.666966] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[117882.667375] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[117882.669472] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
```

One possible workaround, for the apps that support it, is to use the Vulkan backend instead of Rocm.


---

### 评论 #13 — schung-amd (2025-07-08T20:47:39Z)

Closing for now as we don't support gfx1103 with the mainline ROCm releases; however, ROCm gfx1103 is supported by TheRock (https://github.com/ROCm/TheRock), so I recommend trying those releases and see if this problem occurs there. If you are still experiencing this issue on the 780M with TheRock releases, please submit an issue there.

---

### 评论 #14 — wszgrcy (2025-10-13T11:58:47Z)

@schung-amd https://github.com/ollama/ollama/issues/12472
This issue may not only be a problem with 780m, but also similar errors with AMD395

---

### 评论 #15 — Nan-Do (2025-10-15T03:36:55Z)

@wszgrcy 
It does look like the same error, please post it at https://github.com/ROCm/TheRock/issues/1264

For anyone coming to this issue having hangs with the Radeon 780M. 
Please post anything related on the previous link which is where the issue is being investigated.

---
