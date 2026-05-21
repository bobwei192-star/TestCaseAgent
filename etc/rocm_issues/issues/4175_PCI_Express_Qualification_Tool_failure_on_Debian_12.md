# PCI Express Qualification Tool failure on Debian 12

> **Issue #4175**
> **状态**: closed
> **创建时间**: 2024-12-20T17:39:01Z
> **更新时间**: 2025-04-11T19:54:47Z
> **关闭时间**: 2025-04-11T19:54:46Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, 6.3.1
> **URL**: https://github.com/ROCm/ROCm/issues/4175

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.3.1** (颜色: #D28178)

## 描述

The PCI Express Qualification Tool (PEQT) module present in the ROCm Validation Suite (RVS) might fail due to the segmentation issue in Debian 12 (bookworm). This will result in failure to determine the characteristics of the PCIe interconnect between the host platform and the GPU like support for Gen 3 atomic completers, DMA transfer statistics, link speed, and link width. The standard PCIe command `lspci` can be used as an alternative to view the characteristics of the PCIe bus interconnect with the GPU. This issue is under investigation and will be addressed in a future release.

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2025-04-11T19:54:46Z)

Resolved in ROCm 6.4.0.

---
