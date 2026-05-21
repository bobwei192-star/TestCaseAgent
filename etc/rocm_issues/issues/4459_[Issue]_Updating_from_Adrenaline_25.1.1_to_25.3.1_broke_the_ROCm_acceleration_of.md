# [Issue]: Updating from Adrenaline 25.1.1 to 25.3.1 broke the ROCm acceleration of 7900XTX, Windows, Adrenaline, HIP, Zluda, Comfy UI fork. Trying WSL2+ROCm.

> **Issue #4459**
> **状态**: closed
> **创建时间**: 2025-03-07T10:19:02Z
> **更新时间**: 2025-06-14T12:39:40Z
> **关闭时间**: 2025-04-07T17:56:52Z
> **作者**: OrsoEric
> **标签**: Under Investigation, AMD Radeon RX 7900XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4459

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900XTX** (颜色: #ededed)

## 描述

### Problem Description

Updating from Adrenaline 25.1.1 to 25.3.1 broke the ROCm acceleration of 7900XTX, Windows, Adrenaline, HIP, Zluda, Comfy UI fork

I'm having gargantuan issues getting pytorch applications that worked under CUDA to work under ROCm after I upgraded from a RTX3080 to a 7900XTX

### Operating System

PS C:\Users\FatherOfMachines>  (Get-WmiObject Win32_OperatingSystem).Version 10.0.22631

### CPU

PS C:\Users\FatherOfMachines>   (Get-WmiObject win32_Processor).Name 13th Gen Intel(R) Core(TM) i7-13700F

### GPU

PS C:\Users\FatherOfMachines>   (Get-WmiObject win32_VideoController).Name AMD Radeon RX 7900 XTX

### ROCm Version

C:\Program Files\AMD\ROCm\6.2\bin>hipcc --version HIP version: 6.2.41512-db3292736 clang version 19.0.0git (git@github.amd.com:Compute-Mirrors/llvm-project 5353ca3e0e5ae54a31eeebe223da212fa405567a) Target: x86_64-pc-windows-msvc Thread model: posix InstalledDir: C:\Program Files\AMD\ROCm\6.2\bin  C:\Program Files\AMD\ROCm\6.2\bin>hipinfo  device# 0 Name: AMD Radeon RX 7900 XTX pciBusID: 3 pciDeviceID: 0 pciDomainID: 0 multiProcessorCount: 48 maxThreadsPerMultiProcessor: 2048 isMultiGpuBoard: 0 clockRate: 2482 Mhz memoryClockRate: 1250 Mhz memoryBusWidth: 0 totalGlobalMem: 23.98 GB totalConstMem: 2147483647 sharedMemPerBlock: 64.00 KB canMapHostMemory: 1 regsPerBlock: 0 warpSize: 32 l2CacheSize: 4194304 computeMode: 0 maxThreadsPerBlock: 1024 maxThreadsDim.x: 1024 maxThreadsDim.y: 1024 maxThreadsDim.z: 1024 maxGridSize.x: 2147483647 maxGridSize.y: 65536 maxGridSize.z: 65536 major: 11 minor: 0 concurrentKernels: 1 cooperativeLaunch: 0 cooperativeMultiDeviceLaunch: 0 isIntegrated: 0 maxTexture1D: 16384 maxTexture2D.width: 16384 maxTexture2D.height: 16384 maxTexture3D.width: 2048 maxTexture3D.height: 2048 maxTexture3D.depth: 2048 hostNativeAtomicSupported: 1 isLargeBar: 0 asicRevision: 0 maxSharedMemoryPerMultiProcessor: 64.00 KB clockInstructionRate: 1000.00 Mhz arch.hasGlobalInt32Atomics: 1 arch.hasGlobalFloatAtomicExch: 1 arch.hasSharedInt32Atomics: 1 arch.hasSharedFloatAtomicExch: 1 arch.hasFloatAtomicAdd: 1 arch.hasGlobalInt64Atomics: 1 arch.hasSharedInt64Atomics: 1 arch.hasDoubles: 1 arch.hasWarpVote: 1 arch.hasWarpBallot: 1 arch.hasWarpShuffle: 1 arch.hasFunnelShift: 0 arch.hasThreadFenceSystem: 1 arch.hasSyncThreadsExt: 0 arch.hasSurfaceFuncs: 0 arch.has3dGrid: 1 arch.hasDynamicParallelism: 0 gcnArchName: gfx1100 peers: non-peers: device#0  memInfo.total: 23.98 GB memInfo.free: 23.84 GB (99%)

### ROCm Component

_No response_

### Steps to Reproduce

- https://github.com/LeagueRaINi/ComfyUI.git
- Adrenaline 25.3.1
- HIP 6.2.4
- Zluda 

Update from Adrenaline 25.1.1 to 25.3.1 breaks ROCm acceleration. E.g. SD1.5 T2I workflow from <10s now takes 662s.

GIST with the workflow, output repo and details
https://gist.github.com/OrsoEric/5d2222201d167a40486a037e9d6d063b


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

I have been trying to get ROCm acceleration working for about a month. I can get pretty far with enormous effort, but at some point a Comfy UI node won't work and requires me to discard it all and rebuild a new stack from the ground up with another fork to get further.

I did get Flux to accelerate well with this fork + Zluda
https://github.com/LeagueRaINi/ComfyUI.git
But it's too far the mainline and doesn't support Wan nodes, and with the update to Adrenaline 25.3.1 the acceleration broke completely

I'll refrain from wiping the stack so you can ask me diagnostics steps.

---

## 评论 (30 条)

### 评论 #1 — ppanchad-amd (2025-03-07T14:21:56Z)

Hi @OrsoEric. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-03-07T15:57:08Z)

Hi @OrsoEric, thanks for your interest in using ROCm, and sorry this broke for you. This is in an awkward spot because we don't support zluda and therefore don't test for it, but I'll provide support if possible. I'll take a look to see if this issue is on our end, but if this ends up being exclusively a zluda problem it might be hard to make a case to fix it.

Have you tried [ROCm on WSL2](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/howto_wsl.html)? Your hardware is supported, and I can provide assistance in getting it set up if needed. 

---

### 评论 #3 — OrsoEric (2025-03-08T06:59:21Z)

Thanks for answering.

LM Studio + llama.cpp ROCm still work, so I'm pretty confident it's the pytorch binaries bindings that broke. I can't tell where.

It took dozens of try, I went with that Zluda fork because it's the only one that ended up accelerating every ComfyUI node I use, excepts newer ones. (until it bricked). The 7900XTX is really fast when it works, I got Flux dev FP8 to do 1MP image 20 step in one minute, which is excellent performance.

UPDATE: I restored a good chunk of the acceleration. I suspect it is windows related that adrenaline so I did a windows update, and some of the acceleration resumed. SD1.5. gets accelerated 662s->8s the flux workflows took 352s get started but now seems to accelerate right, it might be that the driver needed to recompile? The first run of the node takes between 5 and 10 minutes to warm up it seems.

[2025-03-08a-SD-Flux-Acceleration-Restored.txt](https://github.com/user-attachments/files/19142206/2025-03-08a-SD-Flux-Acceleration-Restored.txt)

I still need to find a way that runs the Wan nodes, and Trellis. With Wan I got close, I got 240p video to render, and I need the latest fork of comfy UI to run GGUF quantized Wan models and reduce memory usage from 40GB->20GB to get 480p and 720p videos going.

I tested and the Wan nodes acceleration is broken badly, I don't think there is coming back from this:
[WAN14-240p-I2V.json](https://github.com/user-attachments/files/19142376/WAN14-240p-I2V.json)
[2025-03-08-Wan-Broken.txt](https://github.com/user-attachments/files/19142378/2025-03-08-Wan-Broken.txt)


With Trellis I'm questioning if it's impossible under ROCm. I never gotten even close.

WSL2

I don't particularly care about what backend works as long as it can accelerate pytorch applications written by others. I'd like the official repos to work:

- https://github.com/comfyanonymous/ComfyUI
- https://github.com/microsoft/TRELLIS

I did try WSL2 before, to no avail. I could get pretty far detecting the card and accelerating e.g. the FLUX sampler, but large swathe of the pytorch acceleration defaulted to CPU (like the VAE decode/encode) or I got driver timeouts.

Many people suggested I try WSL2, so yesterday I went all day, bricking four WSL instances.

I'll share the issues I had with it with as much detail and accuracy as I can:

---

### 评论 #4 — OrsoEric (2025-03-08T07:42:24Z)

WSL2 (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html)

STEP1: Install WSL2

Installing from microsoft store takes up to eight hours, it's very slow and it looks stuck at  0% or 90% for hours.

Luckily there is a command line option to download from another source that is fast.

`wsl --install -d Ubuntu-22.04 --web-download'

This works fine and I get inside WSL2.

STEP2: AMD Driver

I follow the guide, and I get an error, I fix it by fixing the ownership:

`N: Download is performed unsandboxed as root as file '/home/soraka/amdgpu-install_6.3.60304-1_all.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
soraka@TowerOfBabel:~$ ls
amdgpu-install_6.3.60304-1_all.deb
soraka@TowerOfBabel:~$ sudo chown _apt:root /home/soraka/amdgpu-install_6.3.60304-1_all.deb
sudo chmod 644 /home/soraka/amdgpu-install_6.3.60304-1_all.deb
soraka@TowerOfBabel:~$ sudo chmod 644 /home/soraka/amdgpu-install_6.3.60304-1_all.deb
soraka@TowerOfBabel:~$ ls
amdgpu-install_6.3.60304-1_all.deb
soraka@TowerOfBabel:~$ sudo apt install ./amdgpu-install_6.3.60304-1_all.deb`

Attached the full log

[2025-03-07 WSL2 driver install.txt](https://github.com/user-attachments/files/19142314/2025-03-07.WSL2.driver.install.txt)







---

### 评论 #5 — OrsoEric (2025-03-08T08:25:05Z)

STEP3: Torch

I wasn't able to make torch work at all, it's a much deeper issues to the permissions of the driver.

Python

One of the issues comes from the Python version. The AMD instruction clearly say pytorch ONLY work for python 3.10 ([Install PyTorch for ROCm — Use ROCm on Radeon GPUs](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html))

`Important! These specific ROCm WHLs are built for Python 3.10, and will not work on other versions of Python.`

While Comfy UI needs 3.12 (https://github.com/comfyanonymous/ComfyUI)

` python` 3.13 is supported but using 3.12 is recommended because some custom nodes and their dependencies might not support it yet.`

3.12 seems to brick the pytorch that works, while 3.10 seems to brick comfy ui. I'm not sure if this IS possible under ROCm.

Wheels:

Another issue comes from wheel permission, I'd have to test more throughly to get a feel of the issue. This one I couldn't fix with a CHMOD.

`WARNING: Skipping torch as it is not installed.
WARNING: Skipping torchvision as it is not installed.
WARNING: Skipping pytorch-triton-rocm as it is not installed.
Defaulting to user installation because normal site-packages is not writeable
Processing ./torch-2.4.0+rocm6.3.4.git7cecbf6d-cp310-cp310-linux_x86_64.whl
ERROR: Wheel 'torch' located at /mnt/c/Users/FatherOfMachines/torch-2.4.0+rocm6.3.4.git7cecbf6d-cp310-cp310-linux_x86_64.whl is invalid.`

[2025-03-07e Fail to install torch.txt](https://github.com/user-attachments/files/19142502/2025-03-07e.Fail.to.install.torch.txt)



---

### 评论 #6 — OrsoEric (2025-03-08T08:28:33Z)

Last time I gave up at torch and went Zluda.

This time I pressed on and tried the docker.

It needs an ungodly amount of disk space, well over 100GB so it filled my C drive and bricked. Now I'm trying to wipe it, and I'll try to move to another drive. 

[2025-03-07g out of space for WSL2.txt](https://github.com/user-attachments/files/19142507/2025-03-07g.out.of.space.for.WSL2.txt)

I'm not sure what approach has a better chance of working, if WLS2+native pytorch, or WSL2+docker

---

### 评论 #7 — OrsoEric (2025-03-09T11:14:21Z)

Unbricking WSL from a full drive was difficult. I manually removed the feature and manually cleared the bricked downloads from %USERPROFILE%\AppData\Local\Packages\CanonicalGroupLimited*

It's possible to move WSL2 to another drive. It's janky, but first make a WSL2, export it as tar, unregister, and import it.

wsl --shutdown

wsl --export Ubuntu-22.04 "F:\WSL-Ubuntu22\WSL-Ubuntu22.tar"

wsl --unregister Ubuntu-22.04

wsl --import Ubuntu-22.04 "F:\WSL-Ubuntu22" "F:\WSL-Ubuntu22\WSL-Ubuntu22.tar"

this way the ext4 file is on a drive with actual space on it. Now I'm rebuilding it.


---

### 评论 #8 — OrsoEric (2025-03-09T13:00:12Z)

It was really, really hard, but I got pytorch installed, comfy ui installed, and was able to get a basic workflow running under WSL2.

I'm getting even better performance than Zluda on 512x512 going from 2.05s for 20 iterations to 1.14s for 20 iterations. I'll have to see the scaling, the VRAM uses seems higher but I'll need more time to diagnose it, it might be nothing.

I still had the problem of the amd driver needing CHMOD, but I got the pytorch wheels going by doing commands one at a time instead of bundling them, and fiddling with user permissions. Not sure what got it working, but this time it went through without errors.

[The native comfyui repo now works with the linux instructions. But it's capricious diring install](https://github.com/comfyanonymous/ComfyUI)

I had some hiccups that required a few restart of the WSL as it temporarely broke something. But the commands used to check pytorch are a good sanity check, I think a script should first do the sanity checks 

> python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
> python3 -c 'import torch; print(torch.cuda.is_available())'
> python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
> python3 -m torch.utils.collect_env

cd ComfyUI
pip install -r requirements.txt
python3 main.py

Attached is the full logs of the latest fiddling that got it running. I need to see if it survives a system reboot or adding the comfyui extensions.

[2025-03-09f-comfy-ui-sd15-success.log](https://github.com/user-attachments/files/19149621/2025-03-09f-comfy-ui-sd15-success.log)

There are some weird WSL2 quirks that do not help. When windows spin up WSL sometimes it throws weird errors and it start as root and inside a windows folder. So make sure to go to the home folder with the user.

> su soraka
> cd ~

Now I need to load the models inside the WSL2 EXT4 vrtual disk. I was thinking of symlink to the OS, but since I moved the EXT4 itself to a bigger drive, I can just shove the models inside the EXT4 perhaps. I have about 400GB of models to test. SD1.5 T2I is promising, if it scales and it doesn't break.

There are RAM considerations. Windows wanted to give WSL 32GB which is not nearly enough for a 24GB VRAM card. I raised it to 50GB leaving 14GB for the host machine. I have to see how much RAM penality is there. 

---

### 评论 #9 — OrsoEric (2025-03-09T15:14:48Z)

I tried Flux, and there indeed are more RAM issues, but VRAM use seems fine. I got a driver timeout at resolution where Zluda was fine. I downgraded from VAE to TiledVAE.

The speed is better, it's 39.8s for 20 step 1MP which is great.

[2025-03-09h-wsl2-flux-benchmark.log](https://github.com/user-attachments/files/19150383/2025-03-09h-wsl2-flux-benchmark.log)
[2025-03-09g-wsl2-comfy-ui-flux-drivertimeout.log](https://github.com/user-attachments/files/19150382/2025-03-09g-wsl2-comfy-ui-flux-drivertimeout.log)

That's it for today, I'll try to increase VRAM allocation from 50/64 to 56/64. For my system it's not easy to upgrade to 128GB, I have a 4x16GB configuration.

---

### 评论 #10 — schung-amd (2025-03-10T14:24:38Z)

Thanks for the extensive updates, and glad WSL is working for you now! Sorry you ran into some issues during installation, if you still have questions regarding some of the steps let me know.

> The AMD instruction clearly say pytorch ONLY work for python 3.10

Thanks for pointing this out, this is outdated guidance. In fact, the wheel the Ubuntu 24.04 instructions point to is a python 3.12 wheel (`torch-2.4.0+rocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl`), identified by the `cp312` substring. If you need pytorch for alternative versions of python you can browse https://repo.radeon.com/rocm/manylinux to see if a compatible stable wheel exists, or you can use the unstable builds from pytorch.org.

> downgraded from VAE to TiledVAE

No real suggestion here, just a comment: in your timeout log, you're using reduced precision (bf16 in this case) but the VAE decoding is still full precision (probably due to the model not providing reduced precision VAE, although you can double check your configuration). This means that the VAE decoding step might require too much VRAM even if you had enough VRAM to hold the model, so tiled VAE would be required in this scenario.



---

### 评论 #11 — OrsoEric (2025-03-11T08:03:59Z)

> No real suggestion here, just a comment: in your timeout log, you're using reduced precision (bf16 in this case) but the VAE decoding is still full precision (probably due to the model not providing reduced precision VAE, although you can double check your configuration). 

Nice catch, I'll look into it. It's not really a problem to feed a BF16 VAE model.

>  In fact, the wheel the Ubuntu 24.04 instructions point to is a python 3.12 wheel

I'm a bit worried rebuilding WSL2 on ubuntu 24, WSL is really fragile and I don't know if enough of python has the binaries for ubuntu24. If possible I'd like to make 3.12 work on ubuntu22. But I'll do lots of testing.

I'd really like WSL-ROCm to become more reliable.

In order I have to try:

- I2T <- i think it easily works but I have to try it.  
- quantized Wan workflow and acceleration <- what I couldn't with the Zluda fork
- [trellis](https://github.com/microsoft/TRELLIS). I'm planning to use it to do 3D model for my 3D priner, I need a I23D and a T23D generative model to work.
- S2T T2S and multimodal Janus. <- part of building a bigger assistent stack on the computer locally.

I really need ROCm to have a wide acceleration support, it's not enough to accelerate only pieces of pytorch.

LLMs are easier to run native, the guys that built llama.cpp with ROCm acceleration did an okay job with the bidings. In my opinion the endgame would be for a one click installer to let all the acceleration to run natively with the latest pytorch for the most common applicationat least.

---

### 评论 #12 — schung-amd (2025-03-11T14:14:41Z)

> I'm a bit worried rebuilding WSL2 on ubuntu 24

Sorry, didn't mean to imply that you should try Ubuntu 24; rather that we now supply wheels for Python versions other than 3.10, so you should be fine to use Python 3.12 (in conjunction with the `cp312` wheel).

---

### 评论 #13 — OrsoEric (2025-03-14T11:32:27Z)

FLUX VAE

I did some testing, loading various external VAEs, and the problem doesn't seem to be the VAE model itself.

I think it's the SamplerAdvanced. With the regular KSampler it uses lots less RAM.

This workflow below works better.
[FLUX-txt2img.json](https://github.com/user-attachments/files/19246342/FLUX-txt2img.json)

---

### 评论 #14 — OrsoEric (2025-03-14T11:37:56Z)

IMAGE TO 3D

Trellis uses PIL, which I think it's part of the reason I couldn't do it before, so I tried other approaches since asia is contributing some truly amazing models lately.

To my shock, I was able to run image to 3D workflow under 7900XTX Win11 WSL2 ROCm Pytorch ComfyUI! It's also very speedy, 128s per generation and it properly loads 100%.

This worked on first try, I didn't really need to rebuild anything for it to work, just lower security level to weak install custom and reboot. 
https://github.com/kijai/ComfyUI-Hunyuan3DWrapper

Compared to the enormously complicated workflow I did a simplified workflow to just see if it worked, and it did. I'm seriously impressed that ROCm accelerated this.

![Image](https://github.com/user-attachments/assets/b04da00c-4739-4ce7-9f8f-1056547f7ef8)

Simplfied Workflow
[HUNYUAN-T23D.json](https://github.com/user-attachments/files/19246402/HUNYUAN-T23D.json)

Logs of the installation

[2025-03-14a-kijay-hun-3d-working.log](https://github.com/user-attachments/files/19246408/2025-03-14a-kijay-hun-3d-working.log)

---

### 评论 #15 — OrsoEric (2025-03-21T10:44:03Z)

I'm starting to get some errors and warning, the ComfyUI acceleration is still going but I'm not sure if there are deeper issues brewing.

/home/soraka/.local/lib/python3.10/site-packages/torch/cuda/__init__.py:645: UserWarning: Can't initialize amdsmi - Error code: 34
  warnings.warn(f"Can't initialize amdsmi - Error code: {e.err_code}")

[2025-03-21-rocm-error.log](https://github.com/user-attachments/files/19387605/2025-03-21-rocm-error.log)

Also ComfyUI has errors

ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied: '/usr/local/lib/python3.10/dist-packages/comfyui_frontend_package'
Consider using the `--user` option or check the permissions.

I took some time to compile the documentation of the steps that led to working WSL2 acceleration of ComfyUI since many steps aren't obvious from the guide to me

https://github.com/OrsoEric/HOWTO-7900XTX-Win-ROCM


---

### 评论 #16 — schung-amd (2025-03-21T14:11:48Z)

The `amdsmi` error is expected on WSL, the drivers in WSL work differently than on native Linux so we don't have `amdsmi` functionality there (although we are working on porting some of it over to reduce incompatibilities like this). Applications generally use `amdsmi` to get system info. It looks like torch is using `amdsmi` there to get the device count, as long as your workload is still running I wouldn't worry about it.

Thanks for documenting your process! Hopefully this will help other users in getting WSL set up in the future.

---

### 评论 #17 — schung-amd (2025-04-07T17:56:52Z)

Closing this for now as I don't think there's an issue here on our end at the moment. Appreciate the updates, and glad you have workloads running well! Feel free to continue updating here, and we can reopen this or you can submit a new issue if you run into further obstacles. Thanks for your interest in using ROCm!

---

### 评论 #18 — OrsoEric (2025-04-09T08:48:08Z)

So... Looking at the feedback, your conclusion is that ROCm works fine as is?

Documentation is fine?

Experience is fine?

Adrenaline update behavior are fine?

Even the matricies that list windows as compatible with ROCm are truthful?



---

### 评论 #19 — schung-amd (2025-04-09T14:10:17Z)

I meant that there is no specific issue in this thread for us to look at, not that there is nothing wrong with ROCm. There are obviously numerous issues and areas to improve with ROCm, and we're constantly working on improving ROCm behind the scenes. However, the issues section is meant for concrete, actionable items that we can look at and address. If you have specific concerns, you can open issues for them or mention them here and we can take a look. Otherwise, it is more fitting to use a discussion thread. 

> ROCm works fine as is?
> Experience is fine?

ROCm works great in the environment it was originally targeted at, which is a Linux system with MI cards. We have support on Radeon cards where it works well on specific architectures as pointed out in the compatibility matrix, and less well on others. We are also working on Windows support, but this is still a work in progress and some things are missing (Pytorch, cooperative groups, etc.).

There are also some rough patches with application support, but again unless you have a specific issue in mind for us to look at there is nothing to do here.
 
> Adrenaline update behavior are fine?

We have tested the Adrenalin versions that we specify in the ROCm install instructions on Windows. Breaking ZLUDA performance is unfortunate but not our concern as we don't support ZLUDA.

> Even the matricies that list windows as compatible with ROCm are truthful?

Yes, the compatibility matrices are correct. You do have to make sure you're looking at the right matrix though, as there are several ways to use ROCm at the moment (regular Linux-based, Windows via WSL2 and HIP SDK) and each supports a different set of architectures.

---

### 评论 #20 — OrsoEric (2025-04-10T07:08:59Z)

Don't take this the hard way, I mean to be constructive. 

>However, the issues section is meant for concrete, actionable items that we can look at and address.

I have no idea how ROCm works on the inside, nor I want to know. Just like I have no idea how CUDA works on the inside, nor I want to know. I am not qualified to point at specific actionable issues.

What I can do is spend time as a user of ROCm accelerated pytorch applications, follow installation guides and document what does not work and post the logs here, so you can use your expertise to generate actionable items. I believe AMD can achieve useable acceleration, it's why I'm willing to spend time to document issues, and not just return the card and get a Nvidia like I'm advised I should do. if I thought this was hopeless, I wouldn't be here.

> Yes, the compatibility matrices are correct. 

This is an error, as I documented above. 

While I found it possible, even easy, to follow the ROCm windows installation guides with no error to the end. After some effort I got LM Studio to run natively under windows with good ROCm acceleration (with a llama.cpp based runtime). I found no ways to get ROCm accelerated pytorch applications to take advantage of ROCm acceleration. 

Which led me to use Zluda that tries to remap the pytorch CUDA binaries to ROCm as far as I understand, and does achieve better pytorch coverage of the applications I tried, but it's very spotty coverage, causes lots of driver timeouts and is not officially supported by AMD. I'm not asking for AMD to support Zluda, I would rather prefer acceleration works natively under windows for popular ML framework like pytorch.

The first thing you suggested me here was to use linux, which suggest ROCm is not compatible with windows.

The second thing you suggested was to use WSL2 to use linux under windows, which suggest ROCm is not compatible with windows. And WSL2 got me pretty far, but I still get black screen and drivers timeout.

This leads me to the conclusion that ROCm is incompatible with windows.

Here two possible actionable item for you:

1. Update documentation to reflect ROCm incompatibility with windows
2. Update guides to show how to get ROCm to accelerate pytorch applications under windows with full coverage of pytorch calls.

I'm willing to commit more time to test them.

> We are also working on Windows support, but this is still a work in progress and some things are missing (Pytorch, cooperative groups, etc.).

That was not obvious to me reading the guides. I did some research and it led me to believe 7900XTX ROCm acceleration worked under windows. Pytorch is listed as supported there if I read the compatibility matricies right.

An actionable item could be to make it more obvious in the compatibility matricies that pytorch ROCm binaries only have partial coverage under windows.

![Image](https://github.com/user-attachments/assets/38c5cd95-045f-4c20-a33a-d5332d99ca0c)

> There are also some rough patches with application support, but again unless you have a specific issue in mind for us to look at there is nothing to do here.

I have no idea how ROCm works on the inside, nor I want to know. I am not qualified to point at specific actionable issues.

What i can do, Is list you the applications that try to support ROCm, and I had great trouble accelerating. 

- https://lmstudio.ai/ 
- Comfy UI https://github.com/comfyanonymous/ComfyUI
- SD Next https://github.com/vladmandic/sdnext

Quoting from SD NEXT:
> AMD GPUs using ROCm libraries on Linux
Support will be extended to Windows once AMD releases ROCm for Windows

I still get black screens and driver timeout on the VAE Decode, and I take the time to submit driver timeout bug reports via adrenaline bug reports.

> We have tested the Adrenalin versions that we specify in the ROCm install instructions on Windows

I can follow the instruction and install ROCm under windows.

And none of the ROCm accelerated pytorch applications will be fully ROCm accelerated under windows.

perhaps I'm having trouble following the guides, or perhaps the issues is elsewhere. I believe this could be an actionable item. 

> Intermittent application crash or driver timeout may be observed while using ComfyUI with WSL2 on some AMD Graphics Products, such as the Radeon™ RX 7900 Series

![Image](https://github.com/user-attachments/assets/a7a26115-9fb5-4292-bfc3-d32bfdd7b908)

[This quote comes from the adrenaline known issues ](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#release-known-issues) it's the one of the issues I'm experiencing.

I say this with no malice: ROCm, as it stands, is not viable for any work I can think of. I don't know anyone that would recommend ROCm, and I was actively advised against (and laughed at) for attempting using it by multiple people, some in the datacenter space, some researchers,  people that know their stuff. My experience reinforced their advice on the matter. I don't know about Mi300 accelerators, I'll take you at your word that ROCm works great on that platform.

AMD silicon offering is compelling. Compute and VRAM capability have really great performance per dollar compared to Nvidia for ML, it's the reason I picked it. But even if AMD gave accelerators away for free, the people I know would still not pick them. [An example of a researcher looking for a ML  built](https://linustechtips.com/topic/1607495-7000-machine-learning-pc-gpu-choice-overall-specs)

The argument made to me is that while AMD accelerators are cheaper for equal theoretical specs, if I paid myself for the time spent to make ROCm acceleration work, I could afford the next tier up of Nvidia accelerator with CUDA working out of the box. And they were right.

At work we use Nvidia A6000, I wouldn't fathom suggesting using AMD W7900 we need the cards to work, we can't spend time fixing the underlying acceleration stack. The only reason I gave ROCm a try is because I'm doing this as an hobby on my home computer with a 7900 XTX, and I only gave it a try because Nvidia has terrible availability at the moment. Because it's an hobby, I can spend a month trying to debug the ML runtime, i have no deadlines to meet, just assets to generate for my D&D campaigns.



This reads as highly critical but I assure you it's with no malice. My intent is to give you useful feedback in order to get ROCm acceleration running smoothly. There is potential here, what does accelerate, actually accelerate really fast.

My goal is to run ROCm accelerated pytorch application natively under windows, and get full coverage of the pytorch calls for Comfy UI (https://github.com/comfyanonymous/ComfyUI) with no driver timeouts nor black screens.

Do you believe this possible with ROCm under windows?

I am willing to spend time to give ROCm under windows another try if you believe this is possible.

---

### 评论 #21 — schung-amd (2025-04-10T15:09:47Z)

> What I can do is spend time as a user of ROCm accelerated pytorch applications, follow installation guides and document what does not work and post the logs here, so you can use your expertise to generate actionable items.

This is appreciated, and as I said this is only closed for now because the last posted logs don't have anything to address on our end. `amdsmi` is not supported in WSL so that warning is expected and shouldn't break anything. The other error looks like it's ComfyUI specific, I don't see any mention of our components there. You are free and welcomed to continue posting logs, and if something arises that needs our attention (like a specific crash or hang) we can reopen the issue. We would prefer to have issues closed if no immediate work is being done on them, as this repository has historically had a lot of long-standing general issues with no clear resolution.

> Update documentation to reflect ROCm incompatibility with windows

Where did you see indication of native Windows support? We do have native Windows support in the form of HIP SDK, but it is incomplete at the moment. If we have a compatibility matrix advertising native Windows support for the full ROCm stack then that's certainly an error on our part.

> I did some research and it led me to believe 7900XTX ROCm acceleration worked under windows. Pytorch is listed as supported there if I read the compatibility matricies right.

Pytorch is supported under WSL2, but not natively in Windows (i.e. HIP SDK). The compatibility matrix referred to here is Linux-specific.

> My goal is to run ROCm accelerated pytorch application natively under windows

No, I don't believe this is possible at the moment. With Linux or WSL2 you could get these workloads running, but we don't currently support Pytorch in native Windows.

I understand and share your frustration with ROCm as a hobbyist. Our support for Radeon GPUs is quite limited, and our support on Windows is incomplete. It would be great if hobbyist users with typical gaming setups could easily install and use ROCm, and hopefully this will be the case in the future as we work to improve this situation.





---

### 评论 #22 — sfinktah (2025-05-29T04:10:31Z)

> I understand and share your frustration with ROCm as a hobbyist. Our support for Radeon GPUs is quite limited, and our support on Windows is incomplete. [...] hopefully this will be the case in the future as we work to improve this situation.

@schung-amd - it's great to see you say this.  I've read through this entire thing, as there is a similar issue with going from 25.4.1 to 25.5.1 (NOTE TO READERS: The solution is to `patchzluda2.bat` and give it the URL of the latest patch **after going to the repo and copying it's url**)

I just upgrade my 6800 for a 7900XTX today, so I no longer care that the WSL2 ROCm bridge didn't support RDNA2.

I think that given the drop in VRAM for the 9070 (notwithstanding the R9700 which is outside our budgets), the most profitable avenue for advancement would be to encourage/assist in the implementation and adoption of Matrix Fused Multiply-Add (MFMA) operations in pytorch -- and not forgetting the INT8/FP16 ones.  While the FP8 might seem like the more obvious target, neglecting the RDNA3 just because it isn't the latest tech would be dissapointing and I don't think you'll sell many 9070 to the AI crowd.

That said, I'm not sure INT8 for stable diffusion is even practical (surely there's a reason nobody seems to be using it).

I'm also cognizant that CDNA is where you put the real AI goodies (and where your real money comes from), and that RDNA support is more of a happy accident.

Keep up the good work, it's encouraging.  
 

---

### 评论 #23 — jammm (2025-06-04T11:39:12Z)

@OrsoEric @sfinktah can you try these pytorch wheels ? It might solve your issues https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x

it comes bundled with ROCm (compiled using [TheRock](https://github.com/ROCm/TheRock)) so you don't need to install HIP SDK by yourself.

Note that these wheels are unofficial, is in active development, and there might still be issues. I don't recommend trying this if you're not willing to fiddle around. 

---

### 评论 #24 — sfinktah (2025-06-04T14:52:11Z)

> [@OrsoEric](https://github.com/OrsoEric) [@sfinktah](https://github.com/sfinktah) can you try these pytorch wheels ? It might solve your issues https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x

I was about to reply with "I actually don't have any issues", but between then and now (2 hours), I have discovered that WAN2.1 I2V takes a massive dump related to `hipHccModuleLaunchKernel()` (though t2v works fine).

I asked ChatGPT (which is absolutely **awful** at any kind of stable diffusion advice) and it's telling me to go back to HIP SDK: 5.7.1 (from 6.2)... what a horrible idea.   And to go back to an Adrenaline version prior to 25.3.1.

On the other hand, I would have to move to py3.12 to use your wheel, which is a bit "not-zluda" or at least, "not patientx".

On the gripping hand, I want to try out the new Triton and flash-attention stuff for zluda, which may involve updating anyway.

p.s. your Strix Halo (gfx1151) thing looks cool.  how fast is it really?

---

### 评论 #25 — jammm (2025-06-04T14:55:02Z)


> On the gripping hand, I want to try out the new Triton and flash-attention stuff for zluda, which may involve updating anyway.
> 
> p.s. your Strix Halo (gfx1151) thing looks cool. how fast is it really?

The wheel supports flash attention via. aotriton. I don't have extensive benchmark results but on comfyui it gave me around 10it/s on the default SD1.5 workflow.

The gfx1151 is a[ framework desktop ](https://frame.work/desktop).

There's wheels for both 3.11 and 3.12 python versions.
Note that the wheels are unofficial and built by community members like me.

---

### 评论 #26 — sfinktah (2025-06-06T11:01:08Z)

@jammm Oh that framework desktop looks very nice.  I did some quick research upon your mention of the gfx1151 and couldn't find anything other than laptops that were using it yet.  Obviously the concept of being able to use RAM instead of VRAM is very appealing, and AMD users feel it more than most (no fp8 until RDNA4, code generally not optimised for AMD, poor support for gguf).

I'm on python 3.10, and could probably compile it myself (I've done a bit of python package dev, but it was ages ago) but don't want to.  3.10 is arguably the most compatible python version (well, patientx thinks so, i don't really care).

I'm presently dealing with that most common of annoying problems, figuring out why WAN wants to use so much memory that ZLUDA/HIP crashes (I think during the initial VAE image decoding).  Am about to install (yet another) copy of comfyui-zluda to try the triton stuff, so will happily test your wheel too if you like. 

---

### 评论 #27 — jammm (2025-06-06T11:05:02Z)

> [@jammm](https://github.com/jammm) Oh that framework desktop looks very nice. I did some quick research upon your mention of the gfx1151 and couldn't find anything other than laptops that were using it yet. Obviously the concept of being able to use RAM instead of VRAM is very appealing, and AMD users feel it more than most (no fp8 until RDNA4, code generally not optimised for AMD, poor support for gguf).
> 
> I'm on python 3.10, and could probably compile it myself (I've done a bit of python package dev, but it was ages ago) but don't want to. 3.10 is arguably the most compatible python version (well, patientx thinks so, i don't really care).
> 
> I'm presently dealing with that most common of annoying problems, figuring out why WAN wants to use so much memory that ZLUDA/HIP crashes (I think during the initial VAE image decoding). Am about to install (yet another) copy of comfyui-zluda to try the triton stuff, so will happily test your wheel too if you like.

You're welcome to try the wheel out! You'd want to switch to python3.11/3.12 for it though.
For triton you might want to build it yourself, as there's no official windows support for it. Having said that, those pytorch wheels come with aotriton which provides fwd/bwd kernels for flash attention, so it should run things fast with less VRAM when you use `--use-pytorch-cross-attention` in comfyui.

---

### 评论 #28 — sfinktah (2025-06-06T12:15:50Z)

@jammm well, given that my (meant to be easy) update to try patientx's triton build has me pulling apart build.py to find out why a `-Wvisibility` warning about a `structval*` argument would be causing the linker to fail, it looks like i'll be hitting up a my old dev tools sooner rather than later.   But py3.11 is acceptable, I just have a personal dislike because it added a bunch of annoying deprecation messages (iirc).  But I'll give it a try.

If it has HIP built in (and yes, I did look at TheRock) that means ComfyUI running natively on Windows, unless I'm misreading something.  That's pretty brave stuff.

[edit] oh... just read your git profile... you're not playing around :)  also, isn't ray-tracing the thing that nvidia totally pwns amd with?
[2nd edit] oh this is an amd repo, sorry amd.  it's not your fault you can't be best at everything -- we still love you.  though your h264 acceleration, not so much.

---

### 评论 #29 — sfinktah (2025-06-09T06:54:53Z)

@jammm that worked amazingly well.  absolutely no issues.  runs a workflow that uses DisTorch with the new phantom_wan, worked faster and used less vram that Zluda.  I documented the install process and made it into a .bat file for others.  https://gist.github.com/sfinktah/85459b3a9bcf959d6c3ace7e777cb66e 

---

### 评论 #30 — sfinktah (2025-06-14T12:39:40Z)

@jammm That actually didn't seem like enough, so I took a few hours and with the help of an LLM I wrote a more comprehensive guide.  I also got Wan2GP working, which was a bonus.  Guide is at https://github.com/sfinktah/amd-torch/ if it is of any use to you, or anyone else reading this issue.

---
