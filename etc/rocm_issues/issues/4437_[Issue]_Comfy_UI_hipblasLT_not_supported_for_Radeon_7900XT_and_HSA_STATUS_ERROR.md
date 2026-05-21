# [Issue]: Comfy_UI hipblasLT not supported for Radeon 7900XT and HSA_STATUS_ERROR_OUT_OF_REGISTERS error

> **Issue #4437**
> **状态**: closed
> **创建时间**: 2025-03-03T16:32:35Z
> **更新时间**: 2025-03-19T11:55:31Z
> **关闭时间**: 2025-03-17T14:17:24Z
> **作者**: fluidnumericsJoe
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/4437

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 负责人

- tcgu-amd

## 描述

### Problem Description

I'm reporting this issue on behalf of the OP from [this post on discuss.pytorch.org](https://discuss.pytorch.org/t/comfy-ui-attempting-to-use-hipblaslt-on-a-unsupported-architecture/215776).
I've copied the stdout/stderr here

```
Total VRAM 20464 MB, total RAM 63432 MB
pytorch version: 2.6.0.dev20241122+rocm6.2
Set vram state to: NORMAL_VRAM
Device: cuda:0 Radeon RX 7900 XT : native
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
[Prompt Server] web root: /home/sersys/pyproj/ComfyUI-0.3.12/web

Import times for custom nodes:
   0.0 seconds: /home/sersys/pyproj/ComfyUI-0.3.12/custom_nodes/websocket_image_save.py

Starting server

To see the GUI go to: http://127.0.0.1:8188
got prompt
model weight dtype torch.float16, manual cast: None
model_type EPS
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.float32
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load SDXLClipModel
loaded completely 9.5367431640625e+25 1560.802734375 True
/home/sersys/pyproj/ComfyUI-0.3.12/comfy/ops.py:64: UserWarning: Attempting to use hipBLASLt on an unsupported architecture! Overriding blas backend to hipblas (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:296.)
  return torch.nn.functional.linear(input, weight, bias)
Requested to load SDXL
loaded completely 9.5367431640625e+25 4897.0483474731445 True
  0%|                                                                | 0/20 [00:00<?, ?it/s]:0:rocdevice.cpp            :2984: 93862815501 us: [pid:318562 tid:0x7f122e5ff640] Callback: Queue 0x7f0ed8000000 aborting with error : HSA_STATUS_ERROR_OUT_OF_REGISTERS: Kernel has requested more VGPRs than are available on this agent code: 0x2d
Aborted (core dumped)
```

There are two issues here that the OP is concerned about : 

*The first is a non-fatal warning*
There appears to be a warning issued by pytorch stating that the Radeon RX 7900XT is not supported by the HIPBlasLT backend. There is no ROCm documentation that indicates this GPU is not supported by HIPBlasLT; in fact the [compatibility matrix](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus) suggests it is supported. Is this an issue with Pytorch or is this GPU not actually supported in hipblaslt ?

This being said, it does appear that they are not on a [supported Linux kernel](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems) ( 6.12.9 ); however, no errors appear to indicate specifically that this is the culprit.

*The second issue appears fatal*
During the execution of `torch.nn.functional.linear`, the code aborts with an `HSA_STATUS_ERROR_OUT_OF_REGISTERS` error. I suspect this an issue with MIOpen; perhaps it's targeting the wrong architecture and over-allocating vgpr ? My understanding is that some of these torch functions are compiled on the fly during the first execution and this is handled by MIOpen. Any guidance you can provide on further diagnosing the problem here would be great.



### Operating System

Debian GNU/Linux 12

### CPU

AMD Ryzen 9 7900X 12-Core Processor

### GPU

Radeon 7900 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

Pytorch, MIOpen

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (32 条)

### 评论 #1 — ppanchad-amd (2025-03-03T18:07:43Z)

Hi @fluidnumerics-joe. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — fluidnumericsJoe (2025-03-03T18:31:42Z)

This other discussion may be related to the first (non-fatal) issue.

https://discuss.pytorch.org/t/rocm6-2-build-of-pytroch-is-faling-for-llama3-2-vision-model/211622

Here, the users report that another supported AMD Radeon GPU (in this case the Radeon Pro W7900) is being marked as unsupported in hipblaslt . Let me know if you'd like to see another ticket opened for this one.


---

### 评论 #3 — fluidnumericsJoe (2025-03-03T18:40:43Z)

A few other potentially related issues : 

* https://github.com/pytorch/pytorch/issues/138067
* https://github.com/ROCm/hipBLASLt/issues/1243
* https://github.com/pytorch/pytorch/pull/138267

---

### 评论 #4 — tcgu-amd (2025-03-03T19:34:41Z)

Hi @fluidnumerics-joe, thanks for reaching out! The first warning comes from this line of code 

![Image](https://github.com/user-attachments/assets/fd103d54-9719-4f8f-8cea-b4411db3716f)

(https://github.com/ROCm/pytorch/blob/f27220e32af446c24444d4014078106d201d3196/aten/src/ATen/Context.cpp#L329)

The check on line 322 requires ROCm version greater than 6.3 (60300) to support gfx1100 target, which corresponds to RX 7900XT. So, unfortunately, it is not supported on ROCm 6.2 which is the version being used by OP. 

As for the second issue, it is very likely related to unsupported kernel version. I suggest trying downgrading the kernel to a supported version to see if it can resolve the issue, otherwise there would be too many moving parts in the stack to know exactly where went wrong.

Alternatively, I think it might be helpful to set AMD_LOG_LEVEL=3 to trace the ROCr Runtime log, then combine it with HSAKMT_DEBUG_LEVEL=4 to check the HSA/Thunk interface log to pin point the error segment and see what we can do from there. 

Thanks! :)

---

### 评论 #5 — fluidnumericsJoe (2025-03-03T19:43:19Z)

Hey @tcgu-amd - This is incredibly helpful. I'll feed back on this and see if we can help get resolution on this.

---

### 评论 #6 — fluidnumericsJoe (2025-03-03T19:59:58Z)

[OP claims they updated ROCm to v 6.3.2 ](https://discuss.pytorch.org/t/comfy-ui-attempting-to-use-hipblaslt-on-a-unsupported-architecture/215776/6) and still encounter the unsupported gpu in `hipblaslt` issue . From the output from comfy_ui, it appears that it is picking up the ROCm 6.3 install of pytorch 2.7.0 ..

---

### 评论 #7 — fluidnumericsJoe (2025-03-03T20:11:54Z)

From the output they've provided, they're seeing the issue with `pytorch version: 2.7.0.dev20250206+rocm6.3` (February 6 nightly release) . Are we absolutely certain that the changes in https://github.com/pytorch/pytorch/pull/138267 were actually making into nightly builds ? 

We're going to test this out shortly on Radeon Pro W7800 independent of comfy_ui to be certain.

---

### 评论 #8 — tcgu-amd (2025-03-03T20:45:33Z)

@fluidnumerics-joe Interesting...Based on the LOC from the newest error log the change should've made it into the build. I will also try to investigate a bit more on my end. Thanks! 

---

### 评论 #9 — tcgu-amd (2025-03-03T20:52:43Z)

@fluidnumerics-joe Just in case, it might be helpful to manually verify the ROCm version with `torch.version.hip`

---

### 评论 #10 — garrettbyrd (2025-03-03T21:55:57Z)

I was able to test with the specified environment, `torch==2.7.0.dev20250206+rocm6.3` with ROCm 6.3.2.

I did not test on a Radeon RX 7900XT, but I did test on a Radeon PRO W7800, which is also `gfx1100`.

Testing with the [minimal reproducer](https://github.com/pytorch/pytorch/issues/138067#issuecomment-2417505527), I was not able to reproduce the unsupported architecture warning.

I also tested using the latest nightly build of pytorch (`torch==2.7.0.dev20250302+rocm6.3`) and this also ran without raising the warning.

Finally, I also tested on a Radeon RX 7600 with `HSA_OVERRIDE_GFX_VERSION=11.0.0` and this also ran without raising the warning.

---

### 评论 #11 — fluidnumericsJoe (2025-03-04T16:01:31Z)

Thanks @garrettbyrd for adding this - I'm suspecting this is a situation of python environment management issues, more than ROCm. However, we're not looking exactly at a Radeon 7900 XT.

@tcgu-amd Are you able to test the minimal reproducer that Garrett shared on a Radeon 7900XT or are we going to have to pick one up for our cluster ?

---

### 评论 #12 — tcgu-amd (2025-03-04T16:04:40Z)

> Thanks [@garrettbyrd](https://github.com/garrettbyrd) for adding this - I'm suspecting this is a situation of python environment management issues, more than ROCm. However, we're not looking exactly at a Radeon 7900 XT.
> 
> [@tcgu-amd](https://github.com/tcgu-amd) Are you able to test the minimal reproducer that Garrett shared on a Radeon 7900XT or are we going to have to pick one up for our cluster ?

Hi @fluidnumerics-joe, @garrettbyrd yes, I was just able to finish testing. And no, both `export TORCH_BLAS_PREFER_HIPBLASLT=1` and `export TORCH_BLAS_PREFER_HIPBLASLT=0` do not generate warnings on RX 7900XT

---

### 评论 #13 — tcgu-amd (2025-03-04T16:11:34Z)

@fluidnumerics-joe @garrettbyrd, I guess there are two things the OP can check to help debug

1. Use `torch.version.hip` to verify if the ROCm version is indeed >= 6.3
2. Use ` torch.cuda.get_device_properties()` to verify if the `gcnArchName=='gfx1100'`

If both are correct, then something likely is wrong with how ComfyUI is using torch/python. 

---

### 评论 #14 — fluidnumericsJoe (2025-03-04T16:21:20Z)

Thanks @tcgu-amd for testing that out. I'll relay this back to OP

---

### 评论 #15 — fluidnumericsJoe (2025-03-07T18:42:01Z)

Hey @tcgu-amd - I've got some feedback on this one. 

[Here is the output with `AMD_LOG_LEVEL=3` and `HSAKMT_DEBUG_LEVEL=4 `](https://github.com/user-attachments/files/19131804/pyver.txt)

Here is OP's output of

```python
print(torch.version.hip)
print(torch.cuda.get_device_properties())
```

```
6.3.42131-fa1d09cbd
_CudaDeviceProperties(name='Radeon RX 7900 XT', major=11, minor=0, gcnArchName='gfx1100', total_memory=20464MB, multi_processor_count=42, uuid=30303033-6430-3863-3030-303030303030, L2_cache_size=6MB)
```

Here's the [Comfy_UI workflow file](https://github.com/user-attachments/files/19131822/Default.Workflow.json); we're going to take a look at this from Comfy_UI on our system.

Last, OP did mention that their latest attempt was using AMD's Pytorch Docker image (following [these instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/develop/install/3rd-party/pytorch-install.html)) . Also, they confirmed their host system is Debian with Linux kernel 6.12.12-amd64 , which I notice is a minor version ahead of the latest supported Linux kernel in the [supported operating system compatibility matrix](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems)

---

### 评论 #16 — tcgu-amd (2025-03-07T18:49:30Z)

@fluidnumerics-joe Thanks for the update! Interestingly, hip runtime seems to be picking up 2 GPUs on the device, one is gfx1100 and another gfx1036, as can be seen from this part of the logs

 ```
:3:rocdevice.cpp            :1801: 133669785946d us:  Gfx Major/Minor/Stepping: 11/0/0
:3:rocdevice.cpp            :1803: 133669785949d us:  HMM support: 0, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1805: 133669785950d us:  Max SDMA Read Mask: 0x3, Max SDMA Write Mask: 0x3
:3:rocdevice.cpp            :235 : 133669786607d us:  Numa selects cpu agent[0]=0x41b424a0(fine=0x3dcb4590,coarse=0x448ef230) for gpu agent=0x44f26d20 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :287 : 133669786610d us:  Using dev kernel arg wa = 0
:3:rocdevice.cpp            :1801: 133669786959d us:  Gfx Major/Minor/Stepping: 10/3/6
:3:rocdevice.cpp            :1803: 133669786962d us:  HMM support: 0, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1805: 133669786963d us:  Max SDMA Read Mask: 0x1, Max SDMA Write Mask: 0x1
:3:hip_context.cpp          :49  : 133669787646d us:  Direct Dispatch: 1
```
This seems like could be the culprit.

---

### 评论 #17 — fluidnumericsJoe (2025-03-07T19:10:15Z)

@tcgu-amd - The gfx1036 appears to be an iGPU with Ryzen 7000 series CPUs. I suspect they should disable the iGPU : https://rocm.docs.amd.com/projects/radeon/en/latest/docs/prerequisites.html

---

### 评论 #18 — tcgu-amd (2025-03-07T19:56:50Z)

> [@tcgu-amd](https://github.com/tcgu-amd) - The gfx1036 appears to be an iGPU with Ryzen 7000 series CPUs. I suspect they should disable the iGPU : https://rocm.docs.amd.com/projects/radeon/en/latest/docs/prerequisites.html

Makes sense. 

---

### 评论 #19 — fluidnumericsJoe (2025-03-10T16:03:52Z)

Hey @tcgu-amd - I've attached logs ( [igpudisabled.txt](https://github.com/user-attachments/files/19166334/igpudisabled.txt) ) of the same execution, but with the iGPU disabled. This appears to fix the warning related to hipblaslt on an unsupported GPU. However, we're still hitting the `HSA_STATUS_ERROR_OUT_OF_REGISTERS`.

One thing I did notice is that OP is using Python 3.12. This is required for the Comfy_UI package. However, the pytorch installation is using the distributed wheels, which are built against Python 3.10 . [ROCm docs](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html#install-methods) indicate that this configuration won't work


>   Important! These specific ROCm WHLs are built for Python 3.10, and will not work on other versions of Python.

I've fed back that they can uninstall pytorch and [build pytorch from source](https://github.com/pytorch/pytorch/?tab=readme-ov-file#amd-rocm-support) . You may know that this is a time-intensive process, which is why I've also opened up https://github.com/ROCm/ROCm/issues/4473 

~~This is not the only person I've found looking to use Comfy_UI under WSL2 with Radeon GPUs.~~

---

### 评论 #20 — james-banks (2025-03-10T17:01:45Z)

> However, the pytorch installation is using the distributed wheels, which are built against Python 3.10 . [ROCm docs](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html#install-methods) indicate that this configuration won't work
> 
> 
> >   Important! These specific ROCm WHLs are built for Python 3.10, and will not work on other versions of Python.

I believe that notice is outdated. The actual links they provide (and many of the wheels in the repo) are for Python 3.12 (as seen by the `cp312` in the file names): 

> https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torchaudio-2.4.0%2Brocm6.3.4.git69d40773-cp312-cp312-linux_x86_64.whl

---

### 评论 #21 — tcgu-amd (2025-03-10T17:15:01Z)

> Hey [@tcgu-amd](https://github.com/tcgu-amd) - I've attached logs ( [igpudisabled.txt](https://github.com/user-attachments/files/19166334/igpudisabled.txt) ) of the same execution, but with the iGPU disabled. This appears to fix the warning related to hipblaslt on an unsupported GPU. However, we're still hitting the `HSA_STATUS_ERROR_OUT_OF_REGISTERS`.
> 
> One thing I did notice is that OP is using Python 3.12. This is required for the Comfy_UI package. However, the pytorch installation is using the distributed wheels, which are built against Python 3.10 . [ROCm docs](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html#install-methods) indicate that this configuration won't work
> 
> > Important! These specific ROCm WHLs are built for Python 3.10, and will not work on other versions of Python.
> 
> I've fed back that they can uninstall pytorch and [build pytorch from source](https://github.com/pytorch/pytorch/?tab=readme-ov-file#amd-rocm-support) . You may know that this is a time-intensive process, which is why I've also opened up [#4473](https://github.com/ROCm/ROCm/issues/4473)
> 
> This is not the only person I've found looking to use Comfy_UI under WSL2 with Radeon GPUs.

Oh the user is using WSL2? I was under the impression that they were using native linux...

In this case, setting up ROCm on WSL2 works differently from on native Linux, please follow this guide to [install the latest supported ROCm on Radeon](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html), then [this guide for installing pytorch](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html).

Thanks!



---

### 评论 #22 — fluidnumericsJoe (2025-03-10T17:19:55Z)

Apologies, I've gotten this mixed up with other Comfy_UI issues we're tracking. This particular one is on Debian.

---

### 评论 #23 — Sersys (2025-03-11T13:56:36Z)

Hello, I'm OP @fluidnumerics-joe was posting on behalf.

I just want to add a side note, I'm not sure if it's relevant but I'm having issues running Ollama and ffmpeg using av1_amf as well. Both give me the error that they are unable to allocate memory on the GPU. I have a feeling it's the same Rocm issue and probably not a pytorch or comfy_ui fault. Unfortunately I got very little to no help from Ollama and ffmpeg so I can't confirm. 

---

### 评论 #24 — tcgu-amd (2025-03-11T18:18:23Z)

Hi @Sersys, thanks for reaching out to us! Just wondering, do you know if the issues you encountered can be reproduced on one of our supported kernel versions (e.g. 6.11). There has been a few bugs reported to us related to kernel 6.12, just wanted to see if we can isolate the cause here. Thanks! 

---

### 评论 #25 — fluidnumericsJoe (2025-03-13T14:19:02Z)

Hey @Sersys - Have you been able to try reproducing the error on a supported kernel ?

---

### 评论 #26 — Sersys (2025-03-14T18:12:41Z)

I've never installed a custom kernel before, I always used the default kernel the distro was shipped with. I had to read upon it to make sure changing kernels is something I would be able to do. I also had to free up a spare HDD, I can't risk losing my daily drive. I'm still trying to figure out how Grub works because last time I've installed a different distro on a separate hard drive my daily driver failed to boot, I've managed to fix it eventually but I would like to avoid it from happening again. I also have some other things to attend to, I should probably able to get back to you in a day or two, I haven't forgotten about it. My apologies for the delay. 

---

### 评论 #27 — Sersys (2025-03-15T13:57:22Z)

Ok this worked.
`uname -a`
```
Linux sy-lu 6.11.0-19-generic #19~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Feb 17 11:51:52 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```
This is on a separate hard drive, no distrobox, no container, just as is. 
Other info:
`python3 -V`
```
Python 3.12.3
```

`rocminfo`
[rocomubuntu.txt](https://github.com/user-attachments/files/19262538/rocomubuntu.txt)

`pip show torch`
```
pip show torch
Name: torch
Version: 2.8.0.dev20250314+rocm6.3
Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
Home-page: https://pytorch.org/
Author: PyTorch Team
Author-email: packages@pytorch.org
License: BSD-3-Clause
Location: /home/sersys/pyproj/torch/lib/python3.12/site-packages
Requires: filelock, fsspec, jinja2, networkx, pytorch-triton-rocm, setuptools, sympy, typing-extensions
Required-by: kornia, spandrel, torchaudio, torchsde, torchvision
```
Comfy_ui version v0.3.26

I have actually generated my first image.

---

### 评论 #28 — fluidnumericsJoe (2025-03-15T15:00:11Z)

@Sersys - this is fantastic news! I'll drop a comment back on discourse. I'm glad that this resolved the issue. 

---

### 评论 #29 — Sersys (2025-03-15T15:56:31Z)

> [@Sersys](https://github.com/Sersys) - this is fantastic news! I'll drop a comment back on discourse. I'm glad that this resolved the issue.

I don't want to look ungrateful, far from it, I can't thank you enough for the lengths you've gone for me, the reason I haven't closed out the pytorch post is because I thought this experiment was to confirm something and not the final solution.  I take it it's not possible to run rocm on a 6.12 or 6.13 kernel debian then? 

---

### 评论 #30 — fluidnumericsJoe (2025-03-17T14:17:24Z)

@Sersys , that's correct. It appears that you do indeed need to use a supported [Linux distribution and kernel](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-distributions) to use ROCm reliably. I understand it may not be the answer you wanted, but it is the answer.

I suspect that AMD is actively working on support for more recent linux kernels, but as of today this is the answer.

---

### 评论 #31 — tcgu-amd (2025-03-17T14:24:29Z)

> I don't want to look ungrateful, far from it, I can't thank you enough for the lengths you've gone for me, the reason I haven't closed out the pytorch post is because I thought this experiment was to confirm something and not the final solution. I take it it's not possible to run rocm on a 6.12 or 6.13 kernel debian then?

Hi @Sersys to add to @fluidnumerics-joe's answer, when it comes to ROCm support on unrelated Kernel versions, the full solution would be to "support" ROCm on said kernel. If the kernel is going to be supported in the future by ROCm, it should already be a work-in-progress. Either way, once we confirm that the bug is indeed related to kernel support, there is no additional action to take for us. For now, using a supported kernel version is the only viable solution. 

Thanks!

---

### 评论 #32 — Sersys (2025-03-19T11:55:30Z)

Understandable. Thank you for everyone's help. I appreciate you all taking your time for me.

---
