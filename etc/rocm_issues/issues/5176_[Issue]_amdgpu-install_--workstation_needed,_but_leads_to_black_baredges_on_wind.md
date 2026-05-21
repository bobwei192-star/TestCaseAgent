# [Issue]: amdgpu-install --workstation needed, but leads to black bar/edges on windows

> **Issue #5176**
> **状态**: closed
> **创建时间**: 2025-08-09T08:09:59Z
> **更新时间**: 2025-08-10T21:46:20Z
> **关闭时间**: 2025-08-10T21:46:20Z
> **作者**: nada3910
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5176

## 描述

### Problem Description

OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"

CPU: 
model name      : AMD Ryzen 7 9700X 8-Core Processor

GPU:
bash: /opt/rocm/bin/rocminfo: No such file or directory


----------------------------------------------------------------------------------

hello , 

to view TV channels via VLC the amdgpu-install --usecase=graphics won't suffice, leading to crash of program VLC;

however, when using amdgpu-install --usecase=workstation --opencl=rocr --vulkan=amdvlk,pro it would function , leaving however the desktop in a bit miserable state due to encountering black bars on the edges of windows.

since GPU is not supported for ROCm software, i am wondering how i could resolve this issue.

### Operating System

kubuntu 24.04.3

### CPU

9700x

### GPU

radeon rx 7600

### ROCm Version

amdgpu-install 6.4.60402-1

### ROCm Component

_No response_

### Steps to Reproduce

install amdgpu-install drivers with --usecase=workstation
evoke vlc to check if tv streaming is functional
noticing black bars around windows


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

<img width="1737" height="1134" alt="Image" src="https://github.com/user-attachments/assets/4cabfdaa-8f20-4ecc-a385-f4135cc5904b" />

---

## 评论 (3 条)

### 评论 #1 — nada3910 (2025-08-09T08:12:00Z)

[output.txt](https://github.com/user-attachments/files/21696973/output.txt)

---

### 评论 #2 — nada3910 (2025-08-09T08:14:24Z)

not using AMDGPU-install at all would also let me watch TV via VLC (due to AMDGPU being supported via kernel i suppose), however then their would be no OpenCL support which is needed for another program.

also , scrolling is not smooth; 
maybe the **graphics card is not supported entirely** for the --usecase=workstation?

---

### 评论 #3 — nada3910 (2025-08-10T21:46:20Z)

thank you, this has been solved by updating to kubuntu 24.10 which uses "wayland" by default and does no longer present the tearing issue when using amdgpu with certain pro components on this consumer graphics card; vlc no longer crashes; browsing smooth; 




---
