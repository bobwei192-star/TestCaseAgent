# [Issue]: Repo not found

> **Issue #3191**
> **状态**: closed
> **创建时间**: 2024-05-30T17:44:36Z
> **更新时间**: 2024-06-06T19:47:46Z
> **关闭时间**: 2024-06-06T19:47:46Z
> **作者**: tsais7
> **标签**: AMD Radeon RX 7900 XT, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3191

## 标签

- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Install instructions for SUSE Linux does not work 
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html
```
sudo zypper refresh
Retrieving repository 'AMDGPU 6.1.1 repository' metadata ....................................[error]
Repository 'AMDGPU 6.1.1 repository' is invalid.
[amdgpu|https://repo.radeon.com/amdgpu/6.1.1/sle/20240524/main/x86_64] Valid metadata not found at specified URL
History:
 - [|] Error trying to read from 'https://repo.radeon.com/amdgpu/6.1.1/sle/20240524/main/x86_64'
 - Download (curl) error for 'https://repo.radeon.com/amdgpu/6.1.1/sle/20240524/main/x86_64/content':
   Error code: Curl error 56
   Error message: The requested URL returned error: 404
```

GPU: AMD Radeon RX6700S
ROCM version: 6.1.1

### Operating System

openSUSE Tumbleweed

### CPU

AMD Ryzen 9 6900HS with Radeon Graphics

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-06-06T19:47:46Z)

Hi @tsaist1 openSUSE Tumbleweed is not supported by ROCm, please see a list of supported operating systems below. I could not reproduce this issue on SUSE Linux Enterprise Server. Please re-open if you see this issue on a supported OS. Thanks!

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html



---
