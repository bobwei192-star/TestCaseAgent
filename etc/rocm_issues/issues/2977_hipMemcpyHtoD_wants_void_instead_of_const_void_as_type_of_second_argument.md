# hipMemcpyHtoD wants void* instead of const void* as type of second argument

> **Issue #2977**
> **状态**: open
> **创建时间**: 2024-03-25T15:18:16Z
> **更新时间**: 2025-03-26T11:00:24Z
> **作者**: HannoSpreeuw
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon Pro W6800
> **URL**: https://github.com/ROCm/ROCm/issues/2977

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon Pro W6800** (颜色: #ededed)

## 描述

### Problem Description

Calling `hipMemcpyHtoD(dst, src, size)` with the same types of arguments as a succesful call to `cuMemcpyHtoD` gives
```
error: invalid conversion from 'const void*' to 'void*' [-fpermissive]
   48 |   .....(hipMemcpyHtoD(dst, src, size));
      |                            ^~~
      |                            |
      |                            const void*
```

So the problem is with the second argument, i.e. `src` with is of type `const void*` and not `void*`, which `hipMemcpyHtoD` needs, contrary to `cuMemcpyHtoD` .

This means that just running `hipconvertinplace-perl.sh` is insufficient.

### Operating System

NAME="Rocky Linux" VERSION="8.9 (Green Obsidian)"

### CPU

AMD EPYC 7282 16-Core Processor

### GPU

AMD Radeon Pro W6800

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Call `hipMemcpyHtoDAsync` with a `const void*` type second argument while not using `-fpermissive`.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — nartmada (2024-04-01T15:10:33Z)

An internal ticket has been created to track the investigation.

---

### 评论 #2 — nartmada (2024-06-16T14:50:25Z)

@HannoSpreeuw, sorry for the slow response.  Issue will be addressed in an upcoming ROCm release.  Thanks.

---

### 评论 #3 — loostrum (2025-03-26T11:00:24Z)

This issue is still present as of ROCm 6.3.0. While I realise this is a relatively minor issue, it would be nice if it would be fixed eventually.

---
