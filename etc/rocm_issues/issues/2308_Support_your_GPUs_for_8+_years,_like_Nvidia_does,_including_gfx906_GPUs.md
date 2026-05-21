# Support your GPUs for 8+ years, like Nvidia does, including gfx906 GPUs

> **Issue #2308**
> **状态**: closed
> **创建时间**: 2023-06-30T07:48:02Z
> **更新时间**: 2024-10-13T15:42:36Z
> **关闭时间**: 2024-10-13T15:42:36Z
> **作者**: EwoutH
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2308

## 描述

I was utterly amazed to read this in the ROCm 5.6 [release notes](https://rocm.docs.amd.com/en/latest/CHANGELOG.html#rocm-5-6-0):

> - AMD Instinct MI50, Radeon Pro VII, and Radeon VII products (collectively referred to as gfx906 GPUs) will be entering the maintenance mode starting Q3 2023. This will be aligned with ROCm 5.7 GA release date.
>   - No new features and performance optimizations will be supported for the gfx906 GPUs beyond ROCm 5.7
>   - Bug fixes / critical security patches will continue to be supported for the gfx906 GPUs till Q2 2024 (End of Maintenance [EOM])(will be aligned with the closest ROCm release)

The Vega 20 GPU (gfx906) is barely 5 years old. Even more, the Radeon VII, Radeon Pro VII and Instinct MI50 are still being sold!

If you want to know why everyone is going with Nvidia, there are a lot of them, but what they do at least well is they support they GPUs.

In the CUDA 12.x release from December 2022, Nvidia also [dropped support](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#cuda-libraries) for some GPUs:

> Support for the following compute capabilities is removed for all libraries:
> - sm_35 (Kepler)
> - sm_37 (Kepler)

Yes, you read that right, _Kepler_ GPUs. These are 2014 products. Not 2019 products like you're dropping.

So, hereby I would you strongly urge to not force us all to Nvidia again, by properly supporting your products.

---

## 评论 (20 条)

### 评论 #1 — johnnynunez (2023-06-30T08:12:56Z)

> I was utterly amazed to read this in the ROCm 5.6 [release notes](https://rocm.docs.amd.com/en/latest/CHANGELOG.html#rocm-5-6-0):
> 
> > * AMD Instinct MI50, Radeon Pro VII, and Radeon VII products (collectively referred to as gfx906 GPUs) will be entering the maintenance mode starting Q3 2023. This will be aligned with ROCm 5.7 GA release date.
> >   
> >   * No new features and performance optimizations will be supported for the gfx906 GPUs beyond ROCm 5.7
> >   * Bug fixes / critical security patches will continue to be supported for the gfx906 GPUs till Q2 2024 (End of Maintenance [EOM])(will be aligned with the closest ROCm release)
> 
> The Vega 20 GPU (gfx906) is barely 5 years old. Even more, the Radeon VII, Radeon Pro VII and Instinct MI50 are still being sold!
> 
> If you want to know why everyone is going with Nvidia, there are a lot of them, but what they do at least well is they support they GPUs.
> 
> In the CUDA 12.x release from December 2022, Nvidia also [dropped support](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#cuda-libraries) for some GPUs:
> 
> > Support for the following compute capabilities is removed for all libraries:
> > 
> > * sm_35 (Kepler)
> > * sm_37 (Kepler)
> 
> Yes, you read that right, _Kepler_ GPUs. These are 2014 products. Not 2019 products like you're dropping.
> 
> So, hereby I would you strongly urge to not force us all to Nvidia again, by properly supporting your products.

7900xtx and similars including laptops are working now, but not has official support. For the whole community it is already great news, they have finally realized that the whole opensource community (consumer gpus) and PhD students can greatly accelerate the progress of this library. Hopefully they will also give native windows support soon, although it is optional, almost everyone uses linux for AI. 

---

### 评论 #2 — xcom169 (2023-06-30T09:35:27Z)

What about Vega56 / GFX9  is it still supported somehow?

---

### 评论 #3 — MelihDarcanxyz (2023-06-30T14:47:26Z)

While the development of [NVK](https://gitlab.freedesktop.org/nouveau/mesa/-/tree/nvk/main) (a new open source Nvidia driver) is advancing, Nvidia is supporting their GPUs for at least 8 years, and already have the great (and mature) CUDA, I really can't see why a business or an individual should take a risk and go with AMD.

I want to support AMD, I really do. But the reasons above are hard to ignore.

Edit: It turns out NVK is only for Vulkan but it's an improvement still. We'll get there eventually with these.

---

### 评论 #4 — amayra (2023-06-30T22:53:24Z)

as an RDNA user and I'm starting to be interested in AI there is no way to go with new AND GPU just because you don't went support old GPU like my RX 5700 XT 

CUDA looks so sexy from here when I'm trying experiment with Stable Diffusion  

I moved from windows and linux just to use hack environment variable "HSA_OVERRIDE_GFX_VERSION=10.3.0" to make Stable Diffusion work  



---

### 评论 #5 — samuelpmish (2023-07-01T00:56:30Z)

As a long time (10+ years) CUDA developer, I just bought a Radeon VII (because it was one of the few cards AMD appeared to actually support) so I could try out developing for AMD hardware, too. It's also a great card in the sense that it's one of the few options on the market (from any vendor) to have good FP64 performance at a reasonable price point.

It's disappointing to see AMD orphaning capable hardware like this so early in its lifetime.

---

### 评论 #6 — KEDI103 (2023-07-04T01:37:49Z)

As Radeon VII user and since 2005 using starting with Ati area bought always AMD but this thing force me why I am still going with AMD which I can't get support and suffer so much...
Nvidia users ridicule us which isn't nice as AMD user. 
AMD AI yt stream looks good but I can't get any benefit for AI but nvidia users crushing me. 
Even funny thing they removed Radeon vii page from AMD website. I was trying to compare my cards with modern cards I noticed one day puff it gone.
Should I regret my support and trust to AMD for years?
heres my problem right now...
https://github.com/RadeonOpenCompute/ROCm/issues/2314

---

### 评论 #7 — keryell (2023-07-11T21:56:50Z)

I have bought recently 3 Radeon VII for some projects at work (which is... AMD). So this is sad to have them no longer supported soon. :-(
But this depends on what is really behind "entering the maintenance mode" or "Bug fixes will not be back ported to older ROCm releases" from https://rocm.docs.amd.com/en/latest/CHANGELOG.html#os-and-gpu-support-changes. At the end, if everything is *really* open-source in the sense that it can really be compiled everywhere with a unified robust build system and good open-source collaborative spirit at AMD, the open-source community could still do some improvement if it is required.
At the end it would not be that different from the competition where you cannot have anyway super modern features usable on latest GPU, except that if it is really open-source like ROCm, you can still extend the lifetime of some hardware beyond what marketing people care about.

---

### 评论 #8 — stalkerg (2023-08-01T03:44:56Z)

Also, it seems like AMD team has some confusing intentions because AMDKFD interface in the Linux kernel still supports all cards started from GCN, and effectively only ROCm uses such an interface. (rusicls also thinking about it but not yet)
Because the kernel module/interface can exist only if has user space implementation this is a question for Linus and DRM maintainers.

I am a Vega56 user. 

---

### 评论 #9 — stalkerg (2023-08-01T03:46:33Z)

> At the end, if everything is really open-source in the sense that it can really be compiled everywhere with a unified robust build system and good open-source collaborative spirit at AMD, the open-source community could still do some improvement if it is required.

ROCm is open source but not open development. They do even not read the issue tracker usually. 

---

### 评论 #10 — drtpotter (2023-10-27T14:46:28Z)

Yes, please keep supporting gfx906 on ROCM for another few years at least! I use a Radeon VII for HIP training courses and it has by far the best double precision compute available in a consumer grade GPU. It is environmentally irresponsible to force users to discard hardware that still has plenty of life left!



---

### 评论 #11 — ev-dev (2023-12-12T12:38:19Z)

+1 gfx906 support

I waited for **_years_** to  see ROCm come to Windows, only to find out that my Radeon VII, which was considered one of the best consumer GPUs only 2 years ago, wouldn't be included, not even in future releases! Please consider extending hardware support 🙏

---

### 评论 #12 — EwoutH (2023-12-15T23:54:54Z)

> AMD Instinct MI50, Radeon Pro VII, and Radeon VII products (collectively gfx906 GPUs) enters maintenance mode in ROCm 6.0.

Nvidia still supports eight year old 2015 GPUs. AMD is dropping support for four year old 2019 GPUs.

When we finally thought we had a feasible Nvidia alternative, it was too good to be true.

Can’t believe we have to rely on Intel of all companies to offer a sustainable alternative.

---

### 评论 #13 — johnnynunez (2023-12-16T09:46:06Z)

Because Nvidia not change cuda cores drastically over years. AMD is really new with cdna and rdna so in my opinion  they are working on these architectures right now, gcn is totally different.

the problem was the strategy of amd with raytracing and AI, not giving the sufficient importance. Now, nvidia is moving to path tracing and tensor cores and rt cores are quite fast to run algorithms and DL.

Rdna3 is not sufficiently strong in these areas but with rdna4 i’m pretty sure that they put AI hardware

---

### 评论 #14 — johnnynunez (2023-12-16T13:57:36Z)

 Added support for additional GPU architectures.
Navi 3 series: gfx1100, gfx1101, and gfx1102.

---

### 评论 #15 — johnnynunez (2023-12-17T10:47:12Z)

For me it's working very well.
Use my scripts and build tensorflow and pytorch with your id card.
https://github.com/johnnynunez/rocm_lab
https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/pull/2327

---

### 评论 #16 — JustGitting (2024-01-11T03:45:52Z)

Not sure if this should be added as another issue or placed here...

As pointed out by @stalkerg, rocm is "open source but not open development.". Where decisions to drop support for hardware is made behind closed doors with no input from normal users or clear reasons why.

It appears there is no technical reason why 5 year old AMD cards cannot be supported for a much longer period. I speculate that the reason for AMD's decision is data-centers and HPC customers don't use cards older then 4-5 years...

As others have pointed out, it is environmentally irresponsible to cut support or usability of a perfectly capable piece of kit.
It also denies many people around the world from learning computer science / ML / programming with AMD GPU's if they are forced to buy expensive hardware. This means students and those in poorer communities miss-out on the opportunities to learn in this area. Which leads people to go (back) to Nvidia as older and cheaper hardware is supported.

I, like most people, hope AMD do the right thing.

Community/AMD, is it possible to (re)add support for formally dropped cards?

From @stalkerg's [comment](https://github.com/ROCm/ROCm/issues/2308#issuecomment-1659518982) the limitation is not in the driver (amdgpu), but within rocm itself (?).

Is there any documentation or information about adding/maintaining support in rocm for unsupported GPUs?

Would AMD be open to accepting PR's from the community to support unofficial/dropped cards? 
Or could support be added in a modular way without direct inclusion in rocm?

---

### 评论 #17 — alann-sapone (2024-01-11T22:13:45Z)

> as an RDNA user and I'm starting to be interested in AI there is no way to go with new AND GPU just because you don't went support old GPU like my RX 5700 XT
> 
> CUDA looks so sexy from here when I'm trying experiment with Stable Diffusion
> 
> I moved from windows and linux just to use hack environment variable "HSA_OVERRIDE_GFX_VERSION=10.3.0" to make Stable Diffusion work

Hi :)
I've been struggling to make it work and so far I didn't succeed...
Could you provide me any kind of guide (or a docker image) to finally be able to make my 5700XT work ? :)

Thanks =)

---

### 评论 #18 — ENDlezZenith (2024-02-23T18:39:03Z)

I was using Radeon VII 50th Anniversary Edition before. Waited for two years until 2023, I found that there are news about the Windows ROCm. I was thinking that I finally could run AI projects on Windows. So I bought 2 Radeon Pro VII with Infinity Fabric Link Bridge. GFX906 is definitely not out of date, really couldn't understand this act. Also for the ROCm Windows version, GFX906 and GFX1012 are even not supported by the Runtime. I would say it is just threatening "Old" customers by using software disabling.

---

### 评论 #19 — PhilipDeegan (2024-03-05T13:42:53Z)

I want to buy an Radeon VII pro, the specs are great and the price is great, but this is legitimately insane.

---

### 评论 #20 — SMH17 (2024-04-06T21:59:50Z)

> I was utterly amazed to read this in the ROCm 5.6 [release notes](https://rocm.docs.amd.com/en/latest/CHANGELOG.html#rocm-5-6-0):
> 
> > * AMD Instinct MI50, Radeon Pro VII, and Radeon VII products (collectively referred to as gfx906 GPUs) will be entering the maintenance mode starting Q3 2023. This will be aligned with ROCm 5.7 GA release date.
> >   
> >   * No new features and performance optimizations will be supported for the gfx906 GPUs beyond ROCm 5.7
> >   * Bug fixes / critical security patches will continue to be supported for the gfx906 GPUs till Q2 2024 (End of Maintenance [EOM])(will be aligned with the closest ROCm release)
> 
> The Vega 20 GPU (gfx906) is barely 5 years old. Even more, the Radeon VII, Radeon Pro VII and Instinct MI50 are still being sold!
> 
> If you want to know why everyone is going with Nvidia, there are a lot of them, but what they do at least well is they support they GPUs.
> 
> In the CUDA 12.x release from December 2022, Nvidia also [dropped support](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#cuda-libraries) for some GPUs:
> 
> > Support for the following compute capabilities is removed for all libraries:
> > 
> > * sm_35 (Kepler)
> > * sm_37 (Kepler)
> 
> Yes, you read that right, _Kepler_ GPUs. These are 2014 products. Not 2019 products like you're dropping.
> 
> So, hereby I would you strongly urge to not force us all to Nvidia again, by properly supporting your products.

I totally agree, but I have to correct you about the age of the no more supported Kepler GPUs mentioned for comparison:  actually they are **2012** GPUs!

---
