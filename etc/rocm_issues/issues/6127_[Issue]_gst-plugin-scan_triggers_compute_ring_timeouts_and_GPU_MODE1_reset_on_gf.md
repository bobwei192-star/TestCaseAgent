# [Issue]: gst-plugin-scan triggers compute ring timeouts and GPU MODE1 reset on gfx1201 (RDNA 4)

> **Issue #6127**
> **状态**: open
> **创建时间**: 2026-04-08T03:03:53Z
> **更新时间**: 2026-05-19T08:40:13Z
> **作者**: nathancassano
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6127

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

GStreamer's gst-plugin-scan process causes repeated compute ring timeouts, null-pointer page faults, and ultimately a MODE1 GPU reset (with VRAM loss / black screen) when the libgstvaapi.so plugin probes GPU compute queues at login time.                                                                                                                              **Environment:** 
  - OS: Ubuntu 24.04.3 LTS (Noble Numbat)
  - CPU: 12th Gen Intel(R) Core(TM) i5-12600KF
  - GPU: gfx1201 — AMD Radeon AI PRO R9700 (PCI 1002:7551)
  - ROCm: 7.2.0 
  - Kernel: 6.17.0-1012-oem 
  - GStreamer VA-API: gstreamer1.0-vaapi 1.24.2-1                                     
                                                                                                                                                                                              **Observed Behavior**
                                                                                                                                                                                            
  Sequential compute ring timeouts escalate to a full GPU reset:                                                                                                                              
   
  [34.96] ring comp_1.1.0 timeout — Process gst-plugin-scan pid 4087                                                                                                                          
          [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0) addr 0x0000000000000000                                                                                                       
          Ring comp_1.1.0 reset succeeded                                                                                                                                                     
                                                                                                                                                                                              
  [37.00] ring comp_1.0.1 timeout — same process, same null-address page fault                                                                                                                
          Ring comp_1.0.1 reset succeeded                                                                                                                                                     
                                                                                                                                                                                              
  [39.05] ring comp_1.1.1 timeout — same pattern                                                                                                                                              
          Ring comp_1.1.1 reset FAILED
                                                                                                                                                                                              
  [39.78] MODE1 reset
  [40.84] VRAM is lost due to GPU reset!
                                                                                                                                                                                              
Result: black screen / display lockup. If the MODE1 reset succeeds, the desktop eventually recovers. If it doesn't, the system requires a hard reboot.                                      
   


### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

12th Gen Intel(R) Core(TM) i5-12600KF

### GPU

AMD Radeon AI PRO R9700

### ROCm Version

7.2.0 

### ROCm Component

_No response_

### Steps to Reproduce

  1. Boot/login with gstreamer1.0-vaapi installed and libgstvaapi.so present in /usr/lib/x86_64-linux-gnu/gstreamer-1.0/                                                                      
  2. GStreamer's gst-plugin-scan runs automatically to probe hardware codec capabilities
  3. The scanner submits compute work to the GPU that triggers null-pointer page faults                                                                                                       
                                                                                                                                                                                              
The issue is intermittent timing depends on whether gst-plugin-scan hits the GPU before or after the display compositor is fully initialized.        

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

mROCk module version 6.16.13 is loaded
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
  Name:                    12th Gen Intel(R) Core(TM) i5-12600KF
  Uuid:                    CPU-XX                             
  Marketing Name:          12th Gen Intel(R) Core(TM) i5-12600KF
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
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65628776(0x3e96a68) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65628776(0x3e96a68) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65628776(0x3e96a68) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65628776(0x3e96a68) KB             
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
  Uuid:                    GPU-bacdbed38da9cb26               
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

  **Workaround**
                                                                                                                                                                                            
  Disabling the GStreamer VA-API plugin resolves the issue:
  sudo mv /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstvaapi.so /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstvaapi.so.disabled
                                                                                                                                              
  **Additional Notes**
  - dmesg also shows an SMU firmware version mismatch: driver expects 0x2e, firmware reports 0x32                                                                                             
  - The GPU (gfx1201 / RDNA 4) is relatively new and kernel/mesa driver support
  

---

## 评论 (4 条)

### 评论 #1 — nathancassano (2026-04-08T03:13:09Z)

Additionally here is an exert from the kernel dmesg:

```
[   31.513163] rfkill: input handler enabled
[   32.842548] Lockdown: systemd-logind: hibernation is restricted; see man kernel_lockdown.7
[   32.883111] rfkill: input handler disabled
[   34.958357] amdgpu 0000:03:00.0: amdgpu: Dumping IP State
[   34.965182] amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
[   34.965313] amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[   34.965317] amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[   34.965321] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=7, emitted seq=9
[   34.965331] amdgpu 0000:03:00.0: amdgpu:  Process gst-plugin-scan pid 4087 thread gst-plugin:cs0 pid 4213
[   34.965338] amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.0 ring reset
[   34.965359] amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:0)
[   34.965512] amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
[   34.965517] amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
[   34.966247] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
[   34.966284] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   34.966296] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
[   34.966305] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[   34.966314] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[   34.966322] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[   34.966329] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x4
[   34.966336] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   34.966343] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x1
[   37.006266] amdgpu 0000:03:00.0: amdgpu: Dumping IP State
[   37.007690] amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
[   37.007712] amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[   37.007715] amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[   37.007719] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 timeout, signaled seq=29, emitted seq=31
[   37.007729] amdgpu 0000:03:00.0: amdgpu:  Process gst-plugin-scan pid 4087 thread gst-plugin:cs0 pid 4213
[   37.007735] amdgpu 0000:03:00.0: amdgpu: Starting comp_1.0.1 ring reset
[   37.007750] amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:0:1)
[   37.007952] amdgpu 0000:03:00.0: amdgpu: Ring comp_1.0.1 reset succeeded
[   37.007958] amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
[   37.008582] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
[   37.008600] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   37.008607] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
[   37.008612] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[   37.008616] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[   37.008619] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[   37.008632] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x4
[   37.008635] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   37.008638] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x1
[   39.054319] amdgpu 0000:03:00.0: amdgpu: Dumping IP State
[   39.056097] amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
[   39.056118] amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[   39.056122] amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[   39.056126] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=17, emitted seq=19
[   39.056136] amdgpu 0000:03:00.0: amdgpu:  Process gst-plugin-scan pid 4087 thread gst-plugin:cs0 pid 4213
[   39.056142] amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.1 ring reset
[   39.056156] amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:1)
[   39.056992] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
[   39.057010] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   39.057017] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
[   39.057022] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[   39.057026] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[   39.057030] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[   39.057033] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x4
[   39.057036] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   39.057039] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x1
[   39.408262] amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.1 reset failed
[   39.408265] amdgpu 0000:03:00.0: amdgpu: GPU reset begin!. Source:  1
[   39.789207] amdgpu 0000:03:00.0: amdgpu: MODE1 reset
[   39.789215] amdgpu 0000:03:00.0: amdgpu: GPU mode1 reset
[   39.789288] amdgpu 0000:03:00.0: amdgpu: GPU smu mode1 reset
[   40.846548] amdgpu 0000:03:00.0: amdgpu: GPU reset succeeded, trying to resume
[   40.846740] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x00000087D6B00000).
[   40.846805] amdgpu 0000:03:00.0: amdgpu: VRAM is lost due to GPU reset!
[   40.846809] amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
[   41.079153] amdgpu 0000:03:00.0: amdgpu: GECC is disabled, set amdgpu_ras_enable=1 to enable GECC in next boot cycle if needed
[   41.084125] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[   41.084128] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[   41.084131] amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
[   41.084135] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684b00 (104.75.0)
[   41.084139] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[   41.114374] amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
[   41.114601] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
[   41.114605] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
[   41.123843] amdgpu 0000:03:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x0A000601
[   41.623207] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[   41.623212] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[   41.623213] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[   41.623213] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
[   41.623215] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
[   41.623216] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
[   41.623216] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
[   41.623217] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[   41.623218] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[   41.629454] amdgpu 0000:03:00.0: amdgpu: GPU reset(3) succeeded!
[   41.644012] amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
[   42.997448] rfkill: input handler enabled
[   43.069599] rfkill: input handler disabled
[   43.295948] rfkill: input handler enabled
[   45.716611] rfkill: input handler disabled
[   45.852078] Lockdown: systemd-logind: hibernation is restricted; see man kernel_lockdown.7
[  103.826962] rfkill: input handler enabled
```

---

### 评论 #2 — amd-nicknick (2026-04-29T13:56:16Z)

Hi @nathancassano, I tried several boot cycles but I couldn't reproduce this.
Do you have the amdgpu-dkms installed?

Kindly let me know if there's additional steps I need to take in order to repro this.
I made sure that vaapi plugin is visible to gstream.

Thanks!

---

### 评论 #3 — nathancassano (2026-05-12T05:12:42Z)

  Hi @amd-nicknick — thanks for taking a look. Yes, amdgpu-dkms is installed (6.16.13-2278356.24.04, matches the mROCk module version 6.16.13 reported by rocminfo).
  
  Full hardware/firmware details in case any of these matter for repro:

  - System: Alienware Aurora R13, board 0C92D0, BIOS 1.12.0 dated 2023-03-09 (predates RDNA 4)
  - Chipset: Intel Z690 (Alder Lake-S PCH, host bridge 8086:4648)
  - CPU: i5-12600KF
  - GPU: Radeon AI PRO R9700, PCI 1002:7551 rev c0, subsystem 1849:5413 (ASRock-branded, not reference)
  - VBIOS: 113-APM107573-101
  - On-card PCIe switch: 1002:1478 upstream / 1002:1479 downstream
  - Resizable BAR enabled (32 GB prefetchable BAR0)
  - amdgpu-dkms-firmware: 30.30.0.0.30300000
  - ROCm 7.2.0
  - Kernel: 6.17.0-1020-oem (Ubuntu 24.04.3)
  - IOMMU: Intel VT-d enabled


---

### 评论 #4 — amd-nicknick (2026-05-19T08:40:13Z)

Thanks! I still cannot repro this with the steps you described above.
As alignment check:
1. Could you try switching to generic kernel? On desktops we support generic kernel instead of OEM one.
2. Try using the preview 31.20 driver, we have some GEM memory handling fixes checked-in there: https://instinct.docs.amd.com/projects/amdgpu-docs/en/31.20.0-preview/index.html

---
