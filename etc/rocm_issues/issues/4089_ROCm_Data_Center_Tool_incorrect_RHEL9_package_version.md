# ROCm Data Center Tool incorrect RHEL9 package version

> **Issue #4089**
> **状态**: closed
> **创建时间**: 2024-12-03T22:20:00Z
> **更新时间**: 2024-12-03T22:59:36Z
> **关闭时间**: 2024-12-03T22:59:36Z
> **作者**: peterjunpark
> **标签**: Verified Issue, ROCm 6.2.0, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4089

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.2.0** (颜色: #ededed)
- **6.3.0** (颜色: #303737)

## 描述

In previous versions of ROCm Data Center Tool (RDC) included with ROCm 6.2 for RHEL9, RDC’s version number was incorrectly set to 1.0.0. ROCm 6.3 includes RDC with the correct version number.

>[!IMPORTANT]
>If you’re using RHEL9, you must first uninstall the existing ROCm 6.2 RDC 1.0.0 package with `sudo yum remove rdc` before upgrading to the ROCm 6.3 RDC package `sudo yum install rdc`.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2024-12-03T22:59:36Z)

The version number is fixed in ROCm 6.3.0.

RDC users on RHEL9: use the workaround in the issue description when upgrading from ROCm 6.2.x.

---
