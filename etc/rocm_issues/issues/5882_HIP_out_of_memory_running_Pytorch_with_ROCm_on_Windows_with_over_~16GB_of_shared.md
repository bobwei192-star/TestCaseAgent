# HIP out of memory: running Pytorch with ROCm on Windows with over ~16GB of shared graphics memory

> **Issue #5882**
> **状态**: open
> **创建时间**: 2026-01-22T16:00:03Z
> **更新时间**: 2026-03-20T15:16:15Z
> **作者**: kopzwj
> **标签**: Windows, application:pytorch, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5882

## 标签

- **Windows** (颜色: #c2e0c6)
- **application:pytorch** (颜色: #bfdadc)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

Dear ROCm developers:

When I'm trying to testing LLM and Z-image models on my ROG FLOW Z13, If I assign a total shared graphics memory of over ~16 GB to 8060s graphics core, The Pytorch would always told me a Out Of Memeoy Error, but at that time Pytorch could still detect the correct number of shared grahics memory, followed information shows "allocate 0 , allocated 0". I've found this fault could be fixed in Linux by upgrading the 6.16 kernel, but now I'm in Windows enviorment, so is there some way to avoid it or any future fix?
This problem appears both in ROCm 7.1.1 with 25.20 adrenalin catalyst and the newly issued ROCm 7.2 with 26.1.1 adrenalin catalyst.

Here are some informations:
windows version: windows 11 home 25H2
adrenalin catalyst version: 26.1.1
ROCm version: 7.2
Pytorch version: 2.9.1
Hardware platform: ROG FLOW Z13, AMD AI MAX+ 395, 128GB memory with 64GB assigned to intergrated graphics (AMD 8060S)

<img width="2560" height="1599" alt="Image" src="https://github.com/user-attachments/assets/536fca07-a5f9-46fc-9362-a5b25972cb0e" />

<img width="2560" height="1600" alt="Image" src="https://github.com/user-attachments/assets/aa066248-43eb-47c2-8238-9988ec648c30" />

---

## 评论 (2 条)

### 评论 #1 — schung-amd (2026-02-20T20:37:55Z)

Hi @kopzwj, thanks for the report. We're looking into some similar issues reported with dedicated VRAM set higher than default on Windows. Can you provide reproducer code for your issue?  

---

### 评论 #2 — kopzwj (2026-03-20T15:16:15Z)

Sorry for replying late.

You could refer to the sample code in these attachments.

And these codes are also the example codes provided by Modelscope. You could find them on Modelscope model page.

Here's the introduction page for QWEN3-32B: https://www.modelscope.cn/models/Qwen/Qwen3-32B
And the code I used for QWEN3-32B is a changed version only by replacing models from example codes for QWEN3-4B. The reference codes is here: https://www.modelscope.cn/models/Qwen/Qwen3-4B

                                                                                    Thanks.


________________________________
发件人: schung-amd ***@***.***>
已发送: 2026 年 2 月 21 日 星期六 04:38
收件人: ROCm/ROCm ***@***.***>
抄送: kopzwj ***@***.***>; Mention ***@***.***>
主题: Re: [ROCm/ROCm] HIP out of memory: running Pytorch with ROCm on Windows with over ~16GB of shared graphics memory (Issue #5882)

[https://avatars.githubusercontent.com/u/175627365?s=20&v=4]schung-amd left a comment (ROCm/ROCm#5882)<https://github.com/ROCm/ROCm/issues/5882#issuecomment-3937053995>

Hi @kopzwj<https://github.com/kopzwj>, thanks for the report. We're looking into some similar issues reported with dedicated VRAM set higher than default on Windows. Can you provide reproducer code for your issue?

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/5882#issuecomment-3937053995>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/B4P7F5PCWNQOXRJW2WJ5NIT4M5WDTAVCNFSM6AAAAACSR2JRCOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSMZXGA2TGOJZGU>.
You are receiving this because you were mentioned.Message ID: ***@***.***>


---
