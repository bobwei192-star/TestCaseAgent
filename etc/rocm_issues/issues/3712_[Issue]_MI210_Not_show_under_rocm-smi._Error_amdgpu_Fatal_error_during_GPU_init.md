# [Issue]: MI210 Not show under rocm-smi.  Error:  amdgpu: Fatal error during GPU init

> **Issue #3712**
> **状态**: closed
> **创建时间**: 2024-09-12T14:39:16Z
> **更新时间**: 2024-09-12T19:34:53Z
> **关闭时间**: 2024-09-12T19:34:52Z
> **作者**: GowriShankarEAAS
> **标签**: AMD Instinct MI210, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3712

## 标签

- **AMD Instinct MI210** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

MI210 GPUs are not shown under rocm-smi. following is the error from OS logs

[   16.284320] [drm] amdgpu kernel modesetting enabled.
[   16.284345] [drm] amdgpu version: 6.8.5
[   16.284981] amdgpu: Virtual CRAT table created for CPU
[   16.285142] amdgpu: Topology: Add CPU node
[   16.323366] amdgpu: PeerDirect support was initialized successfully
[   16.323773] amdgpu 0000:48:00.0: enabling device (0000 -> 0002)
[   16.324081] amdgpu 0000:48:00.0: amdgpu: Fatal error during GPU init
[   16.324195] amdgpu: probe of 0000:48:00.0 failed with error -12
[   16.324216] amdgpu: legacy kernel without apple_gmux_detect()

Kindly suggest how to debug this.

i have reinstalled os and rocm, still the issue is not resolved


### Operating System

ubuntu 22.04.04

### CPU

AMD EPYC 9554 64-Core Processor

### GPU

AMD Instinct MI210

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

rocm-smi

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-09-12T17:23:01Z)

Hi @GowriShankarEAAS, could you please provide the complete dmesg output and Linux kernel version as well?

---

### 评论 #2 — GowriShankarEAAS (2024-09-12T17:44:39Z)

Linux kernel version : 5.15.0-101-generic

dmesg output:
[ 16.284320] [drm] amdgpu kernel modesetting enabled.
[ 16.284345] [drm] amdgpu version: 6.8.5
[ 16.284981] amdgpu: Virtual CRAT table created for CPU
[ 16.285142] amdgpu: Topology: Add CPU node
[ 16.323366] amdgpu: PeerDirect support was initialized successfully
[ 16.323773] amdgpu 0000:48:00.0: enabling device (0000 -> 0002)
[ 16.324081] amdgpu 0000:48:00.0: amdgpu: Fatal error during GPU init
[ 16.324195] amdgpu: probe of 0000:48:00.0 failed with error -12
[ 16.324216] amdgpu: legacy kernel without apple_gmux_detect()

---

### 评论 #3 — GowriShankarEAAS (2024-09-12T17:45:29Z)

the issue occurred after kernel upgraded to 6.8 and i have reverted back to 5.15, but the problem exists


---

### 评论 #4 — GowriShankarEAAS (2024-09-12T19:34:53Z)

The issue is resolved after OS upgrade. close this issue 

---
