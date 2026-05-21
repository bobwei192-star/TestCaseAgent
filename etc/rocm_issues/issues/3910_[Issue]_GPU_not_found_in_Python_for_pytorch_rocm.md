# [Issue]: GPU not found in Python for pytorch rocm

> **Issue #3910**
> **状态**: closed
> **创建时间**: 2024-10-16T16:37:51Z
> **更新时间**: 2024-11-11T16:27:54Z
> **关闭时间**: 2024-11-11T16:27:54Z
> **作者**: Loungagna
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3910

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

After successfully installing the pytorch rocm package (`https://download.pytorch.org/whl/nightly/rocm6.2/torch-2.6.0.dev20241016%2Brocm6.2-cp312-cp312-linux_x86_64.whl)`, any test of `torch.cuda.is_available()` fails.

rocminfo works fine, all tests from the CLI works fine for ROCM and HIP.
python version is set via mise.

### Operating System

24.04.1 LTS (Noble Numbat)

### CPU

AMD Ryzen 7 7840HS w/ Radeon 780M Graphics

### GPU

Marketing Name:          AMD Radeon Graphics       Name:                    amdgcn-amd-amdhsa--gfx1102

### ROCm Version

ROCm 6.2.2

### ROCm Component

_No response_

### Steps to Reproduce

`python3

import torch
print(torch.cuda.is_available())`

gives
`False`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5137
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
      Size:                    32147684(0x1ea88e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32147684(0x1ea88e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32147684(0x1ea88e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1102
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
    L1:                      32(0x20) KB
    L2:                      2048(0x800) KB
  Chip ID:                 5567(0x15bf)
  ASIC Revision:           9(0x9)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2700
  BDFID:                   50176
  Internal Node ID:        2
  Compute Unit:            12
  SIMDs per CU:            2
  Shader Engines:          1
  Shader Arrs. per Eng.:   2
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
  Packet Processor uCode:: 39
  SDMA engine uCode::      18
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16073840(0xf54470) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16073840(0xf54470) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1102
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

### Additional Information

If I need to submit this issue somewhere else, please let me know.

Thank you very much for all the effort.

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2024-10-16T16:47:11Z)

Hi @Loungagna. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — Loungagna (2024-10-16T18:17:34Z)

BTW, I verified that I'm hitting rocm pytorch with:

```
>>> import torch
>>> print(torch.__version__)
2.6.0.dev20241016+rocm6.2
```

---

### 评论 #3 — harkgill-amd (2024-10-21T20:22:45Z)

Hi @Loungagna, I was not able to reproduce this issue on both a baremetal Pytorch installation and using the rocm/pytorch docker image ([Installation Steps](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-a-wheels-package)). My setup involved a Navi33/RX 7600 dGPU which is a similar ISA as the Radeon 780M Graphics. 

For reference, the torch version on my local install is `2.6.0.dev20241021+rocm6.2` and within the docker container is `2.3.0a0+gitd2f9472`. Could you please give both of these methods a try and report back?


---

### 评论 #4 — taylding-amd (2024-11-11T16:27:54Z)

Hi, this issue will be closed now due to inactivity. Please feel free to reopen it or ask follow-up questions should further assistance be required. Thanks!

---
