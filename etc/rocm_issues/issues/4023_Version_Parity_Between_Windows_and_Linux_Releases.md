# Version Parity Between Windows and Linux Releases

> **Issue #4023**
> **状态**: closed
> **创建时间**: 2024-11-10T06:47:13Z
> **更新时间**: 2024-11-12T18:01:21Z
> **关闭时间**: 2024-11-12T18:01:21Z
> **作者**: johnnynunez
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4023

## 描述

### Suggestion Description

Hello team,

First of all, thank you for your ongoing hard work and for continually improving this project!

I wanted to inquire about the roadmap for achieving version parity between Windows and Linux. Currently, it seems that Windows releases are a step behind the Linux versions in terms of features and updates. This discrepancy makes it challenging for cross-platform development and limits users on Windows from accessing the latest features available on Linux.

Could you please share if there are any plans or ongoing efforts to synchronize the versioning and feature sets across these platforms? Additionally, an estimated timeline for achieving this parity would be very helpful for planning purposes.

Thanks for your attention to this matter, and looking forward to your response.

Best regards,
Johnny

### Operating System

Windows 11

### GPU

W7900 DUAL SLOT

### ROCm Component

6.2.4

---

## 评论 (1 条)

### 评论 #1 — jamesxu2 (2024-11-12T18:01:21Z)

Hi @johnnynunez, thanks for the question. 

We have some documentation on our release approach on Windows and how it compares to Linux: https://rocm.docs.amd.com/projects/install-on-windows/en/latest/conceptual/release-versioning.html#rocm-release-versioning

Like you said, ROCm on Windows releases are a step behind Linux and also only receive a subset of the ROCm releases available on Linux (and a further subset of the features therein). We recognize this that this desynchronization is less than optimal for the user experience, and there is work being done to bridge the cross-OS gap between ROCm features and versioning.

That being said, I'm unfortunately not able to provide you a timeline for when this will be achieved. As you can imagine, it is a formidable task, though one that is being actively worked on by the ROCm team.

---
