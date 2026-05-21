# ROCTracer might fail to report kernel operations

> **Issue #6102**
> **状态**: closed
> **创建时间**: 2026-03-31T16:32:30Z
> **更新时间**: 2026-04-30T20:15:01Z
> **关闭时间**: 2026-04-30T20:15:00Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/6102

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.2.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Applications that use [ROCTracer](https://rocm.docs.amd.com/projects/roctracer/en/latest/index.html) might fail to receive some or all kernel operation events due to a ROCTracer reporting failure. ROCTracer is already deprecated and is scheduled to reach end of support (EoS) by the end of 2026 Q2. For more details on ROCTracer deprecation, see  [ROCm upcoming changes](https://rocm.docs.amd.com/en/docs-7.2.1/about/release-notes.html#roctracer-rocprofiler-rocprof-and-rocprofv2-deprecation). This issue will be resolved in a future PyTorch on ROCm release that replaces ROCTracer with [ROCprofiler-SDK](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/).

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-04-30T20:15:00Z)

Resolved in ROCm 7.2.2.

---
