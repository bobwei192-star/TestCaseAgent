# [Feature]: offline installer as a single file

> **Issue #3560**
> **状态**: open
> **创建时间**: 2024-08-10T01:40:23Z
> **更新时间**: 2025-05-07T20:52:11Z
> **作者**: hpjeonGIT
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3560

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

From: https://rocm.docs.amd.com/projects/install-on-linux/en/develop/install/rocm-offline-installer.html
>> The host system running the ROCm Offline Installer Creator and the target system running the installer must use the same Linux distribution, release version, and Linux kernel version.

My company has firewall and direct download is banned. We have to download all components from a separate environment (windows) and transfer them manually (to RockyOS). The current offline installer creator requires that the creator matches the target system, and this is not available for us.

Can AMD provide those offline installer as a single file (rpm or tar), like what Nvidia does? CUDA driver/toolkits are packaged as a single installer or tar file per OS/environment, and this simplifies the download/install steps.

### Operating System

RockyOS

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2024-08-10T02:25:01Z)

@hpjeonGIT Internal ticket is created to address your request. Thanks!

---

### 评论 #2 — ppanchad-amd (2024-08-16T14:56:44Z)

@hpjeonGIT Firstly, the offline creator tool actually creates a single file for the offline installer when used with the requirements ie. host system = target system.

The reason why we provide a tool to create the install rather than a single pre-packaged installer like NV has to do with the open source nature of ROCm.  Since ROCm is open source and many of our components require different 3rd party dependences, we cannot legally repackage those dependencies in our own installer.

We are aware of this limitation and are working on seeing if we can seperate out the 3rd party dependencies from the installer, and relying on the user to install preq dependencies before the offline install.

Also, note, we do not officially support RockyOS, although you can run the creator tool for the 6.2 release.

---

### 评论 #3 — harkgill-amd (2025-01-22T15:43:58Z)

Hi @hpjeonGIT, please refer to the documentation on the [ROCm Runfile Installer](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/rocm-runfile-installer.html#command-line-install). This installer allows for offline installation without the usage of any native package management system. Could you please confirm if the runfile installer addresses the ask in this feature request?

---

### 评论 #4 — hpjeonGIT (2025-01-22T20:05:41Z)

Hi @harkgill-amd,

As addressed above, we have different OS/computers for download/install - windows for download. Target system is Rocky/RHEL.
Those runfile installers will download components based on the current OS, and this is not a solution for us.

---

### 评论 #5 — harkgill-amd (2025-05-07T20:52:10Z)

The ROCm runfile installer would allow for this as you can download the [RHEL runfile](https://repo.radeon.com/rocm/installer/rocm-runfile-installer/rocm-rel-6.4/el9/) on your Windows machine. The runfile has all the necessary ROCm components packaged within it. The only issue here is that these components have 3rd party dependencies that cannot be packaged, as mentioned in https://github.com/ROCm/ROCm/issues/3560#issuecomment-2293665501. You would need to either have these pre-installed on the target system or have download access during execution of the runfile install in order to resolve the dependencies.

---
