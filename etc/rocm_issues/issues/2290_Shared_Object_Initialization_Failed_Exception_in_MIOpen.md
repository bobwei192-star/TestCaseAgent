# Shared Object Initialization Failed Exception in MIOpen

> **Issue #2290**
> **状态**: closed
> **创建时间**: 2023-06-28T22:03:32Z
> **更新时间**: 2024-04-22T13:53:32Z
> **关闭时间**: 2024-04-22T13:53:32Z
> **作者**: Rmalavally
> **标签**: Verified Issue, 5.6.0
> **URL**: https://github.com/ROCm/ROCm/issues/2290

## 标签

- **Verified Issue** (颜色: #0052cc)
- **5.6.0** (颜色: #b60205)

## 描述

MIOpen throws a shared object initialization failed exception in MI250x products due to a known HIP issue,

```
Memory leak when code object files are loaded/unloaded via hipModuleLoad/hipModuleUnload APIs

```

Therefore, online exhaustive tuning via the MIOpen environment variable is discouraged. Users are encouraged to use the default setting, report any tuning requirements, or process online tuning in smaller batches. This issue will be fixed in a future release.

---

## 评论 (6 条)

### 评论 #1 — mabdallah89 (2023-10-04T00:13:22Z)

@Rmalavally  
Is this issue only for MI250X GPUs or it exists for all MI2xx GPUs family? I am using MI210 and have similar problem and same error message. 

I am also wondering, how does MIopen load OpenCL kernels in default setting if online tuning is discouraged? I am assuming hipModuleLoad/hipModuleUnload APIs are used to load offline compiled OpenCL kernels as well


---

### 评论 #2 — JehandadKhan (2023-10-04T15:51:24Z)

>  I am assuming hipModuleLoad/hipModuleUnload APIs are used to load offline compiled OpenCL kernels as well


@mabdallah89  That is correct


---

### 评论 #3 — Rmalavally (2023-10-04T15:53:04Z)

Thank you, @JehandadKhan, for your response. 

@mabdallah89 Hope this resolves your issue. 

---

### 评论 #4 — mabdallah89 (2023-10-04T18:30:23Z)

@JehandadKhan Thank you for your response!

I am trying to update some MIOpen OpenCL kernels and compile them offline (kernels such as softmax and batch normalization, ..) and load them in another HIP project with "hipModuleLoad" API, similar to what MIopen HIP backend is doing.

However, when I compile the OpenCL kernels offline and load them in HIP with "hipModuleLoad" , it shows an error "Shared Object Initialization Failed"!

My compile command is:

```
/opt/rocm-5.6.0/llvm/bin/clang -mcode-object-version=4 -target amdgcn-amd-amdhsa -x cl -D__AMD__=1 -O3 -cl-kernel-arg-info -cl-denorms-are-zero -cl-std=CL1.2 -mllvm -amdgpu-early-inline-all -mllvm -amdgpu-internalize-symbols vcpy_kernel.cl -o vcpy_kernel.code
```

I am using MI210 GPU, Rocm-5.6.0, Driver version: 6.1.5. Any help how to fix this issue? I tried to use the exact clang compiler flags as in MIOpen code:

https://github.com/ROCmSoftwarePlatform/MIOpen/blob/6d539ee81321121570606e4ef62e6d072775bbd8/src/hipoc/hipoc_program.cpp#L253

I believe it is an assembly format issue and it has something to do with “-mcode-object-version” flag. Could you please share with me the correct clang compilation flags that generates assembly combatable with "hipModuleLoad"?


---

### 评论 #5 — CaptnJackSparrow (2023-10-24T16:21:58Z)

We also hit the same issue, is there a timeline for the fix?

---

### 评论 #6 — Rmalavally (2024-04-22T13:53:32Z)

This issue was fixed in ROCm 5.6.1 and is now closed. 

---
