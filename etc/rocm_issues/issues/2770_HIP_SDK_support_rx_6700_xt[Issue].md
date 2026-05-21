# HIP SDK support rx 6700 xt[Issue]: 

> **Issue #2770**
> **状态**: closed
> **创建时间**: 2023-12-27T12:23:10Z
> **更新时间**: 2024-06-19T17:50:53Z
> **关闭时间**: 2024-06-19T17:50:53Z
> **作者**: MRamazan
> **标签**: Windows
> **URL**: https://github.com/ROCm/ROCm/issues/2770

## 标签

- **Windows** (颜色: #c2e0c6)

## 描述

### Problem Description

rx 6700 xt does not support rocm HIP SDK.

### Operating System

win10

### CPU

r5 5600

### GPU

AMD Radeon RX 6700 XT

### Other

_No response_

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — ForeverHappy (2023-12-29T23:00:18Z)

The Windows requirement page for 5.5.1 (Windows release) can be seen here https://rocm.docs.amd.com/en/docs-5.5.1/release/windows_support.html
And as for the latest 6.0 that shows basically the same can be found here https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html

SDK doesn't support 6700 XT according to the docs and for Windows the latest (and only) installer of ROCm for it is version 5.5.1.
HIP and HIPRT on the other hand (like what the Blender Cycles renderer support and use) can be run with the 6700 XT (listed under "Runtime")

In other words, this does not seem to be an "issue" exactly, but more of a feature/support request perhaps?

---

### 评论 #2 — bdenhollander (2023-12-31T01:45:46Z)

RX 6600 is not listed as supported but HIP SDK 5.5.1 works just fine for me on Windows 10. Did you try it and confirm it's not working?

---

### 评论 #3 — han-minhee (2024-01-04T14:34:41Z)

> RX 6600 is not listed as supported but HIP SDK 5.5.1 works just fine for me on Windows 10. Did you try it and confirm it's not working?

Are you doing the development with rocm or just running programs that uses rocm? If the SDK works well, I'd like to see if all the libraries are supported 

---

### 评论 #4 — bdenhollander (2024-01-05T00:08:00Z)

> Are you doing the development with rocm or just running programs that uses rocm? If the SDK works well, I'd like to see if all the libraries are supported

Development on a project that only needs hipftt and hiprtc. I can't find the list of supported libraries in the documentation at the moment but here's a list of lib files installed by the SDK in ROCm\5.5\lib:
```
amdhip64.lib
amd_comgr.lib
amd_comgr0505.lib
hipblas.lib
hipfft.lib
hiprand.lib
hiprtc-builtins.lib
hiprtc.lib
hipsolver.lib
libhipsparse.dll.a
rocalution.lib
rocblas.lib
rocfft.lib
rocrand.lib
rocsolver.lib
rocsparse.lib
```

---

### 评论 #5 — cgmb (2024-01-05T05:36:15Z)

The HIP Runtime works on gfx1031 (the RX 6700 XT's ISA), but none of the math libraries in the HIP SDK are built for gfx1031. The rocFFT/hipFFT libraries use hiprtc to compile their kernels at runtime, which is why they work despite not having been built for that architecture ahead of time. Other libraries, like rocBLAS, rocSOLVER, rocSPARSE and rocRAND, will not function on gfx1031 unless you build them for that architecture yourself (which is not always easy, but can be done).

---

### 评论 #6 — V6ser (2024-02-04T00:35:29Z)

> The HIP Runtime works on gfx1031 (the RX 6700 XT's ISA), but none of the math libraries in the HIP SDK are built for gfx1031. The rocFFT/hipFFT libraries use hiprtc to compile their kernels at runtime, which is why they work despite not having been built for that architecture ahead of time. Other libraries, like rocBLAS, rocSOLVER, rocSPARSE and rocRAND, will not function on gfx1031 unless you build them for that architecture yourself (which is not always easy, but can be done).

Sure, it's just crazy to me that - as you well said - this can be done. What does that mean? AMD is just unwilling to commission change to a few lines of code ensuring compile support for those HIP Runtime cards on Windows? 
They are clearly already capable with a few user modifications. That's baffling to say the least, talking as an AMD investor. I already compiled rocBLAS and other libraries manually, but the rest is such a hustle for an end-user. I can't imagine this reflecting any different than the latest earnings call.

Well done, AMD!

---

### 评论 #7 — MRamazan (2024-02-04T10:29:50Z)

Then, if i follow the steps above can i run my code on GPU  with pytorch?

---

### 评论 #8 — V6ser (2024-02-04T15:42:13Z)

Which steps are you referring to? If you build, compile rocm libs for your architecture, then do the same for pytorch. Sure, you can build pytorch-rocm on Windows.
As of now to build pytorch-rocm all those packages bellow are listed as REQUIRED:
hip - workaround available
hsa-runtime64
amd_comgr
rocrand
hiprand
rocblas, hipblas - Compiled bins for Windows exist on <gfx1032 cards
hipblaslt
miopen - recent support for Windows build.
hipfft
hipsparse
rccl
rocprim
hipcub
rocthrust
hipsolver

AMD has around 0 of those packages working/supported on Windows for your card.

---

### 评论 #9 — ppanchad-amd (2024-06-19T17:50:53Z)

@MRamazan Closing ticket - GFX1031 is not officially supported in HIP SDK 5.7.1

---
