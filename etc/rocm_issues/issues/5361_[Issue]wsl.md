# [Issue]:wsl

> **Issue #5361**
> **状态**: closed
> **创建时间**: 2025-09-17T04:56:06Z
> **更新时间**: 2025-09-22T15:13:12Z
> **关闭时间**: 2025-09-22T15:13:12Z
> **作者**: xudingzhang
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/5361

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 负责人

- harkgill-amd

## 描述

### Problem Description

sudo apt install ./amdgpu-install_7.0.70000-1_all.deb

amdgpu-install -y --usecase=wsl,rocm --no-dkms


Hit:1 http://mirrors.aliyun.com/ubuntu noble InRelease
Hit:2 http://mirrors.aliyun.com/ubuntu noble-updates InRelease
Hit:3 http://mirrors.aliyun.com/ubuntu noble-backports InRelease
Hit:4 https://mirrors.aliyun.com/docker-ce/linux/ubuntu noble InRelease
Hit:5 http://mirrors.aliyun.com/ubuntu noble-security InRelease
Hit:6 https://repo.radeon.com/amdgpu/30.10/ubuntu noble InRelease
Hit:7 https://repo.radeon.com/rocm/apt/7.0 noble InRelease
Hit:8 https://repo.radeon.com/graphics/7.0/ubuntu noble InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu





### Operating System

Ubuntu24.04

### CPU

7800X3D

### GPU

7900XTX

### ROCm Version

ROCm7.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

我发现ROCm7.0现在还不支持wsl2，，当我去https://repo.radeon.com/amdgpu/7.0/ubuntu/pool/main/寻找，发现没有hsa-runtime-rocr4wsl-amdgpu这个包，但是6.4.2.1是hsa-runtime-rocr4wsl-amdgpu的包，我希望rocm7能尽快支持wsl2，现在越来越多人使用wsl2。

---

## 评论 (5 条)

### 评论 #1 — dvv101111 (2025-09-17T11:51:52Z)

Same problem

---

### 评论 #2 — ppanchad-amd (2025-09-17T14:10:30Z)

Hi @xudingzhang. Internal ticket has been created to assist with your issue. thanks!

---

### 评论 #3 — harkgill-amd (2025-09-17T14:56:06Z)

Hi @dvv47 and @xudingzhang, the latest release for ROCm on WSL is 6.4.2 as seen over at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script. 

The ROCm 7.0 release does not have WSL support yet which is why the `hsa-runtime-rocr4wsl-amdgpu` is unavailable and throwing errors during installation.



---

### 评论 #4 — xudingzhang (2025-09-18T07:14:24Z)

> 你好[@dvv47](https://github.com/dvv47)和[@xudingzhang](https://github.com/xudingzhang)[，WSL 上 ROCm 的最新版本是 6.4.2，如https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script)所示。
> 
> ROCm 7.0 版本尚不支持 WSL，这就是为什么它`hsa-runtime-rocr4wsl-amdgpu`在安装过程中不可用并抛出错误。

是的，我希望能尽快支持wsl或则Windows

---

### 评论 #5 — harkgill-amd (2025-09-22T15:13:11Z)

We are committed to both WSL and Windows native support with the latter having it's first preview release in the near future. As for ROCm 7.0 WSL support, the work is already under way - it's just a matter of time.

---
