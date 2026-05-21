# [Issue]: to download ROCm GPG failed

> **Issue #5407**
> **状态**: closed
> **创建时间**: 2025-09-22T13:07:34Z
> **更新时间**: 2025-09-22T14:00:18Z
> **关闭时间**: 2025-09-22T13:59:08Z
> **作者**: dao0jue
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5407

## 描述

### Problem Description

On Ubuntu 24.04.3 LTS， just want to install ROCm, but to download ROCm GPG failed


#### Add and install ROCm APT repository

`
wget -q -O - https://repo.radeon.com/rocm/rocm.key | sudo apt-key add -
echo 'deb [arch=amd64] https://repo.radeon.com/rotm/apt/6.0.2/ ubuntu main' | sudo tee /etc/apt/sources.list.d/rocm.list.list
sudo apt update`

https://repo.radeon.com/rocm/rocm.key  show 404 page.


### Operating System

Ubuntu 24.04.3 LTS

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD Radeon Graphics (radeonsi, gfx1151, LLVM 20.1.2, DRM 3.61, 6.14.0-29-generic)

### ROCm Version

to be installed 

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — kentrussell (2025-09-22T13:45:53Z)

You should use https://repo.radeon.com/rocm/rocm.gpg.key . rocm.key doesn't exist, as you noted.
Also, https://repo.radeon.com/rotm/apt/6.0.2/ doesn't exist. It's rocm, not rotm. Wherever you copy/pasted those instructions from, they're invalid and incorrect. For ROCm 7.0, try use the instructions provided at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html or https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html

---
