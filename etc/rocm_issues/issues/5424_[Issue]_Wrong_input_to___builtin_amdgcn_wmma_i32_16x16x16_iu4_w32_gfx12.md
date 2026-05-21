# [Issue]: Wrong input to __builtin_amdgcn_wmma_i32_16x16x16_iu4_w32_gfx12

> **Issue #5424**
> **状态**: closed
> **创建时间**: 2025-09-24T09:12:52Z
> **更新时间**: 2025-09-27T10:19:43Z
> **关闭时间**: 2025-09-27T10:19:43Z
> **作者**: zhang-hui-yulo
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5424

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

__builtin_amdgcn_wmma_i32_16x16x16_iu4_w32_gfx12 shall takes a "2 int32_t" as input to represent "16 int4_t", but the code can only be compiled when the input is just "1 int32_t".

__builtin_amdgcn_wmma_i32_16x16x16_iu4_w32 seems to be fine.

### Operating System

Windows 11 10.0.26100

### CPU

AMD Ryzen 9 7900X3D 12-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 6.4.2

### ROCm Component

HIP

### Steps to Reproduce

main.hip
```
#include <hip/hip_runtime.h>

using int32_t_8 = int32_t __attribute__((ext_vector_type(8)));
using int32_t_2 = int32_t __attribute__((ext_vector_type(2)));

__global__ void test() {
#if defined(__GFX12__)
#if 1
    // this is the right code but cannot be compiled
    int32_t_2 am = { 1 };
    int32_t_2 bm = { -1 };
#else
    // this can be compiled but probably not the right code.
    int32_t am = { 1 };
    int32_t bm = { -1 };
#endif
    int32_t_8 cm = { 0 };

    cm = __builtin_amdgcn_wmma_i32_16x16x16_iu4_w32_gfx12(true, am, true, bm, cm, true);

#elif defined(__GFX11__)
    // this can be compiled in gfx11.
    int32_t_2 am = { 1 };
    int32_t_2 bm = { -1 };
    int32_t_8 cm = { 0 };

    cm = __builtin_amdgcn_wmma_i32_16x16x16_iu4_w32(true, am, true, bm, cm, true);
#endif
}

int main(int argc, char** argv) {
    test <<< 1, 32 >>> ();
    return 0;
}
```

build command
```
"%HIP_PATH%bin/clang++" --offload-arch=gfx1201 --offload-arch=gfx1100 main.hip -o main.exe
```

error message
```
main.hip:19:65: error: cannot initialize a parameter of type 'int' with an lvalue of type 'int32_t_2'
      (vector of 2 'int32_t' values)
   19 |     cm = __builtin_amdgcn_wmma_i32_16x16x16_iu4_w32_gfx12(true, am, true, bm, cm, true);
      |                                                                 ^~
1 error generated when compiling for gfx1201.
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2025-09-24T17:28:47Z)

Hi @zhang-hui-yulo. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — zhang-hui-yulo (2025-09-27T10:19:43Z)

Hello @ppanchad-amd and @amd-nicknick ,

I think I've found the root cause, gfx12 changes the mma layout from V16 to V8, so int32_t can represent 8 int4_t, close it.

Best Regards
Hui

---
