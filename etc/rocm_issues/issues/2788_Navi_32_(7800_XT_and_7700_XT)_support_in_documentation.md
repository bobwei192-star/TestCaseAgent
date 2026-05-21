# Navi 32 (7800 XT and 7700 XT) support in documentation.

> **Issue #2788**
> **状态**: closed
> **创建时间**: 2024-01-09T16:16:43Z
> **更新时间**: 2026-01-22T07:18:22Z
> **关闭时间**: 2024-02-21T18:01:56Z
> **作者**: MickenCZ
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2788

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

In the ROCM Windows documentation, it is not listed whether the 7800 XT and 7700 XT are supported. While it is said that not listed GPUs are not supported, if the rx 7600 and rx 7900 XT fully support it, I think it should explicitly say whether the support is there for Navi 32 GPUs or not. I suggest adding these GPUs to the list, as especially the 7800 XT has become very popular, has lots of VRAM and many people will want to start using it for compute, which starts with reading this piece of documentation. Link is here, Radeon Cards.
https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html
![image](https://github.com/ROCm/ROCm/assets/73470371/1ed6d9a6-8f6a-4ab3-b2e9-be5804c2a236)

---

## 评论 (9 条)

### 评论 #1 — nartmada (2024-01-09T20:32:08Z)

Internal ticket has been created to track the issue.

---

### 评论 #2 — Lefthornet (2024-01-23T21:58:52Z)

> In the ROCM Windows documentation, it is not listed whether the 7800 XT and 7700 XT are supported. While it is said that not listed GPUs are not supported, if the rx 7600 and rx 7900 XT fully support it, I think it should explicitly say whether the support is there for Navi 32 GPUs or not. I suggest adding these GPUs to the list, as especially the 7800 XT has become very popular, has lots of VRAM and many people will want to start using it for compute, which starts with reading this piece of documentation. Link is here, Radeon Cards. https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html ![image](https://private-user-images.githubusercontent.com/73470371/295267503-1ed6d9a6-8f6a-4ab3-b2e9-be5804c2a236.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDYwNDcxNTUsIm5iZiI6MTcwNjA0Njg1NSwicGF0aCI6Ii83MzQ3MDM3MS8yOTUyNjc1MDMtMWVkNmQ5YTYtOGY2YS00YWIzLWIyZTktYmU1ODA0YzJhMjM2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAxMjMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMTIzVDIxNTQxNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWU0ZGI0Yzk0N2M5MjI3NzBlZjExMmUzMjg3ZjQ5NDk2ODkwNmYwMzk2YzdmNzY3OWQ5Yzc3ZGQzNTJhNzgwYTImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.KB5Wgu82N2zDCFyJQ4KyfRZBoXXoUq5rsEb6A03Q-pk)

So the 7800 XT is supported? was thinking about buying one, but since I didn't see it on the list thought wasn't supported yet, About the 7900 GRE and 7800 XT, are supported on Linux ROCm or only Windows HIP? (since that card also doesn't appear on the list) 

---

### 评论 #3 — MickenCZ (2024-01-24T07:53:44Z)

> > In the ROCM Windows documentation, it is not listed whether the 7800 XT and 7700 XT are supported. While it is said that not listed GPUs are not supported, if the rx 7600 and rx 7900 XT fully support it, I think it should explicitly say whether the support is there for Navi 32 GPUs or not. I suggest adding these GPUs to the list, as especially the 7800 XT has become very popular, has lots of VRAM and many people will want to start using it for compute, which starts with reading this piece of documentation. Link is here, Radeon Cards. https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html ![image](https://private-user-images.githubusercontent.com/73470371/295267503-1ed6d9a6-8f6a-4ab3-b2e9-be5804c2a236.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDYwNDcxNTUsIm5iZiI6MTcwNjA0Njg1NSwicGF0aCI6Ii83MzQ3MDM3MS8yOTUyNjc1MDMtMWVkNmQ5YTYtOGY2YS00YWIzLWIyZTktYmU1ODA0YzJhMjM2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAxMjMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMTIzVDIxNTQxNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWU0ZGI0Yzk0N2M5MjI3NzBlZjExMmUzMjg3ZjQ5NDk2ODkwNmYwMzk2YzdmNzY3OWQ5Yzc3ZGQzNTJhNzgwYTImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.KB5Wgu82N2zDCFyJQ4KyfRZBoXXoUq5rsEb6A03Q-pk)
> 
> So the 7800 XT is supported? was thinking about buying one, but since I didn't see it on the list thought wasn't supported yet, About the 7900 GRE and 7800 XT, are supported on Linux ROCm or only Windows HIP? (since that card also doesn't appear on the list)

Neither cards are on the list for either Windows or Linux, so one could say that they are not supported. We really are not sure, the 7900 XT(X) are supported on both, and the 7600 is supported only on Windows. There really is no way to know for the 7800 XT, an internal ticked has been created so we should know eventually, I guess they need to do more testing for the Navi 32 compile target.



---

### 评论 #4 — Spacefish (2024-01-29T23:39:10Z)

I have an 7800XT and ROCm 6.0 works just fine, the HIP libraries have gfx1101 enabled, there are even tensile.dat files for rocBLAS.

MIOpen has some gfx11 kernels as well as references to the gfx1101 target, but i didn´t try MIOpen.

However keep in mind, that things like pytorch ship with rocm included and pytorch does not have tensile files for gfx1101 for example. However you can still get it to work by setting: `HSA_OVERRIDE_GFX_VERSION='11.0.0'`, which essentially tells the ROCm libs to use the gfx1100 target instead of the gfx1101 target.

If i try to use pytorch with the gfx1101 target, i get the following error:
```
RuntimeError: HIP error: invalid device function
```
however it runs fine with the gfx1100 target.

a further error message, tells us that it didn´t find the Tensile library .dat files for gfx1101
```
rocBLAS error: Cannot read /home/spacy/src/pytorch-playground/venv/lib/python3.10/site-packages/torch/lib/rocblas/library/TensileLibrary.dat: No such file or directory for GPU arch : gfx1101
```

So: yes 7800 XT works just fine in ROCm, but probably not "officially supported" by AMD.

Not sure why PyTorch for example only includes a ROCm version with limited support, maybe it wasn´t supported in 5.7? As the latest PyTorch Nightly still uses ROCm 5.7 instead of 6.0.. Just replacing the libs with 6.0 did not work :) guess the ABI changed to much / there are other problems in PyTorch which need to be fixed first before adoption.
IMHO ROCm supports gfx1101, but other libs which ship with their own rocm build, might not.

---

### 评论 #5 — OzzyHelix (2024-02-20T22:36:42Z)

I am unsure if I should make this a separate issue so I will say it here. The 7800 XT seems to lack rocm support on Arch Linux. From my testing with 
Retrieval-based-Voice-Conversion(RVCv2) the AI that I have been trying to get working on it. if AMD or someone could make support more official or even just have rocm work with the 7800 XT at all that would be wonderful.

---

### 评论 #6 — OzzyHelix (2024-02-20T22:39:34Z)

I will continue to test but it might just be that python3.8 was no longer suitable for that task

---

### 评论 #7 — yhuiYH (2024-02-21T18:01:56Z)

7800 XT and 7700 XT has been updated on the https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html.  Closing issue now.  Please re-open, if necessary.

---

### 评论 #8 — winfriedgerlach (2024-12-30T19:37:19Z)

@yhuiYH @nartmada shouldn't this also answer #3863?

---

### 评论 #9 — rafrafek (2026-01-22T07:18:22Z)

@yhuiYH is 7800 XT still supported on Windows with ROCm 7.2? It looks like it disappeared without any notice and only 7700 remained supported. That would make buying an AMD graphics card a lottery. Can you give us a roadmap when which GPU will gain or lose support?

https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html

---
