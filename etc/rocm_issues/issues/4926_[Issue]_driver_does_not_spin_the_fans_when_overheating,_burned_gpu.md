# [Issue]: driver does not spin the fans when overheating, burned gpu

> **Issue #4926**
> **状态**: closed
> **创建时间**: 2025-06-13T20:47:44Z
> **更新时间**: 2025-06-17T12:38:41Z
> **关闭时间**: 2025-06-17T12:38:41Z
> **作者**: mahdoosh1
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4926

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

ERROR:root:Driver not initialized (amdgpu not found in modules)

i have tried everything and have reinstalled the gpu many times. it worked previously but after reboot it suddenly doesn't work
i don't know what has caused it but i know none of known solutions fixed any issues.
last time i ran "amdgpu-install --usecase=graphics,rocm,opencl,hip,dkms"
and once i ran "amdgpu-install --usecase=graphics,rocm,opencl --no-dkms"
none worked. OS uses CPU intergrated graphics and none of the apps (CPU-X, CoreCtrl) detect it
CPU-X says it is there but no drivers or extra info, just device id

the commands above also don't detect GPU:
```
OS:
NAME="Ubuntu"
VERSION="24.04.2 LTS (Noble Numbat)"
CPU: 
model name	: Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz
GPU:
```

by the way i am a little beginner in linux, this is my first time trying linux but i had no issues until recently.
i also had to move root partition and fix grub multiple times because i gave too little storage for ubuntu

### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz

### GPU

AMD Radeon RX 5600 (maybe XT)

### ROCm Version

rocm-core6.4.1/noble 6.4.1.60401-83~24.04 amd64

### ROCm Component

rocminfo

### Steps to Reproduce

i have no idea
here is the history, if it ever helps:

[history.txt](https://github.com/user-attachments/files/20732710/history.txt)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

/opt/rocm/bin/rocminfo --support
ROCk module is NOT loaded, possibly no GPU devices

### Additional Information

[dmesg.txt](https://github.com/user-attachments/files/20732743/dmesg.txt)

---

## 评论 (10 条)

### 评论 #1 — harkgill-amd (2025-06-13T21:10:08Z)

Hi @mahdoosh1, can you try manually loading the modules with `sudo modprobe amdgpu` and rerunning rocm-smi/rocminfo?

Also, 

- Can you check if you have `nomodeset` added in `/etc/default/grub` -> `GRUB_CMDLINE_LINUX_DEFAULT`
- Provide the output of `dkms status`

---

### 评论 #2 — mahdoosh1 (2025-06-13T22:24:56Z)

UPDATE: the problem is fixed, the fix includes:
uninstalling all libraries associated with amdgpu: `amdgpu-uninstall` or `amdgpu-install --uninstall`
going into recovery mode in grub menu
installing in --no-dkms mode `amdgpu-install --usecase=graphics,rocm,opencl,hip --no-dkms`
rebooting (using `reboot`), just to see the white screen saying system failed which is common when exiting recovery mode.
rebooting again to make sure everything is working.

ANSWER TO YOUR QUESTION:
during the install process in recovery mode it did gave me a warning that nomodeset is actually set. let me check that file:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
dkms status outputs nothing, probably because amdgpu was uninstalled

if you need extra info, i am here for you, except it is 2 AM here, so wait 8 hours for me to wake up

---

### 评论 #3 — mahdoosh1 (2025-06-13T23:24:05Z)

i almost forgot, so apparently there is the package `amdgpu` and i installed it before uninstalling,
i don't remember if i reinstalled it afterwards or not

---

### 评论 #4 — harkgill-amd (2025-06-16T15:14:29Z)

> during the install process in recovery mode it did gave me a warning that nomodeset is actually set. let me check that file:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
dkms status outputs nothing, probably because amdgpu was uninstalled

Thanks for checking. That warning is standard in recovery mode, you don't actually have the flag set.

With your fix, you've installed the ROCm user space components alongside Ubuntu's built-in kernel amdgpu driver. This is fine though there's no reason why you shouldn't be able to install the ROCm packaged kernel driver in your current configuration. I did see a couple different `amdgpu-install` commands in your history.txt which could be conflicting with your install. If you're willing to try, I'd recommend removing all previous installations with,
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then reinstalling ROCm 6.4.1 for Ubuntu 24.04 with,
```
wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb
sudo apt install ./amdgpu-install_6.4.60401-1_all.deb
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm amdgpu-dkms
```
If you see any errors during the installation, please be sure to share them. Once the installation has completed, reboot your system and give `rocm-smi`/`rocminfo` a run.

---

### 评论 #5 — mahdoosh1 (2025-06-16T21:06:55Z)

i'm not experienced with linux so i don't want to reinstall the drivers because i'm afraid something can go wrong again.
since the problem is solved, the issue can be closed now.

it might even be my fault for not installing the drivers properly.

---

### 评论 #6 — mahdoosh1 (2025-06-16T21:09:26Z)

if it was not my fault,
most probably the issue is that the "amdgpu" package did not get installed, so I had to install it manually.

---

### 评论 #7 — mahdoosh1 (2025-06-17T08:56:10Z)

Update:
gpu overheated and now it is not outputting anything
why? BECAUSE THE DRIVERS DIDN'T TURN ON THE FAN

---

### 评论 #8 — mahdoosh1 (2025-06-17T08:56:45Z)

where is the amdgpu repository btw
EDIT: it is not open source

---

### 评论 #9 — mahdoosh1 (2025-06-17T09:01:33Z)

i'm very cooked. i used remote connect on windows, then did some investigation
graphics card is recognized
it is working
The stress test succeeded, both AMD software and FurMark
it looks like the gpu is fine
thank god.
STILL IT NEEDS TO BE FIXED

---

### 评论 #10 — mahdoosh1 (2025-06-17T12:38:27Z)

wtf
it just fixed itself after powering the pc down for about 2 hours

crazy

---
