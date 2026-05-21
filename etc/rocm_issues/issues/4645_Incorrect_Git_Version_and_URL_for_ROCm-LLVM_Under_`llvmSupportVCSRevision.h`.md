# Incorrect Git Version and URL for ROCm-LLVM Under `llvm/Support/VCSRevision.h`

> **Issue #4645**
> **状态**: open
> **创建时间**: 2025-04-16T18:37:49Z
> **更新时间**: 2025-04-16T20:39:18Z
> **作者**: matinraayai
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4645

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- lamb-j

## 描述

After building and installing LLVM, the file `llvm/Support/VCSRevision.h` under LLVM's include folder indicates the Git repository revision and URL of the LLVM source code. 

In ROCm-LLVM shipped with ROCm, since the version control information is stripped from all pulled projects in the master build script, the folder of the LLVM project is instead used:
```c++
#define LLVM_REVISION "1e0fda770a2079fbd71e4b70974d74f62fd3af10"
#define LLVM_REPOSITORY "/long_pathname_so_that_rpms_can_package_the_debug_info/src/llvm-project/llvm"
```
I don't think this is intended behavior. As an example use case, [our project](https://github.com/matinraayai/Luthier/blob/main/cmake/modules/LuthierFetchLLVMSrc.cmake) relies on parsing this information to obtain the LLVM source code of an already built binary.
__cc__: @lamb-j 

---

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2025-04-16T19:19:29Z)

Hi @matinraayai.  Thanks for reporting.  Internal ticket has been created to fix this issue. Thanks!

---
