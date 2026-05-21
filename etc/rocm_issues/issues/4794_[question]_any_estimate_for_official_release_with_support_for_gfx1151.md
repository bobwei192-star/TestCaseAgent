# [question] any estimate for official release with support for gfx1151?

> **Issue #4794**
> **状态**: closed
> **创建时间**: 2025-05-23T12:11:00Z
> **更新时间**: 2025-05-27T14:14:38Z
> **关闭时间**: 2025-05-27T14:12:46Z
> **作者**: bugbuster-dev
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4794

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

any estimate for official release with support for gfx1151? is there a development branch/patches for gfx1151 i can try?
and integration with vlllm?


---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-05-27T14:12:46Z)

Hi @bugbuster-dev, while I can't provide a timeline on official support for gfx1151, you can utilize TheRock to build ROCm for [gfx1151/Strix Halo](https://github.com/ROCm/TheRock/blob/main/cmake/therock_amdgpu_targets.cmake#L69). TheRock offers a subset of ROCm components with the [list](https://github.com/ROCm/TheRock/blob/main/.gitmodules) continually expanding. For more information and steps to get started with using TheRock, see the project description over at https://github.com/ROCm/TheRock. 

TheRock also includes underlying components for vLLM (hip, hipBLAS.etc) though I can't guarantee it'll work given that it's still in an early preview state. It would be great if you could give it a try and report back on any issues you run into over at https://github.com/ROCm/TheRock/issues. Thanks!

---
