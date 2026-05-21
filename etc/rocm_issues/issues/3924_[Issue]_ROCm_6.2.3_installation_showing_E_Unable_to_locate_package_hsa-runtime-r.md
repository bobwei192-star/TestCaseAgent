# [Issue]: ROCm 6.2.3 installation showing "E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu"

> **Issue #3924**
> **状态**: closed
> **创建时间**: 2024-10-20T12:56:23Z
> **更新时间**: 2024-10-21T18:04:40Z
> **关闭时间**: 2024-10-21T18:04:40Z
> **作者**: jzy023
> **标签**: ROCm 6.2.3, AMD Radeon RX 7900XTX
> **URL**: https://github.com/ROCm/ROCm/issues/3924

## 标签

- **ROCm 6.2.3** (颜色: #ededed)
- **AMD Radeon RX 7900XTX** (颜色: #ededed)

## 描述

### Problem Description

I am trying to install ROCm on WSL2 (Ubuntu 22.04.5 LTS)
to recreate the issue:
>
sudo apt update 
wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all
sudo apt install ./amdgpu-install_6.2.60203-1_all
amdgpu-install -y --usecase=wsl,rocm --no-dkms


and the terminal shows:
>
Hit:1 https://repo.radeon.com/amdgpu/6.2.3/ubuntu jammy InRelease
Hit:2 https://repo.radeon.com/rocm/apt/6.2.3 jammy InRelease
Hit:4 http://archive.ubuntu.com/ubuntu jammy InRelease
Hit:5 http://security.ubuntu.com/ubuntu jammy-security InRelease
Hit:6 http://archive.ubuntu.com/ubuntu jammy-updates InRelease
Hit:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu



However, if i do the same procedure but with "./amdgpu-install_6.1.60103-1_all.deb", the problem goes away.
what could be the issue here and what is the fix?



### Operating System

Ubuntu 22.04.5 LTS (WSL2)

### CPU

AMD Ryzen 7900X

### GPU

AMD Radeon RX 7900XTX

### GPU Driver

AMD Software: Adrenalin Edition 24.10.1

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

to recreate the issue:
>
sudo apt update 
wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all
sudo apt install ./amdgpu-install_6.2.60203-1_all
amdgpu-install -y --usecase=wsl,rocm --no-dkms


and the terminal shows:
>
Hit:1 https://repo.radeon.com/amdgpu/6.2.3/ubuntu jammy InRelease
Hit:2 https://repo.radeon.com/rocm/apt/6.2.3 jammy InRelease
Hit:4 http://archive.ubuntu.com/ubuntu jammy InRelease
Hit:5 http://security.ubuntu.com/ubuntu jammy-security InRelease
Hit:6 http://archive.ubuntu.com/ubuntu jammy-updates InRelease
Hit:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — moyutegong (2024-10-21T06:48:49Z)

You can execute the following command to install hsa-runtime-rocr4wsl-amdgpu.
```
wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.22.04_amd64.deb
sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.22.04_amd64.deb
```

---

### 评论 #2 — harkgill-amd (2024-10-21T18:04:14Z)

Hi @jzy023, WSL support on ROCm 6.2.3 has not yet been officially released. 

The 6.2.3 `hsa-runtime-rocr4wsl-amdgpu` package will be packaged within the WSL usecase once support is enabled. As a temporary workaround, you can pull the package directly from repo.radeon.com and install it using the commands listed by @moyutegong.

---
