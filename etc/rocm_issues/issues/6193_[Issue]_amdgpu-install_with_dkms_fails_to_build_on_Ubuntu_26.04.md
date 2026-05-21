# [Issue]: amdgpu-install with dkms fails to build on Ubuntu 26.04

> **Issue #6193**
> **状态**: open
> **创建时间**: 2026-04-29T21:47:31Z
> **更新时间**: 2026-05-11T19:34:19Z
> **作者**: robegan21
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6193

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

I understand this is not a supported kernel yet, but I hope this report will assist in adopting the most recent version of Ubuntu LTS.  

TL;DR 
  this breaks: "amdgpu-install -y"
  this works: "amdgpu-install -y --usecase=rocm --no-dkms"

Here is the setup config:

OS:
NAME="Ubuntu"
VERSION="26.04 (Resolute Raccoon)"
CPU:
model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151
  Marketing Name:          AMD Radeon Graphics
      Name:                    amdgcn-amd-amdhsa--gfx1151
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
  Name:                    aie2p
  Marketing Name:          RyzenAI-npu5

uname reports:
Linux rog 7.0.0-14-generic #14-Ubuntu SMP PREEMPT_DYNAMIC Mon Apr 13 11:09:53 UTC 2026 x86_64 GNU/Linux

When running amdgpu-install per the directions (https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html)

   wget https://repo.radeon.com/amdgpu-install/7.2.1/ubuntu/noble/amdgpu-install_7.2.1.70201-1_all.deb
   sudo apt install ./amdgpu-install_7.2.1.70201-1_all.deb
   amdgpu-install

it downloads and starts installing many packages and then breaks when building the dkms and leaves the system in a partial state of installation.
...
update-alternatives: using /opt/rocm-7.2.1/bin/clinfo to provide /usr/bin/clinfo (clinfo) in auto mode
Setting up g++-multilib (4:15.2.0-5ubuntu1)…
Processing triggers for man-db (2.13.1-1build1)…
Processing triggers for install-info (7.2-5ubuntu2)…
Processing triggers for base-files (14ubuntu6)…
Processing triggers for libc-bin (2.43-2ubuntu2)…
Processing triggers for systemd (259.5-0ubuntu3)…
Processing triggers for initramfs-tools (0.151ubuntu1)…
update-initramfs: Generating /boot/initrd.img-7.0.0-14-generic
Errors were encountered while processing:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)


When attempted again, it gets a little farther and prints more information:

Setting up amdgpu-dkms (1:6.16.13.30300100-2303411.24.04)…
Removing old amdgpu/6.16.13-2303411.24.04 DKMS files...
Deleting module amdgpu/6.16.13-2303411.24.04 completely from the DKMS tree.
Loading new amdgpu/6.16.13-2303411.24.04 DKMS files...
Building for 7.0.0-14-generic
Building for architecture x86_64

Building initial module amdgpu/6.16.13-2303411.24.04 for 7.0.0-14-generic
Sign command: /usr/bin/kmodsign
Signing key: /var/lib/shim-signed/mok/MOK.priv
Public certificate (MOK): /var/lib/shim-signed/mok/MOK.der

Building module(s)......(bad exit status: 2)
Failed command:
'make' KERNELVER=7.0.0-14-generic
/usr/share/apport/package-hooks/dkms_packages.py:101: DeprecationWarning: apport.fatal() is deprecated. Please use apport.logging.fatal() directly instead.
  apport.fatal('Cannot create report: ' + str(e))
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.crash'

Error! Bad return status for module build on kernel: 7.0.0-14-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.16.13-2303411.24.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 old amdgpu-dkms package postinst maintainer script subprocess failed with exit status 10
Errors were encountered while processing:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)


Then if you look through that log, this looks like mostly just gcc-15 compiler errors and/or deprecated coding patterns and/or incorrect function calls with the 7.0.0 Linux kernel:


# grep error /var/lib/dkms/amdgpu/6.16.13-2303411.24.04/build/make.log|sort | uniq -c
      1 amd/amdgpu/amdgpu_device.c:1752:13: error: too few arguments to function ‘pci_resize_resource’; expected 4, have 3
      1 amd/amdgpu/amdgpu_device.c:5345:17: error: too many arguments to function ‘drm_client_dev_suspend’; expected 1, have 2
      1 amd/amdgpu/amdgpu_device.c:5410:17: error: too many arguments to function ‘drm_client_dev_resume’; expected 1, have 2
      1 amd/amdgpu/amdgpu_device.c:5531:17: error: too many arguments to function ‘drm_client_dev_resume’; expected 1, have 2
      1 amd/amdgpu/amdgpu_device.c:6138:33: error: too many arguments to function ‘drm_client_dev_resume’; expected 1, have 2
      1 amd/amdgpu/amdgpu_device.c:6476:17: error: too many arguments to function ‘drm_client_dev_suspend’; expected 1, have 2
      1 amd/amdkcl/kcl_mm.c:23:6: error: conflicting types for ‘zone_device_page_init’; have ‘void(struct page *)’
      1 amd/amdkcl/kcl_mm.c:31:19: error: conflicting types for ‘zone_device_page_init’; have ‘void(struct page *)’
     24 ././include/kcl/kcl_dma_mapping.h:134:34: error: ‘const struct dma_map_ops’ has no member named ‘map_resource’
     26 ././include/kcl/kcl_mm.h:31:6: error: conflicting types for ‘zone_device_page_init’; have ‘void(struct page *)’
     10 ././include/kcl/kcl_preempt.h:57:29: error: static declaration of ‘migrate_disable’ follows non-static declaration
     10 ././include/kcl/kcl_preempt.h:61:29: error: static declaration of ‘migrate_enable’ follows non-static declaration
      1 ttm/ttm_backup.c:196:59: error: incompatible type for argument 3 of ‘shmem_file_setup’
      1 ttm/ttm_tt.c:336:59: error: incompatible type for argument 3 of ‘shmem_file_setup’
      1 /usr/src/linux-headers-7.0.0-14-generic/include/drm/drm_client_event.h:14:6: error: conflicting types for ‘drm_client_dev_suspend’; have ‘void(struct drm_device *)’
      1 /usr/src/linux-headers-7.0.0-14-generic/include/drm/drm_client_event.h:15:6: error: conflicting types for ‘drm_client_dev_resume’; have ‘void(struct drm_device *)’


My temporary hack to fix this was to back out the bad dkms build and its partial install and then install rocm without dkms, and that worked fine:

apt autoremove amdgpu-dkms dkms
apt install dkms
amdgpu-install -y --usecase=rocm --no-dkms

### Operating System

Ubuntu 26.04 (Resolute Raccoon)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

7.2.1

### ROCm Component

_No response_

### Steps to Reproduce

wget https://repo.radeon.com/amdgpu-install/7.2.1/ubuntu/noble/amdgpu-install_7.2.1.70201-1_all.deb
   sudo apt install ./amdgpu-install_7.2.1.70201-1_all.deb
   amdgpu-install -y || amdgpu-install -y

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

$  /opt/rocm/bin/rocminfo --support
ROCk module is loaded

  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5187
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
      Size:                    128135340(0x7a330ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    128135340(0x7a330ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    128135340(0x7a330ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    128135340(0x7a330ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1151
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
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 34
  SDMA engine uCode::      18
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    114294784(0x6d00000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    114294784(0x6d00000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1151
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PRO
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*******
Agent 3
*******
  Name:                    aie2p
  Uuid:                    AIE-XX
  Marketing Name:          RyzenAI-npu5
  Vendor Name:             AMD
  Feature:                 AGENT_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        1(0x1)
  Queue Min Size:          64(0x40)
  Queue Max Size:          64(0x40)
  Queue Type:              SINGLE
  Node:                    0
  Device Type:             DSP
  Cache Info:
    L2:                      2048(0x800) KB
    L3:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          0(0x0)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            0
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:0
  Memory Properties:
  Features:                AGENT_DISPATCH
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    128135340(0x7a330ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65536(0x10000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    128135340(0x7a330ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — w-sky (2026-05-11T13:34:21Z)

Yes @rocmteam please try to fix this. We need full support for current OS versions and the 7.0 kernel.

---

### 评论 #2 — lucbruni-amd (2026-05-11T19:34:10Z)

>I understand this is not a supported kernel yet, but I hope this report will assist in adopting the most recent version of Ubuntu LTS.

Acknowledging this statement while also providing the [Linux compatibility](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems) documentation so others are informed and aware of this as well.

> TL;DR
> this breaks: "amdgpu-install -y"
> this works: "amdgpu-install -y --usecase=rocm --no-dkms"
...
> GPU:
> Name: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

This is expected for APUs. See the [Set up ROCm Usecase](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#set-up-rocm-usecase) section of the documentation you linked.

Now, regarding the main issue at hand - this is known, but your report does serve well for awareness and tracking purposes and is appreciated. The kernel base in the latest amdgpu release (see package nomenclature [here](https://repo.radeon.com/amdgpu/31.20/ubuntu/pool/main/a/amdgpu-dkms/), as an example - which shows a kernel base version of 6.19) corresponds with the latest supported kernel. Supporting newer kernels is not common because we rebase the whole kernel compatibility layer on the upstream Linux kernel every time, and backporting is strenuous.

When there are updates, I'll update this issue.

---
