# vopd v_dual_and_b32 first argument problem

> **Issue #2230**
> **状态**: closed
> **创建时间**: 2023-06-08T21:26:10Z
> **更新时间**: 2023-06-08T21:43:28Z
> **关闭时间**: 2023-06-08T21:43:28Z
> **作者**: halfminer
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2230

## 描述

v_dual_add_f32 v17, v22, v26 :: v_dual_and_b32 v16, v21, v25 - ok
v_dual_and_b32 v17, v22, v26 :: v_dual_and_b32 v16, v21, v25 - error: invalid instruction

---

## 评论 (2 条)

### 评论 #1 — b-sumner (2023-06-08T21:34:55Z)

Unfortunately the set of X opcodes is not the same as the set of Y opcodes.  The assembler is correct to complain.

---

### 评论 #2 — halfminer (2023-06-08T21:43:28Z)

> Unfortunately the set of X opcodes is not the same as the set of Y opcodes. The assembler is correct to complain.

Oh, i see. Thank you.

---
