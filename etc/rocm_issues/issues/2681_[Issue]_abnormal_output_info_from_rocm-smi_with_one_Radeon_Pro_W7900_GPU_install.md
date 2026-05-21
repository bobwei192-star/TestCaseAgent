# [Issue]: abnormal output info from rocm-smi with one Radeon Pro W7900 GPU installed

> **Issue #2681**
> **状态**: closed
> **创建时间**: 2023-11-29T14:58:44Z
> **更新时间**: 2024-02-02T04:36:04Z
> **关闭时间**: 2024-02-02T04:36:03Z
> **作者**: alexhegit
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2681

## 描述

### Problem Description

1. Run rocm-smi
2. see the output
- unsupported info output from rocm-smi
- Why here are two GPUs info but just one Radeon Pro W7900 GPU installed

### Operating System

Ubuntu 22.04.3

### CPU

AMD Ryzen 7900

### GPU

AMD Radeon Pro W7900

### ROCm Version

5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

Run rocm-smi

### Output of /opt/rocm/bin/rocminfo --support

amd@AIG-PM:~$ rocm-smi


========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
GPU[0]          : get_power_avg, Unexpected data received
====================================================================================
====================================================================================
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
GPU[0]          : get_power_cap, Unexpected data received
ERROR: GPU[1]   : sclk clock is unsupported
====================================================================================
GPU[1]          : get_power_cap, Not supported on the given system
GPU  Temp (DieEdge)  AvgPwr  SCLK  MCLK     Fan  Perf     PwrCap       VRAM%  GPU%
0    N/A             N/A     None  None     0%   unknown  Unsupported    0%   0%
1    42.0c           0.159W  None  3000Mhz  0%   auto     Unsupported    3%   0%
====================================================================================
=============================== End of ROCm SMI Log ================================


---

## 评论 (4 条)

### 评论 #1 — kentrussell (2024-01-02T17:47:54Z)

This was due to a disconnect between the SMI and the kernel. I am not sure if the fix is  ROCm 6.0 or 6.1. @dmitrii-galantsev do you know offhand?

---

### 评论 #2 — dmitrii-galantsev (2024-01-04T15:41:46Z)

@kentrussell 6.0 should have it fixed
likely https://github.com/ROCm/rocm_smi_lib/commit/41ade41d8467eadc37ab60c4a423a1ece9a65449 and https://github.com/ROCm/rocm_smi_lib/commit/a4b470fe71f723fe2c3b90480922820ae8102558 . Both in 6.0

---

### 评论 #3 — nartmada (2024-01-17T04:48:11Z)

Hi @alexhegit, please close the ticket if the issue has been fixed.  Thanks.

---

### 评论 #4 — nartmada (2024-02-02T04:36:04Z)

Closing the ticket as no response from @alexhegit.  Please re-open if the issue still exists with latest ROCm 6.0.2.  Thanks.

---
