# error: reference to __host__ function '<deduction guide for tuple><int, int>' in __host__ __device__ function

> **Issue #5646**
> **状态**: closed
> **创建时间**: 2025-11-09T17:02:55Z
> **更新时间**: 2025-12-02T15:34:50Z
> **关闭时间**: 2025-12-02T15:34:50Z
> **作者**: misos1
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5646

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

Seems like deduction guides are treated as actual functions. They should probably not. Much like `constexpr` functions do not need to be annotated with `__host__`/`__device__`.

``` c++
#include <tuple>
#include <hip/hip_runtime.h>

__host__ __device__ void func()
{
	std::tuple<int, int> t = std::tuple(1, 1);
}
```
```
> hipcc -std=c++23 a.cpp
a.cpp:6:27: error: reference to __host__ function '<deduction guide for tuple><int, int>' in __host__ __device__ function
    6 |         std::tuple<int, int> t = std::tuple(1, 1);
      |                                  ^
/usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/tuple:1203:5: note: '<deduction guide for tuple><int, int>' declared here
 1203 |     tuple(_UTypes...) -> tuple<_UTypes...>;
      |     ^
```


---

## 评论 (1 条)

### 评论 #1 — tcgu-amd (2025-11-10T18:38:05Z)

Hi @misos1, thanks for reporting. Was able to confirm that this is indeed an issue. We will draft a patch for it soon. Thanks! 

---
