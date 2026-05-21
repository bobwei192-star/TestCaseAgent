# [Issue]: RX 9070 XT ROCm via WSL is not working

> **Issue #4490**
> **状态**: closed
> **创建时间**: 2025-03-13T09:27:51Z
> **更新时间**: 2025-06-04T12:05:56Z
> **关闭时间**: 2025-03-13T13:49:43Z
> **作者**: triforcely
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4490

## 描述

### Problem Description

System info:
```
# Linux (WSL)
NAME="Ubuntu"
VERSION="24.04.1 LTS (Noble Numbat)"
CPU:
model name      : AMD Ryzen 7 5800X3D 8-Core Processor
GPU:
  Name:                    AMD Ryzen 7 5800X3D 8-Core Processor
  Marketing Name:          AMD Ryzen 7 5800X3D 8-Core Processor

# Windows
10.0.22631
AMD Ryzen 7 5800X3D 8-Core Processor
Microsoft Remote Display Adapter
AMD Radeon RX 9070 XT
```

I can't get the ROCm to work on my Windows PC with WSL. I followed this guide: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html and the GPU is not detected in `rocminfo`
I'm running driver version 25.3.1 on Windows.





### Operating System

24.04.1 LTS (Noble Numbat)

### CPU

5800X3D

### GPU

RX 9070 XT

### ROCm Version

6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
 /opt/rocm/bin/rocminfo --support
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
  Name:                    AMD Ryzen 7 5800X3D 8-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 5800X3D 8-Core Processor
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
      Size:                    16329040(0xf92950) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16329040(0xf92950) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16329040(0xf92950) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16329040(0xf92950) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
```

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — harkgill-amd (2025-03-13T13:49:43Z)

Hi @triforcely, the 9000 series GPUs are not yet supported for use with ROCm on WSL. 

---

### 评论 #2 — triforcely (2025-03-13T14:06:40Z)

Hey @harkgill-amd, what is the planned release date for 9000 series support?

---

### 评论 #3 — Bestfast (2025-03-16T18:45:52Z)

I'm also interested in this. Is there a known date?

---

### 评论 #4 — leovanalphen (2025-04-01T01:33:42Z)

How is this still not supported?

---

### 评论 #5 — aleksandrtk (2025-04-07T18:40:16Z)

@harkgill-amd, any updates please?

---

### 评论 #6 — jammm (2025-06-04T11:43:42Z)

@Bestfast @leovanalphen @aleksandrtk @triforcely if any of y'all are trying to run pytorch on windows native (not WSL2), try these unofficial wheels https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x

it comes bundled with ROCm and should technically support gfx1201. It was built using [TheRock ](https://github.com/ROCm/TheRock)

Note that these wheels are unofficial, is in active development, and there might still be issues. I don't recommend trying this if you're not willing to fiddle around. 

---
