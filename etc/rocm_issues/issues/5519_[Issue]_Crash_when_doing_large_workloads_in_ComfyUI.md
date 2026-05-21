# [Issue]: Crash when doing large workloads in ComfyUI

> **Issue #5519**
> **状态**: closed
> **创建时间**: 2025-10-15T11:20:13Z
> **更新时间**: 2025-10-28T12:33:28Z
> **关闭时间**: 2025-10-28T12:33:28Z
> **作者**: TheConanRider
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5519

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

AMDGPU crashes with large work loads. I was originally noticing this with torch 2.9.0+rocm7.0 and reverted back to torch 2.8.0+rocm6.4 and had no issues but since upgrading back to 2.9.0+rocm6.4 the issue has returned. 


 

### Operating System

OS: NAME="Linux Mint" VERSION="22.2 (Zara)"

### CPU

 CPU:  model name	: AMD Ryzen 7 5700X3D 8-Core Processor 

### GPU

GPU:   
    Name:                    AMD Ryzen 7 5700X3D 8-Core Processor
    Marketing Name:          AMD Ryzen 7 5700X3D 8-Core Processor
    Name:                    gfx1100                               
    Marketing Name:          Radeon RX 7900 XTX                        
    Name:                    amdgcn-amd-amdhsa--gfx1100               
    Name:                    amdgcn-amd-amdhsa--gfx11-generic

### ROCm Version

ROCM 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

Originally it was reproduced by https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/inference/t2v_comfyui_radeon.html

but after I switched to https://civitai.com/models/1802623/wan-21-lightspeed the issue was visible again.

I am running ComfyUI with --reserve-vram 4 which seemed to help with the issue

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
*** Done ***  

### Additional Information

```
Oct 15 12:05:54 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:54 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Oct 15 12:05:54 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Oct 15 12:05:54 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to evict queue 1
Oct 15 12:05:54 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to evict queue 0
Oct 15 12:05:54 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset begin!
Oct 15 12:05:54 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to restore queue 2
Oct 15 12:05:54 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to restore process queues
Oct 15 12:05:54 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct 15 12:05:54 Desktop-Mint kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct 15 12:05:55 Desktop-Mint NetworkManager[1025]: <warn>  [1760526355.8167] platform-linux: do-add-ip6-address[2: fe80::366d:5b89:363a:c5af]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 15 12:05:57 Desktop-Mint NetworkManager[1025]: <warn>  [1760526357.8169] platform-linux: do-add-ip6-address[2: fe80::336e:2cac:5026:dfeb]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 15 12:05:58 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: failed to suspend display audio
Oct 15 12:05:58 Desktop-Mint systemd[1]: Created slice system-systemd\x2dcoredump.slice - Slice /system/systemd-coredump.
Oct 15 12:05:58 Desktop-Mint systemd[1]: Started systemd-coredump@0-10872-0.service - Process Core Dump (PID 10872/UID 0).
Oct 15 12:05:59 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:59 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 15 12:05:59 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:59 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 15 12:05:59 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:59 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 15 12:05:59 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:59 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 15 12:05:59 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:59 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 15 12:05:59 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:59 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 15 12:05:59 Desktop-Mint NetworkManager[1025]: <warn>  [1760526359.8172] platform-linux: do-add-ip6-address[2: fe80::d1ed:c30c:477f:bd7d]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 15 12:05:59 Desktop-Mint kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct 15 12:05:59 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 15 12:05:59 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MODE1 reset
Oct 15 12:05:59 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU mode1 reset
Oct 15 12:05:59 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU smu mode1 reset
Oct 15 12:06:00 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset succeeded, trying to resume
Oct 15 12:06:00 Desktop-Mint kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
Oct 15 12:06:00 Desktop-Mint kernel: [drm] VRAM is lost due to GPU reset!
Oct 15 12:06:00 Desktop-Mint kernel: [drm] PSP is resuming...
Oct 15 12:06:00 Desktop-Mint kernel: [drm] reserve 0x1300000 from 0x85fc000000 for PSP TMR
Oct 15 12:06:00 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: RAP: optional rap ta ucode is not available
Oct 15 12:06:00 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Oct 15 12:06:00 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU is resuming...
Oct 15 12:06:00 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x0000003f, smu fw program = 0, smu fw version = 0x004e7900 (78.121.0)
Oct 15 12:06:00 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU driver if version not matched
Oct 15 12:06:00 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU is resumed successfully!
Oct 15 12:06:00 Desktop-Mint kernel: [drm] DMUB hardware initialized: version=0x07002900
Oct 15 12:06:01 Desktop-Mint kernel: [drm] kiq ring mec 3 pipe 1 q 0
Oct 15 12:06:01 Desktop-Mint kernel: [drm] VCN decode and encode initialized successfully(under DPG Mode).
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: recover vram bo from shadow start
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: recover vram bo from shadow done
Oct 15 12:06:01 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset(1) succeeded!
Oct 15 12:06:01 Desktop-Mint kernel: show_signal_msg: 115 callbacks suppressed
Oct 15 12:06:01 Desktop-Mint kernel: browser 4 :cs0[4002]: segfault at 0 ip 00005a8655d2ee31 sp 000076b83a3fea30 error 6 in firefox-bin[5a8655ccd000+98000] likely on CPU 7 (core 7, socket 0)
Oct 15 12:06:01 Desktop-Mint kernel: Code: 4c 8b 35 0a 7c 03 00 49 8b 36 e8 fa 50 03 00 49 8b 36 bf 0a 00 00 00 e8 0d 52 03 00 48 89 1d 96 b7 03 00 31 c0 b9 23 00 00 00 <48> 89 08 e8 e7 84 fb ff cc cc cc cc cc cc cc 48 83 ec 38 0f 28 05
Oct 15 12:06:01 Desktop-Mint systemd[1]: Started systemd-coredump@1-10881-0.service - Process Core Dump (PID 10881/UID 0).
Oct 15 12:06:01 Desktop-Mint NetworkManager[1025]: <warn>  [1760526361.8173] ipv6ll[bafc422a1561043a,ifindex=2]: changed: no IPv6 link local address to retry after Duplicate Address Detection failures (back off)
Oct 15 12:06:03 Desktop-Mint systemd-coredump[10882]: [🡕] Process 3233 (RDD Process) of user 1000 dumped core.
                                                      
                                                      Module libgomp.so.1 from deb gcc-14-14.2.0-4ubuntu2~24.04.amd64
                                                      Module libzstd.so.1 from deb libzstd-1.5.5+dfsg2-2build1.1.amd64
                                                      Module libsystemd.so.0 from deb systemd-255.4-1ubuntu8.11.amd64
                                                      Module libgcc_s.so.1 from deb gcc-14-14.2.0-4ubuntu2~24.04.amd64
                                                      Module libstdc++.so.6 from deb gcc-14-14.2.0-4ubuntu2~24.04.amd64
                                                      Stack trace of thread 4002:
                                                      #0  0x00005a8655d2ee31 mozalloc_abort (firefox-bin + 0x86e31)
                                                      #1  0x00005a8655ce732d abort (firefox-bin + 0x3f32d)
                                                      #2  0x000076b843844270 n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0xa44270)
                                                      #3  0x000076b843849246 n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0xa49246)
                                                      #4  0x000076b843360621 n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x560621)
                                                      #5  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #6  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #7  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #8  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 3233:
                                                      #0  0x000076b86331b4fd __GI___poll (libc.so.6 + 0x11b4fd)
                                                      #1  0x000076b85dee001b n/a (libxul.so + 0x7ce001b)
                                                      #2  0x000076b86187868e n/a (libglib-2.0.so.0 + 0xbc68e)
                                                      #3  0x000076b861818a63 g_main_context_iteration (libglib-2.0.so.0 + 0x5ca63)
                                                      #4  0x000076b859b4e8cb n/a (libxul.so + 0x394e8cb)
                                                      #5  0x000076b859b4cee3 n/a (libxul.so + 0x394cee3)
                                                      #6  0x000076b85b2743da n/a (libxul.so + 0x50743da)
                                                      #7  0x000076b85b2741ea n/a (libxul.so + 0x50741ea)
                                                      #8  0x000076b85b27410d n/a (libxul.so + 0x507410d)
                                                      #9  0x000076b85aff031a n/a (libxul.so + 0x4df031a)
                                                      #10 0x00005a8655d22869 n/a (firefox-bin + 0x7a869)
                                                      #11 0x000076b86322a1ca __libc_start_call_main (libc.so.6 + 0x2a1ca)
                                                      #12 0x000076b86322a28b __libc_start_main_impl (libc.so.6 + 0x2a28b)
                                                      #13 0x00005a8655d26e22 _start (firefox-bin + 0x7ee22)
                                                      
                                                      Stack trace of thread 3236:
                                                      #0  0x000076b86331baca __GI___libc_read (libc.so.6 + 0x11baca)
                                                      #1  0x000076b85acf5cda n/a (libxul.so + 0x4af5cda)
                                                      #2  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #3  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #4  0x000076b863329c6c __clone3 (libc.so.6 + 0x129c6c)
                                                      
                                                      Stack trace of thread 3238:
                                                      #0  0x000076b86332728d syscall (libc.so.6 + 0x12728d)
                                                      #1  0x000076b85a15b314 n/a (libxul.so + 0x3f5b314)
                                                      #2  0x000076b85a159e52 n/a (libxul.so + 0x3f59e52)
                                                      #3  0x000076b85acf634c n/a (libxul.so + 0x4af634c)
                                                      #4  0x000076b85acf6187 n/a (libxul.so + 0x4af6187)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329c6c __clone3 (libc.so.6 + 0x129c6c)
                                                      
                                                      Stack trace of thread 4003:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 3264:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x00005a8655d58d46 _ZN7mozilla6detail21ConditionVariableImpl4waitERNS0_9MutexImplE (firefox-bin + 0xb0d46)
                                                      #3  0x000076b859b4f33d n/a (libxul.so + 0x394f33d)
                                                      #4  0x000076b859b4e0f3 n/a (libxul.so + 0x394e0f3)
                                                      #5  0x000076b85acf97ce n/a (libxul.so + 0x4af97ce)
                                                      #6  0x000076b8638f270f n/a (libnspr4.so + 0x1e70f)
                                                      #7  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #8  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #9  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4021:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 3624:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x00005a8655d58efa _ZN7mozilla6detail21ConditionVariableImpl8wait_forERNS0_9MutexImplERKNS_16BaseTimeDurationINS_27TimeDurationValueCalculatorEEE (firefox-bin + 0xb0efa)
                                                      #3  0x000076b85a504c6f n/a (libxul.so + 0x4304c6f)
                                                      #4  0x000076b859b4fe1d n/a (libxul.so + 0x394fe1d)
                                                      #5  0x000076b859b4e012 n/a (libxul.so + 0x394e012)
                                                      #6  0x000076b85acf97ce n/a (libxul.so + 0x4af97ce)
                                                      #7  0x000076b8638f270f n/a (libnspr4.so + 0x1e70f)
                                                      #8  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #9  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #10 0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4004:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4007:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4006:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4020:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4022:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4023:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4024:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4005:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 10852:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329bc8e __pthread_cond_wait_common (libc.so.6 + 0x9bc8e)
                                                      #2  0x00005a8655d58e7f _ZN7mozilla6detail21ConditionVariableImpl8wait_forERNS0_9MutexImplERKNS_16BaseTimeDurationINS_27TimeDurationValueCalculatorEEE (firefox-bin + 0xb0e7f)
                                                      #3  0x000076b859c46b9d n/a (libxul.so + 0x3a46b9d)
                                                      #4  0x000076b859b4fe1d n/a (libxul.so + 0x394fe1d)
                                                      #5  0x000076b859b4e012 n/a (libxul.so + 0x394e012)
                                                      #6  0x000076b85acf97ce n/a (libxul.so + 0x4af97ce)
                                                      #7  0x000076b8638f270f n/a (libnspr4.so + 0x1e70f)
                                                      #8  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #9  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #10 0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 7042:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 10856:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4025:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 10859:
                                                      #0  0x000076b86332728d syscall (libc.so.6 + 0x12728d)
                                                      #1  0x000076b8433530ca n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5530ca)
                                                      #2  0x000076b8433601bf n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5601bf)
                                                      #3  0x000076b843846d31 n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0xa46d31)
                                                      #4  0x000076b8437ee432 n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x9ee432)
                                                      #5  0x000076b842eff3b3 n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0xff3b3)
                                                      #6  0x000076b84cfd7764 vaEndPicture (libva.so.2 + 0x7764)
                                                      #7  0x000076b84f8021fc n/a (libavcodec.so.60 + 0x8021fc)
                                                      #8  0x000076b84f811617 n/a (libavcodec.so.60 + 0x811617)
                                                      #9  0x000076b84f3c1a47 n/a (libavcodec.so.60 + 0x3c1a47)
                                                      #10 0x000076b84f3d5631 n/a (libavcodec.so.60 + 0x3d5631)
                                                      #11 0x000076b84f2a9a45 n/a (libavcodec.so.60 + 0x2a9a45)
                                                      #12 0x000076b84f2aa044 avcodec_send_packet (libavcodec.so.60 + 0x2aa044)
                                                      #13 0x000076b85d601c4b n/a (libxul.so + 0x7401c4b)
                                                      #14 0x000076b85d5be5a6 n/a (libxul.so + 0x73be5a6)
                                                      #15 0x000076b85d5f95a4 n/a (libxul.so + 0x73f95a4)
                                                      #16 0x000076b85d572bbb n/a (libxul.so + 0x7372bbb)
                                                      #17 0x000076b859c47b96 n/a (libxul.so + 0x3a47b96)
                                                      #18 0x000076b859c46d5f n/a (libxul.so + 0x3a46d5f)
                                                      #19 0x000076b859b4fe1d n/a (libxul.so + 0x394fe1d)
                                                      #20 0x000076b859b4e012 n/a (libxul.so + 0x394e012)
                                                      #21 0x000076b85acf97ce n/a (libxul.so + 0x4af97ce)
                                                      #22 0x000076b8638f270f n/a (libnspr4.so + 0x1e70f)
                                                      #23 0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #24 0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #25 0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4026:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4718:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 4717:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 7043:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 7044:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 7045:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 7046:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 7047:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 10851:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329bc8e __pthread_cond_wait_common (libc.so.6 + 0x9bc8e)
                                                      #2  0x00005a8655d58e7f _ZN7mozilla6detail21ConditionVariableImpl8wait_forERNS0_9MutexImplERKNS_16BaseTimeDurationINS_27TimeDurationValueCalculatorEEE (firefox-bin + 0xb0e7f)
                                                      #3  0x000076b859c46b9d n/a (libxul.so + 0x3a46b9d)
                                                      #4  0x000076b859b4fe1d n/a (libxul.so + 0x394fe1d)
                                                      #5  0x000076b859b4e012 n/a (libxul.so + 0x394e012)
                                                      #6  0x000076b85acf97ce n/a (libxul.so + 0x4af97ce)
                                                      #7  0x000076b8638f270f n/a (libnspr4.so + 0x1e70f)
                                                      #8  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #9  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #10 0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 10853:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329bc8e __pthread_cond_wait_common (libc.so.6 + 0x9bc8e)
                                                      #2  0x00005a8655d58e7f _ZN7mozilla6detail21ConditionVariableImpl8wait_forERNS0_9MutexImplERKNS_16BaseTimeDurationINS_27TimeDurationValueCalculatorEEE (firefox-bin + 0xb0e7f)
                                                      #3  0x000076b859c46b9d n/a (libxul.so + 0x3a46b9d)
                                                      #4  0x000076b859b4fe1d n/a (libxul.so + 0x394fe1d)
                                                      #5  0x000076b859b4e012 n/a (libxul.so + 0x394e012)
                                                      #6  0x000076b85acf97ce n/a (libxul.so + 0x4af97ce)
                                                      #7  0x000076b8638f270f n/a (libnspr4.so + 0x1e70f)
                                                      #8  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #9  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #10 0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 10854:
                                                      #0  0x000076b863298f70 futex_wait (libc.so.6 + 0x98f70)
                                                      #1  0x000076b8632a0101 lll_mutex_lock_optimized (libc.so.6 + 0xa0101)
                                                      #2  0x000076b84339367d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59367d)
                                                      #3  0x000076b842ef869d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0xf869d)
                                                      #4  0x000076b84cfd6ca5 vaCreateBuffer (libva.so.2 + 0x6ca5)
                                                      #5  0x000076b84f801e29 n/a (libavcodec.so.60 + 0x801e29)
                                                      #6  0x000076b84f8130d6 n/a (libavcodec.so.60 + 0x8130d6)
                                                      #7  0x000076b84f3d5b85 n/a (libavcodec.so.60 + 0x3d5b85)
                                                      #8  0x000076b84f2a9a45 n/a (libavcodec.so.60 + 0x2a9a45)
                                                      #9  0x000076b84f2aa044 avcodec_send_packet (libavcodec.so.60 + 0x2aa044)
                                                      #10 0x000076b85d601c4b n/a (libxul.so + 0x7401c4b)
                                                      #11 0x000076b85d5be5a6 n/a (libxul.so + 0x73be5a6)
                                                      #12 0x000076b85d5f95a4 n/a (libxul.so + 0x73f95a4)
                                                      #13 0x000076b85d572bbb n/a (libxul.so + 0x7372bbb)
                                                      #14 0x000076b859c47b96 n/a (libxul.so + 0x3a47b96)
                                                      #15 0x000076b859c46d5f n/a (libxul.so + 0x3a46d5f)
                                                      #16 0x000076b859b4fe1d n/a (libxul.so + 0x394fe1d)
                                                      #17 0x000076b859b4e012 n/a (libxul.so + 0x394e012)
                                                      #18 0x000076b85acf97ce n/a (libxul.so + 0x4af97ce)
                                                      #19 0x000076b8638f270f n/a (libnspr4.so + 0x1e70f)
                                                      #20 0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #21 0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #22 0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      
                                                      Stack trace of thread 10855:
                                                      #0  0x000076b863298d71 __futex_abstimed_wait_common64 (libc.so.6 + 0x98d71)
                                                      #1  0x000076b86329b7ed __pthread_cond_wait_common (libc.so.6 + 0x9b7ed)
                                                      #2  0x000076b84339359d n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x59359d)
                                                      #3  0x000076b84336054b n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x56054b)
                                                      #4  0x000076b8433934cc n/a (libgallium-25.0.7-0ubuntu0.24.04.2.so + 0x5934cc)
                                                      #5  0x00005a8655d13ee0 n/a (firefox-bin + 0x6bee0)
                                                      #6  0x000076b86329caa4 start_thread (libc.so.6 + 0x9caa4)
                                                      #7  0x000076b863329a64 __clone (libc.so.6 + 0x129a64)
                                                      ELF object binary architecture: AMD x86-64
Oct 15 12:06:03 Desktop-Mint systemd[1]: systemd-coredump@1-10881-0.service: Deactivated successfully.
```

---

## 评论 (21 条)

### 评论 #1 — tcgu-amd (2025-10-17T18:03:54Z)

Hi @TheConanRider, thanks for reaching out! I can't seem to repro your issue using the ltxv example locally, although I did experience OOM error with the example workflow. However, this seems to be an issue with ComfyUI since after disabling smart memory management the issue appear to have gone away. 

The setups I have tried: 
- CPU  AMD Ryzen 9 7950X + GPU AMD Radeon RX 7900 XT
-  Ubuntu 24.04
- ROCm 7.0.2 installed through the [quick start guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html), 

combined with 
- Official Torch 2.9.0 + ROCm 6.4 (stable) from Pytorch release
- Nightly Torch 2.10 + ROCm 7.0 from Pytorch release
- the [nightly pytorch+rocm7.0.2 build from TheRock](https://github.com/ROCm/TheRock/blob/main/RELEASES.md). 

And I launched ComfyUI with the following command:

`TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python main.py --use-pytorch-cross-attention --disable-smart-memory`

However, we did get some other reports about occasional instability with the official Pytorch builds. Just in case, can you try install pytorch through TheRock and let me know the results? Thanks! 

Also, if you can provide the ComfyUI logs during the crash that would be great. 

---

### 评论 #2 — TheConanRider (2025-10-18T15:21:18Z)

I'll do some more testing but I don't think I can provide ComfyUI logs since the entire system goes down when the amdgpu resets. 

I am unable to test with pytorch+rocm7.0.2 build from TheRock because I can't find that build but testing with 7.10 from TheRock causes a HIP out of memory issue where it seems that I am trying to allocate 78GB of VRAM on a 24GB card. 

The environment variable and disabling smart memory seem to have a large effect on performance (2x slowdown)

I would recommend trying out some of the larger video models i.e Wan2.1, 2.2 etc to more easily reproduce this issue. LTXVideo is very lightweight and was decently consistent before. Repeat runs seem to make it crash too. 

---

### 评论 #3 — TheConanRider (2025-10-18T21:00:23Z)

## Rocm 7.10

Checkpoint files will always be loaded safely.
Total VRAM 24560 MB, total RAM 32019 MB
pytorch version: 2.10.0a0+rocm7.10.0a20251015
AMD arch: gfx1100
ROCm version: (7, 1)
Set vram state to: NORMAL_VRAM
Disabling smart memory management
Device: cuda:0 AMD Radeon RX 7900 XTX : native
Using pytorch attention
Python version: 3.12.11 (main, Jul 23 2025, 00:34:44) [Clang 20.1.4 ]
ComfyUI version: 0.3.64
ComfyUI frontend version: 1.27.10


Gives out of memory
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 77.52 GiB. GPU 0 has a total capacity of 23.98 GiB of which 4.98 GiB is free. Of the allocated memory 18.13 GiB is allocated by PyTorch, and 343.84 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

## Rocm 7
Checkpoint files will always be loaded safely.
Total VRAM 24560 MB, total RAM 32019 MB
pytorch version: 2.10.0.dev20251016+rocm7.0
AMD arch: gfx1100
ROCm version: (7, 0)
Set vram state to: NORMAL_VRAM
Disabling smart memory management
Device: cuda:0 Radeon RX 7900 XTX : native
Using pytorch attention
torchaudio missing, ACE model will be broken
torchaudio missing, ACE model will be broken
Python version: 3.12.11 (main, Jul 23 2025, 00:34:44) [Clang 20.1.4 ]
ComfyUI version: 0.3.64
ComfyUI frontend version: 1.27.10

runs but 2x slower than previously generated with smart memory and env flag off
700s per gen, 1243s for initial

## ROCM 6.4
Checkpoint files will always be loaded safely.
Total VRAM 24560 MB, total RAM 32019 MB
pytorch version: 2.9.0+rocm6.4
AMD arch: gfx1100
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Disabling smart memory management
Device: cuda:0 Radeon RX 7900 XTX : native
Using pytorch attention
Python version: 3.12.11 (main, Jul 23 2025, 00:34:44) [Clang 20.1.4 ]
ComfyUI version: 0.3.64
ComfyUI frontend version: 1.27.10

VAEDecode seems to get into a hung position. 100% system ram (32gb), 100% VRAM (24gb) and 100% disk (100mb/s r/w)


---

### 评论 #4 — TheConanRider (2025-10-19T22:41:58Z)

I reverted back to using rocm6.4 and managed to reproduce with the smartmemory flag enabled with the env flag on. 
 Tutorial to reproduce found here: https://docs.comfy.org/tutorials/video/wan/wan2_2 or you can load the template from comfy > template > video > wan 2.2 14b image to video.

Comfy log from crash: 
```
Adding extra search path checkpoints /home/ryan/Downloads/Data/Models/StableDiffusion
Adding extra search path diffusers /home/ryan/Downloads/Data/Models/Diffusers
Adding extra search path loras /home/ryan/Downloads/Data/Models/Lora
Adding extra search path loras /home/ryan/Downloads/Data/Models/LyCORIS
Adding extra search path clip /home/ryan/Downloads/Data/Models/TextEncoders
Adding extra search path clip_vision /home/ryan/Downloads/Data/Models/ClipVision
Adding extra search path embeddings /home/ryan/Downloads/Data/Models/Embeddings
Adding extra search path vae /home/ryan/Downloads/Data/Models/VAE
Adding extra search path vae_approx /home/ryan/Downloads/Data/Models/ApproxVAE
Adding extra search path controlnet /home/ryan/Downloads/Data/Models/ControlNet
Adding extra search path controlnet /home/ryan/Downloads/Data/Models/T2IAdapter
Adding extra search path gligen /home/ryan/Downloads/Data/Models/GLIGEN
Adding extra search path upscale_models /home/ryan/Downloads/Data/Models/ESRGAN
Adding extra search path upscale_models /home/ryan/Downloads/Data/Models/RealESRGAN
Adding extra search path upscale_models /home/ryan/Downloads/Data/Models/SwinIR
Adding extra search path hypernetworks /home/ryan/Downloads/Data/Models/Hypernetwork
Adding extra search path ipadapter /home/ryan/Downloads/Data/Models/IpAdapter
Adding extra search path ipadapter /home/ryan/Downloads/Data/Models/IpAdapters15
Adding extra search path ipadapter /home/ryan/Downloads/Data/Models/IpAdaptersXl
Adding extra search path prompt_expansion /home/ryan/Downloads/Data/Models/PromptExpansion
Adding extra search path ultralytics /home/ryan/Downloads/Data/Models/Ultralytics
Adding extra search path ultralytics_bbox /home/ryan/Downloads/Data/Models/Ultralytics/bbox
Adding extra search path ultralytics_segm /home/ryan/Downloads/Data/Models/Ultralytics/segm
Adding extra search path sams /home/ryan/Downloads/Data/Models/Sams
Adding extra search path diffusion_models /home/ryan/Downloads/Data/Models/DiffusionModels
[ComfyUI-Manager] Using uv as Python module for pip operations.
Using Python 3.12.11 environment at: venv
[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** ComfyUI startup time: 2025-10-19 23:34:51.541
** Platform: Linux
** Python version: 3.12.11 (main, Jul 23 2025, 00:34:44) [Clang 20.1.4 ]
** Python executable: /home/ryan/Downloads/Data/Packages/ComfyUI/venv/bin/python3
** ComfyUI Path: /home/ryan/Downloads/Data/Packages/ComfyUI
** ComfyUI Base Folder Path: /home/ryan/Downloads/Data/Packages/ComfyUI
** User directory: /home/ryan/Downloads/Data/Packages/ComfyUI/user
** ComfyUI-Manager config path: /home/ryan/Downloads/Data/Packages/ComfyUI/user/default/ComfyUI-Manager/config.ini
** Log path: /home/ryan/Downloads/Data/Packages/ComfyUI/user/comfyui.log
Using Python 3.12.11 environment at: venv
Using Python 3.12.11 environment at: venv

Prestartup times for custom nodes:
   0.7 seconds: /home/ryan/Downloads/Data/Packages/ComfyUI/custom_nodes/ComfyUI-Manager

Checkpoint files will always be loaded safely.
Total VRAM 24560 MB, total RAM 32019 MB
pytorch version: 2.9.0+rocm6.4
AMD arch: gfx1100
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Disabling smart memory management
Device: cuda:0 Radeon RX 7900 XTX : native
Using pytorch attention
Python version: 3.12.11 (main, Jul 23 2025, 00:34:44) [Clang 20.1.4 ]
ComfyUI version: 0.3.64
ComfyUI frontend version: 1.27.10
[Prompt Server] web root: /home/ryan/Downloads/Data/Packages/ComfyUI/venv/lib/python3.12/site-packages/comfyui_frontend_package/static
ComfyUI-GGUF: Allowing full torch compile
### Loading: ComfyUI-Manager (V3.37)
[ComfyUI-Manager] network_mode: public
[ComfyUI-Manager] Since --preview-method is set, ComfyUI-Manager's preview method feature will be ignored.
### ComfyUI Revision: 4053 [63722199] *DETACHED | Released on '2025-10-08'

Import times for custom nodes:
   0.0 seconds: /home/ryan/Downloads/Data/Packages/ComfyUI/custom_nodes/websocket_image_save.py
   0.0 seconds: /home/ryan/Downloads/Data/Packages/ComfyUI/custom_nodes/ComfyUI-Frame-Interpolation
   0.0 seconds: /home/ryan/Downloads/Data/Packages/ComfyUI/custom_nodes/ComfyUI-GGUF
   0.2 seconds: /home/ryan/Downloads/Data/Packages/ComfyUI/custom_nodes/ComfyUI-Manager
   0.4 seconds: /home/ryan/Downloads/Data/Packages/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite

[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/alter-list.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/model-list.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/github-stats.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/extension-node-map.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json
Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://127.0.0.1:8188
FETCH ComfyRegistry Data: 5/101
FETCH ComfyRegistry Data: 10/101
FETCH ComfyRegistry Data: 15/101
FETCH ComfyRegistry Data: 20/101
FETCH ComfyRegistry Data: 25/101
FETCH ComfyRegistry Data: 30/101
FETCH ComfyRegistry Data: 35/101
FETCH ComfyRegistry Data: 40/101
FETCH ComfyRegistry Data: 45/101
FETCH ComfyRegistry Data: 50/101
FETCH ComfyRegistry Data: 55/101
FETCH ComfyRegistry Data: 60/101
FETCH ComfyRegistry Data: 65/101
FETCH ComfyRegistry Data: 70/101
FETCH ComfyRegistry Data: 75/101
FETCH ComfyRegistry Data: 80/101
FETCH ComfyRegistry Data: 85/101
FETCH ComfyRegistry Data: 90/101
FETCH ComfyRegistry Data: 95/101
FETCH ComfyRegistry Data: 100/101
FETCH ComfyRegistry Data [DONE]
[ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json [DONE]
[ComfyUI-Manager] All startup tasks have been completed.
```

Rest of logs from crash (system was locked up)
![Image](https://github.com/user-attachments/assets/c93e72ef-622a-4f7e-ab05-638f7e6bda25)

journalcrl -b -1 --no-pager

```
Oct 19 23:31:39 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Oct 19 23:31:39 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Oct 19 23:31:39 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Oct 19 23:31:39 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to evict queue 1
Oct 19 23:31:39 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to evict process queues
Oct 19 23:31:39 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset begin!
Oct 19 23:31:40 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to restore queue 2
Oct 19 23:31:40 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Failed to restore process queues
Oct 19 23:31:41 Desktop-Mint NetworkManager[1070]: <warn>  [1760913101.4889] platform-linux: do-add-ip6-address[2: fe80::336e:2cac:5026:dfeb]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 19 23:31:43 Desktop-Mint NetworkManager[1070]: <warn>  [1760913103.4900] platform-linux: do-add-ip6-address[2: fe80::d1ed:c30c:477f:bd7d]: failure 13 (Permission denied - ipv6: IPv6 is disabled on this device)
Oct 19 23:31:43 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: failed to suspend display audio
Oct 19 23:31:43 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 2 for dev 28088
Oct 19 23:31:43 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Dumping IP State
Oct 19 23:31:43 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: Dumping IP State Completed
Oct 19 23:31:43 Desktop-Mint systemd[1]: Created slice system-systemd\x2dcoredump.slice - Slice /system/systemd-coredump.
Oct 19 23:31:43 Desktop-Mint systemd[1]: Started systemd-coredump@0-39714-0.service - Process Core Dump (PID 39714/UID 0).
Oct 19 23:31:45 Desktop-Mint NetworkManager[1070]: <warn>  [1760913105.4915] ipv6ll[85852a257f858ddf,ifindex=2]: changed: no IPv6 link local address to retry after Duplicate Address Detection failures (back off)
Oct 19 23:31:45 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Oct 19 23:31:45 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 19 23:31:47 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Oct 19 23:31:47 Desktop-Mint kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: MODE1 reset
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU mode1 reset
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU smu mode1 reset
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset succeeded, trying to resume
Oct 19 23:31:48 Desktop-Mint kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
Oct 19 23:31:48 Desktop-Mint kernel: [drm] VRAM is lost due to GPU reset!
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: PSP is resuming...
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: RAP: optional rap ta ucode is not available
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU is resuming...
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x0000003f, smu fw program = 0, smu fw version = 0x004e7900 (78.121.0)
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU driver if version not matched
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU is resumed successfully!
Oct 19 23:31:48 Desktop-Mint kernel: [drm] DMUB hardware initialized: version=0x07002900
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
Oct 19 23:31:49 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: GPU reset(1) succeeded!
Oct 19 23:31:49 Desktop-Mint systemd[1]: Started systemd-coredump@1-39726-0.service - Process Core Dump (PID 39726/UID 0).


```

---

### 评论 #5 — TheConanRider (2025-10-19T22:42:15Z)

If you need any more information feel free to ask.

---

### 评论 #6 — tcgu-amd (2025-10-21T20:11:24Z)

@TheConanRider Thanks for the update! Although I still cannot seem to reproduce your issue, I did notice something from your log:

```
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x0000003f, smu fw program = 0, smu fw version = 0x004e7900 (78.121.0)
Oct 19 23:31:48 Desktop-Mint kernel: amdgpu 0000:28:00.0: amdgpu: SMU driver if version not matched
```

What is you AMDGPU version?

---

### 评论 #7 — TheConanRider (2025-10-22T14:38:27Z)

Not quite sure how to find that but I am using kernal 6.14.0-33-generic
apt show amdgpu shows 
Package: amdgpu
Version: 1:7.0.70002-2226275.24.04
Priority: optional
Section: metapackages
Maintainer: Advanced Micro Devices (AMD) <slava.grigorev@amd.com>
Installed-Size: 9,216 B
Depends: amdgpu-dkms, amdgpu-lib (= 1:7.0.70002-2226275.24.04)
Download-Size: 1,684 B
APT-Sources: https://repo.radeon.com/graphics/7.0.2/ubuntu noble/main amd64 Packages
Description: Meta package to install amdgpu components.


---

### 评论 #8 — tcgu-amd (2025-10-22T14:59:40Z)

@TheConanRider, sorry I should have mentioned you can find version information with `amd-smi version` and `amd-smi firmware`. 

---

### 评论 #9 — TheConanRider (2025-10-22T15:19:58Z)

I don't have amd-smi installed. It returns "amd-smi: command not found"

---

### 评论 #10 — tcgu-amd (2025-10-22T16:54:47Z)

In that case, try `sudo cat /sys/kernel/debug/dri/0/amdgpu_firmware_info`?

---

### 评论 #11 — tcgu-amd (2025-10-22T17:40:21Z)

By the way, I also see the ridiculous large allocation with rocm7.10 from TheRock. Something definitely is not right here. Will look into what's going on. 

---

### 评论 #12 — tcgu-amd (2025-10-22T18:41:02Z)

@TheConanRider There seems to be some issues with Linux pytorch builds with due to changes in aotriton on Linux (see here https://github.com/ROCm/TheRock/tree/main/external-builds/pytorch#support-status). I think this could be linked to the instability you are experiencing with the latest torch versions. 

---

### 评论 #13 — TheConanRider (2025-10-22T19:25:21Z)

Had to run sudo cat /sys/kernel/debug/dri/**1**/amdgpu_firmware_info , 0 didn't exist

VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000600
PFP feature version: 29, firmware version: 0x00000660
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x00000076
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x00000019
RLCV feature version: 1, firmware version: 0x00000022
MEC feature version: 29, firmware version: 0x00000226
IMU feature version: 0, firmware version: 0x0b1f4900
SOS feature version: 3211312, firmware version: 0x00310030
ASD feature version: 553648315, firmware version: 0x210000bb
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b000205
TA HDCP feature version: 0x00000000, firmware version: 0x1700003a
TA DTM feature version: 0x00000000, firmware version: 0x12000015
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004e7900 (78.121.0)
SDMA0 feature version: 60, firmware version: 0x00000013
SDMA1 feature version: 60, firmware version: 0x00000013
VCN feature version: 0, firmware version: 0x07113000
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x07002900
TOC feature version: 12, firmware version: 0x0000000c
MES_KIQ feature version: 6, firmware version: 0x00000075
MES feature version: 1, firmware version: 0x00000051
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-31XFSHBS1-L03


---

### 评论 #14 — tcgu-amd (2025-10-22T20:50:41Z)

It does appear that your firmware versions, especially your sdma fw and smc fw are a quite couple versions behind. That could be a potential cause. Below is what I have on my end. Can you try upgrading your firmware? 

```
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000956
PFP feature version: 29, firmware version: 0x000009e2
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x00000080
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x00000019
RLCV feature version: 1, firmware version: 0x00000022
MEC feature version: 29, firmware version: 0x00000a28
IMU feature version: 0, firmware version: 0x0b1f4b00
SOS feature version: 3211315, firmware version: 0x00310033
ASD feature version: 553648367, firmware version: 0x210000ef
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b000205
TA HDCP feature version: 0x00000000, firmware version: 0x17000046
TA DTM feature version: 0x00000000, firmware version: 0x12000019
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004e8100 (78.129.0)
SDMA0 feature version: 60, firmware version: 0x00000018
SDMA1 feature version: 60, firmware version: 0x00000018
VCN feature version: 0, firmware version: 0x0911800d
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x07002f00
TOC feature version: 12, firmware version: 0x0000000c
MES_KIQ feature version: 6, firmware version: 0x00000103
MES feature version: 1, firmware version: 0x0000007c
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-D70401XT-N11
```

---

### 评论 #15 — TheConanRider (2025-10-22T21:49:39Z)

I can't. I am fully up to date with all updates avalible on linux mint

---

### 评论 #16 — TheConanRider (2025-10-22T23:32:15Z)

Actually I managed to do a dirty update and I've got a higher version. I will try to reproduce
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000974
PFP feature version: 29, firmware version: 0x00000a14
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x00000080
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x00000019
RLCV feature version: 1, firmware version: 0x00000022
MEC feature version: 29, firmware version: 0x00000a5a
IMU feature version: 0, firmware version: 0x0b1f4b00
SOS feature version: 3211317, firmware version: 0x00310035
ASD feature version: 553648378, firmware version: 0x210000fa
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b000205
TA HDCP feature version: 0x00000000, firmware version: 0x17000049
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004e8200 (78.130.0)
SDMA0 feature version: 60, firmware version: 0x0000001b
SDMA1 feature version: 60, firmware version: 0x0000001b
VCN feature version: 0, firmware version: 0x09118016
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x07002f00
TOC feature version: 12, firmware version: 0x0000000c
MES_KIQ feature version: 6, firmware version: 0x00000104
MES feature version: 1, firmware version: 0x00000080
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-31XFSHBS1-L03

---

### 评论 #17 — tcgu-amd (2025-10-23T16:36:13Z)

Hi @TheConanRider, actually, aside from firmware updates, another potential reasons can be long compute jobs being mistaken for a hang from MES's perspective. There's currently a patch pending for this https://github.com/torvalds/linux/commit/1fb710793ce2619223adffaf981b1ff13cd48f17#diff-a9d0de1bf0951b27b3ae2a92a59ab245fb5a3c1d6b5e20cdefb3deb0842bf76c. 

Another thing that I am curious about is, if you turn off your GUI, can you avoid running into the hang? 

---

### 评论 #18 — TheConanRider (2025-10-23T18:45:38Z)

So far on the latest firmware I am unable to reproduce the crash. I am going to try and restore back to the version I initally reproduced it on and see if that makes any difference. 

---

### 评论 #19 — ianbmacdonald (2025-10-24T02:34:35Z)

On 6.14.0-33-generic, if not patched, it will come back..   Below is the mainline commits to make the kernel work with your 0x80 firmware to avoid the hang (has to be 0x7f or newer) if you want to check your mint kernel changelog.   The patches are simple enough if you want to just apt source / patch / dpkg-buildpackage your own updated mint kernel.   

[https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?h=linux-6.14.y&id=5980a35c9d138804251e50788c1e8137028a47ac](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?h=linux-6.14.y&id=5980a35c9d138804251e50788c1e8137028a47ac)

That `MES feature version: 1, firmware version: 0x00000051` is pretty ancient.  It makes me think your firmware was stuck due to another package policy. 

If you have amdgpu-dkms-firmware installed, it will take priority over linux-firmware, and if you upgraded from ROCm <7.0, you may have also have had an apt policy issue.  

In that problem scenario, even the repo.radeon.com updates will not get applied with the apt preference priority of 600 proposed in the online docs. Here is what Instinct 30.10.2 (ROCm 7.0.2) looks like when its sitting on top of an Instinct/ROCm 6.4.4 install previously.   You can pull the very latest linux-firmware in this state, and end up with some old version like you described above.   The change in numbering for the Instinct drivers throws a wrench into debugging MES firmware if you were hoping an updated linux-firmware was going to solve the firmware problem.   This particular issue does not go away when both linux-firmware and newer instinct amdgpu-dkms-firmware are released if you just upgrade.  You have to update your preferences, or simply remove and reinstall the packages.

```
# apt policy amdgpu-dkms-firmware

amdgpu-dkms-firmware:
  Installed: 1:6.12.12.60404-2202139.24.04
  Candidate: 1:6.12.12.60404-2202139.24.04
  Version table:
 *** 1:6.12.12.60404-2202139.24.04 100
        100 /var/lib/dpkg/status
     30.10.2.0.30100200-2226257.24.04 **600**
        600 https://repo.radeon.com/amdgpu/30.10.2/ubuntu noble/main amd64 Packages
```

Here is what I was using to pull the correct repo.radeon.com package on Ubuntu 25.10 questing (which comes with newer amdgpu, so it just needs firmware for ROCm 7.0.2) before I removed amdgpu-dkms-firmware to make way for a newer linux-firmware @ 0x80 and like yourself, I side-loaded with a quick wget/dpkg -i using the Racoon repo deb @ https://launchpad.net/ubuntu/+source/linux-firmware

```
$ cat /etc/apt/preferences.d/92-instinct-version-pin 
Package: amdgpu-dkms-firmware
Pin: version 30.*
Pin-Priority: 1001

```

---

### 评论 #20 — TheConanRider (2025-10-24T08:37:42Z)

@ianbmacdonald I don't have amdgpu-dkms-firmware installed 
$ apt policy amdgpu-dkms-firmware
amdgpu-dkms-firmware:
  Installed: (none)
  Candidate: 30.10.2.0.30100200-2226257.24.04
  Version table:
     30.10.2.0.30100200-2226257.24.04 600
        600 https://repo.radeon.com/amdgpu/30.10.2/ubuntu noble/main amd64 Packages
        600 https://repo.radeon.com/amdgpu/30.10.2/ubuntu noble/main i386 Packages


---

### 评论 #21 — TheConanRider (2025-10-28T12:33:28Z)

I've tested this a lot and cannot seem to reproduce. I will close this issue now. Thank you for the help

---
