# [Feature]: rocBLAS for AMD NPUs??

> **Issue #4431**
> **状态**: open
> **创建时间**: 2025-02-27T05:35:03Z
> **更新时间**: 2025-05-22T10:26:49Z
> **作者**: kmshort
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4431

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

The new AMD Ryzen AI branded CPUs have integrated NPUs.

Will rocBLAS potentially support the AMD NPUs in the future? I could see potential benefit for users with, for example, an AMD Ryzen 9 AI HX370 that want to use data science applications that can leverage accelerated matrix multiplication. I'm thinking of several R statistics packages that could benefit for statistical and model analysis.

---

## 评论 (4 条)

### 评论 #1 — IntegerTec (2025-05-22T06:35:56Z)

hahaha, AMD Ryzen 9 AI HX370?
They slap an 'AI' label on the chip, but forgot the part where it actually works with their own tools. Brilliant.

---

### 评论 #2 — kmshort (2025-05-22T07:18:55Z)

> hahaha, AMD Ryzen 9 AI HX370? They slap an 'AI' label on the chip, but forgot the part where it actually works with their own tools. Brilliant.

Indeed. It's unlikely the NPU will be able to be leveraged for matrix multiplication etc as it's not designed that way. But who knows.

This appears to use the term NPU but I believe only invokes the gpu
https://www.hackster.io/tina/tina-running-non-nn-algorithms-on-an-amd-ryzen-npu-0cc58c

---

### 评论 #3 — IMbackK (2025-05-22T08:39:52Z)

the programming model of those npus and gpus is very different, while some functions from rocblas could be implemented, it dosent really make sense for that the be part of rocblas as it would share exacly no code with the gpu implementations. Doing so would really be cosmetic only.

---

### 评论 #4 — kmshort (2025-05-22T10:26:48Z)

> the programming model of those npus and gpus is very different, while some functions from rocblas could be implemented, it dosent really make sense for that the be part of rocblas as it would share exacly no code with the gpu implementations. Doing so would really be cosmetic only.

Might be, would there be potential in using them together? If npus are to be a permanent part of AMDs future, now is the thing to unify all this stuff.

---
