# [Question] ROCprof-compute on CDNA3

> **Issue #4277**
> **状态**: closed
> **创建时间**: 2025-01-20T21:22:46Z
> **更新时间**: 2025-01-21T19:43:04Z
> **关闭时间**: 2025-01-21T19:43:03Z
> **作者**: fluidnumericsJoe
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4277

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

When looking at `rocprof-compute` for hardware events profiling on MI300A (CDNA3) platforms, I'm not finding details for the infinity cache. The more I think about it, the more I'm realizing that there is likely things that are missing.

For memory operations profiling, `rocprof-compute` only provides analysis of L1, L2, LDS, and HBM memory; however, CDNA3 introduced another layer of cache (infinity cache) between L2 and HBM. What I'm wondering is what the L2 profiling metrics are actually showing in `rocprof-compute` ? Are they actually showing metrics related to Infinity Cache (L3) ??

Can you provide some clarification about using rocprof-compute on CDNA3 architectures ?

---

## 评论 (1 条)

### 评论 #1 — schung-amd (2025-01-21T19:43:03Z)

Hi @fluidnumerics-joe, we currently don't have the capability to output L3 cache metrics with `rocprof-compute`. The L2 metrics should pertain to L2 only and shouldn't be polluted by unreported L3 metrics. Thanks for your interest! Let me know if you have further questions or need additional clarification or guidance.

---
