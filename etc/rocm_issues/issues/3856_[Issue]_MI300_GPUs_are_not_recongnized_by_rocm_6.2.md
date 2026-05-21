# [Issue]: MI300 GPUs are not recongnized by rocm 6.2

> **Issue #3856**
> **状态**: closed
> **创建时间**: 2024-10-02T15:18:18Z
> **更新时间**: 2024-11-13T02:56:36Z
> **关闭时间**: 2024-10-02T18:22:41Z
> **作者**: GowriShankarEAAS
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3856

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

MI300x GPUs are stopped recognizing after reboot. below error is show on dmesgs. Kindly suggest how to resolve this issue

OS:
NAME="Ubuntu"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
CPU:
model name      : AMD EPYC 9684X 96-Core Processor
GPU:



Error log:

  356.920249] amdgpu 0000:05:00.0: amdgpu: get invalid ip discovery binary signature
[  361.717929] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[  361.718375] amdgpu 0000:05:00.0: amdgpu: Fatal error during GPU init
[  361.718401] amdgpu 0000:05:00.0: amdgpu: amdgpu: finishing device.
[  361.718710] amdgpu: probe of 0000:05:00.0 failed with error -22
[  361.718735] amdgpu: legacy kernel without apple_gmux_detect()
[  361.719281] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[  361.719452] [drm] register mmio base: 0xC4000000
[  361.719455] [drm] register mmio size: 2097152


### Operating System

ubuntu 22.04.04

### CPU

AMD EPYC 9684X 96-Core Processor

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.2.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2024-10-02T16:09:15Z)

Hi @GowriShankarEAAS, couple of questions here,

1. Is this issue persistent on every reboot?
2. Could you confirm which IFWI/VBIOS you are testing with?
3. Could you try loading and unloading the driver modules with
```
sudo modprobe -r amdgpu
sudo modprobe amdgpu
```


---

### 评论 #2 — GowriShankarEAAS (2024-10-02T16:44:22Z)

Hi @harkgill-amd,

Is this issue persistent on every reboot? Yes
Could you confirm which IFWI/VBIOS you are testing with? will update
Could you try loading and unloading the driver modules with ? i did. same issue

---

### 评论 #3 — GowriShankarEAAS (2024-10-02T16:48:28Z)

Hi @harkgill-amd, how to get the IFWI/VBIOS details ?

---

### 评论 #4 — harkgill-amd (2024-10-02T18:22:41Z)

Moved to internal discussion.

---

### 评论 #5 — hetaoaoao (2024-11-13T02:56:35Z)

Same issue here, did you find a solution @GowriShankarEAAS ? is it a software issue or hardware issue?

---
