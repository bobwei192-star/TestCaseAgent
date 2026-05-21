# [Bug]: torch.mm produces data-dependent NaN when input exceeds ~500K rows on gfx1201 (RDNA 4)

> **Issue #6116**
> **状态**: open
> **创建时间**: 2026-04-03T13:35:53Z
> **更新时间**: 2026-04-13T13:00:58Z
> **作者**: jsurquhart614
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6116

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- adityas-amd

## 描述

## Description

`torch.mm` and `F.linear` produce NaN values in a data-dependent pattern when the input tensor exceeds approximately 500,000 rows on RDNA 4 (gfx1201). The same data and weights compute correctly when processed in 100K-row chunks, or when run on CPU. This is not a numerical precision issue — specific data patterns trigger it while random data at the same scale does not.

## Environment

- **GPU**: AMD Radeon RX 9070 XT (16GB)
- **Architecture**: RDNA 4, gfx1201
- **ROCm**: 7.2
- **PyTorch**: 2.9.1+rocm7.2.0 (custom build with gfx1201 arch support)
- **OS**: Ubuntu 24.04 via WSL2 on Windows 11
- **Driver**: WSL2 GPU-PV (DXGI bridge)

## Steps to Reproduce

The bug is data-dependent — it triggers with real model output (sparse convolution features) but not with random data. A minimal tensor reproducer (`.pt` file) can be provided on request.

**How the bug manifests in practice:**

```python
import torch

device = torch.device("cuda")

# x = real sparse conv output, shape [~600K-1.5M, 512], dtype float32
# w = learned weight matrix, shape [512, 512], dtype float32
# (loaded from saved .pt file — random data does NOT reliably trigger this)

# Full matmul — produces NaN
result_full = torch.mm(x, w.T)
print(f"Full:    NaN count = {torch.isnan(result_full).sum().item()}")
# Actual: thousands of NaN, concentrated in rows > ~500K

# Same data, chunked to 100K rows — correct
chunk_size = 100_000
results = []
for i in range(0, rows, chunk_size):
    chunk = torch.mm(x[i:i+chunk_size], w.T)
    results.append(chunk)
result_chunked = torch.cat(results, dim=0)
print(f"Chunked: NaN count = {torch.isnan(result_chunked).sum().item()}")
# Actual: 0

# CPU — correct
result_cpu = torch.mm(x.cpu(), w.T.cpu())
print(f"CPU:     NaN count = {torch.isnan(result_cpu).sum().item()}")
# Actual: 0
```

**To generate triggering data:** Run TRELLIS.2 (microsoft/TRELLIS.2) texture decoder at 512+ resolution. The sparse convolution output features and the SparseLinear output layer both produce inputs large enough to trigger this. I can provide a saved tensor pair (`x.pt`, `w.pt`) that reliably reproduces the NaN on request.

## Observed Behavior

- `torch.mm` with >500K rows: **NaN in output** (count varies by data pattern)
- Same data chunked to 100K rows: **correct output, zero NaN**
- Same data on CPU: **correct output, zero NaN**
- Random data at same scale: **often correct** (the bug is data-dependent, not shape-dependent)

## Impact

This affects any large matmul on gfx1201 — not just specific models. Discovered in two independent contexts:

1. **Sparse convolution output** (FlexGEMM): ~600K rows in TRELLIS.2 shape decoder
2. **nn.Linear / F.linear**: 1.5M-row output layer in TRELLIS.2 texture decoder

Both produce NaN with full tensors, both compute correctly when chunked.

## Workaround

Chunk all matmuls with >500K rows to 100K-row blocks:

```python
def chunked_mm(a, b, chunk_size=100_000):
    if a.shape[0] <= chunk_size:
        return torch.mm(a, b)
    results = []
    for i in range(0, a.shape[0], chunk_size):
        results.append(torch.mm(a[i:i+chunk_size], b))
    return torch.cat(results, dim=0)
```

## Additional Context

- The threshold appears to be around 500K rows but may vary by tensor shape and data distribution
- Not reproducible with purely random data in all cases — the triggering pattern involves regions of near-zero values (as produced by sparse convolution with spatial locality)
- Unknown if this affects other gfx12 variants (gfx1200, gfx1201 confirmed)
- Unknown if this is a MIOpen issue, hipBLAS issue, or lower-level HW issue

---

## 评论 (1 条)

### 评论 #1 — adityas-amd (2026-04-13T13:00:46Z)

Hi @jsurquhart614 Thanks for the detailed report to. I believe here, Large M-dimension (>~500K rows) causing the library to select a different tiling/kernel strategy.
For a definitive root cause analysis, it would really help to get the necessary saved tensors and a small reproducer script form you?

---
