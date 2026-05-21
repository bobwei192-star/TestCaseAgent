# [Issue]: Error -22

> **Issue #4533**
> **状态**: closed
> **创建时间**: 2025-03-26T14:32:41Z
> **更新时间**: 2025-03-27T15:09:24Z
> **关闭时间**: 2025-03-27T15:01:32Z
> **作者**: ognjen011
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4533

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am running ubuntu 24.04 lts 
OS:
NAME="Ubuntu"
VERSION="24.04.2 LTS (Noble Numbat)"
With AMD cpu 
CPU: 
model name	: AMD EPYC 7313 16-Core Processor

rocm driver installed  but gpus are not seen by the os always the same error 


dmesg  | grep e3:00.0
[    6.581503] pci 0000:e3:00.0: [1002:738c] type 00 class 0x038000 PCIe Legacy Endpoint
[    6.581541] pci 0000:e3:00.0: BAR 0 [mem 0x4f800000000-0x4ffffffffff 64bit pref]
[    6.581566] pci 0000:e3:00.0: BAR 2 [mem 0x50000000000-0x500001fffff 64bit pref]
[    6.581582] pci 0000:e3:00.0: BAR 4 [io  0xf000-0xf0ff]
[    6.581598] pci 0000:e3:00.0: BAR 5 [mem 0xc2200000-0xc227ffff]
[    6.581613] pci 0000:e3:00.0: ROM [mem 0xc2280000-0xc229ffff pref]
[    6.581808] pci 0000:e3:00.0: PME# supported from D1 D2 D3hot D3cold
[    6.687727] pci 0000:e3:00.0: Adding to iommu group 89
[   51.820381] amdgpu 0000:e3:00.0: enabling device (0000 -> 0003)
[   51.829903] amdgpu 0000:e3:00.0: amdgpu: Fetched VBIOS from platform
[   51.831796] amdgpu 0000:e3:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[   71.836015] amdgpu 0000:e3:00.0: amdgpu: gpu post error!
[   71.836341] amdgpu 0000:e3:00.0: amdgpu: Fatal error during GPU init
[   71.853942] amdgpu 0000:e3:00.0: amdgpu: amdgpu: finishing device.
[   71.871281] amdgpu: probe of 0000:e3:00.0 failed with error -22

    WARNING: No AMD GPUs specified
    ===================================== ROCm System Management Interface       =====================================
    =============================================== Concise Info  ===============================================
    Device  Node  IDs           Temp    Power  Partitions          SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,  GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                  
         ============================================================================================. ================
                    ============================================================================================================
      =========================================== End of ROCm SMI Log  ============================================

installed packages 

```
dpkg -l | grep rocm
ii  rocm                                 6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) software stack meta package
ii  rocm-cmake                           0.14.0.60303-74~24.04                   amd64        rocm-cmake built using CMake
ii  rocm-core                            6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-dbgapi                          0.77.0.60303-74~24.04                   amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent                     2.0.3.60303-74~24.04                    amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-dev                             6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-developer-tools                 6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                     1.0.0.60303-74~24.04                    amd64        Radeon Open Compute - device libraries
ii  rocm-gdb                             15.2.60303-74~24.04                     amd64        ROCgdb
ii  rocm-hip-libraries                   6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime                     6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev                 6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-sdk                         6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime                6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm                            18.0.0.25012.60303-74~24.04             amd64        ROCm core compiler
ii  rocm-ml-libraries                    6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ml-sdk                          6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl                          2.0.0.60303-74~24.04                    amd64        clr built using CMake
ii  rocm-opencl-dev                      2.0.0.60303-74~24.04                    amd64        clr built using CMake
ii  rocm-opencl-runtime                  6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl-sdk                      6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp-sdk                      6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
ii  rocm-smi-lib                         7.4.0.60303-74~24.04                    amd64        AMD System Management libraries
ii  rocm-utils                           6.3.3.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocminfo                             1.0.0.60303-74~24.04                    amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool

```


### Operating System

Ubuntu 24.04 LTS

### CPU

AMD EPYC 7313 

### GPU

AMD MI100 Instinct

### ROCm Version

rocm 6.3.3

### ROCm Component

_No response_

### Steps to Reproduce

clean ubuntu install than follow install instructions from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — harkgill-amd (2025-03-26T15:13:45Z)

Hey @ognjen011, could you please
1. Provide the complete `dmesg` and `sudo dkms` output
2. Provide the Linux kernel version
3. Try to manually load the amdgpu module with `sudo modprobe amdgpu`

---

### 评论 #2 — ognjen011 (2025-03-26T15:33:41Z)

Hi 

1. dkms status
amdgpu/6.10.5-2119913.24.04, 6.8.0-55-generic, x86_64: installed

`    0.000000] Command line: BOOT_IMAGE=/vmlinuz-6.8.0-55-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro amd_iommu=on iommu=pt idle=poll hugepagesz=2M hugepages=8192 amdgpu.noretry=0
[    2.073215] Kernel command line: BOOT_IMAGE=/vmlinuz-6.8.0-55-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro amd_iommu=on iommu=pt idle=poll hugepagesz=2M hugepages=8192 amdgpu.noretry=0
[   11.423005] [drm] amdgpu kernel modesetting enabled.
[   11.424779] [drm] amdgpu version: 6.10.5
[   11.428040] amdgpu: Virtual CRAT table created for CPU
[   11.428517] amdgpu: Topology: Add CPU node
[   11.480788] amdgpu 0000:43:00.0: enabling device (0000 -> 0003)
[   11.486663] amdgpu 0000:43:00.0: amdgpu: Fetched VBIOS from platform
[   11.486985] amdgpu: ATOM BIOS: 113-D3431401-100
[   11.488801] amdgpu 0000:43:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[   31.489889] [drm:atom_op_jump [amdgpu]] *ERROR* atombios stuck in loop for more than 20secs aborting
[   31.491021] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 0484 (len 110, WS 12, PS 8) @ 0x04E9
[   31.492132] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 040A (len 45, WS 0, PS 8) @ 0x042B
[   31.493242] amdgpu 0000:43:00.0: amdgpu: gpu post error!
[   31.493620] amdgpu 0000:43:00.0: amdgpu: Fatal error during GPU init
[   31.527753] amdgpu 0000:43:00.0: amdgpu: amdgpu: finishing device.
[   31.545013] amdgpu: probe of 0000:43:00.0 failed with error -22
[   31.547253] amdgpu 0000:03:00.0: enabling device (0000 -> 0003)
[   31.554906] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from platform
[   31.555300] amdgpu: ATOM BIOS: 113-D3431401-100
[   31.556902] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[   51.557889] [drm:atom_op_jump [amdgpu]] *ERROR* atombios stuck in loop for more than 20secs aborting
[   51.559055] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 0484 (len 110, WS 12, PS 8) @ 0x04E9
[   51.560181] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 040A (len 45, WS 0, PS 8) @ 0x042B
[   51.561276] amdgpu 0000:03:00.0: amdgpu: gpu post error!
[   51.561646] amdgpu 0000:03:00.0: amdgpu: Fatal error during GPU init
[   51.579536] amdgpu 0000:03:00.0: amdgpu: amdgpu: finishing device.
[   51.597472] amdgpu: probe of 0000:03:00.0 failed with error -22
[   51.600928] amdgpu 0000:e3:00.0: enabling device (0000 -> 0003)
[   51.609144] amdgpu 0000:e3:00.0: amdgpu: Fetched VBIOS from platform
[   51.609469] amdgpu: ATOM BIOS: 113-D3431401-100
[   51.611022] amdgpu 0000:e3:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[   71.611892] [drm:atom_op_jump [amdgpu]] *ERROR* atombios stuck in loop for more than 20secs aborting
[   71.613409] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 0484 (len 110, WS 12, PS 8) @ 0x04E9
[   71.614440] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 040A (len 45, WS 0, PS 8) @ 0x042B
[   71.615452] amdgpu 0000:e3:00.0: amdgpu: gpu post error!
[   71.615776] amdgpu 0000:e3:00.0: amdgpu: Fatal error during GPU init
[   71.633447] amdgpu 0000:e3:00.0: amdgpu: amdgpu: finishing device.
[   71.650800] amdgpu: probe of 0000:e3:00.0 failed with error -22
[   71.652952] amdgpu 0000:c3:00.0: enabling device (0000 -> 0003)
[   71.660678] amdgpu 0000:c3:00.0: amdgpu: Fetched VBIOS from platform
[   71.661017] amdgpu: ATOM BIOS: 113-D3431401-100
[   71.662557] amdgpu 0000:c3:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[   91.663889] [drm:atom_op_jump [amdgpu]] *ERROR* atombios stuck in loop for more than 20secs aborting
[   91.665417] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 0484 (len 110, WS 12, PS 8) @ 0x04E9
[   91.666453] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 040A (len 45, WS 0, PS 8) @ 0x042B
[   91.667479] amdgpu 0000:c3:00.0: amdgpu: gpu post error!
[   91.667804] amdgpu 0000:c3:00.0: amdgpu: Fatal error during GPU init
[   91.685479] amdgpu 0000:c3:00.0: amdgpu: amdgpu: finishing device.
[   91.702817] amdgpu: probe of 0000:c3:00.0 failed with error -22
[   91.704944] amdgpu 0000:a3:00.0: enabling device (0000 -> 0003)
[   91.712867] amdgpu 0000:a3:00.0: amdgpu: Fetched VBIOS from platform
[   91.713202] amdgpu: ATOM BIOS: 113-D3431401-100
[   91.714744] amdgpu 0000:a3:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[  111.715890] [drm:atom_op_jump [amdgpu]] *ERROR* atombios stuck in loop for more than 20secs aborting
[  111.717420] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 0484 (len 110, WS 12, PS 8) @ 0x04E9
[  111.718453] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 040A (len 45, WS 0, PS 8) @ 0x042B
[  111.719471] amdgpu 0000:a3:00.0: amdgpu: gpu post error!
[  111.719795] amdgpu 0000:a3:00.0: amdgpu: Fatal error during GPU init
[  111.754644] amdgpu 0000:a3:00.0: amdgpu: amdgpu: finishing device.
[  111.771970] amdgpu: probe of 0000:a3:00.0 failed with error -22
`

2. Kernel info 2 6.8.0-55-generic #57-Ubuntu SMP PREEMPT_DYNAMIC
3.  lsmod | grep amd
```
amd64_edac             61440  0
edac_mce_amd           28672  1 amd64_edac
kvm_amd               208896  0
kvm                  1404928  1 kvm_amd
ccp                   143360  1 kvm_amd
amdgpu              19423232  0
amddrm_ttm_helper      12288  1 amdgpu
amdttm                110592  2 amdgpu,amddrm_ttm_helper
amddrm_buddy           24576  1 amdgpu
amdxcp                 12288  1 amdgpu
drm_exec               12288  1 amdgpu
drm_suballoc_helper    16384  1 amdgpu
amd_sched              61440  1 amdgpu
amdkcl                 32768  3 amd_sched,amdttm,amdgpu
drm_display_helper    237568  1 amdgpu
video                  77824  1 amdgpu
i2c_algo_bit           16384  3 igb,ast,amdgpu
```

This jsut runs no output `sudo modprobe amdgpu`


---

### 评论 #3 — harkgill-amd (2025-03-26T15:39:23Z)

Is the `lsmod | grep amd` output prior to running `sudo modprobe amdgpu` or after? Can you try running `rocm-smi` in the current state?

---

### 评论 #4 — ognjen011 (2025-03-26T15:45:24Z)

lsmod | grep amd is the same before and after sudo modprobe amdgpu running rocm-smi 

rocm-smi

```

      WARNING: No AMD GPUs specified
      ===================================== ROCm System Management Interface  =====================================
     =============================================== Concise Info ===============================================
     Device  Node  IDs           Temp    Power  Partitions          SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,  GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                              
                  ============================================================================================================
  ============================================================================================================
       =========================================== End of ROCm SMI Log ============================================`
```

---

### 评论 #5 — harkgill-amd (2025-03-26T18:55:04Z)

Thanks for the quick response! Could you also please provide the output of `lspci -nn | grep AMD/ATI`? Also, are you using a xGMI link?

---

### 评论 #6 — ognjen011 (2025-03-26T19:21:08Z)

As far as i know no xGMI link 

lspci -nn | grep AMD/ATI
```
01:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a0] (rev 01)
02:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a1]
03:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [Instinct MI100] [1002:738c] (rev 01)
41:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a0] (rev 01)
42:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a1]
43:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [Instinct MI100] [1002:738c] (rev 01)
a1:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a0] (rev 01)
a2:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a1]
a3:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [Instinct MI100] [1002:738c] (rev 01)
c1:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a0] (rev 01)
c2:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a1]
c3:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [Instinct MI100] [1002:738c] (rev 01)
e1:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a0] (rev 01)
e2:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:14a1]
e3:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [Instinct MI100] [1002:738c] (rev 01)
```

---

### 评论 #7 — ognjen011 (2025-03-27T15:01:25Z)

I think its hardware issue it seems some are failing and others are affected as well. 

---

### 评论 #8 — harkgill-amd (2025-03-27T15:09:23Z)

Hey @ognjen011, just a couple notes that may help you in debugging the hardware on your end.

The below errors in your dmesg point to a failure in reading a GPUs VBIOS. 
```
[   91.665417] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 0484 (len 110, WS 12, PS 8) @ 0x04E9  
[   91.666453] [drm:amdgpu_atom_execute_table_locked [amdgpu]] *ERROR* atombios stuck executing 040A (len 45, WS 0, PS 8) @ 0x042B  
```
In multi-card configurations, we've seen that it's often a single card or the xGMI link that can cause these errors. The next step would be to try isolating the faulty GPU or link.

---
