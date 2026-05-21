# Installing ROCm on windows with GPU RX 6700 XT (Navi 22)

> **Issue #2370**
> **状态**: closed
> **创建时间**: 2023-08-08T03:23:03Z
> **更新时间**: 2025-11-22T07:37:11Z
> **关闭时间**: 2024-04-21T14:03:28Z
> **作者**: darabon
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2370

## 描述

Hello, I have been doing Stable diffusion on my Rx 6700 xt for half a year now and I wanted to install ROCm on my windows 10 PC, but I get error 215. What is this error? If you know how to help me, please help. I've already tried cleaning and reinstalling the drivers, but that didn't help. Thank you in advance!

---

## 评论 (5 条)

### 评论 #1 — Kademo15 (2023-08-12T02:25:17Z)

I think that rocm is on windows but pytorch isnt because there is still stuff that has to be ported you can check here https://github.com/vladmandic/automatic/issues/1880 therefore until pytorch is ported it will not work in the meantime you can use linux or the directml fork. 

---

### 评论 #2 — NeedsMoar (2023-08-16T02:43:22Z)

#2363 
^ This isn't related to pytorch, see that (closed) issue for the fix.  

---

### 评论 #3 — shaner306 (2023-09-05T02:28:25Z)

Its likely failing because the 6800 is supported and the 6700XT is not. See https://rocm.docs.amd.com/en/latest/release/windows_support.html 

They have gotten up to 6800 and likely 6750 and 6700 XT will follow eventually.

---

### 评论 #4 — nartmada (2024-04-21T14:03:28Z)

@darabon, apologies for the lack of response.  

Please refer to the below link for supported GPUs on Windows.
https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html

Thanks.

---

### 评论 #5 — tlee933 (2025-11-22T07:18:06Z)

Native therock 7.10 Radeon RX6700XT  (gfx1031)  Linux Fedora43
    
  I have a fork you can poke around on my personal commits.
 https://github.com/tlee933/TheRock/tree/gfx1031-upstream
  and some other gfx-1031 rocm 7.10 fedora43 building
  most of the stack working and some ollama llama.cpp fixing.  all testing still.
 https://github.com/tlee933/TheRock/tree/gfx1031-support-and-docs

rocBLAS working issue #2720



---
