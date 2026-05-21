# [Issue]: Proble with HSA_OVERRIDE_GFX_VERSION

> **Issue #3065**
> **状态**: closed
> **创建时间**: 2024-04-25T12:54:44Z
> **更新时间**: 2024-06-04T23:27:23Z
> **关闭时间**: 2024-04-25T17:58:33Z
> **作者**: Who-are-me
> **标签**: AMD Radeon VII, ROCm 5.6.0
> **URL**: https://github.com/ROCm/ROCm/issues/3065

## 标签

- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 5.6.0** (颜色: #ededed)

## 描述

### Problem Description

How is set HSA_OVERRIDE_GFX_VERSION for each GPU?

### Operating System

OpenSUSE Leap 15.5

### CPU

r7 2700

### GPU

AMD Radeon VII

### ROCm Version

ROCm 5.6.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — nartmada (2024-04-25T17:23:55Z)

Hi @Who-are-me, your "AMD Radeon VII" is a supported GPU.  You don't need to use HSA_OVERRIDE_GFX_VERSION.  

---

### 评论 #2 — nartmada (2024-04-25T17:58:33Z)

@Who-are-me, you can also google "how to use HSA_OVERRIDE_GFX_VERSION".  Thanks.

---

### 评论 #3 — Who-are-me (2024-04-25T18:28:22Z)

Thx, but HSA_OVERRIDE_GFX_VERSION work on all GPUs, it's possible override version for one specific GPU (for example for second gpu)?

---

### 评论 #4 — Who-are-me (2024-04-25T18:28:51Z)

for example for second GPU (rx 6600)

---

### 评论 #5 — keryell (2024-04-26T10:11:08Z)

OK, so you want a way to have an `HSA_OVERRIDE_GFX_VERSION` per GPU on an heterogeneous multi-GPU system?

---

### 评论 #6 — Who-are-me (2024-04-26T10:24:18Z)

Yes, it's possible?

---

### 评论 #7 — AdamNiederer (2024-06-04T23:27:22Z)

I ran into the same issue; I believe https://github.com/ROCm/ROCT-Thunk-Interface/pull/104 would solve this.

---
