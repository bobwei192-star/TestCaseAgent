# [Issue]: Ubuntu 24 crashes lightly after invoking ROCm

> **Issue #5999**
> **状态**: open
> **创建时间**: 2026-02-24T22:52:52Z
> **更新时间**: 2026-05-13T18:53:26Z
> **作者**: yasharhon
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5999

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

Observed together with #5998.

After trying to run (dockerized) JAX or Pytorch code using ROCm, I get freezes, black screens and graphical glitches, resulting in a lighter crash (all programs die and I am returned to the login screen).



### Operating System

Ubuntu 24.04.4

### CPU

Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz.

### GPU

AMD Radeon RX 9060 XT.

### ROCm Version

ROCm 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
  Name:                    Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz
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
  Max Clock Freq. (MHz):   4100                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1200                            
  Uuid:                    GPU-76d4de1a1944b098               
  Marketing Name:          AMD Radeon RX 9060 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      32768(0x8000) KB                   
  Chip ID:                 30096(0x7590)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2620                               
  BDFID:                   1024                               
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
      Name:                    amdgcn-amd-amdhsa--gfx1200         
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

_No response_

---

## 评论 (12 条)

### 评论 #1 — lucbruni-amd (2026-03-02T21:48:17Z)

Hi @yasharhon, after the graphical issues, could you provide me the output of `dmesg -T`? This will help give us a hint of what's going on with the device. Thanks!

---

### 评论 #2 — yasharhon (2026-03-05T18:12:14Z)

@lucbruni-amd From what I could see, the issue corresponded to the following:

```
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=69, emitted seq=72
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:04:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
amdgpu 0000:04:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
amdgpu 0000:04:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
amdgpu 0000:04:00.0: amdgpu: 	 MORE_FAULTS: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 WALKER_ERROR: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x4
amdgpu 0000:04:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 RW: 0x1
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=71, emitted seq=74
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=72, emitted seq=76
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=74, emitted seq=78
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=76, emitted seq=80
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=78, emitted seq=80
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.1.0 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:1:0)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=10257, emitted seq=10259
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=10258, emitted seq=10259
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 2743 thread gnome-shel:cs0 pid 2775
amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
rfkill: input handler enabled
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.1 timeout, signaled seq=45, emitted seq=47
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 5244 thread gnome-shel:cs0 pid 5284
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.0.1 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:0:1)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.0.1 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
amdgpu 0000:04:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
amdgpu 0000:04:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
amdgpu 0000:04:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
amdgpu 0000:04:00.0: amdgpu: 	 MORE_FAULTS: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 WALKER_ERROR: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x4
amdgpu 0000:04:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 RW: 0x1
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.1 timeout, signaled seq=46, emitted seq=47
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 5244 thread gnome-shel:cs0 pid 5284
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.0.1 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:0:1)
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.0.1 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=10264, emitted seq=10265
amdgpu 0000:04:00.0: amdgpu:  Process gnome-shell pid 5244 thread gnome-shel:cs0 pid 5284
amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
rfkill: input handler disabled
amdgpu 0000:04:00.0: amdgpu: Dumping IP State
amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=23, emitted seq=25
amdgpu 0000:04:00.0: amdgpu:  Process Xwayland pid 5326 thread Xwayland:cs0 pid 5464
amdgpu 0000:04:00.0: amdgpu: Starting comp_1.1.1 ring reset
amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:1:1)
amdgpu 0000:04:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
amdgpu 0000:04:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
amdgpu 0000:04:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
amdgpu 0000:04:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
amdgpu 0000:04:00.0: amdgpu: 	 MORE_FAULTS: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 WALKER_ERROR: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x4
amdgpu 0000:04:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
amdgpu 0000:04:00.0: amdgpu: 	 RW: 0x1
amdgpu 0000:04:00.0: amdgpu: Ring comp_1.1.1 reset failed
amdgpu 0000:04:00.0: amdgpu: GPU reset begin!. Source:  1
amdgpu 0000:04:00.0: amdgpu: MES(1) failed to respond to msg=REMOVE_QUEUE
amdgpu 0000:04:00.0: amdgpu: failed to unmap legacy queue
[drm:gfx_v12_0_cp_gfx_enable.isra.0 [amdgpu]] *ERROR* failed to halt cp gfx
amdgpu 0000:04:00.0: amdgpu: MODE1 reset
amdgpu 0000:04:00.0: amdgpu: GPU mode1 reset
amdgpu 0000:04:00.0: amdgpu: GPU smu mode1 reset
amdgpu 0000:04:00.0: amdgpu: GPU reset succeeded, trying to resume
amdgpu 0000:04:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x0000008000000000).
amdgpu 0000:04:00.0: amdgpu: VRAM is lost due to GPU reset!
amdgpu 0000:04:00.0: amdgpu: PSP is resuming...
amdgpu 0000:04:00.0: amdgpu: RAS: optional ras ta ucode is not available
amdgpu 0000:04:00.0: amdgpu: RAP: optional rap ta ucode is not available
amdgpu 0000:04:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
amdgpu 0000:04:00.0: amdgpu: SMU is resuming...
amdgpu 0000:04:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00664500 (102.69.0)
amdgpu 0000:04:00.0: amdgpu: SMU driver if version not matched
amdgpu 0000:04:00.0: amdgpu: SMU is resumed successfully!
amdgpu 0000:04:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
amdgpu 0000:04:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
amdgpu 0000:04:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x0A000601
amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
amdgpu 0000:04:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
amdgpu 0000:04:00.0: amdgpu: GPU reset(12) succeeded!
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
```

---

### 评论 #3 — lucbruni-amd (2026-03-11T15:13:15Z)

@yasharhon, thanks for the logs.

Do you have a minimal reproducer script (can just be a simple Python script causing the crash - no need to provide anything before entering container yet)?

---

### 评论 #4 — yasharhon (2026-03-12T21:42:08Z)

@lucbruni-amd What I ran inside the container was
```python
import jax
import jax.numpy as jnp
print(jax.devices())
x = jnp.arange(5)
print(x)
```

---

### 评论 #5 — lucbruni-amd (2026-03-16T20:56:54Z)

Thanks for the script. I am unable to reproduce this with ROCm 7.2.0, `6.17.0-19-generic` kernel, 9060XT, running the script in `rocm/jax:latest`. Does this happen intermittently or every time? Could you post the `/sys/class/drm/card1/device/devcoredump/data` coredump?

The crash occurred with the desktop (gnome-shell, Xwayland) and ROCm compute sharing the GPU according to your `dmesg` logs. I wonder if you do not encounter the crash by first logging out of your graphical session and running that container/script via `ssh` from another device.

---

### 评论 #6 — yasharhon (2026-03-24T18:03:31Z)

It happens consistently. The core dump was illegible, but ended with `VRAM lost check is skipped!`. Too long to post, it seems.

Setting up an SSH connection to my desktop might take some time, I might have to get back to you 

---

### 评论 #7 — MaoxinYee (2026-04-10T21:28:10Z)

same issue
linux-generic-hwe-24.04 is already the newest version (6.17.0-20.20~24.04.1).
AMD-SMI 26.2.2+e1a6bc5663    amdgpu version: 6.16.13  ROCm version: 7.2.1 




---

### 评论 #8 — lucbruni-amd (2026-04-13T13:57:32Z)

Thanks @MaoxinYee - are you running the same workload as OP?

---

### 评论 #9 — MaoxinYee (2026-04-13T14:13:52Z)

I have resolved my issues by installing an OEM version of the kernel.
Follow the link  : https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html


---

### 评论 #10 — lucbruni-amd (2026-04-13T15:47:46Z)

Thanks @MaoxinYee. @yasharhon, could you please try swapping kernels per the above workaround?

---

### 评论 #11 — yasharhon (2026-04-13T19:13:05Z)

@lucbruni-amd You're gonna have to clarify if you want me to do that.

My current graphics drivers are working, and per our discussion in #5998, so are the various ML libraries with the env variable workaround. From what I can tell, given that I went the straightforward route for graphics installation with `amdgpu-dkms`, this would require reinstalling both my graphics drivers and ROCm. Why in the world would I do that?

---

### 评论 #12 — lucbruni-amd (2026-05-13T18:51:56Z)

@yasharhon, then we can continue investigating. Were you able to set up the separate SSH connection that reproduced the crash?

If so, please upload the full `devcoredump` to [gist](https://gist.github.com/).

---
