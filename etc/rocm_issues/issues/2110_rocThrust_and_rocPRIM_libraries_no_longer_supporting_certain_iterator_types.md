# rocThrust and rocPRIM libraries no longer supporting certain iterator types

> **Issue #2110**
> **状态**: closed
> **创建时间**: 2023-05-04T09:26:59Z
> **更新时间**: 2023-05-04T09:27:08Z
> **关闭时间**: 2023-05-04T09:27:08Z
> **作者**: Naraenda
> **标签**: Verified Issue, 5.3.0, 5.3.1, 5.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/2110

## 标签

- **Verified Issue** (颜色: #0052cc)
- **5.3.0** (颜色: #fbca04)
- **5.3.1** (颜色: #4FE5CF)
- **5.3.2** (颜色: #503B15)

## 描述

This issue is ported from the release notes.

There is a known known issue with rocThrust and rocPRIM libraries supporting iterator and types in ROCm v5.3.x releases.

- `thrust::merge` no longer correctly supports different iterator types for `keys_input1` and `keys_input2`.
- `rocprim::device_merge` no longer correctly supports using different types for `keys_input1` and `keys_input2`.

---

## 评论 (1 条)

### 评论 #1 — Naraenda (2023-05-04T09:27:08Z)

Fixed in 5.3.3

---
