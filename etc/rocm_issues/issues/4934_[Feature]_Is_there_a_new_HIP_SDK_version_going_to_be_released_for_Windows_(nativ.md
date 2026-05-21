# [Feature]: Is there a new HIP SDK version going to be released for Windows (native)?

> **Issue #4934**
> **状态**: closed
> **创建时间**: 2025-06-17T08:06:21Z
> **更新时间**: 2025-06-18T14:20:20Z
> **关闭时间**: 2025-06-18T14:20:19Z
> **作者**: cmpute
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4934

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

The last published HIP SDK for windows is 6.2.4 (https://www.amd.com/en/developer/resources/rocm-hub/) which doesn't support RDNA4 cards. Is there any plan to release a HIP SDK for windows with RDNA4 support?

### Operating System

Windows

### GPU

RX 9070

### ROCm Component

_No response_

---

## 评论 (4 条)

### 评论 #1 — cmpute (2025-06-17T08:09:40Z)

I came to ROCm repo because downstream applications are pending support for windows: https://github.com/ollama/ollama/issues/9812

---

### 评论 #2 — harkgill-amd (2025-06-17T16:22:19Z)

Hi @cmpute, a new HIP SDK release with RDNA4 support is planned for release in the coming months.

In the meantime, you can try [TheRock](https://github.com/ROCm/TheRock) which allows users to build ROCm/HIP on native Windows for the 9000 series. The project is under active development and currently supports a subset of the complete ROCm component list. For more information, see https://github.com/ROCm/TheRock/blob/main/docs/development/windows_support.md.

---

### 评论 #3 — cmpute (2025-06-18T02:30:43Z)

@harkgill-amd thanks for your information! Looking forward to it!

---

### 评论 #4 — harkgill-amd (2025-06-18T14:20:20Z)

No problem!

---
