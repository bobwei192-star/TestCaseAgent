# Navi 5000 Support

> **Issue #2206**
> **状态**: closed
> **创建时间**: 2023-06-01T12:55:32Z
> **更新时间**: 2024-05-13T17:47:55Z
> **关闭时间**: 2024-05-13T17:47:55Z
> **作者**: daniandtheweb
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2206

## 描述

It's been quite a lot of time since the first generation of RDNA cards have been released and still it seems to be the only cards generation without official ROCm support. Is there any plan to support this generation of cards? 

---

## 评论 (5 条)

### 评论 #1 — ganesh-rao (2023-06-06T08:22:57Z)

I own an RX 5500 XT, and I'm very disappointed with the lack of support for this card. IMO, AMD's decision so far doesn't inspire any confidence in staying with their products in the future when the equivalent Nvidia GPUs appear to be supported and working flawlessly with most ML libraries.

---

### 评论 #2 — Horus2025 (2023-06-09T04:12:10Z)

I own an RX 7600 XT, and I;m very disappointed with the support of AMD, How much?

---

### 评论 #3 — DifferentialityDevelopment (2023-06-30T14:08:50Z)

I'm particularly interested in 7600 XT due to AI Accelerators and I cannot find any benchmarks online, no review does any benchmarks on those.
The 7600 reportedly comes with 60 AI Accelerators, I'd love to know how the card performs with ROCm running inference on a LLM, or better yet how it compares to tensor cores.

---

### 评论 #4 — johnnynunez (2023-06-30T14:11:17Z)

> I'm particularly interested in 7600 XT due to AI Accelerators and I cannot find any benchmarks online, no review does any benchmarks on those. The 7600 reportedly comes with 60 AI Accelerators, I'd love to know how the card performs with ROCm running inference on a LLM, or better yet how it compares to tensor cores.

It's not ai accelerators, they are SIMD units... it's totally different to sistolic arrays(matrix cores from cdna), so no expect a big improvement performace

---

### 评论 #5 — ppanchad-amd (2024-05-13T17:47:55Z)

@daniandtheweb Please refer to following link for supported GPUs in the latest ROCm 6.1.1 (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)

---
