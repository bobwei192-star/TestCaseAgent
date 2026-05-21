# [Issue]: enable MPI support in official builds

> **Issue #4506**
> **状态**: closed
> **创建时间**: 2025-03-17T20:06:37Z
> **更新时间**: 2025-03-28T21:48:09Z
> **关闭时间**: 2025-03-28T21:48:08Z
> **作者**: mmoelle1
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4506

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Would it be possible to compile the official builds of LibTorch (CPU, CUDA, ROCm) for Linux with `-DUSE_DISTRIBUTED=ON`, `-DUSE_MPI=ON` and `-DUSE_C10D_MPI=ON` and ship a version of, e.g., openmpi together with the official build? I don't know if many people would use the Python version with MPI enabled but having an official build that would support distributed training would be really great.

### Operating System

n/a

### CPU

n/a

### GPU

n/a

### ROCm Version

n/a

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — naromero77amd (2025-03-28T21:48:08Z)

This was discussed internally @jeffdaily.

This is difficult to support right now, but we will consider supporting this in the future.

---
