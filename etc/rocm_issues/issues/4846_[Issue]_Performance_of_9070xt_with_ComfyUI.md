# [Issue]: Performance of 9070xt with ComfyUI

> **Issue #4846**
> **状态**: open
> **创建时间**: 2025-05-30T10:17:15Z
> **更新时间**: 2026-04-26T09:20:57Z
> **作者**: alshdavid
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4846

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I'm using the default ComfyUI SDXL workflow with Ubuntu 24.04 and the proprietary AMD drivers. This is also the case using Fedora 42.

Issues:
- Using the default launch settings, the generation crashes with OOM errors
- Using tweaked settings, generation passes but is very slow

Results:

Clean Ubuntu 24.04 installation
AMD proprietary drivers
Python 3.10.17
Pytorch nightly
ROCm 6.4.1

```
export TORCH_COMMAND="--pre torch torchvision torchaudio pytorch-triton-rocm --index-url https://download.pytorch.org/whl/nightly/rocm6.4"

python ./main.py
```


|Card|Model|Steps|Resolution|Time|Notes|
|-----|------|------|----------|----|------|
|6900xt|SD1.5|20|512x512|2.42s|ROCm 6.3|
|9070xt|SD1.5|20|512x512|3.76s||
|6900xt|SDXL|20|1024x1024|15.16s|ROCm 6.3|
|9070xt|SDXL|20|1024x1024|FAIL|Crashed with out of memory|
|9070xt|SDXL|20|1024x1024|30.51s|Used tiled VAE decoder to avoid OOM failure|

Results 2:

Clean Ubuntu 24.04 installation
AMD proprietary drivers
Python 3.10.17
Pytorch nightly
ROCm 6.4.1

```
export PYTORCH_TUNABLEOP_ENABLED=1\
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export TORCH_COMMAND="--pre torch torchvision torchaudio pytorch-triton-rocm --index-url https://download.pytorch.org/whl/nightly/rocm6.4"

python ./main.py --use-pytorch-cross-attention 
```

|Model|Steps|Resolution|Speed|Time|Notes|
|-|-|-|-|-|-|
|SDXL|20|1024x1024|1.49it/s|34.56s||
|SDXL|20|1024x1024|1.5it/s|27.76s|Manual tiled VAE decoder|


### Operating System

Ubuntu 24.04

### CPU

AMD 7950x

### GPU

Radeon RX 9070xt

### ROCm Version

6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

- Install Ubuntu 24.04
- Install AMD proprietary drivers with ROCm
- Install Python 3.10.17
- Clone ComfyUI
- Start ComfyUI
- Use default workflow for SDXL

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (77 条)

### 评论 #1 — ppanchad-amd (2025-05-30T13:46:24Z)

Hi @alshdavid. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — chutchatut (2025-06-01T03:32:42Z)

Can confirm this is happening to me as well on workflow that used to work on 6700.

---

### 评论 #3 — alshdavid (2025-06-01T22:33:17Z)

Also related: https://github.com/comfyanonymous/ComfyUI/issues/7332

---

### 评论 #4 — Matthew-Jenkins (2025-06-05T01:41:39Z)

Prepend `MIOPEN_FIND_MODE=2` to your comfyui command. 

---

### 评论 #5 — alshdavid (2025-06-05T02:27:20Z)

@Matthew-Jenkins, appears to make no difference unfortunately:

With (baseline):

```
export PYTORCH_TUNABLEOP_ENABLED=1
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export TORCH_COMMAND="--pre torch torchvision torchaudio pytorch-triton-rocm --index-url https://download.pytorch.org/whl/nightly/rocm6.4"

python3.10 ./main.py --use-pytorch-cross-attention 
```

|Model|Steps|Resolution|Speed|Time|Notes|
|-|-|-|-|-|-|
|SDXL|20|1024x1024|1.49it/s|34.56s||
|SDXL|20|1024x1024|1.5it/s|27.76s|Manual tiled VAE decoder|

With:
```
export MIOPEN_FIND_MODE=2
export PYTORCH_TUNABLEOP_ENABLED=1
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export TORCH_COMMAND="--pre torch torchvision torchaudio pytorch-triton-rocm --index-url https://download.pytorch.org/whl/nightly/rocm6.4"

python3.10 ./main.py --use-pytorch-cross-attention 
```

|Model|Steps|Resolution|Speed|Time|Notes|
|-|-|-|-|-|-|
|SDXL|20|1024x1024|1.46it/s|34.74s||
|SDXL|20|1024x1024|1.48it/s|27.88s|Manual tiled VAE decoder|

I also tried to use the MIGraphX node however it either doesn't work with SDXL or there is an issue with my configuration. Raised an issue on their repo: https://github.com/pnikolic-amd/ComfyUI_MIGraphX/issues/5

---

### 评论 #6 — Matthew-Jenkins (2025-06-05T14:44:47Z)

9070 support wasn't added until 6.4.1. You'll have problems until pytorch nightly updates to use it. the hsa override can make it run as if it is a previous generation card. 

The next thing to try is the HSA_OVERRIDE_GFX_VERSION . Try 
MIOPEN_FIND_MODE=2 HSA_OVERRIDE_GFX_VERSION=11.0.0

if that doesn't work then try

MIOPEN_FIND_MODE=2 HSA_OVERRIDE_GFX_VERSION=10.3.0

Until pytorch updates to 6.4.1 you will not get any benefit from the ai cores. But once it does you can expect about 1.2TFLOPs for i4 ops.

---

### 评论 #7 — alshdavid (2025-06-06T00:09:39Z)

Thanks for the tips

> Try `MIOPEN_FIND_MODE=2 HSA_OVERRIDE_GFX_VERSION=11.0.0`
> if that doesn't work then try `MIOPEN_FIND_MODE=2 HSA_OVERRIDE_GFX_VERSION=10.3.0`

Just tried both of these, unfortunately no luck there.

> Until pytorch updates to 6.4.1 you will not get any benefit from the ai cores. 

Ah, well that's good news. Will keep an eye out on pytorch's progress

---

### 评论 #8 — kasper93 (2025-06-06T17:31:15Z)

@alshdavid you need this for comfyui to work correctly https://github.com/comfyanonymous/ComfyUI/pull/8289

---

### 评论 #9 — chutchatut (2025-06-07T10:47:40Z)

> [@alshdavid](https://github.com/alshdavid) you need this for comfyui to work correctly [comfyanonymous/ComfyUI#8289](https://github.com/comfyanonymous/ComfyUI/pull/8289)

I tried your commit with SDXL and VAE Decoder (Tiled) stills performs much worse than it used to on my old gpu(6700). Is that the same on your end?

Flag used: --use-pytorch-cross-attention

Edit: Never mind, had to turn off the experimental feature. But somehow the output image is gibberish with weird circular patterns.

Edit2: Using the newest torch from torch instead of amd fixed the weird circular patterns issue.

---

### 评论 #10 — kasper93 (2025-06-07T13:32:14Z)

For convolution workloads winograd solvers in miopen would help a lot, I asked about those here https://github.com/ROCm/MIOpen/issues/3750. Another issues is that GEMM  tuning for gfx1201 for seems to not be optimal by default for some workloads. And probably few other areas that could improve.

With ComfyUI changes I mentioned, `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1` and pytroch install from https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/ it should work "reasonable", meaning there are still a lot performance left on the table, but it's not completely broken anymore...

Using https://rocm.docs.amd.com/projects/hipBLASLt/en/latest/how-to-use-hipblaslt-offline-tuning.html can increase perf 2x in some cases.

---

### 评论 #11 — Loacoon1 (2025-06-08T17:57:38Z)

I'm having the same problem using pytorch-rocm with Chainner.
With my 6800XT, an inference took 17 while the same takes 28 seconds with 9070XT.

---

### 评论 #12 — alshdavid (2025-06-28T02:07:02Z)

Hey @kasper93, regarding this:

> and pytroch install from https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/ it should work "reasonable"

Are there docs on how to install PyTorch from here? 

I have no idea what `pip install` is doing or how Python resolves its dependencies so I don't know how to pick the archives and manually reproduce the `pip` installation. I've been using the `pip3 install` command from pytorch.org, which I assume installs the packages into some global packages folder in the venv folder. Do you just download & extract the archives there?

I tried the following but that doesn't work:
```
pip3 install https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/pytorch_triton_rocm-3.2.0%2Brocm6.4.1.git6da9e660-cp39-cp39-linux_x86_64.whl
```

Also, how do I know that ComfyUI is using those packages rather than the previously installed ones from pytorch.org?

Apparently, PyTorch [just added support for ROCm 6.4.1](https://github.com/pytorch/pytorch/issues/155292#issuecomment-3012269688) but either I am installing it wrong or it doesn't appear to make any difference. 



---

### 评论 #13 — kasper93 (2025-06-28T09:04:21Z)

@alshdavid: Keep expectations low, it's still slow in general. It works, but it seems you have overenthusiastic expectations for it.

See my comment https://github.com/ROCm/ROCm/issues/4846#issuecomment-2952494361

Also, if you workload is only SD, AMD recently updated migrapx node for comfyui. https://github.com/pnikolic-amd/ComfyUI_MIGraphX after compiling the model with it, you will get significantly higher perf, which may meet your expectations.

> Are there docs on how to install PyTorch from here?

https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html

But if upstream nightly pytorch support current version of rocm, you can use that directly.

---

### 评论 #14 — alshdavid (2025-08-08T02:13:39Z)

Not directly related but I just tried ComfyUI under Windows + latest HIP + Zluda on my 9070xt and performance is about the same as ROCm under Linux.

Generating an SDXL image with 1024x1024 resolution and 20 steps takes ~31 seconds (same as ROCm under Linux).

No OOM errors though, which is nice.

---

### 评论 #15 — Loacoon1 (2025-08-08T19:07:07Z)

So this is also a Windows issue and not necessarily Rocm related?! 
I'm honestly amazed at how bad software support is when it come to AI. The cards were released months ago now. Clearly this is my last AMD GPU....

---

### 评论 #16 — alshdavid (2025-08-08T22:52:58Z)

> So this is also a Windows issue and not necessarily Rocm related?!

This occurs both on Windows and Linux. [This thread](https://github.com/ROCm/ROCm/issues/5040) has some interesting insights. It also looks like [running an LLM using a Vulkan backend](https://www.youtube.com/shorts/pYciYq_qcFo) on the 9070xt shows a lot of potential so there's reason to be optimistic.

Looks like the ROCm 7.0 RC1 was cut a few hours ago so here's hoping that improves things. If I figure out how to install it (installing AI tools is madness) I'll report back. 

> Clearly this is my last AMD GPU....

I go back and forth on this too. I daily drive Linux and AMD GPUs have the best Linux support - otherwise I'd have gotten an nvidia 5080. It's quite frustrating that AMD's support for their own AI APIs is so poor. 

The recent "AI Max" APU with up to 96gb of ram sounds perfect for low cost/power efficient local LLM inference and perhaps even training/fine-tuning however it doesn't even support ROCm. It literally has AI in the name and can't run any AI workloads.

---

### 评论 #17 — Loacoon1 (2025-08-09T05:00:34Z)

Well FSR4 is not officially supported yet... DLSS4 is... so..... But yeah, AMD performs better than NV on Linux.  Still, this shouldn't happen! AMD promised much better performances with 9000 series for AI workloads and it's actually worse than previous gens and even makes the display server crash after LOTS of stuttering.

---

### 评论 #18 — FR-Mister-T (2025-08-11T00:12:33Z)

Hello,

I've 0 knowledge on how this work but I can give the workaround that worked out for me.

In comfyUI use the following nodes https://github.com/pollockjj/ComfyUI-MultiGPU

Completly restart the server

In you workflow use comfyui-multigpu VAE loader and setup the VAE device on the cpu...

I went from 560 seconds VAE decode on the GPU (_and whole computer is stuttering like a 2000's PC try to read a 4K movie_)
to a smooth 35/40 second for VAE decoding on CPU. (its the speed for 2 pics in 1024 res)



---

### 评论 #19 — alshdavid (2025-08-14T00:44:57Z)

I have just tried installing ROCm 7 beta on Fedora 42 via the RHEL repos and retried generating a 1024x1024 image with SDXL on ComfyUI.

Relatively easy to install:
https://www.youtube.com/watch?v=7qDlHpeTmC0
https://gist.github.com/B4rr3l-Rid3r/b03460860f2841144135c0fe8bede5be

....And it appears to perform identically to ROCm 6.4 on Linux. So no performance improvement and still slower than my 6900xt 🙄 


---

### 评论 #20 — dragonwise10 (2025-09-10T11:22:55Z)

Thank you for sharing your detailed analysis and benchmarks! I'm experiencing almost identical performance issues with my 9070XT in WSL - also getting around 30-31 seconds for 1024x1024 SDXL generation with 20 steps, which matches your results exactly.

It's somewhat reassuring to know this appears to be a common issue rather than something specific to my setup. The consistency of our results suggests this is indeed a broader compatibility or optimization problem that will likely require AMD's attention to resolve.

I appreciate you taking the time to document and report this issue. Hopefully AMD can address these performance concerns in future ROCm updates, as the 9070XT should theoretically perform much better than what we're currently seeing.

---

### 评论 #21 — Matthew-Jenkins (2025-09-10T13:01:21Z)

I'm interested in side by side benchmarks for the rx 9070 xt with rocm vs vulkan. If anyone could submit benchmarks with the same model but different quants, f16, q8, q4, iq4 that would really be very interesting to me. I've been on the fence to buy a 9070 to replace my 6900 xt.

---

### 评论 #22 — alshdavid (2025-09-10T21:05:11Z)

I'm also interested in Vulkan benchmarks too. I've seen some LLM perform incredibly well on the 9070xt under Vulkan which gives me hope. 

I've been trying to compile Pytorch to use a Vulkan backend but haven't been able to figure out their build process. The Vulkan backend is normally used for Android devices but IMO it would be helpful for getting GPU acceleration on under/unsupported devices (RDNA4, Strix Halo APUs, Intel GPUs, Snapdragon GPUs, etc).

I raised an issue on the pytorch repo asking them to release officially supported prebuilds of pytorch with a Vulkan backend https://github.com/pytorch/pytorch/issues/160230#issuecomment-3186343745

---

### 评论 #23 — Loacoon1 (2025-09-10T21:11:56Z)

IMO it would just be a placeholder anyway. 9000 series have dedicated AI capabilities that should, if software support wasn't abysmally bad, make them much faster than using Vulkan.
At that point I'm just considering selling my card and going back to team green. The release was 6 months ago! It feels like a bad joke considering that part of the marketing of these cards was based on their AI capabilities, but they are still basically unusable.

---

### 评论 #24 — alshdavid (2025-09-10T22:16:58Z)

What makes matters worse is my experiments with ROCm 7 doesn't seem to improve performance on my 9070xt. So much potential in these cards to kick ass but it doesn't look like we will see that materialize in the next 6 months.

I thought about switching to team green too but the 5080 doesn't seem worth the money with only 16gb RAM. In the meantime, I've been renting an Nvidia-powered VPS for ML workloads on-demand. It's like 60 cents an hour.

If the 5080 TI/Super comes out with 32gb then it's a no brainer  

---

### 评论 #25 — Matthew-Jenkins (2025-09-11T02:33:55Z)

> IMO it would just be a placeholder anyway. 9000 series have dedicated AI capabilities that should, if software support wasn't abysmally bad, make them much faster than using Vulkan. At that point I'm just considering selling my card and going back to team green. The release was 6 months ago! It feels like a bad joke considering that part of the marketing of these cards was based on their AI capabilities, but they are still basically unusable.

Vulkan shaders already run on the AI cores.

---

### 评论 #26 — alshdavid (2025-09-17T03:29:15Z)

I just tested official ROCm 7.0 with the ROCm fork of Pytorch

- Ubuntu 24.04
- Python 3.12.11
- ROCm 7.0 ([Installed from AMD](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#rocm-installation))
- Pytorch 2.8.0 ([Installed from AMD](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#rocm-installation))
- ComfyUI
- SDXL
- Image Size 1024 x 1024

Args: `python main.py`
Render time: 168s
Notes: Sometimes throws error: `HIP error: an illegal memory access was encountered`

<details>
<summary>Full Error</summary>
got prompt
!!! Exception during processing !!! HIP error: an illegal memory access was encountered
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

Traceback (most recent call last):
  File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 496, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 315, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 289, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 277, in process_inputs
    result = f(**inputs)
             ^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/ComfyUI/nodes.py", line 1525, in sample
    return common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/ComfyUI/nodes.py", line 1484, in common_ksampler
    noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/ComfyUI/comfy/sample.py", line 13, in prepare_noise
    generator = torch.manual_seed(seed)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/_compile.py", line 53, in inner
    return disable_fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 929, in _fn
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/random.py", line 46, in manual_seed
    torch.cuda.manual_seed_all(seed)
  File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/cuda/random.py", line 131, in manual_seed_all
    _lazy_call(cb, seed_all=True)
  File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/cuda/__init__.py", line 341, in _lazy_call
    callable()
  File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/cuda/random.py", line 129, in cb
    default_generator.manual_seed(seed)
torch.AcceleratorError: HIP error: an illegal memory access was encountered
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
</details>

Args `env PYTORCH_TUNABLEOP_ENABLED=1 TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python ./main.py --use-pytorch-cross-attention`
Render time: 6.65s 🥳 
Notes: First render takes 300-500 seconds. This happens when you first load a model, change models or change VAE decode settings. Would like to see this come down. The second render took 30 seconds. The third+ render takes 6 seconds

It's now twice as fast as my old 6900xt

---

### 评论 #27 — githust66 (2025-09-17T04:34:54Z)

20 steps？



---Original---
From: "David ***@***.***&gt;
Date: Wed, Sep 17, 2025 11:29 AM
To: ***@***.***&gt;;
Cc: ***@***.***&gt;;
Subject: Re: [ROCm/ROCm] [Issue]: Performance of 9070xt with ComfyUI (Issue#4846)


alshdavid left a comment (ROCm/ROCm#4846)
 
I just tested official ROCm 7.0 with the ROCm fork of Pytorch
  
Ubuntu 24.04
 
Python 3.12.11
 
ROCm 7.0 (Installed from AMD)
 
Pytorch 2.8.0 (Installed from AMD)
 
ComfyUI
 
SDXL
 
Image Size 1024 x 1024
  
Args: python main.py
 Render time: 168s
 Notes: Sometimes throws error: HIP error: an illegal memory access was encountered
  Full Error got prompt !!! Exception during processing !!! HIP error: an illegal memory access was encountered HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect. For debugging consider passing AMD_SERIALIZE_KERNEL=3 Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions. 
Traceback (most recent call last):
 File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 496, in execute
 output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 315, in get_output_data
 return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 289, in _async_map_node_over_list
 await process_inputs(input_dict, i)
 File "/home/dalsh/MachineLearning/ComfyUI/execution.py", line 277, in process_inputs
 result = f(**inputs)
 ^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/ComfyUI/nodes.py", line 1525, in sample
 return common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/ComfyUI/nodes.py", line 1484, in common_ksampler
 noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/ComfyUI/comfy/sample.py", line 13, in prepare_noise
 generator = torch.manual_seed(seed)
 ^^^^^^^^^^^^^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/_compile.py", line 53, in inner
 return disable_fn(*args, **kwargs)
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 929, in _fn
 return fn(*args, **kwargs)
 ^^^^^^^^^^^^^^^^^^^
 File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/random.py", line 46, in manual_seed
 torch.cuda.manual_seed_all(seed)
 File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/cuda/random.py", line 131, in manual_seed_all
 _lazy_call(cb, seed_all=True)
 File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/cuda/init.py", line 341, in _lazy_call
 callable()
 File "/home/dalsh/MachineLearning/.local/python/3.12.11/lib/python3.12/site-packages/torch/cuda/random.py", line 129, in cb
 default_generator.manual_seed(seed)
 torch.AcceleratorError: HIP error: an illegal memory access was encountered
 HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
 For debugging consider passing AMD_SERIALIZE_KERNEL=3
 Compile with TORCH_USE_HIP_DSA to enable device-side assertions.
  
Args env PYTORCH_TUNABLEOP_ENABLED=1 TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python ./main.py --use-pytorch-cross-attention
 Render time: 6.65s 🥳
 Notes: First render took 310 seconds
 
It's now twice as fast as my old 6900xt
 
—
Reply to this email directly, view it on GitHub, or unsubscribe.
You are receiving this because you are subscribed to this thread.Message ID: ***@***.***&gt;

---

### 评论 #28 — alshdavid (2025-09-17T04:39:35Z)

20 steps, same workflow/config as the other tests. I tried to get the MiGraphX node working but had no luck unfortunately.

90% of the time is spent in VAE decoding, getting around 4-5 it/sec

---

### 评论 #29 — alshdavid (2025-09-19T00:07:46Z)

First render takes 500 seconds. When I change models first render takes 500 seconds. When I change image sizes the first render takes 500 seconds.

Also I'm occasionally getting this error:
```
!!! Exception during processing !!! HIP error: an illegal memory access was encountered
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

Traceback (most recent call last):
  File "/mnt/data/MachineLearning/ComfyUI/execution.py", line 496, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/execution.py", line 315, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/execution.py", line 289, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/mnt/data/MachineLearning/ComfyUI/execution.py", line 277, in process_inputs
    result = f(**inputs)
             ^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/nodes.py", line 1525, in sample
    return common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/nodes.py", line 1492, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/sample.py", line 45, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/samplers.py", line 1161, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/samplers.py", line 1051, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/samplers.py", line 1036, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/samplers.py", line 1004, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/samplers.py", line 987, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/samplers.py", line 759, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/user/python/3.12.11/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/k_diffusion/sampling.py", line 220, in sample_euler_ancestral
    sigma_down, sigma_up = get_ancestral_step(sigmas[i], sigmas[i + 1], eta=eta)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/data/MachineLearning/ComfyUI/comfy/k_diffusion/sampling.py", line 70, in get_ancestral_step
    sigma_up = min(sigma_to, eta * (sigma_to ** 2 * (sigma_from ** 2 - sigma_to ** 2) / sigma_from ** 2) ** 0.5)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

---

### 评论 #30 — GreenShadows (2025-09-22T19:19:50Z)

> I'm also interested in Vulkan benchmarks too. I've seen some LLM perform incredibly well on the 9070xt under Vulkan which gives me hope.
> 
> I've been trying to compile Pytorch to use a Vulkan backend but haven't been able to figure out their build process. The Vulkan backend is normally used for Android devices but IMO it would be helpful for getting GPU acceleration on under/unsupported devices (RDNA4, Strix Halo APUs, Intel GPUs, Snapdragon GPUs, etc).
> 
> I raised an issue on the pytorch repo asking them to release officially supported prebuilds of pytorch with a Vulkan backend [pytorch/pytorch#160230 (comment)](https://github.com/pytorch/pytorch/issues/160230#issuecomment-3186343745)

https://www.phoronix.com/review/amd-rocm-7-strix-halo

<img width="1080" height="1790" alt="Image" src="https://github.com/user-attachments/assets/276ec917-d73c-44bf-b943-ee1e77c497b5" />

Reviews and independent tests show Vulkan beating ROCm by a wide margin, which is insane because it's generic code versus kernels optimized by the manufacturer itself. AMD needs to fix this. 

It makes me wonder if there isn't anyone testing in realistic scenarios, on products that consumers actually use.

---

### 评论 #31 — alshdavid (2025-09-23T22:34:47Z)

Testing under Windows:

**System**

|||
|-|-|
|Windows|10 22H2 Build: 19045.6332|
|AMD Driver|25.9.2|
|Python|[3.13.7 Standalone](https://github.com/astral-sh/python-build-standalone/releases/download/20250918/cpython-3.13.7+20250918-x86_64-pc-windows-msvc-install_only_stripped.tar.gz)|
|ROCm|Nightly 7|
|pytorch|[2.10.0a0+rocm7.9.0rc20250923](https://d2awnip2yjpvqn.cloudfront.net/v2)|

```powershell
$env:PYTORCH_TUNABLEOP_ENABLED=1 
$env:TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1

python ".\main.py" --use-split-cross-attention
```

**Settings**

Same as Linux test

|||
|-|-|
|Image Size|1024x1024|
|Steps|20|
|Sampler|euler_ancestral|
|Model|SDXL|
|Workflow|Default ComfyUI Bottle Prompt|

**Results**

|||||
|-|-|-|-|
|First Generation|562 seconds|11.25s/it|Error dialog popped up, but generation continued|
|Second Generation|13.52s|3.26it/s||
|Third Generation|15s|3.26it/s|Screen turned off and same error dialog popped up, but generation succeeded|
|Fourth Generation|FAIL|FAIL|HIP out of memory|

<img width="388" height="242" alt="Image" src="https://github.com/user-attachments/assets/5ed101ce-e9dc-43ec-b174-470145972923" />

<details>
  <summary>HIP out of memory error:</summary>

```
  Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
!!! Exception during processing !!! HIP out of memory. Tried to allocate 576.00 MiB. GPU 0 has a total capacity of 15.92 GiB of which 7.82 GiB is free. Of the allocated memory 7.10 GiB is allocated by PyTorch, and 500.08 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
Traceback (most recent call last):
  File "D:\MachineLearning\ComfyUI\comfy\sd.py", line 648, in decode
    out = self.process_output(self.first_stage_model.decode(samples, **vae_options).to(self.output_device).float())
                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\ComfyUI\comfy\ldm\models\autoencoder.py", line 211, in decode
    dec = self.decoder(dec, **decoder_kwargs)
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1777, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1788, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\MachineLearning\ComfyUI\comfy\ldm\modules\diffusionmodules\model.py", line 723, in forward
    h = self.up[i_level].upsample(h)
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1777, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1788, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\MachineLearning\ComfyUI\comfy\ldm\modules\diffusionmodules\model.py", line 114, in forward
    x = self.conv(x)
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1777, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1788, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\MachineLearning\ComfyUI\comfy\ops.py", line 143, in forward
    return super().forward(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\conv.py", line 548, in forward
    return self._conv_forward(input, self.weight, self.bias)
           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\conv.py", line 543, in _conv_forward
    return F.conv2d(
           ~~~~~~~~^
        input, weight, bias, self.stride, self.padding, self.dilation, self.groups
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 2.25 GiB. GPU 0 has a total capacity of 15.92 GiB of which 7.82 GiB is free. Of the allocated memory 7.21 GiB is allocated by PyTorch, and 388.14 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\MachineLearning\ComfyUI\execution.py", line 496, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\ComfyUI\execution.py", line 315, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\ComfyUI\execution.py", line 289, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "D:\MachineLearning\ComfyUI\execution.py", line 277, in process_inputs
    result = f(**inputs)
  File "D:\MachineLearning\ComfyUI\nodes.py", line 295, in decode
    images = vae.decode(samples["samples"])
  File "D:\MachineLearning\ComfyUI\comfy\sd.py", line 658, in decode
    pixel_samples = self.decode_tiled_(samples_in)
  File "D:\MachineLearning\ComfyUI\comfy\sd.py", line 580, in decode_tiled_
    (comfy.utils.tiled_scale(samples, decode_fn, tile_x // 2, tile_y * 2, overlap, upscale_amount = self.upscale_ratio, output_device=self.output_device, pbar = pbar) +
     ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\ComfyUI\comfy\utils.py", line 1012, in tiled_scale
    return tiled_scale_multidim(samples, function, (tile_y, tile_x), overlap=overlap, upscale_amount=upscale_amount, out_channels=out_channels, output_device=output_device, pbar=pbar)
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\utils\_contextlib.py", line 120, in decorate_context
    return func(*args, **kwargs)
  File "D:\MachineLearning\ComfyUI\comfy\utils.py", line 984, in tiled_scale_multidim
    ps = function(s_in).to(output_device)
         ~~~~~~~~^^^^^^
  File "D:\MachineLearning\ComfyUI\comfy\sd.py", line 578, in <lambda>
    decode_fn = lambda a: self.first_stage_model.decode(a.to(self.vae_dtype).to(self.device)).float()
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\ComfyUI\comfy\ldm\models\autoencoder.py", line 211, in decode
    dec = self.decoder(dec, **decoder_kwargs)
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1777, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1788, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\MachineLearning\ComfyUI\comfy\ldm\modules\diffusionmodules\model.py", line 723, in forward
    h = self.up[i_level].upsample(h)
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1777, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1788, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\MachineLearning\ComfyUI\comfy\ldm\modules\diffusionmodules\model.py", line 114, in forward
    x = self.conv(x)
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1777, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\module.py", line 1788, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\MachineLearning\ComfyUI\comfy\ops.py", line 143, in forward
    return super().forward(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\conv.py", line 548, in forward
    return self._conv_forward(input, self.weight, self.bias)
           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\MachineLearning\.local\python\3.13.0\Lib\site-packages\torch\nn\modules\conv.py", line 543, in _conv_forward
    return F.conv2d(
           ~~~~~~~~^
        input, weight, bias, self.stride, self.padding, self.dilation, self.groups
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 576.00 MiB. GPU 0 has a total capacity of 15.92 GiB of which 7.82 GiB is free. Of the allocated memory 7.10 GiB is allocated by PyTorch, and 500.08 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

Got an OOM, unloading all loaded models.
Prompt executed in 9.64 seconds
```

</details>

---

### 评论 #32 — alshdavid (2025-09-24T00:40:56Z)

After a few hours of experimenting with different flags, I haven't found a way to stop the memory related crashing.

Performance is ok if you're generating `768x768` or `768x512` images. Around 3s per generation. Anything higher and the OOM errors either crash the generation or crash Windows.

Imagine if the 9070xt shipped with 32gb of RAM - that would hide this error for most use cases 😝

If the Nvidia 5080 super/ti has 32gb of RAM, AMD better watch out - I would probably jump ship at that point.

---

### 评论 #33 — Loacoon1 (2025-09-24T08:22:55Z)

Yeah, same. 6 months and no decent software support. It's a very bad joke.

---

### 评论 #34 — mordekai2025 (2025-09-24T12:51:49Z)

 Simply use `--disable-smart-memory`

and

add two lines in the file main.py in ComfyUI folder (Create a backup before!):

```
import torch
torch.backends.cudnn.enabled = False
```

in where it belong to:
```
{}".format(args.oneapi_device_selector))

    if args.deterministic:
        if 'CUBLAS_WORKSPACE_CONFIG' not in os.environ:
            os.environ['CUBLAS_WORKSPACE_CONFIG'] = ":4096:8"

    import cuda_malloc

if 'torch' in sys.modules:
    logging.warning("WARNING: Potential Error in code: Torch already imported, torch should never be imported before this point.")

import torch
torch.backends.cudnn.enabled = False

import comfy.utils

import execution
import server
from protocol import BinaryEventTypes
import nodes
import comfy.model_management
import comfyui_version
import app.logger
import hook_breaker_ac10a0
```

With two workarounds combined:

No more OOM, can use VAE Decode normally, it's fast and smooth. No more heavy stuttering, extremely slowdowns during KSampler et cetera. The weirdest unstable memory management was gone as well. It was affected both on Windows and Linux, whatever which pytorch ROCm I use:
pytorch ROCm 6.4 Nightly for Fedora 42 WS (via official pytorch website)
pytorch ROCm 7.0.0 experimental for Windows 11 Pro (for the console outpot see below.)
Both ComfyUI ROCm installied via Stability Matrix App.

Disabling Smart Memory Management wasn't enough to solve everything at once. I had to go deeper for the long & blind trial-and-error until I've found an another culprit: torch.backends.cudnn.enabled

I am not a programmer/developer. Just a casual gamer. So I don't know what the last one meant for. Google Search never helped me in any way, neither Google Gemini or other assistants. I was on my own for the full time and blindly searched any websites like GitHub, Reddits and more until noticed one thing without any further explanation: torch.backends.cudnn.enabled

Google Gemini suggested me to add these lines in file main.py and ran ComfyUI for the experiment. A success!

It's the pure ComfyUI out of the box experience with pure basic workflows only.
Zero third party nodes
Zero modifications and more.
Zero special arguments for HIP, PYTORCH, MIOPEN etc.
Et cetera.

Other arguments used: --normal-vram --preview-method auto --use-pytorch-cross-attention --disable-xformers (and the added --disable-smart-memory )
FP16 by default depends on.

Performance Results:

SD 1.5 - 512x512 - Euler (Normal) -  20 Steps
```
loaded completely 14250.54951171875 1639.406135559082 True
100%|██████████| 20/20 [00:00<00:00, 20.64it/s]
Requested to load AutoencoderKL
loaded completely 13978.75 159.55708122253418 True
Prompt executed in 1.86 seconds
```

SDXL - 1024x1024 - Euler (Normal) -  20 Steps
```
Requested to load SDXL
loaded completely 14194.54951171875 4897.0483474731445 True
100%|██████████| 20/20 [00:04<00:00,  4.21it/s]
Requested to load AutoencoderKL
loaded completely 10655.75 159.55708122253418 True
Prompt executed in 7.27 seconds
```

ComfyUI ROCm Console output after Startup via Stability Matrix App (Windows):
```
Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 65112 MB
pytorch version: 2.10.0a0+rocm7.9.0rc20250923
AMD arch: gfx1201
ROCm version: (7, 1)
Set vram state to: NORMAL_VRAM
Disabling smart memory management
Device: cuda:0 AMD Radeon RX 9070 : native
Using pytorch attention
Python version: 3.12.11 (main, Jul 23 2025, 00:32:20) [MSC v.1944 64 bit (AMD64)]
ComfyUI version: 0.3.60
ComfyUI frontend version: 1.26.13
[Prompt Server] web root: D:\StabilityMatrix\Data\Packages\ComfyUI-ROCm\venv\Lib\site-packages\comfyui_frontend_package\static

Import times for custom nodes:
   0.0 seconds: D:\StabilityMatrix\Data\Packages\ComfyUI-ROCm\custom_nodes\websocket_image_save.py

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://127.0.0.1:8188
```






---

### 评论 #35 — Matthew-Jenkins (2025-09-24T13:04:06Z)

--disable-smart-memory is something I have to use even on my rx 6900 xt. I think comfys smart memory just does not work on amd. Disabling smart memory makes it so it doesn't try to move things in and out of gpu memory. It either all fits or it doesn't. 

---

### 评论 #36 — Hadrianneue (2025-09-25T00:50:03Z)

no sure if anyone had this same experience but using stuff like --use-pytorch-cross-attention, PYTORCH_TUNABLEOP_ENABLED=1 or TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 causes extremely lengthy workflow load, without any of that it loads/runs extremely fast... running with python 3.12 as its the same version packed with my system's rocm7 install

---

### 评论 #37 — ghost (2025-10-11T14:28:34Z)

Right, link after link i ended up here. As suggested above, using --disable-smart-memory and adding import torch & torch.backends.cudnn.enabled = False to main.py solved all the stalling issues i had. Any resolution works fine and quick now, not only a few odd ones.

Linux Mint, 7900 XTX, ROCm 7.0. All working fine now!

---

### 评论 #38 — mordekai2025 (2025-10-11T14:31:01Z)

Yes. It's the best workarounds so far until it's fixed. 

---

### 评论 #39 — alshdavid (2025-10-12T21:56:55Z)

I'm getting this error frequently

```
HIP error: an illegal memory access was encountered
```

<img width="965" height="475" alt="Image" src="https://github.com/user-attachments/assets/1298eb83-f68b-4d68-84c5-4f58bd9750d3" />

---

### 评论 #40 — kasper93 (2025-10-12T22:27:52Z)

> HIP error: an illegal memory access was encountered

At least it doesn't crash your whole gpu driver stack anymore.

---

### 评论 #41 — Loacoon1 (2025-11-10T11:19:34Z)

I see 7.1.0 has been released, any fix on this problem? 

---

### 评论 #42 — alshdavid (2025-11-10T22:55:20Z)

> I see 7.1.0 has been released, any fix on this problem?

No change unfortunately


---

### 评论 #43 — skillmaker-dev (2025-11-28T19:11:37Z)

I have tested the latest released driver for ROCm 7.1 on Windows, with the latest version of ComfyUI, all generations are working without stack overflow, without using `--disable-smart-memory` and using PyTorch cross attention on RX 9070 XT.

For Z-Image FP8, I can generate images 1024x1024 at 1.4it/s.
For SDXL, I can generate images 1024x1024 using Euler normal at 5it/s.

---

### 评论 #44 — mordekai2025 (2025-11-28T19:28:54Z)

It's because of `Set: torch.backends.cudnn.enabled = False for better AMD performance.` on ComfyUI's startup. I can generate SDXL images as well at 4.21 it/s with my RX 9070 on Windows. With PyTorch cross attention. So it didn't change much on my side. I'm still waiting for a proper fix. 

---

### 评论 #45 — Loacoon1 (2025-12-01T22:44:51Z)

No news from AMD devs for months, no fix for what should be considered a critical bug, all that for cards that have been advertised for their "amazing AI capabilities"! I'm pretty sure that the legality of all this is questionable...
Anyway, I guess I'm gonna ask for a refund and get back to team green. They lose performances on Linux gaming but at least it works...

---

### 评论 #46 — GreenShadows (2025-12-01T22:51:15Z)

@powderluv 
Why does solving critical problems seem to move at a snail's pace? That's ridiculous.

---

### 评论 #47 — jammm (2025-12-05T12:30:32Z)

> I have tested the latest released driver for ROCm 7.1 on Windows, with the latest version of ComfyUI, all generations are working without stack overflow, without using `--disable-smart-memory` and using PyTorch cross attention on RX 9070 XT.
> 
> For Z-Image FP8, I can generate images 1024x1024 at 1.4it/s. For SDXL, I can generate images 1024x1024 using Euler normal at 5it/s.

@skillmaker-dev Is your issue fixed?

---

### 评论 #48 — jammm (2025-12-05T12:31:58Z)

> No news from AMD devs for months, no fix for what should be considered a critical bug, all that for cards that have been advertised for their "amazing AI capabilities"! I'm pretty sure that the legality of all this is questionable... Anyway, I guess I'm gonna ask for a refund and get back to team green. They lose performances on Linux gaming but at least it works...

> [@powderluv](https://github.com/powderluv) Why does solving critical problems seem to move at a snail's pace? That's ridiculous.

@Loacoon1  @GreenShadows Can you explain the issues you're currently facing?



---

### 评论 #49 — jammm (2025-12-05T12:33:23Z)

@alshdavid can you try with the latest ROCm 7.1 ?

---

### 评论 #50 — alshdavid (2025-12-05T12:35:48Z)

> @alshdavid can you try with the latest ROCm 7.1 ?

Sure will test it out tomorrow (Australia time). Windows or Linux?

---

### 评论 #51 — jammm (2025-12-05T12:38:30Z)

> > [@alshdavid](https://github.com/alshdavid) can you try with the latest ROCm 7.1 ?
> 
> Sure will test it out tomorrow (Australia time). Windows or Linux?

Thanks! Let's try on both.

If you still face issues, please also consider trying the latest TheRock nightlies from https://github.com/ROCm/TheRock/blob/main/RELEASES.md#torch-for-gfx120x-all
```bash
python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ \
  --pre torch torchaudio torchvision
```

---

### 评论 #52 — jammm (2025-12-05T12:40:57Z)

> It's because of `Set: torch.backends.cudnn.enabled = False for better AMD performance.` on ComfyUI's startup. I can generate SDXL images as well at 4.21 it/s with my RX 9070 on Windows. With PyTorch cross attention. So it didn't change much on my side. I'm still waiting for a proper fix.

@mordekai2025 can you also try the latest TheRock nightlies as mentioned above?

---

### 评论 #53 — Loacoon1 (2025-12-05T13:40:30Z)

> [@Loacoon1](https://github.com/Loacoon1) [@GreenShadows](https://github.com/GreenShadows) Can you explain the issues you're currently facing?

Well the same issue everyone has been facing here. Very long inference time, heavy system stuttering and an eventual crash of the display server.

---

### 评论 #54 — skillmaker-dev (2025-12-05T13:51:34Z)

> > I have tested the latest released driver for ROCm 7.1 on Windows, with the latest version of ComfyUI, all generations are working without stack overflow, without using `--disable-smart-memory` and using PyTorch cross attention on RX 9070 XT.
> > For Z-Image FP8, I can generate images 1024x1024 at 1.4it/s. For SDXL, I can generate images 1024x1024 using Euler normal at 5it/s.
> 
> [@skillmaker-dev](https://github.com/skillmaker-dev) Is your issue fixed?

@jammm The issue I had with the driver crashing is no longer happening, however, when I try to generate a big resolution image (+1700px on height or width), the system becomes slow and stutters at the VAE step, but I can work around it by using a tiled VAE, but it doesn't crash, hopefully this issue is fixed too

---

### 评论 #55 — jammm (2025-12-05T13:56:41Z)

> Well the same issue everyone has been facing here. Very long inference time, heavy system stuttering and an eventual crash of the display server.

Is this on Linux or Windows?



> > [@skillmaker-dev](https://github.com/skillmaker-dev) Is your issue fixed?
> 
> [@jammm](https://github.com/jammm) The issue I had with the driver crashing is no longer happening, however, when I try to generate a big resolution image (+1700px on height or width), the system becomes slow and stutters at the VAE step, but I can work around it by using a tiled VAE, but it doesn't crash, hopefully this issue is fixed too

If you try to generate a larger image, it would exceed the VRAM and go into shared memory. That would explain the slow perf. As for the stuttering, that's probably happening because the GPU is being fully utilized across all shader cores. This is especially visible if you have youtube playing in the background for example. Tiled VAE helps because the tile sizes are small enough to fit within VRAM.



---

### 评论 #56 — Loacoon1 (2025-12-05T14:00:02Z)

> Is this on Linux or Windows?

On Linux.

---

### 评论 #57 — mordekai2025 (2025-12-05T14:07:04Z)

By default on ComfyUI was `Set: torch.backends.cudnn.enabled = False for better AMD performance.` I can generate images with SDXL, Pony and more normally with normal VAE decode.

After editing the file comfy/model_management.py with the specific lines to `Set: torch.backends.cudnn.enabled = True for testing :)`
SDXL Image can not be generated anymore as it's stuck at KSampler at 1024x1024
Same for other models like Pony and others. Can't get everything past. Hm...

I can't test Flux, WAN, AuraFlow and more on both states of CUDNN (enabled and disabled) so I am out of my testing possibilities as it didn't simply compute anything beyond that point. Stuttering or causing black screen and freeze (had 3x recently). 

Startup log:
`Total VRAM 16304 MB, total RAM 65112 MB
pytorch version: 2.10.0a0+rocm7.11.0a20251205
Set: torch.backends.cudnn.enabled = True for testing :)
AMD arch: gfx1201
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 : native
Enabled pinned memory 29300.0

Import times for custom nodes:
   0.0 seconds: D:\StabilityMatrix\Data\Packages\ComfyUI-ROCm\custom_nodes\websocket_image_save.py

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://127.0.0.1:8188`

During the installation of ComfyUI via Stability matrix, it took the latest ROCm libraries specially made for gfx120x GPU like my Radeon RX 9070 16GB.
That was on Windows 11 Pro x64 and Adrenaline 25.9.1 WHQL. Stability Matrix using the latest stable version as well. ComfyUI v0.3.76 Stable.

Gonna test on Fedora Workstation Linux to investigate the behaviour.

---

### 评论 #58 — jammm (2025-12-05T14:09:01Z)

@mordekai2025 I would not recommend `torch.backends.cudnn.enabled = True` for now. There's a good reason it was disabled, and that's because the VAE decode involves 3D convs which aren't supported yet for navi GPUs, so it would end up calling naive convs which are extremely slow.. So it's highly recommended you keep `torch.backends.cudnn.enabled = False`.

There's work ongoing in MIOpen that should fix this so we can eventually re-enable it. But it shouldn't be enabled for now.

---

### 评论 #59 — jammm (2025-12-05T14:14:25Z)

> > Is this on Linux or Windows?
> 
> On Linux.

Does this only happen when you try running larger resolutions? As for the crash, what's the errors you see? Is it memory access fault?

---

### 评论 #60 — Loacoon1 (2025-12-05T14:22:58Z)

I'm testing (well was trying to) upscaling and photo enhancement models I've trained with Chainner, so it's always large images. 
In which log should I see what the error is? Xorg's one?

---

### 评论 #61 — slojosic-amd (2025-12-05T14:33:12Z)

Could you please try to add `amdgpu.cwsr_enable=0` to the kernel command line? https://github.com/ROCm/TheRock/issues/1795#issuecomment-3530012896 

---

### 评论 #62 — mordekai2025 (2025-12-05T14:45:23Z)

> [@mordekai2025](https://github.com/mordekai2025) I would not recommend `torch.backends.cudnn.enabled = True` for now. There's a good reason it was disabled, and that's because the VAE decode involves 3D convs which aren't supported yet for navi GPUs, so it would end up calling naive convs which are extremely slow.. So it's highly recommended you keep `torch.backends.cudnn.enabled = False`.
> 
> There's work ongoing in MIOpen that should fix this so we can eventually re-enable it. But it shouldn't be enabled for now.

Okay. Good to know. I am back to the most working state with `torch.backends.cudnn.enabled = False`.




---

### 评论 #63 — Loacoon1 (2025-12-05T15:20:07Z)

> Could you please try to add `amdgpu.cwsr_enable=0` to the kernel command line? [ROCm/TheRock#1795 (comment)](https://github.com/ROCm/TheRock/issues/1795#issuecomment-3530012896)

Ok Done. I can't reboot right now but I'll try ASAP. Can it create problems on other workflows like gaming for example though? I see that it is supposed to prevent GPU hangs basically so....

---

### 评论 #64 — TheBakusaiga (2025-12-05T16:38:20Z)

> Could you please try to add `amdgpu.cwsr_enable=0` to the kernel command line? [ROCm/TheRock#1795 (comment)](https://github.com/ROCm/TheRock/issues/1795#issuecomment-3530012896)

OH MY GOD
you just saved my sanity. this actually fixed the problem for me. atleast so far. will continue testing but i've already run quite a few workflows without encountering the lovely "Memory access fault by GPU node-1"

---

### 评论 #65 — alshdavid (2025-12-05T22:13:53Z)

# Windows:

**System**

|||
|-|-|
|Windows|10 22H2 Build: 19045.6466|
|AMD Driver|25.11.1|
|Python|[3.13.9 Standalone](https://github.com/astral-sh/python-build-standalone/releases/download/)|
|ROCm|Nightly 7.2|
|pytorch|2.10.0a0+rocm7.11.0a20251205|

No arguments, just launching ComfyUI with latest `master` and no custom nodes/loras/etc.

```powershell
python ".\main.py"
```

Installed pytorch with
```powershell
python -m pip install --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ --pre torch torchaudio torchvision
```

<details>
<summary>Command Output</summary>

```
$ comfyui

Set cuda device to: 1
Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 97446 MB
pytorch version: 2.10.0a0+rocm7.11.0a20251205
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1201
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Enabled pinned memory 43850.0
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
Python version: 3.13.9 (main, Oct 14 2025, 21:22:32) [MSC v.1944 64 bit (AMD64)]
ComfyUI version: 0.3.76
ComfyUI frontend version: 1.33.10
[Prompt Server] web root: D:\MachineLearning\ComfyUI\share\python\Lib\site-packages\comfyui_frontend_package\static
Total VRAM 16304 MB, total RAM 97446 MB
pytorch version: 2.10.0a0+rocm7.11.0a20251205
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1201
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Enabled pinned memory 43850.0
Skipping loading of custom nodes
Failed to initialize database. Please ensure you have installed the latest requirements. If the error persists, please report this as in future the database will be required: (sqlite3.OperationalError) unable to open database file
(Background on this error at: https://sqlalche.me/e/20/e3q8)
Starting server

To see the GUI go to: http://127.0.0.1:8188
```

</details>

**Settings**

|||
|-|-|
|Image Size|1024x1024|
|Steps|20|
|Sampler|euler_ancestral|
|Model|SDXL|
|Workflow|Default ComfyUI Bottle Prompt|

**Results**

|||
|-|-|
|First Generation|32.76 seconds|
|Second Generation|8.71s|
|Third Generation|8.72s|
|Fourth Generation|8.68s|


---

Using the following reduced the second+ generation time to `7.7s`

```powershell
python main.py --use-pytorch-cross-attention
```

Using the following crashed my computer (hard shutdown/power off)

```powershell
$env:PYTORCH_TUNABLEOP_ENABLED=1 
$env:TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1

python main.py --use-pytorch-cross-attention

# Also happens with this:
python main.py --use-split-cross-attention
```

WAN via https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne would not complete with 512x512, 8 fps and 16 frames

---

### 评论 #66 — alshdavid (2025-12-05T23:42:12Z)

# Linux:

**System**

```bash
$ lsb_release -a

LSB Version:    n/a
Distributor ID: Fedora
Description:    Fedora Linux 43 (KDE Plasma Desktop Edition)
Release:        43
Codename:       n/a

$ uname -a

Linux DESKTOP-3NHK9OO 6.17.9-300.fc43.x86_64 #1 SMP PREEMPT_DYNAMIC Mon Nov 24 23:31:27 UTC 2025 x86_64 GNU/Linux
```
|||
|-|-|
|Fedora|43 |
|AMD Driver|Default|
|Python|[3.13.11 Standalone](https://github.com/astral-sh/python-build-standalone/releases/download/)|
|ROCm|Nightly 7.1|
|pytorch|2.10.0a0+rocm7.10.0a20251015|

Looks like installing pytorch with `--pre` results in the same version being installed as without.

No arguments, just launching ComfyUI with latest `master` and no custom nodes/loras/etc.

<details>
<summary>Command Output</summary>

```
$ comfyui

Set cuda device to: 0
Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 95697 MB
pytorch version: 2.10.0a0+rocm7.10.0a20251015
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1201
ROCm version: (7, 1)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Enabled pinned memory 90912.0
Using pytorch attention
Python version: 3.13.11 (main, Dec  5 2025, 20:22:32) [Clang 21.1.4 ]
ComfyUI version: 0.3.76
ComfyUI frontend version: 1.33.10
[Prompt Server] web root: /mnt/storage/MachineLearning/ComfyUI/share/python-linux/lib/python3.13/site-packages/comfyui_frontend_package/static
Total VRAM 16304 MB, total RAM 95697 MB
pytorch version: 2.10.0a0+rocm7.10.0a20251015
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1201
ROCm version: (7, 1)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Enabled pinned memory 90912.0
Skipping loading of custom nodes
Failed to initialize database. Please ensure you have installed the latest requirements. If the error persists, please report this as in future the database will be required: (sqlite3.OperationalError) unable to open database file
(Background on this error at: https://sqlalche.me/e/20/e3q8)
Starting server

To see the GUI go to: http://127.0.0.1:8188
```

</details>

**Settings**

|||
|-|-|
|Image Size|1024x1024|
|Steps|20|
|Sampler|euler_ancestral|
|Model|SDXL|
|Workflow|Default ComfyUI Bottle Prompt|

**Results**

|||
|-|-|
|First Generation|13.30 seconds|
|Second Generation|9.14s|
|Third Generation|8.96s|
|Fourth Generation|9.03s|

WAN video generation (https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne) failed after 1hr with the message:

```
Memory access fault by GPU node-1 (Agent handle: 0x3cca2d00) on address 0x7f7d1a00a000. Reason: Page not present or supervisor privilege.
GPU core dump created: gpucore.15665
./bin/comfyui: line 19: 15665 Aborted                    (core dumped) "$LocalPath/share/python-linux/bin/python" "$LocalPath/share/comfyui/main.py" "${comfyArgs[@]}"
```

---

### 评论 #67 — Loacoon1 (2025-12-08T22:36:18Z)

> Could you please try to add `amdgpu.cwsr_enable=0` to the kernel command line? [ROCm/TheRock#1795 (comment)](https://github.com/ROCm/TheRock/issues/1795#issuecomment-3530012896)

So, it doesn't seem to crash anymore and stutters a LOT less. So this is one thing solved, but this is still awfully slow.

---

### 评论 #68 — Loacoon1 (2026-01-04T04:57:25Z)

And now we have those hangs or hard crashes on heavy usage since kernel 6.17.9 and up... I have a 800€ 9070XT sitting in it's box while I've had to buy a 450€ 5060TI in emergency to just use my computer! 
"But AMD is the best on Linux"... yeah sure... Thanks AMD, never again!

---

### 评论 #69 — RadeonVega-56 (2026-01-05T15:04:35Z)

> And now we have those hangs or hard crashes on heavy usage since kernel 6.17.9 and up... I have a 800€ 9070XT sitting in it's box while I've had to buy a 450€ 5060TI in emergency to just use my computer!
> "But AMD is the best on Linux"... yeah sure... Thanks AMD, never again!

look here for workarounds and fixes: https://github.com/ROCm/ROCm/issues/5833 , https://github.com/ROCm/ROCm/issues/4742

Using those fixes i can generate faster than RTX 4080 and RTX 5070 Ti in comfyui flux image generation.

SD1.5 runs at 24 it/sec. at 512x512, SDXL at 15 it/sec.at 512x512, flux-dev 1.02 it/sec at 1440x810, flux2_fp8 4.24 s/it at 1440x810.

Benchmark example for RTX 4080 Super: https://civitai.com/articles/8309/flux1-fp16-vs-fp8-time-difference-on-rtx-4080-super-in-comfyui

Example for 9070 XT: My Prompt, flux-1-dev_fp8, 2 LoRAs, 1440x810, 42 steps, euler, simple, upscale with lanczos to 3840x2160 takes 46.80 seconds. 

Direct apples-to-apples: Prompt and seed from benchmark link above: flux-dev with fp8, 1024x1024, 40 steps, euler, simple, no upscale takes 34.42 seconds.

RTX 4080 Super: flux-dev with fp8,1024x1024, 40 steps, euler, simple, no upscale takes 44.04 seconds.

10 seconds faster than RTX 4080 Super.

RX 9070 XT: Prompt and seed from benchmark link above: flux-dev with default weight type, 1024x1024, 40 steps, euler, simple, no upscale takes 45.64 seconds. (model weight dtype torch.bfloat16)

RTX 4080 Super: flux-dev with fp16,1024x1024, 40 steps, euler, simple, no upscale takes 66.75.

That is 21 seconds faster than RTX 4080 Super. 

<img width="2560" height="1194" alt="Image" src="https://github.com/user-attachments/assets/79d192af-ed63-4ffa-91bd-3e7205aafbca" />

Generation speed varies a bit. If you generate more images and switch the weigths around, generation gets a bit faster. The latest image i generated was 26.01 seconds, benchmark settings, default weight type, 20 steps. The image after that, the 3rd image, only takes 23.76 seconds. -> RTX 4080 Super: 37.53 seconds.


<img width="2560" height="1194" alt="Image" src="https://github.com/user-attachments/assets/2553e46c-5b38-402f-bc64-02c197bbc71d" />



More Benchmarks: https://www.promptingpixels.com/gpu-benchmarks

But if you want to get the "Full Nvidia experience" go ahead and use that flimsy RTX card. :-P 

---

### 评论 #70 — RadeonVega-56 (2026-01-07T13:29:38Z)

I downloaded the flux1-dev.safetensors file because my flux-dev.saftensor file i used above is several years old. After further debugging i found a another flux workflow in the examples and i got these results using my updated settings https://github.com/ROCm/ROCm/issues/5833#issuecomment-3718504872 :

<img width="2560" height="1197" alt="Image" src="https://github.com/user-attachments/assets/35b7e8c8-0d31-4e30-85eb-5b2233eb0598" />

<img width="2560" height="1196" alt="Image" src="https://github.com/user-attachments/assets/96973fe2-b72a-43b5-8b8e-533d6448171c" />

Regarding this phrase from the benchmark i posted before:

> Note: Each test excludes the time taken to load the model. The reported generation times refer only to the time within kSampler.

He only wrote down the sample times. The time values i posted are for the complete worklow including everything. Look at my posted images, you can see the ksampler time in the terminal in the lower right corner.

---

### 评论 #71 — Loacoon1 (2026-02-01T13:38:01Z)

Ok so, since I got time I tried your settings.
One positive note, inference time is more stable.
As for the rest, well it's horribly slow.
With you settings, 3:35 to 3:40, without them, first inference at 2:35, others between 65 seconds and 1:40 minutes.
Fan speed with your settings 650RPM, without 1500RPM. 
Seems like the GPU is waiting for the CPU as a thread is always maxed out.
So no, no miracles here.

EDIT: I've been making some tests and I actually owe you an apology. Only one export caused that issue. When removed, it actually works pretty fine. A constant 66 seconds for the inference which is about 15 seconds faster than the RTX5060TI 16GB.
In case someone has the same issue here is the culprit:
export MIOPEN_CHECK_NUMERICS=0x02
Just remove it, and everything will work as intended.
Now, let's just hope that it doesn't crash the whole system at some point since this OTHER issue doesn't seem to be resolved.

EDIT2: It works on some models, not others. Changing the model, the crashes are even more frequent as well as slow inference. 

EDIT3: The 'export PYTORCH_TUNABLEOP_ENABLED="1"' is causing the crashes with no gain in speed whatsoever. It can safely be removed. With that, it seems stable, but some models are as fast as expected, others remain quite slow, though not as slow as without these settings, and the duration is much more stable. Overall it's a win, but we're still waiting for a real fix, that seems to have been put very low on the priority list. I mean, how urgent can "things not working" be? Right AMD?

---

### 评论 #72 — alshdavid (2026-02-01T20:41:46Z)

Seems good to me now.

Windows:
- Windows 10
- ROCm 7.12

Flags:
```
--use-pytorch-cross-attention
--disable-smart-memory
```

|Card|Model|Steps|Resolution|Time|
|-----|------|------|----------|----|
|6900xt|SD1.5|20|512x512|2.42s|
|9070xt|SD1.5|20|512x512|1.92s|
|6900xt|SDXL|20|1024x1024|15.16s|
|9070xt|SDXL|20|1024x1024|7.04s|

Linux:
- Fedora 43
- Rocm 7.12

Flags:
```
--use-pytorch-cross-attention
--disable-smart-memory  # crashes without this
```

|Card|Model|Steps|Resolution|Time|
|-----|------|------|----------|----|
|6900xt|SD1.5|20|512x512|2.42s|
|9070xt|SD1.5|20|512x512|1.56s|
|6900xt|SDXL|20|1024x1024|15.16s|
|9070xt|SDXL|20|1024x1024|5.56s|

---

### 评论 #73 — RadeonVega-56 (2026-02-12T19:15:04Z)

I revised my settings some more and it is now faster than before.

Software:
Nobara Linux 43, KDE version
ROCM 7.1.1
Python 3.12
Pytorch 2.10
ComfyUI

Hardware: 
CPU: Ryzen 9 9950X
RAM: Kingston KF560C32RSK2-96, 96 GB DDR5-6000
Motherboard: MSI X670E Gaming Plus WIFI
GPU: Sapphire Pulse Radeon RX 9070 XT

-------------------------------------------

**_.bash.rc settings:_**

export ROCM_PATH=/usr
export HIP_PATH=$ROCM_PATH
export PATH="$ROCM_PATH/bin:$PATH"
export LD_LIBRARY_PATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$LD_LIBRARY_PATH"
export PYTHONPATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$PYTHONPATH"

export HIP_CLANG_PATH=/usr/lib64/rocm/llvm/bin
export DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HIP_DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HSA_PATH=/usr
export LLVM_PATH=/usr/lib64/rocm/llvm/bin

export MIOPEN_USER_DB_PATH="$HOME/.cache/miopen"
export MIOPEN_CUSTOM_CACHE_DIR=${MIOPEN_USER_DB_PATH}

export ROCBLAS_TENSILE_LIBPATH="$ROCM_PATH/lib64/rocblas/library"

export HIP_PLATFORM=amd
export HIP_RUNTIME=rocclr
export HIP_COMPILER=clang

export HSA_OVERRIDE_GFX_VERSION=12.0.1
export PYTORCH_ROCM_ARCH=gfx1201
export GFX_ARCH=gfx1201
export USE_ROCM=1

----------------------------------------------------------------------

**_comfyui launch script:_**

#!/bin/bash
cd ComfyUI/
source my312_venv/bin/activate

export HIP_VISIBLE_DEVICES=0
export ROCM_VISIBLE_DEVICES=0
export HIP_TARGET="gfx1201"
export TORCH_HIP_ARCH_LIST="gfx1201"
export HCC_AMDGPU_TARGET="gfx1201"
export PYTORCH_ROCM_ARCH="gfx1201"

export MESA_LOADER_DRIVER_OVERRIDE=amdgpu
export RADV_PERFTEST="aco,nggc,sam"

export PYTORCH_HIP_ALLOC_CONF="max_split_size_mb:6144,garbage_collection_threshold:0.6"
export PYTORCH_HIP_FREE_MEMORY_THRESHOLD_MB=128
export PYTORCH_ALLOC_CONF=expandable_segments:True

export TORCH_COMPILE=1

export PYTORCH_TUNABLEOP_ENABLED="1"
export PYTORCH_TUNABLEOP_TUNING="1"
export PYTORCH_TUNABLEOP_FILENAME="tunableop_results0.csv"

export TORCH_DEVICE_BACKEND_AUTOLOAD=1

export TORCH_BLAS_PREFER_HIPBLASLT=1
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS="CK,TRITON,ROCBLAS"
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_SEARCH_SPACE="BEST"
export TORCHINDUCTOR_FORCE_FALLBACK=1
export TORCHINDUCTOR_CPP_WRAPPER=1
export TORCHINDUCTOR_FREEZING=1

export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
#export FLASH_ATTENTION_TRITON_AMD_AUTOTUNE="TRUE"
export FLASH_ATTENTION_BACKEND="flash_attn_triton_amd"
export FLASH_ATTENTION_TRITON_AMD_SEQ_LEN=4096
export USE_CK=ON
export TRANSFORMERS_USE_FLASH_ATTENTION=1

export TRITON_USE_ROCM=ON
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1

export OMP_NUM_THREADS=12
export MKL_NUM_THREADS=12
export NUMEXPR_NUM_THREADS=12

export AMD_DIRECT_DISPATCH=1
export TORCH_NCCL_HIGH_PRIORITY=1
export GPU_MAX_HW_QUEUES=16

export HSA_ENABLE_ASYNC_COPY=1
export HSA_ENABLE_SDMA=1
export HSA_ENABLE_PEER_SDMA=1
export HSA_ENABLE_SDMA_COPY=1
export HSA_ENABLE_SDMA_KERNEL_COPY=1
export HSA_FORCE_FINE_GRAIN_PCIE=1

export MIOPEN_ENABLE_AI_IMMED_MODE_FALLBACK=ON
export MIOPEN_FIND_ENFORCE=3
export MIOPEN_FIND_MODE=6
export MIOPEN_ENABLE_CACHE=1
export MIOPEN_CHECK_NUMERICS=0x02
export MIOPEN_CONV_WINOGRAD=1
export MIOPEN_DEBUG_CONV_FFT=0
export MIOPEN_ENABLE_LOGGING_CMD=0
export MIOPEN_DEBUG_CONV_IMPLICIT_GEMM=1

export HIP_FORCE_DEV_KERNARG=1

export ROCBLAS_STREAM_ORDER_ALLOC=1

export ROCBLAS_INTERNAL_FP16_ALT_IMPL=1
export ROCBLAS_LAYER=0
export ROCBLAS_INTERNAL_USE_SUBTENSILE=1

export SAFETENSORS_FAST_GPU=1

python main.py --disable-cuda-malloc --fast fp16_accumulation fp8_matrix_mult autotune --use-pytorch-cross-attention --cache-lru 4 --reserve-vram 0.8 --preview-method none --listen --port 8188

---------------------------------------------------------

**_additional kernel startup arguments:_**

amdgpu.ppfeaturemask=0xffffffff amdgpu.mcbp=0 amdgpu.cwsr_enable=0 amdgpu.queue_preemption_timeout_ms=1 iommu=pt amd_iommu=force_isolation amd_iommu=on

-----------------------------------------------------------

**_additional linux packages installed:_**

sudo dnf install google-benchmark-devel glfw-devel rocthrust-devel rocsparse-devel rocsolver-devel rocfft-devel rocblas-devel hipsolver-devel hipfft-devel hipblas-devel hiprand-devel hipcub-devel

sudo dnf install libavcodec-freeworld.x86_64 libavcodec-freeworld.i686

sudo dnf install rocm-llvm vulkan-loader-devel clblast clblast-devel mesa-libOpenCL-devel

-----------------------------------------------------------

**_additional python packages installed in comfyui venv:_**

pip install matplotlib pandas simpleeval wheel wheel_stub setuptools ninja

----------------------------------------------------

How this works:

----------------------------------------------------

Speed optimization:

Using the above settings for 

export MIOPEN_FIND_ENFORCE=3

and 

export MIOPEN_FIND_MODE=6

and

export PYTORCH_TUNABLEOP_TUNING="1"

will result in a very slow generation on the first run. Usually i set these and then startup comfyui. In the default startup workflow just hit the "RUN" button. You will generate SD1.5 images, the first one can take quite long. When it is finished swap the model for any SDXL model and hit run again. When finished both SD1.5 and SDXL is optimized. 

You can then open another workflow. 

I will usually then continue with the flux-dev fp8 workflow and let that run once or twice. After that i load up flux-dev workflow and do the same there. After that i load flux.2 fp8 workflow, it is called "product mockup Flux.2 fp8" in the templates. 

All of these need to run once to get optimised for fastest image generation. And that can take a loooong time, really.

After you ran all your needed workflows once go to the comfyui console and close the server by pressing CTRL+C.

Speed optimization is now done for the models and image sizes you just ran.

-------------------

Then open your comfyui startup script to edit it once more.

Set

export MIOPEN_FIND_ENFORCE=1

and

export MIOPEN_FIND_MODE=2

and

export PYTORCH_TUNABLEOP_TUNING="0"

This will set these variables to the fastest possible setting i found so far.

Startup the server again with the altered script will get you faster startup times for image generation.

The thing is as soon as you use a model you have not used before with FIND_ENFORCE=3 and FIND_MODE=6 and PYTORCH_TUNABLEOP_TUNING="1" it will take longer on the first run. Entering a different image size than the one you optimized will get you a longer first run.

If you want to optimize another workflow you have to set FIND_ENFORCE=3 and FIND_MODE=6 and PYTORCH_TUNABLEOP_TUNING="1" again and let those run in addition to the other workflows. Then set FIND_ENFORCE=1 and FIND_MODE=2 and PYTORCH_TUNABLEOP_TUNING="0" again to get more speed.

--------------------------

You will lose your optimization data if you update to a newer version of Pytorch. In that case you have to repeat the optimization.

--------------------------

You will lose your optimization data if you keep FIND_ENFORCE=3 and FIND_MODE=6 and PYTORCH_TUNABLEOP_TUNING="1" AND restart the ComfyUI server.

In that case optimization has to be repeated. Only use those values for the optimization, then stop the server and set those to FIND_ENFORCE=1 and FIND_MODE=2 and PYTORCH_TUNABLEOP_TUNING="0" for the fastest possible speed.

----------------------------

Example:  The first image SD1.5 in optimizing stage takes 1166 seconds for the full image. The second image takes 0.92 seconds, the third image 0.87 seconds. Using the same default workflow i just switch the model to SDXL. First image takes 7.91 seconds, second image 1.25 seconds, third image 1.25 seconds. Now the default workflow with SD1.5 and SDXL is optimized for the default image size of 512x512.

Flux1 is much slower on the first image. It usually takes about 2 hours for the first image to appear, Flux2 is even slower, can take almost 3 hours for the first image. But when optimized it is very fast afterwards. Then stop the server, edit the script to FIND_ENFORCE=1 and FIND_MODE=2 and PYTORCH_TUNABLEOP_TUNING="0" and restart. Now you have the optimized speed right at the beginning of your session and it stays that way. In my case it got even faster after generating more images of different sizes and using loras on top. However all your optimizations will be lost when you upgrade pytorch and you have to edit the script again and start optimizing again.

Example picture from optimizing flux.2-fp8 model:

<img width="2559" height="1139" alt="Image" src="https://github.com/user-attachments/assets/fd1d6e98-fdfb-4e3d-86b5-5b59a6cc7ce1" />


The first image took 5178 seconds to complete, second image 296 seconds, third image 284 seconds. Then in switched the weight type from "default" to "fp8_e4m3fn_fast". This sped up the VAE econding. The fourth image took 122 seconds, the fifth 83 seconds, sixth image 118 seconds. And that is only because i already had optimization data from the previous torch version i used. If you start it up after a fresh installation it will take almost double the amount of time. It almost eats up my whole memory. 90 GB of 96 GB is being used and all available GPU memory too by ComfyUI.

-------------------------------

On my system and SD1.5 i started with about 24 it/sec some weeks ago. Now with optimized settings and new kernel 6.18.9-201 it runs at 28 it/sec. SDXL 15 it/sec went up to around 18 it/sec.

----------------------------------

Pages for reference i found:

https://rocm.docs.amd.com/projects/MIOpen/en/latest/how-to/find-and-immediate.html

https://rocm.docs.amd.com/projects/MIOpen/en/develop/conceptual/perfdb.html

https://www.reddit.com/r/comfyui/comments/1nuipsu/finally_my_comfyui_setup_works/

https://gist.github.com/B4rr3l-Rid3r/b03460860f2841144135c0fe8bede5be

https://www.reddit.com/r/ROCm/comments/1jflgg8/rocm_path_and_library_locations_on_fedora/

https://wiki.archlinux.org/title/AMDGPU#Overclocking

--------------------------------------

Using "--disable-smart-memory" results in a memory leak. On each consequential run in flux1 workflows for example the usable memory displayed when generating a new image will be reduced by a small amount leading to a "HIP out of memory" error eventually.

Another variable i found is the browser you use for ComfyUI. I tried the official Firamdgpu.queue_preemption_timeout_ms=1efox browser from the Nobara/Fedora repo and i got frequent crashes using ComfyUI. Then i switched to the ESR version of the Firefox browser and those crashes are gone since then. Turning off hardware acceleration in the browser settings helped further to prevent crashes.

Installed it with snap:

 sudo dnf install snapd

sudo ln -s /var/lib/snapd/snap /snap

sudo snap install firefox --channel=esr/stable

Reference:

https://discussion.fedoraproject.org/t/firefox-esr-for-fedora/79871

-------------------------------------------------

If you are still crashing you should debug with a new terminal running "sudo dmesg". If you get errors they will display there at the end of the output in RED colour. Using the new kernel is still unstable but a bit faster on my machine. To run ComfyUI without any crashes i still have to use kernel version 6.17.12-200. There are warnings still present in my dmesg output in BLUE colour.

-------------------------------------------------

After more testing i found that setting "export HSA_ENABLE_SDMA=0" converted all of my errors into warnings on the latest Nobara kernel 6.19.5-200 and the crashes are gone.

With the latest Kernel 7.0.0-200 i removed the kernel option "amdgpu.queue_preemption_timeout_ms=1" to prevent hangs and garbled output. After some testing it still crashes with the new kernel as well. Kernel 6.19.5-200 works but i still kept kernel 6.17.12-200 to run comfyui because it just works perfect. There are even minor image generation speed updates which i think are related to the updated graphics drivers.

---

### 评论 #74 — Penguin-Guru (2026-04-21T23:59:34Z)

> Could you please try to add `amdgpu.cwsr_enable=0` to the kernel command line? [ROCm/TheRock#1795 (comment)](https://github.com/ROCm/TheRock/issues/1795#issuecomment-3530012896)

I _believe_ this is what _mostly_ stopped my O.S. from locking up, but I've been testing several environmental variables as well so I'm not sure yet. My system still _often_ stuttered heavily during certain parts of most, if not all, the ComfyUI workflow I tried. If I tried to do things while it was stuttering, especially making any windows full-screen, that seemed to increase the chances of a system lock-up substantially. That was mostly tested with `--reserve-vram 0.2` and `--use-flash-attention`. The (tiled) VAE decode was still taking a very long time, but the directions in the comment cited below seem to have resolved that (so far). Both the `--disable-smart-memory` and the code change were necessary-- neither helped independently. I have yet to confirm whether the stuttering behaviour and risk of lock-up have reliably changed.

> Simply use `--disable-smart-memory`
> 
> and
> 
> add two lines in the file main.py in ComfyUI folder (Create a backup before!):
> 
> ```
> import torch
> torch.backends.cudnn.enabled = False
> ```

---

Also, for the record, a lot of us really appreciate what A.M.D. is doing for the open-source community. Having perfect software and firmware when new products launch would obviously be ideal but just the fact that we're here talking about this is a solid step above Nvidia in my opinion. I'm also satisfied with my card's current performance, although I do hope it continues to improve with updates.


---

### 评论 #75 — RadeonVega-56 (2026-04-23T08:53:40Z)

@Penguin-Guru wrote "My system still often stuttered heavily during certain parts of most, if not all, the ComfyUI workflow I tried."

You could lower the core count used by comfyui running your workflows. Using these variables:

export OMP_NUM_THREADS=12
export MKL_NUM_THREADS=12
export NUMEXPR_NUM_THREADS=12

Works good on my machine with 16 cores and for a Ryzen 9 3900 X 12 core cpu i just set those to 10. However with the latest Nobara Kernel 7.0.0-200 it hangs and stutters a lot. Kernel 6.17.12-200 works perfectly fine and i can open steam or using my broswer as usual while generating pictures with Flux1 and Flux2. Especially Flux2 is very resource demanding and uses a lot of RAM too.


---

### 评论 #76 — Penguin-Guru (2026-04-24T05:36:33Z)

@RadeonVega-56 

Yes, I have borrowed those values. It seems like V.A.E. decoding sometimes only uses a single core for some reason, but I don't think that's what was causing the stuttering. Sometimes the python process also maxes out one core even when no workflow is running until I restart ComfyUI, which is obviously a bug but does not cause any stuttering. Since disabling smart memory (and cudnn/MIOpen) helped, I'm guessing the stuttering might be caused by G.P.U./V.RAM bandwidth or something like process management. I haven't tried using a different G.P.U. It might be that the lock-ups have been resolved and only the video stutters and freezes now (with smart memory and MIOpen enabled. I also haven't tried to manually tune resource limits for the ComfyUI/python system processes. Hopefully [this](https://github.com/ROCm/TheRock/issues/2591) helps. I'll probably continue fiddling with the environment variables a bit but I think I'm getting decent performance with MIOpen and smart memory disabled for now. I will try to confirm whether that memory leak is also occurring on my system when I have a chance.

Have you tried L.T.X. 2.3? This is one of the models that was causing the V.A.E. decoding issue most often.

---

### 评论 #77 — RadeonVega-56 (2026-04-26T09:20:57Z)

LTX 2.3 runs perfect. I can do up to 15 seconds 720p at 30 fps in 15 minutes.

---
