# [Issue]: Downloading ROCm packages from Peru (South America) is extremely slow, making installation take 2+ days instead of minutes.

> **Issue #5919**
> **状态**: open
> **创建时间**: 2026-01-30T23:03:00Z
> **更新时间**: 2026-02-06T19:26:57Z
> **作者**: JPachecoZ
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5919

## 描述

### Problem Description

Downloading ROCm packages from Peru (South America) is extremely slow, making installation take 2+ days instead of minutes.

I suspect there are very few ROCm users in LATAM, so no local CDN replica exists. As AMD GPUs gain popularity for local AI inference, this will become a bigger barrier for adoption in the region.

### Operating System

Ubuntu 25.10

### CPU

AMD Ryzen 5 2600

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

7.2

### ROCm Component

_No response_

### Steps to Reproduce

1. Run `sudo amdgpu-install -y --usecase=graphics,rocm`
2. Observe download speeds of 50-70 KB/s for large packages like `composablekernel-dev`


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — iqoptionizator (2026-02-06T19:24:41Z)

i have issue with download, extremally slow(( 
from RU 2KB/s 

---
