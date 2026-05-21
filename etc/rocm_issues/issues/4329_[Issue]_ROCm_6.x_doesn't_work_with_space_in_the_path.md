# [Issue]: ROCm 6.x doesn't work with space in the path

> **Issue #4329**
> **状态**: closed
> **创建时间**: 2025-02-02T17:52:37Z
> **更新时间**: 2025-07-07T14:06:04Z
> **关闭时间**: 2025-07-04T13:37:08Z
> **作者**: pkrasicki
> **标签**: Under Investigation, RX 6700 XT, ROCm 6.2
> **URL**: https://github.com/ROCm/ROCm/issues/4329

## 标签

- **Under Investigation** (颜色: #0052cc)
- **RX 6700 XT** (颜色: #ededed)
- **ROCm 6.2** (颜色: #ededed)

## 描述

### Problem Description

I'm trying to use ROCm with ComfyUI and RX 6700 XT (gfx1031) on Debian 13. It works fine when I use ROCm 5.7 (pytorch 2.3.1+rocm5.7 with HSA_OVERRIDE_GFX_VERSION=10.3.0), but I can't any newer version to work. I get this error when running ROCm 6.2 (pytorch 2.5.1+rocm6.2):

```
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

Is there any way to make it work or am I stuck with ROCm 5.7? I've also tried running Ollama and the error is a bit different there:
```
ROCm error: no kernel image is available for execution on the device
```

### Operating System

Debian 13

### CPU

-

### GPU

RX 6700 XT

### ROCm Version

ROCm 6.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (24 条)

### 评论 #1 — ppanchad-amd (2025-02-03T15:13:40Z)

Hi @pkrasicki. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — zichguan-amd (2025-02-03T21:34:36Z)

Hi @pkrasicki, can you provide a full log with `AMD_LOG_LEVEL=4`?

---

### 评论 #3 — pkrasicki (2025-02-04T12:18:20Z)

Hi @zichguan-amd, I'm attaching full log files for ComfyUI and Ollama 0.5.7. Both executed with `AMD_LOG_LEVEL=4` and `HSA_OVERRIDE_GFX_VERSION=10.3.0`.

I'm not sure which exact version of ROCm is used by Ollama, but it comes with library files named `libamdhip64.so.6` and `libamdhip64.so.6.1.60102`, so I assume it's using version 6.x.

[comfyui_log.txt](https://github.com/user-attachments/files/18656851/comfyui_log.txt)

[ollama_log.txt](https://github.com/user-attachments/files/18656859/ollama_log.txt)

---

### 评论 #4 — zichguan-amd (2025-02-05T20:18:11Z)

Based on the logs, `HSA_OVERRIDE_GFX_VERSION=10.3.0` seems to be working correctly but the kernel launch is not finding the right binaries. 
Ollama 0.5.7 packages prebuilt libraries and runtime on version 6.1.2, which should run regardless of your ROCm installation. I think your ROCm installation might be broken. Can you test Ollama without ROCm installed at all? and test Comfyui in a docker image like https://hub.docker.com/r/rocm/dev-ubuntu-22.04/tags or https://hub.docker.com/layers/rocm/pytorch/rocm6.3_ubuntu24.04_py3.12_pytorch_release_2.4.0/images/sha256-98ddf20333bd01ff749b8092b1190ee369a75d3b8c71c2fac80ffdcb1a98d529?context=explore? You can follow the steps at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html for running PyTorch on docker.

To make sure ROCm is working as expected, you can also try running one of the [rocm-examples](https://github.com/ROCm/rocm-examples/tree/develop/HIP-Basic) like matrix_multiplication, hello_world, or saxpy.

Also, Debian 13 is not officially supported, please consider using one of the supported OS listed here: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

---

### 评论 #5 — pkrasicki (2025-02-06T20:16:29Z)

I've tried with a Debian 12.9 live ISO, but I get the exact same errors in Ollama and ComfyUI. Could this be because I'm using the default driver that comes with Debian? It works fine with ROCm 5.7 on Debian 12 and 13, but maybe it just doesn't work with ROCm 6?

---

### 评论 #6 — zichguan-amd (2025-02-06T20:31:56Z)

I'll try to repro it on a Debian 12.9 live ISO. Do you get the same error with the docker images?

---

### 评论 #7 — kaiusdepaula (2025-02-08T17:00:29Z)

I'm facing similar issues running Rocm on Arch and found out some interesting stuff.

Running it all on this machine:
`
uname -rmo
`
6.13.1-arch1-1 x86_64 GNU/Linux

Also on a RX 6700XT.

rocminfo return on the [gist](https://gist.github.com/kaiusdepaula/c6de7beb99ca9484c2432317818592af).

Here is where the fun stuff begins:
Installing pytorch as a system package (current system python is 3.13) via 
`
pacman -S python-pytorch-rocm
`

And testing it with:
`
python -c "import torch;print(torch.cuda.is_available())"
`
`True`

Running this:
`
python3 -c "import torch; a=torch.randn(3).to('cuda'); print(a)"
`
Runs smoothly, returning `tensor([ 1.0629, -1.4417,  1.6198], device='cuda:0')`

I also configured user to video and render groups correctly.

The issue is that, trying to replicate the same results in a .venv, in any version of python on any version of pytorch, the following happens (I'm using uv to manage python installations and requirements):

```
.venv/bin/activate
python -c "import torch;print(torch.cuda.is_available())"
```
`True`

Running this:
`
HSA_OVERRIDE_GFX_VERSION=10.3.0 python3 -c "import torch; a=torch.randn(3).to('cuda'); print(a)"
`
Returns the same error as the issue.

```
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

But here is the catch: if I run it with `sudo`, inside the venv, with pytorch 2.6.0+rocm6.2.4:
`sudo HSA_OVERRIDE_GFX_VERSION=10.3.0 python3 -c "import torch; a=torch.randn(3).to('cuda'); print(a)"`
returns `tensor([ 0.6746,  0.8812, -2.0647], device='cuda:0')`

I have no clue why this happens but I can say for sure that It began happening a while ago, as I have a ongoing project using pytorch and my system started giving this error since a system update.

[Edit]
Tried running  `chmod 777 -R project_folder/`  and running the same command as before, and the issue persists.
Also tried `chown $USER:$USER ~/opt/rocm` but nothing changed.

I'm starting to believe that being inside my `home partition`, the python interpreter can't seem to locate the `root partition`. So when a .venv is created with a copy of my system python, even tough is the same interpreter, the fact I'm running outside of root (as system python is in /usr/bin/python) makes the /opt folder unreachable.

Just tried out moving the project inside my root partition, in the opt folder. Created a .venv locally, so the output of:
`which python`
is `/opt/myproject/.venv/bin/python`
And the same error keeps occuring, and running with sudo seems to be the only option.

I'm out of ideas.

[Edit 2]
Makes sense that running with sudo works, as the default intepreter will be called. I tried activating the venv with a sudo terminal, by running `sudo su`. The error persists. 

Tried downgrading my lts kernel to 6.6.72, and nothing changed.

[Edit 3]
Experimented with rocm/pytorch latest build image and the error persists.



---

### 评论 #8 — pkrasicki (2025-02-10T18:48:57Z)

@zichguan-amd I've tried this image [dev-ubuntu-22.04:6.2-complete](https://hub.docker.com/layers/rocm/dev-ubuntu-22.04/6.2-complete/images/sha256-e5df8c7787939b5319a02481affb5356198a9365b37a2b8719dba42590fd1812) and Ollama worked! I was finally able to use my GPU with it. I'm confused why it doesn't work normally, though. Is my GPU not supported in the version of ROCm that comes with Ollama or is there something else about the image that makes it work?

I haven't tried ComfyUI yet, because that pytorch image is too big for me to download right now.

---

### 评论 #9 — zichguan-amd (2025-02-10T20:34:58Z)

Hi @pkrasicki, good to hear that. gfx1030 is supported by ROCm 6.1.2, since it worked in the container, it suggests that it's a Ollama or ROCm installation issue. Ollama is supposed to use its own ROCm libraries packed in `ollama-linux-amd64-rocm.tgz`, you're Ollama 0.5.7 might be using some older libraries. 

Can you try a clean install of ROCm and Ollama? Using `OLLAMA_DEBUG=1` also helps identifying where Ollama is looking for the libraries. It may also be related to https://github.com/ollama/ollama/issues/8207

---

### 评论 #10 — zichguan-amd (2025-02-10T21:02:26Z)

Hi @kaiusdepaula, can you check if this helps https://github.com/ROCm/ROCm/issues/3894? Running `sudo` will override the venv and uses system python and packages, so it makes sense that it works since your system torch works. Can you verify the output of `ldd venv/lib/python3.12/site-packages/torch/lib/libtorch_hip.so`?

---

### 评论 #11 — kaiusdepaula (2025-02-10T22:02:09Z)

Funny story: I had given up and started using my system python to proceed on the project. As @zichguan-amd mentioned  #3894 that was very similar to the situation, I went back and recreated the .venv and it was now functional (!?).

Trying to traceback what I've done, I quite literally removed everything rocm related from arch using:
`pacman -Rc $(pacman -Qq | grep rocm)` 

And as the docker solution hadn't work, I decided to use the global python as it was working. So I did:
```
pacman -S rocm-hip-sdk rocm-opencl-sdk rocminfo
reboot
```
And after:
`pacman -S python-pytorch-rocm`

And installed via pip some basic packages I was using. 
After all that, running inside a .venv, even on different python versions, seems to work for some (magical) reason.

---

### 评论 #12 — pkrasicki (2025-02-11T12:19:36Z)

@zichguan-amd This is crazy, but it looks like the issue was caused by a space in the path! The drive I'm using has a space in the name. I've mounted it in a different location and suddenly Ollama and ComfyUI with ROCm 6.2 started working! It didn't work with the live ISO, because I was using the same drive. I guess in the container the path didn't have a space in it and that's why Ollama worked there.

Could this be a bug in ROCm 6.x, since it affects both Ollama and ComfyUI? I guess it could be an issue with some other library that they have in common, though.

@kaiusdepaula Could it be a path issue for you too?

---

### 评论 #13 — zichguan-amd (2025-02-11T15:23:41Z)

Good to hear that it works now for both of you! I'll try to trace down the space issue.

> As @zichguan-amd mentioned https://github.com/ROCm/ROCm/issues/3680 that was very similar to the situation

@kaiusdepaula I think you referenced the wrong issue?

---

### 评论 #14 — kaiusdepaula (2025-02-11T16:01:38Z)

@pkrasicki it could definitely be a space in the path! I've renamed it with a `_` and it worked. This was definitely the issue. 

@zichguan-amd the issue I referred to was wrong, I edited it to be right now. Thank you all very much!

---

### 评论 #15 — zichguan-amd (2025-02-11T19:54:55Z)

Hi @pkrasicki @kaiusdepaula, a fix for the space issue is under development. I'm closing this issue now since a workaround (remove space in path) exists. I'll update once the fix lands in a future ROCm release.

---

### 评论 #16 — pkrasicki (2025-02-13T11:23:44Z)

@zichguan-amd Thank you! But the problem is people will not know about the workaround unless we make the issue as visible as possible. I've struggled with this for many months thinking that my GPU wasn't supported and there are probably more people like that. This bug might have existed since 2023 when ROCm 6.0 was first released.

---

### 评论 #17 — zichguan-amd (2025-02-13T18:07:42Z)

I'll keep the issue open for visibility.

---

### 评论 #18 — YyLlBbYy (2025-02-15T22:56:23Z)

I've been unable to use automatic1111 WebUI and Forge ever since February 4 and I don't have a space in my path.
a1111 and Forge insist on installing rocm 5.7
Between the time that everything was functional and I discovered everything broke, I updated EndeavourOS and installed calligra and Huiontablet packages, and edited ownership of the files in the Huiontablet installation directory.
system packages (which are up to date at what the package managers push to me; rocm 6.2.4 and whatever pytorch) are functional and respond properly to rudimentary tensor calculation troubleshooting tests, once I've exported HSA_OVERRIDE_GFX_VERSION=10.3.0

I'll have to bounce between different operating systems to provide more information, which I will edit into this post.

with automatic1111 activating the venv and calling `HSA_OVERRIDE_GFX_VERSION=10.3.0 python3.10 -c "import torch; a=torch.randn(3).to('cuda');print(a)"` throws me `ImportError: libamdhip64.so: cannot enable executable stack as shared object requires: Invalid argument`
and `ldd venv/lib/python3.10/site-packages/torch/lib/libamdhip64.so` returns [this](https://github.com/user-attachments/files/18816865/dependencies.txt)

I've downgraded to python 3.10.13 (reasoning that 3.10.16 has an install date and time right before my problems began) with no improvement to my predicament, but I've installed ComfyUI now, and everything works as long as I manually activate the venv prior to running ComfyUI. That either points to me installing the dependencies wrong or there's something that's wrong elsewhere but halfway serviceable.
With this in mind there's probably nothing wrong with rocm 6.2 itself for my own situation, and something went wrong somewhere else that's preventing automatic1111/Forge /torch-2.3.1+rocm5.7 from working. and at that point it's probably more sane to nudge those projects into using rocm 6.x than troubleshoot a rocm stack that's 18 months past EOS.

---

### 评论 #19 — zichguan-amd (2025-02-18T15:33:55Z)

@YyLlBbYy based on the error message, have you tried `execstack -c venv/lib/python3.10/site-packages/torch/lib/libamdhip64.so` to clear the flag?

---

### 评论 #20 — YyLlBbYy (2025-02-18T20:14:15Z)

> [@YyLlBbYy](https://github.com/YyLlBbYy) based on the error message, have you tried `execstack -c venv/lib/python3.10/site-packages/torch/lib/libamdhip64.so` to clear the flag?

returns `execstack: venv/lib/python3.10/site-packages/torch/lib/libamdhip64.so: section file offsets not monotonically increasing`

using `patchelf --clear-execstack` instead clears the flag, and I also needed to clear the flag for libhiprtc.so in order to import torch.

oh happy day.




---

### 评论 #21 — zichguan-amd (2025-02-20T20:20:24Z)

[Commit 84a867fb735f69299c45c0b30a085b8e8400cd15](https://github.com/ROCm/clr/commit/84a867fb735f69299c45c0b30a085b8e8400cd15) should address the space issue. If you want to test it out now, you can build `clr` from source on the `amd-staging` branch or cherry pick this commit and rebuild `clr`. Will update again when the fix lands in a future release.

---

### 评论 #22 — zichguan-amd (2025-07-02T16:37:15Z)

Hi @pkrasicki @kaiusdepaula, please try out [ROCm 7 Alpha](https://rocm.docs.amd.com/en/docs-7.0-alpha/preview/install/rocm.html), the space issue is fixed in the Alpha build and will be available in ROCm 7.0. Tested with pytorch nightly build on 7900XTX:
```
(venv with space) ~$  pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.4/
 ...
(venv with space) ~$ python3 -c "import torch;print(torch.cuda.is_available())"
True
(venv with space) ~$ python3 -c "import torch; a=torch.randn(3).to('cuda'); print(a)"
tensor([-1.1108, -1.3592,  0.4885], device='cuda:0')
```

---

### 评论 #23 — pkrasicki (2025-07-05T00:55:59Z)

@zichguan-amd Thank you! I will probably wait for a Debian 13 package, but I'm glad it's fixed now! Do you think it would be possible to have a fix in ROCm 6.x too? I imagine it will take some time for existing software projects to start using the version 7, even after we get a stable release.

---

### 评论 #24 — zichguan-amd (2025-07-07T14:06:04Z)

Unfortunately, I don't have control over that. ROCm 7 is the next major release and should be coming up later this year. If you want it in ROCm 6.x you can always build from source.

---
