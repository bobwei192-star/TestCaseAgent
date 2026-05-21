# Performance Issue on AMD MI300x

> **Issue #4384**
> **状态**: closed
> **创建时间**: 2025-02-17T06:36:24Z
> **更新时间**: 2025-05-26T19:39:18Z
> **关闭时间**: 2025-05-26T19:39:17Z
> **作者**: theneildave
> **标签**: Under Investigation, AMD Instinct MI300X
> **URL**: https://github.com/ROCm/ROCm/issues/4384

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)

## 描述

We are running Pytorch Profiler with 

Model - **Llama 3.3 -70B**
Tensor - **TP4** 
Prompt - **The quick brown fox jumps over the lazy**

and our observation is that accelerator performance is marginal difference but CPU overhead is not able to achieve optimise performance.


![Image](https://github.com/user-attachments/assets/b6faec48-002d-4d81-8825-86ec1b76a316)

![Image](https://github.com/user-attachments/assets/6dbe4eed-a0bf-4dfa-97c9-11b877c5dbc6)

If any further information is required please let me know.

---

## 评论 (5 条)

### 评论 #1 — pruthvistony (2025-02-17T19:12:28Z)

@Neildave999 ,
Are you using vLLM here?

---

### 评论 #2 — theneildave (2025-02-18T06:28:53Z)

@pruthvistony No vLLM is not used for model serving

---

### 评论 #3 — ppanchad-amd (2025-02-18T15:05:24Z)

Hi @Neildave999. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #4 — schung-amd (2025-02-18T15:19:12Z)

Hi @Neildave999, what version of ROCm are you using? From the pytorch profiler output alone this looks a lot like https://github.com/ROCm/clr/issues/78. That issue is fixed in internal builds, but I don't know if the fix landed in 6.3.2. A user in that issue was able to apply the fix on their end by building `clr` from source.

---

### 评论 #5 — schung-amd (2025-05-26T19:39:17Z)

Closing for now due to lack of response, feel free to comment if you are still experiencing this issue in current ROCm versions and we can reopen if necessary.

---
