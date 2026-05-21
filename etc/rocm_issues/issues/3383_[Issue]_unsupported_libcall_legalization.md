# [Issue]: unsupported libcall legalization

> **Issue #3383**
> **状态**: closed
> **创建时间**: 2024-07-02T15:58:37Z
> **更新时间**: 2024-08-08T15:37:11Z
> **关闭时间**: 2024-08-08T15:37:10Z
> **作者**: tkramer-motion
> **标签**: AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3383

## 标签

- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I am getting a unsupported libcall legalization error when trying to compile a hip file.

```
fatal error: error in backend: unsupported libcall legalization
clang++: error: clang frontend command failed with exit code 70 (use -v to see invocation)
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.2 24193 669db884972e769450470020c06a6f132a8a065b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.1.2/llvm/bin
Configuration file: /opt/rocm-6.1.2/lib/llvm/bin/clang++.cfg
clang++: note: diagnostic msg: Error generating preprocessed source(s).
make[2]: *** [CMakeFiles/custom_ops.dir/build.make:127: CMakeFiles/custom_ops.dir/hip/file.cu.hip.o] Error 1
make[1]: *** [CMakeFiles/Makefile2:102: CMakeFiles/custom_ops.dir/all] Error 2
make: *** [Makefile:136: all] Error 2
```

### Operating System

Ubuntu 22.04

### CPU

AMD EPYC 7R32

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — tkramer-motion (2024-07-02T18:39:19Z)

This happens when using Explicit template instantiation

template class SomeClass<double>;

---

### 评论 #2 — harkgill-amd (2024-07-08T16:00:23Z)

Hi @tkramer-motion, could you please provide a minimal reproducible example so we can try to reproduce this internally. Thanks!

---

### 评论 #3 — tkramer-motion (2024-07-13T17:53:22Z)

Here you go.

```
#include <hip/hip_runtime.h>

#define FIXED_EXPONENT 0x1000000000

void __global__ k_example(const double u_orig) {
    double u = u_orig * FIXED_EXPONENT;
    __int128 ret;
    if (!isfinite(u) || static_cast<__int128>(u) >= static_cast<__int128>(LLONG_MAX) ||
        static_cast<__int128>(u) <= static_cast<__int128>(LLONG_MIN)) {
        ret = static_cast<__int128>(LLONG_MAX);
    } else {
        ret = static_cast<__int128>(llrintf(u));
    }
}

class Example {
public:
    void execute_device(hipStream_t stream) {
        int tpb = 64;
        int blocks = 16;
        k_example<<<blocks, tpb, 0, stream>>>(454.34);
    }
};

int main() {
    Example cr;
    hipStream_t stream;
    hipStreamCreate(&stream);
    cr.execute_device(stream);
}
```

Compiling with 

`/opt/rocm-6.1.2/llvm/bin/clang++  -std=gnu++17 --offload-arch=gfx1100  -x hip -c example.cu.hip`

Results in

```
fatal error: error in backend: unsupported libcall legalization
clang++: error: clang frontend command failed with exit code 70 (use -v to see invocation)
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.2 24193 669db884972e769450470020c06a6f132a8a065b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.1.2/llvm/bin
Configuration file: /opt/rocm-6.1.2/lib/llvm/bin/clang++.cfg
clang++: note: diagnostic msg: Error generating preprocessed source(s).
```
```

---

### 评论 #4 — tkramer-motion (2024-07-13T17:56:15Z)

@harkgill-amd This happens regardless of the architecture chosen. 

Issue seems to be caused by the casting to __int128. Operating on 64-bit ints doesn't cause the error but obviously the logic is wrong.

```
#include <hip/hip_runtime.h>

#define FIXED_EXPONENT 0x1000000000

void __global__ k_example(const double u_orig) {
    double u = u_orig * FIXED_EXPONENT;
    __int128 ret;
    if (!isfinite(u) || static_cast<long long>(u) >= static_cast<long long>(LLONG_MAX) ||
        static_cast<long long>(u) <= static_cast<long long>(LLONG_MIN)) {
        ret = static_cast<long long>(LLONG_MAX);
    } else {
        ret = static_cast<long long>(llrintf(u));
    }
}

class Example {
public:
    void execute_device(hipStream_t stream) {
        int tpb = 64;
        int blocks = 16;
        k_example<<<blocks, tpb, 0, stream>>>(454.34);
    }
};

int main() {
    Example cr;
    hipStream_t stream;
    hipStreamCreate(&stream);
    cr.execute_device(stream);
}
```

---

### 评论 #5 — harkgill-amd (2024-07-15T17:08:47Z)

@tkramer-motion, thank you for providing the example; I was able to reproduce the issue. Support for converting a floating point value (double, float) to __int128 will be added in an upcoming ROCm release. 

I will circle back to this once support is out and we can retest/close out this issue.

---

### 评论 #6 — harkgill-amd (2024-08-07T19:42:14Z)

Hi @tkramer-motion, the fix is present in ROCm 6.2.0 and I no longer see any issues when running your example code. Could you please test it out on your end and confirm?

---

### 评论 #7 — tkramer-motion (2024-08-07T19:54:45Z)

Confirmed. We can compile our project with 6.2.0. Thanks!

---

### 评论 #8 — harkgill-amd (2024-08-08T15:37:10Z)

Great! Will close out this issue in that case.

---
