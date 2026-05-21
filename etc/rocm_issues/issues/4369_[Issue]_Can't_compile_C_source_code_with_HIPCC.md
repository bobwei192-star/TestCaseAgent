# [Issue]: Can't compile C source code with HIPCC

> **Issue #4369**
> **状态**: closed
> **创建时间**: 2025-02-12T16:08:47Z
> **更新时间**: 2026-03-19T10:32:57Z
> **关闭时间**: 2025-02-26T22:24:04Z
> **作者**: Equiel-1703
> **标签**: Under Investigation, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4369

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

Hello everyone!

I'm pretty new to GPU programming and specially with ROCm. While I was doing some experiments to learn how things worked I came across a pretty interesting issue. If I try to compile a **C program** using the HIP API I got the following error:

![Image](https://github.com/user-attachments/assets/917a63f8-b2e8-455c-b1ec-d57cdc119990)

Here's the source code for the program (if it's relevant):
```
#include "hip/hip_runtime.h"
#include <stdio.h>

// HIP kernel function
__global__ void helloFromGPU() {
    printf("Hello, World from GPU!\n");
}

int main() {
    printf("Hello, World from CPU!\n");
    
    // Launch the kernel with 1 block and 1 thread
    helloFromGPU<<<1, 1>>>();
    
    // Wait for GPU to finish before accessing printf output
    int ret = hipDeviceSynchronize();
    
    return 0;
}
```

But if simply rename the file to have the .cpp extension, I can compile it perfectly and execute the output program with no issues:

![Image](https://github.com/user-attachments/assets/42383946-383a-4405-83de-de10eebd16cc)

Why is this happening? Am I doing the correct compilation procedure for HIP programs?

Thanks in advance for any help!

### Operating System

Linux Mint 22.1 (Xia)

### CPU

AMD Ryzen 5 5500U with Radeon Graphics

### GPU

AMD Radeon Graphics gfx90c

### ROCm Version

ROCm 6.3.2

### ROCm Component

HIPCC

### Additional Information

Here's the output of my `hipconfig -f` to better understand the environment I'm running ROCm:
```

HIP version: 6.3.42134-a9a80e791

==hipconfig
HIP_PATH           :/opt/rocm-6.3.2
ROCM_PATH          :/opt/rocm-6.3.2
HIP_COMPILER       :clang
HIP_PLATFORM       :amd
HIP_RUNTIME        :rocclr
CPP_CONFIG         : -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.3.2/include -I/include

==hip-clang
HIP_CLANG_PATH     :/opt/rocm-6.3.2/lib/llvm/bin
AMD clang version 18.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-6.3.2 25012 e5bf7e55c91490b07c49d8960fa7983d864936c4)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.3.2/lib/llvm/bin
Configuration file: /opt/rocm-6.3.2/lib/llvm/bin/clang++.cfg
AMD LLVM version 18.0.0git
  Optimized build.
  Default target: x86_64-unknown-linux-gnu
  Host CPU: znver2

  Registered Targets:
    amdgcn - AMD GCN GPUs
    r600   - AMD GPUs HD2XXX-HD6XXX
    x86    - 32-bit X86: Pentium-Pro and above
    x86-64 - 64-bit X86: EM64T and AMD64
hip-clang-cxxflags :
 -O3
hip-clang-ldflags :
--driver-mode=g++ -O3 --hip-link

== Environment Variables
PATH =/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/opt/rocm-6.3.2/bin

== Linux Kernel
Hostname      :
LinuxMint-Henrique
Linux LinuxMint-Henrique 6.11.0-17-generic #17~24.04.2-Ubuntu SMP PREEMPT_DYNAMIC Mon Jan 20 22:48:29 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
No LSB modules are available.
Distributor ID:	Linuxmint
Description:	Linux Mint 22.1
Release:	22.1
Codename:	xia
```

---

## 评论 (7 条)

### 评论 #1 — ppanchad-amd (2025-02-12T18:23:30Z)

Hi @Equiel-1703. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — sohaibnd (2025-02-18T16:27:15Z)

Hi @Equiel-1703, sorry for the late update. Here is an explanation:

- the actual compiler, amdclang++, only treats .hip files as HIP language source files (allowing device code and kernel launch syntax)
- you're using hipcc which is a wrapper around amdclang++ (or around nvcc if you're on a CUDA platform) that should treat C++ source files (.cpp/.cc) and C source files (.c) as HIP language source files too so the latter case needs to be fixed. In the meantime, if you still want to use C source files, you can add `-x hip` to compile it as a HIP program ([docs](https://rocm.docs.amd.com/projects/llvm-project/en/latest/reference/rocmcc.html#amd-gpu-compilation)).

Let me know if you have any follow-up questions!

---

### 评论 #3 — sohaibnd (2025-02-21T16:55:23Z)

@Equiel-1703 I made a mistake in my comment above, hipcc treating C++ source files (.cpp/.cc) as HIP language source files but not C source files (.c) is intended behaviour.

---

### 评论 #4 — Equiel-1703 (2025-02-25T14:23:55Z)

Hi @sohaibnd ! Sorry for the late reply and thank you very much for the feedback! This means that hipcc only treats .hip and C++ (.cc/.cpp) files as HIP language source code (both kernel launch and device code), right?

---

### 评论 #5 — sohaibnd (2025-02-25T15:29:23Z)

Well CUDA files (.cu/.cuh) are treated as HIP language source files too by hipcc if you're on a ROCm platform, but yes not C source files.

---

### 评论 #6 — Equiel-1703 (2025-02-26T22:24:04Z)

Ok! Thank you very much for the help! 

---

### 评论 #7 — etiennemlb (2026-03-19T10:32:57Z)

C code is not HIP code. C files and not HIP files. Cuda/HIP are superset of C++, not C. OFC, C and C++ are close.

```shell
$ module purge; module load rocm; hipcc -Wall -Wextra -Wpedantic -isystem "${ROCM_PATH}/include" -D__HIP_PLATFORM_AMD__ ./test.c; ldd ./a.out
        linux-vdso.so.1 (0x00007ffdda7f7000)
        libamdhip64.so.6 => /opt/rocm-6.4.3/lib/libamdhip64.so.6 (0x00007f698de08000)
        libstdc++.so.6 => /lib64/libstdc++.so.6 (0x00007f698da00000)
        libm.so.6 => /lib64/libm.so.6 (0x00007f698dd14000)
        libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00007f698dcfa000)
        libc.so.6 => /lib64/libc.so.6 (0x00007f698d600000)
        librocprofiler-register.so.0 => /opt/rocm-6.4.3/lib/librocprofiler-register.so.0 (0x00007f698dc52000)
        libamd_comgr.so.3 => /opt/rocm-6.4.3/lib/libamd_comgr.so.3 (0x00007f6983fbb000)
        libhsa-runtime64.so.1 => /opt/rocm-6.4.3/lib/libhsa-runtime64.so.1 (0x00007f6983c74000)
        libnuma.so.1 => /lib64/libnuma.so.1 (0x00007f698dc43000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f698f8cf000)
        libz.so.1 => /lib64/libz.so.1 (0x00007f698dc29000)
        libzstd.so.1 => /lib64/libzstd.so.1 (0x00007f698d947000)
        libelf.so.1 => /lib64/libelf.so.1 (0x00007f698d92c000)
        libdrm.so.2 => /lib64/libdrm.so.2 (0x00007f698d915000)
        libdrm_amdgpu.so.1 => /lib64/libdrm_amdgpu.so.1 (0x00007f698d908000)
$  module purge; module load rocm; gcc -Wall -Wextra -Wpedantic -isystem "${ROCM_PATH}/include" -L "${ROCM_PATH}/lib" -lamdhip64 -D__HIP_PLATFORM_AMD__ ./test.c; ldd ./a.out
```

Please not that because this is C code, you should include the proper header:
```
#include <hip/hip_runtime_api.h>
// #include <hip/hip_runtime.h>
int main(void) {
    hipDeviceSynchronize();
}
```
Indeed, if the cuda/hip API is in C, the rest of the runtime is not necessarily. But this stuff is semantic fudging, you can include `hip_runtime.h` in C code, I havnt had issue with that since a long time.

---
