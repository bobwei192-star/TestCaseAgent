# [Issue]: MAGMA and torch.linalg function errors in different images

> **Issue #5156**
> **状态**: open
> **创建时间**: 2025-08-06T03:41:52Z
> **更新时间**: 2025-10-01T17:03:05Z
> **作者**: RuihongQiu
> **标签**: Under Investigation, AMD Instinct MI300X
> **URL**: https://github.com/ROCm/ROCm/issues/5156

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

When using `hf_model.model.resize_token_embeddings`, there is an error:
```
RuntimeError: Calling torch.linalg.cholesky on a CUDA tensor requires compiling PyTorch with MAGMA. Please use PyTorch built with MAGMA support
```

Seems it's related to docker image building without MAGMA.

More discussions are here:

https://github.com/huggingface/transformers/issues/36660#issuecomment-3153166699

### Operating System

Unknown

### CPU

Unknown

### GPU

Mi300x

### ROCm Version

ROCm 6.4.0

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

### 评论 #1 — ppanchad-amd (2025-08-06T13:12:16Z)

Hi @RuihongQiu. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — nfrumkin (2025-10-01T17:03:05Z)

I ran into this same issue when using `torch.linalg.cholesky(x)`:

ROCm version: 7.4.0
python: 3.12.10
pytorch:  2.7.0a0+git295f2ed



---
