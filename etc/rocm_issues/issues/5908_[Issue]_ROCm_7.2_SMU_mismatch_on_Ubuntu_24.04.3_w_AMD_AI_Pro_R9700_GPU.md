# [Issue]: ROCm 7.2 SMU mismatch on Ubuntu 24.04.3 w/ AMD AI Pro R9700 GPU

> **Issue #5908**
> **状态**: closed
> **创建时间**: 2026-01-28T04:20:08Z
> **更新时间**: 2026-03-29T16:00:49Z
> **关闭时间**: 2026-02-24T06:55:05Z
> **作者**: adam-aggrow
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5908

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

Severe mouse and keyboard lag on login screen immediately after boot; sometimes completely unresponsive; sometimes completely disrupts PCIe state and I lose my WiFi hardware, even through warm boots - need to power drain and recycle to get it back. Logs during boot sequence:

amdgpu: detected ip block number 4 <smu_v14_0_0> (smu)
amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684b00 (104.75.0)
amdgpu: amdgpu: SMU driver if version not matched
amdgpu: SMU is initialized successfully!
amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x0000000A SMN_C2PMSG_82:0x00008000
amdgpu: ring gfx_0.0.0 timeout, signaled seq=255, emitted seq=255


### Operating System

24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 5 7600X 6-Core Processor

### GPU

AMD Radeon AI PRO R9700

### ROCm Version

7.2

### ROCm Component

_No response_

### Steps to Reproduce

Ensure Ubuntu Desktop 24.04.3 up-to-date
Follow installation instructions here https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html

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
  Name:                    AMD Ryzen 5 7600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 7600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   5457                               
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
      Size:                    65385292(0x3e5b34c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65385292(0x3e5b34c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65385292(0x3e5b34c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65385292(0x3e5b34c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-f8893707499ea6f0               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33406976(0x1fdc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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

_No response_

---

## 评论 (8 条)

### 评论 #1 — adam-aggrow (2026-02-01T02:46:20Z)

Addt'l context...

## GPU crash under load (llama.cpp benchmark) - Jan 31 2026                                                                                                                                                                  
                                                                                                                                                                                                                               
  System: Ubuntu 24.04, kernel 6.14.0-37-generic, ROCm 7.2, amdgpu-dkms 6.16.13                                                                                                                                                
                                                                                                                                                                                                                               
  ### SMU mismatch at boot:                                                                                                                                                                                                    
  amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032                                                                                                                                                   
  amdgpu: SMU driver if version not matched                                                                                                                                                                                    
  amdgpu: SMU is initialized successfully!                                                                                                                                                                                     
                                                                                                                                                                                                                               
  ### SMU command stalls begin (~16s after boot, during GPU compute load):                                                                                                                                                     
  amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x0000000A SMN_C2PMSG_82:0x00008000                                                                                                                      
  (repeated 4 times over ~38 seconds)                                                                                                                                                                                          
                                                                                                                                                                                                                               
  ### Ring timeouts and resets cascade:                                                                                                                                                                                        
  amdgpu: ring gfx_0.0.0 timeout, signaled seq=752, emitted seq=752                                                                                                                                                            
  amdgpu: Ring gfx_0.0.0 reset succeeded                                                                                                                                                                                       
  [drm] device wedged, but recovered through reset                                                                                                                                                                             
                                                                                                                                                                                                                               
  amdgpu: ring gfx_0.0.0 timeout, signaled seq=742, emitted seq=755                                                                                                                                                            
  amdgpu: Ring gfx_0.0.0 reset succeeded                                                                                                                                                                                       
  [drm] device wedged, but recovered through reset                                                                                                                                                                             
                                                                                                                                                                                                                               
  amdgpu: ring gfx_0.0.0 timeout, signaled seq=754, emitted seq=759                                                                                                                                                            
  amdgpu: Ring gfx_0.0.0 reset succeeded                                                                                                                                                                                       
  [drm] device wedged, but recovered through reset                                                                                                                                                                             
                                                                                                                                                                                                                               
  ### Page faults follow (10+ consecutive):                                                                                                                                                                                    
  amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:7 pasid:32770)                                                                                                                                                           
  amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x0070113B                                                                                                                                                                           
  amdgpu: Faulty UTCL2 client ID: TCP (0x8)                                                                                                                                                                                    
  amdgpu: WALKER_ERROR: 0x5, PERMISSION_FAULTS: 0x3, MAPPING_ERROR: 0x1                                                                                                                                                        
                                                                                                                                                                                                                               
  ### Final reset:                                                                                                                                                                                                             
  amdgpu: ring gfx_0.0.0 timeout, signaled seq=758, emitted seq=761                                                                                                                                                            
  [drm] device wedged, but recovered through reset

---

### 评论 #2 — amd-nicknick (2026-02-11T23:02:42Z)

Hi @adam-aggrow, sorry for the delayed response. Could you please check the kernel dkms & fw package you've installed?
I assume you installed using amdgpu-install script?
Run the following command to list installed driver packages:
```
sudo apt list --installed | grep amdgpu
```

---

### 评论 #3 — adam-aggrow (2026-02-12T22:36:01Z)

Hi @amd-nicknick - no problem at all - I'm sure you guys are slammed. I actually ended up doing an uninstall of the amdgpu package, reverted to the `6.14.0-37-generic` HWE kernel, and then installed only ROCm via the instructions here [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html), skipping the new AMD-supplied GPU driver package altogether. The machine is stable, now. 

Here's a new readout of rocminfo:

ROCk module is loaded
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
  Name:                    AMD Ryzen 5 7600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 7600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   5457                               
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
      Size:                    65385304(0x3e5b358) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65385304(0x3e5b358) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65385304(0x3e5b358) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65385304(0x3e5b358) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-f8893707499ea6f0               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 68                                 
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31309824(0x1ddc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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

Thanks,
Adam

---

### 评论 #4 — amd-nicknick (2026-02-24T06:55:05Z)

Sounds great, I am guessing there was some leftover packages and incorrect FW being used. The HWE kernel will work, and we support that, it just takes longer for fixes to land on those.
Closing this issue for now, if you have any further questions, feel free to reopen and I can take a look. Thanks!

---

### 评论 #5 — lobsteroh (2026-03-28T00:10:01Z)

got exactly same issue
Card: ASUS Radeon AI PRO R9700
IFWI: 7551OG.23.8.0.68.AS01 / Build date 2025/07/25 / Version 00158744
OS: Ubuntu 24.04 Noble
Kernel: 6.14.0-37-generic (also reproduced on 6.17.0-19-generic)
ROCm tested: 7.1.1 and 7.2.1 — both affected identically
amdgpu-dkms: 6.16.6
SMU mismatch on every boot:
smu driver if version = 0x0000002e
smu fw if version = 0x00000032
SMU driver if version not matched
Critical symptom — fan failure under load:

Fan RPM reports 0 at all times despite speed being commanded at ~76/255
Under sustained GPU compute load (ROCm Validation Suite GST), card reaches 109°C hotspot before thermal throttling kicks in
At 109°C power drops from 300W to 90W — card becomes unusable for training
Fan physically jitters briefly around 80°C but never spins up properly
Card cannot sustain more than ~32 minutes of training workload before throttling

This is a hardware safety issue, not a cosmetic bug. The SMU mismatch appears to be preventing proper fan control communication. The card is at risk of sustained operation above 100°C.
Please prioritize a fix for SMU interface version alignment for this card's firmware (104.75.0).

---

### 评论 #6 — lobsteroh (2026-03-28T00:11:51Z)

sudo apt list --installed | grep amdgpu

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

amdgpu-core/noble,noble,now 1:7.1.70101-2255337.24.04 all [installed,automatic]
amdgpu-dkms-firmware/noble,noble,now 30.20.1.0.30200100-2255209.24.04 all [installed,automatic]
amdgpu-dkms/noble,noble,now 1:6.16.6.30200100-2255209.24.04 all [installed]
amdgpu-install/noble,noble,now 30.20.1.0.30200100-2255209.24.04 all [installed]
libdrm-amdgpu-amdgpu1/noble,now 1:2.4.125.70101-2255337.24.04 amd64 [installed,automatic]
libdrm-amdgpu-common/noble,noble,now 1.0.0.70101-2255337.24.04 all [installed,automatic]
libdrm-amdgpu-dev/noble,now 1:2.4.125.70101-2255337.24.04 amd64 [installed,automatic]
libdrm-amdgpu-radeon1/noble,now 1:2.4.125.70101-2255337.24.04 amd64 [installed,automatic]
libdrm-amdgpu1/noble-updates,now 2.4.125-1ubuntu0.1~24.04.1 amd64 [installed,automatic]
libdrm-amdgpu1/noble-updates,now 2.4.125-1ubuntu0.1~24.04.1 i386 [installed,automatic]
libdrm2-amdgpu/noble,now 1:2.4.125.70101-2255337.24.04 amd64 [installed,automatic]
xserver-xorg-video-amdgpu/noble-updates,now 23.0.0-1ubuntu0.24.04.1 amd64 [installed,automatic]


---

### 评论 #7 — lobsteroh (2026-03-28T00:14:43Z)

rocminfo
ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
  Max Clock Freq. (MHz):   6159                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65765192(0x3eb7f48) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65765192(0x3eb7f48) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65765192(0x3eb7f48) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65765192(0x3eb7f48) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-e764bcabea26ef4e               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   11520                              
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
  Packet Processor uCode:: 108                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31309824(0x1ddc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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
But the fan never comes on, it just seems to jitter a bit back and forth, as is it is unusable for any training

---

### 评论 #8 — lobsteroh (2026-03-29T16:00:49Z)

Same SMU mismatch here on ASUS Turbo Radeon AI Pro R9700 32GB.

Additional finding not yet mentioned in this issue: the SMU mismatch is causing complete fan control failure under load.

Hardware: ASUS Turbo Radeon AI Pro R9700 32GB
vBIOS: 115-G287BP00-100
OS: Ubuntu 24.04
Kernel: 6.17.0-19

---
