# [Feature]: Installation steps for Debian 12

> **Issue #2802**
> **状态**: closed
> **创建时间**: 2024-01-12T18:26:24Z
> **更新时间**: 2024-01-31T03:20:19Z
> **关闭时间**: 2024-01-31T03:20:19Z
> **作者**: meminens
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2802

## 描述

### Suggestion Description

Can you please provide instructions to get ROCm installed on Debian 12? I believe I can follow the Ubuntu instructions with some caveat. But it would be much better if you can include official step by step installation guide. Thanks!

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/index.html


### Operating System

Debian 12

### GPU

7900 XTX

### ROCm Component

_No response_

---

## 评论 (3 条)

### 评论 #1 — supersonictw (2024-01-15T04:12:49Z)

Duplicated
https://github.com/ROCm/ROCm/issues/2646

---

### 评论 #2 — cgmb (2024-01-15T04:52:33Z)

Hi @misaligar, AMD doesn't provide official support for ROCm on Debian, which is why there isn't an official installation guide for Bookworm. I know that some users on Debian install binaries into an Ubuntu container and copy them into `/opt/rocm` on their Debian installation, but I've never tried it myself. Ideally, there would be ROCm packages available in the `bookworm-backports` repo.

The Debian ROCm Team plans to prepare backports once they complete the update to ROCm 5.7 and the packaging of pytorch-rocm for Debian Trixie. If there are any particular packages that you need that are not yet packaged for Debian, please feel free to file an RFP on the Debian bug tracker.

And, of course, it never hurts to get involved yourself. There's a relatively small group of volunteers maintaining ROCm packages on Debian. A few more volunteers with the right skills and motivation could really speed up the process.

---

### 评论 #3 — meminens (2024-01-31T03:20:19Z)

Thank you!

---
