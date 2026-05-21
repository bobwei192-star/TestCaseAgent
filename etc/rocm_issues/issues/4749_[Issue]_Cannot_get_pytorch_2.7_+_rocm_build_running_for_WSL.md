# [Issue]: Cannot get pytorch 2.7 + rocm build running for WSL

> **Issue #4749**
> **状态**: closed
> **创建时间**: 2025-05-16T14:08:18Z
> **更新时间**: 2025-07-29T12:44:35Z
> **关闭时间**: 2025-05-26T14:15:57Z
> **作者**: deep1401
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4749

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Hey,
I'm working at Transformer Lab and recently took on what I thought would be a straightforward task - setting up ROCm for Windows to run some ML workloads. Two weeks and countless frustrations later, I'm reaching out to see if anyone here has successfully navigated these waters.
I initially got things working on my Linux machine with the same hardware configuration. After that to test if the integration works on WSL, I did a dualboot to Windows and opened WSL (Ubuntu 24.04). For hardware context, we have a single AMD Radeon 7900 XTX (gfx11100).

Here's what we've tried and the roadblocks we're hitting:

## WSL Integration Issues:

- Attempted to set up our API installation on bare-metal WSL
- Discovered it's impossible to set up rocm-smi on WSL due to limitations mentioned on the AMD installer page
- This makes tracking GPU usage extremely difficult since we can't properly use the pyrsmi package (which is supposed to be the ROCm equivalent to CUDA's pynvml)

## PyTorch Installation Nightmares on WSL:

- Official installation docs recommend using pre-built binaries
- Problem is, there are no pre-built binaries available yet for torch 2.7 + rocm 6.4
- Tried using the Linux wheel (torch2.7+rocm6.3) but it doesn't work on WSL - torch.cuda.is_available() can't detect anything
- Even tried the classic AMD installer trick of replacing runtime libraries, but no success with this torch2.7+rocm6.3 installation

For context, we installed ROCm 6.4, but we're trying to download ROCm 6.3 packages for PyTorch since the 6.4 wheels aren't available yet.

How do you all run ML workloads on Windows and ROCm with a current version of PyTorch?!

Really hoping to tap into the collective knowledge of this community, as the official documentation hasn't been much help with our specific use case.

Thanks in advance!

### Operating System

WSL (Ubuntu 24.04)

### CPU

AMD Ryzen 5 7600X

### GPU

1 x AMD Radeon 7900 XTX

### ROCm Version

ROCm 6.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (17 条)

### 评论 #1 — ppanchad-amd (2025-05-16T14:17:19Z)

Hi @deep1401. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-05-16T18:32:02Z)

Hi @deep1401, 

> Discovered it's impossible to set up rocm-smi on WSL due to limitations mentioned on the AMD installer page
This makes tracking GPU usage extremely difficult since we can't properly use the pyrsmi package

There were efforts to enable parts of rocm-smi in WSL in order to support ML workloads which depend on it, but I'm not sure what the status of that is; I'll reach out for more info regarding pyrsmi specifically.

> For context, we installed ROCm 6.4, but we're trying to download ROCm 6.3 packages for PyTorch since the 6.4 wheels aren't available yet.

At the moment only specific ROCm releases + Adrenalin driver versions are supported in WSL; see the compatibility matrices at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html. Currently the latest supported releases are ROCm 6.3.4 and Adrenalin 25.3.1. The compatibility matrices also list our officially supported Pytorch versions, although nightly may work. Our officially supported stable wheels for ROCm 6.3.4 are in https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/.

---

### 评论 #3 — jelacicedin (2025-05-16T18:38:43Z)

Hey man, as mentioned above, 6.4 will not yet work on WSL; i.e. even if you manage to install via amdgpu-install the 7900 XTX will not be recognized to HIP. I was in the same boat before going back to 6.3.4. and then it worked. I managed to run AMDs PyTorch with the gpu through WSL like that.

---

### 评论 #4 — deep1401 (2025-05-16T21:03:05Z)

Hey @jelacicedin, 
This didn't help. I also installed the adrenalin driver 25.3.1 but it still wont show up when I do `torch.cuda.is_available()`. To add this setup of pytorch2.7+rocm works perfectly with my linux system. It creates so many issues when I do it on WSL. Even using docker doesn't help.

---

### 评论 #5 — jelacicedin (2025-05-16T21:33:08Z)

Hey @deep1401 ,

I absolutely understand your pain with the process. The issue definitely lies with AMD and their tutorial. What worked for me was the following. First I installed rocm 6.3 (very important to get this one and not 6.4) via 
```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.4/ubuntu/noble/amdgpu-install_6.3.60304-1_all.deb
sudo apt install ./amdgpu-install_6.3.60304-1_all.deb

amdgpu-install -y --usecase=wsl,rocm --no-dkms
```
from [AMD's own latest WSL ROCM link](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html)

and then I installed PyTorch via 

```
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torch-2.4.0%2Brocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torchvision-0.19.0%2Brocm6.3.4.gitfab84886-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/pytorch_triton_rocm-3.0.0%2Brocm6.3.4.git75cc27c2-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torchaudio-2.4.0%2Brocm6.3.4.git69d40773-cp312-cp312-linux_x86_64.whl
pip3 uninstall torch torchvision pytorch-triton-rocm
pip3 install torch-2.4.0+rocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl torchvision-0.19.0+rocm6.3.4.gitfab84886-cp312-cp312-linux_x86_64.whl torchaudio-2.4.0+rocm6.3.4.git69d40773-cp312-cp312-linux_x86_64.whl pytorch_triton_rocm-3.0.0+rocm6.3.4.git75cc27c2-cp312-cp312-linux_x86_64.whl
```
After doing this, torch worked, but I was still getting False on `torch.cuda.is_available()`. However, what I did then was the following:

```
location=$(pip show torch | grep Location | awk -F ": " '{print $2}')
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
cp /opt/rocm/lib/libhsa-runtime64.so.1.14.0 .
ln -sf libhsa-runtime64.so.1.14.0 libhsa-runtime64.so.1
ln -sf libhsa-runtime64.so.1 libhsa-runtime64.so
```
Essentially you have to replace torch's own libs with those from /opt/rocm (note, it must be /opt/rocm, not /opt/rocm-6.4 which is what I tried when I first erroneously installed rocm-6.4, which is definitely not yet supported on WSL). After doing all this, `torch.cuda.is_available()` started returning True and overall working.



---

### 评论 #6 — deep1401 (2025-05-16T21:52:23Z)

@jelacicedin Thanks for providing those ln -sf steps. Those weren't on AMD's official website but the torch 2.4 worked with this. I made some modifications and now got the torch 2.7 showing cuda available as True as well. Thanks a lot!

---

### 评论 #7 — jelacicedin (2025-05-20T07:39:12Z)

@deep1401 No problem! Should we mark the issue as closed then?

---

### 评论 #8 — schung-amd (2025-05-20T14:43:37Z)

@jelacicedin Did you need to copy the `.so` file? The latest [docs](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html) currently say:

```
4. Update to WSL compatible runtime lib.

location=$(pip show torch | grep Location | awk -F ": " '{print $2}')
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
```

In the [6.3 version](https://rocm.docs.amd.com/projects/radeon/en/docs-6.3/docs/install/wsl/install-pytorch.html) of this page we did have `cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so`; if this is still necessary I'll need to check in with the docs team.


---

### 评论 #9 — jammm (2025-05-25T20:38:01Z)

@deep1401 if you'd like to try windows native, try the (unofficial) 2.7 wheels from https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x

---

### 评论 #10 — jelacicedin (2025-06-30T08:33:05Z)

@schung-amd sorry for the late reply, my GitHub notifications were misconfigured. Yes, I did need to copy the .so files to get everything running. However, since the latest AMD Adrenaline drivers dropped, I've been able to setup the whole process via Docker in my WSL, so I'm not sure if this is still the case with the latest on the website, as I have been running solely via Docker. If you would like me to try recreate the issue, please let me know!

Best,
Edin 

---

### 评论 #11 — schung-amd (2025-06-30T14:30:03Z)

@jelacicedin Thanks for the update! Forgot to update here, but we did find a flaw in our documentation from the process you wrote here. As of ROCm 6.4.1 for WSL we no longer require this step, but the docs were updated a bit too soon. The 6.3.4 docs at https://rocm.docs.amd.com/projects/radeon/en/docs-6.3.4/docs/install/wsl/install-pytorch.html have been corrected to copy the runtime file over, and moving forward for versions 6.4.1 and onward we will no longer have this step in the documentation. Thanks again!

---

### 评论 #12 — jelacicedin (2025-07-02T16:15:28Z)

@schung-amd thank you for the prompt fix! You guys rock 👍 

---

### 评论 #13 — sfinktah (2025-07-24T08:59:44Z)

> [@deep1401](https://github.com/deep1401) if you'd like to try windows native, try the (unofficial) 2.7 wheels from https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x

And if you need `pynvml` support on Windows, you can try `pip install pynvml-amd-windows` though I only build it as a shim over `ADLXPybind` to cover the bare minimum stats.  Since some of the better stuff in ADLX is "hidden" behind polymorphic versioned structs, my LLM could not easily create python bindings for everything.  But it is easy enough to extend.

---

### 评论 #14 — deep1401 (2025-07-24T09:02:16Z)

Thanks for the pointer on pynvml windows, I will try that out for sure. I solved my torch problem by doing the symlink instructions sent earlier

---

### 评论 #15 — sfinktah (2025-07-25T09:35:10Z)

No worries, I have noticed it crashing a couple of times, but only under very specific circumstances involving ZLUDA, GGUFs and sage_radial / sage_sparse triton compilation.

I am actually taking the reverse of your journey.  Having pretty much mastered the gfx1100 on Windows, I'm embarking on a journey into WSL to see how many issues with torch and triton still require PRs to fix.

So let me give you the benefit of my wisdom wrt windows.

Want ROCm 6.5 (TheRock) native pytorch with sageattention, flash_attention, triton, and suchlike?  Run this handy installation script.

[patientx-native-rocm-3.zip](https://github.com/user-attachments/files/21428365/patientx-native-rocm-3.zip)

Want to go the ZLUDA route, and still get sageattention, flash_attention, triton and suchlike?  Follow the instructions at https://github.com/patientx/ComfyUI-Zluda  then do the patches at https://github.com/patientx/ComfyUI-Zluda/issues/222

My research (as outlined in the above issue) shows that ZLUDA is actually faster and more memory efficient (if a little bit crashy).  Note that the HIP SDK installation part of the ZLUDA instructions can be ignored if you have already run my script, since that installs HIP SDK 6.5 which seems a little less crashy.  Just use this for your `comfyui-n.bat` launch script: https://gist.github.com/sfinktah/85459b3a9bcf959d6c3ace7e777cb66e#file-comfyui-n-bat

Sorry, I know I have described that all terribly... but hopefully you can figure it out.

---

### 评论 #16 — deep1401 (2025-07-28T22:33:35Z)

> > [@deep1401](https://github.com/deep1401) if you'd like to try windows native, try the (unofficial) 2.7 wheels from https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch-gfx110x
> 
> And if you need `pynvml` support on Windows, you can try `pip install pynvml-amd-windows` though I only build it as a shim over `ADLXPybind` to cover the bare minimum stats. Since some of the better stuff in ADLX is "hidden" behind polymorphic versioned structs, my LLM could not easily create python bindings for everything. But it is easy enough to extend.

Thanks for this! Does this not work with WSL? Is there a WSL alternative?

---

### 评论 #17 — sfinktah (2025-07-29T12:44:35Z)

> Thanks for this! Does this not work with WSL? Is there a WSL alternative?

It does **not** work with WSL, because ADLX is a Windows only AMD library.  There was a linux python package https://test.pypi.org/project/pyrsmi/ that might have worked, however some quick tests on a ROCm enabled WSL Ubuntu session and a rocm/pytorch-nightly Docker container both failed to bring joy.

```
# installation 
python -m pip install --index-url https://test.pypi.org/simple/ pyrsmi

# error when running example from test.pypi.org:
cat: /sys/module/amdgpu/initstate: No such file or directory
```

If there really is no way to get basic stats from your GPU on linux (which I find very hard to believe), you could always cheat and run a python socket listener on the windows host and access it from the wsl machine.  

AMD is also the only GPU provider for macOS machines, and IIRC xbox and playstation.  So I'm sure there's a way.

---
