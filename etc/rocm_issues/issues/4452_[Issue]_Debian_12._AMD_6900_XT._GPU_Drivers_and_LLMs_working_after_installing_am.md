# [Issue]: Debian 12. AMD 6900 XT. GPU Drivers and LLMs working after installing amdgpu-dkms rocm but stop working after reboot

> **Issue #4452**
> **状态**: closed
> **创建时间**: 2025-03-06T07:54:23Z
> **更新时间**: 2025-03-06T14:54:01Z
> **关闭时间**: 2025-03-06T14:51:35Z
> **作者**: inneroot
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4452

## 描述

### Problem Description

Following Quick start installation guide and installing ROCm™ Software 6.3.3.
```
sudo apt update
sudo apt install "linux-headers-$(uname -r)"
sudo apt install -y python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/jammy/amdgpu-install_6.3.60303-1_all.deb
sudo apt install ./amdgpu-install_6.3.60303-1_all.deb
sudo apt update
sudo apt install amdgpu-dkms rocm
```
Then LLMS on ollama working perfectly fine until i ***reboot*** my system.
After reboot i have low resolution on login screen and cant change it after because as i understand GPU drivers stop working

### Operating System

Debian GNU/Linux 12 (bookworm) x86_64

### CPU

AMD Ryzen 7 5700X 8-Core Processor

### GPU

AMD Radeon RX 6900 XT

### ROCm Version

ROCm 6.3.3

### ROCm Component

_No response_

### Steps to Reproduce

On Debian 12 follow Quick start installation guide and then reboot

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
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
DMAbuf Support:          NO

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 7 5700X 8-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 5700X 8-Core Processor
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
  Max Clock Freq. (MHz):   3400
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
      Size:                    32766384(0x1f3f9b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32766384(0x1f3f9b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32766384(0x1f3f9b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32766384(0x1f3f9b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1030
  Uuid:                    GPU-33a8f3dd2a47955f
  Marketing Name:          AMD Radeon RX 6900 XT
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
    L1:                      16(0x10) KB
    L2:                      4096(0x1000) KB
    L3:                      131072(0x20000) KB
  Chip ID:                 29631(0x73bf)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2660
  BDFID:                   3072
  Internal Node ID:        1
  Compute Unit:            80
  SIMDs per CU:            2
  Shader Engines:          4
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
  Packet Processor uCode:: 104
  SDMA engine uCode::      81
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1030
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

```
    ,g$$$$$$$$$$$$$$$P.       -------------
  ,g$$P"     """Y$$.".        OS: Debian GNU/Linux 12 (bookworm) x86_64
 ,$$P'              `$$$.     Kernel: 6.1.0-30-amd64
',$$P       ,ggs.     `$$b:   Uptime: 8 mins
`d$$'     ,$P"'   .    $$$    Packages: 2300 (dpkg), 29 (brew), 54 (flatpak), 8 (snap)
 $$P      d$'     ,    $$P    Shell: zsh 5.9
 $$:      $$.   -    ,d$$'    Resolution: 3440x1440
 $$;      Y$b._   _,d$P'      DE: GNOME 43.9
 Y$$.    `.`"Y$$$$P"'         WM: Mutter
 `$$b      "-.__              WM Theme: Adwaita
  `Y$$                        Theme: Adwaita [GTK2/3]
   `Y$$.                      Icons: gnome [GTK2/3]
     `$$b.                    Terminal: tmux
       `Y$$b.                 CPU: AMD Ryzen 7 5700X (16) @ 3.400GHz
          `"Y$b._             GPU: AMD ATI Radeon RX 6800/6800 XT / 6900 XT
              `"""            Memory: 3303MiB / 31998MiB
```

---

## 评论 (6 条)

### 评论 #1 — inneroot (2025-03-06T09:52:19Z)

Then I just use Timeshift to go back to working setup

---

### 评论 #2 — inneroot (2025-03-06T09:59:07Z)

```
sudo apt show rocm-libs -a

Package: rocm-libs
Version: 6.3.3.60303-74~22.04
Priority: optional
Section: devel
Maintainer: ROCm Dev Support <rocm-dev.support@amd.com>
Installed-Size: 13.3 kB
Depends: hipblas (= 2.3.0.60303-74~22.04), hipblaslt (= 0.10.0.60303-74~22.04), hipfft (= 1.0.17.60303-74~22.04), hipsolver (= 2.3.0.60303-74~22.04), hipsparse (= 3.1.2.60303-74~22.04), hiptensor (= 1.4.0.60303-74~22.04), miopen-hip (= 3.3.0.60303-74~22.04), half (= 1.12.0.60303-74~22.04), rccl (= 2.21.5.60303-74~22.04), rocalution (= 3.2.1.60303-74~22.04), rocblas (= 4.3.0.60303-74~22.04), rocfft (= 1.0.31.60303-74~22.04), rocrand (= 3.2.0.60303-74~22.04), hiprand (= 2.11.1.60303-74~22.04), rocsolver (= 3.27.0.60303-74~22.04), rocsparse (= 3.3.0.60303-74~22.04), rocm-core (= 6.3.3.60303-74~22.04), hipsparselt (= 0.2.2.60303-74~22.04), composablekernel-dev (= 1.1.0.60303-74~22.04), hipblas-dev (= 2.3.0.60303-74~22.04), hipblaslt-dev (= 0.10.0.60303-74~22.04), hipcub-dev (= 3.3.0.60303-74~22.04), hipfft-dev (= 1.0.17.60303-74~22.04), hipsolver-dev (= 2.3.0.60303-74~22.04), hipsparse-dev (= 3.1.2.60303-74~22.04), hiptensor-dev (= 1.4.0.60303-74~22.04), miopen-hip-dev (= 3.3.0.60303-74~22.04), rccl-dev (= 2.21.5.60303-74~22.04), rocalution-dev (= 3.2.1.60303-74~22.04), rocblas-dev (= 4.3.0.60303-74~22.04), rocfft-dev (= 1.0.31.60303-74~22.04), rocprim-dev (= 3.3.0.60303-74~22.04), rocrand-dev (= 3.2.0.60303-74~22.04), hiprand-dev (= 2.11.1.60303-74~22.04), rocsolver-dev (= 3.27.0.60303-74~22.04), rocsparse-dev (= 3.3.0.60303-74~22.04), rocthrust-dev (= 3.3.0.60303-74~22.04), rocwmma-dev (= 1.6.0.60303-74~22.04), hipsparselt-dev (= 0.2.2.60303-74~22.04)
Homepage: https://github.com/RadeonOpenCompute/ROCm
Download-Size: 1,058 B
APT-Sources: https://repo.radeon.com/rocm/apt/6.3.3 jammy/main amd64 Packages
Description: Radeon Open Compute (ROCm) Runtime software stack
```


---

### 评论 #3 — inneroot (2025-03-06T10:10:00Z)

after installing and reboot
```
>rocminfo
ROCk module is NOT loaded, possibly no GPU devices

>clinfo
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               0
```

---

### 评论 #4 — inneroot (2025-03-06T11:07:21Z)

looks like its problem specifically with `amdgpu-dkms`

---

### 评论 #5 — inneroot (2025-03-06T14:51:35Z)

Ok. Problem was with secure boot option in UEFI BIOS. Was selected [Windows], changed it to second possible option [Other OS]. And after reboot with this option drivers loaded properly
```
>lsmod | grep amdgpu
amdgpu              12947456  26
...
```

---

### 评论 #6 — harkgill-amd (2025-03-06T14:54:00Z)

Nice catch. We will be adding documentation on the need to disable Secure Boot, tracked in https://github.com/ROCm/ROCm/issues/4328.

---
