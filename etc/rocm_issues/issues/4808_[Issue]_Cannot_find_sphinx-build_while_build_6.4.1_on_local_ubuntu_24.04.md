# [Issue]: Cannot find sphinx-build while build 6.4.1 on local ubuntu 24.04

> **Issue #4808**
> **状态**: closed
> **创建时间**: 2025-05-27T08:08:31Z
> **更新时间**: 2025-05-27T08:49:33Z
> **关闭时间**: 2025-05-27T08:45:58Z
> **作者**: qiaojbao
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4808

## 描述

### Problem Description

Seems the install-prerequisites.sh didn't install the dependency python module sphinx.
Installing 'python3-sphinx' works for me.

### Operating System

ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz

### GPU

2x RX9070xt

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

Sync the latest ROCm release.
Run the install-prerequisites.sh on host local.
Build all components.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — qiaojbao (2025-05-27T08:45:58Z)

seems the module listed in the shell scripts, no idea why did not work.

---
