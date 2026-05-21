# Clang compilation failure might occur due to incorrectly installed GNU C++ runtime

> **Issue #4612**
> **状态**: closed
> **创建时间**: 2025-04-11T23:17:29Z
> **更新时间**: 2025-10-30T18:18:13Z
> **关闭时间**: 2025-10-30T18:18:13Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4612

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Clang compilation failure with the error `fatal error: 'cmath' file not found` might occur if the GNU C++ runtime is not installed correctly. The error indicates that the `libstdc++-dev` package, compatible with the latest installed GNU Compiler Collection (GCC) version, is missing. This issue is a result of Clang being unable to find the newest GNU C++ runtimes it recognizes and the associated header files. As a workaround, install the `libstdc++-dev` package compatible with the installed GCC version.

---

## 评论 (3 条)

### 评论 #1 — RobertoMaurizzi (2025-04-15T00:30:45Z)

On Debian the packages end up depending on libstdc++-5-dev or libstdc++-7-dev or libstdc++-11-dev (for rocm-llvm) but in recent distros (likely not only Debian) you'll find only libstdc++-12 or greater, in those cases installing libstdc++-dev isn't going to help at all.

---

### 评论 #2 — sbates130272 (2025-10-01T17:19:18Z)

I can confirm that this issue still exists in ROCm 7.0.1 when installed on a minimal Ubuntu 24.04 server system. Adding `libstdc++-14-dev` resolved this issue for me. I did not (yet) test other releases of `libstdc++-dev`.

---

### 评论 #3 — prbasyal-amd (2025-10-30T18:18:13Z)

Resolved in ROCm 7.1.0.

---
