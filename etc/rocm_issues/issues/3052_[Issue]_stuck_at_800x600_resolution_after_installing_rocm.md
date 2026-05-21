# [Issue]: stuck at 800x600 resolution after installing rocm

> **Issue #3052**
> **状态**: closed
> **创建时间**: 2024-04-21T23:15:52Z
> **更新时间**: 2024-05-20T15:13:59Z
> **关闭时间**: 2024-05-20T15:13:59Z
> **作者**: askAvoid
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/3052

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

After installing rocm as per the instructions and rebooting, Ubuntu can only display at 800x600 resolution. There is no other display setting available. There's no indication of any error or troubleshooting steps available anywhere in any official documentation.

Running `amdgpu-uninstall` restores full 4K resolution.


### Operating System

Ubuntu 22.04 LTS

### CPU

Ryzen 5 5600X

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Followed instructions to install rocm (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/) and rebooted.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — nartmada (2024-04-22T16:14:53Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — kentrussell (2024-04-22T16:47:25Z)

Can you attach a full dmesg? I assume that you're likely running the generic software renderer to display the desktop due to amdgpu failing to init

---

### 评论 #3 — nartmada (2024-05-13T19:56:19Z)

@askAvoid, can you pls attach a full dmesg?  Thanks.

---

### 评论 #4 — askAvoid (2024-05-20T15:13:59Z)

Thanks for the response. Currently dealing with another issue, I will reopen with a dmesg if I can get this reproduced.

---
