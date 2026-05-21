# **rocm-smi --showbw displays as 0**

> **Issue #2469**
> **状态**: closed
> **创建时间**: 2023-09-15T17:31:09Z
> **更新时间**: 2024-03-10T05:05:48Z
> **关闭时间**: 2024-03-10T05:05:48Z
> **作者**: Rmalavally
> **标签**: Verified Issue, 5.7.0, Resolved
> **URL**: https://github.com/ROCm/ROCm/issues/2469

## 标签

- **Verified Issue** (颜色: #0052cc)
- **5.7.0** (颜色: #fef2c0)
- **Resolved** (颜色: #6DAE35)

## 描述

When ROCm is installed and a workload is run in a console, checking the bandwidth using the _rocm-smi –showbw_ instruction results in a 0.

 
**Expected behavior**

If _showbw_ is supported in AMD Instinct™ MI200, the result appears as follows, 

_taccuser@TCT-ML-MI210-1:~$ rocm-smi –showbw_


**Current behavior**

_--showbw_ appears as 0 even if a workload runs in the background. 

This known issue is expected to be fixed in a future release. 

---

## 评论 (1 条)

### 评论 #1 — Rmalavally (2023-09-19T18:37:53Z)

This issue is now resolved. 

---
