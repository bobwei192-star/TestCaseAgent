# Did rumored Fiji / Fury / nano / gfx803 support in ROCm 5.5 Release happen?

> **Issue #2101**
> **状态**: closed
> **创建时间**: 2023-05-02T22:46:02Z
> **更新时间**: 2024-02-15T16:09:20Z
> **关闭时间**: 2024-02-15T16:09:20Z
> **作者**: RhynarAI
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2101

## 描述

Since "the internet reported" about Fury support in the upcoming release, I was getting my hopes up for a re-use of my Fury X... I can´t spot any mentioning of it in the release notes in V 5.5

Could the ROCm team please clarify? Older posts state "dropped support" for gfx803/Fury/Fiji

---

## 评论 (10 条)

### 评论 #1 — saadrahim (2023-05-05T17:30:55Z)

I do apologize, the rumours are not true. Fiji support has been dropped. There is no plan to add it back.

---

### 评论 #2 — RhynarAI (2023-05-05T18:44:41Z)

Thanks for confirming. That´s too bad. I just looked up the GPU support over at AMD.docs - only  a handfull of GPUs are supported, most of them being enterprise cards. I had some VEGA64/FE, too which are quite capable of computing FP16 workloads, but these also are not suported anymore.

I really wantd to stick with AMD - but it seems its much easier to simply sell the cards and get a midrange NVIDIA.. With Cuda, I can take any Maxwell Card from the past and just get going - with tensor cores, even a 300 bucks 3060 outperformes a VEGA VII in most inferences..

Its often mentioned - but AMD really should change the tactics in these fields. I get that gaming and bigger data centers are a market - but upscaling inferences, stable diffusion and stuff like this gets more and more important - and AMD is missing out here by a lot.



---

### 评论 #3 — xuhuisheng (2023-05-05T23:20:17Z)

@RhynarAI 
If you are special interesting in gfx803 - fiji, polaris, you can try my patch : <https://github.com/xuhuisheng/rocm-gfx803>

Some kind people said they can run Stable diffusion on gfx803 sucessfully. But I hadn't confirm it by myself.

And, gfx900 - vega64 is just on the AMDGPU_TARGETS list, I don't know why AMD didn't include gfx900 on the supporting list. It should run without any patch. I sugguest you give a try.

---

### 评论 #4 — cgmb (2023-05-07T22:00:57Z)

This was a bit of a miscommunication. The support table had a column that described which parts of the stack the table was describing. It was listed as "full" because the information in the columns to the right applied to the entire stack.

The gfx803 architecture is still available in the binaries that AMD provides for the ROCm math and communication libraries, although you need to set the environment variable `ROC_ENABLE_PRE_VEGA=1` to enable support in ROCclr. However, AMD stopped testing the gfx803 architecture with ROCm 3.5 and there are some known bugs (e.g., with certain operations in rocBLAS). Similarly, there has been no testing for gfx900 since ROCm 4.5. Trying to communicate this situation was one of the goals of the updated support table.

The ROCm librararies are still open to receiving patches that fix issues on these architectures, but stability is also quite important. We can't accept patches that fix some things and break other things. If you have a targeted fix for a problem on an unsupported architecture, you may want to ping me on the PR and I will try to help it along (as not all developers have easy access to unsupported hardware for testing those kinds of changes).

However, I would encourage you to work with one of the distros in maintaining support for these older architectures. I'm pretty involved with Debian and the primary maintainers of ROCm on that platform all have gfx803 GPUs available. They have also enabled ROC_ENABLE_PRE_VEGA by default so you don't have to set the environment variable. The one thing they don't have is very much free time. They're already very busy just trying to get ROCm packages into Debian at all, so I'm sure they would be happy if you want to help test packages on gfx803 and file bug reports. If you have a good patch, the turnaround time for a release of a new version of a distro package with a bugfix is likely to be much faster than a new ROCm release.

---

### 评论 #5 — RhynarAI (2023-05-25T05:58:54Z)

Thank you to both of you for responding. SOrry for my late reply, got manged up at work :)
I´ll have to free up some time to fiddle a little more with it, seems it is possible to get the Furys running somehow - And while I love tampering with this kind of stuff (its a challenge) - AMD would really do itself a favour if they made "stuff like this simpler". In the meanwhile, I grabbed my 3060 , installed it and was ready to go with everything I wanted to get done/try out/etc... Same card for gaming, video editing, inference loads for video editing, etc... And it works - out of the box. No "use this patch, swap the kernel, stick to this distro"...

Meanwhile, the internet is still confused about which cards run and which don´t - since AMD is getting a little into the game, any community I watch that somehow needs compute power has picked up on the new AI API, Rocm releases, HIP Support in Blender and things like this... And in EVERY Discussion, no one has a clue what works and what not - and this fires back on AMD - while one should think that its "Good news" that AMD gets more involved -bad communication or "only nerds get it running" attidude leads to a situation, where the "good news" in discussions turns into: "now we know for sure - stick to Nvidia"... Before, no body was really sure if AMD could be used  - now they have 20 people in the discussion who all tried, failed and therefore switched to Nvidia.... Much worse situation, marketing-wise...

So sad.... I recently used a Fury in ONNX Inference - this oldie really packs a punch, still today..

---

### 评论 #6 — xuhuisheng (2023-05-25T06:21:32Z)

BTW, I upload a patch for blender with gfx803, too.
Anybody who interested can take a try: <https://github.com/xuhuisheng/rocm-gfx803/blob/master/blender.md>

---

### 评论 #7 — RhynarAI (2023-07-14T11:19:58Z)

Thanx for this. 

I see that  a lot is possible to get running when doing some patching here, fiddling there... Sadly, I don´t have the time to tamper with all of this - as a hobby "to get it going", its fine - but in a serious workflow environment, time is money... the time to get stuff running simply is not worth it - compared to NVIDIA, where even old maxwell cards simply work...

(this is mostly aimed at AMD, not your patch - I really do think AMD should change the taktiks about supporting older GPUs .... Although I do own a lot of AMD GPUs and don`t like the fact that for most creative workloads people simply buy Nvidia - I can totally understand the decisions.. )


I appreciate your patches - if I find time, I`ll dig into this - but it really is too much effort to get stuff running, the Fury will probably find the way to ebay before I find time to dig in...

---

### 评论 #8 — nartmada (2024-02-14T04:03:31Z)

Hi @RhynarAI, sorry we are not able to help you much on this ticket.  Can we close the ticket?  Thanks.

---

### 评论 #9 — RhynarAI (2024-02-15T15:55:09Z)

Thank you for catching up. 

It was too much work for me to get the Fury running. I did use it in DIRECT ML Workloads a few times, but eventually sold them and got a NVIDIA GPU - now I can run everything without much trouble and the speeds are much better...

Would have loved to stay with AMD..

---

### 评论 #10 — RhynarAI (2024-02-15T15:57:21Z)

> Hi @RhynarAI, sorry we are not able to help you much on this ticket. Can we close the ticket? Thanks.

yes, the ticket can be closed. Thank you.

---
