# The ‘rocm-smi’ command does not take effect during cgroup isolation

> **Issue #2366**
> **状态**: closed
> **创建时间**: 2023-08-04T02:33:30Z
> **更新时间**: 2024-03-02T03:41:00Z
> **关闭时间**: 2024-03-02T03:40:59Z
> **作者**: wjp-cn
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2366

## 描述

Hello, may I ask for your advice? I have encountered a problem. I have two GPUs with AMD. When I use the ‘rocm-smi’ command in a container that has applied for cgroup isolation of one GPU, it still displays two GPUs. Is this because the ‘rocm-smi’  command does not support cgroup isolation at the bottom level

---

## 评论 (3 条)

### 评论 #1 — akondrat-amd (2024-02-09T18:55:32Z)

Can you post the options that you use when you start the container? 
You can isolate GPUs with "--device=/dev/dri/renderD128" option, where "renderD128" is your GPU. You can also isolate GPU inside the container with environment variable "export ROCR_VISIBLE_DEVICES=0,1" (see rocm-smi for device ids).

---

### 评论 #2 — nartmada (2024-02-23T23:11:55Z)

Hi @Wercurial, can you please post the options that you use when you start the container?  Thanks.

---

### 评论 #3 — nartmada (2024-03-02T03:40:59Z)

Closing the ticket as there is no response from @Wercurial.  Please re-open if you still encounter this issue.  Thanks.

---
