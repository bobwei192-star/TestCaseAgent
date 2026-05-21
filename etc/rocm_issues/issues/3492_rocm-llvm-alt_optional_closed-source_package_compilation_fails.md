# rocm-llvm-alt optional closed-source package compilation fails

> **Issue #3492**
> **状态**: closed
> **创建时间**: 2024-08-02T18:13:47Z
> **更新时间**: 2024-12-04T15:21:44Z
> **关闭时间**: 2024-12-04T15:21:44Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3492

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.2.0** (颜色: #31778C)

## 描述

ROCm provides an optional package – `rocm-llvm-alt` – that provides a closed-source compiler for users interested in additional closed-source CPU optimizations. This feature is not functional in the ROCm 6.2.0 release. Users who attempt to invoke the closed-source compiler will experience an LLVM consumer-producer mismatch and the compilation will fail. There is no workaround that allows use of the closed-source compiler. It is recommended to compile using the default open-source compiler, which generates high-quality AMD CPU and AMD GPU code.

The `rocm-llvm-alt` package will be removed in an upcoming release. Users relying on the functionality provided by the closed-source compiler should transition to the open-source compiler. Once the `rocm-llvm-alt` package is removed, any compilation requesting functionality provided by the closed-source compiler will result in a Clang warning: `[AMD] proprietary optimization compiler has been removed`.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2024-12-04T15:21:44Z)

The `rocm-llvm-alt-package` is removed as of ROCm 6.3.0.

---
