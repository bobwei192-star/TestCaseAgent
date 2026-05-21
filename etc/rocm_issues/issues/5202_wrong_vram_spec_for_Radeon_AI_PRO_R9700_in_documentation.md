# wrong vram spec for Radeon AI PRO R9700 in documentation

> **Issue #5202**
> **状态**: closed
> **创建时间**: 2025-08-16T20:03:34Z
> **更新时间**: 2025-08-18T14:10:46Z
> **关闭时间**: 2025-08-18T14:10:46Z
> **作者**: alexschroeter
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5202

## 描述

16 GiB is wrong according to [AMD website](https://www.amd.com/de/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html).

https://github.com/ROCm/ROCm/blob/55d0a88ec5200462d1fb18e60cc3782047cd2a15/docs/reference/gpu-arch-specs.rst?plain=1#L288C11-L288C15

---

## 评论 (1 条)

### 评论 #1 — darren-amd (2025-08-18T14:10:46Z)

Hi @alexschroeter,

Thanks for letting us know! This has been fixed in: https://github.com/ROCm/ROCm/pull/5203.

---
