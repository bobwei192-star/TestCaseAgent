# [Documentation]: Release 6.3.2 [troubleshooting issue #8]

> **Issue #4328**
> **状态**: closed
> **创建时间**: 2025-02-02T05:46:46Z
> **更新时间**: 2025-05-28T15:01:34Z
> **关闭时间**: 2025-05-28T15:01:33Z
> **作者**: Glohern
> **标签**: Under Investigation, Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4328

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

Description:

Everything was fine during the installation process, and I was able to load the amdgpu module twice. However, after restarting my system, I faced multiple issues trying to make my kernel (6.11.0-14-generic) load the graphics module. It became impossible to load the amdgpu module, and tools like rocminfo and clinfo indicated that the graphics were not loaded.

The cause was related to Secure Boot, which was preventing the kernel from loading the amdgpu module. This issue was not mentioned in the installation prerequisites or the [Installation troubleshooting section](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.2/reference/install-faq.html#issue-8-the-amdgpu-driver-is-not-loaded-after-installation) in the documentation.

Recommendation:

It would be helpful to include a note in the installation prerequisites or troubleshooting section of the documentation to inform users that Secure Boot must be disabled in order for the amdgpu driver to load properly.

    Kernel version: 6.11.0-14-generic 
    Dist: Ubuntu 24.10
    Issue: Secure Boot blocking the loading of the amdgpu module
    Suggested fix: Disable Secure Boot in BIOS/UEFI
    Observations: Not mentioned in the installation prerequisites or the Installation troubleshooting issue#8


---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-02-03T17:02:42Z)

Hi @Glohern, as you encountered, a DKMS installation will flag Secure Boot and result in the kernel failing to load. The amdgpu kernel module installation does include a check for Secure Boot and will sign the driver with a MOK to avoid this. After the driver is signed, the user must import/enroll the key using the MOK manager to avoid errors on subsequent reboots. You can find more information on this in the amdgpu documentation under [Secure Boot Support](https://amdgpu-install.readthedocs.io/en/latest/install-installing.html#secure-boot-support). 

I do agree that this should be more visible in the ROCm documentation as well. Will work on getting the docs updated.

---

### 评论 #2 — harkgill-amd (2025-05-28T15:01:33Z)

Both the installation prerequisites and troubleshooting pages have been updated to highlight the importance of driver signing/secure boot. 

[Installation Prerequisites](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#secure-boot)

![Image](https://github.com/user-attachments/assets/c718f1f4-de1a-4f87-bdf5-b3254e795128)

[Installation Troubleshooting](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/install-faq.html#installation-troubleshooting)

![Image](https://github.com/user-attachments/assets/c7312fb1-2f1a-40b6-b9b5-3c4a1098f920)

---
