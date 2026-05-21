# [Feature]: Wait... Is this real?

> **Issue #2782**
> **状态**: closed
> **创建时间**: 2024-01-07T18:54:34Z
> **更新时间**: 2024-06-19T18:05:44Z
> **关闭时间**: 2024-06-19T18:05:43Z
> **作者**: theron29
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2782

## 描述

### Suggestion Description

So... can we just throw away our otherwise functioning NAVI GPUs... because there is, and will not be, any further support?! :sob: 

![obrazek](https://github.com/ROCm/ROCm/assets/40362621/947fb081-7705-42f3-af1a-40715f33006f)


### Operating System

Ubuntu 22.04

### GPU

RX 5600 XT

### ROCm Component

Any relatively new (and supported)

---

## 评论 (13 条)

### 评论 #1 — ethragur (2024-01-09T09:25:28Z)

Yes for now gfx1010 cannot be used with ROCM >= 5.3, see issue #2527 for more details

---

### 评论 #2 — theron29 (2024-01-10T17:37:14Z)

Yes. Well... I was thinking maybe it is time to actually upgrade my GPU to something newer (and, maybe, supported), especially something with more VRAM. So I was originally planning to buy a new RX7xxx.

Then I saw this^^^ and I finally realized: Why would I invest a lot of money to the latest RDNA3 GPU, when it might/will actually get obsoleted, yet again, by AMD in year or two? So I will get stuck in the same situation we are now with RDNA1 and RDNA2 GPUs quite soon?

(And the worst thing is that from the AMD side, everything is quiet about this! No "that is not correct" or "it is not working that way" or "we have plans...". No, just silence!)

This behaviour is so anti-consumer that I have a hard time to stay polite here!

---

### 评论 #3 — ethragur (2024-01-10T23:10:27Z)

Yeah sadly this is the case. As much as I love AMD GPU's their attitude towards consumer products is terrible. I have old Nvidia Maxwell GPU's which are better supported than 2-3 generations old AMD GPU's. Their attitude towards consumer gpu's really needs to change. 
Having great support for pytorch on their enterprise GPU's is nice, but most of the developers for AI software are using normal consumer grade GPU's and their support with those is abysmal. As long as they cannot fix those issues, AMD will always be behind. Hopefully that will change, but for now we will have to see and wait

---

### 评论 #4 — Randommist (2024-01-21T14:35:51Z)

If rocm is an open source driver, then why aren't there any enthusiasts who would add the necessary support? Not long ago I became the owner of an rx 5700 and I am very upset by this situation

---

### 评论 #5 — DGdev91 (2024-01-29T21:53:55Z)

> Yes for now gfx1010 cannot be used with ROCM >= 5.3, see issue #2527 for more details

It's a bit different. You can have the last version installed, but pytorch (and i guess every other software wich rely on rocm) must be compiled for rocm <= 5.2.
Also, in the same issue you linked, hongxiayang from amd said they were trying to work on it in november, but then 3 days ago commented again saying that since the gpu isn't officially supported it's just normal that newer versions could not work.

I mean, i get that, Navi1 wasn't never supported officially and works on older pytorch versions just thanks to a workaround.


> If rocm is an open source driver, then why aren't there any enthusiasts who would add the necessary support? Not long ago I became the owner of an rx 5700 and I am very upset by this situation

There are, sometimes. For example, i just found that 5 days ago was merged a PR wich aims to make life easier for using rocBLAS on gfx1010 (ironically, it was a problem i experienced myself)
https://github.com/ROCm/Tensile/pull/1862

---

### 评论 #6 — Spacefish (2024-01-29T22:14:46Z)

Had a 5700XT since years and it worked some time with ROCm but 5.4 broke it, as mentioned. I now upgraded to a 7800XT which seems to work fine with HSA_OVERRIDE_GFX_VERSION=1030, unless you use a lot of VRAM, then the compositor crashes 😅.
Guess this limits the card quite a lot though, as gfx1030 didn´t have the MMA instructions, but don´t know wether they are even used by the compiler in day to day code or if they are only availiable via instrinsics and it hand written kernels (which have to be availiable for gfx1100 in MIOpen for example and optimized to use the MMA instructions).

My two cents about the future:
AI is getting important on consumer platforms, especially since Microsoft is pushing this hard with Windows 11 and probably some future games. AMDs Solution seems to be the XDNA/XDNA2 Accelerators which are based on the IP acquired with Xilinx / they are almost identical to a "Xilinx AI Engine" Core configured for some limited set of data types.. 
But in addition AMD seems to push ROCm + GPU Compute for AI on Windows as well, not sure why.. But it´s good news for us! 

Speculation 1: One reason could be to be able to sell Chips with Integrated RDNA2/3 but without XDNA into low-end laptops with Windows 11, once Microsoft requires a certain AI inference performance on the Platform. If you can get away with less chip area by using the same silicon for the GPU and AI that saves a lot of money and Software Development cost is a one time thing + some maintenance but hardware production cost is per unit sold.

Speculation 2: AMDs strategic marketing saw the big influence the green teams platform has in AI and tries to push their own platform that way, but lowering the entry barrier. AI is seen as a big growth market in the next few years, with LLMs and Image Generation networks just getting broad visibility in late 2023.

Not sure at all where all of this leads us though.. As recent nets in image generation and LLMs need more VRAM than availiable in most consumer cards. Look at Mixtral 8x7B for example, the 4bit-quantized form needs 23GB VRAM for inference. The float16 version needs more than 90GB for inference, for training you need even more.
Only a MI300X offers that amount of VRAM currently (192GB). You can´t even use an A100 80GB for that.

IMHO local inference will be limited to smaller tasks, like the typical video conferencing things, like noise reduction, background blur, intelligent filters and so on.

---

### 评论 #7 — DGdev91 (2024-01-29T23:11:24Z)

Well, for me a "solution" for local interference with bigger models was llama-cpp with hipblas support, the gguf models can be partially offloaded to the gpu while the remaining datas are on system ram.
Of course this is way slower than running the whole model on the gpu, but still better than nothing.

Anyway... I suggest you to keep an eye on #2527

---

### 评论 #8 — GZGavinZhao (2024-02-02T03:51:43Z)

gfx1010 should be working fine after ROCm/Tensile#1862. If you can't wait for AMD to release the new rocBLAS, you may want to ask the ROCm maintainers of your distribution to back port that patch. It should apply cleanly to any ROCm version >= 5.5.

---

### 评论 #9 — DGdev91 (2024-02-02T13:54:13Z)

> gfx1010 should be working fine after [ROCm/Tensile#1862](https://github.com/ROCm/Tensile/pull/1862). If you can't wait for AMD to release the new rocBLAS, you may want to ask the ROCm maintainers of your distribution to back port that patch. It should apply cleanly to any ROCm version >= 5.5.

Well, yes... That PR makes the tensile library to be compiled by default, but this doesn't automatically mean that those will be added to the final packages, since it isn't an officially supported arch.
For example, cgmb said in #2527 that he expects to enable that "later this year" in debian packages, but it will probably not going to be included in the official amd ones.

It will probably depend on how each distributions builds his packages. But yes, it most likely will be automatically included.

I've just tried to compile the rocBLAS package from ArchLinux, changing a bit the pkgbuild to make it use version 6.0.2 and that patch (it has been merged to the develop branch, but not yet in 6.0.2). it does indeed compile the lib for gfx1010.
So, it will most likely just be a matter of time, and it will be included in arch packages without any change needed, at least for Arch.

---

### 评论 #10 — GZGavinZhao (2024-02-02T14:00:15Z)

I'm not sure about whether `gfx1010` is an officially supported arch, but I checked that as of 6.0.2 AMD's official rocBLAS debian package does compile with `gfx1010` support enabled. It's just that prior to my PR that lazy library wasn't being built, preventing `gfx1010` from being used. So as soon as they release a new minor rocBLAS version (presumably in ROCm 6.1?) that contains ROCm/Tensile#1862, you should be getting _full_ `gfx1010` support even with the official packages.

---

### 评论 #11 — Zakhrov (2024-04-24T09:14:03Z)

gfx1010 can be made to work. It just needs a few more hacks and steps than simply setting ``HSA_OVERRIDE_GFX_VERSION``
I've written up a mini-guide here:
[https://github.com/ROCm/ROCm/issues/2527#issuecomment-2074468176](https://github.com/ROCm/ROCm/issues/2527#issuecomment-2074468176)

---

### 评论 #12 — theron29 (2024-04-24T14:53:54Z)

> gfx1010 can be made to work. It just needs a few more hacks and steps than simply setting `HSA_OVERRIDE_GFX_VERSION` I've written up a mini-guide here: [#2527 (comment)](https://github.com/ROCm/ROCm/issues/2527#issuecomment-2074468176)

Thank you very much for your effort!

Aynways, I've stopped keeping my breath hoping for a miracle. AMD is a nogo for now and forseeable future for anything else HW accelerated than games. I might return to AMD-related HIP/ML topic in a year or two; maybe there is some progress by then... :disappointed: 

---

### 评论 #13 — ppanchad-amd (2024-06-19T18:05:44Z)

Closing ticket as this is not an issue. 

---
