# [Issue]: <hip/device_functions.h> header automatially padded to <hip/hip/device_function.h> when building rocm for torch extension

> **Issue #3937**
> **状态**: closed
> **创建时间**: 2024-10-23T08:11:09Z
> **更新时间**: 2025-04-22T19:06:27Z
> **关闭时间**: 2025-04-22T19:06:25Z
> **作者**: ZJLi2013
> **标签**: Under Investigation, ROCm 6.2.3, mi300
> **URL**: https://github.com/ROCm/ROCm/issues/3937

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **mi300** (颜色: #ededed)

## 描述

### Problem Description

as  `device_functions.h` is located at `/opt/rocm/include/hip` , so expecting to use it as: 

```c++
#include <hip/hip_runtime.h>
#include <hip/hip_runtime_api.h>
// Buggy: somehow setuptool will add prefix to <hip/hip/device_functions.h>
// #include <hip/device_functions.h>  // for amd_warp_sync_functions
#include <device_functions.h>
```

while it's auto padded to  <hip/hip/device_functions.h>,  and to make it work, had to modify as `#include<device_functions.h>`

is this expected behavior ?

Thanks
David 

### Operating System

Ubuntu 22.04

### CPU

Ryzen 

### GPU

mi300

### ROCm Version

ROCm 6.2.3

### ROCm Component

hipBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2024-10-23T13:56:36Z)

Hi @ZJLi2013. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2024-10-23T15:48:59Z)

Hi @ZJLi2013, can you provide a reproducer for this? I'm not seeing this in a quick test, `setuptools` seems to process `#include <hip/hip_runtime.h>`, `#include <hip/hip_runtime_api.h>`, and `#include <hip/device_functions.h>` fine when I pass it `/opt/rocm/include` as an include directory.

---

### 评论 #3 — ZJLi2013 (2024-10-24T01:21:13Z)

hi, @schung-amd , you can try on this repo: https://github.com/ZJLi2013/grouped_gemm/blob/rocm/csrc/permute.hip

---

### 评论 #4 — schung-amd (2024-10-24T14:30:58Z)

I was able to reproduce the mangling with your code and found the root cause. We do a hipify pass in CUDAExtension [here](https://github.com/ROCm/pytorch/blob/267f82b860ccdf32df3dcb92e2435b64ba0f117a/torch/utils/cpp_extension.py#L1131 ) which maps CUDA header names to HIP header names. This works fine for files that are named differently, but the corresponding CUDA header is also called `device_functions.h` and is mapped to `hip/device_functions.h` [here](https://github.com/ROCm/pytorch/blob/3d2431380999252d5401f83d5010b398a32e7597/torch/utils/hipify/cuda_to_hip_mappings.py#L567), causing the mangling. 

I'm not sure if this workflow is unsupported, or if this simply wasn't tested. The fix is pretty simple, the mapping just needs to map `include <device_functions.h` to `include <hip/device_functions.h` instead. I suspect this is also an issue for `driver_types.h` and `library_types.h`. For now, as you've noted, you can use `device_functions.h` as a workaround.

---

### 评论 #5 — schung-amd (2025-04-22T19:06:25Z)

Closing for now as it's gotten a bit stale; had some internal discussions regarding how we're hipifying these includes but didn't gain any traction on changes. Let me know if the workaround is insufficient and we can reopen.

---
