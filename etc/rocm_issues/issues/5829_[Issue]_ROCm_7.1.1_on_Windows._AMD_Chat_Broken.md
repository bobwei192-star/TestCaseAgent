# [Issue]: ROCm 7.1.1 on Windows. AMD Chat Broken.

> **Issue #5829**
> **状态**: closed
> **创建时间**: 2026-01-03T06:56:04Z
> **更新时间**: 2026-01-30T06:34:45Z
> **关闭时间**: 2026-01-30T06:34:45Z
> **作者**: Spitlebug
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5829

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

ROCm 7.1.1 has broken AMD Chat in AMD Adrenalin 25.12.1.

<img width="494" height="1207" alt="Image" src="https://github.com/user-attachments/assets/f8eb85c1-4c79-47bc-80f8-682a3fbaa5c4" />

### Operating System

Windows 11 - 10.0.26200

### CPU

AMD Ryzen 9 7900 12-Core Processor

### GPU

AMD Radeon(TM) Graphics & AMD Radeon RX 9070 XT

### ROCm Version

7.1.1 ????

### ROCm Component

_No response_

### Steps to Reproduce

Install ROCm 7.1.1 via Git.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — schung-amd (2026-01-29T15:03:46Z)

Hi @Spitlebug, are you still seeing this issue with Adrenalin driver 26.1.1? I haven't been able to reproduce this.

---

### 评论 #2 — Spitlebug (2026-01-30T06:34:15Z)

> Hi [@Spitlebug](https://github.com/Spitlebug), are you still seeing this issue with Adrenalin driver 26.1.1? I haven't been able to reproduce this.

Hello @schung-amd .

I have updated to the latest Adrenalin Drivers (26.1.1). AMD Chat is working correctly. ✅

The implementation leaves something to be desired. No ability to install/uninstall/update/downgrade PyTorch and ROCm in Windows. This is fairly important, I think.

The AMD Install Manager doesn't scale well with 4K displays. (No scroll bars, unable to resize, clickable arrows for sub menus etc...) but I think that is a minor gripe and certainly solvable with a little fine tuning. I appreciate the work being done on this.

![Image](https://github.com/user-attachments/assets/cf799a61-6195-487a-9265-906ecfe71982)
![Image](https://github.com/user-attachments/assets/dd539665-e2be-410a-9440-0452cedefeb0)

---
