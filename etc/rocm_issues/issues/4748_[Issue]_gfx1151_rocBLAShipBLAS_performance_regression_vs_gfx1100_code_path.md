# [Issue]: gfx1151 rocBLAS/hipBLAS performance regression vs gfx1100 code path

> **Issue #4748**
> **状态**: open
> **创建时间**: 2025-05-16T04:40:41Z
> **更新时间**: 2026-05-05T21:41:29Z
> **作者**: lhl
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4748

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I've been testing Strix Halo (gfx1100) hardware and rocBLAS performance is unexpectedly bad - see my llama.cpp issue report for some more details: https://github.com/ggml-org/llama.cpp/issues/13565

Running llama.cpp's `test-backend-ops perf -o MUL_MAT` test on gfx1151, there is a 2X performance difference if I use rocBLAS with gfx1151 vs gfx1100 kernels:

```
❯ llama.cpp-hip/build/bin/test-backend-ops perf -o MUL_MAT
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32
Testing 2 devices

Backend 1/2: ROCm0
  Device description: AMD Radeon Graphics
  Device memory: 104906 MB (104742 MB free)

  MUL_MAT(type_a=f16,type_b=f32,m=16416,n=1,k=128,bs=[8,1],nr=[4,1],per=[0,2,1,3],v=0):                  744 runs -  9930.30 us/run - 134.48 MFLOP/run -  13.54 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=128,n=1,k=16416,bs=[8,1],nr=[4,1],per=[0,1,2,3],v=1):                 4464 runs -   261.01 us/run - 134.48 MFLOP/run - 515.23 GFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1704 runs -  1090.25 us/run - 117.44 MFLOP/run - 107.72 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1704 runs -   587.86 us/run - 117.44 MFLOP/run - 199.78 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               1704 runs -   587.41 us/run - 117.44 MFLOP/run - 199.93 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              22152 runs -    45.68 us/run - 117.44 MFLOP/run -   2.57 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7668 runs -   132.88 us/run - 117.44 MFLOP/run - 883.83 GFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5964 runs -   187.44 us/run - 117.44 MFLOP/run - 626.55 GFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   213.08 us/run - 117.44 MFLOP/run - 551.15 GFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4260 runs -   287.25 us/run - 117.44 MFLOP/run - 408.84 GFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              15336 runs -    68.43 us/run - 117.44 MFLOP/run -   1.72 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7668 runs -   132.25 us/run - 117.44 MFLOP/run - 887.99 GFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              11076 runs -    93.84 us/run - 117.44 MFLOP/run -   1.25 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   203.23 us/run - 117.44 MFLOP/run - 577.86 GFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   229.97 us/run - 117.44 MFLOP/run - 510.67 GFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    7668 runs -   137.48 us/run - 117.44 MFLOP/run - 854.21 GFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    10224 runs -   101.01 us/run - 117.44 MFLOP/run -   1.16 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              7668 runs -   143.33 us/run - 117.44 MFLOP/run - 819.37 GFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                   10224 runs -   102.11 us/run - 117.44 MFLOP/run -   1.15 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             22152 runs -    46.19 us/run - 117.44 MFLOP/run -   2.54 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             20448 runs -    49.60 us/run - 117.44 MFLOP/run -   2.37 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    14484 runs -    72.38 us/run - 117.44 MFLOP/run -   1.62 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              7668 runs -   145.98 us/run - 117.44 MFLOP/run - 804.49 GFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    18744 runs -    53.77 us/run - 117.44 MFLOP/run -   2.18 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 426 runs -  2870.91 us/run - 234.88 MFLOP/run -  81.81 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 852 runs -  1820.67 us/run - 234.88 MFLOP/run - 129.01 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                426 runs -  5557.84 us/run - 234.88 MFLOP/run -  42.26 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              17892 runs -    56.39 us/run - 234.88 MFLOP/run -   4.17 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7242 runs -   139.84 us/run - 234.88 MFLOP/run -   1.68 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5538 runs -   190.16 us/run - 234.88 MFLOP/run -   1.24 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4686 runs -   217.05 us/run - 234.88 MFLOP/run -   1.08 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3834 runs -   288.37 us/run - 234.88 MFLOP/run - 814.52 GFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               9798 runs -   104.39 us/run - 234.88 MFLOP/run -   2.25 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6816 runs -   154.67 us/run - 234.88 MFLOP/run -   1.52 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               8094 runs -   126.92 us/run - 234.88 MFLOP/run -   1.85 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4260 runs -   235.60 us/run - 234.88 MFLOP/run - 996.94 GFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4686 runs -   231.78 us/run - 234.88 MFLOP/run -   1.01 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    6816 runs -   148.62 us/run - 234.88 MFLOP/run -   1.58 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     9372 runs -   111.46 us/run - 234.88 MFLOP/run -   2.11 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6816 runs -   155.33 us/run - 234.88 MFLOP/run -   1.51 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    8946 runs -   112.38 us/run - 234.88 MFLOP/run -   2.09 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             16188 runs -    62.57 us/run - 234.88 MFLOP/run -   3.75 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             15336 runs -    66.92 us/run - 234.88 MFLOP/run -   3.51 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    11502 runs -    87.31 us/run - 234.88 MFLOP/run -   2.69 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6816 runs -   155.05 us/run - 234.88 MFLOP/run -   1.51 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    14910 runs -    68.88 us/run - 234.88 MFLOP/run -   3.41 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 568 runs -  2907.10 us/run - 352.32 MFLOP/run - 121.19 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 568 runs -  1816.06 us/run - 352.32 MFLOP/run - 194.00 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                284 runs -  5758.26 us/run - 352.32 MFLOP/run -  61.19 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              13064 runs -    78.03 us/run - 352.32 MFLOP/run -   4.51 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5964 runs -   170.39 us/run - 352.32 MFLOP/run -   2.07 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5396 runs -   194.17 us/run - 352.32 MFLOP/run -   1.81 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4828 runs -   218.78 us/run - 352.32 MFLOP/run -   1.61 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3692 runs -   291.35 us/run - 352.32 MFLOP/run -   1.21 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7384 runs -   139.20 us/run - 352.32 MFLOP/run -   2.53 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5680 runs -   179.43 us/run - 352.32 MFLOP/run -   1.96 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6532 runs -   153.43 us/run - 352.32 MFLOP/run -   2.30 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3976 runs -   270.36 us/run - 352.32 MFLOP/run -   1.30 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4260 runs -   238.10 us/run - 352.32 MFLOP/run -   1.48 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    6248 runs -   161.69 us/run - 352.32 MFLOP/run -   2.18 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     7952 runs -   126.87 us/run - 352.32 MFLOP/run -   2.78 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5964 runs -   169.90 us/run - 352.32 MFLOP/run -   2.07 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    8236 runs -   123.76 us/run - 352.32 MFLOP/run -   2.85 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             12780 runs -    79.01 us/run - 352.32 MFLOP/run -   4.46 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             11360 runs -    88.43 us/run - 352.32 MFLOP/run -   3.98 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    10508 runs -    97.46 us/run - 352.32 MFLOP/run -   3.61 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6248 runs -   164.77 us/run - 352.32 MFLOP/run -   2.14 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    11644 runs -    87.97 us/run - 352.32 MFLOP/run -   4.01 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 426 runs -  2974.42 us/run - 469.76 MFLOP/run - 157.93 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 639 runs -  1827.80 us/run - 469.76 MFLOP/run - 257.01 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                213 runs -  5619.75 us/run - 469.76 MFLOP/run -  83.59 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              11076 runs -    91.72 us/run - 469.76 MFLOP/run -   5.12 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6390 runs -   160.57 us/run - 469.76 MFLOP/run -   2.93 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   198.39 us/run - 469.76 MFLOP/run -   2.37 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4473 runs -   232.96 us/run - 469.76 MFLOP/run -   2.02 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3408 runs -   294.11 us/run - 469.76 MFLOP/run -   1.60 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5964 runs -   172.12 us/run - 469.76 MFLOP/run -   2.73 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4047 runs -   259.36 us/run - 469.76 MFLOP/run -   1.81 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   202.78 us/run - 469.76 MFLOP/run -   2.32 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3408 runs -   293.80 us/run - 469.76 MFLOP/run -   1.60 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4047 runs -   247.30 us/run - 469.76 MFLOP/run -   1.90 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    5751 runs -   174.78 us/run - 469.76 MFLOP/run -   2.69 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     7242 runs -   141.23 us/run - 469.76 MFLOP/run -   3.33 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5325 runs -   189.41 us/run - 469.76 MFLOP/run -   2.48 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    7242 runs -   139.61 us/run - 469.76 MFLOP/run -   3.36 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             10650 runs -    95.28 us/run - 469.76 MFLOP/run -   4.93 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              9585 runs -   104.67 us/run - 469.76 MFLOP/run -   4.49 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     9159 runs -   110.76 us/run - 469.76 MFLOP/run -   4.24 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5751 runs -   175.47 us/run - 469.76 MFLOP/run -   2.68 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    10011 runs -   101.16 us/run - 469.76 MFLOP/run -   4.64 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 342 runs -  2971.47 us/run - 587.20 MFLOP/run - 197.61 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 684 runs -  1831.17 us/run - 587.20 MFLOP/run - 320.67 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                342 runs -  5760.27 us/run - 587.20 MFLOP/run - 101.94 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               9234 runs -   109.02 us/run - 587.20 MFLOP/run -   5.39 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6156 runs -   164.27 us/run - 587.20 MFLOP/run -   3.57 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4959 runs -   203.76 us/run - 587.20 MFLOP/run -   2.88 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4446 runs -   226.35 us/run - 587.20 MFLOP/run -   2.59 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3420 runs -   297.54 us/run - 587.20 MFLOP/run -   1.97 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4788 runs -   209.28 us/run - 587.20 MFLOP/run -   2.81 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3762 runs -   268.29 us/run - 587.20 MFLOP/run -   2.19 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4275 runs -   240.57 us/run - 587.20 MFLOP/run -   2.44 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3249 runs -   321.27 us/run - 587.20 MFLOP/run -   1.83 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3933 runs -   257.20 us/run - 587.20 MFLOP/run -   2.28 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    5472 runs -   188.21 us/run - 587.20 MFLOP/run -   3.12 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5814 runs -   175.27 us/run - 587.20 MFLOP/run -   3.35 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              4788 runs -   214.01 us/run - 587.20 MFLOP/run -   2.74 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    6669 runs -   151.51 us/run - 587.20 MFLOP/run -   3.88 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              9234 runs -   108.93 us/run - 587.20 MFLOP/run -   5.39 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              7866 runs -   128.44 us/run - 587.20 MFLOP/run -   4.57 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     8037 runs -   126.04 us/run - 587.20 MFLOP/run -   4.66 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5472 runs -   184.44 us/run - 587.20 MFLOP/run -   3.18 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     8892 runs -   113.42 us/run - 587.20 MFLOP/run -   5.18 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 428 runs -  3066.53 us/run - 939.52 MFLOP/run - 306.38 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 642 runs -  1831.45 us/run - 939.52 MFLOP/run - 512.99 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                214 runs -  5735.47 us/run - 939.52 MFLOP/run - 163.81 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6206 runs -   163.79 us/run - 939.52 MFLOP/run -   5.74 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5243 runs -   194.27 us/run - 939.52 MFLOP/run -   4.84 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4494 runs -   225.63 us/run - 939.52 MFLOP/run -   4.16 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4280 runs -   239.53 us/run - 939.52 MFLOP/run -   3.92 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3210 runs -   313.99 us/run - 939.52 MFLOP/run -   2.99 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3103 runs -   323.30 us/run - 939.52 MFLOP/run -   2.91 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               2782 runs -   364.95 us/run - 939.52 MFLOP/run -   2.57 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               2675 runs -   375.36 us/run - 939.52 MFLOP/run -   2.50 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               2247 runs -   462.89 us/run - 939.52 MFLOP/run -   2.03 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3210 runs -   321.86 us/run - 939.52 MFLOP/run -   2.92 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    3959 runs -   258.96 us/run - 939.52 MFLOP/run -   3.63 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5136 runs -   196.14 us/run - 939.52 MFLOP/run -   4.79 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              3959 runs -   258.99 us/run - 939.52 MFLOP/run -   3.63 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    4815 runs -   210.25 us/run - 939.52 MFLOP/run -   4.47 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6420 runs -   157.70 us/run - 939.52 MFLOP/run -   5.96 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5243 runs -   192.33 us/run - 939.52 MFLOP/run -   4.89 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5778 runs -   175.31 us/run - 939.52 MFLOP/run -   5.36 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              4387 runs -   230.05 us/run - 939.52 MFLOP/run -   4.08 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5778 runs -   173.46 us/run - 939.52 MFLOP/run -   5.42 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                94 runs - 10681.19 us/run -  60.13 GFLOP/run -   5.63 TFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                82 runs - 12307.23 us/run -  60.13 GFLOP/run -   4.89 TFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       72 runs - 14260.00 us/run -  60.13 GFLOP/run -   4.22 TFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       76 runs - 13367.83 us/run -  60.13 GFLOP/run -   4.50 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       76 runs - 13244.86 us/run -  60.13 GFLOP/run -   4.54 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       76 runs - 13461.76 us/run -  60.13 GFLOP/run -   4.47 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       78 runs - 12874.67 us/run -  60.13 GFLOP/run -   4.67 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       76 runs - 13325.63 us/run -  60.13 GFLOP/run -   4.51 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       80 runs - 12743.34 us/run -  60.13 GFLOP/run -   4.72 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       78 runs - 13003.81 us/run -  60.13 GFLOP/run -   4.62 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       78 runs - 12892.40 us/run -  60.13 GFLOP/run -   4.66 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       78 runs - 13015.83 us/run -  60.13 GFLOP/run -   4.62 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                       78 runs - 12923.68 us/run -  60.13 GFLOP/run -   4.65 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    78 runs - 12871.58 us/run -  60.13 GFLOP/run -   4.67 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     80 runs - 12796.90 us/run -  60.13 GFLOP/run -   4.70 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      78 runs - 12940.40 us/run -  60.13 GFLOP/run -   4.65 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    78 runs - 12850.27 us/run -  60.13 GFLOP/run -   4.68 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      78 runs - 12875.51 us/run -  60.13 GFLOP/run -   4.67 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      78 runs - 12890.06 us/run -  60.13 GFLOP/run -   4.66 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     78 runs - 12859.42 us/run -  60.13 GFLOP/run -   4.68 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      78 runs - 12839.21 us/run -  60.13 GFLOP/run -   4.68 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     78 runs - 12825.08 us/run -  60.13 GFLOP/run -   4.69 TFLOPS
  Backend ROCm0: OK

...

❯ HSA_OVERRIDE_GFX_VERSION=11.0.0 llama.cpp-hip/build/bin/test-backend-ops perf -o MUL_MAT
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, gfx1100 (0x1100), VMM: no, Wave Size: 32
Testing 2 devices

Backend 1/2: ROCm0
  Device description: AMD Radeon Graphics
  Device memory: 104906 MB (104742 MB free)

  MUL_MAT(type_a=f16,type_b=f32,m=16416,n=1,k=128,bs=[8,1],nr=[4,1],per=[0,2,1,3],v=0):                  744 runs -  1709.42 us/run - 134.48 MFLOP/run -  78.67 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=128,n=1,k=16416,bs=[8,1],nr=[4,1],per=[0,1,2,3],v=1):                 4464 runs -   263.71 us/run - 134.48 MFLOP/run - 509.96 GFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1704 runs -  1091.71 us/run - 117.44 MFLOP/run - 107.57 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1704 runs -   595.41 us/run - 117.44 MFLOP/run - 197.24 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               1704 runs -   593.69 us/run - 117.44 MFLOP/run - 197.81 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              23004 runs -    44.95 us/run - 117.44 MFLOP/run -   2.61 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7668 runs -   133.59 us/run - 117.44 MFLOP/run - 879.12 GFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5964 runs -   187.25 us/run - 117.44 MFLOP/run - 627.20 GFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   213.30 us/run - 117.44 MFLOP/run - 550.58 GFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4260 runs -   286.58 us/run - 117.44 MFLOP/run - 409.79 GFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              15336 runs -    68.20 us/run - 117.44 MFLOP/run -   1.72 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7668 runs -   131.58 us/run - 117.44 MFLOP/run - 892.54 GFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              11076 runs -    93.74 us/run - 117.44 MFLOP/run -   1.25 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   203.25 us/run - 117.44 MFLOP/run - 577.82 GFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   229.98 us/run - 117.44 MFLOP/run - 510.65 GFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    7668 runs -   138.47 us/run - 117.44 MFLOP/run - 848.16 GFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    10224 runs -   100.82 us/run - 117.44 MFLOP/run -   1.16 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              7668 runs -   143.42 us/run - 117.44 MFLOP/run - 818.88 GFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                   10224 runs -   102.44 us/run - 117.44 MFLOP/run -   1.15 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             22152 runs -    46.86 us/run - 117.44 MFLOP/run -   2.51 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             20448 runs -    50.12 us/run - 117.44 MFLOP/run -   2.34 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    15336 runs -    65.65 us/run - 117.44 MFLOP/run -   1.79 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              7668 runs -   146.33 us/run - 117.44 MFLOP/run - 802.58 GFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=1,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    18744 runs -    53.73 us/run - 117.44 MFLOP/run -   2.19 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 426 runs -  2518.50 us/run - 234.88 MFLOP/run -  93.26 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1278 runs -  1086.29 us/run - 234.88 MFLOP/run - 216.22 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               1704 runs -   625.27 us/run - 234.88 MFLOP/run - 375.65 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              17040 runs -    58.76 us/run - 234.88 MFLOP/run -   4.00 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7242 runs -   140.98 us/run - 234.88 MFLOP/run -   1.67 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5538 runs -   189.56 us/run - 234.88 MFLOP/run -   1.24 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4686 runs -   217.53 us/run - 234.88 MFLOP/run -   1.08 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3834 runs -   288.10 us/run - 234.88 MFLOP/run - 815.27 GFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               9798 runs -   104.04 us/run - 234.88 MFLOP/run -   2.26 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6816 runs -   154.91 us/run - 234.88 MFLOP/run -   1.52 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               8520 runs -   119.33 us/run - 234.88 MFLOP/run -   1.97 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4260 runs -   236.05 us/run - 234.88 MFLOP/run - 995.05 GFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4686 runs -   233.15 us/run - 234.88 MFLOP/run -   1.01 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    6816 runs -   149.38 us/run - 234.88 MFLOP/run -   1.57 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     9372 runs -   111.49 us/run - 234.88 MFLOP/run -   2.11 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6816 runs -   155.15 us/run - 234.88 MFLOP/run -   1.51 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    8946 runs -   112.20 us/run - 234.88 MFLOP/run -   2.09 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             16188 runs -    62.89 us/run - 234.88 MFLOP/run -   3.73 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             14910 runs -    67.87 us/run - 234.88 MFLOP/run -   3.46 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    11502 runs -    87.19 us/run - 234.88 MFLOP/run -   2.69 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6816 runs -   154.93 us/run - 234.88 MFLOP/run -   1.52 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=2,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    14484 runs -    69.13 us/run - 234.88 MFLOP/run -   3.40 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 568 runs -  2518.92 us/run - 352.32 MFLOP/run - 139.87 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1136 runs -  1086.60 us/run - 352.32 MFLOP/run - 324.24 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               1704 runs -   625.67 us/run - 352.32 MFLOP/run - 563.11 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              13064 runs -    78.13 us/run - 352.32 MFLOP/run -   4.51 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5964 runs -   168.09 us/run - 352.32 MFLOP/run -   2.10 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5396 runs -   193.99 us/run - 352.32 MFLOP/run -   1.82 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4828 runs -   219.97 us/run - 352.32 MFLOP/run -   1.60 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3692 runs -   290.77 us/run - 352.32 MFLOP/run -   1.21 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               7384 runs -   139.46 us/run - 352.32 MFLOP/run -   2.53 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5680 runs -   178.67 us/run - 352.32 MFLOP/run -   1.97 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6248 runs -   161.50 us/run - 352.32 MFLOP/run -   2.18 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3976 runs -   270.17 us/run - 352.32 MFLOP/run -   1.30 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4260 runs -   238.56 us/run - 352.32 MFLOP/run -   1.48 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    6248 runs -   161.97 us/run - 352.32 MFLOP/run -   2.18 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     7952 runs -   126.21 us/run - 352.32 MFLOP/run -   2.79 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5964 runs -   169.73 us/run - 352.32 MFLOP/run -   2.08 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    8236 runs -   124.08 us/run - 352.32 MFLOP/run -   2.84 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             12780 runs -    79.47 us/run - 352.32 MFLOP/run -   4.43 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             11360 runs -    88.46 us/run - 352.32 MFLOP/run -   3.98 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    10224 runs -    98.64 us/run - 352.32 MFLOP/run -   3.57 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6248 runs -   165.08 us/run - 352.32 MFLOP/run -   2.13 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=3,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    11644 runs -    87.79 us/run - 352.32 MFLOP/run -   4.01 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 426 runs -  2529.64 us/run - 469.76 MFLOP/run - 185.70 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1065 runs -  1091.47 us/run - 469.76 MFLOP/run - 430.40 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               1704 runs -   625.57 us/run - 469.76 MFLOP/run - 750.94 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              10863 runs -    92.99 us/run - 469.76 MFLOP/run -   5.05 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6390 runs -   157.82 us/run - 469.76 MFLOP/run -   2.98 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   198.61 us/run - 469.76 MFLOP/run -   2.37 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4473 runs -   233.16 us/run - 469.76 MFLOP/run -   2.01 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3408 runs -   293.83 us/run - 469.76 MFLOP/run -   1.60 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5964 runs -   173.85 us/run - 469.76 MFLOP/run -   2.70 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4047 runs -   257.95 us/run - 469.76 MFLOP/run -   1.82 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5112 runs -   201.31 us/run - 469.76 MFLOP/run -   2.33 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3408 runs -   294.87 us/run - 469.76 MFLOP/run -   1.59 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4047 runs -   247.92 us/run - 469.76 MFLOP/run -   1.89 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    5751 runs -   174.97 us/run - 469.76 MFLOP/run -   2.68 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     7242 runs -   140.97 us/run - 469.76 MFLOP/run -   3.33 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5538 runs -   184.97 us/run - 469.76 MFLOP/run -   2.54 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    7455 runs -   137.09 us/run - 469.76 MFLOP/run -   3.43 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):             10650 runs -    95.54 us/run - 469.76 MFLOP/run -   4.92 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              9585 runs -   104.39 us/run - 469.76 MFLOP/run -   4.50 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     9159 runs -   111.28 us/run - 469.76 MFLOP/run -   4.22 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5751 runs -   176.45 us/run - 469.76 MFLOP/run -   2.66 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=4,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    10011 runs -   101.45 us/run - 469.76 MFLOP/run -   4.63 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 513 runs -  2523.74 us/run - 587.20 MFLOP/run - 232.67 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                1026 runs -  1094.21 us/run - 587.20 MFLOP/run - 536.65 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               1710 runs -   626.04 us/run - 587.20 MFLOP/run - 937.97 GFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               9234 runs -   109.00 us/run - 587.20 MFLOP/run -   5.39 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5985 runs -   167.47 us/run - 587.20 MFLOP/run -   3.51 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4959 runs -   203.88 us/run - 587.20 MFLOP/run -   2.88 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4446 runs -   225.63 us/run - 587.20 MFLOP/run -   2.60 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3420 runs -   297.15 us/run - 587.20 MFLOP/run -   1.98 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4788 runs -   210.69 us/run - 587.20 MFLOP/run -   2.79 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3762 runs -   268.60 us/run - 587.20 MFLOP/run -   2.19 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4275 runs -   240.11 us/run - 587.20 MFLOP/run -   2.45 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3078 runs -   330.14 us/run - 587.20 MFLOP/run -   1.78 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3933 runs -   256.15 us/run - 587.20 MFLOP/run -   2.29 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    5472 runs -   188.25 us/run - 587.20 MFLOP/run -   3.12 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5643 runs -   180.13 us/run - 587.20 MFLOP/run -   3.26 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              4788 runs -   214.48 us/run - 587.20 MFLOP/run -   2.74 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    6669 runs -   151.03 us/run - 587.20 MFLOP/run -   3.89 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              9234 runs -   109.05 us/run - 587.20 MFLOP/run -   5.38 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              8037 runs -   125.40 us/run - 587.20 MFLOP/run -   4.68 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     8037 runs -   126.59 us/run - 587.20 MFLOP/run -   4.64 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5472 runs -   183.69 us/run - 587.20 MFLOP/run -   3.20 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=5,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     8892 runs -   113.56 us/run - 587.20 MFLOP/run -   5.17 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 428 runs -  2535.39 us/run - 939.52 MFLOP/run - 370.56 GFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                 963 runs -  1103.59 us/run - 939.52 MFLOP/run - 851.34 GFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               1605 runs -   627.17 us/run - 939.52 MFLOP/run -   1.50 TFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               6206 runs -   163.42 us/run - 939.52 MFLOP/run -   5.75 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               5136 runs -   195.31 us/run - 939.52 MFLOP/run -   4.81 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4494 runs -   224.14 us/run - 939.52 MFLOP/run -   4.19 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               4173 runs -   239.65 us/run - 939.52 MFLOP/run -   3.92 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3210 runs -   314.30 us/run - 939.52 MFLOP/run -   2.99 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3103 runs -   322.95 us/run - 939.52 MFLOP/run -   2.91 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               2782 runs -   368.17 us/run - 939.52 MFLOP/run -   2.55 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               2675 runs -   374.34 us/run - 939.52 MFLOP/run -   2.51 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               2247 runs -   462.55 us/run - 939.52 MFLOP/run -   2.03 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               3103 runs -   322.90 us/run - 939.52 MFLOP/run -   2.91 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    3959 runs -   258.82 us/run - 939.52 MFLOP/run -   3.63 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5136 runs -   196.33 us/run - 939.52 MFLOP/run -   4.79 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              3959 runs -   258.47 us/run - 939.52 MFLOP/run -   3.63 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    4815 runs -   209.54 us/run - 939.52 MFLOP/run -   4.48 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              6313 runs -   158.47 us/run - 939.52 MFLOP/run -   5.93 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              5243 runs -   191.33 us/run - 939.52 MFLOP/run -   4.91 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5778 runs -   176.09 us/run - 939.52 MFLOP/run -   5.34 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):              4387 runs -   230.43 us/run - 939.52 MFLOP/run -   4.08 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=8,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     5778 runs -   174.31 us/run - 939.52 MFLOP/run -   5.39 TFLOPS
  MUL_MAT(type_a=f32,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               120 runs -  8371.19 us/run -  60.13 GFLOP/run -   7.18 TFLOPS
  MUL_MAT(type_a=f16,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):               198 runs -  5068.70 us/run -  60.13 GFLOP/run -  11.86 TFLOPS
  MUL_MAT(type_a=bf16,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      196 runs -  5120.82 us/run -  60.13 GFLOP/run -  11.74 TFLOPS
  MUL_MAT(type_a=q4_0,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      174 runs -  5765.95 us/run -  60.13 GFLOP/run -  10.43 TFLOPS
  MUL_MAT(type_a=q4_1,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      174 runs -  5789.61 us/run -  60.13 GFLOP/run -  10.39 TFLOPS
  MUL_MAT(type_a=q5_0,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      172 runs -  5823.52 us/run -  60.13 GFLOP/run -  10.33 TFLOPS
  MUL_MAT(type_a=q5_1,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      172 runs -  5825.00 us/run -  60.13 GFLOP/run -  10.32 TFLOPS
  MUL_MAT(type_a=q8_0,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      170 runs -  5948.59 us/run -  60.13 GFLOP/run -  10.11 TFLOPS
  MUL_MAT(type_a=q2_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      176 runs -  5687.52 us/run -  60.13 GFLOP/run -  10.57 TFLOPS
  MUL_MAT(type_a=q3_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      174 runs -  5753.45 us/run -  60.13 GFLOP/run -  10.45 TFLOPS
  MUL_MAT(type_a=q4_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      174 runs -  5788.98 us/run -  60.13 GFLOP/run -  10.39 TFLOPS
  MUL_MAT(type_a=q5_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      172 runs -  5860.98 us/run -  60.13 GFLOP/run -  10.26 TFLOPS
  MUL_MAT(type_a=q6_K,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                      174 runs -  5808.25 us/run -  60.13 GFLOP/run -  10.35 TFLOPS
  MUL_MAT(type_a=iq2_xxs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                   178 runs -  5671.07 us/run -  60.13 GFLOP/run -  10.60 TFLOPS
  MUL_MAT(type_a=iq2_xs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    178 runs -  5673.10 us/run -  60.13 GFLOP/run -  10.60 TFLOPS
  MUL_MAT(type_a=iq2_s,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     176 runs -  5685.17 us/run -  60.13 GFLOP/run -  10.58 TFLOPS
  MUL_MAT(type_a=iq3_xxs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                   176 runs -  5721.26 us/run -  60.13 GFLOP/run -  10.51 TFLOPS
  MUL_MAT(type_a=iq1_s,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     178 runs -  5657.11 us/run -  60.13 GFLOP/run -  10.63 TFLOPS
  MUL_MAT(type_a=iq1_m,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     178 runs -  5671.78 us/run -  60.13 GFLOP/run -  10.60 TFLOPS
  MUL_MAT(type_a=iq4_nl,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    176 runs -  5748.09 us/run -  60.13 GFLOP/run -  10.46 TFLOPS
  MUL_MAT(type_a=iq3_s,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                     176 runs -  5723.26 us/run -  60.13 GFLOP/run -  10.51 TFLOPS
  MUL_MAT(type_a=iq4_xs,type_b=f32,m=4096,n=512,k=14336,bs=[1,1],nr=[1,1],per=[0,1,2,3],v=0):                    176 runs -  5737.44 us/run -  60.13 GFLOP/run -  10.48 TFLOPS
  Backend ROCm0: OK
```

Running mamf-finder w/o hipBLASLt shows similar very poor perf:

```
Tried  3375 shapes => the best outcomes were:
mean:   5.0 TFLOPS @ 4096x9216x1024 (MxNxK)
median: 5.0 TFLOPS @ 12288x3072x1024 (MxNxK)
max:    5.1 TFLOPS @ 11264x3072x1024 (MxNxK)
Elapsed time: 1 day, 10:40:32
```

vs w/ hipBLASLt:

```
Tried  3375 shapes => the best outcomes were:
mean:   35.1 TFLOPS @ 15360x3072x1024 (MxNxK)
median: 35.1 TFLOPS @ 15360x3072x1024 (MxNxK)
max:    36.9 TFLOPS @ 6144x3072x3072 (MxNxK)

Elapsed time: 6:04:34
```

### Operating System

Fedora Linux 43  (Workstation Edition Prerelease)

### CPU

AMD Ryzen AI MAX+ 395 Strix Halo

### GPU

gfx1151

### ROCm Version

6.3.42134-0 , 6.4.43480-9f04e2822

### ROCm Component

rocBLAS

### Steps to Reproduce

Checkout and build llama.cpp: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#hip

or use my mamf-finder repo: https://github.com/shisa-ai/mamf-finder

Additional Strix Halo testing/notes here: https://llm-tracker.info/_TOORG/Strix-Halo

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (20 条)

### 评论 #1 — ppanchad-amd (2025-05-16T13:54:07Z)

Hi @lhl. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — lhl (2025-05-25T07:21:27Z)

@ppanchad-amd just as an FYI, I did a bit more testing since I spotted https://github.com/adelj88/rocm_wmma_samples and it was easy enough to build and test. I am currently using the latest [TheRock nightly build](https://github.com/ROCm/TheRock/releases/tag/nightly-tarball): therock-dist-linux-gfx1151-6.5.0rc20250524.tar.gz (and gfx110x for gfx1100 kernels) on Fedora Rawhide (6.15.0-0.rc5.250509g9c69f8884904.47.fc43.x86_64)

`hgemm/bench --benchmark_filter=rocblas`:
- gfx1100 rocBLAS has 2.5-6X the performance as gfx1151 rocBLAS
- gfx1100 rocBLAS is 1.5-3X faster than gfx1151 hipBLASLt

gfx1151 rocBLAS:
```
{hgemm:kernel_type::rocblas,m:1024,n:1024,k:1024}/manual_time                       0.352 ms        0.379 ms         1943 TFLOPS=6.10924 bytes_per_second=16.6634Gi/s
{hgemm:kernel_type::rocblas,m:2048,n:2048,k:2048}/manual_time                        2.83 ms         2.85 ms          250 TFLOPS=6.07286 bytes_per_second=8.27458Gi/s
{hgemm:kernel_type::rocblas,m:4096,n:4096,k:4096}/manual_time                        13.8 ms         13.8 ms           49 TFLOPS=9.98742 bytes_per_second=6.78644Gi/s
{hgemm:kernel_type::rocblas,m:8192,n:8192,k:8192}/manual_time                         102 ms          102 ms            6 TFLOPS=10.754 bytes_per_second=3.6613Gi/s
```

gfx1151 rocBLAS ROCBLAS_USE_HIPBLASLT=1:
```
{hgemm:kernel_type::rocblas,m:1024,n:1024,k:1024}/manual_time      0.109 ms        0.135 ms         6420 TFLOPS=19.6586 bytes_per_second=53.6028Gi/s
{hgemm:kernel_type::rocblas,m:2048,n:2048,k:2048}/manual_time      0.600 ms        0.625 ms         1125 TFLOPS=28.6657 bytes_per_second=39.0436Gi/s
{hgemm:kernel_type::rocblas,m:4096,n:4096,k:4096}/manual_time       6.61 ms         6.62 ms          104 TFLOPS=20.7887 bytes_per_second=14.1747Gi/s
{hgemm:kernel_type::rocblas,m:8192,n:8192,k:8192}/manual_time        146 ms          145 ms            5 TFLOPS=7.57158 bytes_per_second=2.57652Gi/s
```

gfx1100 rocBLAS HSA_OVERRIDE_GFX_VERSION=11.0.0:
```
{hgemm:kernel_type::rocblas,m:1024,n:1024,k:1024}/manual_time      0.063 ms        0.087 ms        11305 TFLOPS=34.3626 bytes_per_second=93.6554Gi/s
{hgemm:kernel_type::rocblas,m:2048,n:2048,k:2048}/manual_time      0.445 ms        0.472 ms         1577 TFLOPS=38.599 bytes_per_second=52.6245Gi/s
{hgemm:kernel_type::rocblas,m:4096,n:4096,k:4096}/manual_time       3.11 ms         3.14 ms          221 TFLOPS=44.1693 bytes_per_second=30.1057Gi/s
{hgemm:kernel_type::rocblas,m:8192,n:8192,k:8192}/manual_time       43.5 ms         43.5 ms           16 TFLOPS=25.2763 bytes_per_second=8.61588Gi/s
```

gfx1100 rocBLAS HSA_OVERRIDE_GFX_VERSION=11.0.0 ROCBLAS_USE_HIPBLASLT=1:
```
{hgemm:kernel_type::rocblas,m:1024,n:1024,k:1024}/manual_time      0.109 ms        0.135 ms         6246 TFLOPS=19.6989 bytes_per_second=53.7266Gi/s
{hgemm:kernel_type::rocblas,m:2048,n:2048,k:2048}/manual_time      0.600 ms        0.625 ms         1120 TFLOPS=28.6679 bytes_per_second=39.0454Gi/s
{hgemm:kernel_type::rocblas,m:4096,n:4096,k:4096}/manual_time       9.44 ms         9.44 ms           74 TFLOPS=14.5921 bytes_per_second=9.9338Gi/s
{hgemm:kernel_type::rocblas,m:8192,n:8192,k:8192}/manual_time        175 ms          174 ms            4 TFLOPS=6.29111 bytes_per_second=2.14501Gi/s
```

---

### 评论 #3 — jammm (2025-08-04T11:28:01Z)

@lhl have you tried the more recent builds ? E.g., this change was added which may help improve perf https://github.com/ROCm/rocm-libraries/pull/699/ 

---

### 评论 #4 — lhl (2025-08-04T15:51:16Z)

> [@lhl](https://github.com/lhl) have you tried the more recent builds ? E.g., this change was added which may help improve perf [ROCm/rocm-libraries#699](https://github.com/ROCm/rocm-libraries/pull/699)

Here's what the llama.cpp pp sweep w/ Linux 6.16.0-1-mainline and the latest TheRock/ROCm 7.0 nightly and rocWMMA from source looks like: https://github.com/lhl/strix-halo-testing/tree/main/llm-bench/llama-2-7b.Q4_0#tokenss-performance

There is about a 3X perf difference for using rocBLAS vs hipBLASLt. rocWMMA gives a bit of a boost. I need to re-setup synthetics (hgemm, mamf-finder) for this setup, but this should give an idea on the perf gap that still seems to exist.

---

### 评论 #5 — jammm (2025-08-04T16:21:15Z)

> > [@lhl](https://github.com/lhl) have you tried the more recent builds ? E.g., this change was added which may help improve perf [ROCm/rocm-libraries#699](https://github.com/ROCm/rocm-libraries/pull/699)
> 
> Here's what the llama.cpp pp sweep w/ Linux 6.16.0-1-mainline and the latest TheRock/ROCm 7.0 nightly and rocWMMA from source looks like: https://github.com/lhl/strix-halo-testing/tree/main/llm-bench/llama-2-7b.Q4_0#tokenss-performance
> 
> There is about a 3X perf difference for using rocBLAS vs hipBLASLt. rocWMMA gives a bit of a boost. I need to re-setup synthetics (hgemm, mamf-finder) for this setup, but this should give an idea on the perf gap that still seems to exist.

Does this also include the performance numbers between gfx1151 and gfx1151 with `HSA_OVERRIDE_GFX_VERSION=11.0.0` ? I'm trying to understand if the latest nightly fixes the gap between the with and without `HSA_OVERRIDE_GFX_VERSION=11.0.0` on gfx1151.


---

### 评论 #6 — lhl (2025-08-04T17:28:16Z)

> > > [@lhl](https://github.com/lhl) have you tried the more recent builds ? E.g., this change was added which may help improve perf [ROCm/rocm-libraries#699](https://github.com/ROCm/rocm-libraries/pull/699)
> > 
> > 
> > Here's what the llama.cpp pp sweep w/ Linux 6.16.0-1-mainline and the latest TheRock/ROCm 7.0 nightly and rocWMMA from source looks like: https://github.com/lhl/strix-halo-testing/tree/main/llm-bench/llama-2-7b.Q4_0#tokenss-performance
> > There is about a 3X perf difference for using rocBLAS vs hipBLASLt. rocWMMA gives a bit of a boost. I need to re-setup synthetics (hgemm, mamf-finder) for this setup, but this should give an idea on the perf gap that still seems to exist.
> 
> Does this also include the performance numbers between gfx1151 and gfx1151 with `HSA_OVERRIDE_GFX_VERSION=11.0.0` ? I'm trying to understand if the latest nightly fixes the gap between the with and without `HSA_OVERRIDE_GFX_VERSION=11.0.0` on gfx1151.

No, it doesn't, as the HSA_OVERRIDE_GFX_VERSION can cause instability (hard crashes) that make it unsuitable for scripted testing.

Maybe @ppanchad-amd has more insight on their internal progress/tracking of this issue.

---

### 评论 #7 — Mushoz (2025-08-04T17:34:36Z)

Even without HSA_OVERRIDE_GFX_VERSION things can be quite unstable with big MOE models under Llama.cpp. Thankfully the Vulkan backend is rock solid, albeit with pretty poor prompt processing. I am quite disappointed with the software support for Strix Halo so far.

---

### 评论 #8 — lhl (2025-08-08T12:29:36Z)

> Does this also include the performance numbers between gfx1151 and gfx1151 with `HSA_OVERRIDE_GFX_VERSION=11.0.0` ? I'm trying to understand if the latest nightly fixes the gap between the with and without `HSA_OVERRIDE_GFX_VERSION=11.0.0` on gfx1151.

Had a spare min. Here's rocBLAS, about 60% slower still:

```
❯ HSA_OVERRIDE_GFX_VERSION=11.0.0 ~/llama.cpp/llama.cpp-hip/build/bin/llama-bench -m /models/gguf/llama-2-7b.Q4_0.gguf -fa 1                                                                                                                                                   (base)
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           pp512 |        477.07 ± 1.29 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           tg128 |         48.94 ± 0.01 |

build: 6c7e9a54 (6118)

❯ ~/llama.cpp/llama.cpp-hip/build/bin/llama-bench -m /models/gguf/llama-2-7b.Q4_0.gguf -fa 1                                                                                                                                                                                   (base)
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           pp512 |        297.81 ± 0.26 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           tg128 |         48.80 ± 0.00 |

build: 6c7e9a54 (6118)
```

Looks like hipBLASLt is better now:

```
❯ ROCBLAS_USE_HIPBLASLT=1 HSA_OVERRIDE_GFX_VERSION=11.0.0 ~/llama.cpp/llama.cpp-hip/build/bin/llama-bench -m /models/gguf/llama-2-7b.Q4_0.gguf -fa 1                                                                                                                           (base)
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           pp512 |        627.15 ± 1.22 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           tg128 |         48.91 ± 0.01 |

build: 6c7e9a54 (6118)

❯ ROCBLAS_USE_HIPBLASLT=1 ~/llama.cpp/llama.cpp-hip/build/bin/llama-bench -m /models/gguf/llama-2-7b.Q4_0.gguf -fa 1                                                                                                                                                           (base)
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           pp512 |        681.13 ± 0.81 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |           tg128 |         48.78 ± 0.01 |

build: 6c7e9a54 (6118)
```

Here's what rocWMMA + hipBLASLt looks like - it segfaults on using HSA_OVERRIDE, but it's cleary the way to go I think if you're using ROCm backend:
```
❯ ROCBLAS_USE_HIPBLASLT=1 ~/llama.cpp/llama.cpp-rocwmma/build/bin/llama-bench -m /models/gguf/llama-2-7b.Q4_0.gguf -fa 1                                                                                                                                                       (base)
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm       |  99 |  1 |           pp512 |       1090.52 ± 3.47 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm       |  99 |  1 |           tg128 |         47.98 ± 0.01 |

build: 6c7e9a54 (6118)
```

However, here's what AMDVLK Vulkan looks like atm:
```
❯ ~/llama.cpp/llama.cpp-vulkan/build/bin/llama-bench -m /models/gguf/llama-2-7b.Q4_0.gguf -fa 1                                                                                                                                                                                (base)
ggml_vulkan: Found 1 Vulkan devices:
ggml_vulkan: 0 = Radeon 8060S Graphics (AMD open-source driver) | uma: 1 | fp16: 1 | bf16: 0 | warp size: 64 | shared memory: 32768 | int dot: 1 | matrix cores: KHR_coopmat
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |           pp512 |       1343.71 ± 5.29 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |           tg128 |         48.00 ± 0.03 |

build: 6c7e9a54 (6118)
```

---

### 评论 #9 — Mushoz (2025-08-08T12:33:34Z)

@lhl Just to double check: You are using this file to run your tests, right: https://huggingface.co/TheBloke/Llama-2-7B-GGUF/blob/main/llama-2-7b.Q4_0.gguf

Want to do some tests of my own and compare :)

---

### 评论 #10 — Mushoz (2025-08-09T06:53:32Z)

> This is my results with 6.4.1 from arch only difference is that I rebuilded rocblas to use hipblaslt and also updated hipblaslt to 6.4.2 which has support for gfx1151 and rebuilded it
> 
> ```
> ~/s/llama.cpp master•
> ❱ HSA_OVERRIDE_GFX_VERSION=11.0.0 ROCBLAS_USE_HIPBLASLT=1 llama-bench -m ~/Downloads/llama-2-7b.Q4_0.gguf -fa 1 --mmap 0
> ggml_vulkan: Found 1 Vulkan devices:
> ggml_vulkan: 0 = Radeon 8060S Graphics (RADV GFX1151) (radv) | uma: 1 | fp16: 1 | bf16: 0 | warp size: 64 | shared memory: 65536 | int dot: 1 | matrix cores: KHR_coopmat
> | model                          |       size |     params | backend    | ngl | fa | mmap |            test |                  t/s |
> | ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---: | --------------: | -------------------: |
> | llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |    0 |           pp512 |        785.87 ± 9.22 |
> | llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |    0 |           tg128 |         49.39 ± 0.16 |
> 
> build: cd6983d (3)
> 
> ~/s/llama.cpp master• 18.3s
> ❱ llama-bench -m ~/Downloads/llama-2-7b.Q4_0.gguf -fa 1 --mmap 0
> ggml_vulkan: Found 1 Vulkan devices:
> ggml_vulkan: 0 = Radeon 8060S Graphics (RADV GFX1151) (radv) | uma: 1 | fp16: 1 | bf16: 0 | warp size: 64 | shared memory: 65536 | int dot: 1 | matrix cores: KHR_coopmat
> | model                          |       size |     params | backend    | ngl | fa | mmap |            test |                  t/s |
> | ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---: | --------------: | -------------------: |
> | llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |    0 |           pp512 |        779.43 ± 4.26 |
> | llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |    0 |           tg128 |         49.40 ± 0.12 |
> 
> build: cd6983d (3)
> 
> ~/s/llama.cpp master• 17.5s
> ❱ ROCBLAS_USE_HIPBLASLT=1 llama-bench -m ~/Downloads/llama-2-7b.Q4_0.gguf -fa 1 --mmap 0
> ggml_vulkan: Found 1 Vulkan devices:
> ggml_vulkan: 0 = Radeon 8060S Graphics (RADV GFX1151) (radv) | uma: 1 | fp16: 1 | bf16: 0 | warp size: 64 | shared memory: 65536 | int dot: 1 | matrix cores: KHR_coopmat
> | model                          |       size |     params | backend    | ngl | fa | mmap |            test |                  t/s |
> | ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---: | --------------: | -------------------: |
> | llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |    0 |           pp512 |        779.95 ± 3.89 |
> | llama 7B Q4_0                  |   3.56 GiB |     6.74 B | Vulkan,RPC |  99 |  1 |    0 |           tg128 |         49.43 ± 0.15 |
> ```

Have you tried compiling llamacpp with rocwmma support? It should help with prompt processing as well.

---

### 评论 #11 — phush0 (2025-08-09T06:55:16Z)

Here my results:

```
~/s/llama.cpp master• 17.5s
❱ HSA_OVERRIDE_GFX_VERSION=11.0.0 ROCBLAS_USE_HIPBLASLT=1 build/bin/llama-bench -m ~/Downloads/llama-2-7b.Q4_0.gguf -fa 1 --mmap 0
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon 8060S Graphics, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa | mmap |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           pp512 |        910.22 ± 5.86 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           tg128 |         45.77 ± 0.13 |

build: 0e838446 (6100)

~/s/llama.cpp master• 19.6s
❱ HSA_OVERRIDE_GFX_VERSION=11.0.0 build/bin/llama-bench -m ~/Downloads/llama-2-7b.Q4_0.gguf -fa 1 --mmap 0
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon 8060S Graphics, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa | mmap |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           pp512 |        644.92 ± 7.41 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           tg128 |         45.56 ± 0.12 |

build: 0e838446 (6100)

~/s/llama.cpp master• 20.8s
❱ ROCBLAS_USE_HIPBLASLT=1 build/bin/llama-bench -m ~/Downloads/llama-2-7b.Q4_0.gguf -fa 1 --mmap 0
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon 8060S Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa | mmap |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           pp512 |       1023.67 ± 9.41 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           tg128 |         45.66 ± 0.10 |

build: 0e838446 (6100)

~/s/llama.cpp master• 19s
❱ build/bin/llama-bench -m ~/Downloads/llama-2-7b.Q4_0.gguf -fa 1 --mmap 0
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon 8060S Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl | fa | mmap |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---: | --------------: | -------------------: |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           pp512 |        300.67 ± 4.15 |
| llama 7B Q4_0                  |   3.56 GiB |     6.74 B | ROCm,RPC   |  99 |  1 |    0 |           tg128 |         45.65 ± 0.14 |

build: 0e838446 (6100)
```

this is with default install of ROCm on arch which is 6.4.1, only difference is that I rebuilded rocblas to use hipblaslt and also hipblaslt is 6.4.2 and is rebuilded to support only gfx1100 and gfx1151

edit: I found mistake and reposted but you are too fast with answer

---

### 评论 #12 — Mushoz (2025-10-19T21:26:19Z)

Is this still a problem with the latest ROCm 7.10? From my understanding it had some great performance improvements for gfx1151. Not sure if the gfx1100 codepath is still faster?

---

### 评论 #13 — Djip007 (2025-12-28T14:00:20Z)

> Is this still a problem with the latest ROCm 7.10? From my understanding it had some great performance improvements for gfx1151. Not sure if the gfx1100 codepath is still faster?

Rocm 6.4.4 (from fedora 43 at least) and rocm 7.1.1 / 7.9 work good, but there is regression with rocm-7.10/7.9 on quantized llama.cpp.

cf: https://github.com/ggml-org/llama.cpp/issues/17917

---

### 评论 #14 — darkbasic (2026-05-05T09:58:00Z)

> Is this still a problem with the latest ROCm 7.10? From my understanding it had some great performance improvements for gfx1151. Not sure if the gfx1100 codepath is still faster?

@Mushoz AFAIK in the past year nothing improved on that front and the gfx1100 codepath is still much faster: https://kyuz0.github.io/amd-strix-halo-toolboxes/

I would really love to hear something from AMD about this issue.

---

### 评论 #15 — jrhip (2026-05-05T10:42:59Z)

I'm still seeing the same behaviour on both Pytorch and JAX with gfx1151 : https://github.com/ROCm/ROCm/issues/5807

Full performance (~30 TFLOPS) on float16, but ~10x slower on float32 (~3 TFLOPS)

---

### 评论 #16 — mgehre-amd (2026-05-05T11:31:04Z)

[Initial tuning for fp32 on gfx1151](https://github.com/ROCm/rocm-libraries/pull/5946) is available in the ROCm nightly builds.

---

### 评论 #17 — jrhip (2026-05-05T11:42:26Z)

> [Initial tuning for fp32 on gfx1151](https://github.com/ROCm/rocm-libraries/pull/5946) is available in the ROCm nightly builds.

Great I will re-test and update both issues

---

### 评论 #18 — darkbasic (2026-05-05T13:13:25Z)

@mgehre-amd while fp32 tuning is great to hear that doesn't explain why llama.cpp prompt processing is so much slower on ROCm 7.x compared to 6.x:

<img width="1257" height="524" alt="Image" src="https://github.com/user-attachments/assets/28d37182-b2cf-4dd7-953e-498f5f0449de" />

Any clue why that happens? 7.2 stable is as slow as the nightlies.

---

### 评论 #19 — jrhip (2026-05-05T19:02:31Z)

> > [Initial tuning for fp32 on gfx1151](https://github.com/ROCm/rocm-libraries/pull/5946) is available in the ROCm nightly builds.
> 
> Great I will re-test and update both issues

No change in performance for me with `torch 2.11.0+rocm7.13.0a20260505`

---

### 评论 #20 — mgehre-amd (2026-05-05T21:41:29Z)

> [@mgehre-amd](https://github.com/mgehre-amd) while fp32 tuning is great to hear that doesn't explain why llama.cpp prompt processing is so much slower on ROCm 7.x compared to 6.x:
> 
> <img alt="Image" width="1257" height="524" src="https://private-user-images.githubusercontent.com/1047358/587693002-28d37182-b2cf-4dd7-953e-498f5f0449de.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzgwMTc0OTYsIm5iZiI6MTc3ODAxNzE5NiwicGF0aCI6Ii8xMDQ3MzU4LzU4NzY5MzAwMi0yOGQzNzE4Mi1iMmNmLTRkZDctOTUzZS00OThmNWYwNDQ5ZGUucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUwNSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MDVUMjEzOTU2WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZTE2ZmUzOThjOGJiNTIzMGJlNGRhZmVlNmUwNzM4NWY4MDAyODYxYzRjZTljZDhmNDBmZGRmZWYwNzAwODFhMCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.oaleH2dhq7ZABomzB6tlRvJOvU_5MnUs4ZOePJ5q_P4">
> Any clue why that happens? 7.2 stable is as slow as the nightlies.

llama.cpp uses its own kernels instead of rocBLAS/hipBLASlt for quantized models like Q4_K_L or Q5_L_XL

---
