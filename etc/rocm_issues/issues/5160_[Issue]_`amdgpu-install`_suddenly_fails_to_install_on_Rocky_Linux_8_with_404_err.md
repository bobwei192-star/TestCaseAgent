# [Issue]: `amdgpu-install` suddenly fails to install on Rocky Linux 8 with 404 error

> **Issue #5160**
> **状态**: closed
> **创建时间**: 2025-08-07T08:47:31Z
> **更新时间**: 2025-08-27T13:22:25Z
> **关闭时间**: 2025-08-27T13:22:25Z
> **作者**: bartvdbraak
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5160

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am part of @blender and we are currently in the process of adding new GPU workers to our CI/CD stack, including AMD-specific ones. 

About 2 weeks ago we were following the following instructions for installing them (which I retrieved from [your documentation](https://amdgpu-install.readthedocs.io/en/latest/install-prereq.html#downloading-the-installer-package)) and was successful in doing so, however, re-running this right now causes a 404 error instead:

```
[blender@rocky-x64-amd-01 ~]$ amdgpu-install --usecase=workstation -y --vulkan=pro --opencl=rocr --opengl=mesa --rocmrelease=6.4.0 --accept-eula
AMDGPU 6.4.2 Proprietary repository                                                                                                                                                    485  B/s | 548  B     00:01
Errors during downloading metadata for repository 'amdgpu-proprietary':
  - Status code: 404 for https://repo.radeon.com/amdgpu/6.4.2/rhel/8.10/proprietary/x86_64/repodata/repomd.xml (IP: 104.126.37.145)
Error: Failed to download metadata for repo 'amdgpu-proprietary': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried
```

It looks like the proprietary drivers for Rocky Linux 8 (`rhel8`) have been removed in the meantime.

### Operating System

Rocky Linux 8.10 (Green Obsidian)

### CPU

AMD Ryzen 9 7950X 16-Core Processor

### GPU

AMD Radeon RX 5700 XT (`gfx1010`)

### ROCm Version

ROCm 6.4.2

### ROCm Component

ROCm

### Steps to Reproduce

1. Be on RHEL8-based OS, in my case Rocky Linux 8.
2. Run `wget https://repo.radeon.com/amdgpu-install/6.4.2/rhel/8.10/amdgpu-install-6.4.60402-1.el8.noarch.rpm`
   ```
   --2025-08-06 15:22:55--  https://repo.radeon.com/amdgpu-install/6.4.2/rhel/8.10/amdgpu-install-6.4.60402-1.el8.noarch.rpm
   Resolving repo.radeon.com (repo.radeon.com)... 88.221.24.25, 88.221.24.58, 2a02:26f0:b200::58dd:1989, ...
   Connecting to repo.radeon.com (repo.radeon.com)|88.221.24.25|:443... connected.
   HTTP request sent, awaiting response... 200 OK
   Length: 25856 (25K) [application/x-redhat-package-manager]
   Saving to: ‘amdgpu-install-6.4.60402-1.el8.noarch.rpm’
   
   amdgpu-install-6.4.60402-1.el8.noarch.rpm             100%[========================================================================================================================>]  25.25K  --.-KB/s    in 0.002s
   
   2025-08-06 15:22:55 (10.4 MB/s) - ‘amdgpu-install-6.4.60402-1.el8.noarch.rpm’ saved [25856/25856]
   ```
3. Install using `sudo dnf install amdgpu-install-6.4.60402-1.el8.noarch.rpm -y`:
   ```
   Last metadata expiration check: 0:19:11 ago on Wed 06 Aug 2025 03:03:55 PM UTC.
   Package amdgpu-install-6.4.60402-2187269.el8.noarch is already installed.
   Dependencies resolved.
   Nothing to do.
   Complete!
   ```
5. Try to install Pro drivers using `amdgpu-install --usecase=workstation -y --vulkan=pro --opencl=rocr --opengl=mesa --rocmrelease=6.4.0 --accept-eula` and observe 404 errors:
   ```
   AMDGPU 6.4.2 Proprietary repository                                                                                                                                                    485  B/s | 548  B     00:01
   Errors during downloading metadata for repository 'amdgpu-proprietary':
   - Status code: 404 for https://repo.radeon.com/amdgpu/6.4.2/rhel/8.10/proprietary/x86_64/repodata/repomd.xml (IP: 104.126.37.145)
   Error: Failed to download metadata for repo 'amdgpu-proprietary': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried
   ```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.15
Runtime Ext Version:     1.7
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          NO
VMM Support:             NO

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 9 7950X 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 7950X 16-Core Processor
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
  Max Clock Freq. (MHz):   5881
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            32
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    64728840(0x3dbaf08) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    64728840(0x3dbaf08) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    64728840(0x3dbaf08) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    64728840(0x3dbaf08) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1010
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon RX 5700 XT
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
  Chip ID:                 29471(0x731f)
  ASIC Revision:           2(0x2)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            40
  SIMDs per CU:            2
  Shader Engines:          2
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
  Max Waves Per CU:        40(0x28)
  Max Work-item Per CU:    1280(0x500)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 156
  SDMA engine uCode::      35
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    8372224(0x7fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8372224(0x7fc000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1010:xnack-
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
      Name:                    amdgcn-amd-amdhsa--gfx10-1-generic:xnack-
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
*******
Agent 3
*******
  Name:                    gfx1036
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
  Node:                    2
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      256(0x100) KB
  Chip ID:                 5710(0x164e)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2200
  BDFID:                   4352
  Internal Node ID:        2
  Compute Unit:            2
  SIMDs per CU:            2
  Shader Engines:          1
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
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
  Packet Processor uCode:: 22
  SDMA engine uCode::      9
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    524288(0x80000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    524288(0x80000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1036
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
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic
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

_No response_

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-08-07T14:06:40Z)

Hi @bartvdbraak. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — harkgill-amd (2025-08-12T14:45:59Z)

Hi @bartvdbraak, thanks again for the report. We are working on getting the RHEL 8.10 PRO drivers/packages tested and released. Will provide any relevant updates here.

---

### 评论 #3 — bartvdbraak (2025-08-12T14:48:19Z)

> Hi [@bartvdbraak](https://github.com/bartvdbraak), thanks again for the report. We are working on getting the RHEL 8.10 PRO drivers/packages tested and released. Will provide any relevant updates here.

Thanks for the update, will be keeping a close eye on any updates.

---

### 评论 #4 — bartvdbraak (2025-08-25T09:43:14Z)

@harkgill-amd FYI

I have been informed by one of our contacts at AMD that a 6.4.2.1 version of the repo was released, however, I am still running into some issues.

Downloading and installing the `amdgpu-install` utility from the new `6.4.2.1` version still seems to be creating repository sources related to `6.4.2`:

```bash
[blender@rocky-x64-amd-01 ~]$ wget https://repo.radeon.com/amdgpu/6.4.2.1/rhel/8.10/main/x86_64/amdgpu-install-6.4.60402-2187269.el8.noarch.rpm
--2025-08-25 07:43:46--  https://repo.radeon.com/amdgpu/6.4.2.1/rhel/8.10/main/x86_64/amdgpu-install-6.4.60402-2187269.el8.noarch.rpm
Resolving [repo.radeon.com](http://repo.radeon.com/) ([repo.radeon.com](http://repo.radeon.com/))... 23.73.0.177, 23.73.0.144, 2a02:26f0:1180:33::210:647, ...
Connecting to [repo.radeon.com](http://repo.radeon.com/) ([repo.radeon.com](http://repo.radeon.com/))|23.73.0.177|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 25856 (25K) [application/x-redhat-package-manager]
Saving to: ‘amdgpu-install-6.4.60402-2187269.el8.noarch.rpm’

amdgpu-install-6.4.60402-2 100%[=======================================>]  25.25K  --.-KB/s    in 0.002s

2025-08-25 07:43:47 (11.4 MB/s) - ‘amdgpu-install-6.4.60402-2187269.el8.noarch.rpm’ saved [25856/25856]

[blender@rocky-x64-amd-01 ~]$ ls
amdgpu-install-6.4.60402-2187269.el8.noarch.rpm  git
[blender@rocky-x64-amd-01 ~]$ sudo dnf install amdgpu-install-6.4.60402-2187269.el8.noarch.rpm
Last metadata expiration check: 0:22:23 ago on Mon 25 Aug 2025 07:21:38 AM UTC.
Dependencies resolved.
===========================================================================================================
 Package                  Architecture     Version                            Repository              Size
===========================================================================================================
Installing:
 amdgpu-install           noarch           6.4.60402-2187269.el8              @commandline            25 k
Installing weak dependencies:
 dialog                   x86_64           1.3-13.20171209.el8                appstream              232 k

Transaction Summary
===========================================================================================================
Install  2 Packages

Total size: 257 k
Total download size: 232 k
Installed size: 597 k
Is this ok [y/N]: y
Downloading Packages:
dialog-1.3-13.20171209.el8.x86_64.rpm                                      306 kB/s | 232 kB     00:00
-----------------------------------------------------------------------------------------------------------
Total                                                                      261 kB/s | 232 kB     00:00
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                   1/1
  Installing       : dialog-1.3-13.20171209.el8.x86_64                                                 1/2
  Installing       : amdgpu-install-6.4.60402-2187269.el8.noarch                                       2/2
  Running scriptlet: amdgpu-install-6.4.60402-2187269.el8.noarch                                       2/2
  Verifying        : dialog-1.3-13.20171209.el8.x86_64                                                 1/2
  Verifying        : amdgpu-install-6.4.60402-2187269.el8.noarch                                       2/2

Installed:
  amdgpu-install-6.4.60402-2187269.el8.noarch               dialog-1.3-13.20171209.el8.x86_64

Complete!
[blender@rocky-x64-amd-01 ~]$ amdgpu-install --usecase=workstation -y --vulkan=pro --opencl=rocr --opengl=mesa --dryrun --rocmrelease=6.4.0 --accept-eula
sudo dnf install -y amdgpu-pro amdgpu-dkms rocm-opencl-runtime6.4.0 amdgpu-lib vulkan-amdgpu-pro
sudo ln -sf /usr/bin/amdgpu-install /usr/bin/amdgpu-uninstall
[blender@rocky-x64-amd-01 ~]$ amdgpu-install --usecase=workstation -y --vulkan=pro --opencl=rocr --opengl=mesa --rocmrelease=6.4.0 --accept-eula
AMDGPU 6.4.2 repository                                                    202 kB/s | 3.0 kB     00:00
AMDGPU 6.4.2 Proprietary repository                                        1.0 kB/s | 548  B     00:00
Errors during downloading metadata for repository 'amdgpu-proprietary':
  - Status code: 404 for https://repo.radeon.com/amdgpu/6.4.2/rhel/8.10/proprietary/x86_64/repodata/repomd.xml (IP: 23.73.0.177)
Error: Failed to download metadata for repo 'amdgpu-proprietary': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried
```

When manually updating the `amdgpu.repo` and `amdgpu-proprietary.repo` configurations, it does seem to work:
```
[blender@rocky-x64-amd-01 yum.repos.d]$ cat amdgpu.repo
[amdgpu]
name=AMDGPU 6.4.2.1 repository
baseurl=https://repo.radeon.com/amdgpu/6.4.2.1/rhel/$amdgpudistro/main/x86_64
enabled=1
gpgcheck=1
gpgkey=file:///etc/amdgpu-install/rocm.gpg.key

[amdgpu-src]
name=AMDGPU 6.4.2.1 repository
baseurl=https://repo.radeon.com/amdgpu/6.4.2.1/rhel/$amdgpudistro/main/source
enabled=0
gpgcheck=1
gpgkey=file:///etc/amdgpu-install/rocm.gpg.key
[blender@rocky-x64-amd-01 yum.repos.d]$ cat amdgpu-proprietary.repo
# Enabling this repository requires acceptance of the following license:
# /usr/share/amdgpu-install/AMDGPUPROEULA
[amdgpu-proprietary]
name=AMDGPU 6.4.2.1 Proprietary repository
baseurl=https://repo.radeon.com/amdgpu/6.4.2.1/rhel/$amdgpudistro/proprietary/x86_64
enabled=1
gpgcheck=1
gpgkey=file:///etc/amdgpu-install/rocm.gpg.key
[blender@rocky-x64-amd-01 yum.repos.d]$ sudo dnf clean all
89 files removed
[blender@rocky-x64-amd-01 yum.repos.d]$ sudo dnf makecache
...
AMDGPU 6.4.2.1 repository                      1.2 MB/s |  91 kB     00:00
AMDGPU 6.4.2.1 Proprietary repository          6.1 kB/s | 4.7 kB     00:00
...
Metadata cache created.
[blender@rocky-x64-amd-01 yum.repos.d]$ sudo dnf install -y amdgpu-pro amdgpu-dkms rocm-opencl-runtime6.4.0 amdgpu-lib vulkan-amdgpu-pro
Last metadata expiration check: 0:00:15 ago on Mon 25 Aug 2025 09:38:32 AM UTC.
Dependencies resolved.
===============================================================================
 Package                    Arch   Version                    Repository  Size
===============================================================================
Installing:
 amdgpu-dkms                noarch 1:6.12.12-2187269.el8      amdgpu      16 M
 amdgpu-lib                 x86_64 1:6.4.60402-2187269.el8    amdgpu     6.8 k
 amdgpu-pro                 x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                          12 k
 rocm-opencl-runtime6.4.0   x86_64 6.4.0.60400-47.el8         rocm-6.4.0  11 k
 vulkan-amdgpu-pro          x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                          32 M
Installing dependencies:
 amdgpu                     x86_64 1:6.4.60402-2187269.el8    amdgpu     6.3 k
 amdgpu-dkms-firmware       noarch 1:6.12.12-2187269.el8      amdgpu      18 M
 amdgpu-multimedia          x86_64 1:6.4.60402-2187269.el8    amdgpu     6.5 k
 amdgpu-pro-core            noarch 25.10-2190998.el8          amdgpu-proprietary
                                                                          14 k
 amdgpu-pro-oglp            x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                          12 k
 autoconf                   noarch 2.69-29.el8_10.1           appstream  710 k
 automake                   noarch 1.16.1-8.el8               appstream  713 k
 dkms                       noarch 3.2.1-1.el8                epel        90 k
 libXdamage                 x86_64 1.1.4-14.el8               appstream   26 k
 libXdmcp                   x86_64 1.1.3-1.el8                appstream   40 k
 libXfont2                  x86_64 2.0.3-2.el8                appstream  147 k
 libegl-amdgpu-pro-oglp     x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                          21 k
 libepoxy                   x86_64 1.5.8-1.el8                appstream  224 k
 libevdev                   x86_64 1.10.0-1.el8               appstream   43 k
 libfontenc                 x86_64 1.1.3-8.el8                appstream   36 k
 libgl-amdgpu-pro-oglp      x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                         143 k
 libgl-amdgpu-pro-oglp-dri  x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                          14 M
 libgl-amdgpu-pro-oglp-ext  x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                         123 k
 libgl-amdgpu-pro-oglp-gbm  x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                          24 k
 libgles-amdgpu-pro-oglp    x86_64 25.10-2190998.el8          amdgpu-proprietary
                                                                          45 k
 libinput                   x86_64 1.16.3-3.el8_6             appstream  216 k
 libva-amdgpu               x86_64 2.16.0.60402-2187269.el8   amdgpu      87 k
 libvdpau-amdgpu            x86_64 6.4-2187269.el8            amdgpu      36 k
 libwacom                   x86_64 1.6-3.el8                  appstream   41 k
 libwacom-data              noarch 1.6-3.el8                  appstream  103 k
 libwayland-amdgpu-client   x86_64 1.23.0.60402-2187269.el8   amdgpu      36 k
 libwayland-amdgpu-server   x86_64 1.23.0.60402-2187269.el8   amdgpu      44 k
 libxkbfile                 x86_64 1.1.0-1.el8                appstream   87 k
 llvm-amdgpu-libs           x86_64 1:19.1.60402-2187269.el8   amdgpu      29 M
 llvm-compat-libs           x86_64 17.0.6-3.module+el8.10.0+1875+4f0b06db
                                                              appstream   55 M
 mesa-amdgpu-dri-drivers    x86_64 1:25.0.0.60402-2187269.el8 amdgpu      41 k
 mesa-amdgpu-filesystem     x86_64 1:25.0.0.60402-2187269.el8 amdgpu     6.9 k
 mesa-amdgpu-libEGL         x86_64 1:25.0.0.60402-2187269.el8 amdgpu     140 k
 mesa-amdgpu-libGL          x86_64 1:25.0.0.60402-2187269.el8 amdgpu     157 k
 mesa-amdgpu-libgallium     x86_64 1:25.0.0.60402-2187269.el8 amdgpu     7.0 M
 mesa-amdgpu-libgbm         x86_64 1:25.0.0.60402-2187269.el8 amdgpu      37 k
 mesa-amdgpu-libxatracker   x86_64 1:25.0.0.60402-2187269.el8 amdgpu     1.7 M
 mesa-amdgpu-va-drivers     x86_64 1:25.0.0.60402-2187269.el8 amdgpu     9.7 k
 mesa-amdgpu-vdpau-drivers  x86_64 1:25.0.0.60402-2187269.el8 amdgpu      11 k
 mesa-filesystem            x86_64 23.1.4-4.el8_10            appstream   34 k
 mesa-vulkan-drivers        x86_64 23.1.4-4.el8_10            appstream  9.8 M
 mtdev                      x86_64 1.1.5-12.el8               appstream   23 k
 ocl-icd                    x86_64 2.2.12-1.el8               appstream   50 k
 openmp-extras-runtime6.4.0 x86_64 18.63.0.60400-47.el8       rocm-6.4.0  48 M
 patch                      x86_64 2.7.6-11.el8               baseos     137 k
 pixman                     x86_64 0.38.4-4.el8               appstream  256 k
 rocm-language-runtime6.4.0 x86_64 6.4.0.60400-47.el8         rocm-6.4.0 7.2 k
 rocm-opencl6.4.0           x86_64 2.0.0.60400-47.el8         rocm-6.4.0 481 k
 vulkan-loader              x86_64 1.3.283.0-1.el8_10         appstream  147 k
 xorg-x11-amdgpu-drv-amdgpu x86_64 1:24.1.0-2187269.el8       amdgpu      72 k
 xorg-x11-drv-fbdev         x86_64 0.5.0-2.el8                appstream   26 k
 xorg-x11-drv-libinput      x86_64 0.29.0-1.el8               appstream   49 k
 xorg-x11-drv-vesa          x86_64 2.4.0-3.el8                appstream   30 k
 xorg-x11-server-Xorg       x86_64 1.20.11-26.el8_10          appstream  1.5 M
 xorg-x11-server-common     x86_64 1.20.11-26.el8_10          appstream   45 k
 xorg-x11-xkb-utils         x86_64 7.7-28.el8                 appstream  113 k
Enabling module streams:
 llvm-toolset                      rhel8

Transaction Summary
===============================================================================
Install  61 Packages

Total download size: 237 M
Installed size: 1.4 G
Downloading Packages:
(1/61): libXdamage-1.1.4-14.el8.x86_64.rpm      91 kB/s |  26 kB     00:00
(2/61): automake-1.16.1-8.el8.noarch.rpm       2.3 MB/s | 713 kB     00:00
(3/61): autoconf-2.69-29.el8_10.1.noarch.rpm   2.3 MB/s | 710 kB     00:00
(4/61): libXfont2-2.0.3-2.el8.x86_64.rpm       3.0 MB/s | 147 kB     00:00
(5/61): libevdev-1.10.0-1.el8.x86_64.rpm       461 kB/s |  43 kB     00:00
(6/61): libepoxy-1.5.8-1.el8.x86_64.rpm        1.2 MB/s | 224 kB     00:00
(7/61): libXdmcp-1.1.3-1.el8.x86_64.rpm        192 kB/s |  40 kB     00:00
(8/61): libfontenc-1.1.3-8.el8.x86_64.rpm      591 kB/s |  36 kB     00:00
(9/61): libinput-1.16.3-3.el8_6.x86_64.rpm     4.0 MB/s | 216 kB     00:00
(10/61): libxkbfile-1.1.0-1.el8.x86_64.rpm     1.6 MB/s |  87 kB     00:00
(11/61): libwacom-data-1.6-3.el8.noarch.rpm    1.1 MB/s | 103 kB     00:00
(12/61): mesa-filesystem-23.1.4-4.el8_10.x86_6 629 kB/s |  34 kB     00:00
(13/61): libwacom-1.6-3.el8.x86_64.rpm         203 kB/s |  41 kB     00:00
(14/61): mtdev-1.1.5-12.el8.x86_64.rpm         391 kB/s |  23 kB     00:00
(15/61): ocl-icd-2.2.12-1.el8.x86_64.rpm       620 kB/s |  50 kB     00:00
(16/61): pixman-0.38.4-4.el8.x86_64.rpm        1.8 MB/s | 256 kB     00:00
(17/61): mesa-vulkan-drivers-23.1.4-4.el8_10.x  24 MB/s | 9.8 MB     00:00
(18/61): vulkan-loader-1.3.283.0-1.el8_10.x86_ 1.0 MB/s | 147 kB     00:00
(19/61): xorg-x11-drv-fbdev-0.5.0-2.el8.x86_64 487 kB/s |  26 kB     00:00
(20/61): xorg-x11-drv-libinput-0.29.0-1.el8.x8 878 kB/s |  49 kB     00:00
(21/61): xorg-x11-drv-vesa-2.4.0-3.el8.x86_64. 365 kB/s |  30 kB     00:00
(22/61): xorg-x11-server-common-1.20.11-26.el8 964 kB/s |  45 kB     00:00
(23/61): xorg-x11-xkb-utils-7.7-28.el8.x86_64. 2.3 MB/s | 113 kB     00:00
(24/61): patch-2.7.6-11.el8.x86_64.rpm         7.7 MB/s | 137 kB     00:00
(25/61): xorg-x11-server-Xorg-1.20.11-26.el8_1 8.1 MB/s | 1.5 MB     00:00
(26/61): amdgpu-6.4.60402-2187269.el8.x86_64.r  17 kB/s | 6.3 kB     00:00
(27/61): amdgpu-dkms-6.12.12-2187269.el8.noarc 6.2 MB/s |  16 MB     00:02
(28/61): amdgpu-dkms-firmware-6.12.12-2187269. 7.7 MB/s |  18 MB     00:02
(29/61): amdgpu-lib-6.4.60402-2187269.el8.x86_  19 kB/s | 6.8 kB     00:00
(30/61): amdgpu-multimedia-6.4.60402-2187269.e  17 kB/s | 6.5 kB     00:00
(31/61): libva-amdgpu-2.16.0.60402-2187269.el8 245 kB/s |  87 kB     00:00
(32/61): libvdpau-amdgpu-6.4-2187269.el8.x86_6  79 kB/s |  36 kB     00:00
(33/61): libwayland-amdgpu-server-1.23.0.60402 231 kB/s |  44 kB     00:00
(34/61): libwayland-amdgpu-client-1.23.0.60402  59 kB/s |  36 kB     00:00
(35/61): mesa-amdgpu-dri-drivers-25.0.0.60402-  87 kB/s |  41 kB     00:00
(36/61): mesa-amdgpu-filesystem-25.0.0.60402-2  36 kB/s | 6.9 kB     00:00
(37/61): llvm-compat-libs-17.0.6-3.module+el8.  10 MB/s |  55 MB     00:05
(38/61): mesa-amdgpu-libEGL-25.0.0.60402-21872 231 kB/s | 140 kB     00:00
(39/61): mesa-amdgpu-libGL-25.0.0.60402-218726 224 kB/s | 157 kB     00:00
(40/61): mesa-amdgpu-libgbm-25.0.0.60402-21872  77 kB/s |  37 kB     00:00
(41/61): llvm-amdgpu-libs-19.1.60402-2187269.e  12 MB/s |  29 MB     00:02
(42/61): mesa-amdgpu-libgallium-25.0.0.60402-2 6.3 MB/s | 7.0 MB     00:01
(43/61): mesa-amdgpu-va-drivers-25.0.0.60402-2  48 kB/s | 9.7 kB     00:00
(44/61): mesa-amdgpu-vdpau-drivers-25.0.0.6040  56 kB/s |  11 kB     00:00
(45/61): amdgpu-pro-25.10-2190998.el8.x86_64.r  63 kB/s |  12 kB     00:00
(46/61): amdgpu-pro-core-25.10-2190998.el8.noa  70 kB/s |  14 kB     00:00
(47/61): mesa-amdgpu-libxatracker-25.0.0.60402 1.8 MB/s | 1.7 MB     00:00
(48/61): xorg-x11-amdgpu-drv-amdgpu-24.1.0-218 134 kB/s |  72 kB     00:00
(49/61): libegl-amdgpu-pro-oglp-25.10-2190998. 115 kB/s |  21 kB     00:00
(50/61): amdgpu-pro-oglp-25.10-2190998.el8.x86  32 kB/s |  12 kB     00:00
(51/61): libgl-amdgpu-pro-oglp-25.10-2190998.e 231 kB/s | 143 kB     00:00
(52/61): libgl-amdgpu-pro-oglp-ext-25.10-21909 199 kB/s | 123 kB     00:00
(53/61): libgl-amdgpu-pro-oglp-gbm-25.10-21909  55 kB/s |  24 kB     00:00
(54/61): libgles-amdgpu-pro-oglp-25.10-2190998  96 kB/s |  45 kB     00:00
(55/61): dkms-3.2.1-1.el8.noarch.rpm           1.3 MB/s |  90 kB     00:00
(56/61): libgl-amdgpu-pro-oglp-dri-25.10-21909 7.2 MB/s |  14 MB     00:01
(57/61): rocm-language-runtime6.4.0-6.4.0.6040  17 kB/s | 7.2 kB     00:00
(58/61): rocm-opencl-runtime6.4.0-6.4.0.60400-  49 kB/s |  11 kB     00:00
(59/61): rocm-opencl6.4.0-2.0.0.60400-47.el8.x 1.1 MB/s | 481 kB     00:00
(60/61): vulkan-amdgpu-pro-25.10-2190998.el8.x  14 MB/s |  32 MB     00:02
(61/61): openmp-extras-runtime6.4.0-18.63.0.60  15 MB/s |  48 MB     00:03
-------------------------------------------------------------------------------
Total                                           18 MB/s | 237 MB     00:13
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                       1/1
  Installing       : amdgpu-pro-core-25.10-2190998.el8.noarch             1/61
  Running scriptlet: amdgpu-pro-core-25.10-2190998.el8.noarch             1/61
  Installing       : mesa-amdgpu-filesystem-1:25.0.0.60402-2187269.el8    2/61
  Installing       : libwayland-amdgpu-client-1.23.0.60402-2187269.el8    3/61
  Running scriptlet: libwayland-amdgpu-client-1.23.0.60402-2187269.el8    3/61
  Installing       : libgl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64       4/61
  Running scriptlet: libgl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64       4/61
  Installing       : libwayland-amdgpu-server-1.23.0.60402-2187269.el8    5/61
  Running scriptlet: libwayland-amdgpu-server-1.23.0.60402-2187269.el8    5/61
  Installing       : llvm-amdgpu-libs-1:19.1.60402-2187269.el8.x86_64     6/61
  Running scriptlet: llvm-amdgpu-libs-1:19.1.60402-2187269.el8.x86_64     6/61
  Installing       : mesa-amdgpu-libgallium-1:25.0.0.60402-2187269.el8    7/61
  Running scriptlet: mesa-amdgpu-libgallium-1:25.0.0.60402-2187269.el8    7/61
  Installing       : mesa-amdgpu-libgbm-1:25.0.0.60402-2187269.el8.x86    8/61
  Running scriptlet: mesa-amdgpu-libgbm-1:25.0.0.60402-2187269.el8.x86    8/61
  Installing       : libgl-amdgpu-pro-oglp-gbm-25.10-2190998.el8.x86_6    9/61
  Installing       : mesa-amdgpu-libGL-1:25.0.0.60402-2187269.el8.x86_   10/61
  Running scriptlet: mesa-amdgpu-libGL-1:25.0.0.60402-2187269.el8.x86_   10/61
  Installing       : pixman-0.38.4-4.el8.x86_64                          11/61
  Installing       : autoconf-2.69-29.el8_10.1.noarch                    12/61
  Running scriptlet: autoconf-2.69-29.el8_10.1.noarch                    12/61
  Installing       : automake-1.16.1-8.el8.noarch                        13/61
  Running scriptlet: mesa-amdgpu-dri-drivers-1:25.0.0.60402-2187269.el   14/61
  Installing       : mesa-amdgpu-dri-drivers-1:25.0.0.60402-2187269.el   14/61
  Running scriptlet: mesa-amdgpu-dri-drivers-1:25.0.0.60402-2187269.el   14/61
  Installing       : libgl-amdgpu-pro-oglp-dri-25.10-2190998.el8.x86_6   15/61
  Installing       : mesa-amdgpu-libEGL-1:25.0.0.60402-2187269.el8.x86   16/61
  Running scriptlet: mesa-amdgpu-libEGL-1:25.0.0.60402-2187269.el8.x86   16/61
  Running scriptlet: mesa-amdgpu-va-drivers-1:25.0.0.60402-2187269.el8   17/61
  Installing       : mesa-amdgpu-va-drivers-1:25.0.0.60402-2187269.el8   17/61
  Running scriptlet: mesa-amdgpu-va-drivers-1:25.0.0.60402-2187269.el8   17/61
  Running scriptlet: mesa-amdgpu-vdpau-drivers-1:25.0.0.60402-2187269.   18/61
  Installing       : mesa-amdgpu-vdpau-drivers-1:25.0.0.60402-2187269.   18/61
  Running scriptlet: mesa-amdgpu-vdpau-drivers-1:25.0.0.60402-2187269.   18/61
  Installing       : mesa-amdgpu-libxatracker-1:25.0.0.60402-2187269.e   19/61
  Running scriptlet: mesa-amdgpu-libxatracker-1:25.0.0.60402-2187269.e   19/61
  Installing       : libegl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64     20/61
  Running scriptlet: libegl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64     20/61
  Installing       : libgles-amdgpu-pro-oglp-25.10-2190998.el8.x86_64    21/61
  Running scriptlet: libgles-amdgpu-pro-oglp-25.10-2190998.el8.x86_64    21/61
  Installing       : openmp-extras-runtime6.4.0-18.63.0.60400-47.el8.x   22/61
  Installing       : rocm-language-runtime6.4.0-6.4.0.60400-47.el8.x86   23/61
  Installing       : libvdpau-amdgpu-6.4-2187269.el8.x86_64              24/61
  Running scriptlet: libvdpau-amdgpu-6.4-2187269.el8.x86_64              24/61
  Installing       : amdgpu-dkms-firmware-1:6.12.12-2187269.el8.noarch   25/61
  Installing       : patch-2.7.6-11.el8.x86_64                           26/61
  Installing       : dkms-3.2.1-1.el8.noarch                             27/61
  Running scriptlet: dkms-3.2.1-1.el8.noarch                             27/61
  Installing       : amdgpu-dkms-1:6.12.12-2187269.el8.noarch            28/61
  Running scriptlet: amdgpu-dkms-1:6.12.12-2187269.el8.noarch            28/61
Loading new amdgpu/6.12.12-2187269.el8 DKMS files...
Building for 4.18.0-513.24.1.el8_9.x86_64 4.18.0-553.69.1.el8_10.x86_64

Module build for kernel 4.18.0-513.24.1.el8_9.x86_64 was skipped since the
kernel headers for this kernel do not seem to be installed.

Building initial module amdgpu/6.12.12-2187269.el8 for 4.18.0-553.69.1.el8_10.x86_64
Sign command: /lib/modules/4.18.0-553.69.1.el8_10.x86_64/build/scripts/sign-file
Signing key: /var/lib/dkms/mok.key
Public certificate (MOK): /var/lib/dkms/mok.pub
Certificate or key are missing, generating self signed certificate for MOK...

Building module(s)................. done.
Signing module /var/lib/dkms/amdgpu/6.12.12-2187269.el8/build/amd/amdgpu/amdgpu.ko
Signing module /var/lib/dkms/amdgpu/6.12.12-2187269.el8/build/ttm/amdttm.ko
Signing module /var/lib/dkms/amdgpu/6.12.12-2187269.el8/build/amd/amdkcl/amdkcl.ko
Signing module /var/lib/dkms/amdgpu/6.12.12-2187269.el8/build/scheduler/amd-sched.ko
Signing module /var/lib/dkms/amdgpu/6.12.12-2187269.el8/build/./amddrm_ttm_helper.ko
Signing module /var/lib/dkms/amdgpu/6.12.12-2187269.el8/build/./amddrm_buddy.ko
Signing module /var/lib/dkms/amdgpu/6.12.12-2187269.el8/build/amd/amdxcp/amdxcp.ko
Forcing installation of amdgpu
Found pre-existing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.xz, archiving for uninstallation
Installing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/extra/amdgpu.ko.xz
Installing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/extra/amdttm.ko.xz
Installing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/extra/amdkcl.ko.xz
Installing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/extra/amd-sched.ko.xz
Installing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/extra/amddrm_ttm_helper.ko.xz
Installing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/extra/amddrm_buddy.ko.xz
Installing /lib/modules/4.18.0-553.69.1.el8_10.x86_64/extra/amdxcp.ko.xz
Running depmod... done.
Executing post-transaction command........... done.

  Installing       : ocl-icd-2.2.12-1.el8.x86_64                         29/61
  Running scriptlet: ocl-icd-2.2.12-1.el8.x86_64                         29/61
  Installing       : rocm-opencl6.4.0-2.0.0.60400-47.el8.x86_64          30/61
  Running scriptlet: rocm-opencl6.4.0-2.0.0.60400-47.el8.x86_64          30/61
  Installing       : mtdev-1.1.5-12.el8.x86_64                           31/61
  Running scriptlet: mtdev-1.1.5-12.el8.x86_64                           31/61
  Installing       : mesa-filesystem-23.1.4-4.el8_10.x86_64              32/61
  Installing       : libva-amdgpu-2.16.0.60402-2187269.el8.x86_64        33/61
  Running scriptlet: libva-amdgpu-2.16.0.60402-2187269.el8.x86_64        33/61
  Installing       : amdgpu-multimedia-1:6.4.60402-2187269.el8.x86_64    34/61
  Installing       : llvm-compat-libs-17.0.6-3.module+el8.10.0+1875+4f   35/61
  Running scriptlet: llvm-compat-libs-17.0.6-3.module+el8.10.0+1875+4f   35/61
  Installing       : vulkan-loader-1.3.283.0-1.el8_10.x86_64             36/61
  Installing       : mesa-vulkan-drivers-23.1.4-4.el8_10.x86_64          37/61
  Installing       : libxkbfile-1.1.0-1.el8.x86_64                       38/61
  Installing       : xorg-x11-xkb-utils-7.7-28.el8.x86_64                39/61
  Installing       : xorg-x11-server-common-1.20.11-26.el8_10.x86_64     40/61
  Installing       : libwacom-data-1.6-3.el8.noarch                      41/61
  Installing       : libwacom-1.6-3.el8.x86_64                           42/61
  Installing       : libfontenc-1.1.3-8.el8.x86_64                       43/61
  Installing       : libXfont2-2.0.3-2.el8.x86_64                        44/61
  Installing       : libevdev-1.10.0-1.el8.x86_64                        45/61
  Installing       : libinput-1.16.3-3.el8_6.x86_64                      46/61
  Running scriptlet: libinput-1.16.3-3.el8_6.x86_64                      46/61
  Installing       : libepoxy-1.5.8-1.el8.x86_64                         47/61
  Installing       : libXdmcp-1.1.3-1.el8.x86_64                         48/61
  Installing       : xorg-x11-drv-fbdev-0.5.0-2.el8.x86_64               49/61
  Installing       : xorg-x11-drv-libinput-0.29.0-1.el8.x86_64           50/61
  Installing       : xorg-x11-drv-vesa-2.4.0-3.el8.x86_64                51/61
  Installing       : xorg-x11-server-Xorg-1.20.11-26.el8_10.x86_64       52/61
  Installing       : xorg-x11-amdgpu-drv-amdgpu-1:24.1.0-2187269.el8.x   53/61
  Installing       : amdgpu-lib-1:6.4.60402-2187269.el8.x86_64           54/61
  Installing       : amdgpu-1:6.4.60402-2187269.el8.x86_64               55/61
  Installing       : libXdamage-1.1.4-14.el8.x86_64                      56/61
  Installing       : libgl-amdgpu-pro-oglp-ext-25.10-2190998.el8.x86_6   57/61
  Installing       : amdgpu-pro-oglp-25.10-2190998.el8.x86_64            58/61
  Installing       : amdgpu-pro-25.10-2190998.el8.x86_64                 59/61
  Installing       : vulkan-amdgpu-pro-25.10-2190998.el8.x86_64          60/61
  Running scriptlet: vulkan-amdgpu-pro-25.10-2190998.el8.x86_64          60/61
  Installing       : rocm-opencl-runtime6.4.0-6.4.0.60400-47.el8.x86_6   61/61
  Running scriptlet: rocm-opencl-runtime6.4.0-6.4.0.60400-47.el8.x86_6   61/61
  Running scriptlet: vulkan-amdgpu-pro-25.10-2190998.el8.x86_64          61/61
  Running scriptlet: rocm-opencl-runtime6.4.0-6.4.0.60400-47.el8.x86_6   61/61
  Verifying        : autoconf-2.69-29.el8_10.1.noarch                     1/61
  Verifying        : automake-1.16.1-8.el8.noarch                         2/61
  Verifying        : libXdamage-1.1.4-14.el8.x86_64                       3/61
  Verifying        : libXdmcp-1.1.3-1.el8.x86_64                          4/61
  Verifying        : libXfont2-2.0.3-2.el8.x86_64                         5/61
  Verifying        : libepoxy-1.5.8-1.el8.x86_64                          6/61
  Verifying        : libevdev-1.10.0-1.el8.x86_64                         7/61
  Verifying        : libfontenc-1.1.3-8.el8.x86_64                        8/61
  Verifying        : libinput-1.16.3-3.el8_6.x86_64                       9/61
  Verifying        : libwacom-1.6-3.el8.x86_64                           10/61
  Verifying        : libwacom-data-1.6-3.el8.noarch                      11/61
  Verifying        : libxkbfile-1.1.0-1.el8.x86_64                       12/61
  Verifying        : llvm-compat-libs-17.0.6-3.module+el8.10.0+1875+4f   13/61
  Verifying        : mesa-filesystem-23.1.4-4.el8_10.x86_64              14/61
  Verifying        : mesa-vulkan-drivers-23.1.4-4.el8_10.x86_64          15/61
  Verifying        : mtdev-1.1.5-12.el8.x86_64                           16/61
  Verifying        : ocl-icd-2.2.12-1.el8.x86_64                         17/61
  Verifying        : pixman-0.38.4-4.el8.x86_64                          18/61
  Verifying        : vulkan-loader-1.3.283.0-1.el8_10.x86_64             19/61
  Verifying        : xorg-x11-drv-fbdev-0.5.0-2.el8.x86_64               20/61
  Verifying        : xorg-x11-drv-libinput-0.29.0-1.el8.x86_64           21/61
  Verifying        : xorg-x11-drv-vesa-2.4.0-3.el8.x86_64                22/61
  Verifying        : xorg-x11-server-Xorg-1.20.11-26.el8_10.x86_64       23/61
  Verifying        : xorg-x11-server-common-1.20.11-26.el8_10.x86_64     24/61
  Verifying        : xorg-x11-xkb-utils-7.7-28.el8.x86_64                25/61
  Verifying        : patch-2.7.6-11.el8.x86_64                           26/61
  Verifying        : amdgpu-1:6.4.60402-2187269.el8.x86_64               27/61
  Verifying        : amdgpu-dkms-1:6.12.12-2187269.el8.noarch            28/61
  Verifying        : amdgpu-dkms-firmware-1:6.12.12-2187269.el8.noarch   29/61
  Verifying        : amdgpu-lib-1:6.4.60402-2187269.el8.x86_64           30/61
  Verifying        : amdgpu-multimedia-1:6.4.60402-2187269.el8.x86_64    31/61
  Verifying        : libva-amdgpu-2.16.0.60402-2187269.el8.x86_64        32/61
  Verifying        : libvdpau-amdgpu-6.4-2187269.el8.x86_64              33/61
  Verifying        : libwayland-amdgpu-client-1.23.0.60402-2187269.el8   34/61
  Verifying        : libwayland-amdgpu-server-1.23.0.60402-2187269.el8   35/61
  Verifying        : llvm-amdgpu-libs-1:19.1.60402-2187269.el8.x86_64    36/61
  Verifying        : mesa-amdgpu-dri-drivers-1:25.0.0.60402-2187269.el   37/61
  Verifying        : mesa-amdgpu-filesystem-1:25.0.0.60402-2187269.el8   38/61
  Verifying        : mesa-amdgpu-libEGL-1:25.0.0.60402-2187269.el8.x86   39/61
  Verifying        : mesa-amdgpu-libGL-1:25.0.0.60402-2187269.el8.x86_   40/61
  Verifying        : mesa-amdgpu-libgallium-1:25.0.0.60402-2187269.el8   41/61
  Verifying        : mesa-amdgpu-libgbm-1:25.0.0.60402-2187269.el8.x86   42/61
  Verifying        : mesa-amdgpu-libxatracker-1:25.0.0.60402-2187269.e   43/61
  Verifying        : mesa-amdgpu-va-drivers-1:25.0.0.60402-2187269.el8   44/61
  Verifying        : mesa-amdgpu-vdpau-drivers-1:25.0.0.60402-2187269.   45/61
  Verifying        : xorg-x11-amdgpu-drv-amdgpu-1:24.1.0-2187269.el8.x   46/61
  Verifying        : amdgpu-pro-25.10-2190998.el8.x86_64                 47/61
  Verifying        : amdgpu-pro-core-25.10-2190998.el8.noarch            48/61
  Verifying        : amdgpu-pro-oglp-25.10-2190998.el8.x86_64            49/61
  Verifying        : libegl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64     50/61
  Verifying        : libgl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64      51/61
  Verifying        : libgl-amdgpu-pro-oglp-dri-25.10-2190998.el8.x86_6   52/61
  Verifying        : libgl-amdgpu-pro-oglp-ext-25.10-2190998.el8.x86_6   53/61
  Verifying        : libgl-amdgpu-pro-oglp-gbm-25.10-2190998.el8.x86_6   54/61
  Verifying        : libgles-amdgpu-pro-oglp-25.10-2190998.el8.x86_64    55/61
  Verifying        : vulkan-amdgpu-pro-25.10-2190998.el8.x86_64          56/61
  Verifying        : dkms-3.2.1-1.el8.noarch                             57/61
  Verifying        : openmp-extras-runtime6.4.0-18.63.0.60400-47.el8.x   58/61
  Verifying        : rocm-language-runtime6.4.0-6.4.0.60400-47.el8.x86   59/61
  Verifying        : rocm-opencl-runtime6.4.0-6.4.0.60400-47.el8.x86_6   60/61
  Verifying        : rocm-opencl6.4.0-2.0.0.60400-47.el8.x86_64          61/61

Installed:
  amdgpu-1:6.4.60402-2187269.el8.x86_64
  amdgpu-dkms-1:6.12.12-2187269.el8.noarch
  amdgpu-dkms-firmware-1:6.12.12-2187269.el8.noarch
  amdgpu-lib-1:6.4.60402-2187269.el8.x86_64
  amdgpu-multimedia-1:6.4.60402-2187269.el8.x86_64
  amdgpu-pro-25.10-2190998.el8.x86_64
  amdgpu-pro-core-25.10-2190998.el8.noarch
  amdgpu-pro-oglp-25.10-2190998.el8.x86_64
  autoconf-2.69-29.el8_10.1.noarch
  automake-1.16.1-8.el8.noarch
  dkms-3.2.1-1.el8.noarch
  libXdamage-1.1.4-14.el8.x86_64
  libXdmcp-1.1.3-1.el8.x86_64
  libXfont2-2.0.3-2.el8.x86_64
  libegl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64
  libepoxy-1.5.8-1.el8.x86_64
  libevdev-1.10.0-1.el8.x86_64
  libfontenc-1.1.3-8.el8.x86_64
  libgl-amdgpu-pro-oglp-25.10-2190998.el8.x86_64
  libgl-amdgpu-pro-oglp-dri-25.10-2190998.el8.x86_64
  libgl-amdgpu-pro-oglp-ext-25.10-2190998.el8.x86_64
  libgl-amdgpu-pro-oglp-gbm-25.10-2190998.el8.x86_64
  libgles-amdgpu-pro-oglp-25.10-2190998.el8.x86_64
  libinput-1.16.3-3.el8_6.x86_64
  libva-amdgpu-2.16.0.60402-2187269.el8.x86_64
  libvdpau-amdgpu-6.4-2187269.el8.x86_64
  libwacom-1.6-3.el8.x86_64
  libwacom-data-1.6-3.el8.noarch
  libwayland-amdgpu-client-1.23.0.60402-2187269.el8.x86_64
  libwayland-amdgpu-server-1.23.0.60402-2187269.el8.x86_64
  libxkbfile-1.1.0-1.el8.x86_64
  llvm-amdgpu-libs-1:19.1.60402-2187269.el8.x86_64
  llvm-compat-libs-17.0.6-3.module+el8.10.0+1875+4f0b06db.x86_64
  mesa-amdgpu-dri-drivers-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-filesystem-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-libEGL-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-libGL-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-libgallium-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-libgbm-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-libxatracker-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-va-drivers-1:25.0.0.60402-2187269.el8.x86_64
  mesa-amdgpu-vdpau-drivers-1:25.0.0.60402-2187269.el8.x86_64
  mesa-filesystem-23.1.4-4.el8_10.x86_64
  mesa-vulkan-drivers-23.1.4-4.el8_10.x86_64
  mtdev-1.1.5-12.el8.x86_64
  ocl-icd-2.2.12-1.el8.x86_64
  openmp-extras-runtime6.4.0-18.63.0.60400-47.el8.x86_64
  patch-2.7.6-11.el8.x86_64
  pixman-0.38.4-4.el8.x86_64
  rocm-language-runtime6.4.0-6.4.0.60400-47.el8.x86_64
  rocm-opencl-runtime6.4.0-6.4.0.60400-47.el8.x86_64
  rocm-opencl6.4.0-2.0.0.60400-47.el8.x86_64
  vulkan-amdgpu-pro-25.10-2190998.el8.x86_64
  vulkan-loader-1.3.283.0-1.el8_10.x86_64
  xorg-x11-amdgpu-drv-amdgpu-1:24.1.0-2187269.el8.x86_64
  xorg-x11-drv-fbdev-0.5.0-2.el8.x86_64
  xorg-x11-drv-libinput-0.29.0-1.el8.x86_64
  xorg-x11-drv-vesa-2.4.0-3.el8.x86_64
  xorg-x11-server-Xorg-1.20.11-26.el8_10.x86_64
  xorg-x11-server-common-1.20.11-26.el8_10.x86_64
  xorg-x11-xkb-utils-7.7-28.el8.x86_64

Complete!
```


---

### 评论 #5 — harkgill-amd (2025-08-26T20:06:29Z)

Hi @bartvdbraak, the 6.4.2 PRO drivers/packages have been uploaded to https://repo.radeon.com/amdgpu/6.4.2/rhel/8.10/proprietary/x86_64/ and the install now works correctly with your command,
```
amdgpu-install --usecase=workstation -y --vulkan=pro --opencl=rocr --opengl=mesa --accept-eula
```
I omitted the `--rocmrelease=6.4.0`  - is there any reason as to why you need this flag while using the 6.4.2 installer?

---

### 评论 #6 — bartvdbraak (2025-08-27T13:22:25Z)

@harkgill-amd Thank you for the update. I will close the issues since it is resolved 👍 

As for the ROCm flag, that was just something we needed in addition to the Pro drivers, not related to this issue per se.

---
