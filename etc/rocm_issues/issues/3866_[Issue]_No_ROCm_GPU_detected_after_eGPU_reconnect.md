# [Issue]: No ROCm GPU detected after eGPU reconnect

> **Issue #3866**
> **状态**: closed
> **创建时间**: 2024-10-05T11:51:05Z
> **更新时间**: 2025-01-10T16:13:30Z
> **关闭时间**: 2024-10-15T13:48:08Z
> **作者**: MihaiBojescu
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 GRE
> **URL**: https://github.com/ROCm/ROCm/issues/3866

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 GRE** (颜色: #ededed)

## 描述

### Problem Description

ROCm sees 0 GPUs available after the eGPU is disconnected and reconnected (concrete use-cases: mobility, sleep mode on laptop). Games work perfectly after reconnecting the enclosure.

### Operating System

Arch Linux

### CPU

12th Gen Intel(R) Core(TM) i7-1260P

### GPU

AMD Radeon RX 7900 GRE

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCK-Kernel-Driver, ROCm, rocm-core, rocminfo

### Steps to Reproduce

1. Boot linux-lts 
2. Connect the eGPU enclosure (ref: [link](https://www.adt.link/product/UT3G.html)) with a Sapphire Pulse RX 7900 GRE
3. `rocminfo` returns 1 detected GPU, `rocm-smi` returns 1 GPU, PyTorch (just sometimes?) detects 1 CUDA GPU
4. Disconnect enclosure
5. Reconnect enclosure
6. `rocminfo` returns 0 detected GPUs, `rocm-smi` returns 2 GPUs, PyTorch (always) detects 0 CUDA GPUs

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
Unable to open /dev/kfd read-write: Invalid argument
mihai is member of render group

### Additional Information

- `sudo dmesg` output: [dmesg.log](https://github.com/user-attachments/files/17266021/dmesg.log)
- `sudo lshw` output: [lshw.txt](https://github.com/user-attachments/files/17267498/lshw.txt)
- package versions:
    - linux-lts: 6.6.52-1
    - linux-firmware: 20240909.552ed9b8-1
    - rocm-core: 6.0.2-2
    - rocminfo: 6.0.2-1
    - rocm-smi-lib: 6.0.2-1
- packages were installed using `pacman`, not using the provided driver from AMD
- booting linux instead of linux-lts does not fix the issue
- rebooting always solves the issue
- tried removing the amdgpu module, did not work
- tried forcefully removing the amdgpu module, resulted in (partial?) kernel panic, needed to reboot
- tried to change the firmware of the eGPU enclosure (provided by manufacturer on manufacturer's page), but without luck


---

## 评论 (10 条)

### 评论 #1 — MihaiBojescu (2024-10-07T12:03:01Z)

If it helps, the problem also seems to manifest in ROCm 6.2.1-1

---

### 评论 #2 — harkgill-amd (2024-10-07T14:45:58Z)

Hi @MihaiBojescu, thanks for providing your steps to reproduce and logs. An internal ticket has been created to further investigate this issue.

---

### 评论 #3 — darren-amd (2024-10-07T19:14:09Z)

Hi @MihaiBojescu,

When you disconnect the eGPU and reconnect it, I don't believe that it is being picked up by the drivers. Since the driver would still be in use, you could try switching to the intel display driver before running the following to reboot the driver:

`sudo modprobe -r amdgpu`
`sudo modprobe amdgpu`

Rebooting would fix the issue, as the driver would be able to pick up the GPU again, and would be the easiest solution. The behavior when disconnecting and reconnecting an eGPU is different from when the computer is put to sleep, as sleeping usually puts the GPU into a low power state rather than disconnecting it.

Taking a look at the documentation for your eGPU enclosure, I see "This product supports hot swapping, but if you need to remove the graphics card, please follow the safety prompts of the graphics card software. You must close 3D software and games before plugging or unplugging." 

![image](https://github.com/user-attachments/assets/5e191908-6f93-4b9d-bf38-a659d27d7b91)

Could you try disconnecting the GPU prior to unplugging it and see if that works? Thanks!


---

### 评论 #4 — MihaiBojescu (2024-10-08T05:42:09Z)

Hi @harkgill-amd, @darren-amd,

Thank you for the responses. I tried running the commands above. Seems like when I cannot remove the driver as it is in use (`modprobe: FATAL: Module amdgpu is in use.`). `nvtop` returns that Gnome shell (`/usr/bin/gnome-shell`) uses it.

![Screenshot From 2024-10-08 08-22-54](https://github.com/user-attachments/assets/4e775e9d-3a91-422d-89ee-793d1117e53a)


When I stop gnome shell such that `nvtop` returns that nothing is using the GPU, and I rerun the commands, the command works perfectly. After I reconnect the GPU (either via cable, power supply, switch on enclosure) or I load the `amdgpu` module, `rocminfo` and `rocm-smi` returns 1 GPU. This is really helpful and I can live with this workaround for a while.

Maybe this is a Gnome-specific bug? I haven't tried with Plasma yet. I'll try with it tomorrow and report back on my findings here. If this happens on Plasma too, I don't really know where to place the issue... Could you help me with a project I could forward this to?

Thank you for the help!

---

### 评论 #5 — darren-amd (2024-10-08T13:28:31Z)

Hi @MihaiBojescu,

Awesome to hear that it works! 

My thinking is that gnome shell isn't dynamically looking for a switch in GPU, and so it continues to use the amdgpu module even after the GPU is unplugged (which isn't allowing you to restart it). I'm not entirely sure if it's checking for a change in GPU so unsure if it's a bug at all. You could try reporting the issue here: https://gitlab.gnome.org/GNOME/gnome-shell/-/issues and see what the intended behavior is for hotplugging GPUs. Thanks!

---

### 评论 #6 — MihaiBojescu (2024-10-12T14:08:27Z)

Hey everyone,

I'm back with some results for KDE Plasma 6.2. Plasma does not use the GPU in `nvtop` when idle (as expected), where on Gnome, `nvtop` reports as the desktop environment is using it (unexpected, why would it if nothing is running on it?).

Some use-cases I tried on Plasma 6.2:
1. When putting the laptop in sleep and waking it up:
    - The system is functional
    - `rocm-smi` reports 1 GPU
    - `rocminfo` reports the device as available
    - `nvtop` reports nothing is using the GPU (as expected)
1. When disconnecting and reconnecting the enclosure with the GPU:
    - The system is functional
    - `rocm-smi` reports 1 GPU
    - `rocm-info` throws an error (`Unable to open /dev/kfd read-write: Invalid argument`) even when using with `sudo`
    - `nvtop` reports nothing using the GPU (as expected)
1. When putting the laptop in sleep, disconnecting the GPU, and then waking it up:
    - The system hard crashes. No command other than hard reboot by power button works (possibly a Linux bug, can ignore)
    - Did not investigate `rocm-smi`, `rocm-info`, `nvtop`. Maybe can try it though through SSH, but I sadly lack the time now.

To fix the second 2nd use-case, I removed the `amdgpu` module and loaded it back again without stopping Plasma. After that, `rocm-info` works as normal. There was no need for hard-restarting the desktop environment like on Gnome (thus, my problem might be a Gnome bug).

I'll leave this for future readers that might encounter this issue (_in case it helps_):
- **If on Gnome**, stop your DE and try to reload `amdgpu`. You should see your GPU in `rocm-info`.
- **If on Plasma**, don't stop your DE and try to reload `amdgpu`. You should see your GPU in `rocm-info`.
- Try not to leave the GPU powered on or to leave it connected when putting your device to sleep. It might result in some hard crashes.

_Late post edit_: Posted the issue on `gnome-shell`'s repository here: https://gitlab.gnome.org/GNOME/mutter/-/issues/3785

---

### 评论 #7 — darren-amd (2024-10-15T13:48:08Z)

Awesome, thanks for the tips! Hopefully it'll help other users in the future.

---

### 评论 #8 — waltercool (2024-12-02T02:54:34Z)

Hey, is there any other option?

My iGPU and dGPU use amdgpu, so can't just "rmmod and modprobe" back again. 

This is annoying because when eGPU is reconnected (bind) to the machine, ROCM doesn't work, but Vulkan llama.cpp works fine for text models.

Kind regards.

---

### 评论 #9 — MihaiBojescu (2025-01-06T12:15:09Z)

Greetings @waltercool,

One option that I think might help for now is using a virtual machine with the eGPU passed-through. It clearly isn't the best option, but it might help out a bit. Could you perhaps open an issue for your use-case?

---

### 评论 #10 — waltercool (2025-01-10T16:13:28Z)

Hi @MihaiBojescu,

I did that few weeks ago at their mailing list https://lists.freedesktop.org/archives/amd-gfx/2024-December/118271.html

Still, ROCm GPU should be detected after dGPU/eGPU is reconnected, but seems like /dev/kfd gets messed up.

---
