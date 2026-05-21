# ROCm Compute Profiler CTest failure in CI

> **Issue #4085**
> **状态**: closed
> **创建时间**: 2024-12-03T22:19:41Z
> **更新时间**: 2025-01-28T20:33:53Z
> **关闭时间**: 2025-01-28T20:33:51Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4085

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.3.0** (颜色: #303737)

## 描述

When running ROCm Compute Profiler’s (`rocprof-compute`) CTest in the Azure CI environment, the `rocprof-compute` execution test fails. This issue is due to an outdated test file that was not renamed (`omniperf` to `rocprof-compute`), and due to the `ROCM_PATH` environment variable not being set in the Azure CI environment, causing the tool to be unable to extract chip information as expected. This issue will be addressed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2025-01-28T20:33:51Z)

Fixed in ROCm 6.3.2.

---
