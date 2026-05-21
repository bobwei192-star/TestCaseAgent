# [Documentation]: FNUZ format specification inconsistent with CDNA3 ISA

> **Issue #4756**
> **状态**: closed
> **创建时间**: 2025-05-20T17:21:24Z
> **更新时间**: 2025-07-02T15:37:58Z
> **关闭时间**: 2025-07-02T15:37:58Z
> **作者**: ldrumm
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4756

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

There's an inconsistency between the ROCm documentation and the CDNA3 ISA document regarding FP8 types.

The [ROCm docs on low precision](https://rocm.docs.amd.com/en/docs-6.3.3/reference/precision-support.html) give a good overview on the various kinds of low precision types available in the wild, and the handy table there shows that CDNA only supports the `FP8-FNUZ` format.

It doesn't link to any formal specification of this format, only handwaving that the extra exponent bits become available and suggesting its defined in a separate [academic paper](https://arxiv.org/pdf/2206.02915). Regrettably, that paper is not *at all* precise in its definition of s1e4m3 and various encodings required there and seems to assume an understanding of the underlying binary encoding.

Looking at the HIP headers makes things clearer. The [FNUZ format uses an exponent BIAS of 8](https://github.com/ROCm/clr/blob/cda4b7db1cf27e6214e34b81e4867aea021226be/hipamd/include/hip/amd_detail/amd_hip_fp8.h#L242) while the OCP format (unsupported by e.g. MI300X in hardware) uses an exponent bias of 7.

However, the [MI300x ISA document](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/amd-instinct-mi300-cdna3-instruction-set-architecture.pdf) in table 30 (subsection 7.2. BF8 and FP8 Formats and Conversions) lists an exponent BIAS of 8, but a max normal value of 448; implies support for infinities (only sign bit set); implies support for NaNs (also only sign bit set); and lists subnormal values consistent with an exponent bias of 7 as in the FP8-OCP format.

![Image](https://github.com/user-attachments/assets/e65647e7-b745-4555-a7c3-eda816d7c3b7)

While I think the ROCm docs do a good job of providing an overview of the mess our industry has created, it'd be great if these inconsistencies between ROCm and ISA doc were corrected (TBH I think the ISA doc is incorrect but have no way of filing a bug against it). It'd also be good if it were made absolutely clear what the actual formula for computing the value of a FNUZ bit pattern is, or linking to a document that makes this clear as is already the case of the unsupported (in AMD hardware) OCP format.

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2025-05-21T18:17:47Z)

Hi @ldrumm. Internal ticket has been created to fix the docs. Thanks!


---

### 评论 #2 — ppanchad-amd (2025-07-02T15:37:58Z)

The public spec is updated, available on [www.amd.com/en/support/tech-docs](http://www.amd.com/en/support/tech-docs)

https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/amd-instinct-mi300-cdna3-instruction-set-architecture.pdf

---
