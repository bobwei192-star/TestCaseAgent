# Support for Windows

> **Issue #2065**
> **状态**: closed
> **创建时间**: 2023-04-19T07:36:11Z
> **更新时间**: 2024-08-21T10:57:02Z
> **关闭时间**: 2024-05-10T19:20:54Z
> **作者**: MoonRide303
> **标签**: Windows
> **URL**: https://github.com/ROCm/ROCm/issues/2065

## 标签

- **Windows** (颜色: #c2e0c6)

## 描述

Please add native support for Windows. I was recently evaluating which new GPU with more VRAM I could buy, but lack of support for Windows basically makes AMD cards unusable for me.

I want to be able PyTorch 2.0 with GPU acceleration on Windows, natively - and GPUs that doesn't allow me to do so are simply no-go:

![image](https://user-images.githubusercontent.com/130458190/233003633-e41059f4-7b65-455f-bcc2-1aed6afefd54.png)


---

## 评论 (20 条)

### 评论 #1 — shen9175 (2023-04-19T08:09:43Z)

According to tom's hardware and videocardz, ROCm 5.6.0 Alpha document (internal) shows will support Windows for RDNA2 cards, stay tuned, it seems not far away from now.

---

### 评论 #2 — countradooku (2023-04-28T10:30:31Z)

https://github.com/RadeonOpenCompute/ROCm/pull/2094

they fcked us again

---

### 评论 #3 — evshiron (2023-04-29T09:48:34Z)

@radudiaconu0

ROCm 5.5.0 does not guarantee the inclusion of Windows support. Stay tuned.

---

### 评论 #4 — countradooku (2023-04-29T09:50:37Z)

@evshiron 

I know that..i just hoped from many speculation that the release after 5.4.3 will have windows release. Manny commits to docs said that. So now I am disappointed. They removed windows docs from develop branch for no reason and explanation. I am disappointed right now

---

### 评论 #5 — Nicopara (2023-05-15T07:25:03Z)

Imo they should drop all planned features and rush windows support out the door.

---

### 评论 #6 — boxerab (2023-05-29T18:28:04Z)

From the README

> ROCm’s goal is to allow our users to maximize their GPU hardware investment

---

### 评论 #7 — jkddw (2023-06-29T03:35:15Z)

ROCm 5.6.0 does not have Windows support.

---

### 评论 #8 — evshiron (2023-06-29T04:31:38Z)

Thanks for the notice. It seems like ROCm 5.6.0 is available in https://repo.radeon.com/amdgpu-install/5.6/ now.

---

### 评论 #9 — countradooku (2023-06-29T06:06:28Z)

Yep and we waited like fools

---

### 评论 #10 — comminux (2023-07-27T06:54:39Z)

https://projects.blender.org/blender/blender/pulls/110519

---

### 评论 #11 — johnnynunez (2024-01-10T08:58:51Z)

Will there be miopen support for windows in 6.0.1?

---

### 评论 #12 — briansp2020 (2024-04-17T19:46:21Z)

https://rocm.docs.amd.com/projects/install-on-windows/en/latest/

So, it seems they support windows with 5.7. Still no ML libraries, I think...

---

### 评论 #13 — johnnynunez (2024-04-17T20:33:59Z)

> https://rocm.docs.amd.com/projects/install-on-windows/en/latest/
> 
> So, it seems they support windows with 5.7. Still no ML libraries, I think...

The page was not updated but 6.1 it is supported

---

### 评论 #14 — ppanchad-amd (2024-05-10T19:20:54Z)

Support available. Please check latest ROCm 6.1.1
https://rocm.docs.amd.com/projects/install-on-windows/en/latest/

---

### 评论 #15 — johnnynunez (2024-05-10T19:22:33Z)

> Please check latest ROCm 6.1.1 https://rocm.docs.amd.com/projects/install-on-windows/en/latest/

links is to 5.7.1
![image](https://github.com/ROCm/ROCm/assets/22727137/145df424-a212-4729-8b73-e8588547c167)

---

### 评论 #16 — ppanchad-amd (2024-05-14T14:35:28Z)

@johnnynunez Sorry about the confusion.  Current HIP SDK version available for windows is 5.7.1

---

### 评论 #17 — MoonRide303 (2024-08-21T07:44:18Z)

> Support available. Please check latest ROCm 6.1.1 https://rocm.docs.amd.com/projects/install-on-windows/en/latest/

It doesn't look like "support available" to me (at least according to [pytorch.org](https://pytorch.org/)):

![image](https://github.com/user-attachments/assets/d5289c01-ca63-4087-8577-50332cbc4366)


---

### 评论 #18 — evshiron (2024-08-21T09:02:46Z)

@MoonRide303 

Use ROCm in WSL if you have a compatible GPU:

* https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html

I have been using it for two months and it works (imo better than in Linux), with some tricks.

---

### 评论 #19 — MoonRide303 (2024-08-21T10:16:32Z)

> @MoonRide303
> 
> Use ROCm in WSL if you have a compatible GPU:
> 
> * https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html
> 
> I have been using it for two months and it works (imo better than in Linux), with some tricks.

WSL is a workaround, not a native Windows support.

---

### 评论 #20 — evshiron (2024-08-21T10:57:01Z)

> WSL is a workaround, not a native Windows support.

Alright. In my opinion, choosing to support WSL is a smart decision. It (almost) perfectly integrates with the existing ROCm ecosystem on Linux and can already support many professional workflows. I'm quite satisfied with my two-month experience.

---
