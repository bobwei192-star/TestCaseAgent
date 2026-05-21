# [Issue]: ROCm Ubuntu 20.04 packages SHA256 changed

> **Issue #4658**
> **状态**: closed
> **创建时间**: 2025-04-18T08:46:20Z
> **更新时间**: 2025-04-22T07:16:59Z
> **关闭时间**: 2025-04-22T07:16:58Z
> **作者**: danieldk
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4658

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

We use the ROCm Ubuntu 20.04 packages to build Nix derivations for ROCm. Since Nix requires that data fetched from the internet is a fixed-output, we store the SHA-256 of all packages:

https://github.com/huggingface/rocm-nix/blob/main/pkgs/rocm-packages/rocm-6.3.4-metadata.json

The sha256 checksums are retrieved directly from the package index (`Packages`) from the repository.

However, in the last few days, our builds started failing because the SHA256 hashes of a lot of ROCm 6.3.4 `-rpath` packages changed. Here is the diff:

https://gist.github.com/danieldk/2e75f947c2eaf0953d6f2a2377d96893

Were the packages updated in-place without bumping up the package revision or were they compromised? I inspected one of the packages and could not find anything suspect after a quick look, but wanted to check.

### Operating System

Ubuntu 20.04 (Focal Fossa)

### CPU

AMD EPYC 7R13 Processor

### GPU

None

### ROCm Version

6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-04-21T18:50:19Z)

Thanks for the report @danieldk. Let me confirm with our repo owners and get back to you on this.

---

### 评论 #2 — WBobby (2025-04-21T22:12:17Z)

Thanks for bringing this to our attention, and apologies for the confusion. At the beginning of the April, we introduced multi-version package changes for ROCm 6.3.4 that resulted in updated checksums for some packages. These packages were not compromised; they were re-uploaded to address internal fixes and support multi-version functionality, inadvertently causing the SHA-256 hashes to change without incrementing the package revision number.

---

### 评论 #3 — danieldk (2025-04-22T07:16:58Z)

Thanks for the confirmation @WBobby that it is all good! I'll then sync our build infrastructure with the latest hashes.

---
