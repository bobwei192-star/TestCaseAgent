# [Issue]: Instinct MI60 Fails to initialize with Ubuntu 24.04 and 22.04 Guest VMs under ESXi 8 

> **Issue #4017**
> **状态**: closed
> **创建时间**: 2024-11-07T21:16:04Z
> **更新时间**: 2025-06-18T06:36:29Z
> **关闭时间**: 2024-12-24T20:11:33Z
> **作者**: haydonryan
> **标签**: Under Investigation, ROCm 6.2.2, AMD Instinct MI60, (displays as a 32gb MI50)
> **URL**: https://github.com/ROCm/ROCm/issues/4017

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.2** (颜色: #ededed)
- **AMD Instinct MI60** (颜色: #ededed)
- **(displays as a 32gb MI50)** (颜色: #ededed)

## 描述

### Problem Description

I have a Dell R7515 32 core AMD EPYC rackmount server.  I recently bought a second hand MI60 GPU to get some experience with AMD DC GPUs (It's my first AMD GPU).  
The Dell is running  VMware ESXi, 8.0.3, 24022510 as my hypervisor, and I've tried Ubuntu 22.04 and 24.04 guest VMs.  Unfortunately the card fails to initialize under a VM.  I have also tried it on bare metal Ubuntu 22.04 (same iso) on the same machine and works fine.

[VM settings]
Reserved 32gb ram
pciPassthru.use64bitMMIO set to TRUE
pciPassthru.64bitMMIOSizeGB = 128,
secureboot = false

I have tried doing PCI Passthrough with both Dymanic DirectPathIO and regular Directpath IO.


lspci shows that the card is there
```
$ lspci
00:00.0 Host bridge: Intel Corporation 440BX/ZX/DX - 82443BX/ZX/DX Host bridge (rev 01)
00:01.0 PCI bridge: Intel Corporation 440BX/ZX/DX - 82443BX/ZX/DX AGP bridge (rev 01)
00:07.0 ISA bridge: Intel Corporation 82371AB/EB/MB PIIX4 ISA (rev 08)
00:07.1 IDE interface: Intel Corporation 82371AB/EB/MB PIIX4 IDE (rev 01)
00:07.3 Bridge: Intel Corporation 82371AB/EB/MB PIIX4 ACPI (rev 08)
00:07.7 System peripheral: VMware Virtual Machine Communication Interface (rev 10)
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
02:00.0 Serial Attached SCSI controller: VMware PVSCSI SCSI Controller (rev 02)
02:01.0 Ethernet controller: VMware VMXNET3 Ethernet Controller (rev 01)
02:02.0 SATA controller: VMware SATA AHCI controller
03:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Vega 20 [Radeon Pro VII/Radeon Instinct MI50 32GB]
```

but dmesg shows that there's failures.
```
$ sudo dmesg | grep amd
[    0.000000] Linux version 5.15.0-124-generic (buildd@lcy02-amd64-118) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #134-Ubuntu SMP Fri Sep 27 20:20:17 UTC 2024 (Ubuntu 5.15.0-124.134-generic 5.15.163)
[    4.059471] [drm] amdgpu kernel modesetting enabled.
[    4.060689] amdgpu: CRAT table not found
[    4.061819] amdgpu: Virtual CRAT table created for CPU
[    4.062712] amdgpu: Topology: Add CPU node
[    4.063968] amdgpu 0000:03:00.0: enabling device (0000 -> 0002)
[    4.067449] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[    4.077094] amdgpu 0000:03:00.0: BARt 6: can't assign [??? 0x00000000 flags 0x20000000] (bogus alignment)
[    4.119943] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from ROM
[    4.120839] amdgpu: ATOM BIOS: 113-D1630600-107
[   24.126942] [drm:atom_op_jump [amdgpu]] *ERROR* atombios stuck in loop for more than 20secs aborting
[   24.127710] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 4EC8 (len 74, WS 0, PS 8) @ 0x4EE0
[   24.128761] amdgpu 0000:03:00.0: amdgpu: gpu post error!
[   24.129239] amdgpu 0000:03:00.0: amdgpu: Fatal error during GPU init
[   24.129707] amdgpu 0000:03:00.0: amdgpu: amdgpu: finishing device.
[   24.131460] amdgpu: probe of 0000:03:00.0 failed with error -22
```

I understand these are older cards, but there are a lot of people using these and I personally got one to see how compatible things were prior to buying MUCH more expensive cards for virtualization, as it looks like only the MI210s have been tested with VMware. :(

### Operating System

Ubuntu 22/24  with esxi 8.0.3

### CPU

AMD Epyc

### GPU

AMD Instinct MI60, (displays as a 32gb MI50)

### ROCm Version

ROCm 6.2.2

### ROCm Component

_No response_

### Steps to Reproduce

Create new VM - 32gb ram, 256gb disk, directpathio passthrough of mi60.
set pciPassthru.use64bitMMIO set to TRUE
set pciPassthru.64bitMMIOSizeGB = 128,
set secureboot = false
Fresth install of server minimal Ubuntu 22.04 enable ssh access
follow instructions for 22.04 install of rocm from: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html
(side note if you run this in your home directory you get a warning that the _apt user doesn't have access, better to run it from /tmp/ where all users do have access!)
reboot.

I think there's a kernel parameter or vmware setting that needs to be set to properly align the BAR (I assume that's what I'm reading here)

I have a VM snapshot of a fresh install of ubuntu 22.04 so I can repeat these steps as needed for testing, also happy to do whatever testing is needed.


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
```
$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.8.5 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
Runtime Ext Version:     1.6
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
  Name:                    AMD EPYC 7452 32-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7452 32-Core Processor    
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
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            64                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65826428(0x3ec6e7c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65826428(0x3ec6e7c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65826428(0x3ec6e7c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             
```
### Additional Information

Running on bare metal the GPU initializes correctly:
```
$ sudo dmesg | grep amdgpu
[sudo] password for haydon: 
[    6.909392] [drm] amdgpu kernel modesetting enabled.
[    6.909639] amdgpu: Ignoring ACPI CRAT on non-APU system
[    6.909657] amdgpu: Virtual CRAT table created for CPU
[    6.909688] amdgpu: Topology: Add CPU node
[    7.064057] amdgpu 0000:c5:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[    7.151510] amdgpu 0000:c5:00.0: amdgpu: Fetched VBIOS from ROM BAR
[    7.152748] amdgpu: ATOM BIOS: 113-D1630600-107
[    7.276963] amdgpu 0000:c5:00.0: amdgpu: MEM ECC is active.
[    7.283581] amdgpu 0000:c5:00.0: amdgpu: SRAM ECC is active.
[    7.290116] amdgpu 0000:c5:00.0: amdgpu: RAS INFO: ras initialized successfully, hardware ability[7fff] ras_mask[7fff]
[    7.307903] amdgpu 0000:c5:00.0: amdgpu: VRAM: 32752M 0x0000008000000000 - 0x00000087FEFFFFFF (32752M used)
[    7.316744] amdgpu 0000:c5:00.0: amdgpu: GART: 512M 0x0000000000000000 - 0x000000001FFFFFFF
[    7.325358] amdgpu 0000:c5:00.0: amdgpu: AGP: 267878400M 0x0000008800000000 - 0x0000FFFFFFFFFFFF
[    7.354853] [drm] amdgpu: 32752M of VRAM memory ready
[    7.355978] [drm] amdgpu: 32752M of GTT memory ready.
[    7.381237] amdgpu 0000:c5:00.0: amdgpu: PSP runtime database doesn't exist
[    7.417200] amdgpu: hwmgr_sw_init smu backed is vega20_smu
[    7.735764] amdgpu 0000:c5:00.0: amdgpu: HDCP: optional hdcp ta ucode is not available
[    7.736679] amdgpu 0000:c5:00.0: amdgpu: DTM: optional dtm ta ucode is not available
[    7.737388] amdgpu 0000:c5:00.0: amdgpu: RAP: optional rap ta ucode is not available
[    7.738058] amdgpu 0000:c5:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[    8.059471] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[    8.354264] amdgpu: HMM registered 32752MB device memory
[    8.373541] amdgpu: SRAT table not found
[    8.379308] amdgpu: Virtual CRAT table created for GPU
[    8.400757] amdgpu: Topology: Add dGPU node [0x66a1:0x1002]
[    8.412093] kfd kfd: amdgpu: added device 1002:66a1
[    8.461578] amdgpu 0000:c5:00.0: amdgpu: SE 4, SH per SE 1, CU per SH 16, active_cu_number 64
[    8.480648] amdgpu 0000:c5:00.0: amdgpu: ring gfx uses VM inv eng 0 on hub 0
[    8.488733] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[    8.494434] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[    8.508736] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[    8.516575] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[    8.528760] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[    8.538282] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[    8.547216] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[    8.558412] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[    8.565479] amdgpu 0000:c5:00.0: amdgpu: ring kiq_2.1.0 uses VM inv eng 11 on hub 0
[    8.576903] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 0 on hub 1
[    8.584194] amdgpu 0000:c5:00.0: amdgpu: ring page0 uses VM inv eng 1 on hub 1
[    8.596738] amdgpu 0000:c5:00.0: amdgpu: ring sdma1 uses VM inv eng 4 on hub 1
[    8.603145] amdgpu 0000:c5:00.0: amdgpu: ring page1 uses VM inv eng 5 on hub 1
[    8.615585] amdgpu 0000:c5:00.0: amdgpu: ring uvd_0 uses VM inv eng 6 on hub 1
[    8.622202] amdgpu 0000:c5:00.0: amdgpu: ring uvd_enc_0.0 uses VM inv eng 7 on hub 1
[    8.632733] amdgpu 0000:c5:00.0: amdgpu: ring uvd_enc_0.1 uses VM inv eng 8 on hub 1
[    8.639847] amdgpu 0000:c5:00.0: amdgpu: ring uvd_1 uses VM inv eng 9 on hub 1
[    8.650621] amdgpu 0000:c5:00.0: amdgpu: ring uvd_enc_1.0 uses VM inv eng 10 on hub 1
[    8.659124] amdgpu 0000:c5:00.0: amdgpu: ring uvd_enc_1.1 uses VM inv eng 11 on hub 1
[    8.668217] amdgpu 0000:c5:00.0: amdgpu: ring vce0 uses VM inv eng 12 on hub 1
[    8.677994] amdgpu 0000:c5:00.0: amdgpu: ring vce1 uses VM inv eng 13 on hub 1
[    8.685370] amdgpu 0000:c5:00.0: amdgpu: ring vce2 uses VM inv eng 14 on hub 1
[    8.732550] amdgpu: Detected AMDGPU DF Counters. # of Counters = 8.
[    8.733494] amdgpu: Detected AMDGPU 2 Perf Events.
[    8.751269] [drm] Initialized amdgpu 3.42.0 20150101 for 0000:c5:00.0 on minor 1
```




---

## 评论 (9 条)

### 评论 #1 — ppanchad-amd (2024-11-11T17:46:49Z)

Hi @haydonryan. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — haydonryan (2024-12-10T00:21:24Z)

It's been a month.  Any follow up?

---

### 评论 #3 — jamesxu2 (2024-12-10T22:19:00Z)

Hi @haydonryan, apologies for the delayed response. Like you've said:

>  it looks like only the MI210s have been tested with VMware

This is the case currently as you've likely seen in [our system requirements](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#virtualization-support). Virtualization is a complex usecase that users have asked for, and AMD is working to improve, but our support for it is unfortunately limited at the moment. 

On top of that, general ROCm support for the MI50 has been [deprecated](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus), so you will likely run into more problems in the future if you try to use it with the latest ROCm release. 

That said, I apologize that this is your first experience with an AMD GPU, I know it is a frustrating experience to hear that we've dropped support for a device. I'll try to reproduce the issue internally to assess its magnitude/resolvability and keep you updated on that.

---

### 评论 #4 — jamesxu2 (2024-12-24T20:11:33Z)

Hi @haydonryan, so unfortunately I don't think we've ever supported the virtualization usecase for MI50 and developing those codepaths / validating on that hardware is not planned at the moment. 

Additionally, I see a note in the ROCm 5.6.0 release notes that [MI50 ROCm support has effectively reached EOL](https://rocm.docs.amd.com/en/docs-5.6.0/release.html#os-and-gpu-support-changes) at this point so you shouldn't expect further updates to support that hardware. 

I am sorry about this, but it looks like virtualization is one of those usecases where a significant amount of work needs to be done in firmware and kernel driver and that's just not planned for the MI50 generation of cards. 

---

### 评论 #5 — haydonryan (2024-12-24T20:28:47Z)

Very disappointing :(

Also for what it's worth i have a Mi60 not Mi50

---

### 评论 #6 — jamesxu2 (2024-12-24T20:33:13Z)

@haydonryan MI50 and MI60 are effectively the same, support-wise. I am sorry to disappoint but this is unfortunately the state of ROCm at the moment.

---

### 评论 #7 — haydonryan (2025-01-26T18:17:23Z)

Ok so the only card that supports VMware is an $9,000 card. Not worth it, Bummer.

---

### 评论 #8 — nkuhn-vmw (2025-04-09T14:39:51Z)

@jamesxu2 any idea if a MI100 would work?

---

### 评论 #9 — Outhawk (2025-06-18T06:36:29Z)

@jamesxu2 Hello James seems like you are a expert with that card. Hope you can maybe help me. Its not possible for me to modify the Bios and flash it to the card because of signiture missmatch. I can do some editing with the driver´s (Voltage etc.) but would prefer it at the card. Im really happy that you are the first person and expert who says that the cards are similar. I figure that out some month ago but most people dont belive that. ^^

---
