# [Issue]: amdgpu pagefault under rocm7.2 on gfx1151

> **Issue #5890**
> **状态**: closed
> **创建时间**: 2026-01-23T07:21:59Z
> **更新时间**: 2026-05-06T10:26:54Z
> **关闭时间**: 2026-05-06T10:26:54Z
> **作者**: kellrott
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5890

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

PyTorch was working against rocm7.1 on a Framework Desktop machine. Using Bios portioned GPU memory rather then GTT. Was experiencing effects of #5807 so I updated to rocm7.2. At that point, all torch related code began to hang once elements where copied to the device. Checking dmesg reveled that the hang was actually the result of a lower level system having a page fault. 

```
[ 5071.443221] amdgpu 0000:c2:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32772)
[ 5071.443234] amdgpu 0000:c2:00.0: amdgpu:  Process python pid 15426 thread python pid 15426
[ 5071.443237] amdgpu 0000:c2:00.0: amdgpu:   in page starting at address 0x00007ad8780fe000 from client 10
[ 5071.443239] amdgpu 0000:c2:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[ 5071.443240] amdgpu 0000:c2:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPF (0x4)
[ 5071.443242] amdgpu 0000:c2:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[ 5071.443243] amdgpu 0000:c2:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[ 5071.443244] amdgpu 0000:c2:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[ 5071.443245] amdgpu 0000:c2:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[ 5071.443245] amdgpu 0000:c2:00.0: amdgpu: 	 RW: 0x0
```

### Operating System

Ubuntu 25.10 (Questing Quokka)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

In Python:
```
>>> import torch
>>> torch.cuda.is_available()
True
>>> torch.randn(4096, 4096, device='cuda', dtype=torch.float32)
```

At this point it freezes, `dmesg` logs the page fault


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
      Size:                    32113080(0x1ea01b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32113080(0x1ea01b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32113080(0x1ea01b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32113080(0x1ea01b8) KB             
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
  Marketing Name:          Radeon 8060S Graphics              
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
  BDFID:                   49664                              
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
      Size:                    100663296(0x6000000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    100663296(0x6000000) KB            
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
  Name:                    aie2p                              
  Uuid:                    AIE-XX                             
  Marketing Name:          RyzenAI-npu5                       
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
      Size:                    32113080(0x1ea01b8) KB             
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
      Size:                    32113080(0x1ea01b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***    

### Additional Information

Drivers install via `amdgpu-install_7.2.70200-1_all.deb` 

Reproduced with docker image `rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.9.1` 

Bare metal python install with:
```
pip3 install --force --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm7.1
```
and
```
pip3 install --force --pre torch torchvision torchaudio --index-url https://rocm.nightlies.amd.com/v2/gfx1151/
```

---

## 评论 (24 条)

### 评论 #1 — sandriverfish (2026-01-23T10:07:18Z)

Same issue, and ubuntu version: 24.10.

---

### 评论 #2 — peter247 (2026-01-23T12:08:11Z)

in comfyui ( proxmox debian 13 ) on 7.2 on the gfx1151 , I just get a instant Segmentation fault 

Versions of relevant libraries:
[pip3] numpy==2.4.1
[pip3] torch==2.9.1+rocm7.2.0.lw.git7e1940d4
[pip3] torchaudio==2.9.0+rocm7.2.0.gite3c6ee2b
[pip3] torchsde==0.2.6
[pip3] torchvision==0.24.0+rocm7.2.0.gitb919bd0c
[pip3] triton==3.5.1+rocm7.2.0.gita272dfa8
[conda] Could not collect

torch.randn(4096, 4096, device='cuda', dtype=torch.float32)
Segmentation fault

---

### 评论 #3 — peter247 (2026-01-23T22:53:23Z)

I went back to rocm 7.1 to make sure didn't mess things up.
I wanted to know if the amdgpu rocm 7.2 will work with the :-
pip3 install --force --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm7.1

what I did is :-

amdgpu-install --uninstall --rocmrelease=all
apt purge amdgpu-install
apt autoremove

apt install ./amdgpu-install_7.2.70200-1_all.deb
apt update
But with amdgpu-install -y --usecase=rocm --no-dkms instead of amdgpu-install -y --usecase=graphics,rocm
Now it works with the torch nightly/rocm7.1 repo without a Segmentation fault .



---

### 评论 #4 — winmutt (2026-01-25T13:12:13Z)

Same issue rocm7.2
Linux 6.17.0-1009-oem #9-Ubuntu SMP PREEMPT_DYNAMIC Thu Dec 18 05:48:19 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
Ubuntu 24.04.3 LTS

 amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
 amdgpu 0000:c5:00.0: amdgpu:  Process ollama pid 12713 thread ollama pid 12722
 amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007bddc416a000 from client 10
 amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
 amdgpu 0000:c5:00.0: amdgpu:          Faulty UTCL2 client ID: CPF (0x4)
 amdgpu 0000:c5:00.0: amdgpu:          MORE_FAULTS: 0x0
 amdgpu 0000:c5:00.0: amdgpu:          WALKER_ERROR: 0x1
 amdgpu 0000:c5:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
 amdgpu 0000:c5:00.0: amdgpu:          MAPPING_ERROR: 0x1
 amdgpu 0000:c5:00.0: amdgpu:          RW: 0x0


---

### 评论 #5 — winmutt (2026-01-25T13:34:28Z)

Realized I was on an unsupported kernel version, booted to 6.14:

6.14.0-37-generic


amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
amdgpu 0000:c5:00.0: amdgpu:  Process ollama pid 2328 thread ollama pid 2328
amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000793515482000 from client 10

The rest of the log entries from the previous segfault were missing, presumably kernel version differences?

Downgrading to 7.1 is very disappointing, I have been waiting for NPU support.

---

### 评论 #6 — nirolfa (2026-01-25T19:20:59Z)

same here

6.14.0-1019-oem #19-Ubuntu SMP PREEMPT_DYNAMIC Thu Dec 18 05:40:21 UTC 2025 x86_64 
 (tried 6.18.7-061807-generic too but same problem)
rocm is already the newest version (7.2.0.70200-43~24.04)
when running comfyui -> gtt put to max, vram to min 

running comfyui

[20133.654527] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32774)
[20133.654545] amdgpu 0000:c4:00.0: amdgpu:  in process python3 pid 13258 thread python3 pid 13258)
[20133.654550] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007253927e9000 from client 10
[20133.654553] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[20133.654556] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[20133.654558] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x0
[20133.654559] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
[20133.654561] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[20133.654562] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
[20133.654564] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0

-------
rem
if running with vram max, and gtt min then don't have that issue
---_





---

### 评论 #7 — amd-nicknick (2026-01-26T09:29:48Z)

Hi @kellrott, @sandriverfish, @peter247, @winmutt, for Strix Halo we recommend using Ubuntu OEM kernel drivers instead of amdgpu-install dkms. Is this issue still reproducible with OEM kernel?
Please try installing & booting 24.04c
sudo apt update && sudo apt install linux-oem-24.04c

If you had installed amdgpu-install drivers, ensure those are removed `sudo amdgpu-uninstall` and run `sudo update-initramfs -u` after uninstalling.

Reference this doc instead: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html

For packaged installation (i.e. amdgpu-install), ensure DKMS is OFF when running install. `amdgpu-install -y --usecase=rocm --no-dkms`. You could skip this if you're pip installing ROCm enabled torch.

@nirolfa, I see you're on a correct version of kernel, could you please supply the full dmesg log and output of `sudo cat /sys/kernel/debug/dri/<device ordinal>/amdgpu_firmware_info`?

---

### 评论 #8 — peter247 (2026-01-26T12:19:59Z)

Not sure if I went down the wrong track before  ? , following the Radeon and not the Ryzen parts , I was right about the --no-dkms .


---

### 评论 #9 — winmutt (2026-01-26T12:24:09Z)

@amd-nicknick thanks so much for your response. That did fix the segfault for me, however I am now getting a different issue [https://github.com/ROCm/ROCm/issues/5902].

---

### 评论 #10 — kellrott (2026-01-28T05:17:56Z)

I used `sudo amdgpu-uninstall` to remove dkms and get back to stock. This seemed to solve the issue with pytorch installed with `pip3 install --force --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm7.1` . I'm still experiencing #5807 (slow fp32)

If I follow the instructions from https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html and try to install `torch-2.9.1+rocm7.2.0.lw.git7e1940d4-cp312-cp312-linux_x86_64.whl` I start to get the segfault when calling `torch.randn` from the example above

The dmesg for the segfault is:
```
[ 9570.812114] python[16015]: segfault at 34 ip 00007d0f1f448204 sp 00007ffc713f60a0 error 4 in libhsa-runtime64.so.1.18.70200[48204,7d0f1f41d000+13c000] likely on CPU 2 (core 2, socket 0)
[ 9570.812125] Code: 04 00 00 41 54 55 48 89 f5 53 48 89 fb 48 83 ec 28 4c 8b 66 68 64 48 8b 04 25 28 00 00 00 48 89 44 24 18 31 c0 4d 39 e5 74 4c <41> 83 7c 24 34 03 49 8b 44 24 20 74 5f 41 c7 44 24 34 00 00 00 00
```

This is different from the original pagefault, so I think there are two error cases here: page fault against amdgpu installed dkms drivers and a segfault in libhsa. The pagefault causes the program to stall, probably because the driver never returns a call after the page fault. The segfault causes the program to exit with a core dump.

---

### 评论 #11 — amd-nicknick (2026-01-28T09:49:53Z)

Hi @kellrott, glad to hear you have something running. The slow FP32 issue is being worked on actively on the other issue you mentioned.
Let me also take a look on my system to see what's going on with the 7.2 wheel. Does this happen everytime it is called or it happens from time to time?
Another suggestion would be to try using TheRock nightlies instead, we have further fixes that are only available with TheRock wheels, could you give that a try with the same config (kernel / test program) to help me isolate if it's an issue with the wheel?
See this page for TheRock guidance:
https://github.com/ROCm/TheRock/blob/main/RELEASES.md

---

### 评论 #12 — peter247 (2026-01-28T09:50:36Z)

Tried the same thing with the python 3.13 versions ( cp313 ), segment fault in libhsa-runtime64.so.

---

### 评论 #13 — amd-nicknick (2026-01-28T09:51:47Z)

@winmutt, let's track the OOM on the separate issue you opened. I'll start working on that this week.

---

### 评论 #14 — amd-nicknick (2026-01-28T09:54:12Z)

@peter247, what kernel driver are you on? For halo you should be on in tree driver + OEM kernel 24.04c. (This is really not optional).
Also, please help try TheRock nightlies wheels as well, chances are something is already resolved in latest (TheRock moves much faster than the official track).


---

### 评论 #15 — peter247 (2026-01-28T10:05:04Z)

> [@peter247](https://github.com/peter247), what kernel driver are you on? For halo you should be on in tree driver + OEM kernel 24.04c. (This is really not optional). Also, please help try TheRock nightlies wheels as well, chances are something is already resolved in latest (TheRock moves much faster than the official track).

I'm on the debian 6.17 kernel so that could be it , so why does amdgpu 7.2 without dkms and the pip3 install --force --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm7.1 work ?

---

### 评论 #16 — kellrott (2026-01-29T06:16:59Z)

Tried with `pip3 install --force --pre torch torchvision torchaudio --index-url https://rocm.nightlies.amd.com/v2/gfx1151/` from TheRock instructions. 

`python -m torch.utils.collect_env` returns 
```
Collecting environment information...
PyTorch version: 2.11.0a0+rocm7.11.0a20260106
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 7.2.53150

OS: Ubuntu 25.10 (x86_64)
GCC version: (Ubuntu 15.2.0-4ubuntu4) 15.2.0
Clang version: 20.1.8 (0ubuntu4)
CMake version: version 4.2.1
Libc version: glibc-2.42

Python version: 3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0] (64-bit runtime)
Python platform: Linux-6.17.0-8-generic-x86_64-with-glibc2.42
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: 
GPU models and configuration: Radeon 8060S Graphics (gfx1151)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
Is XPU available: False
HIP runtime version: 7.2.53150
MIOpen runtime version: 3.5.1
Is XNNPACK available: True
Caching allocator config: N/A
```

So I think I'm on rocm 7.2, no segfaults, still seeing slow float fp32 (but that should probably be tracked on another issue)


---

### 评论 #17 — amd-nicknick (2026-01-29T11:58:26Z)

@kellrott, that sounds great, for the FP issue it'll land on TheRock first anyway so I suggest tracking nighlies for that.
I'll close this issue for now, feel free to create a new issue if you encounter any further problem.

@peter247, for Strix Halo, our dkms is really designed for desktop graphics stack and is heavily qualified on those. As integrated GPU tends to follow release schedule along OEM projects, we would track specific distro kernel instead.
I'd suggest you trying out TheRock nightlies as well for torch, we do not qualify as much of the wheels shipped from PyTorch.

---

### 评论 #18 — reywang18 (2026-02-07T00:36:19Z)

Same issue now with 780M GPU

---

### 评论 #19 — namecaps3k (2026-02-19T11:18:56Z)

same issue with strix halo, kernel 6.18.7

---

### 评论 #20 — FlorianFranzen (2026-04-28T11:37:36Z)

@amd-nicknick I am not sure how this issue is closed. I have the exact same issue on NixOS on a gfx1100 using Ollama since updating ROCM and the kernel does not seems to matter (6.18, 6.19, 7.0).

 So this is clearly points towards a serious regression worth fixing!

---

### 评论 #21 — amd-nicknick (2026-04-30T09:28:18Z)

@FlorianFranzen the original issue was for Strix Halo gfx1151. Could you please open a new issue instead & attach your repro steps?
For gfx1100, you should use the amdgpu-dkms. Do you have that installed?

---

### 评论 #22 — cdanis (2026-05-04T23:58:23Z)

Watching for Strix Halo ROCm fixes.

---

### 评论 #23 — FlorianFranzen (2026-05-05T11:34:38Z)

@amd-nicknick I was able to greatly reduce the issue by disabling preempt queue execution via the `amdgpu.mcbp=0` kernel flag and now Ollama works without major issues again, even under v7.2. I can only assume a newer kernel or ROCm version increases the likelihood of MCBP to be used or interrupting a ROCM operation. This is good enough for me. If the issue reappears, I will gladly open a new issue.

---

### 评论 #24 — amd-nicknick (2026-05-06T10:26:52Z)

Closing this issue. If you're encountering any further issues, feel free to open a new one and we'll take a look. Thanks!

---
