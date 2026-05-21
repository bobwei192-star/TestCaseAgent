# [Feature]: hope support [AMD/ATI] Oland PRO [Radeon R7 240/340 / Radeon 520]

> **Issue #4383**
> **状态**: closed
> **创建时间**: 2025-02-17T02:32:53Z
> **更新时间**: 2025-03-04T15:51:03Z
> **关闭时间**: 2025-03-04T15:51:01Z
> **作者**: kylincodelab
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4383

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

hope support [AMD/ATI] Oland PRO [Radeon R7 240/340 / Radeon 520]
cause i have no money buy amd vga card now....

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-03-04T15:51:01Z)

Hi @kylincodelab, unfortunately, ROCm cannot support gfx6/OLAND as it's missing key architecture functionality. This includes internal mechanisms we utilize for our software to interface with the GPU.

If you do end up trying to run ROCm on OLAND, you'll encounter the following error in dmesg, denoting the lack of HW functionality/SW support.
```
kfd: amdgpu: OLAND not supported in kfd
```

---
