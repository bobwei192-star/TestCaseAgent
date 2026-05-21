# Missed synchronization between kernel completion and subsequent dependent data transfer results in an error 

> **Issue #2616**
> **状态**: closed
> **创建时间**: 2023-10-31T15:14:10Z
> **更新时间**: 2025-05-29T16:03:45Z
> **关闭时间**: 2025-05-29T15:31:40Z
> **作者**: Rmalavally
> **标签**: Under Investigation, 5.7.0, 5.7.1, OpenMP (ROCm)
> **URL**: https://github.com/ROCm/ROCm/issues/2616

## 标签

- **Under Investigation** (颜色: #0052cc)
- **5.7.0** (颜色: #fef2c0)
- **5.7.1** (颜色: #b60205)
- **OpenMP (ROCm)** (颜色: #f9d0c4)

## 描述

### Missed synchronization between kernel completion and subsequent dependent data transfer results in an error

ROCm OpenMP 5.7.1 and earlier may result in a randomly appearing defect that is observable as target regions computing wrong answer/results. This is due to a missed synchronization between kernel completion and subsequent dependent data transfer.
 
If this behavior is observed, run the application with the following environment variable set:

HSA_ENABLE_SDMA=0

**Note:** Performance impact may be observed when the above environment variable is used.

### Operating System

Ubuntu 22.04 with AMDGPU 6.2.4 driver

### CPU

AMD EPYC 7A53 64-Core Processor, AMD EPYC 7313 16-Core Processor, and others

### GPU

MI200, MI100, Radeon Pro W6800

### ROCm Version

ROCm 5.7.0, 5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### Output of /opt/rocm/bin/rocminfo --support

NA

---

## 评论 (4 条)

### 评论 #1 — prckent (2023-12-20T18:50:32Z)

Can you please confirm if this still exists in 6.0? If it was fixed, where was the fix made?


---

### 评论 #2 — jplehr (2024-02-15T10:34:59Z)

Only from looking at what I believe are symptoms of this, this issue still exists in ROCm 6.0.0 and ROCm 6.0.2 (amdgpu driver version 6.3.6).
Without the mentioned mitigation, we see spurious fails on OpenMP tests. These fails go away when we use `HSA_ENABLE_SDMA=0`.

---

### 评论 #3 — ppanchad-amd (2025-05-29T15:31:40Z)

Fixed as of ROCm 6.3. Closing ticket.

---

### 评论 #4 — prckent (2025-05-29T16:03:44Z)

FYI, confirming here that we see this as fixed in QMCPACK (OpenMP, HIP, multithreaded offload). We no longer need to use HSA_ENABLE_SDMA=0.


---
