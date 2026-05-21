# [Issue]: EL 9.4 dnf repos result in checksum errors (hipblas, 

> **Issue #4041**
> **状态**: closed
> **创建时间**: 2024-11-19T17:20:00Z
> **更新时间**: 2024-11-21T15:22:32Z
> **关闭时间**: 2024-11-21T15:22:32Z
> **作者**: prarit
> **标签**: Under Investigation, ROCm 6.2.3, N/A
> **URL**: https://github.com/ROCm/ROCm/issues/4041

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **N/A** (颜色: #ededed)

## 描述

### Problem Description

Attempting to install hipblas from the EL 6.2.4 repos results in checksum errors.

### Operating System

RHEL9.4

### CPU

n/a

### GPU

n/a

### ROCm Version

ROCm 6.2.3

### ROCm Component

hipBLAS

### Steps to Reproduce

1.  wget https://repo.radeon.com/amdgpu-install/6.2.4/rhel/9.4/amdgpu-install-6.2.60204-1.el9.noarch.rpm
2.  dnf -y install amdgpu-install-6.2.60204-1.el9.noarch.rpm
3. dnf -y install hipblas

this results in:

[root@vm yum.repos.d]# dnf -y --nodocs install hipblas
Updating Subscription Management repositories.
Unable to read consumer identity

This system is not registered with an entitlement server. You can use "rhc" or "subscription-manager" to register.

Last metadata expiration check: 0:14:06 ago on Tue 19 Nov 2024 11:37:50 AM EST.
Dependencies resolved.
====================================================================================================
 Package                     Architecture  Version                              Repository     Size
====================================================================================================
Installing:
 hipblas                     x86_64        2.2.0.60204-139.el9                  rocm          210 k
Installing dependencies:
 amdgpu-core                 noarch        1:6.2.60204-2070768.el9              amdgpu        8.6 k
 comgr                       x86_64        2.8.0.60204-139.el9                  rocm           51 M
 hip-runtime-amd             x86_64        6.2.41134.60204-139.el9              rocm           12 M
 hsa-rocr                    x86_64        1.14.0.60204-139.el9                 rocm          797 k
 libdrm-amdgpu               x86_64        1:2.4.120.60204-2070768.el9          amdgpu         88 k
 libdrm-amdgpu-common        noarch        1.0.0.60204-2070768.el9              amdgpu        9.0 k
 rocblas                     x86_64        4.2.4.60204-139.el9                  rocm          262 M
 rocm-core                   x86_64        6.2.4.60204-139.el9                  rocm           21 k
 rocminfo                    x86_64        1.0.0.60204-139.el9                  rocm           39 k
 rocprofiler-register        x86_64        0.4.0.60204-139.el9                  rocm          301 k
 rocsolver                   x86_64        3.26.2.60204-139.el9                 rocm          338 M
 rocsparse                   x86_64        3.2.1.60204-139.el9                  rocm          245 M

Transaction Summary
====================================================================================================
Install  13 Packages

Total download size: 909 M
Installed size: 7.7 G
Downloading Packages:
[MIRROR] hipblas-2.2.0.60204-139.el9.x86_64.rpm: Downloading successful, but checksum doesn't match. Calculated: 5489434db5722ef1514cbfbe37f6fd10fbd8325bc3900e2f9c1d21dcd29cbdc3(sha256)  Expected: 88a6665a47adc7ccbd7448b7fea50424a2ad5f7485f933767d355a30e9651cfe(sha256) 
[MIRROR] hipblas-2.2.0.60204-139.el9.x86_64.rpm: Downloading successful, but checksum doesn't match. Calculated: 5489434db5722ef1514cbfbe37f6fd10fbd8325bc3900e2f9c1d21dcd29cbdc3(sha256)  Expected: 88a6665a47adc7ccbd7448b7fea50424a2ad5f7485f933767d355a30e9651cfe(sha256) 
[MIRROR] hipblas-2.2.0.60204-139.el9.x86_64.rpm: Downloading successful, but checksum doesn't match. Calculated: 5489434db5722ef1514cbfbe37f6fd10fbd8325bc3900e2f9c1d21dcd29cbdc3(sha256)  Expected: 88a6665a47adc7ccbd7448b7fea50424a2ad5f7485f933767d355a30e9651cfe(sha256) 
[MIRROR] hipblas-2.2.0.60204-139.el9.x86_64.rpm: Downloading successful, but checksum doesn't match. Calculated: 5489434db5722ef1514cbfbe37f6fd10fbd8325bc3900e2f9c1d21dcd29cbdc3(sha256)  Expected: 88a6665a47adc7ccbd7448b7fea50424a2ad5f7485f933767d355a30e9651cfe(sha256) 
[FAILED] hipblas-2.2.0.60204-139.el9.x86_64.rpm: No more mirrors to try - All mirrors were already tried without success
(2-3/13): hip-runtime-amd-6.2.  2% [-                             ] 7.4 MB/s |  22 MB     01:59 ETA
The downloaded packages were saved in cache until the next successful transaction.
You can remove cached packages by executing 'dnf clean packages'.
Error: Error downloading packages:
  hipblas-2.2.0.60204-139.el9.x86_64: Cannot download, all mirrors were already tried without success
[root@vm]#


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2024-11-19T18:18:33Z)

Hi @prarit. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — zichguan-amd (2024-11-21T14:24:31Z)

Hi @prarit, looks like it's similar to https://github.com/ROCm/rocm-install-on-linux/issues/350, which should be fixed now. Can you try it again?

---

### 评论 #3 — prarit (2024-11-21T15:22:32Z)

Thanks @zichguan-amd it looks like this issue is resolved.

---
