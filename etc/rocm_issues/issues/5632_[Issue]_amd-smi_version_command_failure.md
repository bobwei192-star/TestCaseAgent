# [Issue]: amd-smi version command failure

> **Issue #5632**
> **状态**: closed
> **创建时间**: 2025-11-06T07:23:10Z
> **更新时间**: 2025-12-09T19:46:45Z
> **关闭时间**: 2025-12-08T16:29:32Z
> **作者**: PaoloJr
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5632

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

`amd-smi version` command fails. Here is the output:

```
/usr/include/c++/15/bits/stl_vector.h:1263: std::vector<_Tp, _Alloc>::reference std::vector<_Tp, _Alloc>::operator[](size_type) [with _Tp = void*; _Alloc = std::allocator<void*>; reference = void*&; size_type = long unsigned int]: Assertion '__n < this->size()' failed.
Aborted                    (core dumped) amd-smi version
```

### Operating System

Fedora 43 Sway (Spin)

### CPU

AMD Ryzen 5 5600

### GPU

AMD Radeon 7900 XTX

### ROCm Version

ROCm 6.4.4

### ROCm Component

amdsmi

### Steps to Reproduce

_some context_

after running a jupyter notebook and noticed that (VRAM) resources would not release after notebook shutdown. The `ipykernel` process is stuck in `D` state (uninterruptible), a system reboot is the only way to force the VRAM to clear. Restarting this same workflow would still "freeze" during the training run in the notebook, and the resources would not clear. Restarting the notebook session would spawn a new process occupying more VRAM. 

I have switched between linux kernel 6.17.6 and 6.17.5 to no avail.  Also tried version 6.17.1 and it seems to work more consistantly with the notebook's machine learning workload. There is a mention [here](https://github.com/ollama/ollama/issues/12893#issuecomment-3478001431), albeit for `ollama`, but the experienced issue feels the same

Happy to run more tests if need be.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_note_
installed the `rocm` metapackage as recommended from [fedora packagers](https://fedoraproject.org/wiki/SIGs/HC)

output from `rocminfo`:
```
[37mROCk module is loaded[0m
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.7
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
  Name:                    AMD Ryzen 5 5600 6-Core Processor  
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5600 6-Core Processor  
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
  Max Clock Freq. (MHz):   4470                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32771056(0x1f40bf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32771056(0x1f40bf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32771056(0x1f40bf0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32771056(0x1f40bf0) KB             
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
  Uuid:                    GPU-1fb8a6a50ca222e3               
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
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2304                               
  BDFID:                   11264                              
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 602                                
  SDMA engine uCode::      27                                 
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***             

```

### Additional Information

the recommended system-information commands output the following:
```
OS:
NAME="Fedora Linux"
VERSION="43 (Sway)"
CPU:
model name      : AMD Ryzen 5 5600 6-Core Processor
GPU:
bash: /opt/rocm/bin/rocminfo: No such file or directory
```

for the GPU (which did not display any information), here is output, if it helps, from `amd-smi firmware`:
```
amd-smi firmware
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_PFP
            FW_VERSION: 2580
        FW 1:
            FW_ID: CP_ME
            FW_VERSION: 2420
        FW 2:
            FW_ID: CP_MEC1
            FW_VERSION: 2650
        FW 3:
            FW_ID: RLC
            FW_VERSION: 128
        FW 4:
            FW_ID: SDMA0
            FW_VERSION: 27
        FW 5:
            FW_ID: SDMA1
            FW_VERSION: 27
        FW 6:
            FW_ID: VCN
            FW_VERSION: 09.11.80.16
        FW 7:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.31.00.35
        FW 8:
            FW_ID: ASD
            FW_VERSION: 553648378
        FW 9:
            FW_ID: TA_RAS
            FW_VERSION: 1B.00.02.05
        FW 10:
            FW_ID: PM
            FW_VERSION: 00.78.130.00
```


output from `lspci -k`:
```
2c:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 31 [Radeon RX 7900 XT/7900 XTX/7900 GRE/7900M] (rev c8)
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] RX 7900 XTX / RX 7900 GRE [XFX]
        Kernel driver in use: amdgpu
        Kernel modules: amdgpu
```

recent output from `dmesg | grep -i amdgpu`:
```
[Thu Nov  6 01:38:46 2025] [drm] amdgpu kernel modesetting enabled.
[Thu Nov  6 01:38:46 2025] amdgpu: Virtual CRAT table created for CPU
[Thu Nov  6 01:38:46 2025] amdgpu: Topology: Add CPU node
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x744C 0x1002:0x0E3B 0xC8).
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: register mmio base: 0xEEC00000
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: register mmio size: 1048576
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 0 <soc21_common>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 1 <gmc_v11_0>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 2 <ih_v6_0>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 3 <psp>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 4 <smu>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 5 <dm>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 6 <gfx_v11_0>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 7 <sdma_v6_0>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 8 <vcn_v4_0>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: detected ip block number 10 <mes_v11_0>
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: No more image in the PCI ROM
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: Fetched VBIOS from ROM BAR
[Thu Nov  6 01:38:46 2025] amdgpu: ATOM BIOS: 113-D7020100-102
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: CP RS64 enable
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: vgaarb: deactivate vga console
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: MEM ECC is not presented.
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: SRAM ECC is not presented.
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: VRAM: 24560M 0x0000008000000000 - 0x00000085FEFFFFFF (24560M used)
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: amdgpu: 24560M of VRAM memory ready
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: amdgpu: 16001M of GTT memory ready.
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x07002F00
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 22
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 22
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: RAP: optional rap ta ucode is not available
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8200 (78.130.0)
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: SMU driver if version not matched
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: SMU is initialized successfully!
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] Display Core v3.2.340 initialized on DCN 3.2
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002F00
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Thu Nov  6 01:38:46 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Thu Nov  6 01:38:47 2025] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[Thu Nov  6 01:38:47 2025] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[Thu Nov  6 01:38:47 2025] amdgpu: Virtual CRAT table created for GPU
[Thu Nov  6 01:38:47 2025] amdgpu: Topology: Add dGPU node [0x744c:0x1002]
[Thu Nov  6 01:38:47 2025] kfd kfd: amdgpu: added device 1002:744c
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: SE 6, SH per SE 2, CU per SH 8, active_cu_number 96
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: amdgpu: Using BAMACO for runtime pm
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: [drm] Registered 4 planes with drm panic
[Thu Nov  6 01:38:47 2025] [drm] Initialized amdgpu 3.64.0 for 0000:2c:00.0 on minor 1
[Thu Nov  6 01:38:47 2025] fbcon: amdgpudrmfb (fb0) is primary device
[Thu Nov  6 01:38:47 2025] amdgpu 0000:2c:00.0: [drm] fb0: amdgpudrmfb frame buffer device
[Thu Nov  6 01:38:57 2025] snd_hda_intel 0000:2c:00.1: bound 0000:2c:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
[Thu Nov  6 01:39:09 2025] [drm:amdgpu_job_submit [amdgpu]] *ERROR* Trying to push to a killed entity
[Thu Nov  6 01:39:12 2025] [drm:amdgpu_job_submit [amdgpu]] *ERROR* Trying to push to a killed entity
```

---

## 评论 (3 条)

### 评论 #1 — darren-amd (2025-11-27T21:57:08Z)

Hi @PaoloJr,

Is this issue only present after you run your workload where you observe that the VRAM is not being freed from the notebook? Would you mind trying on the latest ROCm and seeing if the issue persists? Thanks!

---

### 评论 #2 — darren-amd (2025-12-08T16:29:32Z)

I'm going to close this issue out due to inactivity, but please feel free to create another ticket if the issue persists, thanks!

---

### 评论 #3 — PaoloJr (2025-12-09T19:46:45Z)

@darren-amd apologies for the delay.
i just tested the same workflow (basic ML training), with an updated kernel (6.17.9) and clearing the GPU memory appears to function properly from the juptyter notebook. I did not update the `rocm` meta-package (for `fedora`)

```
# output from `uname -r`
6.17.9-300.fc43.x86_64
```

i noticed a difference in the firmware versions here
```
# output from `amd-smi firmware`
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_PFP
            FW_VERSION: 2580
        FW 1:
            FW_ID: CP_ME
            FW_VERSION: 2420
        FW 2:
            FW_ID: CP_MEC1
            FW_VERSION: 2650
        FW 3:
            FW_ID: RLC
            FW_VERSION: 128
        FW 4:
            FW_ID: SDMA0
            FW_VERSION: 27
        FW 5:
            FW_ID: SDMA1
            FW_VERSION: 27
        FW 6:
            FW_ID: VCN
            FW_VERSION: 09.11.80.1B
        FW 7:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.31.00.35
        FW 8:
            FW_ID: ASD
            FW_VERSION: 553648388
        FW 9:
            FW_ID: TA_RAS
            FW_VERSION: 1B.00.02.05
        FW 10:
            FW_ID: PM
            FW_VERSION: 00.78.131.00
```

there are no error messages from ` dmesg | grep -i amdgpu` as initially noted in this issue.

`amd-smi version` still outputs this error:
```
/usr/include/c++/15/bits/stl_vector.h:1263: std::vector<_Tp, _Alloc>::reference std::vector<_Tp, _Alloc>::operator[](size_type) [with _Tp = void*; _Alloc = std::allocator<void*>; reference = void*&; size_type = long unsigned int]: Assertion '__n < this->size()' failed.
zsh: IOT instruction (core dumped)  amd-smi version
```

for this last point, i will update `rocm` using the `fedora rawhide` repo.

many thanks!

---
