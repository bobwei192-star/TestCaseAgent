# [Issue]: hipMemcpy hangs on second calls on 5700G

> **Issue #2781**
> **状态**: closed
> **创建时间**: 2024-01-07T12:53:00Z
> **更新时间**: 2024-04-21T13:18:34Z
> **关闭时间**: 2024-04-21T13:18:34Z
> **作者**: taweili
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2781

## 负责人

- benrichard-amd

## 描述

### Problem Description

```
OS:
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
CPU: 
model name	: AMD Ryzen 7 5700G with Radeon Graphics
GPU:
  Name:                    AMD Ryzen 7 5700G with Radeon Graphics
  Marketing Name:          AMD Ryzen 7 5700G with Radeon Graphics
  Name:                    gfx90c                             
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx90c:xnack-   
```
Compile the following program with hipcc and `HSA_OVERRIDE_GFX_VERSION=9.0.0`
```
OS:
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
CPU: 
model name	: AMD Ryzen 7 5700G with Radeon Graphics
GPU:
  Name:                    AMD Ryzen 7 5700G with Radeon Graphics
  Marketing Name:          AMD Ryzen 7 5700G with Radeon Graphics
  Name:                    gfx900                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx900:xnack-   
```
The allocations work and the first hipMemcpy works but hangs at second call to copy y. 
```c++
#include <hip/hip_runtime.h>
#include <stdio.h>

#define HIP_SAFECALL(x) { \
  hipError_t status = x; \
  if (status != hipSuccess) { \
    printf("HIP Error: %s\n", hipGetErrorString(status)); \
  } \
}

int main(void) {
    const int n = 10000;
    float x[n], y[n];
    float *x_, *y_;

    for (int i = 0; i < n; i++) {
        x[i] = y[i] = 1.0f;
    }

    HIP_SAFECALL(hipMalloc((void **)&x_, sizeof(float) * n));
    printf("x_ allocated\n");
    HIP_SAFECALL(hipMalloc((void **)&y_, sizeof(float) * n));
    printf("y_ allocated\n");
    HIP_SAFECALL(hipMemcpy(x_, x, sizeof(float) * n, hipMemcpyHostToDevice));
    printf("x_ copied\n");
    HIP_SAFECALL(hipMemcpy(y_, y, sizeof(float) * n, hipMemcpyHostToDevice));
    printf("y_ copied\n");

    return 0;
}
```

### Operating System

Ubuntu 22.04

### CPU

AMD Ryzen 7 5700G with Radeon Graphics

### GPU

Other

### Other

_No response_

### ROCm Version

ROCm 6.0.0

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — taweili (2024-01-08T01:29:40Z)

Changing to [hipHostMalloc](https://rocm.docs.amd.com/projects/HIP/en/latest/user_guide/programming_manual.html) solves the hanging problem. 

```c++
#include <hip/hip_runtime.h>
#include <stdio.h>

#define HIP_SAFECALL(x) { \
  hipError_t status = x; \
  if (status != hipSuccess) { \
    printf("HIP Error: %s\n", hipGetErrorString(status)); \
  } \
}

int main(void) {
    const int n = 100000;
    float x[n], y[n];
    float *x_, *y_;

    for (int i = 0; i < n; i++) {
        x[i] = y[i] = 1.0f;
    }

    HIP_SAFECALL(hipHostMalloc((void **)&x_, sizeof(float) * n));
    printf("x_ allocated\n");
    HIP_SAFECALL(hipHostMalloc((void **)&y_, sizeof(float) * n));
    printf("y_ allocated\n");
    HIP_SAFECALL(hipMemcpy(x_, x, sizeof(float) * n, hipMemcpyHostToDevice));
    printf("x_ copied\n");
    HIP_SAFECALL(hipMemcpy(y_, y, sizeof(float) * n, hipMemcpyHostToDevice));
    printf("y_ copied\n");

    return 0;
}
```

---

### 评论 #2 — jin-eld (2024-02-27T01:25:04Z)

@taweili I think the issue might be exactly what I have been trying to debug here https://github.com/ROCm/ROCm/issues/2715 If you need a solution "now" try downgrading to ROCm 5.7.1, I was not able to reproduce the issue there.

I am not sure, that your solution with `hipHostMalloc` is a real replacement though, I am not an expert with HIP, but as far as I understand hipHostMalloc allows the GPU to access host memory which is not the same as allocating memory on the GPU itself? While the code does not hang anymore, it unfortunately does not really solve the general problem, since most applications still use `hipMalloc` and will hang.

@benrichard-amd if there is anything I can do to help speed up a fix or support the investigation - please let me know. So far I have been poking around blindly as I am unfamiliar with the ROCm codebase, I was able to narrow it down to be an issue which was introduced with ROCm 6.0.0, but I am not sure what to look for.

As far as I can tell `rocr::core::InterruptSignal::WaitRelaxed` gets stuck in the `while (true)` loop expecting the `value` which is read out by `value = atomic::Load(&signal_.value, std::memory_order_relaxed);` and which stays a `1` to become lesser than `1`, which never happens:

```
#0  0x00007f0af685c969 in rocr::core::InterruptSignal::WaitRelaxed (
    this=0x1badc40, condition=HSA_SIGNAL_CONDITION_LT, compare_value=1,
    timeout=<optimized out>, wait_hint=HSA_WAIT_STATE_ACTIVE)
    at /usr/include/c++/14/bits/chrono.h:573
```

So far I was not able to figure out who is supposed to set it. The second thread seems to land in a ioctl:
```
#0  __GI___ioctl (fd=fd@entry=3, request=request@entry=3222817548)
    at ../sysdeps/unix/sysv/linux/ioctl.c:36
#1  0x00007f0af7a9e400 in kmtIoctl (fd=3, request=request@entry=3222817548,
    arg=arg@entry=0x7f0aeadff8c0)
    at /usr/src/debug/hsakmt-1.0.6-38.rocm6.0.0.fc40.x86_64/src/libhsakmt.c:13
#2  0x00007f0af7a9f7db in hsaKmtWaitOnMultipleEvents_Ext (
    event_age=0x7f0aeadff970, Milliseconds=4294967294,
    WaitOnAll=<optimized out>, NumEvents=4, Events=0x7f0aeadffa20)
    at /usr/src/debug/hsakmt-1.0.6-38.rocm6.0.0.fc40.x86_64/src/events.c:409
```

If I managed to decode the ioctl request `3222817548 (0xc0184b0c)` correctly, then it should be `AMDKFD_IOC_MAP_MEMORY_TO_GPU` which I guess makes sense, but I was not able to put the puzzle together yet. So if you need more traces, testing or running some more code or have any hints on what to look for - I'd be happy to help.

---

### 评论 #3 — jin-eld (2024-03-02T23:21:54Z)

I think I finally got somewhere, just not as I expected. After various debugging attempts I stumbled upon a similar issue https://github.com/ROCm/ROCm/issues/2418 related to `hipMemcpy` which among other things suggested to use `export HSA_ENABLE_SDMA=0`

This indeed solved the problem for me, now my test application runs through as it should.

---

### 评论 #4 — taweili (2024-03-03T12:15:55Z)

> I think I finally got somewhere, just not as I expected. After various debugging attempts I stumbled upon a similar issue #2418 related to `hipMemcpy` which among other things suggested to use `export HSA_ENABLE_SDMA=0`
> 
> This indeed solved the problem for me, now my test application runs through as it should.

Thanks for the suggestion. I will give it a try and report back this week. 

---

### 评论 #5 — benrichard-amd (2024-03-15T16:10:39Z)

Hi @taweili, @jin-eld,

Thank you for providing code and logs. This should be fixed in the upcoming ROCm 6.1 release.


---

### 评论 #6 — nartmada (2024-04-17T03:59:28Z)

@taweili, please re-test with ROCm 6.1.0.  Thanks.

---

### 评论 #7 — nartmada (2024-04-21T13:18:34Z)

Closing the ticket.  @taweili, please re-open if you still see the issue with ROCm 6.1.0.  Thanks.

---
