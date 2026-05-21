# [Documentation]: download error of triton-3.5.1 when Installing PyTorch for Ryzen APUs

> **Issue #5946**
> **状态**: closed
> **创建时间**: 2026-02-10T12:38:12Z
> **更新时间**: 2026-02-11T00:51:49Z
> **关闭时间**: 2026-02-10T19:54:56Z
> **作者**: zenfey
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5946

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Description of errors

Hi, when I install pytorch on my APU machine Ubuntu 24.04 according to the link https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html, running command wget for triton-3.5.1 results an error as below. 

<img width="2023" height="175" alt="Image" src="https://github.com/user-attachments/assets/edd7c243-0521-4b4e-b365-25cb9ec38ff1" />

This version 3.5.1 seems depends on the bunch of whl packages. When I use the last 3.4.0 version of triton, the installation aborted.

<img width="937" height="352" alt="Image" src="https://github.com/user-attachments/assets/6445945b-c319-4089-a924-6d0914d883a9" />

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2026-02-10T16:35:09Z)

Thanks for catching this @zenfey. Let me check whether we're missing the `3.5.1` wheel or if we should be pointing to a lesser versioned wheel.

---

### 评论 #2 — jj123451 (2026-02-10T19:25:15Z)

looks like it's fixed 
<img width="1047" height="342" alt="Image" src="https://github.com/user-attachments/assets/b1c4b601-006f-439a-b21d-933f8452f087" />

---

### 评论 #3 — harkgill-amd (2026-02-10T19:54:56Z)

Yup, the `triton-3.5.1` wheels were removed but have since been reuploaded. Thanks again!

---

### 评论 #4 — zenfey (2026-02-11T00:51:49Z)

Hi, I've just install pytorch successfully. Thanks for the fix 👍 

---
