# [Issue]: amdgpu-dkms build fails with Ubuntu mainline kernel 6.18.7

> **Issue #5905**
> **状态**: closed
> **创建时间**: 2026-01-26T16:17:44Z
> **更新时间**: 2026-02-15T18:58:41Z
> **关闭时间**: 2026-01-31T12:00:08Z
> **作者**: phueper
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5905

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

[make.log](https://github.com/user-attachments/files/24864707/make.log)

### Problem Description

```
OS:
NAME="Ubuntu"
VERSION="25.10 (Questing Quokka)"
CPU: 
model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    aie2p                              
  Marketing Name:          RyzenAI-npu5  
```

Building amdgpu-dkms fails when installing latest ROCm 7.2 and using a mainline kernel 6.18.7:

```
Autoinstall of module amdgpu/6.16.13-2278356.24.04 for kernel 6.18.7-061807-generic (x86_64)
Building module(s)......(bad exit status: 2)
Failed command:
'make' KERNELVER=6.18.7-061807-generic
ERROR (dkms apport): kernel package linux-headers-6.18.7-061807-generic is not supported
```

Since ROCm 7,.2 on my GPU seems to be supported only on Kernel > 6.18.5 i wanted to try it, but the amdgpu-dkms build fails



### Operating System

Ubuntu 25.10

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

7.2

### ROCm Component

_No response_

### Steps to Reproduce

- use mainline kernel 6.18.7
- install rocm 7.2 and amdgpu 30.30

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
╰─# rocminfo --support
ROCk module version 6.16.6 is loaded
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
      Size:                    128803492(0x7ad62a4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    128803492(0x7ad62a4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    128803492(0x7ad62a4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
```

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — phueper (2026-01-26T16:18:08Z)

similar to #4619  i believe?

---

### 评论 #2 — schung-amd (2026-01-27T16:09:33Z)

Hi @phueper, thanks for the report. I don't think we have a plan to support Ubuntu 25 specifically, so we won't have support for that kernel version until the Ubuntu 24 HWE kernel officially updates to it (similar to the linked issue) or until Ubuntu 26 + support on our end happens.

In the meanwhile you can downgrade your kernel version (I see you mention a Kernel > 6.18.5 requirement, where is that coming from?), or if that's not possible/desirable I'd advise just using the in-kernel driver and not building the DKMS driver.

---

### 评论 #3 — phueper (2026-01-28T16:16:55Z)

Hi @schung-amd  .. thanks for the reply, the info about 6.18.5 i got from https://github.com/kyuz0/amd-strix-halo-gfx1151-toolboxes?tab=readme-ov-file who seems to have experimented with the different combinations... so i tried building  the amdgpu 30.30 dkms now with my kernel, that works fine, but now my ollama build fails with both ROCm 7.2 and 7.1.1 .. i will try to switch back to the previous amdgpu version and try again... the error i get is this in dmesg:

```
[   12.606940] amdgpu 0000:c2:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[   12.606956] amdgpu 0000:c2:00.0: amdgpu:  Process ollama pid 5599 thread ollama pid 5606
[   12.606960] amdgpu 0000:c2:00.0: amdgpu:   in page starting at address 0x00007da1d0003000 from client 10
[   12.606963] amdgpu 0000:c2:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[   12.606965] amdgpu 0000:c2:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[   12.606968] amdgpu 0000:c2:00.0: amdgpu:      MORE_FAULTS: 0x0
[   12.606970] amdgpu 0000:c2:00.0: amdgpu:      WALKER_ERROR: 0x1
[   12.606971] amdgpu 0000:c2:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[   12.606973] amdgpu 0000:c2:00.0: amdgpu:      MAPPING_ERROR: 0x1
[   12.606974] amdgpu 0000:c2:00.0: amdgpu:      RW: 0x0

```


but i think this issue can then be closed since my expectation that the dkms should work with  latest mainline kernels was wrong

---

### 评论 #4 — schung-amd (2026-01-28T16:40:43Z)

Right, missed that you're on Strix Halo; there's a bit of a mess there at the moment around kernel and firmware versions, see https://github.com/ROCm/TheRock/issues/2991#issuecomment-3768808325. In your case using kernel 6.18.5 without building DKMS should be the way to go. Also make sure you've picked up the firmware update.

---

### 评论 #5 — phueper (2026-01-28T20:04:02Z)

Could you elaborate which firmware versions are correct ? I do remember seeing this in the documentation somewhere but can't find it right now 

---

### 评论 #6 — schung-amd (2026-01-28T20:18:17Z)

Not sure if there's a difference for Ubuntu 25 vs 24, but on the latter `20240318.git3b128b60-0ubuntu2.17` and higher versions (2.17 is the versioning here, the date is irrelevant) will be sufficient. The relevant fixes went out in September IIRC so if you've kept up to date you should already be on a good firmware version.

---

### 评论 #7 — phueper (2026-01-31T12:00:08Z)

Thanks a lot for the info, i managed now to get ROCm 7.2 ollama running even with the default Ubuntu 25.10 kernel and the amdgpu-dkms driver , so no mainline Kernel needed for me (at least not yet ) ... critical issue was the firmware package, the default Ubuntu 25.10 linux-firmwware references a git tag from August for the linux-firmware git repo, i upgraded to newer firmware and now can run ollama with ROCm 7.2 .
Closing this. Thanks once again @schung-amd 

---

### 评论 #8 — phueper (2026-01-31T13:56:01Z)

just in case anybody else finds this:

i manually loaded the linux-firmware package for resolute (i.e. Ubuntu 26.04) and installed it from https://launchpad.net/ubuntu/+source/linux-firmware

Thus whenever i update or a newer version of linux-firmware wil be released it would hopefully automatically update for me. Then used the default ROCm (7.2)  and amdgpu (30.30)  install for Ubuntu and this now allows me to use ROCm 7.2 ollama docker image on our Strix Halo 

---

### 评论 #9 — NickJLange (2026-02-09T05:01:45Z)

I've posted my fix to [get 6.18.7 going on strix halo here](https://github.com/ROCm/TheRock/issues/2991#issuecomment-3768808325 )

tldr; uninstall then reinstall without dkms for now.

---

### 评论 #10 — phueper (2026-02-15T18:58:41Z)

Fwiw... I updated to amdgpu 31.10 still using the default Ubuntu kernel 6.17.0-14 but the updated linux-firmware package linked in my last comment and it continues to work for me 

---
