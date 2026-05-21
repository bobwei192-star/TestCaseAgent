# rccl test fail with "free(): double free detected in tcache 2" on system with rocm 5.6.1 and MI250

> **Issue #2448**
> **状态**: closed
> **创建时间**: 2023-09-12T13:42:21Z
> **更新时间**: 2023-10-29T05:48:26Z
> **关闭时间**: 2023-09-12T14:27:33Z
> **作者**: walkup
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2448

## 描述

RCCL tests were working correctly on our system with older ROCM software, but the same tests fail with "free(): double free detected in tcache 2" after installing ROCM 5.6.1.  The same type of failure occurs with all RCCL tests that we have tried, including all_reduce_perf from the rccl-tests repo.  Our test system has Driver version: 4.18.0-477.21.1.el8_8.x86_64.  This failure prevents multi-gpu AI training jobs on our system with MI250 GPUs.

---

## 评论 (3 条)

### 评论 #1 — walkup (2023-09-12T14:27:33Z)

It appears that the issue was with the driver version : after update to "Driver version: 6.1.5" the RCCL tests run correctly.  

---

### 评论 #2 — sherryxiao1988 (2023-10-28T22:51:22Z)

Hi @walkup, I am experiencing the same issue. May I ask which driver are you talking about? How did you find out the driver version and how did you update it? Thanks.

---

### 评论 #3 — sherryxiao1988 (2023-10-29T05:48:25Z)

Somehow downgrading to ROCM 5.4.2 worked for me.....

---
