# [Feature]: "real" just works™ wsl support

> **Issue #4018**
> **状态**: closed
> **创建时间**: 2024-11-08T05:53:46Z
> **更新时间**: 2024-11-08T20:00:44Z
> **关闭时间**: 2024-11-08T19:45:50Z
> **作者**: luantak
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4018

## 描述

### Suggestion Description

I've followed [this guide](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html), to install rocm in wsl. I've validated the install via "rocminfo" and the pytorch example.

I then installed ollama, unfortunately it didn't detect/ use the GPU via rocm. I then read the source to find out how [AMD GPU detection in ollama](https://github.com/ollama/ollama/blob/main/discover%2Famd_linux.go) works. I contemplated if I should raise an issue against ollama to make sure it also works under wsl, however I know this code works flawlessly on a bare-metal Linux installation so I don't really think ollama is at fault here.

After that I tried to install [invoke](https://github.com/invoke-ai/InvokeAI). The default installation didn't detect the GPU again so I used the workaround for pytorch from the docs to replace the relevant file in which then detected the GPU but also crashed due to some error.

In short this is really bad UX. I should follow the install guide and then just be able to run any rocm compatible application no tinkering required.

**Why don't you just install the "native" Windows version?**
I would like to administer these services remotely and administering Linux via ssh is way easier. I would also like to run some additional services which only have a Linux version.

**So why don't you just use a bare metal Linux install?**
I would, however this machine is also used as a shared console like gaming PC, so for broad game compatibility it has to run windows.

### Operating System

Windows 11 + WSL Ubuntu 22.04

### GPU

RX 7900xt

### ROCm Component

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-11-08T19:45:50Z)

Hi @lu4p, ROCm for WSL is currently a beta release. With that being said, there are architectural differences between the WSL implementation and baremetal Linux that can result in conflicting behaviors. Some of the architectural limitations are briefly touched on at [ROCm Support in Virtual Environments](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#rocm-support-in-wsl-environments). In the case of ollama, the GPU detection utilizes the `kfd` (Kernel Fusion Driver) device which exists within a regular ROCm Linux installation but is replaced with `dxg` inside WSL ([ref](https://github.com/ollama/ollama/blob/main/discover%2Famd_linux.go#L86-L87C44)). I understand this may pose challenges from a UX perspective; however, ROCm on WSL is still in its early development phases and there is constant work being done to improve both the implementation and support. 

Back to ollama, I did find a thread over at https://github.com/ollama/ollama/issues/5275#issuecomment-2270886785 which enables the usage of AMD GPUs through ROCm on WSL (Thanks to @justinkb and @evshiron). I gave this a try myself and was able to run models on a 7900XT but please note that this is not an official AMD recommended solution.  We are also planning to change the state of the discussions section in ROCm/ROCm to better promote this kind of community interaction and development. 

---
