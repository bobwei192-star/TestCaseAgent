# [Issue]: torch 2.9 + rocm7.1 release as a docker image in `rocm/pytorch`

> **Issue #5695**
> **状态**: closed
> **创建时间**: 2025-11-25T19:35:04Z
> **更新时间**: 2025-12-12T17:43:17Z
> **关闭时间**: 2025-12-12T17:43:01Z
> **作者**: fxmarty-amd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5695

## 描述

### Problem Description

Hi,

I noticed there is no docker image for torch 2.9 + rocm 7.1 at https://hub.docker.com/r/rocm/pytorch/tags. Do you know why is that?

`rocm/vllm-dev:nightly_main_20251117` contains a certain `2.9.0a0+git1c57644`, which seems to come from https://github.com/vllm-project/vllm/blob/c32a18cbe7342ac0700802b94ae98bbf928a00f0/docker/Dockerfile.rocm_base#L4 i.e. https://github.com/ROCm/pytorch/commit/1c57644d4cb3aff84642e1326d88681a656507ce

Any chance to get a pytorch 2.9 stable + rocm 7.1 release, as a standalone docker image?

PyTorch 2.10 release is only planned end January (see https://dev-discuss.pytorch.org/t/pytorch-release-2-10-key-dates-updated/3259), and using nightly is not the greatest of ideas.

Thank you!

### Operating System

Irrelevant

### CPU

Irrelevant

### GPU

Irrelevant

### ROCm Version

Irrelevant

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — ianbmacdonald (2025-11-29T00:42:38Z)

If you follow that breadcrumb, you might wonder as I do, why AMD is not using the release below in the current nightly.  My guess is just the slow roll of CI when you need to make sure stability [on CDNA platforms] is maintained for all active use cases. 

https://github.com/ROCm/pytorch/commits/release/2.9_aiter_update

This version brings it past the a0 alpha release to 2.9.0 now supported by ROCm 7.1.1, fixes dependency issues in uv venvs by droping the alpha, and improves alignment with submodules for triton and aiter.  Seems like a no brainer for vllm builds, and I use it for my py2.9 wheels currently.   

---

### 评论 #2 — fxmarty-amd (2025-12-12T17:43:00Z)

Closing as torch 2.9 + rocm7.1 images have been released on https://hub.docker.com/r/rocm/pytorch/tags

---
