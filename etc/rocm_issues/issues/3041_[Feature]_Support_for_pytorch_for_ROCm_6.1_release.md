# [Feature]: Support for pytorch for ROCm 6.1 release.

> **Issue #3041**
> **状态**: closed
> **创建时间**: 2024-04-18T13:48:30Z
> **更新时间**: 2024-04-22T05:01:11Z
> **关闭时间**: 2024-04-19T18:48:02Z
> **作者**: kannan-scalers-ai
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3041

## 描述

### Suggestion Description

Currently the torch stable support is at ROCm 5.7 and nightly support is untill 6.0. The official ROCm pytorch image supports upto ROCm 6.0.2.

When can we expect a docker image release with torch on ROCm 6.1? Is there is any plan to provide ROCm 6.1 stable support on torch?

### Operating System

Ubuntu

### GPU

MI300X

### ROCm Component

ROCm

---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-04-19T18:48:02Z)

@kannan-scalers-ai, 

•	When can we expect a docker image release with torch on ROCm 6.1 ?
o	Rocm/pytorch docker images will be showing up in a few days as QA is currently testing them. Generally speaking, the rocm/pytorch docker images show up a few days after GA for any ROCm release.
•	Is there any plan to provide ROCm 6.1 stable support on torch ?
o	We are currently working on getting PyTorch nightly wheels upgraded to ROCm6.1. PyTorch2.4 will be the earliest version where will have stable wheels with ROCm6.1 or later.


---

### 评论 #2 — kannan-scalers-ai (2024-04-22T04:55:04Z)

@nartmada Thanks for your updates on the release timeline. I can see the ROCm 6.1 torch image release on the [ROCm Docker hub page](https://hub.docker.com/layers/rocm/pytorch/rocm6.1_ubuntu22.04_py3.10_pytorch_2.1.2/images/sha256-f6ea7cee8aae299c7f6368187df7beed29928850c3929c81e6f24b34271d652b?context=explore).

---
