# [Feature]: 

> **Issue #4064**
> **状态**: closed
> **创建时间**: 2024-11-29T05:32:21Z
> **更新时间**: 2024-12-05T16:24:44Z
> **关闭时间**: 2024-11-29T16:47:44Z
> **作者**: yanite
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4064

## 描述

### Suggestion Description

Request support for wsl2 Ubuntu 24.04 python 3.12.7
Ubuntu 22.04 does work very well

I use amdgpu-install -y --usecase=wsl,rocm --no-dkms
feedback
E: Unable to locate package amdgpu-lib
E: Unable to locate package amdgpu-lib32
E: Unable to locate package rocm-opencl-runtime
E: Unable to locate package rocm-hip-runtime
E: Unable to locate package amdgpu-dkms
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu

Strongly requested

Is there a way to compile it from source code yourself?

### Operating System

wsl2

### GPU

7900xtx

### ROCm Component

rocm

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-11-29T16:47:44Z)

Hi @yanite, it looks like you're trying to install the ROCm 6.1.3 packages within an Ubuntu 24.04 container. This is likely causing your dependency errors as 24.04 support was introduced in ROCm 6.2.0. For more information on this, please see the [WSL compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html).

You can start using ROCm 6.2.3 on WSL already as the packages are  available on repo.radeon.com as highlighted over at https://github.com/ROCm/ROCm/issues/3563#issuecomment-2423673336. Give the installation steps there a try and feel free to use the that thread to report any issues that you find. Thanks!



---
