# I have a question on how to download pytorch.

> **Issue #4872**
> **状态**: closed
> **创建时间**: 2025-06-03T12:57:20Z
> **更新时间**: 2025-06-05T00:24:16Z
> **关闭时间**: 2025-06-04T02:55:05Z
> **作者**: soapold
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4872

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I am working with a 7900XTX GPU and a Windows 11 system. As we all know that we have windows' version ROCm , whitch is called HIP_SDK, please forgive me about my stupid, but I truly unable to download a suitable pytorch for HIP_SDK 6.2. Has anyone tried this ? I really cannot find a suitable way.

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2025-06-03T18:57:09Z)

Hi @soapold, the best method to use ROCm + PyTorch on Windows is through the Windows Subsystem for Linux (WSL). You can find more information on how to get started with ROCm on WSL over at [Install Radeon Software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#install-radeon-software-for-wsl-with-rocm). Let me know if you have any questions!

As for native Windows support, ROCm + PyTorch on Windows is still under development, with an official release planned for Q3 2025. You'll have to wait for this release as the HIP SDK does not currently enable you to run PyTorch natively. 

---

### 评论 #2 — soapold (2025-06-04T02:55:05Z)

Thanks,I just tried your suggestion and it works, I can truly work on something now.

---

### 评论 #3 — jammm (2025-06-04T11:39:49Z)

@soapold There's unofficial native pytorch wheels available in https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x built using [TheRock](https://github.com/ROCm/TheRock). Feel free to try it!

---

### 评论 #4 — soapold (2025-06-05T00:24:15Z)

Wow, that's cool, I will try that later.

---
