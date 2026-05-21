# Issue uninstalling ROCm Bandwidth Test using amdgpu-install script

> **Issue #5611**
> **状态**: closed
> **创建时间**: 2025-10-31T22:12:15Z
> **更新时间**: 2025-11-27T15:03:59Z
> **关闭时间**: 2025-11-27T15:03:59Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/5611

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Due to a missing `rocm-core` dependency from the ROCm Bandwidth Test, you can't cleanly uninstall ROCm Bandwidth Test using the `amdgpu-install` script. As a workaround, uninstall ROCm Bandwidth Test manually, using the native package managers. For more information, see [Installation via native package manager](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager-index.html). The issue will be fixed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-11-27T15:03:59Z)

Resolved in ROCm 7.1.1.

---
