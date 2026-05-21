# rocprofv3 fails on RPM-based OS with Python 3.10 (and later)

> **Issue #5606**
> **状态**: closed
> **创建时间**: 2025-10-31T17:50:01Z
> **更新时间**: 2026-01-28T16:18:21Z
> **关闭时间**: 2026-01-28T16:18:21Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/5606

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

On RPM-based operating systems (such as RHEL 8), the `rocprofv3` tool fails with Python 3.10 and later due to missing ROCPD bindings. As a workaround, use Python 3.6 if you need to use the `rocprofv3` tool with ROCm 7.1.0. This issue will be fixed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-01-28T16:18:21Z)

Resolved in ROCm 7.2.0.

---
