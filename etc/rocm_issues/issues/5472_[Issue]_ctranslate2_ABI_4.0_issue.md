# [Issue]: ctranslate2 ABI 4.0 issue

> **Issue #5472**
> **状态**: closed
> **创建时间**: 2025-10-05T13:16:54Z
> **更新时间**: 2026-05-07T14:43:13Z
> **关闭时间**: 2026-05-07T14:43:12Z
> **作者**: hayloftbisque
> **标签**: Feature Request, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5472

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

the fork is so much behind that it can not be used as a replacement for the current ctranslate2 shared lib. its not possible if ctranslate2 is used in a cpp project and the user wants to use it with rocm, which projects that are up to date

### Operating System

all

### CPU

all

### GPU

all

### ROCm Version

all

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-10-06T14:48:32Z)

Hi @hayloftbisque. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — hayloftbisque (2025-10-07T12:04:52Z)

I think ROCm 7.0+ isnt supported yet for ctranslate2

---

### 评论 #3 — harkgill-amd (2025-10-15T14:46:28Z)

> I think ROCm 7.0+ isnt supported yet for ctranslate2

Our fork, https://github.com/ROCm/CTranslate2, hasn't been updated for ROCm 7.0 yet. I've brought this up with the maintainers and we're scoping out what needs to be done to add support for our latest release. Will provide any updates on this thread.

---

### 评论 #4 — hayloftbisque (2025-12-24T19:12:10Z)

@harkgill-amd tehrr seems to be prs for both features. What’s the state. Will it get merged/used. How long till it’s ready?

---

### 评论 #5 — harkgill-amd (2026-05-07T14:43:12Z)

With https://github.com/ROCm/CTranslate2/pull/2, our for fork now has ROCm 7 support for CTranslate2! Will close this issue out but feel free to leave a comment if you have any questions.

---
