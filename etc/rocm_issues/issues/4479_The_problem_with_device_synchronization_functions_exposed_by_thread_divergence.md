# The problem with device synchronization functions exposed by thread divergence

> **Issue #4479**
> **状态**: closed
> **创建时间**: 2025-03-11T06:55:54Z
> **更新时间**: 2025-03-26T15:17:16Z
> **关闭时间**: 2025-03-26T15:16:43Z
> **作者**: wumuren-123
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4479

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

**Problem Description**
When I ran the test cases designed by myself, I found logical errors in __all_sync and __match_all_sync;

**Environment**
OS: CentOS Linux release 7.6.1810

ROCm Version: 6.3.x

**Reproduction Steps**
1:__all_sync demo:If the threads diverge, this use case is plugging in, and by analogy there is a case where __all_sync and __all compute inconsistent data;It is possible to reason about and test the results at 32 differentiation, 48 differentiation, and 64 differentiation
```
#include <iostream>
#include <hip/hip_runtime.h>
#include <vector>
__device__ int A[64];
__device__ int result[64];
__device__ int result16[64];
__global__ void warp_all_sync_test() {
    unsigned long long mask = 0xffffffffffffffff;
    int tx = threadIdx.x;
    if (threadIdx.x < 16) {
        A[tx] = 0;
    } else {
        A[tx] = 1;
    }
    __syncthreads();
    if (threadIdx.x < 16) {
        result16[tx] = __all_sync(mask, A[tx]);
    } else {
        result16[tx] = __all_sync(mask, A[tx]);
    }
    printf("result16 = %d\n", result16[tx]);
}
int main () {
    warp_all_sync_test<<<1, 64>>>();
    return 0;
}
```

2:__match_all_sync demo:The following example causes the program to crash,It is possible to reason about and test the results at 32 differentiation, 48 differentiation, and 64 differentiation

```
#include <iostream>
#include <hip/hip_runtime.h>
#include <vector>
__device__ int A[64];
__device__ unsigned long long result16[64];
__global__ void warp_match_all_sync_test() {
    unsigned long long mask = 0xffffffffffffffff;
    int tx = threadIdx.x;
    if (threadIdx.x < 16) {
        A[tx] = 0;
    } else {
        A[tx] = 1;
    }
    int valueToMatch = 1;
    int *pred = &valueToMatch;
    __syncthreads();
    if (threadIdx.x < 16) {
        result16[tx] = __match_all_sync(mask, A[tx], pred);
    } else {
        result16[tx] = __match_all_sync(mask, A[tx], pred);
    }
    printf("result16[%d] = %llx\n", tx, result16[tx]);
}
int main () {
    warp_match_all_sync_test<<<1, 64>>>();
    return 0;
}
```

**Expected Result**
The program should compile and run successfully.

Actual Result
Error message:causes crush

Notes for Submission:
Compile with the following command:
hipcc xx.cu -o xx -DHIP_ENABLE_WARP_SYNC_BUILTINS

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-03-11T14:12:17Z)

Hi @wumuren-123. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — wumuren-123 (2025-03-11T14:12:51Z)

这是来自QQ邮箱的假期自动回复邮件。
 
您好，我最近正在休假中，无法亲自回复您的邮件。我将在假期结束后，尽快给您回复。

---

### 评论 #3 — wumuren-123 (2025-03-12T01:18:39Z)

> Hi [@wumuren-123](https://github.com/wumuren-123). Internal ticket has been created to investigate this issue. Thanks!
I have a solution here：
Inside the __all_sync function is __ballot_sync()==mask; To implement。We can change this to compare with __activemask();
__match_all_sync crashes because __hip_assert(MASK == __ballot(true)) in the macro definition __hip_do_sync, This can be modified to __hip_assert(__activemask() == __ballot(true)) avoidance;
But I think you have a better way




---

### 评论 #4 — b-sumner (2025-03-12T01:45:06Z)

The masks being used in the two examples are not valid.  Consider this requirement from the Cuda programming guide section on independent thread scheduling:

Note, however, that for Pascal and earlier architectures, all threads in mask must execute the same warp intrinsic instruction in convergence, and the union of all values in mask must be equal to the warp’s active mask. 

All AMD GPUs have the same requirement as they do not support independent thread scheduling.

---

### 评论 #5 — sohaibnd (2025-03-26T15:16:43Z)

@wumuren-123 Closing this issue due to inactivity but feel free to re-open it if you have any follow-up questions.

---

### 评论 #6 — wumuren-123 (2025-03-26T15:17:15Z)

这是来自QQ邮箱的假期自动回复邮件。
 
您好，我最近正在休假中，无法亲自回复您的邮件。我将在假期结束后，尽快给您回复。

---
