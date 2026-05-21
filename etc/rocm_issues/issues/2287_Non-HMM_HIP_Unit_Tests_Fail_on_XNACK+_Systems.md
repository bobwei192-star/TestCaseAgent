# Non-HMM HIP Unit Tests Fail on XNACK+ Systems

> **Issue #2287**
> **状态**: closed
> **创建时间**: 2023-06-28T21:59:13Z
> **更新时间**: 2023-12-23T19:04:05Z
> **关闭时间**: 2023-12-23T19:04:04Z
> **作者**: Rmalavally
> **标签**: Under Investigation, Verified Issue, 5.6.0, Resolved
> **URL**: https://github.com/ROCm/ROCm/issues/2287

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Verified Issue** (颜色: #0052cc)
- **5.6.0** (颜色: #b60205)
- **Resolved** (颜色: #6DAE35)

## 描述

Several non-HMM HIP unit tests, when running on xnack+ memory mode systems, fail. 

This issue is under investigation and will be fixed in a future release.

---

## 评论 (3 条)

### 评论 #1 — milthorpe (2023-10-15T21:32:28Z)

Is this still an open issue? The [ROCM 5.7.0 Changelog](https://rocm.docs.amd.com/en/latest/CHANGELOG.html#rocm-5-7-0) mentions in Fixed Defects: "Failures observed with non-HMM HIP directed catch2 tests with XNACK+".

---

### 评论 #2 — Rmalavally (2023-10-17T20:42:11Z)

@milthorpe Thank you for reaching out. Yes, this issue was fixed in the ROCm 5.7.0 release.

---

### 评论 #3 — tasso (2023-12-23T19:04:04Z)

Closing the issue since it was confirmed fixed on Oct. 17, 2023. 

---
