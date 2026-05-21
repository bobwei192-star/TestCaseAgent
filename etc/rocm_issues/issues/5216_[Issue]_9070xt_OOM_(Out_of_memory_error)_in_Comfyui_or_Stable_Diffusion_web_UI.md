# [Issue]: 9070xt OOM (Out of memory error) in Comfyui or Stable Diffusion web UI

> **Issue #5216**
> **状态**: open
> **创建时间**: 2025-08-21T15:04:13Z
> **更新时间**: 2025-09-05T18:48:40Z
> **作者**: fangwen1102
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5216

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

After installing Rocm and the driver according to the official documentation 

(https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)

,python=3.10, I installed Torch using 

pip3 install torch torchvision --index-url https://download.pytorch.org/whl/rocm6.4

. I then git cloned ComfyUi, using the -r flag to install dependencies, and then directly launched python main.py with the default workflow and 512x512 resolution. This caused an OOM error and crash during VAE decoding. I tried using --vae-cpu on ComfyUI, but the speed was incredibly slow. SDL VAE processing typically takes several minutes. This issue persists on Linux, WSL, and Windows. Is it a 9070 issue? It hasn't been resolved since June. The system was newly installed, with no other software installed or variables set.

The image cannot be generated normally in sd1.5. Using sdxl 1024x1024 will also cause OOM errors in VAE. When checking the GPU status in the Windows environment, only 8G video memory is used during the sampling process, but when it comes to VAE decoding, 16G video memory will be used instantly.

### Operating System

Linux Ubuntu 24.04.3 LTS, WSL2 Ubantu 24.04, Windows10

### CPU

14600kf

### GPU

9070xt

### ROCm Version

6.4.1, 6.4.3

### ROCm Component

_No response_

### Steps to Reproduce

1.Install the new ubantu24.04.3

2.Install rocm

wget https://repo.radeon.com/amdgpu-install/6.4.3/ubuntu/noble/amdgpu-install_6.4.60403-1_all.deb
sudo apt install ./amdgpu-install_6.4.60403-1_all.deb
sudo apt update
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm

3.Install driver

wget https://repo.radeon.com/amdgpu-install/6.4.3/ubuntu/noble/amdgpu-install_6.4.60403-1_all.deb
sudo apt install ./amdgpu-install_6.4.60403-1_all.deb
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo apt install amdgpu-dkms

sudo reboot
4.git clone https://github.com/comfyanonymous/ComfyUI.git

5.
cd ~/ComfyUI
pip3 install -r requirements.txt

cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager
cd ComfyUI-Manager
pip3 install -r requirements.txt

6.
cd ~/ComfyUI
python main.py

After the window starts, click the first sample workflow. If it prompts that the file is missing, click Download, put the downloaded file in the checkpoint directory, and then click Run to execute the workflow.
Then you will get OOM error.

Then your PC will become very lag and you will get an OOM error after a while.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (11 条)

### 评论 #1 — ppanchad-amd (2025-08-21T17:26:12Z)

Hi @fangwen1102. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-08-21T18:45:34Z)

@fangwen1102, Thanks for reaching out! I am sorry you are experiencing issues, but yeah, there has been few issues with ComfyUI on 9070xt. 

https://github.com/ROCm/ROCm/issues/4846
https://github.com/ROCm/ROCm/issues/4742

The issue is in part due to ComfyUI's own design, which can be fixed by this patch (https://github.com/comfyanonymous/ComfyUI/pull/8289)

and the other part is due to MIOpen still yet to complete port all algorithms to 9070 yet. We are working on this and it should be available soon. 

Again, apologies for the poor experience....

---

### 评论 #3 — briansp2020 (2025-08-21T19:44:06Z)

@tcgu-amd Do you have ETA for MIOpen for 9070? I just bought Radeon™ AI PRO R9700 and it is not performing well. I was hoping that complete RDNA4 support would be released by the time AMD release a pro grade product with AI in the name...

---

### 评论 #4 — fangwen1102 (2025-08-21T22:55:55Z)

> [@fangwen1102](https://github.com/fangwen1102), Thanks for reaching out! I am sorry you are experiencing issues, but yeah, there has been few issues with ComfyUI on 9070xt.
> 
> [#4846](https://github.com/ROCm/ROCm/issues/4846) [#4742](https://github.com/ROCm/ROCm/issues/4742)
> 
> The issue is in part due to ComfyUI's own design, which can be fixed by this patch ([comfyanonymous/ComfyUI#8289](https://github.com/comfyanonymous/ComfyUI/pull/8289))
> 
> and the other part is due to MIOpen still yet to complete port all algorithms to 9070 yet. We are working on this and it should be available soon.
> 
> Again, apologies for the poor experience....

What about Stable Diffusion web UI? Is there any solution at present?

---

### 评论 #5 — tcgu-amd (2025-08-22T18:23:45Z)

> > [@fangwen1102](https://github.com/fangwen1102), Thanks for reaching out! I am sorry you are experiencing issues, but yeah, there has been few issues with ComfyUI on 9070xt.
> > [#4846](https://github.com/ROCm/ROCm/issues/4846) [#4742](https://github.com/ROCm/ROCm/issues/4742)
> > The issue is in part due to ComfyUI's own design, which can be fixed by this patch ([comfyanonymous/ComfyUI#8289](https://github.com/comfyanonymous/ComfyUI/pull/8289))
> > and the other part is due to MIOpen still yet to complete port all algorithms to 9070 yet. We are working on this and it should be available soon.
> > Again, apologies for the poor experience....
> 
> What about Stable Diffusion web UI? Is there any solution at present?

The ComfyUI issue shouldn't be present with Stable Diffusion, but under the hood both rely on MIOpen. 

---

### 评论 #6 — fangwen1102 (2025-08-23T00:27:43Z)

> > > [@fangwen1102](https://github.com/fangwen1102), Thanks for reaching out! I am sorry you are experiencing issues, but yeah, there has been few issues with ComfyUI on 9070xt.
> > > [#4846](https://github.com/ROCm/ROCm/issues/4846) [#4742](https://github.com/ROCm/ROCm/issues/4742)
> > > The issue is in part due to ComfyUI's own design, which can be fixed by this patch ([comfyanonymous/ComfyUI#8289](https://github.com/comfyanonymous/ComfyUI/pull/8289))
> > > and the other part is due to MIOpen still yet to complete port all algorithms to 9070 yet. We are working on this and it should be available soon.
> > > Again, apologies for the poor experience....
> > 
> > 
> > What about Stable Diffusion web UI? Is there any solution at present?
> 
> The ComfyUI issue shouldn't be present with Stable Diffusion, but under the hood both rely on MIOpen.

I encountered the same problem in Stable Diffusion web UI, which also appeared in the final vae decoding process

---

### 评论 #7 — fangwen1102 (2025-08-23T13:07:09Z)

> > > [@fangwen1102](https://github.com/fangwen1102), Thanks for reaching out! I am sorry you are experiencing issues, but yeah, there has been few issues with ComfyUI on 9070xt.
> > > [#4846](https://github.com/ROCm/ROCm/issues/4846) [#4742](https://github.com/ROCm/ROCm/issues/4742)
> > > The issue is in part due to ComfyUI's own design, which can be fixed by this patch ([comfyanonymous/ComfyUI#8289](https://github.com/comfyanonymous/ComfyUI/pull/8289))
> > > and the other part is due to MIOpen still yet to complete port all algorithms to 9070 yet. We are working on this and it should be available soon.
> > > Again, apologies for the poor experience....
> > 
> > 
> > What about Stable Diffusion web UI? Is there any solution at present?
> 
> The ComfyUI issue shouldn't be present with Stable Diffusion, but under the hood both rely on MIOpen.

The same steps, just change the address of comfyui to the address of 1111's webui warehouse, and then use any sd1.5 model. The computer will be very lag during the final vae decoding, and then report an oom error.

---

### 评论 #8 — tcgu-amd (2025-08-25T18:52:14Z)

@fangwen1102, yeah, both share the same MIOpen dependency, so right now there's no optimized algorithm for VAE yet. ComfyUI has an additional issue of forcing fp32 for VAE, but even without that it is still slow. 

---

### 评论 #9 — githust66 (2025-09-02T07:31:19Z)

> [@fangwen1102](https://github.com/fangwen1102), yeah, both share the same MIOpen dependency, so right now there's no optimized algorithm for VAE yet. ComfyUI has an additional issue of forcing fp32 for VAE, but even without that it is still slow.

Hello, can't the problem of slow VAE be solved? Will ROCM7 solve it?

---

### 评论 #10 — tcgu-amd (2025-09-02T14:40:40Z)

> > [@fangwen1102](https://github.com/fangwen1102), yeah, both share the same MIOpen dependency, so right now there's no optimized algorithm for VAE yet. ComfyUI has an additional issue of forcing fp32 for VAE, but even without that it is still slow.
> 
> Hello, can't the problem of slow VAE be solved? Will ROCM7 solve it?

Yes it can be solved. We are adding winograd support and it should be available in ROCm 7.x. Thanks! 

---

### 评论 #11 — Monger-man (2025-09-05T18:41:48Z)

What is the time table on ROCm 7.x? At the moment not only is VAE decoding glacially slow, but I'm also having issues where color output is corrupted.  This is in Wan, other outputs are correct, IE. flux, Qwen-Image.  But all the encodes/decodes are slow beyond reason. I just received my r9700 and have been pulling my hair out wondering what I was doing wrong.

---
