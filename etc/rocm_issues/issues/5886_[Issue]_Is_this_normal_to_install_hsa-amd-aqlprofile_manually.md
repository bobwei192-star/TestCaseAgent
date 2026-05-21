# [Issue]: Is this normal to install hsa-amd-aqlprofile manually

> **Issue #5886**
> **状态**: closed
> **创建时间**: 2026-01-22T18:59:30Z
> **更新时间**: 2026-02-20T20:20:49Z
> **关闭时间**: 2026-02-20T20:20:49Z
> **作者**: ye-luo
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5886

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- darren-amd

## 描述

### Problem Description

I usually install rocm as
```
apt install rocm-hip-sdk rocm-openmp-sdk amd-smi-lib rocprofiler-sdk
```
However, to get the profiler fully functional, I have to manually install `hsa-amd-aqlprofile`.
is this additional step expected?

### Operating System

24.04.3 LTS (Noble Numbat)

### CPU

AMD EPYC 7282 16-Core Processor

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.3-7.2

### ROCm Component

rocprofiler

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — darren-amd (2026-01-22T19:50:18Z)

Hi @ye-luo,

Thanks for reporting this issue! Yes, it does look like `rocprofiler-sdk` does not have `hsa-amd-aqlprofile` as an explicit dependency even though it is required. I made a PR to add it as an dependency so you'd no longer have to manually install it.

---
