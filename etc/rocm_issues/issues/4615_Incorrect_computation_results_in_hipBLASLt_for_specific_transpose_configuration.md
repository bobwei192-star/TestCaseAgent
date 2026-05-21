# Incorrect computation results in hipBLASLt for specific transpose configuration

> **Issue #4615**
> **状态**: open
> **创建时间**: 2025-04-11T23:20:43Z
> **更新时间**: 2025-04-11T23:20:43Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4615

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

When running the hipBLASLt library using the transpose configuration (TT) with FP32 and XF32 data types, you might receive incorrect computation results. As a workaround, select alternative solutions from the list returned by `hipblasLtMatmulAlgoGetHeuristic()`. Verify the result to identify the correct alternative solution. The issue will be fixed in a future ROCm release.
