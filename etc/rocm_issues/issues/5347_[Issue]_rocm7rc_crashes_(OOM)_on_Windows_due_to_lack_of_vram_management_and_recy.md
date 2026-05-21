# [Issue]: rocm7rc crashes (OOM) on Windows due to lack of vram management and recycling mechanism

> **Issue #5347**
> **状态**: closed
> **创建时间**: 2025-09-16T16:03:00Z
> **更新时间**: 2025-09-16T19:18:38Z
> **关闭时间**: 2025-09-16T19:18:38Z
> **作者**: fangwengit04
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5347

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- darren-amd

## 描述

### Problem Description

On Windows 10 22h2, using comfyui, I installed the latest TheRock rocm+torch precompiled package as of September 16, 2025, using Python 12. After installing only rocm and torch without any parameters, I ran python main.py directly, loaded any example workflow, and clicked run. The first run was usually fine, but if you change the model or even the imported image, it will directly cause vram overflow, lag, and then the driver to drop (OOM).

comfyui has been trying to use shared vram on 9070xt instead of using only dedicated vram. I had this problem with version 0826 last month. I tried again today and the problem still exists.

Example video https://youtu.be/0j9zENuqxAA
The situations I encountered during use, flux change prompts, sdxl ControlNet change pictures and models

### Operating System

Windows 10 19045.6332

### CPU

14600kf

### GPU

9070xt

### ROCm Version

torch-2.9.0a0+rocm7.0.0rc20250909

### ROCm Component

_No response_

### Steps to Reproduce

python -m pip install --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ --pre torch torchaudio torchvision
Use this command to install Torch and Rocm.

git clone https://github.com/comfyanonymous/ComfyUI.git
cd comfyui
pip install -r requirements.txt

python main.py
Load any official example workflow, flux dev is recommended, click Generate. Then, select a model in the workflow and switch to another one (from fp16 to fp8, or fp8 to fp16). Click Run again and observe the video memory usage. It overflows immediately, and then there's a lag in the sampler stage. The driver then drops, and ComfyUI reports an OutOfMemory Error.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_
