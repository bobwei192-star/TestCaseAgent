# [Issue]: rdc/rdc.h is missing #include <stdbool.h>

> **Issue #5061**
> **状态**: closed
> **创建时间**: 2025-07-16T19:52:25Z
> **更新时间**: 2025-08-14T13:43:43Z
> **关闭时间**: 2025-08-14T13:43:43Z
> **作者**: morrone
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5061

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

In ROCM 6.4.1, rdc/rdc.h introduces the use of the "bool" type, but it fails to include stdbool.h. It needs to add:

```
#include <stdbool.h>
```

It would be also be great if you could add a simple C build test for this header. This is the second time that rdc.h has failed to compile under C in recent history.

Here's what happens without stdbool.h included:

```
In file included from conftest.c:30:
/opt/rocm-6.4.1/include/rdc/rdc.h:659:3: error: unknown type name 'bool'
   bool is_p2p_accessible;
   ^~~~
/opt/rocm-6.4.1/include/rdc/rdc.h:1739:1: error: unknown type name 'bool'; did you mean '_Bool'?
 bool rdc_is_partition_string(const char* s);
 ^~~~
 _Bool
/opt/rocm-6.4.1/include/rdc/rdc.h:1750:1: error: unknown type name 'bool'; did you mean '_Bool'?
 bool rdc_parse_partition_string(const char* s, uint32_t* physicalGpu, uint32_t* partition);
 ^~~~
 _Bool

```

### Operating System

Any

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2025-07-17T14:10:48Z)

Hi @morrone. Internal ticket has been created to fix this issue. Thanks!

---

### 评论 #2 — lucbruni-amd (2025-08-14T13:43:43Z)

A fix was provided to RDC, which has recently been moved to https://github.com/ROCm/rocm-systems/tree/develop/projects/rdc to address this issue. See https://github.com/ROCm/rocm-systems/commit/ef65d4814995e7aed9e7152753d326ed5af302c4.

If you encounter more issues with C builds for this component in the future, I'll reopen discussion with the team regarding C build tests as there are no plans for them at the moment.

Build from source following [these steps](https://github.com/ROCm/rocm-systems/blob/develop/projects/rdc/README.md#%EF%B8%8F-building-rdc-from-source) on the latest `develop` branch. Also, please feel free to reopen this issue or open a new one if you encounter more build issues. Thanks!

---
