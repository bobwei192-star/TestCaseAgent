# [Issue]: lld-link cannot link dll with -fgup-rdc

> **Issue #5467**
> **状态**: open
> **创建时间**: 2025-10-03T08:10:52Z
> **更新时间**: 2025-10-22T14:49:25Z
> **作者**: zhang-hui-yulo
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5467

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

lld-link cannot link -fgpu-rdc dll, I have change the LINK_FLAGS from "-fuse-ld=lld-link" to "-fuse-ld=lld" in build.ninja to use lld to link the dll.


### Operating System

Windows 11 10.0.26100

### CPU

AMD Ryzen 9 7900X3D 12-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 6.4.2

### ROCm Component

HIP

### Steps to Reproduce

main.hip
```
#include <hip/hip_runtime.h>
#include <hip/hip_fp16.h>

__constant__ half g_count[2];

__declspec(dllexport) extern "C" void set_g_count(float c1, float c2) {
    half2 count {c1, c2};
    hipMemcpyToSymbol(g_count, &count, sizeof(g_count));
}
```

kernel.hip
```
#include <hip/hip_runtime.h>
#include <hip/hip_fp16.h>


extern __constant__ half g_count[2];

__global__ void test(half* data) {
    half2 h2{g_count[0], g_count[1]};
    unsafeAtomicAdd((half2*)data, h2);
}

__declspec(dllexport) extern "C" void test_kernel(half* ptr) {
    test<<<1, 64>>>(ptr);
}
```

CMakeLists.txt
```
cmake_minimum_required(VERSION 3.21)
project(hip_project LANGUAGES CXX HIP)

find_package(HIP REQUIRED)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_HIP_STANDARD 17)

set(CMAKE_HIP_ARCHITECTURES gfx1201)

add_library(main SHARED)

target_sources(main PRIVATE
    main.hip
    kernel.hip
)


target_compile_options(main PRIVATE $<$<COMPILE_LANGUAGE:HIP>:-fgpu-rdc>)
target_link_options(main PRIVATE $<$<LINK_LANGUAGE:HIP>:-fgpu-rdc>)
```

build command
```
set PATH=%HIP_PATH%bin;%PATH%
cmake -G Ninja -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

error message
```
[2/2] Linking HIP shared library main.dll
FAILED: main.dll main.lib
C:\WINDOWS\system32\cmd.exe /C "cd . && "D:\Program Files\AMD\ROCm\6.4\bin\clang++.exe" -nostartfiles -nostdlib -O3 -DNDEBUG --offload-arch=gfx1201 -D_DLL -D_MT -Xclang --dependent-lib=msvcrt  -fgpu-rdc --hip-link --rtlib=compiler-rt -fuse-ld=lld-link -shared -o main.dll  -Xlinker /MANIFEST:EMBED -Xlinker /implib:main.lib -Xlinker /pdb:main.pdb -Xlinker /version:0.0 CMakeFiles/main.dir/main.hip.obj CMakeFiles/main.dir/kernel.hip.obj  "D:/Program Files/AMD/ROCm/6.4/lib/amdhip64.lib"  -lkernel32 -luser32 -lgdi32 -lwinspool -lshell32 -lole32 -loleaut32 -luuid -lcomdlg32 -ladvapi32 -loldnames  && cd ."
clang++: error: invalid linker name in argument '-fuse-ld=lld-link'
ninja: build stopped: subcommand failed.
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2025-10-03T14:13:50Z)

Hi @zhang-hui-yulo. Internal ticket has been created to investigate this issue. Thanks!

---
