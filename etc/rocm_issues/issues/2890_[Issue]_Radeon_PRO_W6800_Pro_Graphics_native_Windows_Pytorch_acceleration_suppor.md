# [Issue]: Radeon PRO W6800 Pro Graphics native Windows Pytorch acceleration support via ROCm / HIP or some other way?

> **Issue #2890**
> **状态**: closed
> **创建时间**: 2024-02-08T21:36:39Z
> **更新时间**: 2024-09-23T19:25:31Z
> **关闭时间**: 2024-09-23T19:25:31Z
> **作者**: AshleyT3
> **标签**: ROCm 6.0.0, ROCm 5.7.1, AMD Radeon Pro W6800
> **URL**: https://github.com/ROCm/ROCm/issues/2890

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon Pro W6800** (颜色: #ededed)

## 描述

### Problem Description

Is there a plan to eventually support Radeon PRO W6800 Pro Graphics native Windows Pytorch acceleration support via ROCm / HIP or some other way? Today, it seems Pytorch is not supported natively on Windows aside from using DirectML. DirectML is usable but in at least one case it requires customizations to pre-existing Pytorch code so does not insert GPU acceleration support seamlessly in such a case.

I've seen some online commentary about ROCm 6.1 possibly supporting native Windows ROCm / Pytorch support but it's not official AMD commentary. If there is no official public word on this, it would be great to get some FAQ or comment on this. 

### Operating System

Windows 11

### CPU

5800X

### GPU

AMD Radeon Pro W6800

### ROCm Version

ROCm 6.0.0, ROCm 5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2024-06-19T19:34:42Z)

@AshleyT3 Can you please close this ticket and open it under 'Discussions' section? Thanks!

---
