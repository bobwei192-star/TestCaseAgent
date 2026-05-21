# GFX Freq information is unavailable in the rocm-smi when running in SRIOV mode enabled on MI210

> **Issue #4603**
> **状态**: open
> **创建时间**: 2025-04-11T23:09:59Z
> **更新时间**: 2025-04-11T23:09:59Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4603

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

In ROCm 6.4.0, you cannot see the GFX Freq information in the guest VM. In SRIOV mode, the AMD Platform Management Firmware (PMFW) does not share the graphics frequency information with the guest VMs and is only available to Host systems. This issue will be addressed in a future ROCm release.
