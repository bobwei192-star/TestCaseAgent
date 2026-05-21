# [Issue]: ROCm 7.0.2 Installation Error

> **Issue #5535**
> **状态**: closed
> **创建时间**: 2025-10-17T17:45:33Z
> **更新时间**: 2025-10-22T16:13:58Z
> **关闭时间**: 2025-10-22T16:13:58Z
> **作者**: patelMaharshii
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5535

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Hey everyone,

I recently tried downloading the entire ROCm ecosystem but for some reason my gpu isn't being detected (I think). I'm a bit of a beginner to this so any help is appreciated. Just as a summary, I have a 9060 xt 16 gb and I'm trying to download the latest software (7.0.2) on WSL2 Ubuntu on Windows 11.  I'm not sure if this version can run on WSL2, but if it can't can anyone let me know the latest version I can run?

wsl --version output:
WSL version: 2.6.1.0
Kernel version: 6.6.87.2-1
WSLg version: 1.0.66
MSRDC version: 1.2.6353
Direct3D version: 1.611.1-81528511
DXCore version: 10.0.26100.1-240331-1435.ge-release
Windows version: 10.0.26100.6899

Windows Info:
AMD Ryzen 5 9600X 6-Core Processor
AMD Radeon RX 9060 XT
AMD Radeon(TM) Graphics

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 5 9600X 6-Core Processor

### GPU

AMD Radeon RX 9060 XT 16GB

### ROCm Version

ROCm 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

I followed all the instructions from these [docs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/detailed-install.html).

Prerequisites: 
I used group membership for configuring permissions for GPU access.

Installation Methods:
I went with the installation via native package manager. 

Post-Installation:
I configured ROCm using Option A: update-alternatives. I can see the packages are installed but when I do the following commands it gives errors:

rocminfo:
WSL environment detected.
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocminfo/rocminfo.cc:1304
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events

amd-smi version:
ERROR:root:Unable to get devices, driver not initialized (amdgpu not found in modules)
ERROR:root:Unable to detect any GPU devices, check amdgpu version and module status (sudo modprobe amdgpu)
ERROR:root:Unable to detect any CPU devices, check amd_hsmp version and module status (sudo modprobe amd_hsmp)
AMDSMI Tool: 26.0.2+39589fda | AMDSMI Library version: 26.0.2 | ROCm version: 7.0.2

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

WSL environment detected.
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocminfo/rocminfo.cc:1304
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-10-17T17:50:59Z)

Hi @patelMaharshii, for ROCm on WSL, the latest supported release is 6.4.4, here's the relevant documentation. https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html#install-radeon-software-for-wsl-with-rocm. 

You can uninstall the 7.0.2 packages with,
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then continue to follow the steps in the above link to install 6.4.4. Let me know if you have any questions!



---

### 评论 #2 — harkgill-amd (2025-10-22T14:29:20Z)

Closing for now but feel free to leave a comment if you have any further questions.

---
