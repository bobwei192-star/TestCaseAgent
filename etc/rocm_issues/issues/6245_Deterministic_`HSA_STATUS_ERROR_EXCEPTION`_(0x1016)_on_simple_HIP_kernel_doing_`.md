# Deterministic `HSA_STATUS_ERROR_EXCEPTION` (0x1016) on simple HIP kernel doing `printf` + `__builtin_trap()` (MI355X, ROCm 7.1.1)

> **Issue #6245**
> **状态**: open
> **创建时间**: 2026-05-12T23:36:04Z
> **更新时间**: 2026-05-13T01:23:22Z
> **作者**: JoeLoser
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6245

## 描述

**Problem Description**

A minimal HIP program that launches a kernel where one thread calls `printf` and every thread then calls `__builtin_trap()` **fails deterministically on AMD Instinct MI355X + ROCm 7.1.1**: the host-side queue is aborted by `libhsa-runtime64` *before* the `printf` reaches stdout. **30 out of 30 sequential runs** in our environment trigger the same error:

```
:0:rocdevice.cpp :3587: <ts>: Callback: Queue 0x<...> aborting with error :
  HSA_STATUS_ERROR_EXCEPTION: An HSAIL operation resulted in a hardware exception. code: 0x1016
```

The expected `ABORT: gpu abort message …` line never reaches stdout, suggesting the queue-abort callback is firing before the GPU printf buffer is drained to the host. The trap itself is intentional (it's `__builtin_trap` from device code), but the host should see the printf output that preceded it.

**Environment**

- GPU: AMD Instinct MI355X (CDNA3, gfx950, 64-wide wavefronts)
- ROCm: 7.1.1 (`/opt/rocm-7.1.1`)
- OS / kernel: *<fill in>*

**Minimal reproducer**

```cpp
// trap_flake_repro.cpp
#include <hip/hip_runtime.h>
#include <cstdio>

__global__ void abort_kernel() {
  if (threadIdx.x == 0 && threadIdx.y == 0 && threadIdx.z == 0 &&
      blockIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0) {
    printf("ABORT: gpu abort message from block [%d,%d,%d] thread [%d,%d,%d]\n",
           blockIdx.x, blockIdx.y, blockIdx.z,
           threadIdx.x, threadIdx.y, threadIdx.z);
  }
  __builtin_trap();
}

int main() {
  abort_kernel<<<dim3(2, 1, 1), dim3(32, 1, 1)>>>();
  (void)hipDeviceSynchronize();
  return 0;
}
```

**Build & run**

```bash
hipcc -O2 -o trap_flake_repro trap_flake_repro.cpp

for i in $(seq 1 30); do
  echo "=== run $i ==="
  ./trap_flake_repro 2>&1
done
```

**Expected**

Every run prints:
```
ABORT: gpu abort message from block [0,0,0] thread [0,0,0]
```
(the trap-induced queue abort is fine — that's intentional; only the missing printf is the bug).

**Actual**

30/30 runs produce only:
```
:0:rocdevice.cpp :3587: <ts>: Callback: Queue 0x<...> aborting with error :
  HSA_STATUS_ERROR_EXCEPTION: An HSAIL operation resulted in a hardware exception. code: 0x1016
```
…with no printf output.

**Additional context**

- This was originally observed at a lower flaky rate (17% rate in a Mojo test in our codebase ([`mojo/stdlib/test/os/test_trap_gpu.mojo`](https://github.com/modular/modular/blob/main/mojo/stdlib/test/os/test_trap_gpu.mojo)), where `abort()` lowers to a gated printf + `__builtin_trap()` from every thread. The Mojo wrapper apparently masks the bug ~83% of the time. The standalone HIP version above reproduces deterministically.
- Two failure modes have been observed:
  - `HSA_STATUS_ERROR_EXCEPTION` (`0x1016`) — most common; what the HIP repro shows 30/30 times.
  - `HSA_STATUS_ERROR_OUT_OF_RESOURCES` (`0x1008`, "Available Free mem : 0 MB") — observed in some Mojo invocations; appears to be the same race with a different timing window.
- We have disabled the affected test on AMD as a workaround.
- Related: [ROCm/ROCm#5025](https://github.com/ROCm/ROCm/issues/5025) (closed for inactivity, same code, different workload), [ROCm/ROCm#6023](https://github.com/ROCm/ROCm/issues/6023) (open, MI325X, same code).
- We are happy to test patches.


---

## 评论 (1 条)

### 评论 #1 — b-sumner (2026-05-13T01:23:22Z)

Hi @JoeLoser.   The expectation expressed here is incorrect.  Block (0,0,0) is not guaranteed to make progress before other blocks, and even if it happens to start first, it is incorrect to assume that any operations in it happen before any operations carried out by other blocks.  Some sort of synchronization is required if ordering must be guaranteed.

---
