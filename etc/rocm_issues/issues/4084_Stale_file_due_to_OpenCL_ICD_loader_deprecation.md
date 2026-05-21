# Stale file due to OpenCL ICD loader deprecation

> **Issue #4084**
> **状态**: closed
> **创建时间**: 2024-12-03T22:19:39Z
> **更新时间**: 2025-01-28T18:43:26Z
> **关闭时间**: 2025-01-28T18:43:24Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4084

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.3.0** (颜色: #303737)

## 描述

When upgrading from ROCm 6.2.x to ROCm 6.3.0, the [removal of the rocm-icd-loader package](https://rocm.docs.amd.com/en/docs-6.3.0/about/release-notes.html#opencl-icd-loader-separated-from-rocm) leaves a stale file in the old `rocm-6.2.x` directory. This has no functional impact. As a workaround, manually uninstall the `rocm-icd-loader` package to remove the stale file. This issue will be addressed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-01-28T18:43:24Z)

This has been resolved in ROCm 6.3.1 with the following changes https://github.com/ROCm/clr/commit/7c9c7a6332f69f740f59aaaeb83ad6eeff4598d6. The stale file is no longer present post upgrade.

---
