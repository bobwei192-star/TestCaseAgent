# [Documentation]: Update ROCm docs to include `gfx1200` and `gfx1201`

> **Issue #4485**
> **状态**: closed
> **创建时间**: 2025-03-12T16:37:46Z
> **更新时间**: 2025-05-26T15:16:37Z
> **关闭时间**: 2025-05-26T15:16:36Z
> **作者**: garrettbyrd
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4485

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

It seems that as of #4162, `gfx1200` and `gfx1201` have been added to the ROCm build scripts.

Documentation (mainly support matrices) should be updated to reflect these supported architectures and corresponding hardware, namely Radeon 9070 and Radeon 9070 XT.

Here are some pages which require updates, though this is likely not an exhaustive list:
- https://rocm.docs.amd.com/en/docs-6.3.3/compatibility/compatibility-matrix.html
- https://rocm.docs.amd.com/projects/radeon/en/docs-6.3/docs/compatibility/native_linux/native_linux_compatibility.html
- https://rocm.docs.amd.com/projects/radeon/en/docs-6.3/docs/compatibility/wsl/wsl_compatibility.html

This also addresses some of the questions posed in #4443.

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-03-12T17:48:41Z)

Hi @garrettbyrd. Internal ticket has been created to update docs. Thanks!

---

### 评论 #2 — Apriqi (2025-04-17T07:10:40Z)

7800XT ？？？？？
When ？？？？？

---

### 评论 #3 — harkgill-amd (2025-05-26T15:16:36Z)

Hi @garrettbyrd, with the release of ROCm 6.4.1 comes official support for the 9070 and 9070XT on Linux! The [System Requirements - Supported GPUs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus) table and [ROCm on Radeon Support Matrix](https://rocm.docs.amd.com/projects/radeon/en/docs-6.4.1_a/docs/compatibility/native_linux/native_linux_compatibility.html#linux-support-matrices-by-rocm-version) have been updated to reflect these new additions. 

ROCm on WSL is still on the 6.3.4 release which does not have support for the 9000 series GPUs. Once support is added, the documentation will be updated as well.

---
