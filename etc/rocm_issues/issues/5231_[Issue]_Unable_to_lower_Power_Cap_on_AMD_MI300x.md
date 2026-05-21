# [Issue]: Unable to lower Power Cap on AMD MI300x

> **Issue #5231**
> **状态**: open
> **创建时间**: 2025-08-27T16:12:56Z
> **更新时间**: 2026-03-23T18:16:27Z
> **作者**: kev-pebble
> **标签**: Feature Request, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5231

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description


I am unable to lower the power cap on MI300x. We need to lower the power from 750W to 500W. 

rocm-smi --version
ROCM-SMI version: 3.0.0+e68c0d1
ROCM-SMI-LIB version: 7.5.0 

```
rocm-smi

============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK     MCLK    Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       1     0x74b5,   21947  39.0°C      191.0W    NPS1, SPX, 0        2105Mhz  900Mhz  0%   auto  750.0W  95%    0%    
==========================================================================================================================
================================================== End of ROCm SMI Log =================================================== 
```



```
sudo rocm-smi --setpoweroverdrive 500

============================ ROCm System Management Interface ============================
================================ Set GPU Power OverDrive =================================
ERROR: GPU[0]   : Unable to set Power OverDrive to 500W
==========================================================================================
================================== End of ROCm SMI Log ===================================
```


```
rocminfo
ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    INTEL(R) XEON(R) PLATINUM 8568Y+   
  Uuid:                    CPU-XX                             
  Marketing Name:          INTEL(R) XEON(R) PLATINUM 8568Y+   
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
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            20                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    247409328(0xebf2ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    247409328(0xebf2ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    247409328(0xebf2ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    247409328(0xebf2ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-adaa93110835edcd               
  Marketing Name:          AMD Instinct MI300X VF             
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
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29877(0x74b5)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   33536                              
  Internal Node ID:        1                                  
  Compute Unit:            304                                
  SIMDs per CU:            4                                  
  Shader Engines:          32                                 
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
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 177                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    200998912(0xbfb0000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    200998912(0xbfb0000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    200998912(0xbfb0000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
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

### Operating System

Ubuntu 24.04

### CPU

NA

### GPU

AMD MI300x

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

```
sudo rocm-smi --setpoweroverdrive 500

============================ ROCm System Management Interface ============================
================================ Set GPU Power OverDrive =================================
ERROR: GPU[0]   : Unable to set Power OverDrive to 500W
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (17 条)

### 评论 #1 — ppanchad-amd (2025-08-28T14:29:24Z)

Hi @kev-pebble. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — harkgill-amd (2025-08-28T18:15:38Z)

Hi @kev-pebble, noticed your GPU is a `AMD Instinct MI300X VF`. Could you please share some more information regarding your virtualization config/setup?

We're still working towards enabling power cap management on Linux Guest platforms with https://github.com/ROCm/amdsmi/commit/2d5accd000400fcc7e8cca8409960ac35b0c3f86 and https://github.com/ROCm/amdsmi/commit/4ffa468613c8d620ca5335051ca5d00622df0135 being the first in a line of upcoming changes necessary for this feature.

---

### 评论 #3 — harkgill-amd (2025-11-21T18:00:34Z)

Hi @kev-pebble, this feature (adjusting power cap on Linux guest platforms) was implemented in ROCm 7.1. Closing this out but feel free to leave a comment if you're seeing any issues with this on the latest ROCm release.

---

### 评论 #4 — kev-pebble (2026-01-09T20:45:58Z)

@harkgill-amd We verified we are on `ROCm 7.1` and using `MI300X` but still not able to adjust power cap or setclk frequencies. 

```
# Set SCLK (System Clock) range: min 1000MHz, max 2100MHz
sudo rocm-smi --setsrange 1000 2100 --device 0

# Set MCLK (Memory Clock) range: min 800MHz, max 1200MHz
sudo rocm-smi --setmrange 800 1200 --device 0

GPU[0]          : set_gpu_clk_freq_mclk, Not supported on the given system 
```

`rocm-smi --setpoweroverdrive 200` doesn't work either.  Please re-open the issue and look into it. 


---

### 评论 #5 — harkgill-amd (2026-01-09T21:01:32Z)

Could you please share the output of `amd-smi` and `dmesg | grep amdgpu` logs?

---

### 评论 #6 — sachin-gopebble (2026-01-09T21:12:49Z)

> Could you please share the output of `amd-smi` and `dmesg | grep amdgpu` logs?

posting the output on behalf of @kev-pebble 

**Output of `amd-smi`**
```
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.0+021c61fc      amdgpu version: 6.16.6   ROCm version: 7.1.1    |
| VBIOS version: 00159017                                                      |
| Platform: Linux Guest                                                        |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:ff:00.0 AMD Instinct MI300X VF | 0 %      37 °C   0           141/750 W |
|   0       0       2        SPX/NPS1 | 0 %        N/A           285/196288 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```

**Output of `dmesg | grep amdgpu`**
[dmesg.log](https://github.com/user-attachments/files/24535657/dmesg.log)




---

### 评论 #7 — harkgill-amd (2026-01-09T21:36:43Z)

Could you also try the `amd-smi` specific version of the set power cap command?
```
sudo amd-smi set -o 500 -g 0
```

---

### 评论 #8 — sachin-gopebble (2026-01-09T21:45:00Z)

> Could you also try the `amd-smi` specific version of the set power cap command?
> 
> ```
> sudo amd-smi set -o 500 -g 0
> ```

```
amdsmi.amdsmi_exception.AmdSmiLibraryException: Error code:
	10 | AMDSMI_STATUS_NO_PERM - Permission Denied

The above exception was the direct cause of the following exception:

PermissionError: Command requires elevation
```

---

### 评论 #9 — kev-pebble (2026-01-14T00:56:03Z)

@harkgill-amd any updates on this? We weren't able to power cap / adjust clock frequency of MI300X GPUs. 

Do you think it would work on Bare Metal GPU cluster? Is there a way to enable power cap / adjust clock frequency on GPUs? 

---

### 评论 #10 — harkgill-amd (2026-01-14T16:22:15Z)

So the ability to adjust power cap on Linux guest systems did make it into ROCm 7.1.1, though it likely has a dependency on your systems BKC/firmware to run correctly. I'm still trying to iron out the exact details around this dependency - if you could share the BKC version you're currently using and any additional information about your system (OEM.etc) that would be helpful.

> Do you think it would work on Bare Metal GPU cluster? Is there a way to enable power cap / adjust clock frequency on GPUs?

Yes, the `sudo amd-smi set -o 500 -g 0` command should work on baremetal - this has always been available and is the recommended way to alter power cap values. It's the ability to do it on Linux Guest platforms which was recently introduced.

---

### 评论 #11 — sachin-gopebble (2026-01-14T17:08:54Z)

@harkgill-amd I don't see any BKC version.
Here's the output of 
**amd-smi version**
```
AMDSMI Tool: 26.2.0+021c61fc | AMDSMI Library version: 26.2.0 | ROCm version: 7.1.1 | amdgpu version: 6.16.6 | amd_hsmp version: N/A
```

**amd-smi firmware**
```
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_MEC1
            FW_VERSION: 32959
        FW 1:
            FW_ID: CP_MEC2
            FW_VERSION: 32959
        FW 2:
            FW_ID: RLC
            FW_VERSION: 69
        FW 3:
            FW_ID: SDMA0
            FW_VERSION: 25
        FW 4:
            FW_ID: SDMA1
            FW_VERSION: 25
        FW 5:
            FW_ID: VCN
            FW_VERSION: 09.11.80.15
        FW 6:
            FW_ID: RLC_RESTORE_LIST_GPM_MEM
            FW_VERSION: 4
        FW 7:
            FW_ID: RLC_RESTORE_LIST_SRM_MEM
            FW_VERSION: 4
        FW 8:
            FW_ID: RLC_RESTORE_LIST_CNTL
            FW_VERSION: 4
        FW 9:
            FW_ID: TA_RAS
            FW_VERSION: 1B.36.02.1A
        FW 10:
            FW_ID: TA_XGMI
            FW_VERSION: 20.00.00.14
        FW 11:
            FW_ID: PM
            FW_VERSION: 00.85.129.03
        FW 12:
            FW_ID: PLDM_BUNDLE
            FW_VERSION: 01.25.03.12

```

---

### 评论 #12 — sachin-gopebble (2026-01-14T19:07:30Z)

@harkgill-amd Here's some additional information.
The machine where the guest runs is a Dell PowerEdge XE9680 with baseboard bundle 01.25.03.12.76.

**Machine specification:**
Item | Description | Total
-- | -- | --
CPU | Your choice of Highest Core or Highest Clock Intel CPUs:◦ Intel® Xeon® Platinum 8470 2G, 52C/104T, 16GT/s, 105M Cache, Turbo, HT (350W)◦ Intel® Xeon® Platinum 8462Y+ 2.8G, 32C/64T, 16GT/s, 60M Cache, Turbo, HT (300W) | 52 core or 32 core
GPU | AMD MI300X 8-GPU OAM 192GB 750W GPUs [x8] | 1.5 TB HBM3
RAM | 64GB RDIMM, 4800MT/s Dual Rank [x32] | 2048 GB
DIsk | 15.36TB Enterprise NVMe Read Intensive AG Drive U.2 Gen4 [x8] | 122.88 TB
Network | Broadcom 57608 Dual Port 200G Q112 Adapter, PCIe Full Height [x8] | 8x 400G (3200 Gbps ROCEv2 Ethernet)
PDU | Geist NU30213 - 6 per rack for redundancy | 6x / rack



---

### 评论 #13 — harkgill-amd (2026-01-14T20:10:53Z)

Thanks, that's exactly what I needed. Could you also try setting the powercap on baremetal and confirm it works?

---

### 评论 #14 — harkgill-amd (2026-01-15T20:37:25Z)

From your output,
>
        FW 11:
            FW_ID: PM
            FW_VERSION: 00.85.129.03
        FW 12:
            FW_ID: PLDM_BUNDLE
            FW_VERSION: 01.25.03.12

You currently have the 25.03 BKC installed which provides PMFW 85.129 however, the new feature of altering power cap on Linux guest systems depends on PMFW 85.130.0. This should be available in an upcoming BKC released scheduled for release towards the end of next month - apologies for the confusion here.

---

### 评论 #15 — kev-pebble (2026-02-12T06:46:39Z)

@harkgill-amd we were able to confirm that power capping works on BareMetal Cluster. 

```
hotaisle@ENC1-CLS01-SVR07:~$ sudo amd-smi set -o 500 -g 0
GPU: 0
  POWERCAP: Successfully set power cap to 500W

hotaisle@ENC1-CLS01-SVR07:~$ rocm-smi


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device Node IDs       Temp    Power   Partitions     SCLK   MCLK  Fan Perf PwrCap VRAM% GPU%  
       (DID,   GUID) (Junction) (Socket) (Mem, Compute, ID)                          
==========================================================================================================================
0    2   0x74a1,  55354 47.0°C   178.0W  NPS1, SPX, 0    2106Mhz 900Mhz 0%  auto 500.0W 40%  0%   
1    3   0x74a1,  41632 39.0°C   181.0W  NPS1, SPX, 0    2113Mhz 900Mhz 0%  auto 750.0W 40%  0%   
2    4   0x74a1,  47045 42.0°C   170.0W  NPS1, SPX, 0    2100Mhz 900Mhz 0%  auto 750.0W 40%  0%   
3    5   0x74a1,  60169 47.0°C   191.0W  NPS1, SPX, 0    2100Mhz 900Mhz 0%  auto 750.0W 40%  0%   
4    6   0x74a1,  56024 46.0°C   193.0W  NPS1, SPX, 0    2106Mhz 900Mhz 0%  auto 750.0W 40%  0%   
5    7   0x74a1,  705  40.0°C   184.0W  NPS1, SPX, 0    2105Mhz 900Mhz 0%  auto 750.0W 40%  0%   
6    8   0x74a1,  59108 49.0°C   194.0W  NPS1, SPX, 0    2102Mhz 900Mhz 0%  auto 750.0W 40%  0%   
7    9   0x74a1,  10985 41.0°C   176.0W  NPS1, SPX, 0    2100Mhz 900Mhz 0%  auto 750.0W 40%  0%   
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
```

---

### 评论 #16 — sachin-gopebble (2026-03-23T14:44:33Z)



> From your output,
> 
> > 
> 
> ```
>     FW 11:
>         FW_ID: PM
>         FW_VERSION: 00.85.129.03
>     FW 12:
>         FW_ID: PLDM_BUNDLE
>         FW_VERSION: 01.25.03.12
> ```
> 
> You currently have the 25.03 BKC installed which provides PMFW 85.129 however, the new feature of altering power cap on Linux guest systems depends on PMFW 85.130.0. This should be available in an upcoming BKC released scheduled for release towards the end of next month - apologies for the confusion here.

@harkgill-amd Was there any firmware release made to support the power cap of GPUs on virtual machines?

---

### 评论 #17 — harkgill-amd (2026-03-23T18:16:27Z)

Hey @sachin-gopebble, the firmware/BKC release got pushed out - current target is for release mid next week. Will update this thread once it's been released.

---
