# [Issue]: No warning should be given when using CMAKE_HIP_ARCHITECTURES=gfx90a in CMake

> **Issue #4296**
> **状态**: open
> **创建时间**: 2025-01-24T20:09:36Z
> **更新时间**: 2025-03-08T09:40:39Z
> **作者**: ye-luo
> **标签**: Under Investigation, N/A, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4296

## 标签

- **Under Investigation** (颜色: #0052cc)
- **N/A** (颜色: #ededed)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

I got misleading CMake warnings and it should be printed at all. See details in the "steps to reproduce"
The underlying issue is why `hip-config-amd.cmake` tries to detect AMD GPUs even `CMAKE_HIP_ARCHITECTURES` has been given explicitly. It is completely unnecessary and slow down CMake invocation.

### Operating System

SLES 15.4

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 6.3.0

### ROCm Component

HIP

### Steps to Reproduce

To reproduce the warning, AMD GPU should not be available.
Reproducer https://github.com/ye-luo/cmake_gpu/blob/master/test_rocm/CMakeLists.txt
When I give explicit architecture via `CMAKE_HIP_ARCHITECTURES`
```
mkdir build; cd build
cmake -DCMAKE_CXX_COMPILER=amdclang++ -DCMAKE_HIP_ARCHITECTURES=gfx90a ..
```
I should not see the following warning since I'm using well documented option "CMAKE_HIP_ARCHITECTURES"
`AMDGPU_TARGETS` should not be exposed to users at all.

```
CMake Warning (dev) at /soft/compilers/rocm/rocm-6.3.0/lib/cmake/hip/hip-config-amd.cmake:91 (message):
   AMDGPU_TARGETS was not set, and system GPU detection was unsuccsesful.
   
   The amdgpu-arch tool failed:
   Error: 'Failed to get device count'
   Output: ''
   
   As a result, --offload-arch will not be set for subsuqent
   compilations, and the default architecture
   (gfx906 for dynamic build / gfx942 for static build) will be used

Call Stack (most recent call first):
  /soft/compilers/rocm/rocm-6.3.0/lib/cmake/hip/hip-config.cmake:149 (include)
  /soft/buildtools/cmake/3.28.3/share/cmake-3.28/Modules/CMakeFindDependencyMacro.cmake:76 (find_package)
  /soft/compilers/rocm/rocm-6.3.0/lib/cmake/hipblas/hipblas-config.cmake:90 (find_dependency)
  CMakeLists.txt:9 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.
```
This warning is actually misleading. The final generated commands do correctly pick up `gfx90a` instead of what are mentioned in the warning.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-01-27T16:08:29Z)

Hi @ye-luo, thanks for the report. I was able to reproduce the warnings which are a result of the device/arch checks done at https://github.com/ROCm/clr/blob/amd-staging/hipamd/hip-config-amd.cmake.in#L77-L107. These can probably be skipped if  
 a target is already defined by `CMAKE_HIP_ARCHITECTURES`. An internal ticket has been created to address this issue.

---

### 评论 #2 — harkgill-amd (2025-02-18T19:49:23Z)

@ye-luo, please see the latest version of `hip-config-amd.cmake.in` in amd-staging [here](https://github.com/ROCm/clr/blob/amd-staging/hipamd/hip-config-amd.cmake.in). The latest version includes https://github.com/ROCm/clr/commit/935b53826142c585032a0904fb18acaba3f61996, which specifies that gfx906 and gfx942 will only be used **for compiling device code in C++ language mode** if amdgpu-arch fails. It also now uses `GPU_TARGETS` rather than `AMDGPU_TARGETS` as the latter has been deprecated.

After syncing with the CLR folks, there were a couple reasons as to why we decided to go with a minor change to the warning message rather than a change in logic.

1. GPU_TARGETS is for setting the GPU's to be compiled when using the C++ language with hip::device target. CMAKE_HIP_ARCHITECTURES is used to set the HIP_ARCHTECTURES property default value, which is used for setting the gpus for the HIP language, not the C++ language. Mixing these two together could lead to confusion.
2. hip-config.cmake is expected to work with any cmake version and cannot assume you are using a version that has CMAKE_HIP_ARCHITECTURES defined.
3. It would be more correct for an application/library that's enforcing a cmake version to set GPU_TARGETS equal to CMAKE_HIP_ARCHITECTURES rather than in hip-config.cmake.

The current warning message no longer misleads user's on how the hip sources are compiled. Please let me know if you have any questions regarding these changes.

---

### 评论 #3 — ye-luo (2025-02-18T21:05:19Z)

Based on ["for compiling device code in C++ language mode"](https://rocm.docs.amd.com/en/latest/conceptual/cmake-packages.html#compiling-device-code-in-c-language-mode), this mode is for users stuck with < CMake 3.21. Could you make this warning away when using CMake >=3.21?

> hip-config.cmake is expected to work with any cmake version and cannot assume you are using a version that has CMAKE_HIP_ARCHITECTURES defined.

It can detect the version of CMake and the existence of `CMAKE_HIP_ARCHITECTURES`, it doesn't need to assume anything.

---

### 评论 #4 — harkgill-amd (2025-03-07T18:52:40Z)

> Based on ["for compiling device code in C++ language mode"](https://rocm.docs.amd.com/en/latest/conceptual/cmake-packages.html#compiling-device-code-in-c-language-mode), this mode is for users stuck with < CMake 3.21. Could you make this warning away when using CMake >=3.21?

The C++ language mode can be used by users with **any** CMake version while HIP language mode requires CMake >= 3.21. 

Removing this warning when CMake >= 3.21 would not be correct as the C++ language mode is still valid in this case.

---

### 评论 #5 — ye-luo (2025-03-08T09:40:38Z)

`CheckLanguage` is there to check if HIP language mode is in use.

---
