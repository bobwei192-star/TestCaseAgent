# ROCm competition

> **Issue #2188**
> **状态**: closed
> **创建时间**: 2023-05-29T13:36:02Z
> **更新时间**: 2023-06-10T22:32:11Z
> **关闭时间**: 2023-06-10T22:32:11Z
> **作者**: boxerab
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2188

## 描述

https://geohot.github.io//blog/jekyll/update/2023/05/24/the-tiny-corp-raised-5M.html

````
The software is terrible! There’s kernel panics in the [driver](https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver). You have to run a newer kernel than the Ubuntu default to make it remotely stable. I’m still not sure if the driver supports putting two cards in one machine, or if there’s some poorly written global state. When I put the second card in and run an OpenCL program, half the time it kernel panics and you have to reboot.

That’s the kernel space, the user space isn’t better. The [compiler](https://github.com/RadeonOpenCompute/llvm-project) is so bad that [clpeak](https://github.com/krrishnarraj/clpeak) only gets half the max possible FLOPS. And clpeak is a completely contrived workload attempting to maximize FLOPS, never mind how many FLOPS you get on a real program (usually like 25%).

The software is called ROCm, it’s open source, and supposedly it works with [PyTorch](https://pytorch.org/blog/pytorch-for-amd-rocm-platform-now-available-as-python-package/). Though I’ve tried 3 times in the last couple years to build it, and every time it didn’t build out of the box, I struggled to fix it, got it built, and it either segfaulted or returned the wrong answer. In comparison, I have probably built CUDA PyTorch 10 times and never had a single issue.

Where does the tiny corp come in?
Forget all that software. The RDNA3 [Instruction Set](https://www.amd.com/system/files/TechDocs/rdna3-shader-instruction-set-architecture-feb-2023_0.pdf) is well documented. The hardware is great. We are going to write our own software.

If you were to tape out your own chip, you’d be struggling with both hardware bugs and software bugs, and you wouldn’t be sure which one it is. Here, you have a good idea, and have the AMD provided driver as an open source reference.

This is life on easy mode, and I still doubt any of those AI startups could have done it. This is what the tiny corp is going to do to start. **Build a framework, runtime, and driver for AMD chips.**
```


---

## 评论 (2 条)

### 评论 #1 — De-Been-Tech-Solutions (2023-06-01T01:04:26Z)

Looks like a scam.

---

### 评论 #2 — De-Been-Tech-Solutions (2023-06-02T08:08:50Z)

Never mind, it isn't. I have it installed.

---
