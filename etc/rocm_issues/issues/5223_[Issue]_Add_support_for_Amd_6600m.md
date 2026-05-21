# [Issue]: Add support for Amd 6600m

> **Issue #5223**
> **状态**: open
> **创建时间**: 2025-08-22T08:03:53Z
> **更新时间**: 2025-08-22T13:38:23Z
> **作者**: linuxkernel94
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/5223

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Problem Description

Currently I cannot use ROCm with a Radeon 6600M on Linux unless I set the Ollama parameter to 10.3.0. Even then, performance is not optimal. Please provide official ROCm support for the Radeon 6600M and its family of GPUs so they work correctly and perform well on Linux.

### Operating System

OS: NAME="Fedora Linux" VERSION="42.20250821.0 (Silverblue)"

### CPU

AMD Ryzen 7 5800H with Radeon Graphics

### GPU

AMD Radeon RX 6600M

### ROCm Version

Latest

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

ROCm should work out-of-the-box with Radeon 6600M and related GPUs on Linux, with native drivers and optimal performance without requiring manual parameter tweaks.


