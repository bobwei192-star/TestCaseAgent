# [Issue]: kernels > 6.13 crash driver due to scheduler comp_1.1.1 is not ready

> **Issue #4965**
> **状态**: closed
> **创建时间**: 2025-06-25T03:43:48Z
> **更新时间**: 2025-06-26T01:00:43Z
> **关闭时间**: 2025-06-25T15:02:59Z
> **作者**: chboishabba
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4965

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

OS:
NAME="Arch Linux"
CPU: 
model name	: Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz
GPU:
  Name:                    Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz
  Marketing Name:          Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz
  Name:                    gfx803                             
  Marketing Name:          AMD Radeon RX 580 Series           
      Name:                    amdgcn-amd-amdhsa--gfx803       


#AI


Subject: [REGRESSION] RX-580 (gfx803) GPU hangs since v6.14.1 – “scheduler comp_1.1.1 is not ready” / ROCm 5.7+ broken

Hello AMD GPU &amp; ROCm maintainers,

TL;DR  
My Polaris (RX-580, gfx803) freezes under compute load on a number of kernels after having successfully returned compatibility via:

https://github.com/robertrosenbusch/gfx803_rocm/

https://github.com/robertrosenbusch/gfx803_rocm/issues/35#issuecomment-2996884779
![Image](https://github.com/user-attachments/assets/d342fc01-a3e7-4ff9-9bd4-84386a5b5173)

➜ **v6.14.1-rc1** and newer.  
Last known good       : **v6.11**  
First known bad       : **v6.12**  
Regression bisected to:  
  * de84484c6f8b (“drm/amdkfd: Improve signal event slow path”, 2024-12-19)  
  * bac38ca057fe (“drm/amdkfd: implement per queue sdma reset …”, 2025-03-06)

Reverting *both* commits on top of **v6.16-rc3** restores full stability and allows ROCm 5.7 workloads (e.g. Stable-Diffusion, faster-whisper) to run for hours. This was not previously required prior to 6.15 for ROCm 6.4.0 on gfx803  cards. The above repo uses official debian ROC builds for these deprecated cards, to my knowledge.  

---


https://github.com/robertrosenbusch/gfx803_rocm/issues/35#issuecomment-2996884779

| Kernel            | Result | Note                              |
|-------------------|--------|-----------------------------------|
| 6.13.y (LTS)      |      |                           |
| **6.14.0**        |      | baseline - I believe this was MY last working                          |
| **6.14.1-rc1**    | BAD    | first hang                        |
| 6.15-rc1          | BAD    | hang                              |
| 6.15.8            | BAD    | hang                              |
| 6.16-rc3          | BAD    | hang                              |
| 6.16-rc3 – **revert de84484 + bac38ca** | OK |  | (not confirmed by me)

---

### Reproduction
1. Boot the docker under a bad kernel.
2. Run a ROCm workload that creates several compute queues, e.g.  
   `python stable-diffusion.py` or `faster-whisper --model medium ...`
3. Upon model initialisation, an immediate driver crash is caused, which can be witnessed on the host machine via  

```
<p>[drm] scheduler comp_1.1.1 is not ready, skipping<br>
[drm:sched_job_timedout] <em>ERROR</em> ring comp_1.1.1 timeout</p>
```

followed by a hard GPU reset (visible only within logs, no apparent visual artifacts) and, reliably produces a full system lockup whereby the hang appears to prevent Python or Docker from killing their processes, leaving the docker hanging, and requiring manual rebooting (sudo cannot kill the tasks upon reboot and the tasks do not receive SIGKILL). This eventually leads to a degraded state where the desktop slowly loses interactivity over the course of several hours.

---

### Bisect details
I had previously attempted a git bisect (limited to *drivers/gpu/drm/amd*) between v6.12 and v6.15-rc1:


<p>$ git bisect start v6.15-rc1 v6.14 -- drivers/gpu/drm/amd<br>
...<br>
de84484c6f8b07ad0850d6c4  bad<br>
bac38ca057fef2c8c024fe9e  bad</p>

Cherry-picking *reverts* of both commits on top of v6.16-rc3 restores
normal behaviour; leaving either patch in place reproduces the hang.

---

### Relevant log excerpts
*(full dmesg attached)*


<p>[drm] scheduler comp_1.1.1 is not ready, skipping<br>
[  97.602622] amdgpu 0000:08:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=123456 emitted seq=123459<br>
[  97.602630] amdgpu 0000:08:00.0: amdgpu: GPU recover succeeded, reset domain time = 2ms</p>

---

### Downstream references
* Arch Forum thread documenting identical hang – “Polaris GPU ‘scheduler not ready’ after 6.14.1” :contentReference[oaicite:0]{index=0}  
* Fedora bug 2284329 – “RX-580 compute freezes on 6.15+” :contentReference[oaicite:1]{index=1}  
* Tinygrad issue 3096 – same dmesg signature under AI load :contentReference[oaicite:2]{index=2}  

---

### Suspect commits
* **de84484c6f8b**  
  “drm/amdkfd: Improve signal event slow path” (Philip Yang, 2024-12-19)  
  Patch view: git.kernel.org 
* **bac38ca057fe**  
  “drm/amdkfd: implement per queue sdma reset for gfx 9.4+” (Jonathan Kim, 2025-03-06)  
  Patch view: GitHub mirror :contentReference[oaicite:4]{index=4}

Both patches touch amdkfd queue reset paths and are first included in the
exact releases where the regression appears.

---

### Why this matters
Although **gfx803** is EOL for official ROCm, large user communities
(stable-diffusion, whisper, tinygrad) still depend on it :contentReference[oaicite:5]{index=5}.  
Community builds prove ROCm 5.7 + RX-580 are functional on 6.14 kernels
and below :contentReference[oaicite:6]{index=6}.

---

### Proposed next steps
* Review interaction between the new KFD signal-event slow-path and
  legacy GPUs that lack valid event IDs.
* Confirm whether `hqd_sdma_get_doorbell()` logic (added in bac38ca)
  returns stale doorbells on gfx803, causing false positives.
* Consider back-outs for 6.15-stable / 6.16-rc while a proper fix is
  developed.

Please let me know any further diagnostics or testing you need.
I can easily rebuild kernels and provide annotated traces.

Thanks for your time!

Best regards,
&lt;Johl Brown&gt;
&lt;johlbrown[@]gmail[.]com&gt;
</code></pre>
<hr>
<h3>Sources consulted</h3>

Topic | Representative sources
-- | --
Error string “scheduler comp_1.1.1 is not ready, skipping” | Arch forum (bbs.archlinux.org) · tinygrad GH (gist.github.com) · Fedora bug (discussion.fedoraproject.org)
Commit de84484 | kernel.org patch view
Commit bac38ca | GitHub mirror search (lkml.org)
Event-handling change discussion | LKML thread snippet (github.com)
SDMA reset discussions | LKML search (github.com)
Polaris ROCm community usage | README (community build) (github.com)
Official ROCm support matrix (Polaris dropped) | AMD docs (rocm.docs.amd.com)



### Sources consulted

[1]: https://bbs.archlinux.org/viewtopic.php?id=302729&utm_source=chatgpt.com "It's back: Log spam: [drm] scheduler comp_1.0.2 is not ready, skipping ..."
[2]: https://gist.github.com/fxkamd/ffd02d66a2863e444ec208ea4f3adc48?utm_source=chatgpt.com "Observations about HSA and KFD backends in TinyGrad · GitHub"
[3]: https://discussion.fedoraproject.org/t/amd-rx580-system-freeze-on-maximum-vram-speed/136639?utm_source=chatgpt.com "AMD RX580 system freeze on maximum VRAM speed"
[4]: https://lkml.org/lkml/2025/4/5/394?utm_source=chatgpt.com "LKML: Linus Torvalds: Re: [git pull] drm fixes for 6.15-rc1"
[5]: https://github.com/torvalds/linux/commits?before=805ba04cb7ccfc7d72e834ebd796e043142156ba+6335&utm_source=chatgpt.com "Commits · torvalds/linux - GitHub"
[6]: https://github.com/torvalds/linux/commits?before=5bc1018675ec28a8a60d83b378d8c3991faa5a27+7980&utm_source=chatgpt.com "Commits · torvalds/linux - GitHub"
[7]: https://github.com/woodrex83/ROCm-For-RX580/blob/main/README.md?utm_source=chatgpt.com "ROCm-For-RX580/README.md at main - GitHub"
[8]: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility.html?utm_source=chatgpt.com "Compatibility matrices — Use ROCm on Radeon GPUs - AMD"

### Operating System

Linux archb 6.15.2-arch1-1 #1 SMP PREEMPT_DYNAMIC Tue, 10 Jun 2025 21:32:33 +0000 x86_64 GNU/Linux

### CPU

i7 7700k

### GPU

RX 580

### ROCm Version

HSA System Attributes     Runtime Version:         1.1 Runtime Ext Version:     1.7

### ROCm Component

_No response_

### Steps to Reproduce

Kernels before 6.13 appear to be working
Kernel 6.16rc2 appears to work after patching two commits.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
(Wed Jun 25 13:41:32) c@archb ~$ /opt/rocm/bin/rocminfo --support
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.7
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           YES
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz
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
  Max Clock Freq. (MHz):   4900                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32827564(0x1f4e8ac) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32827564(0x1f4e8ac) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32827564(0x1f4e8ac) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32827564(0x1f4e8ac) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx803                             
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 580 Series           
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
  Chip ID:                 26591(0x67df)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1411                               
  BDFID:                   256                                
  Internal Node ID:        1                                  
  Compute Unit:            36                                 
  SIMDs per CU:            4                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
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
  Packet Processor uCode:: 730                                
  SDMA engine uCode::      58                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8388608(0x800000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8388608(0x800000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx803          
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

```
(Wed Jun 25 13:58:53) c@archb ~$ lspci -nnk -d 1002:* 
01:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] [1002:67df] (rev e7)
	Subsystem: ASUSTeK Computer Inc. Device [1043:0519]
	Kernel driver in use: amdgpu
	Kernel modules: amdgpu
01:00.1 Audio device [0403]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere HDMI Audio [Radeon RX 470/480 / 570/580/590] [1002:aaf0]
	Subsystem: ASUSTeK Computer Inc. Device [1043:aaf0]
	Kernel driver in use: snd_hda_intel
	Kernel modules: snd_hda_intel
(Wed Jun 25 13:58:54) c@archb ~$ /opt/rocm/bin/rocm-smi -a


============================ ROCm System Management Interface ============================
============================== Version of System Component ===============================
Driver version: 6.15.2-arch1-1
==========================================================================================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		AMD Radeon RX 580 Series
GPU[0]		: Device ID: 		0x67df
GPU[0]		: Device Rev: 		0xe7
GPU[0]		: Subsystem ID: 	0x0519
GPU[0]		: GUID: 		38156
==========================================================================================
======================================= Unique ID ========================================
GPU[0]		: Unique ID: 0x0
==========================================================================================
========================================= VBIOS ==========================================
GPU[0]		: VBIOS version: 115-D000PIL-100
==========================================================================================
====================================== Temperature =======================================
GPU[0]		: Temperature (Sensor edge) (C): 64.0
==========================================================================================
=============================== Current clock frequencies ================================
GPU[0]		: mclk clock level: 0: (300Mhz)
GPU[0]		: sclk clock level: 3: (1158Mhz)
GPU[0]		: pcie clock level: 1 (8.0GT/s x16)
==========================================================================================
=================================== Current Fan Metric ===================================
GPU[0]		: Unable to detect fan speed for GPU 0
==========================================================================================
================================= Show Performance Level =================================
GPU[0]		: Performance Level: auto
==========================================================================================
==================================== OverDrive Level =====================================
GPU[0]		: GPU OverDrive value (%): 0
==========================================================================================
==================================== OverDrive Level =====================================
GPU[0]		: GPU Memory OverDrive value (%): 0
==========================================================================================
======================================= Power Cap ========================================
GPU[0]		: Max Graphics Package Power (W): 180.0
==========================================================================================
================================== Show Power Profiles ===================================
GPU[0]		: 1. Available power profile (#1 of 7): CUSTOM
GPU[0]		: 2. Available power profile (#2 of 7): VIDEO
GPU[0]		: 3. Available power profile (#3 of 7): POWER SAVING
GPU[0]		: 4. Available power profile (#4 of 7): COMPUTE
GPU[0]		: 5. Available power profile (#5 of 7): VR
GPU[0]		: 6. Available power profile (#6 of 7): 3D FULL SCREEN*
GPU[0]		: 7. Available power profile (#7 of 7): BOOTUP DEFAULT
==========================================================================================
=================================== Power Consumption ====================================
GPU[0]		: Current Socket Graphics Package Power (W): 18.029
==========================================================================================
============================== Supported clock frequencies ===============================
GPU[0]		: 
GPU[0]		: 
GPU[0]		: Supported mclk frequencies on GPU0
GPU[0]		: 0: 300Mhz *
GPU[0]		: 1: 1000Mhz
GPU[0]		: 2: 2000Mhz
GPU[0]		: 
GPU[0]		: Supported sclk frequencies on GPU0
GPU[0]		: 0: 300Mhz
GPU[0]		: 1: 751Mhz
GPU[0]		: 2: 1048Mhz
GPU[0]		: 3: 1158Mhz *
GPU[0]		: 4: 1240Mhz
GPU[0]		: 5: 1309Mhz
GPU[0]		: 6: 1364Mhz
GPU[0]		: 7: 1411Mhz
GPU[0]		: 
GPU[0]		: 
GPU[0]		: Supported PCIe frequencies on GPU0
GPU[0]		: 0: 2.5GT/s x8
GPU[0]		: 1: 8.0GT/s x16 *
GPU[0]		: 
------------------------------------------------------------------------------------------
==========================================================================================
=================================== % time GPU is busy ===================================
GPU[0]		: GPU use (%): 0
==========================================================================================
=================================== Current Memory Use ===================================
GPU[0]		: GPU Memory Allocated (VRAM%): 35
GPU[0]		: GPU Memory Read/Write Activity (%): 2
GPU[0]		: Memory Activity: N/A
GPU[0]		: Not supported on the given system
==========================================================================================
===================================== Memory Vendor ======================================
GPU[0]		: get_vram_vendor, Not supported on the given system
==========================================================================================
================================== PCIe Replay Counter ===================================
GPU[0]		: PCIe Replay Count: 0
==========================================================================================
===================================== Serial Number ======================================
GPU[0]		: get_serial_number, Not supported on the given system
GPU[0]		: Serial Number: N/A
==========================================================================================
===================================== KFD Processes ======================================
No KFD PIDs currently running
==========================================================================================
================================== GPUs Indexed by PID ===================================
No KFD PIDs currently running
==========================================================================================
======================= GPU Memory clock frequencies and voltages ========================
GPU[0]		: get_od_volt, Not supported on the given system
==========================================================================================
==================================== Current voltage =====================================
GPU[0]		: Voltage (mV): 1031
==========================================================================================
======================================= PCI Bus ID =======================================
GPU[0]		: PCI Bus: 0000:01:00.0
==========================================================================================
================================== Firmware Information ==================================
GPU[0]		: CE firmware version: 		140
GPU[0]		: MC firmware version: 		62184512
GPU[0]		: ME firmware version: 		167
GPU[0]		: MEC firmware version: 	730
GPU[0]		: MEC2 firmware version: 	730
GPU[0]		: PFP firmware version: 	254
GPU[0]		: RLC firmware version: 	286
GPU[0]		: SDMA firmware version: 	58
GPU[0]		: SDMA2 firmware version: 	58
GPU[0]		: SMC firmware version: 	00.23.17.00
GPU[0]		: UVD firmware version: 	0x01821000
GPU[0]		: VCE firmware version: 	0x351a0300
==========================================================================================
====================================== Product Info ======================================
GPU[0]		: Card Series: 		AMD Radeon RX 580 Series
GPU[0]		: Card Model: 		0x67df
GPU[0]		: Card Vendor: 		Advanced Micro Devices, Inc. [AMD/ATI]
GPU[0]		: Card SKU: 		D000PIL
GPU[0]		: Subsystem ID: 	0x0519
GPU[0]		: Device Rev: 		0xe7
GPU[0]		: Node ID: 		1
GPU[0]		: GUID: 		38156
GPU[0]		: GFX Version: 		gfx803
==========================================================================================
======================================= Pages Info =======================================
GPU[0]		: ras, Not supported on the given system
================================= Show Valid sclk Range ==================================
GPU[0]		: get_od_volt, Not supported on the given system
==========================================================================================
================================= Show Valid mclk Range ==================================
GPU[0]		: get_od_volt, Not supported on the given system
==========================================================================================
================================ Show Valid voltage Range ================================
GPU[0]		: get_od_volt, Not supported on the given system
==========================================================================================
================================== Voltage Curve Points ==================================
GPU[0]		: get_od_volt_info, Not supported on the given system
WARNING: GPU[0]	: Voltage curve Points unsupported.
==========================================================================================
==================================== Consumed Energy =====================================
GPU[0]		: % Energy Counter, Unexpected data received
==========================================================================================
=============================== Current Compute Partition ================================
GPU[0]		: Not supported on the given system
==========================================================================================
================================ Current Memory Partition ================================
GPU[0]		: Not supported on the given system
==========================================================================================
====================================== GPU Metrics =======================================
GPU[0]		: get_gpu_metrics, Unexpected data received
ERROR: GPU[0]	: Failed to retrieve GPU metrics, metric version may not be supported for this device.
==========================================================================================
================================== End of ROCm SMI Log ===================================
(Wed Jun 25 13:59:13) c@archb ~$ /opt/rocm/bin/rocm-smi --showtopo


============================ ROCm System Management Interface ============================
================================ Weight between two GPUs =================================
       GPU0         
GPU0   0            

================================= Hops between two GPUs ==================================
       GPU0         
GPU0   0            

=============================== Link Type between two GPUs ===============================
       GPU0         
GPU0   0            

======================================= Numa Nodes =======================================
GPU[0]		: (Topology) Numa Node: 0
GPU[0]		: (Topology) Numa Affinity: -1
================================== End of ROCm SMI Log ===================================
```

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-06-25T14:15:35Z)

Hi @chboishabba. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-06-25T15:02:59Z)

Hi @chboishabba, I am sorry that you are having issues with ROCm, and thanks for reaching out to us! Please keep in mind that we cannot really guarantee ROCm working with any kernel version not [officially supported](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#operating-systems-kernel-and-glibc-versions), which is still at kernel version 6.11. Despite some users might be able to find success working with versions 6.12 and later, I would not expect these experiences to be transferrable. Moreover, issues with kernel versions 6.13, 6.14 has been also seen before as well (e.g. https://github.com/ROCm/ROCm/issues/4619). 

Typically, unless the issue affects both supported and unsupported kernel versions, it won't make sense for us to fix it. And if we plan on future support for the particular version of kernel, work should likely already be underway and there's not much else we need to add. A fix will be released in a newer version supporting the kernel, again, if support for the particular kernel version is planned. 

Edit: Since this issue also affects a EOL card, it is possible that even in the case when a newer supported version comes out, support still will not be available for this particular card. However, we are working on expanding our line of support of legacy cards . I cannot say whether it will cover RX580, but post like this will help us plan out the scope for sure.

Finally, I just wanted to add although we are not really able to help out in this particular case, we really appreciate your post and your dedication in supporting the ROCm ecosystem from the community side! Thank you!

---

### 评论 #3 — chboishabba (2025-06-26T01:00:43Z)

Hello and thank you for your reply. I am responding briefly by email.
Perhaps the roc docs could be improved if support is expected for new roc
on legacy kernels for gfx8. Previously, the community project
rocm_sdk_builder compiled various patches for a large variety of cards. I
believe the development of the project is no longer active due to the Dev
now contributing by more formal means.

I am aware of the deprecated state of gfx8 for GPGPU however generally roc
components can be built successfully using the above project. I probably
need to sit down and reply properly sorry :)

On Thu, 26 June 2025, 1:03 am Tim Gu, ***@***.***> wrote:

> *tcgu-amd* left a comment (ROCm/ROCm#4965)
> <https://github.com/ROCm/ROCm/issues/4965#issuecomment-3005124072>
>
> Hi @chboishabba <https://github.com/chboishabba>, I am sorry that you are
> having issues with ROCm, and thanks for reaching out to us! Please keep in
> mind that we cannot really guarantee ROCm working with any kernel version
> not officially supported
> <https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#operating-systems-kernel-and-glibc-versions>,
> which is still at kernel version 6.11. Despite some users might be able to
> find success working with versions 6.12 and later, I would not expect these
> experiences to be transferrable. Moreover, issues with kernel versions
> 6.13, 6.14 has been also seen before as well (e.g. #4619
> <https://github.com/ROCm/ROCm/issues/4619>).
>
> Typically, unless the issue affects both supported and unsupported kernel
> versions, it won't make sense for us to fix it. And if we plan on future
> support for the particular version of kernel, work should likely already be
> underway and there's not much else we need to add. A fix will be released
> in a newer version supporting the kernel, again, if support for the
> particular kernel version is planned.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4965#issuecomment-3005124072>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AGM4B3U6WIRVZSITSDVNAYD3FK23VAVCNFSM6AAAAACACBRL52VHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTAMBVGEZDIMBXGI>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---
