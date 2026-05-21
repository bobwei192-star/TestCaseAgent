# [Documentation]: MI250X Peak Flops typo

> **Issue #3547**
> **状态**: closed
> **创建时间**: 2024-08-08T17:42:28Z
> **更新时间**: 2024-08-20T14:24:32Z
> **关闭时间**: 2024-08-20T14:24:32Z
> **作者**: ausellis0
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/3547

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

AMD Instinct™ MI250 microarchitecture page

`Therefore, the theoretical maximum FP64 peak performance per GCD is 45.3 TFLOPS for vector instructions.`
should be
`Therefore, the theoretical maximum FP64 peak performance for both GCDs is 45.3 TFLOPS for vector instructions.`
or
`Therefore, the theoretical maximum FP64 peak performance per GCD is 22.6 TFLOPS for vector instructions.`

### Attach any links, screenshots, or additional evidence you think will be helpful.

https://rocm.docs.amd.com/en/latest/conceptual/gpu-arch/mi250.html


---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-08-09T17:35:56Z)

Hi @ausellis0, thank you for reporting this issue. I'll verify this and get back to you.

---

### 评论 #2 — harkgill-amd (2024-08-12T18:10:52Z)

@ausellis0, the documentation has been updated to the following:

`Therefore, the theoretical maximum FP64 peak performance per GCD is 22.6 TFLOPS for vector instructions. This equates to 45.3 TFLOPS for vector instructions for both GCDs together.`

Please close out the ticket if everything looks good at [AMD Instinct™ MI250 microarchitecture](https://rocm.docs.amd.com/en/latest/conceptual/gpu-arch/mi250.html).

---
