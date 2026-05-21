# [Issue]: dkms failed for running kernel

> **Issue #3883**
> **状态**: closed
> **创建时间**: 2024-10-11T13:10:10Z
> **更新时间**: 2024-10-11T19:15:50Z
> **关闭时间**: 2024-10-11T19:15:50Z
> **作者**: Loungagna
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3883

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

I get:

dkms is already the newest version (3.0.11-1ubuntu13).
amdgpu-lib is already the newest version (1:6.1.60102-1781449.22.04).
rocm-opencl-runtime is already the newest version (6.2.1.60201-112~22.04).
rocm-hip-runtime is already the newest version (6.2.1.60201-112~22.04).
amdgpu-dkms is already the newest version (1:6.7.0.60102-1781449.22.04).
The following additional packages will be installed:
  linux-headers-6.8.0-45
The following NEW packages will be installed:
  linux-headers-6.8.0-45 linux-headers-6.8.0-45-generic
0 upgraded, 2 newly installed, 0 to remove and 8 not upgraded.
Need to get 17.7 MB of archives.
After this operation, 115 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://us.archive.ubuntu.com/ubuntu noble-updates/main amd64 linux-headers-6.8.0-45 all 6.8.0-45.45 [13.7 MB]
Get:2 http://us.archive.ubuntu.com/ubuntu noble-updates/main amd64 linux-headers-6.8.0-45-generic amd64 6.8.0-45.45 [3969 kB]
Fetched 17.7 MB in 0s (59.6 MB/s)
Selecting previously unselected package linux-headers-6.8.0-45.
(Reading database ... 296350 files and directories currently installed.)
Preparing to unpack .../linux-headers-6.8.0-45_6.8.0-45.45_all.deb ...
Unpacking linux-headers-6.8.0-45 (6.8.0-45.45) ...
Selecting previously unselected package linux-headers-6.8.0-45-generic.
Preparing to unpack .../linux-headers-6.8.0-45-generic_6.8.0-45.45_amd64.deb ...
Unpacking linux-headers-6.8.0-45-generic (6.8.0-45.45) ...
Setting up linux-headers-6.8.0-45 (6.8.0-45.45) ...
Setting up linux-headers-6.8.0-45-generic (6.8.0-45.45) ...
/etc/kernel/header_postinst.d/dkms:
 * dkms: running auto installation service for kernel 6.8.0-45-generic
 * dkms: autoinstall for kernel 6.8.0-45-generic
   ...done.
WARNING: amdgpu dkms failed for running kernel

and I cannot then get any quantizer installed for fine-tuning my LLM.

### Operating System

24.04.1 LTS

### CPU

AMD Ryzen 7 7840HS w/ Radeon 780M Graphics

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

sudo amdgpu-install dkms

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5137                               
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
      Size:                    32147688(0x1ea88e8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32147688(0x1ea88e8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32147688(0x1ea88e8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
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
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           9(0x9)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   50176                              
  Internal Node ID:        2                                  
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
  Packet Processor uCode:: 35                                 
  SDMA engine uCode::      17                                 
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
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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


### Additional Information

My GPU is AMD Ryzen 7 7840HS w/ Radeon 780M Graphics

---

## 评论 (7 条)

### 评论 #1 — harkgill-amd (2024-10-11T13:29:35Z)

Hi @Loungagna, there is a known issue building amdgpu-dkms with ROCm 6.2.0+linux kernel 6.8.0-45 which is resolved in ROCm 6.2.1. Could you try either upgrading your ROCm version or downgrading your linux kernel to 6.8.0-41 and confirm if you still see the build failure?

---

### 评论 #2 — Loungagna (2024-10-11T14:46:45Z)

I'm running rocm 6.2.1 (and same issue happened with rocm 6.2.2 BTW).

The issue report form proposes only 6.2.0 in the dropdown. I should have been more explicit. I apologize.

You could see in my issue report these lines:
rocm-opencl-runtime is already the newest version (**6.2.1**.60201-11222.04).
rocm-hip-runtime is already the newest version (**6.2.1**.60201-11222.04).

---

### 评论 #3 — harkgill-amd (2024-10-11T14:59:38Z)

No worries, I'll get the dropdown updated so this doesn't happen in the future. Could you please provide the ouptut of `sudo dkms status` and `ls /var/lib/dkms/amdgpu/`?

---

### 评论 #4 — Loungagna (2024-10-11T16:07:31Z)

sudo dkms status does not return anything.


ls /var/lib/dkms/amdgpu/
"/var/lib/dkms/amdgpu/": No such file or directory (os error 2)

---

### 评论 #5 — harkgill-amd (2024-10-11T16:47:48Z)

Upon further inspection, it looks like your `amdgpu` and `rocm` packages point to different ROCm versions (6.1.2 vs 6.2.1). 

rocm-opencl-runtime is already the newest version (6.2.1.**60201**-11222.04)
amdgpu-dkms is already the newest version (1:6.7.0.**60102**-1781449.22.04).

Could you please remove the existing packages and amdgpu-install with the following commands
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then reinstall ROCm 6.2.2 (For Ubuntu 24.04)
```
wget https://repo.radeon.com/amdgpu-install/6.2.2/ubuntu/noble/amdgpu-install_6.2.60202-1_all.deb
sudo apt install ./amdgpu-install_6.2.60202-1_all.deb
sudo apt update
sudo amdgpu-install --usecase=rocm
```
This will install the correct DKMS package for the 6.8.0-45 kernel.

---

### 评论 #6 — Loungagna (2024-10-11T19:02:54Z)

Thank you. This now shows an active dkms.

---

### 评论 #7 — harkgill-amd (2024-10-11T19:15:50Z)

My pleasure! Will close out this issue.

---
