# [Issue]: ROCm runtime on windows cause model to load into shared memory instead dedicated memory for N31

> **Issue #4040**
> **状态**: closed
> **创建时间**: 2024-11-19T16:06:05Z
> **更新时间**: 2024-11-28T21:13:35Z
> **关闭时间**: 2024-11-28T21:13:35Z
> **作者**: sorasoras
> **标签**: Under Investigation, ROCm 6.1.0, 7900xtx
> **URL**: https://github.com/ROCm/ROCm/issues/4040

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.1.0** (颜色: #ededed)
- **7900xtx** (颜色: #ededed)

## 描述

### Problem Description

https://github.com/ggerganov/llama.cpp/discussions/9960#discussioncomment-11141805

https://github.com/ggerganov/llama.cpp/issues/9964


### Operating System

Windows11

### CPU

7950X3D

### GPU

7900XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

ROCR-Runtime

### Steps to Reproduce

llama.cpp Windows/ROCm builds are broken. Using shared GPU memory instead of dedicated
https://github.com/ggerganov/llama.cpp/issues/9964
workaround:

 latest ROCm runtime (1.1.13). Switching to Vulkan or 1.1.10 runtime works.


---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2024-11-19T16:56:01Z)

Hi @sorasoras. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2024-11-21T17:40:17Z)

This looks like a known issue for Adrenalin version 24.9.1 and 24.10.1 where HIP uses shared memory for any allocation over 4GB (see: https://github.com/ROCm/HIP/issues/3644). For now, a workaround is to downgrade to Adrenalin 24.8.1 or use the Pro driver (24.Q2 appears to be functional). This should be addressed in an upcoming Adrenalin release, although I'll have to check where the fix has landed specifically.  @SteelPh0enix does this fix the performance degradation you're seeing in the linked issues?

---

### 评论 #3 — schung-amd (2024-11-28T21:13:35Z)

Closing for now as I am fairly sure this is the same issue. Feel free to comment if the above does not resolve your issue and we can reopen for investigation.

---
