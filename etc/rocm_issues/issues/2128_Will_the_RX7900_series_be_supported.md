# Will the RX7900 series be supported?

> **Issue #2128**
> **状态**: closed
> **创建时间**: 2023-05-10T18:13:06Z
> **更新时间**: 2023-05-11T17:37:06Z
> **关闭时间**: 2023-05-11T17:37:06Z
> **作者**: MomijiHanako
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2128

## 描述

I hope so.

---

## 评论 (1 条)

### 评论 #1 — TheCowboyHermit (2023-05-11T02:34:37Z)

7900 XTX is not supported as of ROCm 5.5.0 despise some commenting suggesting that it may be supported (RDNA3). I have tested ROCm 5.5.0 and modified Stable Diffusion Webui to run on ROCm proper and also tested custom models too. In all cases, it fail and it fails directly in hip libraries.

My advice at this point is to consider ROCm a long term project that may come at the end of this year at soonest and likely next year June which is my assumption. And to look into neural net framework focusing on Vulkan API instead, rather than ROCm, it exists for far longer and is very much well supported on AMD GPU in comparison. Pytorch support for Vulkan is still at it's early stage and I have provided a link to it:

<https://pytorch.org/tutorials/prototype/vulkan_workflow.html>

If I may be allowed to add my biased opinion on ROCm, I think ROCm is not worth the effort to invest when more could be invested on Vulkan Compute instead especially in machine learning endeavor.

---
