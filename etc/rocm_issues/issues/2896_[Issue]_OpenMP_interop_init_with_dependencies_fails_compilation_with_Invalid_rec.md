# [Issue]: OpenMP interop init with dependencies fails compilation with Invalid record error

> **Issue #2896**
> **状态**: closed
> **创建时间**: 2024-02-14T13:12:12Z
> **更新时间**: 2024-06-25T06:19:27Z
> **关闭时间**: 2024-06-25T06:19:26Z
> **作者**: Thyre
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2896

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

While trying to build reproducers to work around https://github.com/ROCm/rocm_smi_lib/issues/129 and https://github.com/ROCm/HIP/issues/3330, I've ran into a simple issue when trying interoperability between HIP and OpenMP offloading. 

With the following reproducer, compilation fails with ROCm 6.0.2 and ROCm 5.7.0. 

```c
#include <omp.h>

int main( void )
{
  int N = 100000;
  int *A = (int *)malloc(sizeof(int) * N);
  #pragma omp target enter data map(alloc: A[:N])
  
  #pragma omp target depend(out: A)
  for (int i = 0; i < N; ++i)
    A[i] = i;
  
  omp_interop_t iobj = omp_interop_none;
  #pragma omp interop init(targetsync: iobj) depend(in: A)
}
```

Here's the output of the compilation:
```console
$ amdclang --version
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-5.7.0 23352 d1e13c532a947d0cbfc94759c00dcf152294aa13)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/ROCm/5.7.0/llvm/bin
$ amdclang -fopenmp --offload-arch=gfx1101 minimal.c 
error: Invalid record (Producer: 'LLVM17.0.0git' Reader: 'LLVM 17.0.0git')
1 error generated.
error: Invalid record (Producer: 'LLVM17.0.0git' Reader: 'LLVM 17.0.0git')
```

The same result can be observed with ROCm 6.0.2. LLVM/Clang 16.0.6 fails the compilation more spectacularly with the assertion:
```
clang-16: /opt/apps/sources/LLVM/llvm-project/llvm/lib/IR/Instructions.cpp:636: void llvm::CallInst::init(llvm::FunctionType*, llvm::Value*, llvm::ArrayRef<llvm::Value*>, llvm::ArrayRef<llvm::OperandBundleDefT<llvm::Value*> >, const llvm::Twine&): Assertion `(i >= FTy->getNumParams() || FTy->getParamType(i) == Args[i]->getType()) && "Calling a function with a bad signature!"' failed.
```

LLVM/Clang 17.0.6 can compile the program fine and shows to issues. 

The issue occurs because of the `depend(in: A)` clause for the `#pragma omp interop init`. Removing the clause will fix the compilation, but is not desired since we intend to use `#pragma omp interop init(...) nowait depend(in: A)` in our code. 

### Operating System

Ubuntu 22.04.3 LTS

### CPU

Intel Core i7-12700

### GPU

AMD Radeon RX 7700 XT

### ROCm Version

ROCm 6.0.2

### ROCm Component

llvm-project

---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-02-16T16:01:13Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — Thyre (2024-06-25T06:19:26Z)

This issue seems to be solved in ROCm 6.1.2.

---
