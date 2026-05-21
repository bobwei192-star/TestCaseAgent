# [Feature]: When will ROCm support WSL2+other RDNA3 GPUs rather than navi31 core?

> **Issue #3863**
> **状态**: closed
> **创建时间**: 2024-10-04T15:38:12Z
> **更新时间**: 2025-06-11T18:46:08Z
> **关闭时间**: 2025-06-11T18:46:08Z
> **作者**: Headcrabed
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3863

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

Hello, NAVI31 is already supported to run rocm under wsl2 since 24.6.1 driver, but for NAVI32/33/phoneix platform it is still not supported yet. So when will the support for those platforms land?

### Operating System

WSL2

### GPU

RX 7800 XT

### ROCm Component

_No response_

---

## 评论 (14 条)

### 评论 #1 — rafrafek (2024-10-10T10:38:17Z)

I believe there will be ROCm support for the RX 7800 XT on both Linux and WSL2 in the future, based on the ongoing improvements and expanding hardware support in recent updates. We’ve already seen official ROCm support for the RX 7800 XT on Windows, which is a promising sign.

---

### 评论 #2 — InfiniteBSOD (2024-11-27T18:27:52Z)

Will this also mean that when / if support comes for NAVI32 it will be for [ROCm 6.2.3](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html) or greater which should [support ](https://rocm.docs.amd.com/en/docs-6.2.2/compatibility/compatibility-matrix.html )Ubuntu 24.04.1 (on WSL2)?

---

### 评论 #3 — Apriqi (2024-12-03T09:43:56Z)

请问有什么结果了吗？

---

### 评论 #4 — LeoooChen (2024-12-06T09:41:36Z)

rocm 6.2.3 released, still not support NAVI32. As 8000 series gpu is about to release, the probability of supporting NAVI32 is almost zero. So distinct hierarchy of AMD graphics cards...I'll not choose amd product any more...

---

### 评论 #5 — mrmac189 (2024-12-08T10:14:08Z)

In the end I just use Linux in dual boot, idk why it's such a problem to support wsl, considering that rocm in Linux supports Navi32 

---

### 评论 #6 — maxi201567 (2024-12-20T15:21:44Z)

请问有结果吗？ROCM未来安排什么版本支持一下旧版显卡，本人使用6600XT， navi21，如果不打算支持，是否意味着以往的显卡AI都是噱头，根本就不打算给用户使用。

---

### 评论 #7 — thegreyfellow (2025-02-10T01:02:42Z)

> In the end I just use Linux in dual boot, idk why it's such a problem to support wsl, considering that rocm in Linux supports Navi32

Hi can you confirm that rocm works for navi32 in linux (not wsl) ? as in RX 7800 XT works in linux ?!

---

### 评论 #8 — Headcrabed (2025-02-10T06:28:52Z)

> > In the end I just use Linux in dual boot, idk why it's such a problem to support wsl, considering that rocm in Linux supports Navi32
> 
> Hi can you confirm that rocm works for navi32 in linux (not wsl) ? as in RX 7800 XT works in linux ?!

@thegreyfellow I can confirm it’s working, I am currently using 7800xt under Fedora 41 KDE.

---

### 评论 #9 — Apriqi (2025-04-17T07:05:57Z)

请问有结果吗？ROCM未来安排什么版本支持一下旧版显卡，本人使用7800XT，如果不打算支持，能否告知？是否意味着以往的显卡AI都是噱头？

---

### 评论 #10 — Headcrabed (2025-04-17T10:30:57Z)

> 请问有结果吗？ROCM未来安排什么版本支持一下旧版显卡，本人使用7800XT，如果不打算支持，能否告知？是否意味着以往的显卡AI都是噱头？

@Apriqi 我也是7800xt，目前wsl还没支持，个人建议搞个实体机Linux，我现在是win11+fedora 41 kde双系统，软件支持很完善。

---

### 评论 #11 — Apriqi (2025-04-23T09:29:12Z)

> > 请问有结果吗？ROCM未来安排什么版本支持一下旧版显卡，本人使用7800XT，如果不打算支持，能否告知？是否意味着以往的显卡AI都是噱头？
> 
> [@Apriqi](https://github.com/Apriqi) 我也是7800xt，目前wsl还没支持，个人建议搞个实体机Linux，我现在是win11+fedora 41 kde双系统，软件支持很完善。

双启动实在是太麻烦了，主要还是用windows，代码在ondrive云端同步，linux没有onedrive

---

### 评论 #12 — Headcrabed (2025-04-23T11:40:55Z)

> > > 请问有结果吗？ROCM未来安排什么版本支持一下旧版显卡，本人使用7800XT，如果不打算支持，能否告知？是否意味着以往的显卡AI都是噱头？
> > 
> > 
> > [@Apriqi](https://github.com/Apriqi) 我也是7800xt，目前wsl还没支持，个人建议搞个实体机Linux，我现在是win11+fedora 41 kde双系统，软件支持很完善。
> 
> 双启动实在是太麻烦了，主要还是用windows，代码在ondrive云端同步，linux没有onedrive

@Apriqi 代码同步管理还是git更合适吧..

---

### 评论 #13 — maximilienleclei (2025-05-20T18:50:36Z)

for anyone as impatient as I am, here is a `torch` + `rocm` windows wheel compiled for the 7800 xt: https://drive.proton.me/urls/4QRV647ZXC#RPyLKsYAOHIv

---

### 评论 #14 — harkgill-amd (2025-06-11T18:46:08Z)

Hi @Headcrabed, with the release of ROCm 6.4.1 for WSL, support has been introduced for Navi32/Radeon RX 7800XT! Please see the [GPU Support Matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix) for more information.

We are committed to expanding our hardware support across all our projects whether it's Windows, WSL or Linux. While the remaining SKUs you mentioned don't currently have official WSL support, you can try using [TheRock](https://github.com/ROCm/TheRock) which has build options for these GPUs on native Windows. I'll close out this issue for now but feel free to leave a comment if you have any questions. Thanks!

---
