# [Issue]: Low performance in llama.cpp mmf mul_mat_f on 9070XT

> **Issue #5727**
> **状态**: closed
> **创建时间**: 2025-12-01T03:44:32Z
> **更新时间**: 2025-12-12T18:10:43Z
> **关闭时间**: 2025-12-12T18:10:43Z
> **作者**: zhang-hui-yulo
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5727

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

ROCm compiler doesn't generate the code with good enough performance for 9070XT, the performance of "MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],k_v=0,o=1)" is 3.1 tflops, I need use some weird code to force compiler to unroll more codes then the performance becomes to 4.95 tflops.

This will reduce the performance of dense model like deepseek R1 about 30%.

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 7900X3D 12-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 7.1.1

### ROCm Component

HIP

### Steps to Reproduce

llama.cpp version
```
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
git checkout ff90508
```

build command
```
cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1201 -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=OFF -DGGML_HIP_ROCWMMA_FATTN=ON
cmake --build build -j
```

run command
```
./build/bin/test-backend-ops perf -o "MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],k_v=0,o=1)"
```

the original output, the performance is 3.09 tflops
```
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon RX 9070 XT, gfx1201 (0x1201), VMM: no, Wave Size: 32
Testing 2 devices

Backend 1/2: ROCm0
  Device description: AMD Radeon RX 9070 XT
  Device memory: 16304 MB (16238 MB free)

  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],k_v=0,o=1):                 3317 runs -   303.79 us/run - 939.52 MFLOP/run -   3.09 TFLOPS
  Backend ROCm0: OK
Backend 2/2: CPU
  Skipping CPU backend
2/2 backends passed
OK
```

Use this attached [mmf.zip](https://github.com/user-attachments/files/23844560/mmf.zip) to replace the original one, then recompile the code and rerun the command.

The output after patch, the performance becomes to 4.94 tflops
```
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon RX 9070 XT, gfx1201 (0x1201), VMM: no, Wave Size: 32
Testing 2 devices

Backend 1/2: ROCm0
  Device description: AMD Radeon RX 9070 XT
  Device memory: 16304 MB (16238 MB free)

  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],k_v=0,o=1):                 5350 runs -   190.37 us/run - 939.52 MFLOP/run -   4.94 TFLOPS
  Backend ROCm0: OK
Backend 2/2: CPU
  Skipping CPU backend
2/2 backends passed
OK
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — zhang-hui-yulo (2025-12-01T04:41:41Z)

cc @JohannesGaessler

---

### 评论 #2 — tcgu-amd (2025-12-02T16:55:07Z)

Hi @zhang-hui-yulo, thanks for reaching out! We will look in to this shortly.

---

### 评论 #3 — tcgu-amd (2025-12-03T18:11:31Z)

Hi @zhang-hui-yulo, I took a look at your patch. First of all, awesome work increasing the performance by up 60%! However, a bit of clarifications might be helpful. When you said that it doesn't generate "good enough" performance for 9070XT, did you have a frame of reference to compare with (e.g. with 7000 cards or nividia cards)? Also, when you mentioned "This will reduce the performance of dense model like deepseek R1 about 30%.", did you mean the patch you added reduces the performance by 30%, or that that without the patch the performance is lowered by 30%? Can you provide the exact workload/test configurations you used? 

On a side note, please keep in mind that the compiler needs to consider a wide range of scenarios which oftentimes will mean the default heuristics might be conservative, that's why application specific optimizations are often necessary. Your code seems to work by forcing the compiler to allocate more registers, which could explain the increased performance. This is certainly a great hack, but might not necessarily indicate a bug in the compiler. Thanks! 

---

### 评论 #4 — zhang-hui-yulo (2025-12-04T03:00:34Z)

> Hi [@zhang-hui-yulo](https://github.com/zhang-hui-yulo), I took a look at your patch. First of all, awesome work increasing the performance by up 60%! However, a bit of clarifications might be helpful. When you said that it doesn't generate "good enough" performance for 9070XT, did you have a frame of reference to compare with (e.g. with 7000 cards or nividia cards)? Also, when you mentioned "This will reduce the performance of dense model like deepseek R1 about 30%.", did you mean the patch you added reduces the performance by 30%, or that that without the patch the performance is lowered by 30%? Can you provide the exact workload/test configurations you used?
> 
> On a side note, please keep in mind that the compiler needs to consider a wide range of scenarios which oftentimes will mean the default heuristics might be conservative, that's why application specific optimizations are often necessary. Your code seems to work by forcing the compiler to allocate more registers, which could explain the increased performance. This is certainly a great hack, but might not necessarily indicate a bug in the compiler. Thanks!

Hello, can you reproduce it? For the perf data, you can have a check on this https://github.com/ggml-org/llama.cpp/pull/17437, mul_mat_f is about 25~30% slower than hipblas on 9070XT, but it's way faster than hipblas on 9060. Also, this hack will cause code crash on 9060, so I didn't dear to merge it into the repo as I don't know if it will crash on specific rocm version.

mul_mat_f actually works quite well on NVIDIA GPUs and can earn at least 20% perf improvement, so this is why I said rocm compiler cannot generate better code.

Anyway, the decision belongs to you, I will be very apricated if you can fix it as it doesn't make sense that enable mul_mat_f on 9060 but disable it on 9070, thank you.

---

### 评论 #5 — zhang-hui-yulo (2025-12-04T07:50:15Z)

Hello @tcgu-amd , if you could provide a safe way to let compiler to generate higher perf version of mul_mat_f, that would also be a good choice, the thing to prevent to merge it into llama.cpp repo is unknown bad code from compiler. Thank you.

---

### 评论 #6 — kyuz0 (2025-12-07T10:42:02Z)

I've applied this patch and tested it on AMD R9700 AI Pro, the container to look for if `rocm-7.1.1-mmf`:

https://kyuz0.github.io/amd-r9700-ai-toolboxes/

I cannot see an increase in performance and this crashed on a few models unfortunately.

---

### 评论 #7 — tcgu-amd (2025-12-12T18:10:43Z)

Hi @zhang-hui-yulo, after some discussions, your proposed change does not seem appropriate for the compiler at this time given the performance benefit does not seem to be super obvious and the potential instability it could introduce. As a platform we must prioritize stability in a broader application scope, so even exposing an API option that can jeopardize this would not be the best idea. I will be closing this issue as a will not fix for now, but please feel free to continue to follow up if you require additional assistance. Thanks. 

---
