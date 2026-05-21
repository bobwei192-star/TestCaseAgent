# [Issue]: HIPRTC allocates unusually high amounts of LDS memory when compiling a kernel

> **Issue #3806**
> **状态**: closed
> **创建时间**: 2024-09-24T18:52:23Z
> **更新时间**: 2024-10-02T18:19:42Z
> **关闭时间**: 2024-10-02T18:19:41Z
> **作者**: TomClabault
> **标签**: Under Investigation, ROCm 5.7.1, AMD Radeon RX 7900 XTX, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3806

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

HIPRTC allocates LDS memory on its own (isn't LDS allocation a programmer-only choice?) and in unreasonable amounts (~45k bytes) when compiling my kernels at runtime. This drastically reduces the occupancy of my kernels and kills performance.

The amount of LDS allocated is retrieved by calling `hipFuncGetAttribute()`. Radeon GPU Profiler also reports the same high-amount of LDS used when profiling my kernels.

I can reproduce this (although not on a minimal reproducer unfortunately) consistently on both Ubuntu 22.04 & Windows 11 with ROCm 6.2.0 and ROCm 5.7.1 respectively.

The only difference in my kernel between the version that allocates way too much LDS and the one that doesn't is the change from `int priority;` to `char priority;` ([link to Github diff](https://github.com/TomClabault/HIPRT-Path-Tracer/compare/d546340..ffe540a))

To begin with, is HIPCC "allowed" to allocate LDS on its own if it judges that this is going to benefit performance? Are there known issues with such automatic LDS allocation?

### Operating System

Windows 11 & Ubuntu 22.04

### CPU

Inte i5 13600KF

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.0, ROCm 5.7.1

### ROCm Component

HIP, HIPCC

### Steps to Reproduce

Not a minimal reproducer but I can reproduce it consistently on both Windows and Ubuntu 22.04 with ROCm 5.7.1 & ROCm 6.2.0 respectively:

Clone the repository of my project and build it with CMake:

```
git clone -b ROCmIssueLDSHighAmount https://github.com/TomClabault/HIPRT-Path-Tracer.git --recursive
cd HIPRT-Path-Tracer
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
```

Compile with your build system and run (set HIPRTPathTracer as the startup project if using the Visual Studio generator on Windows).

The program outputs the following (on Windows):

```
hiprt ver.02004
Executing on 'AMD Radeon RX 7900 XTX'
Kernel "ReSTIR_DI_InitialCandidates" compiled in 2127ms.
        96 registers.
        59392 shared memory.
Kernel "ReSTIR_DI_SpatialReuse" compiled in 1467ms.
        96 registers.
        62464 shared memory.
Kernel "FullPathTracer" compiled in 4256ms.
        96 registers.
        53248 shared memory.
```
50k+ bytes of shared memory is way too high and I do not use shared memory in my kernels.

The expected amount is way lower than that.
Checking out the other branch that does not show the issue and building again:

```
git checkout ROCmIssueLDSFix
<Build with build system>

./HIPRTPathTracer
```

Run the program and it then outputs:
```
hiprt ver.02004
Executing on 'AMD Radeon RX 7900 XTX'
Kernel "ReSTIR_DI_InitialCandidates" compiled in 2077ms.
        96 registers.
        6144 shared memory.
Kernel "ReSTIR_DI_SpatialReuse" compiled in 1452ms.
        96 registers.
        9216 shared memory.
Kernel "FullPathTracer" compiled in 4224ms.
        96 registers.
        0 shared memory.
```

Which is way more reasonable, but even then, it should be 0. I am not using shared memory in any of my kernels.

The only difference between the two branches is a variable type change in a stack structure (which can be made manually, there's not even a need to checkout another branch actually).

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2024-09-26T15:48:28Z)

Hi @TomClabault, an internal ticket has been created to further analyze this issue. Thanks!

---

### 评论 #2 — jamesxu2 (2024-09-30T20:01:57Z)

Hi @TomClabault ,

To answer your question - no, HIPCC should not automatically allocate LDS, and it is strange that you're observing this. LDS can be allocated either by marking a variable inside a kernel with ```__shared__``` or passing a nonzero sharedMemBytes when launching your kernel. 

I see a use of ```__shared__``` [here in Intersect.h](https://github.com/TomClabault/HIPRT-Path-Tracer/blob/124eed3a9fea548319c2bb3966d6f637f7e308a1/src/Device/includes/Intersect.h#L110-L113) - are you sure it's not this that's causing use of shared memory (It's only commented out in the ROCmIssueLDSHighAmount branch). 

---

I'm giving your application from the ROCmIssueLDSHighAmount branch a try on Ubuntu 2204 - do you expect to see this output (no info on how much shared memory is used) followed by a GUI window opening and closing immediately?

```
$ ./HIPRTPathTracer
hiprt ver.02004
Executing on 'Radeon RX 7900 XT'
Kernel "ReSTIR_DI_InitialCandidates" compiled in 7ms.
Kernel "ReSTIR_DI_SpatialReuse" compiled in 0ms.
Kernel "FullPathTracer" compiled in 1ms.
```

Additionally, I'm not sure how you're using ```hipFuncGetAttributes()``` with HIPRTC-compiled kernels - I believe you can only get a function handle of type **hipFunction_t** from a HIPRTC-compiled kernel through hipModuleGetFunction, and you can't pass it as the second argument to [hipFuncGetAttributes](https://rocm.docs.amd.com/projects/HIP/en/latest/doxygen/html/group___module.html#ga18a72890686975fdd46c7c8a7bb5a607) which expects a function pointer to the kernel. Trying to do so results in "Error: invalid device symbol".

---

### 评论 #3 — meistdan (2024-10-01T02:17:14Z)

Try using launch bounds.

---

### 评论 #4 — TomClabault (2024-10-01T06:54:17Z)

Hi @meistdan , @jamesxu2 

@meistdan Using `__launch_bounds__` does indeed fix the problem. That's what I've been using as a quick fix but this looks like sidestepping the issue and maybe that this is in fact hiding another problem?

@jamesxu2 
> To answer your question - no, HIPCC should not automatically allocate LDS, and it is strange that you're observing this.

Some sources lead me to believe that HIPCC can spill registers to shared memory if needed? Is that correct?

> I see a use of __shared__ [here in Intersect.h](https://github.com/TomClabault/HIPRT-Path-Tracer/blob/124eed3a9fea548319c2bb3966d6f637f7e308a1/src/Device/includes/Intersect.h#L110-L113)

I removed them on both branches just to be sure. The results are the same.

> do you expect to see this output (no info on how much shared memory is used)

I pushed a fix for that, that was my bad. Could you please pull and try again?

> followed by a GUI window opening and closing immediately?

This part is expected. I tried to simplify the behavior of the application for this issue to focus just on the shared memory issue rather than the whole runtime.

> Additionally, I'm not sure how you're using `hipFuncGetAttributes()`

That was a typo in the description of the issue. I'm using `hipFuncGetAttribute()` without the s at the end which takes an `hipFunction_t` as argument.

---

### 评论 #5 — jamesxu2 (2024-10-02T18:19:41Z)

Hello @TomClabault , thanks for updating your repo, I was able to reproduce your findings.

After some further research, I believe I'm mistaken and you're correct here - HIPCC does indeed spill register contents into LDS if they're under pressure, and it [actually says this in the documentation](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/cpp_language_extensions.html#compiler-impact). 

Based on some discussion with the compiler team, I believe the compiler might be breaking up your StackPriorityEntry struct via [SROA](https://llvm.org/docs/Passes.html#sroa-scalar-replacement-of-aggregates) which are then stored in SGPR/VGPR registers (increasing register pressure) to the point of running out of room, at which point the registers are spilling into LDS via the [promote-alloca-to-lds optimization](https://llvm.org/doxygen/AMDGPUPromoteAlloca_8cpp_source.html). Suppressing this behaviour via launch bounds is one way to prevent the compiler from performing this "optimization".

I don't think this hides another problem and it's safe to continue using launch bounds. This issue more likely reveals a shortcoming in these overeager compiler optimizations. The heuristics guiding the use of these optimizations aren't bulletproof and I think your workload just exposes one edgecase in which they lead to a performance degradation.

---
