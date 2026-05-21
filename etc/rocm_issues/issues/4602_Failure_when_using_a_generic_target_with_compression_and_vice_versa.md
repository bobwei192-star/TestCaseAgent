# Failure when using a generic target with compression and vice versa

> **Issue #4602**
> **状态**: closed
> **创建时间**: 2025-04-11T23:05:09Z
> **更新时间**: 2025-09-16T17:37:59Z
> **关闭时间**: 2025-09-16T17:37:59Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4602

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

In ROCm 6.4.0, compilation for generic target with compression will fail. As a result, you won't be able to compile for a generic target and use compression simultaneously. As a workaround, it's recommended not to use compression when using generic targets and vice versa. This issue will be addressed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-09-16T17:37:59Z)

Resolved in ROCm 7.0.0.

---
