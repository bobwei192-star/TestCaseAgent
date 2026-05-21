# [Issue]: incorrect L2_cache_size reported by torch.cuda.get_device_properties

> **Issue #4203**
> **状态**: closed
> **创建时间**: 2024-12-27T00:54:33Z
> **更新时间**: 2025-05-30T16:32:51Z
> **关闭时间**: 2025-05-30T16:02:11Z
> **作者**: stas00
> **标签**: Under Investigation, MI300X, ROCm 6.2.4
> **URL**: https://github.com/ROCm/ROCm/issues/4203

## 标签

- **Under Investigation** (颜色: #0052cc)
- **MI300X** (颜色: #ededed)
- **ROCm 6.2.4** (颜色: #ededed)

## 描述

### Problem Description

w/ `torch-2.6` `torch.cuda.get_device_properties` reports:
```
_CudaDeviceProperties(name='AMD Instinct MI300X', major=9, minor=4, 
gcnArchName='gfx942:sramecc+:xnack-', total_memory=196592MB, multi_processor_count=304, 
uuid=66333330-6463-3464-3030-646565323262, 
L2_cache_size=4MB)
```

It currently reports an invalid `L2_cache_size`- it reports the size of a single compute die and not of the whole accelerator. It's 4MB per compute die - but there is no information of how many compute dies there are or if it's suggesting that it's per die - so this is then misleading/incorrect name of the field.

There should be 8 in the case of MI300X and the total should be then 32MB.

I first thought it was a pytorch issue, but I was told that the issue comes from ROCm.

If you're on torch slack please see this thread:

https://pytorch.slack.com/archives/C3PDTEV8E/p1735067560696929?thread_ts=1735017298.875249&cid=C3PDTEV8E


### Operating System

Ubuntu

### CPU

not sure

### GPU

MI300X

### ROCm Version

ROCm 6.2.4

### ROCm Component

HIP

### Steps to Reproduce

`torch.cuda.get_device_properties()`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

torch=2.6.0a0+gitd6a066e
hip=6.2.41133-dd7f95766

---

## 评论 (10 条)

### 评论 #1 — ppanchad-amd (2024-12-30T15:17:08Z)

Hi @stas00. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — jamesxu2 (2025-01-09T18:22:02Z)

@stas00 I was able to reproduce this, and I see the internal API call to hipGetDeviceProperties also reports **l2CacheSize = 4194304**

> It currently reports an invalid L2_cache_size- it reports the size of a single compute die and not of the whole accelerator. It's 4MB per compute die  [...] There should be 8 in the case of MI300X and the total should be then 32MB.

Why do you say this? The MI300X datasheet specifies the L2 cache is shared between compute units. ([source](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-data-sheet.pdf))

>  Each OAM module includes:
• Eight accelerated compute dies (XCDs) with 38 compute units (CUs),
32 KB of L1 cache per CU, 4 MB shared L2 cache shared across CUs,
and 256 MB of AMD Infinity Cache™ shared across 8 XCDs. The 




---

### 评论 #3 — stas00 (2025-01-10T02:13:30Z)

it's 4MB per XCD and there are 8 XCDS - so `4*8=32`, no?

L3 256MB is shared across 8 XCDs. L2 is not shared across 8 XCDs - at least based on text you quoted above.

4MB total of L2 sounds very low comparatively to the other accelerators: https://github.com/stas00/ml-engineering/tree/master/compute/accelerator#caches

But if it's 4MB indeed then the description should say:

> • Eight accelerated compute dies (XCDs) with 38 compute units (CUs),
32 KB of L1 cache per CU, 4 MB shared L2 cache shared across 8 XCDs,
and 256 MB of AMD Infinity Cache™ shared across 8 XCDs. The

that's "shared across 8 XCDs" and not "shared across CUs", does it make sense?

---

### 评论 #4 — jamesxu2 (2025-01-10T14:41:30Z)

Hi @stas00 , apologies, upon rereading the datasheet, you are right - it is 4MB L2 cache per XCD, shared across CUs within each XCD. There should be 32MB total available across all 8 XCDs. Let me look into this further.  

---

### 评论 #5 — stas00 (2025-01-10T17:37:08Z)

excellent. 

Since you misread it I am sure others would as well. Therefore it might even help to spell it out in the specs to be:

> 4 MB shared L2 cache shared across 8 XCDs for a total of 32MB



---

### 评论 #6 — stas00 (2025-01-10T17:38:28Z)

And tangentially to this issue - shouldn't device properties also return L3 256MB cache? I know NVIDIA/Intel don't have L3 cache, but I think it's a crucial information for AMD users.

This last info is crucial if someone running benchmarks and they would need to know L3 size in order to reset it between benchmark iterations.

---

### 评论 #7 — tcgu-amd (2025-01-23T19:17:40Z)

Hi @stas00, a bit of an update. Seems like this issue is linked to the behavior of lower level runtime and device interface. Displaying L2 Cache size is a relatively new introduction to the upstream PyTorch across all platforms. We are in the process of addressing this issue and will keep you updated. Thanks!

---

### 评论 #8 — stas00 (2025-01-23T19:50:38Z)

Thank you for working on this, @tcgu-amd!

---

### 评论 #9 — tcgu-amd (2025-05-30T16:02:11Z)

Hi @stas00, thank you for your patience. A patch has been merged to ROCR-Runtime which should fix this issue and provide the correct total L2 cache size https://github.com/ROCm/ROCR-Runtime/commit/fc561ff37a4496d20f744fdef38f5fb7c797056d. Please note that this change should be effective in a future Pytorch + ROCm release. I will be closing this issue for now. Thanks! 

---

### 评论 #10 — stas00 (2025-05-30T16:32:50Z)

Thank you for fixing, @tcgu-amd!

---
