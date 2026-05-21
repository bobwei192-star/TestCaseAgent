# scratch_load_dword returns zeros on GFX942 (MI300X) — correct KD, AQL, and FLAT_SCRATCH setup

> **Issue #6030**
> **状态**: open
> **创建时间**: 2026-03-11T09:19:22Z
> **更新时间**: 2026-03-11T21:53:57Z
> **作者**: Zaneham
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6030

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

Scratch memory reads return zero on GFX942 (MI300X). Private segment loads always produce 0x00000000 regardless of what was stored, even within the same thread on the same wavefront.

I am writing a CUDA compiler that targets AMDGPU directly via HSA, without HIP or the ROCm compiler stack. The compiler produces .hsaco ELF binaries with valid kernel descriptors and dispatches them through the HSA runtime
API. Everything works correctly on RDNA3 (GFX1100) including scratch/private memory. On GFX942 (MI300X), kernarg reads work, LDS works, global memory works, but any value spilled to or explicitly allocated in scratch reads back as zero.

Minimal reproducer: a kernel that allocates a local float array, writes known values, then reads one back into a
global buffer. Thread 0 writes scratch_test[3] = 3.0 and then stores scratch_test[3] to global memory. The global
output is 0.0 instead of 3.0. The kernel descriptor has SCRATCH_EN set in COMPUTE_PGM_RSRC2 and
private_segment_fixed_size is nonzero. The dispatch packet's private_segment_size is set to the value reported by the
executable symbol query (HSA_EXECUTABLE_SYMBOL_INFO_KERNEL_PRIVATE_SEGMENT_SIZE).

I have attached the kernel source, the standalone HSA launcher (pure C, no HIP), and the compiled .hsaco. The launcher uses only public HSA APIs and can reproduce the issue on any MI300X system with the ROCm runtime installed.


This is blocking real workloads. My production kernel (a Monte Carlo neutron transport code, its nuclear physics in case you're curious) has approximately 200 register spills on GFX942 due to the 26-parameter signature. Since every spill round-trips through scratch, the kernel produces entirely wrong results. There is no documentation I can find for what GFX942 specifically requires for scratch setup beyond what the kernel descriptor and AQL packet provide. If there is an additional initialization step I cannot seem to find it.


the runtime or compiler is expected to perform for architected flat scratch on CDNA3, it is not documented anywhere I have looked, including the GFX9 ISA manual, the AMDGPU ABI spec, and the HSA runtime specification. If anyone has any pointers or any ways to tackle this, I am all ears.

[diag_test.c (Change to a .c file).txt](https://github.com/user-attachments/files/25896522/diag_test.c.Change.to.a.c.file.txt)

[tp_diag2.txt](https://github.com/user-attachments/files/25896430/tp_diag2.txt)

The repo is here for the compiler
https://github.com/Zaneham/BarraCUDA
