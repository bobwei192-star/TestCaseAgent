# [Issue]: Windows 11 ROCm 6.1 and 6.2 detects 6800XT as gfx1036 instead of gfx1030

> **Issue #4390**
> **状态**: closed
> **创建时间**: 2025-02-18T17:23:30Z
> **更新时间**: 2025-02-18T20:48:54Z
> **关闭时间**: 2025-02-18T20:48:54Z
> **作者**: banyartibi
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4390

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Based on documentation AMD Radeon RX 6800 XT | RDNA2 | is gfx1030
With ROCm 6.1 and 6.2 my ASUS TUF 6800XT reports as gfx1036 and nothing working with the GPU.

PS C:\Users\banya> & 'C:\Program Files\AMD\ROCm\6.1\bin\amdgpu-arch.exe'
gfx1036
PS C:\Users\banya>   (Get-WmiObject Win32_OperatingSystem).Version
10.0.22631
PS C:\Users\banya>   (Get-WmiObject win32_Processor).Name
AMD Ryzen 5 9600X 6-Core Processor
PS C:\Users\banya>   (Get-WmiObject win32_VideoController).Name
AMD Radeon(TM) Graphics
AMD Radeon RX 6800 XT
PS C:\Users\banya>

### Operating System

Windows 11 Pro 23H2

### CPU

AMD Ryzen 5 9600X

### GPU

AMD RX6800XT

### ROCm Version

ROCm 6.1.2 and 6.2.4

### ROCm Component

_No response_

### Steps to Reproduce

Install HIP SDK, run \amdgpu-arch.exe or try any AI solution.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-02-18T18:22:09Z)

Hi @banyartibi. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — banyartibi (2025-02-18T19:18:35Z)

Maybe it's the iGPU in the 9600X what mess up?

---

### 评论 #3 — schung-amd (2025-02-18T20:46:41Z)

Hi @banyartibi, gfx1036 is indeed an iGPU architecture which we don't support. Disabling your integrated graphics should resolve this issue.

---

### 评论 #4 — banyartibi (2025-02-18T20:48:50Z)

Thanks that's the case yes. Same RDNA2 and iGPU found by ROCm. Disabled, solved.

---
