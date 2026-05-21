# Difference between hip_bfloat16 and __hip_bfloat16?

> **Issue #2534**
> **状态**: closed
> **创建时间**: 2023-10-09T00:42:40Z
> **更新时间**: 2024-11-14T19:14:11Z
> **关闭时间**: 2024-11-14T19:14:11Z
> **作者**: pcmoritz
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2534

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I'm using ROCm 5.7. Currently there are two datatypes for `bfloat16` -- `hip_bfloat16` and `__hip_bfloat16`. They seem to be defined respectively as

```
struct __hip_bfloat16 {
  unsigned short data;
};
```
(in `/opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_bf16.h`) and

```
struct hip_bfloat16
{
    __hip_uint16_t data;
   // ...
};
```
(in `/opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_bfloat16.h`).

Unfortunately there doesn't seem to be an out-of-the box way to convert between them. Some of the HIP operations expect `hip_bfloat16` and others expect `__hip_bfloat16`.

Would it be possible to either define an automatic conversion between them, or get rid of one of them? Also if there is any guidance on how to convert between them manually in the mean time, that would be helpful (I'm trying to do it by just creating the respective struct and assigning the `data` field). I didn't find more details about it in the docs :)

Your help is very much appreciated.

---

## 评论 (14 条)

### 评论 #1 — b-sumner (2023-10-09T01:08:28Z)

@pcmoritz hip_bfloat16.h appeared before cuda_bf16.h and contains what was needed at the time.  hip_bf16.h is meant to match cuda_bf16.h, and is probably the header of choice at this point.  hip_bfloat16.h will remain for any developers that adopted it before hip_bf16.h appeared.

---

### 评论 #2 — pcmoritz (2023-10-09T01:33:48Z)

Thanks a lot for the clarification! If you add this info to https://rocm.docs.amd.com/projects/HIP/en/latest/reference/math_api.html or https://rocm.docs.amd.com/projects/HIP/en/latest/reference/terms.html or add a section about bfloat16 to the docs, I think that would be very helpful for others.

---

### 评论 #3 — b-sumner (2023-10-09T14:00:25Z)

Thanks, I've forwarded your comments.

---

### 评论 #4 — pcmoritz (2023-10-10T19:22:20Z)

Thanks a lot -- btw, the reason why I was running into this is because currently `__hip_bfloat16` doesn't support the `+` operator. Maybe fixing that would be the highest ROI, see https://github.com/vllm-project/vllm/pull/1313/files#diff-de16383df6eb2fb3faca61a12fa02cc572ce5cdaf84bd4856d2408ee9b4b3211R113 :)

---

### 评论 #5 — b-sumner (2023-10-10T19:55:09Z)

@pcmoritz hip_bf16.h is meant to simplify the porting of an application that include cuda_bf16.h.  The latter does not provide operators and nor does the former.  These headers instead provide functions like __hadd() which can be used if needed to implement operators.

---

### 评论 #6 — pcmoritz (2023-10-10T20:46:14Z)

Thanks @b-sumner -- as the diff I posted above shows, the cuda data type does support `+`, so for convenience of porting it would be valuable if HIP supported that as well I think :)

---

### 评论 #7 — b-sumner (2023-10-10T20:52:13Z)

@pcmoritz I don't know where that operator is coming from.  https://docs.nvidia.com/cuda/cuda-math-api/group__CUDA__MATH____BFLOAT16__FUNCTIONS.html certainly doesn't mention any operators.

---

### 评论 #8 — b-sumner (2023-10-10T20:59:56Z)

Sorry, I now see them in section 1.3.2.

---

### 评论 #9 — pcmoritz (2023-12-18T04:03:03Z)

Since others also seem to be running into this, is there any chance you are willing to fix it? That would be appreciated :)

---

### 评论 #10 — JLT032 (2024-01-02T20:21:44Z)

with the near zero level of projects endorsing rocm and almost uniquely working with cuda, evading HIP, is this ever going to happen ?

truely perplexed both cuda and rocm are very much hardware specific and highly anti-compatible 
it seems the Radeon VII is mostly useless for anything else than hashcat, at least for now

---

### 评论 #11 — zichguan-amd (2024-10-15T19:39:33Z)

Hi @pcmoritz, you can now directly convert between the two data types in the latest ROCm release.

---

### 评论 #12 — ZJLi2013 (2024-10-21T03:29:12Z)

> Hi @pcmoritz, you can now directly convert between the two data types in the latest ROCm release.

btw, can you provide the public image link for latest rocm build ?

a further question, what's the replacement for `__nv_bfloat16` in rocm,  still `hip_bfloat16` ? 

---

### 评论 #13 — ZJLi2013 (2024-10-21T07:52:13Z)

another thing, if need `__float2bfloat16()`,  `__hip_bfloat16` has built-in apis, while `hip_bfloat16` doesn't

---

### 评论 #14 — zichguan-amd (2024-10-21T13:42:32Z)

> btw, can you provide the public image link for latest rocm build ?

You can find the public images here: https://hub.docker.com/r/rocm/rocm-terminal. 6.2.2 release is on the way.
> a further question, what's the replacement for `__nv_bfloat16` in rocm, still `hip_bfloat16` ?

It's `__hip_bfloat16`. See [this line](https://github.com/ROCm/hipother/blob/e22853eb4d89460682ea89a091e43b315f957a4e/hipnv/include/hip/nvidia_detail/nvidia_hip_bf16.h#L36).

> another thing, if need `__float2bfloat16()`, `__hip_bfloat16` has built-in apis, while `hip_bfloat16` doesn't

See previous comment about the difference between the two:

> @pcmoritz hip_bfloat16.h appeared before cuda_bf16.h and contains what was needed at the time. hip_bf16.h is meant to match cuda_bf16.h, and is probably the header of choice at this point. hip_bfloat16.h will remain for any developers that adopted it before hip_bf16.h appeared.



---
