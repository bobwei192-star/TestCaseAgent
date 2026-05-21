# __shfl_sync: case of false advertising?

> **Issue #5852**
> **状态**: closed
> **创建时间**: 2026-01-14T23:16:45Z
> **更新时间**: 2026-02-23T19:41:33Z
> **关闭时间**: 2026-02-23T19:41:33Z
> **作者**: dot-asm
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5852

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

Since ROCm aims to align with CUDA, a case can be made that recently introduced __shfl_sync primitives are inadequate reflections of their CUDA counterparts. Let's compare. ROCm performs an elaborate dance that effectively boils down to:
```
heavily_over_engineered_assert(mask == __activemask());
__shfl(...);
```
To illuminate the difference with CUDA let's consider the following snippet:
```
__global__ void kernel(long *p)
{
    long m;

    if (threadIdx.x & 1) {
        m = __activemask();
        m = __shfl_xor_sync(~0L, m, 1);
    } else {
        m = __activemask();
        m = __shfl_xor_sync(~0L, m, 1);
    }
    p[threadIdx.x] = m;
}
```
Does it work on AMD? No, it crashes due to heavily_over_engineered_assert. Does it work on CUDA? Yes! Well, it's kind of a tricky question in the sense that it works differently on pre-Volta and post-Volta, but at the very least it doesn't crash and produces predictable result.

Hardware-wise AMD GPUs are equivalent to pre-Volta with respect to shuffle operation. So given the initial assessment what does ROCm try to achieve? If to simply reflect hardware capabilities and align with pre-Volta, then it fails. And if it attempts to align with with post-Volta, then it fails again...

For reference. On pre-Volta __shfl_sync-s are compiled as simple __shfl-s. That's it. One can argue that it can be confusing to the programmer, but that's how it is, and therefore is supposed to be recognized/known. For post-Volta let's consider more generalized
```
if (condition) {
    // pre-true
    __shfl_sync(mask, ...);
    // post-true
} else {
    // pre-false
    __shfl_sync(mask, ...);
    // post-false
}
```
It's "**executed**" as
```
if (condition) {
    // pre-true
} else {
    // pre-false
}
__shlf(...);
if (condtion) {
    // post-true
} else {
    // post-false
}
```
I've put "executed" in quotes to denote the fact that it's not how the binary code will look like. But it's a valid way for us to **think** about it. There are nuances, but overall the point is that this is the minimum a compiler would have to do **if** it aimed to align with post-Volta on pre-Volta hardware.


---

## 评论 (7 条)

### 评论 #1 — dot-asm (2026-01-16T11:44:38Z)

> it works differently on pre-Volta and post-Volta, but at the very least it doesn't crash and produces predictable result.

This might be inaccurate in pre-Volta context, where result is not actually specified. The following snippet would be more illustrative on pre-Volta
```
__global__ void kernel(long *p)
{
    long m;

    if (threadIdx.x & 2) {
        m = __shfl_xor_sync(~0L, threadIdx.x, 1);
    } else {
        m = __shfl_xor_sync(~0L, threadIdx.x, 1);
    }
    p[threadIdx.x] = m;
}
```


---

### 评论 #2 — ssahasra (2026-02-21T05:01:14Z)

From the CUDA programming guide, the example in the ticket is declared invalid. Hence its outcome is *undefined* and not *unspecified*.

https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#independent-thread-scheduling-7-x

     "...  valid on NVIDIA Volta GPU Architecture, but not on Pascal or earlier architectures."
     
> Does it work on CUDA? Yes! Well, it's kind of a tricky question in the sense that it works differently on pre-Volta and post-Volta, but at the very least it doesn't crash and produces predictable result.

It's not clear what the ask is. Does it crash on Pascal? No. Does it produce predictable results? Sure, but what is the predictable result? It's all in "here be dragons" territory. Pascal hardware doesn't specify anything. PTX says it is UB. There is no way for HIP  to commit to a match for this situation. At least HIP cannot commit to a general *guess* about what Pascal might or might not be doing.

> For reference. On pre-Volta __shfl_sync-s are compiled as simple __shfl-s. That's it. One can argue that it can be confusing to the programmer, but that's how it is, and therefore is supposed to be recognized/known.

That sounds like a "just so" argument. What is the actual ask? What is the use-case for HIP to specify the outcome of this incorrect pattern?

> I've put "executed" in quotes to denote the fact that it's not how the binary code will look like. But it's a valid way for us to think about it. There are nuances, but overall the point is that this is the minimum a compiler would have to do if it aimed to align with post-Volta on pre-Volta hardware.

The interpretation is wrong on pre-Volta hardware. The shfl_sync() is called in divergent control flow, and there could be other matching static instances of shfl_sync() that might dynamically sync with these. Hence, there is no general way for the compiler to reason about how to "reconverge" that code into a single call. If it was that easy, users would not have to port old shfl() calls to the new shfl_sync() calls. Of course, it's always awesome to discover that maybe there is a way to interpret this in a consistent manner, and we are always open to that.

---

### 评论 #3 — dot-asm (2026-02-21T09:55:07Z)

> > Does it work on CUDA? Yes! Well, it's kind of a tricky question in the sense that it works differently on pre-Volta and post-Volta, but at the very least it doesn't crash and produces predictable result.
> 
> It's not clear what the ask is.

ROCm __shfl_sync were intoduced to mimic CUDA counterparts. And since they don't, the ask is to align it with CUDA. If you aim to align with post-Volta, then the compiler would need to break the if statements as desctibed above. If you aim for pre-Volta, then just drop the heavily over-engineered assert. In worst case don't over-engineer it. As a compromise make the assertion dependent on the optimization flag. The idea would be that only debug builds would expose the mask and activemask discrepancy.

> > I've put "executed" in quotes to denote the fact that it's not how the binary code will look like. But it's a valid way for us to think about it. There are nuances, but overall the point is that this is the minimum a compiler would have to do if it aimed to align with post-Volta on pre-Volta hardware.
> 
> The interpretation is wrong on pre-Volta hardware.

I explicitly said that the interpretation in question applies to post-Volta hardware. Again, with the purpose to illuminate what a compiler **would** have to do to mimic the post-Volta behaviour on pre-Volta hardware.


---

### 评论 #4 — ssahasra (2026-02-22T06:19:28Z)

> ROCm __shfl_sync were intoduced to mimic CUDA counterparts. And since they don't, the ask is to align it with CUDA.

This is the actual mission statement:
https://rocm.docs.amd.com/projects/HIP/en/latest/what_is_hip.html

"HIP supports building and running on both AMD GPUs or NVIDIA GPUs. GPU Programmers familiar with NVIDIA CUDA or OpenCL will find the HIP API familiar and easy to use. [snip] However, HIP is **not intended to be a drop-in replacement** for CUDA, and developers should **expect to do some manual coding** and performance tuning work [snip]."

I don't really see any false advertising here. If the statement is not clear enough, then maybe that can be fixed.

As acknowledged in the issue description, AMD GPUs are equivalent to pre-Volta NVIDIA GPUs. So, behaviour on Volta and later hardware is a moot point. The program is invalid on pre-Volta hardware as well as AMD GPUs. Breaking loudly is better than silently producing incorrect results, because the latter will encourage the user to expect behaviour that cannot be expressed in clear terms on AMD GPUs.

https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#independent-thread-scheduling-7-x

But this is not an attempt to conveniently hide behind a spec. Identifying a useful niche will not be easy, both in the HIP spec and for the user to use correctly. So the question is still the same. What is the value proposition for this added complexity? Is there a compelling use-case for carving out some defined behaviour on AMD GPUs within this universe of invalid programs? I would prefer to frame this as a pure language semantics question rather than a "just so" argument built around CUDA happenstance. What is a meaningful outcome of that HIP program that we are leaving on the table?

---

### 评论 #5 — dot-asm (2026-02-23T14:02:59Z)

> "... developers should **expect to do some manual coding** and performance tuning work [snip]."

There is an inherent contradiction. On one hand, shfl_sync-s were added to lower the said expectation, but on the other hand they effectively raise it by not actually mirroring CUDA. Recall that support for pre-Volta is being dropped, so that new CUDA users have higher expectations already... Which is why I'm kind of making a case for HIP's shfl_sync-s effectively misleading users. Moreover, I'm inclined to believe that you're misleading yourself. Not you personally of course, but AMD :-) As established, you're not aiming to mimic post-Volta. In which case what is the over-engineered assert trying to achieve? The loop part... It looks as if the expectation is that threads execute it independently... Which is not the case... Either way, as already implied, I accept that there is value in failing loudly, but it doesn't have to be over-engineered. And the trouble is that once the problem is ironed out, the assert becomes a burden. Well, one can  say that a pair of additional instructions, comparison and non-taken branch, is a reasonable price, but it's currently far from being the case. To summarize, as already mentioned, three options: mimic post-Volta for real (rejected, fair enough), don't over-engineer the assertion (so that it's compiled as two instructions), better yet empower users by making it optional.

As for "just so" vs. "pure language semantics." Consider following:
```
__global__ void kernel(long *p, long mask)
{
    long m;
    m = __shfl_xor_sync(mask, threadIdx.x, 1);
    p[threadIdx.x] = m;
}
```
How is __shfl_xor_sync compiled by CUDA here? In the binary code that is, not PTX... Since the code generator detects that there is no possibility for divergence, `mask` is actually ignored and a raw non-sync shfl is issued. In other words it's situational. Also note that one can get undefined results even if mask == __activemask(), as in
```
__global__ void kernel(long *p)
{
    long m = 0;
    if (threadIdx.x & 1)
        m = __shfl_xor_sync(__activemask(), threadIdx.x, 1);
    p[threadIdx.x] = m;
}
```
What I'm trying to demonstrate is that there are no pure language semantics in the context of inter-lane shuffles. It's all about users understanding how the hardware works.

As for use-case. I don't have one, not anymore, as after evaluating all this I've decided to implement own shfl wrappers around __builtin_amdgcn_ds_bpermute. My goal here is to advocate for common sense and transparency.

---

### 评论 #6 — dot-asm (2026-02-23T16:47:13Z)

> To summarize, as already mentioned, three options: mimic post-Volta for real (rejected, fair enough), don't over-engineer the assertion (so that it's compiled as two instructions), better yet empower users by making it optional.

A fourth option naturally exists: roll back and remove shfl_sync-s. I didn't bring it up, because it would surely be rejected, one can't put the toothpaste back into the tube.

Additional remark about failing loudly. What is more user friendly? "Axe" crash you can't diagnose without a debugger, or "mask != __activemask() in line X" message? Obviously the latter. While what you offer is the former. In other words, if anything, one can say that it's not loud enough ;-) Just in case, I recognize that having a code that prints a message can be undesirable in a production kernel. But having an option to switch it on during the development phase would surely be appreciated. Again, empower users!

---

### 评论 #7 — schung-amd (2026-02-23T19:41:33Z)

Thanks for the discussion @dot-asm. This isn't the first tangle we've had with HIP/CUDA alignment, and the finer points are always interesting to debate.

Not to be fully dismissive, but as @ssahasra states, we don't currently have interest in changing this. While you are correct that the behaviour of our `shfl_sync` differs from CUDA in this example, at the end of the day we aim to align with CUDA spec, and this is UB in the equivalent pre-Volta case. We don't have a definitive answer for what this code should do and have no reason to decide on one. 

1-to-1 alignment with the actual undefined CUDA behaviour is only beneficial here if there's a usecase that it serves; if there is such a usecase which compels us to make a decision on this, we'll happily revisit this discussion. I would argue that this will always be better served with documentation than a functional change however, as relying on undefined behaviour to be consistent is dangerous. If the goal here is better clarity for users on what's happening at a hardware level and how to write valid code using `shfl_sync`, perhaps we can write a guide or blog post on that. There are a lot of ways to write invalid programs though, and I'm not sure that this is one of the more common ones.

I'm going to close this for now, but feel free to continue discussion.

---
