# Does the CU MASK really work

> **Issue #2138**
> **状态**: closed
> **创建时间**: 2023-05-14T15:06:12Z
> **更新时间**: 2024-08-01T15:12:41Z
> **关闭时间**: 2024-08-01T15:12:41Z
> **作者**: gofreelee
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2138

## 描述

Hi, I am learning CU_MASK mechanism, my experiment scenario is like this:
I used two separate sets of masks

unsigned int cuMaskAll[2] = {0xFFFFFFFF, 0xFFFFFFF0};
unsigned int cuMaskBE[2] = {0x11111111, 0x0000000};
They are used to create two streams, which are used to carry out a bert model inferrence
There is little difference in the infer latency between the two of them. cuMaskBE is supposed to enable only 8 CUS. Why wouldn't it ？
Thank you in advance.


---

## 评论 (5 条)

### 评论 #1 — langyuxf (2023-05-15T00:45:40Z)

Which GPU are you using?

---

### 评论 #2 — gofreelee (2023-05-15T04:30:21Z)

AMGGPU MI50  with 4 SE, each SE 15 CUS

---

### 评论 #3 — langyuxf (2023-05-15T07:01:27Z)

Make sure your workloads saturate all the CUs, then you will see the difference.

---

### 评论 #4 — ppanchad-amd (2024-05-13T17:24:10Z)

@gofreelee Has your issue been resolved? If so, please close the ticket. Thanks!

---

### 评论 #5 — ppanchad-amd (2024-08-01T15:12:41Z)

@gofreelee Closing ticket since we haven't heard from you in a while. If you still see the issue with our latest ROCm stack, please re-open the issue. Thanks!

---
