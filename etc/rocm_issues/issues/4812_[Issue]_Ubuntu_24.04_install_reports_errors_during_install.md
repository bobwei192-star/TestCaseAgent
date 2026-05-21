# [Issue]: Ubuntu 24.04 install reports errors during install

> **Issue #4812**
> **状态**: closed
> **创建时间**: 2025-05-27T16:36:30Z
> **更新时间**: 2025-05-28T19:56:30Z
> **关闭时间**: 2025-05-28T19:56:29Z
> **作者**: mcordery
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4812

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Error observed during install after 'sudo apt update' step

Reading package lists... Done
E: The repository 'https://repo.radeon.com/amdgpu/6.4 noble Release' does not have a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.

NAME="Ubuntu"
VERSION="24.04.2 LTS (Noble Numbat)"
CPU: 
model name	: AMD Ryzen Threadripper PRO 7955WX 16-Cores
GPU:
  Name:                    AMD Ryzen Threadripper PRO 7955WX 16-Cores
  Marketing Name:          AMD Ryzen Threadripper PRO 7955WX 16-Cores
  Name:                    gfx1100                            
  Marketing Name:          Radeon RX 7900 GRE                 
      Name:                    amdgcn-amd-amdhsa--gfx1100         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   

### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen Threadripper PRO 7955WX

### GPU

Radeon RX 7900 GRE

### ROCm Version

rocm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

Follow instructions for installing rocm via 'sudo apt' commands

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

mcordery@mcordery-amd-linux:~$ /opt/rocm/bin/rocminfo --support
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
  Name:                    AMD Ryzen Threadripper PRO 7955WX 16-Cores
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper PRO 7955WX 16-Cores
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
  Max Clock Freq. (MHz):   5371                               
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
      Size:                    131102476(0x7d0770c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131102476(0x7d0770c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131102476(0x7d0770c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131102476(0x7d0770c) KB            
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
  Uuid:                    GPU-1811724d0cc8d8dd               
  Marketing Name:          Radeon RX 7900 GRE                 
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
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   1927                               
  BDFID:                   33536                              
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
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
  Packet Processor uCode:: 542                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***             


### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-05-28T14:31:45Z)

Hi @mcordery, not seeing this on my end anymore. This was likely an intermittent error caused by updates/changes in the repo.radeon backend. 

The `Release` file is now present over at https://repo.radeon.com/amdgpu/6.4/ubuntu/dists/noble/. Could you please give this another try and close out the issue if it's been resolved. Thanks!

---

### 评论 #2 — mcordery (2025-05-28T16:29:16Z)

> Hi [@mcordery](https://github.com/mcordery), not seeing this on my end anymore. This was likely an intermittent error caused by updates/changes in the repo.radeon backend.
> 
> The `Release` file is now present over at https://repo.radeon.com/amdgpu/6.4/ubuntu/dists/noble/. Could you please give this another try and close out the issue if it's been resolved. Thanks!


Nope, still seeing it.

sudo apt update

Hit:1 http://us.archive.ubuntu.com/ubuntu noble InRelease                                                                                                              
Get:2 http://us.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]                                                                                             
Get:3 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]    
Get:4 http://us.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]            
Get:5 http://us.archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [161 kB]  
Ign:6 https://repo.radeon.com/amdgpu/6.4 noble InRelease                                       
Get:7 http://us.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Components [212 B]    
Get:8 http://us.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [377 kB]
Hit:9 https://repo.radeon.com/rocm/apt/6.4.1 noble InRelease                                   
Get:10 http://us.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]                                 
Get:11 http://us.archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [7076 B]                                                                 
Get:12 http://us.archive.ubuntu.com/ubuntu noble-backports/restricted amd64 Components [212 B]                                                            
Get:13 http://us.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [16.4 kB]                                                             
Get:14 http://us.archive.ubuntu.com/ubuntu noble-backports/multiverse amd64 Components [212 B]                                                               
Get:15 http://security.ubuntu.com/ubuntu noble-security/main amd64 Packages [862 kB]                                                                       
Get:16 http://security.ubuntu.com/ubuntu noble-security/main amd64 Components [21.6 kB]
Get:17 http://security.ubuntu.com/ubuntu noble-security/restricted amd64 Components [208 B]
Get:18 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Packages [843 kB]
Get:19 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Components [52.2 kB]
Get:20 http://security.ubuntu.com/ubuntu noble-security/multiverse amd64 Components [208 B]
Err:21 https://repo.radeon.com/amdgpu/6.4 noble Release                                
  404  Not Found [IP: 2600:140a:1000:a::b81e:9665 443]
Reading package lists... Done
E: The repository 'https://repo.radeon.com/amdgpu/6.4 noble Release' does not have a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.



---

### 评论 #3 — mcordery (2025-05-28T17:40:59Z)

For reference, I've not seen this in any other prior versions of ROCm that I've installed. It basically started with 6.4.0

---

### 评论 #4 — harkgill-amd (2025-05-28T17:49:02Z)

Noted. I'm seeing remnants of both 6.4.0 and 6.4.1 installations in your `apt update`. To get a clean baseline, could you uninstall all ROCm versions with
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then, reinstall 6.4.1 with the following commands
```
wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb
sudo apt install ./amdgpu-install_6.4.60401-1_all.deb
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm amdgpu-dkms
```
If you're still experiencing any errors during the installation, please share the errors and output of `cat /etc/apt/sources.list.d/amdgpu.list`. 

---

### 评论 #5 — mcordery (2025-05-28T19:56:29Z)

Seems to have run ok, thanks!

---
