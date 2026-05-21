# [Issue]: rocminfo - Unable to open /dev/kfd read-write: Invalid argument

> **Issue #5379**
> **状态**: closed
> **创建时间**: 2025-09-18T11:35:06Z
> **更新时间**: 2025-09-19T19:45:36Z
> **关闭时间**: 2025-09-19T19:45:36Z
> **作者**: AndreasMurk
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5379

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- harkgill-amd

## 描述

### Problem Description

NAME="Ubuntu"
VERSION="24.04 LTS (Noble Numbat)"
CPU:
model name      : AMD Ryzen 7 9700X 8-Core Processor
GPU:


### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen 7 9700X

### GPU

AMD 9070 XT

### ROCm Version

ROCm 7.0.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
root@gpu-test-2:~#  /opt/rocm/bin/rocminfo --support
ROCk module is loaded
Unable to open /dev/kfd read-write: Invalid argument
root is member of render group
```

Hi! I'm facing issues on setting up ROCm with an unprivileged LXC Container under Proxmox with latest ROCm 7.0.1 and AMD 9070 XT. I have passed through my GPU using working tutorials.

I have the right permissions set already (root is both in video and render group).

```
root@gpu-test-2:~# groups
root video render
```

I can see both /dev/kfd and /dev/dri*:

```
root@gpu-test-2:~# ls -la /dev/kfd /dev/dri*
crw-rw-rw- 1 root render 511, 0 Sep 18 11:04 /dev/kfd

/dev/dri:
total 0
drwxr-xr-x 2 root root        80 Sep 18 11:04 .
drwxr-xr-x 7 root root       520 Sep 18 11:04 ..
crw-rw---- 1 root video 226, 128 Sep 18 11:04 renderD128
crw-rw---- 1 root video 226, 129 Sep 18 11:04 renderD129
```

I have installed it using the [official instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)

I'm running Ubuntu 24.04 with Kernel 6.14.11-1:

```
root@gpu-test-2:~# uname -srmv
Linux 6.14.11-1-pve #1 SMP PREEMPT_DYNAMIC PMX 6.14.11-1 (2025-08-26T16:06Z) x86_64
root@gpu-test-2:~# uname -m && cat /etc/*release
x86_64
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04 LTS"
PRETTY_NAME="Ubuntu 24.04 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
```

However, whenever I'm trying to access it using rocminfo I keep getting:

```
root@gpu-test-2:~# rocminfo
ROCk module is loaded
Unable to open /dev/kfd read-write: Invalid argument
root is member of render group
```

**On the host:** AMD Gpu information:

```
➜  ~ dmesg | grep amdgpu
[229101.186133] amdgpu 0000:03:00.0: amdgpu: detected ip block number 0 <soc24_common>
[229101.186136] amdgpu 0000:03:00.0: amdgpu: detected ip block number 1 <gmc_v12_0>
[229101.186138] amdgpu 0000:03:00.0: amdgpu: detected ip block number 2 <ih_v7_0>
[229101.186139] amdgpu 0000:03:00.0: amdgpu: detected ip block number 3 <psp>
[229101.186140] amdgpu 0000:03:00.0: amdgpu: detected ip block number 4 <smu>
[229101.186142] amdgpu 0000:03:00.0: amdgpu: detected ip block number 5 <dm>
[229101.186143] amdgpu 0000:03:00.0: amdgpu: detected ip block number 6 <gfx_v12_0>
[229101.186144] amdgpu 0000:03:00.0: amdgpu: detected ip block number 7 <sdma_v7_0>
[229101.186146] amdgpu 0000:03:00.0: amdgpu: detected ip block number 8 <vcn_v5_0_0>
[229101.186147] amdgpu 0000:03:00.0: amdgpu: detected ip block number 9 <jpeg_v5_0_0>
[229101.186148] amdgpu 0000:03:00.0: amdgpu: detected ip block number 10 <mes_v12_0>
[229101.186167] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from VFCT
[229101.186169] amdgpu: ATOM BIOS: 113-EXT112414-100
[229101.194722] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[229101.194751] amdgpu 0000:03:00.0: amdgpu: MEM ECC is not presented.
[229101.194753] amdgpu 0000:03:00.0: amdgpu: SRAM ECC is not presented.
[229101.194774] amdgpu 0000:03:00.0: amdgpu: VRAM: 16304M 0x0000008000000000 - 0x00000083FAFFFFFF (16304M used)
[229101.194776] amdgpu 0000:03:00.0: amdgpu: GART: 512M 0x0000000000000000 - 0x000000001FFFFFFF
[229101.194824] [drm] amdgpu: 16304M of VRAM memory ready
[229101.194825] [drm] amdgpu: 30946M of GTT memory ready.
[229101.194881] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x00000083DAB00000).
[229101.484377] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[229101.484382] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[229101.484411] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684a00 (104.74.0)
[229101.484414] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[229101.510355] amdgpu 0000:03:00.0: amdgpu: SMU is initialized successfully!
[229101.531843] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
[229101.531848] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
[229101.578354] amdgpu: HMM registered 16304MB device memory
[229101.579309] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[229101.579322] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[229101.579352] amdgpu: Virtual CRAT table created for GPU
[229101.579458] amdgpu: Topology: Add dGPU node [0x7550:0x1002]
[229101.579460] kfd kfd: amdgpu: added device 1002:7550
[229101.579468] amdgpu 0000:03:00.0: amdgpu: SE 4, SH per SE 2, CU per SH 8, active_cu_number 64
[229101.579472] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[229101.579473] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[229101.579475] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[229101.579476] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
[229101.579477] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
[229101.579478] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
[229101.579479] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
[229101.579480] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[229101.579481] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[229101.586331] amdgpu 0000:03:00.0: amdgpu: Using BACO for runtime pm
[229101.586618] amdgpu 0000:03:00.0: [drm] Registered 4 planes with drm panic
[229101.586620] [drm] Initialized amdgpu 3.61.0 for 0000:03:00.0 on minor 0
[229101.590644] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[229594.873445] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x00000083DAB00000).
[229594.873467] amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
[229595.075149] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[229595.075153] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[229595.075155] amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
[229595.075158] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684a00 (104.74.0)
[229595.075161] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[229595.088738] amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
[229595.088896] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
[229595.088898] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
[229595.106172] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[229595.106177] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[229595.106178] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[229595.106180] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[229595.106181] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
[229595.106181] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
[229595.106182] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
[229595.106184] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
[229595.106185] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[229595.106186] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[229595.111686] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[229609.024239] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x00000083DAB00000).
[229609.024265] amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
[229609.226191] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[229609.226194] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[229609.226197] amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
[229609.226199] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684a00 (104.74.0)
[229609.226202] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[229609.240221] amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
[229609.240376] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
[229609.240380] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
[229609.257105] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[229609.257110] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[229609.257112] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[229609.257113] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[229609.257114] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
[229609.257115] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
[229609.257116] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
[229609.257117] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
[229609.257118] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[229609.257120] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[229609.261733] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[230037.912351] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x00000083DAB00000).
[230037.912378] amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
[230038.113546] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[230038.113553] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[230038.113556] amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
[230038.113560] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684a00 (104.74.0)
[230038.113563] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[230038.126687] amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
[230038.126842] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000
[230038.126845] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000
[230038.143671] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[230038.143682] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[230038.143684] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[230038.143686] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[230038.143688] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0
[230038.143689] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0
[230038.143691] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0
[230038.143692] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0
[230038.143694] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[230038.143695] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[230038.147220] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
```

I am clueless and this point unfortunately. Thanks for any help!

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-09-18T20:49:52Z)

Hi @AndreasMurk, do you have GPU access on your host machine - are you able to run commands such as `rocminfo` and `rocm-smi`?

Could you also please share the steps you followed to setup/launch your container?

---

### 评论 #2 — AndreasMurk (2025-09-19T07:31:52Z)

Hi @harkgill-amd, thank you for your fast response.

The issue seems to be resolved.

There is an ongoing error with newer AMD 9000 series GPUs where it gets stuck when passing it down a VM and back to the host. After a reboot, it seems to work now:

<details>
<summary>Click to expand</summary>

```
root@gpu-test-2:~# rocminfo
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:
  Uuid:                    CPU-XX
  Marketing Name:
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
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5582
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
      Size:                    63378528(0x3c71460) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    63378528(0x3c71460) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    63378528(0x3c71460) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    63378528(0x3c71460) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1201
  Uuid:                    GPU-2f987739463f9020
  Marketing Name:          AMD Radeon RX 9070 XT
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
    L2:                      8192(0x2000) KB
    L3:                      65536(0x10000) KB
  Chip ID:                 30032(0x7550)
  ASIC Revision:           1(0x1)
  Cacheline Size:          256(0x100)
  Max Clock Freq. (MHz):   2520
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            64
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
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 58
  SDMA engine uCode::      380
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16695296(0xfec000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1201
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx12-generic
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
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
  Chip ID:                 5056(0x13c0)
  ASIC Revision:           1(0x1)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2200
  BDFID:                   31488
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
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 22
  SDMA engine uCode::      9
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    31689264(0x1e38a30) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31689264(0x1e38a30) KB
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*** Done ***
```
</details>

Thank you very much!

---

### 评论 #3 — harkgill-amd (2025-09-19T19:45:36Z)

Glad to hear you got it working on your end! Will close this issue out for now but feel free to leave a comment if you encounter any further issues.

---
