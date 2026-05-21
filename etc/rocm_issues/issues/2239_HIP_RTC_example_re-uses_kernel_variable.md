# HIP RTC example re-uses "kernel" variable

> **Issue #2239**
> **状态**: closed
> **创建时间**: 2023-06-13T18:28:50Z
> **更新时间**: 2024-12-10T20:16:47Z
> **关闭时间**: 2024-12-10T20:16:46Z
> **作者**: skyreflectedinmirrors
> **标签**: Under Investigation, Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2239

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Documentation** (颜色: #5319e7)

## 描述

![image](https://github.com/RadeonOpenCompute/ROCm/assets/6463881/c7133e51-5471-4ab1-ba5c-a48c6df0e6d5)
![image](https://github.com/RadeonOpenCompute/ROCm/assets/6463881/703bbc08-3215-4a32-b8a8-d1fdb2ce2e4a)

I.e., if you're copy-pasting the examples, you'll get a duplicate variable name.

---

## 评论 (12 条)

### 评论 #1 — saadrahim (2023-06-13T18:30:30Z)

Can you link to the code or page?

---

### 评论 #2 — skyreflectedinmirrors (2023-06-13T18:31:03Z)

https://rocm.docs.amd.com/projects/HIP/en/latest/user_guide/hip_rtc.html#example

---

### 评论 #3 — skyreflectedinmirrors (2023-06-13T18:38:26Z)

Honestly, I think a fully worked example, or linking to:

>Please have a look at saxpy.cpp and hiprtcGetLoweredName.cpp files for a detailed example.

would be helpful here (I can't seem to find those anymore)

---

### 评论 #4 — nartmada (2024-02-25T04:37:07Z)

Hi @skyreflectedinmirrors, do you still need help with this ticket?  Thanks.

---

### 评论 #5 — skyreflectedinmirrors (2024-02-26T14:48:07Z)

The same code is still present in the documentation, so yes the issue is still there.

See my comment here: https://github.com/ROCm/ROCm/issues/2239#issuecomment-1589838618

---

### 评论 #6 — nartmada (2024-02-26T15:11:01Z)

@skyreflectedinmirrors, thank you for getting back.  Let me find someone to take a look.

---

### 评论 #7 — nartmada (2024-02-26T21:41:17Z)

An internal ticket has been created for investigation.

---

### 评论 #8 — harkgill-amd (2024-07-12T15:06:50Z)

Hi @skyreflectedinmirrors, the HIP RTC example has been updated to no longer have duplicate variable names. You can find the updated documentation at [Programming for HIP Runtime Compiler (RTC)](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_rtc.html). 

Please close the ticket if the issue has been addressed, thanks!

---

### 评论 #9 — skyreflectedinmirrors (2024-07-12T15:12:28Z)

Looks pretty good, I think there's one remaining issue:

```
hiprtcCreateProgram(&prog,                 // HIPRTC program
                    kernel,                // kernel string
                    "gpu_kernel.cu",       // Name of the file
                    num_headers,           // Number of headers
                    &header_sources[0],    // Header sources
                    &header_names[0]);     // Name of header files
```

Basically, this still uses "kernel" instead of "kernel_source"

---

### 评论 #10 — harkgill-amd (2024-07-12T15:23:12Z)

Noted, I will look into this and get back to you.

---

### 评论 #11 — harkgill-amd (2024-12-10T19:02:05Z)

Hi @skyreflectedinmirrors, the section with the call to `hiprtcCreateProgram` has been corrected to follow the `vector_add.cpp` example with `kernel_source`. 
```
hiprtcCreateProgram(&prog,                 // HIPRTC program handle
                    kernel_source,         // HIP kernel source string
                    "vector_add.cpp",      // Name of the HIP program, can be null or an empty string
                    0,                     // Number of headers
                    NULL,                  // Header sources
                    NULL);                 // Name of header files
```
Please take a look at the updated documentation [here ](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_rtc.html#compilation-apis) and confirm if everything looks good.

---

### 评论 #12 — skyreflectedinmirrors (2024-12-10T20:05:59Z)

LGTM, thanks!

---
