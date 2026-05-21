# [Issue]: Does 6950xt support ROCm via wsl?

> **Issue #4503**
> **状态**: closed
> **创建时间**: 2025-03-16T01:32:48Z
> **更新时间**: 2025-03-31T17:34:46Z
> **关闭时间**: 2025-03-31T17:34:46Z
> **作者**: crazyhulk
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4503

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Does 6950xt support ROCm via wsl?

rocminfo can not get amdgpu info.

---

## 评论 (4 条)

### 评论 #1 — KarpovVolodymyr (2025-03-19T19:29:43Z)

I have the same problem with my 6950 on wsl

---

### 评论 #2 — zichguan-amd (2025-03-20T18:18:06Z)

gfx1030 is not supported as per the [compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html).

---

### 评论 #3 — crazyhulk (2025-03-21T01:49:17Z)

> gfx1030 is not supported as per the [compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html).

Are there any supported plans for the future?

---

### 评论 #4 — zichguan-amd (2025-03-21T14:04:03Z)

We do plan to expand the supported device list, you can join the conversation here https://github.com/ROCm/ROCm/discussions/4276

---
