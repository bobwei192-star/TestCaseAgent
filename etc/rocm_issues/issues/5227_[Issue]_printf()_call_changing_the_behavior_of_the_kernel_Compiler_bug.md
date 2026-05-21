# [Issue]: printf() call changing the behavior of the kernel? Compiler bug?

> **Issue #5227**
> **状态**: closed
> **创建时间**: 2025-08-24T14:03:59Z
> **更新时间**: 2025-09-11T06:32:56Z
> **关闭时间**: 2025-09-11T06:32:56Z
> **作者**: TomClabault
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5227

## 描述

### Problem Description

My application started behaving unexpectedly so I started adding some printf() calls in the kernel to try and debug the values. Turns out that adding printf() calls changes the output of the application which isn't expected.

The same issue happens both on Linux 24 with ROCm 6.4 or on Window 11 with the [HIPSDK 6.42](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html)

### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat) & Windows 11

### CPU

13th Gen Intel(R) Core(TM) i5-13600KF

### GPU

Radeon RX 7900 XTX

### ROCm Version

ROCm 6.4.0.60400-47~24.04

### ROCm Component

HIP

### Steps to Reproduce

```
git clone --recursive https://github.com/TomClabault/HIPRT-Path-Tracer.git HIPRTPathTracer
cd HIPRTPathTracer
git checkout ROCMIssue
git update submodule update --recursive --init
mkdir build
cd build
cmake ..
<compile the application with the generator chosen>
./HIPRTPathTracer
```

Expected output in the console (the logging comes from a printf() in the kernel: [/HIPRT-Path-Tracer/src/Device/kernels/ReSTIR/ReGIR/GridFillTemporalReuse.h](https://github.com/TomClabault/HIPRT-Path-Tracer/blob/ROCMIssue/src/Device/kernels/ReSTIR/ReGIR/GridFillTemporalReuse.h)):
```
PDF: -nan
PDF: -nan
PDF: -nan
```
Application GUI:

<img width="3876" height="2072" alt="Image" src="https://github.com/user-attachments/assets/6d2b97cd-7e9a-440d-ba4c-efb888216d55" />

Un-commenting the printf() call line 57 & 58 of the same kernel [GridFillTemporalReuse.h:58](https://github.com/TomClabault/HIPRT-Path-Tracer/blob/ROCMIssue/src/Device/kernels/ReSTIR/ReGIR/GridFillTemporalReuse.h#L58) and restarting the application with `./HIPRTPathTracer` (no CPU recompilation needed) yields:
```
binPower: 40.000008
PDF: 0.250000
binPower: 40.000008
PDF: 0.250000
binPower: 40.000008
PDF: 0.250000
```
Application GUI:

<img width="3876" height="2072" alt="Image" src="https://github.com/user-attachments/assets/c793db23-f641-4fec-8ed6-b0a8146a1179" />

The second behavior is correct and I don't expect a single printf() call to change the behavior of the application like that?

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Running the application with `rocgdb` doesn't raise any exception so this probably isn't a memory access fault causing undefined beahvior?

---

## 评论 (6 条)

### 评论 #1 — b-sumner (2025-08-24T15:54:13Z)

Hello @TomClabault.  The use of printf can significantly affect an application.  The calling warp waits for the output to be processed by the CPU.  This has many benefits for debugging, etc. but does affect the timing of things significantly.  Also, since printf is not a tiny function, it is not inlined, and this can change the scheduling of all the code around it.

You code could have a race condition or other memory coherence issue leading to the NaNs.  Or there could be a compiler issue.  Do the NaN's disappear when using a lower optimization level?   Do the NaNs appear when the printf is moved before or after the loop? 

---

### 评论 #2 — TomClabault (2025-08-24T16:30:40Z)

Hi @b-sumner 

>You code could have a race condition or other memory coherence issue

Interesting. Are there any tools for checking that maybe? Everything was running fine until some recent changes (quite big, hard to track) seemingly non race-condition-risky. I've already had this exact issue (where the behavior is broken but adding printf() or doing some other changes to the code fixes it) in this codebase, in some other places of the code (although having some pieces in common) however.

Passing "-O1" to HIPRTC (I'm using HIPRTC) gives the second behavior (which is correct). "-O2" and above don't have any effect and result in the first behavior. Is -O2 the default?

- Removing all printfs() from the code results in the first, incorrect, behavior. 
- Moving the printf() from line 57/58 to after the loop [line 68](https://github.com/TomClabault/HIPRT-Path-Tracer/blob/ReGIRCellLightDistributionsFaceBinning/src/Device/kernels/ReSTIR/ReGIR/GridFillTemporalReuse.h#L48) results in the first, incorrect, behavior. Same when moving that printf() to above the loop [line 48](https://github.com/TomClabault/HIPRT-Path-Tracer/blob/ReGIRCellLightDistributionsFaceBinning/src/Device/kernels/ReSTIR/ReGIR/GridFillTemporalReuse.h#L48).
 
The correct behavior is only obtained with -O1 or the printf inside the loop at line 57/58.

---

### 评论 #3 — b-sumner (2025-08-25T01:45:23Z)

-O1 can also change timing, but it could be a compiler issue.    There is also a division by zero at line 60 and if bin_weight also happens to be zero, the result is NaN.  Are you sure this logic is good?

---

### 评论 #4 — TomClabault (2025-08-25T05:39:22Z)

Hmm that's a good point. Fixing that logic fixes the issue and I'm now getting the correct behavior even without the printf. 
But why would the printf help get the correct result even with a logic that produces NaNs? I'm not quite confident that the issue won't come back after I move a few more lines of code around

---

### 评论 #5 — b-sumner (2025-08-25T14:05:38Z)

I believe that standard C++ calls division by 0.0 undefined behavior, and the compiler could clearly see that it would happen.  The print might have impeded its response to that undefined behavior.  Just guessing.

---

### 评论 #6 — TomClabault (2025-09-11T06:32:52Z)

Okay this indeed was because of some issues in my code.

The NaN issue discussed just above as well as using uninitialized variables in some other places of the code. 

---
