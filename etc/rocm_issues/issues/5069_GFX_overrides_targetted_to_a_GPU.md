# GFX overrides targetted to a GPU

> **Issue #5069**
> **状态**: closed
> **创建时间**: 2025-07-19T14:47:53Z
> **更新时间**: 2025-07-22T06:28:55Z
> **关闭时间**: 2025-07-22T06:28:55Z
> **作者**: Blaze-Leo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5069

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

So I have a 9060XT 16GB and a RX 6600 8GB, I am using `rocm6.4`. Since the 9060XT is `gfx1200` it is working well but since the 6600 is `gfx1032`, I have to override it to `gfx1030`. 

Both individually are working, but I cannot get them to work simultaneously. When I use `os.environ['HSA_OVERRIDE_GFX_VERSION'] = '10.3.0'` all the GPU gfx versions change to gfx1030, so the 9060XT becomes unusable. 

Is there any way to assign GFX overrides to a specific GPU, or can the 6600 be permanently overridden to gfx1030, or will there ever be any official support for `gfx1032`?

### Operating System

Ubuntu 24.04

### GPU

9060XT 16GB and RX6600 8GB

### ROCm Component

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-07-21T14:05:33Z)

Hi @Blaze-Leo. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — kentrussell (2025-07-21T14:29:15Z)

This feature got merged back in ROCm 6.2, in the thunk, but that was included in the ROCr merge. See
https://github.com/ROCm/ROCT-Thunk-Interface/pull/104#issuecomment-2760479694
for more info on it

---

### 评论 #3 — Blaze-Leo (2025-07-21T15:35:51Z)

Thanks, I will try this, when I searched for this issue somehow that post didn't show up.

---

### 评论 #4 — kentrussell (2025-07-21T16:43:33Z)

Not to worry. It took me 20min to find it, and I knew what I was looking for... Since we deprecated the thunk and merged it into ROCr, it's been harder to find things that went in there first.

---
