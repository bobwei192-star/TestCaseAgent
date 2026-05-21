# [Issue]: v_dot4_i32_i8 treats int8 operands as unsigned on RDNA3 (gfx1101)

> **Issue #6126**
> **状态**: open
> **创建时间**: 2026-04-07T20:08:58Z
> **更新时间**: 2026-05-19T02:06:58Z
> **作者**: VX1D
> **标签**: status: triage, status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/6126

## 标签

- **status: triage** (颜色: #585dd7)
- **status: fix submitted** (颜色: #75d97e)

## 负责人

- Jonathan03ant

## 描述

### Problem Description

`v_dot4_i32_i8` produces wrong results on gfx1101. Negative int8 values are treated as unsigned.
`-1` (0xFF) becomes 255.

`q=[1,-1,1,-1]`, `k=[1,1,1,1]`: expected `0`, got `512`. The instruction is computing `1*1 + 255*1 + 1*1 + 255*1 = 512` ; treating `-1` (0xFF) as 255.
EDIT:
`v_dot4_i32_i8` does not exist as a native instruction on GFX11 (RDNA3). The hardware offers `v_dot4_i32_iu8`, which encodes signedness of each operand via `neg_lo` modifier bits. LLVM's SelectionDAG correctly lowers `v_dot4_i32_i8` to `v_dot4_i32_iu8 neg_lo:[1,1,0]` when compiling device code but **inline asm strings are passed directly to the assembler, bypassing this lowering**. The assembler accepts `v_dot4_i32_i8` as an alias and emits `v_dot4_i32_iu8` with `neg_lo` unset (all unsigned), which explains the observed behaviour.
### Operating System

Arch Linux rolling

### CPU

AMD Ryzen 7 9800X3D

### GPU

AMD RX 7800 XT

### ROCm Version

7.2.1

### ROCm Component

_No response_

### Steps to Reproduce

```cuda
extern "C"
__global__ void test_dot4(int* out) {
    int q = (1) | (0xFF << 8) | (1 << 16) | (0xFF << 24);  // [1, -1, 1, -1]
    int k = (1) | (1 << 8) | (1 << 16) | (1 << 24);        // [1, 1, 1, 1]
    int result;
    int zero = 0;
    //literal 0 as src2 also tested - same sign-extension bug
    asm volatile("v_dot4_i32_i8 %0, %1, %2, %3"
                 : "=v"(result)
                 : "v"(q), "v"(k), "v"(zero));
    out[threadIdx.x] = result;
}
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.15
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 7 9800X3D 8-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 9800X3D 8-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5271
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            8
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    31908628(0x1e6e314) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31908628(0x1e6e314) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31908628(0x1e6e314) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    31908628(0x1e6e314) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1101
  Uuid:                    GPU-e10f2e38e35f3587
  Marketing Name:          AMD Radeon RX 7800 XT
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      65536(0x10000) KB
  Chip ID:                 29822(0x747e)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2254
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            60
  SIMDs per CU:            2
  Shader Engines:          3
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 632
  SDMA engine uCode::      29
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1101
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*******
Agent 3
*******
  Name:                    gfx1036
  Uuid:                    GPU-XX
  Marketing Name:          AMD Ryzen 7 9800X3D 8-Core Processor
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    2
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      256(0x100) KB
  Chip ID:                 5056(0x13c0)
  ASIC Revision:           1(0x1)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2200
  BDFID:                   4096
  Internal Node ID:        2
  Compute Unit:            2
  SIMDs per CU:            2
  Shader Engines:          1
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 26
  SDMA engine uCode::      9
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    15954312(0xf37188) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15954312(0xf37188) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1036
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*** Done ***

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — Jonathan03ant (2026-05-03T07:15:34Z)

Hi @VX1D 
I've been attempting to reproduce this issue but cannot reproduce the bug on my system. My setup is 7900 XT (gfx1101) GPU, which is the same as your agent. 

I used your exact test code from the issue 
```cpp
extern "C"
__global__ void test_dot4(int* out) {
    int q = (1) | (0xFF << 8) | (1 << 16) | (0xFF << 24);  // [1, -1, 1, -1]
    int k = (1) | (1 << 8) | (1 << 16) | (1 << 24);        // [1, 1, 1, 1]
    int result;
    int zero = 0;
    //literal 0 as src2 also tested - same sign-extension bug
    asm volatile("v_dot4_i32_i8 %0, %1, %2, %3"
                 : "=v"(result)
                 : "v"(q), "v"(k), "v"(zero));
    out[threadIdx.x] = result;
}
```
However, I consistently get 0 (correct signed behavior) instead of 512. I did verify the following though
1. The assembler does accept `v_dot4_i32_i8` as an alias
2.  When testing the encodings directly, `v_dot4_i32_iu8` with and without neg_lo:[1,1,0] produce different byte encodings
  (0x7c vs 0x1c)
3. Values are correctly passed to the GPU (verified with debug output), and I tested this with multiple optimization levels. 

Can you still reproduce the bug with ROCm 7.2.1 or later versions? What was your exact compilation command? Not sure if there are any specific compiler flags or env variables you used? 

Please let me know.

---

### 评论 #2 — Jonathan03ant (2026-05-11T15:21:12Z)

@VX1D Let me know if you have an update. 

Thanks.

---

### 评论 #3 — VX1D (2026-05-11T15:50:50Z)

Still reproduces on my end. Gfx1101, ROCm 7.2.1, Torch 2.9.1+rocm7.2.1 (hip 7.2.53211). **7800XT** (Navi31 vs Navi32 difference?). If there are any dumps or logs that you'd need, please mention me and I'll provide. 
RE:2) Yeah those match what I see too - the bit that confuses me is which one my assembler ends up emitting for the `v_dot4_i32_i8` alias, because on my build the disasm clearly shows 0x1c (no neg_lo) and the result is 512.
No extra flags. Only --offload-arch=gfx1101 passed to hiprtc:

```
  q = [1, -1, 1, -1], k = [1, 1, 1, 1]
  Result:           512
  Expected signed:  0
```
# ISA (no neg_lo modifier)
```
A. Inline asm v_dot4_i32_i8
  Result: 512
  ISA:    v_dot4_i32_iu8 v1, v1, v2, v3                  // CC164001 1C0E0501

  B. Inline asm v_dot4_i32_iu8 ... neg_lo:[1,1,0] (explicit signed form)
  Result: 0
  ISA:    v_dot4_i32_iu8 v1, v1, v2, v3 neg_lo:[1,1,0]   // CC164001 7C0E0501
```
# Exact ver and misc.
``` 
AMD clang 22.0.0git (roc-7.2.1, f58b06dce1f9c15707c5f808fd002e18c2accf7e)
  hipcc 7.2.53211-e1a6bc5663
  hip-runtime-amd 7.2.53211.70201
  amdgpu-core 1:7.2.70201-2303469.24.04
  GPU: RX 7800 XT (gfx1101)
``` 
You can look at the repo with the exact scripts that I ran right now and my .hsaco dumps https://github.com/VX1D/rocm-issue-6126

---

### 评论 #4 — VX1D (2026-05-11T16:04:21Z)

https://github.com/llvm/llvm-project/pull/118997 
```
 // On GFX11, v_dot4_i32_i8 is a valid SP3 alias for v_dot4_i32_iu8.
  // However, we intentionally leave it unimplemented because on other
  // processors v_dot4_i32_i8 denotes an instruction of a different
  // behaviour, which is considered potentially dangerous.
  v_dot4_i32_i8 v0, v1, v2, v3
  // GFX11: :[[@LINE-1]]:{{[0-9]+}}: error: instruction not supported on this GPU
```

```
 v_dot4_i32_i8 v5, v1, v2, s3
  // GFX11: v_dot4_i32_iu8 v5, v1, v2, s3 ; encoding: [...,0x18]
```

---

### 评论 #5 — Jonathan03ant (2026-05-13T00:52:51Z)

@VX1D  Thanks again. Can confirm the bug exists in the LLVM assembler. The `v_dot4_i32_i8` alias does not set the `neg_lo` modifier bits:

  ```bash
  # Wrong encoding (missing neg_lo bits):
  $ echo 'v_dot4_i32_i8 v0, v1, v2, v3' | llvm-mc -arch=amdgcn -mcpu=gfx1101 -show-encoding
  v_dot4_i32_iu8 v0, v1, v2, v3  ; encoding: [0x00,0x40,0x16,0xcc,0x01,0x05,0x0e,0x1c]

  # Correct encoding (with neg_lo):
  $ echo 'v_dot4_i32_iu8 v0, v1, v2, v3 neg_lo:[1,1,0]' | llvm-mc -arch=amdgcn -mcpu=gfx1101 -show-encoding
  v_dot4_i32_iu8 v0, v1, v2, v3 neg_lo:[1,1,0]  ; encoding: [0x00,0x40,0x16,0xcc,0x01,0x05,0x0e,0x7c]
```
The alias at VOP3PInstructions.td:2594 performs a simple mnemonic substitution without setting the required modifier bits.
I'm preparing a fix and will submit a PR. 

Thanks again. 

---
