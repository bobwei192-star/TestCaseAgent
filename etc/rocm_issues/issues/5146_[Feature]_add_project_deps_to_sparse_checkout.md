# [Feature]: add project deps to sparse checkout

> **Issue #5146**
> **状态**: open
> **创建时间**: 2025-08-01T17:05:37Z
> **更新时间**: 2025-08-27T18:59:13Z
> **作者**: davidd-amd
> **标签**: External CI
> **URL**: https://github.com/ROCm/ROCm/issues/5146

## 标签

- **External CI** (颜色: #58C55D)

## 负责人

- jayhawk-commits

## 描述

### Suggestion Description

To use first party component dependencies from rocm-libraries we need to clone both the component being tested along with the components first party deps. Can we add a section to the yaml spec to list the component deps which may be in shared or projects

### Operating System

all

### GPU

all

### ROCm Component

rocm-libraries

---

## 评论 (1 条)

### 评论 #1 — jayhawk-commits (2025-08-27T18:59:13Z)

Do you think this selective sparse-checkout behaviour is needed with the superbuild work being done?

---
