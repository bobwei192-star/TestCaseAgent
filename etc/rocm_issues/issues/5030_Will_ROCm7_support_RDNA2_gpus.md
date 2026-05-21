# Will ROCm7 support RDNA2 gpus?

> **Issue #5030**
> **状态**: closed
> **创建时间**: 2025-07-10T16:42:18Z
> **更新时间**: 2025-07-15T03:03:36Z
> **关闭时间**: 2025-07-15T03:03:15Z
> **作者**: rez3vil
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5030

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Pretty much the title. Will it support windows or WSL? I am only asking for runtime support, not HIP SDK.

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2025-07-11T14:26:39Z)

Hi @rez3vil, RDNA2 support on Windows includes both the HIP runtime and SDK as highlighted on our [System Requirements](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html#windows-supported-gpus-and-apus) page. 

Unfortunately, these GPUs are not currently supported on WSL and likely won't be for the initial WSL release of ROCm 7. However, we’re continually working to expand support, so this may change in the future. In the meantime, users can consider using [TheRock](https://github.com/ROCm/TheRock), which enables building ROCm/HIP on native Windows with RDNA2 support. 

---

### 评论 #2 — rez3vil (2025-07-12T02:26:35Z)

> Hi [@rez3vil](https://github.com/rez3vil), RDNA2 support on Windows includes both the HIP runtime and SDK as highlighted on our [System Requirements](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html#windows-supported-gpus-and-apus) page.
> 
> Unfortunately, these GPUs are not currently supported on WSL and likely won't be for the initial WSL release of ROCm 7. However, we’re continually working to expand support, so this may change in the future. In the meantime, users can consider using [TheRock](https://github.com/ROCm/TheRock), which enables building ROCm/HIP on native Windows with RDNA2 support.

Hi, thank you for response. My specific query was for RX 6700s. I couldn't figure out the LLVM target from the system requirement. Is it gfx1031 or gfx1032. I couldn't find specific website on amd regarding the same.

---

### 评论 #3 — harkgill-amd (2025-07-14T15:51:11Z)

The RX6700S is `gfx1032`. We do have the [Accelerator and GPU hardware specifications](https://rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html#accelerator-and-gpu-hardware-specifications) table that highlights LLVM target names though it doesn't include mobile chips.

---

### 评论 #4 — rez3vil (2025-07-15T03:03:15Z)

Thank you for clarifying. I'll give TheRock shot.

---
