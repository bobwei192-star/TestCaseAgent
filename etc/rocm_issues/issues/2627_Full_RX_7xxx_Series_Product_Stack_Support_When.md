# Full RX 7xxx Series Product Stack Support When?

> **Issue #2627**
> **状态**: closed
> **创建时间**: 2023-11-03T03:36:20Z
> **更新时间**: 2024-11-15T16:09:29Z
> **关闭时间**: 2024-11-15T16:09:29Z
> **作者**: KaoGomi
> **标签**: Question, Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/2627

## 标签

- **Question** (颜色: #cc317c)
- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Was previewing the ROCm documentation for a few hours and was interested in seeing how I would go about installing this software stack because I would like to do some independent AI stuff.
Checked to see if I had a supported GPU, and I do not.
Unfortunately, my 7900XT (the 2nd highest card in the product stack) is not supported on Linux.
I'm just a bit baffled by this because Windows has support for this card, and forcing me to switch to a platform where most AI development is _not_ happening seems a bit egregious.
Even the humble RX 7600 has full support for the Runtime and HIP SDK on Windows.

![Screenshot_20231102_233131](https://github.com/RadeonOpenCompute/ROCm/assets/43391426/dad8a704-0d8f-493f-bf81-c88506116503)

I guess the part that is more or less confusing to me is that the Radeon Pro WX7800 exists and that is just, to my understanding, essentially a 7900XT chip, but with 32GB of memory over the consumer card's 20GB of memory.

![Screenshot_20231102_233232](https://github.com/RadeonOpenCompute/ROCm/assets/43391426/46750f36-a13c-4e3d-aeab-7109d06a546b)

Also, a card that is listed as unsupported by AMD gets full ROCm support officially? It just seems a bit odd that the Radeon VII consumer card gets ROCm support, but objectively more powerful cards do not.

![Screenshot_20231102_233102](https://github.com/RadeonOpenCompute/ROCm/assets/43391426/1526e061-d951-4229-967e-edf6c1ff70d2)

At it's base, I just want to know if there is a time line for the entire product stack to be supported. 

TL;DR: Is there any plan to expand support to the remaining/entire Radeon consumer product stack on Linux?


### Operating System

_No response_

### GPU

AMD Radeon RX 7900 XT

### ROCm Component

_No response_

---

## 评论 (22 条)

### 评论 #1 — briansp2020 (2023-11-03T03:43:16Z)

7900XT and 7900XTX are the same chip and work fine under linux. You should just try it.

---

### 评论 #2 — KaoGomi (2023-11-03T16:27:31Z)

> 7900XT and 7900XTX are the same chip and work fine under linux. You should just try it.

It works and quite well.
I know the documentation team must be busy, but... why not just update the "Linux Supported GPUs" list? I'm certain there must've been some effort to validate it under Linux

---

### 评论 #3 — johnnynunez (2023-11-03T16:57:08Z)

Tensorflow ![image](https://github.com/RadeonOpenCompute/ROCm/assets/22727137/d08eb521-7fb6-4f62-bc85-8b0e4708e40f)

Pytorch
![image](https://github.com/RadeonOpenCompute/ROCm/assets/22727137/8310c078-a256-4995-8f19-e70892da6322)

---

### 评论 #4 — jalberto (2023-11-06T21:34:18Z)

Any update on RX 7600 on linux?

---

### 评论 #5 — danielzgtg (2023-11-08T20:15:52Z)

@johnnynunez What is the output of your `sudo dmesg`?

I wonder if this is related to my different model GPU freezing after a similar command. Even thought it's not supported, it was working fine before I updated.

---

### 评论 #6 — Flameancer (2023-11-13T20:34:51Z)

lol. I'm still waiting for the 7800XT to be added to the supported list. Though now the W7700 exist which appears to be the exact same chip as the 7800XT with the same amount of RAM. Right now in order to get a 7800XT to work in Stable diffusion I have to use HSA_OVERRIDE to a GFX1100

---

### 评论 #7 — ErykDev (2023-12-13T17:11:00Z)

> Any update on RX 7600 on linux?

@jalberto 

After tinkering, I managed to get it working. It's still unsupported

powercolor rx 7600 hellhound

Ubuntu 22.04.3 LTS
Kernel 6.2.0-37-generic

drivers : https://repo.radeon.com/amdgpu-install/23.30.3/

Driver installer
sudo dpkg -i ./amdgpu-install_5.7.50703-1_all.deb

it's quite important to specify that you want rocm
amdgpu-install --usecase=graphics,rocm

What's quite funny is the fact that the amdgpu-install  will install rocm version 5.7.3, if you don't specify it.
At the time of writing this reply, isn't even out.

pytorch/torchvision: https://repo.radeon.com/rocm/manylinux/rocm-rel-5.7/
Install torch from AMD repos, the one from download.pytorch.org/whl are quite outdated.

Honesty that is it,
Only caveat it that you have to run things with HSA_OVERRIDE_GFX_VERSION=11.0.0
Using 11.0.2 throws hip errors

for instance PYTORCH_ROCM_ARCH=gfx1102 HSA_OVERRIDE_GFX_VERSION=11.0.0 python3 train.py

(roc-smi while teaching deepfill)
https://github.com/nipponjo/deepfillv2-pytorch
[roc_smi.txt](https://github.com/ROCm/ROCm/files/13663575/roc_smi.txt)

[rocinfo.txt](https://github.com/ROCm/ROCm/files/13663368/rocinfo.txt)

(script for testing rocm)
[test-rocm.py.txt](https://github.com/ROCm/ROCm/files/13663446/test-rocm.py.txt)
result
[test_rocm_res.txt](https://github.com/ROCm/ROCm/files/13663457/test_rocm_res.txt)

![image](https://github.com/ROCm/ROCm/assets/32577176/9c591441-e8f2-45db-806d-3926f8ec2d3b)

I can run some benchmarks if someone is interested.
Kind Regards 
Eryk Szmyt



---

### 评论 #8 — gnoejuan (2023-12-29T09:33:35Z)

I'm interested! I got just enough to buy 1, and would like to upgrade a RX 550, for blender and rocm stuff. 

But only if Rocm can be used. 

---

### 评论 #9 — Spacefish (2024-02-02T10:15:40Z)

At least ROCm 6.0.2 seems to support the gfx1101 out of the box, it´s just not included in the libs bundled in the official pytorch release yet.
I built torch, torchvision and torchaudio from source yesterday against ROCm 6.0.2 (the officially binary packages released by AMD) and it works just fine, without the need to do an "HSA_OVERRIDE_GFX_VERSION" or something like that on my gfx1101 based 7800 XT.

i didn´t meassure it, but stable diffusion for example feels faster with the ROCm 6.0.2 and the real gfx1101 target compared to ROCm 5.6 and gfx1100 as target via HSA_OVERRIDE_GFX_VERSION.
Probably it choose more optimized wave sizes and such, as it has the Tensile files for the real gfx1101 chip.

---

### 评论 #10 — johnnynunez (2024-02-02T11:51:52Z)

> At least ROCm 6.0.2 seems to support the gfx1101 out of the box, it´s just not included in the libs bundled in the official pytorch release yet. I built torch, torchvision and torchaudio from source yesterday against ROCm 6.0.2 (the officially binary packages released by AMD) and it works just fine, without the need to do an "HSA_OVERRIDE_GFX_VERSION" or something like that on my gfx1101 based 7800 XT.
> 
> i didn´t meassure it, but stable diffusion for example feels faster with the ROCm 6.0.2 and the real gfx1101 target compared to ROCm 5.6 and gfx1100 as target via HSA_OVERRIDE_GFX_VERSION. Probably it choose more optimized wave sizes and such, as it has the Tensile files for the real gfx1101 chip.

yes, i use this forked repository https://github.com/johnnynunez/rocm_lab

you can compile also tensorflow and check if still exists freezes when tensorflow allocate data to vram.
To compile tensorflow you have to change the code from tensorflow repository because it save 64gb ram and 72 threads.

in build_rocm_python3:
```python
ROCM_INSTALL_DIR=/opt/rocm-6.0.0 --> ROCM_INSTALL_DIR=/opt/rocm-6.0.2
```
```python
RESOURCE_OPTION="--local_ram_resources=60000 --local_cpu_resources=35 --jobs=70"
```
your ram and cpu cores and threads:
in my case 7950x3d(16 cores, 32 threads) and 32gb ram
```python
RESOURCE_OPTION="--local_ram_resources=28000 --local_cpu_resources=16 --jobs=32"
```



---

### 评论 #11 — Spacefish (2024-02-02T13:38:37Z)

> you can compile also tensorflow and check if still exists freezes when tensorflow allocate data to vram. To compile tensorflow you have to change the code from tensorflow repository because it save 64gb ram and 72 threads.
> 
> in build_rocm_python3:
> 
> ```python
> ROCM_INSTALL_DIR=/opt/rocm-6.0.0 --> ROCM_INSTALL_DIR=/opt/rocm-6.0.2
> ```
> 
> ```python
> RESOURCE_OPTION="--local_ram_resources=60000 --local_cpu_resources=35 --jobs=70"
> ```

Well the "RESOURCE_OPTION" thing is only for the build / is passed to bazel (the build system) and has no relevance during execution of tensorflow as i understand it. You only need to set it if your machine does not have enough RAM to build it with the default settings. 
There is no problem with having more jobs running than there are CPU cores IMHO, as some will wait for I/O anyway, the main limiting factor is RAM.

> you can compile also tensorflow and check if still exists freezes when tensorflow allocate data to vram.
i have seen issues with my window manager crashing, when i allocate a lot of VRAM via ROCm, maybe you load a model in tf which doesn´t fit into VRAM or tensorflow tries to allocate all availiable VRAM at the start anyway?
With pytorch: Starting the same thing from a pure text console without the window manager running helped in this case.

Guess the ROCm Framework just allocates the VRAM requested on the GPU if the application asks it to do so.. If you allocate all remaining VRAM, once the window manager tries to allocate any additional VRAM for a new surface or buffer it probably crashes.. Haven´t looked into the logs though.

Not sure if the GPU supports mapping host memory pages into the Virtual Address Space of the GPU and do transparent DMA via PCIe.. However even if this works, it would be extremly slow depending on what you are doing. Imagine having to read the every weight for every node for every iteration of a net over PCIe.. The latency is isanly high and the bandwidth extremly slow, compared to the GDDR6 chips on the card or the Infinity Cache.

Edit: Ah that´s actually possible, but not recommended: https://rocm.docs.amd.com/en/latest/conceptual/gpu-memory.html#pinned-memory

---

### 评论 #12 — Spacefish (2024-02-03T01:14:24Z)

Tensorflow works as well.
I used the official https://github.com/ROCm/tensorflow-upstream repo.

Had to do minimal changes to the code, so it accepts my Navi32 gfx1101.
See: https://github.com/ROCm/tensorflow-upstream/commit/1c3f58db55b87b0d30cd2cfefbe3b31a9b8987da

Seems to work just fine:
![image](https://github.com/ROCm/ROCm/assets/375633/697bc84b-26d6-4ebc-9416-20ec44b4773b)
![image](https://github.com/ROCm/ROCm/assets/375633/55bc3781-2f72-41d9-a19a-12dde96157c9)
![image](https://github.com/ROCm/ROCm/assets/375633/47f103aa-8226-4459-91ba-a3b6ab1f65c8)

and runs on the GPU `Compiled cluster using XLA!  This line is logged at most once for the lifetime of the process.`

no crashes so far.

Edit: definetly runs on the GPU! If i train a net with 3x 4096 node dense layers it takes ~210ms per Step on the CPU but only 6ms on the GPU! Nice 35x fold performance increase!

---

### 评论 #13 — johnnynunez (2024-02-03T09:21:41Z)

> Tensorflow works as well. I used the official https://github.com/ROCm/tensorflow-upstream repo.
> 
> Had to do minimal changes to the code, so it accepts my Navi32 gfx1101. See: [ROCm/tensorflow-upstream@1c3f58d](https://github.com/ROCm/tensorflow-upstream/commit/1c3f58db55b87b0d30cd2cfefbe3b31a9b8987da)
> 
> Seems to work just fine: ![image](https://private-user-images.githubusercontent.com/375633/302003713-697bc84b-26d6-4ebc-9416-20ec44b4773b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDY5NTIzMjIsIm5iZiI6MTcwNjk1MjAyMiwicGF0aCI6Ii8zNzU2MzMvMzAyMDAzNzEzLTY5N2JjODRiLTI2ZDYtNGViYy05NDE2LTIwZWM0NGI0NzczYi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMjAzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDIwM1QwOTIwMjJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mMWRlZTBkZDZiNmQwZmZlZDZmYzFiMmUwZTlhYzNmYTJkNTc4ZDVhZDA3ODJiN2MyNjMxMGUzMDNiNDJlYWIyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.8NsY7wKG8uYZjeFvzCfgg_ZoFfua5qXPhILsoj1hpzQ) ![image](https://private-user-images.githubusercontent.com/375633/302003739-55bc3781-2f72-41d9-a19a-12dde96157c9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDY5NTIzMjIsIm5iZiI6MTcwNjk1MjAyMiwicGF0aCI6Ii8zNzU2MzMvMzAyMDAzNzM5LTU1YmMzNzgxLTJmNzItNDFkOS1hMTlhLTEyZGRlOTYxNTdjOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMjAzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDIwM1QwOTIwMjJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zZDZhMzljOWQ1YTAxNjE1ZTJjNTlhNGUyNjNiZGZhYzk5MjJhNjI3NjQ5MGU1MWYwYzYxN2YwNTUwNzY4YjkyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.duCz6gzY9bvx3_F7y7QTULoBiGADuwn6PruuYfrFUjs) ![image](https://private-user-images.githubusercontent.com/375633/302003775-47f103aa-8226-4459-91ba-a3b6ab1f65c8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDY5NTIzMjIsIm5iZiI6MTcwNjk1MjAyMiwicGF0aCI6Ii8zNzU2MzMvMzAyMDAzNzc1LTQ3ZjEwM2FhLTgyMjYtNDQ1OS05MWJhLWEzYjZhYjFmNjVjOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMjAzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDIwM1QwOTIwMjJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wMmYyM2Q5Y2RjNzE1NzY1ZmRkMGQ4NWZiNGQyNDQwOThjNjBkYzZlYmFmYTYzNjFhNGMxYTZkZjQ2ZTFmMWIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.Obh40bLKXNoIuVuEBwWZD6y4TVcPZlsGJLG7k5MccwQ)
> 
> and runs on the GPU `Compiled cluster using XLA! This line is logged at most once for the lifetime of the process.`
> 
> no crashes so far.
> 
> Edit: definetly runs on the GPU! If i train a net with 3x 4096 node dense layers it takes ~210ms per Step on the CPU but only 6ms on the GPU! Nice 35x fold performance increase!

Install pip install new-ai-benchmark

from ai_benchmark import AIBenchmark
benchmark = AIBenchmark(verbose_level=2)

---

### 评论 #14 — Spacefish (2024-02-03T22:48:38Z)

> Install pip install new-ai-benchmark
> 
> from ai_benchmark import AIBenchmark benchmark = AIBenchmark(verbose_level=2)

dont have anything to compare it too, but this is the output:
[benchmark_output.txt](https://github.com/ROCm/ROCm/files/14154477/benchmark_output.txt)

benchmark.run unfortunately throws an error, so the result return value is not availiable:
`AttributeError: `LSTMCell` is not available with Keras 3.`


---

### 评论 #15 — ppanchad-amd (2024-05-17T14:53:25Z)

@KaoGomi 7900XT is supported in lastest ROCm 6.1.1 (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)

@Spacefish Please create a separate ticket for your issue to track. Thanks!

---

### 评论 #16 — binarynoise (2024-05-17T14:56:43Z)

I don't think the issue is completed yet.
Out of the 7xxx series, only 7900 is supported.
What about the others? When will they be added to the set of supported GPUs?

---

### 评论 #17 — Spacefish (2024-05-17T16:43:03Z)

@KaoGomi 
I don't have any issues, everything works for me. ROCm supports my 7800XT when I compile it from source.

---

### 评论 #18 — SusieDreemurr (2024-06-06T01:15:51Z)

> I don't think the issue is completed yet. Out of the 7xxx series, only 7900 is supported. What about the others? When will they be added to the set of supported GPUs?

Exactly. It's been months now and there still isn't support for the rest. Still waiting for my 7600 XT support.

---

### 评论 #19 — sancspro (2024-07-16T02:59:24Z)

When will we get an official 7800XT support on Linux?

---

### 评论 #20 — 2eQTu (2024-07-26T15:49:59Z)

Is there any expected timeline for official ROCm 7800XT / Navi32 support on Linux?  

I can get it to work on my 7800XT, but I do see some instability and I assume the testing for formal support would help sort more bugs out.

At the time I purchased my 7800 XT the 7900 GRE was a China-only part, so that was not an option.

---

### 评论 #21 — Flameancer (2024-10-10T04:18:32Z)

> Is there any expected timeline for official ROCm 7800XT / Navi32 support on Linux?
> 
> I can get it to work on my 7800XT, but I do see some instability and I assume the testing for formal support would help sort more bugs out.
> 
> At the time I purchased my 7800 XT the 7900 GRE was a China-only part, so that was not an option.

I doubt it at this point. RDNA4 is probably releasing in the next 6 months. If they don't have NAVI32 support now I doubt we'll see it unless it comes much later as a sign of good faith. I was in the same boat, would've bought a 7900GRE but that was a china only part at the time the 7800XT released with no sign of that card being released outside of China. Had I had waited 6 months I would've gotten a GRE instead but here we are. For sure NAVI4X will have proper ROCM support. 

---

### 评论 #22 — rafrafek (2024-10-10T10:56:47Z)

The RX 7800 XT already has full official support for Windows. I think Linux and WSL2 support will follow soon.

---
