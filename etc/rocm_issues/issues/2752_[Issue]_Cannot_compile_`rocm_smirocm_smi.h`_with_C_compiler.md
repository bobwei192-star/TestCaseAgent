# [Issue]: Cannot compile `rocm_smi/rocm_smi.h` with C compiler

> **Issue #2752**
> **状态**: closed
> **创建时间**: 2023-12-19T13:44:06Z
> **更新时间**: 2024-01-09T17:22:21Z
> **关闭时间**: 2024-01-09T17:22:20Z
> **作者**: bertwesarg
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2752

## 描述

### Problem Description

This header does not compile with any C compiler. I already reported this to @vlaindic via mail.

### Operating System

Docker image rocm/dev-ubuntu-22.04:6.0

### CPU

any

### GPU

Other

### Other

any

### ROCm Version

ROCm 6.0.0

### ROCm Component

rocm_smi_lib

### Steps to Reproduce

```console
$ docker run --rm -it rocm/dev-ubuntu-22.04:6.0
# echo '#include <rocm_smi/rocm_smi.h>' >test.c
# /opt/rocm-6.0.0/bin/amdclang -I/opt/rocm-6.0.0/include -c test.c
In file included from test.c:1:
/opt/rocm-6.0.0/include/rocm_smi/rocm_smi.h:5370:51: error: must use 'struct' tag to refer to type 'metrics_table_header_t'
rsmi_dev_metrics_header_info_get(uint32_t dv_ind, metrics_table_header_t* header_value);
                                                  ^
                                                  struct 
1 error generated.
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — Thyre (2023-12-19T13:50:13Z)

Just as a note: Adding the `struct` keyword fixes the issue. 

---

### 评论 #2 — bertwesarg (2023-12-19T13:52:04Z)

> Just as a note: Adding the `struct` keyword fixes the issue.

yeah, thats what the compiler already proposed. Though the file is using `typedef` so it should be consistent. And the `typedef`s are all prefixed with `rsmi_`

---

### 评论 #3 — vlaindic (2023-12-20T08:39:32Z)

Hi @bertwesarg @Thyre ,

Thank you very much for reporting this issue! I had already reported it issue to the team responsible for maintaining the rocm-smi and they proposed the fixed that is under review. 

Hey @oliveiradan , could you provide more information when we can expect the fix to land? Thanks!

Best,
Vladimir

---

### 评论 #4 — vlaindic (2024-01-09T17:22:20Z)

Hi @bertwesarg @Thyre ,

The related issues is opened here: https://github.com/ROCm/rocm_smi_lib/issues/147 , so I will close this one! :) 

Best regards, 
Vladimir

---
