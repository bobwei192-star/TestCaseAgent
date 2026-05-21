# [Issue]: hipcc --version takes a minute to respond

> **Issue #3598**
> **状态**: closed
> **创建时间**: 2024-08-15T22:52:52Z
> **更新时间**: 2024-09-11T18:27:49Z
> **关闭时间**: 2024-09-11T18:27:49Z
> **作者**: mcordery
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3598

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

Installed new version of rocm6.2 after using 6.1
A response from hipcc --version takes nearly a minute
This was definitely not the case with 6.1

mcordery@DESKTOP-J13NI0K:~$ time hipcc --version
HIP version: 6.2.41133-dd7f95766
AMD clang version 18.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-6.2.0 24292 26466ce804ac523b398608f17388eb6d605a3f09)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.2.0/lib/llvm/bin
Configuration file: /opt/rocm-6.2.0/lib/llvm/bin/clang++.cfg

real    1m0.048s
user    0m57.240s
sys     0m3.346s

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

time hipcc --version

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2024-08-19T19:47:14Z)

@mcordery Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2024-08-21T18:12:11Z)

Hi @mcordery, I can't reproduce this locally; hipcc --version takes under 0.1s to run in ROCm 6.2 as well as ROCm 6.1. Does anything else run slowly for you with ROCm 6.2, or is it just hipcc --version so far? Could you try uninstalling ROCm completely and reinstalling? Also, can you provide the output of `sudo dmesg | grep atomic`? Thanks!

---

### 评论 #3 — mcordery (2024-08-21T18:21:07Z)

Yeah, I was trying to avoid that but I'll give it a try. There is nil output from the command that you requested that I run.

---

### 评论 #4 — harkgill-amd (2024-09-09T20:14:45Z)

Hi @mcordery, are you still experiencing a delay when running `hipcc --version` on ROCm 6.2?

---

### 评论 #5 — mcordery (2024-09-10T17:15:08Z)

[AMD Official Use Only - AMD Internal Distribution Only]

Yes but I think it’s ignorable for now. It’s probably just me.

Matthew J Cordery, PhD
Principal Member of Technical Staff
AI Group

From: harkgill-amd ***@***.***>
Sent: Monday, September 9, 2024 2:15 PM
To: ROCm/ROCm ***@***.***>
Cc: Cordery, Matthew ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: hipcc --version takes a minute to respond (Issue #3598)

Caution: This message originated from an External Source. Use proper caution when opening attachments, clicking links, or responding.


Hi @mcordery<https://github.com/mcordery>, are you still experiencing a delay when running hipcc --version on ROCm 6.2?

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/3598#issuecomment-2339001148>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/AEJ5XWN7ANJOKG7OMUK6KU3ZVX6UXAVCNFSM6AAAAABMTA6AXSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMZZGAYDCMJUHA>.
You are receiving this because you were mentioned.Message ID: ***@***.******@***.***>>


---
