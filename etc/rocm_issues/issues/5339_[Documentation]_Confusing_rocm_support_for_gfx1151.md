# [Documentation]: Confusing rocm support for gfx1151

> **Issue #5339**
> **状态**: closed
> **创建时间**: 2025-09-16T15:33:42Z
> **更新时间**: 2026-03-25T18:29:27Z
> **关闭时间**: 2026-03-25T18:29:27Z
> **作者**: VantorreWannes
> **标签**: Under Investigation, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5339

## 标签

- **Under Investigation** (颜色: #0052cc)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Description of errors

I would love to buy a framework desktop which has a AMD Ryzen™ AI Max 385.
My intended use is to train small to medium size AI models with Rocm for my bachelors degree.
But after checking the documentation for Rocm i am extremely confused.

Some sources claim the gfx1151 has had support since Rocm 6, but on the announcements page of Rocm 7 it said:

```
### Expanding ROCm Ecosystem Across AMD Ryzen™ AI Processor and AMD Radeon™ Graphics

ROCm endpoint AI ecosystem supports Linux and Windows on AMD Radeon products including the latest Radeon RX 9000 series, as well as the class leading Ryzen AI MAX products.
```

Which sounds to me an awful lot like the Ryzen AI max products / gfx1151 are getting support with Rocm 7.

So i initially waited until the updated documentation for Rocm 7 was posted online. Before jumping to conclusions.
Yet when i checked the updated documentation today, it looks like gfx1151 doesn't have Rocm spport at all...

gfx1151 isn't even mentioned on the compatibility matrix page once, nor on the release notes page of Rocm 7.


If someone could please inform me what is going on here and where I'm making a mistake in my reasoning, that would be awesome.

### Attach any links, screenshots, or additional evidence you think will be helpful.

https://www.amd.com/en/products/software/rocm/whats-new.html
https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html
https://rocm.docs.amd.com/en/latest/about/release-notes.htm
https://www.amd.com/en/developer/resources/technical-articles/2025/amd-rocm-7-built-for-developers-ready-for-enterprises.html

---

## 评论 (18 条)

### 评论 #1 — ppanchad-amd (2025-09-16T15:50:00Z)

Hi @VantorreWannes. Internal ticket has been created to assist you. Thanks!

---

### 评论 #2 — harkgill-amd (2025-09-22T14:57:44Z)

Hi @VantorreWannes, thanks for sharing this feedback. I've raised these concerns with our documentation team and we have a series of fixes prepared to help address the lack of clarity surrounding gfx1151. In the meantime, here's a brief summary of where we're at currently with gfx1151/Strix Halo,

- TheRock provides support for these APUs with [wheels](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx1151) for both Linux and Windows.
- We support the APUs on Windows with the [HIP SDK](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html#windows-supported-gpus-and-apus).

We will also soon deliver a preview release of 

- PyTorch on Linux for the Ryzen AI 300 Series* and Ryzen AI Max Series 
- PyTorch on Windows for Ryzen AI 300 Series*, Ryzen AI Max Series and all Radeon RX/PRO 7000 Series and above.


This'll be the first release targeting gfx1151 with more support planned in the future. Upon release, the relevant compatibility matrix will also be updated to denote support of the APUs.

---

### 评论 #3 — janantos (2025-09-23T15:13:35Z)

Hi @harkgill-amd any ETA for this preview release of PyTorch on Linux?

---

### 评论 #4 — harkgill-amd (2025-09-24T18:34:07Z)

The release is out now! https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/index.html

---

### 评论 #5 — DisturbedNeo (2025-09-26T23:39:01Z)

That link says it’s supported on 6.4.4 specifically,  but says nothing about ROCm 7.

So it’s still unclear whether we’re able to use the latest version, or if we have to stick with third-party packages to get stuff working.

---

### 评论 #6 — mustachemo (2025-09-29T20:23:49Z)

Would love an answer on this too.. This is quite important

---

### 评论 #7 — janantos (2025-09-29T20:36:06Z)

The only mention on gfx1151 about rocm7 I can find only here in nightlies https://github.com/ROCm/TheRock. Telling me that there is not stable support in rocm7 yet. I was able to get it working with PyTorch from there. Also looks like when I compiled llama.cpp using rocm7 ubuntu complete image, it is somehow working. I am not able to compile aotriton and vllm to working state. Sad AMD is ignoring Ryzen AI line. For me their statements about support are false claims and lies. Also so called preview "support" in 6.4 is highly arguable. 

---

### 评论 #8 — harkgill-amd (2025-09-30T15:16:15Z)

The 6.4.4 PyTorch on Windows/Linux releases are stepping stones to getting full support with ROCm 7.x + Strix Halo. They are deemed preview releases as the intention was to enable users to start running workloads on both the APUs and native Windows. Going forward, there will be more releases with Strix support including ones on the ROCm 7 branch.

> it’s still unclear whether we’re able to use the latest version

It's always safest to use the latest supported release for your hardware. The configurations laid out in the compatibility matrices are thoroughly tested before being listed as "supported". That being said, [TheRock](https://github.com/ROCm/TheRock) does provide ROCm 7 wheels for gfx1151 as an alternative. These should be considered bleeding edge and are intended for user's wanting the latest features that are under active development. @janantos, If you do come across issues working with these wheels, you can file an issue under TheRock repository - there is a large community and internal developer presence here working on gfx1151. 

---

### 评论 #9 — mustachemo (2025-10-01T15:38:00Z)

@harkgill-amd batch norm operation does not work for the new gfx1152 (strix halo) architecture with ROCm 6.4.4. Shall I make an issue for this?

<img width="2181" height="1630" alt="Image" src="https://github.com/user-attachments/assets/a2f5fef2-6578-4ed1-8c69-16cde16fd7f6" />

this is using this dockerfile
```python
FROM rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

# * Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# * Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml .
RUN pip install .
```

---

### 评论 #10 — harkgill-amd (2025-10-01T16:02:26Z)

@mustachemo, this looks similar to the issue reported here https://github.com/ROCm/ROCm/issues/5441. Could you share more information including a small reproducer on that thread?

---

### 评论 #11 — mustachemo (2025-10-01T17:15:38Z)

yes, thank you!

---

### 评论 #12 — harkgill-amd (2025-10-14T18:35:51Z)

ROCm 7.0.2 is out now with support for gfx1150 and gfx1151 on Linux! https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html#rocm-7-0-2

---

### 评论 #13 — mustachemo (2025-10-14T20:32:41Z)

@harkgill-amd that's awesome!! I see the only supported data type is FP16? does that mean the kernels were written only for that Datatype? More to come soon?

---

### 评论 #14 — KrisBigK (2025-10-20T06:53:17Z)

I tried torch.nn.BatchNorm2d with the latest nightly previews, but both FP16 and FP32 failed for my gfx1151. It seemed to be an assembly error in MIOpen, so I made an issue report in the rocm-libraries repo, https://github.com/ROCm/rocm-libraries/issues/2169 . I included a reproducer there. @harkgill-amd 

---

### 评论 #15 — johnlockejrr (2025-12-05T10:18:07Z)

> [@harkgill-amd](https://github.com/harkgill-amd) batch norm operation does not work for the new gfx1152 (strix halo) architecture with ROCm 6.4.4. Shall I make an issue for this?
> 
> <img alt="Image" width="2000" height="1630" src="https://private-user-images.githubusercontent.com/93756682/496238983-a2f5fef2-6578-4ed1-8c69-16cde16fd7f6.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjQ5MzAwODgsIm5iZiI6MTc2NDkyOTc4OCwicGF0aCI6Ii85Mzc1NjY4Mi80OTYyMzg5ODMtYTJmNWZlZjItNjU3OC00ZWQxLThjNjktMTZjZGUxNmZkN2Y2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEyMDUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMjA1VDEwMTYyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTYzZTRjZjNlOGM5YjllYTM2NTBkNjFjZGI1NDJhZWRkN2RhNDE3ZjM0YzIwNjY5NzliN2YxNTVjZDQ2NDhkNWMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.XlSulB4aOHX1AfBCV9qhvryd0WJipcGskePiL-8mACc">
> this is using this dockerfile
> 
> FROM rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1
> 
> # * Set environment variables
> ENV PYTHONUNBUFFERED=1 \
>     PYTHONDONTWRITEBYTECODE=1 \
>     PIP_NO_CACHE_DIR=1 \
>     PIP_DISABLE_PIP_VERSION_CHECK=1
> 
> # * Install system dependencies
> RUN apt-get update && apt-get install -y \
>     build-essential \
>     curl \
>     git \
>     && rm -rf /var/lib/apt/lists/*
> 
> WORKDIR /app
> COPY pyproject.toml .
> RUN pip install .

Same with me, `AMD RYZEN AI MAX+ 395 w/ Radeon 8060S`, `ROCm 7.1.1`
Code:
```
import torch.nn as nn

# Make sure you're on ROCm and have a GPU available
print("CUDA available:", torch.cuda.is_available())
print("Device:", torch.cuda.get_device_name(0))

# Define a simple BatchNorm2d layer
bn = nn.BatchNorm2d(16).cuda()

# Create a random input tensor on GPU
x = torch.randn(8, 16, 32, 32, device="cuda")  # (N, C, H, W)

# Forward pass (this is where MIOpen may crash)
y = bn(x)

print("Output shape:", y.shape)
```

Error:
```
UDA available: True
Device: AMD Radeon Graphics
<inline asm>:14:20: error: not a valid operand.
v_add_f32 v4 v4 v4 row_bcast:15 row_mask:0xa
                   ^
<inline asm>:15:20: error: not a valid operand.
v_add_f32 v7 v7 v7 row_bcast:15 row_mask:0xa
                   ^
<inline asm>:17:20: error: not a valid operand.
v_add_f32 v4 v4 v4 row_bcast:31 row_mask:0xc
                   ^
<inline asm>:18:20: error: not a valid operand.
v_add_f32 v7 v7 v7 row_bcast:31 row_mask:0xc
                   ^
<inline asm>:14:20: error: not a valid operand.
v_add_f32 v1 v1 v1 row_bcast:15 row_mask:0xa
                   ^
<inline asm>:15:20: error: not a valid operand.
v_add_f32 v0 v0 v0 row_bcast:15 row_mask:0xa
                   ^
<inline asm>:17:20: error: not a valid operand.
v_add_f32 v1 v1 v1 row_bcast:31 row_mask:0xc
                   ^
<inline asm>:18:20: error: not a valid operand.
v_add_f32 v0 v0 v0 row_bcast:31 row_mask:0xc
                   ^
MIOpen(HIP): Error [Do] 'amd_comgr_do_action(kind, handle, in.GetHandle(), out.GetHandle())' AMD_COMGR_ACTION_CODEGEN_BC_TO_RELOCATABLE: ERROR (1)
MIOpen(HIP): Error [BuildOcl] comgr status = ERROR (1)
MIOpen(HIP): Warning [BuildOcl] error: cannot compile inline asm
error: cannot compile inline asm
error: cannot compile inline asm
error: cannot compile inline asm
error: cannot compile inline asm
error: cannot compile inline asm
error: cannot compile inline asm
error: cannot compile inline asm
8 errors generated.

MIOpen Error: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: MIOpenBatchNormFwdTrainSpatial.cl
Traceback (most recent call last):
  File "/home/incognito/AI/pylaia-reloaded/datasets/sam_44_mss_pango/trigger.py", line 15, in <module>
    y = bn(x)
        ^^^^^
  File "/home/incognito/AI/pylaia-reloaded/.venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/incognito/AI/pylaia-reloaded/.venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/incognito/AI/pylaia-reloaded/.venv/lib/python3.12/site-packages/torch/nn/modules/batchnorm.py", line 193, in forward
    return F.batch_norm(
           ^^^^^^^^^^^^^
  File "/home/incognito/AI/pylaia-reloaded/.venv/lib/python3.12/site-packages/torch/nn/functional.py", line 2813, in batch_norm
    return torch.batch_norm(
           ^^^^^^^^^^^^^^^^^
RuntimeError: miopenStatusUnknownError
```

On FP16 it works, no error
Code:
```
import torch
import torch.nn as nn

print("CUDA available:", torch.cuda.is_available())
print("Device:", torch.cuda.get_device_name(0))

# BatchNorm in FP16
bn = nn.BatchNorm2d(16).cuda().half()   # move layer to GPU and FP16

# Random input tensor in FP16
x = torch.randn(8, 16, 32, 32, device="cuda", dtype=torch.float16)

# Forward pass
y = bn(x)

print("Output dtype:", y.dtype)
print("Output shape:", y.shape)
```

---

### 评论 #16 — pmperry (2026-01-10T11:53:41Z)

> That link says it’s supported on 6.4.4 specifically, but says nothing about ROCm 7.
> 
> So it’s still unclear whether we’re able to use the latest version, or if we have to stick with third-party packages to get stuff working.

Anything below the 365 is not Strix Point, it’s Kraken point and I see no official support named for those chips.  It’s frustrating.

---

### 评论 #17 — warneat (2026-03-11T09:08:11Z)

**Confirmed: gfx1151 works with ROCm 7.2.0 for GGML-based workloads (whisper.cpp, llama.cpp)**

Quick data point: whisper.cpp with `-DGGML_HIP=ON -DAMDGPU_TARGETS="gfx1151"` builds and runs correctly on ROCm 7.2.0 (native, no Docker). Getting **31.9x realtime** on a Whisper large-v3 finetuned model with Radeon 8060S.

Key finding: GGML bypasses rocWMMA entirely (uses its own HIP kernels), which is why it works even though rocWMMA still has gfx1151 issues ([rocm-libraries#4618](https://github.com/ROCm/rocm-libraries/issues/4618)).

ROCm 6.4.4 (Docker) did **not** work — ABI mismatch with local 7.2.0 libs (libhipblas.so.2 vs .3, libamdhip64.so.6 vs .7).

Full build details and benchmarks in my post on [ggml-org/llama.cpp#14734](https://github.com/ggml-org/llama.cpp/issues/14734).

---

### 评论 #18 — harkgill-amd (2026-03-25T18:29:27Z)

There have been a couple different releases since this ticket was first opened so here's a quick rundown of where we're currently at with Strix Halo,

- Our ROCm on Radeon portal is now ROCm on Radeon/Ryzen and calls out support for Strix Halo directly in our latest releases ([ref](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html))
- The [ROCm 7.11 preview release](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html) marks the start of our new release stream which will unify all the different documentation portals. This release also has Strix Halo support and subsequent releases in this stream will continue to have support as well.
- https://github.com/ROCm/TheRock from which the new 7.11 release stream is based off provides nightly wheels for Strix Halo https://rocm.nightlies.amd.com/v2/gfx1151/ along with other gfx115X devices.

Going to close this issue out as we've made large strides from the original point of not mentioning gfx1151/Strix Halo in any of our official documentation. If there are still any gaps that need to be addressed, please open a new issue and we can tackle it further from there. Thanks for all your patience and support!

---
