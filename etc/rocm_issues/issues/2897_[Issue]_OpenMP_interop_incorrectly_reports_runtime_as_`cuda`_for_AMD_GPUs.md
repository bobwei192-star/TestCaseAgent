# [Issue]: OpenMP interop incorrectly reports runtime as `cuda` for AMD GPUs

> **Issue #2897**
> **状态**: closed
> **创建时间**: 2024-02-14T15:52:15Z
> **更新时间**: 2025-10-22T12:40:52Z
> **关闭时间**: 2025-10-22T12:40:52Z
> **作者**: Thyre
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2897

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

While building a test case while working around #2896, I've stumbled upon another issue with OpenMP interops. 
Simply printing the output of `omp_get_interop_[x]` reveals that the runtime reports having `cuda` when an AMD GPU with ROCm is used. The reasons can probably be found in [omp.h#L137](https://github.com/llvm/llvm-project/blob/995c9061ed13c5e494ef5883cfd8c813eb5c32c3/openmp/libomptarget/include/OpenMP/omp.h#L137) and here [InterOPAPI.cpp#L224](https://github.com/llvm/llvm-project/blob/457c17944c6eb3d89ae6a765e4795c1cc3148506/openmp/libomptarget/src/OpenMP/InteropAPI.cpp#L224). Regardless of the GPU type, the struct is always initialized with CUDA as default and never overwritten (see [InteropAPI.h#L28](https://github.com/llvm/llvm-project/blob/995c9061ed13c5e494ef5883cfd8c813eb5c32c3/openmp/libomptarget/include/OpenMP/InteropAPI.h#L28))

To reproduce, one can use this simple test case:
```c
#include <omp.h>
#include <stdio.h>

const char* interop_int_to_string( const int interop_int )
{
    switch( interop_int )
    {
        case 1:
            return "cuda";
        case 2:
            return "cuda_driver";
        case 3:
            return "opencl";
        case 4:
            return "sycl";
        case 5:
            return "hip";
        case 6:
            return "level_zero";
        default:
            return "unknown";
    }
}

int main( int argc, char** argv )
{
    omp_interop_t iobj = omp_interop_none;
    #pragma omp interop init(targetsync: iobj)

    int err;
    int interop_int = omp_get_interop_int( iobj, omp_ipr_fr_id, &err );

    if( err )
    {
        fprintf( stderr, "omp_get_interop_int failed: %d\n", err );
        return -1;
    }

    printf( "omp_get_interop_int returned %s\n", interop_int_to_string( interop_int ) );

    const char* interop_vendor = omp_get_interop_str( iobj, omp_ipr_vendor_name, &err );
    if( err )
    {
        fprintf( stderr, "omp_get_interop_str failed: %d\n", err );
        return -1;
    }

    printf( "omp_get_interop_str returned %s\n", interop_vendor );

    const char* interop_fr_name = omp_get_interop_str( iobj, omp_ipr_fr_name, &err );
    if( err )
    {
        fprintf( stderr, "omp_get_interop_str failed: %d\n", err );
        return -1;
    }

    printf( "omp_get_interop_str returned %s\n", interop_fr_name );

    #pragma omp interop destroy(iobj)
    return 0;
}
```

Here's the output of different compilers:

**ROCm 6.0.2:**
```console
$ amdclang -fopenmp --offload-arch=gfx1101 print_interop.c
$ ./a.out
omp_get_interop_int returned cuda
omp_get_interop_str returned cuda
omp_get_interop_str failed: -5
```

**LLVM 17.0.6:**
```console
$ clang -fopenmp --offload-arch=gfx1101 print_interop.c --rocm-path=/opt/apps/software/ROCm/6.0.2/
$ ./a.out
omp_get_interop_int returned cuda
omp_get_interop_str returned cuda
omp_get_interop_str failed: -5
```

**oneAPI 2024.0 (with Intel Arc iGPU):**
```console
$ icx -fiopenmp -fopenmp-targets=spir64 print_interop.c
$ ./a.out
omp_get_interop_int returned level_zero
omp_get_interop_str returned intel
omp_get_interop_str returned level_zero
```

**NVHPC 24.1 (with NVIDIA GPU):**
```console
$ nvc -mp=gpu print_interop.c
"print_interop.c", line 28: error: invalid text in pragma
      #pragma omp interop init(targetsync: iobj)
                          ^

1 error detected in the compilation of "print_interop.c".
```

### Operating System

Ubuntu 22.04.3 LTS

### CPU

Intel Core i7-12700

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — nartmada (2024-02-16T15:53:29Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — mhalk (2024-04-08T14:42:20Z)

Working on it:
Will be resolved by https://github.com/llvm/llvm-project/pull/88000

---

### 评论 #3 — jplehr (2025-10-02T09:14:32Z)

Pretty old issue, finally towards resolution, I think. There was some back and forth upstream too.

I created a PR upstream that adds this test (thank you for putting together): https://github.com/llvm/llvm-project/pull/161434
This is part of this effort: https://github.com/llvm/llvm-project/pull/161429

More discussion here: https://github.com/llvm/llvm-project/pull/161279

---

### 评论 #4 — Thyre (2025-10-02T09:23:59Z)

> Pretty old issue, finally towards resolution, I think. There was some back and forth upstream too.
> 
> I created a PR upstream that adds this test (thank you for putting together): [llvm/llvm-project#161434](https://github.com/llvm/llvm-project/pull/161434) This is part of this effort: [llvm/llvm-project#161429](https://github.com/llvm/llvm-project/pull/161429)
> 
> More discussion here: [llvm/llvm-project#161279](https://github.com/llvm/llvm-project/pull/161279)

Great! Thanks for looking into this. I'll also take a look at those PRs hopefully today, though I unfortunately can't add much to any discussion about LLVM internals. Really need to look into the LLVM internals a bit more.

---

### 评论 #5 — jplehr (2025-10-22T12:40:52Z)

I tested this with an AOMP build today and the interop regression test I added for this passes with the expected results.
Thank you, I'm gonna close this issue as resolved.

---
