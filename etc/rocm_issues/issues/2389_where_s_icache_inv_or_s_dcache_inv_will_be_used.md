# where s_icache_inv or s_dcache_inv will be used?

> **Issue #2389**
> **状态**: closed
> **创建时间**: 2023-08-21T09:53:14Z
> **更新时间**: 2024-01-30T19:09:30Z
> **关闭时间**: 2024-01-30T19:09:30Z
> **作者**: clp510
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2389

## 描述

can anyone knows under what circumstance, the RDNA instruction (or CDNA instruction), S_ICACHE_INV or S_DCACHE_INV will be used?

here attach the rdna isa spec :  https://www.amd.com/system/files/TechDocs/rdna-shader-instruction-set-architecture.pdf

---

## 评论 (1 条)

### 评论 #1 — ipanfilo (2024-01-30T19:09:30Z)

The s_icache_inv instruction is used to invalidate the instruction cache, typically when you have self-modifying code or when you are loading new code into memory.
This instruction ensures that the GPU does not continue to use an old, cached version of the instructions, but instead loads the new instructions from memory. 

The s_dcache_inv instruction is used to invalidate the data cache, for instance when you have updated data in global memory and you want to ensure that the GPU does not continue to use an old, cached version of the data.
This instruction is particularly useful when you have multiple threads or cores that are reading and writing to the same memory locations to ensure that all threads or cores see the most recent version of the data.

However, using these instructions frequently can have a negative impact on performance, as they force the GPU to fetch instructions or data from memory rather than using the faster on-chip cache. Therefore, they should be used judiciously.

It's worth noting that these instructions are not new in RDNA or CDNA, you can find them in previous GCN GPU generations as well

---
