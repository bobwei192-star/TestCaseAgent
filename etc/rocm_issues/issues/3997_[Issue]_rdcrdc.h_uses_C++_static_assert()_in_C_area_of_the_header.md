# [Issue]: rdc/rdc.h uses C++ static_assert() in C area of the header

> **Issue #3997**
> **状态**: closed
> **创建时间**: 2024-11-06T00:42:09Z
> **更新时间**: 2025-01-13T19:49:03Z
> **关闭时间**: 2025-01-13T19:49:03Z
> **作者**: morrone
> **标签**: Under Investigation, ROCm 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/3997

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.1** (颜色: #ededed)

## 描述

### Problem Description

Building a C program that includes rdc/rdc.h from ROCm 6.2.1, I'm hitting this error:

```
In file included from conftest.c:28:
/opt/rocm-6.2.1/include/rdc/rdc.h:325:33: error: expected ')' before '%' token
 static_assert(RDC_FI_ECC_SDMA_CE % 2 == 0, "Correctable Error enum is not even");
```

It look like the header uses static_assert(), which I assume is only available in C++, in a C-exposed area of the header.


### Operating System

RHEL8

### CPU

Irrelevant

### GPU

Irrelevant

### ROCm Version

ROCm 6.2.1

### ROCm Component

rdc

### Steps to Reproduce

Compile any C program while including rdc/rdc.h.


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — morrone (2024-11-06T00:45:28Z)

It looks like static_assert() is available in C if the assert.h header is included. rdc/rdc.h fails to include <assert.h>.


---

### 评论 #2 — harkgill-amd (2024-11-06T18:28:49Z)

Hi @morrone, thanks for pointing this out. I was able to reproduce the errors and resolve them by including `assert.h` for C compilation. Will work on getting this change implemented. 

---

### 评论 #3 — harkgill-amd (2025-01-13T19:49:03Z)

@morrone, the fix has made it into amd-staging at https://github.com/ROCm/rdc/commit/83f36f1673e9662da3f4387dd0678e20aacd3346 and will be included in an upcoming ROCm release. Will close out this issue, if you have any questions or concerns please leave a comment and I'll re-open this ticket. Thanks!

---
