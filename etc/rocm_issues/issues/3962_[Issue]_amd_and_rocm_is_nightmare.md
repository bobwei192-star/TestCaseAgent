# [Issue]: amd and rocm is nightmare 

> **Issue #3962**
> **状态**: closed
> **创建时间**: 2024-10-30T15:44:40Z
> **更新时间**: 2024-10-31T13:32:34Z
> **关闭时间**: 2024-10-31T13:32:33Z
> **作者**: ttJuicer
> **标签**: ROCm 6.2.2, rx6800
> **URL**: https://github.com/ROCm/ROCm/issues/3962

## 标签

- **ROCm 6.2.2** (颜色: #ededed)
- **rx6800** (颜色: #ededed)

## 描述

### Problem Description

i bought rx6800 4 months ago and i have problem with everything related to rocm its so hard and frustrating to make atleast smth to work like all ai apps on pinokio or stable diffusion... every app is trying to find cuda 

### Operating System

Linux Mint 21.3 Cinnamon

### CPU

AMD Ryzen 5 7600X 

### GPU

rx6800

### ROCm Version

ROCm 6.2.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — ttJuicer (2024-10-30T16:09:02Z)

fk am going to install ubuntu and if that will not work ill return all amd sht and buy nvidia 

---

### 评论 #2 — harkgill-amd (2024-10-31T13:32:34Z)

Hi @ttJuicer, various applications will look for `cuda` in the frontend and delegate to the ROCm libraries once an AMD GPU is detected. As for Stable Diffusion, I was able to get it working on a RX 6800 by following the steps over at [Install and Run on AMD GPUs](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs#running-natively). Please be sure to update the index url to `https://download.pytorch.org/whl/rocm6.2` for the latest PyTorch wheels. 

If you encounter any additional issues with SD or ROCm, please open a new ticket with detailed steps to reproduce the problem. This will help us investigate further and work toward a solution on our end. Thank you!

---
