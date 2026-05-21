# [Issue]:  Bugs of HIPBLAS and HIPBLASLT on gfx1151

> **Issue #4566**
> **状态**: closed
> **创建时间**: 2025-04-07T14:55:26Z
> **更新时间**: 2025-05-07T19:10:08Z
> **关闭时间**: 2025-05-07T19:10:07Z
> **作者**: moonshadow-25
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4566

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

# Performance Analysis of hipBLASLT for Matrix Multiplication Operations

## Summary
This report presents a comprehensive performance analysis of matrix multiplication operations using hipBLAS and hipBLASLT libraries on an AMD GPU. Our benchmarks compare the performance of both FP32 and FP16 data types across various matrix sizes to evaluate the effectiveness of hipBLASLT for accelerating matrix operations.

## Test Configuration
- Hardware: AMD Radeon Graphics (gfx1151)
- Software: ROCm 6.3.4
- Matrix sizes tested: 1024×1024, 2048×2048, 4096×4096, and 8192×8192
- Operations: General Matrix Multiplication (GEMM)
- Data types: FP32 and FP16
- Libraries: Standard hipBLAS and hipBLASLT

## Key Findings

### Performance Metrics (in TFLOPS)
| Matrix Size | FP32 (hipBLAS) | FP16 (hipBLAS) | FP32 (hipBLASLT) | FP16 (hipBLASLT) | Speedup: FP16LT vs FP32LT |
|-------------|----------------|----------------|------------------|------------------|---------------------------|
| 1024        | 4.71           | 4.19           | 1.16             | 13.02            | 11.26x                    |
| 2048        | 5.28           | 3.87           | 1.00             | 32.07            | 32.04x                    |
| 4096        | 5.24           | 6.60           | 0.41             | 23.94            | 58.24x                    |
| 8192        | 5.04           | 4.53           | 0.16             | 14.31            | 89.69x                    |

### Observations
1. **hipBLASLT excels with FP16 operations**: The hipBLASLT library delivers exceptional performance for FP16 matrix multiplication, achieving up to 32.07 TFLOPS for 2048×2048 matrices - a 6x improvement over standard hipBLAS.

2. **FP32 performance degradation with hipBLASLT**: Interestingly, when using FP32 data types, hipBLASLT performs significantly worse than standard hipBLAS, with performance decreasing as matrix size increases.

3. **Dramatic FP16 vs FP32 speedup in hipBLASLT**: The performance gap between FP16 and FP32 in hipBLASLT grows substantially with matrix size, reaching an impressive 89.69x speedup for 8192×8192 matrices.

4. **Optimal matrix size**: For FP16 operations with hipBLASLT, 2048×2048 matrices demonstrated the best performance at 32.07 TFLOPS.

## Implications

1. **Targeted optimization**: hipBLASLT appears to be specifically optimized for FP16 matrix operations, likely leveraging AMD GPU Tensor Core hardware acceleration.

2. **Mixed precision consideration**: Applications requiring high performance should consider using FP16 with hipBLASLT for matrix multiplication operations while keeping FP32 operations on standard hipBLAS.

3. **Application-specific tuning**: The performance characteristics suggest that matrix size selection can significantly impact performance, with mid-size matrices (2048×2048) showing optimal results for FP16 operations.

## Conclusion

hipBLASLT delivers remarkable performance improvements for FP16 matrix multiplication operations, making it an excellent choice for applications that can leverage half-precision arithmetic. However, developers should be aware of its poor performance with FP32 operations and plan their implementation strategies accordingly. This specialized behavior suggests hipBLASLT is designed primarily to accelerate tensor operations using hardware-specific features of AMD GPUs.

These findings could be valuable for machine learning frameworks and other high-performance computing applications looking to optimize matrix operations on AMD GPUs.


### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

AMD AI MAX+ 395

### GPU

GFX1151

### ROCm Version

ROCM 6.3.4

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

### 评论 #1 — darren-amd (2025-05-07T19:10:07Z)

Hi @moonshadow-25,

This appears to be a duplicate of https://github.com/ROCm/ROCm/issues/4499, lets centralize our discussion there. Thanks!

---
