# [Issue]: HSA API call failure in rocminfo.cc:1306 - HSA_STATUS_ERROR_OUT_OF_RESOURCES

> **Issue #4435**
> **状态**: closed
> **创建时间**: 2025-03-02T23:42:04Z
> **更新时间**: 2025-03-03T14:34:00Z
> **关闭时间**: 2025-03-03T14:33:58Z
> **作者**: jereimers
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4435

## 描述

### Problem Description

Unable to install ROCm in WSL2 (Windows 11 Pro v.24H2). 

Here's the view from inside Ubuntu-22.04 (via WSL):

OS:
NAME="Ubuntu"
VERSION="22.04.5 LTS (Jammy Jellyfish)"
CPU: 
model name      : AMD Ryzen 7 5800X 8-Core Processor
GPU:
ROCR: unsupported GPU

And from host Windows 11:
OS Version 10.0.26100
AMD Ryzen 7 5800X 8-Core Processor
AMD Radeon RX 7600 XT

Attempting to install ROCm 6.2.3. 
AMD Software: PRO Edition Version 24.20.36

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 7 5800X

### GPU

AMD Radeon RX 7600 XT

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

WSL environment detected.
ROCR: unsupported GPU
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1306
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-03-03T14:33:58Z)

Hi @jereimers, the `HSA_STATUS_ERROR_OUT_OF_RESOURCES` preceded by `ROCR: unsupported GPU` is expected as the RX 7600 XT is not supported for ROCm + WSL. Please refer to the [GPU Support Matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix) for more information.

---
