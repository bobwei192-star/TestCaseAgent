# [gfx1151] Page Fault on hipMemcpy() in ROCm 7.2.1 - Even official samples fail

> **Issue #6146**
> **状态**: closed
> **创建时间**: 2026-04-13T17:00:15Z
> **更新时间**: 2026-04-16T06:11:56Z
> **关闭时间**: 2026-04-16T06:11:56Z
> **作者**: oliveagle
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6146

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

# [gfx1151] Page Fault on hipMemcpy() in ROCm 7.2.1

## Hardware Configuration
- **GPU**: AMD Radeon 8060S (0x1586, gfx1151)
- **Architecture**: RDNA 3 (Strix Halo, iGPU)
- **CPU**: AMD Ryzen AI MAX+ 395 w/ Radeon 8060S
- **System Memory**: 128GB DDR5 (shared with GPU)
- **Compute Units**: 40

## Software Configuration
- **ROCm**: 7.2.1 (70201-81~24.04)
- **Driver**: 6.16.13
- **OS**: Ubuntu 24.04.4 LTS
- **Kernel**: Linux 6.17.0-20-generic

## Kernel Parameters
```
amdgpu.vm_fragment_size=9
amdgpu.gttsize=126976
amdgpu.no_system_mem_limit=1
amdgpu.noretry=0
ttm.pages_limit=32505856
```

## Issue Description

### Problem Summary
When attempting to perform **GPU memory copies** (`hipMemcpy`) on the **gfx1151 (Radeon 8060S iGPU)**, the program crashes with a **GPU memory access fault (page fault)**.

### ⭐ Critical Finding
**Even the OFFICIAL ROCm HIP samples fail!** This confirms it's a fundamental ROCm compatibility issue with gfx1151, not a problem with our code.

### Symptom
```
Memory access fault by GPU node-1 (Agent handle: 0x...)
on address 0x...
Reason: Page not present or supervisor privilege.
```

### What Works
- ✅ `rocm-smi` correctly identifies the GPU
- ✅ `rocminfo` shows proper HSA agents
- ✅ `hipMalloc()` successfully allocates device memory
- ✅ `hipFree()` works fine
- ✅ All device query APIs work perfectly

### What Fails
- ❌ `hipMemcpy()` (Host to Device) - **PAGE FAULT**
- ❌ `hipMemcpy()` (Device to Host) - **PAGE FAULT**
- ❌ Any GPU memory copy operation
- ❌ **OFFICIAL ROCm HIP SQUARE SAMPLE** also fails!

## Reproduction Steps

### Minimal Reproducible Example: OFFICIAL HIP Sample

The issue is reproducible with **unmodified ROCm official sample code** from `/opt/rocm/share/hip/samples/0_Intro/square/`:

```cpp
#include <stdio.h>
#include "hip/hip_runtime.h"

#define CHECK(cmd)                                                                                 \
  {                                                                                                \
    hipError_t error = cmd;                                                                        \
    if (error != hipSuccess) {                                                                     \
      fprintf(stderr, "error: '%s'(%d) at %s:%d\n", hipGetErrorString(error), error, __FILE__,     \
              __LINE__);                                                                           \
      exit(EXIT_FAILURE);                                                                          \
    }                                                                                              \
  }

template <typename T> __global__ void vector_square(T* C_d, const T* A_d, size_t N) {
  size_t offset = (blockIdx.x * blockDim.x + threadIdx.x);
  size_t stride = blockDim.x * gridDim.x;

  for (size_t i = offset; i < N; i += stride) {
    C_d[i] = A_d[i] * A_d[i];
  }
}

int main(int argc, char* argv[]) {
  float *A_d, *C_d;
  float *A_h, *C_h;
  size_t N = 1000000;
  size_t Nbytes = N * sizeof(float);
  static int device = 0;
  CHECK(hipSetDevice(device));
  hipDeviceProp_t props;
  CHECK(hipGetDeviceProperties(&props, device));
  printf("info: running on device %s\n", props.name);
#ifdef __HIP_PLATFORM_AMD__
  printf("info: architecture on AMD GPU device is: %s\n", props.gcnArchName);
#endif

  A_h = (float*)malloc(Nbytes);
  CHECK(A_h == 0 ? hipErrorOutOfMemory : hipSuccess);
  C_h = (float*)malloc(Nbytes);
  CHECK(C_h == 0 ? hipErrorOutOfMemory : hipSuccess);
  for (size_t i = 0; i < N; i++) {
    A_h[i] = 1.618f + i;
  }

  CHECK(hipMalloc(&A_d, Nbytes));
  CHECK(hipMalloc(&C_d, Nbytes));

  printf("info: copy Host2Device\n");
  CHECK(hipMemcpy(A_d, A_h, Nbytes, hipMemcpyHostToDevice));  // CRASHES HERE!

  const unsigned blocks = 512;
  const unsigned threadsPerBlock = 256;

  printf("info: launch 'vector_square' kernel\n");
  hipLaunchKernelGGL(vector_square, dim3(blocks), dim3(threadsPerBlock), 0, 0, C_d, A_d, N);

  printf("info: copy Device2Host\n");
  CHECK(hipMemcpy(C_h, C_d, Nbytes, hipMemcpyDeviceToHost));

  printf("info: check result\n");
  for (size_t i = 0; i < N; i++) {
    if (C_h[i] != A_h[i] * A_h[i]) {
      CHECK(hipErrorUnknown);
    }
  }

  CHECK(hipFree(A_d));
  CHECK(hipFree(C_d));
  free(A_h);
  free(C_h);

  printf("PASSED!\n");
}
```

### Actual Behavior (FAILED)
```
info: running on device Radeon 8060S Graphics
info: architecture on AMD GPU device is: gfx1151
info: allocate host mem (  7.63 MB)
info: allocate device mem (  7.63 MB)
info: copy Host2Device
Memory access fault by GPU node-1 (Agent handle: 0x...)
on address 0x...
Reason: Page not present or supervisor privilege.
Aborted (core dumped)
```

## Key Findings

**1. Issue is NOT permission-related**
- Running with `sudo` produces the same result
- User is already in `render` group
- Device permissions are correct

**2. Issue is NOT PyTorch-specific**
- Native HIP C++ code also fails with identical error
- **OFFICIAL ROCm HIP SAMPLES FAIL** - this is definitive proof!
- Error occurs during `hipMemcpy()` call, not during `hipMalloc()`

**3. `amdgpu.vm_fragment_size=9` helps but doesn't fully fix**
- Before: Even simple `hipMalloc()` would fail
- After: `hipMalloc()` works, but `hipMemcpy()` still fails

## Request

1. **Confirmation** that this is a known issue with gfx1151 in ROCm 7.2
2. **Guidance** on whether a fix is planned for ROCm 7.3+
3. **Suggestions** for additional kernel parameters or workarounds to try

## Additional Information Available
- Full rocminfo output
- Complete dmesg/kernel logs
- Full package list of all 65 ROCm packages
- Any additional testing or debugging requested


---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2026-04-14T18:27:18Z)

Hey @oliveagle, this does look like a known issue related to https://github.com/ROCm/TheRock/issues/2991. Could you swap onto the `6.14-1018 OEM kernel` as described in https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#prepare-the-system and also make sure to remove `amdgpu-dkms` if installed (sudo apt remove amdgpu-dkms amdgpu-dkms-firmware)?

The output of `sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES` before and after the kernel swap would also be helpful.

---

### 评论 #2 — oliveagle (2026-04-16T06:11:32Z)

## Update: Issue Resolved with OEM Kernel + vLLM ROCm Verified

Following the advice from @harkgill-amd, I swapped to the **6.14.0-1018-oem** kernel and removed `amdgpu-dkms`. The issue is now **completely resolved**.

### Changes Made

1. **Kernel**: `6.17.0-20-generic` → `6.14.0-1018-oem`
2. **Removed**: `amdgpu-dkms` (`sudo apt remove amdgpu-dkms amdgpu-dkms-firmware`)

### MES Firmware Info (After Fix)

```
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
```

### GPU Verification

```
$ rocminfo | grep -A5 "Agent 2"
  Name:                    gfx1151
  Marketing Name:          AMD Radeon Graphics
  Device Type:             GPU
  Compute Unit:            40

$ rocm-smi
Device  Node  IDs              Temp    Power     VRAM%  GPU%
0       1     0x1586,   11323  33.0C  12.08W    34%    0%
```

### vLLM ROCm Inference Verified

Successfully installed and ran **vLLM 0.19.0+rocm721** with **Qwen3-0.6B** on the Radeon 8060S:

```bash
pip install vllm --extra-index-url https://wheels.vllm.ai/rocm
```

```
vLLM version: 0.19.0
Model: Qwen3-0.6B (FP16)
Device: Radeon 8060S Graphics
Memory: 124.0 GB (unified)

Prompt: 'What is the capital of France?'
Output: ' The capital of France is Paris...'
Speed: ~26.8 tok/s output
```

### GPU Operator Benchmarks (FP16)

| Operator | Dimensions | Time | Throughput |
|----------|-----------|------|------------|
| **GEMM QKV Fusion** | 1024x1024x4608 | 0.33 ms | **29.0 TFLOPS** |
| **GEMM GateUp Fusion** | 1024x1024x9728 | 1.50 ms | **13.6 TFLOPS** |
| **GEMM Down Proj** | 1024x4864x1024 | 0.75 ms | **13.6 TFLOPS** |
| **BF16 QKV** | 1024x1024x4608 | 0.34 ms | **28.9 TFLOPS** |
| Attention Q@K^T+S@V | batch=32, seq=512 | 76 ms | OK |
| Attention Q@K^T+S@V | batch=64, seq=1024 | 488 ms | OK |
| RMSNorm | (32, 512, 1024) | 46 ms | OK |
| LayerNorm | (32, 512, 1024) | 5 ms | OK |
| RoPE | batch=32, seq=2048 | 9 ms | OK |
| SiLU / GELU / ReLU | (32, 512, 3072) | 9-18 ms | OK |
| Softmax | (32, 16, 512) | 17 ms | OK |
| Reduce Sum/Mean/Max | (32, 512, 1024) | 0.1-13 ms | OK |
| Embedding | 151936x1024, 16384 tokens | 1.8 ms | OK |

All 8 categories of GPU operators passed: GEMM (FP16/BF16), Element-wise, Normalization, Attention, RoPE, Reduction, Embedding.

### Note: vLLM Memory Profiling Patch

On ROCm unified memory systems, vLLM's memory profiling assert fails because free GPU memory can slightly *increase* between snapshots (121.49 -> 121.5 GiB). This is a known behavior with AMD APU unified memory. I patched `vllm/v1/worker/gpu_worker.py` line 408 to use a warning instead of assert.

### Summary

- **Root cause**: The `6.17.0-20-generic` kernel's `amdgpu` driver had a MES firmware incompatibility causing page faults on `hipMemcpy`
- **Fix**: Switch to `6.14.0-1018-oem` kernel and remove `amdgpu-dkms`
- **Everything now works**: PyTorch, vLLM, all GPU operators

Thanks @harkgill-amd for the guidance! This issue can be closed.

---

### 评论 #3 — oliveagle (2026-04-16T06:11:55Z)

Issue resolved. Switching to 6.14.0-1018-oem kernel and removing amdgpu-dkms fixed the page fault. All GPU operators and vLLM verified working on gfx1151.

---
