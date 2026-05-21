# [Feature]: Pytorch ROCM Windows?

> **Issue #4045**
> **状态**: closed
> **创建时间**: 2024-11-21T06:10:45Z
> **更新时间**: 2025-09-26T18:56:16Z
> **关闭时间**: 2025-09-26T18:29:43Z
> **作者**: johnnynunez
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4045

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

https://github.com/pytorch/pytorch/pull/137279

when will it merged to compile pytorch from windows?

### Operating System

Windows

### GPU

_No response_

### ROCm Component

HIP SDK

---

## 评论 (14 条)

### 评论 #1 — schung-amd (2024-11-22T16:24:15Z)

Hi @johnnynunez, native Pytorch support on Windows for AMD GPUs will involve more than just this PR. We're aware that this is a need for many users and are working on it; stay tuned for formal announcements from AMD in the future. Thanks for your interest!

---

### 评论 #2 — johnnynunez (2024-11-22T16:32:30Z)

> Hi @johnnynunez, native Pytorch support on Windows for AMD GPUs will involve more than just this PR. We're aware that this is a need for many users and are working on it; stay tuned for formal announcements from AMD in the future. Thanks for your interest!

oh thank you! Do you have an idea or deadline about that? I would like show to general public, about rocm status on youtube channels etc and promote ROCM and RDNA, I have w7900 dual slot

---

### 评论 #3 — schung-amd (2024-11-22T16:37:40Z)

Unfortunately, there is no information we can provide about the timeline for this at the moment.

---

### 评论 #4 — johnnynunez (2024-12-04T08:35:23Z)

Will it be rocm 6.3.0 for windows?

---

### 评论 #5 — RoyiAvital (2025-01-17T08:37:01Z)

Could you share some info on the process?

It would be great to have PyTorch support on Windows.
Especially with the upcoming Strix Halo CPU's.

---

### 评论 #6 — johnnynunez (2025-02-14T16:17:39Z)

https://github.com/ROCm/pytorch/issues/1802#issuecomment-2649202534

---

### 评论 #7 — jammm (2025-06-04T11:48:41Z)

There's unofficial native pytorch wheels available in https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x built using [TheRock](https://github.com/ROCm/TheRock). Feel free to try it!

Note that these wheels are unofficial, is in active development, and there might still be issues. I don't recommend trying this if you're not willing to fiddle around. 

---

### 评论 #8 — johnnynunez (2025-06-04T20:50:49Z)

> There's unofficial native pytorch wheels available in https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x built using [TheRock](https://github.com/ROCm/TheRock). Feel free to try it!
> 
> Note that these wheels are unofficial, is in active development, and there might still be issues. I don't recommend trying this if you're not willing to fiddle around.

How did you access to rocm 6.5?

---

### 评论 #9 — jammm (2025-06-04T21:02:08Z)

> > There's unofficial native pytorch wheels available in https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x built using [TheRock](https://github.com/ROCm/TheRock). Feel free to try it!
> > Note that these wheels are unofficial, is in active development, and there might still be issues. I don't recommend trying this if you're not willing to fiddle around.
> 
> How did you access to rocm 6.5?

It's the dev branch built using TheRock which builds from the dev branches of all OSS ROCm repos. See https://github.com/ROCm/TheRock

---

### 评论 #10 — johnnynunez (2025-06-04T21:35:03Z)

> > > There's unofficial native pytorch wheels available in https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x built using [TheRock](https://github.com/ROCm/TheRock). Feel free to try it!
> > > Note that these wheels are unofficial, is in active development, and there might still be issues. I don't recommend trying this if you're not willing to fiddle around.
> > 
> > 
> > How did you access to rocm 6.5?
> 
> It's the dev branch built using TheRock which builds from the dev branches of all OSS ROCm repos. See https://github.com/ROCm/TheRock

Interesting! Thanks

---

### 评论 #11 — art-Gam (2025-09-25T16:18:47Z)

It's been a long time but ROCm pytorch is coming with another preview version and "How to..." from AMD:
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html

---

### 评论 #12 — RoyiAvital (2025-09-26T18:36:03Z)

Will the support be integrated into PyTorch like the `mps`, `cuda` and `xpu` backends?

---

### 评论 #13 — jammm (2025-09-26T18:39:02Z)

> Will the support be integrated into PyTorch like the `mps`, `cuda` and `xpu` backends?

It's re-used as the `cuda` backend. There's no specific `hip` backend on PyTorch. It's intentional to allow PyTorch to run as-is across CUDA and HIP GPUs.

---

### 评论 #14 — RoyiAvital (2025-09-26T18:56:16Z)

I can see the logic when targeting existing code.  
Yet it would be great to have similar experience to a CUDA backend when just installing the regular PyTorch.  

Under the assumption PyTorch itself won't accept a pull where if one use `hip` backend then it overrides `cuda` I can see what you did.
I wonder if design wise, with some Python magic you could do something like:

1. Integrate an official `hip` backend into PyTorch.  
   This should work for new users just like any backend.
2. An AMD special package, with a Macro / Scope or any other Python magic, can redirect `cuda` based PyTorch code to use the official `hip` backend.

This design will get you best of both world.  
For users of PyTorch writing new code everything works out of the box with the official PyTorch.  
For those with `cuda` backend code, they will install a dedicated package, as they do now, which shadows `cuda` backend by the `hip` backend.

---
