# Instinct MI300 series: backward weights convolution performance issue

> **Issue #4080**
> **状态**: closed
> **创建时间**: 2024-12-03T22:19:26Z
> **更新时间**: 2024-12-20T23:07:21Z
> **关闭时间**: 2024-12-20T23:07:21Z
> **作者**: peterjunpark
> **标签**: Verified Issue, AMD Instinct MI300X, AMD Instinct MI300A, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4080

## 标签

- **Verified Issue** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **AMD Instinct MI300A** (颜色: #ededed)
- **6.3.0** (颜色: #303737)

## 描述

A performance issue affects certain tensor shapes during backward weights convolution when using FP16 or FP32 data types on Instinct MI300 series accelerators. This issue will be addressed in a future ROCm release.

To mitigate the issue during model training, set the following environment variables:
```shell
export MIOPEN_FIND_MODE=3
export MIOPEN_FIND_ENFORCE=3
```

These settings enable auto-tuning on the first occurrence of a new tensor shape. The tuning results are stored in the user database, eliminating the need for repeated tuning when the same shape is encountered in subsequent runs. See the [MIOpen](https://rocm.docs.amd.com/en/latest/how-to/tuning-guides/mi300x/workload.html#miopen) section in the workload optimization guide to learn more about MIOpen’s auto-tuning capabilities.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2024-12-20T23:07:21Z)

Fixed in ROCm 6.3.1.

---
