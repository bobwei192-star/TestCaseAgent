# Compiler errors with high register pressure

> **Issue #2109**
> **状态**: closed
> **创建时间**: 2023-05-04T09:14:47Z
> **更新时间**: 2023-05-04T09:14:55Z
> **关闭时间**: 2023-05-04T09:14:55Z
> **作者**: Naraenda
> **标签**: Verified Issue, 5.4.2
> **URL**: https://github.com/ROCm/ROCm/issues/2109

## 标签

- **Verified Issue** (颜色: #0052cc)
- **5.4.2** (颜色: #e99695)

## 描述

This issue is ported from the release notes.

Under certain circumstances typified by high register pressure, users may encounter a compiler abort with one of the following error messages:

- `error: unhandled SGPR spill to memory`
- `cannot scavenge register without an emergency spill slot!`
- `error: ran out of registers during register allocation`

---

## 评论 (1 条)

### 评论 #1 — Naraenda (2023-05-04T09:14:55Z)

Fixed in 5.4.3

---
