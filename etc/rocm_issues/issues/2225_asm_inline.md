# asm inline

> **Issue #2225**
> **状态**: closed
> **创建时间**: 2023-06-07T14:15:53Z
> **更新时间**: 2024-07-16T19:02:06Z
> **关闭时间**: 2024-07-16T19:02:06Z
> **作者**: qiji2023
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2225

## 描述

https://github.com/ROCm-Developer-Tools/HIP/tree/master/samples/2_Cookbook/10_inline_asm
The example is so easy！
For v_mad_u64_u32 instruction, how should i use it?

---

## 评论 (3 条)

### 评论 #1 — preda (2023-06-19T19:14:26Z)

IMO the best way is to state the arithmetic operation in a high-level language such as OpenCL (C) or C++, and rely on the compiler to generate the v_mad_u64_u32 where appropirate. You can look into the generated ISA, and if it's not what you expected, try to understand why. Use a simple kernel to try to understand the behavior of the compiler. In the unlikely case that you consider that the compiler/optimizer is not doing its job, you can report an issue.

If you write the ASM by hand, it's difficult, error-prone, and often slower than what the compiler was doing in the first place.


---

### 评论 #2 — ppanchad-amd (2024-05-13T18:02:59Z)

@qiji2023 Do you still need assistance with this ticket? If not, please close the ticket. Thanks!

---

### 评论 #3 — harkgill-amd (2024-07-16T19:02:06Z)

Closing this ticket. If you still need help with inline assembly examples, please re-open this issue or file a new ticket. Thanks!

---
