# Search in documentation does not work with keywords alone

> **Issue #2765**
> **状态**: closed
> **创建时间**: 2023-12-21T15:18:19Z
> **更新时间**: 2024-06-25T19:55:41Z
> **关闭时间**: 2024-06-25T19:09:14Z
> **作者**: gsitaram
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2765

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

I wanted to get documentation on __threadfence_block(), but when I searched for "threadfence", I didn't get any results. Even "threadfence_block" did not pull up any results. Only the exact "__threadfence_block" pulled up 2 results. Could the search functionality be improved so that users don't have to know the exact thing they want? That kind-of defeats the purpose.. 

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2024-05-17T18:16:22Z)

@gsitaram Internal ticket has been created to fix documentation. Thanks!

---

### 评论 #2 — samjwu (2024-06-25T19:09:14Z)

![image](https://github.com/ROCm/ROCm/assets/22262939/25bf2633-5ff8-49db-976c-9e21cb9fc04f)

Matches for partial search

---

### 评论 #3 — samjwu (2024-06-25T19:55:40Z)

the search across subprojects appears to be less detailed than the search in the current project
https://docs.readthedocs.io/en/stable/server-side-search/index.html

compare
https://rocm.docs.amd.com/en/latest/search.html?q=threadfence#
to
https://rocm.docs.amd.com/projects/HIP/en/latest/search.html?q=threadfence
and
https://rocm.docs.amd.com/projects/HIPIFY/en/latest/search.html?q=threadfence

---
