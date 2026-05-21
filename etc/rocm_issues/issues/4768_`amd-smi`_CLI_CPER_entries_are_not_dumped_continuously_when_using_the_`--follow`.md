# `amd-smi` CLI: CPER entries are not dumped continuously when using the `--follow` flag

> **Issue #4768**
> **状态**: closed
> **创建时间**: 2025-05-21T18:44:11Z
> **更新时间**: 2025-07-21T20:47:23Z
> **关闭时间**: 2025-07-21T20:47:23Z
> **作者**: peterjunpark
> **标签**: Verified Issue, ROCm 6.4.1
> **URL**: https://github.com/ROCm/ROCm/issues/4768

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.1** (颜色: #aaaaaa)

## 描述

When using the `--follow` flag with `amd-smi ras --cper`, CPER entries are not streamed continuously as intended. This will be fixed in an upcoming ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-07-21T20:47:23Z)

Resolved in ROCm 6.4.2.

---
