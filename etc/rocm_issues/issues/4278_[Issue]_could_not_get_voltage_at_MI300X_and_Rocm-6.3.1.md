# [Issue]: could not get voltage at MI300X and Rocm-6.3.1

> **Issue #4278**
> **状态**: closed
> **创建时间**: 2025-01-21T01:35:05Z
> **更新时间**: 2025-01-22T14:41:36Z
> **关闭时间**: 2025-01-21T15:56:09Z
> **作者**: Alice1069
> **标签**: Under Investigation, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4278

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

hi, I have a 8 x MI300X system, could not get voltage at MI300X and Rocm-6.3.1

When I run below command, I get:
 rocm-smi --showvoltage


============================ ROCm System Management Interface ============================
==================================== Current voltage =====================================
GPU[0]          : get_volt_metric, Not supported on the given system
GPU[1]          : get_volt_metric, Not supported on the given system
GPU[2]          : get_volt_metric, Not supported on the given system
GPU[3]          : get_volt_metric, Not supported on the given system
GPU[4]          : get_volt_metric, Not supported on the given system
GPU[5]          : get_volt_metric, Not supported on the given system
GPU[6]          : get_volt_metric, Not supported on the given system
GPU[7]          : get_volt_metric, Not supported on the given system
==========================================================================================
================================== End of ROCm SMI Log ===================================

Is it rocm-6.3.1 too new to support this feature? is that will be ok if i install a lower version of Rocm-6.0.
or it's because MI300X hardware does not open this feature?

### Operating System

Ubuntu VERSION="22.04.5 LTS (Jammy Jellyfish)"

### CPU

Intel(R) Xeon(R) Platinum 8470

### GPU

AMD MI300X

### ROCm Version

ROCm 6.3.0

### ROCm Component

rocm_smi_lib

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-01-21T15:18:01Z)

Hi @Alice1069. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-01-21T15:56:09Z)

Hi @Alice1069, as the log suggests this is unsupported on MI300, sorry for the inconvenience. 

---

### 评论 #3 — Alice1069 (2025-01-22T01:41:24Z)

So it's not plan to implement read voltage feature on MI300X?
and it's no use if i downgrade to rocm-6.1.2? previous this version is ok to get voltage at MI250X. I think it might be a software regression issue.
any alternative ways? if i request a new feature of AMD-SMI command, is that work?

---

### 评论 #4 — schung-amd (2025-01-22T14:41:34Z)

This is a hardware issue, the voltage metrics we used on older APUs such as the MI250 are not applicable to the MI300 and there is no alternative metric as far as I'm aware. If older versions of ROCm report voltages for the MI300 they should be treated as spurious values.

---
