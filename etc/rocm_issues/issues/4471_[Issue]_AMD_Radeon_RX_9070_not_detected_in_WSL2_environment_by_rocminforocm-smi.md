# [Issue]: AMD Radeon RX 9070 not detected in WSL2 environment by rocminfo/rocm-smi

> **Issue #4471**
> **状态**: closed
> **创建时间**: 2025-03-10T12:58:48Z
> **更新时间**: 2025-06-12T18:12:56Z
> **关闭时间**: 2025-03-10T18:28:48Z
> **作者**: Y0oMu
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4471

## 描述

### Problem Description

## Description:

I'm unable to access my new AMD Radeon RX 9070 GPU from within WSL2. Both `rocminfo` and `rocm-smi` fail to detect the GPU, with `rocminfo` only showing my Intel CPU and `rocm-smi` failing with a driver initialization error.

### Error Output:

```
# rocm-smi output:
WSL environment detected.
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
  Name:                    13th Gen Intel(R) Core(TM) i5-13600KF
  Uuid:                    CPU-XX                             
  Marketing Name:          13th Gen Intel(R) Core(TM) i5-13600KF
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
  Cacheline Size:          64(0x40)                           
  Internal Node ID:        0                                  
  Compute Unit:            20                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16281964(0xf8716c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16281964(0xf8716c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16281964(0xf8716c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16281964(0xf8716c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***   
[rocminfo only shows CPU, no AMD GPU detected]
```

### Additional Information:

- The GPU is properly detected and functioning in Windows
- I've confirmed WSL2 is using the latest version (`wsl --version`)
- Windows 11 is up to date with all drivers installed
- The RX 9070 is a recent model which may require updated support in ROCm

### What I've tried:

- Updated WSL2 to the latest version
- Configured `.wslconfig` with `gpuSupport=true`
- Installed latest AMD drivers on Windows host
- Restarted WSL using `wsl --shutdown`

### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

13th Gen Intel(R) Core(TM) i5-13600KF

### GPU

AMD Radeon RX 9070

### ROCm Version

ROCm 6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

1. Follow the instructions at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html to install ROCm
2. Execute "rocm-smi" - fails with driver initialization error
3. Execute "rocminfo" - only detects CPU, no GPU found

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-03-10T18:28:48Z)

Hi @Y0oMu, this is expected as the 9000 series GPUs are not currently supported for use with ROCm on WSL. Please see the [GPU Support Matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix) for more information on supported SKUs.

---

### 评论 #2 — walsons (2025-03-26T08:50:40Z)

when will the RX 9070XT support ROCm via WSL

---

### 评论 #3 — tzarebczan (2025-04-25T21:13:02Z)

Have a 9070XT myself, would be awesome to run this! 

---

### 评论 #4 — KenKbs (2025-05-10T22:35:50Z)

On the same page here - please add support for the 9070XT!

---

### 评论 #5 — Headcrabed (2025-06-12T18:12:56Z)

It’s now supported by 25.6.1 driver, and navi44 and navi32’s wsl2 support are also added in this version of driver.

---
