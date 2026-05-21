# [Issue]: ROCm 6.2.3 in WSL seems to regress?

> **Issue #4119**
> **状态**: closed
> **创建时间**: 2024-12-06T04:50:53Z
> **更新时间**: 2026-01-12T19:54:27Z
> **关闭时间**: 2026-01-12T19:54:27Z
> **作者**: evshiron
> **标签**: Under Investigation, ROCm 6.2.3, RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4119

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

I was using ComfyUI in ROCm 6.1.3 for WSL with PyTorch `2.5.1+rocm6.1`, and it was working pretty well.

As ROCm 6.2.3 for WSL rolling out, I installed [Adrenalin Edition 24.12.1](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-12-1.html), `amdgpu-uninstall` previous ROCm 6.1.3 installation in WSL, and reinstalled ROCm 6.2.3 following the [instructions](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html).

For ComfyUI, I `pip3 --force-reinstall` PyTorch `2.5.1+rocm6.2`, and launched it using `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python3 main.py --use-pytorch-cross-attention`.

In my simple SDXL workflow, which directly generates an image of 1024x1536, the host driver keeps timed out during VAE decoding. Until I mess around and remove `~/.triton`, it progresses but with a warning of "Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding", which has never been seen when using ROCm 6.1.3 for WSL.

The overall experience is not satisfying, tiled upscaling has also stuck for some time.

### Operating System

Ubuntu 22.04.5 LTS in WSL 2 in Windows 10 22H2

### CPU

Ryzen 7 7800X3D

### GPU

RX 7900 XTX

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

![ComfyUI_114514](https://github.com/user-attachments/assets/d83d0ef1-e438-4e07-ac1e-7525ea4172be)

Drag the image into ComfyUI to load the workflow, and then click "Queue Prompt".

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (17 条)

### 评论 #1 — xCentral (2024-12-06T13:27:38Z)

Try rolling back Adrenalin Edition 24.12.1 to Adrenalin Edition 24.9.1. I noticed a performance decrease on anything above this on generation side. With it significantly slowing down in the past as well. Not sure that's the issue, but was causing my slowdowns. Also using --use-pytorch-cross-attention

---

### 评论 #2 — zichguan-amd (2024-12-09T16:05:15Z)

Hi @evshiron, thanks for reporting. I do observe the issue with rocm6.2 on WSL, I've tested with older Adrenalin drivers, and it seems that the problem is with the new ROCm release on WSL. I've reached out to internal team to investigate.

---

### 评论 #3 — githust66 (2024-12-10T06:01:59Z)

ROCm 6.3 has the same problem on the WSL

---

### 评论 #4 — githust66 (2024-12-10T06:08:27Z)

> Try rolling back Adrenalin Edition 24.12.1 to Adrenalin Edition 24.9.1. I noticed a performance decrease on anything above this on generation side. With it significantly slowing down in the past as well. Not sure that's the issue, but was causing my slowdowns. Also using --use-pytorch-cross-attention

I have tried Adrenalin Edition 24.9.1 and the speed is the same down, removing the- -use-pytorch-cross-attention parameter speed is normal

---

### 评论 #5 — zichguan-amd (2024-12-11T19:08:53Z)

Hi @evshiron, just want to confirm which model are you using? I managed to repro the issue once, but I can't get it to hang anymore. It either runs with tiled VAE or the driver times out but VAE decode still manages to finish.

---

### 评论 #6 — evshiron (2024-12-11T19:38:17Z)

@zichguan-amd

It's [NoobAI-XL](https://civitai.com/models/833294?modelVersionId=1116447) if you are interested. In my case, it didn't use tiled VAE at the beginning and caused the hang. The VAE decoding no longer hung when tiled VAE was used, but ComfyUI always left a warning for it.

I switched back to ROCm 6.1.3 when [UltimateSDUpscale](https://github.com/ssitu/ComfyUI_UltimateSDUpscale) hung a lot. It might become smooth after some attempts, but I lost my patience at that time and had never tried again.

In my opinion, the release of ROCm 6.2.3 for WSL is a step down in user experience from the ROCm 6.1.3 one.

---

### 评论 #7 — zichguan-amd (2025-01-08T17:03:12Z)

Hi @evshiron, the next WSL release should address this issue.

---

### 评论 #8 — githust66 (2025-02-06T05:24:01Z)

> Hi [@evshiron](https://github.com/evshiron), the next WSL release should address this issue.

I also encountered this problem, the whole system is stuck for a long time, and sometimes the pop-up driver times out after the stuck recovery, which makes it impossible to complete the picture output, when will the next WSL version of ROCM be released?

---

### 评论 #9 — zichguan-amd (2025-02-06T16:03:04Z)

Unfortunately, I don't know when will the next ROCm for WSL be released. For the time being, if you are experiencing issues with 6.2.3, please consider using 6.1.3 instead.

---

### 评论 #10 — amd-zoybai (2025-02-06T17:45:32Z)

The new ROCm 6.3.2 has been released this week, it may alleviate the issue a little bit.

---

### 评论 #11 — githust66 (2025-02-07T00:55:07Z)

> The new ROCm 6.3.2 has been released this week, it may alleviate the issue a little bit.

I tried ROCm 6.3.2 and still got stuck and timed out when I got to the VAE decoder node. I'll go down to 6.1.3 and get feedback

---

### 评论 #12 — githust66 (2025-02-07T04:24:29Z)

> Unfortunately, I don't know when will the next ROCm for WSL be released. For the time being, if you are experiencing issues with 6.2.3, please consider using 6.1.3 instead.

It seems that 6.1.3 will also get stuck and then time out.

![Image](https://github.com/user-attachments/assets/82efdbda-afd2-4b58-98cb-52d27ac2a7a6)

---

### 评论 #13 — zichguan-amd (2025-02-07T15:15:06Z)

Which Adrenalin driver are you using with 6.1.3? Adrenalin 24.9.1 with ROCm 6.1.3 should have no problem.

---

### 评论 #14 — githust66 (2025-02-08T02:09:37Z)

> Which Adrenalin driver are you using with 6.1.3? Adrenalin 24.9.1 with ROCm 6.1.3 should have no problem.

I have tried versions 24.9.1 and 24.12.1, and the situation is the same.I suspect that it is due to insufficient memory. I will try adding a memory stick and then come back for feedback.

---

### 评论 #15 — githust66 (2025-02-11T06:29:12Z)

> > Which Adrenalin driver are you using with 6.1.3? Adrenalin 24.9.1 with ROCm 6.1.3 should have no problem.
> 
> I have tried versions 24.9.1 and 24.12.1, and the situation is the same.I suspect that it is due to insufficient memory. I will try adding a memory stick and then come back for feedback.

After increasing the memory by 16g, the same problem still exists.

---

### 评论 #16 — zichguan-amd (2025-02-18T22:47:36Z)

Hi @githust66, thanks for reporting it. Internal team is aware of the issue and is working on it. I'll update when we have more details.

---

### 评论 #17 — zichguan-amd (2025-09-11T20:56:55Z)

The issue should be fixed by the [25.8.1](https://www.amd.com/en/resources/support-articles/release-notes/rn-rad-win-25-8-1.html) driver. Please let me know if you are still encountering TDR issues with latest driver.

---
