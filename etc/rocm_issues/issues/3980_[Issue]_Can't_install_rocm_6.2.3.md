# [Issue]: Can't install rocm 6.2.3

> **Issue #3980**
> **状态**: closed
> **创建时间**: 2024-10-31T18:37:44Z
> **更新时间**: 2024-11-09T07:10:58Z
> **关闭时间**: 2024-11-04T19:55:51Z
> **作者**: WareZTv
> **标签**: Under Investigation, ROCm 6.2.3, rx 7900xtx
> **URL**: https://github.com/ROCm/ROCm/issues/3980

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **rx 7900xtx** (颜色: #ededed)

## 描述

### Problem Description

Hello, have the 6.8.0.48 kernel and the comand "amdgpu-install -y --usecase=graphics,rocm" is giving me this error:
Err:7 https://repo.radeon.com/amdgpu/6.2.3/ubuntu jammy/main amd64 Packages
  File has unexpected size (14796 != 14502). Mirror sync in progress?

### Operating System

Ubuntu 22.04.5LTS

### CPU

ryzen 7 7800x3d

### GPU

rx 7900xtx

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

sudo apt-get update
sudo apt-get dist-upgrade
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all.deb
sudo apt install ./amdgpu-install_6.2.60203-1_all.deb
amdgpu-install -y --usecase=graphics,rocm

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — harkgill-amd (2024-10-31T19:19:54Z)

Hi @WareZTv, thanks for the report! Will look into this further and get back to you.

---

### 评论 #2 — harkgill-amd (2024-11-04T15:27:16Z)

@WareZTv, the error with our CDN has been addressed and the ROCm 6.2.3 installation is now working. Could you please confirm the issue is resolved on your end as well?

---

### 评论 #3 — WareZTv (2024-11-04T18:46:38Z)

@harkgill-amd Thanks a lot for your help, the rocm 6.2.3 installation now works with my gpu

---

### 评论 #4 — harkgill-amd (2024-11-04T19:55:51Z)

Great! Happy to help.

---

### 评论 #5 — imkow (2024-11-08T21:27:20Z)

r u kidding me? 

Err:7 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages
  File has unexpected size (68560 != 29552). Mirror sync in progress?

---

### 评论 #6 — jontomas1000 (2024-11-09T07:10:57Z)

I have the same message on a fresh ubuntu server install.  Just added the repo and did sudo apt update. GPU is RX6700XT

`Failed to fetch https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/main/binary-amd64/Packages.gz  File has unexpected size (68560 != 29552). Mirror sync in progress? [IP: 104.96.169.171 443]`


---
