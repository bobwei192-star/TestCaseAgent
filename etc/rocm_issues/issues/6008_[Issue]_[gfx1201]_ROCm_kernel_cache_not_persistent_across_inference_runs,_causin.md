# [Issue]: [gfx1201] ROCm kernel cache not persistent across inference runs, causing significant performance regression on subsequent runs

> **Issue #6008**
> **状态**: open
> **创建时间**: 2026-03-01T17:08:19Z
> **更新时间**: 2026-03-30T21:11:16Z
> **作者**: ReinerBforartists
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6008

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

  (Get-WmiObject win32_Processor).Name

When running WAN VAE (CausalConv3d operations) in ComfyUI on gfx1201 (Radeon AI PRO R9700), subsequent inference runs are significantly slower than the first. The slowdown scales with resolution and frame count – at 1024x576 @ 81 frames it is 4-5x slower, at lower resolutions around 2-3x slower.

The problem appears with ComfyUI and runing a Wan Image to Video workflow, where we get a dramatical speed regression between first run and second run.

It is reproducable on both, Windows 11 and a Docker in Ubuntu 24 with also ROCm 7.2, so no Windows only problem.

### Operating System

Windows 11 Pro 25H2

### CPU

AMD Ryzen 9 9900X

### GPU

AMD Radeon AI Pro 32 Gb

### ROCm Version

7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

Download latest WIndows ComfyUI portable here: https://github.com/Comfy-Org/ComfyUI/releases

Load the attached Wan Image to Video workflow on a PC with AMD card and ROCm 7.2. See attached assets.
Download the models that are linked in the workflow.
Let the workflow run through.
Change the image.
Let it run through again.
Watch the generation times.

Minimal reproduction confirms kernel recompilation on new tensor shapes, i ran it from the ComfyUI_windows_portable folder:

```
import torch, time
device = "cuda:0"
x1 = torch.randn(1, 96, 1, 576, 1024, device=device, dtype=torch.float16)
conv = torch.nn.Conv3d(96, 96, 3, padding=1).to(device).half()
start = time.time(); conv(x1); print(f"1 frame: {time.time()-start:.3f}s")
x2 = torch.randn(1, 96, 6, 576, 1024, device=device, dtype=torch.float16)
start = time.time(); conv(x2); print(f"6 frames first call: {time.time()-start:.3f}s")
start = time.time(); conv(x2); print(f"6 frames second call: {time.time()-start:.3f}s")
```

Output:
1 frame: 7.640s
6 frames first call: 83.488s
6 frames second call: 0.001s

The kernel cache works within a session when the same tensor shapes are called back-to-back. However ROCm does not persist this cache across subsequent inference runs, causing full recompilation on every run after the first.

Additional observation: Between Run 1 and Run 2, ComfyUI unloads significantly more VRAM before reloading the diffusion model (Unloaded partially: 8569 MB in Run 2 vs 1232 MB in Run 1). Whether this is related or a separate issue is unclear.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

For the Linux version see this docker here if needed: https://github.com/YanWenKun/ComfyUI-Docker/tree/main/rocm7

**Evidence:

Running ComfyUI with these startup parameters:

--novram (all computation on CPU, no VRAM load/unload) → no performance regression between runs, it is even faster at the second run. This strongly suggests the regression is tied to VRAM load/unload cycles.
--cache-none (disables ComfyUI's internal caching) → regression persists, ruling out ComfyUI cache as cause,  and points directly at ROCm.

--novram result

```
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Found quantization metadata version 1
Using MixedPrecisionOps for text encoder
Requested to load WanTEModel
loaded completely;  6419.48 MB loaded, full load: True
CLIP/text encoder model load device: cpu, offload device: cpu, current: cpu, dtype: torch.float16
FETCH ComfyRegistry Data [DONE]
[ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json [DONE]
[ComfyUI-Manager] All startup tasks have been completed.
Requested to load WanVAE
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
### vae.encode done
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
gguf qtypes: F16 (694), Q4_K (280), Q6_K (120), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
loaded partially; 0.00 MB usable, 0.00 MB loaded, 9337.19 MB offloaded, 656.56 MB buffer reserved, lowvram patches: 0
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:10<00:00,  5.15s/it]
gguf qtypes: F16 (694), Q4_K (280), Q6_K (120), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
loaded partially; 0.00 MB usable, 0.00 MB loaded, 9337.19 MB offloaded, 656.56 MB buffer reserved, lowvram patches: 0
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:09<00:00,  4.65s/it]
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
Loading RIFE model from: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-VFI\rife\train_log\flownet.pkl
Prompt executed in 283.42 seconds
got prompt
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
### vae.encode done
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
loaded partially; 0.00 MB usable, 0.00 MB loaded, 9337.19 MB offloaded, 656.56 MB buffer reserved, lowvram patches: 0
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.32s/it]
loaded partially; 0.00 MB usable, 0.00 MB loaded, 9337.19 MB offloaded, 656.56 MB buffer reserved, lowvram patches: 0
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.25s/it]
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
Prompt executed in 177.25 seconds
```

--cache-none result

```

got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Found quantization metadata version 1
Using MixedPrecisionOps for text encoder
Requested to load WanTEModel
loaded completely;  6419.48 MB loaded, full load: True
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cuda:0, dtype: torch.float16
Requested to load WanVAE
loaded completely; 30717.34 MB usable, 242.03 MB loaded, full load: True
### vae.encode done
gguf qtypes: F16 (694), Q4_K (280), Q6_K (120), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
loaded completely; 27948.86 MB usable, 9337.19 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:07<00:00,  3.64s/it]
gguf qtypes: F16 (694), Q4_K (280), Q6_K (120), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
loaded completely; 27797.48 MB usable, 9337.19 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:06<00:00,  3.28s/it]
Loading RIFE model from: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-VFI\rife\train_log\flownet.pkl
Prompt executed in 37.50 seconds
FETCH ComfyRegistry Data [DONE]
[ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json [DONE]
[ComfyUI-Manager] All startup tasks have been completed.
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Found quantization metadata version 1
Using MixedPrecisionOps for text encoder
Requested to load WanTEModel
loaded completely;  6419.48 MB loaded, full load: True
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cuda:0, dtype: torch.float16
Requested to load WanVAE
loaded completely; 30374.13 MB usable, 242.03 MB loaded, full load: True
### vae.encode done
gguf qtypes: F16 (694), Q4_K (280), Q6_K (120), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
loaded completely; 27698.33 MB usable, 9337.19 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:06<00:00,  3.27s/it]
gguf qtypes: F16 (694), Q4_K (280), Q6_K (120), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
loaded completely; 27698.33 MB usable, 9337.19 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:06<00:00,  3.15s/it]
Prompt executed in 78.02 seconds

```

Notice the generation time between first run and second run. Prompt executed in ...

Videos were generated in a size of 320 x 240 px

**Related** 
ComfyUI issue with further informations: https://github.com/Comfy-Org/ComfyUI/issues/12672

Assets contains the test_rocm.py, the wan image to video workflow and two example images in png format.

[assets.zip](https://github.com/user-attachments/files/25663525/assets.zip)



---

## 评论 (29 条)

### 评论 #1 — ReinerBforartists (2026-03-01T17:16:12Z)

May i add that this is for me a showstopper bug? I cannot wait  45 minutes for a video generation when it runs through in the first run in 8 minutes.

---

### 评论 #2 — rattus128 (2026-03-01T23:19:53Z)

clarification: --novram does not mean CPU compute, it means no VRAM is reserved for model weights and all weights are transferred to the GPU every layer as temporaries. Inference temporaries are still GPU and all compute is GPU.

the --cache-none is the minimal reproducer from an under-the-hood point of view. It will do the usual load the whole model, run it then free the VRAM.

--novram has more variables due to the comfyUI weight offload engine and caching of assets at multiple layers. I would suggest limiting scope to only the --cache-none data point in initial investigations.

---

### 评论 #3 — Only8Bits (2026-03-02T11:20:31Z)

@ReinerBforartists WAN VAE issue is a long known problem, to me it looks like MIOpen is not properly caching the solutions found during benchmarking step, and what's worse it also tries naive solvers that are very slow in general.

See my comments at https://github.com/ROCm/TheRock/issues/2591

There's 3 possible workarounds that I found:

1) Modify your VAE nodes, or add node wrappers, setting torch.backends.cudnn.enabled = False. You want to cudnn enabled for everything else so it's not a good idea to just disable it permanently at the start of Comfy. This is a fast and reliable solution but the downside is your VAE steps will take more VRAM. You might have to resort to tiled VAE anyway.

2) Tiled VAE will also "solve" this issue because the tiles are way smaller and the time wasted by MIOpen solver search is greatly reduced. Might be easier to implement if you're not comfortable with modifying Python sources, but tiled VAEs introduce errors at the seams and also the VAE doesn't "see" the entire picture so for example you might get strange movements, like human arms bending in weird ways, etc.

3) Set PYTORCH_TUNABLEOP_ENABLED=1, this will result in even slower first run (torch will be doing it's own benchmarking on top of MIOpen) but after that step the cache database will be properly populated, for some reason. Now this results in VAE times that are still some 2x longer than with cudnn=False, but it's 20s vs 12s, not minutes or worse. So the result is acceptable, if not optimal, VAE times and no need to resort to tiled VAE and no higher VRAM usage (except maybe that first time).

See if any of these help you. Also consider adding "expandable_segments:True" to your PYTORCH_ALLOC_CONF for the other issue you've posted. I'm not sure if it works properly on RDNA3, I used to get a warning trying it in the past, but I've just tried it again on ROCm 7.2 (on Linux) and there was no such message anymore. Not yet sure if it actually does anything useful, but worth testing I think.

---

### 评论 #4 — ReinerBforartists (2026-03-02T13:09:11Z)

Thanks for the ideas. But this looks to me like another issue. I have tried all three options at my way before reporting this issue. To no avail.

But there is an easy way to find out if i have overlooked something. Could you plesae try out the workflow that is linked to the issue and try your fixes? Simply download the assets.zip, it contains the workflow.

---

### 评论 #5 — Only8Bits (2026-03-02T17:13:01Z)

I guess I misunderstood the issue you have. Anyway - I've tried the minimal reproducer for now, tell me if this is what you expected or not:

1st run:
1 Frame no cache: 10.471s
6 Frames with cache: 140.937s
6 Frames second call: 0.005s

2nd run:
1 Frame no cache: 0.109s
6 Frames with cache: 2.706s
6 Frames second call: 0.000s

3rd run:
1 Frame no cache: 0.110s
6 Frames with cache: 0.018s
6 Frames second call: 0.000s

Any subsequent run is more or less equal to the 3rd one. I'm not sure if you are measuring the execution time correctly, first I've noticed the script takes quite a few seconds to close after being run and printing out the results, and radeontop shows 100% GPU activity during that period. Second I've seen other people do it with some extra barriers to make sure the GPU compute queue is done before measuring time. So I modified the code, adding "torch.cuda.synchronize ()" before each print, and this is what I get now:

1 Frame no cache: 0.144s
6 Frames with cache: 17.380s
6 Frames second call: 17.472s

This is consistent across many runs. Note these results are without a workaround that I'd usually use to overcome performance loss I get on ROCm 7.2 and current driver. With the workaround enabled the times are also consistent but quite better:

1 Frame no cache: 0.112s
6 Frames with cache: 14.128s
6 Frames second call: 14.239s

---

### 评论 #6 — Only8Bits (2026-03-02T18:06:07Z)

Two more data points, obtained by running _MIOPEN_FIND_ENFORCE="DB_CLEAN" python3 test_rocm.py_:

No performance workaround:
1 Frame no cache: 9.636s
6 Frames with cache: 156.638s
6 Frames second call: 17.357s

With workaround:
1 Frame no cache: 8.635s
6 Frames with cache: 128.557s
6 Frames second call: 14.163s

This suggests MIOpen actually working properly in this case, the first call is slow but second is already fast, and this persists between runs as seen in my previous post.

---

### 评论 #7 — ReinerBforartists (2026-03-03T06:33:03Z)

This issue is about video generation speed degeneration. The python script is just a quick example to strengthen the point and to rule out a few things. When you want to test then please run the attached workflow.

I understand you’re trying to help, but your workarounds don’t apply here. As mentioned, I already ruled them out at the beginning of my investigation. The MIOpen cache problem is a separate issue, and I’d like to keep this thread focused on the current problem. The issue you linked was created in December and so refers to ROCm 6.4. Version 7 appeared in january. I’m specifically talking about ROCm 7.2 here.

I just noticed that i have missed an important information. I initially ran a separate ROCm 7.1.1 driver on Windows because ROCm 7 was not yet available in Adrenalin. I generated several videos with 7.1.1 without any slowdowns using the same workflow. This points to a regression between 7.1.1 and 7.2. Too bad that most of my other software has quit working with 7.1.1, else i would switch back.

---

### 评论 #8 — tcgu-amd (2026-03-04T17:25:13Z)

> This issue is about video generation speed degeneration. The python script is just a quick example to strengthen the point and to rule out a few things. When you want to test then please run the attached workflow.
> 
> I understand you’re trying to help, but your workarounds don’t apply here. As mentioned, I already ruled them out at the beginning of my investigation. The MIOpen cache problem is a separate issue, and I’d like to keep this thread focused on the current problem. The issue you linked was created in December and so refers to ROCm 6.4. Version 7 appeared in january. I’m specifically talking about ROCm 7.2 here.
> 
> I just noticed that i have missed an important information. I initially ran a separate ROCm 7.1.1 driver on Windows because ROCm 7 was not yet available in Adrenalin. I generated several videos with 7.1.1 without any slowdowns using the same workflow. This points to a regression between 7.1.1 and 7.2. Too bad that most of my other software has quit working with 7.1.1, else i would switch back.

Hi @ReinerBforartists, thanks for reaching out and I am really sorry that you are experiencing this issue. I tried to run your workflow but seems like it's missing a couple custom nodes? Can you please include them as well? Thanks! 

<img width="618" height="440" alt="Image" src="https://github.com/user-attachments/assets/95269805-c5e2-462b-8443-0bc78fb775e9" />

I also have a few questions. In the issue description you mentioned that the problem was that kernel cache was not persistent, but in your last comment you mentioned that the MIOpen cache problem is a separate problem. Just trying to get this straight: what did you mean by the kernel cache then? As far as I understand the ROCm kernel cache *is* the MIOpen cache, or perhaps you are referring to the regression in general and kernel caching is just a hypothesis?

Also, you mentioned
> I initially ran a separate ROCm 7.1.1 driver on Windows because ROCm 7 was not yet available in Adrenalin. 

What did you mean by this? What "separate driver" did you run? I am not aware of alternatives to Adrenaline driver, can you please link them? 

Last but not least, it would be helpful if you could run comfy UI with the environment variable `MIOPEN_LOG_LEVEL=7` and attach the outputs here. It will help us figure out what going on in MIOpen.

Thanks!!

---

### 评论 #9 — ReinerBforartists (2026-03-04T20:09:46Z)

The "kernel cache" I was referring to is the in-process PyTorch/ROCm cache that gets built up during a running Python session when new tensor shapes are processed through Conv3d for the first time. Our test script demonstrates this clearly: the second call with the same tensor shape completes in 0.001s, proving the cache exists and works within a session.
MIOpen is the persistent disk-based cache that survives between Python sessions. We tested this separately (MIOPEN_USER_DB_PATH) and it had no effect on the regression.
The hypothesis is: the in-process cache gets invalidated between inference runs somehow – even though the Python process is still running. Why exactly is unclear. MIOpen as a persistent cache would have been the solution, but did not help in our case.
So to clarify: "kernel cache not persistent" in my description means "in-process cache appears to get invalidated between inference runs within the same Python session", not the MIOpen disk cache. The two are separate things and I should have been more precise about that. Apologies for the confusion.

> What did you mean by this? What "separate driver" did you run? I am not aware of alternatives to Adrenaline driver, can you please link them?

This was this one from what i remember, a standalone rocm driver, not in Adrenaline: https://www.amd.com/en/resources/support-articles/release-notes/RN-AMDGPU-LINUX-ROCM-7-1-PREVIEW.html

> Last but not least, it would be helpful if you could run comfy UI with the environment variable MIOPEN_LOG_LEVEL=7 and attach the outputs here. It will help us figure out what going on in MIOpen.

Will do tomorrow. Same for the custom nodes. I haven't thought about that you might not know ComfyUI. Usually the first thing you do is to install the manager. And then it is as easy as clicking at install missing nodes in this manager.

I'll have a look to place the links to the missing nodes tomorrow. Sorry for the inconvenience.

---

### 评论 #10 — ReinerBforartists (2026-03-05T07:03:01Z)

I have to correct myself, it was this windows pytorch driver. I knew it was something with 7.1.1. Never answer issues in the late evening ...

https://www.amd.com/en/resources/support-articles/release-notes/RN-AMDGPU-WINDOWS-PYTORCH-7-1-1.html

For the missing nodes, best is as told to install the manger addon. It appears in the header. Click at it, choose Install Missing Nodes, and install the nodes that are listed there.

![Image](https://github.com/user-attachments/assets/289a3160-5154-475f-8379-a744c0fbc906)

https://github.com/Comfy-Org/ComfyUI-Manager

The single nodes are located here:

https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

https://github.com/rgthree/rgthree-comfy

https://github.com/GACLove/ComfyUI-VFI

https://github.com/city96/ComfyUI-GGUF

Here the miopen cache log with log level 7. It does not print the whole log though. It is too long for the console. It gets flooded with this message:

MIOpen(HIP): Info2 [GetInvoker] Returning an invoker for problem 32x64x96x3x3x32x64x96x1xNCHWxFP16x1x1x1x1x1x1x1xFxDefault and algorithm miopenConvolutionFwdAlgoWinograd
MIOpen(HIP): Info2 [MakeGcnAsmWinoV2InvokerFactory]  N=1 C=32 H=64 W=96 K=32 R=3 S=3 pad_H=1 pad_W=1 out_H=64 out_W=96 G=1 alpha=0 beta=0 act_mode=0 d_offset=0 f_offset=0 o_offset=0 b_offset=0 d_N_stride=196608 d_C_stride=6144 d_H_stride=96 d_G_stride=196608 f_K_stride=288 f_C_stride=9 f_R_stride=3 f_G_stride=9216 o_N_stride=196608 o_K_stride=6144 o_H_stride=96 o_G_stride=196608 n_groups=64 flags64=0xe200 sync_limit=0 sync_period=0
MIOpen(HIP): Info2 [run] kernel_name = miopenSp3AsmConvFury_v4_6_0_gfx12_1536vgprs_fp16_fp32acc_f2x3_c16_stride1, global_work_dim = { 24576, 1, 1 }, local_work_dim = { 384, 1, 1 }
MIOpen(HIP): Info [get_device_name] Raw device name: gfx1201
MIOpen(HIP): Info [SetStream] stream: 0000000000000000, device_id: 0

The available log is attached as text.

[miopenloglevel7.txt](https://github.com/user-attachments/files/25760061/miopenloglevel7.txt)


---

### 评论 #11 — tcgu-amd (2026-03-10T19:07:49Z)

Hi @ReinerBforartists sorry for the delayed response as my attention was pulled elsewhere last week. Thanks for the detailed instructions, I was able to run your workflow. So I think I did "kind of" reproduce the regression, but mine probably has a different underlying cause. My log for the runs look like below

```
Prompt executed in 42.15 seconds
Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.28s/it]
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.09s/it]
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Prompt executed in 182.47 seconds
        got prompt
Prompt executed in 0.66 seconds
got prompt
Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.05s/it]
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.06s/it]
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Prompt executed in 27.26 seconds
got prompt
Prompt executed in 0.65 seconds
got prompt
Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.06s/it]
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.09s/it$
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Prompt executed in 27.49 seconds:
```

I do notice that the second run is much slower than the rest. However, I think it might have more to do with memory management as ComfyUI shouldn't be forced to enter tiled decode mode here. In that case, it would be more of a ComfyUI issue than ROCm. I am not quite sure if the kernel cache persistence is the source of the issue as you mentioned, because it shouldn't have caused a "slow down". At worse, it should only make the subsequent runs as slow as the first one. 

By the way, I was reproducing your issue on native Linux since you did mention this occurs on both Windows and Linux. However, just in case, by "reproducible on Linux" did you mean by native Linux or Linux in Docker on Windows? Because the two share only the HIP-runtime and nothing common below that. 

Thanks! 

---

### 评论 #12 — ReinerBforartists (2026-03-11T07:10:07Z)

Great that you were able to reproduce the issue.

I’m running ComfyUI in Docker at Linux. I wasn’t able to install native ComfyUI on my Ubuntu 24 system because I couldn’t get the dependencies to work. If I remember correctly, there was a missing ROCm wheel in the end, and at that point I gave up. So I went the Docker route, which wasn’t so challenging.

>However, I think it might have more to do with memory management as ComfyUI shouldn't be forced to enter tiled decode mode here.

The fact that it enters tiled mode is a sign that the available VRAM becomes insufficient, and it shouldn’t. The first run worked. So between the first and the second run, the available VRAM becomes smaller. This could be caused by ComfyUI, but it could also be the driver, or a combination of both. Whenever i search for amd and ComfyUI i get told about the well known problem of ram fragmentation. And this could imho explain what is happening here.

I cannot tell what the actual problem is. I don’t have the tools or the knowledge to find the root cause. That’s why I created the bug report after digging as deep as I could. First in the ComfyUI tracker, and after I was told that this is most likely a ROCm issue, also here. The ComfyUI developers are also clueless what the cause could be.

Either way, we need a solution. How could we prove whether the problem is caused by the driver or by ComfyUI?

---

### 评论 #13 — tcgu-amd (2026-03-11T15:23:04Z)

> Great that you were able to reproduce the issue.

I am not quite sure what I reproduced was the same issue you were seeing. Do you see it enter tiled VAE decode mode on your end? Did you use --lowvram or other flags when running ComfyUI (I didn't by the way)?

> I’m running ComfyUI in Docker at Linux. I wasn’t able to install native ComfyUI on my Ubuntu 24 system because I couldn’t get the dependencies to work. If I remember correctly, there was a missing ROCm wheel in the end, and at that point I gave up. So I went the Docker route, which wasn’t so challenging.

Okay that works as well. Yeah, I'm sorry regarding the frustrating installation experience. Typically, how I set up the installation is to first install the amdgpu-dkms driver from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#amdgpu-driver-installation, then install the latest pytorch wheels with ROCm for your gpu (gfx1201) from [TheRock](https://github.com/ROCm/TheRock/blob/main/RELEASES.md) via pip in your virtual environment. After that, delete/comment out torch/torchvision/torchaudio from `requirement.txt` in the ComfyUI folder and install the rest with `pip install -r requirements.txt`. 

> The fact that it enters tiled mode is a sign that the available VRAM becomes insufficient, and it shouldn’t. The first run worked. So between the first and the second run, the available VRAM becomes smaller. This could be caused by ComfyUI, but it could also be the driver, or a combination of both. Whenever i search for amd and ComfyUI i get told about the well known problem of ram fragmentation. And this could imho explain what is happening here.

The memory issue is pretty much the result of a combination between ComfyUI's memory allocation strategy, PyTorch memory reservation mechanism, and ROCm's memory consumption pattern. However, ultimately, ComfyUI is the end program that determines how much memory to use and whether to clean up memory/unload model to get more space ahead of entering VAE, so fixes should be implemented there imo. ROCm's contribution is usually in the form of using different algorithms between versions which may have different memory consumption patterns, which can push the amount of memory estimated to be available by ComfyUI just over the edge. 

> I cannot tell what the actual problem is. I don’t have the tools or the knowledge to find the root cause. That’s why I created the bug report after digging as deep as I could. First in the ComfyUI tracker, and after I was told that this is most likely a ROCm issue, also here. The ComfyUI developers are also clueless what the cause could be.

Makes sense -- I was just trying to ascertain the correct direction to investigate. Since this issue points to the kernel cache in the title, I wanted to know if you were certain regarding the cause.

> Either way, we need a solution. How could we prove whether the problem is caused by the driver or by ComfyUI?

I'd assume we would know once we found the actual cause for the slow down. However, typically, the investigation is started at the high level then progressed down once you are reasonably sure the about a specific cause in the lower layer. i.e. ComfyUI -> PyTorch -> ROCm. From our standpoint, right now we are still in a stage where we had to debug ComfyUI first, which is not my area of expertise, and would be more effective if were done by the ComfyUI devs. So unless you are sure regarding this is a ROCm specific bug (e.g. kernel cache persistence, which I doubt), I would say it is more efficient to take it to the ComfyUI side. 


---

### 评论 #14 — ReinerBforartists (2026-03-11T17:27:03Z)

>I am not quite sure what I reproduced was the same issue you were seeing. 

When you see a slowdown in the second run, then it is. There is no message that it is entering the slow VAE tiled mode, at least i haven't noticed one. But that's the typical fallback strategy. So i assume that this is what happens.

I understand your point, and I agree that the investigation should follow the stack from top to bottom. However, I believe we already have evidence that points below the ComfyUI layer.
The test script I provided runs without ComfyUI at all – just pure PyTorch directly calling Conv3d:
```
pythonimport torch, time
device = "cuda:0"
conv = torch.nn.Conv3d(96, 96, 3, padding=1).to(device).half()
x2 = torch.randn(1, 96, 6, 576, 1024, device=device, dtype=torch.float16)
start = time.time(); conv(x2); print(f"first call: {time.time()-start:.3f}s")
start = time.time(); conv(x2); print(f"second call: {time.time()-start:.3f}s")
```
The second call is 0.001s – the kernel cache works. But if you add any VRAM pressure between the two calls (allocate and free large tensors), does the cache still hold? That would isolate whether ROCm invalidates its kernel cache under memory pressure, completely independent of ComfyUI.
This is the next step I cannot do myself because I lack the ROCm internals knowledge to interpret the results. Would you be willing to run this test?

---

### 评论 #15 — ReinerBforartists (2026-03-11T19:09:14Z)

Found a way to do this test myself.

```
import torch, time
device = "cuda:0"
conv = torch.nn.Conv3d(96, 96, 3, padding=1).to(device).half()

x2 = torch.randn(1, 96, 6, 576, 1024, device=device, dtype=torch.float16)
start = time.time(); conv(x2); print(f"first call: {time.time()-start:.3f}s")
start = time.time(); conv(x2); print(f"second call (should be fast): {time.time()-start:.3f}s")

# Simuliere VRAM Druck wie zwischen zwei ComfyUI Runs
print("Allocating and freeing large tensors...")
for i in range(5):
    big = torch.randn(1, 9337, 1024, 1024, device=device, dtype=torch.float16)
    del big
torch.cuda.empty_cache()

start = time.time(); conv(x2); print(f"third call after VRAM pressure: {time.time()-start:.3f}s")
```

I then ran the VRAM pressure test:
```
first call: 3.276s
second call (should be fast): 0.000s
Allocating and freeing large tensors...
third call after VRAM pressure: 0.000s
```
The third call after simulated VRAM pressure is still fast. This means VRAM pressure alone does not invalidate the ROCm kernel cache. Something specific in ComfyUI between inference runs must be causing the invalidation. I will take this back to the ComfyUI issue tracker.

---

### 评论 #16 — tcgu-amd (2026-03-11T19:24:27Z)

@ReinerBforartists Awesome! Thanks for the hardwork! If you can manage to get a reproducer that is independent of ComfyUI that would make it much easier for us. Thanks! 

---

### 评论 #17 — ReinerBforartists (2026-03-12T06:22:07Z)

There is one thing that didn't let me sleep last night. I stated that i used another driver before the official driver with Adrenaline came out. And i had no slowdown problem with the very same workflow.

This one. https://www.amd.com/en/resources/support-articles/release-notes/RN-AMDGPU-WINDOWS-PYTORCH-7-1-1.html

Could you please check if with this driver the second run of the workflow is equal slow than with the latest driver at your end too? In case the slowdown is still there, then we have a ComfyUI problem. If not, when the workflow does not show the slowdown in the second run, then we have the proof for a driver problem. And that something has changed at the driver end.

The different Pytorch version is not of interest for us since ComfyUI portable runs in a Venv with its own Pytorch version. So it is really the driver then.

---

### 评论 #18 — tcgu-amd (2026-03-13T19:32:40Z)

Hi @ReinerBforartists, yeah that's a good point. Before trying that though, I did do more investigation and found something interesting. It appears that the slow down on my end actually came from MIOpen invalidating its own db and re-searching for optimal kernels during its second iterations. It does that despite my setting FIND_MODE explicitly to FAST, and regardless of how much VRAM is available. Can you try on your end with `set MIOPEN_LOG_LEVEL=5`? You should see messages with `FindSolutionImpl` on the second run, which is when MIOpen search for a solution. I am still not quite sure why MIOpen does that, but this is truly the cause then it gives us a very clear direction to look into. Thanks! 

---

### 评论 #19 — tcgu-amd (2026-03-13T20:00:57Z)

@ReinerBforartists Update: It does seem like in the second iteration MIOpen is searching for an entirely different group of problems. For example `3x3x384x480x1x3x3x1x96x1x1x1x0x1x1x1x1x1x1x0x1xNCDHWxBF16xF=ConvHipImplicitGemm3DGroupFwdXdlops` was not used in the first iteration at all. This probably explains why MIOpen had to search for solutions again. Looks like somethings changed and somewhere in the higher layer is trying to tell MIOpen to wor on these new problems from the second iteration onwards. 

---

### 评论 #20 — ReinerBforartists (2026-03-14T07:31:27Z)

Big find!
Thank you for pointing me to MIOPEN_LOG_LEVEL=5 again. The log confirms exactly what you described.
In Run 1, MIOpen sees 1-frame tensor shapes like:
3-1-240-320-1x3x3-96-1-240-320
In Run 2, after the first chunk, entirely new shapes appear with 6 frames and batch size 4:
3-6-240-320-3x3x3-96-4-240-320

The log is attached.

I think this is caused by the temporal cache (feat_cache) in WanVAE.encode in comfy/ldm/wan/vae.py. The first chunk always processes 1 frame with no cache. I can even give you the code part for it.

```
if x.shape[2] > 1 and self.kernel_size[1] == 3:
    first_result = self.forward(x[:, :, :1, :, :], cache_x=cache_x)
    out = torch.empty((x.shape[0], first_result.shape[1], x.shape[2], 
                       first_result.shape[3], first_result.shape[4]), 
                       device=x.device, dtype=x.dtype)
    out[:, :, 0, :, :] = first_result[:, :, 0, :, :]
    del first_result
    for i in range(1, x.shape[2]):
        frame = x[:, :, i:i+1, :, :]
        result = self.forward(frame, cache_x=x[:, :, i-1:i, :, :])
        out[:, :, i, :, :] = result[:, :, 0, :, :]
        del result
    return out
```

Subsequent chunks process 4 frames WITH the cache from the previous chunk prepended, resulting in 6-frame tensors. On the first run MIOpen never sees these 6-frame shapes because the cache is empty. On the second run the cache is populated from Run 1 and MIOpen encounters completely new problem configurations it has never seen before.

So the root cause is confirmed to be in ComfyUI/WAN VAE: the chunked encoding with temporal cache produces different tensor shapes between Run 1 and Run 2. This part is a ComfyUI/model implementation issue, not a ROCm bug. At least at the fist look.

On my way i alsou found a fix that adresses the root cause. By processing frames one-by-one in CausalConv3d.forward instead of in 4-frame chunks, we can ensure MIOpen always sees the same 1-frame tensor shapes regardless of whether feat_cache is populated or not.

def forward(self, x, cache_x=None, cache_list=None, cache_idx=None):
        if cache_list is not None:
            cache_x = cache_list[cache_idx]
            cache_list[cache_idx] = None

        if cache_x is None and x.shape[2] == 1:
            #Fast path - the op will pad for use by truncating the weight
            #and save math on a pile of zeros.
            return super().forward(x, autopad="causal_zero")

        # Frame-by-frame fast path for multi-frame tensors with spatial 3x3 kernel
        if x.shape[2] > 1 and self.kernel_size[1] == 3:
            first_result = self.forward(x[:, :, :1, :, :], cache_x=cache_x)
            out = torch.empty((x.shape[0], first_result.shape[1], x.shape[2], first_result.shape[3], first_result.shape[4]), device=x.device, dtype=x.dtype)
            out[:, :, 0, :, :] = first_result[:, :, 0, :, :]
            del first_result
            for i in range(1, x.shape[2]):
                frame = x[:, :, i:i+1, :, :]
                result = self.forward(frame, cache_x=x[:, :, i-1:i, :, :])
                out[:, :, i, :, :] = result[:, :, 0, :, :]
                del result
            return out

        if self._padding > 0:
            padding_needed = self._padding
            if cache_x is not None:
                cache_x = cache_x.to(x.device)
                padding_needed = max(0, padding_needed - cache_x.shape[2])
            padding_shape = list(x.shape)
            padding_shape[2] = padding_needed
            padding = torch.zeros(padding_shape, device=x.device, dtype=x.dtype)
            x = torch_cat_if_needed([padding, cache_x, x], dim=2)
            del cache_x

        return super().forward(x)

This eliminates the new MIOpen problem configurations entirely and makes Run 2 as fast as Run 1 for the VAE encoding step. At least in theory. But this "fix" increases VRAM usage by approximately 1GB during VAE encoding, which causes OOM in the KSampler on a 32GB GPU at 1024x576 @ 81 frames. We were unable to find a way to reduce the VRAM overhead sufficiently. So this way is impracticable.

The complete fix therefore lies on the MIOpen side. If MIOpen persisted its kernel cache for new problem configurations across inference runs, Run 3, 4, 5 would all be fast automatically without any ComfyUI changes. As long as MIOpen re-searches for every new problem configuration it encounters, any workaround on the ComfyUI side will be fighting symptoms rather than the actual cause.

So yes – it is a ComfyUI bug that triggers the problem, but it can imho only be truly fixed at the MIOpen level. That's at least what i can say with my limited knowledge about the matter.

I will now post this also at the ComfyUI tracker. Many thanks for the investigation so far :)

[comfyui.log](https://github.com/user-attachments/files/25992441/comfyui.log)

---

### 评论 #21 — ReinerBforartists (2026-03-14T08:10:31Z)

Also here, found a mutable default argument bug.

The mutable default argument feat_idx=[0] in Resample, ResidualBlock, Encoder3d and Decoder3d classes in comfy/ldm/wan/vae.py causes the index to persist between inference runs. Changing to feat_idx=None with if feat_idx is None: feat_idx = [0] fixes the slowdown from Run 3 onwards. Run 2 remains slower as MIOpen still encounters new tensor shapes for the first time, but all subsequent runs are now as fast as the first run.

Affected classes in comfy/ldm/wan/vae.py:

class Resample
class ResidualBlock
class Encoder3d
class Decoder3d

Replace

def forward(self, x, feat_cache=None, feat_idx=[0]):

by

def forward(self, x, feat_cache=None, feat_idx=None):
    if feat_idx is None:
        feat_idx = [0]

---

### 评论 #22 — ReinerBforartists (2026-03-14T17:04:31Z)

Ah, not the cause and not the fix. The index null isn't even used. And the behaviour that just the second run is slow was present before the fix already. Another dead end ...

---

### 评论 #23 — tcgu-amd (2026-03-16T18:37:05Z)

>Subsequent chunks process 4 frames WITH the cache from the previous chunk prepended, resulting in 6-frame tensors. On the first run MIOpen never sees these 6-frame shapes because the cache is empty. On the second run the cache is populated from Run 1 and MIOpen encounters completely new problem configurations it has never seen before.

@ReinerBforartists  Interesting find! However, I don't think this fully explains why MIOpen is trying to solve 3d kernels and BF16 tensors. There's likely some other optimization in PyTorch or MIOpen that's playing a hand here. I am trying my best to track it down but it would definitely be helpful if someone from the other side can take a look as well. 

> But this "fix" increases VRAM usage by approximately 1GB during VAE encoding, which causes OOM in the KSampler on a 32GB GPU at 1024x576 @ 81 frames. We were unable to find a way to reduce the VRAM overhead sufficiently. So this way is impracticable.

In this case, you can try with `--reserve-vram` flag in ComfyUI. If you set it to something like 5~10 GB then ComfyUI will unload one of the models and allow more space for VAE I think.

> If MIOpen persisted its kernel cache for new problem configurations across inference runs, Run 3, 4, 5 would all be fast automatically without any ComfyUI changes. As long as MIOpen re-searches for every new problem configuration it encounters, any workaround on the ComfyUI side will be fighting symptoms rather than the actual cause. 

Again, I highly doubt it is a problem with kernel cache. In my case at least, ComfyUI is already fast on run 3,4,5 without any additional patches. For example, my first run would take somewhere around 40s, my second 170s, and my third and onwards would be 20 seconds.

 It looks like that run 1 receives a certain set of problems (conv2d + fp16), and on run 2 and onwards, a different set of problems are being solved (conv3d + bf16). Please do note that conv3d + bf16 support is a relatively new addition to ROCm, and I was using the latest nightly build of ROCm on Ubuntu so it might solve these problems faster than your ROCm 7.2 on windows. Can you check with MIOPEN_ENABLE_LOGGING_CMD=1 to see what problems are being solved on your second run and onwards? 




---

### 评论 #24 — ReinerBforartists (2026-03-16T19:17:01Z)

> Again, I highly doubt it is a problem with kernel cache. In my case at least, ComfyUI is already fast on run 3,4,5 without any additional patches. For example, my first run would take somewhere around 40s, my second 170s, and my third and onwards would be 20 seconds.

Yeah again, that was where i was wrong. I was under the impression that my fix did change the third run to faster. But it did not. It was from the beginning the pattern first run fast, second run slow, third run and any subsequent runs fast again. And i did not notice it. Sorry for confusion. 

I share your wish that the ComfyUI developers gets involved here too. But i guess they are as lost as me with this issue. I wish i could be of more help here.

Unfortunately MIOPEN_ENABLE_LOGGING_CMD=1 is not supported in ComfyUI.

G:\comfyamd\ComfyUI_windows_portable>MIOPEN_ENABLE_LOGGING_CMD=1
Der Befehl "MIOPEN_ENABLE_LOGGING_CMD" ist entweder falsch geschrieben oder
konnte nicht gefunden werden.

Did you have a chance to check with the old driver yet? The 7.1.1 one?


---

### 评论 #25 — tcgu-amd (2026-03-17T15:36:29Z)

>Yeah again, that was where i was wrong. I was under the impression that my fix did change the third run to faster. But it did not. It was from the beginning the pattern first run fast, second run slow, third run and any subsequent runs fast again. And I did not notice it. Sorry for confusion.

@ReinerBforartists, no I haven't had the chance to check the old driver yet, but the issue is fairly clear to me know. It appears to be that due to missing system kernel db/precompiled kernel cache for gfx12, MIOpen is defaulting to reconstructing user kernel db everytime it is run. In other words, normally, the 40s/180s runtime of the first two iterations should only happen once. On your subsequent loads of ComfyUI, MIOpen should be able to remember the kernels chosen and avoid all the benchmarking, but it is not doing that. This is a bug that needs to be fixed on our end. However, once the official system kernel db gets released it should also cover up the problem as well. 

The non-ROCm part of the problem, and imo the part that you might want to focus more on, is why ComfyUI is forcing MIOpen to solve conv3d BF16 problems. Conv3d and BF16 are not well supported on MIOpen. You see, MIOpen benchmarks all algorithms on both the first and the second iterations, so the reason that there's a slow down on the second one is actually because those algorithms are that much slower compared to Conv2d and FP16 ones. Even if we solve the kenerl db issue, without this problem being fixed you will still end up using slower algorithms to solve problems. 

---

### 评论 #26 — ReinerBforartists (2026-03-17T17:32:42Z)

Ah great. I am happy to hear that you have nailed down the problem. And that a solution is even on its way. Many thanks for your patience and investigation.

Why ComfyUI uses Conv3D and BF16 i don't know. That's honestly behind my horizon, and is best asked the ComfyUI developers.

Shall i copy over your answer to the ComfyUI issue?

---

### 评论 #27 — ReinerBforartists (2026-03-20T11:51:04Z)

> The non-ROCm part of the problem, and imo the part that you might want to focus more on, is why ComfyUI is forcing MIOpen to solve conv3d BF16 problems. Conv3d and BF16 are not well supported on MIOpen. You see, MIOpen benchmarks all algorithms on both the first and the second iterations, so the reason that there's a slow down on the second one is actually because those algorithms are that much slower compared to Conv2d and FP16 ones. Even if we solve the kenerl db issue, without this problem being fixed you will still end up using slower algorithms to solve problems.

Did some research again, and as i understood it right, we cannot simply use Conv2D, since we need the third dimension for the timeline in video generation. I couldn't spot any difference with FP16 versus BF16, generation times were pretty equal. I even had the feeling that the quality goes down a bit. But i would need to test it in full resolution.


---

### 评论 #28 — tcgu-amd (2026-03-25T17:23:19Z)

Hi @ReinerBforartists, sorry for the delayed response again:

> Did some research again, and as I understood it right, we cannot simply use Conv2D, since we need the third dimension for the timeline in video generation. I couldn't spot any difference with FP16 versus BF16, generation times were pretty equal. I even had the feeling that the quality goes down a bit. But i would need to test it in full resolution.

For video generation in general you would be correct, but in our case, MIOpen is only being used a part of the VAE decoding process which 2D kernels should suffice. 

Just to be safe I ran MIOPEN_ENABLE_LOGGING_CMD and checked the commands being used -- there were no 3D kernels. But your observation is very interesting, because it suggests that MIOpen might be unintentionally used in other parts of the pipeline. This is worth investigating.  

---

### 评论 #29 — crosson (2026-03-30T21:11:16Z)

As someone with similar hardware to OP why do I not experience this issue? Is this just isolated to the bf16 model only then? I have not run into this on the fp8 model.

---
