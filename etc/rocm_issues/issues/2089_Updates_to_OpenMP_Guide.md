# Updates to OpenMP Guide

> **Issue #2089**
> **状态**: closed
> **创建时间**: 2023-04-26T22:29:41Z
> **更新时间**: 2023-05-03T15:55:57Z
> **关闭时间**: 2023-05-03T15:55:56Z
> **作者**: saadrahim
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2089

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- Naraenda

## 描述

List of things to modify:

-	OpenMP Usage: “The example programs can be compiled and run by pointing the environment variable AOMP to the OpenMP install directory.”
o	There is no AOMP setting in the example command lines that follows this statement. I tested the command lines and they work without setting AOMP, so I suggest replacing AOMP with ROCM_PATH. The only problem with the example is that the “make run” effect is to attempt to create a binary file in the same folder in which we are running the command. If you are not sudo on the system, you will get a permission error (that’s what I got). If I manually copy-paste the compile command and replace -o veccopy with -o /tmp/veccopy, everything works as expected. It even runs successfully.
o	-fopenmp -offload-arch is not shown when running “make run” in the build command. It uses the more classical and verbose “-fopenmp -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a”. Not sure if this is an issue, but I believe we should make it clear to users, something like:
	The compiler also accepts the alternative offloading notation “-fopenmp -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=<gpu-arch>
	I am only mentioning this because this is what llvm/clang trunk expects as well.
-	Environment Variables: OMPX_DISABLE_MAPS
o	Please remove this entry from the list. It is turned off by default and it does nothing when turned on. We are in the process of cleaning up this support in the runtime, but still not done. Once we have a new cleaner design and implementation, I will provide user manual information
-	Asynchronous Behavior in OpenMP Target Regions
o	This no longer applies to our runtime, due to a recent upgrade in a software module. Please remove this section from the manual.

-	Xnack capability: this section needs rewriting. I am proposing the text below here:

When enabled, Xnack capability allows GPU threads to access CPU (system) memory, allocated with OS-allocators, such as malloc, new, and mmap.
Xnack must be enabled both at compile- and run-time. To enable xnack support at compile-time, the programmer should use
--offload-arch=gfx908:xnack+
or, equivalently
--offload-arch=gfx908
(this second case is called xnack-any and it is functionally equivalent to the first case).
At runtime, programmers enable Xnack functionality on a per-application basis using an environment variable:
HSA_XNACK=1 ./<executable>

When Xnack support is not needed, then applications can be built to maximize resource utilization using:
--offload-arch=gfx908:xnack-
At runtime, the HSA_XNACK environment variable can be set to 0, as Xnack functionality is not needed.



