# [Issue]: AMD Radeon RX 7600 performance with ROCm

> **Issue #5400**
> **状态**: closed
> **创建时间**: 2025-09-19T19:39:14Z
> **更新时间**: 2025-10-14T14:35:58Z
> **关闭时间**: 2025-10-14T14:35:58Z
> **作者**: FelipeDeAngelis
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5400

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I need to use my AMD Radeon RX 7600 to perform some model training. I am mainly using the Tensorflow library.

I am getting several errors and am unable to perform the training with my GPU.

I noticed in the Compatibility Matrix [1] that the card is not listed. I would like to know if there is a solution for using ROCm with the AMD Radeon RX 7600 graphics card?

Could you help me?

[1] https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#rdna-os-past-60

### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

MD Ryzen 5 3600 6-Core Processor

### GPU

AMD Radeon RX 7600

### ROCm Version

amdgcn-amd-amdhsa--gfx1102

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-09-23T19:32:09Z)

Hi @FelipeDeAngelis, TheRock provides ROCm wheels specifically for gfx1102 - https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx110x-dgpu.

Could you share more information regarding the tensorflow workflow you're running and the errors encountered?

---

### 评论 #2 — FR-Mister-T (2025-10-01T21:31:16Z)

I'm running some basic gen's on comfyui with rx7600xt , even if there is no offical support, it work in most common workflow, but it can be god awfully slow to work . I still don't know why VAE is so slow

<img width="1211" height="329" alt="Image" src="https://github.com/user-attachments/assets/df45f4a0-3641-4899-97db-1d4dc10a9f24" />

---

### 评论 #3 — harkgill-amd (2025-10-06T16:10:09Z)

@FR-Mister-T, can you try setting the following environment variable and then rerunning your workflow,
```
export MIOPEN_FIND_MODE=2
```
This'll set your MIOpen Find Mode to fast find which will skip searching and benchmarking different kernels in favour of falling back to an immediate mode fallback. Fast find isn't always optimal but with the default dynamic_hybrid find, naive kernels were almost exclusively getting selected leading to slow VAE decoding. Swapping find modes significantly reduced the both the VAE decode step and OOM errors on my end.

https://rocm.docs.amd.com/projects/MIOpen/en/latest/how-to/find-and-immediate.html#find-modes


---

### 评论 #4 — FR-Mister-T (2025-10-12T21:31:55Z)

Thanks you, this parameter did the trick !

---

### 评论 #5 — harkgill-amd (2025-10-14T14:35:58Z)

Glad to hear it's running better on your end :)

@FelipeDeAngelis, I'm going to close this issue out for now, but will re-open once you're able to share more information regarding your TF workflow.

---
