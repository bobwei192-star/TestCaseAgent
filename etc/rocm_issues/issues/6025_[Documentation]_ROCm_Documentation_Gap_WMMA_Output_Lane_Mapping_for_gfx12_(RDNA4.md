# [Documentation]:  ROCm Documentation Gap: WMMA Output Lane Mapping for gfx12 (RDNA4)

> **Issue #6025**
> **状态**: closed
> **创建时间**: 2026-03-08T15:15:36Z
> **更新时间**: 2026-03-30T09:00:51Z
> **关闭时间**: 2026-03-30T09:00:51Z
> **作者**: JohnTDI-cpu
> **标签**: Documentation, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6025

## 标签

- **Documentation** (颜色: #5319e7)
- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Description of errors

# ROCm Documentation Gap: WMMA Output Lane Mapping for gfx12 (RDNA4)

## Summary

The RDNA4 ISA reference and GPUOpen guides document the `v_wmma_f32_16x16x16_f16` instruction encoding and HIP intrinsic signatures, but do not specify the **output lane-to-element mapping** — i.e., which matrix element each lane's accumulator register corresponds to.

This is critical information for anyone writing HIP WMMA kernels directly (outside of rocBLAS/CK). Without it, developers have to reverse-engineer the mapping empirically or dig through CK source code.

## The Missing Information

On gfx12 (Wave32), `v_wmma_f32_16x16x16_f16` uses a **column-distributed fragment layout**:

```
Lane i (0..31) holds:
  Column:  i % 16
  Rows:    (i / 16) * 8  ..  (i / 16) * 8 + 7
  acc[j] = element at row (i/16)*8 + j, column i%16
```

Or as a formula:

```
VGPR[lane][j] = matrix[(lane / 16) * 8 + j][lane % 16]
```

The fast-varying dimension across lanes is the **column index** (N), not the row index (M). This means `lane % 16` selects the column, not the row.

## Why This Matters

The natural assumption for many developers is `lane % 16 = row`, which produces **silently transposed** 16x16 output tiles. The kernel compiles and runs without errors — the output is just wrong in a way that's difficult to diagnose without knowing the correct mapping.

We hit this exact issue building a fused MXFP4 WMMA GEMM kernel on Radeon AI PRO R9700 (gfx1201). It took systematic debugging (identity matrix tests, single-tile isolation, lane-by-lane inspection) to identify the root cause.

## Where This Should Be Documented

The mapping is already present in CK source code (`wmma_gemm.hpp`, lines 31-80) as an ASCII diagram, but:

1. **RDNA4 ISA Reference** — documents instruction encoding but not output lane mapping
2. **GPUOpen "Using Matrix Cores on RDNA4" guide** — shows intrinsic signatures and fragment descriptions, but does not specify which dimension lanes index
3. **No standalone reference** exists that says "for FP16 WMMA on gfx12, lanes index columns"

Adding a lane mapping table or diagram to the GPUOpen guide (similar to what CK has internally) would prevent this issue for every future WMMA kernel developer on RDNA4.

## Additional Observations

The same column-distributed layout appears to apply to all WMMA data types on gfx12 (verified for FP16 and INT4), which is consistent with MFMA on CDNA where `lane % 16` also selects the column. This is a shared architectural convention that would be worth documenting explicitly.

## Verification

We verified the mapping on:
- **Hardware**: AMD Radeon AI PRO R9700 (gfx1201, RDNA4, 32GB)
- **ROCm**: 7.1.0
- **Compiler**: hipcc (clang-19)
- **Tests**: identity matrices, small known matrices, asymmetric matrices (for INT4), and large matrices up to 17408x5120

Full writeup with derivation, correct store patterns, and verification methodology: (https://github.com/JohnTDI-cpu/rdna4-wmma-guide)

## Environment

- ROCm version: 7.1.0
- GPU: gfx1201 (Radeon AI PRO R9700)
- OS: Ubuntu (ROCm default)
- Component: Documentation (ISA Reference / GPUOpen)

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (5 条)

### 评论 #1 — amd-nicknick (2026-03-18T05:42:13Z)

Hi @JohnTDI-cpu, I reviewed the documentation, the layout and difference between RDNA3 and RDNA4 is documented in https://gpuopen.com/learn/using_matrix_core_amd_rdna4/
Have I missed anything or is the matrix layout graph incorrect / misleading?

---

### 评论 #2 — JohnTDI-cpu (2026-03-18T08:38:27Z)

I've looked carefully at the diagrams and I appreciate the visual detail, but I think there are two concrete gaps that still make this harder than it needs to be.

**1. Why the visual isn't enough — The "Mental Model" Trap**

Developer expectation (CUDA/standard):
```
matrix[row][col], where row = lane % 16  ← what most developers assume
```
RDNA4 reality (verified on gfx1201):
```
matrix[row][col], where col = lane % 16  ← actual hardware behavior
```
When a developer looks at the GPUOpen diagram, they see a grid. Without a legend or a formula, their brain defaults to the mapping they use 90% of the time. Since WMMA is a black-box instruction, there is no compiler warning — just a transposed result that passes all unit tests except for actual value verification.

Adding `Column = LaneID % 16` directly to the guide would turn a pretty picture into a technical specification.

**2. The CK discrepancy**

Composable Kernel — AMD's own official library — includes detailed ASCII lane mapping tables in `wmma_gemm.hpp` (lines 31–80) that are far more explicit than anything in the GPUOpen guide or ISA reference. The fact that AMD's own engineers felt the need to write those tables internally is strong evidence that the public documentation is insufficient for low-level kernel development.

I'm not disputing the diagrams are wrong — they're correct. The ask is simple: one explicit formula stating the lane-to-column mapping, similar to what CK already has internally.

Full writeup: https://github.com/JohnTDI-cpu/rdna4-wmma-guide

---

### 评论 #3 — amd-nicknick (2026-03-25T08:18:35Z)

I think I understood you now, in the sample code's store line:
```
c[16 * ( ele + laneGroup * WMMA_DATA_WIDTH ) + laneWrapped] = c_frag[ele];
```
Where `row = ele + (threadIdx.x / 16) * 8`, `col = threadIdx.x % 16`
`c_frag[0..7]` therefore corresponds to `C[(threadIdx.x / 16) * 8 + 0..7][threadIdx.x % 16]`
This decomposition matches the CK document.

You might be mixing up where the CUDA comes into play here though. There isn't really a documented CUDA equivalent to ISA intrinsics at this level. 
The equivalent would be SASS, and there exist some instructions using a column-major format there as well. Just that PTX/CUDA will expect you to use `wmma + load/store/sync`, which maps the output to expected row-major format internally, even if the underlying instruction operates otherwise.

If you're looking for higher level APIs equivalent on ROCm which does this for you, you should use hipBLAS / hipBLASLt / CK instead.

Nonetheless, I do agree the document could be more specific to point this out. I'll talk to the document team and update it to highlight this common pitfall.

Thanks for bringing this to our attention, I really appreciate your feedback!

---

### 评论 #4 — JohnTDI-cpu (2026-03-26T13:55:07Z)

Regarding the suggestion to use higher-level APIs like hipBLASLt or Composable Kernel:

This is exactly the gap that motivated me to develop custom HIP kernels. In my benchmarks on RDNA4 (gfx1201), hipBLASLt still trails Vulkan (RADV/AMDVLK) by a significant margin in LLM inference decode throughput — in the range of 20–40% depending on model and quantization. Even on ROCm 7.1+, the Vulkan backend delivers better token generation speed with lower power draw on consumer hardware.

Until the higher-level HIP libraries close this gap on RDNA4, writing RDNA4-optimized kernels directly against WMMA intrinsics is the most viable path I've found to match or exceed Vulkan-level performance from the HIP side. I've spent over two weeks iterating with AI-assisted optimization and empirical testing to work out the lane-to-element mapping for WMMA output on gfx12 — so any additional documentation or examples in this area would be hugely appreciated.

Good point on the SASS vs. PTX distinction — I'll correct that in my writeup.

Really appreciate the follow-up and internal review!

---

### 评论 #5 — amd-nicknick (2026-03-30T09:00:51Z)

Closing this issue as all questions answered & under internal review. Thanks!

---
