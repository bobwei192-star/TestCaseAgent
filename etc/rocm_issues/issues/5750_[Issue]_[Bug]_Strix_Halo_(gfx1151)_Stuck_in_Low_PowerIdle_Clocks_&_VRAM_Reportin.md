# [Issue]: [Bug] Strix Halo (gfx1151): Stuck in Low Power/Idle Clocks & VRAM Reporting Underflow (ROCm 7.1 / Kernel 6.14)

> **Issue #5750**
> **状态**: closed
> **创建时间**: 2025-12-08T19:00:46Z
> **更新时间**: 2026-01-14T15:05:08Z
> **关闭时间**: 2026-01-14T15:05:08Z
> **作者**: 926nathant
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5750

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

**System Configuration:**
*   **Hardware:** AMD Ryzen AI Max+ 395 (Strix Halo / gfx1151)
*   **OS:** Ubuntu 24.04 LTS
*   **Kernel:** 6.14.0-36-generic
*   **Driver:** ROCm 7.1.1 DKMS (Driver version 6.16.6)
*   **Boot Args:** `amdgpu.ppfeaturemask=0xffffffff amdgpu.runpm=0 pcie_aspm=off`

**Issue Description:**
On Strix Halo hardware, the dGPU partition (`gfx1151`) fails to enter high-performance power states under compute load. Despite `radeontop` showing high pipeline utilization, clock speeds remain stuck at idle (~800-1000MHz SCLK/MCLK), resulting in severely degraded compute performance (e.g., 0.5 t/s on LLM inference).

Additionally, `rocm-smi` reports an integer underflow for VRAM usage, and power profiles (`pp_power_profile_mode`) are missing from sysfs despite `ppfeaturemask` being applied.

**Diagnostic Data (rocm-smi -a):**
*   **Clocks:** Supported max is 2900Mhz, but device is locked at Level 1 (885Mhz).
*   **Power:** Draws ~26W under load (effectively idle/soc overhead).
*   **Memory Reporting:** `VRAM USED: 18446744073709547520` (Underflow).
*   **Features:** `get_power_profiles`, `get_power_cap`, `overdrive` all report "Not supported on the given system".

**Steps Taken:**
1.  Disabled Secure Boot.
2.  Applied `amdgpu.ppfeaturemask=0xffffffff`.
3.  Disabled Runtime PM (`runpm=0`).
4.  Forced CPU Governor to Performance.
5.  Attempted `echo high > /sys/class/drm/card0/device/power_dpm_force_performance_level` (Command accepted, but no change in clocks).

**Logs:**
**System Configuration:**
*   **Hardware:** AMD Ryzen AI Max+ 395 (Strix Halo / gfx1151)
*   **OS:** Ubuntu 24.04 LTS
*   **Kernel:** 6.14.0-36-generic
*   **Driver:** ROCm 7.1.1 DKMS (Driver version 6.16.6)
*   **Boot Args:** `amdgpu.ppfeaturemask=0xffffffff amdgpu.runpm=0 pcie_aspm=off`

**Issue Description:**
On Strix Halo hardware, the dGPU partition (`gfx1151`) fails to enter high-performance power states under compute load. Despite `radeontop` showing high pipeline utilization, clock speeds remain stuck at idle (~800-1000MHz SCLK/MCLK), resulting in severely degraded compute performance (e.g., 0.5 t/s on LLM inference).

Additionally, `rocm-smi` reports an integer underflow for VRAM usage, and power profiles (`pp_power_profile_mode`) are missing from sysfs despite `ppfeaturemask` being applied.

**Diagnostic Data (rocm-smi -a):**
*   **Clocks:** Supported max is 2900Mhz, but device is locked at Level 1 (885Mhz).
*   **Power:** Draws ~26W under load (effectively idle/soc overhead).
*   **Memory Reporting:** `VRAM USED: 18446744073709547520` (Underflow).
*   **Features:** `get_power_profiles`, `get_power_cap`, `overdrive` all report "Not supported on the given system".

**Steps Taken:**
1.  Disabled Secure Boot.
2.  Applied `amdgpu.ppfeaturemask=0xffffffff`.
3.  Disabled Runtime PM (`runpm=0`).
4.  Forced CPU Governor to Performance.
5.  Attempted `echo high > /sys/class/drm/card0/device/power_dpm_force_performance_level` (Command accepted, but no change in clocks).

**Logs:**
[Insert the output of your 'rocm-smi -a' here]

### Operating System

Ubuntu 24.04 LTS

### CPU

AMD Ryzen AI Max+ 395 (Strix Halo / gfx1151)

### GPU

AMD Ryzen AI Max+ 395 (Strix Halo / gfx1151)

### ROCm Version

ROCm 7.1.1 DKMS (Driver version 6.16.6)

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ntennant@magicMax:~$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    131009772(0x7cf0cec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131009772(0x7cf0cec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131009772(0x7cf0cec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131009772(0x7cf0cec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
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
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65504884(0x3e78674) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65504884(0x3e78674) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
*******                  
Agent 3                  
*******                  
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
  Vendor Name:             AMD                                
  Feature:                 AGENT_DISPATCH                     
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        1(0x1)                             
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          64(0x40)                           
  Queue Type:              SINGLE                             
  Node:                    0                                  
  Device Type:             DSP                                
  Cache Info:              
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          0(0x0)                             
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            0                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:0                                  
  Memory Properties:       
  Features:                AGENT_DISPATCH
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    131009772(0x7cf0cec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536(0x10000) KB                  
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131009772(0x7cf0cec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             
ntennant@magicMax:~$ 


### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — 926nathant (2025-12-08T19:25:14Z)

<img width="389" height="295" alt="Image" src="https://github.com/user-attachments/assets/8b6c638b-0796-4c31-be5f-fd4878a46fd0" /> 
Performance mode in BIOS and in OS.

---

### 评论 #2 — ianbmacdonald (2025-12-08T23:58:02Z)

steps to reproduce?  Maybe install [ryzenadj](https://github.com/FlyGoat/RyzenAdj) and check you power limits.. here is what the defaults look like on a Framework 16
```

~#ryzenadj -i
detected compatible ryzen_smu kernel module
CPU Family: Strix Halo
SMU BIOS Interface Version: 25
Version: v0.18.0 
PM Table Version: 64020c
|        Name         |   Value   |     Parameter      |
|---------------------|-----------|--------------------|
| STAPM LIMIT         |   100.000 | stapm-limit        |
| STAPM VALUE         |     3.536 |                    |
| PPT LIMIT FAST      |   115.000 | fast-limit         |
| PPT VALUE FAST      |     5.822 |                    |
| PPT LIMIT SLOW      |   100.000 | slow-limit         |
| PPT VALUE SLOW      |     7.174 |                    |
| StapmTimeConst      |       nan | stapm-time         |
| SlowPPTTimeConst    |       nan | slow-time          |
| PPT LIMIT APU       |    70.000 | apu-slow-limit     |
| PPT VALUE APU       |     0.000 |                    |
| TDC LIMIT VDD       |       nan | vrm-current        |
| TDC VALUE VDD       |       nan |                    |
| TDC LIMIT SOC       |       nan | vrmsoc-current     |
| TDC VALUE SOC       |       nan |                    |
| EDC LIMIT VDD       |       nan | vrmmax-current     |
| EDC VALUE VDD       |       nan |                    |
| EDC LIMIT SOC       |       nan | vrmsocmax-current  |
| EDC VALUE SOC       |       nan |                    |
| THM LIMIT CORE      |   100.000 | tctl-temp          |
| THM VALUE CORE      |    44.223 |                    |
| STT LIMIT APU       |   100.000 | apu-skin-temp      |
| STT VALUE APU       |    44.223 |                    |
| STT LIMIT dGPU      |   100.000 | dgpu-skin-temp     |
| STT VALUE dGPU      |    44.169 |                    |
| CCLK Boost SETPOINT |       nan | power-saving /     |
| CCLK BUSY VALUE     |       nan | max-performance    |
```


---

### 评论 #3 — 926nathant (2025-12-10T13:52:33Z)

I can't NOT reproduce it. It shows this under load, at idle, always.

$ sudo ryzenadj -i
[sudo] password for ntennant: 
no compatible ryzen_smu kernel module found, fallback to /dev/mem
CPU Family: Strix Halo
SMU BIOS Interface Version: 25
Version: v0.18.0 
PM Table Version: 64020c
|        Name         |   Value   |     Parameter      |
|---------------------|-----------|--------------------|
| STAPM LIMIT         |   120.000 | stapm-limit        |
| STAPM VALUE         |    19.241 |                    |
| PPT LIMIT FAST      |   140.000 | fast-limit         |
| PPT VALUE FAST      |    19.974 |                    |
| PPT LIMIT SLOW      |   120.000 | slow-limit         |
| PPT VALUE SLOW      |     7.756 |                    |
| StapmTimeConst      |       nan | stapm-time         |
| SlowPPTTimeConst    |       nan | slow-time          |
| PPT LIMIT APU       |    70.000 | apu-slow-limit     |
| PPT VALUE APU       |     0.000 |                    |
| TDC LIMIT VDD       |       nan | vrm-current        |
| TDC VALUE VDD       |       nan |                    |
| TDC LIMIT SOC       |       nan | vrmsoc-current     |
| TDC VALUE SOC       |       nan |                    |
| EDC LIMIT VDD       |       nan | vrmmax-current     |
| EDC VALUE VDD       |       nan |                    |
| EDC LIMIT SOC       |       nan | vrmsocmax-current  |
| EDC VALUE SOC       |       nan |                    |
| THM LIMIT CORE      |    98.000 | tctl-temp          |
| THM VALUE CORE      |    36.896 |                    |
| STT LIMIT APU       |    98.000 | apu-skin-temp      |
| STT VALUE APU       |    36.896 |                    |
| STT LIMIT dGPU      |    98.000 | dgpu-skin-temp     |
| STT VALUE dGPU      |    38.204 |                    |
| CCLK Boost SETPOINT |       nan | power-saving /     |
| CCLK BUSY VALUE     |       nan | max-performance    |


---

### 评论 #4 — 926nathant (2025-12-15T22:22:51Z)

I guess maybe I should say "to reproduce bug boot system".  The problem statement is "rocm-smi reports gpu low power state and 937mhz clock at all times, under all loads". I don't know if this is a reporting issue or a functional issue.

---

### 评论 #5 — bkpaine1 (2025-12-16T23:58:05Z)

🎉 SOLVED: Strix Halo Clocks & VRAM Underflow on ROCm 7.9/TheROCK
Configuration:

Hardware: Strix Halo (gfx1151)

ROCm Version: ROCm 7.9.0 (TheROCK Preview)

Workload: High-sustained compute (e.g., ComfyUI / LLM Rendering)

I was experiencing the symptoms reported here (clocks stuck at ~1000MHz and VRAM underflow in rocm-smi -a).

The Solution was using coreclt.

Specifically, I used the internal utility coreclt to manually manage/set the clocks. After running the utility, the GPU was able to correctly ramp up to its high-frequency state, and the VRAM reporting issue was simultaneously resolved. The system is now stable under heavy load.

Could the developers please comment on the functionality of coreclt and if its equivalent clock management logic can be integrated into the default ROCm kernel module for gfx1151?

I can paste screenshots I am running 45s/it on ComfyUI with Corectl managing my GPU  

|███████████████████████████████████████████| 20/20 [11:50<00:00, 35.51s/it]
ROCM Tiled VAE Decode completed in 176.26s
Prompt executed in 00:14:57
got prompt
100%|███████████████████████████████████████████| 20/20 [11:50<00:00, 35.54s/it]
ROCM Tiled VAE Decode completed in 175.00s
Prompt executed in 00:14:58
got prompt
100%|███████████████████████████████████████████| 20/20 [11:49<00:00, 35.49s/it]
ROCM Tiled VAE Decode completed in 175.59s
Prompt executed in 00:14:56
got prompt
100%|███████████████████████████████████████████| 20/20 [11:51<00:00, 35.56s/it]
ROCM Tiled VAE Decode completed in 175.69s
Prompt executed in 00:14:57
got prompt
100%|███████████████████████████████████████████| 20/20 [11:42<00:00, 35.14s/it]
ROCM Tiled VAE Decode completed in 175.80s
Prompt executed in 00:14:49
got prompt
100%|███████████████████████████████████████████| 20/20 [11:38<00:00, 34.95s/it]
ROCM Tiled VAE Decode completed in 175.06s
Prompt executed in 00:14:46
got prompt
100%|███████████████████████████████████████████| 20/20 [11:39<00:00, 34.95s/it]
ROCM Tiled VAE Decode completed in 175.68s
Prompt executed in 00:14:45
got prompt
100%|███████████████████████████████████████████| 20/20 [11:40<00:00, 35.04s/it]
ROCM Tiled VAE Decode completed in 175.39s
Prompt executed in 00:14:47
got prompt
100%|███████████████████████████████████████████| 20/20 [11:32<00:00, 34.62s/it]
ROCM Tiled VAE Decode completed in 175.38s
Prompt executed in 00:14:38
got prompt
100%|███████████████████████████████████████████| 20/20 [11:50<00:00, 35.54s/it]
ROCM Tiled VAE Decode completed in 174.83s
Prompt executed in 00:14:58
got prompt
100%|███████████████████████████████████████████| 20/20 [11:49<00:00, 35.45s/it]
ROCM Tiled VAE Decode completed in 176.38s
Prompt executed in 00:14:56
got prompt


Ubuntu 25.10 Also is the answer  

edit: I had issues with power draw at full speed so I limited to this 12/16/2025


Brent

<img width="1708" height="837" alt="Image" src="https://github.com/user-attachments/assets/7d69c506-0adf-498d-9a45-5c275632905b" />

---

### 评论 #6 — darren-amd (2026-01-07T20:31:52Z)

Hi @926nathant,

Thanks for reporting this issue, just gave this a try on a gfx1151 system with a small workload on the latest TheRock wheels (Instructions for install [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-releases-using-pip)) and was unable to reproduce the issue:
```
==========================================================================================
=============================== Current clock frequencies ================================
GPU[0]          : mclk clock level: 2: (1000Mhz)
GPU[0]          : sclk clock level: 2: (2900Mhz)
==========================================================================================
``` 
Would you mind giving it a try on the latest ROCm version and if the issue persists could you please share the workload you are running, as well as the logs for `rocm-smi -a` and `rocm-smi` before, during, and after the workload? Thanks!

---

### 评论 #7 — bkpaine1 (2026-01-07T21:38:09Z)

I am not using old rocm I have switched to TheROCK 7.11 now (started with 7.9) this works better.  Less stable but fast and integrated with Ubuntu 25.10 kernel.  The amd-smi is useless use CoreCtl  amd-smi USELESS  | AMD-SMI 26.1.0+5df6c765      amdgpu version: 6.17.0-8 ROCm version: 7.1.0    |
| VBIOS version: 023.011.000.039.000001                                        |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c6:00.0    AMD Radeon Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A          35103/65536 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|    0      15222  python3.11            19.6 MB   33.1 GB    33.9 GB  N/A     |
+-----------------------------------------------------------------------------  My CoreCT show 2800Ghz  I limit due to power causes overheating.  This is running comfyui at max GPU

<img width="1526" height="784" alt="Image" src="https://github.com/user-attachments/assets/002176a2-9505-43d1-aeb5-1a1444eacaea" />

 


---

### 评论 #8 — darren-amd (2026-01-14T15:05:08Z)

Thanks for confirming! For the missing amd-smi metrics being displayed as N/A, we have a ticket: https://github.com/ROCm/TheRock/issues/1881 to track adding additional support for metrics that the driver supports. 

---
