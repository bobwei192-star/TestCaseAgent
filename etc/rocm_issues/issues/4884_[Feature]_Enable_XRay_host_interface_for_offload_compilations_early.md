# [Feature]: Enable XRay host interface for offload compilations early

> **Issue #4884**
> **状态**: closed
> **创建时间**: 2025-06-05T15:49:18Z
> **更新时间**: 2025-06-13T14:48:54Z
> **关闭时间**: 2025-06-13T14:23:15Z
> **作者**: Thyre
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4884

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

### Moviation

Performance tools, e.g. for HPC software like Score-P, need to get information about what functions are executed by a user to present a full overview of the users program.
While some tools rely on sampling, tools utilizing instrumentation methods require supported compiler methods. Both GCC and LLVM support `cyg_profile_func` via `-finstrument-functions`.

Performance tools can then look up the function with tools like `addr2line` (or other native interfaces).
This works just fine in most cases. However, there are significant drawbacks, e.g. that the functions cannot be easily filtered or are dispatched for _every_ function, which can be especially bad for C++ codes like LULESH causing high overhead and clutter in the results.

---

Performance tools have started to implement alternative ways to get this information, e.g. using native LLVM IR plug-ins. Such features exist e.g. in TAU and Score-P. However, this imposes other challenges for tool developers, as the LLVM IR interface is not stable at all, requiring constant patching.

Additionally, while filtering _is_ possible at compile-time, changing potential filters requires rebuilding the software. While this may be fine for many codes, one doesn't want to rebuild GROMACS just to change a small filter.

---

LLVM includes another interface for a very long time (at least since LLVM 5.0): XRay.
More information can be found in this paper: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45287.pdf

Tools implementing the interface as described in the LLVM `xray/xray_interface.h` header are able to get similar information to `cyg_profile_func`, but with the option to patch and unpatch functions during runtime, therefore significantly reducing overhead and removing the need to re-compile the program.

The interface itself is also not perfect, as LLVM lacks handling for exceptions (similar to `cyg_profile_func`) and Fortran support missing at the moment.
However, this interface still offers significant enough benefits, that tools started to look into this for integration.

A prototype was developed for Score-P by people from TU Darmstadt, see: https://github.com/tudasc/scorep-xray
We're now in the process of integrating this properly into Score-P, with the current status being available here: https://perftools.pages.jsc.fz-juelich.de/cicd/scorep/branches/MR578/latest.tar.gz

It's worth noting though that XRay can also be used just with LLVM components, as described here: https://llvm.org/docs/XRay.html

### XRay and offloading

There's one significant issue, affecting ROCm in particular due to the heavy interest in, well, offloading work to accelerators:

```
$ amdclang -fopenmp --offload-arch=gfx1201 -fxray-instrument test.c
clang: error: unsupported option '-fxray-instrument' for target 'amdgcn-amd-amdhsa'
$ hipcc --offload-arch=gfx1201 -fxray-instrument test.cpp
clang++: error: unsupported option '-fxray-instrument' for target 'amdgcn-amd-amdhsa'
failed to execute:/opt/apps/software/ROCm/6.4.0/lib/llvm/bin/clang++  --offload-arch=gfx1201 -O3 --driver-mode=g++ -O3 --hip-link  -fxray-instrument -x hip test.cpp
```

This is fine, we don't expect the interface to work on accelerators. However, `-Xarch_host` is broken, and doesn't active the interface for the host either.

```
$ amdclang++ -fopenmp --offload-arch=gfx1101 -Xarch_host -fxray-instrument test.cpp && objdump -h ./a.out | grep xray || echo "header not found"
clang++: warning: argument unused during compilation: '-Xarch_host -fxray-instrument' [-Wunused-command-line-argument]
header not found
```

This issue is described in https://github.com/llvm/llvm-project/issues/140748 and will be resolved in LLVM 21.1.0.

### The main question

If possible, we would love to see the required changes to support this feature being ported earlier than LLVM 21.1.0 for ROCm. Given that ROCm 6.4.0 is based on LLVM 19.x, waiting for LLVM 21.x would take quite a while where we wouldn't be able to offer this feature without breaking analyzing offload programs as well.
The LLVM plug-in is an alternative option, but not ideal if people try to mix ROCm e.g. with LLVM.

The upstream PR is available here: https://github.com/llvm/llvm-project/pull/141043


### Operating System

Ubuntu 22.04 LTS, Rocky Linux 9

### GPU

gfx1101, gfx1201, gfx90a

### ROCm Component

llvm-project

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-06-06T13:14:27Z)

Hi @Thyre. Internal ticket has been created to address this feature request. Thanks!

---

### 评论 #2 — tcgu-amd (2025-06-13T14:23:15Z)

Hi @Thyre, thanks for reaching out! The commit is actually already in amd-staging, and we have just promoted it be included in the ROCm 7.0 release. Thanks! 

---

### 评论 #3 — Thyre (2025-06-13T14:48:54Z)

Thanks a lot for the quick response and update. Great to hear!

---
