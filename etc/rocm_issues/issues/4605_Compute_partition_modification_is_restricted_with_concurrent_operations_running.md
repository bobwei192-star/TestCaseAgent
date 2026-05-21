# Compute partition modification is restricted with concurrent operations running in parallel

> **Issue #4605**
> **状态**: open
> **创建时间**: 2025-04-11T23:11:32Z
> **更新时间**: 2025-04-11T23:41:20Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4605

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Modification to compute partition in GPU is prohibited by design while concurrent operations run in parallel. You must ensure no concurrent operations on the device are running when attempting to modify the compute partitions. Additional checks and error messaging to inform users of correct operation for partition modification are planned for future ROCm releases.
