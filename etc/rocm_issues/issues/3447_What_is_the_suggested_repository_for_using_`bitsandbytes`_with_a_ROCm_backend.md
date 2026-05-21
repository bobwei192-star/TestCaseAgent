# What is the suggested repository for using `bitsandbytes` with a ROCm backend?

> **Issue #3447**
> **状态**: closed
> **创建时间**: 2024-07-22T15:31:16Z
> **更新时间**: 2024-07-31T20:12:02Z
> **关闭时间**: 2024-07-31T20:12:02Z
> **作者**: garrettbyrd
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3447

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

AMD has forked `bitsandbytes` [here](https://github.com/ROCm/bitsandbytes). There was a [bit of confusion](https://github.com/ROCm/ROCm/issues/3132) regarding the installation and usage of this fork and its `rocm_enabled` branch; I have not tested this fork/branch within a week or so, but it seems that it is still unclear if this will work out of the box, or even if this is the correct fork/branch to be using.

The developers at the [upstream branch](https://github.com/bitsandbytes-foundation/bitsandbytes) have recently released the `bitsandbytes/multi-backend-refactor` branch ([link](https://github.com/bitsandbytes-foundation/bitsandbytes/tree/multi-backend-refactor?tab=readme-ov-file)) that is in the testing phase for supporting AMD GPUs and Intel GPUs.

Which of these two, between `ROCm/bitsandbytes` and `bitsandbytes-foundation/bitsandbytes` should be considered the go-to? Is AMD contributing to the upstream branch? If not, why? What has been developed for the ROCm branch that is not in the `multi-backend-refactor` upstream branch?

---

## 评论 (7 条)

### 评论 #1 — ppanchad-amd (2024-07-29T15:34:01Z)

@garrettbyrd Internal ticket is created to assist with your issues. Thanks!

---

### 评论 #2 — schung-amd (2024-07-29T17:01:05Z)

Hi @garrettbyrd, I reached out to the internal team handling `ROCm/bitsandbytes`. Changes to the AMD fork are also pushed to the `multi-backend-refactor` upstream branch, so you should be able to use either. I can see from your linked open issue (https://github.com/ROCm/ROCm/issues/3132) that you're having install or configuration issues with `ROCm/bitsandbytes`. If you decide to try the `multi-backend-refactor` upstream branch and experience similar issues, please comment on this in your existing issue or open a new issue.

If this answers your question, you can close this issue. If not or if there are any additional items you'd like clarified, you can reach out to me here or to @pnunna93 in your existing issue. Thanks!

---

### 评论 #3 — saadrahim (2024-07-29T17:03:07Z)

@schung-amd can you check where this will be documented for posterity? This question may be repeated by others. 

---

### 评论 #4 — schung-amd (2024-07-29T17:38:20Z)

@saadrahim Great suggestion, thanks. Incorporation of the ROCm fork to the upstream branch was noted [here](https://github.com/bitsandbytes-foundation/bitsandbytes/issues/1271), but this isn't the most visible; I'm reaching out to @pnunna93 to see if we can get something added to the description of the ROCm fork.

---

### 评论 #5 — garrettbyrd (2024-07-30T14:58:14Z)

@schung-amd Thanks for the information. I will be happy to close if/once something is added to the description of the ROCm fork, as you suggested.

---

### 评论 #6 — pnunna93 (2024-07-31T19:39:28Z)

I have updated our fork to reflect this. Thanks for the feedback @garrettbyrd!

---

### 评论 #7 — garrettbyrd (2024-07-31T20:12:02Z)

@pnunna93 Lovely! Thanks for the addition.

---
