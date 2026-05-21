# Failure to declare out-of-bound CPERs for bad memory page

> **Issue #5345**
> **状态**: open
> **创建时间**: 2025-09-16T15:40:09Z
> **更新时间**: 2025-09-16T15:40:09Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/5345

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Exceeding bad memory page threshold fails to declare Out-Of-Band Common Platform Error Records (CPERs). This issue affects all AMD Instinct MI300 Series and MI350 Series GPUs, and will be fixed in a future AMD GPU Driver release.
