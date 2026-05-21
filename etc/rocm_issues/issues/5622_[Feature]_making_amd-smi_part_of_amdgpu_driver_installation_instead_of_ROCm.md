# [Feature]: making amd-smi part of amdgpu driver installation instead of ROCm

> **Issue #5622**
> **状态**: closed
> **创建时间**: 2025-11-04T16:44:43Z
> **更新时间**: 2025-11-21T19:20:38Z
> **关闭时间**: 2025-11-21T19:20:29Z
> **作者**: ye-luo
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/5622

## 标签

- **Feature Request** (颜色: #fbca04)

## 负责人

- darren-amd

## 描述

### Suggestion Description

amd-smi is a management tool and should be like nvidia-smi being part of nvidia driver.
Currently installing amd-smi requires installing rocm bits which mess up with versioned rocm installation in alternative locations.

### Operating System

Linux

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (2 条)

### 评论 #1 — ianbmacdonald (2025-11-05T12:32:13Z)

amdgpu ships with the kernel for 6.17+ ;  

open source.

---

### 评论 #2 — darren-amd (2025-11-21T19:20:29Z)

Hi @ye-luo,

Thanks for the feature suggestion! I had a chat with the amd-smi team and unfortunately this is not currently something we have plans to support.

---
