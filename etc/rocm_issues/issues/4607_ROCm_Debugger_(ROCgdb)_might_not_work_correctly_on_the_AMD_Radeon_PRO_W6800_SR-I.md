# ROCm Debugger (ROCgdb) might not work correctly on the AMD Radeon PRO W6800 SR-IOV virtualization environment

> **Issue #4607**
> **状态**: open
> **创建时间**: 2025-04-11T23:13:15Z
> **更新时间**: 2025-04-11T23:13:15Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4607

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

The ROCm Debugger (ROCgdb) component needs access to some registers to fetch debugging information. These registers are blocked in the AMD Radeon PRO W6800 SR-IOV virtualization environment, resulting in the ROCm Debugger (ROCgdb) being non-functional. The issue is due to the limitation in the virtualization environment and isn't specific to ROCm. Further investigation is in progress.
