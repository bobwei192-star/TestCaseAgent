# running on stream 0 and syncing stream 0 is faster than on other stream

> **Issue #2504**
> **状态**: closed
> **创建时间**: 2023-09-27T18:01:42Z
> **更新时间**: 2024-08-12T19:22:23Z
> **关闭时间**: 2024-08-12T19:22:23Z
> **作者**: jinhongyii
> **标签**: hardware:Radeon
> **URL**: https://github.com/ROCm/ROCm/issues/2504

## 标签

- **hardware:Radeon** (颜色: #2B113F)

## 描述

I tried two approaches to run a program. In the first approach, I launch all the computation and rccl kernels on stream 0, and use hipStreamSynchronize to sync with stream 0 to ensure all the kernels are completed. In the second approach, I hipStreamCreate a new stream and launch all the kernels on it. Also, I use hipStreamSynchronize to sync with the created stream in the end. It's a bit surprising to me that approach 0 is 25% faster than approach 1. Is this an expected behavior? 

---

## 评论 (3 条)

### 评论 #1 — jinhongyii (2023-09-27T18:02:12Z)

My hardware is rtx 7900 xtx, and my rocm version is 5.7.

---

### 评论 #2 — schung-amd (2024-07-19T19:23:22Z)

Hi @jinhongyii, can you provide the code you used when encountering this issue, or if not, any other code which exhibits this behaviour? Thanks!

---

### 评论 #3 — schung-amd (2024-08-12T19:22:23Z)

Closing this issue for now, feel free to reopen with more details if you are still experiencing this issue on current ROCm. Running all of your computation on a new stream is not expected to provide any performance benefits, as the advantage of using streams is being able to compute with multiple streams concurrently. Without source code, it is difficult to say whether there is actually an issue here.

---
