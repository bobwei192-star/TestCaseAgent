# [Issue]: 'Unable to locate package hsa-runtime-rocr4wsl-amdgpu' on win 10 wsl2 ubuntu 22.04.4 LTS ROCm 6.1 (same on 6.02) Radeon 7700 XT

> **Issue #3051**
> **状态**: closed
> **创建时间**: 2024-04-21T10:21:04Z
> **更新时间**: 2024-07-17T15:21:35Z
> **关闭时间**: 2024-07-17T15:21:35Z
> **作者**: incense
> **标签**: ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/3051

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

Trying to install with
sudo amdgpu-install -y --usecase=wsl
throws error 'Unable to locate package hsa-runtime-rocr4wsl-amdgpu'
Not able to find any workaround on the net nor sources to compile.
Any help?

### Operating System

Ubuntu 22.04.4 LTS on wsl

### CPU

AMD Ryzen 5800X

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (19 条)

### 评论 #1 — incense (2024-04-21T10:21:56Z)

ROCm Version is 6.1 (was not selectable)
GPU is Radeon RX 7700 XT (was not selectable)


---

### 评论 #2 — BrandenStoberReal (2024-04-21T21:25:49Z)

Same issue on my machine. (Windows 10 fresh install)

---

### 评论 #3 — Engininja2 (2024-04-21T22:41:31Z)

I think AMD is working on WSL support but it's not public yet. You either need to use Linux with direct access to the GPU, or the HIP SDK for Windows.

---

### 评论 #4 — incense (2024-04-22T06:21:27Z)

> I think AMD is working on WSL support but it's not public yet. You either need to use Linux with direct access to the GPU, or the HIP SDK for Windows.

Well, if you
`sudo amdgpu-install --list-usecase`
it lists as well 
> wsl             (for using ROCm in a WSL context)
>  - ROCr WSL runtime library (Ubuntu 22.04 only)

Thus, in my understanding, the amdgpu driver _should_ support ROCm in the wsl environment out of the box.

---

### 评论 #5 — javenli (2024-04-25T02:07:13Z)

Same issue here. That would be great if wsl is supported.

---

### 评论 #6 — AndrMoura (2024-04-26T16:29:05Z)

Same issue too

---

### 评论 #7 — crosys (2024-04-29T07:38:41Z)

Same issue...

---

### 评论 #8 — incense (2024-04-29T08:29:15Z)

Dear AMD (@saadrahim),
A short info from your end would be highly appreciated.
Many thanks in advance!
With best regards,
Rolf

---

### 评论 #9 — Tweschke3 (2024-05-06T23:04:33Z)

Same problem here. I would be very interested in a solution (@saadrahim)

---

### 评论 #10 — ALParsons (2024-05-07T02:15:08Z)

same issue, following - keen to see rocm/wsl usecase supported (same error for both) in WSL for gpu acceleration

Operating System
Ubuntu 22.04.4 LTS on wsl

CPU
AMD Ryzen 7900

GPU
AMD Radeon RX 7900 XTX

ROCm Version
from package amdgpu-install_6.1.60100-1_all.deb
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html

ROCm Component
ROCm

---

### 评论 #11 — ppanchad-amd (2024-05-09T15:41:06Z)

@incense Currently, it does not support wsl environment out of the box. This is coming very soon! Thanks!

---

### 评论 #12 — rainabba (2024-05-14T21:47:01Z)

> @incense Currently, it does not support wsl environment out of the box. This is coming very soon! Thanks!

So the guide from AMD isn't really reliable right now? https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html

"very soon" meaning days, weeks or months? :D 

---

### 评论 #13 — weikangqi (2024-06-16T16:26:52Z)

same for AMD8845 780M

---

### 评论 #14 — mirh (2024-06-19T20:04:31Z)

https://repo.radeon.com/amdgpu/6.1.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/

---

### 评论 #15 — Thiryn (2024-07-05T13:55:33Z)

I imagine this isn't quite released yet at the [latest](https://rocm.docs.amd.com/en/latest/) docs page is still 6.1.2 at the time of writing Anyone able to run `amdgpu-install --usecase=wsl` with the 2 packages @mirh linked installed?
Seems to me that it is trying to build a kernel module, but there is no kernel header package distributed for WSL afaik. [This thread](https://askubuntu.com/questions/1350457/installing-linux-headers-standard-on-ubuntu-20-04-wsl2) actually seems to indicate that you actually can't load kernel module in WSL2.
Just wondering how to use this. Anyone?

Below, the error I get when installing. 
```shell
$> sudo apt-get install amdgpu-core
$> sudo dpkg -i ./hsa-runtime-rocr4wsl-amdgpu_1.13.0-1789577.22.04_amd64.deb
$> sudo apt-get install rocm-core
$> sudo dpkg -i ./rocminfo4wsl-amdgpu_1.13.0-1789577.22.04_amd64.deb
$> amdgpu-install --usecase=wsl
[...]
Selecting previously unselected package amdgpu-dkms-firmware.
(Reading database ... 81457 files and directories currently installed.)
Preparing to unpack .../amdgpu-dkms-firmware_1%3a6.7.0.60102-1781449.22.04_all.deb ...
Unpacking amdgpu-dkms-firmware (1:6.7.0.60102-1781449.22.04) ...
Selecting previously unselected package amdgpu-dkms.
Preparing to unpack .../amdgpu-dkms_1%3a6.7.0.60102-1781449.22.04_all.deb ...
Unpacking amdgpu-dkms (1:6.7.0.60102-1781449.22.04) ...
Setting up amdgpu-dkms-firmware (1:6.7.0.60102-1781449.22.04) ...
Setting up amdgpu-dkms (1:6.7.0.60102-1781449.22.04) ...
Loading new amdgpu-6.7.0-1781449.22.04 DKMS files...
Building for 5.15.153.1-microsoft-standard-WSL2
Building for architecture x86_64
Module build for kernel 5.15.153.1-microsoft-standard-WSL2 was skipped since the
kernel headers for this kernel does not seem to be installed.
update-initramfs: Generating /boot/initrd.img-added
W: missing /lib/modules/added
W: Ensure all necessary drivers are built into the linux image!
depmod: ERROR: Bad version passed added
cat: /var/tmp/mkinitramfs_QlogIL/lib/modules/added/modules.builtin: No such file or directory
W: Can't find modules.builtin.modinfo (for locating built-in drivers' firmware, supported in Linux >=5.2)
I: The initramfs will attempt to resume from /dev/sdb
I: (UUID=a3a9d864-0b92-492d-89ec-63240fbcdd74)
I: Set the RESUME variable to override this.
depmod: ERROR: Bad version passed added
WARNING: amdgpu dkms failed for running kernel
```


---

### 评论 #16 — mirh (2024-07-05T14:44:07Z)

You are looking at the wrong.. uh, docs sub-domain
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html
The headers problem may instead be WSL2 having updated its kernel away from 5.15 perhaps? Idk. 

---

### 评论 #17 — Thiryn (2024-07-05T15:52:08Z)

`amdgpu-install -y --usecase=wsl,rocm --no-dkms` actually worked. I assume the kernel issue was probably linked to the dkms install?

`rocminfo` shows my gpu now ;) 

I actually double checked the docs and thought I looked at the right place, as that's the same domain from the readme. Might want to add a link to the WSL setup on here https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/ubuntu.html

---

### 评论 #18 — mirh (2024-07-05T16:07:47Z)

That's the linux guide, not wsl

---

### 评论 #19 — harkgill-amd (2024-07-17T15:21:35Z)

Hi @incense, the beta release of WSL with ROCm is out. You can find more information, including installation steps at [Install Radeon Software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html).

If you encounter any issues with `amdgpu-install -y --usecase=wsl,rocm --no-dkms` after fulfilling the prerequisites and installing the ROCm 6.1.3 driver packages, please open a new ticket. Thanks!

---
