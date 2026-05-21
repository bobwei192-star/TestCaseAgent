# [Issue]: Missing 7.1 AMDGPU Repository URL

> **Issue #5798**
> **状态**: closed
> **创建时间**: 2025-12-19T14:45:08Z
> **更新时间**: 2025-12-22T16:55:39Z
> **关闭时间**: 2025-12-22T16:38:02Z
> **作者**: matinraayai
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5798

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Hi,
I've noticed that version 7.1 and 7.1.1 versions of the AMDGPU driver are missing from the Radeon repo website under [here](https://repo.radeon.com/amdgpu/). In contrast, the [AMDGPU install folder](https://repo.radeon.com/amdgpu-install/) has them.
Is this intentional?

Thanks

### Operating System

N/A

### CPU

N/A

### GPU

N/A

### ROCm Version

7.1.0, 7.1.1

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

### 评论 #1 — harkgill-amd (2025-12-22T16:38:03Z)

Hi @matinraayai, this is intentional as we've shifted to a new versioning scheme for the amdgpu driver in recent releases. You can find some of the newer versions that are tied to 7.1 (30.20) and 7.1.1 (30.20.1) here

<img width="700" height="161" alt="Image" src="https://github.com/user-attachments/assets/cca4afad-d466-429b-a614-4754ce5c660d" />

This blog post delves into the specifics behind the split https://rocm.blogs.amd.com/ecosystems-and-partners/instinct-gpu-driver/README.html. 

---
