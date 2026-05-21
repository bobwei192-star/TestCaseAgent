# MIVisionX memory access fault in Canny edge detection

> **Issue #4086**
> **状态**: closed
> **创建时间**: 2024-12-03T22:19:44Z
> **更新时间**: 2025-01-28T20:32:48Z
> **关闭时间**: 2025-01-28T20:32:47Z
> **作者**: peterjunpark
> **标签**: Verified Issue, AMD Instinct MI300X, AMD Instinct MI300A, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4086

## 标签

- **Verified Issue** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **AMD Instinct MI300A** (颜色: #ededed)
- **6.3.0** (颜色: #303737)

## 描述

Canny edge detection kernels might access out-of-bounds memory locations while computing gradient intensities on edge pixels. This issue is isolated to Canny-specific use cases on Instinct MI300 series accelerators. This issue is resolved in the [MIVisionX develop branch](https://github.com/ROCm/mivisionx) and will be part of a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2025-01-28T20:32:47Z)

Fix is validated in the ROCm 6.3.2 release.

---
