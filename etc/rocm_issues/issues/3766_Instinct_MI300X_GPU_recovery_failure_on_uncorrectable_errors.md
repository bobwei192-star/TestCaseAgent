# Instinct MI300X GPU recovery failure on uncorrectable errors

> **Issue #3766**
> **状态**: closed
> **创建时间**: 2024-09-20T21:19:48Z
> **更新时间**: 2024-09-27T19:24:35Z
> **关闭时间**: 2024-09-27T19:24:34Z
> **作者**: peterjunpark
> **标签**: Verified Issue, AMD Instinct MI300X, 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/3766

## 标签

- **Verified Issue** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **6.2.1** (颜色: #BDBEE3)

## 描述

For the AMD Instinct MI300X accelerator, GPU recovery resets triggered by uncorrectable errors (UE) might not complete successfully, which can result in the system being left in an undefined state. A system reboot is needed to recover from this state. Additionally, error logging might fail in these situations, hindering diagnostics.

This issue is under investigation and will be resolved in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2024-09-27T19:24:35Z)

Fixed in ROCm 6.2.2

---
