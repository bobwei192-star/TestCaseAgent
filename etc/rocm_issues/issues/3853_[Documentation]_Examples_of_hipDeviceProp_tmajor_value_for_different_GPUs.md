# [Documentation]: Examples of hipDeviceProp_t::major value for different GPUs

> **Issue #3853**
> **状态**: closed
> **创建时间**: 2024-10-02T07:33:11Z
> **更新时间**: 2025-02-14T14:52:01Z
> **关闭时间**: 2025-02-14T14:52:01Z
> **作者**: nazar-pc
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/3853

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

I was trying to find what values of `hipDeviceProp_t::major` correspond to what GPU and wasn't able to find it.
There are also seemingly no official CLI tools that print it, the only option is to own the GPU and write a piece of code myself.

I also tried to find in the source code and didn't succeed so far.

Would be great to have it described somewhere.

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-10-02T14:49:46Z)

Hi @nazar-pc, `hipDeviceProp_t::major` and `hipDeviceProp_t::minor` reference the GPUs architecture. The [system requirements](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus) page has a table which you can use to decode which architecture a GPU corresponds with. For example

An AMD Radeon RX 7900 XTX which is `gfx1100` will have a major value of 11 and a minor value of 0.
An AMD Instinct MI100 which is `gfx908` will have a major value of 9 and a minor value of 0.

---

### 评论 #2 — nazar-pc (2024-10-02T14:51:24Z)

Interesting, that makes a lot of sense to me, but wasn't obvious at all. Would be great to improve documentation in that respect.

Thanks for quick response!

---

### 评论 #3 — harkgill-amd (2024-10-02T15:46:41Z)

No problem! I agree that the documentation could use some additions in regards to compute capability. I will reach out to the docs team and confirm how we want to go about adding it in. 

---

### 评论 #4 — harkgill-amd (2025-02-14T14:47:28Z)

https://github.com/ROCm/ROCm/pull/4350 and https://github.com/ROCm/HIP/pull/3721 have been merged. Both changes provide more context as to what the values represent and the expected output as well. 

---
