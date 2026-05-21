# [Issue]: build script does not have a list of requirements for a RHEL-like environment

> **Issue #4753**
> **状态**: closed
> **创建时间**: 2025-05-19T05:41:47Z
> **更新时间**: 2025-05-22T18:25:48Z
> **关闭时间**: 2025-05-22T18:25:47Z
> **作者**: fwyzard
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4753

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

The ROCm build system contains a list of requirements for various Ubuntu LTS releases.
It does not contain the corresponding list of requirements for RedHat Enterprise Linux 8.x, 9.x or 10.x and derived systems. 

### Operating System

RedHat Enterprise Linux 8.10

### CPU

any

### GPU

any

### ROCm Version

6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

Check under https://github.com/ROCm/ROCm/tree/rocm-6.4.0/tools/rocm-build/docker/ .

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-05-22T13:56:47Z)

Hi @fwyzard. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-05-22T15:50:34Z)

Hi @fwyzard, yes, the requirements under https://github.com/ROCm/ROCm/tree/rocm-6.4.0/tools/rocm-build/docker/ are intended for building ROCm in docker containers from Ubuntu images. It is possible to install them directly to host, but only if the host happens to be running Ubuntu as well. 

Unfortunately, there is currently no plans to add RHEL-based instructions, because we cannot support RHEL-based docker images due to licensing. However, we are currently working on adding support for RHEL-like OS to allow building for RHEL-compatible packages. 

Sorry for the inconvenience, and thanks for raising this issue! 

---

### 评论 #3 — fwyzard (2025-05-22T16:08:43Z)

Alma Linux-based instructions would work for me :-)

---

### 评论 #4 — tcgu-amd (2025-05-22T18:25:47Z)

Thanks for the suggestion! Your feedback will be part of our decision making. I will be closing this issue for now, but please feel free to continue to ping us for progress. Thanks! 

---
