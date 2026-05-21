# [QUESTION] Quotesion related to HSA_OVERRIDE_GFX_VERSION and optimization? 

> **Issue #2976**
> **状态**: closed
> **创建时间**: 2024-03-25T13:02:23Z
> **更新时间**: 2024-07-17T14:16:41Z
> **关闭时间**: 2024-07-17T14:16:41Z
> **作者**: serhii-nakon
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2976

## 描述

I not fully understand does this variable is solution or just trick/workaround. I mean if we can use gfx1100 code for gfx1103 or gfx1102 why just not link all this codes internally inside ROCM why it force users to use this variable? Does it produce some problem (like performance or etc) of using existing code but for another compatible GPU

Also I want to know what difference in case if I rebuild ROCM especially for gfx1102 or gfx1103, does it will produce exactly the same files like for gfx1100 but with another name or it will produce optimized code/files for specific architecture?

If it produce optimized code, what parts of already prebuilt ROCM need to rebuild - if I correctly understand it should be enough to rebuild only this packages: rocBLAS, rocFFT, rocSPARSE, MIOpen, rocRAND, rccl... is not it?

---

## 评论 (6 条)

### 评论 #1 — serhii-nakon (2024-03-25T13:06:38Z)

I ask about it because this https://salsa.debian.org/rocm-team/community/team-project/-/wikis/Supported-GPU-list#architecture-notes show that ROCM can technically work with almost all GPUs. And I need to know what the best way to use ROCM for unofficially supported GPUs. Does better to rebuild or just use env variable and it will do exactly the same as for rebuild...

---

### 评论 #2 — GZGavinZhao (2024-03-25T20:07:11Z)

Perhaps [this thread](https://www.reddit.com/r/ROCm/comments/1bd8vde/comment/kvux38v/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) on Reddit may answer some of your questions.

tl;dr: `HSA_OVERRIDE_GFX_VERSION` shouldn't bring any noticeable performance regression and I don't recall ever seeing anyone reporting so. If you do suspect there are significant regressions, please benchmark and file a bug report :)

---

### 评论 #3 — serhii-nakon (2024-03-25T21:59:12Z)

@GZGavinZhao Hello
Hmm, I just now have laptop with gfx1012 with pre-compiled ROCm 5.4 for especially for it, if it true that 6.1 will released with gfx1010 I will benchmark it.

---

### 评论 #4 — serhii-nakon (2024-03-25T22:51:25Z)

@GZGavinZhao One more question where I can check all available gfx101* in new ROCm release? Also does it mean that Docker container will with already prebuild ML frameworks? 
Because I don't see here gfx101* https://hub.docker.com/layers/rocm/pytorch-nightly/latest/images/sha256-9520c161d80bc72132b54ebcd32bd1ac842d18ecd73099dcab81c1d5f416c7ab?context=explore

---

### 评论 #5 — ppanchad-amd (2024-07-04T15:56:33Z)

@serhii-nakon gfx101* series are not supported in the latest ROCm 6.1.2 release. Please let me know if this ticket can be closed. Thanks!

---

### 评论 #6 — serhii-nakon (2024-07-16T18:11:36Z)

@ppanchad-amd Hello, yes you can

---
