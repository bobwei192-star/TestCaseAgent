# Create docs/x.y.z branches

> **Issue #2212**
> **状态**: closed
> **创建时间**: 2023-06-01T15:56:45Z
> **更新时间**: 2023-06-05T22:32:00Z
> **关闭时间**: 2023-06-05T22:31:59Z
> **作者**: saadrahim
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2212

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- samjwu

## 描述

- [x] For all ROCm releases from 5.0.0 to 5.5.1, create a docs/x.y.z branch.

- [x] Also create the corresponding RTD build jobs.

- [x] Make just the latest versions visible in the flyout menu via RTD config.

---

## 评论 (3 条)

### 评论 #1 — samjwu (2023-06-01T22:15:06Z)

Branches have been created for ROCm repositories with tags in the format below:

tag `rocm-5.x.x` > branch `docs/5.x.x`

---

### 评论 #2 — samjwu (2023-06-02T23:55:00Z)

Also create the corresponding RTD build jobs.
Make just the latest versions visible in the flyout menu via RTD config.

Done for all repos except rdc (need an admin to activate the GitHub webhook for this repo)

---

### 评论 #3 — samjwu (2023-06-05T22:31:59Z)

Done for all repos that have tags with the format `rocm-5.x.x`

---
