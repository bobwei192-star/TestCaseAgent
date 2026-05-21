# [Feature/RFC]: Allow caching of HIP compilations

> **Issue #2817**
> **状态**: open
> **创建时间**: 2024-01-17T21:36:57Z
> **更新时间**: 2024-10-08T19:38:31Z
> **作者**: GZGavinZhao
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/2817

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

# tl;dr

We want to introduce caching of HIP compilations. This will greatly alleviate the problem of long compilation times between builds, especially in a CI environment and for distribution packagers, opening the door to rapid iteration/CI/CD, thorough testing, and in general a better developer experience. This feature request boils down to 2 steps:
1. Add support for HIPCC to execute Clang through a compiler wrapper/launcher. ROCm/llvm-project#14
2. Add support to cache HIP compilations in tools like `sccache`. mozilla/sccache#2044, mozilla/sccache#2045

Note that if you're using CMake's native support for HIP, you only need to wait for 2 and export the environment variable `CMAKE_HIP_COMPILER_LAUNCHER=<path-to-sccache>`.

# Motivation
It is well known that the compilation time of HIP programs and libraries grows linearly with respect to the number of GPU architectures to support. Therefore, developers often have to wait for an extremely long time for the entire project to compile even when only a short portion of code is changed. Admittedly, CMake can reduce this burden by only recompiling files that have changed, but only to a certain extent because as soon as the build directory is removed or if a build option changed that requires a rerun of CMake, a majority if not all of the build artifacts becomes invalidated and needs to be recompiled. 

A direct consequence of this is that CI/CD time for HIP projects are massive (ranging anywhere from 30 minutes to several hours) because every CI run needs to compile the entire project from scratch, discouraging thorough testing of HIP support on different GPU models and decreasing developer productivity in general. Distribution packages also have a hard time packaging the ROCm stack, because even if we just want to make a small adjustments to file installation paths, we must recompile the entire project, which usually leads to several hours of wait even on very decent hardware. At Solus, one of our build servers run on a 24-thread Ryzen 9 5900X, and even with this amount of parallelization (`-j24`), packages like rocBLAS, rocFFT, rocSOLVER, RCCL, MIOpen take almost 2 hours to build, and the composable_kernel is the most severe, taking **14 hours** to build _every time_ regardless of how small of a change we made.

# Solution
A similar problem occurs for C/C++ projects, but tools like `ccache` and `sccache` greatly reduce this problem by wrapping the compiler and caching compilation outputs. Even if the CMake build directory is deleted, as long as the `ccache` cache directory is not cleared, the compilation outputs are still cached, therefore allowing maximum re-use of previous compilation artifacts. More notably, there is already `sccache` integration of NVIDIA CUDA for both `nvcc` and `clang`.

Therefore, the solution is to implement HIP support for tools like `sccache`, and then implement support for the HIPCC compiler to use `sccache`. Please see the top section for PRs that implement these features.

# Request for Comments

I have been using this feature to help me package ROCm for Solus, and the experience has been great so far with a much more rapid iteration. I hope this feature can be useful for a wider audience and improve the overall ROCm ecosystem.

Supporting a compiler cache is not an extremely hard task but due to different environments, it is hard to create a _correct_ compiler cache since there are many corner cases to take into account. For example, what if `ROCM_PATH` changed? What if `DEVICE_LIB_PATH` changed? What if no `--offload-arch` is specified and the target architectures now depend on the local machine? Therefore, I hope interested users and relevant parties can provide comments and feedback on current implementations of this feature. I encourage people who need this feature to try out those PRs and report back whether they are useful for you and what needs to improve.

Current limitations:
- [x] Distinguish between different ROCm versions (particularly with the ROCm-Device-Libs bitcode). This shouldn't be an issue for most users.

# Final notes
I believe this is a feature that is worth considering officially by AMD, because this will open up opportunities to ensure the ROCm software stack is being thoroughly tested on all officially supported platform and greatly boosting developer productivity. For example, AMD could easily setup a (remote) shared cache for their CI builders and enable rapid testing and iteration for all supported architectures. This will also increase general developer experience for projects that would like to integrate HIP support.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

HIPCC
