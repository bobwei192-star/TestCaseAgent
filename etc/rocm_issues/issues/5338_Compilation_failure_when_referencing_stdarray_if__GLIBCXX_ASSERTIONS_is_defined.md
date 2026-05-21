# Compilation failure when referencing std::array if _GLIBCXX_ASSERTIONS is defined

> **Issue #5338**
> **状态**: open
> **创建时间**: 2025-09-16T15:30:23Z
> **更新时间**: 2025-09-16T15:34:11Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/5338

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Compiling from a device kernel or function results in failure when attempting to reference `std::array` if `_GLIBCXX_ASSERTIONS` is defined. The issue occurs because there's no device definition for `std::__glibcxx_asert_fail()`. This issue will be resolved in a future ROCm release with the implementation of `std::__glibcxx_assert_fail()`.
