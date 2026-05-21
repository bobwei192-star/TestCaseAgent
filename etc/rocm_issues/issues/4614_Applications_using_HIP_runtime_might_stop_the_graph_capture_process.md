# Applications using HIP runtime might stop the graph capture process

> **Issue #4614**
> **状态**: open
> **创建时间**: 2025-04-11T23:19:59Z
> **更新时间**: 2025-04-11T23:19:59Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4614

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Applications using the HIP runtime might stop the graph capture process if the HIP runtime detects an invalid stale state from a previous capture on the same HIP stream. Resetting the stale set for every new capture in the HIP runtime can resolve the issue. The issue will be fixed in a future ROCm release.
