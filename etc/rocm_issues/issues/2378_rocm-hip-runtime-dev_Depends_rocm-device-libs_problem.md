# rocm-hip-runtime-dev : Depends: rocm-device-libs problem

> **Issue #2378**
> **状态**: closed
> **创建时间**: 2023-08-14T09:18:50Z
> **更新时间**: 2024-01-25T09:11:19Z
> **关闭时间**: 2024-01-25T09:11:19Z
> **作者**: habernir
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2378

## 描述

i try to install sudo amdgpu-install --usecase=rocm in ubuntu 22.04 (version 5.6.0)
but i get this


The following packages have unmet dependencies:
 rocm-hip-runtime-dev : Depends: rocm-device-libs (= 1.0.0.50600-67~22.04) but 5.0.0-1 is to be installed
 rocm-openmp-sdk : Depends: rocm-device-libs (= 1.0.0.50600-67~22.04) but 5.0.0-1 is to be installed
E: Unable to correct problems, you have held broken packages.
habernir@nirUbuntu:~/Documents$ 




thanks 
nir


---

## 评论 (2 条)

### 评论 #1 — pramenku (2023-10-24T09:30:56Z)

@habernir  Can you try again. I tried and it works.
You can try latest 5.7.1 or 5.6.0 itself

---

### 评论 #2 — nartmada (2024-01-25T02:34:29Z)

Hi @habernir, do you still see this issue with latest ROCm 6.0.0?  If not, please close the ticket.  Thanks. 

---
