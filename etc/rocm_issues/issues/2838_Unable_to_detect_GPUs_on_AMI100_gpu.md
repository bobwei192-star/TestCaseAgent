# Unable to detect GPUs on AMI100 gpu 

> **Issue #2838**
> **状态**: closed
> **创建时间**: 2024-01-25T05:59:00Z
> **更新时间**: 2024-01-29T20:44:02Z
> **关闭时间**: 2024-01-29T20:44:02Z
> **作者**: kf-cuanschutz
> **标签**: Under Investigation, AMD Instinct MI100, ROCm 5.5.0
> **URL**: https://github.com/ROCm/ROCm/issues/2838

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI100** (颜色: #ededed)
- **ROCm 5.5.0** (颜色: #ededed)

## 描述

### Problem Description

On our HPC cluster, 
we are using pytorch/1.13.0 which was installed with rocm/5.2.3.
After loading those modules I am unable to detect the AMD GPU

```bash
[ nvidia_amd_benchmarking]$ python3
Python 3.10.0 (default, Mar  3 2022, 09:58:08) [GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.is_available()
False
```

When running rocminfo I get:

```bash
nvidia_amd_benchmarking]$ rocminfo
ROCk module is loaded
Unable to open /dev/kfd read-write: Permission denied
Failed to get user name to check for video group membership
```

When running the test from [here](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533) I get the following: 

```bash
Checking ROCM support...
BAD: No ROCM devices found.
Checking PyTorch...
GOOD: PyTorch is working fine.
Checking user groups...
Cannot find rocminfo command information. Unable to determine if AMDGPU drivers with ROCM support were installed.
```

rocm-smi shows:

```bash
======================= ROCm System Management Interface =======================
================================= Concise Info =================================
GPU  Temp   AvgPwr  SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
0    33.0c  35.0W   300Mhz  1200Mhz  0%   auto  290.0W    0%   0%    
================================================================================
============================= End of ROCm SMI Log ==============================
```



### Operating System

Red Hat Enterprise Linux 8.4 (Ootpa)

### CPU

Model name:          AMD EPYC 7543 32-Core Processor

### GPU

AMD Instinct MI100

### ROCm Version

ROCm 5.5.0

### ROCm Component

rocminfo

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — kf-cuanschutz (2024-01-25T06:00:31Z)

ROCM version is rocm/5.2.3. It did not show when looking at the drop-down menu

---

### 评论 #2 — nartmada (2024-01-25T17:24:39Z)

An internal ticket has been created to investigate the issue.

---

### 评论 #3 — vstempen (2024-01-25T17:28:20Z)

Hi, could you check your user privileges? Here I have just tried rocminfo for a new user, for example:
$ sudo useradd -g users test
$ id test
uid=1001(test) gid=100(users) groups=100(users)
$ rocminfo
ROCk module is loaded
Unable to open /dev/kfd read-write: Permission denied
rocm is member of render group
$ id rocm
uid=1000(rocm) gid=1000(rocm) groups=1000(rocm),4(adm),24(cdrom),27(sudo),30(dip),44(video),46(plugdev),110(render),122(lpadmin),135(lxd),136(sambashare)
). 

Can you also try to run the commands with sudo?
Thanks.

---

### 评论 #4 — kf-cuanschutz (2024-01-25T17:35:36Z)

So, I do not have user privileges on the cluster, I have reached out to our admins on the cluster 
regarding the rocminfo permission denied issue. Will get back to you guys.

---

### 评论 #5 — kf-cuanschutz (2024-01-29T20:43:58Z)

The issue has been fixed! I got removed from the video group without realizing it. Once they put me back in the video group everything worked seamlessly.

---
