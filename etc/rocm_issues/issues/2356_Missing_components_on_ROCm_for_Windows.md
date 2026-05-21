# Missing components on ROCm for Windows

> **Issue #2356**
> **状态**: closed
> **创建时间**: 2023-07-30T11:33:04Z
> **更新时间**: 2023-07-30T13:15:01Z
> **关闭时间**: 2023-07-30T13:15:01Z
> **作者**: evshiron
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2356

## 描述

Greetings.

I am experimenting with ROCm for Windows, but I can't find MIOpen, RCCL, ROCr (`hsa-runtime64`) and rocTracer, which are required to compile PyTorch for ROCm on Linux.

Did I miss anything?

---

## 评论 (2 条)

### 评论 #1 — Jan-Huber (2023-07-30T13:06:28Z)

https://rocm.docs.amd.com/en/docs-5.5.1/rocm.html#rocm-on-windows

Neither AI Libraries nor AI Frameworks are available for ROCm on Windows

---

### 评论 #2 — evshiron (2023-07-30T13:15:01Z)

@Jan-Huber 

Thank you! Honestly, I didn't get to that section. But it's good to see the first step on Windows 🚀

---
