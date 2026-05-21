# [Issue]: Ubuntu 24.04.1 LTS incompatibility with rocm 6.2

> **Issue #3662**
> **状态**: closed
> **创建时间**: 2024-09-02T18:07:31Z
> **更新时间**: 2024-09-20T18:29:16Z
> **关闭时间**: 2024-09-20T18:29:15Z
> **作者**: Wintoplay
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3662

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

rocminfo show
ROCk module is NOT loaded, possibly no GPU devices

I previously used rocm 6.1 on Ubuntu 24.04.4 (previous version but the number is somehow larger .4 vs .1). There was no problem, but I format my PC. Then, I install 24.04.1 and rocm 6.2, and rocminfo cannot load the GPU device.

I am not sure if this is ROCM's fault or Ubuntu's fault.

### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

13th Gen Intel(R) Core(TM) i5-13600K

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.0

### ROCm Component

rocminfo

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — Wintoplay (2024-09-02T18:10:10Z)

Btw, how to specifically install rocm 6.1 on 24.04.1?

---

### 评论 #2 — harkgill-amd (2024-09-03T17:55:53Z)

Hi @Wintoplay, I wasn't able to reproduce the `ROCk module is NOT loaded, possibly no GPU devices` error when installing ROCm 6.2 on Ubuntu 24.04.1 with the [quick install instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#quick-start-installation-guide). Could you please specify the steps you followed to install ROCm 6.2 and also give the quick install instructions a try? 

Currently, only ROCm 6.2 is supported on Ubuntu 24.04 while ROCm 6.1 is supported on Ubuntu 22.04 and other OSes as specified in the [compatibility matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#compatibility-matrix).

---

### 评论 #3 — Wedge009 (2024-09-11T08:14:24Z)

> I previously used rocm 6.1 on Ubuntu 24.04.4 (previous version but the number is somehow larger .4 vs .1). There was no problem, but I format my PC. Then, I install 24.04.1 and rocm 6.2, and rocminfo cannot load the GPU device.

At time of writing, there's no Ubuntu 24.04.4 - you sure you didn't mean 22.04.4?


---

### 评论 #4 — harkgill-amd (2024-09-20T18:29:15Z)

Closing out this issue. @Wintoplay, if you are still experiencing the `ROCk module is NOT loaded, possibly no GPU devices` with ROCm 6.2 on Ubuntu 24.04, please provide your installation steps. Thanks!

---
