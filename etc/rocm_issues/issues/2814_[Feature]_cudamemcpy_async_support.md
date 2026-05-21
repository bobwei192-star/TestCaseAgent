# [Feature]: cuda::memcpy_async support

> **Issue #2814**
> **状态**: closed
> **创建时间**: 2024-01-17T12:49:21Z
> **更新时间**: 2024-05-26T07:12:58Z
> **关闭时间**: 2024-05-26T07:12:58Z
> **作者**: sorasoras
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2814

## 描述

### Suggestion Description

With cuda::memcpy_async, the thread block no longer stages data through registers, freeing the thread block from the task of moving data and freeing registers to be used by computations.

Do ROCm has something similar  to cuda::memcpy_async that could do this?

![journey-through-memory-hierarchy-1 1](https://github.com/ROCm/ROCm/assets/6722084/a434ba7b-4548-46d9-bf09-15fcafd791e6)


### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-05-26T02:58:59Z)

@sorasoras There’s no HW support.  Would you want the API implemented anyway even though it would be synchronous.  Please advise. Thanks!

---

### 评论 #2 — sorasoras (2024-05-26T07:12:58Z)

> @sorasoras There’s no HW support. Would you want the API implemented anyway even though it would be synchronous. Please advise. Thanks!
if this is the case, it's probably not worth to implement it. API implemented would only help compatible with cuda code. 
Thanks for answer my question.

---
