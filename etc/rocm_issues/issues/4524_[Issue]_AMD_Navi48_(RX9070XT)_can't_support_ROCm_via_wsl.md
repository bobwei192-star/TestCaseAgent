# [Issue]: AMD Navi48 (RX9070XT) can't support ROCm via wsl

> **Issue #4524**
> **状态**: closed
> **创建时间**: 2025-03-24T07:06:08Z
> **更新时间**: 2025-03-24T14:04:07Z
> **关闭时间**: 2025-03-24T14:04:06Z
> **作者**: littleyellowwolf
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4524

## 描述

### Problem Description

GPU: AMD Navi48 XT (RX9070XT OC)
OS: WSL (ubuntu 22.04) in win11
Issue: After I install the driver, the wsl can't find the graphic card when we use rocminfo to check the device.

Step:
1. sudo apt update
2. wget https://repo.radeon.com/amdgpu-install/6.3.4/ubuntu/jammy/amdgpu-install_6.3.60304-1_all.deb
3. sudo apt install ./amdgpu-install_6.3.60304-1_all.deb
4. amdgpu-install -y --usecase=wsl,rocm --no-dkms
5. rocminfo

And it only shows that:
lab@PLUA9VQN:/mnt/c/Users/lab$ rocminfo
WSL environment detected.
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
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
  Name:                    Intel(R) Core(TM) i9-14900K
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i9-14900K
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
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            32
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32733000(0x1f37748) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32733000(0x1f37748) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32733000(0x1f37748) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32733000(0x1f37748) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***


### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

Intel(R) Core(TM) i9-14900K

### GPU

AMD RX9070XT

### ROCm Version

ROCm 6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-03-24T14:04:06Z)

Hi @littleyellowwolf, this is expected as the 9000 series GPUs are not yet supported for use in WSL.

---
