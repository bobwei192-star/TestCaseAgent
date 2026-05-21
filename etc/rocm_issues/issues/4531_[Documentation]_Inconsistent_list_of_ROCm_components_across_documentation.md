# [Documentation]: Inconsistent list of ROCm components across documentation

> **Issue #4531**
> **状态**: open
> **创建时间**: 2025-03-26T01:42:18Z
> **更新时间**: 2025-05-15T13:56:09Z
> **作者**: garrettbyrd
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4531

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

There are a few pages in the documentation/source code that provide lists of ROCm components. There are some minor inconsistencies across these pages that slightly obscure which packages are considered as "ROCm Components". Below is a table that outlines these inconsistencies; included in this are whether or not packages are included in `apt` / `dnf` / spack. Including `default.xml` since "The default.xml file contains information for all repositories and the associated commit used to build the current ROCm release" - [`ROCm/README.md`](https://github.com/ROCm/ROCm/?tab=readme-ov-file#rocm-documentation). This is up-to-date as of 6.3.3.


Pages:
- [What is ROCm?](https://rocm.docs.amd.com/en/latest/what-is-rocm.html)
- [`ROCm/default.xml`](https://github.com/ROCm/ROCm/blob/develop/default.xml)
- [ROCm Documentation for Spack](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/spack.html#rocm-packages-in-spack)
- [ROCm Compatibility Matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html)
- [Version release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html#rocm-components)

Inconsistencies:

| Package              | `apt`/`dnf` | Spack | `default.xml` | What is ROCm? | 6.3.3 Version Release Notes | Compatibility Matrix |
|----------------------|-------------|-------|---------------|---------------|-----------------------------|----------------------|
| rocm-utils           |          ✅ |    ❌ |            ❌ |            ❌ |                          ❌ |                   ❌ |
| hipother             |          ❌ |    ❌ |            ✅ |            ❌ |                          ❌ |                   ✅ |
| ROCT-Thunk-Interface¹ |          ✅ |    ✅ |            ❌ |            ❌ |                          ❌ |                   ✅ |
| rock-kernel-driver   |          ❌ |    ❌ |            ✅ |            ❌ |                          ❌ |                   ❌ |
| transferbench        |          ✅ |    ❌ |            ✅ |            ❌ |                          ❌ |                   ❌ |
| rocm-opencl          |          ✅ |    ✅ |            ❌ |            ❌ |                          ❌ |                   ❌ |

[1] ROCT-Thunk-Interface maintained in `dnf` as `hsakmt`; in `apt` as `libhsakmt-dev`; in spack as [`hsakmt-roct`](https://packages.spack.io/package.html?name=hsakmt-roct).

ROCT-Thunk-Interface is appended with the following note in the Compatibility Matrix page:
 > Starting from ROCm 6.3.0, the ROCT Thunk Interface is included as part of the ROCr runtime package.

I understand now that ROCT-Thunk-Interface is deprecated, but thought it would be worth including anyway.

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2025-05-15T13:56:08Z)

Hi @garrettbyrd. Internal ticket has been created to fix this in docs. Thanks!

---
