# Port `roc-obj-*` utilities over to Windows (and install with the HIP SDK)

> **Issue #2396**
> **状态**: closed
> **创建时间**: 2023-08-22T10:52:16Z
> **更新时间**: 2024-03-31T14:01:30Z
> **关闭时间**: 2024-03-31T14:01:30Z
> **作者**: MathiasMagnus
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2396

## 负责人

- david-salinas
- kzhuravl

## 描述

These Perl utilities occasionally call into Linux utilities like `dd` which clearly don't exist on Windows.

Please port them to work on Windows.

---

## 评论 (1 条)

### 评论 #1 — nartmada (2024-03-31T14:01:30Z)

Issue has been fixed in the "staging" branch and will be available in an upcoming release.

---
