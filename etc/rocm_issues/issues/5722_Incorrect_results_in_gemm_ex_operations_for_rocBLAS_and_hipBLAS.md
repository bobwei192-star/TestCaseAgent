# Incorrect results in gemm_ex operations for rocBLAS and hipBLAS

> **Issue #5722**
> **状态**: closed
> **创建时间**: 2025-11-28T21:40:46Z
> **更新时间**: 2026-01-28T16:18:40Z
> **关闭时间**: 2026-01-28T16:18:40Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.1
> **URL**: https://github.com/ROCm/ROCm/issues/5722

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Some `gemm_ex` operations with 8-bit input data types (`int8`, `float8`, `bfloat8`) for specific matrix dimensions (K = 1 and number of workgroups > 1) might yield incorrect results. The issue results from incorrect tailloop code that fails to consider workgroup index when calculating valid element size. The issue will be fixed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-01-28T16:18:40Z)

Resolved in ROCm 7.2.0.

---
