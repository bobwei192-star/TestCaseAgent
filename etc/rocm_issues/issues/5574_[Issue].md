# [Issue]:

> **Issue #5574**
> **状态**: closed
> **创建时间**: 2025-10-27T01:28:21Z
> **更新时间**: 2025-11-01T00:35:09Z
> **关闭时间**: 2025-11-01T00:35:08Z
> **作者**: tplaiho777
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5574

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

### TL;DR

ROCm 7.0.2 on RDNA3 (RX 7900 XTX / gfx1100) causes a black screen on Ubuntu 24.04 **unless `--usecase=graphics` is included** during installation.

The installer allows:
```bash
sudo amdgpu-install --usecase=rocm,hip,opencl
```
but this breaks the graphical stack after reboot.

Only:
```bash
sudo amdgpu-install --usecase=graphics,rocm,hip,opencl
```
prevents the black screen.

Additionally,  
`https://repo.radeon.com/amdgpu/7.0.2/ubuntu` is missing a valid GPG key  
(`NO_PUBKEY 9386B48A1A693C5C`), forcing fallback to `/amdgpu/7.0/` repo.

---

## Full Report

### System Info

- GPU: Radeon RX 7900 XTX (gfx1100, RDNA3)
- OS: Ubuntu 24.04 LTS
- ROCm tested: 7.0.2
- amdgpu-install: 30.10.2.0-30100200
- Desktop: Xorg & Wayland (both affected)
- Kernel: `<uname -r>` (RDNA3 compatible)

---

### Steps to Reproduce

```bash
sudo amdgpu-install --usecase=rocm,hip,opencl --accept-eula
sudo reboot
```

Result: boot → **black screen** (no display output after init)

---

### Expected Behavior

The system should still boot to a functional desktop environment even without `--usecase=graphics`. ROCm should not break the display stack on a desktop GPU.

---

### Actual Behavior

- DKMS module builds correctly
- `modprobe amdgpu` returns 0 **before** reboot
- Kernel initializes GPU fine
- After reboot, **Xorg/Wayland fails to start** (black screen)
- Only TTY is reachable, GUI cannot start

---

## Root Cause Analysis

This is caused by a **userspace mismatch** between ROCm’s compute stack and the graphics stack on RDNA3.

When `--usecase=graphics` is **not** specified:

| Layer             | Status     | Notes |
|------------------|------------|-------|
| Kernel / DKMS     | ✅ loads   | module OK |
| ROCm runtime      | ✅ loads   | HIP/OpenCL OK |
| Display stack     | ❌ fails   | ICD mismatch |
| Mesa/graphics ICD | ❌ broken  | lost alignment with ROCm userspace |

RDNA3 requires a **unified graphics + compute stack**, otherwise the graphics session fails at login display.

This behavior is not documented.

---

### Workaround (Confirmed)

```bash
sudo amdgpu-install --usecase=graphics,rocm,hip,opencl
```

This forces a unified ICD/userspace stack and prevents the black screen.

---

## Secondary Issue: GPG Key Missing for 7.0.2

The repo:

```
https://repo.radeon.com/amdgpu/7.0.2/ubuntu
```

is missing a valid GPG signing key  
`NO_PUBKEY 9386B48A1A693C5C`.

This blocks DKMS/graphics dependency resolution and forces users to revert to:
```
https://repo.radeon.com/amdgpu/7.0/ubuntu
```

This also is not documented.

---

## What Should Be Fixed

1. Restore valid GPG signature for `/amdgpu/7.0.2/ubuntu`.
2. Document that RDNA3 desktop GPUs **require `--usecase=graphics`**.
3. If installer detects `gfx1100`, warn or auto-append `--usecase=graphics`.
4. Alternatively: fail install gracefully rather than breaking desktop boot.

---

### Impact

This affects **all RDNA3 desktop GPUs** trying to install ROCm 7.x with the default/typical flags.

The current behavior silently bricks the graphical environment and requires offline recovery or full rollback.



### Operating System

Ubuntu Studio 24.04.03 LTS

### CPU

AMD Ryzen 7 

### GPU

AMD RADEON RX 7900 XTX

### ROCm Version

ROCm 7.0.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

In general I think that ROCm update should be possible to do with a one command only. 

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — ianbmacdonald (2025-10-27T14:11:50Z)

On the gpg key, it has not changed for ROCm or Instinct recently.  7.0.1 and 7.0.2 use the same key, so there is probably an issue with you apt sources.  If they existed prior to running the amdgpu-install wrapper script, I might guess you did not opt to replace your existing versions with the distribution maintainers.  

If you share your current /etc/apt/sources.list.d/amdgpu.list and /etc/apt/sources.list.d/rocm.list file contents should provide all the information required to understand why you are getting the NO_PUBKEY error above.  

---

### 评论 #2 — harkgill-amd (2025-10-27T19:36:10Z)

I was able to reproduce the GPG error - it doesn't occur after a regular `sudo apt install ./amdgpu-install_7.0.2.70002-1_all.deb` -> `sudo apt update` though once you actually invoke the script with flag `--accept-eula`, the error presents itself. There have been a couple changes in repo.radeon recently that could be causing this - will dig into this, thanks for bringing it up. @ianbmacdonald, if you get a chance, could you also try running `amdgpu-install` with the `--accept-eula` to see if you can repro as well? 

As for the black screen, I don't see this on my end with or without the `--graphics` usecase + your configuration. For reference, ROCm on Radeon does recommend applying this usecase if you're working with a display connected https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html#graphics-usecase. We don't force the usecase to allow for users to run in a headless configuration as well.

EDIT: Just wanted to add, if you're not using the `workstation` usecase w/ amdgpu-install, `--accept-eula` isn't actually doing anything. You can remove it from your install command entirely.

---

### 评论 #3 — tplaiho777 (2025-10-30T14:54:46Z)

1. I first intall ROCm 7.0.1. Everything works just fine. 
2. Then I try to remove 7.0.1 and update it with 7.0.2. 
3. The end result is as I have described. 

In general I would say that this kind of update process is entirely pain. It should be possible to update from 7.0.1 to 7.x.x with one command only: sudo apt update rocm - and thats it. As far as this is not possible I keep this as beta version, no matter what you say. 

---

### 评论 #4 — harkgill-amd (2025-10-30T15:06:50Z)

I definitely agree that a one command upgrade process would remove a lot of the confusion. This however, won't be an issue as we move to using TheRock for our release infrastructure https://rocm.docs.amd.com/en/7.9.0-preview/about/release-notes.html#rocm-core-sdk-7-9-0-release-notes. With a shift to using ROCm python wheels, upgrading and managing multiple user space installations will be much simpler. 

> Then I try to remove 7.0.1 and update it with 7.0.2.

Can you share the exact steps you use to remove and update ROCm? 

---

### 评论 #5 — tplaiho777 (2025-10-31T15:51:56Z)

Fresh Ubuntu 24.04 LTS install (RX 7900 XTX)

1. Installed AMD repo + amdgpu-install .deb
2. Ran installation *without* graphics stack:

    sudo amdgpu-install --usecase=rocm,hip,opencl --accept-eula -y

3. Kernel module built successfully
4. Verified before reboot:

    sudo modprobe amdgpu
    echo $?  → 0

5. Reboot → system boots to a black screen (no X/Wayland session)
   Only TTY works (Ctrl+Alt+F3)

Workaround that avoids the issue:

    sudo amdgpu-install --usecase=graphics,rocm,hip,opencl --accept-eula -y

So the black screen only happens when installing ROCm stack *without* the graphics stack on RDNA3.

---

### 评论 #6 — tplaiho777 (2025-10-31T23:29:28Z)

It seems that the problem is solved with 7.1.0 version, or I did something seriously wrong with my earlier attemps. 

Now I simply:

```
sudo apt autoremove rocm
sudo apt autoremove rocm-core
```
and also

```
# Remove the repositories
sudo rm /etc/apt/sources.list.d/rocm.list

# Clear the cache and clean the system
sudo rm -rf /var/cache/apt/*
sudo apt clean all
sudo apt update

```

Then I installed normally accepting distributors settings: 

```
wget https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb
sudo apt install ./amdgpu-install_7.1.70100-1_all.deb
sudo apt update
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm
```
and it all went smoothly. No black screens of TTY, only pure correct function. I will later test system stability and speed better. 




---

### 评论 #7 — tplaiho777 (2025-11-01T00:35:09Z)

https://gravitymark.tellusim.com/report/?id=46e4976a61ce158395f035d3b5410a5509fb50e0

I think my computer and GPU with ROCm is just fine?

---
