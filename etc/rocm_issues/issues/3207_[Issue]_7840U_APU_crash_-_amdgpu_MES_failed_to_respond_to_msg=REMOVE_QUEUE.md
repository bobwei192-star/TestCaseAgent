# [Issue]: 7840U APU crash - amdgpu: MES failed to respond to msg=REMOVE_QUEUE

> **Issue #3207**
> **状态**: closed
> **创建时间**: 2024-05-31T15:26:18Z
> **更新时间**: 2026-01-10T19:33:00Z
> **关闭时间**: 2024-06-21T20:26:38Z
> **作者**: jrl290
> **标签**: ROCm 5.7.1, AMD Radeon VII, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3207

## 标签

- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Ubuntu 24.04 - Kernel 6.1 rc1
Rocm Version - 6.1.1
PyTorch Version - 2.4.0.dev20240529+rocm6.1

export PYTORCH_ROCM_ARCH="gfx1100"
export HSA_OVERRIDE_GFX_VERSION=11.0.0

Run a pytorch inference on repeat and reset the GPU after each one. Crash happens randomly and freezes/kills the process, including any subsequent python instructions

Also tried Ubuntu 24.1 and 22.04, also Rocm 5.7
No problems with 6800u apu

dmesg before and after GPU reset
```
[40802.818692] amdgpu 0000:c3:00.0: amdgpu: GPU reset(24) succeeded!
[40869.919369] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[40869.919380] amdgpu 0000:c3:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[40869.919384] amdgpu 0000:c3:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[40869.919386] amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 1
[40869.919389] amdgpu: Failed to evict process queues
[40869.919406] amdgpu 0000:c3:00.0: amdgpu: GPU recovery disabled.
[40869.921734] amdgpu 0000:c3:00.0: amdgpu: Failed to restore queue 2
[40869.921739] amdgpu: Failed to restore process queues
[40886.771569] amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!
[40887.964053] amdgpu 0000:c3:00.0: amdgpu: Failed to remove queue 2
[40887.964064] amdgpu 0000:c3:00.0: amdgpu: Failed to remove queue 0
[40887.974318] workqueue: kfd_process_wq_release [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
[40890.791490] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[40890.791496] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[40891.984627] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER)
[40891.984631] [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
[40894.813029] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[40894.813037] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[40894.814738] amdgpu 0000:c3:00.0: amdgpu: MODE2 reset
[40894.847959] amdgpu 0000:c3:00.0: amdgpu: GPU reset succeeded, trying to resume
[40894.848676] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[40894.848764] amdgpu 0000:c3:00.0: amdgpu: SMU is resuming...
[40894.851361] amdgpu 0000:c3:00.0: amdgpu: SMU is resumed successfully!
[40894.853700] [drm] DMUB hardware initialized: version=0x08003300
[40894.855387] [drm] kiq ring mec 3 pipe 1 q 0
[40894.857912] amdgpu 0000:c3:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[40894.858596] amdgpu 0000:c3:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[40894.858600] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[40894.858602] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[40894.858604] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[40894.858607] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[40894.858609] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[40894.858610] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[40894.858613] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[40894.858615] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[40894.858617] amdgpu 0000:c3:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[40894.858619] amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[40894.858621] amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[40894.858623] amdgpu 0000:c3:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[40894.860509] amdgpu 0000:c3:00.0: amdgpu: recover vram bo from shadow start
[40894.860511] amdgpu 0000:c3:00.0: amdgpu: recover vram bo from shadow done
[40894.860541] amdgpu 0000:c3:00.0: amdgpu: GPU reset(25) succeeded!
```

(During crash)
```
minipc@minipc-Mercury-series:~/aipython$ /opt/rocm/bin/rocm-smi -a


============================ ROCm System Management Interface ============================
============================== Version of System Component ===============================
Driver version: 6.10.0-061000rc1-generic
==========================================================================================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		Phoenix1
GPU[0]		: Device ID: 		0x15bf
GPU[0]		: Device Rev: 		0xc9
GPU[0]		: Subsystem ID: 	Radeon HD 6470M
GPU[0]		: GUID: 		4765
==========================================================================================
======================================= Unique ID ========================================
GPU[0]		: Unique ID: N/A
==========================================================================================
========================================= VBIOS ==========================================
GPU[0]		: VBIOS version: 113-PHXGENERIC-001
==========================================================================================
====================================== Temperature =======================================
GPU[0]		: Temperature (Sensor edge) (C): 55.0
==========================================================================================
=============================== Current clock frequencies ================================
GPU[0]		: fclk clock level: 2: (1200Mhz)
GPU[0]		: mclk clock level: 1: (800Mhz)
GPU[0]		: sclk clock level: 1: (1798Mhz)
GPU[0]		: socclk clock level: 4: (900Mhz)
==========================================================================================
=================================== Current Fan Metric ===================================
GPU[0]		: Not supported
==========================================================================================
================================= Show Performance Level =================================
GPU[0]		: Performance Level: auto
==========================================================================================
==================================== OverDrive Level =====================================
GPU[0]		: get_overdrive_level_sclk, Not supported on the given system
==========================================================================================
==================================== OverDrive Level =====================================
GPU[0]		: get_mem_overdrive_level_mclk, Not supported on the given system
==========================================================================================
======================================= Power Cap ========================================
GPU[0]		: get_power_cap, Not supported on the given system
GPU[0]		: Max Graphics Package Power Unsupported
==========================================================================================
================================== Show Power Profiles ===================================
GPU[0]		: get_power_profiles, Not supported on the given system
==========================================================================================
=================================== Power Consumption ====================================
GPU[0]		: Current Socket Graphics Package Power (W): 15.171
==========================================================================================
============================== Supported clock frequencies ===============================
GPU[0]		: Clock [dcefclk] on device [0] exists but EMPTY! Likely driver error!
GPU[0]		: Supported fclk frequencies on GPU0
GPU[0]		: 0: 400Mhz
GPU[0]		: 1: 800Mhz
GPU[0]		: 2: 1200Mhz *
GPU[0]		: 3: 1600Mhz
GPU[0]		: 
GPU[0]		: Supported mclk frequencies on GPU0
GPU[0]		: 0: 400Mhz
GPU[0]		: 1: 800Mhz *
GPU[0]		: 2: 800Mhz
GPU[0]		: 3: 800Mhz
GPU[0]		: 
GPU[0]		: Supported sclk frequencies on GPU0
GPU[0]		: 0: 800Mhz
GPU[0]		: 1: 1798Mhz *
GPU[0]		: 2: 2700Mhz
GPU[0]		: 
GPU[0]		: Supported socclk frequencies on GPU0
GPU[0]		: 0: 400Mhz
GPU[0]		: 1: 600Mhz
GPU[0]		: 2: 720Mhz
GPU[0]		: 3: 800Mhz
GPU[0]		: 4: 900Mhz *
GPU[0]		: 5: 1028Mhz
GPU[0]		: 6: 1028Mhz
GPU[0]		: 7: 1200Mhz
GPU[0]		: 
------------------------------------------------------------------------------------------
==========================================================================================
=================================== % time GPU is busy ===================================
GPU[0]		: GPU use (%): 99
==========================================================================================
=================================== Current Memory Use ===================================
GPU[0]		: % memory use, Not supported on the given system
GPU[0]		: Memory Activity: N/A
GPU[0]		: Not supported on the given system
==========================================================================================
===================================== Memory Vendor ======================================
GPU[0]		: get_vram_vendor, Not supported on the given system
==========================================================================================
================================== PCIe Replay Counter ===================================
GPU[0]		: PCIe Replay Count: 0
==========================================================================================
===================================== Serial Number ======================================
GPU[0]		: get_serial_number, Not supported on the given system
GPU[0]		: Serial Number: N/A
==========================================================================================
===================================== KFD Processes ======================================
KFD process information:
PID  	PROCESS NAME  	GPU(s)	VRAM USED 	SDMA USED	CU OCCUPANCY	
16943	pt_main_thread	1     	1544712192	0        	UNKNOWN     	
==========================================================================================
================================== GPUs Indexed by PID ===================================
PID 16943 is using 1 DRM device(s):
0 
==========================================================================================
======================= GPU Memory clock frequencies and voltages ========================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
==========================================================================================
==================================== Current voltage =====================================
GPU[0]		: Voltage (mV): 944
==========================================================================================
======================================= PCI Bus ID =======================================
GPU[0]		: PCI Bus: 0000:C3:00.0
==========================================================================================
================================== Firmware Information ==================================
GPU[0]		: ASD firmware version: 	0x210000c7
GPU[0]		: get_firmware_version_CE, Not supported on the given system
GPU[0]		: get_firmware_version_DMCU, Not supported on the given system
GPU[0]		: get_firmware_version_MC, Not supported on the given system
GPU[0]		: ME firmware version: 		39
GPU[0]		: MEC firmware version: 	35
GPU[0]		: get_firmware_version_MEC2, Not supported on the given system
GPU[0]		: MES firmware version: 	0x00000052
GPU[0]		: MES KIQ firmware version: 	0x00000073
GPU[0]		: PFP firmware version: 	47
GPU[0]		: RLC firmware version: 	127
GPU[0]		: get_firmware_version_RLC SRLC, Not supported on the given system
GPU[0]		: get_firmware_version_RLC SRLG, Not supported on the given system
GPU[0]		: get_firmware_version_RLC SRLS, Not supported on the given system
GPU[0]		: SDMA firmware version: 	16
GPU[0]		: get_firmware_version_SDMA2, Not supported on the given system
GPU[0]		: SMC firmware version: 	00.76.65.00
GPU[0]		: get_firmware_version_SOS, Not supported on the given system
GPU[0]		: get_firmware_version_TA RAS, Not supported on the given system
GPU[0]		: get_firmware_version_TA XGMI, Not supported on the given system
GPU[0]		: get_firmware_version_UVD, Not supported on the given system
GPU[0]		: get_firmware_version_VCE, Not supported on the given system
GPU[0]		: VCN firmware version: 	0x07113000
==========================================================================================
====================================== Product Info ======================================
GPU[0]		: Card Series: 		Phoenix1
GPU[0]		: Card Model: 		0x15bf
GPU[0]		: Card Vendor: 		Advanced Micro Devices, Inc. [AMD/ATI]
GPU[0]		: Card SKU: 		PHXGENERIC
GPU[0]		: Subsystem ID: 	Radeon HD 6470M
GPU[0]		: Device Rev: 		0xc9
GPU[0]		: Node ID: 		1
GPU[0]		: GUID: 		4765
GPU[0]		: GFX Version: 		gfx11003
==========================================================================================
======================================= Pages Info =======================================
GPU[0]		: ras, Not supported on the given system
================================= Show Valid sclk Range ==================================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
==========================================================================================
================================= Show Valid mclk Range ==================================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
==========================================================================================
================================ Show Valid voltage Range ================================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
==========================================================================================
================================== Voltage Curve Points ==================================
GPU[0]		: get_od_volt_info, Requested function is not implemented on this setup
ERROR: GPU[0]	: Voltage curve Points unsupported.
==========================================================================================
==================================== Consumed Energy =====================================
GPU[0]		: % Energy Counter, Unexpected data received
==========================================================================================
=============================== Current Compute Partition ================================
GPU[0]		: Not supported on the given system
==========================================================================================
================================ Current Memory Partition ================================
GPU[0]		: Not supported on the given system
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

```
minipc@minipc-Mercury-series:~/aipython$ hipconfig
HIP version  : 6.1.40092-038397aaa

== hipconfig
HIP_PATH     : /opt/rocm-6.1.1
ROCM_PATH    : /opt/rocm-6.1.1
HIP_COMPILER : clang
HIP_PLATFORM : amd
HIP_RUNTIME  : rocclr
CPP_CONFIG   :  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.1.1/include -I/opt/rocm-6.1.1/lib/llvm/lib/clang/17
 

== hip-clang
HIP_CLANG_PATH   : /opt/rocm-6.1.1/llvm/bin
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.1 24154 f53cd7e03908085f4932f7329464cd446426436a)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.1.1/llvm/bin
Configuration file: /opt/rocm-6.1.1/lib/llvm/bin/clang++.cfg
AMD LLVM version 17.0.0git
  Optimized build.
  Default target: x86_64-unknown-linux-gnu
  Host CPU: znver4

  Registered Targets:
    amdgcn - AMD GCN GPUs
    r600   - AMD GPUs HD2XXX-HD6XXX
    x86    - 32-bit X86: Pentium-Pro and above
    x86-64 - 64-bit X86: EM64T and AMD64
hip-clang-cxxflags :  -isystem "/opt/rocm-6.1.1/include" -O3
hip-clang-ldflags  : --driver-mode=g++ -O3 --hip-link --rtlib=compiler-rt -unwindlib=libgcc

=== Environment Variables
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

== Linux Kernel
Hostname     : minipc-Mercury-series
Linux minipc-Mercury-series 6.10.0-061000rc1-generic #202405262234 SMP PREEMPT_DYNAMIC Sun May 26 22:46:25 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04 LTS
Release:	24.04
Codename:	noble
```

```
minipc@minipc-Mercury-series:~/aipython$ rocminfo
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.13
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
  Name:                    AMD Ryzen 7 7840U w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7840U w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5132                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    31546376(0x1e15c08) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31546376(0x1e15c08) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31546376(0x1e15c08) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1103                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           9(0x9)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   49920                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
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
  Packet Processor uCode:: 35                                 
  SDMA engine uCode::      16                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15773188(0xf0ae04) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15773188(0xf0ae04) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1103         
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
```

### Operating System

Ubuntu 24.04 LTS (Noble Numbat)

### CPU

AMD Ryzen 7 7840U w/ Radeon 780M Graphics

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.1.0, ROCm 5.7.1

### ROCm Component

amdsmi, ROCm

### Steps to Reproduce

export PYTORCH_ROCM_ARCH="gfx1100"
export HSA_OVERRIDE_GFX_VERSION=11.0.0

Run a pytorch inference on repeat and reset the GPU after each one. Crash happens randomly

Also tried Ubuntu 24.1 and 22.04, also Rocm 5.7
No problems with 6800u apu

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — woachk (2024-06-01T03:01:42Z)

I think you'd rather want:

```
export PYTORCH_ROCM_ARCH="gfx1102"
export HSA_OVERRIDE_GFX_VERSION=11.0.2
```

because the APUs seem to have a reduced register file like Navi33

---

### 评论 #2 — jrl290 (2024-06-01T12:02:09Z)

> I think you'd rather want:
> 
> ```
> export PYTORCH_ROCM_ARCH="gfx1102"
> export HSA_OVERRIDE_GFX_VERSION=11.0.2
> ```
> 
> because the APUs seem to have a reduced register file like Navi33

Thank you for your suggestion. Unfortunately I get this error with those variables
``` 
File "/home/minipc/python-env/lib/python3.12/site-packages/torch/nn/modules/conv.py", line 456, in _conv_forward
    return F.conv2d(input, weight, bias, self.stride,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

Probably should include the PyTorch version:
```
(python-env) minipc@minipc-Mercury-series:~/aipython$ python -c "import torch; print(torch.__version__)"
2.4.0.dev20240529+rocm6.1
```

Any ideas?

---

### 评论 #3 — woachk (2024-06-01T18:03:55Z)

This means that your ROCm + PyTorch builds you have were not built with Navi33 support...

---

### 评论 #4 — jrl290 (2024-06-01T18:47:56Z)

> This means that your ROCm + PyTorch builds you have were not built with Navi33 support...

I'll certainly take your knowledge over my own. I just assumed that F.conv2d would be pretty basic and "invalid device function" would put it on the device driver side. I'll make a post on PyTorch github

Thank you again for your insight

---

### 评论 #5 — ppanchad-amd (2024-06-21T19:59:08Z)

@jrl290 Please confirm if we can close this ticket. Thanks!

---

### 评论 #6 — jeremielec (2026-01-10T19:33:00Z)

Note for anyone who are impacted by similar problem : for my case,  running on an 780M, and suffer of lot of GPU reset (message was the same)

How over, despite the 96gb ram available (86Gb on GTT and used as reported by radeontop), 1gb was allocated on VRAM in the bios. Increasing this one to 4gb on the bios has solved the issue.

---
