# Applications using OpenCV might fail due to package incompatibility between the OS

> **Issue #5501**
> **状态**: closed
> **创建时间**: 2025-10-10T22:49:13Z
> **更新时间**: 2026-01-28T16:18:26Z
> **关闭时间**: 2026-01-28T16:18:26Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.2
> **URL**: https://github.com/ROCm/ROCm/issues/5501

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.2** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

OpenCV packages built on Ubuntu 24.04 are incompatible with Debian 13 due to a version conflict. As a result, applications, tests, and samples that use OpenCV might fail. As a workaround, rebuild OpenCV with the version corresponding to Debian 13 from source, followed by the application that uses OpenCV. This issue will be fixed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-01-28T16:18:26Z)

Resolved in ROCm 7.2.0.

---
