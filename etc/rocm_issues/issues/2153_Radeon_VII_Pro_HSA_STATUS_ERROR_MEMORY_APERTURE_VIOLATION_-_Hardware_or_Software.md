# Radeon VII Pro: HSA_STATUS_ERROR_MEMORY_APERTURE_VIOLATION - Hardware or Software

> **Issue #2153**
> **状态**: closed
> **创建时间**: 2023-05-19T10:19:08Z
> **更新时间**: 2023-11-11T19:38:40Z
> **关闭时间**: 2023-11-10T16:33:08Z
> **作者**: fftfp64
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2153

## 描述

Hi,
Simulation code with embedded hip running on Radeon VII pro and ROCm 5.18.13. It  *always* fails with some memory error, most commonly with something like:

:0:rocdevice.cpp :2672: 0696142325 us: 5999 : [tid:0x7f676e4c7640] Device::callbackQueue aborting with error : HSA_STATUS_ERROR_MEMORY_APERTURE_VIOLATION: The agent attempted to access memory beyond the largest legal address. code: 0x29
forrtl: error (76): Abort trap signal  + some backtrace.

but it *always* works on MI60, MI50 and Radeon VII (non-pro).

Is it possible to:
1) Say if this is hardware or driver error.
2) Any possible test for the card itself.
3) Say anything at all.

Thanks.
--







---

## 评论 (2 条)

### 评论 #1 — kentrussell (2023-11-10T16:33:08Z)

This should have been resolved in ROCm 5.5 or 5.6 (I forget which one). Can you try to update to 5.7.x and reopen this if the issue still persists? If it's still persisting, can you attach a full dmesg so we can take a look at what's happening? Thanks!

---

### 评论 #2 — fftfp64 (2023-11-11T19:38:40Z)

That took awhile. I returned the card to the seller as faulty.

---
