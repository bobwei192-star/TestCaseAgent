# [Issue]: hipcc does not work with O0

> **Issue #2957**
> **状态**: closed
> **创建时间**: 2024-03-10T08:27:21Z
> **更新时间**: 2024-08-12T04:11:46Z
> **关闭时间**: 2024-03-17T11:11:44Z
> **作者**: noderyagever132
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2957

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

I've been trying to compile hip source code for AMD GPU RX7600 for a while now. I had some bugs in my code so I tried to compile the source code with O0 (optimization level). With the O0 optimization level - the kernel does not seem to dispatch with error code 401 (Invalid state of device - I have no clue what it means and could not find any documentation). When compiled with any other optimization level - everything seems to work fine.

I tried using the precompiled hipcc (which is installed with rocm) and even tried to compile it by myself using aomp and it doesn't work in both cases.


### Operating System

Ubunutu 20.06 LTS

### CPU

intel i5 12600

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

aomp, HIPCC

### Steps to Reproduce

Compile any code with hipcc -O0 and dispatch a kernel

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — nartmada (2024-03-11T16:28:31Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — noderyagever132 (2024-03-14T14:18:49Z)

I've narrowed down the problem a bit, still can't solve it:
https://stackoverflow.com/questions/78161172/enable-pcie-atomic-on-ubuntu-20
 

---

### 评论 #3 — noderyagever132 (2024-03-17T11:12:23Z)

The problem was atomic PCIe - I did have support on my computer but only for one pcie port - switched a port and it worked like magic.

---

### 评论 #4 — RnMss (2024-08-12T04:10:12Z)

@noderyagever132  I find '-O0' very broken. (6.0.0) I think your case worked just because you were lucky this time. For me `-O0` generate wrong results compared to `-O1` `-O2` `-O3` of hipcc and all levels including `-G` of nvcc. And 6.1.0+ is even more broken.
Because it was so broken I'm doubting that `-O0` should be used at all.

---
