# [Issue]: 

> **Issue #2928**
> **状态**: closed
> **创建时间**: 2024-02-26T07:18:20Z
> **更新时间**: 2024-02-26T10:09:02Z
> **关闭时间**: 2024-02-26T10:09:02Z
> **作者**: ugcoder
> **标签**: ROCm 6.0.0, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/2928

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

Did I make the wrong choice by going with the RX7900XTX?
It took me days to be able to use tensorflow-rocm properly with gpu acceleration. I've followed the official docs for the nth time, how the hell can I get an AMD GPU to work like CUDA? What should I do?

### Operating System

22.04.1-Ubuntu(docker)

### CPU

ntel(R) Xeon(R) E5-2630 v4 (40) @ 3.10 GHz

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — ugcoder (2024-02-26T07:21:46Z)

2024-02-26 07:35:02.170205: E tensorflow/compiler/xla/stream_executor/rocm/rocm_driver.cc:302] failed call to hipInit: HIP_ERROR_InvalidDevice
2024-02-26 07:35:02.170258: I tensorflow/compiler/xla/stream_executor/rocm/rocm_diagnostics.cc:111] retrieving ROCM diagnostic information for host: e16902508cda
2024-02-26 07:35:02.170270: I tensorflow/compiler/xla/stream_executor/rocm/rocm_diagnostics.cc:118] hostname: e16902508cda
2024-02-26 07:35:02.170308: I tensorflow/compiler/xla/stream_executor/rocm/rocm_diagnostics.cc:141] librocm reported version is: NOT_FOUND: was unable to find librocm.so DSO loaded into this program
2024-02-26 07:35:02.170322: I tensorflow/compiler/xla/stream_executor/rocm/rocm_diagnostics.cc:145] kernel reported version is: UNIMPLEMENTED: kernel reported driver version not implemented

---
