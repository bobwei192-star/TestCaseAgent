# [Issue]: ROCm OpenCL leaves GPU compute state wedged on gfx1201; subsequent Vulkan apps fail with VK_ERROR_DEVICE_LOST

> **Issue #5825**
> **状态**: closed
> **创建时间**: 2026-01-01T05:40:26Z
> **更新时间**: 2026-01-14T18:41:47Z
> **关闭时间**: 2026-01-14T18:41:47Z
> **作者**: xplatinum
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5825

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

update : Issue reproduces on ROCm 6.4.x and 7.1.x; points to kernel amdgpu compute reset.

### Problem Description

Running an OpenCL workload via **ROCm OpenCL** leaves the GPU compute state in a bad (wedged) state on RDNA3 (`gfx1201`). After the OpenCL application exits, any subsequent **Vulkan** application fails with `VK_ERROR_DEVICE_LOST` until the system is rebooted.

This is **100% reproducible** on my system and does **not** occur if OpenCL is disabled or if the ROCm OpenCL runtime is removed.

### Operating System

Arch Linux

### CPU

12th Gen Intel(R) Core(TM) i7-12700K

### GPU

AMD Radeon 9070 XT

### ROCm Version

7.1.1-1

### ROCm Component

_No response_

### Steps to Reproduce

1. Boot the system
2. Launch **Darktable** with OpenCL enabled (ROCm OpenCL is used)
3. Close Darktable
4. Launch any Vulkan application (e.g. *Arc Raiders*, *Path of Exile 2*)
5. Vulkan application fails with `VK_ERROR_DEVICE_LOST`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```text
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
  Name:                    12th Gen Intel(R) Core(TM) i7-12700K
  Uuid:                    CPU-XX                             
  Marketing Name:          12th Gen Intel(R) Core(TM) i7-12700K
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
  Max Clock Freq. (MHz):   4900                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            20                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32593528(0x1f15678) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32593528(0x1f15678) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32593528(0x1f15678) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32593528(0x1f15678) KB             
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
  Uuid:                    GPU-5eda17060dc35a47               
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
  Max Clock Freq. (MHz):   2400                               
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

```text
amdgpu: ring comp_1.1.0 timeout
amdgpu: [gfxhub] page fault ... address 0x0000000000000000
amdgpu: Faulty UTCL2 client ID: CPC
[drm] device wedged, but recovered through reset
```

---

## 评论 (8 条)

### 评论 #1 — schung-amd (2026-01-02T15:49:50Z)

Hi @xplatinum, thanks for the report. Do you have a more minimal reproducer for this (i.e. does this repro with a simple Vulkan application rather than a game)?

---

### 评论 #2 — xplatinum (2026-01-02T16:57:35Z)

> Hi [@xplatinum](https://github.com/xplatinum), thanks for the report. Do you have a more minimal reproducer for this (i.e. does this repro with a simple Vulkan application rather than a game)?

I tested additional minimal Vulkan applications.

- `vkcube` works normally after running an OpenCL workload.
- `vulkaninfo` completes successfully and reports the device correctly after running an OpenCL workload.

However, more complex Vulkan applications (games) still fail reliably with `VK_ERROR_DEVICE_LOST` after an OpenCL application exits.

edit

I tested additional minimal Vulkan workloads:

- `vkcube`: works after running an OpenCL workload
- `vulkaninfo`: completes successfully after running an OpenCL workload
- `vkmark`: runs successfully and completes all tests after running an OpenCL workload

However, full Vulkan applications (games) still fail reliably with `VK_ERROR_DEVICE_LOST` after an OpenCL application exits.

This suggests the device is left in a partially inconsistent state after OpenCL teardown, but the issue only manifests under heavier Vulkan workloads (likely involving multiple queues / async compute), not simple graphics workloads.

---

### 评论 #3 — xplatinum (2026-01-02T17:24:15Z)

Update: this does not appear to be a ROCm user-space issue.

I tested across multiple ROCm versions (6.4.x, 7.1.0, 7.1.1) and the behavior is unchanged on the mainline Arch kernel. However, when booting the system with `linux-lts` (6.6.x), the issue no longer reproduces.

Repro summary:
- On mainline kernel: running an OpenCL workload (ROCm OpenCL) and exiting leaves the GPU in a state where subsequent Vulkan games fail with VK_ERROR_DEVICE_LOST until reboot.
- On linux-lts (6.12.63): OpenCL workloads exit cleanly and Vulkan applications continue to work normally.

This strongly suggests a regression in recent AMDGPU kernel changes (likely compute/reset handling on RDNA3), with ROCm acting only as the trigger. I have reported this upstream to the drm/amd (AMDGPU) kernel issue tracker.


---

### 评论 #4 — schung-amd (2026-01-02T21:42:01Z)

Thanks for the update. Can you link the upstream report here?

---

### 评论 #5 — xplatinum (2026-01-03T04:54:10Z)

> Thanks for the update. Can you link the upstream report here?

https://gitlab.freedesktop.org/drm/amd/-/issues/4832

---

### 评论 #6 — hcmnbv (2026-01-13T19:34:30Z)

> Update: this does not appear to be a ROCm user-space issue.
> I tested across multiple ROCm versions (6.4.x, 7.1.0, 7.1.1) and the behavior is unchanged on the mainline Arch kernel.
> However, when booting the system with `linux-lts` (6.6.x), the issue no longer reproduces.

similar issue i was struggling. rocm with torch on arch kernel 6.8.15 using a sdxl model. 
but on GFX1200... but also with mixed loads (pytorch, and chromium gpu accel)

```
amdgpu 0000:03:00.0: Using 39-bit DMA addresses
amdgpu 0000:03:00.0: amdgpu: Dumping IP State
amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card2/device/devcoredump/data
amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=486, emitted seq=488
amdgpu 0000:03:00.0: amdgpu:  Process chromium pid 5216 thread chromium:cs0 pid 5232
amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:03:00.0: amdgpu: Dumping IP State
amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card2/device/devcoredump/data
amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=487, emitted seq=488
amdgpu 0000:03:00.0: amdgpu:  Process chromium pid 5216 thread chromium:cs0 pid 5232
amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:6 pasid:32779)
amdgpu 0000:03:00.0: amdgpu:  Process chromium pid 5216 thread chromium:cs0 pid 5232
amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000800007828000 from client 10
amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00601430
amdgpu 0000:03:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
amdgpu 0000:03:00.0: amdgpu:          MORE_FAULTS: 0x0
amdgpu 0000:03:00.0: amdgpu:          WALKER_ERROR: 0x0
amdgpu 0000:03:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
amdgpu 0000:03:00.0: amdgpu:          MAPPING_ERROR: 0x0
amdgpu 0000:03:00.0: amdgpu:          RW: 0x0
```

downgraded to linux-lts... and it's stable!
/lib/modules/6.12.65-1-lts/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.zst


---

### 评论 #7 — xplatinum (2026-01-13T19:37:04Z)

> > Update: this does not appear to be a ROCm user-space issue.
> > I tested across multiple ROCm versions (6.4.x, 7.1.0, 7.1.1) and the behavior is unchanged on the mainline Arch kernel.
> > However, when booting the system with `linux-lts` (6.6.x), the issue no longer reproduces.
> 
> similar issue i was struggling. rocm with torch on arch kernel 6.8.15 using a sdxl model.
> 
> downgraded to linux-lts... and it's stable! /lib/modules/6.12.65-1-lts/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.zst

FYI It has been resolved. https://gitlab.freedesktop.org/drm/amd/-/issues/4765

---

### 评论 #8 — schung-amd (2026-01-14T18:41:47Z)

Great, glad to hear it's fixed and that downgrading the kernel is a viable workaround. Closing this here as the solution doesn't pertain primarily to ROCm, can reopen if necessary.

---
