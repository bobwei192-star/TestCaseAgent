# [OMP] hipcc won't define _OPENMP macro

> **Issue #2186**
> **状态**: closed
> **创建时间**: 2023-05-29T03:55:05Z
> **更新时间**: 2024-11-01T03:39:54Z
> **关闭时间**: 2024-11-01T03:39:53Z
> **作者**: dipietrantonio
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2186

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- david-salinas

## 描述

Dear developers, the `hipcc` compiler driver won't define the `_OPENMP` macro when the `-fopenmp` option is specified. The macro will be defined only when GPU offloading is requested. This can cause issues during the CMake configuration step when testing for OpenMP availability.

ROCm versions: 5.0.2, 5.4.3

How to reproduce:

```
$ cat test.cpp 
#ifndef _OPENMP
#error NO OPENMP defined
#endif

int main () {}
$ hipcc -fopenmp test.cpp 
test.cpp:2:2: error: NO OPENMP defined
#error NO OPENMP defined
 ^
1 error generated when compiling for gfx90a.
$ clang -fopenmp test.cpp 
$ # success 
$ hipcc -fopenmp -target x86_64-pc-linux-gnu -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a test.cpp 
$ # success
```
Is this the intended behaviour?

Thank you

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2024-05-13T17:44:14Z)

@dipietrantonio Apologies for the lack response.  Do you still need assistance with this ticket? Thanks!

---

### 评论 #2 — dipietrantonio (2024-05-15T04:08:38Z)

Hi @ppanchad-amd,

the error is still present in rocm/5.7.3, I cannot test for later versions yet but I suspect it is still there. I believe this should be fixed as soon as possible.

---

### 评论 #3 — harkgill-amd (2024-07-15T20:39:42Z)

Hi @dipietrantonio, this is the intended behaviour as OpenMP is not enabled for the GPU. A simple workaround for this issue is to guard the OpenMP code from entering the GPU compilation as shown below:

```
#ifndef __HIP_DEVICE_COMPILE__
#ifndef _OPENMP
#error NO OPENMP defined
#endif
#endif
```
This will prevent the `#ifndef _OPENMP #error NO OPENMP defined` assertation from throwing an error.

---

### 评论 #4 — dipietrantonio (2024-07-18T06:33:11Z)

hi @harkgill-amd I will do some experimenting and will get back to you. I had issues because I was using OpenMP but for CPU parallelisation in other parts of the code. One can still use OpenMP together with HIP..

---

### 评论 #5 — harkgill-amd (2024-09-23T20:06:03Z)

Hi @dipietrantonio, any updates on this?

---

### 评论 #6 — dipietrantonio (2024-09-24T22:17:41Z)

Hi @harkgill-amd, thanks for your patience. I think there has been a misunderstanding.

I am currently working on a library that has a CPU and GPU implementation for every numerical algorithm. I want them to coexist together. I am using OpenMP for CPU parallelisation and HIP to offload to GPU. I am NOT using OpenMP offloading features.

This setup works, meaning that `hipcc` is happy to translate OpenMP macros to appropriate parallelisation functions and to compile HIP code in the same object file. And the code runs fine. I suppose `hipcc` offloads (pun not intended) OpenMP support to `clang`. 

My problem is only with the `_OPENMP` macro. Because I give the option to the user whether to compile with OpenMP or not,  I would like the macro to be defined when I pass `-fopenmp`.  To recap, OpenMP CPU + HIP works fine, I just need `hipcc` to define the macro.

---

### 评论 #7 — zichguan-amd (2024-10-29T14:53:20Z)

Hi @dipietrantonio, if all you need is to have `_OPENMP` defined, the compiler already does that. You can verify it with 
```
$ echo | hipcc -fopenmp -dM -E - | grep OPENMP
#define _OPENMP 202011
```
The error only happens during compilation because the compiler compiles the source code in separate passes for CPU and GPU, and openmp is not enabled for GPU, therefore it fails at the GPU pass. The previous suggestion guards the error exactly from it. You can use the macro for CPU at runtime with no problem.

---

### 评论 #8 — dipietrantonio (2024-11-01T03:39:53Z)

Hi @zichguan-amd , @harkgill-amd thank you both for your explanation, considering the two passes now it makes sense to me.



---
