# [Feature]: How to obtain the physical address given a device pointer?

> **Issue #2786**
> **状态**: closed
> **创建时间**: 2024-01-09T14:35:22Z
> **更新时间**: 2024-09-10T14:54:32Z
> **关闭时间**: 2024-09-10T14:54:31Z
> **作者**: xuantengh
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2786

## 描述

### Suggestion Description

NVIDIA provides a mechanism for developers to obtain the physical address of a allocated pointer [via their driver API](https://docs.nvidia.com/cuda/gpudirect-rdma/index.html). In AMD GPU and ROCm, is there any similar approach to achieve this, i.e., given a virtual address returned by `hipMalloc`, query the underlying phyiscal address corresponding to it.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (4 条)

### 评论 #1 — b-sumner (2024-01-09T15:49:41Z)

@Huangxt57 would you please comment on why the physical address is interesting/useful to you?

---

### 评论 #2 — xuantengh (2024-01-10T02:24:50Z)

> @Huangxt57 would you please comment on why the physical address is interesting/useful to you?

It's about my research. I'm conducting some dissecting/micro-benchmarking works to figure out the address mapping policy  between the physical address and the VRAM channels (memory module), i.e., data requests targeting on what address ranges will be directed into one memory module.

---

### 评论 #3 — b-sumner (2024-01-10T15:17:11Z)

Thanks for the information.

---

### 评论 #4 — alexxu-amd (2024-09-10T14:54:31Z)

Closing the issue for the same reason as: https://github.com/ROCm/ROCK-Kernel-Driver/issues/158

---
