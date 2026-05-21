# RCCL profiler plugin failure with AllToAll operations

> **Issue #5653**
> **状态**: closed
> **创建时间**: 2025-11-11T21:41:52Z
> **更新时间**: 2025-11-27T15:04:06Z
> **关闭时间**: 2025-11-27T15:04:06Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/5653

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

The RCCL profiler plugin `librccl-profiler.so` might fail with a segmentation fault during `AllToAll` collective operations due to improperly assigned point-to-point task function pointers. This leads to invalid memory access and prevents profiling of `AllToAll` performance. Other operations, like `AllReduce`, are unaffected. It's recommended to avoid using the RCCL profiler plugin with `AllToAll` operations until the fix is available. This issue is resolved in the [RCCL `develop` branch](https://github.com/ROCm/rccl/tree/develop) and will be part of a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-11-27T15:04:06Z)

Resolved in ROCm 7.1.1.

---
