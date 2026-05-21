# [Feature]: Shrink rocm-llvm distribution packages by not statically linking libLLVM, libclang-cpp etc.

> **Issue #2703**
> **状态**: closed
> **创建时间**: 2023-12-11T02:21:32Z
> **更新时间**: 2024-04-17T05:01:17Z
> **关闭时间**: 2024-04-17T05:01:17Z
> **作者**: rbberger
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2703

## 负责人

- lamb-j

## 描述

### Suggestion Description

For the various supported systems, the `rocm-llvm` rpm/deb packages are about 1GB of total download size and about 4GB in installation size. The main reason for this seems to be that all `llvm` binaries were statically linked with `libLLVM`, `libclang-cpp` and so on. That means multiple binaries all have their own copy of `libLLVM` (~130MB), `libclang-cpp` (~50MB). It also seems they contain superfluous symbols, since they shrink a bit when applying `strip` on them. The installation also includes static libraries used for linking to llvm/clang libraries.

This makes downloading and installing the ROCm stack unnecessarily cumbersome, specifically when building base containers for development.

Is there a technical reason for the static linking of LLVM? If not, the suggestion would be to make the installation use shared libraries and appropriate RPATHs instead. Debug symbols and static libraries, if needed, should be moved into something like `rocm-llvm-dev` and not be part of the `rocm` use case in the installer.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

rocm-llvm

---

## 评论 (5 条)

### 评论 #1 — kzhuravl (2023-12-11T13:58:32Z)

Hi @rbberger, this feature is somewhat complete, but disabled for now. There is a regression in one of the OpenGL conformance tests (issue with registering llvm options) when we enable dynamic linking.

I will try and find out the status and timeline of enabling this feauture.

---

### 评论 #2 — rbberger (2023-12-11T14:08:17Z)

@kzhuravl as an intermediate step you could at least separate the static libraries/headers that get currently shipped as part of rocm-llvm from the rest of the installation and put them in a development package such as rocm-llvm-dev.

---

### 评论 #3 — kzhuravl (2023-12-11T14:15:05Z)

@rbberger, package split is implemented internally and going to be included in 6.1. We have split llvm into 2 packages: package 1 (rocm-llvm) includes everything needed for compilation. package 2 (rocm-llvm-dev[el]) includes everything needed for compiler and application developers. If you need, I can share package contents for each package.

---

### 评论 #4 — rbberger (2023-12-11T14:19:18Z)

Great! That's a start. Don't need the details, I trust you do something reasonable. :wink: Thx for the insight.

---

### 评论 #5 — rbberger (2024-04-17T05:01:11Z)

Fixed in ROCm 6.1.0

---
