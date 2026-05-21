# HSA API Call Failure in rocminfo.cc:1282 – HSA_STATUS_ERROR_OUT_OF_RESOURCES

> **Issue #4382**
> **状态**: open
> **创建时间**: 2025-02-16T03:10:02Z
> **更新时间**: 2026-04-04T23:28:07Z
> **作者**: connorblack
> **标签**: Under Investigation, AMD Radeon RX 7900XTX, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4382

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900XTX** (颜色: #ededed)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

![Image](https://github.com/user-attachments/assets/d24749c8-d98d-4e56-95c2-a836d5cb6976)

Error after fresh install of Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-131-generic x86_64). 

AMD installer runs fine, runtime error during post install steps, specifically when running `rocminfo`:
```
$ amdgpu-install --usecase=dkms,rocm,rocmdev,rocmdevtools,lrt,openclsdk,hip,hiplibsdk,openmpsdk,mllib,mlsdk,asan --install-recommends --install-suggests
Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
Hit:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease
Hit:3 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease
Hit:4 https://download.docker.com/linux/ubuntu jammy InRelease                                                                                  
Hit:5 https://repo.radeon.com/amdgpu/6.3.2/ubuntu jammy InRelease                                                                               
Hit:6 https://repo.radeon.com/rocm/apt/6.3.2 jammy InRelease                                                              
Hit:7 http://security.ubuntu.com/ubuntu jammy-security InRelease                                                          
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
linux-headers-5.15.0-131-generic is already the newest version (5.15.0-131.141).
amdgpu-dkms is already the newest version (1:6.10.5.60302-2109964.22.04).
rocm is already the newest version (6.3.2.60302-66~22.04).
rocm-asan is already the newest version (6.3.2.60302-66~22.04).
rocm-dev is already the newest version (6.3.2.60302-66~22.04).
rocm-developer-tools is already the newest version (6.3.2.60302-66~22.04).
rocm-hip-runtime is already the newest version (6.3.2.60302-66~22.04).
rocm-hip-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-language-runtime is already the newest version (6.3.2.60302-66~22.04).
rocm-ml-libraries is already the newest version (6.3.2.60302-66~22.04).
rocm-ml-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-opencl-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-openmp-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-utils is already the newest version (6.3.2.60302-66~22.04).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.

$ rocminfo
$ clinfo
ROCk module version 6.10.5 is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1282
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 0
```

### Operating System

Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-131-generic x86_64)

### CPU

11th Gen Intel(R) Core(TM) i9-11900K @ 3.50GHz

### GPU

Radeon RX 7900 XTX

### ROCm Version

6.3.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

`$ /opt/rocm/bin/rocminfo --support`
ROCk module version 6.10.5 is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1282
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

### Additional Information

_No response_

---

## 评论 (12 条)

### 评论 #1 — ppanchad-amd (2025-02-18T15:38:11Z)

Hi @connorblack. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-02-18T16:44:14Z)

Hi @connorblack, is that user added to the `render` and `video` groups? 

---

### 评论 #3 — connorblack (2025-02-21T17:39:15Z)

@schung-amd yes

```
$ rocminfo
ROCk module version 6.10.5 is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1282
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
$ groups
connor adm cdrom sudo dip video plugdev render lxd ollama
```

Since I posted this I've also tried to see if a fresh install/upgrade to ubuntu 24 might fix it but same exact issue.

---

### 评论 #4 — schung-amd (2025-02-21T20:31:28Z)

Thanks, I'll take a look and see if I can reproduce this.

---

### 评论 #5 — schung-amd (2025-03-04T20:49:33Z)

@connorblack Sorry for the delay on this, I haven't been able to reproduce this so far. Can you get output from `rocm-smi -a` or is that also broken?

---

### 评论 #6 — felipemarkson (2025-03-19T22:55:33Z)

I'm having a similar issue. It looks like an permission issue because I'm able to run as root but not as the user.

---

### 评论 #7 — schung-amd (2025-03-21T15:13:55Z)

@connorblack @felipemarkson Are you on baremetal or in a VM or Docker? We've found a reproducer with the rocm/rocm-terminal Docker image (launch command from https://github.com/ROCm/ROCm-docker), but I suspect the permissions issue there is in the Docker image and not sure at the moment how this can arise from a baremetal installation.

---

### 评论 #8 — felipemarkson (2025-03-21T15:14:55Z)

Baremetal, Debian 12

---

### 评论 #9 — schung-amd (2025-03-21T15:22:46Z)

@felipemarkson Thanks for the quick response! Can you provide the output of `ls -la /dev/dri` and `groups`? Also, what steps did you take to install ROCm?

---

### 评论 #10 — cw-koh (2025-03-29T13:49:05Z)

This problem happens to me too,
It usually happens if I repeatedly load/unload AI models using ollama/lmstudio.

~~~text
CPU: amd 9700x
GPU: 7900xtx, 7800xt
OS:
Ubuntu 24.04.2 LTS
Linux amd-9700x 6.11.0-21-generic #21~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Feb 24 16:52:15 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

22:16 worker@amd-9700x:~$ rocminfo
ROCk module version 6.10.5 is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1282
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
22:16 worker@amd-9700x:~$ rocm-smi


Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
=========================================== ROCm System Management Interface ===========================================
===================================================== Concise Info =====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK   MCLK   Fan  Perf     PwrCap       VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)
========================================================================================================================
0       1     0x744c,   47413  28.0°C  13.0W  N/A, N/A, 0         10Mhz  96Mhz  0%   auto     303.0W       1%     0%
1       2     0x747e,   55553  N/A     N/A    N/A, N/A, 0         None   None   0%   unknown  Unsupported  1%     0%
========================================================================================================================
================================================= End of ROCm SMI Log ==================================================
22:16 worker@amd-9700x:~$ groups
worker adm cdrom sudo dip video plugdev users lpadmin ollama render docker
22:21 worker@amd-9700x:~$ ls -la /dev/dri
합계 0
drwxr-xr-x   3 root root        140  3월 29 21:46 .
drwxr-xr-x  19 root root       5160  3월 29 21:46 ..
drwxr-xr-x   2 root root        120  3월 29 21:46 by-path
crw-rw----+  1 root video  226,   0  3월 29 22:07 card0
crw-rw----+  1 root video  226,   1  3월 29 21:46 card1
crw-rw----+  1 root render 226, 128  3월 29 21:46 renderD128
crw-rw----+  1 root render 226, 129  3월 29 21:46 renderD129
~~~

---

### 评论 #11 — schung-amd (2025-07-02T19:03:38Z)

@cw-koh Sorry for the delay, your issue has additional output that seems similar to https://github.com/ROCm/ROCm/issues/4878; can you try the solution in the linked issue?

@connorblack @felipemarkson Do you also see the `Expected integer value from monitor, but got ""` output? If so, please try the solution in the linked issue.

---

### 评论 #12 — felipemarkson (2026-04-04T23:27:20Z)

> [@connorblack](https://github.com/connorblack) [@felipemarkson](https://github.com/felipemarkson) Do you also see the `Expected integer value from monitor, but got ""` output? If so, please try the solution in the linked issue.


@schung-amd: Running `sudo rocm-smi` I didn't got the `Expected integer value from monitor, but got ""` error

Please see the output bellow.
```
$ ls -la /dev/dri
total 0
drwxr-xr-x   3 root root        100 abr  4 19:53 .
drwxr-xr-x  20 root root       3560 abr  4 19:54 ..
drwxr-xr-x   2 root root         80 abr  4 19:53 by-path
crw-rw----+  1 root video  226,   0 abr  4 19:53 card0
crw-rw----+  1 root render 226, 128 abr  4 19:53 renderD128
$ groups
felipe cdrom floppy sudo audio dip video plugdev users render netdev bluetooth lpadmin scanner ollama devteam
$ sudo rocm-smi
[sudo] senha para felipe: 


======================================== ROCm System Management Interface ========================================
================================================== Concise Info ==================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK    MCLK   Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                 
==================================================================================================================
0       1     0x7480,   26825  39.0°C  3.0W   N/A, N/A, 0         127Mhz  96Mhz  0%   auto  145.0W  7%     0%    
==================================================================================================================
============================================== End of ROCm SMI Log ===============================================
$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.16.13 is loaded
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:1329
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
$ sudo /opt/rocm/bin/rocminfo --support
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
  Name:                    AMD Ryzen 5 8400F 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 8400F 6-Core Processor 
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
  Max Clock Freq. (MHz):   4757                               
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
      Size:                    32443424(0x1ef0c20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32443424(0x1ef0c20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32443424(0x1ef0c20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32443424(0x1ef0c20) KB             
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
  Marketing Name:          AMD Radeon RX 7600                 
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2356                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 602                                
  SDMA engine uCode::      23                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8372224(0x7fc000) KB               
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
```

---
