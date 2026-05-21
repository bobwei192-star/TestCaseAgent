# [Issue]: _sync functions don't work when a non-full mask is given

> **Issue #5241**
> **状态**: open
> **创建时间**: 2025-09-01T16:09:15Z
> **更新时间**: 2025-09-02T01:42:48Z
> **作者**: alexfs
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5241

## 描述

### Problem Description

Do sync functions even work with a non-full mask? 
Always getting HSA_STATUS_ERROR_EXCEPTION: An HSAIL operation resulted in a hardware exception. code: 0x1016

#include <hip/hip_runtime.h>
#include <stdio.h>

__global__ void test_ballot() {
    unsigned lane = threadIdx.x & (warpSize - 1);
    unsigned long long mask = 0xFFFFull;        // lower 16 lanes

    unsigned long long vote = __ballot_sync(mask, (lane % 2 == 0));

    if (lane == 0) {
        printf("warpSize=%u activemask=0x%016llx vote=0x%016llx\n",
               warpSize, (unsigned long long)__activemask(), vote);
    }
}

int main() {
    test_ballot<<<1, warpSize>>>();
    hipDeviceSynchronize();
    return 0;
}

### Operating System

Ubuntu 22.04

### CPU

Intel(R) Xeon(R) Platinum 8470

### GPU

AMD Instinct MI300X

### ROCm Version

6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — b-sumner (2025-09-02T01:42:48Z)

@alexfs AMD GPUs do not support "independent thread scheduling" (and there are certain advantages in this).  If you use the *_sync APIs, you must follow the same guidance Nvidia gives for pre-volta architectures: "Note, however, that for Pascal and earlier architectures, _all threads in mask must execute the same warp intrinsic instruction in convergence, and the union of all values in mask must be equal to the warp’s active mask_."

---
