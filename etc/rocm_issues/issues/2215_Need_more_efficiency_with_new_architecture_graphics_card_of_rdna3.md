# Need more efficiency with new architecture graphics card of rdna3

> **Issue #2215**
> **状态**: closed
> **创建时间**: 2023-06-02T01:53:10Z
> **更新时间**: 2024-08-01T15:20:48Z
> **关闭时间**: 2024-08-01T15:20:47Z
> **作者**: PennyFranklin
> **标签**: hardware:Radeon
> **URL**: https://github.com/ROCm/ROCm/issues/2215

## 标签

- **hardware:Radeon** (颜色: #2B113F)

## 描述



Could ROCm please make use of the AI units that are already present in their rdna3 graphics card, especially after announcing that their 7x40 CPU has AI units? The current stable diffusion calculations feel like they were made without relying on the AI units, with the XTX graphics card having a fp32 computational power of 61.4t and image generation speed of more than twice that of the 2060 graphics card's 6.4t. They're not even on the same level. I would like to know when ROCm will improve the software calls to the hardware efficiency of the new architecture graphics cards, especially since the Radeon Pro W7900 graphics card has also been released.

---

## 评论 (17 条)

### 评论 #1 — evshiron (2023-06-02T09:12:11Z)

Maybe some resources:

* https://gpuopen.com/learn/wmma_on_rdna3/
* https://github.com/ROCmSoftwarePlatform/rocWMMA

The ROCm ecosystem still has a long way to go, which also means there is even greater room for improvement.

Many upstream supporting libraries are still in the early stages, and downstream developers will still prioritize CUDA over ROCm/HIP. ~~ROCm 5.5 has no official support for gfx1100, and ROCm 5.5.1's changelog is even late for a week.~~ Nevertheless, I am eagerly anticipating the release of ROCm 5.6, when things will be much easier to use.

---

### 评论 #2 — PennyFranklin (2023-06-02T17:35:58Z)

Well, time will tell us everything. Looking for the day rocm have both compatibility and efficiency. 

---

### 评论 #3 — PennyFranklin (2023-06-29T16:00:31Z)

The rocm5.5 already supposed gfx1100, because I successfully ran sdwebui with nightly pytorch with rc5.5. But it's just 'supported', not 'optimized'. The rocm5.6.0 also released, i wonder if there is some efficiency improvement with gfx11.

---

### 评论 #4 — johnnynunez (2023-06-29T16:01:51Z)

> The rocm5.5 already supposed gfx1100, because I successfully ran sdwebui with nightly pytorch with rc5.5. But it's just 'supported', not 'optimized'. The rocm5.6.0 also released, i wonder if there is some efficiency improvement with gfx11.

https://community.amd.com/t5/rocm/new-rocm-5-6-release-brings-enhancements-and-optimizations-for/ba-p/614745/jump-to/first-unread-message

``
We’ve also seen tremendous interest from developers wanting to run the ROCm open software platform for AI and ML on our Radeon™ consumer and Radeon™ Pro workstation GPUs and have heard the community challenges with specific driver issues on unsupported GPUs. I’m pleased to say that we have fixed the reported issues in ROCm 5.6 and we are committed to expanding our support going forward.  

We plan to expand ROCm support from the currently supported[ AMD RDNA 2 workstation GPUs: the Radeon Pro v620 and w6800](https://docs.amd.com/en/docs-5.0.2/CHANGELOG.html#radeon-pro-v620-and-w6800-workstation-gpus) to select AMD RDNA 3 workstation and consumer GPUs. Formal support for RDNA 3-based GPUs on Linux is planned to begin rolling out this fall, starting with the 48GB Radeon PRO W7900 and the 24GB Radeon RX 7900 XTX, with additional cards and expanded capabilities to be released over time.
``



---

### 评论 #5 — evshiron (2023-06-29T16:03:23Z)

Not so much at the moment until https://github.com/ROCmSoftwarePlatform/flash-attention gets Navi 3x support.

I am getting 17it/s when doing benchmark with https://github.com/vladmandic/sd-extension-system-info, and AITemplate gives me 25it/s, but I am expecting 40it/s (and more).

---

### 评论 #6 — evshiron (2023-07-02T17:30:43Z)

I upgraded ROCm from 5.5.1 to 5.6 today, and built `torch` nightly for ROCm 5.6 locally.

There is 10-20% performance boost when generating images, which is pretty cool.

---

### 评论 #7 — PennyFranklin (2023-07-03T06:19:33Z)

It sounds pretty cool. But after downloading your torch, how can I put it in the sdwebui to replace the old one? 

---

### 评论 #8 — evshiron (2023-07-03T07:35:38Z)

I am using Vlad's, and I will guess some commands for you. The steps below might not work:

```bash
cd stable-diffusion-webui

# activate existing venv, path may vary
source venv/bin/activate

# uninstall existing torch and torchvision, torchaudio is not used
pip3 uninstall torch torchvision torchaudio

# install downloaded wheels, path may vary
pip3 install path/to/torch.whl
pip3 install path/to/torchvision.whl

# launch a1111 webui
./webui-user.sh
```

---

### 评论 #9 — PennyFranklin (2023-07-03T08:52:49Z)

Thanks a lot. I'll have a try soon later. 

---

### 评论 #10 — PennyFranklin (2023-07-03T09:37:05Z)

Well..I followed the instruction to install and it said the torch and torchvision successfully been installed, but the performance of image generation seems not improved ,and the torch seems not be replaced by your new version.By he way ,I'm using a1111's webui,7900xtx gpu.
![截图 2023-07-03 17-30-42](https://github.com/RadeonOpenCompute/ROCm/assets/104998459/3ae52016-c81c-4b2e-b8b5-0059b5be43db)


---

### 评论 #11 — evshiron (2023-07-03T10:05:11Z)

Do benchmark with this extension so we have a baseline:

* https://github.com/vladmandic/sd-extension-system-info

Vlad's does have tweaks for better performance. I will benchmark in A1111's later.

---

### 评论 #12 — PennyFranklin (2023-07-03T13:02:49Z)

Here is the results,unexpectedly low...
![截图 2023-07-03 21-00-41](https://github.com/RadeonOpenCompute/ROCm/assets/104998459/312e28f7-d149-429f-9762-6211046b1b54)


---

### 评论 #13 — evshiron (2023-07-03T13:41:09Z)

Don't worry. You are still using old `torch` build. The low performance is due to AOT compilation. If you run it again, the performance will be back to normal.

To reach best performance, add `--opt-sdp-attention` to `COMMANDLINE_ARGS`, SDP will be faster then Doggettx (but not as fast as it is for CUDA).

Then install wheels from:

* https://github.com/evshiron/rocm_lab/releases/tag/rocm-5.6-builds

~~I have uploaded some wheels for temporary use until I actually fix the versioning (been doing this all day).~~

<img width="1224" alt="Screenshot 2023-07-03 at 21 39 40" src="https://github.com/RadeonOpenCompute/ROCm/assets/8800643/0bb164d3-0303-4bcf-9934-69a89a7b9780">

For extra performance, use Vlad's, or tweak settings like "Token merge ratio".


---

### 评论 #14 — PennyFranklin (2023-07-03T14:23:34Z)

I made it! The new torch runs smoothly for now,and there's quite some  improments.
![截图 2023-07-03 22-23-15](https://github.com/RadeonOpenCompute/ROCm/assets/104998459/f606b443-9270-4897-a8f9-81ee8e931c9d)
 

---

### 评论 #15 — ppanchad-amd (2024-05-13T17:54:10Z)

@PennyFranklin Can you please test with latest ROCm 6.1.1? If resolved, please close the ticket. Thanks!

---

### 评论 #16 — johnnynunez (2024-05-13T18:22:53Z)

> @PennyFranklin Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

where is the link for windows? 
It appears 5.7.1

---

### 评论 #17 — PennyFranklin (2024-05-20T01:48:36Z)

> @PennyFranklin Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

I'm sorry but I sold my whole desktop including 79xtx and bought a r7000p2060 laptop for school lessons' frequently moving requirements. I'm waiting for the next generation 8000 Radeon cards for now.

---
