# [Issue]: Link to "Get Started for Windows" broken on Rocm-Hub

> **Issue #2846**
> **状态**: closed
> **创建时间**: 2024-01-27T00:51:58Z
> **更新时间**: 2024-01-29T20:55:06Z
> **关闭时间**: 2024-01-29T20:45:27Z
> **作者**: Spacefish
> **标签**: AMD Instinct MI300X, ROCm 6.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/2846

## 标签

- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.0.0** (颜色: #ededed)

## 描述

### Problem Description

If you visit https://www.amd.com/en/developer/resources/rocm-hub.html#start
and click on the "Get Started for Windows" Button, you will land on a 404 page with the URL:
https://www.amd.com/content/amd/live-site/en/developer/resources/rocm-hub/hip-sdk

### Operating System

irrelevant

### CPU

irrelevant

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — c0dn (2024-01-29T02:46:44Z)

Support link is broken because there isn't a windows version
https://github.com/ROCm/ROCm/releases/tag/win-5.5

Last windows release is 5.5, doesn't support MI300X
https://rocm.docs.amd.com/en/docs-5.5.1/release/windows_support.html

---

### 评论 #2 — Sabrewarrior (2024-01-29T14:59:31Z)

@c0dn There was a 5.7.1 released for Windows on that support page which worked a week ago but now the page is 404. It can still be downloaded directly from https://download.amd.com/developer/eula/rocm-hub/AMD-Software-PRO-Edition-23.Q4-Win10-Win11-For-HIP.exe
Pretty sure no Instinct GPUs were supported for Windows in 5.7.1 though. 
Broken links should be fixed though. Should either have links to the 5.7.1 and 5.5.0 releases, say 6.0 is not released or just remove the link.

---

### 评论 #3 — yhuiYH (2024-01-29T20:45:27Z)

Links should be fixed and working now for the HIP-SDK pages as of this comment.

Thanks all for bringing it to our attention.

Closing this ticket now. Please feel free to point us to any other errors you encounter.

---

### 评论 #4 — neonarc4 (2024-01-29T20:55:04Z)

@Sabrewarrior what the benfit of hip sdk ? since we cant even use torch or tensorflow in rx 7800 xtx  ;/

---
