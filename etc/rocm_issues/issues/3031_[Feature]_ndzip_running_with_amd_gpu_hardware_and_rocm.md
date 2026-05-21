# [Feature]: ndzip running with amd gpu hardware and rocm?

> **Issue #3031**
> **状态**: closed
> **创建时间**: 2024-04-17T14:39:48Z
> **更新时间**: 2025-07-08T14:24:30Z
> **关闭时间**: 2025-07-08T14:24:29Z
> **作者**: stefano2734
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3031

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

NDzip is a fast zip implementation to GPU.
With fast pci ssd cpu is often not fast enough. 
with GPU 75 GB/s are possible in compression and decompression.

Ndzip better than NVIDIA nvCOMP. nvCOMP is closed source with version 2.3 and higher.

Is ndzip running on amd gpu? Or is something to do by amd ROCm?

See 
https://github.com/celerity/ndzip
https://dps.uibk.ac.at/~fabian/slides/2021-sc21-ndzip-gpu-efficient-lossless-compression-of-scientific-floating-point-data-on-gpus.pdf
https://dps.uibk.ac.at/~fabian/publications/2021-ndzip-gpu-efficient-lossless-compression-of-scientific-floating-point-data-on-gpus.pdf

https://github.com/NVIDIA/nvcomp
https://developer.nvidia.com/blog/accelerating-lossless-gpu-compression-with-new-flexible-interfaces-in-nvidia-nvcomp/
https://developer.nvidia.com/nvcomp




### Operating System

_No response_

### GPU

_No response_

### ROCm Component

where is ROCm gpu Compression tool like rocmZIP?

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-06-25T20:30:07Z)

Hi @stefano2734, please see https://github.com/ROCm/hipCOMP-core which is a port based on nvCOMP.

---

### 评论 #2 — harkgill-amd (2025-07-08T14:24:30Z)

Closing this issue out for now but feel free to leave a comment if you have any questions.

---
