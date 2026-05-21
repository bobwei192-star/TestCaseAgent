# Radeon AI PRO R9700 hangs when running Stable Diffusion 2.1 at batch sizes above 4

> **Issue #4770**
> **状态**: open
> **创建时间**: 2025-05-21T18:50:16Z
> **更新时间**: 2025-05-28T17:50:42Z
> **作者**: peterjunpark
> **标签**: Verified Issue, ROCm 6.4.1, AMD Radeon AI PRO R9700
> **URL**: https://github.com/ROCm/ROCm/issues/4770

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.1** (颜色: #aaaaaa)
- **AMD Radeon AI PRO R9700** (颜色: #007c97)

## 描述

[Radeon AI PRO R9700](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html) GPUs might hang when running [Stable Diffusion 2.1](https://huggingface.co/stabilityai/stable-diffusion-2-1) with batch sizes greater than 4. As a workaround, limit batch sizes to four or fewer. This issue will be addressed in a future ROCm release.
