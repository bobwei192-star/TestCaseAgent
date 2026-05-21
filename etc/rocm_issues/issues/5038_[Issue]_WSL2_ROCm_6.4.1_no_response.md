# [Issue]: WSL2 ROCm 6.4.1 no response

> **Issue #5038**
> **状态**: closed
> **创建时间**: 2025-07-13T14:30:29Z
> **更新时间**: 2025-07-22T19:19:41Z
> **关闭时间**: 2025-07-21T07:24:38Z
> **作者**: yihuishou
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/5038

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

<img width="1885" height="237" alt="Image" src="https://github.com/user-attachments/assets/d381e498-3177-4c57-8e2b-595c835808f3" />

After updating the driver to 25.6.3, Comfyui does not respond when starting. After reinstalling WSL2, rocminfo can be used to see the graphics card information, but pytorch does not respond when getting device information.

Destroyed the entire WSL2 instance, and a complete reinstall can recover.
Are there any destructive updates to the drivers for 25.6.x ?

### Operating System

Ubuntu 22.04

### CPU

7900X

### GPU

7900XTX

### ROCm Version

ROCm 6.4.1

### ROCm Component

ROCm

### Steps to Reproduce

After upgrading from ROCm version 6.2 to 6.4 and driver from 25.3.1 to 25.6.3, WSL got stuck on reading graphics card information.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-07-14T13:22:43Z)

Hi @yihuishou. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — yihuishou (2025-07-15T02:58:51Z)

> Hi [@yihuishou](https://github.com/yihuishou). Internal ticket has been created to assist with your issue. Thanks!

WSL installed 6.2.x and Windows started working fine from 12.x. When the Windows side kept updating the driver, WSL started to be unable to obtain the graphics card information... So every time the Windows driver is updated, do I have to reinstall WSL as well?

---

### 评论 #3 — schung-amd (2025-07-17T17:21:09Z)

Hi @yihuishou, is ROCm working with driver 25.6.3 after you reinstalled WSL?

---

### 评论 #4 — yihuishou (2025-07-19T16:40:52Z)

> Hi [@yihuishou](https://github.com/yihuishou), is ROCm working with driver 25.6.3 after you reinstalled WSL?

Yea, it`s works. why updated not work...

---

### 评论 #5 — schung-amd (2025-07-22T19:19:41Z)

We've seen this happen occasionally, but the issue fixed itself with a reboot. If you see this happen in the future, please comment here (we can reopen if necessary) or submit a new issue for investigation.

---
