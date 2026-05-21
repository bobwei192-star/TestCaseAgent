# [Issue]: ubuntu 24.04 with AMD RYZEN AI MAX+ 395 igpu not detected. Firmware is missing.

> **Issue #4992**
> **状态**: closed
> **创建时间**: 2025-06-30T18:13:49Z
> **更新时间**: 2025-10-30T18:41:00Z
> **关闭时间**: 2025-07-02T18:00:57Z
> **作者**: johnxu2013
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4992

## 描述

### Problem Description

$sudo dmesg | grep -i amdgpu

[    3.702135] [drm] amdgpu kernel modesetting enabled.
[    3.705824] amdgpu: Virtual CRAT table created for CPU
[    3.705834] amdgpu: Topology: Add CPU node
[    3.705938] amdgpu 0000:c5:00.0: enabling device (0006 -> 0007)
[    3.708915] amdgpu 0000:c5:00.0: amdgpu: Fatal error during GPU init
[    3.708920] amdgpu 0000:c5:00.0: amdgpu: amdgpu: finishing device.
[    3.708948] amdgpu: probe of 0000:c5:00.0 failed with error -22


it appears that firmware for this gpu is missing. gfx firmwares are not in /lib/firmware/amdgpu.

Can anyone provide firmware?

### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

AMD RYZEN AI MAX+ 395

### GPU

AMD RYZEN AI MAX+ 395/Radeon 8060S

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — johnxu2013 (2025-06-30T18:17:07Z)

Model name:             AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
    CPU family:           26


---

### 评论 #2 — xuegao-tzx (2025-07-01T08:28:21Z)

You can install rocm normally using https://github.com/lamikr/rocm_sdk_builder/

---

### 评论 #3 — johnxu2013 (2025-07-02T18:00:57Z)

This machine works on ollama deepseek-r1 in windows 11 pro using the gpu. And in dual boot ubuntu 24.04, the ollama models processed pretty quick, maybe this is not so critical. I could run models 32b without problem. It may be just ubuntu itself didn't correctly recognize igpu. I would develop using pytorch with cpu code. I also tested using pytorch with directml gpu code on windows 10. pytorch with directml is 5 times slower than the same code running pytorch with cpu.

---

### 评论 #4 — TorgeSchmidt (2025-10-30T18:41:00Z)

@johnxu2013 Fyi: issue seems to be solved on Ubuntu 25.10

---
