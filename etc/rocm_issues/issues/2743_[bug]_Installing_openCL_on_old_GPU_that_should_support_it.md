# [bug]: Installing openCL on old GPU that should support it

> **Issue #2743**
> **状态**: closed
> **创建时间**: 2023-12-18T00:07:41Z
> **更新时间**: 2024-11-06T15:22:03Z
> **关闭时间**: 2024-11-06T15:22:03Z
> **作者**: BarbzYHOOL
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2743

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

Hello, I have an AMD Radeon HD 7870 and it should support opencl

I'm on POPOS 22.04 and I managed to install these:
amdgpu-install_5.4.50401-1_all.deb  amdgpu-install_5.7.50702-1_all.deb    amdgpu-install_5.5.50503-1_all.deb 

Install with 5.7 == impossible to work, it doesn't find some packages (spent 1h on google and no one has any solution)

For both below, I had to install in top of that mesa-opencl-icd
Install with 5.4 == i didn't notice errors but it doesn't work in the end
Install with 5.5 == several errors, and it doesn't work either

"clinfo" gives me 2 platforms but always 0 devices

I cannot find any solution, everybody just say to retry reinstalling with different options, it makes no sense
I installed with --use-case=opencl (or without this) and --opencl=legacy

### Operating System

pop os 22.04

### GPU

Radeon HD 7870 

### ROCm Component

_No response_

---

## 评论 (23 条)

### 评论 #1 — xiaobo1025 (2023-12-18T01:56:01Z)

Hello, I have recently failed to install ROCm on my windaos10 system. Can you tell me how to install it? 
Thank you very much.

---

### 评论 #2 — illwieckz (2023-12-22T00:13:47Z)

@xiaobo1025 Please create your own issue for your own problem: [here](https://github.com/ROCm/ROCm/issues/new/choose). 🙂️

---

### 评论 #3 — illwieckz (2023-12-22T00:20:56Z)

Hi, @BarbzYHOOL the AMD Radeon HD 7870 is a GCN1 device. The ROCm driver never supported this card and AMD has no plan to support it ever.

The AMD driver for this card is fglrx, more precisely “AMD Radeon Software Crimson Edition 15.12 Proprietary Linux” from the year 2015 and you need Ubuntu 14.04.2 or Ubuntu 12.04.4 (yeas, distributions from year 2014 or 2012). In other hand, AMD has no solution for you.

The legacy Orca legacy driver which is newer than fglrx may list your device but I never seen it working with any GCN1 device I tried. The less-legacy Orca legacy driver (the one you get with the `--opencl=legacy` option) will even not list your GPU.

Your only options are the Mesa OpenCL drivers, the most complete one for AMD GCN1 devices is rusticl.

Your only true hope with a GCN1 card like the AMD Radeon HD 7870 is to use rusticl. A tutorial is coming in the following comment. I made the following tutorial generic (not just for you), but I verified that your card is supported by this other driver.

---

### 评论 #4 — illwieckz (2023-12-22T00:21:48Z)

## Installing latest Mesa rusticl OpenCL driver for GCN/RDNA/CDNA AMD graphics card on Ubuntu Linux and derivatives

Here is a generic tutorial to install the latest Mesa rusticl driver for all GCN and RDNA cards on Ubuntu-derivated distributions like Pop OS or Linux Mint (Ubuntu based). To adapt this tutorial to non-Ubuntu distributions, the key thing is 1. to get _very recent_ Mesa OpenCL drivers, 2. to use the `RUSTICL_ENABLE='radeonsi'` environment variable trick.

This only works for OpenCL, there is no Mesa HIP drivers. ROCm is the only HIP driver for AMD cards on Linux so if your card is not supported by ROCm you can't use HIP at all.

To know if your graphics card is supported by the rusticl driver, search for your graphics card name on [techpowerup](https://www.techpowerup.com/gpu-specs/) website. If the page for your graphics card says the architecture of the graphics card is either GCN, RDNA or CDNA, this tutorial is for you. The TeraScale architectures are not supported yet by rusticl.

First you need to install the Mesa OpenCL drivers, I recommend you to also install the `clinfo` tool for the next instructions (to check if everything works).

Install the [Oibaf PPA repository](https://launchpad.net/~oibaf/+archive/ubuntu/graphics-drivers), this will provide you updated Mesa drivers and then rusticl:

```sh
sudo add-apt-repository 'ppa:oibaf/graphics-drivers'
sudo apt-get update
sudo apt-get dist-upgrade
```

Then you install the Mesa OpenCL drivers, the second command will disable the `clover` OpenCL driver which is now less good than rusticl, and keep rusticl enabled:

```sh
sudo apt-get install 'mesa-opencl-icd' 'clinfo'
sudo dpkg-divert --divert '/etc/OpenCL/vendors/mesa.icd.disabled' --rename '/etc/OpenCL/vendors/mesa.icd'
```

Then before you run your application, set some environment variable, let's try with `clinfo` first:

```sh
export RUSTICL_ENABLE='radeonsi'
clinfo --list
```

The environment variable makes sure you enable rusticl for AMD Radeon cards. The rusticl driver is still experimental and then not installed by default.

If that works for you, to make this variables permanent, edit a profile file:

```sh
sudo nano '/etc/profile.d/rusticl.sh'
```

Then paste this content:

```sh
export RUSTICL_ENABLE='radeonsi'
```

And save the file. Close your session and reopen.

Now, simply doing this should work:

```sh
clinfo --list
```

This should print you something like this (with other card name):

```
Platform #0: rusticl
 `-- Device #0: AMD Radeon PRO W7600 (gfx1102, LLVM 15.0.7, DRM 3.56, 6.5.0-14-generic)
```

To completely revert to your previous state and uninstall everything we did, you would do:

```sh
sudo rm '/etc/profile.d/rusticl.sh'
sudo dpkg-divert --rename --remove '/etc/OpenCL/vendors/mesa.icd'
sudo apt-get autoremove --purge 'mesa-opencl-icd' 'clinfo'
sudo ppa-purge 'ppa:oibaf/graphics-drivers'
```

And you would have to close and re-open your session.

I'm not an AMD employee, but this may save you a lot of time. I'm not paid to give you this help but I was passing by while dealing with some other ROCm issues and thought I could help you. I maintain some information about what driver supports what GPU here: https://gitlab.com/illwieckz/i-love-compute/ . If I saved your life you may find ways to thank me. 😉️

---

### 评论 #5 — BarbzYHOOL (2023-12-26T23:56:15Z)

> Hi, @BarbzYHOOL the AMD Radeon HD 7870 is a GCN1 device. The ROCm driver never supported this card and AMD has no plan to support it ever.
> 
> The AMD driver for this card is fglrx, more precisely “AMD Radeon Software Crimson Edition 15.12 Proprietary Linux” from the year 2015 and you need Ubuntu 14.04.2 or Ubuntu 12.04.4 (yeas, distributions from year 2014 or 2012). In other hand, AMD has no solution for you.
> 
> The legacy Orca legacy driver which is newer than fglrx may list your device but I never seen it working with any GCN1 device I tried. The less-legacy Orca legacy driver (the one you get with the `--opencl=legacy` option) will even not list your GPU.
> 
> Your only options are the Mesa OpenCL drivers, the most complete one for AMD GCN1 devices is rusticl.
> 
> Your only true hope with a GCN1 card like the AMD Radeon HD 7870 is to use rusticl. A tutorial is coming in the following comment. I made the following tutorial generic (not just for you), but I verified that your card is supported by this other driver.

what about trying one of the AMD driver "Linux" and try to compile it for my own distribution? it seems like they have given this option on AMD driver page

And thank you very much for the tutorial, I'm gonna do this in the upcoming days. First I'll remove everything else I added.

Btw why keep the "clover" thing? why not remove it all?

---

### 评论 #6 — BarbzYHOOL (2023-12-28T00:42:45Z)

@illwieckz 
I had installed all of these before opening the issue, what should I uninstall and keep?

```
  54    install amdgpu-install_5.4.50401-1_all.deb                                           2023-12-12 02:24:38 CET           3    me (1000)    
  55    install opencl-headers ocl-icd-libopencl1 clinfo                                     2023-12-12 03:06:54 CET           4    me (1000)    
  56    install mesa-opencl-icd                                                              2023-12-13 00:55:57 CET          13    me (1000)    
  58    install vainfo                                                                       2023-12-16 00:58:30 CET           1    me (1000)    
  59    install mesa-va-drivers                                                              2023-12-16 23:05:28 CET           1    me (1000)    
  60    history undo 56                                                                      2023-12-17 23:43:04 CET          10    me (1000)    
  61    install amdgpu-install_5.7.50702-1_all.deb                                           2023-12-18 00:01:25 CET           2    me (1000)    
  62    install amdgpu-install_5.5.50503-1_all.deb                                           2023-12-18 00:26:14 CET           2    me (1000)    
  63    install mesa-opencl-icd                                                              2023-12-18 00:48:47 CET          10    me (1000) 
```

---

### 评论 #7 — illwieckz (2023-12-28T02:36:49Z)

As root:

```sh
apt-mark auto opencl-headers ocl-icd-libopencl1
amdgpu-uninstall
apt-get autoremove --purge amdgpu-install
rm /etc/modprobe.d/blacklist-radeon.conf /etc/modprobe.d/blacklist-amdgpu.conf
update-initramfs -k all -u
```

Some commands may be useless (the `update-initramfs` one), or report some errors (the `rm` one), depending on what you have installed or not, but doing them will not do harm if not needed.

_Before rebooting_, make sure that this command reports nothing:

```
grep -ER 'blacklist radeon$|blacklist amdgpu$' /etc/modprobe.d/
```

If it report some file, delete the said file and re-run `update-initramfs -k all -u` _before rebooting_.

---

### 评论 #8 — BarbzYHOOL (2023-12-29T00:14:30Z)

the modprobe files were kinda empty but i removed them

also those commands did not remove some of the stuff amdgpu installed like `amdgpu-core amdgpu-dkms-firmware amdgpu-pro-core autoconf automake autotools-dev grub-common grub-efi-amd64 grub-efi-amd64-bin   grub-efi-amd64-signed grub2-common libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm2-amdgpu m4 mokutil ocl-icd-libopencl1-amdgpu-pro os-prober shim-signed`


the update-initramfs command returned:

```
update-initramfs: Generating /boot/initrd.img-6.4.6-76060406-generic
cryptsetup: WARNING: Resume target cryptswap uses a key file
W: Possible missing firmware /lib/firmware/amdgpu/ip_discovery.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/vega10_cap.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/sienna_cichlid_cap.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/navi12_cap.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/psp_13_0_6_sos.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/aldebaran_cap.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/gc_11_0_0_toc.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/sdma_4_4_2.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/sienna_cichlid_mes1.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/sienna_cichlid_mes.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/navi10_mes.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/gc_11_0_3_mes.bin for module amdgpu
```

and many more, and I'm on an older kernel so I feel like i'm gonna get screwed when rebooting

---

### 评论 #9 — illwieckz (2023-12-29T05:32:12Z)

For the remaining packages, well, if you're sure all of them were installed by `amdgpu-install`, then remove them all.
If you're note sure, you should remove at least `amdgpu-core amdgpu-dkms-firmware amdgpu-pro-core ocl-icd-libopencl1-amdgpu-pro libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm2-amdgpu`.

You can totally ignore the `W: possible missing firmware` messages, they are abouts GPUs you don't have. Those messages mean your kernel is more recent than your firmwares, and the missing firmwares are those of newer GPUs you don't have. All you have to do is to make sure `linux-firmware` is installed.

---

### 评论 #10 — BarbzYHOOL (2023-12-29T19:11:05Z)

ok it all worked. For those extra packages, I had noted them down, but since I reinstalled another amdgpu-install once, I suppose I have other useless packages installed, but I may find them back in apt log

Everything works atm, in fact when I installed the previous drivers, it gave me some errors. Now I'm gonna do what you said to install the right drivers and tell you the result, thanks

---

### 评论 #11 — BarbzYHOOL (2023-12-31T00:15:17Z)

Ok @illwieckz  it printed one device:

```
Platform #0: Clover
 `-- Device #0: PITCAIRN (radeonsi, , LLVM 15.0.7, DRM 2.50, 6.2.6-76060206-generic)
```

Now running a miner using OpenCl, I get this:
```
OpenCL driver detected.
Number of OpenCL supported GPUs: 0 
```
Another:
```
[2023-12-31 01:14:25] Found 1 OpenCL platforms, but none is AMD, NVIDIA OR INTEL
```

I guess I'm doomed

---

### 评论 #12 — illwieckz (2023-12-31T04:02:40Z)

> Ok @illwieckz it printed one device:
> 
> ```
> Platform #0: Clover
>  `-- Device #0: PITCAIRN (radeonsi, , LLVM 15.0.7, DRM 2.50, 6.2.6-76060206-generic)
> ```

This is progressing!

Your GPU is properly detected, but it is detected by the `clover` driver, not the `rusticl` one. Mesa has two OpenCL drivers, the older and less complete `clover`, and a newer and more complete `rusticl`, you better want to use rusticl.

In my tutorial there was some instructions to disable Clover, but don't worry, keep it for now.

Does the `/etc/OpenCL/vendors/rusticl.icd` file exist?

You can check for its existence this way:

```
file '/etc/OpenCL/vendors/rusticl.icd'
```

> Now running a miner using OpenCl, I get this:
> 
> ```
> OpenCL driver detected.
> Number of OpenCL supported GPUs: 0 
> ```

Since Clover is incomplete, tt's possible that the device is ignored because it misses some important required things. Though usually Clover is enough for non-graphics applications…

We still need to make rusticl work in case of rusticl is good with this one.

> Another:
> 
> ```
> [2023-12-31 01:14:25] Found 1 OpenCL platforms, but none is AMD, NVIDIA OR INTEL
> ```

For this one, you're probably screwed, as the developper seems to have written a white list of drivers and doesn't care about other drivers. The purpose of OpenCL is to have a single code and to run it on any OpenCL driver. You may check if the software has an option to continue anyway, otherwise it may require patching of the software. The software is explicitly looking for a specific AMD driver or a set of specific AMD drivers (like fglrx, Orca, PAL or ROCm), and doesn't check for OpenCL compatibility, what it should do. This is very bad practice and it's the miner developer's fault. I would report that issue to the miner developer.

---

### 评论 #13 — BarbzYHOOL (2024-01-01T00:19:16Z)

I didn't run the command to disable Clover because I thought the command would rename in the other sense, I didn't realize it was to disable Clover lol. I had to adapt some commands to my fish shell etc... that's why I diverged a bit.
I also ran "upgrade" and not "dist-upgrade" because I didn't want to update my kernel, I guess it didn't matter it still did -__-'

Now I ran the disabling command.

```
/etc/OpenCL/vendors/rusticl.icd: cannot open `/etc/OpenCL/vendors/rusticl.icd' (No such file or directory)
```
No file, so "clinfo --list" gives nothing now

@illwieckz 

---

### 评论 #14 — BarbzYHOOL (2024-01-02T22:55:58Z)

@illwieckz Since I disabled clover, i cannot read any video, no OpenGl lol

---

### 评论 #15 — BarbzYHOOL (2024-01-06T21:41:18Z)

@illwieckz hey sorry to call you again, but I'm waiting for a last reply (just in case there is a solution) before I roll back all the changes of the last entire month, if you have any other idea to solve this or time to reply else just tell me and i'll roll back

---

### 评论 #16 — illwieckz (2024-01-11T13:59:20Z)

Hmm, @BarbzYHOOL for some reasons I only got a notice for the closing, not for the mentions. 🤔️

So I'm sorry to answer this late.

Disabling Clover cannot remove OpenGL at all, make sure `libglx-mesa0` is installed, and make sure a kernel module is loaded. What is the output of `lsmod | grep -E 'radeon|amdgpu'`?

Make sure you have removed all files doing `blacklist radeon` or `blacklist amdgpu` in `/etc/modprobe.d` and updated initramfs as indicated here: https://github.com/ROCm/ROCm/issues/2743#issuecomment-1870768714

---

### 评论 #17 — BarbzYHOOL (2024-01-12T01:26:45Z)

@illwieckz 
```
libglx-mesa0 23.3.0-1pop0~1702935939~22.04~67e417a [Pop!_OS Release/jammy main]
├── is installed and upgradable to 23.3.2-1pop0~1704238321~22.04~36f1d0e
└── free implementation of the OpenGL API -- GLX vendor library
```


```
lsmod | grep -E 'radeon|amdgpu'                                                                                                      2.3s|02:19:51
amdgpu              14774272  0
iommu_v2               24576  1 amdgpu
drm_buddy              20480  1 amdgpu
gpu_sched              57344  1 amdgpu
radeon               2101248  34
video                  69632  2 amdgpu,radeon
i2c_algo_bit           16384  2 amdgpu,radeon
drm_suballoc_helper    16384  2 amdgpu,radeon
drm_ttm_helper         12288  2 amdgpu,radeon
ttm                   106496  3 amdgpu,radeon,drm_ttm_helper
drm_display_helper    217088  2 amdgpu,radeon
drm_kms_helper        258048  3 drm_display_helper,amdgpu,radeon
drm                   708608  22 gpu_sched,drm_kms_helper,drm_suballoc_helper,drm_display_helper,drm_buddy,amdgpu,radeon,drm_ttm_helper,ttm
```

```
rm /etc/modprobe.d/blacklist-radeon.conf /etc/modprobe.d/blacklist-amdgpu.conf                                                     0.2s|02:22:51
rm: cannot remove '/etc/modprobe.d/blacklist-radeon.conf': No such file or directory
rm: cannot remove '/etc/modprobe.d/blacklist-amdgpu.conf': No such file or directory
```

```
╰─# set RUSTICL_ENABLE 'radeonsi'                                                                                                        
╰─# clinfo --list                                                                                                                             02:22:27
---------------------
```
Nothing

---

### 评论 #18 — BarbzYHOOL (2024-01-20T00:23:22Z)

I waited too long and now my automatic backups have been deleted so I cannot rollback and I still can try to make this work if you know what to do @illwieckz 

---

### 评论 #19 — BarbzYHOOL (2024-02-01T01:01:43Z)

I uninstalled everything and I still have log errors everyday after boot
![image](https://github.com/ROCm/ROCm/assets/29780637/718228c0-78f2-4d3a-82e9-759a64c8c0e3)
UBSAN: array-index-out-of-bounds in /build/linux-7T0Dsf/linux-6.6.6/drivers/gpu/drm/radeon/si_dpm.c:6868:32

@illwieckz 

---

### 评论 #20 — jon-gao-yang (2024-08-31T03:49:52Z)

> ## Installing latest Mesa rusticl OpenCL driver for GCN/RDNA/CDNA AMD graphics card on Ubuntu Linux and derivatives
> 

> ```shell
> sudo apt-get install 'mesa-opencl-icd' 'clinfo'
> sudo dpkg-divert --divert '/etc/OpenCL/vendors/mesa.icd.disabled' --rename '/etc/OpenCL/vendors/mesa.icd'
> ```
> ```shell
> export RUSTICL_ENABLE='radeonsi'
> clinfo --list
> ```

the ubuntu rusticl tutorial posted above worked for me. I have an AMD Radeon RX 580 GPU and Ubuntu 24.04.1 (noble). Rusticl was included in noble's 'mesa-opencl-icd' package, and all I needed to do was install it and set the environment variable RUSTICL_ENABLE='radeonsi'. 

I realize this post may come too late to solve the original issue but I wanted to record how I got OpenCL working on AMD GPU for future readers

---

### 评论 #21 — illwieckz (2024-08-31T18:02:47Z)

Thanks @jon-gao-yang for the feedback! 👍️

Indeed with Noble no PPA should be needed (though a PPA may provide a more up-to-date features), I may update the tutorial in regard to that. 🙂️

---

### 评论 #22 — schung-amd (2024-10-16T18:56:17Z)

Hi @BarbzYHOOL, sorry for the delay. Are you still experiencing those log errors?

---

### 评论 #23 — schung-amd (2024-11-06T15:21:52Z)

Converting this to a discussion, as some great advice has been given here on getting old hardware to work. As stated earlier in this thread, we don't officially support this hardware (or Pop OS for that matter), but future users with similar configurations may find this guidance useful.

---
