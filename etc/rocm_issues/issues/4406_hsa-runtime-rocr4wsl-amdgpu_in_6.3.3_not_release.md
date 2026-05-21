# hsa-runtime-rocr4wsl-amdgpu in 6.3.3 not release

> **Issue #4406**
> **状态**: closed
> **创建时间**: 2025-02-21T08:15:53Z
> **更新时间**: 2025-02-25T03:35:22Z
> **关闭时间**: 2025-02-25T03:35:22Z
> **作者**: yihuishou
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4406

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Where is the hsa-runtime-rocr4wsl-amdgpu package?

https://repo.radeon.com/amdgpu/6.3.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/ is not exist.

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-02-21T14:35:15Z)

Hi @yihuishou. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-02-21T15:06:26Z)

Hi @yihuishou, there is no ROCm 6.3.3 release for WSL at this time. Please refer to https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html.

---

### 评论 #3 — yihuishou (2025-02-22T01:56:09Z)

> Hi [@yihuishou](https://github.com/yihuishou), there is no ROCm 6.3.3 release for WSL at this time. Please refer to https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html。

But why Rocm 6.3.2 has?

---

### 评论 #4 — schung-amd (2025-02-24T14:58:04Z)

I don't believe that is an official/finalized release, it may be there for testing purposes. You're free to try to use it of course, but there may not be a compatible Adrenalin driver available yet. The compatibility matrix and install guide will be updated to reflect the latest stable release as it officially becomes available.

---
