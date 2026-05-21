# [Issue]: RuntimeError: HIP error: an illegal memory access was encountered

> **Issue #5245**
> **状态**: closed
> **创建时间**: 2025-09-03T06:30:42Z
> **更新时间**: 2026-02-26T10:00:08Z
> **关闭时间**: 2026-01-22T20:29:25Z
> **作者**: mihongyu
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5245

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- tcgu-amd

## 描述

### Problem Description

hello everyone. I am using a newly purchased PC with AI MAX+395 and Ubuntu 24.04. When I use rocm6.4, the installation is normal, but when I start using any AI app, it reports an error:

**torch.AcceleratorError:** 
**HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.**

I have studied the discussions in the Git community and it seems that 6.4 cannot support gfx1151, so I followed the discussion and used the development version of rocm7, which is currently available. but at
During use, whether it is inference, model training, or daily use, there will be sudden black screens randomly, which will cause my Ubuntu to log out and return to the interface waiting to enter my account and password.
The following text is the error message:

**RuntimeError: HIP error: an illegal memory access was encountered
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.**
**For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.**

I noticed that there are also many similar discussions in the Git discussion forum. The AI MAX+395 has been sold in the market for a long time, and its main sales content is AI. But now it has been unable to be used stably. ROCM7 is not sure when it will be released, I will use the following link:

**pip install   --index-url  https://d2awnip2yjpvqn.cloudfront.net/v2/gfx1151/    rocm[libraries,devel]**

But this development version is very unstable. I am very worried about becoming an abandoned user, and I want to know how to deal with the current problem? Also, what are AMD's plans? When can it be completely resolved? Can someone tell me?

### Operating System

ubuntu 24.04

### CPU

AI MAX+395

### GPU

AI MAX+395

### ROCm Version

ROCM6.4 and ROCM7 dev

### ROCm Component

_No response_

### Steps to Reproduce

ALL AI app

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (54 条)

### 评论 #1 — tcgu-amd (2025-09-03T17:41:14Z)

Hi @mihongyu, thank you for reaching out, and sorry that you are experiencing issues with ROCm. Yeah, it certainly can be frustrating that official support is still not there -- it is really close, but it really couldn't have come soon enough. 

On the bright side, since rocm is open source, you don't really have to wait for official release. We do have rocm support for gfx1151 (AKA the AI Max + 395/Strix Halo) available for PyTorch right now for testing through [TheRock](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-releases-using-pip) project. You can install the artifacts directly through pip to try it out:

Install ROCm for gfx1151

```
python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  rocm[libraries,devel]
```

Installing PyTorch for gfx1151
```
python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  torch torchaudio torchvision
```

Just make sure you uninstall your current ROCm version first. Please give that a try and let me know if you encounter any issues. 

Thanks!

---

### 评论 #2 — mihongyu (2025-09-04T02:23:07Z)



@tcgu-amd 。
Thank you for your reply. Regarding what you mentioned:

**Install ROCm for gfx1151

python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  rocm[libraries,devel]**

I have been using it for half a month now. I have already mentioned in the content submitted above:

**It is unstable, often causing the machine to restart and reporting errors:**

**RuntimeError: HIP error: an illegal memory access was encountered
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with TORCH_USE_HIP_DSA to enable device-side assertions.**

I fully understand that ROCM is an open-source project and I cannot make too many demands on its progress. But currently it's really frustrating, I have to look for a machine with an N-card to help me complete my work tasks, even though it's obvious that I have an AMD computer with AI MAX+ 395.

Finally, I sincerely hope that ROCM can provide a stable version as soon as possible. At least, I hope to continue working instead of being forced to restart my computer halfway through.

Thank you very much for your efforts in the ROCM project.

---

### 评论 #3 — tcgu-amd (2025-09-04T14:14:25Z)

@mihongyu, oh so you have already been using the test version. Sorry the link was different so I thought that was a third-party wheel (there are a few out there I think). Do you have a workload that I can use to reproduce the `RuntimeError: HIP error: an illegal memory access was encountered` error? Thanks! 

---

### 评论 #4 — mihongyu (2025-09-05T02:56:10Z)

@tcgu-amd  ,
Thank you very much for your reply.
The 'Sorry the link was different' you mentioned, I have checked and indeed the link is different. But this link was also found on the website of AMD/Rocm. I'm not sure when the changes occurred, but based on the actual results, the test versions they provided yielded the same outcome.
Now I am providing steps to reproduce the problem, which may be a bit complicated as they come from third-party applications.
When starting ComfyUI, a core dump was obtained. Please refer to the attached image.
![Image](https://github.com/user-attachments/assets/0ddb4e1d-60b6-4b22-954a-3848bfef9560)

Firstly, use git clone on GitHub to obtain its entire content and install the relevant dependencies according to readme. md. Finally, use Python main. py to launch ComfyUI. You will receive a prompt for core dump. This issue has caused me to be completely unable to use ComfyUI for work. It is worth noting that this core dump is from the test version 20250814. There was no core dump issue before this version. I once submitted this issue in the community, but it did not receive attention. Please refer to the attached content.

![Image](https://github.com/user-attachments/assets/91d3b07c-29b9-4d29-8ca9-e135c7858c5c)

This core dump file exceeds 1GB, so I cannot upload it either. And I don't know how to use GDB to view it.
2. Random memory errors occur during use.
I use DiffSynth Studio for Lora training（ https://github.com/modelscope/DiffSynth-Studio ）Due to frequent memory errors, training cannot be completed.
You can download this DiffSynth Studio and train it using the examples/qwen_image/model_training/lora/Qwen-Imag.sh model. This requires you to download Qwen/Qwen Image and Qwen/Qwen Image Edit in advance and place them in its models directory.

（I understand that using these third-party applications may make it difficult for you to find bugs. But this is also the daily work of ROCM users. ）

During the training process, there are 5 num_ epochs. And generate multiple epoch-x.safetensors (x represents 0-4, num_epochs）。
Usually, it may take several hours to successfully generate the first safetensors. Then, there is a 50% chance of a memory error occurring when generating the second safetensors. There is a 100% chance that all user applications will be killed and the computer will be forcibly restarted during the third safetensors, lost  all work progress.

**Memory access fault by GPU node-1 (Agent handle: 0x139c99a0) on address 0x77600ff76000. Reason: Page not present or supervisor privilege.
HW Exception by GPU node-1 (Agent handle: 0x179d82b0) reason :GPU Hang
Aborted (core dumped)**

This error message comes from yesterday's test version. Prior to this version, error prompts were typically:

**RuntimeError: HIP error: an illegal memory access was encountered
Under Investigation**


The same problem also exists in other AI applications. For example, when I select the engine as ROCM instead of Vulkan in LM studio, LMstudio will immediately crash. So, I don't think it's an application issue.

I fully understand that as an open-source project ROCM, I cannot rush its development progress too much. I also understand that when using third-party applications, the complex environment poses testing difficulties for your team. However, having an advanced AI MAX+395 PC but not being able to use its AI functions properly makes me feel very uncomfortable.
I have tried reinstalling the operating system, reinstalling ROCM, and modifying the VRAM values in BIOS, but the problem still persists.
At present, I can only use the Vulkan engine in lmstudio to generate text, and when training Lora, I pray that it will not crash too early, while other functions can only wait .....

Finally, thank you to your team for their continuous work and dedication on ROCM.


---

### 评论 #5 — tcgu-amd (2025-09-05T14:56:34Z)

@mihongyu Thanks for the detailed instructions!! So a quick update, I was able to reproduce what you are seeing in ComfyUI and the culprit seems to be that pip installed an incompatible torchaudio version. After trying to install the pre release versions from the repo, the issue seems to have gone away. 

To install the pre-release versions, please

1. Uninstall torch torchaudio torch vision
`pip uninstall torch torchvision torchaudio`

2. Install the pre-release versions with 
```
python -m pip install \
  --pre \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  torch torchaudio torchvision
```

Please give this a try and let me know if it works. I will investigate on the issues you are seeing with the other applications in the meantime. 

And apologies again -- this is on us for not clarifying the instructions. 

Thanks! 

---

### 评论 #6 — mihongyu (2025-09-05T16:22:29Z)

@tcgu-amd 
Thank you for your work.
Yes, according to the link you provided, after reinstalling, ComfyUI can be launched and there are no more core dump issues. Thank you very much for your help.

Now, I will conduct another test to see if the issue of memory errors has been improved. As is well known, this may take several hours or a whole day to verify. If there are any results, I will immediately post them here.


---

### 评论 #7 — mihongyu (2025-09-06T01:48:14Z)

@tcgu-amd 

Unfortunately, the memory error still exists. I executed the DiffSynth Studio training code for Lora, and after 5 hours of training, there was a memory error that caused my computer to automatically restart.

---

### 评论 #8 — tcgu-amd (2025-09-06T02:31:57Z)

@mihongyu Thanks for reporting back! Will look into it. 

---

### 评论 #9 — using-cpp (2025-09-06T15:47:33Z)

> [@tcgu-amd](https://github.com/tcgu-amd) , Thank you very much for your reply. The 'Sorry the link was different' you mentioned, I have checked and indeed the link is different. But this link was also found on the website of AMD/Rocm. I'm not sure when the changes occurred, but based on the actual results, the test versions they provided yielded the same outcome. Now I am providing steps to reproduce the problem, which may be a bit complicated as they come from third-party applications. When starting ComfyUI, a core dump was obtained. Please refer to the attached image. ![Image](https://github.com/user-attachments/assets/0ddb4e1d-60b6-4b22-954a-3848bfef9560)
> 
> Firstly, use git clone on GitHub to obtain its entire content and install the relevant dependencies according to readme. md. Finally, use Python main. py to launch ComfyUI. You will receive a prompt for core dump. This issue has caused me to be completely unable to use ComfyUI for work. It is worth noting that this core dump is from the test version 20250814. There was no core dump issue before this version. I once submitted this issue in the community, but it did not receive attention. Please refer to the attached content.
> 
> ![Image](https://github.com/user-attachments/assets/91d3b07c-29b9-4d29-8ca9-e135c7858c5c)
> 
> This core dump file exceeds 1GB, so I cannot upload it either. And I don't know how to use GDB to view it. 2. Random memory errors occur during use. I use DiffSynth Studio for Lora training（ https://github.com/modelscope/DiffSynth-Studio ）Due to frequent memory errors, training cannot be completed. You can download this DiffSynth Studio and train it using the examples/qwen_image/model_training/lora/Qwen-Imag.sh model. This requires you to download Qwen/Qwen Image and Qwen/Qwen Image Edit in advance and place them in its models directory.
> 
> （I understand that using these third-party applications may make it difficult for you to find bugs. But this is also the daily work of ROCM users. ）
> 
> During the training process, there are 5 num_ epochs. And generate multiple epoch-x.safetensors (x represents 0-4, num_epochs）。 Usually, it may take several hours to successfully generate the first safetensors. Then, there is a 50% chance of a memory error occurring when generating the second safetensors. There is a 100% chance that all user applications will be killed and the computer will be forcibly restarted during the third safetensors, lost all work progress.
> 
> **Memory access fault by GPU node-1 (Agent handle: 0x139c99a0) on address 0x77600ff76000. Reason: Page not present or supervisor privilege. HW Exception by GPU node-1 (Agent handle: 0x179d82b0) reason :GPU Hang Aborted (core dumped)**
> 
> This error message comes from yesterday's test version. Prior to this version, error prompts were typically:
> 
> **RuntimeError: HIP error: an illegal memory access was encountered Under Investigation**
> 
> The same problem also exists in other AI applications. For example, when I select the engine as ROCM instead of Vulkan in LM studio, LMstudio will immediately crash. So, I don't think it's an application issue.
> 
> I fully understand that as an open-source project ROCM, I cannot rush its development progress too much. I also understand that when using third-party applications, the complex environment poses testing difficulties for your team. However, having an advanced AI MAX+395 PC but not being able to use its AI functions properly makes me feel very uncomfortable. I have tried reinstalling the operating system, reinstalling ROCM, and modifying the VRAM values in BIOS, but the problem still persists. At present, I can only use the Vulkan engine in lmstudio to generate text, and when training Lora, I pray that it will not crash too early, while other functions can only wait .....
> 
> Finally, thank you to your team for their continuous work and dedication on ROCM.

Use python -X faulthandler ComfyUI/main.py  when pytorch report core dump problem,Causes package dependency conflicts in custom nodes like ComfyUI-Manager.

---

### 评论 #10 — tcgu-amd (2025-09-09T20:10:07Z)

@movecpp Interesting, so you are still seeing core dump even with the pre-release builds? How did you set up your environment?

---

### 评论 #11 — tcgu-amd (2025-09-12T19:06:32Z)

@mihongyu Hi, sorry for the lack of updates -- we are still trying to reproduce the DiffSynth Studio issue, and it is probably going to take a bit longer. In the meantime, can you provide a bit more information about your system? What brand/make is your laptop, and how much ram does it have? Also, would it be possible to capture the system memory state before the crash in any ways? Thanks! 

---

### 评论 #12 — mihongyu (2025-09-13T02:55:13Z)

@tcgu-amd hi, Nice to see your email, thank you for still following up on this issue.
My computer is a mini PC, FEVM FAEX9. It is mainly equipped with AI MAX+395 and LPDDR5 8000M 128 unified memory, with a maximum of 96G VRAM. I think this is also a hardware standard configuration recommended by AMD.
You can learn about my computer environment through the following pictures.

![Image](https://github.com/user-attachments/assets/1dd58f56-426b-49e0-9b7f-1cac26014352)

![Image](https://github.com/user-attachments/assets/7703f679-7ba2-4f28-a771-8750b3faed01)

The following image is my Python 3.12 virtual environment used for training DiffSynth Studio lora.

![Image](https://github.com/user-attachments/assets/6a4d48df-3754-4522-a7ee-865cb4242d5d)

When the problem occurred, all processes were killed and the current user was forcibly logged out. Therefore, it is difficult to capture the system state at that moment. However, throughout the entire process, I often paid attention to the usage of memory, and by using top and rocm smi to check, there was no occurrence of memory exceeding. Usually, the memory usage is around 50%. I use the 32/96 memory allocation mode. The system memory during training is shown in the following figure:

![Image](https://github.com/user-attachments/assets/3d151ff6-0fe9-4ae2-8933-4e09ab26e8b0)

Now, I will try to save the system memory state in a text file every 1 second during training to see if I can capture the memory state at the moment of the problem. This may take several more hours, and once there are results, I will submit them here.



---

### 评论 #13 — mihongyu (2025-09-13T03:01:25Z)

@tcgu-amd Sorry, the image above shows the 64/64 memory allocation mode, but the result is the same as 32/96.

---

### 评论 #14 — alshdavid (2025-09-19T00:13:40Z)

Also experiencing this on my 9070xt with ROCm 7.0 https://github.com/ROCm/ROCm/issues/4846#issuecomment-3310053766

---

### 评论 #15 — mihongyu (2025-10-01T07:45:38Z)

@tcgu-amd hi, I'm here again:)
I noticed that ROCM7 has been released, but pytorch is still only 6.4. So I am still using the following address:
pip install   --index-url  https://rocm.nightlies.amd.com/v2/gfx1151/    torch torchaudio torchvision pytorch-triton-rocm numpy
The torchauudio used in this URL still causes COMfyUI to fail to start. Did you forget to fix this issue with the version at this URL?

---

### 评论 #16 — mihongyu (2025-10-04T06:45:13Z)

Traceback (most recent call last):
  File "/home/mewmhy/AI/ComfyUI/nodes.py", line 2129, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/mewmhy/AI/ComfyUI/comfy_extras/nodes_audio_encoder.py", line 2, in <module>
    import comfy.audio_encoders.audio_encoders
  File "/home/mewmhy/AI/ComfyUI/comfy/audio_encoders/audio_encoders.py", line 6, in <module>
    import torchaudio
  File "/home/mewmhy/miniconda3/envs/dayilytest/lib/python3.12/site-packages/torchaudio/__init__.py", line 7, in <module>
    from . import _extension  # noqa  # usort: skip
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mewmhy/miniconda3/envs/dayilytest/lib/python3.12/site-packages/torchaudio/_extension/__init__.py", line 37, in <module>
    _load_lib("libtorchaudio")
  File "/home/mewmhy/miniconda3/envs/dayilytest/lib/python3.12/site-packages/torchaudio/_extension/utils.py", line 58, in _load_lib
    torch.ops.load_library(path)
  File "/home/mewmhy/miniconda3/envs/dayilytest/lib/python3.12/site-packages/torch/_ops.py", line 1392, in load_library
    ctypes.CDLL(path)
  File "/home/mewmhy/miniconda3/envs/dayilytest/lib/python3.12/ctypes/__init__.py", line 379, in __init__
    self._handle = _dlopen(self._name, mode)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^
**OSError: /home/mewmhy/miniconda3/envs/dayilytest/lib/python3.12/site-packages/torchaudio/lib/libtorchaudio.so: undefined symbol: _ZNK3c106SymInt22maybe_as_int_slow_pathEv**


---

### 评论 #17 — tcgu-amd (2025-10-14T14:01:09Z)

Hi @mihongyu, sorry for the late reply... To answer your question, no I don't think rocm 7.0 explicitly fixed the memory issue. However, the error log you linked seems like an issue with installation. Have you tried to install both ROCm and python following the link? Or did you only install the python wheel?


---

### 评论 #18 — tcgu-amd (2025-10-14T14:04:49Z)

> Also experiencing this on my 9070xt with ROCm 7.0 [#4846 (comment)](https://github.com/ROCm/ROCm/issues/4846#issuecomment-3310053766)

Hi @alshdavid, not sure your issue is the same as the one mentioned in this ticket, but unfortunately winograd and CK support for gfx1201 was not able to make into the rocm 7.0 release. I know it is frustrating -- but it should be available in one of the upcoming minor releases.

---

### 评论 #19 — mihongyu (2025-10-14T16:27:00Z)

> Hi [@mihongyu](https://github.com/mihongyu), sorry for the late reply... To answer your question, no I don't think rocm 7.0 explicitly fixed the memory issue. However, the error log you linked seems like an issue with installation. Have you tried to install both ROCm and python following the link? Or did you only install the python wheel?


 The latest version can now run normally. So the issue of 'undefined symbol: _ZNK3c106SymInt22maybe_as_int_stlow_ pathEv' no longer exists.
I am still researching the issue of training Lora. Recent attempts have made me realize that this memory issue seems to be caused by the resource file being too large. For example, using images with a resolution exceeding 1024 during training can greatly increase the probability of memory errors. I am not sure if there is a problem with the training script or if there is a problem with the rocm when dealing with large memory. I am continuing to work hard on testing





---

### 评论 #20 — muhammadn (2025-10-16T18:25:33Z)

@tcgu-amd 

My hardware is an AMD R9700 AI Pro 32GB (gfx1201)

This is working for me as well with ComfyUI and the new Ovi T2AV (Text to Audio/Video)/I2AV (Image to AV) using the 'The Rocks" nightly on my docker container using ROCm 7.0.2 (stable). Is it possible that we can have a stable release instead of nightly because of hit and miss of getting a broken build?

All official from Pytorch's pytorch/vision/audio libraries for ROCm are having this error even with `export PYTORCH_NO_HIP_MEMORY_CACHING=1` with and error saying `HIP out of memory` or OOM, no matter if it's official pytorch stable (2.9.0) or Preview (2.10). So now ironically i might avoid official builds from pytorch.

---

### 评论 #21 — tcgu-amd (2025-10-16T19:05:34Z)

> [@tcgu-amd](https://github.com/tcgu-amd)
> 
> My hardware is an AMD R9700 AI Pro 32GB (gfx1201)
> 
> This is working for me as well with ComfyUI and the new Ovi T2AV (Text to Audio/Video)/I2AV (Image to AV) using the 'The Rocks" nightly on my docker container using ROCm 7.0.2 (stable). Is it possible that we can have a stable release instead of nightly because of hit and miss of getting a broken build?
> 
> All official from Pytorch's pytorch/vision/audio libraries for ROCm are having this error even with `export PYTORCH_NO_HIP_MEMORY_CACHING=1` with and error saying `HIP out of memory` or OOM, no matter if it's official pytorch stable (2.9.0) or Preview (2.10). So now ironically i might avoid official builds from pytorch.

Hi @muhammadn, I am glad you were able to find a working version. TheRock, being ROCm's build system, will always contain the latest changes from ROCm dev branches. We work our best to push the changes to stable releases, but the cadence of "official" release is slower and takes time to catch up. Let me know if the next release is still broken, and I will elevate the issue. Thanks! 

---

### 评论 #22 — muhammadn (2025-10-16T19:54:13Z)

Just to note if someone comes across here, i don't think ROCm is broken. I think it's the official pytorch is broken with OOM errors.

I had tried ROCm 6.4.4 + official pytorch 2.8.0 and 2.9.0, OOM.
Also tried ROCm 7.0.2 + official pytorch preview 2.10 daily builds, also OOM.

So after using TheRocks and it only installs AMD's fork of pytorch + rocm python libraries, everything like the above mentioned worked well.

---

### 评论 #23 — alshdavid (2025-10-16T21:04:26Z)

> Just to note if someone comes across here, i don't think ROCm is broken. I think it's the official pytorch is broken with OOM errors.
> 
> I had tried ROCm 6.4.4 + official pytorch 2.8.0 and 2.9.0, OOM. Also tried ROCm 7.0.2 + official pytorch preview 2.10 daily builds, also OOM.
> 
> So after using TheRocks and it only installs AMD's fork of pytorch + rocm python libraries, everything like the above mentioned worked well.

Can I ask, how do you install Pytorch from TheRock?

Python package management is a bit of a mystery to me, I am using:

```bash
python -m pip install torch torchvision torchaudio --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all
```

If I understand correctly, this installs the torch version from the supplied index URL (which I believe is the one I should be using).

I am getting this HIP error constantly and my local environment is virtually unusable.

Should I use `--pre`? When I do, it appears to install an older version (judging by the Pytorch semver printed in stdout)

---

### 评论 #24 — muhammadn (2025-10-16T21:30:16Z)

@alshdavid yes pre. also your ROCm should be 7.0.2 from the usual https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html

Also add a flag when you try to install with pip with `--force-reinstall` to force replace the torch libraries.

---

### 评论 #25 — alshdavid (2025-10-16T22:14:28Z)

> Also add a flag when you try to install with pip with --force-reinstall to force replace the torch libraries.

If I am using something like ComfyUI, do I need to consider the order of installation?

```bash
cd ComfyUI
python -m pip install -r ./requirements.txt
python -m pip install --force-reinstall --pre torch torchvision torchaudio --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all
```
Or is this okay?
```bash
python -m pip install --force-reinstall --pre torch torchvision torchaudio --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all

cd ComfyUI
python -m pip install -r ./requirements.txt
```

---

### 评论 #26 — muhammadn (2025-10-16T22:27:35Z)

@alshdavid  The second is  correct.

---

### 评论 #27 — mikealanni (2025-10-20T14:11:14Z)

Have same issue in Comfyu, Rocm is not stable on GMK evo x2, used ROCM 6.3, 6.4, 6.4.4 7 AND 7.1 all keep getting issues, on Ubuntu 24.04, 25.04 and even 25.10. I think just not ready yet. I will wait for stable version as I gave up.

---

### 评论 #28 — tcgu-amd (2025-10-21T14:15:48Z)

Hi everyone, thanks for your patience! Just wanted to update that we have been actively working on investigating this issue. Thanks!

---

### 评论 #29 — nvdg (2025-10-31T19:18:26Z)

Still present in Rocm 7.1, it even seems to have gotten worse, it used to just give an error but now it crashes my entire system.

---

### 评论 #30 — mikealanni (2025-11-02T15:51:13Z)

I feel this error it's like a medication you need to see it every 6 hours or so 😅

---

### 评论 #31 — tcgu-amd (2025-11-04T15:34:22Z)

Just a quick update, the issue is still being worked on. Thank you all for your patience...

---

### 评论 #32 — peter247 (2025-11-07T11:21:51Z)

Stupid question , are the  https://rocm.nightlies.amd.com/v2/****** , for both Linux and windows ?
With some workflows I'm in a no win , I can't run in window without getting a sage attention not installed error  , or in linux I get a illegal memory error all the time.
The windows computer having a NVidia card and the Linux computer being a ai max 395+ on ubuntu .

---

### 评论 #33 — using-cpp (2025-11-08T02:20:45Z)

> [@movecpp](https://github.com/movecpp) Interesting, so you are still seeing core dump even with the pre-release builds? How did you set up your environment?

the following content is my comfyui startup shell,when i use --use-flash-attention parameter,some times linux kernel will throw driver problem even though i installed https://rocm.nightlies.amd.com/v2/ latest version
PYTORCH_TRITON_DISABLE_AUTOTUNE=1 TRITON_ALLOW_NON_CONSTEXPR_GLOBALS=1 AMD_SERIALIZE_KERNEL=3 TORCH_USE_HIP_DSA=1 TRITON_MAX_TENSOR_NUMEL=1073741824 TRITON_MAX_BLOCK_SIZE=512 PYTORCH_TRITON_DISABLE_FP8=1 FLASH_ATTENTION_USE_CK=FALSE FLASH_ATTENTION_TRITON_AMD_ENABLE=TRUE MIOPEN_FIND_MODE=2 PYTORCH_TUNABLEOP_ENABLED=1 MIGRAPHX_MLIR_USE_SPECIFIC_OPS="attention" TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 PYTORCH_ALLOC_CONF=expandable_segments:True TRITON_HIP_LLD_PATH=/home/const/miniconda3/envs/rocm/lib/python3.13/site-packages/_rocm_sdk_core/lib/llvm/bin/ld.lld python -X falthandler ComfyUI/main.py --listen 0.0.0.0 --port 8000  --disable-mmap --async-offload --disable-smart-memory --force-non-blocking --use-flash-attention --cache-classic --gpu-only --supports-fp8-compute --fp16-vae

---

### 评论 #34 — muhammadn (2025-11-08T02:23:02Z)

i always keep the working version which is on 16th last month.

never upgraded since because it works.

On Sat, 8 Nov 2025 at 10:21 AM, movecpp ***@***.***> wrote:

> *movecpp* left a comment (ROCm/ROCm#5245)
> <https://github.com/ROCm/ROCm/issues/5245#issuecomment-3505619679>
>
> @movecpp <https://github.com/movecpp> Interesting, so you are still
> seeing core dump even with the pre-release builds? How did you set up your
> environment?
>
> the following content is my comfyui startup shell,when i use
> --use-flash-attention parameter,some times linux kernel will throw driver
> problem even though i installed https://rocm.nightlies.amd.com/v2/ latest
> version
> PYTORCH_TRITON_DISABLE_AUTOTUNE=1 TRITON_ALLOW_NON_CONSTEXPR_GLOBALS=1
> AMD_SERIALIZE_KERNEL=3 TORCH_USE_HIP_DSA=1
> TRITON_MAX_TENSOR_NUMEL=1073741824 TRITON_MAX_BLOCK_SIZE=512
> PYTORCH_TRITON_DISABLE_FP8=1 FLASH_ATTENTION_USE_CK=FALSE
> FLASH_ATTENTION_TRITON_AMD_ENABLE=TRUE MIOPEN_FIND_MODE=2
> PYTORCH_TUNABLEOP_ENABLED=1 MIGRAPHX_MLIR_USE_SPECIFIC_OPS="attention"
> TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
> PYTORCH_ALLOC_CONF=expandable_segments:True
> TRITON_HIP_LLD_PATH=/home/const/miniconda3/envs/rocm/lib/python3.13/site-packages/_rocm_sdk_core/lib/llvm/bin/ld.lld
> python -X falthandler ComfyUI/main.py --listen 0.0.0.0 --port 8000
> --disable-mmap --async-offload --disable-smart-memory --force-non-blocking
> --use-flash-attention --cache-classic --gpu-only --supports-fp8-compute
> --fp16-vae
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5245#issuecomment-3505619679>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AAZRZ472ZB5SLXAH5G5EZS333VHRJAVCNFSM6AAAAACFPPOMYWVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTKMBVGYYTSNRXHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #35 — mikealanni (2025-11-08T02:30:17Z)

For some reason this 
amdgpu.mcbp=0 amdgpu.cwsr_enable=0 amdgpu.queue_preemption_timeout_ms=1

Prevent my GMK evo x2 90% of crashes 

---

### 评论 #36 — using-cpp (2025-11-08T02:36:45Z)

> Stupid question , are the https://rocm.nightlies.amd.com/v2/****** , for both Linux and windows ? With some workflows I'm in a no win , I can't run in window without getting a sage attention not installed error , or in linux I get a illegal memory error all the time. The windows computer having a NVidia card and the Linux computer being a ai max 395+ on ubuntu .

you were running rocm on a NVIDIA Graphics Card? how did you do that? lol,any way,you should install sage-attention whl version because it takes many of RAM to compile

---

### 评论 #37 — peter247 (2025-11-08T09:47:15Z)

> you were running rocm on a NVIDIA Graphics Card? how did you do that? lol,any way,you should install sage-attention whl version because it takes many of RAM to compile

No, the windows machine ( laptop ) with a Nvidia card is running just the stock exe , The other computer is a Minisforum MS-S1 MAX which I've tried windows and ubuntu + proxmox .
I've tried to installing sage-attention but just get a new set of errors , missing this or that or error compile with this setting .
BACK TO MY STUPID QUESTION , is the nighties windows and Linux ? 

---

### 评论 #38 — alshdavid (2025-11-08T19:04:05Z)

> BACK TO MY STUPID QUESTION , is the nighties windows and Linux ? 

Yes

---

### 评论 #39 — tcgu-amd (2025-11-10T14:47:03Z)

> > you were running rocm on a NVIDIA Graphics Card? how did you do that? lol,any way,you should install sage-attention whl version because it takes many of RAM to compile
> 
> No, the windows machine ( laptop ) with a Nvidia card is running just the stock exe , The other computer is a Minisforum MS-S1 MAX which I've tried windows and ubuntu + proxmox . I've tried to installing sage-attention but just get a new set of errors , missing this or that or error compile with this setting . BACK TO MY STUPID QUESTION , is the nighties windows and Linux ?

Hi @peter247, yes we do build for both Windows and Linux, and they are released in the index you linked. However ROCm on Windows/Linux are different builds with different supported subset of features. You can check out here for the major differences https://github.com/ROCm/TheRock/blob/main/docs/development/windows_support.md. Even among "supported" components there's will be subtle differences. Differences for the Pytorch releases are less drastic but they are still different builds. 

---

### 评论 #40 — using-cpp (2025-11-12T09:13:02Z)

> > you were running rocm on a NVIDIA Graphics Card? how did you do that? lol,any way,you should install sage-attention whl version because it takes many of RAM to compile
> 
> No, the windows machine ( laptop ) with a Nvidia card is running just the stock exe , The other computer is a Minisforum MS-S1 MAX which I've tried windows and ubuntu + proxmox . I've tried to installing sage-attention but just get a new set of errors , missing this or that or error compile with this setting . BACK TO MY STUPID QUESTION , is the nighties windows and Linux ?

yes,i have a AI MAX+ 395 machine but not running on windows,this link[https://huggingface.co/Kijai/PrecompiledWheels] will help you

---

### 评论 #41 — peter247 (2025-11-18T14:10:47Z)

Anything changed ? , is the Linux version of comfyui stable ? , I've been using Windows and not had 1 problem with ROCm nighty's , but on Linux it was unstable , But that could have been my fault , because I was install the driver from https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb , then installing ROCm nighty's in the virtual environment .  


---

### 评论 #42 — tcgu-amd (2025-11-18T15:15:09Z)

> Anything changed ? , is the Linux version of comfyui stable ? , I've been using Windows and not had 1 problem with ROCm nighty's , but on Linux it was unstable , But that could have been my fault , because I was install the driver from https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb , then installing ROCm nighty's in the virtual environment .

Hi @peter247, we have a patch for this issue but it has yet to make to public releases. You can check out this issue for some potential workarounds https://github.com/ROCm/TheRock/issues/1795. Otherwise, the issue seem to originate from hipblaslt so you can either disable it (use rocblas instead), or revert to pytorch version < 2.7.0 / rocm < 6.4.0. 

---

### 评论 #43 — tcgu-amd (2025-11-24T20:57:34Z)

Hi all, just an update, the fix is **not** going to be available with ROCm 7.1.1 release. We are currently looking at ROCm 7.2, although this is subject to change as well. Thanks! 

---

### 评论 #44 — void95 (2026-01-10T21:35:22Z)

Is there any possible fix for Windows 11 // Im running the latest nightlies, but also always running into hip errors after some gens. 

Or do i just have to wait till 7.2? Thanks in Advance 

Im using a 9070XT 

---

### 评论 #45 — rafavcc (2026-01-21T01:28:25Z)

Any new on ROCM 7.2? Launch date?

---

### 评论 #46 — tcgu-amd (2026-01-22T20:20:16Z)

Hi everyone, ROCm 7.2 is now live and it includes the fix for this issue. Thanks! 

---

### 评论 #47 — nvdg (2026-01-22T20:21:59Z)

YEAH! I've been testing it all night and had 0 memory errors! 🙌 

---

### 评论 #48 — tcgu-amd (2026-01-22T20:29:25Z)

I will be closing this issue then, please feel free to ping me if anyone still observe memory issues in 7.2 or have any other questions. Thanks! 

---

### 评论 #49 — pkrasicki (2026-02-15T03:57:29Z)

Initially nothing improved for me when I installed PyTorch with ROCm 7.2, but then I noticed that I still had one other Triton package installed, called `triton-rocm`. I had to remove it and now I'm not getting this error anymore. Thank you for fixing it!

---

### 评论 #50 — pkrasicki (2026-02-15T22:51:57Z)

Never mind, it happened again today. I'm using those packages:
```
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torch-2.9.1%2Brocm7.2.0.lw.git7e1940d4-cp313-cp313-linux_x86_64.whl
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchvision-0.24.0%2Brocm7.2.0.gitb919bd0c-cp313-cp313-linux_x86_64.whl
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/triton-3.5.1%2Brocm7.2.0.gita272dfa8-cp313-cp313-linux_x86_64.whl
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchaudio-2.9.0%2Brocm7.2.0.gite3c6ee2b-cp313-cp313-linux_x86_64.whl
```

Partial ComfyUI log:
```
$ HSA_OVERRIDE_GFX_VERSION=10.3.0 FLASH_ATTENTION_TRITON_AMD_ENABLE=TRUE python main.py

[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** Platform: Linux
** Python version: 3.13.5 (main, Jun 25 2025, 18:55:22) [GCC 14.2.0]
** Python executable: /mnt/AI/ComfyUI/env/bin/python
** ComfyUI Path: /mnt/AI/ComfyUI
** ComfyUI Base Folder Path: /mnt/AI/ComfyUI
** User directory: /mnt/AI/ComfyUI/user
** ComfyUI-Manager config path: /mnt/AI/ComfyUI/user/__manager/config.ini
** Log path: /mnt/AI/ComfyUI/user/comfyui.log

Checkpoint files will always be loaded safely.
Found comfy_kitchen backend eager: {'available': True, 'disabled': False, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Found comfy_kitchen backend triton: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Found comfy_kitchen backend cuda: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Total VRAM 12272 MB, total RAM 28026 MB
pytorch version: 2.9.1+rocm7.2.0.git7e1940d4
AMD arch: gfx1030
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 6700 XT : native
Using async weight offloading with 2 streams
Enabled pinned memory 26624.0
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
Python version: 3.13.5 (main, Jun 25 2025, 18:55:22) [GCC 14.2.0]
ComfyUI version: 0.13.0
ComfyUI frontend version: 1.38.13

(...)

Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
Requested to load WAN21
0 models unloaded.
loaded partially; 4691.20 MB usable, 4580.45 MB loaded, 4756.74 MB offloaded, 161.55 MB buffer reserved, lowvram patches: 0
  0%|                                                                             | 0/3 [00:00<?, ?it/s]got prompt
100%|████████████████████████████████████████████████████████████████████| 3/3 [12:56<00:00, 258.91s/it]
Requested to load WAN21
0 models unloaded.
loaded partially; 4695.20 MB usable, 4580.45 MB loaded, 4756.74 MB offloaded, 161.55 MB buffer reserved, lowvram patches: 0
100%|████████████████████████████████████████████████████████████████████| 3/3 [12:35<00:00, 251.85s/it]
Requested to load WanVAE
Unloaded partially: 328.28 MB freed, 4252.17 MB remains loaded, 161.55 MB buffer reserved, lowvram patches: 16
loaded completely; 3037.77 MB usable, 242.03 MB loaded, full load: True
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Prompt executed in 00:33:04
Requested to load WanTEModel
Unloaded partially: 955.96 MB freed, 3296.21 MB remains loaded, 161.55 MB buffer reserved, lowvram patches: 16
loaded completely; 7088.81 MB usable, 6419.48 MB loaded, full load: True
!!! Exception during processing !!! HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

Traceback (most recent call last):
  File "/mnt/AI/ComfyUI/execution.py", line 530, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/execution.py", line 334, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/custom_nodes/ComfyUI-Lora-Manager/py/metadata_collector/metadata_hook.py", line 168, in async_map_node_over_list_with_metadata
    results = await original_map_node_over_list(
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
    )
    ^
  File "/mnt/AI/ComfyUI/execution.py", line 308, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/mnt/AI/ComfyUI/execution.py", line 296, in process_inputs
    result = f(**inputs)
  File "/mnt/AI/ComfyUI/comfy_api/internal/__init__.py", line 149, in wrapped_func
    return method(locked_class, **inputs)
  File "/mnt/AI/ComfyUI/comfy_api/latest/_io.py", line 1710, in EXECUTE_NORMALIZED
    to_return = cls.execute(*args, **kwargs)
  File "/mnt/AI/ComfyUI/custom_nodes/ComfyUI-PainterI2Vadvanced/nodes.py", line 59, in execute
    concat_latent_image = vae.encode(image[:, :, :, :3])
  File "/mnt/AI/ComfyUI/comfy/sd.py", line 1007, in encode
    model_management.load_models_gpu([self.patcher], memory_required=memory_used, force_full_load=self.disable_offload)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 716, in load_models_gpu
    free_memory(total_memory_required[device] * 1.1 + extra_mem, device, for_dynamic=free_for_dynamic, ram_required=total_ram_required[device])
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 635, in free_memory
    if memory_to_free > 0 and current_loaded_models[i].model_unload(memory_to_free):
                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 551, in model_unload
    self.model.detach(unpatch_weights)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_patcher.py", line 1021, in detach
    self.unpatch_model(self.offload_device, unpatch_weights=unpatch_all)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/custom_nodes/ComfyUI-GGUF/nodes.py", line 78, in unpatch_model
    return super().unpatch_model(device_to=device_to, unpatch_weights=unpatch_weights)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_patcher.py", line 886, in unpatch_model
    self.model.to(device_to)
    ~~~~~~~~~~~~~^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1371, in to
    return self._apply(convert)
           ~~~~~~~~~~~^^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  [Previous line repeated 2 more times]
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 957, in _apply
    param_applied = fn(param)
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1357, in convert
    return t.to(
           ~~~~^
        device,
        ^^^^^^^
        dtype if t.is_floating_point() or t.is_complex() else None,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        non_blocking,
        ^^^^^^^^^^^^^
    )
    ^
  File "/mnt/AI/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 58, in to
    new = super().to(*args, **kwargs)
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_tensor.py", line 1654, in __torch_function__
    ret = func(*args, **kwargs)
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


Prompt executed in 23.73 seconds
Exception in thread Thread-2 (prompt_worker):
Traceback (most recent call last):
  File "/usr/lib/python3.13/threading.py", line 1043, in _bootstrap_inner
    self.run()
    ~~~~~~~~^^
  File "/usr/lib/python3.13/threading.py", line 994, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/main.py", line 302, in prompt_worker
    comfy.model_management.soft_empty_cache()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 1702, in soft_empty_cache
    torch.cuda.synchronize()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/__init__.py", line 1082, in synchronize
    with torch.cuda.device(device):
         ~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/__init__.py", line 529, in __init__
    self.idx = _get_device_index(device, optional=True)
               ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/_utils.py", line 373, in _get_device_index
    return _torch_get_device_index(device, optional, allow_cpu)
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 870, in _get_device_index
    device_idx = _get_current_device_index()
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 807, in _get_current_device_index
    return _get_device_attr(lambda m: m.current_device())
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 792, in _get_device_attr
    return get_member(torch.cuda)
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 807, in <lambda>
    return _get_device_attr(lambda m: m.current_device())
                                      ~~~~~~~~~~~~~~~~^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/__init__.py", line 1070, in current_device
    return torch._C._cuda_getDevice()
           ~~~~~~~~~~~~~~~~~~~~~~~~^^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

---

### 评论 #51 — tcgu-amd (2026-02-19T19:34:57Z)

Hi @pkrasicki, this doesn't quite look like the original issue.  Looks like you are forcing gfx1030 with HSA_OVERRIDE_GFX_VERSION=10.3.0. Can you try removing it and see if the error persists? 

---

### 评论 #52 — pkrasicki (2026-02-21T02:24:40Z)

Hi, what's different about it? I might have misunderstood something, but to me it looks similar to this log: https://github.com/ROCm/ROCm/issues/5742. And I think it also started happening after I switched to ROCm 7. Aren't all those issues related?

Without the override variable, ComfyUI crashes on start (Segmentation fault). My GPU, RX 6700 XT (gfx1031) has never been officially supported by ROCm for some reason. The only way to make it work is by using this variable.

---

### 评论 #53 — tcgu-amd (2026-02-25T16:22:23Z)

> Hi, what's different about it? I might have misunderstood something, but to me it looks similar to this log: [#5742](https://github.com/ROCm/ROCm/issues/5742). And I think it also started happening after I switched to ROCm 7. Aren't all those issues related?
> 
> Without the override variable, ComfyUI crashes on start (Segmentation fault). My GPU, RX 6700 XT (gfx1031) has never been officially supported by ROCm for some reason. The only way to make it work is by using this variable.

Thanks for the follow up @pkrasicki! Illegal memory access issues may all look similar, but they can cover quite a wide range of issues/bugs. One of the most common causes is using HSA_OVERRIDE_GFX_VERSION, with a lot of cases in the past. That environment variable works on a very simple principle: it tells HSA to ignore all errors/warning due to incompatibility and just run the binaries compiled for the specified GFX version. This *can* work, if the architectures are similar enough, such as in the case of gfx1030 and gfx1031, but crashes are still expected when using it -- these are different architectures after all. Illegal memory access is just one of the possible crashes. 

At the very least, if amdgpu.cwsr_enable=0 does not work for your case, then you are experiencing a different issue from this one. Please feel free to open another issue and we can take a look at it, although there's might not be a lot that can be done since gfx1030 is not supported....

---

### 评论 #54 — pkrasicki (2026-02-26T10:00:07Z)

@tcgu-amd Thank you for explaining! I created a separate issue: https://github.com/ROCm/ROCm/issues/6003.

I haven't tried setting that kernel parameter, because I don't understand what the tradeoff is or what it does. I haven't seen any official documentation about it.

It's kind of crazy to hear that this card isn't supported, because I've used it in ROCm for years (and so have other people). The random crashes can be very annoying sometimes, but other than that it works fine in ComfyUI, Llama.cpp and Blender (I can't remember if those other programs have the same crashes that I get in ComfyUI or not).

---
