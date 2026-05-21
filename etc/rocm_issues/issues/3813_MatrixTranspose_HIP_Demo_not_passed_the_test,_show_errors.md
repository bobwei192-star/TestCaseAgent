# MatrixTranspose HIP Demo not passed the test, show errors

> **Issue #3813**
> **状态**: closed
> **创建时间**: 2024-09-26T04:10:49Z
> **更新时间**: 2024-09-28T00:27:14Z
> **关闭时间**: 2024-09-27T15:33:39Z
> **作者**: tauruswang
> **标签**: AMD Radeon Pro W6800, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3813

## 标签

- **AMD Radeon Pro W6800** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

MatrixTranspose HIP Demo not passed the test, show errors

### Operating System

win11 10.0.22631

### CPU

AMD Ryzen 9 6900HX with Radeon Graphics

### GPU

AMD Radeon Pro W6800

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIP

### Steps to Reproduce

install AMD-Software-PRO-Edition-24.Q3-Win10-Win11-For-HIP.exe, the
start visual studio 2022, use the template HIP MatrixTranspose demo template.
compile and run it.
<img width="1520" alt="Screenshot 2024-09-26 113318" src="https://github.com/user-attachments/assets/279ba155-1594-438d-bec5-89731a9be055">


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

GEM12 Mini PC, AMD Ryzen 9 6900HX , run HIP demo 
<img width="796" alt="Screenshot 2024-09-26 113425" src="https://github.com/user-attachments/assets/eb5e0d50-48c9-4447-a491-342a6631d4dd">
<img width="857" alt="Screenshot 2024-09-26 113759" src="https://github.com/user-attachments/assets/ba704d7d-aa58-44c3-a66a-5177aa9effb6">
<img width="1493" alt="Screenshot 2024-09-26 114352" src="https://github.com/user-attachments/assets/23f18dd2-9f5d-4f79-947c-2fd5cee0500c">
<img width="687" alt="Screenshot 2024-09-26 114441" src="https://github.com/user-attachments/assets/29ed9627-6da9-4c48-ac6a-d83f4ef14227">


### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — tauruswang (2024-09-26T04:18:33Z)

this is mini pc have no AMD Radeon Pro W6800 graphic card ...

---

### 评论 #2 — tcgu-amd (2024-09-27T15:23:45Z)

> this is mini pc have no AMD Radeon Pro W6800 graphic card ...

Hi @tauruswang , thanks for reaching out! Seems like your device only has an APU available. The HIP example you are trying to run tests for the results between CPU computed values and dGPU computed values on a supported discrete AMD Graphics device (i.e. the Radeon/Instinct series). In your case, since no physical device exists, the device-side function returns zeros, causing the assertion error. 

You can try to install the [HIP-CPU headers](https://github.com/ROCm/HIP-CPU), which should delegate the device side functions to the CPU, so you can run hip programs intended for GPU on CPU without needing to change things. Please keep in mind that HIP-CPU is not stable yet and might run into bugs.

Hope this helps!

---
