# Reduced precision in gemm_ex operations for rocBLAS and hipBLAS

> **Issue #5640**
> **状态**: closed
> **创建时间**: 2025-11-07T23:50:06Z
> **更新时间**: 2025-11-27T15:04:15Z
> **关闭时间**: 2025-11-27T15:04:15Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/5640

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Some `gemm_ex` operations with `half` or `f32_r` data types might yield 16-bit precision results instead of the expected 32-bit precision when matrix dimensions are m=1 or n=1. The issue results from the optimization that enables `_ex` APIs to use lower precision multiples. It limits the high-precision matrix operations performed in PyTorch with rocBLAS and hipBLAS. The issue will be fixed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-11-27T15:04:15Z)

Resolved in ROCm 7.1.1.

---
