# [Documentation]: Update changelogs to remove need for custom templates

> **Issue #3056**
> **状态**: closed
> **创建时间**: 2024-04-22T20:26:53Z
> **更新时间**: 2024-07-16T22:36:56Z
> **关闭时间**: 2024-07-16T22:36:56Z
> **作者**: samjwu
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/3056

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- samjwu

## 描述

### Description of errors

Eventually remove custom templates `tools/autotag/util/custom_templates` when changelogs follow format in defaults.py

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (6 条)

### 评论 #1 — samjwu (2024-07-09T20:32:09Z)

ck.py 
hipfort.py 
hipify.py 
mivisionx.py 
rpp.py 
rvs.py

---

### 评论 #2 — samjwu (2024-07-09T21:39:50Z)

note: hipify does not appear to have version numbers

---

### 评论 #3 — samjwu (2024-07-09T21:56:55Z)

mivisionx already appears fixed

---

### 评论 #4 — samjwu (2024-07-12T00:03:41Z)

todo rpp, rvs

then try removing unused templates

---

### 评论 #5 — samjwu (2024-07-16T18:13:48Z)

ck, rpp, rvs
have different spelling (ck, rvs) or capitalization (rpp) which causes autotag to miss

---

### 评论 #6 — samjwu (2024-07-16T22:34:55Z)

missing version numbers in hipfort, hipify, rvs

---
