# [Issue]: Support for Kernel 6.15

> **Issue #5086**
> **状态**: closed
> **创建时间**: 2025-07-22T17:14:56Z
> **更新时间**: 2025-07-23T16:44:57Z
> **关闭时间**: 2025-07-22T19:23:14Z
> **作者**: Blaze-Leo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5086

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

So I got a 9000 series card, and to be able to control the fan curves (very bad premade curve, literally at 50% when junction temperature reaches 100), but I need 6.15 to run on LACT. Is there any update on when 6.15 will be supported? Also I have the adrenaline software on Windows as dual boot. Is there any way to load a custom fan profile as the default into the GPU? that would save a little trouble.

### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen 7 5600x

### GPU

9060XT

### ROCm Version

6.4.2



---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-07-22T18:54:42Z)

Hi @Blaze-Leo. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-07-22T19:23:14Z)

Hi @Blaze-Leo, thanks for reaching out! Unfortunately, we currently have no public information regarding when/if 6.15 is going to be supported. And as far as I know there is no method to add a "default profile" to the GPU that works across OS. Sorry for not being able to offer much help in this case...Please feel free to follow up if you need help setting up fan curves on either OS, and we will be happy to help. Thanks! 

---

### 评论 #3 — Blaze-Leo (2025-07-22T23:50:58Z)

How to modify the fan curves of a 9060XT in Ubuntu 24.04 and kernel 6.14. I looked into past issues and something called overdrive which uses a command called modprobe, has now become obsolete in ROCm 6.4 . I couldn't find any other information and `rocm-smi` gives this message `you cannot do this on this system` when using `setfan` method.

---

### 评论 #4 — Blaze-Leo (2025-07-23T03:49:14Z)

Hey, I just found out that enabling `AMD overclocking` option under `OC` in LACT allows me to change all the option including fan speed and voltage stuff, although I can't change the `Zero RPM` setting, its fine anyways.

---

### 评论 #5 — tcgu-amd (2025-07-23T16:44:57Z)

@Blaze-Leo, thanks for the update. Glad you got it working! 

---
