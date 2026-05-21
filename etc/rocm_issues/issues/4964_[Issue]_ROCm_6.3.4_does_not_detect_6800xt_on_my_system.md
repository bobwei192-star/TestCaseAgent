# [Issue]: ROCm 6.3.4 does not detect 6800xt on my system//

> **Issue #4964**
> **状态**: closed
> **创建时间**: 2025-06-24T22:58:07Z
> **更新时间**: 2025-06-25T14:20:50Z
> **关闭时间**: 2025-06-25T14:20:50Z
> **作者**: AbhiMayadam
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4964

## 描述

### Problem Description

After installing amdgpu drivers (amdgpu-install_6.3.60304-1_all.deb) and installing it with wsl and rocm, rocminfo does not report an Agent 2 with my 6800XT, only my CPU. I am running Adrenalin 25.6.1 on Windows 11. 

### Operating System

Ubuntu 24.04.02 LTS (Noble Numbat) with WSL2

### CPU

Intel Core i9-9900KF

### GPU

AMD Radeon RX 6800XT

### ROCm Version

ROCm 6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

1. Install amdgpu drivers in WSL.
2. Run rocminfo

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
  Name:                    Intel(R) Core(TM) i9-9900KF CPU @ 3.60GHz
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i9-9900KF CPU @ 3.60GHz
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
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    16341176(0xf958b8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16341176(0xf958b8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16341176(0xf958b8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16341176(0xf958b8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
```

### Additional Information

https://github.com/ROCm/ROCm/issues/4659 seems to have the same issue as me, but different CPU and GPU. 

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-06-25T14:20:50Z)

Hi @AbhiMayadam, the 6800XT is not supported for use with ROCm on WSL and as a result will not be detected/function correctly if used in this environment. This usually manifests in the form of a `WSL environment detected. ROCR: unsupported GPU` error though in either case, the result is the same. 

You can find the list of supported GPUs over at the [WSL compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix).


---
