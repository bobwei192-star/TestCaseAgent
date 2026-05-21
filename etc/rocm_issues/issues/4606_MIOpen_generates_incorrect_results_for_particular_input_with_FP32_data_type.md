# MIOpen generates incorrect results for particular input with FP32 data type

> **Issue #4606**
> **状态**: closed
> **创建时间**: 2025-04-11T23:12:30Z
> **更新时间**: 2025-07-21T20:48:13Z
> **关闭时间**: 2025-07-21T20:48:13Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4606

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

In ROCm 6.4.0, MIOpen generates incorrect results on the `conv2dbackward` function for a particular input with 32-bit floating point (FP32) data types. The issue is only specific to FP32 data types with 2 * 2 kernel size and dilation 2 * 1. As a workaround, change the data type from FP32 to FP16. The issue will be addressed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-07-21T20:48:13Z)

Resolved in ROCm 6.4.2.

---
