# How to compile the rocm version of aarch64?

> **Issue #4405**
> **状态**: closed
> **创建时间**: 2025-02-21T03:47:41Z
> **更新时间**: 2025-05-08T10:51:14Z
> **关闭时间**: 2025-02-21T15:49:07Z
> **作者**: mulinhu
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4405

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

How to compile the rocm version of aarch64?

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-02-21T14:32:14Z)

Hi @mulinhu. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-02-21T15:49:07Z)

Hi @mulinhu, ROCm does not support AArch64 (or any ARM architecture for that matter) at this time and we have no plans in the short term for this that I'm aware of.

---

### 评论 #3 — mulinhu (2025-03-27T09:32:11Z)

Thank you very much !!!

---

### 评论 #4 — timohyva (2025-05-07T19:21:32Z)

> Hi [@mulinhu](https://github.com/mulinhu), ROCm does not support AArch64 (or any ARM architecture for that matter) at this time and we have no plans in the short term for this that I'm aware of.

Thank you for @schung-amd 's answer. However I found this rather bit confusing after I read this quote:

"In addition, based on **AMD ROCm™ software**, an open-source AI/HPC software stack for GPUs, and **Fujitsu’s Arm-based FUJITSU-MONAKA software**, Fujitsu and AMD will enhance their collaboration with the open-source community. Both companies seek to advance the development of open-source AI software that is optimized for the AI computing platforms they will provide, and work to expand the ecosystem."

from AMD's article release: https://www.amd.com/en/newsroom/press-releases/2024-11-01-amd-and-fujitsu-to-begin-strategic-partnership-to-develop-more-s.html

If I understand right, this release means AMD has project on letting ROCm works on Fujitsu's ARM CPU, right?

---

### 评论 #5 — schung-amd (2025-05-07T21:14:13Z)

@timohyva Good catch, although that announcement isn't specific about what form the collaboration will take and I wouldn't say 2027 is short-term; regardless, until more details are officially revealed I don't have anything to share on the matter (other than that ARM support is on our radar).

---

### 评论 #6 — timohyva (2025-05-08T10:51:13Z)

> [@timohyva](https://github.com/timohyva) Good catch, although that announcement isn't specific about what form the collaboration will take and I wouldn't say 2027 is short-term; regardless, until more details are officially revealed I don't have anything to share on the matter (other than that ARM support is on our radar).

Hi, @schung-amd , thank you for clarifying. My naive guess of collaboration may be supporting Fujitsu ARM as host on AMD GPUs. 

---
