# [Issue]: ROCm SDK 5.7.1 causes crash on gfx90c

> **Issue #3133**
> **状态**: closed
> **创建时间**: 2024-05-15T18:26:12Z
> **更新时间**: 2024-05-23T15:12:20Z
> **关闭时间**: 2024-05-23T15:12:20Z
> **作者**: enpinion
> **标签**: ROCm 5.7.1, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/3133

## 标签

- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

HIP binary built with ROCm SDK 5.7.1 causes crash on Windows system with gfx90c (Vega Integrated).
This error raises whenever device access the memory.
amdhip64.dll -> hipMemUnmap + 340128 - Access Violation reading location 0x00000020

### Operating System

Windows 11 23H2 (22631.3593)

### CPU

AMD Ryzen 7 Pro 5850U with Radeon Graphics

### GPU

AMD Radeon Graphics (gfx90c)
RX 560 (gfx803)

### ROCm Version

ROCm 5.7.1

### ROCm Component

HIP

### Steps to Reproduce

* Step 1 through 5 can be skipped. It is just for verify 5.5.1 works without any problem.
1. Install HIP SDK 5.5.1 (https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html)
2. Create "MatrixTranspose" HIP example project in Visual Studio
3. Add "gfx90c" to offloading
4. Build and run.
5. No problem
6. Install HIP SDK 5.7.1
7. Setup the "MatrixTranspose" HIP example project to use HIP SDK 5.7.1 in Visual Studio
8. Build and run.
9. Crash.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Driver version: 24.3.1

---

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2024-05-23T15:12:20Z)

@enpinion gfx90c is not officially supported in ROCm SDK 5.7.1. 

---
