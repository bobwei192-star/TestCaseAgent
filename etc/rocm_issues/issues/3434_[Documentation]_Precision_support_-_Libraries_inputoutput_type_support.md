# [Documentation]: Precision support - Libraries input/output type support

> **Issue #3434**
> **状态**: open
> **创建时间**: 2024-07-18T15:50:01Z
> **更新时间**: 2024-12-10T14:58:05Z
> **作者**: garrettbyrd
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/3434

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

The support matrix discussed below needs to provide information on all ROCm libraries, not just the six provided.

Currently the documentation for precision support ([here](https://rocm.docs.amd.com/en/latest/compatibility/precision-support.html#libraries-input-output-type-support)) aims to provide an overview for supported and unsupported precisions (e.g., `float16`) across various ROCm libraries. However, only 3 roc + 3 hip libraries are provided. This is a tiny amount of the actual number of ROCm libaries ([here](https://rocm.docs.amd.com/en/latest/reference/api-libraries.html)); particularly, the Math libraries, which are arguably some of the most relevant for non-standard precisions, are severely lacking in the supported/unsupported matrix.

Also, the libraries hipRAND and hipCUB have implied hyperlinks in the form of "(details)", but these are just text and do not link to anything.


### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-07-19T15:19:26Z)

Hi @garrettbyrd, an internal ticket has been created to update/fix the documentation. Thanks!

---

### 评论 #2 — harkgill-amd (2024-12-10T14:58:03Z)

@garrettbyrd, quick update on this issue. The hyperlinks for both `hipRAND` and `hipCUB` have been fixed and now link to the correct pages. We are also working on extending the list to cover more libraries, including the missing Math libraries. These changes will be live in an upcoming ROCm release.

---
