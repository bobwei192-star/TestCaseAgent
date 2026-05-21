# hipLaunchCooperativeKernel slowdown

> **Issue #3410**
> **状态**: closed
> **创建时间**: 2024-07-10T12:39:51Z
> **更新时间**: 2025-04-17T13:01:57Z
> **关闭时间**: 2025-04-16T19:32:40Z
> **作者**: elbriggs
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/3410

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

I wanted to try using Cooperative groups as appears as if it would be helpful in some future work. I began by trying to launch a kernel using hipLaunchCooperativeKernel. Note that this kernel did not use any cooperative features I was just trying to get the framework in place to start implementing them. The kernel ran correctly but was an order of magnitude slower than when launched in the normal way. I tried running it with only 1 thread block and observed the same behavior. My question is if this is the expected behavior for the current implementation. If so I'll just shelve the idea for now.

### Operating System

22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD EPYC 7443P 24-Core Processor

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-07-16T15:48:38Z)

Hi @elbriggs, I will confirm the expected behaviour with our internal team and let you know.

---

### 评论 #2 — yiakwy-xpu-ml-framework-team (2025-01-26T03:32:24Z)

@elbriggs this feature will be used in this [PR#3137](https://github.com/sgl-project/sglang/pull/3137). Could we confirm the performance issue havs been resolved ?

---

### 评论 #3 — harkgill-amd (2025-04-16T19:32:41Z)

@elbriggs, there have been fixes put in since this ticket was opened which improve the performance of `hipLaunchCooperativeKernel`. Could you please retest this with ROCm 6.4.0 when you get a chance? If the issue persists, I will re-open this ticket, thanks!

---

### 评论 #4 — elbriggs (2025-04-17T13:01:56Z)

Thanks @harkgill-amd  I'm busy with some other stuff right now but will get back to this and let you know what I find.

---
