# Minor performance regression for MIGraphX with int8-quantized models

> **Issue #6195**
> **状态**: open
> **创建时间**: 2026-05-04T14:45:39Z
> **更新时间**: 2026-05-04T14:46:37Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.2.3
> **URL**: https://github.com/ROCm/ROCm/issues/6195

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.2.3** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

You might observe a slight performance regression when running int8-quantized models with MIGraphX. This impact is generally minimal and does not affect correctness. However, workloads sensitive to peak throughput might have reduced performance when compared to non-quantized or alternative execution paths. This issue is currently under investigation and will be fixed in a future ROCm release.
