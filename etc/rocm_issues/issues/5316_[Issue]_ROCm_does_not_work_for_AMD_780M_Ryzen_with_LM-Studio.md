# [Issue]: ROCm does not work for AMD 780M Ryzen with LM-Studio

> **Issue #5316**
> **状态**: open
> **创建时间**: 2025-09-16T03:00:01Z
> **更新时间**: 2026-04-29T14:30:41Z
> **作者**: amd1890
> **标签**: Under Investigation, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5316

## 标签

- **Under Investigation** (颜色: #0052cc)
- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem Description

I keep trying to use LM Studio with Rocm drivers for 890M AMD Ryzen and have had no success, even with HSA_OVERRIDE_GFX_VERSION="11.0.2" lm-studio flag that should make it easier for the program to access rocm.

LM studio is one of the best programs if not the best program for local AI Models and it's surprising to me that it's this hard to get it to work when there is a rocm linux extension in the program. (ROCm llama.cpp (Linux)
v1.50.2 Engine Not Compatible AMD ROCm accelerated llama.cpp engine.) It keeps not detecting the hardware and other users have shared similar experiences.

Many Nvidia users do not have the same problems with using AI models locally and using the full potential of their chipsets and I wish AMD prioritized making it easier for non-developers to be able to use their products for learning about LLMs.

There is still an issue open on this topic for lm studio:
https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/426

I am not sure if this is just lm studio not implementing rocm but that extension shows.

### Operating System

Pop! OS 22.04

### CPU

Amd Ryzen 8840U

### GPU

AMD 780M Ryzen

### ROCm Version

6.4.3

### ROCm Component

_No response_

### Steps to Reproduce

Have Ryzen 8840U and 780M Ryzen GPU
Download LM studio
Install ROCm Repo
Install ROCm using AMD instructions
Run LM Studio and hope it detects ROCm
ROCm not detected and slower Vulkan process is used
AI LLM is much slower

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

rocminfo
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
...
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 8840U w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 8840U w/ Radeon 780M Graphics
...
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1103                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
  Vendor Name:             AMD                                


### Additional Information

_No response_

---

## 评论 (22 条)

### 评论 #1 — ppanchad-amd (2025-09-16T19:14:54Z)

Hi @amd1890. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — zichguan-amd (2025-09-24T19:12:48Z)

Hi @amd1890, it's hard to say why the extension does not detect ROCm with the override, there doesn't seem to be a toggle to change the GPU backend, and there's no source code available. I don't have a 780M to test it currently, but I'll try with other iGPU asics and see if there's anything that can be done on ROCm side.

---

### 评论 #3 — zichguan-amd (2025-09-25T18:18:31Z)

After playing around with gfx1151 (supported) and gfx906 (unsupported), it seems that LM studio is whitelisting the supported cards and preventing the extension from being able to be downloaded if you don't have a whitelisted card. On gfx1151 I can download the extension and use it without any issues, but on gfx906 there's no way to download it through the GUI. You can manually change the backend to ROCm once it is downloaded in Discover > Runtime > Selections.

I don't think this can be resolved from ROCm's side, you don't need ROCm installed to run LM studio and the check for extension download isn't affected by `HSA_OVERRIDE_GFX_VERSION` since it's likely not ROCm/HSA dependent. Once you have the extension and mathlibs from llama.cpp tho, you should be able to select ROCm backend and with `HSA_OVERRIDE_GFX_VERSION` LM studio should detect a working ROCm device. I manually copied the extension over from the gfx1151 system to the gfx906 system and with `HSA_OVERRIDE_GFX_VERSION` to any supported asic LM studio is able to detect a ROCm capable device.

Is your issue with not being able to download the extension or the extension does not detect a ROCm capable device? I'm using `llama.cpp-linux-x86_64-amd-rocm-avx2-1.50.2` with `LM-Studio-0.3.26-6-x64.AppImage`.

---

### 评论 #4 — reywang18 (2025-10-04T22:08:38Z)

My 780M Ubuntu 24.04, 64GB has no issue with ROCm 6.14.14
$ rocminfo
ROCk module version 6.14.14 is loaded

I tried to install ROCm 7.0.1, installed fine. But still show 6.14.14.
Ollama and Open WebUI all work fine, expected. But some Models do not work properly.

---

### 评论 #5 — zichguan-amd (2025-10-08T15:39:03Z)

Hi @reywang18, 6.14.14 is the amdgpu driver version, 6.14.14 is the latest version that comes with ROCm 7.0.1. Can you create a separate ticket for you issue and provide more details about your workload, system setup, and regression info if possible?

---

### 评论 #6 — reywang18 (2025-10-08T20:48:24Z)

I did open a case. Can we hire more QA people to speed up bug fixes?

---

### 评论 #7 — reywang18 (2025-10-09T02:44:09Z)

$ rocminfo | head -5
**ROCk module version** 6.14.14 is loaded ;; is it Doc issue? Should be more clear, such AMD GPU driver version.
=====================    
HSA System Attributes    

And which CMD or how to know the system is installed with ROCm 7.0.1?
Thru files under /opt/

$ pwd; ls
/opt
amdgpu  containerd  google  ollama_models  rocm  rocm-7.0.1 

A better way to verify which ROCm version in system.

---

### 评论 #8 — zichguan-amd (2025-10-09T13:40:43Z)

See https://github.com/ROCm/ROCm/issues/419. You can also try 
```
$ cat /opt/rocm/.info/version
7.0.1
```


---

### 评论 #9 — amd1890 (2025-11-01T17:29:15Z)

> After playing around with gfx1151 (supported) and gfx906 (unsupported), it seems that LM studio is whitelisting the supported cards and preventing the extension from being able to be downloaded if you don't have a whitelisted card. On gfx1151 I can download the extension and use it without any issues, but on gfx906 there's no way to download it through the GUI. You can manually change the backend to ROCm once it is downloaded in Discover > Runtime > Selections.
> 
> I don't think this can be resolvted from ROCm's side, you don't need ROCm installed to run LM studio and the check for extension download isn't affected by `HSA_OVERRIDE_GFX_VERSION` since it's likely not ROCm/HSA dependent. Once you have the extension and mathlibs from llama.cpp tho, you should be able to select ROCm backend and with `HSA_OVERRIDE_GFX_VERSION` LM studio should detect a working ROCm device. I manually copied the extension over from the gfx1151 system to the gfx906 system and with `HSA_OVERRIDE_GFX_VERSION` to any supported asic LM studio is able to detect a ROCm capable device.
> 
> Is your issue with not being able to download the extension or the extension does not detect a ROCm capable device? I'm using `llama.cpp-linux-x86_64-amd-rocm-avx2-1.50.2` with `LM-Studio-0.3.26-6-x64.AppImage`.

I'm not a developer and don't have the luxury of multiple AMD GPU cards so I can somehow get LM-Studio to download the proper item on a different computer to copy over and don't know their directory structure on their server to try to manually download it using wget. Since LM-Studio is the premiere linux App for running local models in linux with a GUI, if it is possible to communicate some technical information to the LM-Studio team so this error can be resolved, it would be appreciated.

I don't know how to properly communicate the problem to the LM-Studio team. I did update the open issue with what you had mentioned in this issue in the hopes that it expedites a resolution of the problem. This is still an open issue (https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1003).

I have already spent over 50 hours trying to configure ollama to recognize rocm for the 780M (which I was able to figure out) and get LM-Studio to recognize 780M (which hasn't been resolved).

I appreciate AMD, their wonderful products, and the effort you took in looking into a response, and hope this will be resolved.



---

### 评论 #10 — zichguan-amd (2025-11-03T15:16:41Z)

Hi @amd1890, thanks for the clarification. I found this command 
```
curl -fsSL https://files.lmstudio.ai/linux/0.2.31/beta/extension-pack-install-scripts/lin-rocm-0.2.31-ext-install.sh | sh
```
from an archived repo here https://github.com/lmstudio-ai/configs/blob/main/Extension-Pack-Instructions.md#amd-rocm-1 and gave it a try. 
The script can still be downloaded and upon inspecting the commands I found these links 
```
vendor_dl_url="https://extensions.lmstudio.ai/vendor-linux-llama-rocm-vendor-v1.tar.gz"
lm_dl_url="https://extensions.lmstudio.ai/backend-llama.cpp-linux-x86_64-amd-rocm-avx2-1.1.5.tar.gz"
```
and target directories
```
target_dir="$HOME/.cache/lm-studio/extensions/backends/lin-llama-rocm-0.2.31"
vendor_dir_name="linux-llama-rocm-vendor-v1"
vendor_target_dir="$HOME/.cache/lm-studio/extensions/backends/vendor/$vendor_dir_name"
lm_dir_name="linux-llama-rocm-lm"
```

Tried changing the URLs to `https://extensions.lmstudio.ai/vendor-linux-llama-rocm-vendor-v3.tar.gz` and `https://extensions.lmstudio.ai/backend-llama.cpp-linux-x86_64-amd-rocm-avx2-1.50.2.tar.gz` and was able to download.

However, the directory structure seems to have changed to `$HOME/.lmstudio`. If you put the files as such
```
$ ls $HOME/.lmstudio/extensions/backends/
llama.cpp-linux-x86_64-amd-rocm-avx2-1.50.2  llama.cpp-linux-x86_64-nvidia-cuda-avx2-1.50.2  vendor
llama.cpp-linux-x86_64-avx2-1.50.2           llama.cpp-linux-x86_64-vulkan-avx2-1.50.2
$ ls $HOME/.lmstudio/extensions/backends/vendor/
_amphibian  linux-llama-cuda-vendor-v1  linux-llama-rocm-vendor-v3  linux-llama-vulkan-vendor-v1
```
you should be able to select and use the extension with `HSA_OVERRIDE_GFX_VERSION`.

LM-Studio is closed-source so I cannot contribute to their codebase and propose any changes. You have to wait for them to address the issue you've created in their repo. However, I have escalated this issue internally to push for official HW support for 780M. 

Hopefully this helps you to get it running for now. Please give it a try and let me know if it works.

---

### 评论 #11 — zichguan-amd (2026-01-15T15:12:01Z)

Closing this issue due to inactivity. Please let me know if you are still encountering issues and I'll reopen it.

---

### 评论 #12 — alpharder (2026-02-23T00:42:46Z)

The issue is still the fact that iGPUs are a joke for you guys

---

### 评论 #13 — mistrjirka (2026-02-25T13:39:15Z)

> The issue is still the fact that iGPUs are a joke for you guys

not just that basically the rx 9070 is kinda affected too. 

---

### 评论 #14 — amd1890 (2026-04-18T17:02:09Z)

I still can't get rocm to work in LM Studio. Additionally, it seems like unless I switch to Ubuntu, it's very very hard to get rocm to work. For example, I use Pop! OS and the rocm install script has at times not worked because it's Ubuntu based. Additionally, integrating rocm into the kernel with dkms has been extremely hard and annoying. I never had this much trouble before when using Nvidia. This is still an issue, there aren't clear instructions, and I'm still frustrated about this situation. I bought my current setup not realizing what poor support amd provides for rocm and most linux distros. There is so much user friction with unlisted distros and rocm and 780M and other mobile cards and it would be nice if it weren't like that. My computer knowledge is also not beginner level; I have taken coding classes, I often use Qubes, and I am used to complexity. The instructions and support for 780M has just been bad when it comes to rocm. I am considering installing Ubuntu, a distro I absolutely hate, just to see if I can finally get rocm to work after struggling for years to try to get it working.

I know you are all working hard and trying to make progress on these things. I know this isn't easy and much work is being done and I am just mentioning there is still much user friction.

---

### 评论 #15 — reywang18 (2026-04-19T02:17:02Z)

> > The issue is still the fact that iGPUs are a joke for you guys
> 
> not just that basically the rx 9070 is kinda affected too.

If so, can we have a ROCm checkOS_gpu.ksh script and flag it is not supported?

---

### 评论 #16 — amd1890 (2026-04-24T01:28:11Z)

> Closing this issue due to inactivity. Please let me know if you are still encountering issues and I'll reopen it.

I am still having issues with this. I can't get LM Studio to recognize the rocm hardware tag when rocm is installed. I may switch to Ubuntu to see if I can get it working instead of Pop! but had the rocm drivers installed with Pop! when it would not load.

---

### 评论 #17 — zichguan-amd (2026-04-24T15:10:13Z)

I agree that the currently documentation is not clear and we only have instructions on supported distros. However, it's been some time since when this issue was first raised and we are now actively working on TheRock which aims to provide a broader range of arch support and nightly builds for quicker updates.

Please check out TheRock installation page [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md). It's built on manylinux docker image which should provide better compatibility for distros outside our official support list, see https://github.com/ROCm/TheRock/blob/faa3419fe581219075e8b73a05ebe4cb1166f17e/docs/design/manylinux_builds.md#compatibility. It provides prebuilt rocm/pytorch/jax wheels & tarballs for more archs, including gfx1103 and other gfx10 iGPUs, see https://github.com/ROCm/TheRock/blob/main/ROADMAP.md. So you won't be needing `HSA_OVERRIDE_GFX_VERSION` anymore.

As of amdgpu and dkms, we try our best to provide upstream in-kernel support, but it's not always possible on older kernels, which is why we need to patch with dkms. We have limited testing in place for gfx1103 so I can't say for sure which combination to use. Please try without dkms first.

As we discussed earlier, I can't help much on lm-studio side as it's closed-source third-party software that we have no control on. We do have active integration with open-source projects such as llama.cpp and vllm. You can always give those a try and if there's any issue in the process, please let me know and I'm happy to help.

---

### 评论 #18 — amd1890 (2026-04-24T15:34:00Z)

> Please check out TheRock installation page [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md). It's built on manylinux docker image which should provide better compatibility for distros outside our official support list, see https://github.com/ROCm/TheRock/blob/faa3419fe581219075e8b73a05ebe4cb1166f17e/docs/design/manylinux_builds.md#compatibility. It provides prebuilt rocm/pytorch/jax wheels & tarballs for more archs, including gfx1103 and other gfx10 iGPUs, see https://github.com/ROCm/TheRock/blob/main/ROADMAP.md. So you won't be needing `HSA_OVERRIDE_GFX_VERSION` anymore.

I may try to do this. In 2025 I spent over 100 hours trying to get rocm to work and only was able to get it to work in ollama in docker. This looks good, however. I had to have Claude explain to me what it does because it was hard for me to understand, but it seems like it just uses Docker on your end to help users build things with pip so it can work in many situations. It seems worth a try, although I may just reluctantly switch to Ubuntu 26.04 LTS because it has rocm built into the repo. I am not sure if TheRock or Ubuntu with rocm would be a better solution. I also really like the flow from Bazzite and would prefer to switch to Bazzite but I am not sure if TheRock would work with Bazzite because of its atomic nature (Claude also didn't know).
 
> As of amdgpu and dkms, we try our best to provide upstream in-kernel support, but it's not always possible on older kernels, which is why we need to patch with dkms. We have limited testing in place for gfx1103 so I can't say for sure which combination to use. Please try without dkms first.

I have tried it without dkms and with dkms. I have tried it many, many ways. (Also Pop! often has more recent kernels and it likely sometimes failed with dkms because they were unsupported custom new kernels.)

> As we discussed earlier, I can't help much on lm-studio side as it's closed-source third-party software that we have no control on. We do have active integration with open-source projects such as llama.cpp and vllm. You can always give those a try and if there's any issue in the process, please let me know and I'm happy to help.

I understand you can't control LM Studio. Your point about it being closed source is a good one. I am trying to move over to Jan.ai for that very reason.

---

### 评论 #19 — zichguan-amd (2026-04-24T16:08:33Z)

> but it seems like it just uses Docker on your end to help users build things with pip so it can work in many situations.

Right, it's a docker image we use to build ROCm off of to reduce distro-specific dependencies as much as possible.

> It seems worth a try, although I may just reluctantly switch to Ubuntu 26.04 LTS because it has rocm built into the repo. I am not sure if TheRock or Ubuntu with rocm would be a better solution. I also really like the flow from Bazzite and would prefer to switch to Bazzite but I am not sure if TheRock would work with Bazzite because of its atomic nature (Claude also didn't know).

Definitely give TheRock a try, it's in preview right now and it will become our mainline release builds at some point in the future (when it's mature enough for production use). 26.04 in-distro packages are also going to shift to TheRock builds when it becomes our official release. I'm not familiar with Bazzite, but since it's fedora based, it should mostly be fine with the ROCm stack, I'm more worried about driver support.

---

### 评论 #20 — amd1890 (2026-04-29T01:41:44Z)

> > but it seems like it just uses Docker on your end to help users build things with pip so it can work in many situations.
> 
> Right, it's a docker image we use to build ROCm off of to reduce distro-specific dependencies as much as possible.
> 
> > It seems worth a try, although I may just reluctantly switch to Ubuntu 26.04 LTS because it has rocm built into the repo. I am not sure if TheRock or Ubuntu with rocm would be a better solution. I also really like the flow from Bazzite and would prefer to switch to Bazzite but I am not sure if TheRock would work with Bazzite because of its atomic nature (Claude also didn't know).
> 
> Definitely give TheRock a try, it's in preview right now and it will become our mainline release builds at some point in the future (when it's mature enough for production use). 26.04 in-distro packages are also going to shift to TheRock builds when it becomes our official release. I'm not familiar with Bazzite, but since it's fedora based, it should mostly be fine with the ROCm stack, I'm more worried about driver support.

I did try this and ran into some issues when trying to set it up, probably because the files are so big and my Internet isn't that fast. (see https://github.com/ROCm/TheRock/issues/4916)

---

### 评论 #21 — zichguan-amd (2026-04-29T14:28:55Z)

I see that you are trying to clone TheRock and curl failed with connection error during submodule checkout, it is a large repo, if you just want to start using it you can use the prebuilt tarballs and wheels, see https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx110X-all for gfx1103.

---

### 评论 #22 — zichguan-amd (2026-04-29T14:30:41Z)

You may also want to set some environment variables for your workload to pick it up, see https://github.com/ROCm/TheRock/issues/1658

---
