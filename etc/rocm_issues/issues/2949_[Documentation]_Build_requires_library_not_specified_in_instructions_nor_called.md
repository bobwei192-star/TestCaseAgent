# [Documentation]: Build requires library not specified in instructions nor called out when failure occurs

> **Issue #2949**
> **状态**: closed
> **创建时间**: 2024-03-06T17:37:40Z
> **更新时间**: 2025-07-21T15:09:55Z
> **关闭时间**: 2025-07-21T15:09:55Z
> **作者**: seraasch
> **标签**: Under Investigation, Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2949

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/ubuntu.html

The current version requires an additional C++ library which is used when building the dynamic library locally:

add:  "sudo apt-get install libstdc++-12-dev" to instructions

Found at:  https://github.com/ROCm/ROCm/issues/2031

### Attach any links, screenshots, or additional evidence you think will be helpful.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/ubuntu.html

https://github.com/ROCm/ROCm/issues/2031

---

## 评论 (4 条)

### 评论 #1 — nartmada (2024-03-07T05:10:00Z)

Internal ticket has been created for this issue.

---

### 评论 #2 — al42and (2024-03-08T18:47:20Z)

FWIW, a similar problem occurs on RHEL-like systems

---

### 评论 #3 — JackAKirk (2024-05-10T13:59:13Z)

Is there any expectation that gcc11 will be supported at some point on 22.04 for rocm? This is the default version of gcc for 22.04 after all.

---

### 评论 #4 — harkgill-amd (2025-07-21T15:09:55Z)

The version of `libstdc++` required is dependent on your system's installed `gcc` version as explained here https://github.com/ROCm/ROCm/issues/1843#issuecomment-1813746898. 

We have updated our FAQ to better outline the `libstdc++` requirement - [Issue #4: C++ libraries
](https://github.com/ROCm/rocm-install-on-linux/blob/develop/docs/reference/install-faq.rst#issue-4-c-libraries)

---
