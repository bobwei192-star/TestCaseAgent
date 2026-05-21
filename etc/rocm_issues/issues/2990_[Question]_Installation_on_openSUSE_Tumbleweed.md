# [Question]: Installation on openSUSE Tumbleweed

> **Issue #2990**
> **状态**: closed
> **创建时间**: 2024-04-02T07:36:34Z
> **更新时间**: 2026-05-11T11:10:38Z
> **关闭时间**: 2024-05-07T20:43:19Z
> **作者**: NYBACHOK
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2990

## 描述

Hi. Im trying to install rocm on openSUSE Tumbleweed using [this](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/sles.html) guide from documentation. Application able to use hip, but plasma6 becomes buggy and unstable. It is almost impossible to use OS like that.

So what I'm curious:
1.  Is this my fault or there any additional step specific to openSUSE?
2. Is this possible to install rocm with distrobox and ubuntu container?

CPU: AMD Ryzen 9 7900X
GPU: Radeon 7800XT

---

## 评论 (9 条)

### 评论 #1 — tinchee (2024-04-03T04:58:28Z)

Sorry, I want to ask another question, this seems not very relevant to this issue
It is written in the docs([https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)) that 7800XT does not support Linux, I want to know whether my 7800XT GPU can use Rocm on the Linux?

---

### 评论 #2 — one-lithe-rune (2024-04-03T11:57:29Z)

I run ROCm for things that need HIP on Tumbleweed using the docker image through [distrobox](https://distrobox.it/). I didn't attempt installing the SLES packages directly as my - not necessarily correct - understanding was that SLES and Tumbleweed are sufficiently different that this would be likely to make a mess.

I haven't noticed anything weird happening since the Plasma 6 update other than a wake from sleep issue with X11 that was a Plasma 6 bug, but I haven't been doing ROCm things very much recently.

Doing it this way is workable though not ideal, because you have to switch between the Tumbleweed and Ubuntu context appropriately.

In case it helps, below is my `distrobox.ini` for the ROCm container. This version is set up as rootless (which is distrobox default). This means it also needs - not necessarily sane - changes to `/etc/subgid` (also below, replace 'your_username' as appropriate).

The group and group id shenanigans are needed so that the groups for the video card devices are correctly exposed into the containers. So I would check that your `render` and `video` groups on the Tumbleweed side do have the same gids as for me before just running this as is.

Using a rootful setup is probably more natural for how containers work, and *I think* that would let you avoid some of the mucking about with groups in the init lines. However my memory is that  distrobox that wanted me to enter my root password whenever I enter the box, which was inconvenient.

`distrobox.ini`

```ini
[rocm-rl]
image=docker.io/rocm/dev-ubuntu-22.04:6.0.2-complete
init=false
additional_packages="build-essential libtcmalloc-minimal4 wget git software-properties-common libgl1 libglib2.0-0 neofetch vulkan-tools cmake ninja-build"
additional_flags="--device=/dev/kfd --device=/dev/dri"
init_hooks="add-apt-repository ppa:deadsnakes/ppa;"
init_hooks="apt update -y;"
init_hooks="apt install python3.11 python3.11-venv python3.11-tk -y;"
init_hooks="groupadd -fg 486 host_render;"
init_hooks="groupadd -fg 483 host_video;"
init_hooks="usermod -aG host_render,host_video $LOGNAME;"
init_hooks="export ROCM_PATH=/opt/rocm;"
nvidia=false
pull=false
root=false
replace=true
start_now=false
```

`/etc/subgid`

```
your_username:100000:65536
your_username:0:483
your_username:483:3
your_username:486:1
```

---

### 评论 #3 — NYBACHOK (2024-04-03T12:03:29Z)

@one-lithe-rune Thanks for help! 

---

### 评论 #4 — Rewarp (2024-04-10T08:36:52Z)

Thank you so much for your script. I have been searching for a way to do this in Tumbleweed for years. Finally got it running with your Distrobox setup.

I can also confirm:

> Using a rootful setup is probably more natural for how containers work, and _I think_ that would let you avoid some of the mucking about with groups in the init lines. However my memory is that distrobox that wanted me to enter my root password whenever I enter the box, which was inconvenient.

I changed your `distrobox.ini` file for `root=false` to `root=true`.

To confirm it worked. I installed ComfyUI and monitored the GPU when it did its image generation. Remarkable. We can use our favourite rolling release distro now with ROCm.

---

### 评论 #5 — ppanchad-amd (2024-05-07T19:13:32Z)

@NYBACHOK Do you still require assistance with this issue? If not, please close ticket. Thanks!

---

### 评论 #6 — NYBACHOK (2024-05-07T20:43:19Z)

> @NYBACHOK Do you still require assistance with this issue? If not, please close ticket. Thanks!

Hi. I forgot to close. Thanks for remind

---

### 评论 #7 — torsten-online (2024-07-29T04:07:11Z)

Hi,

I got it work on OpenSUSE Tumbleweed / MicroOS with the Distrobox Container solution, also running in rootless mode!

So, I created just a gist which describes my final solution.

https://gist.github.com/torsten-online/22dd2746ddad13ebbc156498d7bc3a80

Thanks to @one-lithe-rune for providing the input about the distrobox container!

Any comments are welcome,
Have a lot of Fun
Torsten

---

### 评论 #8 — jornfranke (2025-09-23T19:38:55Z)

I also have some instructions: https://jornfranke.codeberg.page/technology-tutorials/immutable-linux-neural-pc/
The main difference is that I use Kalpa Desktop and all the software is installed in rootless distrobox (no need to install drivers or amdgpu outside)

You can now btw. also use a Tumbleweed-Repo for ROCm:
```
sudo zypper ar https://download.opensuse.org/repositories/science:/GPU:/ROCm/openSUSE_Tumbleweed/ ROCm
sudo zypper ref
```

---

### 评论 #9 — SauerNinja (2026-05-11T11:10:38Z)

Thanks for creating this issue, currently doing the same on Leap 16. 

---
