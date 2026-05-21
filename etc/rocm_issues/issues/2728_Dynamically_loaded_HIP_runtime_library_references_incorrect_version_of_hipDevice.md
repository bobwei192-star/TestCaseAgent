# Dynamically loaded HIP runtime library references incorrect version of hipDeviceGetProperties API

> **Issue #2728**
> **状态**: closed
> **创建时间**: 2023-12-15T21:46:14Z
> **更新时间**: 2024-09-09T19:37:55Z
> **关闭时间**: 2024-09-09T19:37:55Z
> **作者**: Rmalavally
> **标签**: Under Investigation, Verified Issue, 6.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/2728

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Verified Issue** (颜色: #0052cc)
- **6.0.0** (颜色: #01DED3)

## 描述

When an application loads the HIP runtime library dynamically from ROCm 6.0 and attempts to use hipDeviceGetProperties, the application incorrectly uses the hipDeviceGetProperties API from a previous ROCm release instead of the newer ROCm 6.0 implementation.

The issue will be fixed in a future release.


---

## 评论 (1 条)

### 评论 #1 — tcgu-amd (2024-09-09T19:37:55Z)

This issue is fixed by this commit here https://github.com/ROCm/clr/commit/0479cdb3dd30ef58718cad44e424bd793c394cc0

---
