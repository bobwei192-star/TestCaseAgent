# [Documentation]: RDNA 3.5 details missing from Accelerator and GPU hardware specifications

> **Issue #5445**
> **状态**: closed
> **创建时间**: 2025-09-29T16:07:05Z
> **更新时间**: 2026-02-18T15:56:12Z
> **关闭时间**: 2026-02-18T15:56:12Z
> **作者**: Snektron
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5445

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Description of errors

The "Accelerator and GPU hardware specifications" page lists almost all (recent-ish) AMD architectures, except those from RDNA 3.5. There is quite some interest in using these architectures for ROCm, and those details are a useful reference even outside of ROCm. Specifically, the details for Radeon 8060S, Radeon 8050S, and Radeon 80480S are missing.

### Attach any links, screenshots, or additional evidence you think will be helpful.

https://rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html#accelerator-and-gpu-hardware-specifications

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-09-30T17:16:02Z)

Hi @Snektron, thanks for the heads up. The GPU specification page should definitely have these APUs as we're ramping up support for them. Will work with the docs team to get these in.

---

### 评论 #2 — harkgill-amd (2026-01-16T20:03:40Z)

@Snektron, the APU entries have now been added to the GPU specs table at https://rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html.

---
