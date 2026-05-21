# [Issue]: rocprofv3 --pmc crashes on gfx1151 (Strix Halo) - hsa_ven_amd_aqlprofile_get_info abort

> **Issue #5951**
> **状态**: closed
> **创建时间**: 2026-02-10T21:16:43Z
> **更新时间**: 2026-02-12T17:16:55Z
> **关闭时间**: 2026-02-12T17:16:55Z
> **作者**: john-hahn
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5951

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

## Description

Hardware counter collection with `rocprofv3` crashes with `SIGABRT` on gfx1151 (AMD Ryzen AI MAX+ 395 / Radeon 8060S). Basic tracing (`--hip-trace`, `--kernel-trace`) works correctly — only PMC/hardware counter collection fails.

The crash originates in `libhsa-amd-aqlprofile64.so` during `hsa_ven_amd_aqlprofile_get_info`, triggered when `hsa_iterate_agents` fails with `HSA_STATUS_ERROR`.

## Environment

- **GPU:** AMD Ryzen AI MAX+ 395 w/ Radeon 8060S (gfx1151)
- **OS:** Ubuntu 24.04 (kernel 6.14.0-1020-oem)
- **ROCm:** 7.2.0 (also tested with 7.9.0rc tarball aqlprofile — same crash)
- **rocprofv3:** rocprofiler-sdk 1.1.0
- **amdgpu driver:** amdgpu-dkms 6.16.13

## Steps to Reproduce

1. Compile a simple HIP program:

```cpp
#include <hip/hip_runtime.h>
#include <cstdio>

__global__ void simple_kernel(float* out, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) out[i] = (float)i * 2.0f;
}

int main() {
    const int N = 1024;
    float* d_out;
    hipMalloc(&d_out, N * sizeof(float));
    simple_kernel<<<N/256, 256>>>(d_out, N);
    hipDeviceSynchronize();
    hipFree(d_out);
    printf("Done\n");
    return 0;
}
```

```bash
hipcc test_hip.cpp -o test_hip
```

2. Run with hardware counters:

```bash
rocprofv3 --pmc SQ_WAVES -o /tmp/counter_test -- ./test_hip
```

## Expected Behavior

Hardware counters should be collected and reported.

## Actual Behavior

Crash in `hsa_ven_amd_aqlprofile_get_info`:

```
W20260210 20:36:13.516926 tool.cpp:2422] HSA version 8.20.0 initialized (instance=0)
Error Calling hsa_iterate_agents: HSA_STATUS_ERROR: A generic error has occurred.
*** SIGABRT (@0x3e90000d149) received by PID 53577 (TID 0x7509735fdf40) from PID 53577; stack trace: ***
    ...
    hsa_ven_amd_aqlprofile_get_info
    ...
Aborted (core dumped)
```

## Working vs Broken

| Command | Result |
|---|---|
| `rocprofv3 --hip-trace -- ./test_hip` | Works correctly |
| `rocprofv3 --pmc SQ_WAVES -- ./test_hip` | SIGABRT crash |
| `rocprofv2 --list-counters` | Core dump |

## Additional Testing

- Swapped `libhsa-amd-aqlprofile64.so` from TheRock 7.9.0rc20251008 tarball (via `LD_PRELOAD`) — same SIGABRT crash in `hsa_ven_amd_aqlprofile_get_info`
- Used full 7.9.0rc tarball's rocprofv3 with `LD_LIBRARY_PATH` — different crash (SIGSEGV in `GpuAgent::ReleaseQueueMainScratch` due to version mismatch with system HSA runtime)
- `HSA_OVERRIDE_GFX_VERSION=11.0.0` — SIGSEGV (worse)
- `HSA_OVERRIDE_GFX_VERSION=11.5.0` — SIGSEGV (worse)
- Both 7.2.0 and 7.9.0rc `libhsa-amd-aqlprofile64.so` contain `Gfx115xFactory` but no gfx1151-specific factory
- `rocprofv2 --list-counters` also core dumps
- The nightly pip package (`rocm-sdk-devel 7.12.0a20260210`) does not include aqlprofile or rocprofiler

## Analysis

The `Gfx115xFactory` in `libhsa-amd-aqlprofile64.so` appears to not properly handle gfx1151 hardware counter setup. The library recognizes the gfx115x family but crashes when attempting to configure PMC collection, suggesting incomplete or broken counter definitions for this ASIC.


---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2026-02-11T15:16:40Z)

Hey @john-hahn, could you give this a try with the latest nightlies, version `7.12.0a20260211`, using the following command 
```
$(rocm-sdk path --bin)/rocprofv3 --pmc SQ_WAVES -o /tmp/counter_test -- ./test_hip
```
This'll force usage of the rocprofv3 bundled in the nightly. For context, I did see the same issue on my end when `which rocprofv3` pointed to the 7.2.0 installation and not the nightlies - running the aforementioned command resolved this.

---

### 评论 #2 — john-hahn (2026-02-12T17:16:55Z)

Hi, I forgot to mention that I was able to fix this issue by cloning the rocm-systems repo and then symlinking it before your reply. Thanks for the help, I'll be closing this now!

---
