# RCCL multi-node performance degradation with Linux kernel 6.8.0+ on RoCE networks

> **Issue #3772**
> **状态**: closed
> **创建时间**: 2024-09-20T23:04:52Z
> **更新时间**: 2024-12-03T23:35:21Z
> **关闭时间**: 2024-12-03T23:35:20Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.2.0, 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/3772

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.2.0** (颜色: #31778C)
- **6.2.1** (颜色: #BDBEE3)

## 描述

On systems running Linux kernel 6.8.0, such as Ubuntu 24.04, Direct Memory Access (DMA) transfers between the GPU and NIC are disabled and impacts multi-node RCCL performance.
 
This issue was reproduced with RCCL 2.20.5 (ROCm 6.2.0 and 6.2.1) on systems with Broadcom Thor-2 NICs and affects other systems with RoCE networks using Linux 6.8.0 or newer. Older RCCL versions are also impacted.
 
This issue will be addressed in a future ROCm release.

---

## 评论 (2 条)

### 评论 #1 — hassanhub (2024-10-27T15:33:05Z)

Is there a fix or an ETA for this issue to be resolved?

---

### 评论 #2 — peterjunpark (2024-12-03T23:35:20Z)

Fixed in ROCm 6.3.0.

---
