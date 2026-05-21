# [Issue]: *ERROR* MES failed to response msg=3

> **Issue #3265**
> **状态**: closed
> **创建时间**: 2024-06-07T00:00:53Z
> **更新时间**: 2024-07-23T14:06:59Z
> **关闭时间**: 2024-07-23T14:06:59Z
> **作者**: becky-soda
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3265

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Running Stable Diffusion on Radeon 7900XTX regularly crashes display driver, filling screen with tiling, colored static. System becomes unresponsive; I am unable to recover Wayland/X, and unable to access TTY plain-text terminals. However, I am able to reboot with alt+sysreq+REISUB.

Graphics card works fine for gaming, including during graphically-intensive games (such as Cyberpunk 2077).

An excerpt from one of the '/var/log/messages' is shown below under 'Additional Information'.

I have tried ROCm 6.0.0 from Fedora 40 and ROCm 6.1.0 from Fedora Rawhide. I have tried reinstalling Fedora from known good media twice.

### Operating System

Fedora Linux 40 (KDE Plasma)

### CPU

Intel(R) Core(TM) i7-8086K CPU @ 4.00GHz

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0, ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Start any stable diffusion process (Automatic1111, ComfyUI).
2. Open UI (ie through Firefox, Chromium, etc)
3. Run one or more tasks.
4. Display driver crashes, sometimes on first task, otherwise on second or third. (System recoverable only through hard reboot or 'alt + SysReq + REISUB').

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    Intel(R) Core(TM) i7-8086K CPU @ 4.00GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i7-8086K CPU @ 4.00GHz
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
  Max Clock Freq. (MHz):   5000                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32785016(0x1f44278) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32785016(0x1f44278) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32785016(0x1f44278) KB             
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
  Uuid:                    GPU-4370ae80e03b5ed9               
  Marketing Name:          AMD Radeon RX 7900 XTX             
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
  Max Clock Freq. (MHz):   2304                               
  BDFID:                   768                                
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
  Packet Processor uCode:: 102                                
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

Originally reported here: https://discussion.fedoraproject.org/t/how-to-stop-display-from-crashing-when-using-rocm/118041

/var/log/messages from one crash includes this at time of crash:

```
May 26 18:09:55 fedora kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
May 26 18:09:55 fedora kernel: amdgpu 0000:03:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1006
May 26 18:09:55 fedora kernel: amdgpu 0000:03:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
May 26 18:09:55 fedora kernel: amdgpu 0000:03:00.0: amdgpu: Failed to evict queue 5
May 26 18:09:55 fedora kernel: amdgpu: Failed to evict process queues
May 26 18:09:55 fedora kernel: amdgpu: Failed to quiesce KFD
May 26 18:09:55 fedora kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset begin!
May 26 18:09:55 fedora kwin_wayland[2209]: kwin_scene_opengl: A graphics reset not attributable to the current GL context occurred.
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: IP block:gfx_v11_0 is hung!
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 Faulty UTCL2 client ID: CPC (0x5)
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 MORE_FAULTS: 0x1
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 WALKER_ERROR: 0x1
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 PERMISSION_FAULTS: 0x5
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 MAPPING_ERROR: 0x1
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 RW: 0x1
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 Faulty UTCL2 client ID: CB/DB (0x0)
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 MORE_FAULTS: 0x0
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 WALKER_ERROR: 0x0
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 PERMISSION_FAULTS: 0x0
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 MAPPING_ERROR: 0x0
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: #011 RW: 0x0
May 26 18:09:57 fedora kernel: [drm] kiq ring mec 3 pipe 1 q 0
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: recover vram bo from shadow start
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: recover vram bo from shadow done
May 26 18:09:57 fedora kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset(1) succeeded!
```

…followed by a massive amount of repeating…

```
May 26 18:09:57 fedora kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
May 26 18:09:57 fedora kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
```

...until reboot. Note that it reports that GPU reset succeeded, but Wayland/X will not recover, and TTY plain-text terminals are inaccessible.

---

## 评论 (22 条)

### 评论 #1 — smirgol (2024-06-15T19:03:12Z)

I'm experiencing the same issue I think.
I've recently upgraded from 6.0.2 to 6.1.2 by deinstalling everything first, then doing a `amdgpu-install --usecase=hiplibsdk,rocm,opencl`. I should note that I fiddled with the 6.0.2 installation, as it was problematic at first too, so it wasn't a full default installation - just to say that the issue might have been present in a default installation of 6.0.2 too, I don't know for sure.

Now, when trying to create an image in automatic1111, it will always hard crash the gpu driver forcing me to do a full reboot.

This is the log from dmesg:
```
[  484.427794] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 5559 thread python3 pid 5559)
[  484.427810] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x00007eec4cc00000 from client 10
[  484.427816] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  484.427821] amdgpu 0000:0e:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  484.427825] amdgpu 0000:0e:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  484.427829] amdgpu 0000:0e:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  484.427833] amdgpu 0000:0e:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  484.427837] amdgpu 0000:0e:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  484.427841] amdgpu 0000:0e:00.0: amdgpu: 	 RW: 0x0
[  484.427851] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 5559 thread python3 pid 5559)
[  484.427859] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x00007eec4cc00000 from client 10
[  484.427864] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  484.427868] amdgpu 0000:0e:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[  484.427873] amdgpu 0000:0e:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  484.427877] amdgpu 0000:0e:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  484.427881] amdgpu 0000:0e:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[  484.427885] amdgpu 0000:0e:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  484.427889] amdgpu 0000:0e:00.0: amdgpu: 	 RW: 0x0
[  484.427899] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 5559 thread python3 pid 5559)
[  484.427906] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x00007eec4cc00000 from client 10
[  484.427911] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  484.427915] amdgpu 0000:0e:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[  484.427920] amdgpu 0000:0e:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  484.427924] amdgpu 0000:0e:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  484.427928] amdgpu 0000:0e:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[  484.427932] amdgpu 0000:0e:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  484.427936] amdgpu 0000:0e:00.0: amdgpu: 	 RW: 0x0
[  484.427945] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 5559 thread python3 pid 5559)
[  484.427952] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x00007eec4cc00000 from client 10
[  484.427957] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  484.427961] amdgpu 0000:0e:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[  484.427965] amdgpu 0000:0e:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  484.427969] amdgpu 0000:0e:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  484.427973] amdgpu 0000:0e:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[  484.427977] amdgpu 0000:0e:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  484.427981] amdgpu 0000:0e:00.0: amdgpu: 	 RW: 0x0
[  484.427991] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 5559 thread python3 pid 5559)
[  484.427998] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x00007eec4cc00000 from client 10
[  484.428002] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  484.428007] amdgpu 0000:0e:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[  484.428011] amdgpu 0000:0e:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  484.428015] amdgpu 0000:0e:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  484.428019] amdgpu 0000:0e:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[  484.428023] amdgpu 0000:0e:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  484.428027] amdgpu 0000:0e:00.0: amdgpu: 	 RW: 0x0
[  484.428038] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 5559 thread python3 pid 5559)
[  484.428044] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x00007eec4cc00000 from client 10
[  484.428049] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  484.428053] amdgpu 0000:0e:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[  484.428057] amdgpu 0000:0e:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  484.428061] amdgpu 0000:0e:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  484.428066] amdgpu 0000:0e:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[  484.428070] amdgpu 0000:0e:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  484.428074] amdgpu 0000:0e:00.0: amdgpu: 	 RW: 0x0
[  488.504148] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[  488.504658] amdgpu 0000:0e:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[  488.504666] amdgpu 0000:0e:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  488.504672] amdgpu 0000:0e:00.0: amdgpu: Failed to evict queue 1
[  488.504742] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504754] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504765] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504770] amdgpu 0000:0e:00.0: amdgpu: GPU reset begin!
[  488.504773] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504781] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504792] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504802] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504812] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504823] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  488.504832] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  490.264897] amdgpu 0000:0e:00.0: amdgpu: Failed to remove queue 0
[  492.835891] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[  492.836398] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[  493.076120] [drm:gfx_v11_0_cp_gfx_enable.isra.0 [amdgpu]] *ERROR* failed to halt cp gfx
[  493.124493] amdgpu 0000:0e:00.0: amdgpu: MODE1 reset
[  493.124498] amdgpu 0000:0e:00.0: amdgpu: GPU mode1 reset
[  493.124571] amdgpu 0000:0e:00.0: amdgpu: GPU smu mode1 reset
[  493.652327] amdgpu 0000:0e:00.0: amdgpu: GPU reset succeeded, trying to resume
[  493.652579] [drm] PCIE GART of 512M enabled (table at 0x00000085FEB00000).
[  493.652686] [drm] VRAM is lost due to GPU reset!
[  493.652689] amdgpu 0000:0e:00.0: amdgpu: PSP is resuming...
[  493.722550] amdgpu 0000:0e:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[  493.864828] amdgpu 0000:0e:00.0: amdgpu: RAP: optional rap ta ucode is not available
[  493.864832] amdgpu 0000:0e:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  493.864835] amdgpu 0000:0e:00.0: amdgpu: SMU is resuming...
[  493.864839] amdgpu 0000:0e:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7e00 (78.126.0)
[  493.864843] amdgpu 0000:0e:00.0: amdgpu: SMU driver if version not matched
[  493.941509] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[  493.941803] [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
[  494.022013] amdgpu 0000:0e:00.0: amdgpu: SMU is resumed successfully!
[  494.024047] [drm] DMUB hardware initialized: version=0x07002600
[  494.269392] [drm] kiq ring mec 3 pipe 1 q 0
[  494.275518] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  494.276841] amdgpu 0000:0e:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[  494.277481] amdgpu 0000:0e:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  494.277485] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  494.277489] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  494.277493] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  494.277497] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  494.277500] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  494.277504] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  494.277507] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  494.277511] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  494.277515] amdgpu 0000:0e:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  494.277519] amdgpu 0000:0e:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  494.277522] amdgpu 0000:0e:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  494.277526] amdgpu 0000:0e:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[  494.277530] amdgpu 0000:0e:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[  494.277534] amdgpu 0000:0e:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[  494.280769] amdgpu 0000:0e:00.0: amdgpu: recover vram bo from shadow start
[  494.282558] amdgpu 0000:0e:00.0: amdgpu: recover vram bo from shadow done
[  494.282582] amdgpu 0000:0e:00.0: amdgpu: GPU reset(1) succeeded!
```

My specs:
---
OS: Ubuntu 22.04.4 LTS
Kernel: 6.5.0-35-generic
CPU: AMD Ryzen 9 3900X (24) @ 3.800GHz
GPU: 7900 XTX
DE: Xfce 4.16
WM: Xfwm4


---

### 评论 #2 — briansp2020 (2024-06-15T20:05:56Z)

@smirgol 
What speed ram are you using? I've had a lot of mysterious issues which turned out to me unstable memory. If you are using EXPO setting, try running your memory at the default speed and see if that improves the situation


---

### 评论 #3 — smirgol (2024-06-15T21:08:43Z)

@briansp2020 That was actually the first thing I've tried. Didn't improve the situation, unfortunately. The log is with default RAM settings, no overclocking profile active.

---

### 评论 #4 — briansp2020 (2024-06-15T23:58:02Z)

I've had similar issues in the past but it went away the last time I tried it. Also, I think Kernel version 5.15 worked better for me compared to 6.5. I have a separate machine I used for testing ROCm and it worked better when I install Ubuntu 22.04 server compared to the desktop edition and the main difference I noticed is the kernel they install by default.

---

### 评论 #5 — madness742 (2024-06-16T03:00:08Z)

@smirgol, if you have a spare gpu (integrated or dedicated) then you can try the workaround that I've described in #3166. Hopefully this problem gets fixed soon as having a 1440p and 4k monitor running off my iGPU results in sluggish KDE animations..

---

### 评论 #6 — smirgol (2024-06-16T10:15:40Z)

I've uninstalled everything and this time installed only a few selected packages by hand:
```
sudo apt install rocminfo rocblas hipblas hipblas-dev
``` 

With that, I can run LLMs using `koboldcpp-rocm` and hipBLAS (admittedly I didn't try that with my previous full installation, so it might have worked beforehand, too).
When trying to run image stuff using automatic1111 it will still crash, though. :-/

---

### 评论 #7 — smirgol (2024-06-16T13:10:55Z)

I finally again reached the point where it somewhat works again. This is what I did (in addition to my post above):

1. Update torch for automatic1111 venv to rocm6.1:
```
cd /path/to/my/automatic1111
source venv/bin/activate
pip install --force-reinstall --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1/
deactivate
```

2. Run automatic1111
`TORCH_BLAS_PREFER_HIPBLASLT=0 ./webui.sh`

Note that you **need** to start it with the env `TORCH_BLAS_PREFER_HIPBLASLT=0`
See here: https://github.com/comfyanonymous/ComfyUI/issues/3698#issuecomment-2166000180

---

If it crashes with `Memory access fault by GPU node-1 (Agent handle: 0x194c680) on address 0x761647200000. Reason: Page not present or supervisor privilege.`, do a full reboot, restart automatic1111 and switch the checkpoint once. That seemed to have fixed it for someone *shrugs*
See here: https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/8139

FWIW: my full cmd to start automatic1111 is like this:
`TORCH_BLAS_PREFER_HIPBLASLT=0 PYTORCH_HIP_ALLOC_CONF=max_split_size_mb:128 ./webui.sh --opt-split-attention --no-half-vae`

---

### 评论 #8 — amardhruva (2024-06-17T07:02:45Z)

> I finally again reached the point where it somewhat works again. This is what I did (in addition to my post above):
> 
>     1. Update torch for automatic1111 venv to rocm6.1:
> 
> 
> ```
> cd /path/to/my/automatic1111
> source venv/bin/activate
> pip install --force-reinstall --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1/
> deactivate
> ```
> 
>     2. Run automatic1111
>        `TORCH_BLAS_PREFER_HIPBLASLT=0 ./webui.sh`
> 
> 
> Note that you **need** to start it with the env `TORCH_BLAS_PREFER_HIPBLASLT=0` See here: [comfyanonymous/ComfyUI#3698 (comment)](https://github.com/comfyanonymous/ComfyUI/issues/3698#issuecomment-2166000180)
> 
> If it crashes with `Memory access fault by GPU node-1 (Agent handle: 0x194c680) on address 0x761647200000. Reason: Page not present or supervisor privilege.`, do a full reboot, restart automatic1111 and switch the checkpoint once. That seemed to have fixed it for someone _shrugs_ See here: [AUTOMATIC1111/stable-diffusion-webui#8139](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/8139)
> 
> FWIW: my full cmd to start automatic1111 is like this: `TORCH_BLAS_PREFER_HIPBLASLT=0 PYTORCH_HIP_ALLOC_CONF=max_split_size_mb:128 ./webui.sh --opt-split-attention --no-half-vae`

This Workaround works!!! Thanks!!!

---

### 评论 #9 — becky-soda (2024-06-17T07:23:41Z)

> I finally again reached the point where it somewhat works again. This is what I did (in addition to my post above):
> 
>     1. Update torch for automatic1111 venv to rocm6.1:
> 
> 
> ```
> cd /path/to/my/automatic1111
> source venv/bin/activate
> pip install --force-reinstall --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1/
> deactivate
> ```
> 
>     2. Run automatic1111
>        `TORCH_BLAS_PREFER_HIPBLASLT=0 ./webui.sh`
> 
> 
> Note that you **need** to start it with the env `TORCH_BLAS_PREFER_HIPBLASLT=0` See here: [comfyanonymous/ComfyUI#3698 (comment)](https://github.com/comfyanonymous/ComfyUI/issues/3698#issuecomment-2166000180)
> 
> If it crashes with `Memory access fault by GPU node-1 (Agent handle: 0x194c680) on address 0x761647200000. Reason: Page not present or supervisor privilege.`, do a full reboot, restart automatic1111 and switch the checkpoint once. That seemed to have fixed it for someone _shrugs_ See here: [AUTOMATIC1111/stable-diffusion-webui#8139](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/8139)
> 
> FWIW: my full cmd to start automatic1111 is like this: `TORCH_BLAS_PREFER_HIPBLASLT=0 PYTORCH_HIP_ALLOC_CONF=max_split_size_mb:128 ./webui.sh --opt-split-attention --no-half-vae`

Thanks for the suggestion. I can't get this to work though, I'm sorry to say. I'm still getting:

```
Jun 17 00:36:17 fedora kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Jun 17 00:36:17 fedora kernel: amdgpu 0000:03:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Jun 17 00:36:17 fedora kernel: amdgpu 0000:03:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Jun 17 00:36:17 fedora kernel: amdgpu 0000:03:00.0: amdgpu: Failed to evict queue 1
Jun 17 00:36:17 fedora kernel: amdgpu: Failed to evict process queues
Jun 17 00:36:17 fedora kernel: amdgpu: Failed to evict queues of pasid 0x8048
Jun 17 00:36:17 fedora kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset begin!
```

I tested with Automatic1111. I tried both `TORCH_BLAS_PREFER_HIPBLASLT=0 ./webui.sh` and `TORCH_BLAS_PREFER_HIPBLASLT=0 PYTORCH_HIP_ALLOC_CONF=max_split_size_mb:128 ./webui.sh --opt-split-attention --no-half-vae` to launch, but they both crash my display with the above 'MES failed to response msg=3' message in /var/log/messages.

Thanks for the information, though. I'll work on trying to fix it. I'll report back if I discover anything new.

(Edit: corrected formatting)

---

### 评论 #10 — AngryLoki (2024-06-26T03:32:58Z)

> do a full reboot

IIRC, geohot encountered similar issues many time and recovered without reboot with `sudo rmmod amdgpu && sudo modprobe amdgpu`

Before ROCm 6.0.3 release there was a bug (https://twitter.com/__tinygrad__/status/1770196937142313245) with MES queue corruption. It was told that such issues are fixable only on driver or firmware level (at this point it does not matter which version of ROCm libraries are in your venv). Make sure that your linux-firmware/amd-gpu-firmware are the latest one (ideally to eliminate potential issues with the latest kernel). Also check GPU temperature, my previous GPU reached >100°C when fully loaded, then went defunct until reboot. It was not an issue of driver, it was just heat.

---

### 评论 #11 — matoro (2024-06-26T22:21:53Z)

I also see this on my 7900XTX, but only with larger models chewing most of the VRAM.  Ubuntu 22.04 container, Gentoo kernel 6.9, rocm version `6.1.2.60102-119~20.04`, pytorch version `2.5.0.dev20240625+rocm6.1`.

However, I was able to successfully recover without a reboot by simply ssh-ing in and killing my X server.  Using Xorg only, no wayland.

---

### 评论 #12 — enesaltinkaya (2024-07-02T01:40:22Z)

I've been using nvidia for over 20 years. I wanted to give amd a shot and bought a 7900xtx, arrived today.
Having the same issue as you guys. 
ComfyUi never crashed but Automatic1111 and variants crash the gpu while generating images.

Searching for "*ERROR* MES failed to response" on google shows open issues from last year.

Should i return and get an nvidia instead?

Edit:
I noticed some people suggesting using **amdgpu.mcbp=0** boot flag.
After booting with this flag I've been running _a1111 sd-forge_  for about 20mins non-stop.
Looking good.

---

### 评论 #13 — matoro (2024-07-02T04:19:00Z)

> Edit: I noticed some people suggesting using **amdgpu.mcbp=0** boot flag. After booting with this flag I've been running _a1111 sd-forge_ for about 20mins non-stop. Looking good.

I just tested this and it did not help.

```
$ cat /sys/module/amdgpu/parameters/mcbp
0
$ dmesg -T | grep -i "MES failed to response"
[Tue Jul  2 00:15:21 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:22 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=14
[Tue Jul  2 00:15:22 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:22 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:22 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:22 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:22 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:22 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:23 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:23 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul  2 00:15:23 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
```

---

### 评论 #14 — enesaltinkaya (2024-07-02T11:36:09Z)

> > Edit: I noticed some people suggesting using **amdgpu.mcbp=0** boot flag. After booting with this flag I've been running _a1111 sd-forge_ for about 20mins non-stop. Looking good.
> 
> I just tested this and it did not help.

Yup it crashed for me as well, i was hoping that was it :/



---

### 评论 #15 — becky-soda (2024-07-06T13:02:26Z)

I updated to the latest Fedora 40 a few days ago, and using these in conjunction with the Fedora 41 ROCm *seems* to have solved the issue for me, at least. I think @AngryLoki was right, at least in my case.

I don't know what the etiquette is in these cases, but because the issue is still affecting others I'll just leave this as a comment, and I won't touch any of the close buttons.

---

### 评论 #16 — enesaltinkaya (2024-07-15T13:19:19Z)

I'm quite sure this is related to bad power management.

I'm running arch linux with sapphire pulse 7900xtx.
I was having crashes during gaming as well.
I found a bug report on amd driver gitlab page. https://gitlab.freedesktop.org/drm/amd/-/issues/3131
They suggested manually tweaking power levels, clocks etc..

So I tried _CoreCtrl_ and _lact_ applications to do those tweaks.
But they don't work accurately because of another driver bug, that is;
when you adjust fan curve and apply, clock settings reset,
when you adjust clock settings, fun curve settings reset, it's a mess.

Turns out if you make a small script and run it after boot and suspend, everything works fine.
I've played many hours of games since and generated lots of images using ComfyUi and Fooocus without a problem.
Here is a video of stable diffusion running; https://www.youtube.com/watch?v=UrAINplUKKQ
(In the video I'm using lact only for monitoring, it's service is not running)

Here is my amdpower.sh script and systemd service file to run it after boot and suspend.
You might want to try it without adjusting voltage offset first. I found that -50mv is stable for my card.

``` bash
#!/bin/bash
gpu=card1
device=/sys/class/drm/${gpu}/device
fan=/sys/class/drm/${gpu}/device/gpu_od/fan_ctrl

#reset gpu settings
echo "r" > $fan/fan_target_temperature
echo "r" > $fan/acoustic_target_rpm_threshold
echo "r" > $fan/acoustic_limit_rpm_threshold
echo "r" > $fan/fan_minimum_pwm

beep
sleep 1

#set gpu fan curve
echo "0 60 30" > $fan/fan_curve
echo "1 65 40" > $fan/fan_curve
echo "2 70 50" > $fan/fan_curve
echo "3 80 90" > $fan/fan_curve
echo "4 90 100" > $fan/fan_curve

#set gpu max clock to 2525mhz and voltage offset to -50mv (for sapphire pulse 7900xtx)
echo "s 1 2525" > $device/pp_od_clk_voltage
echo "vo -50" > $device/pp_od_clk_voltage

#set gpu max power to 370watts (for sapphire pulse 7900xtx)
echo "370000000" > $device/hwmon/*/power1_cap

#commit gpu settings
echo "c" > $device/pp_od_clk_voltage
echo "c" > $fan/fan_curve

```

```
[Unit]
Description=amd power system
After=suspend.target multi-user.target

[Service]
ExecStart=/bin/bash /home/enes/tools/scripts/amdpower.sh

[Install]
WantedBy=suspend.target multi-user.target
```

---

### 评论 #17 — matoro (2024-07-15T15:03:19Z)

> I'm quite sure this is related to bad power management.
> 
> I'm running arch linux with sapphire pulse 7900xtx. I was having crashes during gaming as well. I found a bug report on amd driver gitlab page. https://gitlab.freedesktop.org/drm/amd/-/issues/3131 They suggested manually tweaking power levels, clocks etc..
> 
> So I tried _CoreCtrl_ and _lact_ applications to do those tweaks. But they don't work accurately because of another driver bug, that is; when you adjust fan curve and apply, clock settings reset, when you adjust clock settings, fun curve settings reset, it's a mess.
> 
> Turns out if you make a small script and run it after boot and suspend, everything works fine. I've played many hours of games since and generated lots of images using ComfyUi and Fooocus without a problem. Here is a video of stable diffusion running; https://www.youtube.com/watch?v=UrAINplUKKQ (In the video I'm using lact only for monitoring, it's service is not running)
> 
> Here is my amdpower.sh script and systemd service file to run it after boot and suspend. You might want to try it without adjusting voltage offset first. I found that -50mv is stable for my card.

Unfortunately I just tried this and still got the same error.  When I get this error, the fans don't spin up or anything, the display just crashes to a black screen, and SD displays this error:

```
Memory access fault by GPU node-1 (Agent handle: 0x559925543180) on address 0x7f5f35c00000. Reason: Page not present or supervisor privilege.s]
./webui.sh: line 304:   164 Aborted                 "${python_cmd}" -u "${LAUNCH_SCRIPT}" "$@"
```

---

### 评论 #18 — enesaltinkaya (2024-07-15T15:15:02Z)

One thing i failed to mention, i used this command to install pytorch inside _venv_;
```pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1```
then
```pip install -r comfyui/requirements.txt```

I also made sure lact service is disabled, and corectrl is not running. I think corectrl and/or lact service periodically commits those gpu settings and it messes things.


---

### 评论 #19 — matoro (2024-07-15T15:17:17Z)

> One thing i failed to mention, i used this command to install pytorch inside _venv_; `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1` then `pip install -r comfyui/requirements.txt`
> 
> I also made sure lact service is disabled, and corectrl is not running. I think corectrl and/or lact service periodically commits those gpu settings and it messes things.

Yes, I am also using nightly pytorch against ROCm 6.1, that's necessary or else nothing even loads.  Not running corectrl or lact service, don't even have either of those installed.

---

### 评论 #20 — harkgill-amd (2024-07-19T19:37:38Z)

Hi @becky-soda, an internal ticket has been created to further investigate this issue.

---

### 评论 #21 — schung-amd (2024-07-22T13:30:23Z)

Hi all, there appears to be a cluster of similar issues affecting 7900XTX users. We're investigating these reports on a case-by-case basis, but due to the differences in configuration in affected systems there may not be a blanket solution. If you are currently experiencing this issue, please provide as much detail as you can regarding your hardware and your installation of Stable Diffusion (and dependencies).

Have you run into any further issues after upgrading ROCm @becky-soda?

---

### 评论 #22 — schung-amd (2024-07-23T14:06:59Z)

I was able to reproduce consistent crashes in Stable Diffusion with a 7900XTX on Ubuntu 22.04. To reproduce, I followed the installation steps at https://are-we-gfx1100-yet.github.io/post/a1111-webui/ but with ROCm 6.1.3 and corresponding torch packages found at https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/. The output in /var/log/syslog shows the same "MES failed to response msg=3" signature that several of these reports display.

The solution on my end was to use Stable Diffusion with the --no-half-vae flag, which disables use of the fp16 datatype in the variational autoencoder. This will slightly increase the VRAM usage. In addition, I set the environment variables HSA_OVERRIDE_GFX_VERSION=11.0.0, PYTORCH_ROCM_ARCH=gfx1100, HIP_VISIBLE_DEVICES=0, and PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512, and invoked with --opt-sdp-attention.

However, @becky-soda and @smirgol report using --no-half-vae and still encountering issues, so there must be other causes as well. The workaround I used is likely specific to the versions of ROCm and torch used to reproduce the issue. https://github.com/ROCm/ROCm/issues/3166#issuecomment-2197123313 and https://github.com/ROCm/ROCm/issues/2935#issuecomment-2182980971 have working configurations for Stable Diffusion; for those still affected by this or similar issues, you can try reinstalling using those steps.

I will be closing this for now as the original poster appears to have resolved their issue, but feel free to reopen @becky-soda if you still encounter this issue. If you are still experiencing this issue @matoro, @enesaltinkaya, @smirgol, @amardhruva, please open separate tickets for them with as much information as possible so we can investigate your issues more closely, as there are a lot of moving parts here. 

---
