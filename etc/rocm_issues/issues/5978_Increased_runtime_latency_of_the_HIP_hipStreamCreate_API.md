# Increased runtime latency of the HIP hipStreamCreate API

> **Issue #5978**
> **状态**: closed
> **创建时间**: 2026-02-18T15:07:52Z
> **更新时间**: 2026-03-25T23:49:47Z
> **关闭时间**: 2026-03-25T23:49:47Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/5978

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.2.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Doubling of runtime latency of the [HIP](https://rocmdocs.amd.com/projects/HIP/en/latest/doxygen/html/group___stream.html) `hipStreamCreate` API might be observed. While this affects RCCL `all_reduce_perf` tests, it has minimal impact on real production workloads. No slowdowns have been observed in other common benchmarks, including PyTorch, vLLM, and other application‑level tests. The issue is currently under investigation and will be fixed in an upcoming ROCm release. 

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-03-25T23:49:47Z)

Resolved in ROCm 7.2.1

---
