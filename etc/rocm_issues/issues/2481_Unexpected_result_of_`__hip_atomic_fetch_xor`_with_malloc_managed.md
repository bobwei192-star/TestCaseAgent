# Unexpected result of `__hip_atomic_fetch_xor` with malloc managed

> **Issue #2481**
> **状态**: closed
> **创建时间**: 2023-09-19T15:04:38Z
> **更新时间**: 2023-09-19T17:02:49Z
> **关闭时间**: 2023-09-19T16:41:30Z
> **作者**: hdelan
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2481

## 描述

In CUDA, managed memory allocated with `cudaMallocManaged` can be accessed on host and device without needing to prefetch. Since the HIP API is meant to match the CUDA API closely, I expect the same behaviour for `hipMallocManaged`.

However, this simple example fails when `__hip_atomic_fetch_xor` is used with memory allocated with `hipMallocManaged`.

```
#include "hip/hip_runtime.h"

#include <cassert>

constexpr int init = 0;
constexpr int n = 1;

__global__ void test_xor(int *data, int val) {
#ifdef MY_ATOMIC_ADD
  __hip_atomic_fetch_add(data, val, __ATOMIC_RELAXED,
                         __HIP_MEMORY_SCOPE_WAVEFRONT);
#else
  __hip_atomic_fetch_xor(data, val, __ATOMIC_RELAXED,
                         __HIP_MEMORY_SCOPE_WAVEFRONT);
#endif
}

#define CHECK(res)                                                             \
  if (res != hipSuccess) {                                                     \
    fprintf(stderr, #res " failed!\n");                                        \
    std::terminate();                                                          \
  }

int main(int argc, char **argv) {
  int *data = nullptr;
  CHECK(hipMallocManaged(&data, n * sizeof *data, hipMemAttachGlobal));
  hipStream_t s;
  CHECK(hipStreamCreate(&s));
  for (size_t i = 0; i < n; ++i)
    data[i] = init;

#ifdef MY_PREFETCH
  CHECK(hipMemPrefetchAsync(data, n * sizeof *data, 0));
#endif
  int xor_val = 1;
  hipLaunchKernelGGL(test_xor, 1, 1, 0, s, data, xor_val);
  CHECK(hipDeviceSynchronize());

  for (size_t i = 0; i < n; ++i)
    printf("Malloc managed ans: %d\tExpected: %d\n", data[i], init ^ xor_val);
  CHECK(hipFree(data));
}

```

Output:
```
$ hipcc hip_xor.cpp && ./a.out
Malloc managed ans: 0	Expected: 1
```
The example will work if `__hip_atomic_fetch_add` is used instead of `__hip_atomic_fetch_xor`:
```
$ hipcc hip_xor.cpp -DMY_ATOMIC_ADD && ./a.out
Malloc managed ans: 1	Expected: 1
```
The sample will also work with a prefetch and xor:
```
$ hipcc hip_xor.cpp -DMY_PREFETCH && ./a.out
Malloc managed ans: 1	Expected: 1
```

Is a prefetch needed in order to use atomic ops on the GPU? If so then why does it work without the prefetch for `__hip_atomic_fetch_add` and not for `__hip_atomic_fetch_xor`? Or is there a problem with this single builtin (`__hip_atomic_fetch_xor`)? Thanks in advance.

Ping @ldrumm

OS: Ubuntu 22.04 
GPU: W6800 gfx1030
ROCm: Tested on rocm/5.4.3 and rocm/5.6.1.


---

## 评论 (8 条)

### 评论 #1 — b-sumner (2023-09-19T15:18:41Z)

@hdelan not sure why you're using a builtin rather than the standard atomicXor nor how you chose that scope?

My theory is that with your setup, the atomic is trying to cross the PCIe bus, and PCIe does not support atomic XOR.  Your test might pass with atomic ADD IF your system supports PCIe atomics (not all do).

---

### 评论 #2 — hdelan (2023-09-19T15:27:25Z)

Hi @b-sumner thanks for the quick response. The behaviour is the same if I use the standard atomic ops:
```
__global__ void test_xor(int *data, int val) {
#ifdef MY_ATOMIC_ADD
  atomicAdd(data, val);
#else
  atomicXor(data, val);
#endif
}
```

So the PCIe bus must support atomicXor in order to succeed? Could you possibly link me to some docs where I can read more about this? Thanks

---

### 评论 #3 — ldrumm (2023-09-19T15:33:58Z)

For some extra context, hdelan is following up after we added a workaround for this issue in the dpc++ runtime. My investigation might be useful context https://github.com/intel/llvm/issues/7252#issuecomment-1584995188

As for the builtins: In hdelan's original example they're simply expanded directly from the header for clarity. `atomicSub` won't reproduce this issue as it's implemented as the addition of a negated value, but atomicXor will

---

### 评论 #4 — b-sumner (2023-09-19T15:47:05Z)

This may help: https://rocm.docs.amd.com/en/latest/understand/More-about-how-ROCm-uses-PCIe-Atomics.html .  There is also a great deal of discussion about AMD's use of PCIe atomics in other issues.  Unfortunately, many platform vendors do not include atomic support some of all of their PCIe pathways.

---

### 评论 #5 — hdelan (2023-09-19T16:22:38Z)

Thanks very much @b-sumner . Just out of curiosity, why does HIP not choose to emulate atomicXor with a CAS loop, given that support for native atomic Xor is patchy for PCIe vendors?

---

### 评论 #6 — b-sumner (2023-09-19T16:33:07Z)

Hi @hdelan.  It's being discussed.  There is a concern about pessimizing existing code that may be running on systems with more capable interconnects.  Also, this may not work anyway given my previous comments about PCIe.  And we've observed that atomic AND, OR, and XOR are rarely used for communication between agents but frequently within an agent.

---

### 评论 #7 — hdelan (2023-09-19T16:41:20Z)

Thanks very much for your explanations @b-sumner. I am happy to close this issue. Ping @zjin-lcf for reference

---

### 评论 #8 — zjin-lcf (2023-09-19T17:02:49Z)

Hello @hdelan,

Thank you very much for discussing the issue with @b-sumner !  
The issue was first reported by @krasznaa


---
