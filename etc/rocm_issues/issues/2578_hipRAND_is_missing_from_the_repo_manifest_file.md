# hipRAND is missing from the repo manifest file

> **Issue #2578**
> **状态**: closed
> **创建时间**: 2023-10-18T16:39:30Z
> **更新时间**: 2024-01-17T16:36:12Z
> **关闭时间**: 2024-01-17T16:36:12Z
> **作者**: BenWibking
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2578

## 描述

There is no entry for hipRAND in the `default.xml` repo manifest file: https://github.com/RadeonOpenCompute/ROCm/blob/roc-5.7.x/default.xml

This makes it unnecessarily difficult to build a complete set of ROCm components.

---

## 评论 (2 条)

### 评论 #1 — saadrahim (2023-10-18T16:42:52Z)

rocRAND contains a submodule for hipRAND in 5.7.1. Please see https://github.com/ROCmSoftwarePlatform/rocRAND/tree/rocm-5.7.1. hipRAND code was historically included in the rocRAND repo. The slow separation of the code bases is nearly complete. ROCm 6.0 will contain hipRAND in the manifest.

---

### 评论 #2 — nartmada (2024-01-17T04:52:41Z)

Hi @BenWibking, please close the ticket if your issue has been fixed in ROCm6.0.0.  Thanks.

---
