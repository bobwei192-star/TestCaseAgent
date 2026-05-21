# Recommended TFLOPs benchmark script

> **Issue #5923**
> **状态**: closed
> **创建时间**: 2026-02-02T17:58:36Z
> **更新时间**: 2026-05-12T17:40:49Z
> **关闭时间**: 2026-05-12T17:40:49Z
> **作者**: josef-hak
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5923

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- benrichard-amd

## 描述

Hey,

 please, how can I verify TFLOPs values shown here <https://www.amd.com/en/products/accelerators/instinct/mi300/mi325x.html#tabs-27754605c8-item-1cfc3fe320-tab>?

I am trying to verify that using my pytorch script:

~~~python
import torch
import time

# Make sure you're on ROCm
assert torch.version.hip is not None

device = "cuda"

M = N = K = 2**14

# dtype = torch.float32 # FP32 (Vector)
dtype = torch.float64 # FP64 (Vector)

A = torch.randn((M, K), device=device, dtype=dtype)
B = torch.randn((K, N), device=device, dtype=dtype)

# Warmup
for _ in range(10):
    C = torch.matmul(A, B)

torch.cuda.synchronize()

# Timed runs
iters = 20
start = time.time()
for _ in range(iters):
    C = torch.matmul(A, B)

torch.cuda.synchronize()
elapsed = time.time() - start

# FLOPs calculation
flops = 2 * M * N * K * iters
tflops = flops / elapsed / 1e12

print(f"Elapsed time: {elapsed:.3f} s")
print(f"GEMM Throughput: {tflops:.1f} TFLOPs")
~~~

I am getting 82.4 TFLOPs for float64 and 130.6 float32. I actually expected something like 164 TFLOPs for float64 as the script makes matrix multiplication.
 
Please provide some script (preferably bash, python - pytorch, etc.) I can use in my stack:
- Ubuntu 22.04
- CPU: AMD EPYC 9965
- GPU: AMD MI325x

Thanks in advance

---

## 评论 (2 条)

### 评论 #1 — benrichard-amd (2026-03-05T16:55:29Z)

Hi @Josca ,

You probably won't get much higher than this for FP64 GEMM. Remember that FP64 requires 2x memory, bandwidth, registers, etc. as FP32. Memory is the bottle-neck.

The figure on the spec sheet is the theoretical peak. It's the clock speed multiplied by the number of floating-point operations per clock. If you just want to verify this number, there are microbenchmarks that test only the matrix cores and don't involve moving data in/out of the GPU.

For instance, rocprofiler-compute has a built-in benchmark

```
git clone https://github.com/ROCm/rocm-systems.git
cd rocm-systems/projects/rocprofiler-compute
PYTHONPATH=src python src/utils/benchmark.py
```

```
Peak MFMA FLOPs (F64), GPU ID: 0, workgroupSize:256, workgroups:38912, experiments:100, FLOP:637534208000, duration:4.34 ms, mean:147052.7 GFLOPS, stdev:1025.3 GFLOPS
```

Let me know if you have any other questions.

Thanks!

---

### 评论 #2 — benrichard-amd (2026-05-12T17:40:49Z)

Closing as submitter has no further questions.

---
