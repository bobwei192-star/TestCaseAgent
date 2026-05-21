# [Issue]: Extraneous spaces in some varaible names in hip runtime include files causing compiler faults

> **Issue #3221**
> **状态**: closed
> **创建时间**: 2024-06-03T21:01:51Z
> **更新时间**: 2024-08-26T15:21:28Z
> **关闭时间**: 2024-08-26T15:21:28Z
> **作者**: mcordery
> **标签**: AMD Instinct MI300X, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3221

## 标签

- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I'm currently trying to port an NVIDIA code to ROCM/HIP using amdclang++
While compiling I've noticed that I'm getting some errors caused by extra space in some hip runtime include files, specifically 
Currently using amdclang++ 17.0.0

_In amd_hip_runtime_pt_api.h_
In file included from /opt/rocm-6.1.0/include/hip/hip_runtime_api.h:8915:
/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_runtime_pt_api.h:94:48: error: expected ')'
   94 |                                  size_t **offset __dparm(**0),
      |                                                ^
/


_In hip_runtime_api.h_
DEPRECATED(DEPRECATED_MSG)
hipError_t hipBindTexture(
    size_t* offset,
    const textureReference* tex,
    const void* devPtr,
    const hipChannelFormatDesc* desc,
    size_t **size __dparm(**UINT_MAX));

You'll note that there are variable names here, offset_dparm and size_dparm, that have an extraneous space in the middle of the variable name and this is causing compiler faults. I've grepped through these files for other examples and have noticed a couple of more.I am a new employee and am working on a home computer that does not currently have an AMD gpu in it but that's of little matter as I'm just trying to do a lot of porting now.

### Operating System

Ubuntu 20.04.6 LTS 

### CPU

Intel Core i7-6700K

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIPCC

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — b-sumner (2024-06-03T21:55:04Z)

Please see the definition of __dparm(X) in hip_runtime_api.h

---

### 评论 #2 — harkgill-amd (2024-08-23T17:18:47Z)

Hi @mcordery, the `__dparm(x)` macro is defined as follows 
```
#ifdef __cplusplus
  #define __dparm(x) \
          = x
#else
  #define __dparm(x)
  ```
From my understanding, It is used to set a default parameter value in C++ and is not part of a variable name. For example in C++,  `size_t offset __dparm(0)` would evaluate to `size_t offset = 0`. 

Are you still experiencing this issue porting your NVIDIA code with ROCm 6.2.0? If so could you provide more details about the errors you are experiencing and potentially the steps to reproduce your issue? 


---

### 评论 #3 — mcordery (2024-08-26T15:13:03Z)

[AMD Official Use Only - AMD Internal Distribution Only]

This is the error I was seeing before in 6.1. I don’t believe we’re seeing this at this point.

In amd_hip_runtime_pt_api.h
In file included from /opt/rocm-6.1.0/include/hip/hip_runtime_api.h:8915:
/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_runtime_pt_api.h:94:48: error: expected ')'
   94 |                                  size_t offset __dparm(0),
      |                                                ^
/


In hip_runtime_api.h
DEPRECATED(DEPRECATED_MSG)
hipError_t hipBindTexture(
    size_t* offset,
    const textureReference* tex,
    const void* devPtr,
    const hipChannelFormatDesc* desc,
    size_t size __dparm(UINT_MAX));


Matthew J Cordery, PhD
Principal Member of Technical Staff
AI Group

From: harkgill-amd ***@***.***>
Sent: Friday, August 23, 2024 11:19 AM
To: ROCm/ROCm ***@***.***>
Cc: Cordery, Matthew ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: Extraneous spaces in some varaible names in hip runtime include files causing compiler faults (Issue #3221)

Caution: This message originated from an External Source. Use proper caution when opening attachments, clicking links, or responding.


Hi @mcordery<https://github.com/mcordery>, the __dparm(x) macro is defined as follows

#ifdef __cplusplus

  #define __dparm(x) \

          = x

#else

  #define __dparm(x)

From my understanding, It is used to set a default parameter value in C++ and is not part of a variable name. For example in C++, size_t offset __dparm(0) would evaluate to size_t offset = 0.

Are you still experiencing this issue porting your NVIDIA code with ROCm 6.2.0? If so could you provide more details about the errors you are experiencing and potentially the steps to reproduce your issue?

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/3221#issuecomment-2307500383>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/AEJ5XWL7E6FMLGBEZGE7FN3ZS5VI3AVCNFSM6AAAAABIXHWLOKVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMBXGUYDAMZYGM>.
You are receiving this because you were mentioned.Message ID: ***@***.******@***.***>>


---

### 评论 #4 — harkgill-amd (2024-08-26T15:21:28Z)

Great, in that case I'll close out this ticket. 

If you do encounter the issue again, feel free to open a new ticket or comment here and I will re-open this one. Thanks!

---
