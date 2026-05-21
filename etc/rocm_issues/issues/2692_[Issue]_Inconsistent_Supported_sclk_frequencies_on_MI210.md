# [Issue]: Inconsistent *Supported sclk frequencies* on MI210

> **Issue #2692**
> **状态**: closed
> **创建时间**: 2023-12-06T14:59:51Z
> **更新时间**: 2024-09-05T16:16:03Z
> **关闭时间**: 2024-08-28T15:37:39Z
> **作者**: amir-raoofy
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2692

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am observing a strange issue regarding clock frequency settings on MI210: I see different *supported sclk frequencies* depending on whether the *performance level* is set to auto (e.g., reseting the settings with `rocm_smi -r`) or manual (setting a particular frequency manually with rocm-smi --setclock sclk 0/1/2).

I see the following supported sclk frequencies after running `rocm-smi --setclock sclk 0`: level0: 500Mhz, level1: 1700Mhz
I see the following supported sclk frequencies after running `rocm_smi -r`: level0: 500Mhz, level1: 800Mhz, level2: 1700Mhz

This means that the levels are inconsistent in different modes (e.g., auto/manual) and therefore I cannot set the frequency to 800Mhz using --setclock flag, and I can only set it to 800Mhz when using -r flag!

I don't see a similar issue on MI100 with an older version of the rocm stack (5.4.3) and driver (5.16.9.22.20).



### Operating System

SLES 15-SP5

### CPU

AMD EPYC 7773X 64-Core Processor

### GPU

MI210

### ROCm Version

5.7.1

### ROCm Component

Driver version: 6.2.4

### Steps to Reproduce

rocm-smi --setclock sclk 0
rocm-smi -s
rocm-smi -r
rocm-smi -s
rocm-smi --setclock sclk 1
rocm-smi -s
rocm-smi -r
rocm-smi -s
rocm-smi --setclock sclk 2
rocm-smi -s
rocm-smi -r
rocm-smi -s


### Output of /opt/rocm/bin/rocminfo --support


[support.txt](https://github.com/RadeonOpenCompute/ROCm/files/13587454/support.txt)





---

## 评论 (4 条)

### 评论 #1 — nartmada (2023-12-13T14:23:29Z)

Hi @amir-raoofy, can you please provide the output from each rocm-smi command in your repro steps?  Just want to confirm the symptoms you are seeing.  Thanks.

---

### 评论 #2 — amir-raoofy (2023-12-13T15:27:42Z)

Sure, here is the log attached

[log.txt](https://github.com/ROCm/ROCm/files/13662499/log.txt)


---

### 评论 #3 — harkgill-amd (2024-08-21T13:32:48Z)

Hi @amir-raoofy, this discrepancy is expected. The frequencies reported in the `auto` performance level cannot be set when using the `manual` performance level. The correct way to utilize `setclk` is to

1. Set perflevel to manual using `rocm-smi --setperflevel`. You can check the current perflevel with `--showperflevel`.
2. Note the available frequencies with `rocm-smi -s`.
3. Set the frequency with `rocm-smi --setclk`

---

### 评论 #4 — amir-raoofy (2024-09-05T16:16:01Z)

Hi, 

This makes sense! So, we should explicitly set the performance level before. We missed this step since the frequencies associated with different performance levels were consistent in our older GPUs, and we extrapolated the behavior to MI210. 

This clarifies things and solves the issue. Many thanks!

---
