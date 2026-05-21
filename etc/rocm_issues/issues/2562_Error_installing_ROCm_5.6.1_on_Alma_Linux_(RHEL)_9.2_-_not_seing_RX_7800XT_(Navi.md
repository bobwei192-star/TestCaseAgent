# Error installing ROCm 5.6.1 on Alma Linux (RHEL) 9.2 - not seing RX 7800XT (Navi 3) GPU

> **Issue #2562**
> **状态**: closed
> **创建时间**: 2023-10-14T20:28:14Z
> **更新时间**: 2023-10-21T15:41:45Z
> **关闭时间**: 2023-10-21T15:41:45Z
> **作者**: luraess
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2562

## 描述

I am trying to install and use ROCm + HIP with a recently acquired RX 7800XT (Navi 3) GPU on an Alma Linux (RHEL) 9.2 distribution with ROCm 5.6.1. **Install succeeds but I can't see and access the GPU.**

I have checked the pre-requisite from the website https://rocm.docs.amd.com/en/docs-5.6.1/deploy/linux/prerequisites.html#
```
uname -m && cat /etc/*release
x86_64
AlmaLinux release 9.2 (Turquoise Kodkod)
NAME="AlmaLinux"
VERSION="9.2 (Turquoise Kodkod)"
ID="almalinux"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.2"
PLATFORM_ID="platform:el9"
PRETTY_NAME="AlmaLinux 9.2 (Turquoise Kodkod)"
ANSI_COLOR="0;34"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:almalinux:almalinux:9::baseos"
HOME_URL="https://almalinux.org/"
DOCUMENTATION_URL="https://wiki.almalinux.org/"
BUG_REPORT_URL="https://bugs.almalinux.org/"

ALMALINUX_MANTISBT_PROJECT="AlmaLinux-9"
ALMALINUX_MANTISBT_PROJECT_VERSION="9.2"
REDHAT_SUPPORT_PRODUCT="AlmaLinux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.2"
AlmaLinux release 9.2 (Turquoise Kodkod)
AlmaLinux release 9.2 (Turquoise Kodkod)
```
And the kernel is
```
uname -srmv
Linux 5.14.0-284.30.1.el9_2.x86_64 #1 SMP PREEMPT_DYNAMIC Tue Sep 12 09:28:32 EDT 2023 x86_64
```
This information matches requirements as per documentation. EPEL and linux headers installed without issues as well.

Installing both from the package manager or using the `amdgpu-install`  script succeed without errors. https://rocm.docs.amd.com/en/docs-5.6.1/deploy/linux/installer/install.html (RHEL 9.2).

Verification returns:
```
dkms status
amdgpu/6.1.5-1649308.el9, 5.14.0-284.30.1.el9_2.x86_64, x86_64: installed (original_module exists)
```

However, I can't see the GPU (which is listed in `lspci`). `rocminfo` lists CPU only
```
/opt/rocm/bin/rocminfo
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
  Name:                    Intel(R) Core(TM) i5-4460  CPU @ 3.20GHz
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i5-4460  CPU @ 3.20GHz
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
  Compute Unit:            4
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32531828(0x1f06574) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32531828(0x1f06574) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32531828(0x1f06574) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
```
and `clinfo` sees 0 device
```
/opt/rocm/opencl/bin/clinfo
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3581.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 0
```

The only warnings or potential hints I have are following:
- amdgpu-dkms install
```
  Installing       : amdgpu-dkms-firmware-1:6.1.5.50601-1649308.el9.noarch                                                                                  86/93
  Installing       : amdgpu-dkms-1:6.1.5.50601-1649308.el9.noarch                                                                                           87/93
  Running scriptlet: amdgpu-dkms-1:6.1.5.50601-1649308.el9.noarch                                                                                           87/93
EFI variables are not supported on this system
Loading new amdgpu-6.1.5-1649308.el9 DKMS files...
dpkg: warning: version '4.18.0-240.22.1.el8_3.x86_64' has bad syntax: invalid character in revision number
dpkg: warning: version '5.14.0-284.30.1.el9_2.x86_64' has bad syntax: invalid character in revision number
dpkg: warning: version '4.18.0-477.27.2.el8_8.x86_64' has bad syntax: invalid character in revision number
dpkg: warning: version '5.14.0-284.30.1.el9_2.x86_64' has bad syntax: invalid character in revision number
dpkg: warning: version '5.14.0-284.30.1.el9_2.x86_64' has bad syntax: invalid character in revision number
dpkg: warning: version '5.14.0-284.30.1.el9_2.x86_64' has bad syntax: invalid character in revision number
Building for 5.14.0-284.30.1.el9_2.x86_64
Building initial module for 5.14.0-284.30.1.el9_2.x86_64
Done.
Forcing installation of amdgpu
```

- `lsmod`:
```
lsmod | grep amd
amdgpu              10719232  0
amddrm_ttm_helper      16384  1 amdgpu
amdttm                 94208  2 amdgpu,amddrm_ttm_helper
iommu_v2               24576  1 amdgpu
amddrm_buddy           20480  1 amdgpu
amd_sched              49152  1 amdgpu
amdkcl                 36864  3 amd_sched,amdttm,amdgpu
i2c_algo_bit           16384  2 amdgpu,i915
drm_display_helper    172032  2 amdgpu,i915
drm_kms_helper        192512  3 drm_display_helper,amdgpu,i915
drm                   581632  11 drm_kms_helper,amd_sched,amdttm,drm_display_helper,drm_buddy,amdgpu,amddrm_buddy,i915,ttm,amddrm_ttm_helper
```

- `dmesg`
```
dmesg | grep -i amdgpu
[    3.814225] [drm] amdgpu kernel modesetting enabled.
[    3.814247] [drm] amdgpu version: 6.1.5
[    3.814367] amdgpu: CRAT table not found
[    3.814383] amdgpu: Virtual CRAT table created for CPU
[    3.814407] amdgpu: Topology: Add CPU node
[    3.824904] amdgpu 0000:03:00.0: enabling device (0000 -> 0003)
[    3.872887] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from ROM BAR
[    3.872911] amdgpu: ATOM BIOS: 115-D712BP2-100
[    3.872964] amdgpu 0000:03:00.0: Direct firmware load for amdgpu/psp_13_0_10_sos.bin failed with error -2
[    3.872996] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -19
[    3.873342] amdgpu 0000:03:00.0: Direct firmware load for amdgpu/smu_13_0_10.bin failed with error -2
[    3.873379] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <smu> failed -19
[    3.873727] amdgpu 0000:03:00.0: Direct firmware load for amdgpu/gc_11_0_3_pfp.bin failed with error -2
[    3.873764] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <gfx_v11_0> failed -19
[    3.874699] amdgpu 0000:03:00.0: [drm:jpeg_v4_0_early_init [amdgpu]] JPEG decode is enabled in VM mode
[    3.875107] amdgpu 0000:03:00.0: Direct firmware load for amdgpu/gc_11_0_3_mes_2.bin failed with error -2
[    3.875148] [drm] try to fall back to amdgpu/gc_11_0_3_mes.bin
[    3.875195] amdgpu 0000:03:00.0: Direct firmware load for amdgpu/gc_11_0_3_mes.bin failed with error -2
[    3.875231] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <mes_v11_0> failed -19
[    3.875506] amdgpu 0000:03:00.0: amdgpu: Fatal error during GPU init
[    3.875532] amdgpu 0000:03:00.0: amdgpu: amdgpu: finishing device.
[    3.875627] amdgpu: legacy kernel without apple_gmux_detect()
```

Any hints on what may go wrong?

---

## 评论 (4 条)

### 评论 #1 — pramenku (2023-10-17T18:09:42Z)

@luraess 
Suggest to refer the rocm documentation with list of supported GPU.

As I can read the documentation, Navi3,7800XT is NOT supported GPU for ROCm5.6.x

---

### 评论 #2 — pramenku (2023-10-17T18:12:22Z)

https://rocm.docs.amd.com/en/docs-5.6.1/release/gpu_os_support.html

Although, ROCm5.7.1 supports 7900, https://rocm.docs.amd.com/en/docs-5.7.1/release/gpu_os_support.html

---

### 评论 #3 — luraess (2023-10-17T22:32:40Z)

Thanks for the pointers @pramenku !

---

### 评论 #4 — pramenku (2023-10-21T15:41:45Z)

Closing the issue. Feel free to reopen if needed.

---
