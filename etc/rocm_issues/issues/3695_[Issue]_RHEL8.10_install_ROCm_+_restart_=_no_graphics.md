# [Issue]: RHEL8.10 install ROCm + restart = no graphics

> **Issue #3695**
> **状态**: closed
> **创建时间**: 2024-09-09T21:55:54Z
> **更新时间**: 2024-09-10T20:14:29Z
> **关闭时间**: 2024-09-10T20:14:28Z
> **作者**: rogerselly
> **标签**: Under Investigation, AMD Radeon Pro VII, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3695

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro VII** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

New RHEL8.10 with Registered Subscription. Followed AMD instructions here https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html and https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/rhel.html using tabs for RHEL8.10, up to sudo dnf install rocm, then restart causes Red Hat logo to appear briefly then some commands execute and graphics does blank screen.
Note: integrated graphics disabled.
rocminfo runs ok before restart.
ROCT-Thunk-Interface cmake build fails on libdrm .pc not found.
Maybe libdrm has a conflict or fault with this ROCm package for RHEL8.10 ?
Hardware or Software ?  Ubuntu 22.04 + ROCm 6.1 works great on same hardware. See below rocminfo


### Operating System

RHEL 8.10

### CPU

AMD Ryzen 7 PRO 4750G with Radeon Graphics

### GPU

AMD Radeon Pro VII

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

New RHEL8.10 install
AMD ROCm install instructions as above 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[rocminfo.txt](https://github.com/user-attachments/files/16936976/rocminfo.txt)


### Additional Information

[rocminfo.txt](https://github.com/user-attachments/files/16936989/rocminfo.txt)


---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-09-10T14:19:54Z)

Hi @rogerselly, could you please try installing ROCm with the [amdgpu-install method](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html#red-hat-enterprise-linux) while specifying the graphics and rocm usecase? 

To do this, you would simply install the prerequisites and then run the following
```
sudo yum install https://repo.radeon.com/amdgpu-install/6.2/el/8.10/amdgpu-install-6.2.60200-1.el8.noarch.rpm
sudo amdgpu-install --usecase=graphics,rocm
```


---

### 评论 #2 — rogerselly (2024-09-10T20:14:28Z)

amdgpu-install method worked. Problem solved, Thank you!

---
