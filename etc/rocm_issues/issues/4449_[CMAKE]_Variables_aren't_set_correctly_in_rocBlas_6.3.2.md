# [CMAKE] Variables aren't set correctly in rocBlas 6.3.2

> **Issue #4449**
> **状态**: open
> **创建时间**: 2025-02-12T13:08:05Z
> **更新时间**: 2025-03-06T09:50:15Z
> **作者**: jdumke
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4449

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- TorreZuk

## 描述

Heelo,
sometimes it makes me curious how you get your builds done. In this case some CMAKE-variables aren't set in your scripts.
I tried to build rocBlas with the "T_rocblas" make-target on cmd.
Details are in the tarball. 
[rocblas_issue.tar.gz](https://github.com/user-attachments/files/18768247/rocblas_issue.tar.gz)
The variable in question are:
CMAKE_CXX_COMPILER
CMAKE_MAKE_PROGRAM

 

---

## 评论 (11 条)

### 评论 #1 — ppanchad-amd (2025-02-12T14:29:47Z)

Hi @jdumke. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — TorreZuk (2025-02-12T16:25:23Z)

@jdumke can you provide the link to the source of your build script you used as it is clear it is not building from the rocBLAS repo guide (install.sh or rmake.py) from https://github.com/ROCm/rocBLAS.  The cmake -DCMAKE_TOOLCHAIN_FILE=toolchain-linux.cmake  (a root level file) will set CMAKE_CXX_COMPILER but your script needs to be triaged to the provider for fixes to be advised.  Thanks.

---

### 评论 #3 — jdumke (2025-02-12T17:56:10Z)

Sure, I tried to build rocBlas with the following commandline:
make -f ./ROCm/tools/rocm-build/ROCm.mk -j8 T_rocblas

ROCm.mk like provided by the ROCm/ROCm repo for Rocm-6.3.2.

It seems, there are some inconsistencies between the several subprojects.

By the way, is hipblaslt a hard dependency?

---

### 评论 #4 — TorreZuk (2025-02-13T23:08:13Z)

Still waiting for other investigators to comment.   For a standard build hipblaslt yes it is a hard dependency. 
You can build without the GEMM assembly backends with -DBUILD_WITH_HIPBLASLT=OFF  and -DBUILD_WITH_TENSILE=OFF, just run python script rmake.py --help to see various options.  But once you go down the build customization road you will diverge from the tested release.

---

### 评论 #5 — jdumke (2025-02-14T10:32:00Z)

I got your point, thanks. As workaround I use the precompiled hipblaslt. Hipblaslt doesn't compile for my gfx's, so I've to tweak around.

---

### 评论 #6 — TorreZuk (2025-02-14T15:15:20Z)

If just makig a personal build you are not sharing with other users (and other gfx) and your gfx isn't supported by hipBLASLt then just build rocblas with additional cmake argument -DBUILD_WITH_HIPBLASLT=OFF or if using rmake.py --no_hipblaslt

---

### 评论 #7 — jdumke (2025-02-14T22:00:53Z)

Thanks for helping me with the side question.
Another problem raised, none of the installed fortram compilers seem to fit, I can't figure out why so far.

---

### 评论 #8 — jdumke (2025-02-15T19:47:12Z)

I find the reason for the  main question.
When building with ROCm.mk (which I use to build the full stack, one day) the script build_rocblas.sh from the same directory is invoked, this file calls cmake with -DCMAKE_TOOLCHAIN_FILE=toolchain-linux.cmake (line 39). After deleting this line, the configuration runs until the compiler flag test. 
If I understand it correctly, the mentioned test is intended to work as follows:
 For all requested offload-architectures do:
1. pass the given flags to the compiler in question to build CMakeCXXCompilerId.cpp deep in the subdirectories of the sources.
2. the program performs it's magic to produce a cryptic return code.
3. decrypt this return code to a proper c-identifier

Is this right?
When I perform steps 1 and 2 by hand with amdclang all went fine, but while building all tests fail. 
Okay, the idea is correct, but the sourcecode to test against is wrong, I think, but where is the correct one?

---

### 评论 #9 — TorreZuk (2025-03-04T21:40:00Z)

@ppanchad-amd have you gotten any feedback from the owner of the makefile ROCm.mk ?    Should we move this issue to their repo?

---

### 评论 #10 — ppanchad-amd (2025-03-05T19:26:58Z)

@TorreZuk ROCm.mk is owned by DevOps.  I'll move the issue to ROCm/ROCm and we'll continue investigating from there. Thanks!

---

### 评论 #11 — jdumke (2025-03-06T09:50:14Z)

Due to working reasons my rocm-ambitions are actually reduced. I found out something:
1. The build-control script (build_rocblas.sh) in  ROCm/tools/rocm-build uses a different tool-chain file like your project does, but calling your CMakeLists.txt. There seem to be differences between both worlds in naming and using such variables.

---
