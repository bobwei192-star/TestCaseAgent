# RCCL - MSCCL initialization failure

> **Issue #4769**
> **状态**: open
> **创建时间**: 2025-05-21T18:45:58Z
> **更新时间**: 2025-05-21T18:47:12Z
> **作者**: peterjunpark
> **标签**: Verified Issue, ROCm 6.4.1
> **URL**: https://github.com/ROCm/ROCm/issues/4769

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.1** (颜色: #aaaaaa)

## 描述

When splitting a communicator using `ncclCommSplit` in some GPU configurations, MSCCL initialization can cause a segmentation fault. The recommended workaround is to disable MSCCL with `export RCCL_MSCCL_ENABLE=0`. This issue will be fixed in a future ROCm release.
