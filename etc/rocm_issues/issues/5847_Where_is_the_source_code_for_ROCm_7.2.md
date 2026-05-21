# Where is the source code for ROCm 7.2 ?

> **Issue #5847**
> **状态**: closed
> **创建时间**: 2026-01-09T08:08:53Z
> **更新时间**: 2026-01-26T20:49:27Z
> **关闭时间**: 2026-01-14T17:08:23Z
> **作者**: akuckartz
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5847

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

According to press statements published by AMD a version 7.2 is available.

But where is the source code?

According to https://rocm.docs.amd.com/en/latest/release/versions.html the latest version is 7.1.1

---

## 评论 (5 条)

### 评论 #1 — d-shehu (2026-01-14T16:27:47Z)

I'm also confused by AMD's release process here. If you announce a release then it should actually be "released" to the public or a date is published. If it's been delayed can we please see progress / bugs tracked, etc?

My interest is specifically a stable ROCm release to test VLLM with dual R9700 pro and tensor parallelism. Thanks.

Reference: https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-expands-ai-leadership-across-client-graphics-.html

> AMD announces AMD ROCm 7.2 software for Windows and Linux, delivering seamless support for Ryzen AI 400 Series processors and integration into ComfyUI.

> AMD also announced new ROCm™ 7.2 software support for all Ryzen™ AI 400 Series processors, along with a new AI bundle feature for AMD Software: Adrenalin™ Edition, making AI adoption, development, and deployment seamless and accessible.

> AMD ROCm Software Expands Developer Access
> AMD announced AMD ROCm software, the open software platform from AMD, now supports Ryzen AI 400 Series processors and is available as an integrated download through ComfyUI. The upcoming AMD ROCm software 7.2 release will extend compatibility across both Windows and Linux, and new PyTorch builds can now be easily accessed through AMD software for streamlined deployment on Windows.

---

### 评论 #2 — schung-amd (2026-01-14T17:08:23Z)

Hi @akuckartz and @d-shehu, sorry for the confusion! ROCm 7.2 isn't out yet, and we haven't announced when it will be released; if your source is the linked press release, it's misleading as it does state that 7.2 is upcoming but not in the summary.

Poor communication in media releases and regarding timelines in general has been a common pain point that I'm hoping will improve in the future. For now unfortunately you'll have to wait on an announcement that specifically states that 7.2 is released and/or the appearance of the release in the repo.

I'll be closing this as there isn't anything to do but wait, but feel free to continue discussion here if desired.

---

### 评论 #3 — schung-amd (2026-01-21T22:35:26Z)

7.2 is now live: https://github.com/ROCm/ROCm/releases/tag/rocm-7.2.0. Thanks for your patience!

---

### 评论 #4 — d-shehu (2026-01-24T05:01:49Z)

Good news but it's not clear that vllm is fully compatible with ROCm 7.2.  Since AMD is packaging vllm with ROCM presumably to address dependencies and compatibility in a dockerized image I was hoping there would be an update there as part of the release.

The docs were updated to 7.2 but the release is not all encompassing? Thanks for the update! 

* https://hub.docker.com/r/rocm/vllm
* https://rocm.docs.amd.com/en/docs-7.2.0/how-to/rocm-for-ai/inference/llm-inference-frameworks.html#

---

### 评论 #5 — schung-amd (2026-01-26T20:49:26Z)

ROCm 7.2 is compatible with vLLM as far as I'm aware, but we're investigating a performance regression with vLLM that's keeping us tied to ROCm 7.0 at the moment. Once we've sorted that out we'll be able to move forward with new inference Docker releases. No firm timeline on that as it depends how effective our fixes are, but likely not short term and would expect something in the next few months.

---
