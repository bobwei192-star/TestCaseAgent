# Segmentation fault in ROCprofiler-SDK due to ABI mismatch affecting std::regex

> **Issue #5343**
> **状态**: closed
> **创建时间**: 2025-09-16T15:38:31Z
> **更新时间**: 2025-10-30T18:17:29Z
> **关闭时间**: 2025-10-30T18:17:02Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/5343

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Starting with GCC 5.1, GNU `libstdc++` introduced a dual Application Binary Interface (ABI) to adopt `C++11`, primarily affecting the `std::string` and its dependencies, including `std::regex`. If your code is compiled against headers expecting one ABI but linked or run with the other, it can cause problems with `std::string` and `std::regex`, leading to a segmentation fault in ROCprofiler-SDK, which uses `std::regex`. This issue is resolved in the [ROCm Systems `develop` branch](https://github.com/ROCm/rocm-systems) and will be part of a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-10-30T18:17:02Z)

Resolved in ROCm 7.1.0.

---
