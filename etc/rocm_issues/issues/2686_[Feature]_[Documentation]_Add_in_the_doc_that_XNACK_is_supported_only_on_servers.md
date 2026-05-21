# [Feature]: [Documentation] Add in the doc that XNACK is supported only on servers hosting AMD GPU cards which are ALL supporting XNACK 

> **Issue #2686**
> **状态**: open
> **创建时间**: 2023-12-01T10:46:04Z
> **更新时间**: 2024-05-17T17:02:23Z
> **作者**: pierreantoineH
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2686

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- SwRaw

## 描述

### Suggestion Description

It has been observed that on a server hosting both MI210's cards (suporting XNACK+) and  Radeon Pro W6800 cards, HMM is not working on MI210. When the Radeon Pro W6800 cards is removed from the server, XNACK is working on MI210 cards.
Per the current understanding, SVM memory manager only supports the same XNACK mode for all GPUs, thus this behavior is expected. 
Is it possible to indicate in the documentation that XNACK is supported only on servers hosting AMD GPU cards which are ALL supporting XNACK ? 

### Operating System

_No response_

### GPU

MI210 + W6800

### ROCm Component

ROCm Documentation

---

## 评论 (6 条)

### 评论 #1 — SwRaw (2023-12-04T15:47:31Z)

@saadrahim Does this call for updates in https://rocm.docs.amd.com/en/develop/conceptual/gpu-memory.html#xnack? 

---

### 评论 #2 — pierreantoineH (2023-12-05T14:08:58Z)

Yes, that will be a good place .

---

### 评论 #3 — SwRaw (2023-12-06T09:45:48Z)

@saadrahim Who is the SME for this? I am seeking confirmation of the validity of the given information

---

### 评论 #4 — SwRaw (2023-12-06T09:46:49Z)

@pierreantoineH Do Radeon Pro W6800 not support XNACK? Is XNACK only supported on the MI200 series?

---

### 评论 #5 — ppanchad-amd (2024-05-17T16:57:44Z)

@SwRaw MI products are the only products with XNACK support in ROCm. Thanks!

---

### 评论 #6 — ppanchad-amd (2024-05-17T17:02:23Z)

@pierreantoineH Internal ticket has been created to add XNACK support in documentation. Thanks!

---
