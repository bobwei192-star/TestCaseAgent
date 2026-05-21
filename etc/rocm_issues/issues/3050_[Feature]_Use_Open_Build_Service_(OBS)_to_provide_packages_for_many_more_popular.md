# [Feature]: Use Open Build Service (OBS) to provide packages for many more popular GNU/Linux distributions

> **Issue #3050**
> **状态**: open
> **创建时间**: 2024-04-21T01:45:41Z
> **更新时间**: 2025-02-19T08:13:39Z
> **作者**: JLP
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3050

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Currently ROCm packages are provided only for very few distributions. AMD should be using [Open Build Service (OBS)](https://openbuildservice.org/) to provide packages for many more popular GNU/Linux distributions and for much easier installation, and the packages are built from the single package specification for all the distributions.

### Operating System

GNU/Linux

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2024-05-06T15:29:07Z)

@JLP Will check with internal team and let you know. Thanks!

---

### 评论 #2 — clemperorpenguin (2024-05-16T14:29:19Z)

> @JLP Will check with internal team and let you know. Thanks!

If this can't be done, can you look into distributing the source RPM files for SUSE and RHEL? This would make community support on OBS and COPR much easier.

---

### 评论 #3 — Conan-Kudo (2024-06-04T12:44:53Z)

A good starting point would be the packaging the Fedora AI/ML SIG has done. It's been cleaned up and well-integrated for distribution tooling. It's relatively easy to use Fedora packaging as the starting point for building cross-distribution RPM and Debian packaging with OBS.

---

### 评论 #4 — GZGavinZhao (2024-06-05T18:28:39Z)

> If this can't be done, can you look into distributing the source RPM files for SUSE and RHEL? This would make community support on OBS and COPR much easier.

I believe they're using CPack to produce both the official deb and rpm packages: https://github.com/ROCm/rocm-cmake/blob/a83c5075d85f1fd28d657a9277eb21c834d76f3f/docs/src/reference/ROCMCreatePackage.rst#L22

---

### 评论 #5 — AMDphreak (2025-02-19T08:13:02Z)

Dear God they need this so bad.

I can't even build this thing on openSUSE Tumbleweed because Python 3.6 is so old. They need to update their Python version. I mean, are they using a 10 year old computer to build this?

Python 3.6 is NO LONGER SUPPORTED. MOVE ON.

![Image](https://github.com/user-attachments/assets/d493ea0b-b7a6-443a-bc35-87272a565576)

---
