# [Issue]: ROCR: unsupported GPU

> **Issue #4068**
> **状态**: closed
> **创建时间**: 2024-11-30T04:03:33Z
> **更新时间**: 2025-01-28T07:49:23Z
> **关闭时间**: 2024-12-02T14:42:56Z
> **作者**: Apriqi
> **标签**: ROCm 6.1.0, AMD Radeon 7800XT
> **URL**: https://github.com/ROCm/ROCm/issues/4068

## 标签

- **ROCm 6.1.0** (颜色: #ededed)
- **AMD Radeon 7800XT** (颜色: #ededed)

## 描述

### Problem Description

ROCR: unsupported GPU
hsa api call failure at: ./sources/wsl/tools/rocminfo/rocminfo.cc:1087
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.



### Operating System

Linux DESKTOP-0O8UKKK 5.15.167.4-microsoft-standard-WSL2 #1 SMP Tue Nov 5 00:21:55 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

### CPU

AMD Ryzen 7500F

### GPU

AMD Radeon 7800XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-12-02T14:42:56Z)

Hi @Apriqi, the `ROCR: unsupported GPU` error is expected as the 7800XT is not supported for ROCm on WSL. 

Please see the [GPU Support Matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix) for a complete list of supported GPUs in the beta release of ROCm on WSL.

---

### 评论 #2 — Apriqi (2024-12-05T03:24:19Z)

When will it support?  

---

### 评论 #3 — matinzd (2025-01-28T07:49:22Z)

Are there any plans to support 7800XT as well on WSL2?

---
