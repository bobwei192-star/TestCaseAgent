# HIP masked stream soft hang

> **Issue #2082**
> **状态**: closed
> **创建时间**: 2023-04-25T02:49:50Z
> **更新时间**: 2023-04-27T08:45:07Z
> **关闭时间**: 2023-04-27T08:43:00Z
> **作者**: xuantengh
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2082

## 描述

In the [change log](https://github.com/RadeonOpenCompute/ROCm/blob/develop/CHANGELOG.md#softhang-with-hipstreamwithcumask-test-on-amd-instinct) I notice that configuring the stream CU mask incorrectly will cause soft hangs in HIP. I'm using 6900xt (`gfx1030`) right now. IIUSC, it composes 4 SEs, then each SE has 2 SAs (shader array) and each SA has 5 CUs, thus totally 40 CUs (returned by the device property `prop.multiProcessorCount`).

The change log says two CUs making up one WGP must be activated at the same time, so I'm wondering now how can I tell whether two CUs belong to one WGP? How this reveals in its 40bit-wide CU masking array?

---

## 评论 (6 条)

### 评论 #1 — langyuxf (2023-04-25T23:44:03Z)

See https://github.com/RadeonOpenCompute/ROCR-Runtime/blob/master/src/inc/hsa_ext_amd.h#L871

---

### 评论 #2 — xuantengh (2023-04-26T02:11:12Z)

> See https://github.com/RadeonOpenCompute/ROCR-Runtime/blob/master/src/inc/hsa_ext_amd.h#L871

Thanks a lot! There is another question: the 6900XT seems to have 80 CUs, but why HIP returns only 40 from the device property query (i.e., `prop.multiProcessorCount`)?

---

### 评论 #3 — langyuxf (2023-04-27T02:25:56Z)

multiProcessorCount means WGP count for RDNA GPU, 1 WGP = 2 CUs.

---

### 评论 #4 — xuantengh (2023-04-27T05:22:16Z)

> multiProcessorCount means WGP count for RDNA GPU, 1 WGP = 2 CUs.

So there should be 80-bit wide for the CU mask array passed to the [stream masking API](https://docs.amd.com/bundle/4.5-HIP-API/page/group___stream.html#gad61df06555ebdfa30784b3233ca5e13f)?

---

### 评论 #5 — langyuxf (2023-04-27T07:38:11Z)

> > multiProcessorCount means WGP count for RDNA GPU, 1 WGP = 2 CUs.
> 
> So there should be 80-bit wide for the CU mask array passed to the [stream masking API](https://docs.amd.com/bundle/4.5-HIP-API/page/group___stream.html#gad61df06555ebdfa30784b3233ca5e13f)?

Yes.

---

### 评论 #6 — xuantengh (2023-04-27T08:43:00Z)

Thanks a lot. And I hope the details should be reflected on the official docs.

---
