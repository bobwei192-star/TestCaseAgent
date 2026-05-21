# When will ROCm support 680M and 780M aka ryzen 7735U?

> **Issue #5815**
> **状态**: closed
> **创建时间**: 2025-12-25T20:11:58Z
> **更新时间**: 2026-02-17T19:15:08Z
> **关闭时间**: 2026-02-17T19:15:08Z
> **作者**: MYCHMA
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5815

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Suggestion Description

on windows
I want to use my gpu as accelerator for my code I do not have nvidia gpus so I am still waiting(1 year) when you do finely port your first party "GPU PARALER PROGRAMING LANGUAGE EXTENSION"(aka CUDA lib sh*t) to windows. Even though I hate it I do not have the luxury to migrate to linux.
And also lately I really like to have my llm in llm studio running faster. Vulkan is good but its by windows meter utilized 70% - 80% whith is not ideal. Also I can be thea models are more memory bound than procesing. sooo yeeah 

Whatever just add the support for it so I can start to optimitze my liquid sim to it. PLS. Thanks.


### Operating System

Windows 10/11

### GPU

680M and 780M

### ROCm Component

everything

---

## 评论 (2 条)

### 评论 #1 — schung-amd (2026-01-27T19:55:32Z)

Hi @MYCHMA, we have gfx1103 (780M) support via TheRock: see https://github.com/ROCm/TheRock/blob/main/ROADMAP.md. TheRock does not have support for 680M (gfx1035) and other RDNA2 architectures, but that is on our radar.

---

### 评论 #2 — schung-amd (2026-02-17T19:15:08Z)

@MYCHMA I've been informed that TheRock is now expected to work on RDNA2, gfx1035 is not specifically listed as we do not have hardware to validate it.

I'll close this for now as your support requests should be fulfilled via TheRock. Feel free to comment here and/or open new issues if it doesn't work for you or is insufficient for your needs.

---
