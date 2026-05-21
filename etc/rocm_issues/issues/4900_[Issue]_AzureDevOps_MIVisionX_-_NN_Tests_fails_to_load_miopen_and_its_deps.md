# [Issue]: AzureDevOps: MIVisionX - NN Tests fails to load miopen and its deps

> **Issue #4900**
> **状态**: closed
> **创建时间**: 2025-06-08T18:58:22Z
> **更新时间**: 2025-08-27T19:29:18Z
> **关闭时间**: 2025-08-27T19:29:18Z
> **作者**: kiritigowda
> **标签**: External CI
> **URL**: https://github.com/ROCm/ROCm/issues/4900

## 标签

- **External CI** (颜色: #58C55D)

## 负责人

- jayhawk-commits
- danielsu-amd

## 描述

### Problem Description

Two part issue

1. Failure in CI test phase is not reported as an overall failure
2. NN Tests fails to load MIOpen Libs - https://dev.azure.com/ROCm-CI/ROCm-CI/_build/results?buildId=33312&view=logs&j=bc31fbc9-d111-59c6-34df-decf2734c416&t=180f951e-01da-54ef-61a5-7f0739f2c417


![Image](https://github.com/user-attachments/assets/b70c507b-e0da-4a90-8873-1f60d01abf79)

![Image](https://github.com/user-attachments/assets/76edc3ae-4025-4046-a6a6-e79fab969689)

### Operating System

Ubuntu 22/24

### CPU

Any

### GPU

Any

### ROCm Version

Latest

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

### 评论 #1 — danielsu-amd (2025-08-27T19:29:18Z)

Fixed in https://github.com/ROCm/ROCm/pull/4937

---
