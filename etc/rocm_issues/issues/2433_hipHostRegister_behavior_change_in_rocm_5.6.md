# hipHostRegister behavior change in rocm 5.6

> **Issue #2433**
> **状态**: closed
> **创建时间**: 2023-09-04T22:12:25Z
> **更新时间**: 2024-06-24T19:15:21Z
> **关闭时间**: 2024-06-24T19:15:21Z
> **作者**: ye-luo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2433

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Noticed significant slow down of hipHostRegister which seems due to underlying implementation change to SVM in hsa in rocm 5.6.
There is an undocumented environment variable `HSA_USE_SVM` after digging into ROCr.

[many_transfers.zip](https://github.com/RadeonOpenCompute/ROCm/files/12516910/many_transfers.zip)

All the timings reported here are from runs on a RadeonVII gfx906 but newer GPUs like MI250x shows the same issue.
```
#threaded OMP case
hipcc -fopenmp -g -DCUDA2HIP many_transfer.omp.cpp -o many_transfer.omp.x
```

Using rocm-5.6.0, default setting HSA_USE_SVM=1
```
yeluo@epyc-server:~/temp/many_transfers$ OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 5.37867e+07 us # very very slow, a huge regression.
Function many_transfer.omp thread 0 takes 42616.2 us
Function many_transfer.omp thread 2 takes 26110.7 us
Function many_transfer.omp thread 7 takes 28389.9 us
Function many_transfer.omp thread 4 takes 72282.9 us
Function many_transfer.omp thread 3 takes 85687.2 us
Function many_transfer.omp thread 5 takes 87175.1 us
Function many_transfer.omp thread 1 takes 93498.1 us
Function many_transfer.omp thread 6 takes 99937.7 us
```
Usually slower hipHostRegister is not a bit deal since reasonable codes just need to register once. However, in this case, the slowdown is so huge that reasonable codes got noticeable slowdown.
If changing `#define N 16384` to `32768` in the source code, at least 10^8 us is needed in the initialization.

Using rocm-5.6.0, turning off SVM and got back rocm 5.5 behavior in hipHostRegister
```
yeluo@epyc-server:~/temp/many_transfers$ OMP_NUM_THREADS=8 HSA_USE_SVM=0 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 708273 us
Function many_transfer.omp thread 0 takes 49525.1 us
Function many_transfer.omp thread 5 takes 41510.6 us
Function many_transfer.omp thread 7 takes 28397.9 us
Function many_transfer.omp thread 1 takes 28777.3 us
Function many_transfer.omp thread 4 takes 5.62431e+06 us # drunk?
Function many_transfer.omp thread 6 takes 27235.2 us
Function many_transfer.omp thread 2 takes 5.63835e+06 us # drunk?
Function many_transfer.omp thread 3 takes 26933.6 us
```
Some threads seem stranded. Very concerning behavior for codes using multiple streams from host threads.

Using rocm-5.5.0
```
yeluo@epyc-server:~/temp/many_transfers$ OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 709061 us
Function many_transfer.omp thread 0 takes 85138.3 us
Function many_transfer.omp thread 5 takes 62581.4 us
Function many_transfer.omp thread 7 takes 34131.3 us
Function many_transfer.omp thread 3 takes 98494.9 us
Function many_transfer.omp thread 6 takes 118628 us
Function many_transfer.omp thread 4 takes 112630 us
Function many_transfer.omp thread 2 takes 127532 us
Function many_transfer.omp thread 1 takes 115938 us
```

Clearly, switching to SVM makes code initialization much longer.
If not using SVM, rocm 5.6 improved hipMemcpyAsync on some threads in a threaded scenario compared to rocm-5.5.0 but still the huge imbalance is also extremely concerning.

---

## 评论 (7 条)

### 评论 #1 — ye-luo (2023-09-17T16:19:20Z)

ROCm 5.7.0, the situation seems improved. Using the default SVM implementation, the timing improved.
```
yeluo@epyc-server:~/temp/many_transfers$ OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 1.46004e+07 us
Function many_transfer.omp thread 0 takes 40738.9 us
Function many_transfer.omp thread 3 takes 46968.5 us
Function many_transfer.omp thread 4 takes 70925.8 us
Function many_transfer.omp thread 1 takes 78349.2 us
Function many_transfer.omp thread 6 takes 73105.9 us
Function many_transfer.omp thread 5 takes 91836.4 us
Function many_transfer.omp thread 7 takes 97764.5 us
Function many_transfer.omp thread 2 takes 98400.3 us
```
After disabling SVM `HSA_USE_SVM=0`, imbalance is much smaller than 5.6.0
```
yeluo@epyc-server:~/temp/many_transfers$ HSA_USE_SVM=0 OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 306820 us
Function many_transfer.omp thread 0 takes 25743.1 us
Function many_transfer.omp thread 5 takes 28098.2 us
Function many_transfer.omp thread 7 takes 29085.8 us
Function many_transfer.omp thread 3 takes 67193.5 us
Function many_transfer.omp thread 1 takes 73911.8 us
Function many_transfer.omp thread 6 takes 85485.6 us
Function many_transfer.omp thread 2 takes 85562.1 us
Function many_transfer.omp thread 4 takes 101128 us
```

---

### 评论 #2 — ye-luo (2023-12-15T23:16:11Z)

ROCm 6.0. With SVM
```
yeluo@epyc-server:~/temp/many_transfers$ HSA_USE_SVM=1 OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 3.36361e+07 us
Function many_transfer.omp thread 0 takes 34763.8 us
Function many_transfer.omp thread 1 takes 30083.9 us
Function many_transfer.omp thread 5 takes 41826.3 us
Function many_transfer.omp thread 6 takes 49715.2 us
Function many_transfer.omp thread 3 takes 61341.6 us
Function many_transfer.omp thread 7 takes 73459.2 us
Function many_transfer.omp thread 4 takes 72389.7 us
Function many_transfer.omp thread 2 takes 75572.9 us
```
disable SVM
```
yeluo@epyc-server:~/temp/many_transfers$ HSA_USE_SVM=0 OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 442394 us
Function many_transfer.omp thread 0 takes 19135.1 us
Function many_transfer.omp thread 5 takes 29784.1 us
Function many_transfer.omp thread 7 takes 42229.3 us
Function many_transfer.omp thread 3 takes 40986 us
Function many_transfer.omp thread 2 takes 56050.9 us
Function many_transfer.omp thread 1 takes 59936.1 us
Function many_transfer.omp thread 6 takes 65883.3 us
Function many_transfer.omp thread 4 takes 63146.1 us
```

---

### 评论 #3 — nartmada (2024-03-16T01:42:17Z)

Internal ticket has been created for investigation.

---

### 评论 #4 — jamesxu2 (2024-06-24T15:02:11Z)

Hello @ye-luo ,

Thank you for the detailed ticket information and follow-ups - I have rerun your tests on ROCm 6.1.2 and  RX7900XT GPU with the following results:

**Use SVM**
```
$ OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 7.38809e+06 us  
Function many_transfer.omp thread 0 takes 26934.4 us
Function many_transfer.omp thread 7 takes 23488.8 us
Function many_transfer.omp thread 5 takes 23726.6 us
Function many_transfer.omp thread 4 takes 26932.9 us
Function many_transfer.omp thread 6 takes 48800.3 us
Function many_transfer.omp thread 3 takes 73209.1 us
Function many_transfer.omp thread 1 takes 73152.8 us
Function many_transfer.omp thread 2 takes 76329.7 us
Success
```
**Disable SVM**
```
$ OMP_NUM_THREADS=8 HSA_USE_SVM=0 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 973686 us 
Function many_transfer.omp thread 0 takes 27131.2 us
Function many_transfer.omp thread 4 takes 23808.2 us
Function many_transfer.omp thread 5 takes 24007.6 us
Function many_transfer.omp thread 6 takes 26098.9 us
Function many_transfer.omp thread 3 takes 74056.2 us
Function many_transfer.omp thread 7 takes 85318.2 us
Function many_transfer.omp thread 1 takes 92107.3 us
Function many_transfer.omp thread 2 takes 92728.5 us
Success
```

The hipHostRegister slowdown is much less significant and thread timing variation appear significantly improved since your ticket was opened. Do you need any additional assistance?

---

### 评论 #5 — ye-luo (2024-06-24T17:23:08Z)

It is also behaving well on my side. Rocm 6.0.0 and 6.1.0 are both good on my computers today. From rocm 6.1.0
```
yeluo@epyc-server:~/temp/many_transfers$ HSA_USE_SVM=0 OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 321647 us
Function many_transfer.omp thread 0 takes 19772.5 us
Function many_transfer.omp thread 7 takes 28569.3 us
Function many_transfer.omp thread 6 takes 35933.1 us
Function many_transfer.omp thread 1 takes 60198.3 us
Function many_transfer.omp thread 3 takes 57116.4 us
Function many_transfer.omp thread 2 takes 65832.3 us
Function many_transfer.omp thread 4 takes 71110.1 us
Function many_transfer.omp thread 5 takes 69075.2 us
Success
yeluo@epyc-server:~/temp/many_transfers$ HSA_USE_SVM=1 OMP_NUM_THREADS=8 ./many_transfer.omp.x
Function many_transfer.omp HostRegistering takes 178131 us
Function many_transfer.omp thread 0 takes 28538.3 us
Function many_transfer.omp thread 5 takes 32518.6 us
Function many_transfer.omp thread 4 takes 35609.2 us
Function many_transfer.omp thread 6 takes 55837 us
Function many_transfer.omp thread 1 takes 66706.2 us
Function many_transfer.omp thread 3 takes 75144.2 us
Function many_transfer.omp thread 7 takes 69983 us
Function many_transfer.omp thread 2 takes 76483 us
Success
```
I think the key bug fix is probably in the amdgpu kernel module. That is the only difference between my Dec run with rocm 6.0.0 and the current one.
@jamesxu2 Could you confirm?

---

### 评论 #6 — jamesxu2 (2024-06-24T19:01:11Z)

Hello @ye-luo ,

I'm unfortunately not able to pinpoint what exactly fixed this issue. I've tested with two older versions of the amdgpu-dkms + rocm 6.1.2 and don't observe a significant performance degradation compared to the recent amdgpu-dkms (v6.7.0). I'm not sure what version you were running with ROCm 6.0.0 in December.

## amdgpu-dkms v6.1.5 + rocm 6.1.2
**SVM enable**
```
Function many_transfer.omp HostRegistering takes 8.75597e+06 us
Function many_transfer.omp thread 0 takes 28421.6 us
Function many_transfer.omp thread 5 takes 23343.6 us
Function many_transfer.omp thread 2 takes 26120.3 us
Function many_transfer.omp thread 3 takes 47295.5 us
Function many_transfer.omp thread 1 takes 48362.9 us
Function many_transfer.omp thread 4 takes 55981.2 us
Function many_transfer.omp thread 6 takes 58690.1 us
Function many_transfer.omp thread 7 takes 58921.8 us
Success
```
**SVM disable**
```
Function many_transfer.omp HostRegistering takes 1.02954e+06 us
Function many_transfer.omp thread 0 takes 17603 us
Function many_transfer.omp thread 5 takes 24052.5 us
Function many_transfer.omp thread 2 takes 26336.6 us
Function many_transfer.omp thread 6 takes 48084.7 us
Function many_transfer.omp thread 4 takes 53874.9 us
Function many_transfer.omp thread 1 takes 57824.4 us
Function many_transfer.omp thread 3 takes 58070 us
Function many_transfer.omp thread 7 takes 58750.4 us
Success
```
## amdgpu-dkms v6.2.4 + rocm 6.1.2
**SVM enable**
```
Function many_transfer.omp HostRegistering takes 7.39387e+06 us
Function many_transfer.omp thread 0 takes 39069 us
Function many_transfer.omp thread 5 takes 50171 us
Function many_transfer.omp thread 6 takes 35310.9 us
Function many_transfer.omp thread 4 takes 23396.8 us
Function many_transfer.omp thread 2 takes 24044.4 us
Function many_transfer.omp thread 1 takes 39921.9 us
Function many_transfer.omp thread 7 takes 44040.7 us
Function many_transfer.omp thread 3 takes 43674.3 us
Success
```
**SVM disable**
```
Function many_transfer.omp HostRegistering takes 1.23591e+06 us
Function many_transfer.omp thread 0 takes 34534.9 us
Function many_transfer.omp thread 5 takes 53741.4 us
Function many_transfer.omp thread 6 takes 53207.9 us
Function many_transfer.omp thread 2 takes 25616.1 us
Function many_transfer.omp thread 4 takes 30073.6 us
Function many_transfer.omp thread 3 takes 41609.2 us
Function many_transfer.omp thread 1 takes 42335.4 us
Function many_transfer.omp thread 7 takes 35851 us
Success
```

---

### 评论 #7 — ye-luo (2024-06-24T19:12:35Z)

Much appreciated for the digging.
I was using amdgpu-dkms v6.3.6 + rocm 6.0.0 on ubuntu 20.04 (kernel 5.15) in Dec.
Anyway I'm happy that all abnormalities are gone.

---
