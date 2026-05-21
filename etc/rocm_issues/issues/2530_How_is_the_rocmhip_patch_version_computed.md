# How is the rocm/hip patch version computed?

> **Issue #2530**
> **状态**: closed
> **创建时间**: 2023-10-06T14:37:28Z
> **更新时间**: 2024-04-07T21:45:01Z
> **关闭时间**: 2024-04-07T21:45:01Z
> **作者**: jczhang07
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2530

## 描述

By hip version, I mean 5.4.6, 5.5.2, 5.6.0, 5.6.1 etc.  In `/opt/rocm-5.6.0/include/hip/hip_version.h`, I see

```
      #define HIP_VERSION_MAJOR 5
      #define HIP_VERSION_MINOR 6
      #define HIP_VERSION_PATCH 31061
      #define HIP_VERSION    (HIP_VERSION_MAJOR * 10000000 + HIP_VERSION_MINOR * 100000 + HIP_VERSION_PATCH)
```

But how is the `HIP_VERSION_PATCH` mapped to the `z` in `rocm-x.y.z`?



---

## 评论 (1 条)

### 评论 #1 — nartmada (2024-04-07T21:45:01Z)

@jczhang07, apologies for the lack of response.

![image](https://github.com/ROCm/ROCm/assets/144284448/bbe17b6b-8d69-4611-aba2-6e3e3a851d51)
![image](https://github.com/ROCm/ROCm/assets/144284448/7dc1b541-fc4d-4418-a29f-b0f7df99b975)

Please reopen if I have not answered your question.  Thanks.

---
