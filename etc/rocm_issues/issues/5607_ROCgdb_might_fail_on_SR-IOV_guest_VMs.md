# ROCgdb might fail on SR-IOV guest VMs

> **Issue #5607**
> **状态**: open
> **创建时间**: 2025-10-31T18:00:12Z
> **更新时间**: 2025-10-31T18:00:28Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/5607

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

ROCgdb might fail when running the `step-schedlock-spurious-waves.exp` test case on SR-IOV guest virtual machines (VMs). As a workaround, avoid running an inferior in ROCgdb if a background process is already heavily utilizing the GPU. The issue is currently under investigation and will be fixed in a future ROCm release.
