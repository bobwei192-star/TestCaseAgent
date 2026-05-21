# [Feature]: ROCm supports SgLang

> **Issue #3744**
> **状态**: closed
> **创建时间**: 2024-09-18T03:53:05Z
> **更新时间**: 2025-08-06T08:26:49Z
> **关闭时间**: 2024-12-04T14:44:33Z
> **作者**: githust66
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3744

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

ROCm supports SgLang and vLLM

### Operating System

ubuntu 22.04

### GPU

7900xt

### ROCm Component

torch2.4.0+ROCm 6.1

---

## 评论 (6 条)

### 评论 #1 — githust66 (2024-11-22T03:17:39Z)

At present, ROCm 6.2 already supports vLLM, is there a plan to support SgLang in the future?

---

### 评论 #2 — harkgill-amd (2024-12-03T18:35:53Z)

Hi @githust66, you can find instructions on how to run SGLang with ROCm in our newly published blog, [SGLang: Fast Serving Framework for Large Language and Vision-Language Models on AMD GPUs](https://rocm.blogs.amd.com/artificial-intelligence/sglang/README.html).

You can also find AMD/ROCm specific install instructions directly on the [SGLang project page](https://sgl-project.github.io/start/install.html#install-sglang). These developments are fairly new and as such, only MI/Instinct cards are currently supported. 

---

### 评论 #3 — githust66 (2024-12-04T02:15:00Z)

> Hi @githust66, you can find instructions on how to run SGLang with ROCm in our newly published blog, [SGLang: Fast Serving Framework for Large Language and Vision-Language Models on AMD GPUs](https://rocm.blogs.amd.com/artificial-intelligence/sglang/README.html).
> 
> You can also find AMD/ROCm specific install instructions directly on the [SGLang project page](https://sgl-project.github.io/start/install.html#install-sglang). These developments are fairly new and as such, only MI/Instinct cards are currently supported.

OK, Thanks. My gfx1100 already uses SgLang

---

### 评论 #4 — harkgill-amd (2024-12-04T14:44:34Z)

Even better! Feel free to create a new issue if you encounter any difficulties running SGLang.

---

### 评论 #5 — dazipe (2025-02-12T19:34:01Z)

> > Hi [@githust66]
> OK, Thanks. My gfx1100 already uses SgLang

Could you please share your experience with the SGLang vs vLLM or Llama.cpp. Token generation, memory consumption, etc...


---

### 评论 #6 — a-huk (2025-08-06T08:26:49Z)

Hello @githust66,

Could you quickly explain how you got it to run on a 7900XTX, I am struggling...

Thank you

---
