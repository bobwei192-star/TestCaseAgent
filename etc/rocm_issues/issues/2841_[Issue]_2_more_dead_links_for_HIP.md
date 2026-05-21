# [Issue]:  2 more dead links for HIP

> **Issue #2841**
> **状态**: closed
> **创建时间**: 2024-01-26T17:22:11Z
> **更新时间**: 2024-04-09T05:32:31Z
> **关闭时间**: 2024-01-29T21:14:13Z
> **作者**: ArtisticMusician
> **标签**: ROCm 5.5.0, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/2841

## 标签

- **ROCm 5.5.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

This page has a 404 error link  near the bottom of the page with the text "HIP-SDK Download Page"

https://rocm.docs.amd.com/projects/install-on-windows/en/latest/how-to/install.html

The next page has 2 bad links, on link goes to a 404 error  page and the other link got back to the page you came from

1. The first link is located in the first paragraph the link text is "Install HIP SDK" - this link goes pack to the pge you came from 
2. The second link is in set 1  under download the installer and the link text is "HIP-SDK download page"

https://rocm.docs.amd.com/projects/install-on-windows/en/latest/index.html#hip-install-quick

### Operating System

Win11

### CPU

AMD Ryzen 9 7950X

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 5.5.0

### ROCm Component

_No response_

### Steps to Reproduce

Got to the urls listed above and click on the links specified.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

I actually have no ROCm version installed on my machine. Although not for lack of trying. But this form forced me to choose a ROCm version before letting me submit it. 

---

## 评论 (3 条)

### 评论 #1 — Spacefish (2024-01-27T00:48:28Z)

The old links to the windows installers for the HIP-SDK still work:
https://download.amd.com/developer/eula/rocm-hub/AMD-Software-PRO-Edition-23.Q3-Win10-Win11-For-HIP.exe
https://download.amd.com/developer/eula/rocm-hub/AMD-Software-PRO-Edition-23.Q2-Win10-Win11-For-HIP.exe

however there is no:
https://download.amd.com/developer/eula/rocm-hub/AMD-Software-PRO-Edition-24.Q1-Win10-Win11-For-HIP.exe

so i guess they haven´t even released the Hip-SDK 6.0.0 for windows..

---

### 评论 #2 — yhuiYH (2024-01-29T21:14:13Z)

Links should be fixed and working now for the HIP-SDK pages as of this comment.

Thanks all for bringing it to our attention.

Closing this ticket now. Please feel free to point us to any other errors you encounter.

---

### 评论 #3 — FlattusBlastus (2024-04-09T05:32:31Z)

Not found as of 4-8-2024

---
