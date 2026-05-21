# A memory error in the kernel might lead to applications using the ROCr library becoming unresponsive

> **Issue #5334**
> **状态**: open
> **创建时间**: 2025-09-16T15:17:29Z
> **更新时间**: 2025-09-16T15:33:41Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/5334

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Applications using the ROCr library might become unresponsive if a memory error occurs in the launched kernel when the queue from which it was launched is destroyed. The application is unable to receive further signal, resulting in the stall condition. The issue will be fixed in a future ROCm release.
