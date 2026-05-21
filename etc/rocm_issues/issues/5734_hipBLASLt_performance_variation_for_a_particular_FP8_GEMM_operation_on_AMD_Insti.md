# hipBLASLt performance variation for a particular FP8 GEMM operation on AMD Instinct MI325X GPUs

> **Issue #5734**
> **状态**: open
> **创建时间**: 2025-12-03T13:03:31Z
> **更新时间**: 2025-12-03T13:03:50Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.1
> **URL**: https://github.com/ROCm/ROCm/issues/5734

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

If you’re using hipBLASLt on AMD Instinct MI325X GPUs for large FP8 GEMM operations (such as 9728x8192x65536), you might observe a noticeable performance variation. The issue is currently under investigation and will be fixed in a future ROCm release.
