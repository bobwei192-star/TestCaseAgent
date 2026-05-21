# [Issue]: amd-smi changed to amd_smi in ROCm 6.3.x

> **Issue #4700**
> **状态**: closed
> **创建时间**: 2025-04-30T04:13:05Z
> **更新时间**: 2025-05-26T14:41:03Z
> **关闭时间**: 2025-05-26T14:41:02Z
> **作者**: bthurber
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4700

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

amd-smi util present in ROCm 6.2.4 has changed command syntax to amd_smi in ROCm 6.3.4.  This can break automation and documentation for end users.

### Operating System

Red Hat Enterprise Linux AI 1.5

### CPU

Not related

### GPU

AMD MI300X

### ROCm Version

6.3.4

### ROCm Component

amdsmi

### Steps to Reproduce

1. Deploy RHEL-AI with ROCm 6.3.4
2. Try to run amd-smi

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-04-30T14:50:16Z)

Hi @bthurber, could you please clarify how you installed ROCm 6.3.4 on RHEL AI? 

For context, ROCm 6.3.4 is a Radeon specific release and only supports Ubuntu 24.04/22.04 ([ref](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script)). `amd-smi` on ROCm 6.4.0 + RHEL works as expected using the official packages/installation ([ref](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script)). 
```
Installed Packages
Name         : amd-smi-lib
Version      : 25.3.0.60400
Release      : 47.el9
Architecture : x86_64
Size         : 4.6 M
Source       : amd-smi-lib-25.3.0.60400-47.el9.src.rpm
Repository   : @System
From repo    : rocm
Summary      : AMD System Management libraries
License      : MIT
```
There hasn't been any change in the syntax for `amd-smi ` that I'm aware of.

---

### 评论 #2 — harkgill-amd (2025-05-26T14:41:02Z)

Closing this issue out. Feel free to leave a comment if you have any further questions.

---
