# Incorrect compilation with uninitialized parameters in __shfl function

> **Issue #3499**
> **状态**: closed
> **创建时间**: 2024-08-02T18:57:06Z
> **更新时间**: 2024-12-03T23:34:27Z
> **关闭时间**: 2024-12-03T23:34:27Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3499

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.2.0** (颜色: #31778C)

## 描述

The compiler may incorrectly compile a program that uses the `__shfl(var, srcLane, width)` function when one of the parameters to the function is undefined along some path to the function. For most functions, uninitialized inputs cause undefined behavior.

>Note:
>
>The `-Wall` compilation flag prompts the compiler to generate a warning if a variable is uninitialized along some path.

As a workaround, initialize the parameters to __shfl. For example:

```
unsigned long istring = 0 // Initialize the input to __shfl
return __shfl(istring, 0, 64)
```

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2024-12-03T23:34:27Z)

Fixed in ROCm 6.3.0.

---
