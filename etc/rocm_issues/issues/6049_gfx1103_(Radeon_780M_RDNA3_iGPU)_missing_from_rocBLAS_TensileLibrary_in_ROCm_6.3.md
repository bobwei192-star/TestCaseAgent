# gfx1103 (Radeon 780M / RDNA3 iGPU) missing from rocBLAS TensileLibrary in ROCm 6.3.2

> **Issue #6049**
> **状态**: closed
> **创建时间**: 2026-03-20T17:11:47Z
> **更新时间**: 2026-04-13T03:00:53Z
> **关闭时间**: 2026-04-13T03:00:53Z
> **作者**: MageofCode
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6049

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

## Hardware
- APU: AMD Ryzen 9 7940HS
- iGPU: AMD Radeon 780M (gfx1103, RDNA3)
- RAM: 24GB shared (UMA architecture)
- OS: Linux Mint 22.2 (Ubuntu 24.04 base)
- ROCm version: 6.3.2-66

## Summary
rocBLAS in ROCm 6.3.2 includes TensileLibrary files for every discrete RDNA3 GPU 
but is missing gfx1103 — the iGPU variant used in all Ryzen 7000 series APUs. 
This causes any application that calls rocBLAS matrix operations to crash at 
runtime on gfx1103 hardware.

## Exact Error
rocBLAS error: Cannot read /opt/rocm/lib/rocblas/library/TensileLibrary.dat: 
Illegal seek for GPU arch: gfx1103

List of available TensileLibrary Files:
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1100.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1101.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1102.dat"
(gfx1103 absent from this list)

## What Is Present vs Missing

RDNA3 discrete GPUs — all supported:
- gfx1100 — RX 7900 XTX / 7900 XT
- gfx1101 — RX 7800 XT / 7700 XT
- gfx1102 — RX 7600

RDNA3 iGPU — not supported:
- gfx1103 — Radeon 780M / 760M (Ryzen 7000 series APU)

## Confirmed Working
- ROCm correctly detects gfx1103 via rocminfo
- Compiling HIP code with --offload-arch=gfx1103 succeeds
- Custom compiled HIP kernels run correctly on gfx1103
- The gap is specifically rocBLAS TensileLibrary runtime support

## Why This Matters
gfx1103 is not a niche or edge case chip. It ships in:
- Every AMD Ryzen 7000 series laptop (7940HS, 7840HS, 7640U etc)
- Popular mini PCs (GEEKOM A7, Minisforum UM780, etc)
- A large and growing segment of consumer AMD hardware

It is arguably the most widely deployed RDNA3 chip in existence. As AI inference 
on consumer hardware grows — local LLMs, image generation, etc — gfx1103 users 
represent a significant and underserved user base.

Applications like KoboldCPP, llama.cpp, and others can successfully compile and 
run GPU accelerated inference on gfx1103 using custom HIP kernels. The missing 
TensileLibrary support is the specific bottleneck preventing newer versions of 
these applications from working correctly.

## Request
Please add gfx1103 to the rocBLAS TensileLibrary build targets alongside the 
existing RDNA3 discrete GPU entries. Given the architectural similarity to 
gfx1100/1101/1102 this should be a relatively contained addition.

A fallback path or graceful degradation when TensileLibrary is missing for a 
given arch would also significantly improve the user experience for iGPU users.

## References
- KoboldCPP issue filed separately describing the application-level impact:
- https://github.com/LostRuins/koboldcpp/issues/2055
- gfx1103 HIP compilation confirmed working with LLAMA_HIPBLAS=1 and 
  GPU_TARGETS=gfx1103

---

## 评论 (4 条)

### 评论 #1 — amd-nicknick (2026-03-24T05:39:17Z)

Hi @GallinX, ROCm 6.3.2 does not support gfx1103. We're actively working on support for APUs and Radeon GPUs in newer ROCm releases. I suggest giving TheRock nightlies a try: https://github.com/ROCm/TheRock/blob/main/RELEASES.md
We provide prebuilt ROCm supporting gfx1103 there. Thanks!

---

### 评论 #2 — MageofCode (2026-03-25T14:43:30Z)

@amd-nicknick Thanks Nick i did that already! ^^ its how i got KoboldCPP ver.107 running after i compiled the program from source. here is my full report 

"KoboldCpp 1.107.3 compiled from source runs perfectly on gfx1103 with full ROCm
acceleration. KoboldCpp 1.110 compiled from source crashes on warmup with two
separate issues.
Issue 1 — Missing TensileLibrary for gfx1103

rocBLAS has TensileLibrary files for every RDNA3 discrete GPU but not the iGPU variant:

Present:

    TensileLibrary_lazy_gfx1100.dat (RX 7900 series)
    TensileLibrary_lazy_gfx1101.dat (RX 7800 series)
    TensileLibrary_lazy_gfx1102.dat (RX 7600)

Missing:

    TensileLibrary_lazy_gfx1103.dat (Radeon 780M/760M — most common RDNA3 chip)

Error produced:
rocBLAS error: Cannot read TensileLibrary.dat: Illegal seek for GPU arch: gfx1103
Issue 2 — Flash Attention kernel crash

Even with --noflashattention workaround for Issue 1, the FA kernel crashes:

HIP kernel flash_attn_ext_f16 has no device code compatible with HIP arch 1300
Memory access fault by GPU node-1 on address (nil)

Root cause appears to be the new warp-level FA kernels introduced in 1.110 which
were tuned for discrete RDNA3 CU counts. The 780M has fewer Compute Units than
discrete cards and the warp scheduler hangs.

Ver.107.3 used a more generic FA kernel path (fattn-mma-f16) which works fine on
the 780M. 1.110 switched to fattn-wmma-f16 which does not.
Workaround

Disabling FlashAttention entirely allows 1.110 to run but this is a regression
from 1.107.3 which ran with FA enabled and stable."

just to confirm:"you are actively working on support for APUs and Radeon GPUs in newer ROCm releases."

meaning sopport for gfx1103 we at some point be merged this repo?

thank you for taking the time to address my concerns! ^^ 



---

### 评论 #3 — amd-nicknick (2026-03-30T10:55:42Z)

@GallinX, I am a little confused, for the issue 1: rebuilding with TheRock nightlies for gfx1103 will result in missing Tensile libraries?
I checked the latest nightlies tarball `therock-dist-linux-gfx110X-all-7.13.0a20260329.tar.gz`, it does contain the dat files. (Perhaps it's not located correctly?)

<img width="338" height="213" alt="Image" src="https://github.com/user-attachments/assets/e5db300d-5d79-4b1e-80d1-b2c81cc0b586" />

For the custom kernel path, that looks like a compilation issue in KoboldCpp not targeting gfx1103 when compiling the kernel. You'd need to raise that to the KoboldCpp repo.

For newer ROCm releases, we're migrating the standard version release (7.1, 7.2 ...) to the new TheRock build system. After the migration you could expect regular support to a wider variety of iGPU and dGPU targets having release and fixes much more regularly.

---

### 评论 #4 — amd-nicknick (2026-04-13T03:00:53Z)

Closing due to inactivity, if you have any further questions, feel free to reopen or create a new issue. Thanks!

---
