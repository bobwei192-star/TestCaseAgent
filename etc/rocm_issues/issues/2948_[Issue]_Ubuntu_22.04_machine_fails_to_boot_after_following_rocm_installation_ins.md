# [Issue]: Ubuntu 22.04 machine fails to boot after following rocm installation instructions

> **Issue #2948**
> **状态**: closed
> **创建时间**: 2024-03-06T15:34:51Z
> **更新时间**: 2024-08-30T07:53:23Z
> **关闭时间**: 2024-03-08T02:01:45Z
> **作者**: samuelpmish
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/2948

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

I followed the instructions described in https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html

Everything seemed to install without issue. I got a note about some secure boot authorization that would take place on the next reboot to enable AMD's third-party drivers, and set up a password for that. After shutting down, the next time the machine started, I only saw a black screen. I thought that this might be related to the graphics card driver update, so I tried all the different HDMI and displayport ports on the GPU and motherboard, but none of them worked.

After that, I powered down the machine and tried rebooting again, to see if anything different would happen. Now, one of the HDMI ports on the GPU does produce an image to the screen, but it just splashes the motherboard vendor logo briefly before reverting to a black screen with a blinking white cursor in the top left. Subsequent reboots have the same effect.

I'd like to include detailed info about my OS and GPU, but I can't successfully boot the machine any more to run those commands. I know its running ubuntu 22.04, with an intel 12700K CPU and a Radeon VII GPU, but I don't know anything more specific than that.

Can anyone help me figure out what to do to recover from this borked installation? 

### Operating System

Ubuntu 22.04

### CPU

intel 12700k

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — nartmada (2024-03-07T17:25:16Z)

Internal ticket has been created for this issue.

---

### 评论 #2 — kentrussell (2024-03-07T17:56:18Z)

Can you check if SecureBoot is enabled? If so, the kernel won’t load. A DKMS install taints the kernel, which means that it’s no longer “secure”. SecureBoot being enabled in the SBIOS means that it won’t load a tainted kernel.

---

### 评论 #3 — akondrat-amd (2024-03-08T00:36:58Z)

Follow Method1 here to enter BIOS to disable secure boot: https://www.tomshardware.com/reviews/bios-keys-to-access-your-firmware,5732.html

---

### 评论 #4 — samuelpmish (2024-03-08T02:01:45Z)

Thanks, I was hoping to find a solution that didn't involve disabling secure boot, but it does resolve the issue.

---

### 评论 #5 — nama1arpit (2024-08-30T07:53:21Z)

@samuelpmish I faced a similar issue but after installation and while trying to run an application with rcom. **Were you able to find some solution?**

My secure boot is already disabled and it didn't help. I have tried [this grub hack](https://askubuntu.com/a/1251028) to enter UI but it seems like everything is slow and only runs on one monitor. 

---
