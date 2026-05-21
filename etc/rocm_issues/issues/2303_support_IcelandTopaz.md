# support Iceland/Topaz

> **Issue #2303**
> **状态**: closed
> **创建时间**: 2023-06-29T12:11:57Z
> **更新时间**: 2024-02-02T04:23:01Z
> **关闭时间**: 2024-02-02T04:23:01Z
> **作者**: yashikada
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2303

## 描述

I have this GPU:

```
01:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Topaz XT [Radeon R7 M260/M265 / M340/M360 / M440/M445 / 530/535 / 620/625 Mobile] (rev c1)
	Subsystem: Dell Topaz XT [Radeon R7 M260/M265 / M340/M360 / M440/M445 / 530/535 / 620/625 Mobile]

           *-display
                description: Display controller
                product: Topaz XT [Radeon R7 M260/M265 / M340/M360 / M440/M445 / 530/535 / 620/625 Mobile]
                vendor: Advanced Micro Devices, Inc. [AMD/ATI]
                physical id: 0
                bus info: pci@0000:01:00.0

clinfo
  Platform Name                                   AMD Accelerated Parallel Processing
Number of devices                                 1
  Device Name                                     Iceland
  Device Vendor                                   Advanced Micro Devices, Inc.
  Device Vendor ID                                0x1002
  Device Version                                  OpenCL 1.2 AMD-APP (3224.4)
  Driver Version                                  3224.4
  Device OpenCL C Version                         OpenCL C 1.2 
  Device Type                                     GPU
  Device Board Name (AMD)                         AMD Radeon Graphics
  Device PCI-e ID (AMD)                           0xc749940
  Device Topology (AMD)                           PCI-E, 0000:01:00.0
  Device Profile                                  FULL_PROFILE
```
Is detected from clinfo, but rocminfo give me only CPU no GPU.
```
rocminfo 
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
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
  Max Clock Freq. (MHz):   4000                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16270300(0xf843dc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16270300(0xf843dc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16270300(0xf843dc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***      
```

rocm-smi report

```
======================= ROCm System Management Interface =======================
WARNING: No AMD GPUs specified
================================= Concise Info =================================
GPU  Temp  AvgPwr  SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%  
================================================================================
============================= End of ROCm SMI Log ==============================
```

Kernel module amdgpu report this:

```
[    6.382498] [drm] amdgpu kernel modesetting enabled.
[    6.382499] [drm] amdgpu version: 6.1.5
[    6.382511] amdgpu: vga_switcheroo: detected switching method \_SB_.PCI0.GFX0.ATPX handle
[    6.382709] amdgpu: CRAT table not found
[    6.382711] amdgpu: Virtual CRAT table created for CPU
[    6.382722] amdgpu: Topology: Add CPU node
[    6.388578] amdgpu 0000:01:00.0: enabling device (0006 -> 0007)
[    6.404381] amdgpu 0000:01:00.0: amdgpu: Fetched VBIOS from ATRM
[    6.404383] amdgpu: ATOM BIOS: BR42924.002
[    6.404399] kfd kfd: amdgpu: TOPAZ  not supported in kfd
[    6.404423] amdgpu 0000:01:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[    6.404425] amdgpu 0000:01:00.0: amdgpu: PCIE atomic ops is not supported
[    6.414773] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_mc.bin
[    6.414792] amdgpu 0000:01:00.0: amdgpu: VRAM: 4096M 0x000000F400000000 - 0x000000F4FFFFFFFF (4096M used)
[    6.414800] amdgpu 0000:01:00.0: amdgpu: GART: 256M 0x000000FF00000000 - 0x000000FF0FFFFFFF
[    6.414903] [drm] amdgpu: 4096M of VRAM memory ready
[    6.414908] [drm] amdgpu: 7944M of GTT memory ready.
[    6.418335] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_pfp.bin
[    6.421648] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_me.bin
[    6.424627] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_ce.bin
[    6.427659] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_rlc.bin
[    6.432214] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_mec.bin
[    6.435456] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_sdma.bin
[    6.437578] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_sdma1.bin
[    6.437651] amdgpu: [powerplay] hwmgr_sw_init smu backed is iceland_smu
[    6.440738] amdgpu 0000:01:00.0: firmware: direct-loading firmware amdgpu/topaz_smc.bin
[    6.466194] amdgpu: [powerplay] can't get the mac of 5
[    6.471844] amdgpu 0000:01:00.0: amdgpu: SE 1, SH per SE 1, CU per SH 6, active_cu_number 6
[    6.474800] amdgpu 0000:01:00.0: amdgpu: Using BOCO for runtime pm
[    6.474890] [drm] Initialized amdgpu 3.53.0 20150101 for 0000:01:00.0 on minor 1
[   62.961944] amdgpu: [powerplay] can't get the mac of 5
[  169.131872] amdgpu: [powerplay] can't get the mac of 5
[  430.550984] amdgpu: [powerplay] can't get the mac of 5
[  502.555659] amdgpu: [powerplay] can't get the mac of 5
[  571.047796] amdgpu: [powerplay] can't get the mac of 5
[  596.514162] amdgpu: [powerplay] can't get the mac of 5
[  872.787630] amdgpu: [powerplay] can't get the mac of 5
[  886.711494] amdgpu: [powerplay] can't get the mac of 5
[  900.510384] amdgpu: [powerplay] can't get the mac of 5
```

kfd is not supported is it an issue?

Is it supported my GPU on rocm, I think no, is it correct?
I tested many versions also the latest 5.6, on ubuntu 22.04 LTS, but none show the GPU.


---

## 评论 (2 条)

### 评论 #1 — PGA68 (2023-11-10T13:54:30Z)

How rollback TOPAZ from Parrot OS GRUB?

---

### 评论 #2 — nartmada (2024-02-02T04:23:01Z)

Sorry @yashikada, Iceland/Topaz is no longer supported.  For reference, you can check latest and previous version of ROCm.

Latest ROCm6.0.2
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

Links to previous version.
https://rocm.docs.amd.com/en/latest/release/versions.html


---
