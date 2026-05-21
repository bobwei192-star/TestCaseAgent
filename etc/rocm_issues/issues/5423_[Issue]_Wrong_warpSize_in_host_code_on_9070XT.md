# [Issue]: Wrong warpSize in host code on 9070XT

> **Issue #5423**
> **状态**: closed
> **创建时间**: 2025-09-24T08:46:50Z
> **更新时间**: 2025-09-29T19:09:10Z
> **关闭时间**: 2025-09-29T19:09:10Z
> **作者**: zhang-hui-yulo
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5423

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

warpSize return 64 in my host code, but it return 32 in my device code, the warp mode is 32 by default on my 9070XT, so I think the warpSize shall be 32 in both host and device code.

This happens on both Windows ROCm 6.4.2 and Linux ROCm 7.0.0 rc1. 

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat) and Windows 11 10.0.26100

### CPU

AMD Ryzen 9 7900X3D 12-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 6.4.2 on Windows and ROCm 7.0.0 rc1 on Linux

### ROCm Component

HIP

### Steps to Reproduce

main.hip
```
#include <hip/hip_runtime.h>

__global__ void test() {
    if (threadIdx.x == 0) {
        printf("warpSize from device is %i.\n", warpSize);
    }
}

int main(int argc, char** argv) {
    printf("warpSize from host is %i.\n", warpSize);
    test <<< 1, warpSize >>> ();
    return 0;
}
```

build command
```
"%HIP_PATH%bin/clang++" --offload-arch=gfx1201 main.hip -o main.exe
```

output
```
warpSize from host is 64.
warpSize from device is 32.
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-09-24T15:13:04Z)

Hi @zhang-hui-yulo, `warpSize` has undergone multiple changes with the release of ROCm 7.0, see https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_cpp_language_extensions.html#warpsize. 

The correct way to query warpSize on the host is with hipDeviceGetAttribute() or hipDeviceGetProperties(), for example,
```
int warpSizeHost;
hipDeviceGetAttribute(&warpSizeHost, hipDeviceAttributeWarpSize, deviceId);
```
This correctly returns `32` for gfx1200 on ROCm 7.0.

---

### 评论 #2 — zhang-hui-yulo (2025-09-25T03:26:32Z)

I got it, but I still suggest amd to maintain a compiled time warp size in hip sdk, like the hip doc mentions

```
#if defined(__GFX8__) || defined(__GFX9__)
  #define WarpSize 64
#else
  #define WarpSize 32
#endif
```

---

### 评论 #3 — harkgill-amd (2025-09-29T19:09:10Z)

Appreciate the feedback! The design decision was made to let users define the macro on their end but I'll share this feedback for future discussion.

---
