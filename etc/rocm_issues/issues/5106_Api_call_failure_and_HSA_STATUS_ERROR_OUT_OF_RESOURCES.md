# Api call failure and HSA_STATUS_ERROR_OUT_OF_RESOURCES

> **Issue #5106**
> **状态**: closed
> **创建时间**: 2025-07-27T17:56:38Z
> **更新时间**: 2025-08-13T18:05:51Z
> **关闭时间**: 2025-08-13T18:05:51Z
> **作者**: indai123
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5106

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Whenever I run rocminfo it prints out following:

WSL environment detected.
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocminfo/rocminfo.cc:1306
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

### Operating System

WSL 2 Ubuntu Jammy 22.04.5 LTS

### CPU

AMD Ryzen 7 7800X3D

### GPU

rx 7800 xt 

### ROCm Version

6.4.2

### ROCm Component

ROCm

### Steps to Reproduce

I upgraded from 6.4.1 to 6.4.2 since I had torch, torchvision and etc for 6.4.2 and when I did sudo reboot and shutdown, this happened.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Now while rx 7800 xt is in the supported category, I find this very frustrating, since I cannot run my gpu for AI development.

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-07-28T13:27:02Z)

Hi @indai123.  Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-07-28T14:37:31Z)

Hi @indai123, unfortunately ROCm 6.4.2 does not have WSL support. Only specific ROCm releases are WSL-compatible; the latest compatible version will be indicated in the install instructions at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html. You'll have to use 6.4.1 on WSL until a newer WSL-compatible version is released, sorry for the inconvenience.

---

### 评论 #3 — schung-amd (2025-08-07T20:47:23Z)

@indai123 We now have a new ROCm on WSL release, 6.4.2.1; please try this and report any issues you encounter. Refer to the installation instructions for the link to the compatible package.


---

### 评论 #4 — schung-amd (2025-08-13T18:05:51Z)

Closing for now; please comment if you're still experiencing this with the latest WSL-compatible ROCm release and appropriate Adrenalin driver version and we can reopen if necessary.

---
