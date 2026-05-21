# [Feature]: JIT compilation

> **Issue #3170**
> **状态**: open
> **创建时间**: 2024-05-28T19:01:08Z
> **更新时间**: 2024-06-24T15:17:15Z
> **作者**: DemiMarie
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3170

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

ROCm currently requires ahead-of-time compilation, which results in very large packages with limited hardware support.  CUDA, on the other hand, uses just-in-time compilation: software is shipped as an IR, and the runtime compiles only the code the user actually needs.  It would be nice if ROCm had the same ability.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (1 条)

### 评论 #1 — b-sumner (2024-05-28T21:04:55Z)

@DemiMarie this is a frequently requested feature and we are exploring approaches that should help.

---
