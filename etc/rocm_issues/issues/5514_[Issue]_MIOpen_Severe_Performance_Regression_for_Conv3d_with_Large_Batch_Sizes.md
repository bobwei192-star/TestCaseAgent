# [Issue]: MIOpen: Severe Performance Regression for Conv3d with Large Batch Sizes

> **Issue #5514**
> **状态**: closed
> **创建时间**: 2025-10-14T08:29:14Z
> **更新时间**: 2025-10-23T20:10:55Z
> **关闭时间**: 2025-10-21T14:54:56Z
> **作者**: healy-hub
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5514

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

MIOpen demonstrates a severe, non-linear performance degradation when executing a `torch.nn.Conv3d` operation with `bfloat16` or `float16` precision as the batch size increases dramatically.

When processing a `Conv3d` layer with a typical, small batch size, MIOpen delivers excellent performance. However, when the same layer is subjected to a very large batch size, its performance collapses, resulting in extremely long execution times (over 4 seconds per operation). The per-unit efficiency becomes over **1300 times worse** than in the small-batch case. **For context, on NVIDIA GPUs, the per-patch efficiency remains nearly constant regardless of the input batch size, indicating this is a MIOpen-specific issue rather than a general algorithmic limitation.**

This "performance cliff" indicates a fundamental issue in MIOpen's kernel selection or execution strategy for large-tensor scenarios, forcing it into a highly unoptimized fallback path.

To identify the bottleneck, the large-batch operation was profiled using `rocprofv3`. The analysis of the profiler trace data clearly shows that the overwhelming majority of the execution time is consumed by a single matrix multiplication (GEMM) kernel.

*   **Dominant Kernel:**
    `"Cijk_Ailk_Bljk_BBS_BH_MT128x32x16_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL0_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS0_ELFLR0_EMLL0_FSSC10_FL0_GLVWA1_GLVWB1_GRCGA1_GRCGB1_GRPM1_GRVW1_GSU1_GSUASB_GLS0_ISA000_IU1_K1_KLS_LBSPPA0_LBSPPB0_LPA0_LPB0_LDL1_LRVW1_LWPMn1_LDW0_FMA_MIAV0_MDA2_MO40_MMFSC_MKFGSU256_NTA_..._WGM8"`

*   **Performance Impact:** This single kernel is responsible for approximately **96% of the total GPU computation time**.


### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

13th Gen Intel(R) Core(TM) i9-13900K

### GPU

Radeon RX 7900 XTX

### ROCm Version

ROCm 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

### Minimal Reproduction Code

The following self-contained script definitively reproduces the issue. It first tests `nn.Conv3d` with a large batch size (`56700`) identical to the one observed in vLLM's `profile_run`, and then with a normal, small batch size (`1`).

```python
import torch
import torch.nn as nn
import time

def run_reproduction():
    device = "cuda"
    dtype = torch.bfloat16
    
    print("--- Environment ---")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Data type: {dtype}")
    print("-" * 20)
    
    # --- Conv3d Parameters ---
    in_channels = 3
    out_channels = 1152
    kernel_size = (2, 14, 14)

    # ======================================================================
    # SCENE 1: Replicating vLLM Profile-Run (Huge Batch)
    # ======================================================================
    print("\n" + "#"*50)
    print("### SCENE 1: Testing with Huge Batch (from vLLM logs) ###")
    print("#"*50)

    # This model instance is ONLY for the huge batch test
    model_for_huge = nn.Conv3d(
        in_channels, out_channels, kernel_size, stride=kernel_size, bias=False
    ).to(device, dtype)

    batch_size_vllm = 56700
    c, t, h, w = 3, 2, 14, 14
    
    try:
        input_vllm = torch.randn(
            batch_size_vllm, c, t, h, w, device=device, dtype=dtype
        )
        print(f"\nTesting with input shape: {input_vllm.shape}")

        print("Warming up... (This may be very slow or crash)")
        with torch.no_grad():
            _ = model_for_huge(input_vllm)
        torch.cuda.synchronize()

        print("Benchmarking...")
        num_runs = 5
        start_time = time.time()
        with torch.no_grad():
            for _ in range(num_runs):
                _ = model_for_huge(input_vllm)
        torch.cuda.synchronize()
        end_time = time.time()
        
        latency_vllm = (end_time - start_time) / num_runs * 1000
        efficiency_vllm = (latency_vllm / batch_size_vllm) * 1000
        
        print(f"--> Huge Batch Latency: {latency_vllm:.2f} ms")
        print(f"    Per-Patch Efficiency: {efficiency_vllm:.4f} µs/patch")

    except RuntimeError as e:
        print(f"\n!!! CRASH REPRODUCED !!!")
        print(f"ERROR: {e}")
        print("This confirms the `miopenStatusUnknownError` seen in vLLM.")
        latency_vllm, efficiency_vllm = float('inf'), float('inf')
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        latency_vllm, efficiency_vllm = float('inf'), float('inf')

    # ======================================================================
    # SCENE 2: Simulating Real-World Inference (Small Batch)
    # ======================================================================
    print("\n" + "#"*50)
    print("### SCENE 2: Testing with Small Batch (Normal Inference) ###")
    print("#"*50)
    
    # We create a NEW model instance for a clean test
    model_for_small = nn.Conv3d(
        in_channels, out_channels, kernel_size, stride=kernel_size, bias=False
    ).to(device, dtype)

    # === FIX WAS HERE: Define kernel dimensions before use ===
    kernel_t, kernel_h, kernel_w = kernel_size

    batch_size_real = 1
    temporal_dim, height, width = 64, 224, 224
    
    input_real = torch.randn(
        batch_size_real, in_channels, temporal_dim, height, width, 
        device=device, dtype=dtype
    )
    print(f"\nTesting with input shape: {input_real.shape}")
    
    print("Warming up...")
    with torch.no_grad():
        for _ in range(10):
            _ = model_for_small(input_real)
    torch.cuda.synchronize()

    print("Benchmarking...")
    num_runs = 100
    start_time = time.time()
    with torch.no_grad():
        for _ in range(num_runs):
            _ = model_for_small(input_real)
    torch.cuda.synchronize()
    end_time = time.time()
    
    latency_real = (end_time - start_time) / num_runs * 1000
    num_patches_real = (temporal_dim//kernel_t) * (height//kernel_h) * (width//kernel_w)
    efficiency_real = (latency_real / num_patches_real) * 1000

    print(f"--> Small Batch Latency: {latency_real:.2f} ms")
    print(f"    Per-Patch Efficiency: {efficiency_real:.4f} µs/patch")
    
    print("\n--- FINAL CONCLUSION ---")
    if efficiency_vllm != float('inf'):
        slowdown_factor = efficiency_vllm / efficiency_real
        print(f"The per-patch efficiency drops by a factor of {slowdown_factor:.2f}x when first called with a large batch.")
        print("This demonstrates a catastrophic performance fallback in MIOpen's kernel selection.")
    else:
        print("The operation crashes with a large batch, indicating a fatal bug in the MIOpen backend.")

if __name__ == "__main__":
    run_reproduction()
```

### Results Observed
```
##################################################
### SCENE 1: Testing with Huge Batch (from vLLM logs) ###
##################################################

Testing with input shape: torch.Size([56700, 3, 2, 14, 14])
Warming up... (This may be very slow or crash)
Benchmarking...
--> Huge Batch Latency: 3965.24 ms
    Per-Patch Efficiency: 69.9336 µs/patch

##################################################
### SCENE 2: Testing with Small Batch (Normal Inference) ###
##################################################

Testing with input shape: torch.Size([1, 3, 64, 224, 224])
Warming up...
Benchmarking...
--> Small Batch Latency: 0.43 ms
    Per-Patch Efficiency: 0.0527 µs/patch

--- FINAL CONCLUSION ---
The per-patch efficiency drops by a factor of 1327.23x when first called with a large batch.
This demonstrates a catastrophic performance fallback in MIOpen's kernel selection.
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

/opt/rocm/bin/rocminfo --support
ROCk module version 6.14.14 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:                    13th Gen Intel(R) Core(TM) i9-13900K
  Uuid:                    CPU-XX
  Marketing Name:          13th Gen Intel(R) Core(TM) i9-13900K
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
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5800
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            32
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65510484(0x3e79c54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65510484(0x3e79c54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65510484(0x3e79c54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65510484(0x3e79c54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1100
  Uuid:                    GPU-2af6f87456aeb5a8
  Marketing Name:          Radeon RX 7900 XTX
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
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29772(0x744c)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2371
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
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
  Packet Processor uCode:: 552
  SDMA engine uCode::      24
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1100
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
*** Done ***

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — huanrwan-amd (2025-10-20T14:01:53Z)

Thanks for posting the question @healy-hub.  We're currently working on adding CK (composable kernels) kernels for supporting Navi card.

---

### 评论 #2 — kingguppy (2025-10-21T14:00:01Z)

@huanrwan-amd does that include support for Strix Halo?

Edit: My question was ignored here, but I got the answer from elsewhere that no, in this case "Navi" doesn't include Strix Halo.

---

### 评论 #3 — healy-hub (2025-10-21T14:15:11Z)

> Thanks for posting the question [@healy-hub](https://github.com/healy-hub). We're currently working on adding CK (composable kernels) kernels for supporting Navi card.

Thank you for the prompt reply and for the information @huanrwan-amd . It's great to hear that Composable Kernel (CK) support for Navi cards is in active development. I'm eagerly looking forward to its release.
I was able to implement the Conv3d operator myself using Triton and a GEMM approach, and the performance was excellent. This confirms that the underlying RDNA hardware is very capable and that the performance bottleneck is indeed in the software layer.
We've noticed that the current MIOpen on RDNA seems to be missing a few other operator implementations as well, such as certain variations of dilated convolution. The upcoming CK support will hopefully address these gaps too.
Thanks again for the update, and we're excited to see these improvements roll out.

---

### 评论 #4 — huanrwan-amd (2025-10-21T14:54:56Z)

@healy-hub Thanks for letting us know your results. Let's wait for the future release and close this issue for now.

---
