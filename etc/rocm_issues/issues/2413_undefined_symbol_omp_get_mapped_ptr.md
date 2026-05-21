# undefined symbol: omp_get_mapped_ptr

> **Issue #2413**
> **状态**: closed
> **创建时间**: 2023-08-28T23:36:07Z
> **更新时间**: 2024-03-21T04:02:39Z
> **关闭时间**: 2024-03-21T04:02:39Z
> **作者**: Ashutosh-Londhe
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2413

## 描述

I am getting an error for `undefined symbol: omp_get_mapped_ptr` when compiling for OpenMP offload 

I am using following command
` clang++ -O3 -fPIC -DUNIX -Wall -g -std=c++11 -fopenmp -fopenmp=libomp -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx908 -I/ext-home/asl/OPS_cg/OPS/ops/c/include -L/ext-home/asl/OPS_cg/OPS/ops/c/lib/clang  laplace2d_ops.cpp  -I. ./openmp_offload/openmp_offload_kernels.cpp   -lops_ompoffload -lomptarget -o laplace2d_ompoffload`

I am using a Rocm5.4.3 version.
I have another clang installation, in its libomptarget i found the `omp_get_mapped_ptr` using `nm` command
but its not there in libomptarget.so file under Rocm/llvm/lib



---

## 评论 (3 条)

### 评论 #1 — Thyre (2023-08-29T13:10:40Z)

ROCm 5.4 is based on LLVM 15 which did not contain `omp_get_mapped_ptr` as a symbol. 
It is first implemented in LLVM 16.0.0 (and its release canidates). ROCm 5.5.0 did use a pre-release LLVM 16 and did not contain the function either, but ROCm 5.6 has it for sure. Don't know about the patch releases in between 5.5 and 5.6.

Here's the corresponding LLVM commit: https://github.com/llvm/llvm-project/commit/6e18277a51187ce8e861cdf0ab1395235e5b83d4


---

### 评论 #2 — nartmada (2024-03-16T02:06:24Z)

@Thyre, thank you for your comment.

@Ashutosh-Londhe, has your issue been resolved?  Thanks.

---

### 评论 #3 — nartmada (2024-03-21T04:02:39Z)

Closing the issue as no response from @Ashutosh-Londhe.  Please re-open if you still observe this issue with latest ROCm 6.0.2.  Thanks.

---
