# Compilation failure via hipRTC when compiling with std=c++11

> **Issue #5341**
> **状态**: open
> **创建时间**: 2025-09-16T15:35:50Z
> **更新时间**: 2025-09-16T15:35:50Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/5341

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Applications compiling kernels using `hipRTC` might fail while passing the `std=c++11` compiler option. This issue will be fixed in a future ROCm release.
