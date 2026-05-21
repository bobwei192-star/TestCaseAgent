# Failure to use –kokkos-trace option in ROCm Compute Profiler

> **Issue #4604**
> **状态**: closed
> **创建时间**: 2025-04-11T23:11:09Z
> **更新时间**: 2025-09-16T17:38:21Z
> **关闭时间**: 2025-09-16T17:38:21Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4604

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

In ROCm 6.4.0, it’s not recommended to use the `--kokkos-trace` option. `--kokkos-trace` has been partially implemented in the `rocprofv3` tool, resulting in a difference between the output of `--kokkos-trace` and the `counter_collection.csv` output file. The program will exit with a warning message if the `-kokkos-trace` option is detected in the ROCm Compute Profiler. The issue will be addressed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-09-16T17:38:21Z)

Resolved in ROCm 7.0.0.

---
