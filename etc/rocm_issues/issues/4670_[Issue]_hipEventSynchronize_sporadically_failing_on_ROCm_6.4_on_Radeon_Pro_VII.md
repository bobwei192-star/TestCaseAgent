# [Issue]: hipEventSynchronize sporadically failing on ROCm 6.4 on Radeon Pro VII

> **Issue #4670**
> **状态**: closed
> **创建时间**: 2025-04-23T11:59:59Z
> **更新时间**: 2025-04-28T19:15:08Z
> **关闭时间**: 2025-04-25T06:28:23Z
> **作者**: maartenarnst
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4670

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

We see `hipEventSynchronize` sporadically fail on ROCm 6.4 on **Radeon Pro VII**.

The failures arise in the CICD pipelines of our HPC code that we build on top of `Kokkos` with the `HIP` backend.

The failures are sporadic, but frequent enough to impact our work significantly. The error message looks like:
```bash
terminate called after throwing an instance of 'std::runtime_error'
  what():  hip_instance->hip_event_synchronize_wrapper( HIPInternal::constantMemReusable[hip_device]) error( hipErrorCapturedEvent): operation not permitted on an event last recorded in a capturing stream /opt/kokkos/include/HIP/Kokkos_HIP_KernelLaunch.hpp:525
Aborted (core dumped)
```

The error message is a bit surprising, because neither in our HPC code, neither in `Kokkos`, there is a graph capture. We raised the issue on the `Kokkos` repository:

- https://github.com/kokkos/kokkos/issues/8006

We posted a self-contained reproducer in a Dockerfile in that issue.

One particularity of the context in which the issue arises is that the "event record" and the "event synchronize" might be far apart. It can even happen that our code calls `eventSynchronize` on an event that was recorded into a stream when that stream may actually have been destroyed in the mean time.

We see the issue on Radeon PRO VII. We did limited testing on MI300A, where we didn't see the issue. We didn't test other architectures.

We are aware that Radeon PRO VII has been deprecated for a while in ROCm. But we did see Radeon PRO VII in AMD's recent "Developers, Developers, Developers" video for the community. So also tagging @powderluv in the hope that this apparent bug with the HIP event management API on (at least) Radeon PRO VII can be looked into and solved. Radeon PRO VII is (currently) the last prosumer GPU with great FP64 support. Thanks in any case.

@Rombur @romintomasetti




### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen 5950X

### GPU

AMD Radeon PRO VII

### ROCm Version

Rocm 6.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — ppanchad-amd (2025-04-23T14:00:33Z)

Hi @maartenarnst. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-04-23T19:41:39Z)

@maartenarnst, thanks for reaching out, and I am sorry that you are experiencing this bug. 

>One particularity of the context in which the issue arises is that the "event record" and the "event synchronize" might be far apart. It can even happen that our code calls eventSynchronize on an event that was recorded into a stream when that stream may actually have been destroyed in the mean time.

This is really suspicious. As you mentioned in your other post, calling eventSynchronize on an event that might have its associated stream already destroyed can lead to undefined behavior, which could result in the error message you are seeing. 

This explanation is especially likely since the error message your are getting is `hipErrorCapturedEvent`. As we can see from the source code here

https://github.com/ROCm/clr/blob/64d6f5714a1d4b3c792b5d734e31c935257af435/hipamd/src/hip_event.cpp#L462-L466

`hipEventSynchronize` will return this error when it finds the stream associated with the event is no longer active. 

I am not really sure why only Radeon VII Pro experiences this, but my guess is that it probably has something to do with the more limited hardware specs causing streams being created and destroyed more frequently under kokkos' constant memory mechanism, which increases the odds of this happening. 

I think trying to synchronize an event without knowing if the underlying stream is already destroyed falls dangerously close to the programming error category. Is there any reason/constraints preventing you from checking the stream status prior to calling the command? 


---

### 评论 #3 — maartenarnst (2025-04-24T10:13:13Z)

Hi @tcgu-amd. Thank you for your response.

It appears we are looking at a sequence of API calls like:

```
#include <iostream>

#include "hip/hip_runtime.h"

#define HIP_SAFE_CALL(x) (h((x), __FILE__, __LINE__))

inline void h(hipError_t err, const char *file, int line)
{
    if (err != hipSuccess)
    {
        std::cerr << file << ":" << line << " error " << hipGetErrorString(err) << "\n";
        exit(1);
    }

}

int main () {
    // Create a stream.
    hipStream_t stream;
    HIP_SAFE_CALL(hipStreamCreate(&stream));
    
    // Create an event and record it into the stream.
    hipEvent_t event;
    HIP_SAFE_CALL(hipEventCreate(&event));
    HIP_SAFE_CALL(hipEventRecord(event, stream));

    // Destroy the stream.
    HIP_SAFE_CALL(hipStreamDestroy(stream));

    // **After destroying the stream**, synchronize the event that we had recorded into that stream.
    HIP_SAFE_CALL(hipEventSynchronize(event));

    // Destroy the event.
    HIP_SAFE_CALL(hipEventDestroy(event));
}
```

On our system, this code compiles and runs without error. But it appears the question is whether that is actually the appropriate behavior of this code.

What is supposed to happen on the line `HIP_SAFE_CALL(hipEventSynchronize(event));` in question?

- Is it, as you say, a programming error? In other words, is it illegal to call `hipEventSynchronize` on an `event` after destroying the `stream` in which that `event` had been recorded? If so, that would point to the problem being in the Kokkos code and we should fix it there on their side. 

- Or, is this line of code actually fine? In other words, is it actually legal to call `hipEventSynchronize` on an `event` after destroying the `stream` in which that `event` had been recorded? And so, should the `hip` `clr` implementation of `hipEventSynchronize` be revised to ensure that a meaningful result is returned, even when the stream stored in the event is no longer valid? We noticed that other `hip` `clr` implementations of event management functions proceed in such a way by calling `hip::isValid` before checking or manipulating the stream that they store, e.g.:

https://github.com/ROCm/clr/blob/64d6f5714a1d4b3c792b5d734e31c935257af435/hipamd/src/hip_event.cpp#L358C7-L362
 
and so it may also be the case that we're dealing with a bug in the `hip` `clr` implementation of `hipEventSynchronize`.


Would you have a moment to clarify whether or not the `hipEventSynchronize` call in the snippet is legal? It appears clarifying this point will be necessary to see how we should proceed to solve the issue. If you see any issues with this analysis, do not hesitate to suggest. Many thanks in advance!


---

### 评论 #4 — tcgu-amd (2025-04-24T14:58:27Z)

@maartenarnst I believe the `hipEventSynchronize` call in the snippet should be considered illegal in this scenario. Events are fundamentally linked to the stream they were recorded on, so attempting to synchronize using an event whose stream has been invalidated doesn't align with the operation's intent.

From an API design perspective, when `hipEventSynchronize` is called, the API implicitly assumes the user is working with a valid stream. If this expectation is violated (i.e., the stream is invalid), the API should return an error. This would correctly signal a likely bug or misuse in the calling code.

The situation with `hipEventDestroy` is different. An event can reasonably be destroyed whether its underlying stream is valid or invalid. If the stream is active at the time of destruction, the implementation needs to remove the event from the stream's tracking, which corresponds to the lines of code you linked:
https://github.com/ROCm/clr/blob/64d6f5714a1d4b3c792b5d734e31c935257af435/hipamd/src/hip_event.cpp#L358C7-L362.

Hope this helps.

Thanks! 

---

### 评论 #5 — maartenarnst (2025-04-24T15:16:16Z)

Hi @tcgu-amd. OK! Thanks a lot. This clarifies things indeed. We'll follow up on the Kokkos side to so see how to fix it there.

Just a note though. We agree that given that the call is illegal, the api should return an error. But, we feel that the returned error code is a bit surprising. Currently, the returned error code relates to "stream capture", hence it is related to the hip graph, even though we're nowhere using a hip graph or a capture. It seems it would be more relevant for the error code to be `hipErrorContextIsDestroyed`. Do you think we should open an issue in the `clr` repository?  

---

### 评论 #6 — tcgu-amd (2025-04-24T15:35:43Z)

> Hi [@tcgu-amd](https://github.com/tcgu-amd). OK! Thanks a lot. This clarifies things indeed. We'll follow up on the Kokkos side to so see how to fix it there.
> 
> Just a note though. We agree that given that the call is illegal, the api should return an error. But, we feel that the returned error code is a bit surprising. Currently, the returned error code relates to "stream capture", hence it is related to the hip graph, even though we're nowhere using a hip graph or a capture. It seems it would be more relevant for the error code to be `hipErrorContextIsDestroyed`. Do you think we should open an issue in the `clr` repository?

Yes this is a valid concern indeed. I agree the error returned is not appropriate. Please open an issue on clr so the engineers can start working on addressing that.

Meanwhile, do you mind closing this issue for now? 

Thanks! 

---

### 评论 #7 — tcgu-amd (2025-04-28T19:15:06Z)

@maartenarnst, after some further investigation, seems like the error message was correct but it shouldn't have been displayed. This is due to an oversight/error in clr. A fix has already been made and is live in ROCm 6.4+. For more details please see https://github.com/ROCm/clr/issues/157. Thanks! 

---
