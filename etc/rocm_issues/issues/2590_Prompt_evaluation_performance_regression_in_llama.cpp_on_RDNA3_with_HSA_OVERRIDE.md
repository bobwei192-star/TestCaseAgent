# Prompt evaluation performance regression in llama.cpp on RDNA3 with HSA_OVERRIDE_GFX_VERSION=11.0.1 vs 11.0.0

> **Issue #2590**
> **状态**: closed
> **创建时间**: 2023-10-20T16:12:53Z
> **更新时间**: 2024-07-19T17:14:08Z
> **关闭时间**: 2024-07-19T17:14:08Z
> **作者**: Googulator
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2590

## 描述

We're evaluating llama.cpp with ROCm offloading on various RDNA3 GPUs (primarily RX 7800 XT and RX 7900 XT).

On initial testing, we found that a 13b model with Q6_K quantization fully offloaded to GPU (-ngl 43) showed significantly slower prompt evaluation times on the 7800 compared to the 7900, far beyond what would be expected from the relative performance difference between these 2 GPUs. On the 7800, prompt evaluation would take more than a minute on our example prompt, while it was near instantaneous (less than a second) on the 7900.

Upon further investigation, the RX 7800 shows a 3 second penalty for every 64 tokens of prompt (0-64 tokens 3 seconds, 65-128 tokens 6s, 129-192 tokens 9s, and so on) over the 7900.

Since the 7800 is recognized by ROCm as gfx1101, vs gfx1100 on the 7900, we tried setting HSA_OVERRIDE_GFX_VERSION=11.0.0, which led to massive performance improvement, with the 7800 only proportionally slower than the 7900, as expected based on the specifications. We then tested HSA_OVERRIDE_GFX_VERSION=11.0.1 (and 11.0.2) on the 7900, and saw the exact same performance issue as on the 7800.

The testing was performed on Ubuntu 22.04.3 Server, using ROCm v5.7.0, apparently the latest version available for this version of Ubuntu.

---

## 评论 (7 条)

### 评论 #1 — Pierre-vh (2023-11-29T06:45:15Z)

Hi,

We're investigating this, can you provide some instructions to reproduce this issue? 
How can we test llama.cpp in the same way you did?

Thanks

---

### 评论 #2 — kzhuravl (2023-12-06T14:07:14Z)

@Googulator, gentle ping. Can you provide repro steps?

---

### 评论 #3 — Googulator (2023-12-07T03:04:47Z)

Hi!

You will need a 7800 XT, 7900 GRE, 7900 XT or 7900 XTX card, the latest llama.cpp code, and a matching recent Llama 2-13B-based GGUF model.

Export HSA_OVERRIDE_GFX_VERSION=11.0.1 in your environment, then compile llama.cpp for ROCm (using the LLAMA_HIPBLAS=1 option).

Launch the server:
```
./server -m /path/to/model.gguf -c 4096 -ngl 43 --mlock --host 0.0.0.0 --port 8080
```

Open http://localhost:8080 in your browser, set temperature to zero, and insert the following prompt in the bottom field:

```
What happened to Apollo 13?
```

(Don't change any other options.)

Click Send, then measure the time it takes before Llama starts generating text. (The speed of text generation is unaffected, it's the time it takes for Llama to even begin generating text that takes time. Also, only the first invocation with each prompt is slow - subsequent invocations without restarting the server will come from the prompt cache, and thus hide the regression.)

Now, repeat this procedure with HSA_OVERRIDE_GFX_VERSION=11.0.0 exported in your environment (instead of 11.0.1). Observe how the text starts to get generated almost instantaneously,instead of a multi-second delay as with 11.0.1.

If you replace the prompt with something longer (e.g. "What is this song called?" followed by the lyrics of your country's national anthem), the difference gets exponentially worse.

---

### 评论 #4 — kzhuravl (2024-01-05T18:11:21Z)

This was rootcaused by @Pierre-vh  and **_Stempen, Vladimir_** as an issue in llama.cpp.

Fix is here: https://github.com/ggerganov/llama.cpp/pull/4787

---

### 评论 #5 — SlyEcho (2024-01-06T20:32:00Z)

Hello, I was one of the people that worked on ROCm support on llama.cpp. While the code that we came up with in the end is working, it is still not really well tested on all GPUs.

I would say that there is still an issue with ROCm itself because of lacking certain features that CUDA has namely the `__dp4a` integer intrinsic. I think it would be much better if it were implemented by 1st party engineers from AMD.

---

### 评论 #6 — kzhuravl (2024-01-09T15:46:08Z)

@Googulator, can you re-test with the https://github.com/ggerganov/llama.cpp/pull/4787 and see if we can close this ticket?

@SlyEcho, I will forward your comment to someone internally.

---

### 评论 #7 — ppanchad-amd (2024-07-19T17:14:08Z)

@Googulator Closing ticket since there is no response.  Please re-open if you still see the issue. Thanks!

---
