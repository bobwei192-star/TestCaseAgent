# [Feature]: global synchronization 

> **Issue #4120**
> **状态**: closed
> **创建时间**: 2024-12-06T08:06:31Z
> **更新时间**: 2024-12-06T16:32:15Z
> **关闭时间**: 2024-12-06T16:32:15Z
> **作者**: johnnynunez
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4120

## 描述

### Suggestion Description

Rocm has cooperative_groups.this_grid().sync()? (This is from nvidia cooperative groups)
I mean Global Synchronization in the grid, it is like cooperative_groups.this_grid().sync()

also:
Does rocm also have shared memory?
That you can use with “asynchronous copies,” where what interests me the most is the ability to move data from the device to shared memory without going through the registers.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (1 条)

### 评论 #1 — b-sumner (2024-12-06T15:17:45Z)

Cooperative groups are supported, including this_grid.sync().

HIP, like Cuda, has __shared__ variables.  HIP doesn't currently support some of the Cuda async functions.

---
