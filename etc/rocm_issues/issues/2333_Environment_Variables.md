# Environment Variables

> **Issue #2333**
> **状态**: closed
> **创建时间**: 2023-07-25T16:56:53Z
> **更新时间**: 2024-03-18T16:07:24Z
> **关闭时间**: 2024-03-18T16:07:10Z
> **作者**: samjwu
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2333

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

For each project, have there be a Markdown (or XML) file for environment variables
- XML for common format for projects that do not use Markdown

In ROCm main docs, have a list of all the env vars, similar to how autotag compiles CHANGELOGS

Format:
Name | Component | Description

---

## 评论 (3 条)

### 评论 #1 — amd-isparry (2023-07-29T08:56:43Z)

Environment variables for runtime or compile time or both?

If the variables are intended to be temporary, should they be added? If so what is the support implications? As an example suppose there is a need to sum the first N numbers. The code was written with a for loop "sum=0; for(i=0;i<=N;i++) sum+=i". Later it was suggested a better way was to use a formula attributed to Gauss "sum=N*(N-1)/2". For a trial period you can switch between the two ways by defining the SLOWSUM environment variable so you can check that you get the same result both ways. The long term aim is to remove the loop version of the code and the SLOWSUM variable, which is essentially there for internal debugging purposes.

---

### 评论 #2 — nartmada (2024-03-16T02:26:25Z)

Hi @samjwu, is this task completed?  Just want to check if I can close the ticket.  Thanks.

---

### 评论 #3 — samjwu (2024-03-18T16:07:10Z)

This initiative seems to have been dropped. Closing for now and will reopen when this is revisited

---
