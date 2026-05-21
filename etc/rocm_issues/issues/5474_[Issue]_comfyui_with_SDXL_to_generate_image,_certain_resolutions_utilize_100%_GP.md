# [Issue]: comfyui with SDXL to generate image, certain resolutions utilize 100% GPU without progress

> **Issue #5474**
> **状态**: open
> **创建时间**: 2025-10-06T17:42:51Z
> **更新时间**: 2026-02-10T16:32:30Z
> **作者**: chikei
> **标签**: status: triage, project: miopen
> **URL**: https://github.com/ROCm/ROCm/issues/5474

## 标签

- **status: triage** (颜色: #585dd7)
- **project: miopen** (颜色: #962619)

## 负责人

- darren-amd

## 描述

### Problem Description

Workflow [amd.json](https://github.com/user-attachments/files/22727458/amd.json)

When use above basic workflow, *some* resolutions work normally and finished in ~8 seconds, *some* resolutions stuck at sampler 0th step while utilizing 100% GPU,  *some* resolutions stuck at VAE decoder while utilizing 100% GPU.

When stuck, it will take several minutes then trigger a driver timeout and then may or may not progress.

The system is configured with 64GB dedicated graphics memory.

For my system, following resolutions (w*h) work normally:
* 1024x1024
* 1344x768
* 1024x1536

Following resolutions (w*h) stuck:
* 1216x832
* 768x1344
* 1152x896
* 1536x1024

(Yes, weirdly the working/non-working resolutions are not symmetrical on w/h)

The ComfyUI is setup with following steps:
1. install python 3.12.10
2. install uv
3. git clone https://github.com/comfyanonymous/ComfyUI.git
4. remove torch, torchaudio, torchvision from requirement.txt
5. setup uv venv
6. uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ "rocm[libraries,devel]"
7. uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch torchaudio torchvision
8. uv pip install -r requirements.txt

### Operating System

Windows 11 10.0.26100

### CPU

CPU: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S AMD Radeon(TM) 8060S Graphics

### GPU

AMD Radeon(TM) 8060S Graphics

### ROCm Version

7.9.0rc20250928

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (13 条)

### 评论 #1 — ppanchad-amd (2025-10-06T18:01:11Z)

Hi @chikei. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — lostdisc (2025-10-06T20:32:01Z)

On my end, with a Ryzen AI HX 370 and ComfyUI on Windows (installed with [these instructions](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedryz/windows/comfyui/installcomfyui.html)), the first time generating a given image resolution takes 30 minutes or more, and then subsequent gens take ~1 minute.  Changing dimensions and then changing back retains the faster 1-minute speed for the previously-used size. The speedup is also retained across computer restarts, and carries over to other SDXL models that have never been run before. Settings other than dimensions don't seem to make a difference (e.g. steps, cfg, sampler, scheduler).

On a slow first run, most of the extra time seems to be VAE-related, i.e. before and after the KSampler/unet stage. The KSampler steps seem basically normal speed (~1 min for 20 steps), except the progress bar stays empty for ~6 minutes of high GPU activity before it starts actually filling. (This doesn't seem to be the initial model-loading from disk, which is quicker. If I change dimensions while keeping the same model loaded, I still get this ~6-minute mystery job before the unet looping can start.) Then the VAE decoding afterward takes over 20 minutes of GPU activity (longer if it has to retry with tiling), with a few stages of increasing GPU RAM usage. Non-GPU-RAM usage stays relatively stable, unless/until the VAE decoding starts overflowing into shared RAM.

My system has 32GB RAM, and I've tested different amounts dedicated to GPU.  16/16 works with 1024x1024, but froze up when I tried some larger sizes, so now I tend to do 24GB.  (Still tends to need VAE tiling though.)

More possibly-related info at [this ComfyUI bug report](https://github.com/comfyanonymous/ComfyUI/issues/5759).

---

### 评论 #3 — chikei (2025-10-07T18:19:34Z)

Thanks for the info, and I did some sacrificial 1 step run then the other wonky resolutions now works speedy. Which leads me believe that ROCm does some cached JIT compilation as other people mentioned in the linked issue.

If it is the case, then current JIT implementation is seriously flawed. First of all, that should not trigger a driver timeout. Second, current implementation seems unable to swap the compiled computation after first iteration. So if a compiled step take 2s and an uncompiled step take 2m and one setup a n step run for an unJITed resolution, it seems take 2*n mins instead of 2min + (n-1)*2s one would expected.

Currently it seems best workaround is run a sacrificial 1 step run, but it becomes very annoy for complex workflow involving different resolutions (such as tiled or Ultimate Stable Diffusion Upscale).

---

### 评论 #4 — chikei (2025-10-08T13:04:14Z)

Further google around leads me to [this comment](https://github.com/ROCm/ROCm/issues/4846#issuecomment-3328270404), and disabling torch cudnn backend workaround this issue with at most 10% performance loss on SDXL generation, apparently ROCm's cudnn compatible implementation is questionable.

---

### 评论 #5 — darren-amd (2025-11-19T19:03:34Z)

Hi @chikei,

Thanks for reporting this issue, does this issue still persist? It looks like the `torch.backends.cudnn.enabled = False` is being set on ComfyUI by default now.

---

### 评论 #6 — lostdisc (2025-11-21T19:48:10Z)

On my end, ComfyUI disabling cudnn did fix VAE slowness, albeit at a cost to other workloads (see complaints in the [merge](https://github.com/comfyanonymous/ComfyUI/pull/10302)).  For a 1280x1600 image, VAE decode's RAM usage roughly doubled from 10GB to 19GB, but it now takes <5s for both old and new resolutions, whereas with cudnn it could take up to 100s for old or 30 mins for new, depending on image size.  (More details in [this comment](https://github.com/comfyanonymous/ComfyUI/pull/10302#issuecomment-3447787820).)

---

### 评论 #7 — Enlightnd (2026-01-04T08:30:28Z)

You sure this isn't the default behavior where ROCm runs a full test suite to select the optimal kernels when it detects a new resolution.
A test that can take anywhere from 5 to 10 minutes, but should only run once (but if you tweak Comfy settings between runs, can actually be retriggered)?

---

### 评论 #8 — lostdisc (2026-01-04T22:11:22Z)

It is probably that.  The underlying slowness issues around that are being investigated [here](https://github.com/ROCm/TheRock/issues/2591).

---

### 评论 #9 — darren-amd (2026-01-20T22:09:15Z)

Hi all,

This issue is related to the performance issues observed with MIOpen. As pointed out above we are currently working on optimizations for these kernels and thus improvements in performance with ComfyUI. Please stay tuned for updates!

---

### 评论 #10 — darren-amd (2026-02-04T20:24:14Z)

Hi,

We've made many improvements to performance for ComfyUI workloads and through my testing I've observed more stability/improved performance on the latest torch + rocm wheels. We're actively making more improvements, which you can track here: https://github.com/ROCm/TheRock/issues/2591 for the latest updates. I wanted to check in if you're still running into driver timeouts with SDXL?

---

### 评论 #11 — lostdisc (2026-02-05T22:15:14Z)

I tried reenabling MIOpen and testing it with the new wheels for ROCm 7.2 and PyTorch 2.9.1 that were released a few weeks ago.  VAE decode still takes a long (long) time on gfx1150 (with a couple of driver timeouts for the first run at a given resolution), but I was able to collect logs this time; see [this comment](https://github.com/ROCm/TheRock/issues/2591#issuecomment-3856388371).

---

### 评论 #12 — chikei (2026-02-06T13:09:26Z)

ComfyUI 0.12.3 with torch 2.10.0+rocm7.12.0a20260204 and MIOpen enabled. Above basic workflow with 1536x1024 (w*h), I am still running into driver timeout.

---

### 评论 #13 — darren-amd (2026-02-10T16:23:25Z)

Hi @chikei,

I was not able to reproduce this on the latest torch + rocm-devel/libraries. 

Would you mind sharing your output of `pip list`, as well as your Adrenaline driver version? Also, are you still encountering the issue on smaller resolutions (such as the other 3 you reported issues on). We're continuing to work on further optimizations so this should be improved soon, we're also collecting logs in https://github.com/ROCm/TheRock/issues/2591 so if you get a chance please contribute to that as well, thanks!

---
