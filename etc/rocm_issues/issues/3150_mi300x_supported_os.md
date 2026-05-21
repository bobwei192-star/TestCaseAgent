# mi300x supported os

> **Issue #3150**
> **状态**: closed
> **创建时间**: 2024-05-23T01:49:00Z
> **更新时间**: 2024-06-13T03:17:10Z
> **关闭时间**: 2024-06-13T03:17:10Z
> **作者**: Asyvix
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3150

## 描述

We are testing the MI300x system.

Does the MI300x support Ubuntu 22.04 with a 6.5 kernel? I am currently running it on 6.5, and it seems to be working fine with the RVS test. I am aware that the documentation states that only 5.15 is supported. Is it better to use 5.15?

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-06-12T14:14:16Z)

Hi @Asyvix, it would be best to use kernel version 5.15 as it is officially supported. Other unsupported kernels may work but could lead to compatibility issues.

---
