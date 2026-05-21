# [Documentation]: Matrix Core Docs Only Cover CDNA2

> **Issue #4523**
> **状态**: closed
> **创建时间**: 2025-03-23T05:29:08Z
> **更新时间**: 2025-03-25T14:40:29Z
> **关闭时间**: 2025-03-25T14:40:29Z
> **作者**: ntenenz
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4523

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Description of errors

Docs should be updated to clarify supported modes of operation on newer microarch.

### Attach any links, screenshots, or additional evidence you think will be helpful.

https://rocm.blogs.amd.com/software-tools-optimization/matrix-cores/README.html

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-03-25T13:31:43Z)

Hi @ntenenz, the [AMD matrix cores](https://rocm.blogs.amd.com/software-tools-optimization/matrix-cores/README.html) blog was published prior to the release of the MI300/CDNA3 and therefore does not include information on it. 

You can find the supported modes of operation and performance capabilities for MI300 on the [AMD Instinct™ MI300 series microarchitecture](https://rocm.docs.amd.com/en/latest/conceptual/gpu-arch/mi300.html) page or in the [MI300 ISA Reference Guide](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/amd-instinct-mi300-cdna3-instruction-set-architecture.pdf) (7.1. Matrix fused-multiply-add (MFMA)). Please let me know if there's any additional information in the blogpost that is not covered by the aforementioned pages.

---

### 评论 #2 — ntenenz (2025-03-25T14:40:15Z)

My apologies. I didn't realize it was a blog post. Those docs are exactly what I was searching for.

---
