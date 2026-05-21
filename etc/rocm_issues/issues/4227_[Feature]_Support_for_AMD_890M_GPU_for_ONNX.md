# [Feature]: Support for AMD 890M GPU for ONNX

> **Issue #4227**
> **状态**: closed
> **创建时间**: 2025-01-06T12:06:34Z
> **更新时间**: 2025-02-10T11:51:52Z
> **关闭时间**: 2025-02-10T11:51:52Z
> **作者**: zydjohnHotmail
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4227

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Hi, I have a new PC with AMD Ryzen AI 9 HX 370 with 890M GPU.
I have installed HIP SDK 6.2.  And I can see the architecture:
C:\Program Files\AMD\ROCm\6.2\bin>.\amdgpu-arch.exe
gfx1150
Since I am using ONNX to run many language models, but since I can only use CPU, the inference performance is very bad.  And I can't find good document on how to use AMD GPU for Windows.  The latest document seems only support GPU in Linux, but I am using Windows 11.
Please show me some instructions on how to enable GPU in ONNX for Windows.
Thanks,

### Operating System

Windows 11

### GPU

M890

### ROCm Component

ONNX with AMD GPU support

---

## 评论 (3 条)

### 评论 #1 — alert101 (2025-01-10T07:13:56Z)

+1 for RDNA 3.5 support.

I'm planning on getting one of the recently announced Ryzen AI MAX APUs and it would be great to be able to use it locally for training models.

---

### 评论 #2 — harkgill-amd (2025-01-27T21:14:32Z)

Hi @zydjohnHotmail, please see the following documentation on how to use ONNX with DirectML on Windows for your AMD Ryzen AI 9 HX 370, [DirectML Flow](https://ryzenai.docs.amd.com/en/latest/gpu/ryzenai_gpu.html). You can also follow the [Ryzen™ AI iGPU Example](https://github.com/amd/RyzenAI-SW/tree/main/example/iGPU/getting_started#getting-started-with-igpu) for a more hands-on sample of the Olive -> ONNX -> DirectML workflow.

---

### 评论 #3 — barberben (2025-02-10T00:27:21Z)

For AMD gfx1150 support you may check
[https://github.com/likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU](https://github.com/likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU)

---
