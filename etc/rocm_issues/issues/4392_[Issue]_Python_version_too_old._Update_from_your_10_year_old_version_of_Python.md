# [Issue]: Python version too old. Update from your 10 year old version of Python

> **Issue #4392**
> **状态**: closed
> **创建时间**: 2025-02-19T08:23:18Z
> **更新时间**: 2025-02-26T18:41:52Z
> **关闭时间**: 2025-02-26T18:41:51Z
> **作者**: AMDphreak
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4392

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I can't even build this thing on openSUSE Tumbleweed because Python 3.6 is so old. You need to update your Python version. I mean, are you using a 10 year old computer to build this?

Python 3.6 is NO LONGER SUPPORTED. MOVE ON.

![Image](https://github.com/user-attachments/assets/d524affe-6990-47f2-ade8-5610a76dba4d)

### Operating System

Linux 5.15.167.4-microsoft-standard-WSL2 #1 SMP Tue Nov 5 00:21:55 UTC 2024

### CPU

AMD Ryzen 7 5700G with Radeon Graphics            3.80 GHz

### GPU

AMD Radeon RX 6600 XT

### ROCm Version

NOT APPLICABLE

### ROCm Component

_No response_

### Steps to Reproduce

Try to install using SLES instructions on WSL version of openSUSE Tumbleweed.
https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.2.2/install/native-install/sles.html

![Image](https://github.com/user-attachments/assets/5b028fb8-c685-4028-bcb1-b8e1693c9e81)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

inapplicable

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — darren-amd (2025-02-20T22:10:49Z)

Hi @AMDphreak,

I believe that the default python version packaged with SLES 15.6 is 3.6.15, which you can install with `sudo zypper install python3`. We currently support SLES 15.6 and 15.5: [Supported OS](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems). You can install python3.6 on SLES Tumbleweed with `sudo zypper install python36`.

---
