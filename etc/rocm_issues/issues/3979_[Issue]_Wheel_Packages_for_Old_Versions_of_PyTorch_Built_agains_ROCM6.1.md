# [Issue]: Wheel Packages for Old Versions of PyTorch Built agains ROCM/6.1 

> **Issue #3979**
> **状态**: closed
> **创建时间**: 2024-10-31T05:29:13Z
> **更新时间**: 2024-11-04T01:30:12Z
> **关闭时间**: 2024-11-04T01:30:12Z
> **作者**: vitduck
> **标签**: Under Investigation, ROCm 6.1.0, N/A
> **URL**: https://github.com/ROCm/ROCm/issues/3979

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.1.0** (颜色: #ededed)
- **N/A** (颜色: #ededed)

## 描述

### Problem Description

Please provide wheel packages for older versions of PyTorch, e.g. 2.1, 2,2 and 2.3 which are built against more recent ROCm 6.1. 

I would like to determine if there is performance regression with new releases of PyTorch. 
This has been observed with NVIDIA as well. 
So we would like to find best versions without relying on containers.   

### Operating System

RHEL 8

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

```
$ conda create -n torch-2.1.2 python=3.10
$ conda activate torch-2.1.2
$ pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/rocm6.1 
ERROR: Could not find a version that satisfies the requirement torch==2.1.2 (from versions: 2.4.0+rocm6.1, 2.4.1+rocm6.1, 2.5.0+rocm6.1, 2.5.1+rocm6.1)
ERROR: No matching distribution found for torch==2.1.2
```
So for ROCm-6.+, only recent 2.4+ releases are provided.  

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2024-10-31T14:11:25Z)

Hi @vitduck. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — zichguan-amd (2024-10-31T19:50:22Z)

Hi @vitduck, you can find the wheel packages on https://repo.radeon.com/rocm/manylinux/. We don't have all 2.1 to 2.3 but you can find torch 2.1 for ROCm 6.1 for example.

---

### 评论 #3 — vitduck (2024-11-04T01:28:04Z)

@ppanchad-amd @zichguan-amd 

While all versions are not covered, the versions provided by Radeon repo will suffice. 

I would like to close the issue.  
Thanks very much for your help. 

---
