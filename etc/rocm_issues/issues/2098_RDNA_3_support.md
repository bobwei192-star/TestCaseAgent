# RDNA 3 support

> **Issue #2098**
> **状态**: closed
> **创建时间**: 2023-05-02T06:50:58Z
> **更新时间**: 2024-05-13T15:36:14Z
> **关闭时间**: 2024-05-13T15:36:14Z
> **作者**: countradooku
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2098

## 描述

We have RDNA support or no in 5.5 release?
I ask this because THERE IS NOTHING IN DOCS. How can you have no windows support adn no rx 7900xtx supoprt in this release?

---

## 评论 (14 条)

### 评论 #1 — mszpulak (2023-05-02T09:24:04Z)

https://www.reddit.com/r/Amd/comments/135f8we/amd_rocm_55_in_the_process_of_being_released/?utm_source=share&utm_medium=android_app&utm_name=androidcss&utm_term=1&utm_content=share_button

---

### 评论 #2 — xfalcox (2023-05-02T17:51:29Z)

This will be solved https://github.com/RadeonOpenCompute/ROCm/pull/2099 that is slated to the 5.6.0 milestone.

---

### 评论 #3 — TheCowboyHermit (2023-05-11T18:39:13Z)

I own 7900 XTX and ROCm 5.5.0 does not work. Both in Stable Diffusion, custom model, and other compute purposes, It failed in **ALL** cases, specifically due to segfault in Hip libraries that AMD directly provided. 

---

### 评论 #4 — johnnynunez (2023-06-22T08:39:20Z)

A lot is changing at RocM. Maybe in RocM 5.6(as they update GPU list) https://twitter.com/aschilling/status/1671447333635260416?s=20

---

### 评论 #5 — xfalcox (2023-06-22T16:30:15Z)

Got my 7900XTX to work with PyTorch by installing nightly PyTorch for RoCM 5.5

---

### 评论 #6 — NaMoCv (2023-06-23T01:40:34Z)

> A lot is changing at RocM. Maybe in RocM 5.6(as they update GPU list) https://twitter.com/aschilling/status/1671447333635260416?s=20

sry, i just forget reboot my machine

---

### 评论 #7 — TheCowboyHermit (2023-06-27T09:50:03Z)

Confirmed that it works on nightly preview for ROCm Pytorch for 7900 XTX on Arch Linux.

---

### 评论 #8 — countradooku (2023-06-27T10:02:52Z)

I tried to install rocm 5.5 on popos but i cant becxause it has a tooo new kernel 

---

### 评论 #9 — johnnynunez (2023-06-27T11:29:23Z)

anyone can execute: https://pypi.org/project/new-ai-benchmark/
```python
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

from ai_benchmark import AIBenchmark
benchmark = AIBenchmark(verbose_level=2)
results = benchmark.run()
```

---

### 评论 #10 — serhii-nakon (2023-08-29T13:35:15Z)

For GFX1101 (W7800, W7900, RX7900, RX7950, RX7990) try use https://hub.docker.com/r/rocm/pytorch-nightly

---

### 评论 #11 — briansp2020 (2023-09-04T15:41:25Z)

Are there still people who are waiting for 7900XTX support? Though the performance is still a bit poor, TensorFlow-upstream now runs when built on the latest ROCm release. I was looking into the status of ROCm support for 7900XTX and found a few issues opened by different people and wanted to link all to the issue I opened in MIOpen repo. Though there has not been any confirmation from the developer, I think the performance issues are due to insufficient optimization of MIOpen. 
https://github.com/ROCmSoftwarePlatform/MIOpen/issues/2342

---

### 评论 #12 — briansp2020 (2023-09-04T15:57:29Z)

@johnnynunez 
I ran the benchmark and posted the output to 
https://gist.github.com/briansp2020/e885f0eb6cbec45fcaf0c2eac8c3ee11

ROCm is in the arena trying stuff. Some will work, some won't. But always learning. j/k.

It actually looks better than I feard. I was really disappointed when I opened https://github.com/ROCmSoftwarePlatform/MIOpen/issues/2342 but it seems that was like one of the worst case scenarios. According to the benchmark output, there are many cases 7900XTX is optimized well enough. Still more work needs to be done. But I'm a lot more hopeful now.

BTW, does anyone know how to disable all the debug output from ROCm? I did os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' trick to get rid of some. But ROCm still prints out too much debug output.

---

### 评论 #13 — johnnynunez (2023-09-05T11:03:37Z)

> @johnnynunez I ran the benchmark and posted the output to https://gist.github.com/briansp2020/e885f0eb6cbec45fcaf0c2eac8c3ee11
> 
> ROCm is in the arena trying stuff. Some will work, some won't. But always learning. j/k.
> 
> It actually looks better than I feard. I was really disappointed when I opened [ROCmSoftwarePlatform/MIOpen#2342](https://github.com/ROCmSoftwarePlatform/MIOpen/issues/2342) but it seems that was like one of the worst case scenarios. According to the benchmark output, there are many cases 7900XTX is optimized well enough. Still more work needs to be done. But I'm a lot more hopeful now.
> 
> BTW, does anyone know how to disable all the debug output from ROCm? I did os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' trick to get rid of some. But ROCm still prints out too much debug output.

Nice, There is room for improvement!

---

### 评论 #14 — ppanchad-amd (2024-05-13T15:36:14Z)

@radudiaconu0 RDNA3 support is available as of latest ROCm 6.1.1. Thanks!

---
