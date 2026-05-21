# MIOpen kdb files with ROCm PyTorch wheels missing for gfx1100

> **Issue #3214**
> **状态**: closed
> **创建时间**: 2024-06-01T12:03:27Z
> **更新时间**: 2025-05-08T18:35:09Z
> **关闭时间**: 2025-05-08T18:35:09Z
> **作者**: joshbla
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3214

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I was following the "Using a wheels package", "Install on bare metal" instructions from the ROCm documentation: [Install on Linux - PyTorch](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/3rd-party/pytorch-install.html).

The issue arises at step 4, where the instructions suggest using the helper script `install_kdb_files_for_pytorch_wheels.sh` to download and install MIOpen kdb files. Here is the original response from the terminal using the unmodified script:

```bash
desktop@desktop:~$ export GFX_ARCH=gfx1100
export ROCM_VERSION=6.1
./install_kdb_files_for_pytorch_wheels.sh
ROCM version: 6.1
GFX architectures: gfx1100
PyTorch installation path: /home/desktop/.local/lib/python3.10/site-packages
Downloading .kdb files for rocm-6.1 (gfx1100 arch) ...
Extracting deb packages for gfx1100 ...
ls: cannot access '*deb': No such file or directory
Copying kdb files to /home/desktop/.local/lib/python3.10/site-packages/torch/share
cp: cannot stat 'opt/rocm-*/share/miopen': No such file or directory
desktop@desktop:~$ 
```
I modified the script to include additional debugging statements to identify where the error occurred. The modified script confirmed that the necessary .deb files for gfx1100 architecture do not exist at the specified URL.

The script points to the following URL for downloading the kdb files:
https://repo.radeon.com/rocm/apt/6.1/pool/main/m/

Additionally, I checked the URL for ROCm version 6.1.1, and the files do not exist there either.

Please provide the necessary kdb files for the gfx1100 architecture or hire me to generate and upload the files.

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 5900X 12-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

MIOpen

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.7.0 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.13
Runtime Ext Version:     1.4
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
  Name:                    AMD Ryzen 9 5900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5900X 12-Core Processor
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65726556(0x3eae85c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65726556(0x3eae85c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65726556(0x3eae85c) KB             
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
  Uuid:                    GPU-7f21bc6c495882ee               
  Marketing Name:          Radeon RX 7900 XTX                 
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
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2371                               
  BDFID:                   3328                               
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 92                                 
  SDMA engine uCode::      20                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
*** Done ***    

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — linepe (2024-06-15T07:29:32Z)

Pretty sure the files where present for the version 5.7. I've tried to upgrade to a newer version and there are no files for gfx1100 anymore.

see: https://repo.radeon.com/rocm/apt/5.7/pool/main/m/


---

### 评论 #2 — joshbla (2024-06-16T01:36:45Z)

I've checked a few versions previous to 5.7 as well and they are not present.

---

### 评论 #3 — harkgill-amd (2024-06-26T19:21:06Z)

Hi @joshbla, I will look into this issue and get back to you on it.

---

### 评论 #4 — harkgill-amd (2024-06-27T13:49:55Z)

@joshbla, only architectures that have additional tuning focus have their respective kdb files generated and uploaded to the repository. The error you are seeing is to be expected as gfx1100 is not one of the arch's with additional tuning. We will work on getting the documentation updated to reflect the supported architectures for the `install_kdb_files_for_pytorch_wheels.sh` script. Thank you!

---

### 评论 #5 — harkgill-amd (2025-05-08T18:35:09Z)

The `install_kdb_files_for_pytorch_wheels.sh` script has been updated with more descriptive errors should a gfx architecture without kdb files be requested. For example, running with `GFX_ARCH=gfx1100` returns

```
ERROR: No MIOpen kernel database files found for gfx1100
Please check https://repo.radeon.com/rocm/apt/latest/pool/main/m/ for supported architectures
```

---
