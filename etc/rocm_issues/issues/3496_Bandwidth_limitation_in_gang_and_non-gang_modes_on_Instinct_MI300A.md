# Bandwidth limitation in gang and non-gang modes on Instinct MI300A

> **Issue #3496**
> **状态**: closed
> **创建时间**: 2024-08-02T18:31:59Z
> **更新时间**: 2024-12-03T22:20:21Z
> **关闭时间**: 2024-12-03T22:20:20Z
> **作者**: peterjunpark
> **标签**: Verified Issue, AMD Instinct MI300A, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3496

## 标签

- **Verified Issue** (颜色: #0052cc)
- **AMD Instinct MI300A** (颜色: #ededed)
- **6.2.0** (颜色: #31778C)

## 描述

Expected target peak non-gang performance (~60GB/s) and target peak gang performance (~90GB/s) are not achieved. Both gang and non-gang performance are observed to be limited at 45GB/s.

This issue will be addressed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2024-12-03T22:20:20Z)

Fixed in ROCm 6.3.0.

---
