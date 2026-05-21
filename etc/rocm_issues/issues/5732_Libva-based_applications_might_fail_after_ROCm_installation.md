# Libva-based applications might fail after ROCm installation

> **Issue #5732**
> **状态**: closed
> **创建时间**: 2025-12-02T18:35:15Z
> **更新时间**: 2026-02-18T17:26:44Z
> **关闭时间**: 2026-02-18T17:26:44Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.2
> **URL**: https://github.com/ROCm/ROCm/issues/5732

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.2** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

After installing ROCm, certain applications that are dependent on the libva library (such as `vainfo` and `ffmpeg`) might fail to function correctly. This issue is only relevant if you're using libva-based applications outside of ROCm on RHEL 8.10 and Oracle Linux 8. The failure occurs due to a symbol clash between the AMD-packaged `libva-amdgpu` and the system-provided libva. This conflict was introduced when adapting the RHEL 8 build to support additional operating systems, which required changes to the build options. The issue will be fixed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-02-18T17:26:29Z)

Resolved in ROCm 7.2.0.

---
