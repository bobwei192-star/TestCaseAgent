# [Issue]: Problems installing ROCm 6.3.* on Ubuntu 22.04

> **Issue #4489**
> **状态**: closed
> **创建时间**: 2025-03-12T23:47:41Z
> **更新时间**: 2025-05-07T19:49:23Z
> **关闭时间**: 2025-05-07T19:49:22Z
> **作者**: loadams
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4489

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am working with the following system:

NAME="Ubuntu"
VERSION="22.04.5 LTS (Jammy Jellyfish)"
CPU:
model name      : Intel(R) Xeon(R) Platinum 8480C
GPU:
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:          AMD Instinct MI300X VF
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-

The specific kernel version that is running is 5.15.0-1081-azure (when I successfully install 6.2.4).  

When I update the kernel version to 6.8.0-1021-azure I am unable to install either 6.2.4 or 6.3.* (which requires the newer kernel based on [these docs](https://rocm.docs.amd.com/en/docs-6.3.1/compatibility/compatibility-matrix.html#compatibility-matrix)).

After updating the kernel and running `sudo modprobe amdgpu` I get the attached logs from dmesg (no errors from modprobe but it takes quite a while to return).

[modprobe_log.txt](https://github.com/user-attachments/files/19219195/modprobe_log.txt)


### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

Intel(R) Xeon(R) Platinum 8480C

### GPU

AMD Instinct MI300X VF

### ROCm Version

ROCm 6.3.*

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-03-17T15:53:29Z)

Hi @loadams. Internal ticket has been created to investigate your issue. Thanks! 

---

### 评论 #2 — darren-amd (2025-03-18T19:04:25Z)

Hi @loadams,

Thanks for reporting the issue! Could you please provide the complete `dmesg` dump. Also, what is the error message when you try to install ROCm on the newer kernel version? Could you try to [uninstall](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html#uninstalling-rocm), [reinstall](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html#installation), run `rocminfo` and provide the error log? Thanks!

---

### 评论 #3 — loadams (2025-03-19T18:08:44Z)

Thanks @ppanchad-amd  and @darren-amd.  I'll get the full dmesg log and share it shortly, just need to wrap up other work on the node first before reinstalling/rebooting/etc.

---

### 评论 #4 — darren-amd (2025-05-07T19:02:44Z)

Hi @loadams,

Is this issue still persisting? 

---

### 评论 #5 — loadams (2025-05-07T19:49:22Z)

Hi @darren-amd  - we were able to resolve this internally, thanks for following up but I can close this now.

---
