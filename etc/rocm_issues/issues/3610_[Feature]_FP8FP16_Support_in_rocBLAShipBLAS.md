# [Feature]: FP8/FP16 Support in rocBLAS/hipBLAS

> **Issue #3610**
> **状态**: closed
> **创建时间**: 2024-08-19T19:21:19Z
> **更新时间**: 2025-06-25T18:38:34Z
> **关闭时间**: 2025-06-25T18:38:34Z
> **作者**: garrettbyrd
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3610

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Low-precision tensor operations are rising in usage as techniques such as LLM quantization gain traction in contemporary machine learning ecosystems. As such, it is appropriate to arm lower-level toolkits such as `hipBLAS` with the appropriate functionality to accommodate models and tools that utilize lower-precision operations. 

There is already some non-`FP32`/`FP64` precision support available in the hipBLAS API, but this support is quite limited. Brain floating point is only supported by the Level 1 `dot` operation (`hipblasBfdot`) and its `Batched`/`Stridedbatched` extensions. Similarly, the datatype `hipblasHalf` is only supported in the Level 1 `axpy` and Level 3 `gemm` operations (and their extensions). Curiously, there is no `hipblasHalf` support in the Level 2 `gemv` operation.

`hipBLASLt` already provides functionality for a variety of lower/mixed precision, including `FP16`, `FP8`, `BF16`, `BF8`, and `INT8`. This focus is reasonable; in AI models such as the transformer model, `gemm` is overwhelmingly the most relevant and necessary operation. However, expanding the `hipBLAS` datatype support for lower precisions (at least `FP16` and `FP8`) would provide a more expansive toolkit for various research areas, namely AI and HPC.

Even providing initial support in the "core" tensor operations (`axpy`, `gemv`, `gemm`) would be sufficient for many application areas, such as benchmarking for these precisions.

I also acknowledge that _full_ cross-platform support in `hipBLAS` would require support from both `rocBLAS` and `cuBLAS`, thus the mention of `rocBLAS`.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

hipBLAS

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-08-22T18:24:12Z)

Hi @garrettbyrd, there are currently no plans to introduce FP8/FP16 support. 

Could you please provide more details on the types of applications that would benefit from these features? It would be even better if you could point us to any open-source packages that could leverage this added support. Thanks!

---

### 评论 #2 — IMbackK (2024-09-05T09:53:03Z)

for fp16 gmmv there is rocblas_hshgemv_batched in rocblas, but its not very fast

---
