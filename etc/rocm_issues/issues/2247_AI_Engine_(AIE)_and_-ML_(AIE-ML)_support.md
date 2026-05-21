# AI Engine (AIE) and -ML (AIE-ML) support

> **Issue #2247**
> **状态**: closed
> **创建时间**: 2023-06-15T21:03:16Z
> **更新时间**: 2024-05-13T18:16:30Z
> **关闭时间**: 2024-05-13T18:16:29Z
> **作者**: EwoutH
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2247

## 描述

I would love to see ROCm platform's support for AMD's [AI Engine](https://www.xilinx.com/products/technology/ai-engine.html), part of the Versal ACAP architecture. Specifically, the two variants AIE and AIE-ML, found in chips like the AMD Ryzen 7x40HS and 7x40U series.

If ROCm already supports the AI Engine (both AIE and AIE-ML), then this is a request for documentation on it. If it doesn't, consider this a feature request to include such support.

---

## 评论 (4 条)

### 评论 #1 — saadrahim (2023-06-15T21:09:46Z)

ROCm does not support the AMD AI Engine. 

Is there a particular use case that you are making a feature request for? Please elaborate if possible.

---

### 评论 #2 — chaudhariatul (2023-07-11T18:52:21Z)

Unified support with Raedon GPU, Xilinx FPGA available with AMD Ryzen 7x40HS and 7x40U series will improve the edge device solutions. This will be great value add. 

---

### 评论 #3 — keryell (2023-07-14T21:57:38Z)

I have been waiting for years to have a laptop myself with an AMD Ryzen 9 7940HS. :-)
But how do you imagine AIE support in ROCm? Something like HIP?
Each work-item in a GPU can access its global memory while on AIE you cannot without programming some DMA to transfer explicitly some memory chunks to get the performance.
So either the programming style is different from HIP (but can still be part of ROCm at large) or you need a serious auto-magic compiler.
But if you have some good ideas, you are welcome. :-)
Otherwise there is a research project making progress and you can look at the latest presentation of https://xilinx.github.io/mlir-aie/Presentations.html

---

### 评论 #4 — saadrahim (2023-08-02T23:14:34Z)

Please see https://ryzenai.docs.amd.com/en/latest/


---
