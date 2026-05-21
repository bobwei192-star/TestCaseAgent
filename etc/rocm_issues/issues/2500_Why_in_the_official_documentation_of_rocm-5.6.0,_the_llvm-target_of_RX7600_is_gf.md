# Why in the official documentation of rocm-5.6.0, the llvm-target of RX7600 is gfx1100

> **Issue #2500**
> **状态**: closed
> **创建时间**: 2023-09-26T08:36:09Z
> **更新时间**: 2023-10-08T04:26:26Z
> **关闭时间**: 2023-10-08T04:26:26Z
> **作者**: JiaJiDuan
> **标签**: hardware:Radeon
> **URL**: https://github.com/ROCm/ROCm/issues/2500

## 标签

- **hardware:Radeon** (颜色: #2B113F)

## 负责人

- Naraenda

## 描述

I learned through rocminfo that my RX7600 corresponds to gfx1102. But in the official documents, it is gfx1100 that is tested. Why?
[https://rocm.docs.amd.com/en/docs-5.6.0/release/windows_support.html](url)  
Is RX7600 officially supported on linux?  
What should my llvm-target set for RX7600 on a Ubuntu system?  



---

## 评论 (3 条)

### 评论 #1 — YellowRoseCx (2023-09-28T17:28:24Z)

Good catch, I've added it to the others in my pull request https://github.com/RadeonOpenCompute/ROCm/pull/2497

---

### 评论 #2 — evshiron (2023-09-29T15:53:04Z)

@JiaJiDuan 

> What should my llvm-target set for RX7600 on a Ubuntu system?

I am afraid treating it as `gfx1100` via `export HSA_OVERRIDE_GFX_VERSION=11.0.0` should just work.

---

### 评论 #3 — JiaJiDuan (2023-10-08T04:26:26Z)

Thank you for your answers, I will close this issue.

---
