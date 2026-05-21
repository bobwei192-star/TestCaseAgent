# RCCL performance degradation on AMD Instinct MI300X GPU with AMD Pollara AI NIC

> **Issue #5717**
> **状态**: closed
> **创建时间**: 2025-11-28T15:09:15Z
> **更新时间**: 2026-01-28T16:18:10Z
> **关闭时间**: 2026-01-28T16:18:10Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.1
> **URL**: https://github.com/ROCm/ROCm/issues/5717

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

If you’re using RCCL on AMD Instinct MI300X GPUs with AMD Pollara AI NIC, you might observe performance degradation for specific collectives and message sizes. The affected collectives are `Scatter`, `AllToAll`, and `AlltoAllv`. It's recommended to avoid using RCCL packaged with ROCm 7.1.1. As a workaround, use the {fab}`github`[RCCL `develop` branch](https://github.com/ROCm/rccl/tree/develop), which contains the fix and will be included in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-01-28T16:18:10Z)

Resolved in ROCm 7.2.0.

---
