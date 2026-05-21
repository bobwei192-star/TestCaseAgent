# [Feature]: PyTorch Windows Support

> **Issue #2915**
> **状态**: closed
> **创建时间**: 2024-02-21T06:34:34Z
> **更新时间**: 2024-10-28T19:08:39Z
> **关闭时间**: 2024-03-14T07:51:34Z
> **作者**: ZhiQiu-Kinsey
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2915

## 描述

I am using ROCm on Windows to run deep learning models, but I found that it does not support PyTorch and TensorFlow, two popular deep learning frameworks. I wonder if you have any plans to support these frameworks.

My expectations are:

- **I hope that ROCm on Windows can support PyTorch and TensorFlow, or at least tell me when it will be able to support them. Do you have this plan? Is it in development? Is there any progress?**
- **I hope to be able to run deep learning models on AMD GPUs, without having to switch to other platforms or devices**

My actual results are:

I cannot use PyTorch and TensorFlow on ROCm on Windows, and I have not found any relevant information or documentation
I feel that ROCm on Windows has very limited support for deep learning, which does not meet my needs

### Operating System

Windows

### GPU

RX7800XT

### ROCm Component

PyTorch

---

## 评论 (12 条)

### 评论 #1 — ZhiQiu-Kinsey (2024-02-22T06:21:06Z)

@nartmada

---

### 评论 #2 — johnnynunez (2024-02-22T10:39:48Z)

> I am using ROCm on Windows to run deep learning models, but I found that it does not support PyTorch and TensorFlow, two popular deep learning frameworks. I wonder if you have any plans to support these frameworks.
> 
> My expectations are:
> 
> * **I hope that ROCm on Windows can support PyTorch and TensorFlow, or at least tell me when it will be able to support them. Do you have this plan? Is it in development? Is there any progress?**
> * **I hope to be able to run deep learning models on AMD GPUs, without having to switch to other platforms or devices**
> 
> My actual results are:
> 
> I cannot use PyTorch and TensorFlow on ROCm on Windows, and I have not found any relevant information or documentation I feel that ROCm on Windows has very limited support for deep learning, which does not meet my needs
> 
> ### Operating System
> Windows
> 
> ### GPU
> RX7800XT
> 
> ### ROCm Component
> PyTorch

To be compatible, the entire RocM pipeline must first be compatible. For IA it is MIOpen and AMDMIGraphX. As you can see in their PRs in MiOpen they were all attached and in AMDMIGraphX there are 3 pending. 
After this, AMD engineers should add the amd whl build for windows to the Pytorch CI.

---

### 评论 #3 — johnnynunez (2024-02-26T21:01:58Z)

@ZhiQiu-Kinsey rocm6.1 will support windows as changelongs says

---

### 评论 #4 — ZhiQiu-Kinsey (2024-02-28T09:59:13Z)

> rocm6.1 will support windows as changelongs says

@johnnynunez Thanks for the update! Could you please share the source or reference for the information about ROCm 6.1 supporting Windows? I'd like to get more details on it.


---

### 评论 #5 — johnnynunez (2024-02-28T18:08:28Z)

> > rocm6.1 will support windows as changelongs says
> 
> @johnnynunez Thanks for the update! Could you please share the source or reference for the information about ROCm 6.1 supporting Windows? I'd like to get more details on it.


https://github.com/ROCm/AMDMIGraphX/commit/40f306377b5ab1a0af0c080b08cdc54f3190193c

---

### 评论 #6 — Arondight (2024-03-01T18:40:12Z)

> > > rocm6.1 will support windows as changelongs says
> > 
> > 
> > @johnnynunez Thanks for the update! Could you please share the source or reference for the information about ROCm 6.1 supporting Windows? I'd like to get more details on it.
> 
> [ROCm/AMDMIGraphX@40f3063](https://github.com/ROCm/AMDMIGraphX/commit/40f306377b5ab1a0af0c080b08cdc54f3190193c)

it is just initial code i think

---

### 评论 #7 — Arondight (2024-03-01T18:46:23Z)

> I am using ROCm on Windows to run deep learning models, but I found that it does not support PyTorch and TensorFlow, two popular deep learning frameworks. I wonder if you have any plans to support these frameworks.

哥们，要么换系统，要么换硬件，我去年买 7950x + 7900xtx 的票上了这条破船，居家办公又没法换系统，我只能又搞了一个 2696v3 + 2080ti22g x 2 的机器，我觉得还是不要对 amd 抱有什么期望为好

我之前用他家写在官网首页上的 storemi，你选软件前五里面就有，我只想说这玩意儿用着真的可能会死人，别对 amd 有啥幻想了，好多东西都是赶鸭子上架弄得

---

### 评论 #8 — ZhiQiu-Kinsey (2024-03-02T14:30:06Z)

> > I am using ROCm on Windows to run deep learning models, but I found that it does not support PyTorch and TensorFlow, two popular deep learning frameworks. I wonder if you have any plans to support these frameworks.
> 
> 哥们，要么换系统，要么换硬件，我去年买 7950x + 7900xtx 的票上了这条破船，居家办公又没法换系统，我只能又搞了一个 2696v3 + 2080ti22g x 2 的机器，我觉得还是不要对 amd 抱有什么期望为好
> 
> 我之前用他家写在官网首页上的 storemi，你选软件前五里面就有，我只想说这玩意儿用着真的可能会死人，别对 amd 有啥幻想了，好多东西都是赶鸭子上架弄得

AI方面amd就不行，打不过英伟达的CUDA生态,我当时买amd就是为了性价比，主要用来打游戏，最近玩Stable Diffusion，AMD显卡没法全性能运行。

---

### 评论 #9 — znsoftm (2024-03-24T22:35:30Z)

AMD consistently champions the battles of tomorrow, not today's.

---

### 评论 #10 — znsoftm (2024-03-24T22:36:21Z)

苏妈的软件一直不太灵。 The software of AMD sucks.

---

### 评论 #11 — Arondight (2024-03-26T11:54:08Z)

> 苏妈的软件一直不太灵。 The software of AMD sucks.

雀食按摩店萨克斯，2080ti22g x2 的炉子花了 9000 块钱，当初要是上 4090 还能剩下不少，一声叹息，希望早日支持 windows 吧（而且不要有啥八哥），我还是很希望手里的 xtx 能发光发热的

---

### 评论 #12 — johnnynunez (2024-10-28T19:08:37Z)

https://github.com/pytorch/pytorch/pull/137279 here! native version

---
