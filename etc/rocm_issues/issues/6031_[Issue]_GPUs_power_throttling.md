# [Issue]: GPUs power throttling

> **Issue #6031**
> **状态**: open
> **创建时间**: 2026-03-11T12:26:23Z
> **更新时间**: 2026-03-20T15:42:33Z
> **作者**: ewindisch
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6031

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

GPUs do not scale beyond 80W limiting throughput.

### Operating System

Proxmox 9.1.1 (Debian 13 base)

### CPU

Intel(R) Core(TM) Ultra 9 285K

### GPU

AMD Instinct mi210

### ROCm Version

ROCm 7.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

/opt/rocm-7.2.0/bin$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.16.13 is loaded
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
  Name:                    Intel(R) Core(TM) Ultra 9 285K     
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) Ultra 9 285K     
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
  Compute Unit:            18                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    64295012(0x3d51064) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    64295012(0x3d51064) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    64295012(0x3d51064) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    64295012(0x3d51064) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-327c8626c83ec858               
  Marketing Name:          AMD Instinct MI210                 
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
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   256                                
  Internal Node ID:        1                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 96                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
  Name:                    gfx90a                             
  Uuid:                    GPU-753ef2efdc04e86d               
  Marketing Name:          AMD Instinct MI210                 
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
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   512                                
  Internal Node ID:        2                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 96                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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

### Additional Information

ASPM disabled in BIOS.

Running the validation suite (RVS):

+=====================================================================+
|                 ROCm Validation Suite (RVS) Summary                 |
+=====================================================================+
|                           System Overview                           |
+---------------------------------------------------------------------+
| Operating System                 | Debian GNU/Linux 12              |
| RVS version                      | 1.3.0                            |
| ROCm version                     | 7.2.0-43                         |
| amdgpu version                   | N/A                              |
| GPUs                             | 2                                |
+---------------------------------------------------------------------+
| GPU Name - GPU ID                |                                  |
| ID - Node ID - BDF               |                                  |
+---------------------------------------------------------------------+
| AMD Instinct MI210 - 20068       | AMD Instinct MI210 - 48932       |
| 0 - 1 - 0000:01:00.0             | 1 - 2 - 0000:02:00.0             |
+=====================================================================+
| Action Name                      | Module         | Result          |
+=====================================================================+
| action_1                         | GPUP           | PASS            |
| action_2                         | PEQT           | PASS            |
| action_3                         | PEBB           | PASS            |
| action_4                         | PBQT           | PASS            |
| action_5                         | IET            | FAIL            |
| action_6                         | GST            | FAIL            |
| action_7                         | BABEL          | PASS            |
| action_8                         | MEM            | PASS            |
| action_9                         | PESM           | PASS            |
+---------------------------------------------------------------------+
[RESULT] [   521.259539] [module_terminate] PCIe monitoring ended after wait duration.

[RESULT] [   356.416045] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   357.416583] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   357.416603] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   358.417136] [action_5] [GPU:: 48932] Power(W) 78.000000
[RESULT] [   358.417152] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   359.417652] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   359.417671] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   360.418175] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   360.418177] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   361.418721] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   361.418733] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   362.419176] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   362.419180] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   363.419791] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   363.419796] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   364.420317] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   364.420318] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   365.420849] [action_5] [GPU:: 20068] Power(W) 79.000000
[RESULT] [   365.420863] [action_5] [GPU:: 48932] Power(W) 77.000000
[RESULT] [   365.504184] [action_5] [GPU:: 48932] pass: FALSE
[RESULT] [   365.538665] [action_5] [GPU:: 20068] pass: FALSE
RVS-ERROR [iet] [action_5] Action failed to run successfully.

---

## 评论 (8 条)

### 评论 #1 — ewindisch (2026-03-11T13:33:06Z)

Just for completeness sake as I've tried most things I can via software, I tried a brand new power supply with no luck (both PSU were 1200W).

---

### 评论 #2 — ewindisch (2026-03-11T16:39:56Z)

```$ rocm-smi --showhw


WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

===================================== ROCm System Management Interface =====================================
========================================== Concise Hardware Info ===========================================
GPU  NODE  DID     GUID   GFX VER  GFX RAS  SDMA RAS  UMC RAS  VBIOS            BUS           PARTITION ID  
0    1     0x740f  20068  gfx90a   ENABLED  ENABLED   ENABLED  113-D67301V-075  0000:01:00.0  0             
1    2     0x740f  48932  gfx90a   ENABLED  ENABLED   ENABLED  113-D67301V-075  0000:02:00.0  0             
============================================================================================================
=========================================== End of ROCm SMI Log ============================================```

I've updated the VBIOS on both cards, but the voltages are still limited.

---

### 评论 #3 — darren-amd (2026-03-19T19:07:17Z)

Hi @ewindisch,

Thanks for reporting the issue! I was able to reproduce something similar on an older amdgpu version where my wattage capped out around 140W. However, [updating amdgpu](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#amdgpu-driver-installation) fixed the problem and I'm getting near the theoretical maximum now:
```
[RESULT] [ 71784.891317] [action_5] [GPU:: 20602] Power(W) 46.000000
[RESULT] [ 71785.892093] [action_5] [GPU:: 20602] Power(W) 133.000000
[RESULT] [ 71786.892572] [action_5] [GPU:: 20602] Power(W) 206.000000
[RESULT] [ 71787.893035] [action_5] [GPU:: 20602] Power(W) 250.000000
[RESULT] [ 71788.893546] [action_5] [GPU:: 20602] Power(W) 269.000000
[RESULT] [ 71789.894057] [action_5] [GPU:: 20602] Power(W) 278.000000
[RESULT] [ 71790.894535] [action_5] [GPU:: 20602] Power(W) 288.000000
[RESULT] [ 71791.895153] [action_5] [GPU:: 20602] Power(W) 289.000000
[RESULT] [ 71792.895609] [action_5] [GPU:: 20602] Power(W) 288.000000
[RESULT] [ 71793.896327] [action_5] [GPU:: 20602] Power(W) 294.000000
[RESULT] [ 71794.896842] [action_5] [GPU:: 20602] Power(W) 296.000000
[RESULT] [ 71795.897317] [action_5] [GPU:: 20602] Power(W) 298.000000
[RESULT] [ 71796.898035] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71797.898888] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71798.899426] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71799.900132] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71800.900603] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71801.901544] [action_5] [GPU:: 20602] Power(W) 296.000000
[RESULT] [ 71802.902269] [action_5] [GPU:: 20602] Power(W) 297.000000
[RESULT] [ 71803.902965] [action_5] [GPU:: 20602] Power(W) 293.000000
[RESULT] [ 71804.903641] [action_5] [GPU:: 20602] Power(W) 296.000000
[RESULT] [ 71805.904170] [action_5] [GPU:: 20602] Power(W) 293.000000
[RESULT] [ 71806.904759] [action_5] [GPU:: 20602] Power(W) 296.000000
[RESULT] [ 71807.905235] [action_5] [GPU:: 20602] Power(W) 293.000000
[RESULT] [ 71808.905890] [action_5] [GPU:: 20602] Power(W) 296.000000
[RESULT] [ 71809.906361] [action_5] [GPU:: 20602] Power(W) 294.000000
[RESULT] [ 71810.906936] [action_5] [GPU:: 20602] Power(W) 296.000000
[RESULT] [ 71811.907674] [action_5] [GPU:: 20602] Power(W) 294.000000
[RESULT] [ 71812.908322] [action_5] [GPU:: 20602] Power(W) 296.000000
[RESULT] [ 71813.908797] [action_5] [GPU:: 20602] Power(W) 295.000000
[RESULT] [ 71814.909415] [action_5] [GPU:: 20602] Power(W) 297.000000
[RESULT] [ 71815.909855] [action_5] [GPU:: 20602] Power(W) 298.000000
[RESULT] [ 71816.910501] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71817.910935] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71818.911578] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71819.912050] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71820.912902] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71821.913416] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71822.913886] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71823.914556] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71824.915050] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71825.915653] [action_5] [GPU:: 20602] Power(W) 299.000000
[RESULT] [ 71825.928461] [action_5] [GPU:: 20602] pass: TRUE
```
Could you please give that a try and let me know if you run into any issues? Please make sure to remove older amdgpu driver versions before updating, thanks!

---

### 评论 #4 — ewindisch (2026-03-19T19:18:58Z)

```
wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/jammy/amdgpu-install_7.2.70200-1_all.deb
sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
sudo apt update
sudo apt install "linux-headers-$(uname -r)"
sudo apt install amdgpu-dkms
```

I was already on a 7.2 release, but there was a minor update. I applied it and rebooted, but I am still throttled to 55W on both GPUs.


---

### 评论 #5 — darren-amd (2026-03-19T19:23:57Z)

Could I get the output of `amd-smi`, `dkms status`, and `apt list | grep amdgpu`? Also could you try setting the power cap with `amd-smi set -o 300`?

---

### 评论 #6 — ewindisch (2026-03-19T19:36:01Z)

Note this is in a guest VM. The virtual machine host has the same version of amdgpu. I have included results from both for the package versions. With PCIe passthrough, the host does not see the cards unless the VM is shut down.

## guest

```
$ amd-smi
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.1+fc0010cf6a    amdgpu version: 6.16.13  ROCm version: 7.2.0    |
| VBIOS version: 625576                                                        |
| Platform: Linux Guest (Passthrough)                                          |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:01:00.0     AMD Instinct MI210 | 0 %      37 °C   0            33/300 W |
|   0       0     N/A             N/A | 0 %        N/A             10/65520 MB |
|-------------------------------------+----------------------------------------|
| 0000:02:00.0     AMD Instinct MI210 | 0 %      31 °C   0            32/300 W |
|   1       1     N/A             N/A | 0 %        N/A             10/65520 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
birdetta@hypr1:~$ dkms status
-bash: dkms: command not found
birdetta@hypr1:~$ sudo dkms status
[sudo] password for birdetta: 
amdgpu/6.16.13-2278356.24.04, 6.1.0-43-amd64, x86_64: installed
birdetta@hypr1:~$ uname -a
Linux hypr1 6.1.0-43-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.162-1 (2026-02-08) x86_64 GNU/Linux
birdetta@hypr1:~$ apt list | grep amdgpu

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

amdgpu-core/noble,noble 1:7.2.70200-2278374.24.04 all [upgradable from: 1:7.2.70200-2278374.22.04]
amdgpu-dkms-firmware/noble,noble 30.30.0.0.30300000-2278356.24.04 all [upgradable from: 30.30.0.0.30300000-2278356.22.04]
amdgpu-dkms/noble,noble,now 1:6.16.13.30300000-2278356.24.04 all [installed]
amdgpu-doc/noble,noble 1:7.2-2278374.24.04 all
amdgpu-insecure-instinct-udev-rules/noble,noble 30.30.0.0-2278356.24.04 all
amdgpu-install/noble,noble,now 30.30.0.0.30300000-2278356.24.04 all [installed]
amdgpu-lib32/noble 1:7.2.70200-2278374.24.04 amd64
amdgpu-lib/noble 1:7.2.70200-2278374.24.04 amd64
amdgpu-multimedia/noble 1:7.2.70200-2278374.24.04 amd64
amdgpu/noble 1:7.2.70200-2278374.24.04 amd64
hsa-runtime-rocr4wsl-amdgpu/noble 25.30.13-2281980.24.04 amd64
libdrm-amdgpu-amdgpu1/noble 1:2.4.125.70200-2278374.24.04 amd64 [upgradable from: 1:2.4.125.70200-2278374.22.04]
libdrm-amdgpu-amdgpu1/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-common/noble,noble 1.0.0.70200-2278374.24.04 all [upgradable from: 1.0.0.70200-2278374.22.04]
libdrm-amdgpu-dev/noble 1:2.4.125.70200-2278374.24.04 amd64 [upgradable from: 1:2.4.125.70200-2278374.22.04]
libdrm-amdgpu-dev/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-radeon1/noble 1:2.4.125.70200-2278374.24.04 amd64 [upgradable from: 1:2.4.125.70200-2278374.22.04]
libdrm-amdgpu-radeon1/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-static/noble 1:2.4.125.70200-2278374.24.04 amd64
libdrm-amdgpu-static/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-utils/noble 1:2.4.125.70200-2278374.24.04 amd64
libdrm-amdgpu-utils/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu1/oldstable,now 2.4.114-1+b1 amd64 [installed,automatic]
libdrm2-amdgpu/noble 1:2.4.125.70200-2278374.24.04 amd64 [upgradable from: 1:2.4.125.70200-2278374.22.04]
libdrm2-amdgpu/noble 1:2.4.125.70200-2278374.24.04 i386
libegl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libegl1-amdgpu-mesa-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
libegl1-amdgpu-mesa/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa/noble 1:26.0.0.70200-2278374.24.04 i386
libgbm-amdgpu-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libgbm-amdgpu-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libgbm1-amdgpu/noble 1:26.0.0.70200-2278374.24.04 amd64
libgbm1-amdgpu/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-dri/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-dri/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-glx/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-glx/noble 1:26.0.0.70200-2278374.24.04 i386
libllvm20.1-amdgpu/noble 1:20.1.70200-2278374.24.04 amd64
libllvm20.1-amdgpu/noble 1:20.1.70200-2278374.24.04 i386
libwayland-amdgpu-bin/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-bin/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-client0/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-client0/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-cursor0/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-cursor0/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-dev/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-dev/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-doc/noble,noble 1.24.0.70200-2278374.24.04 all
libwayland-amdgpu-egl-backend-dev/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-egl-backend-dev/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-egl1/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-egl1/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-server0/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-server0/noble 1.24.0.70200-2278374.24.04 i386
llvm-amdgpu-20.1-dev/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-20.1-dev/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-20.1-runtime/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-20.1-runtime/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-20.1/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-20.1/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-dev/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-dev/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-runtime/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-runtime/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu/noble 1:20.1.70200-2278374.24.04 i386
mesa-amdgpu-common-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-common-dev/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-libgallium/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-libgallium/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-va-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-va-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-vulkan-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-vulkan-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
ricks-amdgpu-utils/oldstable 3.8.0-1 all
umr-amdgpu-dev/noble 0.0-2278374.24.04 amd64
umr-amdgpu/noble 0.0-2278374.24.04 amd64
umrlite-amdgpu-dev/noble 0.0-2278374.24.04 amd64
umrlite-amdgpu/noble 0.0-2278374.24.04 amd64
wayland-protocols-amdgpu/noble,noble 1.45.70200-2278374.24.04 all
xserver-xorg-video-amdgpu/oldstable 23.0.0-1 amd64
birdetta@hypr1:~$ amd-smi set -o 300
usage: amd-smi set [-h]
                   [-f % | -l LEVEL | -P PROFILE_LEVEL | -d SCLKMAX | -C TYPE/INDEX | -M PARTITION | -o PWR_TYPE WATTS | -p POLICY_ID | -x POLICY_ID | -c CLK_TYPE [PERF_LEVELS ...]
                   | -S STATUS | -F FRMT1,FRMT2 | -L CLK_TYPE LIM_TYPE VALUE | -R STATUS]
                   [-g GPU [GPU ...]] [--json | --csv] [--file FILE] [--loglevel LEVEL]
amd-smi set: error: argument -o/--power-cap: expected 2 arguments
birdetta@hypr1:~$ amd-smi set -o ppt0 300
GPU: 0
    POWERCAP: PPT0 power cap is already set to 300W

GPU: 1
    POWERCAP: PPT0 power cap is already set to 300W


birdetta@hypr1:~$ amd-smi set -o ppt1 300
GPU: 0
    POWERCAP: [AMDSMI_STATUS_NOT_SUPPORTED] Unable to set PPT1 power cap to 300W

GPU: 1
    POWERCAP: [AMDSMI_STATUS_NOT_SUPPORTED] Unable to set PPT1 power cap to 300W
```


## host

```
# apt list | grep amdgpu

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

amdgpu-core/noble,noble,now 1:7.2.70200-2278374.24.04 all [installed,automatic]
amdgpu-dkms-firmware/noble,noble,now 30.30.0.0.30300000-2278356.24.04 all [installed,automatic]
amdgpu-dkms/noble,noble,now 1:6.16.13.30300000-2278356.24.04 all [installed]
amdgpu-doc/noble,noble 1:7.2-2278374.24.04 all
amdgpu-insecure-instinct-udev-rules/noble,noble 30.30.0.0-2278356.24.04 all
amdgpu-install/noble,noble,now 30.30.0.0.30300000-2278356.24.04 all [installed]
amdgpu-lib32/noble 1:7.2.70200-2278374.24.04 amd64
amdgpu-lib/noble 1:7.2.70200-2278374.24.04 amd64
amdgpu-multimedia/noble 1:7.2.70200-2278374.24.04 amd64
amdgpu/noble 1:7.2.70200-2278374.24.04 amd64
hsa-runtime-rocr4wsl-amdgpu/noble 25.30.13-2281980.24.04 amd64
libdrm-amdgpu-amdgpu1/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]
libdrm-amdgpu-amdgpu1/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-common/noble,noble,now 1.0.0.70200-2278374.24.04 all [installed,automatic]
libdrm-amdgpu-dev/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]
libdrm-amdgpu-dev/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-radeon1/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]
libdrm-amdgpu-radeon1/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-static/noble 1:2.4.125.70200-2278374.24.04 amd64
libdrm-amdgpu-static/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu-utils/noble 1:2.4.125.70200-2278374.24.04 amd64
libdrm-amdgpu-utils/noble 1:2.4.125.70200-2278374.24.04 i386
libdrm-amdgpu1/stable,now 2.4.124-2 amd64 [installed,automatic]
libdrm2-amdgpu/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]
libdrm2-amdgpu/noble 1:2.4.125.70200-2278374.24.04 i386
libegl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libegl1-amdgpu-mesa-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
libegl1-amdgpu-mesa/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa/noble 1:26.0.0.70200-2278374.24.04 i386
libgbm-amdgpu-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libgbm-amdgpu-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libgbm1-amdgpu/noble 1:26.0.0.70200-2278374.24.04 amd64
libgbm1-amdgpu/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-dri/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-dri/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-glx/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-glx/noble 1:26.0.0.70200-2278374.24.04 i386
libllvm20.1-amdgpu/noble 1:20.1.70200-2278374.24.04 amd64
libllvm20.1-amdgpu/noble 1:20.1.70200-2278374.24.04 i386
libwayland-amdgpu-bin/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-bin/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-client0/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-client0/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-cursor0/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-cursor0/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-dev/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-dev/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-doc/noble,noble 1.24.0.70200-2278374.24.04 all
libwayland-amdgpu-egl-backend-dev/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-egl-backend-dev/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-egl1/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-egl1/noble 1.24.0.70200-2278374.24.04 i386
libwayland-amdgpu-server0/noble 1.24.0.70200-2278374.24.04 amd64
libwayland-amdgpu-server0/noble 1.24.0.70200-2278374.24.04 i386
llvm-amdgpu-20.1-dev/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-20.1-dev/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-20.1-runtime/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-20.1-runtime/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-20.1/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-20.1/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-dev/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-dev/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu-runtime/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu-runtime/noble 1:20.1.70200-2278374.24.04 i386
llvm-amdgpu/noble 1:20.1.70200-2278374.24.04 amd64
llvm-amdgpu/noble 1:20.1.70200-2278374.24.04 i386
mesa-amdgpu-common-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-common-dev/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-libgallium/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-libgallium/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-va-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-va-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-vulkan-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-vulkan-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
ricks-amdgpu-utils/stable 3.9.0-1 all
umr-amdgpu-dev/noble 0.0-2278374.24.04 amd64
umr-amdgpu/noble 0.0-2278374.24.04 amd64
umrlite-amdgpu-dev/noble 0.0-2278374.24.04 amd64
umrlite-amdgpu/noble 0.0-2278374.24.04 amd64
wayland-protocols-amdgpu/noble,noble 1.45.70200-2278374.24.04 all
xserver-xorg-video-amdgpu/stable 23.0.0-1 amd64
```

---

### 评论 #7 — ewindisch (2026-03-19T19:47:32Z)

Further host information. Normally I use other software and not ollama for testing, but we don't normally run our software on the host OS, and it was easy to get Ollama up for a quick benchmark.

# Host

```
$ amd-smi
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.1+fc0010cf6a    amdgpu version: 6.16.13  ROCm version: 7.2.0    |
| VBIOS version: 625576                                                        |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:04:00.0     AMD Instinct MI210 | 2 %      40 °C   0            57/300 W |
|   0       0     N/A             N/A | 100 %      N/A          40762/65520 MB |
|-------------------------------------+----------------------------------------|
| 0000:08:00.0     AMD Instinct MI210 | 0 %      32 °C   0            32/300 W |
|   1       1     N/A             N/A | 0 %        N/A             10/65520 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|    0    3880797  ollama                 7.9 MB   38.5 GB    39.8 GB    1.0 % |
|    1    3880797  ollama                 7.9 MB   38.5 GB    39.8 GB    1.0 % |
+------------------------------------------------------------------------------+
```

```
# dkms status
amdgpu/6.16.13-2278356.24.04, 6.17.2-2-pve, x86_64: installed (Original modules exist)

# uname -a
Linux mars 6.17.2-2-pve #1 SMP PREEMPT_DYNAMIC PMX 6.17.2-2 (2025-11-26T12:33Z) x86_64 GNU/Linux
```

---

### 评论 #8 — darren-amd (2026-03-20T15:41:38Z)

Thanks, could you run the validation suite again on the host and provide me with the full output as well as the `dmesg` log?

---
