# [Issue]:  /usr/bin/amdgpu-install: satır 436: ${USECASE_GRAPHİCS_PACKAGES[*]}: hatalı ikame

> **Issue #4026**
> **状态**: closed
> **创建时间**: 2024-11-12T18:03:53Z
> **更新时间**: 2024-11-12T19:29:12Z
> **关闭时间**: 2024-11-12T19:29:12Z
> **作者**: LmEnes
> **标签**: Under Investigation, ROCm 6.0.0, ROCm 6.1.0, ROCm 6.2.0, ROCm 6.2.3, ROCm 6.2.2, ROCm 6.2.1, Rx 6600XT
> **URL**: https://github.com/ROCm/ROCm/issues/4026

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)
- **ROCm 6.2.3** (颜色: #ededed)
- **ROCm 6.2.2** (颜色: #ededed)
- **ROCm 6.2.1** (颜色: #ededed)
- **Rx 6600XT** (颜色: #ededed)

## 描述

### Problem Description

i will describe it shorly
languages that has İ letter has this issue, copy of https://github.com/ROCm/ROCm/issues/2888
i had to change my language from linux mint language setting and set it to en_US
after changing language my problem was fixed



### Operating System

Linux Mint 22 Cinnamon

### CPU

AMD Ryzen 5 5500

### GPU

Rx 6600XT

### ROCm Version

ROCm 6.2.3, ROCm 6.2.2, ROCm 6.2.1, ROCm 6.2.0, ROCm 6.1.0, ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Installing any os with Turkish or Azerbaijan language pack must do, im using linux mint but same issue encoured with Ubuntu 22.04.3 or/& newest versions too.
sudo amdgpu-install 
Here's the thing; if i do amdgpu-install --usecase=dkms and sudo amdgpu-install --usecase=rocm it actually installs but if i try to sudo amdgpu-install --usecase=graphics it fails.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

No, i described everything. Its about the İ letter. amdgpu-installer changes its install language by local language, if Turkish or Azeribaijani language detected en_US language may used. 

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-11-12T18:48:51Z)

Hi @LmEnes, the fix mentioned in https://github.com/ROCm/ROCm/issues/2888 will be apart of the ROCm 6.3 release. It will simply set the `LC_ALL` environment variable to `C`  which forces the system to use the default, minimal locale settings. You can set this on your end with `export LC_ALL=C`. Please let me know if this resolves your issue.

---

### 评论 #2 — LmEnes (2024-11-12T19:15:24Z)

Okey

---

### 评论 #3 — LmEnes (2024-11-12T19:16:32Z)

Yeah, fixed the issue.

---
