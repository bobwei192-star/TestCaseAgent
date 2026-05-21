# Systems with a display GPU and eight AMD Instinct MI300 series GPUs reboot when loading the AMDGPU driver

> **Issue #4589**
> **状态**: open
> **创建时间**: 2025-04-11T19:34:43Z
> **更新时间**: 2025-04-11T19:37:46Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4589

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Due to limitations in older `libdrm` libraries, you might not be able to use an AMD Instinct MI300 series GPUs with a display GPU on a single server. This limitation means there can only be a maximum of 64 DRM devices at any time, regardless of vendor. When attempting to initialize all DRM device modules, the kernel will PANIC on the 65th DRM device, resulting in a system reboot. This issue will be properly fixed when resolved in `libdrm` libraries and the Linux kernel, to be distributed by the OS per their release schedules. Remove the non-AMD Instinct MI300 series GPUs as a workaround, or add the following in the GRUB setting for the onboard modules.

```bash
modprobe.blacklist=$MODULE
```
For Example:

* For Aspeed, use:
```bash
modprobe.blacklist=ast
```
* For Mellanox, use:
```bash
modprobe.blacklist=mgag200
```
