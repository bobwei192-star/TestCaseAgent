# Transformer Engine `test_distributed_fused_attn` aborts with fatal Python error

> **Issue #4087**
> **状态**: closed
> **创建时间**: 2024-12-03T22:19:50Z
> **更新时间**: 2025-04-11T19:54:22Z
> **关闭时间**: 2025-04-11T19:42:57Z
> **作者**: peterjunpark
> **标签**: 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4087

## 标签

- **6.3.0** (颜色: #303737)

## 描述

The `test_distributed_fused_attn` Pytest case for JAX in [Transformer Engine for ROCm](https://github.com/ROCm/TransformerEngine) fails with a fatal Python error under certain conditions. The root cause is unrelated Transformer Engine but due to some issue within XLA. This XLA issue is under investigation and will be addressed in a future release.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2025-04-11T19:42:57Z)

Resolved as part of ROCm 6.4.0.

---
