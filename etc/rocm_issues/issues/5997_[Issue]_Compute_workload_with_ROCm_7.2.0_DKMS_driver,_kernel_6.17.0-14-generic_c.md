# [Issue]: Compute workload with ROCm 7.2.0 DKMS driver, kernel 6.17.0-14-generic causes system freeze with graphical environment

> **Issue #5997**
> **状态**: closed
> **创建时间**: 2026-02-24T22:30:05Z
> **更新时间**: 2026-05-07T13:33:06Z
> **关闭时间**: 2026-03-25T18:25:30Z
> **作者**: 11BelowStudio
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5997

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

Running a pytorch jupyter notebook with ROCm enabled causes my entire system to freeze up, requiring me to raise the elephant and restart. I think it's a ROCm issue.

Also, neofetch says my linux kernel version is `6.17.0-14-generic`

### Operating System

Linux Mint 22.3 (Zena) (Cinnamon)

### CPU

Intel(R) Core(TM) i5-4690 CPU @ 3.50GHz

### GPU

AMD Radeon RX 9060 XT

### ROCm Version

ROCm 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Have ROCm installed, with everything on default settings ~~I have no idea how to change them from the default settings~~
2. Open DataLore, with this project and branch open: <https://github.com/11BelowStudio/auto_encoding_variable_bayes_sr/blob/rocm-crashing-my-desktop/vae.ipynb> (probably will still crash if you just open it in pycharm/vs code/plain old jupyter)
3. Make sure the ROCm version of pytorch is installed on your python venv or whatever
4. Run all cells
5. Wait a moment
6. Everything crashes, need to raise the elephant and reboot system.

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
  Name:                    Intel(R) Core(TM) i5-4690 CPU @ 3.50GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i5-4690 CPU @ 3.50GHz
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
  Max Clock Freq. (MHz):   3900                               
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
      Size:                    32810768(0x1f4a710) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32810768(0x1f4a710) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32810768(0x1f4a710) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32810768(0x1f4a710) KB             
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
  Uuid:                    GPU-c2524b2d872c04c5               
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
  Max Clock Freq. (MHz):   2780                               
  BDFID:                   768                                
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

Here's the journalctl entry from the most recent time it crashed, I'd rather not crash my desktop again (as raising the elephant seems to screw around with my profiles on firefox, and is probably having side-effects on other parts of my system as well): [2026_02_24_21_31_28_journalctl.log](https://github.com/user-attachments/files/25531836/2026_02_24_21_31_28_journalctl.log)

Unfortunately, despite the directions in the journalctl log, `/sys/class/drm/card1/device/devcoredump/data` doesn't seem to exist, so I can't give you any data from there.

The main things of note seem to be:
* `Feb 24 21:28:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 timeout, signaled seq=384, emitted seq=387`
* `Feb 24 21:28:45 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=78602, emitted seq=78606`



---

## 评论 (26 条)

### 评论 #1 — 11BelowStudio (2026-02-25T19:03:40Z)

I decided to give it another go today - still broken, of course. However, this new dmesg log file has some interesting tidbits for your consideration [2026_02_25_18_28_12_journalctl_dmesg.log](https://github.com/user-attachments/files/25554346/2026_02_25_18_28_12_journalctl_dmesg.log)

<details><summary>Interesting logs during bootup</summary>
<pre><code>
Feb 25 17:57:56 minty kernel: amdkcl: loading out-of-tree module taints kernel.
Feb 25 17:57:56 minty kernel: amdkcl: module verification failed: signature and/or required key missing - tainting kernel
...

Feb 25 17:57:56 minty kernel: [drm] amdgpu kernel modesetting enabled.
Feb 25 17:57:56 minty kernel: [drm] amdgpu version: 6.16.13
Feb 25 17:57:56 minty kernel: [drm] OS DRM version: 6.17.0
...
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 10 <mes_v12_0_0> (mes_v12_0)
Feb 25 17:57:56 minty kernel: resource: resource sanity check: requesting [mem 0x00000000000c0000-0x00000000000dffff], which spans more than PCI Bus 0000:00 [mem 0x000d0000-0x000dffff window]
Feb 25 17:57:56 minty kernel: caller pci_map_rom+0x6c/0x1d0 mapping multiple BARs
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: No more image in the PCI ROM
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from ROM BAR
Feb 25 17:57:56 minty kernel: amdgpu: ATOM BIOS: 113-44TC6SHB1-P03
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: vgaarb: deactivate vga console
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: VRAM: 16304M 0x0000008000000000 - 0x00000083FAFFFFFF (16304M used)
...
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x0A000601
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] REG_WAIT timeout 1us * 150000 tries - optc401_disable_crtc line:235
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
...
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: MES FW version must be >= 0x82 to enable LR compute workaround.
...
Feb 25 17:57:56 minty kernel: [drm] Initialized amdgpu 3.64.0 for 0000:03:00.0 on minor 1
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Failed to setup vendor infoframe on connector HDMI-A-1: -22
Feb 25 17:57:56 minty kernel: fbcon: amdgpudrmfb (fb0) is primary device
Feb 25 17:57:56 minty kernel: fbcon: Deferring console take-over
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: [drm] fb0: amdgpudrmfb frame buffer device
Feb 25 17:57:56 minty kernel: [drm] pre_validate_dsc:1955 MST_DSC dsc precompute is not needed
Feb 25 17:57:56 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] REG_WAIT timeout 1us * 150000 tries - optc401_disable_crtc line:235
Feb 25 17:57:56 minty kernel: raid6: avx2x4   gen() 30197 MB/s

</code></pre>
</details>

----
<details><summary>confusing GPU reset (not sure what this was)</summary>
this was a few minutes before The Incident.
<pre></code>
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=275, emitted seq=276
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process cef_server pid 17230 thread cef_server:cs0 pid 17254
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.1 ring reset
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:1)
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.1 reset succeeded
Feb 25 18:20:59 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
</code></pre>
</details>

---
<details><summary>the crash itself</summary>
Same situation as last time (running a jupyter notebook containing pytorch using ROCm)
<pre><code>
Feb 25 18:25:04 minty kernel: [UFW BLOCK] IN=enp5s0 OUT= MAC=01:00:5e:00:00:01:60:8d:26:aa:c5:64:08:00 SRC=192.168.1.254 DST=224.0.0.1 LEN=36 TOS=0x00 PREC=0x00 TTL=1 ID=64491 DF PROTO=2 
Feb 25 18:25:18 minty kernel: sysrq: Emergency Sync
Feb 25 18:25:18 minty kernel: Emergency Sync complete
Feb 25 18:25:23 minty kernel: sysrq: This sysrq operation is disabled.
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=175151, emitted seq=175154
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process cef_server pid 17230 thread cef_server:cs0 pid 17254
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
Feb 25 18:25:34 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=340, emitted seq=342
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process cef_server pid 20422 thread cef_server:cs0 pid 20426
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.0 ring reset
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:0)
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:          MORE_FAULTS: 0x0
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:          WALKER_ERROR: 0x0
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:          PERMISSION_FAULTS: 0x4
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:          MAPPING_ERROR: 0x0
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu:          RW: 0x1
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.0 reset failed
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset begin!. Source:  1
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: Suspending all queues failed
Feb 25 18:25:36 minty kernel: amdgpu 0000:03:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 2 for dev 16300
Feb 25 18:25:38 minty kernel: amdgpu 0000:03:00.0: amdgpu: MES(1) failed to respond to msg=REMOVE_QUEUE
Feb 25 18:25:38 minty kernel: amdgpu 0000:03:00.0: amdgpu: failed to unmap legacy queue
Feb 25 18:25:38 minty kernel: amdgpu 0000:03:00.0: amdgpu: MODE1 reset
Feb 25 18:25:38 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU mode1 reset
Feb 25 18:25:38 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU smu mode1 reset
Feb 25 18:25:39 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset succeeded, trying to resume
Feb 25 18:25:39 minty kernel: amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x0000008000000000).
Feb 25 18:25:39 minty kernel: amdgpu 0000:03:00.0: amdgpu: VRAM is lost due to GPU reset!
Feb 25 18:25:39 minty kernel: amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: RAS: optional ras ta ucode is not available
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00664500 (102.69.0)
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x0A000601
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset(3) succeeded!
Feb 25 18:25:40 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 18:26:13 minty kernel: sysrq: This sysrq operation is disabled.
Feb 25 18:26:20 minty kernel: sysrq: This sysrq operation is disabled.
Feb 25 18:26:39 minty kernel: sysrq: This sysrq operation is disabled.
Feb 25 18:26:48 minty kernel: sysrq: Emergency Sync
Feb 25 18:26:48 minty kernel: Emergency Sync complete
Feb 25 18:27:09 minty kernel: [UFW BLOCK] IN=enp5s0 OUT= MAC=01:00:5e:00:00:01:60:8d:26:aa:c5:64:08:00 SRC=192.168.1.254 DST=224.0.0.1 LEN=36 TOS=0x00 PREC=0x00 TTL=1 ID=22167 DF PROTO=2 
Feb 25 18:28:04 minty kernel: sysrq: Emergency Sync
Feb 25 18:28:04 minty kernel: Emergency Sync complete
Feb 25 18:28:11 minty kernel: sysrq: Emergency Remount R/O
Feb 25 18:28:12 minty kernel: EXT4-fs (nvme0n1p3): re-mounted 709762bb-7d55-4daa-8c5c-8bd9ae3f5476 ro.
Feb 25 18:28:12 minty kernel: EXT4-fs (sdc2): re-mounted 06f28a52-65d2-4ba4-803b-a077d4ce3164 ro.
</code></pre>
</details>

The problem appears to be a page fault with the GPU, within the comp_1.1.0 ring. However, like last night, I could not find any core dump file.

---

### 评论 #2 — 11BelowStudio (2026-02-25T19:32:46Z)

aaaaaaaand it just happened again, except this time I just had Firefox open (no pytorch was attempted during that bootup).

Here's the full dmesg log, and once again, no core dumps could be found on disk [2026_02_25_19_16_10_journalctl_dmesg.log](https://github.com/user-attachments/files/25555362/2026_02_25_19_16_10_journalctl_dmesg.log)

Started out with just
```
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=151, emitted seq=153
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process firefox-bin pid 7401 thread firefox:cs0 pid 7453
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.1 ring reset
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:1)
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:          MORE_FAULTS: 0x0
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:          WALKER_ERROR: 0x0
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:          PERMISSION_FAULTS: 0x4
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:          MAPPING_ERROR: 0x0
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu:          RW: 0x1
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.1 reset succeeded
Feb 25 19:15:03 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 19:15:04 minty kernel: [UFW BLOCK] IN=enp5s0 OUT= MAC=01:00:5e:00:00:01:60:8d:26:aa:c5:64:08:00 SRC=192.168.1.254 DST=224.0.0.1 LEN=36 TOS=0x00 PREC=0x00 TTL=1 ID=63493 DF PROTO=2 
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=152, emitted seq=153
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process firefox-bin pid 7401 thread firefox:cs0 pid 7453
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.1 ring reset
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:1)
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.1 reset succeeded
Feb 25 19:15:05 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=219135, emitted seq=219137
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process firefox-bin pid 7401 thread firefox:cs0 pid 7453
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
Feb 25 19:15:13 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 19:15:15 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
```
looped around a bit before another page fault
```
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=125, emitted seq=129
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process firefox-bin pid 7401 thread firefox:cs0 pid 7453
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.0 ring reset
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:0)
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:32 vmid:0 pasid:0)
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040A40
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:          MORE_FAULTS: 0x0
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:          WALKER_ERROR: 0x0
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:          PERMISSION_FAULTS: 0x4
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:          MAPPING_ERROR: 0x0
Feb 25 19:15:17 minty kernel: amdgpu 0000:03:00.0: amdgpu:          RW: 0x1
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=127, emitted seq=129
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process firefox-bin pid 7401 thread firefox:cs0 pid 7453
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.0 ring reset
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: reset compute queue (1:1:0)
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring comp_1.1.0 reset succeeded
Feb 25 19:15:19 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 19:15:21 minty kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
```

then continued looping around crashing but resetting but the screen was still frozen and I was unable to do anything with my computer
```
Feb 25 19:15:21 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=219182, emitted seq=219184
Feb 25 19:15:21 minty kernel: amdgpu 0000:03:00.0: amdgpu:  Process firefox-bin pid 7401 thread firefox:cs0 pid 7453
Feb 25 19:15:21 minty kernel: amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
Feb 25 19:15:23 minty kernel: amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset failed
Feb 25 19:15:23 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset begin!. Source:  1
Feb 25 19:15:26 minty kernel: amdgpu 0000:03:00.0: amdgpu: MES(1) failed to respond to msg=REMOVE_QUEUE
Feb 25 19:15:26 minty kernel: amdgpu 0000:03:00.0: amdgpu: failed to unmap legacy queue
Feb 25 19:15:26 minty kernel: [drm:gfx_v12_0_cp_gfx_enable.isra.0 [amdgpu]] *ERROR* failed to halt cp gfx
Feb 25 19:15:26 minty kernel: amdgpu 0000:03:00.0: amdgpu: MODE1 reset
Feb 25 19:15:26 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU mode1 reset
Feb 25 19:15:26 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU smu mode1 reset
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset succeeded, trying to resume
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x0000008000000000).
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: VRAM is lost due to GPU reset!
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: RAS: optional ras ta ucode is not available
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00664500 (102.69.0)
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x0A000601
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset(7) succeeded!
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Feb 25 19:15:27 minty kernel: amdgpu 0000:03:00.0: amdgpu: [drm] *ERROR* Failed to initialize parser -125!
Feb 25 19:15:52 minty kernel: sysrq: This sysrq operation is disabled.
Feb 25 19:15:58 minty kernel: sysrq: This sysrq operation is disabled.
Feb 25 19:16:02 minty kernel: sysrq: This sysrq operation is disabled.
Feb 25 19:16:05 minty kernel: sysrq: Emergency Sync
Feb 25 19:16:05 minty kernel: Emergency Sync complete
Feb 25 19:16:09 minty kernel: sysrq: Emergency Remount R/O
Feb 25 19:16:09 minty kernel: EXT4-fs (nvme0n1p3): re-mounted 709762bb-7d55-4daa-8c5c-8bd9ae3f5476 ro.
Feb 25 19:16:10 minty kernel: EXT4-fs (sdc2): re-mounted 06f28a52-65d2-4ba4-803b-a077d4ce3164 ro.
```



---

### 评论 #3 — schung-amd (2026-02-25T19:49:18Z)

Hi @11BelowStudio, thanks for the report and the detailed logs, I'll try to repro and take a look. From your most recent update it does sound like this might be an issue with the driver and not isolated to torch, so I'd recommend uninstalling ROCm for now and hopefully that will stabilize things. If your system is fine after that I'd suggest installing without the DKMS module so your system will use the in-box kernel driver:

```
wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/noble/amdgpu-install_7.2.70200-1_all.deb
sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
amdgpu-install -y --usecase=rocm --no-dkms
```

which may not fix the torch-related issues but hopefully won't break your other system applications. We did also have an issue with some incompatible mesa drivers before, what is the output of `apt list | grep mesa` on your system?

---

### 评论 #4 — 11BelowStudio (2026-02-25T20:07:05Z)

Thanks for the response. So

> I'd recommend uninstalling ROCm for now and hopefully that will stabilize things.

On it. I will let you know if things crash again. Not sure if I'll attempt reinstalling it in the immediate future, but I'll give the non-dkms version a whirl if you need me to investigate that.

> We did also have an issue with some incompatible mesa drivers before, what is the output of `apt list | grep mesa` on your system?

```
apt list | grep mesa

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

libd3dadapter9-mesa-dev/noble-updates 25.0.7-0ubuntu0.24.04.2 amd64
libd3dadapter9-mesa-dev/noble-updates 25.0.7-0ubuntu0.24.04.2 i386
libd3dadapter9-mesa/noble-updates 25.0.7-0ubuntu0.24.04.2 amd64
libd3dadapter9-mesa/noble-updates 25.0.7-0ubuntu0.24.04.2 i386
libegl-mesa0/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
libegl-mesa0/noble-updates,now 25.2.8-0ubuntu0.24.04.1 i386 [installed,automatic]
libegl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libegl1-amdgpu-mesa-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
libegl1-amdgpu-mesa/noble 1:26.0.0.70200-2278374.24.04 amd64
libegl1-amdgpu-mesa/noble 1:26.0.0.70200-2278374.24.04 i386
libegl1-mesa-dev/noble-updates 25.2.8-0ubuntu0.24.04.1 amd64
libegl1-mesa-dev/noble-updates 25.2.8-0ubuntu0.24.04.1 i386
libgl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-dev/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-dri/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-dri/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-amdgpu-mesa-glx/noble 1:26.0.0.70200-2278374.24.04 amd64
libgl1-amdgpu-mesa-glx/noble 1:26.0.0.70200-2278374.24.04 i386
libgl1-mesa-dev/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
libgl1-mesa-dev/noble-updates 25.2.8-0ubuntu0.24.04.1 i386
libgl1-mesa-dri/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
libgl1-mesa-dri/noble-updates,now 25.2.8-0ubuntu0.24.04.1 i386 [installed]
libglapi-mesa/noble-updates,now 24.2.8-1ubuntu1~24.04.1 amd64 [installed]
libglapi-mesa/noble-updates 24.2.8-1ubuntu1~24.04.1 i386
libgles2-mesa-dev/noble-updates 25.2.8-0ubuntu0.24.04.1 amd64
libgles2-mesa-dev/noble-updates 25.2.8-0ubuntu0.24.04.1 i386
libglu1-mesa-dev/noble,now 9.0.2-1.1build1 amd64 [installed,automatic]
libglu1-mesa-dev/noble 9.0.2-1.1build1 i386
libglu1-mesa/noble,now 9.0.2-1.1build1 amd64 [installed]
libglu1-mesa/noble 9.0.2-1.1build1 i386
libglw1-mesa-dev/noble 8.0.0-3 amd64
libglw1t64-mesa/noble 8.0.0-3 amd64
libglx-mesa0/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
libglx-mesa0/noble-updates,now 25.2.8-0ubuntu0.24.04.1 i386 [installed,automatic]
libosmesa6-dev/noble-updates 25.1.7-1ubuntu2~24.04.1 amd64
libosmesa6-dev/noble-updates 25.1.7-1ubuntu2~24.04.1 i386
libosmesa6/noble-updates,now 25.1.7-1ubuntu2~24.04.1 amd64 [installed,automatic]
libosmesa6/noble-updates,now 25.1.7-1ubuntu2~24.04.1 i386 [installed,automatic]
librust-osmesa-sys-dev/noble 0.1.2-1 amd64
mesa-amdgpu-common-dev/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-common-dev/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-libgallium/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-libgallium/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-va-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-va-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-amdgpu-vulkan-drivers/noble 1:26.0.0.70200-2278374.24.04 amd64
mesa-amdgpu-vulkan-drivers/noble 1:26.0.0.70200-2278374.24.04 i386
mesa-common-dev/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
mesa-common-dev/noble-updates 25.2.8-0ubuntu0.24.04.1 i386
mesa-drm-shim/noble-updates 25.2.8-0ubuntu0.24.04.1 amd64
mesa-drm-shim/noble-updates 25.2.8-0ubuntu0.24.04.1 i386
mesa-libgallium/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
mesa-libgallium/noble-updates,now 25.2.8-0ubuntu0.24.04.1 i386 [installed,automatic]
mesa-opencl-icd/noble-updates 25.2.8-0ubuntu0.24.04.1 amd64
mesa-opencl-icd/noble-updates 25.0.7-0ubuntu0.24.04.2 i386
mesa-utils-bin/noble,now 9.0.0-2 amd64 [installed]
mesa-utils/noble,now 9.0.0-2 amd64 [installed]
mesa-va-drivers/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
mesa-va-drivers/noble-updates,now 25.2.8-0ubuntu0.24.04.1 i386 [installed,automatic]
mesa-vdpau-drivers/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
mesa-vdpau-drivers/noble-updates,now 25.2.8-0ubuntu0.24.04.1 i386 [installed,automatic]
mesa-vulkan-drivers/noble-updates,now 25.2.8-0ubuntu0.24.04.1 amd64 [installed]
mesa-vulkan-drivers/noble-updates,now 25.2.8-0ubuntu0.24.04.1 i386 [installed,automatic]
mesaflash/noble 3.4.6-1 amd64
```

Anywho, please let me know if anything interesting happens on your end, or if you need me to try testing anything else locally.

---

### 评论 #5 — Only8Bits (2026-02-26T12:38:56Z)

I had a similar issue a few days ago - I was not using pytorch anymore but I was running it earlier that day. After switching tabs in Firefox to one with video playback my mouse slowed down, then the display system froze completly. The issue probably started earlier though (journalctl -r -g amdgpu):

> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset compute queue (1:2:1)
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting comp_1.2.1 ring reset
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 2846 thread firefox:cs0 pid 29>
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=1709, emitted>
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcor>
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 16 12:20:54 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset compute queue (1:2:1)
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting comp_1.2.1 ring reset
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 2846 thread firefox:cs0 pid 29>
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=1684, emitted>
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcor>
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 16 11:59:12 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 16 11:52:13 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 35 times, con>
> feb 16 11:52:11 x kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us>
> feb 16 11:52:10 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 19 times, con>
> feb 16 11:52:09 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 11 times, con>
> feb 16 11:52:09 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 7 times, cons>
> feb 16 11:32:36 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 5 times, cons>
> feb 16 11:06:34 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, cons>

And then the crash itself in the afternoon:

> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:          RW: 0x0
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:          MAPPING_ERROR: 0x1
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:          WALKER_ERROR: 0x1
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:          MORE_FAULTS: 0x1
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B33
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 17:33:10 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid>

After a few of these paging events the main blow:

> -- Boot 74a89d02f9e347f4ade8ec081796f50d --
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset(17) succeeded!
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002D00
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU is resumed successfully!
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU driver if version not matched
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if versi>
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU is resuming...
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is n>
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: RAP: optional rap ta ucode is not available
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: reserve 0x1300000 from 0x84fc000000 for PSP TMR
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: PSP is resuming...
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: VRAM is lost due to GPU reset!
> feb 16 18:39:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset succeeded, trying to resume
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU smu mode1 reset
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU mode1 reset
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: MODE1 reset
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 4>
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: Suspending all queues failed
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: Suspending all queues failed
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset begin!. Source:  1
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring comp_1.2.1 reset failed
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:          RW: 0x1
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:          MAPPING_ERROR: 0x1
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:          WALKER_ERROR: 0x1
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:          MORE_FAULTS: 0x0
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B52
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x0000000000000000 fr>
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid>
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset compute queue (1:2:1)
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting comp_1.2.1 ring reset
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process kwin_x11 pid 2335 thread kwin_x11:cs0 pid >
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=2961, emitted>
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcor>
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 16 18:39:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State

It says the subsystem has recovered but no such luck, I had to hard reboot. This only happend once so far but I've only started using ROCm 7.2 and it's driver recently, and this was the first time system crashed while not doing any compute on GPU at that moment.

HW: Radeon 7900XT on Kubuntu 24.04

---

### 评论 #6 — schung-amd (2026-02-26T15:18:18Z)

@Only8Bits Thanks for the additional logs. Are you on the same kernel version (`6.17.0-14-generic`)? If you're willing to try, is this fixed after removing the DKMS module (either via `sudo apt autoremove amdgpu-dkms dkms` or uninstalling and reinstalling ROCm with 
```
amdgpu-install --uninstall 
amdgpu-install -y --usecase=rocm --no-dkms
```
and/or explicitly installing the graphics components with `amdgpu-install -y --usecase=graphics,rocm`?

---

### 评论 #7 — Only8Bits (2026-02-26T17:42:26Z)

The kernel version indeed is 6.17.0-14-generic #14~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Jan 15 15:52:10 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

I'll try to remove amdgpu-dkms over the weekend, right now I need the system running.

---

### 评论 #8 — 11BelowStudio (2026-02-27T00:49:00Z)

> If your system is fine after that I'd suggest installing without the DKMS module so your system will use the in-box kernel driver:
> 
> which may not fix the torch-related issues but hopefully won't break your other system applications.

Good news!

I decided to reinstall it without DKMS earlier on today, and my computer hasn't crashed yet. Furthermore, Pytorch still works with acceleration even with the non-DKMS version of ROCm.

For the time being, I guess it's fixed - but I'll let you know if I encounter any more issues later on.

---

### 评论 #9 — Only8Bits (2026-02-27T20:47:33Z)

Not so good news on my end. The non-dkms driver also crashed on me, but during compute task so it's more "typical" crash than the one I described before. Logs don't look all that different though.

Again it seems amdgpu has already tripped over something in the morning but seemingly kept going:

> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset compute queue (1:2:1)
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting comp_1.2.1 ring reset
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process Xorg pid 1897 thread Xorg:cs0 pid 1898
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=19, emitted seq=21
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 10:48:44 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 10:19:36 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 67 times, consider switching to WQ_UNBOUND
> feb 27 10:19:33 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 35 times, consider switching to WQ_UNBOUND
> feb 27 10:19:30 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 19 times, consider switching to WQ_UNBOUND
> feb 27 10:11:46 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
> feb 27 10:10:57 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
> feb 27 10:10:42 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
> feb 27 10:10:37 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
> feb 27 09:37:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc dolphin(13275) task dolphin:cs0(13268) is non-zero when fini
> feb 27 09:37:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc kioslave5(13367) task kioslave5:cs0(13362) is non-zero when fini
> feb 27 09:37:13 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc kioslave5(13414) task kioslave5:cs0(13411) is non-zero when fini
> feb 27 09:37:04 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc kioslave5(13387) task kioslave5:cs0(13384) is non-zero when fini
> feb 27 09:36:53 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc kioslave5(13332) task kioslave5:cs0(13325) is non-zero when fini
> feb 27 09:36:45 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc kioclient5(13255) task kioclient:cs0(13252) is non-zero when fini

There were a few more events during the day:

> feb 27 15:56:17 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc kscreenlocker_g(33951) task kscreenloc:cs0(33949) is non-zero when fini
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring comp_1.2.0 reset succeeded
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset compute queue (1:2:0)
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting comp_1.2.0 ring reset
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process kwin_x11 pid 2429 thread kwin_x11:cs0 pid 2492
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.0 timeout, signaled seq=529, emitted seq=530
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 14:47:33 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 14:44:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc kscreenlocker_g(27747) task kscreenloc:cs0(27745) is non-zero when fini
> feb 27 14:03:14 x kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
> feb 27 14:03:10 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 515 times, consider switching to WQ_UNBOUND
> feb 27 13:08:46 x kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
> feb 27 12:51:47 x kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
> feb 27 12:17:51 x kernel: amdgpu 0000:0c:00.0: amdgpu: VM memory stats for proc okular(16385) task okular:cs0(16382) is non-zero when fini
> feb 27 12:10:49 x kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
> feb 27 12:10:39 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 259 times, consider switching to WQ_UNBOUND
> feb 27 11:17:27 x kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 131 times, consider switching to WQ_UNBOUND
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring comp_1.2.0 reset succeeded
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset compute queue (1:2:0)
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting comp_1.2.0 ring reset
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process kwin_x11 pid 2429 thread kwin_x11:cs0 pid 2492
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.0 timeout, signaled seq=516, emitted seq=517
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 11:00:37 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State

Then in the afternoon I had another job running and this one crashed the driver good, messing up X11 and freezing my display and disabling the keyboard:

> feb 27 16:55:35 x kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 19 times, consider switching to WQ_UNBOUND
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process kwin_x11 pid 2429 thread kwin_x11:cs0 pid 2492
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036139, emitted seq=1036141
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:31 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process kwin_x11 pid 2429 thread kwin_x11:cs0 pid 2492
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036137, emitted seq=1036141
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:29 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process Xorg pid 1897 thread Xorg:cs0 pid 1898
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036135, emitted seq=1036139
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:27 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process Xorg pid 1897 thread Xorg:cs0 pid 1898
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036133, emitted seq=1036137
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:25 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3091 thread firefox:cs0 pid 3233
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036132, emitted seq=1036135
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:23 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3091 thread firefox:cs0 pid 3233
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036131, emitted seq=1036133
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3091 thread firefox:cs0 pid 3233
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036087, emitted seq=1036090
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3091 thread firefox:cs0 pid 3233
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036086, emitted seq=1036088
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3091 thread firefox:cs0 pid 3233
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036046, emitted seq=1036048
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:11 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3091 thread firefox:cs0 pid 3233
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1036011, emitted seq=1036013
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:07 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3091 thread firefox:cs0 pid 3233
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1035947, emitted seq=1035949
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 27 16:50:02 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State

Firefox is again mentioned in the final crash sequence. This time it seems the job I started kept running so I hoped it would complete, but it has stalled somewhere at some point and didn't produce results I could trace. I was able to ssh into this machine from a laptop and restart the sddm service, getting the display and keyboard back but it resulted in killing all the previous windows and attached processes.

The dkms driver tends to crash when the compute task slowly allocates all the VRAM and leaves too little for X11 to work with, this one didn't do it - yet. I have not used it long enough to tell if it's more stable or I just didn't push it over the edge the right way.

Also of note is the VRAM clock behaviour on non-dkms driver during compute is identical to dkms and I have to resort to workarounds to avoid performance loss. Switching profile in pp_power_profile_mode to COMPUTE does not help.

---

### 评论 #10 — schung-amd (2026-02-27T20:55:10Z)

@Only8Bits Thanks for the update and additional logs. I've been able to reproduce some similar symptoms to the initial reports (system becoming unresponsive possibly triggered by Firefox video playback) but not consistently. I assume the issue you're seeing is not workload-dependent, but can you provide a reproducer just in case?

> Also of note is the VRAM clock behaviour on non-dkms driver during compute is identical to dkms and I have to resort to workarounds to avoid performance loss. Switching profile in pp_power_profile_mode to COMPUTE does not help.

I'm not sure what you're referring to here, was this reported elsewhere?

---

### 评论 #11 — Only8Bits (2026-02-27T21:19:18Z)

I wish I could offer a reproductible test case but that issue is quite random, and can even have different outcomes. The freeze is the most common one but I have seen recovery too, even hours later (when the compute task eventually finished), and almost immediate reboots as well. Though lately it's pretty much always slowdowns that announce the eventual total freeze. Best I can tell is run the compute hard - WAN video generation with settings that take as much VRAM as you can, while doing light desktop usage at the same time. Light because with heavy compute going on the system is barely usable. The usage part is optional, it will crash on it's own as well (with Firefox running, if that makes a difference). It can take minutes to (usually) hours before the system crashes. I've yet to see a crash while gaming though - it all seems compute related.

As for the VRAM clock, I mentioned it in another thread: https://github.com/ROCm/TheRock/issues/2591
TL;DR is the compute tasks are not a constant load and it looks to me that the driver is too eagerly downclocking VRAM to reduce power usage. It takes time to switch the states again I suppose because performance suffers. The way I now work around that is limit the available VRAM power states to the highest level only by doing:

echo "3" >/sys/class/drm/card1/device/pp_dpm_mclk

This however will prevent the card from going into low power mode, the fans keep going and power usage is some 50W higher than typical low power state. IMHO it would be better to just not downclock so aggressively when profile is switched to COMPUTE. This would prevent that ping-pong effect with memory clock and performance loss, while allowing low power state after compute is done. 

---

### 评论 #12 — aswindy (2026-02-28T00:22:47Z)

I have the same problem after update rocm 7.2 and correspondent torch. but it's normal on rocm 7.1.1. I sent sys log to chatgpt and it told me "ring comp_1.1.0 timeout
ring gfx_0.0.0 timeout
device wedged, but recovered through reset
page fault
GCVM_L2_PROTECTION_FAULT_STATUS
PERMISSION_FAULTS: 0x4" . these are why to crash. it suggested me to rollback to 7.1.1

---

### 评论 #13 — Only8Bits (2026-02-28T11:31:26Z)

I tried to create some sort of portable reproducer that wouldn't need half a day to crash the driver. I've made a ComfyUI workflow that creates 640x640 video with 129 frames using WanVideoWrapper nodes, that seems heavy enough to cause crashes more often. I can try to refine that a bit and share if it's of interest for debugging this issue.

I was watching the log at the same time as this workflow progressed and noticed a few things. I was trying to run this with torch compile using max-autotune-no-cudagraphs setting. I had first few "device wedged" log entries during the initial triton benchmark for optimal solutions, but all that recovered. Finally I had another freeze that I was hoping for, here's the log:

> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset(18) succeeded!
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002D00
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU is resumed successfully!
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU driver if version not matched
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8000 (78.128.0)
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU is resuming...
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: RAP: optional rap ta ucode is not available
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: reserve 0x1300000 from 0x84fc000000 for PSP TMR
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: PSP is resuming...
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: VRAM is lost due to GPU reset!
> feb 28 12:06:21 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset succeeded, trying to resume
> feb 28 12:06:20 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU smu mode1 reset
> feb 28 12:06:20 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU mode1 reset
> feb 28 12:06:20 x kernel: amdgpu 0000:0c:00.0: amdgpu: MODE1 reset
> feb 28 12:06:20 x kernel: [drm:gfx_v11_0_cp_gfx_enable.isra.0 [amdgpu]] *ERROR* failed to halt cp gfx
> feb 28 12:06:20 x kernel: amdgpu 0000:0c:00.0: amdgpu: failed to unmap legacy queue
> feb 28 12:06:20 x kernel: amdgpu 0000:0c:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 4 for dev 24677
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: Suspending all queues failed
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: Suspending all queues failed
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset begin!. Source:  1
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring gfx_0.0.0 reset failed
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: The CPFW hasn't support pipe reset yet.
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset via MES failed and try pipe reset -110
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: failed to reset legacy queue
> feb 28 12:06:18 x kernel: amdgpu 0000:0c:00.0: amdgpu: MES failed to respond to msg=RESET
> feb 28 12:06:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting gfx_0.0.0 ring reset
> feb 28 12:06:16 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process plasmashell pid 2438 thread plasmashel:cs0 pid 2468
> feb 28 12:06:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=500019, emitted seq=500021
> feb 28 12:06:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> feb 28 12:06:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> feb 28 12:06:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
> feb 28 12:06:16 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State

What is interesting is both the early events and the eventual crash happened as I was using Firefox, but not while switching tabs but rather while scrolling through the page (with mouse wheel). In fact it was this very issue page that caused the final freeze and there's no videos here (though I did visit some other tabs with video before that).

I'll disable Firefox HW acceleration now (though this didn't help before) and try a few more things, maybe I can narrow it down a bit more.

---

### 评论 #14 — schung-amd (2026-03-02T16:56:08Z)

Thanks for the updates. What version of `linux-firmware` are you on?

@aswindy Do you have the DKMS driver installed?
@Only8Bits A reproducer would be great, even if inconsistent. Are your crashes happening when using Firefox (or other graphical applications) while running the workflow, or do you see crashes even when not using torch? Also, if you have the opportunity to test, do you see these crashes with the display off as well?

---

### 评论 #15 — Only8Bits (2026-03-02T17:52:01Z)

APT reports linux-firmware/noble-updates,now 20240318.git3b128b60-0ubuntu2.25 amd64

Still working on the reproducer, the idea was to load the card for quite some time and I got exactly that but I'm still hoping for something crashing more often - this one also can take hours. Give me a few more days, this is time consuming and prevents me from using this machine for other tasks.

However I can say this: Disabling Firefox HW acceleration still does nothing to cure it. One of the freezes I got was me not even being near the machine, it was the screensaver/locker kicking in after some time that tripped it. Firefox was open though.
Another idea I had, and already tried in the past with good results, was to start the ComfyUI job and then CTRL+ALT+F3 to "text mode" console. I know it's not really a text mode anymore with UEFI but the important thing there is no GUI and very little screen refresh. None if no commands are typed and run. All the processes (including Firefox) are still running but not refreshing the screen in other words - and this seems way more stable. I've yet to trip this method into freeze - but it doesn't play well with the remote desktop access I use.

So I think the issue is connected to heavy compute running along frequent screen updates. That is what video playback and page scrolling will do. Firefox might be factor or just a red herring, not enough data points yet. I don't see crashes while not using torch, even that one crash outside compute job was after the Comfy finished and went idle, but still loaded.
Display off is something I need to retry with ROCm 7.2, it's on my list. I was even considering unplugging the DP cable to be sure the card is not driving anything. However on previous ROCm versions I did get crashes with the monitor being soft-off (but still powered on standby and DP cable connected) while using remote access via VNC. Not exactly sure if this qualifies as on or off.

---

### 评论 #16 — ehoogeveen-medweb (2026-03-02T19:31:05Z)

Not sure if related as I'm on Strix Halo with the Arch-based CachyOS, but I've found that setting `amdgpu.cwsr_enable=0` in the kernel commandline helps to prevent crashes from "long pauses". With cwsr disabled, I sometimes get big lag spikes while running heavy computation - but with it *enabled* I get crashes instead, including full system freezes.

---

### 评论 #17 — Only8Bits (2026-03-02T19:53:40Z)

I've tried that, after I found some posts from Strix users that it helps. I had this added to command line:

amdgpu.mcbp=0 amdgpu.cwsr_enable=0 amdgpu.queue_preemption_timeout_ms=1

Didn't do all that much when cudnn was disabled, but when I re-enabled it for testing I had very consistent reboots the moment VAE processing started. Got rid of all these and the reboots went away. Didn't investigate further which one caused this, I figured different arch might just have different driver bugs and what helps Strix is bad for RDNA3. I could try a deeper dive if it's of interest.

---

### 评论 #18 — schung-amd (2026-03-02T21:49:34Z)

@ehoogeveen-medweb What kernel version are you on? See https://rocm.docs.amd.com/en/latest/how-to/system-optimization/strixhalo.html#required-kernel-version. A note there does say that Arch should have some native fixes but I'm not sure what kernel versions those extend to or if that extends to CachyOS as well.

We had implemented a workaround for some issues seen on Strix Halo, but it was not fully effective. We have since addressed the root cause and have recently reverted the WA: https://lore.kernel.org/amd-gfx/20260225165116.46224-1-mario.limonciello@amd.com/. As the description of that commit states, this may have been causing instabilities on non-Strix products, which may be related to what @Only8Bits is seeing. I don't think there's a new kernel version with the revert yet.

@Only8Bits No rush, I'm also still working on getting a consistent reproducer for the issue. I'll let you know if I get there before you do.

---

### 评论 #19 — Only8Bits (2026-03-11T10:39:48Z)

This is just a small update, I have not abandoned the idea of creating some sort of reproducer but the random nature of the problem has me questioning, by now, not only this issue but also my sanity.

Long story short to make sure I can give a Comfy workflow to someone else and expect similar results I've updated all my sources and nodes to newest git versions. And there was some sort of Python update from Ubuntu, as well as new Firefox version. And now I get different behavior from my reproducer. Seems more stable but also more prone to memory fragmentation and OOM errors that cause it stop early. Makes the whole testing much more annoying than it already was.

I have observed, also quite random, two more issues - not related to the topic but caused by the reproducer task. First is the trick I mentioned earlier with switching to console mode, out of X windows, during the Comfy run. And switching the monitor off. Twice already this has caused the compute task to just stall at some point, as if the card eventually went to deep sleep even though a compute job was running. Not a crash, the task would resume the moment I turned the monitor on and used the keyboard to wake the screen up. Note my PC is set to display off after 10 minutes of inactivity but all deep sleep/hibernation modes are disabled. No amdgpu logs explaining what has happened, just seemingly a power-saving kicking in when it should not. I do not remember this happening with dkms driver, and I'm now using the non-dkms one.

The second thing is now the compute tasks somehow seem to load the system more evenly, the PC feels more "laggy" but is still usable. Depending on the task running I can even watch full screen videos without noticing any frame drops or the sort. Except when I'm using SageAttention (sageattn 1.0.6 with some minor source changes from Zluda folks to make it fast on AMD HW), this can still result in pretty severe desktop usability degradation (basically system freezes for 0.5s every 1s) - but this behavior is also not consistent. Just as I was about to report it, along with the Comfy workflow to reproduce it, it just went away. Also no logs from amdgpu, and forcing the VRAM clock to highest state does help to resolve it to some extent (as well as restore performance). Perhaps heavy mixing of floating point and integer operations is somehow a factor.

All in all I'm sort of back to the starting point and now trying to at least isolate and reproduce these two new issues in hope that it will be of some use. Or at the very least if these can be fixed it'll be easier to come with more stable reproducer for the original issue.

---

### 评论 #20 — schung-amd (2026-03-11T21:39:52Z)

Thanks for the update. I have a system that reproduces crashes with the DKMS driver installed after running a heavy ComfyUI workload and interacting with parts of the KDE desktop UI. I suspect the issue here is an incompatibility with KDE/sddm, I don't think we test it with the DKMS driver. Still gathering info on this, and will also look into the other issues you're seeing without the DKMS driver.

e: Nevermind, can repro the DKMS issue with gdm as well. Have a consistent reproducer now at least.

---

### 评论 #21 — Only8Bits (2026-03-12T09:53:16Z)

Great to hear, because to be perfectly honest my system became much more stable now with non-dkms driver. What I also did when I updated my software stack to latest versions is I deleted ~/.triton cache directory. The more I think about it, the more I suspect this was actually what caused this sudden change in how my workflows now behave. This might have been my mistake but I don't remember cleaning Triton cache when I moved between 7.x ROCm versions, last time was when I went from 6.4 to 7. Something to consider perhaps, I do manual software setup but maybe the amdgpu-install script should do that for people just in case.

---

### 评论 #22 — schung-amd (2026-03-12T18:27:02Z)

Glad to hear things have improved on your end. It looks like there are some patches in the 6.18 kernel driver that aren't in the mainline ROCm DKMS driver yet and which should help with these issues. Users on kernel versions 6.17 and higher should avoid installing the DKMS driver until those fixes land. I don't think this is slated to happen for another couple months though, I'll see if we have interest in expediting.

---

### 评论 #23 — Only8Bits (2026-03-17T10:17:36Z)

Just FYI the non-dkms driver is also freezing, but way less often. Let's say less than once a week vs once day (or more) on dkms. It's also quite random and the system log is pretty much what I posted last, that is ring gfx_0.0.0 timeout followed by MES failed to respond to msg=RESET and eventual "recovery" via MODE1 reset. Which requires X to be restarted via SSH because keyboard is not working at this point. So far this freeze has only occurred while compute was running, again it seems any screen refresh (even a text file editor) can cause it - this last time it happened while using VNC and the monitor connected to the machine was in soft-off state.

If it keeps to be rare like that I'm not going to report any more events unless I happen to catch something that might be a clue.

---

### 评论 #24 — schung-amd (2026-03-18T19:34:08Z)

The DKMS issue appears to be resolved in a ROCm version hopefully releasing soon. I would expect stability to also improve in general, but it sounds like things are already ok with the in-kernel driver. Once the next release happens and we verify that this isn't happening we can close this off, I'll leave this open until then.

---

### 评论 #25 — schung-amd (2026-03-25T18:25:30Z)

ROCm 7.2.1 is now out and the DKMS incompatibility should be fixed there from my testing. Please let me know if you encounter this issue again, although the workaround will still be to not install/uninstall the DKMS driver. Closing for now, can reopen if necessary.

---

### 评论 #26 — Only8Bits (2026-05-07T13:33:06Z)

I've updated my ROCm install to 7.2.3 and decided to give the DKMS driver (30.30.3) another try. Sadly it froze the system in the usual way on the first big job I've thrown at it. Log below but it's pretty much same story as before:

> may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.0.1 timeout, signaled seq=583, emitted seq=584
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu:  Process firefox pid 3217 thread firefox:cs0 pid 3378
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: Starting comp_1.0.1 ring reset
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: reset compute queue (1:0:1)
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: Ring comp_1.0.1 reset failed
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset begin!. Source:  1
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: Failed to evict queue 2
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 1 for dev 24677
may 07 12:09:05 x plasmashell[3217]: ATTENTION: default value of option mesa_glthread overridden by environment.
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] *ERROR* Failed to initialize parser -125!
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: MODE1 reset
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU mode1 reset
may 07 12:09:05 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU smu mode1 reset
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset succeeded, trying to resume
may 07 12:09:06 x kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: VRAM is lost due to GPU reset!
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: PSP is resuming...
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: reserve 0x1300000 from 0x84fc000000 for PSP TMR
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: RAP: optional rap ta ucode is not available
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU is resuming...
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8300 (78.131.0)
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU driver if version not matched
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: SMU is resumed successfully!
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002F00
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset(1) succeeded!
may 07 12:09:06 x kernel: amdgpu 0000:0c:00.0: [drm] device wedged, but recovered through reset

So I'm reverting to non-dkms again. Which also has some issues - like randomly reporting page faults that kill my jobs but that's pretty rare, so I guess I'll take that instead...

---
