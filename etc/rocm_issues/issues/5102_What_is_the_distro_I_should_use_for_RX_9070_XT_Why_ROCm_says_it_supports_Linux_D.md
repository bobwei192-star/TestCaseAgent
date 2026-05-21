# What is the distro I should use for RX 9070 XT? Why ROCm says it supports Linux Distros which can't even recognize RX 9070 XT due to outdated Kernel and Mesa?

> **Issue #5102**
> **状态**: closed
> **创建时间**: 2025-07-25T12:20:32Z
> **更新时间**: 2025-08-08T10:20:05Z
> **关闭时间**: 2025-08-01T13:57:42Z
> **作者**: Lonceg
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5102

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Hi,

I've been using Windows for the most part and I have tried hopping on to Linux after buying AMD GPU.

I wanted to try doing some AI experimenting with RX 9070 XT. I installed supported Ubuntu version, followed the guide on ROCm 6.4.1 and it didn't really work for me. Ubuntu 24.04.02 with 6.8 Kernel didn't recognize the GPU.

I've tried some other distros and landed on Arch Linux. Being bleeding edge with newer Kernel at least it recognizes the GPU. I tried installing ROCm from pacman repository and it also didn't work for me. Basically one of the packages for Python itself constantly failed to install. ROCm packages installed but no idea if they work.

To be honest I wanted to try out Fedora the most due to it being more recent than Ubuntu, and more secure by default than Arch. But then I learned Fedora 42 doesn't support 6.4.1 yet, and likely this version will be available with Fedora 43.

At this point I honestly have no idea what to do to use this GPU for AI. What distro should I try and what guide to follow. After following the official ROCm guide I've been pretty much stuck with chat GPT. And I am pretty disappointed in it since it has been pretty much 5 months since I have bought the GPU. All the stable recommended distros don't seem to support ROCm 6.4.1 or have outdated kernel for RX 9070 XT which means I am forced to use bleeding edge. I have worked with RTX 2060 before and it took some tinkering but it worked on Windows in the end.

There is only one video I have found where somebody has made it work on OpenSUSE and I am wondering if I should switch my distro completely to Tumbleweed just because of this video: https://youtu.be/yCCoQ72DBpM?si=-lJKNVMzD6fnZtt3

---

## 评论 (10 条)

### 评论 #1 — ppanchad-amd (2025-07-25T15:45:25Z)

Hi @Lonceg. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — harkgill-amd (2025-07-25T17:46:01Z)

Hi @Lonceg, Ubuntu 24.04 is both supported and recommended for use with ROCm on Radeon GPUs as highlighted in our [OS support matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html#os-support-matrix). While the supported kernel for 24.04 is technically 6.11, the 6.8 kernel should work just fine as well. Could you give the following steps a try to first remove any existing ROCm installations from your system,
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
 ```
Then reinstall ROCm 6.4.1 with,
```
sudo apt install python3-setuptools python3-wheel
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb
sudo apt install ./amdgpu-install_6.4.60401-1_all.deb
amdgpu-install -y --usecase=graphics,rocm
```
After following these steps, you should see your 9070 listed in the output of `rocminfo`. If this still isn't the case, please provide the output of the following so we can get a better picture of what's going on,
1. `uname -r`
2. Complete `dmesg` and `sudo dkms status` output
3. `lspci | grep VGA`
4. `rocm-smi`
5. `lsmod | grep amdgpu`

---

### 评论 #3 — sofiageo (2025-07-26T16:35:10Z)

> I tried installing ROCm from pacman repository and it also didn't work for me.

If you are still on Arch you can also try [opencl-amd-dev](https://aur.archlinux.org/packages/opencl-amd-dev) from the AUR. It's currently on version 6.4.2 and I've also uploaded PKBUILDS for 7.0 beta in the comments. They both seem to work fine so far.

---

### 评论 #4 — Lonceg (2025-07-27T15:05:01Z)

Thanks for your responses, @harkgill-amd and @sofiageo. I decided to reinstall Ubuntu. I have some questions, but please don't hate on me as I just want to understand some things, and as said before I am new to Linux.

> After following these steps, you should see your 9070 listed in the output of rocminfo. If this still isn't the case, please provide the output of the following so we can get a better picture of what's going on,

    uname -r
    Complete dmesg and sudo dkms status output
    lspci | grep VGA
    rocm-smi
    lsmod | grep amdgpu

I followed your steps which I also found here: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html

Also, is this basically a combination of both ROCm and GPU drivers? From here: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html

I have reinstalled Ubuntu 24.04.02 from scratch. When running from USB it asked me if I would like to update the installer. I selected yes. I think that was a mistake as it seems to have installed my OS with 6.14 kernel? Do I have to re download Ubuntu and make it not update itself before install?

rocminfo 
`ROCk module is NOT loaded, possibly no GPU devices`
uname -r
`6.14.0-24-generic`
sudo dkms status
`amdgpu/6.12.12-2187269.24.04, 6.14.0-24-generic, x86_64: installed`
lspci | grep VGA 
`28:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 48 [Radeon RX 9070/9070 XT/9070 GRE] (rev c0)`
rocm-smi 
`ERROR:root:Driver not initialized (amdgpu not found in modules)`
lsmod | grep amdgpu
``

The last one returns nothing

sudo lshw -C display would return following
`description: VGA compatible controller
       product: Navi 48 [Radeon RX 9070/9070 XT/9070 GRE]
       vendor: Advanced Micro Devices, Inc. [AMD/ATI]
...
`

Also after a reboot, GPU doesn't transmit any sound to my monitor via DisplayPort, issue I had before with Ubuntu, and something I didn't have on Arch. The same for settings like Refresh Rate which is stuck at 60 Hz. With fresh Ubuntu I could change it to 165Hz.

`sudo amdgpu-uninstall` gave me back sound.




---

### 评论 #5 — harkgill-amd (2025-07-28T14:17:01Z)

No problem, happy to answer any questions you have.

> Also, is this basically a combination of both ROCm and GPU drivers?

The [ROCm on Radeon](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html) releases are an extension of our regular [ROCm releases](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html). The key difference is that the Radeon releases support graphical workloads such as Blenders whereas the regular releases are intended for headless (no display) configurations. Both releases include the ROCm packages and GPU drivers in their installation steps.

The issue you're currently facing is due the ROCm 6.4.1 kernel driver not being compatible with the 6.14 kernel you have installed. To resolve this, you can simply upgrade to the latest ROCm 6.4.2 release. You can do this by following the uninstall steps highlighted here https://github.com/ROCm/ROCm/issues/5102#issuecomment-3119739407, then install ROCm 6.4.2 following the instructions [here](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script).



---

### 评论 #6 — Lonceg (2025-08-01T13:56:29Z)

I've tried going back to Windows and using WSL2 with Ubuntu. I've followed these guides: `https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html` and `https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html`

[rocminfo.txt](https://github.com/user-attachments/files/21549474/rocminfo.txt)

I've tried using comfyui, I have made sure not to overwrite the pytorch modules. I before I have also tried with `pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.4` straight from the PyTorch website.

[comfyui.txt](https://github.com/user-attachments/files/21549505/comfyui.txt)

---

### 评论 #7 — harkgill-amd (2025-08-01T14:32:02Z)

From the output of rocminfo, your WSL instance is working correctly and can detect your GPU. The `RuntimeError: No HIP GPUs are available` has to do with your PyTorch installation specifically. Could you provide the output of the following in your WSL instance? 

1. `python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'`  
2. `python3 -c 'import torch; print(torch.cuda.is_available())'`

This'll help narrow down which portion of the installation is failing.


---

### 评论 #8 — Lonceg (2025-08-03T13:57:47Z)

@harkgill-amd I redid everything from the start, even reinstalling Ubuntu in WSL2. It finally runs although I have yet to test any models in comfyui.

<img width="2450" height="1195" alt="Image" src="https://github.com/user-attachments/assets/4010b080-e1da-4d5a-b62c-b3580d097ca4" />

Perhaps there were some issues caused by me installing the PyTorch directly from the website before installing the .whl.

As mentioned before I followed these guides:
`https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html`
`https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html`
`https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/comfyui/installcomfyui.html`

Only difference is that I installed .whl pytorch in virtual environment along with comfyui requirements.

Once I test it more and get it working, I will try running it with Docker as well.

Edit: I just inferenced Hunyuan model to generate a 3d model. I am very happy that this works on AMD.

@harkgill-amd regarding just the ROCm, how would you advise to control the Kernel version if I decided to use Linux instead of WSL2? Let's say I want my OS to use the recent Kernel or use slightly more bleeding edge distro like Fedora or Arch (@sofiageo are the packages in pacman enough? I am reluctant to use AUR for example.)

Or should I just dual boot specific version of Ubuntu with specific Kernel version if I want to use AI?

---

### 评论 #9 — sofiageo (2025-08-03T17:10:49Z)

@Lonceg Yes the AUR packages should be enough in most cases. You can check the PKGBUILD yourself, it is just installing the Ubuntu packages which are also verified with a SHA256 hash for extra security. In most cases it works the same as with Ubuntu. You can even try the 7.0 beta if you want (I have it installed on my PC since it was released and it is working fine).

Regarding your question about the kernel version, I think it doesn't matter for most cases. And it won't matter in the future either. If you read the blog post for ROCm gets [modular](https://rocm.blogs.amd.com/ecosystems-and-partners/instinct-gpu-driver/README.html) it says:

> Users choosing to use amdgpu from the stock Linux kernels may choose to skip all the installation documentation for ROCm that references the Instinct driver.

p.s I'm not an expert, just commenting my experience so far.

---

### 评论 #10 — TR4UM4H4WK (2025-08-08T10:20:05Z)

CachyOS has been perfect for me. Much better performance on my brand new ASUS Prime rx 9070 XT than my old RTX 4070 Ti too. I haven't had one issue yet. I havent had to make many adjustments in steam launch options. all my games just work. i play darktide, cyberpunk, death stranding, marvel rivals. all at 4k. I also have 5800x3d and 64 gb ram. i even get the best frame rates i have ever had now in star citizen. play a bunch of other games, all work great. 

---
