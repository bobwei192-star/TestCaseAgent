# ROCm Validation Suite (RVS) needs specified configuration file

> **Issue #4090**
> **状态**: closed
> **创建时间**: 2024-12-03T22:20:04Z
> **更新时间**: 2025-01-28T19:14:12Z
> **关闭时间**: 2025-01-28T19:14:11Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4090

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.3.0** (颜色: #303737)

## 描述

ROCm Validation Suite might fail for certain platforms if executed without the `-c` option and specifying the configuration file. See [RVS command line options](https://rocm.docs.amd.com/projects/ROCmValidationSuite/en/docs-6.3.0/ug1main.html#command-line-options) for more information. This issue will be addressed in a future release.

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-01-28T19:14:11Z)

The default configuration file was reintroduced in ROCm 6.3.1 with https://github.com/ROCm/ROCmValidationSuite/commit/60734d2c19a77702d07fdbc7e0e9b1f453b3d3d3. This file will continue to be referenced if the `-c` option is not passed in the command line.

---
