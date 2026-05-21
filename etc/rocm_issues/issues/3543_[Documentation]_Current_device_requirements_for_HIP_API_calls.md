# [Documentation]: Current device requirements for HIP API calls

> **Issue #3543**
> **状态**: closed
> **创建时间**: 2024-08-08T05:26:16Z
> **更新时间**: 2024-10-30T15:16:08Z
> **关闭时间**: 2024-10-30T15:16:07Z
> **作者**: sogartar
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3543

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I would like to know what HIP API functions require the current device to match the one from explicit arguments like streams or graphs.

For example `hipFreeAsync`. Does it require the current device to match the one associated with the stream argument?
There are some obvious functions that would depend on the current device, like `hipMalloc`.
It seems the [HIP documentation](https://rocm.docs.amd.com/projects/HIP/en/latest/) is lacking this information.
I am concerned for pretty much all functions from the API. Does the omission of restrictions in the doc mean it is allowed?

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-08-09T17:41:32Z)

Hi @sogartar, let me look into your query and circle back to you.

---

### 评论 #2 — schung-amd (2024-10-25T15:17:31Z)

> Does the omission of restrictions in the doc mean it is allowed?

This is correct, HIP API functions which take a stream as an explicit argument do not require you to set the current device to match the stream's device.

---

### 评论 #3 — schung-amd (2024-10-30T15:16:08Z)

Closing this, feel free to comment if you need additional guidance on HIP API calls taking explicit stream arguments.

---
