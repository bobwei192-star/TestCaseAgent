# [Issue]: 'Unable to locate package hsa-runtime-rocr4wsl-amdgpu' on win 11 wsl2 ubuntu 24.04 ROCm 7.0.2 on ryzen ai max+ 395

> **Issue #5509**
> **状态**: closed
> **创建时间**: 2025-10-12T10:02:40Z
> **更新时间**: 2025-10-22T20:05:29Z
> **关闭时间**: 2025-10-15T14:27:42Z
> **作者**: isanych
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5509

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Host:
```
OS: Windows 11 25H2 10.0.26200
CPU: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU: AMD Radeon(TM) 8060S Graphics
```
wsl2:
```
OS: Ubuntu 24.04.3 LTS (Noble Numbat)
CPU: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
uname: Linux u24 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```
after installation of https://repo.radeon.com/amdgpu-install/7.0.2/ubuntu/noble/amdgpu-install_7.0.2.70002-1_all.deb amdgpu-install failing:
```
$ sudo amdgpu-install -y --usecase=wsl,rocm --no-dkms
Hit:1 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:2 https://download.docker.com/linux/ubuntu noble InRelease
Hit:3 https://repo.radeon.com/amdgpu/30.10.2/ubuntu noble InRelease
Hit:4 https://repo.radeon.com/rocm/apt/7.0.2 noble InRelease
Hit:5 http://archive.ubuntu.com/ubuntu noble InRelease
Get:6 http://archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
Hit:7 https://repo.radeon.com/graphics/7.0.2/ubuntu noble InRelease
Hit:8 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Hit:9 https://ppa.launchpadcontent.net/ubuntu-toolchain-r/test/ubuntu noble InRelease
Fetched 126 kB in 0s (293 kB/s)
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu
```
Similar issue for ROCm 6 suggest manual download and install of hsa-runtime-rocr4wsl-amdgpu, but I don't see that package in ROCm 7 repos, only in ROCm 6

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat) in wsl2 vm on Windows 11 25H2 10.0.26200

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD Radeon(TM) 8060S Graphics

### ROCm Version

ROCm 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

```
wget https://repo.radeon.com/amdgpu-install/7.0.2/ubuntu/noble/amdgpu-install_7.0.2.70002-1_all.deb
sudo apt-get install -y ./amdgpu-install_7.0.2.70002-1_all.deb
sudo apt update
sudo apt full-upgrade -y
sudo amdgpu-install -y --usecase=wsl,rocm --no-dkms
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
$ /opt/rocm/bin/rocminfo --support
WSL environment detected.
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocminfo/rocminfo.cc:1304
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```
I'm getting the same error from rocminfo built from https://github.com/ROCm/TheRock.git (cmake -DTHEROCK_AMDGPU_TARGETS=gfx1151) and downloaded from https://therock-nightly-tarball.s3.amazonaws.com/therock-dist-linux-gfx1151-7.10.0a20251012.tar.gz

### Additional Information

```
$ sudo modprobe vgem
$ sudo ls -la /dev/dri
total 0
drwxr-xr-x  3 root root        100 Oct 12 09:43 .
drwxr-xr-x 16 root root       3880 Oct 12 09:43 ..
drwxr-xr-x  2 root root         80 Oct 12 09:43 by-path
crw-rw----  1 root video  226,   0 Oct 12 09:43 card0
crw-rw----  1 root render 226, 128 Oct 12 09:43 renderD128
```

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-10-14T14:06:45Z)

Hi @isanych, there is no ROCm 7.0.2 WSL release - currently, the latest release is ROCm 6.4.2.1 https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html#install-radeon-software-for-wsl-with-rocm.

Once a ROCm 7 WSL release is available, the corresponding `hsa-runtime-rocr4wsl-amdgpu` package will be published.

---

### 评论 #2 — wislon (2025-10-18T12:34:11Z)

I've had exactly the same problem, and it led me here. Thanks for clarifying @harkgill-amd :)

> Once a ROCm 7 WSL release is available, the corresponding hsa-runtime-rocr4wsl-amdgpu package will be published.

Do you guys have a rough time-frame for this, i.e. days/weeks/months? 

Thank you :)

---

### 评论 #3 — FruitcakeElemental (2025-10-22T07:08:40Z)

@harkgill-amd I second the request for a timeline.

You've effectively removed a previously advertised feature of rocm without any communications as to why, if its coming back great, but it'd be nice to know when. 

---

### 评论 #4 — harkgill-amd (2025-10-22T15:16:51Z)

Hey @wislon and @FruitcakeElemental, unfortunately I can't share any timelines for the ROCm 7 WSL release. 

The WSL point releases have always lagged behind the major Linux releases - ROCm 7 is no different. There is already work being done to support ROCm 7 on WSL and once I'm able to share more information on a timeline, I'll update this thread. Apologies for the inconvenience.

---

### 评论 #5 — wislon (2025-10-22T20:05:29Z)

Thanks @harkgill-amd I appreciate the update. I've survived without it this long, and I can understand the pressure you all may be facing to deliver all this stuff, wsl being only a tiny part of it.
Thank you (and your team) for the effort you're putting in to get this all working for us! 👍

---
