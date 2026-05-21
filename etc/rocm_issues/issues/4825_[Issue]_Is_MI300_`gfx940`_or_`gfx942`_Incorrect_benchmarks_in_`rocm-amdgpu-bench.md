# [Issue]: Is MI300 `gfx940` or `gfx942`? Incorrect benchmarks in `rocm-amdgpu-bench`?

> **Issue #4825**
> **状态**: closed
> **创建时间**: 2025-05-28T18:06:47Z
> **更新时间**: 2025-06-06T18:38:37Z
> **关闭时间**: 2025-06-06T18:11:22Z
> **作者**: garrettbyrd
> **标签**: Under Investigation, AMD Instinct MI300A
> **URL**: https://github.com/ROCm/ROCm/issues/4825

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300A** (颜色: #ededed)

## 描述

### Problem Description

My understanding was that MI300A and MI300X are both `gfx942`, supported by [this documentation](https://rocm.docs.amd.com/en/docs-6.4.1/reference/gpu-arch-specs.html). This is verified when I run `rocminfo` on MI300A (this returns `Name: gfx942`). Also as expected, `gfx940` and `gfx941` are not even present in the [LLVM docs](https://llvm.org/docs/AMDGPUUsage.html).

However, `rocm-amdgpu-bench` seems to indicate that `gfx940` correlates to the MI300A ([here](https://github.com/ROCm/rocm-amdgpu-bench/blob/35d12013fac83f12be943933a41e14db7e639e89/roofline.cpp#L52)). This checks out with the correct number of compute units on the 300A.

Does this imply incorrect benchmarking results from `rocm-amdgpu-bench`? I.e., since it is calculating `datasetEntries` and other variables using 304 instead of 228, is this affecting the accuracy of benchmarks on MI300A?

### Operating System

Rocky 9.5

### CPU

MI300A

### GPU

MI300A

### ROCm Version

ROCm 6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-05-28T18:46:43Z)

Hi @garrettbyrd. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — harkgill-amd (2025-06-02T20:47:45Z)

Hey @garrettbyrd, `gfx940` and `gfx941` were architecture targets for pre-release/A0 revisions of MI300A and MI300X respectively. These are no longer in use and all release MI300A/MI300X accelerators have LLVM target name `gfx942`.

https://github.com/ROCm/rocm-amdgpu-bench/blob/main/roofline.cpp has since been updated to correctly denote this. Thanks for the catch!

EDIT: Just now noticing the discrepancy in CUs despite the LLVM target names being correct. Will look into this as well.

---

### 评论 #3 — harkgill-amd (2025-06-06T18:11:22Z)

The hardcoded mapping from LLVM Target Name -> # of CUs was incorrect in the case of `gfx942` as the #of CUs varies for MI300A vs MI300X. The changes in https://github.com/ROCm/rocm-amdgpu-bench/pull/18, which are now in the main branch, address this issue by dynamically retrieving the #of CUs from the hip runtime. Thanks for bringing this up @garrettbyrd.

---

### 评论 #4 — garrettbyrd (2025-06-06T18:38:36Z)

Nice, thanks for the fix.

---
