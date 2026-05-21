# KFDTest failure on Instinct MI300X with Oracle Linux 8.9

> **Issue #3495**
> **状态**: closed
> **创建时间**: 2024-08-02T18:27:18Z
> **更新时间**: 2024-12-10T14:47:04Z
> **关闭时间**: 2024-12-10T14:47:04Z
> **作者**: peterjunpark
> **标签**: Verified Issue, AMD Instinct MI300X, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3495

## 标签

- **Verified Issue** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **6.2.0** (颜色: #31778C)

## 描述

The `KFDEvictTest.QueueTest` is failing on the MI300X platform during KFD (Kernel Fusion Driver) tests, causing the full suite to not execute properly. This issue is suspected to be hardware-related.

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-12-10T14:47:04Z)

Fixed in ROCm 6.3.0.



---
