# [Issue]: amdgpu driver  errors

> **Issue #2642**
> **状态**: closed
> **创建时间**: 2023-11-14T16:30:59Z
> **更新时间**: 2025-09-25T17:10:27Z
> **关闭时间**: 2024-08-20T18:13:11Z
> **作者**: bog-dan-ro
> **标签**: 5.7.0, 5.7.1
> **URL**: https://github.com/ROCm/ROCm/issues/2642

## 标签

- **5.7.0** (颜色: #fef2c0)
- **5.7.1** (颜色: #b60205)

## 描述

### Problem Description

When running some examples I see errors in dmesg:

/opt/rocm-5.7.0/share/hip/samples/2_Cookbook/0_MatrixTranspose
```
[  262.094619] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:158 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  262.094625] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0010 address=0x64a7f000 flags=0x0000]
[  262.094626] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[  262.094630] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3C
[  262.094634] amdgpu 0000:03:00.0: amdgpu:    Faulty UTCL2 client ID: CPC (0x5)
[  262.094637] amdgpu 0000:03:00.0: amdgpu:    MORE_FAULTS: 0x0
[  262.094639] amdgpu 0000:03:00.0: amdgpu:    WALKER_ERROR: 0x6
[  262.094641] amdgpu 0000:03:00.0: amdgpu:    PERMISSION_FAULTS: 0x3
[  262.094643] amdgpu 0000:03:00.0: amdgpu:    MAPPING_ERROR: 0x1
[  262.094645] amdgpu 0000:03:00.0: amdgpu:    RW: 0x0
[  262.094688] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0010 address=0x64a7f000 flags=0x0020]
[  262.230974] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0010 address=0x64a7f000 flags=0x0020]
```
Same error ^  /opt/rocm-5.7.0/share/hip/samples/2_Cookbook/10_inline_asm

/opt/rocm-5.7.0/share/hip/samples/2_Cookbook/16_assembly_to_executable$ ./square_asm.out
app output:
```
info: running on device Radeon RX 7900 XT
info: allocate host mem (  7.63 MB)
info: allocate device mem (  7.63 MB)
info: copy Host2Device
info: launch 'vector_square' kernel
info: copy Device2Host
info: check result
error: 'unknown error'(999) at square.cpp:92
```

dmesg output:
```
[  456.201981] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:158 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  456.201986] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[  456.201988] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3C
[  456.201989] amdgpu 0000:03:00.0: amdgpu:    Faulty UTCL2 client ID: CPC (0x5)
[  456.201991] amdgpu 0000:03:00.0: amdgpu:    MORE_FAULTS: 0x0
[  456.201992] amdgpu 0000:03:00.0: amdgpu:    WALKER_ERROR: 0x6
[  456.201993] amdgpu 0000:03:00.0: amdgpu:    PERMISSION_FAULTS: 0x3
[  456.201994] amdgpu 0000:03:00.0: amdgpu:    MAPPING_ERROR: 0x1
[  456.201995] amdgpu 0000:03:00.0: amdgpu:    RW: 0x0
[  456.202002] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0010 address=0x64a7f000 flags=0x0000]
[  456.202058] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0010 address=0x64a7f000 flags=0x0020]
[  456.332547] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0010 address=0x64a7f000 flags=0x0020]
```


### Operating System

22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 7950X3D

### GPU

Radeon RX 7900 XT

### ROCm Version

5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

Run those examples and check the `dmesg` output.

Running the same examples and some LLMs using the FOSS mesa drivers work just fine, is `amdgpu` really needed for ROCm? If not what are the advantages of the `amdgpu`  ?


### Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    AMD Ryzen 9 7950X3D 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X3D 16-Core Processor
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
  Max Clock Freq. (MHz):   5759                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65564044(0x3e86d8c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65564044(0x3e86d8c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65564044(0x3e86d8c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-0001b7e800000000               
  Marketing Name:          Radeon RX 7900 XT                  
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
    L3:                      81920(0x14000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2075                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            84                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
  Packet Processor uCode:: 494                                
  SDMA engine uCode::      19                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20955136(0x13fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    20955136(0x13fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
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


---

## 评论 (13 条)

### 评论 #1 — ZhangLearning (2023-11-15T07:21:59Z)

This issues is same to me. If it's solved, please let me know. 
I used RX7600 On ROCm 5.7.1 ,I was running the opencl cts test and found the same dmesg error，but the test was still runing,It didn't seem to have any impact。

dmesg log：
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.614:2): apparmor="STATUS" operation="profile_load" profile="unconfined" name="libreoffice-xpdfimport" pid=690 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.614:3): apparmor="STATUS" operation="profile_load" profile="unconfined" name="libreoffice-oosplash" pid=687 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.614:4): apparmor="STATUS" operation="profile_load" profile="unconfined" name="libreoffice-senddoc" pid=688 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.618:5): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/bin/man" pid=685 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.618:6): apparmor="STATUS" operation="profile_load" profile="unconfined" name="man_filter" pid=685 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.618:7): apparmor="STATUS" operation="profile_load" profile="unconfined" name="man_groff" pid=685 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.618:8): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lsb_release" pid=681 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.618:9): apparmor="STATUS" operation="profile_load" profile="unconfined" name="nvidia_modprobe" pid=682 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.618:10): apparmor="STATUS" operation="profile_load" profile="unconfined" name="nvidia_modprobe//kmod" pid=682 comm="apparmor_parser"
[三 11月 15 15:13:45 2023] audit: type=1400 audit(1700032426.618:11): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/sbin/cups-browsed" pid=692 comm="apparmor_parser"
[三 11月 15 15:13:46 2023] Generic FE-GE Realtek PHY r8169-0-400:00: attached PHY driver (mii_bus:phy_addr=r8169-0-400:00, irq=MAC)
[三 11月 15 15:13:46 2023] r8169 0000:04:00.0 enp4s0: Link is Down
[三 11月 15 15:13:46 2023] loop15: detected capacity change from 0 to 8
[三 11月 15 15:13:47 2023] rfkill: input handler disabled
[三 11月 15 15:13:50 2023] r8169 0000:04:00.0 enp4s0: Link is Up - 1Gbps/Full - flow control off
[三 11月 15 15:13:50 2023] IPv6: ADDRCONF(NETDEV_CHANGE): enp4s0: link becomes ready
[三 11月 15 15:13:55 2023] kauditd_printk_skb: 39 callbacks suppressed
[三 11月 15 15:13:55 2023] audit: type=1400 audit(1700032435.858:51): apparmor="STATUS" operation="profile_load" profile="unconfined" name="docker-default" pid=1840 comm="apparmor_parser"
[三 11月 15 15:13:55 2023] bridge: filtering via arp/ip/ip6tables is no longer available by default. Update your scripts to load br_netfilter if you need this.
[三 11月 15 15:13:55 2023] Bridge firewalling registered
[三 11月 15 15:13:55 2023] Initializing XFRM netlink socket
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:158 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0000]
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3C
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu:          MORE_FAULTS: 0x0
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu:          WALKER_ERROR: 0x6
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu:          MAPPING_ERROR: 0x1
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: amdgpu:          RW: 0x0
[三 11月 15 15:15:38 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0020]
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0020]
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0000]
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:158 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3C
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0020]
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu:          MORE_FAULTS: 0x0
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu:          WALKER_ERROR: 0x6
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu:          MAPPING_ERROR: 0x1
[三 11月 15 15:15:47 2023] amdgpu 0000:07:00.0: amdgpu:          RW: 0x0
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0020]
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:158 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3C
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu:          MORE_FAULTS: 0x0
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0000]
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu:          WALKER_ERROR: 0x6
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu:          MAPPING_ERROR: 0x1
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: amdgpu:          RW: 0x0
[三 11月 15 15:19:52 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0020]
[三 11月 15 15:21:59 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0020]
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:158 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0013 address=0xbfffd000 flags=0x0000]
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3C
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu:          MORE_FAULTS: 0x0
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu:          WALKER_ERROR: 0x6
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu:          MAPPING_ERROR: 0x1
[三 11月 15 15:22:00 2023] amdgpu 0000:07:00.0: amdgpu:          RW: 0x0


---

### 评论 #2 — danielzgtg (2023-11-15T20:45:20Z)

> GCVM_L2_PROTECTION_FAULT_STATUS

~~Duplicate~~ Potential duplicate of my #2596

They said it's caused by a bug in the CPU page table update code. You can either revert the commit I mentioned and hope some thing work, or wait for them to release the actual fix.

---

### 评论 #3 — voyageur (2023-12-22T17:50:11Z)

I do not think it is a duplicate of #2596, the GCVM_L2_PROTECTION_FAULT_STATUS is different and there is no NULL pointer dereference. Also the mentioned possible workarounds have no effect for this 0x00000B3C status (revert of https://lists.freedesktop.org/archives/amd-gfx/2023-October/100298.html, revert of 96c211f1f9ef82183493f4ceed4e347b52849149 as mentioned in https://gitlab.freedesktop.org/drm/amd/-/issues/2991, or changing amdgpu.vm_update_mode)

I also have a RX 7900 XT  and the same error as here, there is also this stable-diffusion-webui report with same card and same code: https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/14128. This sounds like a Navi 31 specific bug.

I am not sure if the bug is directly in amdgpu or in rocm,but running stable-diffusion-webui with rocm 5.7 triggers a lot of these faults, until it triggers a GPU reset ([dmesg log](https://github.com/ROCm/ROCm/files/13755089/dmesg-GCVM_L2_PROTECTION_FAULT_STATUS.0x00000B32.txt) attached). As mentioned this happens almost immediately with:
`TORCH_COMMAND="pip install torch torchvision --index-url https://download.pytorch.org/whl/nightly/rocm5.7"`
But I had no issue yet with 5.6 and:
`TORCH_COMMAND="pip install torch torchvision --index-url https://download.pytorch.org/whl/test/rocm5.6"`

---

### 评论 #4 — voyageur (2024-01-11T22:45:57Z)

Update on my previous comment, I am now running kernel 6.7.0 and stable diffusion works well now with rocm 5.7.
System log reports a few protection faults with a new code, B32 (mostly on UI startup or heavy activity) but that does not make the system unstable.
Sample error:
```
amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00000004fa801000 from client 10
amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x1
amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
```



---

### 评论 #5 — DistantThunder (2024-02-04T20:13:12Z)

Same here on Linux 6.6.10:

```
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu:   in page starting at address 0x000000057c801000 from client 10
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu:          MORE_FAULTS: 0x0
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu:          WALKER_ERROR: 0x1
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu:          MAPPING_ERROR: 0x1
févr. 04 21:11:02 _HOST_ kernel: amdgpu 0000:2b:00.0: amdgpu:          RW: 0x0
```

Running SD on 7900XTX with ROCm 5.7.

---

### 评论 #6 — voyageur (2024-03-06T09:00:37Z)

These GCVM_L2_PROTECTION_FAULT_STATUS errors seem to have completely disappeared now, after rebooting to kernel 6.7.7 (also switched to rocm 6)

---

### 评论 #7 — FeepingCreature (2024-03-30T15:27:33Z)

```
[ 6730.695657] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[ 6730.695663] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 6730.695665] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[ 6730.695666] amdgpu 0000:03:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[ 6730.695667] amdgpu 0000:03:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 6730.695668] amdgpu 0000:03:00.0: amdgpu:      WALKER_ERROR: 0x1
[ 6730.695669] amdgpu 0000:03:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[ 6730.695669] amdgpu 0000:03:00.0: amdgpu:      MAPPING_ERROR: 0x1
[ 6730.695670] amdgpu 0000:03:00.0: amdgpu:      RW: 0x0
```
`6.7.10-x64v3-xanmod1`, `Version: 6.0.2.60002-115~22.04`


---

### 评论 #8 — ppanchad-amd (2024-05-17T14:57:41Z)

@bog-dan-ro Can you please test with latest ROCm 6.1.2? If resolved, please close the ticket. Thanks!

---

### 评论 #9 — harkgill-amd (2024-08-20T18:13:11Z)

Hi @bog-dan-ro, I wasn't able to reproduce these page faults after running the MatrixTranspose, inline_asm or assembly_to_executable tests. My testing was done using ROCm 6.2 on a system running the Linux 6.8 kernel. 

I do see a couple of fixes rolled out related to page faults occuring after tests were successful. The root cause was likely the same  and the fix should resolve all the errors reported in this thread. If you do encounter these page faults again on the latest ROCm release, please open a new ticket and we will further investigate the issue. Thanks!

---

### 评论 #10 — yhojann-cl (2025-04-01T23:17:54Z)

Is a driver problem, have same crash playing Doom Eternal on Ubuntu 24.04 LTS using AMD Radeon RX 6800 XT and AMD Ryzen 7 5800 X3D:

```
[26164.481129] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:4 pasid:32790)
[26164.481137] amdgpu 0000:2f:00.0: amdgpu:  in process DOOMEternalx64v pid 39007 thread Default Worker  pid 39013
[26164.481141] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00008003e72a1000 from client 0x1b (UTCL2)
[26164.481145] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00441050
[26164.481148] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[26164.481151] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[26164.481153] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[26164.481156] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
[26164.481158] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[26164.481160] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x1
[26228.452216] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=154489, emitted seq=154490
[26228.452224] amdgpu 0000:2f:00.0: amdgpu: Process information: process DOOMEternalx64v pid 39007 thread Default Worker  pid 39010
[26228.452227] amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
...
[26229.863093] amdgpu 0000:2f:00.0: amdgpu: GPU reset(1) succeeded!
[26229.863337] [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!
```

---

### 评论 #11 — yhojann-cl (2025-09-20T23:55:32Z)

As of now, the amdgpu driver does not work well with the latest versions of the Linux kernel; it causes frequent crashes, both for gaming and for artificial intelligence applications.  Therefore, it's not worth buying an AMD graphics card yet.

Large threads for this unresolved issue:

- https://gitlab.freedesktop.org/drm/amd/-/issues/3067
- https://gitlab.freedesktop.org/drm/amd/-/issues/3131
- https://gitlab.freedesktop.org/drm/amd/-/issues/2496
- https://gitlab.freedesktop.org/drm/amd/-/issues/2408
- Etc...

---

### 评论 #12 — SwooshyCueb (2025-09-23T14:42:18Z)

I don't think the issues you have linked are related to this issue

---

### 评论 #13 — yhojann-cl (2025-09-25T17:10:27Z)

> I don't think the issues you have linked are related to this issue

Is not a ROCm issue, is a amdgpu driver issue, this is due to issues related to insecure memory management and problems in environment recovery, as described in the aforementioned issues.

---
