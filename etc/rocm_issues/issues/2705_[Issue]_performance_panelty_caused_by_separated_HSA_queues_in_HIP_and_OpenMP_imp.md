# [Issue]: performance panelty caused by separated HSA queues in HIP and OpenMP implementations

> **Issue #2705**
> **状态**: closed
> **创建时间**: 2023-12-11T22:29:12Z
> **更新时间**: 2024-11-01T15:47:34Z
> **关闭时间**: 2024-11-01T15:47:33Z
> **作者**: ye-luo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2705

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

The two programming models OpenMP and HIP provided by ROCm leverage the same HSA runtime. HIP holds its own pool HSA queues controlled by the `GPU_MAX_HW_QUEUES` environment variable and OpenMP holds its own pool HSA queues controlled by the `LIBOMPTARGET_AMDGPU_NUM_HSA_QUEUES` environment variable.

However, HSA queues are directly related if not one-to-one mapped to hardware queues and over-subscription causes huge performance penalty. I can view this from the application performance regression and kernel log
`amdgpu: Runlist is getting oversubscribed. Expect reduced ROCm performance.`

For applications using both GPU programming models, developers need to take into account how many HSA queues in each programming model runtime to use when figuring out the optimal performance. This is unnecessary complication added for applications. On the contrary, all the CUDA streams (runtime and driver APIs) are virtualized and decoupled from the hardware count. Although concurrent execution is still limited by the hardware queues, users can create any amount of CUDA streams without much penalty.

One possible solution could be HSA making its queues virtualized.
Potentially, one can implement Vulkan APIs on top of HSA and cause further problems if the current design issue retains.


### Operating System

Any Linux

### CPU

Any CPU

### GPU

Any AMD GPUs

### ROCm Version

Throughout 5.x and beyond

### ROCm Component

HIP, OpenMP, HSA

### Steps to Reproduce

_No response_

### Output of /opt/rocm/bin/rocminfo --support
```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES
```


---

## 评论 (11 条)

### 评论 #1 — JonChesterfield (2023-12-12T10:51:30Z)

HSA queues are virtualised if you allocate too many - that's what the oversubscription warning is about.

I'm not sure this is solvable at the language runtime level. If there's a program running openmp offloading and hip offloading to the same GPU, and both language runtimes allocated four queues (I think that's the current default for openmp, guessing hip is vaguely similar), and GPUs have of the order of 32 or so hardware queues, all would be fine.

So I think to hit this oversubscription the setup must be something like eight independent host processes running on the same GPU, each running HIP and OpenMP, each allocating their own four queues for ~64 total. Or that sort of setup - maybe something MPI inspired?

Something knows how many processes are on each GPU, and how many queues there are available, but I don't think it's the language runtimes. Is the fix here an additional /2 in whatever is setting those environment variables, or some other ratio between the languages?

edit: I'm not sure how the over-subscription is implemented - two obvious choices would be to allocate the backing memory for each queue and CWSR them on and off the GPU, which would have the proper semantics and poor performance - or to hand out the same buffer on multiple requests, which would have no context switching cost but would introduce spurious serialisation between otherwise unrelated packets. Neither seem great relative to staying within the count of hardware queues.

---

### 评论 #2 — ye-luo (2023-12-12T15:44:29Z)

When running nightly test, I frequently oversubscribe a GPU with 8 or 16 MPI processes. runtime doesn't need to know the processes but the lower level runtime (HSA) of the higher level runtimes (HIP/OpenMP) is responsible for a sensible number of queues interacting with the GPU driver that should handle multiple processes.

Need a way to cap the number of HSA queues at HSA runtime level. Not good to make the driver screaming.

---

### 评论 #3 — ye-luo (2023-12-12T16:19:20Z)

Actually I saw the over-subscription warning even with just 2 MPI processes talking to the same GPU W6800 which is RNDA2.

---

### 评论 #4 — fxkamd (2023-12-12T16:27:55Z)

On Navi2x and later consumer GPUs, there are only 16 compute HQDs (hardware queue descriptors), and only 8 of them are available for ROCm. On Vega GPUs, Navi1x and MI-GPUs, there are 32 HQDs, with 24 available for ROCm.

Another resource that can get oversubscribed is VMIDs (virtual address space IDs). This is a hard limits on the number of concurrent ROCm processes before you get into oversubscriptions. There are 16. On consumer GPUs 8 are used by ROCm, 7 are for graphics, 1 is for kernel mode. On MI-GPUs 13 are used by ROCm, 2 for graphics (used for video post-processing) and 1 for kernel mode.

Navi3x has a more capable firmware scheduler, where oversubscription is handled more gracefully.

---

### 评论 #5 — torrance (2023-12-14T02:05:48Z)

I want to chime in here: I've spent the last few days understanding performance regressions in an application we are building, after switching from a threaded model (independent execution paths using `std::thread`) to a process-based model (using MPI).

Despite identical workloads, the process-based model is significantly slower. In a [minimum-working example](https://github.com/torrance/rocm-mwe) on a W6800 development environment with 8 independent execution paths, we see a regression from 21.22 s down 28.3 s. If we add more processes/threads, the regression becomes much more severe. 

With the process-based model, we see kernel messages such as:

```
Dec 14 01:39:18 xxxx kernel: [2582911.421491] amdgpu: Runlist is getting oversubscribed. Expect reduced ROCm performance.
Dec 14 01:39:19 xxxx kernel: [2582911.790196] amdgpu: No more SDMA queue to allocate
Dec 14 01:39:19 xxxx kernel: [2582911.791289] amdgpu: Pasid 0x8011 DQM create queue type 1 failed. ret -12
```

The thread-based model doesn't show such messages at all.

For the simplicity of code and the ease of distributing work over an HPC cluster, we want to avoid having to implement a hybrid process/thread model just to avoid this regression.

**Is there anything we can do mitigate this penalty?** We are OK with serialising work on the GPU from independent processes when they identify they are using the same GPU - in fact, we've already done this, but it doesn't currently mitigate the regression so long as the processes continue to be alive (I assume they continue to hold onto resources even after all kernels and memory transfers have finished).

---

### 评论 #6 — torrance (2024-01-18T01:12:47Z)

Regarding my last message, is this the wrong place to ask for this support/mitigations or report these performance issues?

Is there are more appropriate avenue that will get engagement from AMD?

---

### 评论 #7 — ye-luo (2024-01-18T03:07:37Z)

@torrance My two cents. The performance of ROCm software in a threaded environment is all over the place and is way behind other competitors. I raised this issue directly to AMD engineers at least half a year ago if not more. They seem to understand the situation but call it a feature and didn't act on it. There might be several reasons that they didn't view it as a priority. The reason I put out this issue publicly is to let ROCm users who suffer from this issue share concerns. When time comes, they may tackle it.

---

### 评论 #8 — ye-luo (2024-05-13T16:26:38Z)

AMD published the [MES](https://gpuopen.com/download/documentation/micro_engine_scheduler.pdf) firmware documentation giving a bit details behind the scene.

It seems to be the only mechanism to round-robin dispatching HSA queues to the hardware queues when over-subscription happens.

---

### 评论 #9 — schung-amd (2024-10-16T22:15:03Z)

Hi, sorry for the limited response in this thread to date. I'll reach out internally to see what we're doing to address these performance issues.

As a note, although this doesn't offer any solutions and is a bit sparse at the moment, we have some conceptual documentation of queue oversubscription now at https://rocm.docs.amd.com/en/latest/conceptual/oversubscription.html.

---

### 评论 #10 — schung-amd (2024-10-21T14:21:46Z)

We're planning a feature to allow HIP and OpenMP to pull from a shared pool of queues, which should mitigate oversubscription issues in situations where both are being used. There is no timeline for this as of yet. Let me know if you have any questions about this and I'll forward them to the internal team.

---

### 评论 #11 — schung-amd (2024-11-01T15:47:33Z)

Closing this for now; this is in the pipeline but there is no timeline for it, and it shouldn't be expected in the near future.

---
