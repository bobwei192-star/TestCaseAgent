# [Feature]: Will rocm 6.4 be supported for WSL2

> **Issue #4650**
> **状态**: closed
> **创建时间**: 2025-04-17T02:20:12Z
> **更新时间**: 2025-04-21T19:22:55Z
> **关闭时间**: 2025-04-21T14:01:28Z
> **作者**: Kademo15
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4650

## 描述

### Suggestion Description

ROCm 6.4 is quite a big update with a lot of sub modules reviving newer versions, it would be nice to get these improvements for WSL2 users.  

### Operating System

Windows 11, WSL2

### GPU

rx 7900xtx

### ROCm Component

ROCm

---

## 评论 (6 条)

### 评论 #1 — githust66 (2025-04-17T02:31:30Z)

Is supported, can be installed directly

---

### 评论 #2 — Apriqi (2025-04-17T07:09:03Z)

7800XT！！！！！！！
When？？？？？？？

---

### 评论 #3 — githust66 (2025-04-17T07:26:24Z)

>7800XT! ! ! ! ! ! ! When? ? ? ? ? ? ?

I have a 7900 series, the 7800 series probably doesn't support it yet

---

### 评论 #4 — Kademo15 (2025-04-17T17:48:29Z)

> Is supported, can be installed directly

@githust66 
When i tried and ran `torch.cuda.is_available()` it returned `false` did do something extra or just a plain install because for me it doesn't work.

---

### 评论 #5 — harkgill-amd (2025-04-21T14:01:28Z)

Official WSL support will be introduced in a future point release of ROCm 6.4. 

The 6.4 WSL packages that are currently hosted on repo.radeon.com have not completed full testing and their usage may result in errors/bugs. I'll close out this issue as the feature is already being planned for release. Feel free to continue using this thread/open a discussion post regarding using the pre-release WSL packages.

---

### 评论 #6 — Kademo15 (2025-04-21T19:22:55Z)

thanks for the confirmation @harkgill-amd 

---
