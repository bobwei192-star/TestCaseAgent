# [Feature]: Add support for Instinct MI50/MI60 (gfx906)

> **Issue #5215**
> **状态**: open
> **创建时间**: 2025-08-21T12:06:27Z
> **更新时间**: 2025-08-26T09:17:05Z
> **作者**: William-Droin
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/5215

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Please add support for MI50, they are great GPUs with a lot of VRAM that can be found for cheap on the used market. A cluster of 4 MI50 can be built for 800$, 128gb of fast HBM memory for this price is amazing for students and tinkerers, which will be the people making decisions to buy AMD or not in their future careers.

Dropping support for a server grade GPU after 5 years is not a good sign for people looking to get into AMD's ecosystem. This card has great potential to be an entry point into Machine Learning for people with small budgets but the software support is killing that opportunity.

I was looking at buying a pair of MI210 but I can't commit to something that might have its support dropped within the next 2 years.

Please add support for the MI50 and MI60

### Operating System

_No response_

### GPU

MI50

### ROCm Component

_No response_

---

## 评论 (1 条)

### 评论 #1 — slavap (2025-08-26T09:17:05Z)

@ppanchad-amd By the way, gfx906 is still working on 6.4.0 (and maybe even a later versions) with simple copy hack https://github.com/ROCm/ROCm/issues/4625#issuecomment-2899838977

So just restore support, moving mi50/60 to unsupported is a big mistake. 

---
