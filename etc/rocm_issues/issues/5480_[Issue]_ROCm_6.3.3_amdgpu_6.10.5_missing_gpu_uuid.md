# [Issue]: ROCm 6.3.3 / amdgpu 6.10.5 missing gpu uuid

> **Issue #5480**
> **状态**: closed
> **创建时间**: 2025-10-08T08:26:05Z
> **更新时间**: 2025-11-17T16:43:19Z
> **关闭时间**: 2025-11-17T16:43:19Z
> **作者**: torehl
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5480

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Problem:  ROCm 6.3.3 w/amdgpu 6.10.5

root@n016:~# rocm-smi --showuniqueid

============================ ROCm System Management Interface ============================
======================================= Unique ID ========================================
GPU[0]		: Unique ID: N/A
GPU[1]		: Unique ID: N/A
==========================================================================================
================================== End of ROCm SMI Log ===================================


### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD EPYC 7763 64-Core Processor

### GPU

2 qty AMD Instinct Mi210 (gfx90a)

### ROCm Version

ROCm 6.3.3

### ROCm Component

rocm_smi_lib

### Steps to Reproduce

AMD ROCm 6.3.3 w/ amdgpu 6.10.5  rocm-smi --showuniqueid   do not return uui for cards


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

`root@n016:~# /opt/rocm/bin/rocminfo --support
ROCk module is loaded
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
DMAbuf Support:          NO

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD EPYC 7763 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7763 64-Core Processor    
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
  Max Clock Freq. (MHz):   2450                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            128                                
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    1044302628(0x3e3ecb24) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    1044302628(0x3e3ecb24) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1044302628(0x3e3ecb24) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    1044302628(0x3e3ecb24) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 7763 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7763 64-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2450                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            128                                
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    1056867340(0x3efe840c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    1056867340(0x3efe840c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1056867340(0x3efe840c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    1056867340(0x3efe840c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-67c63ac3c3c637f9               
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   768                                
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 92                                 
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 4                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-7b6b270993774982               
  Marketing Name:          AMD Instinct MI210                 
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   33536                              
  Internal Node ID:        3                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 92                                 
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***       `

### Additional Information

NA

---

## 评论 (15 条)

### 评论 #1 — torehl (2025-10-08T08:27:28Z)

Is this fixed in later versions of ROCm > 6.3.3?

---

### 评论 #2 — harkgill-amd (2025-10-08T15:01:00Z)

Hi @torehl, are you able to see GPU's listed with the generic `rocm-smi` command? Just trying to narrow down whether this is an issue with `--showuniqueid` or with GPU visibility in general. 

Could you also try the relevant amd-smi command as well -> `amd-smi list`. 

---

### 评论 #3 — chandujr (2025-10-09T19:46:08Z)

> Hi [@torehl](https://github.com/torehl), are you able to see GPU's listed with the generic `rocm-smi` command? Just trying to narrow down whether this is an issue with `--showuniqueid` or with GPU visibility in general.

In my case, this is the output of `rocm-smi`:
```
Exception caught: map::at
========================================== ROCm System Management Interface ==========================================
==================================================== Concise Info ====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK  MCLK     Fan  Perf  PwrCap       VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                      
======================================================================================================================
0       1     0x73df,   45052  46.0°C  7.0W   N/A, N/A, 0         0Mhz  96Mhz    0%   auto  130.0W       0%     0%    
1       2     0x1638,   54183  54.0°C  29.0W  N/A, N/A, 0         None  1600Mhz  0%   auto  Unsupported  95%    1%    
======================================================================================================================
================================================ End of ROCm SMI Log =================================================
```

`rocminfo` output is:
```
OCk module is loaded
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
...
...
*******                  
Agent 2                  
*******                  
  Name:                    gfx1031                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 6800M                
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
...
...
*******                  
Agent 3                  
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
  Node:                    2                                  
  Device Type:             GPU
...
...
```

---

### 评论 #4 — harkgill-amd (2025-10-09T20:04:42Z)

@chandujr, are you sharing this information as you're seeing the same `N/A` uuid from rocm-smi or as an extension of https://github.com/ROCm/ROCm/issues/2941#issuecomment-3386957719? If it's the latter, please open a new issue [here](https://github.com/ROCm/rocm-systems/issues/new?template=issue_report.yml).

---

### 评论 #5 — 2maz (2025-10-10T15:17:58Z)

@harkgill-amd (to answer for @torehl)
```
$> rocm-smi --showuniqueid


============================ ROCm System Management Interface ============================
======================================= Unique ID ========================================
GPU[0]		: Unique ID: N/A
GPU[1]		: Unique ID: N/A
==========================================================================================
================================== End of ROCm SMI Log ===================================

$> rocm-smi
========================================= ROCm System Management Interface =========================================
=================================================== Concise Info ===================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                   
====================================================================================================================
0       2     0x740f,   22303  42.0°C  39.0W  N/A, N/A, 0         800Mhz  1600Mhz  0%   auto  300.0W  32%    0%    
1       3     0x740f,   31706  30.0°C  40.0W  N/A, N/A, 0         800Mhz  1600Mhz  0%   auto  300.0W  0%     0%    
====================================================================================================================
=============================================== End of ROCm SMI Log ================================================


$> amd-smi list
GPU: 0
    BDF: 0000:03:00.0
    UUID: 00ff740f-0000-1000-8000-000000000000
    KFD_ID: 22303
    NODE_ID: 2
    PARTITION_ID: 0

GPU: 1
    BDF: 0000:83:00.0
    UUID: 00ff740f-0000-1000-8000-000000000000
    KFD_ID: 31706
    NODE_ID: 3
    PARTITION_ID: 0
```

---

### 评论 #6 — chandujr (2025-10-12T10:27:05Z)

> [@chandujr](https://github.com/chandujr), are you sharing this information as you're seeing the same `N/A` uuid from rocm-smi or as an extension of [#2941 (comment)](https://github.com/ROCm/ROCm/issues/2941#issuecomment-3386957719)? If it's the latter, please open a new issue [here](https://github.com/ROCm/rocm-systems/issues/new?template=issue_report.yml).

No, that was was a different issue. As I mentioned in that thread, that issue got resolved. But I still have this missing unique ID issue in rocm-smi.

This is the part of the output when I do `dnf list --installed | grep rocm`:
```
...
...
rocm-rpm-macros.noarch                                6.3.1-5.fc42                                nobara
rocm-rpm-macros-modules.noarch                        6.3.1-5.fc42                                nobara
rocm-runtime.x86_64                                   6.3.1-4.fc42                                nobara
rocm-runtime-devel.x86_64                             6.3.1-4.fc42                                nobara
rocm-smi.x86_64                                       6.3.1-3.fc42                                nobara
rocminfo.x86_64                                       6.3.0-2.fc42                                nobara
```

---

### 评论 #7 — torehl (2025-10-13T08:10:03Z)

Can anyone confirm if this is fixed in 6.4.3? What about 7.0.2?


---

### 评论 #8 — harkgill-amd (2025-10-14T13:46:11Z)

We do have a few fixes regarding duplicate/NA UUID values in ROCm 7.0+. https://github.com/ROCm/amdsmi/commit/01a6158c85108f910fc5205dfd78710238e5a42d specifically resolves an issue where duplicate UUIDs are reported when `amd-smi list` is ran without `sudo` as you don't have access to the real values. Could you confirm if this is the issue you're encountering by running `sudo amd-smi list | grep UUID` and checking if the values differ for each GPU?

https://github.com/ROCm/amdsmi/commit/b58625cafa74f72d04edf1c86cdc1917549f015f and https://github.com/ROCm/amdsmi/commit/817c077067ec00f8fc2a9394a91bdf3623cca7ab are the other patches pertaining to your dup UUIDs though these seem to be more related to partitioned GPUs. Will confirm with the amdsmi team in parallel whether these are applicable to your usecase.

---

### 评论 #9 — torehl (2025-10-14T18:06:49Z)

@harkgill-amd 

They are as Thomas reported the same.

torel@n016:~$ module load amd/rocm/6.3.3 
torel@n016:~$ sudo amd-smi list | grep UUID
[sudo] password for torel: 
    UUID: 00ff740f-0000-1000-8000-000000000000
    UUID: 00ff740f-0000-1000-8000-000000000000

torel@n016:~$ amd-smi list
GPU: 0
    BDF: 0000:03:00.0
    UUID: 00ff740f-0000-1000-8000-000000000000
    KFD_ID: 22303
    NODE_ID: 2
    PARTITION_ID: 0

GPU: 1
    BDF: 0000:83:00.0
    UUID: 00ff740f-0000-1000-8000-000000000000
    KFD_ID: 31706
    NODE_ID: 3
    PARTITION_ID: 0


---

### 评论 #10 — torehl (2025-10-15T12:46:55Z)

I hope you find this info useful.  - For some other reason I removed one Mi210, the uuid is correct!!! 

I reconfigured my POD with 1 qty Mi210 and 1 qty A100, instead of 2 Mi210's. 

torel@n016:~$ lspci | egrep -i -e "nvidia|display"
03:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Aldebaran (rev 02)
81:00.0 3D controller: NVIDIA Corporation GA100 [A100 PCIe 40GB] (rev a1)

torel@n016:~$ module load amd/rocm/6.3.3 

torel@n016:~$ amd-smi list
GPU: 0
    BDF: 0000:03:00.0
    UUID: 67ff740f-0000-1000-80c6-3ac3c3c637f9
    KFD_ID: 12261
    NODE_ID: 2
    PARTITION_ID: 0

torel@n016:~$ rocm-smi --showuniqueid

============================ ROCm System Management Interface ============================
======================================= Unique ID ========================================
GPU[0]		: Unique ID: 0x67c63ac3c3c637f9
==========================================================================================
================================== End of ROCm SMI Log ===================================



---

### 评论 #11 — chandujr (2025-10-15T16:51:19Z)

@harkgill-amd I tried with sudo but the output is the same.

---

### 评论 #12 — harkgill-amd (2025-10-16T21:18:32Z)

@torehl, can you swap the second MI210 back into your system and see if the UUIDs are still `N/A`? I'm curious to see if the issue is persistent across reboots as well. If this does end up being the case, I'd suggest updating to ROCm 7.0.2. It'll be easer to debug there once we can rule out all the issues that have already been patched surrounding UUIDs.

I did also notice that `rocminfo` is still outputting UUIDs for both GPUs in your initial report.
```
Uuid: GPU-67c63ac3c3c637f9
Marketing Name: AMD Instinct MI210
```
You can query this is as a workaround but it'd be best to see if the issue persists in ROCm 7.0.2 (w/corresponding amdgpu driver) and root cause it within the SMI tools.

---

### 评论 #13 — torehl (2025-10-22T16:31:23Z)

@harkgill-amd  Will do once we are done with benchmarking.

---

### 评论 #14 — torehl (2025-11-17T15:27:09Z)

@harkgill-amd  Sorry for the delay.  

Back to previous config. But now with linux-hwe 6.8 kernel (due to better support for perf counters ++).  Looks like microcode has changed, and of course, a few Ubuntu security updates have gone in. 


```


xxx@n016:~$ uname -ar
Linux n016 6.8.0-87-generic #88~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Tue Oct 14 14:03:14 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

xxx@n016:~$ sudo dmesg |grep "amdgpu version:"
[sudo] password for xxx: 
[   38.689929] [drm] amdgpu version: 6.10.5


xxx@n016:~$ module load amd/rocm/6.3.3 
xxx@n016:~$ rocm-smi --showproductname

============================ ROCm System Management Interface ============================
====================================== Product Info ======================================
GPU[0]		: Card Series: 		Instinct MI210
GPU[0]		: Card Model: 		0x740f
GPU[0]		: Card Vendor: 		Advanced Micro Devices, Inc. [AMD/ATI]
GPU[0]		: Card SKU: 		D67301
GPU[0]		: Subsystem ID: 	0x0c34
GPU[0]		: Device Rev: 		0x02
GPU[0]		: Node ID: 		2
GPU[0]		: GUID: 		12261
GPU[0]		: GFX Version: 		gfx90a
GPU[1]		: Card Series: 		Instinct MI210
GPU[1]		: Card Model: 		0x740f
GPU[1]		: Card Vendor: 		Advanced Micro Devices, Inc. [AMD/ATI]
GPU[1]		: Card SKU: 		D67301
GPU[1]		: Subsystem ID: 	0x0c34
GPU[1]		: Device Rev: 		0x02
GPU[1]		: Node ID: 		3
GPU[1]		: GUID: 		36740
GPU[1]		: GFX Version: 		gfx90a
==========================================================================================
================================== End of ROCm SMI Log ===================================

xxx@n016:~$ rocm-smi --showuniqueid

============================ ROCm System Management Interface ============================
======================================= Unique ID ========================================
GPU[0]		: Unique ID: 0x67c63ac3c3c637f9
GPU[1]		: Unique ID: 0x95a1ca7691e7c391
==========================================================================================
================================== End of ROCm SMI Log ===================================

xxx@n016:~$ amd-smi list
GPU: 0
    BDF: 0000:03:00.0
    UUID: 67ff740f-0000-1000-80c6-3ac3c3c637f9
    KFD_ID: 12261
    NODE_ID: 2
    PARTITION_ID: 0

GPU: 1
    BDF: 0000:83:00.0
    UUID: 95ff740f-0000-1000-80a1-ca7691e7c391
    KFD_ID: 36740
    NODE_ID: 3
    PARTITION_ID: 0

```

Seems to work fine now.  Must have been 5.15.0-161-generic specific issue?  


---

### 评论 #15 — harkgill-amd (2025-11-17T16:43:19Z)

No worries, thanks for getting back. 

> Must have been 5.15.0-161-generic specific issue?

Could be though I'm leaning more towards an intermittent issue fetching the UUIDs that was resolved with a reboot - a lot of these UUID related issues have been addressed in newer releases. In any case, as the issue is resolved on your end, I'll close this one out. If you do encounter the issue again, feel free to leave a comment and I'll re-open this ticket for further investigation.

---
