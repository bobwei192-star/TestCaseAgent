# [Feature]: ROCm Support for AMD Ryzen 9 7940HS with Radeon 780M Graphics

> **Issue #3398**
> **状态**: open
> **创建时间**: 2024-07-05T14:10:51Z
> **更新时间**: 2026-02-23T19:46:15Z
> **作者**: pearsonc
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3398

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Hi ROCm Development Team,

I hope this message finds you well. I am writing to request the development of ROCm (Radeon Open Compute) support for the AMD Ryzen 9 7940HS processor paired with Radeon 780M graphics.

The AMD Ryzen 9 7940HS is increasingly becoming a popular choice among both professional and enthusiast communities due to its impressive performance and energy efficiency. With its powerful integrated Radeon 780M graphics, this chip is making its way into a variety of setups, particularly in home labs, small-scale development environments, and DIY computing projects.

However, the lack of ROCm support for this processor is a significant drawback for many users. The home lab community, which often relies on AMD hardware for its balance of cost, performance, and energy efficiency, is currently feeling excluded. This lack of support is leading to considerable frustration and regret among users who have invested in this otherwise excellent hardware.

Integrating ROCm support for the Ryzen 9 7940HS would not only enhance the capabilities of these systems but also expand the reach and adoption of AMD’s hardware in various computing environments. The home lab community, in particular, stands to benefit greatly from this support, enabling them to leverage ROCm’s powerful computing capabilities for a range of applications, from machine learning and AI development to advanced data analytics and scientific computing.

Moreover, extending ROCm support to this processor will demonstrate AMD’s commitment to providing comprehensive support across its product range, thereby strengthening customer loyalty and satisfaction. Given the growing popularity of the Ryzen 9 7940HS, I believe that this enhancement aligns well with AMD’s strategic goals and market demands.

Thank you for considering this request. I am confident that this addition would be highly appreciated by a broad segment of your user base and would significantly enhance the usability and appeal of AMD’s hardware in diverse computing environments.

Best regards,

Chris Pearson

### Operating System

Linux

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (36 条)

### 评论 #1 — AlexHe99 (2024-07-05T14:48:50Z)

Hello, I just commit a pull request (https://github.com/ollama/ollama/pull/5426) which is a tutorial in markdown file to guide enable AMD iGPU780M with ROCm.  I hope it should be a beginning to answer this FR. It is waiting for your review and happy to see it will be merged soon into Ollama repo.

---

### 评论 #2 — lqyiwwx (2024-07-14T06:42:38Z)

I hope the development team can consider the adaptation of nuclear display.

---

### 评论 #3 — pearsonc (2024-07-24T09:39:52Z)

> Hello, I just commit a pull request ([ollama/ollama#5426](https://github.com/ollama/ollama/pull/5426)) which is a tutorial in markdown file to guide enable AMD iGPU780M with ROCm. I hope it should be a beginning to answer this FR. It is waiting for your review and happy to see it will be merged soon into Ollama repo.

This is awesome, great work.

I do have other requirements for rocm though so I hope the development team consider this request to add support for iGPU's including the 780M.

---

### 评论 #4 — CallmeAG (2024-08-09T02:48:45Z)

Is this feature supported currently? I've been working on this APU recently, and I'm eagerly anticipating a guide or tutorial.

---

### 评论 #5 — santiago-afonso (2024-08-18T20:51:10Z)

I just cannot believe the poor support provided for the Radeon APUs. I had a better chance of running accelerated code on my 6 year old laptop with a discrete GPU than with this brand new APU. Huge purchasing error.

---

### 评论 #6 — euuurgh (2024-08-29T14:10:13Z)

Definitely a +1 from me. When I bought the CPU, a 7640U with 760M in my case, I though it would just be supported. Why would such a recent APU not be supported?

Now the unfortunate surprise to find not just the GPU unsupported, but also the Ryzen AI NPU that is advertised on my CPUs [product page](https://www.amd.com/en/products/processors/laptop/ryzen/7000-series/amd-ryzen-5-7640u.html) does not show up on rocminfo.

I'm a student and really can't afford a desktop AND a laptop. I can definitely live with having slow inference and training times, I can just run it overnight, but having the GPU not supported at all, leaving the CPU to fend for itself is such a disappointment.

I paid for the hardware; for the love of God, please let me use it. 

---

### 评论 #7 — fenio (2024-10-15T17:17:37Z)

I bought Deskmeet x600 for my lab and I equipped it with Ryzen 7 8700G.
https://www.amd.com/en/products/processors/desktops/ryzen/8000-series/amd-ryzen-7-8700g.html
I also thought it will be simply supported. Not sure why are AI capabilities listed on its page. Seems to be pretty useless for this purposes.

---

### 评论 #8 — euuurgh (2024-10-15T18:57:57Z)

Good news: I've been keeping an eye on Phoronix to see any updates on the xdna driver situation, and in this article: https://www.phoronix.com/news/AMD-XDNA-Linux-Driver-v4 from 3 days ago reports on the fourth revision of xdna drivers undergoing code review.

The article states that the earliest release these drivers can be merged into is 6.13 at the end of November. Stable distros won't get that kernel into their repos till February, but one can always just use the bleeding edge of releases. The thing is that applications need to utilize the xdna hardware inside these CPUs, so it's also worth to keep up to date on progress of xdna support on projects like llama.cpp

Really disappointed from AMD, not supporting iGPUs on ROCM is already a serious blunder, but releasing chips with a boatload of AI-hype-milking-marketing™ and only providing access to the hardware two years after release is purposefully misleading and a really shitty thing to do. Do better

---

### 评论 #9 — pearsonc (2024-10-24T13:00:08Z)

Has anyone on the ROCM team even looked at this?

---

### 评论 #10 — euuurgh (2024-10-24T15:23:26Z)

> Has anyone on the ROCM team even looked at this?

I don't think it's up to the engineers, but to management to finally support mobile gpus on ROCm, but they don't seem to deem it worthy to invest engineering resources in.
Maybe Strix Halo will change _anything_, but I might just be huffing hopium at that point. I mean god damnit: They can't even properly support the NPU

---

### 评论 #11 — johnnytshi (2024-11-11T19:38:35Z)

+1, absolutely need this for Strix Halo

---

### 评论 #12 — bkamuz (2024-11-16T16:29:43Z)

+100
We all really need iGPU support, including AMD Ryzen 9 7940HS with Radeon 780M graphics

---

### 评论 #13 — pearsonc (2024-12-07T22:15:46Z)

Maybe if we all duplicate this issue individually and mass post it to the issues list it might get some attention!

---

### 评论 #14 — euuurgh (2024-12-07T22:19:00Z)

> Maybe if we all duplicate this issue individually and mass post it to the issues list it might get some attention!

Thats a great way to get a lot of engineers mad because they had to block a bunch of accounts and close duplicate tickets instead of actually working on ROCm, while the actual decision makers don't even notice  

---

### 评论 #15 — dkull (2024-12-18T19:36:55Z)

Just received an expensive fully AMD work laptop, the Lenovo T16 Gen2, with 7840U and 780M. I was expecting lightweight LLM loads to be supported by the GPU, but I am disappointed to see the lacking hardware support. +1 for 780M support on Windows and Linux.

---

### 评论 #16 — euuurgh (2024-12-18T19:50:47Z)

> Just received an expensive fully AMD work laptop, the Lenovo T16 Gen2, with 7840U and 780M. I was expecting lightweight LLM loads to be supported by the GPU, but I am disappointed to see the lacking hardware support. +1 for 780M support on Windows and Linux.

Small tip: If you use a frontend for llama.cpp, work can be pushed to the GPU via the Vulkan compute API. There are plenty of applications requiring ROCm though, and the lack of support from AMDs side is just stunning.

---

### 评论 #17 — difrost (2025-01-06T18:20:54Z)

Hi Folks,

I'm trying to make the 890M and/or the XDNA NPU to work with ollama. I've got the XDNA driver up and running, there are some issues with the amdgpu stability, but I would like to testdrive both.

Any links I could use?

Cheers

---

### 评论 #18 — sailorbob74133 (2025-01-09T20:18:26Z)

Take a look at this thread about XDNA support in the llama.cpp project:
https://github.com/ggerganov/llama.cpp/issues/1499

---

### 评论 #19 — JonChesterfield (2025-01-09T23:43:27Z)

The rocm packaged by debian ran fine out of the box on a 4800U a few weeks back. That's pretty similar to the APU being asked about here. I haven't tried the official binaries.

---

### 评论 #20 — superjamie (2025-01-10T00:21:48Z)

I have an easy way to compile llama.cpp with ROCm for any AMD GPU here:

https://github.com/superjamie/rocswap

This uses the Debian ROCm library which supports more GPUs than the official ROCm library. Anything RX Vega or newer should compile and run.

Not sure about the new chips discussed here, but I've tried this with a 5600G integrated GPU and it was no faster than CPU inference because the bottleneck is not processing speed but RAM speed.

I doubt AMD will add official ROCm support for these GPUs. The latest ROCm release just *dropped* support for 7800XT - literally 15 month old hardware.

I've seen ROCm developers commenting on Mastodon and they're positive helpful folks, but management are calling the shots here and their focus seems to be on enterprise accelerators and commercial distros. The devs likely have no time left over for us hobbyists with desktop GPUs.

Edit: Talking to some folks, RDNA APUs do see a small speedup when using ROCm, so that seems worth tinkering with.

---

### 评论 #21 — lhl (2025-01-10T16:42:22Z)

While official support should be a thing, on Linux at least, it’s relatively easy to install ROCm and just use `HSA_OVERRIDE_GFX_VERSION=11.0.0` to get any RDNA3 APU running.

---

### 评论 #22 — difrost (2025-01-12T11:00:14Z)

Thanks folks, I've actually manged to get Ollama running with ROCm on 890M iGPU - pretty decent performance TBH (see https://github.com/ollama/ollama/issues/3004). Now when AMD released [initial support](https://github.com/Xilinx/llvm-aie/commit/685e83f8f375b088517d80322ea7e78f1e0de56e) for Strix Point in LLVM-AIE it should be easier to get the XDNA2 into llama.cpp.

---

### 评论 #23 — hashangit (2025-02-21T03:37:08Z)

No support yet for gfx1150 in 6.3.3 as far as I can see. AMD needs to make their AI laptops actually capable of doing proper hybrid CPU,GPU,NPU inferencing. 

---

### 评论 #24 — euuurgh (2025-02-22T08:01:18Z)

> No support yet for gfx1150 in 6.3.3 as far as I can see. AMD needs to make their AI laptops actually capable of doing proper hybrid CPU,GPU,NPU inferencing.

uuuuuuhm, you might want to go with 6.10+ if you are gonna use new hardware...
The latest release is 6.13.3, 6.3 was released on the 23 of April 2023, long before the release of RDNA 3.5, so how could it support it?

---

### 评论 #25 — lhl (2025-02-22T09:46:21Z)

@euuurgh he’s talking about ROCm not the kernel. I assume that you can use an HSA override as I mentioned before to get it working like w/ other unsupported RDNA3 chips, but it still shows how unserious AMD is to release an “AI” chip without support for their AI framework. Who allows that to even happen? Is there no one at AMD that’s not ok with that?

---

### 评论 #26 — euuurgh (2025-02-22T09:58:14Z)

Oooh, there are multiple threads about GPU/NPU support I am a part of, and thought I was in a different one. That makes much more and much less sense at the same time. AMD does not support mobile graphics for ROCm period.

1151 with Halo and mobile variants of desktop cards - sure.

The problem is not that they did not release support for gfx1150, but that they never will.
I commented on another thread that this is a absolute shame, and that they should support their mobile segment as well, but the way hashangit worded it seemed like they were complaining about drivers, as inference is already possible through llama.cpp with the Vulkan API, on all modern GPUs.

---

### 评论 #27 — da-phil (2025-02-23T20:04:53Z)

> While official support should be a thing, on Linux at least, it’s relatively easy to install ROCm and just use `HSA_OVERRIDE_GFX_VERSION=11.0.0` to get any RDNA3 APU running.

It is interesting that the limitation seems to only apply to their ROCM HIP interface (I suppose? correct me if I'm wrong), while their ROCr OpenCL interface (rocm-opencl package) seems to work flawlessly in darktable (image processing program) without any HSA override hacks for me.

But yeah, it's a big shame AMD is disappointing and putting off so many (once loyal) customers who just want to do AI work on their consumer grade GPUs, just letting them go to their "CUDA competitor" so easily.

---

### 评论 #28 — OrsoEric (2025-03-12T10:49:26Z)

> Definitely a +1 from me. When I bought the CPU, a 7640U with 760M in my case, I though it would just be supported. Why would such a recent APU not be supported?

I have the same APU, currently I'm running LM Studio with llama.cpp Vulkan runtime and it does accelerate LLM inference no issues.  I get about 3T/s on 14BQ4 models.

On my desktop Vulkan incours into a severe performance penality compared to ROCm runtime (around 1/5 on my system), I don't know if there is a similar penality on 760M because I haven't tried ROCm in there.

As for the NPU, I saw online someone that made it work, but was much slower acceleration than the iGPU in LLM inference. It's just 10 TOPS.

I haven't tried but AMD has this application:
https://github.com/amd/RyzenAI-SW/tree/main

---

### 评论 #29 — kevinzhow (2025-03-24T02:56:49Z)

Following several tests, I found that with ROCm 6.2.4, `HSA_OVERRIDE_GFX_VERSION=11.0.2` is compatible with PyTorch 2.8. However, for `onnxruntime-rocm`, `HSA_OVERRIDE_GFX_VERSION=11.0.1` may be necessary. Even with this configuration, segmentation faults can occur with different models.


---

### 评论 #30 — tangibleaiadmin (2025-06-13T20:48:07Z)

I need this feature for  ML research on my Framework Laptop.

---

### 评论 #31 — YuHayring (2025-06-16T02:17:44Z)

> I need this feature for ML research on my Framework Laptop.

There is a third-party support. https://github.com/lamikr/rocm_sdk_builder

---

### 评论 #32 — kainsk (2025-11-29T10:02:55Z)

+1
need iGPU support AMD Ryzen 9 7940HS with Radeon 780M graphics


---

### 评论 #33 — dreirund (2025-11-29T11:04:31Z)

[Comment #15092178 in discussion #2631](https://github.com/ROCm/ROCm/discussions/2631#discussioncomment-15092178) says that it now is supported:

> *ROCm officially supports gfx1103 starting with v7.1.0: [\[rocBLAS\] Add rocblas support for gfx1103](https://github.com/ROCm/rocm-libraries/pull/1320)*

---

### 评论 #34 — z3rg (2025-12-06T22:48:40Z)

for ollama 780m build see here https://github.com/z3rg/ollama-AMD-Radeon-780M

<img width="1680" height="152" alt="Image" src="https://github.com/user-attachments/assets/2bbc2e57-3c8e-42bd-ad0a-23d55445ad58" />

---

### 评论 #35 — alpharder (2026-02-23T00:29:04Z)

What a joke is the existence of this issue in 2026! 

Selling my AMD hardware and switching to Intel just because of AMD's moronic idea of putting some unusable and unsupported hardware into the market. Great job, AMD!

---

### 评论 #36 — johnnytshi (2026-02-23T19:46:14Z)

you can use the https://github.com/ROCm/TheRock for 780M, its more cutting edge anyways

---
