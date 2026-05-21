# How do I install ROCm for fedora 40? Where are the repositories?

> **Issue #3446**
> **状态**: closed
> **创建时间**: 2024-07-21T00:24:52Z
> **更新时间**: 2024-07-24T13:31:33Z
> **关闭时间**: 2024-07-24T13:31:32Z
> **作者**: grahamberends
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3446

## 描述

Question: How do I install ROCm for fedora 40? Where are the repositories?

CUDA: My ROCm is not not linking my GPU to my CPU. Hey, ...ROCm is not even installed!
I can't find how to install it.
Please help:
- How do I install ROCm for fedora 40? 
- Where are the repositories? Or, usable repositories?
- Where is some form of documentation?

Look forward to your replies
Regards
Graham

**My computer:**
Fedora 6.9.8-200.fc40.x86_64 #1 SMP PREEMPT_DYNAMIC Fri Jul  5 16:20:11 UTC 2024 x86_64 GNU/Linux. 
**CPU** is 12th Gen Intel(R) Core(TM) i9-12900K with 64 cores. 
**GPU** is Navi 33 Radeon 7600 Advanced Micro Devices, Inc. 
After install of fc40 and first upgrade, from dmesg
 Firmware is amdgpu 0000:03:00.0: amdgpu: Will use PSP to load VCN firmware.
And, From dmesg
 amdgpu: Will use PSP to load VCN firmware
 amdgpu: reserve 0x1300000 from 0x81fc000000 for PSP TMR
  amdgpu: RAS: optional ras ta ucode is not available
 amdgpu: RAP: optional rap ta ucode is not available
 amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
 amdgpu: smu driver if version = 0x00000035, smu fw if version = 0x00000040, smu fw program = 0, smu fw version =  0x00525b00 (82.91.0)
 amdgpu: SMU driver if version not matched
 amdgpu: SMU is initialized successfully!
**Python** 3.12.4. 
**CUDA** I use torch to test if I have parallel processing: 
$ python ./test_for_GPU_torch.py
Code:
```
import torch
query = torch.cuda.is_available()
print("If ROCm is installed, torch.cuda.is_available() will return True.")
print(f"Question: torch.cuda.is_available: {query}")

```
Reply:
If ROCm is installed, torch.cuda.is_available() will return True.
Question: torch.cuda.is_available: False



---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-07-23T19:13:49Z)

Hi @grahamberends, while Fedora is not an officially supported operating system, you can follow these [install instructions](https://fedoraproject.org/wiki/SIGs/HC#Installation) from the Fedora Wiki to get started with ROCm. The packages listed in the installation are shipped with Fedora and don't require adding external repositories.

After installing ROCm, you can run the following command to install PyTorch 2.3.0 for ROCm 6.0.0.
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0`

By following these steps, I was able to run your sample code and output the following: 
```
If ROCm is installed, torch.cuda.is_available() will return True.
Question: torch.cuda.is_available: True
```

---

### 评论 #2 — grahamberends (2024-07-23T23:21:16Z)

Dear harkgill-amd.

Thank you so much. Your instructions ran without a hitch. It was easy. 

And, I like the idea that the _opencl_ code is used. It was also good to use the output from rocminfo and rocm-clinfo. 

I ran my little test code, see above ... and got this output:
  > If ROCm is installed, torch.cuda.is_available() will return True.
  > Question: torch.cuda.is_available: True

So, my cuda is available. What a relief! 

Now, the exciting work begins!

Yours gratefully
Graham

---

### 评论 #3 — harkgill-amd (2024-07-24T13:31:32Z)

Great! Happy to help :) 

---
