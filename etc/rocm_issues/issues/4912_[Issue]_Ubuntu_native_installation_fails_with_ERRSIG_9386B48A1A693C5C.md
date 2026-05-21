# [Issue]: Ubuntu native installation fails with ERRSIG 9386B48A1A693C5C

> **Issue #4912**
> **状态**: closed
> **创建时间**: 2025-06-10T20:27:50Z
> **更新时间**: 2025-06-17T17:25:22Z
> **关闭时间**: 2025-06-17T17:25:22Z
> **作者**: andrew-aladjev
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4912

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am trying to install the ROCm via [the following guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html).

```
OS:
NAME="Ubuntu"
VERSION="25.10 (Questing Quokka)"
```

```
sudo mkdir --parents --mode=0755 /etc/apt/keyrings
wget https://repo.radeon.com/rocm/rocm.gpg.key -O - | gpg --dearmor | sudo tee /etc/apt/keyrings/rocm.gpg > /dev/null
sha1sum /etc/apt/keyrings/rocm.gpg
```
> ececf5eea22ced391975f46ba3e11ad58a12c794

```
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.4.1 noble main" | sudo tee /etc/apt/sources.list.d/rocm.list
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update
```
> Get:4 https://repo.radeon.com/rocm/apt/6.4.1 noble InRelease [2,605 B]                                                                  
> Err:4 https://repo.radeon.com/rocm/apt/6.4.1 noble InRelease                                                                           
>   The following signatures were invalid: ERRSIG 9386B48A1A693C5C

I've tried `sudo gpg --keyserver keyserver.ubuntu.com --recv-keys 9386B48A1A693C5C`, but nothing changed.

### Operating System

Ubuntu 25.10 (Questing Quokka)

### CPU

AMD Ryzen 7 5700G with Radeon Graphics

### GPU

AMD RX 7600 XT

### ROCm Version

ROCM 6.4.1


---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-06-12T16:49:36Z)

Hi @andrew-aladjev, this is likely due to the usage of the 24.04 install instructions on 25.10. I'll give this a try on my end and see if there's any way to workaround this.

---

### 评论 #2 — harkgill-amd (2025-06-13T20:59:55Z)

@andrew-aladjev, I wasn't able to reproduce the `ERRSIG` error on 25.10 though I did notice convert the signing-key would sometimes get stuck. As an alternative, you can follow the quick start installation guide which worked consistently on my end.
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html or simply,

```
wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb
sudo apt install ./amdgpu-install_6.4.60401-1_all.deb
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm amdgpu-dkms
```
Please note that amdgpu-dkms will fail to build for the packaged 6.14.0 kernel as ROCm does not currently support this kernel. Support is expected in a future release and currently being tracked in https://github.com/ROCm/ROCm/issues/4619.

---

### 评论 #3 — harkgill-amd (2025-06-17T17:25:22Z)

Will close this issue out for now as https://github.com/ROCm/ROCm/issues/4619 tracks the 6.14.0 kernel + amdgpu-dkms known build issue. Feel free to leave a comment if you have any questions or concerns and I'll reopen the issue. Thanks!

---
