# [Issue]: [ROCm][Windows] NotImplementedError for FP8 (e4m3fn) operators on RDNA4 (Navi 48) GPUs

> **Issue #6019**
> **状态**: closed
> **创建时间**: 2026-03-05T05:35:01Z
> **更新时间**: 2026-04-22T14:01:05Z
> **关闭时间**: 2026-03-12T14:29:58Z
> **作者**: amd-fangchou
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6019

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

While official documentation for RDNA4 (Navi 48) and PyTorch on Windows states that FP8 (E5M2, E4M3) is supported, basic Eager-mode operators such as torch.mm and torch.mul throw a NotImplementedError. This suggests that the dispatching logic or the necessary ROCm/hipBLAS kernels are missing or not correctly linked for the Windows ROCm build.


### Operating System

Microsoft Windows 11 Pro (10.0.26200 64-bit)

### CPU

12th Gen Intel(R) Core(TM) i5-12400

### GPU

AMD Radeon AI PRO R9700 (gfx1201)

### ROCm Version

ROCm7.11

### ROCm Component

_No response_

### Steps to Reproduce

import torch
a = torch.ones((512,512), dtype=torch.float8_e4m3fn).cuda()
b = torch.ones((512,512), dtype=torch.float8_e4m3fn).cuda()
a
tensor([[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.],
...,
[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.]], device='cuda:0',
dtype=torch.float8_e4m3fn)
b
tensor([[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.],
...,
[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.],
[1., 1., 1., ..., 1., 1., 1.]], device='cuda:0',
dtype=torch.float8_e4m3fn)
c = torch.mm(a,b)
Traceback (most recent call last):
File "", line 1, in
NotImplementedError: "addmm_cuda" not implemented for 'Float8_e4m3fn'
d = torch.mul(a,b)
Traceback (most recent call last):
File "", line 1, in
NotImplementedError: "mul_cuda" not implemented for 'Float8_e4m3fn'

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

PyTorch version: 2.9.1+rocmsdk20260116
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 7.2.26024-f6f897bd3d

OS: Microsoft Windows 11 Pro (10.0.26200 64-bit)
GCC version: Could not collect
Clang version: Could not collect
CMake version: version 4.2.1
Libc version: N/A

Python version: 3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:05:38) [MSC v.1929 64 bit (AMD64)] (64-bit runtime)
Python platform: Windows-11-10.0.26200-SP0
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to:
GPU models and configuration: AMD Radeon AI PRO R9700 (gfx1201)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
Is XPU available: False
HIP runtime version: 7.2.26024
MIOpen runtime version: 3.5.1
Is XNNPACK available: True

Versions of relevant libraries:
[pip3] numpy==2.4.1
[pip3] torch==2.9.1+rocmsdk20260116
[pip3] torchaudio==2.9.1+rocmsdk20260116
[pip3] torchvision==0.24.1+rocmsdk20260116
[conda] numpy 2.4.1 pypi_0 pypi
[conda] torch 2.9.1+rocmsdk20260116 pypi_0 pypi
[conda] torchaudio 2.9.1+rocmsdk20260116 pypi_0 pypi
[conda] torchvision 0.24.1+rocmsdk20260116 pypi_0 pypi

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — schung-amd (2026-03-05T15:30:58Z)

Hi @amd-fangchou, the regular matmul operation isn't supported in torch for those types, you have to use scaled matmul instead; see https://github.com/pytorch/pytorch/issues/107087, https://github.com/pytorch/pytorch/issues/123761.

---

### 评论 #2 — amd-fangchou (2026-03-10T09:21:22Z)

Hi @schung-amd 

Thank you for the guidance. I've tested the FP8 workflows on Navi 48 under Windows. I can confirm that the float8_e4m3fnuz dtype exists and casting works (e.g., generating random data in FP16 and then casting to FP8 using .to()). However, I encountered the following blockers when trying to use or compute with these tensors:

**Scaled Matmul Failure:** When performing torch._scaled_mm with the manually casted FP8 tensors, it fails with:
RuntimeError: CUDA error: HIPBLAS_STATUS_NOT_SUPPORTED when calling hipblaslt_status_to_torch_status(status)
This suggests hipBLASLt on Windows does not yet support FP8 kernels for the RDNA4 architecture.

**Basic Operators Missing:** Even basic reduction like a_fp8.sum() results in:
NotImplementedError: "sum_cuda" not implemented for 'Float8_e4m3fnuz'.

**Environment Details:**
OS: Windows
Hardware: Navi 48 (RDNA4)
PyTorch Version: 

- torch==2.11.0a0+rocm7.12.0a20260213
- torchaudio==2.11.0a0+rocm7.12.0a20260224
- torchvision==0.25.0a0+rocm7.12.0a20260205

ROCm Version: 

- rocm==7.12.0a20260213
- rocm-sdk-core==7.12.0a20260213
- rocm-sdk-libraries-gfx120X-all==7.12.0a20260213

Is this expected for the Windows ROCm stack at this stage? Is there any specific branch or environment variable I should use to enable RDNA4 FP8 compute support?

**Below is the script I used** 
```
import torch

device = "cuda"

a_hp = torch.randn(512, 512, device=device, dtype=torch.float16)
b_hp = torch.randn(512, 512, device=device, dtype=torch.float16)

a_fp8 = a_hp.to(torch.float8_e4m3fnuz)
b_fp8 = b_hp.to(torch.float8_e4m3fnuz)

scale_a = torch.tensor([1.0], device=device, dtype=torch.float32)
scale_b = torch.tensor([1.0], device=device, dtype=torch.float32)

try:
    output, _ = torch._scaled_mm(
        a_fp8, 
        b_fp8.t(), 
        scale_a=scale_a, 
        scale_b=scale_b, 
        out_dtype=torch.float16
    )
    print("✅ Navi 48 FP8 scaled_mm works")
    print(f"Output shape: {output.shape}, type: {output.dtype}")
except Exception as e:
    print(f"❌ Fail: {e}")
```

Test result

<img width="1042" height="70" alt="Image" src="https://github.com/user-attachments/assets/5b7369d3-2d50-4817-979c-a3a6a308634a" />


---

### 评论 #3 — schung-amd (2026-03-10T15:53:37Z)

I'll look into the scaled matmul failure on RDNA4. As for the `NotImplementedError`, AFAIU that is a lack of support on the pytorch side for the datatype. If you do see docs or examples of one of those missing ops working on other hardware, I'll be happy to look into it.

---

### 评论 #4 — schung-amd (2026-03-10T20:49:08Z)

Your reproducer runs fine with `float8_e4m3fn`, so it looks like there isn't support for `e4m3fnuz` on RDNA4. According to https://rocm.docs.amd.com/projects/hipBLASLt/en/latest/reference/data-type-support.html,

>The hipblaslt_f8_fnuz and hipblaslt_bf8_fnuz data types are only supported on the gfx942 platform. The hipblaslt_f8 and hipblaslt_bf8 data types are only supported on the gfx950 and gfx12 platforms.


---

### 评论 #5 — amd-fangchou (2026-03-11T06:09:37Z)

Hi @schung-amd,

Thank you for the clarification. You were correct, float8_e4m3fnuz is indeed unsupported on Navi 48 (RDNA4) in my current environment, but switching to torch.float8_e4m3fn and torch.float8_e5m2 worked perfectly with scaled mm

---

### 评论 #6 — schung-amd (2026-03-11T18:37:49Z)

Great, glad to hear it's working for you. Any other guidance or clarifications needed here?

---

### 评论 #7 — amd-fangchou (2026-03-12T04:56:19Z)

Hi @schung-amd,

No further questions from my side. Thanks for the clarification

---

### 评论 #8 — schung-amd (2026-03-12T14:29:58Z)

Closing for now then, feel free to comment if you run into further issues on this topic and we can reopen if necessary.

---

### 评论 #9 — roytan883 (2026-04-22T12:02:40Z)

> Hi [@schung-amd](https://github.com/schung-amd),
> 
> Thank you for the clarification. You were correct, float8_e4m3fnuz is indeed unsupported on Navi 48 (RDNA4) in my current environment, but switching to torch.float8_e4m3fn and torch.float8_e5m2 worked perfectly with scaled mm

@amd-fangchou @schung-amd 
BUT `c = torch.mm(a,b)` still not work. I got error: NotImplementedError: "addmm_cuda" not implemented for 'Float8_e4m3fn' on Radeon RX 9000 GPU.

---

### 评论 #10 — schung-amd (2026-04-22T14:01:05Z)

@roytan883 As described above pytorch itself does not have support for the normal mm with these datatypes. You need to use scaled_mm instead for FP8.

---
