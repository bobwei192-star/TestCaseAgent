# [Issue]: bfloat16 functions emit duplicate host symbols in multi-TU HIP builds

> **Issue #6112**
> **状态**: closed
> **创建时间**: 2026-04-02T18:05:10Z
> **更新时间**: 2026-04-13T21:13:41Z
> **关闭时间**: 2026-04-13T21:13:41Z
> **作者**: mkoker
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6112

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- zichguan-amd

## 描述

### Problem

When multiple `.cu` / `.hip` files include HIP headers and use bfloat16, the linker reports duplicate symbol errors for functions like `__float2bfloat16`, `__bfloat1622float2`, `__double2bfloat16`, etc. — despite these being declared `static inline` in the header.

### Reproduction

Any multi-TU HIP project that includes bfloat16 headers. Reproduced with llama.cpp (`cmake -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1201`):

```
ld.lld: error: duplicate symbol: __float2bfloat16(float)
>>> defined at acc.cu
>>> defined at arange.cu
ld.lld: error: duplicate symbol: __bfloat1622float2(__hip_bfloat162)
ld.lld: error: duplicate symbol: __double2bfloat16(double)
ld.lld: error: duplicate symbol: __float22bfloat162_rn(HIP_vector_type<float, 2u>)
ld.lld: error: duplicate symbol: __high2float(__hip_bfloat162)
ld.lld: error: duplicate symbol: __low2float(__hip_bfloat162)
```

### Root Cause

In `amd_hip_bf16.h:131`:

```cpp
#define __BF16_HOST_DEVICE_STATIC__ __BF16_HOST_DEVICE__ static inline
```

The functions are correctly declared `static inline`. However, when the HIP compiler processes `.cu` files for dual-target compilation (device + host), the `static inline` qualifier appears to be stripped or ignored during host-side emission, causing each translation unit to emit a non-static host symbol.

### What doesn't work

- `-Wl,--allow-multiple-definition` / `-Wl,-z,muldefs`: Links but causes **runtime segfaults** (wrong symbol resolved)
- `__attribute__((weak))`: Stripped by HIP compiler during dual-target compilation
- `-fvisibility=hidden`: No effect
- `-fgpu-rdc`: Needs HIP-specific linker flags that CMake doesn't route correctly

### Workaround

No clean workaround found. Possible approaches:
1. Concatenate all `.cu` files into a single translation unit
2. Build with `-fgpu-rdc` and `--hip-link` (requires HIP-aware linker invocation)
3. Build ROCm from source (confirmed working by tlee933/llama.cpp-rdna4-gfx1201)

### Expected Fix

The HIP compiler should properly honor `static inline` on host-side emission during dual-target compilation, or emit these as `weak` symbols.

### Environment

- **GPU:** AMD Radeon AI PRO R9700 (gfx1201, RDNA4)
- **ROCm:** 7.2.0 and 7.2.1
- **OS:** Ubuntu 24.04, kernel 6.17.0
- **Impact:** Blocks building any multi-file HIP project using bfloat16 (including llama.cpp with ~40 .cu files). Affects all GPU architectures, not just RDNA4.

### Related

- #6110 (gfx1201 "2 ISAs" device rejection)
- #6111 (gfx1201 `__AMDGCN_WAVEFRONT_SIZE` undefined)

---

## 评论 (3 条)

### 评论 #1 — zichguan-amd (2026-04-08T18:50:22Z)

Hi @mkoker, I'm able to build llama.cpp at `d12cc3d1ca6bba741cd77887ac9c9ee18c8415c7` with ROCm 7.2.1 on ubuntu 24.04.4 using cmake command `cmake --fresh -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1201 -S . -B build && cmake --build build -j`. Do you have any smaller reproducer?

---

### 评论 #2 — mkoker (2026-04-12T22:41:25Z)

@zichguan-amd I dug into this more and I think the build failure I was hitting is actually caused by the same stale header issue I described in #6111 — I have Ubuntu's `libamdhip64-dev` 5.7.1 installed alongside ROCm 7.2.1, and the old headers in `/usr/include/hip/` get picked up before `/opt/rocm/include/hip/`.

When I build llama.cpp at the commit you tested (`d12cc3d`), I get a different error than the bfloat16 one I originally reported:

```
/usr/include/hip/hip_runtime_api.h:2211:12: note: candidate function not viable: requires 3 arguments, but 2 were provided
 2211 | hipError_t hipStreamWaitEvent(hipStream_t stream, hipEvent_t event, unsigned int flags);
```

That's the 5.7.1 header's `hipStreamWaitEvent` signature (3 args) vs the 7.2.1 one (2 args with a default). So the build is failing because of the wrong headers, not bfloat16.

I need to remove the stale `libamdhip64-dev` package first and then retest. If the bfloat16 issue still reproduces after that, I'll come back with a clean repro. Apologies for the noise — this was likely two problems stacked on top of each other.


---

### 评论 #3 — mkoker (2026-04-12T22:51:48Z)

Confirmed — the bfloat16 issue was not real. It was caused by the stale Ubuntu-packaged ROCm 5.7.1 headers shadowing the ROCm 7.2.1 ones (same root cause as #6111).

After removing the old packages, llama.cpp builds cleanly with `GGML_HIP=ON -DAMDGPU_TARGETS=gfx1201` on current master. No bfloat16 linker errors.

This can be closed. Sorry for the false report.


---
