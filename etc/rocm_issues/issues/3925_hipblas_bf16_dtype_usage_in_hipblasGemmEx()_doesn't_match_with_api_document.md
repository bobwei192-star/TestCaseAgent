# hipblas_bf16 dtype usage in hipblasGemmEx() doesn't match with api document

> **Issue #3925**
> **状态**: closed
> **创建时间**: 2024-10-21T02:47:54Z
> **更新时间**: 2024-10-21T03:12:16Z
> **关闭时间**: 2024-10-21T03:12:16Z
> **作者**: ZJLi2013
> **标签**: ROCm 6.2.3, ROCm 6.2.2, mi300
> **URL**: https://github.com/ROCm/ROCm/issues/3925

## 标签

- **ROCm 6.2.3** (颜色: #ededed)
- **ROCm 6.2.2** (颜色: #ededed)
- **mi300** (颜色: #ededed)

## 描述

### Problem Description

```c++
hipblasStatus_t hipblasGemmEx(hipblasHandle_t handle, hipblasOperation_t transA, hipblasOperation_t transB, int m, int n, int k, const void *alpha, const void *A, hipblasDatatype_t aType, int lda, const void *B, hipblasDatatype_t bType, int ldb, const void *beta, void *C, hipblasDatatype_t cType, int ldc, hipblasDatatype_t computeType, hipblasGemmAlgo_t algo)

hipblasGemmEx(cublas_handle,
			   transpose_b, transpose_a,
			   m, n, k, &alpha,
			   b, HIP_R_16BF, ldb,
			   a, HIP_R_16BF, lda,
			   &beta,
			   c, HIP_R_16BF, c_cols, HIP_R_32F,
			   HIPBLAS_GEMM_DEFAULT)
```

by [hipblasGemmEx definition](https://rocm.docs.amd.com/projects/hipBLAS/en/latest/functions.html#list-of-blas-extension-functions), the data type should be used as:

|a type | b type | c type | compute type |
|---|---|---|---|
|HIP_R_16F | HIP_R_16F | HIP_R_16F | HIPBLAS_COMPUTE_32F


while in real, it give errors: 

```yml
error: no matching function for call to 'hipblasGemmEx'
   88 |   CUBLAS_CALL(hipblasGemmEx(cublas_handle,
 no known conversion from 'hipDataType'(HIP_R_16BF) to 'hipblasDatatype_t'(HIPBLAS_R_16BF) for 9th argument
``` 

I am expecting using `HIP_R_16BF` for dtype of matrix a, b; and if i replace it by `HIPBLAS_R_16BF`, it give another error that `HIPBLAS_R_16BF` is not founded.  then how to make it work then ?

 
Thanks
David 

### Operating System

Ubuntu 22.04

### CPU

Ryzen 

### GPU

mi300

### ROCm Version

ROCm 6.2.3, ROCm 6.2.2

### ROCm Component

hipBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — ZJLi2013 (2024-10-21T03:12:16Z)

ok , found a workable way:

1. add `-DHIPBLAS_V2` in cmake build flag
2. call gemmEx as  :
```c++
  CUBLAS_CALL(hipblasGemmEx(cublas_handle,
			   transpose_b, transpose_a,
			   m, n, k, &alpha,
			   b, HIP_R_16BF, ldb,
			   a, HIP_R_16BF, lda,
			   &beta,
			   c, HIP_R_16BF, c_cols, HIPBLAS_COMPUTE_32F,
			   HIPBLAS_GEMM_DEFAULT))
``` 

---
