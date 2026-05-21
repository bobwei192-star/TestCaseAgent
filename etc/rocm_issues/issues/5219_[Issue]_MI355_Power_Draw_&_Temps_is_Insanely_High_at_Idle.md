# [Issue]: MI355 Power Draw & Temps is Insanely High at Idle

> **Issue #5219**
> **状态**: closed
> **创建时间**: 2025-08-21T21:31:23Z
> **更新时间**: 2026-01-14T19:33:54Z
> **关闭时间**: 2026-01-14T19:33:54Z
> **作者**: functionstackx
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5219

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Can AMD team look into optimizing idle power state? it is quite high

MI355 idle power draw is 238W & idle temp is at 45C
air cooled B200 idle power draw 137W is and idle temp is at 28C

+Viz @qcolombet

<img width="1016" height="283" alt="Image" src="https://github.com/user-attachments/assets/8fb3773c-c53a-4b77-9f22-ecb671a7485a" />

<img width="1131" height="819" alt="Image" src="https://github.com/user-attachments/assets/bc674d49-1e96-48c9-9ceb-959b0c97ce22" />

### Operating System

ubuntu

### CPU

cpu 

### GPU

mi355

### ROCm Version

rocm 7.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-08-22T13:47:02Z)

Hi @functionstackx. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-08-25T16:53:50Z)

Hi @functionstackx, thanks for reaching out! This power draw seems in line with the expected power draw of MI355 at idle. 

---

### 评论 #3 — LunNova (2025-08-27T20:04:45Z)

Does it support [amdgpu.runpm=1](https://docs.kernel.org/gpu/amdgpu/module-parameters.html#runpm-int) to power down when left idle for a while?

---

### 评论 #4 — tcgu-amd (2025-08-28T14:08:42Z)

> Does it support [amdgpu.runpm=1](https://docs.kernel.org/gpu/amdgpu/module-parameters.html#runpm-int) to power down when left idle for a while?

I do not think so. However, please feel free to give it a try on your setup. 

---
