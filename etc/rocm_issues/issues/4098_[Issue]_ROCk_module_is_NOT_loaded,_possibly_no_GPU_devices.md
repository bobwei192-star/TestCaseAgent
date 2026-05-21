# [Issue]: ROCk module is NOT loaded, possibly no GPU devices

> **Issue #4098**
> **状态**: closed
> **创建时间**: 2024-12-04T17:28:02Z
> **更新时间**: 2025-03-30T09:01:03Z
> **关闭时间**: 2024-12-10T03:25:49Z
> **作者**: thomaslittletrainx
> **标签**: Under Investigation, ROCm 6.2.3, AMD Instinct MI210X
> **URL**: https://github.com/ROCm/ROCm/issues/4098

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **AMD Instinct MI210X** (颜色: #ededed)

## 描述

### Problem Description

I'm an internal user from AMD. I'm trying to install rocm on a 4xMI210 GPU Dell server. Followed all steps in this [guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/detailed-install.html). Looks like no gpu is detected.

### Operating System

24.04.1 LTS (Noble Numbat) (GNU/Linux 6.8.0-49-generic x86_64)

### CPU

Intel(R) Xeon(R) Platinum 8462Y+

### GPU

AMD Instinct MI210X

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

```
amd@dbs-mkm-gpu01:~$ clinfo 
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3625.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback
  Platform Name:                                 AMD Accelerated Parallel Processing
  Number of devices:                               0
```

```
amd@dbs-mkm-gpu01:~$ rocm-smi
cat: /sys/module/amdgpu/initstate: No such file or directory
ERROR:root:Driver not initialized (amdgpu not found in modules)
```

```
amd@dbs-mkm-gpu01:~$ lspci | grep -i vga
lspci | grep -i amd
04:00.0 VGA compatible controller: Matrox Electronics Systems Ltd. Integrated Matrox G200eW3 Graphics Controller (rev 04)
4a:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 14c7
4b:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 14c8
4c:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Aldebaran/MI200 [Instinct MI210] (rev 02)
61:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 14c7
62:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 14c8
63:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Aldebaran/MI200 [Instinct MI210] (rev 02)
ca:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 14c7
cb:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 14c8
cc:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Aldebaran/MI200 [Instinct MI210] (rev 02)
e1:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 14c7
e2:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 14c8
e3:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Aldebaran/MI200 [Instinct MI210] (rev 02)
```



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support


amd@dbs-mkm-gpu01:~$ rocminfo
ROCk module is NOT loaded, possibly no GPU devices

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-12-04T20:28:36Z)

Hi @thomaslittletrainx, it looks like the amdgpu module failed to load. Can you try manually loading the module with `sudo modprobe amdgpu` and rerunning `rocm-smi`/`rocminfo`? Please also provide the dmesg output so we can further investigate why the amdgpu module failed to initialize.

---

### 评论 #2 — thomaslittletrainx (2024-12-10T03:25:24Z)

Hi I tried all solution from the Internet. And finally finds that the problem is an option in grub.
Remove the nomodeset option in grub solves everything. Thanks!

---

### 评论 #3 — gaohey (2025-03-30T09:01:02Z)

This workd !!! I had  7900xtx and only sees one monitor after removing `nomodeset` in grub, it fixes everything !! thank you 

---
