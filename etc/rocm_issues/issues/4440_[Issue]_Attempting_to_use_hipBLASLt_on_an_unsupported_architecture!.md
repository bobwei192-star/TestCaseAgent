# [Issue]: Attempting to use hipBLASLt on an unsupported architecture!

> **Issue #4440**
> **状态**: closed
> **创建时间**: 2025-03-03T19:42:22Z
> **更新时间**: 2025-06-23T14:08:46Z
> **关闭时间**: 2025-06-23T14:08:46Z
> **作者**: garrettbyrd
> **标签**: Under Investigation, ROCm 6.2.2
> **URL**: https://github.com/ROCm/ROCm/issues/4440

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.2** (颜色: #ededed)

## 负责人

- schung-amd

## 描述

### Problem Description

This issue is posted it on behalf of OP on [this post from discuss.pytorch.org](https://discuss.pytorch.org/t/rocm-hipblaslt-error-with-gfx1103/212721).

PyTorch outputs the following when attempting to use HipBlasLt as the BLAS backend:

`UserWarning: Attempting to use hipBLASLt on an unsupported architecture! Overriding blas backend to hipblas`

The user has set `HSA_OVERRIDE_GFX_VERSION=11.0.0` on a machine using a Radeon 780M (`gfx1103` by default).

ROCm has been installed via [`pacman`](https://gitlab.archlinux.org/archlinux/packaging/packages/rocm-hip-sdk), HipBlasLt has been built/installed from [source](https://github.com/ROCm/hipBLASLt).

This minimal example is enough to reproduce the error:

```
>>> import torch
>>> t = torch.rand((5,5), device=0)
>>> l = torch.nn.Linear(5,5).to(0)
>>> l(t)
```

Arch is not a supported operating system, but this error is consistent with other reports on cards using `gfx1100`.

[Here](https://discuss.pytorch.org/t/rocm6-2-build-of-pytroch-is-faling-for-llama3-2-vision-model/211622) is another post from discuss.pytorch.org that reports a similar issues when using a Radeon 7900 XTX (natively `gfx1100`). For this user, it seems that updating PyTorch resolved the issue.

#4437 outlines a similar error in detail.

#3949 Describes this issue, and links to a relevant [issue](https://github.com/pytorch/pytorch/issues/138067) and [PR](https://github.com/pytorch/pytorch/pull/138267) on the pytorch repo. It seems that this PR was [eventually merged into the ROCm branch of pytorch](https://github.com/ROCm/pytorch/pull/1855).

Could we get verification that this issue no longer persists on `gfx1100`?

### Operating System

Arch Linux

### CPU

Unknown

### GPU

AMD Radeon 780M

### ROCm Version

ROCm 6.2.2

### ROCm Component

hipBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — schung-amd (2025-03-03T22:16:00Z)

Hi @garrettbyrd, I'll look into whether the issue is addressed on `gfx1100`. A note on `gfx1103`, however: while `gfx1102` and `gfx1103` hardware can be made to use the `gfx1100` ISA with `HSA_OVERRIDE_GFX_VERSION=11.0.0`, these architectures have less VGPRs than `gfx1100` and `gfx1101`, and will report `HSA_STATUS_ERROR_INVALID_ISA` or `HSA_STATUS_ERROR_OUT_OF_REGISTERS` in some workloads (`fp16`, but maybe others as well) as we currently do not provide appropriate kernels for these architectures.

---

### 评论 #2 — fluidnumericsJoe (2025-04-03T19:13:29Z)

Hey @schung-amd - is there a list somewhere that shows which AMD GPUs are *not* supported in ROCm and in hipblasLt ? It would be nice if one never had to think about setting `HSA_OVERRIDE_GFX_VERSION` for an AMD GPU (at some point). 

In hipblas and hipblaslt, is the reason that some kernels are not written for gfx1101-1103 ? Is their inline assembly. Can you point me to which kernels you're talking about here ? I'd love to take a look to see if we can contribute something to improve portability to AMD's own GPUs.

---

### 评论 #3 — schung-amd (2025-04-03T19:53:08Z)

Hi @fluidnumerics-joe, sorry for the lack of response on this. I haven't had time to verify that the issue is addressed on `gfx1100`, but since the PR was merged I would assume that it is unless you're seeing otherwise.

As for your questions here, the hardware compatibility matrices show which GPUs are officially supported. In terms of GPUs that might have issues with `HSA_OVERRIDE_GFX_VERSION`, this is a bit murkier as it no longer falls under official support and is very much case-by-case depending on the hardware. If you look at the "target restrictions" column in https://llvm.org/docs/AMDGPUUsage.html#amdgpu-generic-processor-table, you can see some of the differences between architectures in the same family, but whether or not these differences cause issues in practice has not been investigated and documented thoroughly. My comment on `gfx1102` and `gfx1103` in particular stems from experience with an issue observed in the wild: https://github.com/ROCm/clr/issues/151. For this issue in particular, a workaround is to use bf16 as we do provide bf16 kernels that happen to have an appropriate number of VGPRs.

We don't provide kernels for these architectures because they're not officially supported. Omitting them also helps us to control the installation size of ROCm. We're working on providing some degree of extended support via the generic architecture targets in the linked table above, but I don't know when, if at all, kernels will be added for the generic architecture targets. There is a push internally for extending ROCm support to more architectures though, so I'm hopeful that this will happen at some point.

---

### 评论 #4 — fluidnumericsJoe (2025-04-04T17:11:02Z)

> There is a push internally for extending ROCm support to more architectures though, so I'm hopeful that this will happen at some point.

This would be awesome. Curious to know if PR's that help extend support to more architectures would be considered.

---

### 评论 #5 — schung-amd (2025-04-07T17:40:35Z)

> Curious to know if PR's that help extend support to more architectures would be considered.

If you mean external PRs, we welcome and encourage external contributions in the form of PRs but may not always have the resources to review them in a timely manner.

---

### 评论 #6 — schung-amd (2025-06-23T14:08:46Z)

Closing this for now, feel free to comment if you still see this on `gfx1100` or need further guidance on this matter and we can reopen if necessary.

---
