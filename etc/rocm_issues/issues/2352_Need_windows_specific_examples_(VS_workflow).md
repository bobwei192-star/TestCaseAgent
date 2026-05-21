# Need windows specific examples (VS workflow?)

> **Issue #2352**
> **状态**: open
> **创建时间**: 2023-07-29T13:21:55Z
> **更新时间**: 2023-08-24T13:47:28Z
> **作者**: gbeatty
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2352

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

With the release of HIP SDK for windows, it would be nice to see some (any) windows specific examples. Everything out there is make/cmake based. Great for existing cmake projects or new projects that can choose to use cmake. But, what about direct integration with existing Visual Studio projects. CUDA Toolkit installation automatically configures visual studio to use the nvcc compiler to build .cu files seamlessly. All the HIP examples out there mix HIP code directly in the .cpp files. Does this mean all compilation has to go through the AMD HIP compiler? How do we get this to play nicely with existing projects developed in Visual Studio?

---

## 评论 (3 条)

### 评论 #1 — saadrahim (2023-07-31T13:17:12Z)

Hi @gbeatty ,
Please take a look at https://github.com/amd/rocm-examples/tree/develop. I will also make public documentation for our visual studio plugin.

---

### 评论 #2 — saadrahim (2023-08-03T22:39:25Z)

![image](https://github.com/RadeonOpenCompute/ROCm/assets/44449863/902e4351-3bb3-4269-b37f-e3aa5d6f6baa)
I am adding these two sections to the install section to address your concerns. see #2365 

---

### 评论 #3 — gbeatty (2023-08-24T13:39:10Z)

I'm still confused on the implications of migrating to HIP on windows. Is there any high level documentation on the HIP compiler for Visual Studio? Is the HIP/clang compiler a complete C++ compiler, or is it a pre-compiler/steering compiler that eventually builds the final object files with the msvc compiler (like NVCC). It sure sounds like using the HIP compiler moves all compilation for that project over to clang and away from the msvc compiler. Is that true?

From a developer standpoint, that seems to introduce significant risk into our process. For our non-trivial product (multiple VS projects & solutions) it sounds like we're going to end up with some code built with the VS compiler, and other code built with clang. So, now we inherit bugs from both msvc and clang, plus any issues resulting from msvc compiled code loading dlls/libs built with HIP/clang.

Am I missing something fundamental here?

---
