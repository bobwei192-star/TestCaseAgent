# [Issue]: hipDeviceProp_t name attribute is empty 

> **Issue #3069**
> **状态**: closed
> **创建时间**: 2024-04-25T21:24:35Z
> **更新时间**: 2024-06-21T19:27:27Z
> **关闭时间**: 2024-06-21T19:27:17Z
> **作者**: abagusetty
> **标签**: AMD Instinct MI250X, ROCm 6.0.0, AMD Instinct MI100, AMD Instinct MI250
> **URL**: https://github.com/ROCm/ROCm/issues/3069

## 标签

- **AMD Instinct MI250X** (颜色: #ededed)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Instinct MI100** (颜色: #ededed)
- **AMD Instinct MI250** (颜色: #ededed)

## 描述

### Problem Description

Reopening since the attribute name for the device string is empty with rocm-6.0.0 on MI250, MI100, MI250x. Tagging @nartmada 
```bash
HIP version: 6.0.32830-d62f6a171
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.0.0 23483 7208e8d15fbf218deb74483ea8c549c67ca4985e)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /soft/compilers/rocm/rocm-6.0.0/llvm/bin
Configuration file: /soft/compilers/rocm/rocm-6.0.0/lib/llvm/bin/clang++.cfg
```


### Operating System

openSUSE Leap 15.4

### CPU

AMD EPYC 7543 32-Core Processor

### GPU

AMD Instinct MI250X, AMD Instinct MI250, AMD Instinct MI100

### ROCm Version

ROCm 6.0.0

### ROCm Component

HIP

### Steps to Reproduce

```c++
#include<iostream>
#include <hip/hip_runtime.h>
int main(){
  hipDeviceProp_t deviceProp;
  hipGetDeviceProperties(&deviceProp, 0);
  std::cout << deviceProp.name << std::endl;
}
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Mentioned in these issues: https://github.com/ROCm/ROCm/issues/1625, https://github.com/ROCm/ROCm/issues/1778

---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-04-25T21:38:27Z)

@abagusetty, can you please try ROCm 6.1.0?  Thanks.
![image](https://github.com/ROCm/ROCm/assets/144284448/a98e0e5f-af27-4d21-9181-29817b1fac1f)


---

### 评论 #2 — harkgill-amd (2024-06-21T19:27:17Z)

Hi @abagusetty, I was not able to reproduce this issue with ROCm 6.1.2 on a MI100 system. If you see this issue again, please re-open this ticket, thanks!

---
