# distributed/test_distributed_spawn Fails

> **Issue #2107**
> **状态**: closed
> **创建时间**: 2023-05-04T08:00:10Z
> **更新时间**: 2024-02-16T20:10:51Z
> **关闭时间**: 2024-02-16T20:10:51Z
> **作者**: Naraenda
> **标签**: Verified Issue, 5.5.0
> **URL**: https://github.com/ROCm/ROCm/issues/2107

## 标签

- **Verified Issue** (颜色: #0052cc)
- **5.5.0** (颜色: #fbca04)

## 描述

This issue is ported from the release notes.

When user applications call `ncclCommAbort` to destruct communicators and then create new
communicators repeatedly, subsequent communicators may fail to initialize.

---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-02-14T03:44:17Z)

Hi @Naraenda, does this issue still exists with latest ROCm 6.0.2 ?  If issue is resolved, please close the ticket.  Thanks.

---

### 评论 #2 — nartmada (2024-02-16T20:10:51Z)

Closing the ticket as no response from @Naraenda.  Please re-open if the issue is not fixed in latest ROCm6.0.2

---
