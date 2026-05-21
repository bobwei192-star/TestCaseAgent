# [Issue]: pytorch issue with AMD Radeon 7700S (Framework Laptop 16")

> **Issue #4375**
> **状态**: closed
> **创建时间**: 2025-02-14T13:41:05Z
> **更新时间**: 2025-03-03T14:31:30Z
> **关闭时间**: 2025-03-03T14:31:29Z
> **作者**: gianpaj
> **标签**: Under Investigation, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4375

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

Can anybody shed a light on this? I'm having similar issues with `pytorch`

The python script from https://community.frame.work/t/amd-rocm-for-local-training-and-inferencing/58377/3?u=gianfranco_palumbo fails on `torch.cuda.is_available()` when I run it:

```bash
$ poetry run python3 checkrocm.py

Checking ROCM support...
GOOD: ROCM devices found: 2
Checking PyTorch...
GOOD: PyTorch is working fine.
Checking user groups...
GOOD: The user gianpa is in `render` and `video` groups.
BAD: PyTorch ROCM support NOT found.
```

I installed `pytorch` using the steps on https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html specifically:
- `pytorch_triton_rocm-3.1.0+rocm6.3.2.b253a53766-cp310-cp310-linux_x86_64.whl`
- `torch-2.5.1+rocm6.3.2-cp310-cp310-linux_x86_64.whl`

Newer versions of the Ubuntu kernel didn't load the login screen.

Thanks a lot :pray: 

### Operating System

24.04.2 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 7940HS w/ Radeon 780M Graphics

### GPU

AMD Ryzen 9 7940HS w/ Radeon 780M Graphics

### ROCm Version

ROCm 6.3.2

### ROCm Component

_No response_

### Steps to Reproduce

The python script from https://community.frame.work/t/amd-rocm-for-local-training-and-inferencing/58377/3?u=gianfranco_palumbo fails on `torch.cuda.is_available()` when I run it

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

<details><summary>rocminfo</summary>
<p>

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
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 9 7940HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 7940HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5743
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
      Size:                    63580336(0x3ca28b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    63580336(0x3ca28b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    63580336(0x3ca28b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    63580336(0x3ca28b0) KB
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
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon™ RX 7700S
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
  Chip ID:                 29824(0x7480)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2208
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            32
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
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 550
  SDMA engine uCode::      16
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
*** Done ***
```

</p>
</details>

<details><summary>rocm-smi</summary>
<p>

```
============================================= ROCm System Management Interface =============================================
======================================================= Concise Info =======================================================
Device  Node  IDs              Temp    Power    Partitions          SCLK    MCLK     Fan    Perf  PwrCap       VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Avg)    (Mem, Compute, ID)
============================================================================================================================
0       1     0x7480,   19047  33.0°C  25.0W    N/A, N/A, 0         808Mhz  456Mhz   29.8%  auto  100.0W       0%     0%
1       2     0x15bf,   11294  36.0°C  27.178W  N/A, N/A, 0         None    2800Mhz  0%     auto  Unsupported  17%    0%
============================================================================================================================
=================================================== End of ROCm SMI Log ====================================================
```

</p>
</details>

Info
```
Framework 16"

$ uname -a
Linux gianpa-frm16 6.8.0-48-generic #48-Ubuntu SMP PREEMPT_DYNAMIC Fri Sep 27 14:04:52 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

$ echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
OS:
NAME="Ubuntu"
VERSION="24.04.2 LTS (Noble Numbat)"
```


### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-02-14T16:21:10Z)

Hi @gianpaj. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-02-14T16:56:23Z)

Hi @gianpaj, thanks for reaching out! Unfortunately, ROCm 6.3.2 is not supported for ROCm on Radeon software. The latest supported version is 6.2.3. Please try to install it with the following commands:

```
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/torch-2.3.0%2Brocm6.2.3-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/torchvision-0.18.0%2Brocm6.2.3-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/pytorch_triton_rocm-2.3.0%2Brocm6.2.3.5a02332983-cp310-cp310-linux_x86_64.whl
pip3 uninstall torch torchvision pytorch-triton-rocm
pip3 install torch-2.3.0+rocm6.2.3-cp310-cp310-linux_x86_64.whl torchvision-0.18.0+rocm6.2.3-cp310-cp310-linux_x86_64.whl pytorch_triton_rocm-2.3.0+rocm6.2.3.5a02332983-cp310-cp310-linux_x86_64.whl
```

If this still doesn't work, I recommend trying `Option B: Docker installation` on https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html and see if that works so we can isolate the problem. 
Thanks! 

---

### 评论 #3 — tcgu-amd (2025-02-19T14:06:17Z)

Hey @gianpaj, just checking if you still requires help with this issue. Thanks! 

---

### 评论 #4 — tcgu-amd (2025-03-03T14:31:29Z)

Hi @gianpaj, I will be closing this issue for now due to inactivity; however, please feel free to follow up with more questions below. Thanks! 

---
