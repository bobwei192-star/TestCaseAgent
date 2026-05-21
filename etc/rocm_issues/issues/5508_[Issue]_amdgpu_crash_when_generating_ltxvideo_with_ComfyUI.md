# [Issue]: amdgpu crash when generating ltxvideo with ComfyUI

> **Issue #5508**
> **状态**: closed
> **创建时间**: 2025-10-11T23:56:46Z
> **更新时间**: 2025-10-13T19:52:21Z
> **关闭时间**: 2025-10-12T00:32:09Z
> **作者**: TheConanRider
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5508

## 描述

### Problem Description

Every 2-3 generations with ltx-video on ComfyUI the screen will go black and then display a unresponsive instance of the last visible state of the monitor. When in that state nothing will become responsive again requiring the system to be rebooted manually. 

Logs show that amdgpu detects issue and attempts to restart the GPU
```
Oct 12 00:30:25 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:25 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Oct 12 00:30:25 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Oct 12 00:30:25 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to evict queue 1
Oct 12 00:30:25 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to evict queue 0
Oct 12 00:30:25 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset begin!
Oct 12 00:30:25 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to restore queue 2
Oct 12 00:30:25 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to restore process queues
Oct 12 00:30:26 Desktop-Mint NetworkManager[1106]: <warn>  [1760225426.6057] platform-linux: do-add-ip6-address[2: fe80::366d:5b89:363a:c5af]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:26 Desktop-Mint NetworkManager[1106]: <warn>  [1760225426.6058] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00:db31:80e7:885c:521f]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:26 Desktop-Mint NetworkManager[1106]: <warn>  [1760225426.6058] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00::24]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:28 Desktop-Mint NetworkManager[1106]: <warn>  [1760225428.6069] platform-linux: do-add-ip6-address[2: fe80::336e:2cac:5026:dfeb]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:28 Desktop-Mint NetworkManager[1106]: <warn>  [1760225428.6069] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00:db31:80e7:885c:521f]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:28 Desktop-Mint NetworkManager[1106]: <warn>  [1760225428.6069] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00::24]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:29 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: failed to suspend display audio
Oct 12 00:30:29 Desktop-Mint systemd[1]: Started systemd-coredump@1-10011-0.service - Process Core Dump (PID 10011/UID 0).
Oct 12 00:30:29 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:29 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:29 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:29 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:29 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:29 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:30 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:30 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:30 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:30 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:30 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:30 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:30 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:30 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:30 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:30 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:30 Desktop-Mint NetworkManager[1106]: <warn>  [1760225430.6081] platform-linux: do-add-ip6-address[2: fe80::d1ed:c30c:477f:bd7d]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:30 Desktop-Mint NetworkManager[1106]: <warn>  [1760225430.6082] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00:db31:80e7:885c:521f]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:30 Desktop-Mint NetworkManager[1106]: <warn>  [1760225430.6082] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00::24]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:30 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 12 00:30:30 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 12 00:30:30 Desktop-Mint kernel: [drm:gfx_v11_0_cp_gfx_enable.isra.0 [amdgpu]] *ERROR* failed to halt cp gfx
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MODE1 reset
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU mode1 reset
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU smu mode1 reset
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset succeeded, trying to resume
Oct 12 00:30:31 Desktop-Mint kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
Oct 12 00:30:31 Desktop-Mint kernel: [drm] VRAM is lost due to GPU reset!
Oct 12 00:30:31 Desktop-Mint kernel: [drm] PSP is resuming...
Oct 12 00:30:31 Desktop-Mint kernel: [drm] reserve 0x1300000 from 0x85fc000000 for PSP TMR
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: RAP: optional rap ta ucode is not available
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU is resuming...
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x0000003f, smu fw program = 0, smu fw version = 0x004e7900 (78.121.0)
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU driver if version not matched
Oct 12 00:30:31 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU is resumed successfully!
Oct 12 00:30:31 Desktop-Mint kernel: [drm] DMUB hardware initialized: version=0x07002900
Oct 12 00:30:32 Desktop-Mint kernel: [drm] kiq ring mec 3 pipe 1 q 0
Oct 12 00:30:32 Desktop-Mint kernel: [drm] VCN decode and encode initialized successfully(under DPG Mode).
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: recover vram bo from shadow start
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: recover vram bo from shadow done
Oct 12 00:30:32 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset(1) succeeded!
Oct 12 00:30:32 Desktop-Mint NetworkManager[1106]: <warn>  [1760225432.6092] ipv6ll[5c9265eb963b72d5,ifindex=2]: changed: no IPv6 link local address to retry after Duplicate Address Detection failures (back off)
Oct 12 00:30:32 Desktop-Mint NetworkManager[1106]: <warn>  [1760225432.6094] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00:db31:80e7:885c:521f]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:32 Desktop-Mint NetworkManager[1106]: <warn>  [1760225432.6094] platform-linux: do-add-ip6-address[2: 2a0e:1d47:830c:ef00::24]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 12 00:30:32 Desktop-Mint NetworkManager[1106]: <warn>  [1760225432.6095] l3cfg[d5652fc43265268a,ifindex=2]: unable to configure IPv6 route: type unicast fe80::a643:8cff:fe38:71d0/128 dev 2 metric 100 mss 0 rt-src ndisc pref high
```


### Operating System

Linux Mint 22.2 (Zara)

### CPU

AMD Ryzen 7 5700X3D 8-Core Processor

### GPU

AMD Radeon 7900XTX

### ROCm Version

ROCm 6.4

### ROCm Component

_No response_

### Steps to Reproduce

https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/inference/t2v_comfyui_radeon.html

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             NO

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 5700X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5700X3D 8-Core Processor
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
  Max Clock Freq. (MHz):   3000                               
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
      Size:                    32781504(0x1f434c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32781504(0x1f434c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32781504(0x1f434c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32781504(0x1f434c0) KB             
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
  Uuid:                    GPU-d210e43beedf0dd6               
  Marketing Name:          Radeon RX 7900 XTX                 
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
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   10240                              
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      19                                 
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
```



### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — TheConanRider (2025-10-12T00:32:09Z)

I think updating to rocm 7.0.2 may have fixed this issue. 

---
