# Incorrect Returns for hipSetDevice and hipSetDeviceFlags APIs

> **Issue #2288**
> **状态**: closed
> **创建时间**: 2023-06-28T22:00:43Z
> **更新时间**: 2024-03-18T15:48:34Z
> **关闭时间**: 2024-03-18T15:48:34Z
> **作者**: Rmalavally
> **标签**: Under Investigation, Verified Issue, 5.6.0
> **URL**: https://github.com/ROCm/ROCm/issues/2288

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Verified Issue** (颜色: #0052cc)
- **5.6.0** (颜色: #b60205)

## 描述

hipSetDevice and hipSetDeviceFlags APIs return hipErrorInvalidDevice instead of hipErrorNoDevice on a system without a GPU.

This issue is under investigation and will be fixed in a future release.

---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-03-16T02:32:07Z)

Hi @Rmalavally, does this issue still exist in latest ROCm 6.0.2?  Thanks.

---

### 评论 #2 — nartmada (2024-03-18T15:48:34Z)

Closing the ticket as issue has been fixed in ROCm 5.6.  

---
