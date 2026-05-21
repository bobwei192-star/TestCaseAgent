# [Issue]: amdgpu 30.10.x and ROCm 6.2.4 compatibility list seems incorrect

> **Issue #5963**
> **状态**: closed
> **创建时间**: 2026-02-12T14:14:37Z
> **更新时间**: 2026-02-13T16:23:43Z
> **关闭时间**: 2026-02-12T19:43:55Z
> **作者**: alexschroeter
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5963

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

According to this list (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/user-kernel-space-compat-matrix.html) amdgpu driver 30.10.x is compatible with ROCm 6.2.x but when running this combination and trying to install rocm I get the following conflict.

```
sudo yum install rocm6.2.4 rocm7.2.0 rocm-llvm-devel6.2.4 rocm-llvm-devel7.2.0
ROCm 7.2 repository                                                                                1.1 MB/s | 688 kB     00:00    
ROCm 6.2.4 repository                                                                              4.5 MB/s | 646 kB     00:00    
AMD Graphics 30.10.3 repository                                                                     99 kB/s | 3.0 kB     00:00    
Error: 
 Problem: package rocm6.2.4-6.2.4.60204-139.el9.x86_64 from rocm-6.2.4 requires mivisionx6.2.4 = 3.0.0.60204-139, but none of the providers can be installed
  - package mivisionx6.2.4-3.0.0.60204-139.x86_64 from rocm-6.2.4 requires rocdecode6.2.4, but none of the providers can be installed
  - conflicting requests
  - nothing provides libdrm-amdgpu needed by rocdecode6.2.4-0.6.0.60204-139.x86_64 from rocm-6.2.4
  - nothing provides mesa-amdgpu-va-drivers needed by rocdecode6.2.4-0.6.0.60204-139.x86_64 from rocm-6.2.4
  - nothing provides mesa-amdgpu-dri-drivers needed by rocdecode6.2.4-0.6.0.60204-139.x86_64 from rocm-6.2.4
(try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
```

The issue seems to be that for ROCm 6.2.4 specifically, the rocdecode package still has hard dependencies on libdrm-amdgpu, mesa-amdgpu-va-drivers, and mesa-amdgpu-dri-drivers. This dependency seems to have been removed later, so my 6.2.4 install is stuck with the old dependency chain.

### Operating System

Alma 9.7

### CPU

Irrelevant

### GPU

MI210

### ROCm Version

6.2.4,7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — tcgu-amd (2026-02-12T19:43:55Z)

Hi @alexschroeter, thanks for bring this problem to our attention. Yes this is a known dependency issue, the core amdgpu-dkms should be compatible, but the peripheral library dependencies for some of the ROCm packages have changed. Do you need mivisionx/rocdecode as part of your install? If you don't need it, I think you can just exclude them. If you do need them, you can try installing the missing dependencies from the old index and see if that works. Thanks! 

---

### 评论 #2 — alexschroeter (2026-02-13T16:23:43Z)

I fixed the issue by installing everything that is part of the rocm package separately and removing mivisionx6.2.4 and rocdecode6.2.4 from the list. This is not a satisfactory solution since it leaves packages that might be needed off the table. I am not sure how I feel about taking packages of one driver version and installing them on another driver version.

I think AMD could do more here. It seems reasonable to me to add these dependent packages to the driver repos of all those that claim to have compatibility with the last rocm version, which has the dependency. This would ensure they are compatible, and since they wouldn't be referenced in the higher ROCM version, they would simply not be installed.

---
