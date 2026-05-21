# AddressSanitizer instrumentation incorrect for device global variables

> **Issue #2551**
> **状态**: closed
> **创建时间**: 2023-10-13T21:38:20Z
> **更新时间**: 2024-04-17T20:19:40Z
> **关闭时间**: 2024-04-17T20:19:40Z
> **作者**: Rmalavally
> **标签**: Under Investigation, Verified Issue, Resolved, 5.7.1, 6.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/2551

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Verified Issue** (颜色: #0052cc)
- **Resolved** (颜色: #6DAE35)
- **5.7.1** (颜色: #b60205)
- **6.0.0** (颜色: #01DED3)

## 描述

The AddressSanitizer instrumentation results in incorrect information about the size of device global variables, which causes,

- the function *hipModuleGetGlobal* to return an incorrect size, resulting in the generation of a buffer overflow report if used in a hipMemcpy operation

- failures reported by calls to the function *hipModuleGetTexRef*

This issue is under investigation and will be fixed in a future release.


---

## 评论 (1 条)

### 评论 #1 — Rmalavally (2024-04-17T13:16:04Z)

This issue is resolved in the ROCm 6.1 release. 

AddressSanitizer (ASan):
- Added sanitized_padded_global LLVM ir attribute to identify sanitizer instrumented globals.
- For ASan instrumented global, emit two symbols: one with actual size and the other with instrumented size.

For details, refer to the ROCm 6.1 changelog at https://rocm.docs.amd.com/en/latest/about/CHANGELOG.html

---
