# [Issue]: 

> **Issue #2908**
> **状态**: closed
> **创建时间**: 2024-02-20T12:15:32Z
> **更新时间**: 2024-06-19T19:50:34Z
> **关闭时间**: 2024-06-19T19:50:34Z
> **作者**: badverybadboy
> **标签**: ROCm 5.7.1, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/2908

## 标签

- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

I am using UBUNTU 23.10 with Vega 64 using the latest ROCm 5.7 drivers. This started when I upgraded to 23.10. Was not happening in 22.04 or 23.04.

In Wayland, it always crashes the gnome session and I have to hardware power off the system. It also sometimes makes a weird pixelated image on the screen, kind of like static with both firefox and brave broswers.

In xorg session only firefox seems to crash the session but weirdly it just "logs me out" to the welcome screen. Brave works fine.

I thought it was a mem issue but I have run memtest twice now with all tests passing for the whole night. I have also run prime95 successfully on both windows and ubuntu now for 5-6 hours as well just to stress the system for both CPU and mem and no issues there.

Bug on ubuntu launchpad
https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2045584

### Operating System

Ubuntu 23.10 Mantic Minotaur

### CPU

AMD Ryzen 7 1700

### GPU

AMD Radeon VII

### ROCm Version

ROCm 5.7.1

### ROCm Component

ROCm

### Steps to Reproduce



Can be easily replicated by having vega64 gpu:

- install rocm drivers on ubuntu 23.10
- run firefox or brave browser and open speedtest.net
- let test run and move your mouse around 




### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

Had to remove the rocm version as it was causing issues so do not have access to rocminfo


### Additional Information

_No response_

---

## 评论 (13 条)

### 评论 #1 — nartmada (2024-02-20T14:53:15Z)

Hi @badverybadboy, thank you for your feedback.  

However, UBUNTU 23.10 is not supported.  Please refer to the below link for system requirements.
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html



---

### 评论 #2 — badverybadboy (2024-02-22T15:01:22Z)

From the documentation it seems that even the Vega architecture seems to have been dropped. Not even about the OS anymore. This is a weird thing as it seems that the newer AMD APUs are still using that architecture. Is there any plans to support ROCm on those or development has been stopped?

---

### 评论 #3 — preda (2024-02-23T21:29:38Z)

Are you overclocking and/or undervolting the GPU? in particular, are you overclocking the RAM?

---

### 评论 #4 — badverybadboy (2024-02-24T00:09:31Z)

Hi Preda

I am not over locking the GPU or GPU ram but I have over clocked the CPU and the main RAM. I have run prime95 etc stability tests for ram. My ram is supposed to be 3600mhz Ram but I'm only running at 3299mhz but I think for my motherboard they only officially support 3200mhz. Is there something that you are getting at ?

---

### 评论 #5 — preda (2024-02-24T05:32:48Z)

@badverybadboy thank you, that is not it then. In the past I did see strange whole-system lockups with overclocked *video* RAM on the Radeon VII -- but that does not seem to be your case. (I do not suspect the system RAM).

You may try the latest ROCm, 6.0.2, just to see whether it changes anything (probably won't help though).

When things crash, you may have a look towards the end of "sudo dmesg" (if you still can run that) to see what is reported there, may provide some clues.


---

### 评论 #6 — badverybadboy (2024-02-24T12:07:05Z)

Thanks @preda. I will check it and come back to you. How would I know if my GPU  was over clocked ? 

---

### 评论 #7 — badverybadboy (2024-02-26T13:44:05Z)

It seems that there is an issue in Rocm 6.0.2 and AMD has dropped support for Vega64 graphics card. This really sucks as it is a card that could really be used for inference related tasks. I cannot find anywhere where its properly docmuented what is the supported Rocm release for vega64 that I could use. @nartmada @preda do you know where I can find that info? It seems AMD officially only supports RDNA2 cards now and has removed documentation and download links to older versions.

---

### 评论 #8 — nartmada (2024-03-13T16:07:28Z)

@badverybadboy, I consulted internally with @kentrussell and ROCm 4.5.x officially supports Vega64.  https://repo.radeon.com/rocm/apt/4.5.2/

"Supported hardware" means "hardware that we actively test and report against for a release".  For "unsupported hardware", the bits are all still in there, but we just don't test it.  Sometime something might break, but in general, things should still work unless there are major architectural changes.  Older releases can be found at [****](https://repo.radeon.com/)https://repo.radeon.com//.  You can try older and newer releases to find one that suits your needs.

Hope this helps.  

---

### 评论 #9 — serhii-nakon (2024-03-25T13:43:25Z)

@nartmada Can you please add exactly the same text `"Supported hardware" means "hardware that we actively test and report against for a release". For "unsupported hardware", the bits are all still in there, but we just don't test it. Sometime something might break, but in general, things should still work unless there are major architectural changes.` to page where list of supported cards and add those list of cards that technically should works? Because as customer I really thought that you support only ~6 cards in ROCM!!! (I not joke and not only I think so...)

---

### 评论 #10 — nartmada (2024-03-31T15:01:06Z)

@serhii-nakon, thanks for your feedback.  I have forwarded your concerns to the documentation team.  

---

### 评论 #11 — serhii-nakon (2024-03-31T15:34:57Z)

@nartmada Thanks!

---

### 评论 #12 — serhii-nakon (2024-03-31T15:38:41Z)

@nartmada I would like also see mapping of each card model to related last supporting ROCm version. I think it can help to build inside Docker newest frameworks like Pytorch from source in case when it deprecated officially. 

I think it allow technically handle all deprecations without affecting customers.

---

### 评论 #13 — nartmada (2024-04-05T15:25:02Z)

> @nartmada I would like also see mapping of each card model to related last supporting ROCm version. I think it can help to build inside Docker newest frameworks like Pytorch from source in case when it deprecated officially.
> 
> I think it allow technically handle all deprecations without affecting customers.

Noted.  Thanks.

---
