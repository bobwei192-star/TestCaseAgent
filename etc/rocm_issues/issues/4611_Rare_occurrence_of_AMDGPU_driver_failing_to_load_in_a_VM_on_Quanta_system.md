# Rare occurrence of AMDGPU driver failing to load in a VM on Quanta system

> **Issue #4611**
> **状态**: open
> **创建时间**: 2025-04-11T23:16:40Z
> **更新时间**: 2025-04-11T23:16:40Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4611

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

In a rare occurrence (1 in 500 reboots), the guest kernel might display the call trace due to the AMDGPU driver failing to load in a repeated power cycle virtual machine (VM) on a Quanta system. This issue will limit you from using the AMD GPUs in the guest kernel. As a workaround, reboot the VM to avoid the failure.
