# [Issue]: rocm 6.1 not include gfx1103?

> **Issue #3059**
> **状态**: closed
> **创建时间**: 2024-04-23T12:19:25Z
> **更新时间**: 2024-05-23T06:55:18Z
> **关闭时间**: 2024-04-23T15:17:13Z
> **作者**: wszgrcy
> **标签**: ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/3059

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

I run command `ls /opt/rocm/lib/rocblas/library|grep 110` both native and docker(rocm 6.1). but I can't find 1103.but rocm 6.1 document mention it

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

 AMD Ryzen 7 8845HS w/ Radeon 780M Graphics

### GPU

780m
### ROCm Version

ROCm 6.1.0

### ROCm Component

ROCm

### Steps to Reproduce

ls /opt/rocm/lib/rocblas/library|grep 110

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — nartmada (2024-04-23T15:17:13Z)

@wszgrcy, gfx1103 is not supported in ROCm 6.1.0.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html


---

### 评论 #2 — wszgrcy (2024-04-23T15:19:35Z)

> @wszgrcy, gfx1103 is not supported in ROCm 6.1.0.
> 
> https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

![image](https://github.com/ROCm/ROCm/assets/9607121/154c7db3-6b2b-4725-aa2f-167a1bdc9982)
So what does this document mean by gfx1103?

---

### 评论 #3 — nartmada (2024-04-23T15:37:21Z)

@wszgrcy, please share the link of your screen capture so I can follow up with internal teams.

---

### 评论 #4 — wszgrcy (2024-04-23T15:39:07Z)

> @wszgrcy, please share the link of your screen capture so I can follow up with internal teams.

https://github.com/ROCm/ROCm/releases/tag/rocm-6.1.0

---

### 评论 #5 — kentrussell (2024-04-23T19:51:48Z)

That's for Composable Kernel, not for the entire ROCm stack. Hence it being in the Composable Kernel documentation. It doesn't say that it supports gfx1103 on the entire ROCm stack. Just that you can use Composable Kernels in gfx1103. Because they enabled support for that in their specific component. 

---

### 评论 #6 — jnolck (2024-05-20T16:17:38Z)

I just noticed that fedora rawhide has a package for rocblas-gfx1103. Haven't tested it though. Check if Ubuntu has a similar package. 

---

### 评论 #7 — NeoChen1024 (2024-05-23T06:55:17Z)

> I just noticed that fedora rawhide has a package for rocblas-gfx1103. Haven't tested it though. Check if Ubuntu has a similar package.

Ubuntu doesn't have packages similar to thoese in Fedora rawhide.

---
