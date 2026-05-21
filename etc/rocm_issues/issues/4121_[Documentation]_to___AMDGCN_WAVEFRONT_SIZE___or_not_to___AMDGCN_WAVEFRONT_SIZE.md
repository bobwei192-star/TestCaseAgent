# [Documentation]: to __AMDGCN_WAVEFRONT_SIZE__ or not to __AMDGCN_WAVEFRONT_SIZE__

> **Issue #4121**
> **状态**: closed
> **创建时间**: 2024-12-06T15:02:40Z
> **更新时间**: 2026-01-29T15:33:01Z
> **关闭时间**: 2026-01-29T15:33:01Z
> **作者**: dot-asm
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/4121

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Description of errors

[ROCm release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html#amdgpu-wavefront-size-compiler-macro-deprecation) declare `__AMDGCN_WAVEFRONT_SIZE__` deprecated and refer to [clang documentation](https://rocm.docs.amd.com/projects/llvm-project/en/docs-6.3.0/LLVM/clang/html/AMDGPUSupport.html) for **more** information. The issue is that the said additional information contradicts the release notes, because it states that it's `__AMDGCN_WAVEFRONT_SIZE` that is supposed to be deprecated, leaving developers uncertain about how to future-proof their code. Please resolve the contradiction.


### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (36 条)

### 评论 #1 — harkgill-amd (2024-12-06T20:21:27Z)

Hi @dot-asm, thanks for pointing this discrepancy out. Clarifying this internally and will let you know.

---

### 评论 #2 — harkgill-amd (2024-12-09T15:53:24Z)

@dot-asm, both `__AMDGCN_WAVEFRONT_SIZE__ ` and `__AMDGCN_WAVEFRONT_SIZE` will be deprecated in an upcoming release. The release notes and AMDGPU support page will be updated to reflect this shortly.

---

### 评论 #3 — dot-asm (2024-12-09T16:49:41Z)

Oh! And what will replace them? Or in other words how are we supposed to figure out which wavefront size does compiler generate code for?

---

### 评论 #4 — harkgill-amd (2024-12-11T15:01:24Z)

Users can still determine the wavefront size in device code via the [warpSize variable](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/cpp_language_extensions.html#warpsize) (which however will stop being constexpr when the `__AMDGCN_WAVEFRONT_SIZE__` macro is removed) and via [hipGetDeviceProperties ](https://rocm.docs.amd.com/projects/HIP/en/docs-6.0.0/doxygen/html/structhip_device_prop__t.html#af3357d33c004608bf05bc21a352be81b)in host code. The wavefront size will no longer be available as a compile-time constant.

---

### 评论 #5 — dot-asm (2024-12-11T17:32:31Z)

> warpSize variable ... will stop being constexpr

Really? The wording suggests that it would be a run-time variable, for example be a launch parameter. Is this the suggestion? I fail to believe it. At least internally the compiler has to operate with wavefront size being a compile-time constant. Most notably the type of the scalar registers that are used as carries/borrows and results of comparisons directly depends on wavefront size. With wavefront size of 32 the compiler allocates one scalar register, and with 64 - a pair. With this in mind, how would `if (warpSize == 32) {} else {}` have to be compiled with run-time variable warpSize? With different scalar bitness? Is it even possible? Or is it rather that warpSize will remain compile-time constant, at least internally, and one of the paths will be removed as dead code? At it is now. Well... ~It~ I can imagine a future with warpSize being a run-time variable necessarily **smaller** than a platform-specific maximum carry/condition bitness. Is this it? But even then wouldn't the compiler need to operate with a compile-time constant that would describe the said maximum? In which case why would you insist on hiding it from the application code?


---

### 评论 #6 — dot-asm (2024-12-11T17:51:59Z)

Or maybe it's just a branding problem? I refer to "GCN" in the macro name. Indeed, ROCm has deprecated GPUs with GCN ISA, so why would one keep the reference in the macro name? In which case a replacement name would be appropriate. I mean appreciated. Just in case, it is in fact about the carry/condition type, which has to be determined at compile time, but not on a value of a constexpr variable.

---

### 评论 #7 — harkgill-amd (2024-12-18T21:42:51Z)

The basis of the decision to deprecate `__AMDGCN_WAVEFRONT_SIZE__ ` revolves around the macro being easy to misuse. It was common in the past for users to mistakenly reference the macro in host code where it had no meaningful value as wave size is a built-in property of a target device. To avoid this, the decision was made to deprecate the macro and make access to the wavefront size only possible through well-defined means. 

As for the future implementation of `warpSize`, the only real change will be in the user-facing API. Later stages of the compiler will still be able to generate code that works for the hardware's wavefront size. For more context, you can review some of the discussion that led to these changes over at https://github.com/llvm/llvm-project/pull/109663 and https://github.com/llvm/llvm-project/pull/112849.

---

### 评论 #8 — dot-asm (2024-12-19T17:02:43Z)

> The basis of the decision to deprecate `__AMDGCN_WAVEFRONT_SIZE__ ` revolves around the macro being easy to misuse.

There are an innumerable amount of things to misuse, easier than this one... But what is the problem? Developers make mistakes, figure it out and correct... Why take it out on the macro in question? But on a serious note. Again, I (for one) use this macro to distinguish the **type** of the scalar registers used as result of comparison or carry. As in
```
# if __AMDGCN_WAVEFRONT_SIZE == 64
    using cond_t = uint64_t;
# else
    using cond_t = uint32_t;
# endif
```
This can't be achieved with a variable. What are the options without the macro [in question]?

Well, granted, the macro in question is a mess. It's always 64 on the host side, and on the device side it reflects the defunct `-mwavefrontsize64` option. By "defunct" I mean that you can't pass it when you compile for RDNA, while on CDNA  the wavefront size in question is **the** one and only option, hence specifying it is just redundant. Just in case you sense a contradiction between "reflects" and "can't pass". "Reflects" refers to the fact that you can run `hipcc -dM -E -x hip /dev/null --offload-arch=gfx1100 | grep WAVEFRONT` without and with `-mwavefrontsize64` and note the value changing (on the device side). However, you can't pass it in practice, because real-life code is practically bound to include hip/hip_runtime.h, which will terminate the attempt to target RDNA with `-mwavefrontsize64` with `#error HIP is not supported on the specified GPU ARCH with wavefront size 64`. So it sounds like while you're at it, why not deprecate and remove `-mwavefrontsize64`? But keep the macro, or provide a replacement, on the device side ;-)

---

### 评论 #9 — jameseperry (2024-12-19T17:34:31Z)

> Users can still determine the wavefront size in device code via the [warpSize variable](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/cpp_language_extensions.html#warpsize) (which however will stop being constexpr when the `__AMDGCN_WAVEFRONT_SIZE__` macro is removed) and via [hipGetDeviceProperties ](https://rocm.docs.amd.com/projects/HIP/en/docs-6.0.0/doxygen/html/structhip_device_prop__t.html#af3357d33c004608bf05bc21a352be81b)in host code. The wavefront size will no longer be available as a compile-time constant.

I understand the rationale for deprecating the macro (and I'm not sure I agree), but what is the rationale for making warpSize non-constexpr? That's a functional regression.

---

### 评论 #10 — kliegeois (2025-03-06T16:57:55Z)

@jameseperry this is a late response but there is another way to determine the warp size which is still a constexpr from within device code: https://rocm.docs.amd.com/projects/rocPRIM/en/latest/reference/intrinsics.html#_CPPv4N7rocprim16device_warp_sizeEv .
There is also a way to get the warp size from the host for a specific device https://rocm.docs.amd.com/projects/rocPRIM/en/latest/reference/intrinsics.html#_CPPv4N7rocprim14host_warp_sizeEKiRj .

---

### 评论 #11 — dot-asm (2025-03-06T17:33:19Z)

A library can't do better than the compiler it compiles. The referred rocprim::device_warp_size simply returns the value of __AMDGCN_WAVEFRONT_SIZE macro, as per https://github.com/ROCm/rocPRIM/blob/develop/rocprim/include/rocprim/intrinsics/thread.hpp#L52-L56 and https://github.com/ROCm/rocPRIM/blob/develop/rocprim/include/rocprim/config.hpp#L247-L249. So the original question still stands. In this context it's the following. If the macro in [question] is removed, how would https://github.com/ROCm/rocPRIM/blob/develop/rocprim/include/rocprim/types.hpp#L80-L84 look like?

---

### 评论 #12 — dot-asm (2025-03-06T17:47:35Z)

> https://github.com/ROCm/rocPRIM/blob/develop/rocprim/include/rocprim/config.hpp#L247-L249

Well, granted, there is #ifndef __AMDGCN_WAVEFRONT_SIZE few lines above, but it doesn't really answer the question. If the macro is removed, you'll make the ~rocprim::device_warp_size caller~ rocprim user "believe" that wavefront is 64 on all platforms.

---

### 评论 #13 — dot-asm (2025-03-06T18:15:48Z)

> A library can't do better than the compiler it compiles.

Just in case, while I'm referring to **my** problem, one equivalent to \<rocprim\>/types.hpp, the most recent reply was to a related question about constness of the `warpSize` variable. To take it into this context, if the macro is removed and rocprim switches to non-const warpSize, rocprim::device_warp_size won't compile as constexpr. One can't do better than the compiler :-) You can naturally say "we'll figure out how to maintain constexpr-ness of the interface as suggested compiler modifications hit us." Fair enough, but I reckon everybody would appreciate a self-consistent heads-up depicting a path forward.

---

### 评论 #14 — AlexVlx (2025-03-20T18:55:03Z)

Client components / applications can define their own wave_size macro / variable, based on the architecture identifiers, which remain available: <https://clang.llvm.org/docs/AMDGPUSupport.html>. For the given example of rocPRIM, there's already a `ROCPRIM_NAVI` check, which can drive selection / instantiation: 

```cpp
#ifndef ROCPRIM_WAVEFRONT_SIZE
    #ifdef ROCPRIM_NAVI
      #define ROCPRIM_WAVEFRONT_SIZE 32
    #else
      #define ROCPRIM_WAVEFRONT_SIZE 64
    #endif
#endif
```

It's a boring search & replace at most. It would be preferable to not do this (for the mask type example it would be preferable to have an opaque type which models Integer, rather than hardcode the bit-ness), but that would be more intrusive / potentially disruptive. The lowest effort solution to e.g. your conundrum around <https://github.com/ROCm/rocPRIM/blob/develop/rocprim/include/rocprim/types.hpp#L80-L84>:

```cpp
#ifdef ROCPRIM_NAVI
using lane_mask_type = unsigned int;
#else
using lane_mask_type = unsigned long long int;
#endif
```

---

### 评论 #15 — dot-asm (2025-03-20T20:51:48Z)

> Client components / applications can define their own wave_size macro / variable, based on the architecture identifiers, which remain available: https://clang.llvm.org/docs/AMDGPUSupport.html.

So the circle is complete. The initial question was which macro directly describing the wavefront will remain. Since the documentation as whole contradicts itself. The answer was "**both** will disappear." And now it's "see the documentation," which is the source of the dispute.

As for applications defining their own macro/variable. The stated rationale behind removal of the macros in question was "it's too easy to misuse." Are you suggesting that defining own macro/variable would be  **harder** to misuse?


---

### 评论 #16 — AlexVlx (2025-03-20T22:22:55Z)

> > Client components / applications can define their own wave_size macro / variable, based on the architecture identifiers, which remain available: https://clang.llvm.org/docs/AMDGPUSupport.html.
> 
> So the circle is complete. The initial question was which macro directly describing the wavefront will remain. Since the documentation as whole contradicts itself. The answer was "**both** will disappear." And now it's "see the documentation," which is the source of the dispute.
> 
> As for applications defining their own macro/variable. The stated rationale behind removal of the macros in question was "it's too easy to misuse." Are you suggesting that defining own macro/variable would be **harder** to misuse?

I believe there is a misunderstanding. Yes, both macros will disappear. The suggestion was not "see the documentation", but rather see "the architecture identifiers, which remain available: here's the documentation". This is a somewhat important distinction, I do apologise if my wording was somehow confusing to you.

As to your second question, I am not suggesting anything. I am providing a transition path which does not rely on features that are currently deprecated, and will be removed in a future version. A client application defining a macro has more information about its context and use, and it engages in a localised, conscious, opt-in, rather than grabbing a magically provided symbol. Furthermore, it can attach semantics that fit its use case, can choose mechanisms other than a macro etc. Finally, it would have to knowingly engage in providing this quantity on the host side, where it'd have more control over its compilation setup, and thus could provide a meaningful value, rather than hardcode 64. 

---

### 评论 #17 — IMbackK (2025-03-20T23:29:49Z)

@AlexVlx

I am the hip maintainer of https://github.com/ggml-org/llama.cpp. I would like to make the case that the deprecation of `__AMDGCN_WAVEFRONT_SIZE__` inside device code has bad implications for us. We maintain a piece of compute code that is expected to compile against CUDA / ROCM/HIP and MUSA compute environments.

For performance reasons we must have the wave size as known at compile time in order to unroll various loops, fold various branches and so on. The difference this makes is huge in terms of performance. 
This leaves us with only one option: we have to template the warp size, but this forces us to senselessly compile a kernel for each supported warp size (we must support 32, 64 and 128) for each target architecture. Our compile times are already extremely long, as particularly amdclang is very very slow and our matrix of template parameters for each compute kernel is already quite large. These kernels would then be pointless baggage as no gfx908 device will ever end up with warp size 32 and no RDNA device will ever end up with warp size 128 and yet this change forces us to pointlessly keep a kernel for combination (next to all the combinations for problem sizes we already have) around just in case this where to ever happen. This is __simply unworkable__ and thus the only way forward for us is to guess the warp size based on the target architecture when compiling our kernels.

This will necessarily be a __more brittle, more prone to misuse and more maintenance heavy__ as we will be forced to choose by hand for eatch architecture.

For us there is however no other options, and no amount of refactoring our code or rearchitectureing will ever make this problem go away, it is simply fundamental to the problem at hand.

I understand that clearly the visibly of `__AMDGCN_WAVEFRONT_SIZE__` in host code was wrong and should be fixed, but there is no technical reason that hip could not provide a `constexpr __device__` function that returns the warp size of the target currently being compiled for.
An no amdgcn flavored spirv is not a reason, for this case this function could simply return -1 which would trigger the device code to use a slower path where the warp size is not known at compile time.

---

### 评论 #18 — AlexVlx (2025-03-21T00:01:15Z)

> [@AlexVlx](https://github.com/AlexVlx)
> 
> I am the hip maintainer of https://github.com/ggml-org/llama.cpp. I would like to make the case that the deprecation of `__AMDGCN_WAVEFRONT_SIZE__` inside device code has bad implications for us. We maintain a piece of compute code that is expected to compile against CUDA / ROCM/HIP and MUSA compute environments.
> 
> For performance reasons we must have the wave size as known at compile time in order to unroll various loops, fold various branches and so on. The difference this makes is huge in terms of performance. This leaves us with only one option: we have to template the warp size, but this forces us to senselessly compile a kernel for each supported warp size (we must support 32, 64 and 128) for each target architecture. Our compile times are already extremely long, as particularly amdclang is very very slow and our matrix of template parameters for each compute kernel is already quite large. These kernels would then be pointless baggage as no gfx908 device will ever end up with warp size 32 and no RDNA device will ever end up with warp size 128 and yet this change forces us to pointlessly keep a kernel for combination (next to all the combinations for problem sizes we already have) around just in case this where to ever happen. This is **simply unworkable** and thus the only way forward for us is to guess the warp size based on the target architecture when compiling our kernels.
> 
> This will necessarily be a **more brittle, more prone to misuse and more maintenance heavy** as we will be forced to choose by hand for eatch architecture.
> 
> For us there is however no other options, and no amount of refactoring our code or rearchitectureing will ever make this problem go away, it is simply fundamental to the problem at hand.
> 
> I understand that clearly the visibly of `__AMDGCN_WAVEFRONT_SIZE__` in host code was wrong and should be fixed, but there is no technical reason that hip could not provide a `constexpr __device__` function that returns the warp size of the target currently being compiled for. An no amdgcn flavored spirv is not a reason, for this case this function could simply return -1 which would trigger the device code to use a slower path where the warp size is not known at compile time.

This is useful feedback but, again, I believe that there is some lingering lack of clarith. The architecture identifier macros already unambiguously encode the wave size (the `mwavefrontsize64` option isn't intended for production use, and taking a dependence on it is unsupported, so please do not do that). Note that it is not necessary to check per each individual gfxip, but rather just per family (the `__<GFXN>__` macro). I will also observe that this need not be exhaustive, the option is actually binary, and would make your current implementation <https://github.com/ggml-org/llama.cpp/blob/e04643063b3d240b8c0fdba98677dff6ba346784/ggml/src/ggml-cuda/common.cuh#L254> look like so:

```cpp
static constexpr __device__ int ggml_cuda_get_physical_warp_size() {
#if defined(GGML_USE_HIP) && defined(__HIP_PLATFORM_AMD__) && defined(__GFX9__)
    return 64;
#else
    return 32;
#endif // defined(GGML_USE_HIP) && defined(__HIP_PLATFORM_AMD__)
}
```

This is a one-time change, which can be done today, and will work without needing revisiting in the foreseeable future. I cannot comment on MUSA or how that is connected to this topic. In closing, I will emphasise that I am very grateful for the analysis on alternative designs for HIP, it is extremely appreciated.

---

### 评论 #19 — IMbackK (2025-03-21T00:04:10Z)

Your example already shows why this is a bad idea. We also compile for and run on gfx803 which you just broke. There is also no reason to believe that in the future amd will not release some new device that is not gfx9 but is warp64 (UDNA Maybe?) again we would have to then update this (essentially a table).

Its pointless, the compiler has this information by definition, i should just give it to us. 

---

### 评论 #20 — AlexVlx (2025-03-21T00:21:48Z)

> Your example already shows why this is a bad idea. We also compile for and run on gfx803 which you just broke. There is also no reason to believe that in the future amd will not release some new device that is not gfx9 but is warp64 (UDNA Maybe?) again we would have to then update this (essentially a table).
> 
> Its pointless, the compiler has this information by definition, i should just give it to us.

It is extremely good to hear that you compile and run for gfx803! I had erroneously assumed that it [being unsupported](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html) would've been an issue, however it is great to see that's not a problem. Fortunately, we do expose a family identifier for it as well, which can be incorporated (it might, inconveniently, necessitate a line break, as the predicate itself would be rather long). In what regards future devices, I am not at liberty to speculate beyond observing that this sort of alternance between wave sizes is extremely unlikely. Thank you very much for your continued contributions to this topic!

---

### 评论 #21 — dot-asm (2025-03-21T08:55:48Z)

> the compiler has this information by definition, it should just give it to us.

Exactly.

As for "the `mwavefrontsize64` option isn't intended for production use, and taking a dependence on it is unsupported." Compiler documentation just states that the option is available, and RDNA ISA spec states that "both wave sizes are supported" and tells you to instruct the compiler accordingly. Granted, you figure out that the option is simply defunct soon enough, but nowhere does documentation make the said recommendation. If I missed it, could you please point the location? Anyway, the question also is what does the future hold. Does the statement and current state of affairs mean that a) the option will stay defunct, or b) will become operational? If former, then it wouldn't it be appropriate to remove [along with corresponding paragraph in ISA spec]? And if latter, how would the application know?

---

### 评论 #22 — IMbackK (2025-03-21T09:18:20Z)

> As for "the `mwavefrontsize64` option isn't intended for production use, and taking a dependence on it is unsupported." Compiler documentation just states that the option is available, and RDNA ISA spec states that "both wave sizes are supported" and tells you to instruct the compiler accordingly. Granted, you figure out that the option is simply defunct soon enough, but nowhere does documentation make the said recommendation. If I missed it, could you please point the location? Anyway, the question also is what does the future hold. Does the statement and current state of affairs mean that a) the option will stay defunct, or b) will become operational? If former, then it wouldn't it be appropriate to remove [along with corresponding paragraph in ISA spec]? And if latter, how would the application know?

Not only is it supported by the compiler it is in fact effectively used all the time. Both vulkan and opencl do run rdna in wave64 mode, for radv this is even the default (attmittly llvm is not the default for radv, aco is, but llvm as shader compiler is also supported).

Its only HIP where wave64 mode is not available on RDNA, this is also a limitation that would ideally be lifted as opencl and radv show that for quite some workloads wave64 performs mutch better, esp on rdna3

---

### 评论 #23 — dot-asm (2025-03-21T10:22:46Z)

> Its only HIP where wave64 mode is not available on RDNA,

Oh! I didn't know that, thanks! I apologize for my ignorance, but what is "the compiler" then? Do you mean the clang in question, but without hip/hip_runtime.h? Either way, it sounds like it's not impossible to imagine that it [the mwavefront64 option] won't be removed, in which case the question [to the AMD] is, again, how would application code tell?

---

### 评论 #24 — IMbackK (2025-03-21T14:27:33Z)

> Oh! I didn't know that, thanks! I apologize for my ignorance, but what is "the compiler" then? Do you mean the clang in question, but without hip/hip_runtime.h? Either way, it sounds like it's not impossible to imagine that it [the mwavefront64 option] won't be removed, in which case the question [to the AMD] is, again, how would application code tell?

LLVM is the compiler, clang is just one front end other languages use other front ends. Point is that the machinery behind mwavefrontsize64 is not going anywhere as its widely used, in fact i would say that the vast majority of rdna devices spend the vast majority of their time executeing code in cu mode.

---

### 评论 #25 — al42and (2025-03-31T21:08:23Z)

I'd also like to point out that, when a user implements wave-size detection themselves, they are, with modern hardware, equally likely to do

```cpp
#if defined(__GFX8__) || defined(__GFX9__)
    return 64;
#else
    return 32;
#endif
```

and

```cpp
#if defined(__GFX10__) || defined(__GFX11__) || defined(__GFX12__)
    return 32;
#else
    return 64;
#endif
```

Only one of the two is future-proof; good luck choosing the correct one unless you happen to stumble on this discussion.

UPD: And note that this suffers from the exact same issue as `__AMDGCN_WAVEFRONT_SIZE__` in that it can produce unexpected results on host (or, presumably, with SPIR-V target). So, I fail to see how it improves over the old design, except shifting the responsibility of maintaining the list of architectures with Wave64 and implementing guardrails against improper use onto the user. 

---

### 评论 #26 — dot-asm (2025-04-15T11:59:45Z)

The release notes are finally updated suggesting
```
   #if defined(__GFX9__)
   <choose your 64 wavefront poison>
   #else
   <choose your 32 wavefront poison>
   #endif
```

The declared rationale for the change was that the macro in question [\_\_AMDGCN\_WAVEFRONT\_SIZE] is too easy to misuse. I for one fail to see how the suggested alternative makes it less error prone. Indeed, recall that \_\_GFX\*\_\_ are defined only on the device side, so that people are effectively bound to make the very same mistakes. Except that there will be a wider variety of them, every developer will make their own.

As for downgrading warpSize to non-const. Let's consider the `warpSize = 42` assignment that would have to become legitimate. There are two options, a) the compiler will reject it, which means that it would be in formal violation of the language specification; b)  the compiler will compile it, which would arguably qualify as undefined behaviour one way or another. Indeed, it would be either compiled as nop, if not trap, or will have to reserve a memory cell, but what would it actually mean? At the very least it would mean nothing to the hardware, right?

As for the `-mwavefrontsize64` compiler option. Given the suggestion that the wavefront size is to be queried with hipGetDeviceProperties on the host side, specifically hipcc command should arguably reject the option. Indeed, hipGetDeviceProperties returns per-device parameter, while `-mwavefrontsize64` controls per-application, or even per-kernel, one.

To summarize. I sense that non-AMD commenters would agree that suggested deprecations complicate developer's life. It would be beneficial for the compiler to convey the critical information it has to possess [to generate the code] to the application.


---

### 评论 #27 — GMNGeoffrey (2025-04-21T17:27:15Z)

I just came across this issue in my efforts to hipify a CUDA project correctly (as opposed to my current approach of hardcoding warp size as 64). I remain confused about what exactly is happening and what the expectation is from users, especially because numerous ROCm libraries are still themselves using the macro (e.g. https://github.com/ROCm/clr/issues/154). Is `::rocmprim::device_warp_size()` still going to be a compile-time constant, just implemented using the `__GFX*__` macros or is every end user expected to define these themselves? I agree that `__AMDGCN_WAVEFRONT_SIZE__` is easy to misuse, but I echo the commenters above in saying that I think this doesn't make misuse any less likely and is just generally a pain. If you really think it's necessary to alert people to their misuse of the macro in host code, perhaps you could replace it with `__AMD_GCN_WAVEFRONT_SIZE_DONT_USE_THIS_IN_HOST_CODE_IT_WILL_BREAK_YOU__` and then continue to provide `__device__` only APIs like `::rocmprim::device_warp_size()` and `warpSize`. Maybe even have amdclang++ define it on the host side as `#error don't use this in host code` (can someone think of a place that macro could get expanded and not produce a compiler error?). Those seem a bit silly, but less error prone than what I understand to be the proposed plan and less of a pain for users of ROCm.

---

### 评论 #28 — tedliosu (2025-05-31T06:35:52Z)

Hi all, I’d like to share my experience regarding the recent deprecation of `__AMDGCN_WAVEFRONT_SIZE__` and how it may be affecting system stability when using ROCm 6.4.1 with RDNA3 (gfx1102) hardware.

1. **Working setup on ROCm 6.3:**
   While using ROCm 6.3, I successfully patched [hipCollections](https://github.com/ROCm/hipCollections) to support `gfx1102`, since `gfx1100` was already present in the codebase. This required minimal changes—just adding `gfx1102` strings and conditionals to the build system and its dependencies like `libhipcxx`. I was able to compile the examples and test suite, and confirmed that the `static_set` example (and others) ran successfully without issue on my RDNA3 system.

2. **System crashes with ROCm 6.4.1:**
   After upgrading to ROCm 6.4.1 (latest minor version at current time of writing), recompiling and running the same patched hipCollections code caused a full system freeze with a **ring gfx timeout**, requiring REISUB to recover. The same failure behavior also occurred when using the [hipDF](https://github.com/ROCm-DS/hipDF) project (a HIP port of cuDF/libcudf), also patched for `gfx1102`.

3. **Macro deprecation warning as a suspect:**
   While I can’t definitively prove that the deprecation of `__AMDGCN_WAVEFRONT_SIZE__` is the root cause, it's worth noting that the **only major difference in compile-time output** between ROCm 6.3.4 and ROCm 6.4.1 is the **deprecation warning** for this macro. Given that many HIP applications rely on this macro to conditionally specialize logic for `wavefront_size == 32` vs. `64`, it is plausible that incorrect wavefront assumptions are being encoded in the generated device binary, leading to undefined behavior or crashes on execution.

4. **Request to AMD:**
   Please **either do not deprecate `__AMDGCN_WAVEFRONT_SIZE__`** (as it's essential for certain device-side optimizations and correctness checks), **or ensure that all affected ROCm libraries and projects** (including hipCollections, hipDF, and their dependencies) are updated to safely and correctly handle wavefront size without relying on that macro — **especially in a way that avoids hard system lockups**.

Let me know if there's anything I can do to help narrow down a repro or provide diagnostic logs. Thanks!

---

### 评论 #29 — dot-asm (2025-07-22T10:32:24Z)

Quoting https://rocm.blogs.amd.com/ecosystems-and-partners/transition-to-hip-7.0-blog/README.html#warpsize-change:

> **In order to match the CUDA specification**, the `warpSize` variable is no longer `constexpr`.

I've emphasized the beginning of the sentence in order to illuminate the fact that the motivation is demonstrably misguided. While it's true that `warpSize` is not declared specifically `constexpr` in CUDA, it is a pure constant on the device side as in
```
__device__ constexpr int foo() { return warpSize; }
__global__ void bar(int *p) { *p = foo(); }
```
If the upcoming HIP compiler can compile this snippet, then at least one side of the conundrum would be a non-issue. (Just in case a reminder, the problem is two-fold a) using warpSize as [device-only] variable, and b) type declarations that depend on the wavefront size.)


---

### 评论 #30 — harkgill-amd (2025-08-13T14:48:14Z)

The recent change to warpSize has been finalized and will align with CUDA starting from ROCm 7.0. It remains an early-folded constant, allowing its use for loop bounds and loop unrolling in the same manner as a compile-time warp size. It is important to note that warpSize has never functioned as a compile-time constant in CUDA. The adjustments in ROCm reflect this behavior: using warpSize as a compile-time constant - for example, for array sizes or within if constexpr conditions - will result in compilation errors in all past and present versions of CUDA as well as forthcoming ROCm releases.
 
We understand that some users may prefer not to rewrite their libraries or applications. For this reason, the HIP programming guide includes examples demonstrating how to access the warp size at compile time. In such cases, the recommended approach is to determine the GPU's warp size on the host side and configure the kernel accordingly. You can find the examples at the HIP programming guide:
https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_cpp_language_extensions.html#warp-size

@dot-asm, While your example compiles on CUDA as-is, using the foo() function in any context that actually requires it to be constexpr will fail. For example,
```
__device__ constexpr int foo() { return warpSize; }
__global__ void bay()
{
    if constexpr(foo() == 32)
        printf("Warp size is 32\n");
}
```
The only difference with the HIP compiler is that we turn on the warning -Winvalid-constexpr and make it behave like an error. Passing in -Wno-invalid-constexpr or using C++23 mode, where constexpr requirements were relaxed, will result in the exact same behaviour as CUDA (Your example compiles but fails when warpSize is used in constexpr context).

---

### 评论 #31 — harkgill-amd (2025-09-08T14:16:22Z)

@dot-asm, checking in here - do you have any further questions regarding the deprecation of the macros?

---

### 评论 #32 — dot-asm (2025-09-08T15:42:07Z)

> @dot-asm, checking in here - do you have any further questions regarding the deprecation of the macros?

Not really. I still consider the decision poorly motivated and unhelpful, but who am I to tell you what to do:-) For reference, I for one have settled for the following:
```
#pragma clang diagnostic ignored "-Wdeprecated-pragma"
#ifndef __AMDGCN_WAVEFRONT_SIZE
# ifdef __GFX9__
#  define __AMDGCN_WAVEFRONT_SIZE 64
# else
#  define __AMDGCN_WAVEFRONT_SIZE 32
# endif
#endif
```
As a reminder, the point of contention for me is **not** warpSize, but types, even more specifically scalar register types in inline assembly.

As for warpSize, on a somewhat tangential note. The quoted examples are wasteful, because for any given target both templates will have to be instantiated, but only one will be used. It wastes CPU time during compilation and increases the load time on GPU. Cheers.

---

### 评论 #33 — harkgill-amd (2025-09-12T20:57:25Z)

Appreciate the detailed feedback. Given the compatibility considerations, we'll be going forward with the deprecation. More information surrounding the deprecation will be available in future release notes. Closing this out for now, thanks again for sharing your insights on the changes.

---

### 评论 #34 — yiakwy-xpu-ml-framework-team (2025-10-10T08:28:33Z)

Hi friends , previously we use `warpSize` to refer to warp size. It can be safely used both in host side and device side.

However, it becomes device side only now in ROCm 7.0:

```
inline __device__ const struct final {
  __device__
  __attribute__((always_inline, const))
    operator int() const noexcept {
      return __builtin_amdgcn_wavefrontsize();
    }   
} warpSize{};
```

Is there any reason for this change ?

---

### 评论 #35 — dot-asm (2026-01-14T23:19:27Z)

> Is there any reason for this change ?

Enough reason is provided in this thread alone. There was no reason to re-open it.

---

### 评论 #36 — harkgill-amd (2026-01-29T15:33:01Z)

Hey @yiakwy-xpu-ml-framework-team, as mentioned the rationale is shared above in this thread, most notably in https://github.com/ROCm/ROCm/issues/4121#issuecomment-2552320405. Closing this out but if you do have any further questions, please open a new issue.

---
