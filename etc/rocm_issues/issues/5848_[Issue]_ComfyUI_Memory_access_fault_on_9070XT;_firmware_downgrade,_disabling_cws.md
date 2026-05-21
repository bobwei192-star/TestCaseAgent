# [Issue]: ComfyUI Memory access fault on 9070XT; firmware downgrade, disabling cwsr not helping

> **Issue #5848**
> **状态**: closed
> **创建时间**: 2026-01-11T01:58:30Z
> **更新时间**: 2026-02-11T08:57:48Z
> **关闭时间**: 2026-01-26T15:21:52Z
> **作者**: runtimeHorror
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5848

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

GPU runs into error and crashes/while while running any rocm-dependent program on my Linux setup, (including ComfyUI and koboldcpp):

`Memory access fault by GPU node-1.`

`Reason: Page not present or supervisor privilege.`
 
Already tried:
- Downgraded to `linux-firmware-amdgpu 20251111-1`
- Put `amdgpu.cwsr_enable=0`

Nothing helped.

Kernel: `6.18.4-arch1-1`

Note: Vulkan-based operations work fine.

### Operating System

Arch Linux

### CPU

AMD Ryzen 5 5600X

### GPU

AMD Radeon RX 9070 XT 

### ROCm Version

ROCm 7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

Reproduction example on ComfyUI:

1. Launch ComfyUI
2. Generate an image or put multiple gens on queue.
3. Wait. Even if process is not interrupted by memory access fault, GPU will still crash/freeze in a few moments.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
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
  Name:                    AMD Ryzen 5 5600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   4654                               
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
      Size:                    32786520(0x1f44858) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32786520(0x1f44858) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32786520(0x1f44858) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32786520(0x1f44858) KB             
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
  Uuid:                    GPU-9fe866206892bb09               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2460                               
  BDFID:                   3584                               
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
      Size:                    16695296(0xfec000) KB              
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

```

### Additional Information

If on Windows, everything works fine. GPU Zelenograd memtest passes.

---

## 评论 (10 条)

### 评论 #1 — runtimeHorror (2026-01-11T22:14:28Z)

Switched kernel to `linux-lts 6.12.64`. No improvement.

---

### 评论 #2 — amd-nicknick (2026-01-14T10:22:42Z)

Hi @runtimeHorror, could you please try using TheRock Nightlies for ComfyUI workloads? We have several fixes in place that are available from there.
For GFX12, uninstall and reinstall torch with the following index:
```
pip install --force-reinstall --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ torch torchaudio torchvision
```
If you're still reproducing even after reinstalling torch, please provide the workflow you're using, and I can try to reproduce this issue.
Thanks!

---

### 评论 #3 — runtimeHorror (2026-01-16T22:24:19Z)

> Hi [@runtimeHorror](https://github.com/runtimeHorror), could you please try using TheRock Nightlies for ComfyUI workloads? We have several fixes in place that are available from there. For GFX12, uninstall and reinstall torch with the following index:
> 
> ```
> pip install --force-reinstall --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ torch torchaudio torchvision
> ```
> 
> If you're still reproducing even after reinstalling torch, please provide the workflow you're using, and I can try to reproduce this issue. Thanks!

Thanks for the response. Sadly, there appears to be a misunderstanding. My issue is not limited to ComfyUI or Torch. Reinstalling torch as you suggested did not help. I have this problem across the board with any ROCm interaction, Koboldcpp (ROCm fork) being another example.

Speaking of ComfyUI workflows, I have tried 9 different workflows and everything leads to the same error within 3 minutes. So, for experiment purposes, you can try any workflow you wish as the problem is not dependent on them. This is not a "ComfyUI memory issue" as you've re-titled; it is a more global memory issue with ROCm or the amdgpu driver itself on my setup.

I wish to reiterate that this problem does not occur if I'm using Vulkan-based methods to run the same ML models. It's specific to ROCm.

---

### 评论 #4 — amd-nicknick (2026-01-19T04:42:02Z)

Well received on the Vulkan part. Could you please provide a full dmesg log?
Also, please provide the firmware version you're currently using. You could check that with command: `sudo cat /sys/kernel/debug/dri/<device ordinal>/amdgpu_firmware_info`

---

### 评论 #5 — amd-nicknick (2026-01-23T09:22:06Z)

Hi @runtimeHorror, pinging you to check if you're still encountering the issue?

---

### 评论 #6 — amd-nicknick (2026-01-26T15:21:52Z)

Closing this issue due to inactivity, if you are still encountering this, feel free to reopen & provide further information. Thanks!

---

### 评论 #7 — runtimeHorror (2026-02-03T12:14:08Z)

> Hi [@runtimeHorror](https://github.com/runtimeHorror), pinging you to check if you're still encountering the issue?

Hello. I was away for a few weeks. Apologies.



> Could you please provide a full dmesg log? Also, please provide the firmware version you're currently using. You could check that with command: `sudo cat /sys/kernel/debug/dri/<device ordinal>/amdgpu_firmware_info`

Full dmesg log attached.

[dmesg.log](https://github.com/user-attachments/files/25045225/dmesg.log)

Firmware details:
`sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info

VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b40
PFP feature version: 29, firmware version: 0x00000b86
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000c80
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3805204, firmware version: 0x003a1014
ASD feature version: 553648388, firmware version: 0x21000104
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684b00 (104.75.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x0910b001
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x0a000700
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x00000084
MES feature version: 1, firmware version: 0x00000084
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-3E490TX-UP4`

---

### 评论 #8 — amd-nicknick (2026-02-06T07:15:55Z)

@runtimeHorror, I took a look at the dmesg you provided, it doesn't contain indication that any gpu page fault occurred.
I have also checked FW you're using, it looks good.
Please paste the entire application output + dmesg log immediately after the crash had occurred. Also, enable verbose logging on HIP side by setting `export AMD_LOG_LEVEL=4`, you could turn on KMD debug logging as well:
Choose either way:
* Add kernel module parameter `amdgpu.dyndbg=+flmpt`, either by GRUB or `/etc/modprobe.d`:
  ```
  options amdgpu dyndbg=+flmpt
  ```
* Dynamically toggle on debug log (Replace debugfs with the path it is mounted, eg. default `/sys/kernel/debug` on Ubuntu): 
  ```
  echo -n 'module amdgpu +p' > <debugfs>/dynamic_debug/control
  ```

---

### 评论 #9 — runtimeHorror (2026-02-10T12:39:30Z)

> [@runtimeHorror](https://github.com/runtimeHorror), I took a look at the dmesg you provided, it doesn't contain indication that any gpu page fault occurred. I have also checked FW you're using, it looks good. Please paste the entire application output + dmesg log immediately after the crash had occurred. Also, enable verbose logging on HIP side by setting `export AMD_LOG_LEVEL=4`, you could turn on KMD debug logging as well: Choose either way:
> 
>     * Add kernel module parameter `amdgpu.dyndbg=+flmpt`, either by GRUB or `/etc/modprobe.d`:
>       ```
>       options amdgpu dyndbg=+flmpt
>       ```
> 
>     * Dynamically toggle on debug log (Replace debugfs with the path it is mounted, eg. default `/sys/kernel/debug` on Ubuntu):
>       ```
>       echo -n 'module amdgpu +p' > <debugfs>/dynamic_debug/control
>       ```

Well, that's because it's not possible to do anything immediately after crash because the entire system freezes and becomes unusable until force restart. I can only enable or disable things before the crash occurs or after a hard reboot. Please suggest what you would like me to do given this situation.

---

### 评论 #10 — amd-nicknick (2026-02-11T08:57:48Z)

The AMD_LOG_LEVEL should be set as the environment variable when you launch ComfyUI. The kernel debug logging should also be enabled before the crash.
Try redirecting the stdout and stderr of ComfyUI to file and provide previous boot dmesg + log file.

---
