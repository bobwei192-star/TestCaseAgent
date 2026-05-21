# [Issue]: MI308x can only achieve 2TB/s in the /opt/rocm/bin/roofline*

> **Issue #5070**
> **状态**: open
> **创建时间**: 2025-07-21T01:43:44Z
> **更新时间**: 2025-07-23T01:53:39Z
> **作者**: shengtai1990
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5070

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

We tests our HPC program, which computing density is 0.5/1.0 FLOPS/Byte in double/single precision, the speed of it is limited by the memory bandwidth of HBM. 
For the MI308x, which we have tried three different rocm, 2 different operating system, it always shows 2TB/s in the /opt/rocm/bin/roofline* tests. For the MI300x, it gives 4.2TB/s, the memory bandwidth should not decrease from MI300x to MI308x. 
The speed of our program runs on MI300x is like 3 times faster than MI308x. I doubt it caused by the rocm is not very fit the MI308x, or it has some bugs for MI308x. 

### Operating System

Ubuntu 22.04.5 LTS and Rocky-9.5

### CPU

AMD EPYC 9654

### GPU

AMD instinct MI308x

### ROCm Version

Rocm-7.0.0, Rocm-6.4.1, Rocm-6.3.3

### ROCm Component

HIPCC

### Steps to Reproduce

<img width="973" height="627" alt="Image" src="https://github.com/user-attachments/assets/5bea4566-0f74-422f-bdac-82a056413b08" />

<img width="992" height="595" alt="Image" src="https://github.com/user-attachments/assets/c207403c-aecf-4806-9b0f-d1037f7c2677" />

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-07-21T13:23:57Z)

Hi @shengtai1990. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-07-21T16:49:06Z)

Hi @shengtai1990, thanks for reaching out! I am sorry that you are experiencing issues with MI308x. Can do you know the firmware version on your 308 system?


---

### 评论 #3 — shengtai1990 (2025-07-22T01:21:48Z)

> Hi [@shengtai1990](https://github.com/shengtai1990), thanks for reaching out! I am sorry that you are experiencing issues with MI308x. Can do you know the firmware version on your 308 system?

The current 308 system is Version: 01.21.01

---

### 评论 #4 — tcgu-amd (2025-07-22T14:10:59Z)

@shengtai1990 Thanks for the additional info. We were able to reproduce this issue with the roofline binaries. We are currently in the process of root-cause analysis. To help us better isolate the issue, do you think it would be possible to also provide us a reproducer for your program that reported a 3x slow down on 308 compared to 300? Thanks! 

---

### 评论 #5 — shengtai1990 (2025-07-23T01:53:39Z)

@tcgu-amd The current HPC software is open source code SIMULATeQCD, for the performance you may want to test the target multiRHSProf, which gives 2x slow down on 308. Thanks! And for other softwares in Lattice QCD, like QUDA, Grid, I think the speed are as well slow down a lot, since all of them are HBM memory limited. 

---
