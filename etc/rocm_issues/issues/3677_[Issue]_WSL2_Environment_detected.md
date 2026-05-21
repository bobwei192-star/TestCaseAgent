# [Issue]: WSL2 Environment detected

> **Issue #3677**
> **状态**: closed
> **创建时间**: 2024-09-04T19:16:35Z
> **更新时间**: 2024-09-10T16:18:33Z
> **关闭时间**: 2024-09-04T21:06:37Z
> **作者**: BedBath-N-UrMom
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3677

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

When i run rocminfo i get the error

WSL environment detected.
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1306
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

Also when I try to run 

 echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)"

There is nothing listed. I have tried different versions of the AMD adrenalin software that shows support for wsl2.

### Operating System

WSL2 Ubuntu 24.04

### CPU

Ryzen 9 3900x

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

rocminfo

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

WSL environment detected.
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1306
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2024-09-04T20:36:37Z)

Ubuntu 24.04 and ROCm 6.2.0 are not currently supported for use with ROCm on WSL. These incompatibilities are likely causing the `WSL environment detected` error that you are encountering. 

The only supported configuration would be ROCm 6.1.3 and Ubuntu 22.04 as mentioned in the [compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#compatibility-matrices-wsl). Could you please try the steps at [Install Radeon software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#install-radeon-software-for-wsl-with-rocm) on the aforementioned setup to see if your issue is resolved?

---

### 评论 #2 — BedBath-N-UrMom (2024-09-04T20:48:33Z)

I have tried that but i guess my gpu isn't supported. I actually have a 7800xt and it is not listed in the supported gpus. In Ubuntu 22.04 i get the ROCR: unsupported GPU error. Is there a plan to support a 7800xt and if so is there an estimated time frame?

---

### 评论 #3 — harkgill-amd (2024-09-04T21:06:37Z)

Unfortunately, the ROCR error is expected as well with the 7800XT. The WSL release is technically a "beta release" and only the GPUs listed in the compatibility matrix are supported. There will likely be support for additional GPUs added in future releases, but I can't provide a specific timeframe. 

---

### 评论 #4 — githust66 (2024-09-07T11:41:09Z)

> Ubuntu 24.04 and ROCm 6.2.0 are not currently supported for use with ROCm on WSL. These incompatibilities are likely causing the `WSL environment detected` error that you are encountering.
> 
> The only supported configuration would be ROCm 6.1.3 and Ubuntu 22.04 as mentioned in the [compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#compatibility-matrices-wsl). Could you please try the steps at [Install Radeon software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#install-radeon-software-for-wsl-with-rocm) on the aforementioned setup to see if your issue is resolved?

Will WSL support ROCM6.2.0+Torch2.20+, the current ROCM6.1.3 compatible torch version is 2.1.2, the version is a bit low, and many models do not support the use of this version

---

### 评论 #5 — supernovae (2024-09-10T16:18:32Z)

Any chance to support WSL2 with ROCM 6.2? Seems like we take one step forward and two steps back.  Ubuntu 24.04 support is becoming critical and when we finally got it, it didn't work with wsl2 :( 

---
