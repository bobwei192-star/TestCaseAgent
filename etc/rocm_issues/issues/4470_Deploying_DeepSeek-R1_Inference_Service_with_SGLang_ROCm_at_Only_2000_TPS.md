# Deploying DeepSeek-R1 Inference Service with SGLang ROCm at Only 2000 TPS

> **Issue #4470**
> **状态**: closed
> **创建时间**: 2025-03-10T12:00:15Z
> **更新时间**: 2025-03-16T02:35:54Z
> **关闭时间**: 2025-03-16T02:35:53Z
> **作者**: divinerapier
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4470

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I followed the [operational procedures](https://rocm.blogs.amd.com/artificial-intelligence/DeepSeekR1_Perf/README.html) outlined in the article and ran tests on the MI325 x8, hoping to replicate the same results. Unfortunately, with a BatchSize=160, the TPS only reached around 2000. Do you have any suggestions?

CMD:

``` bash
python3 -m sglang.launch_server \
  --model deepseek-ai/DeepSeek-R1 \
  --port 8000 \
  --trust-remote-code \
  --tp 8
```

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2025-03-10T14:38:36Z)

Hi @divinerapier. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — divinerapier (2025-03-16T02:35:53Z)

Unfortunately, the AMD machines we used for testing expired a few days ago. I will provide an update once I have more information. 

T.T

---
