# [DOCS: Typo in the RHEL repository generator

> **Issue #2764**
> **状态**: closed
> **创建时间**: 2023-12-21T14:51:39Z
> **更新时间**: 2024-01-17T07:54:39Z
> **关闭时间**: 2024-01-17T04:40:15Z
> **作者**: lordrip
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2764

## 描述

### Problem Description

There's a typo in the RHEL repositories, it shows `...thel/...` and it should be `...rhel/...`

Related page:
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/rhel.html#register-rocm-packages

See the following snapshot
![image](https://github.com/ROCm/ROCm/assets/16512618/0db09fd4-bfba-46bc-976e-7cb4f294b837)


### Operating System

Red Hat Enterprise Linux

### CPU

AMD Ryzen 7 5800X

### GPU

Other

### Other

RX 7800XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

Other

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — lordrip (2023-12-21T14:52:21Z)

I tried to submit a fix for this but it looks like the either the repository is private or the link is wrong :smiley: 

---

### 评论 #2 — nartmada (2024-01-17T04:40:15Z)

The issue has been fixed.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/rhel.html#register-rocm-packages
![image](https://github.com/ROCm/ROCm/assets/144284448/8aab931b-c6ce-4cb8-8bcf-bdced7d95fcd)
![image](https://github.com/ROCm/ROCm/assets/144284448/adc5c889-9dfa-4d36-ad95-080463c91ed3)



---

### 评论 #3 — lordrip (2024-01-17T07:54:38Z)

Thanks a lot 🙏  @nartmada 

---
