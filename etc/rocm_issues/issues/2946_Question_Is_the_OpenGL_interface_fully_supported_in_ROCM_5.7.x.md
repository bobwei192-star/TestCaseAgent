# Question: Is the OpenGL interface fully supported in ROCM 5.7.x?

> **Issue #2946**
> **状态**: closed
> **创建时间**: 2024-03-06T08:34:09Z
> **更新时间**: 2024-08-14T03:29:48Z
> **关闭时间**: 2024-04-13T02:58:54Z
> **作者**: lilx-dev
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2946

## 描述

Hello, I would like to ask about some interfaces of OpenGL in ROCM 5.7.x version, especially the following three interfaces: HipGLGetDevices, hipGraphicsGLRegisterBuffer and hipGraphicsGLRegisterImage, whether to fully support the three interfaces, about the three interfaces, whether have drawbacks.
I hope to hear from you soon. Thank you very much!

---

## 评论 (4 条)

### 评论 #1 — nartmada (2024-04-13T02:58:54Z)

@lisa123456-cell, sorry for not responding sooner.  After checking with the internal team, HIP runtime should support all those 3 interfaces under Linux.

---

### 评论 #2 — lilx-dev (2024-04-13T03:08:54Z)

Thank you. That means the functions corresponding to the three interfaces are fully supported, right? There's no imperfection, is there?

---

### 评论 #3 — nartmada (2024-04-13T03:11:12Z)

The 3 interfaces are fully supported.  Are you seeing some issues?

---

### 评论 #4 — lilx-dev (2024-04-13T03:14:38Z)

No problems have been found so far. I just want to confirm whether the functions of these three interfaces are perfect. Thank you very much for your answer！

---
