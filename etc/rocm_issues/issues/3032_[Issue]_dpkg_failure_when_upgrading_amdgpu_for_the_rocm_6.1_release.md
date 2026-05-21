# [Issue]: dpkg failure when upgrading amdgpu for the rocm 6.1 release

> **Issue #3032**
> **状态**: closed
> **创建时间**: 2024-04-17T14:48:41Z
> **更新时间**: 2024-10-08T14:09:27Z
> **关闭时间**: 2024-10-08T14:09:27Z
> **作者**: ye-luo
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/3032

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

```
Preparing to unpack .../libllvm17.0-amdgpu_1%3a17.0.60100-1756574.20.04_amd64.deb ...
Unpacking libllvm17.0-amdgpu:amd64 (1:17.0.60100-1756574.20.04) ...
dpkg: error processing archive /var/cache/apt/archives/libllvm17.0-amdgpu_1%3a17.0.60100-1756574.20.04_amd64.deb (--unpack):
 trying to overwrite '/opt/amdgpu/lib/x86_64-linux-gnu/llvm-17.0/lib/libLLVM-17.so', which is also in package libllvm17.0.60000-amdgpu:amd64 1:17.0.60000-1697589.20.04
dpkg-deb: error: paste subprocess was killed by signal (Broken pipe)
Errors were encountered while processing:
 /var/cache/apt/archives/libllvm17.0-amdgpu_1%3a17.0.60100-1756574.20.04_amd64.deb
E: Sub-process /usr/bin/dpkg returned an error code (1)
```
while upgrading amdgpu due to rocm 6.1 release.

### Operating System

ubuntu 20.04.6 LTS

### CPU

AMD EPYC 7282 16-Core Processor

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

```
sudo apt update
sudo apt dist-upgrade
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — Vexi23 (2024-04-17T17:34:10Z)

Can confirm


`Przygotowywanie do rozpakowania pakietu .../libllvm17.0-amdgpu_1%3a17.0.60100-1756574.22.04_amd64.deb ...
Rozpakowywanie pakietu libllvm17.0-amdgpu:amd64 (1:17.0.60100-1756574.22.04) ...
dpkg: błąd przetwarzania archiwum /var/cache/apt/archives/libllvm17.0-amdgpu_1%3a17.0.60100-1756574.22.04_amd64.deb (--unpack):
 próba nadpisania "/opt/amdgpu/lib/x86_64-linux-gnu/llvm-17.0/lib/libLLVM-17.so", który istnieje także w pakiecie libllvm17.0.60002-amdgpu:amd64 1:17.0.60002-1718217.22.04
dpkg-deb: błąd: podproces wklej został zabity sygnałem (Przerwany potok)
Przygotowywanie do rozpakowania pakietu .../libllvm17.0-amdgpu_1%3a17.0.60100-1756574.22.04_i386.deb ...
Rozpakowywanie pakietu libllvm17.0-amdgpu:i386 (1:17.0.60100-1756574.22.04) ...
dpkg: błąd przetwarzania archiwum /var/cache/apt/archives/libllvm17.0-amdgpu_1%3a17.0.60100-1756574.22.04_i386.deb (--unpack):
 próba nadpisania "/opt/amdgpu/lib/i386-linux-gnu/llvm-17.0/lib/libLLVM-17.so", który istnieje także w pakiecie libllvm17.0.60002-amdgpu:i386 1:17.0.60002-1718217.22.04
dpkg-deb: błąd: podproces wklej został zabity sygnałem (Przerwany potok)
Wystąpiły błędy podczas przetwarzania:
 /var/cache/apt/archives/libllvm17.0-amdgpu_1%3a17.0.60100-1756574.22.04_amd64.deb
 /var/cache/apt/archives/libllvm17.0-amdgpu_1%3a17.0.60100-1756574.22.04_i386.deb
E: Sub-process /usr/bin/dpkg returned an error code (1)
`

**OS**

22.04.4LTS

**CPU**

5600X

**GPU**

7900GRE

**ROCm Ver**

6.0.2





---

### 评论 #2 — Wedge009 (2024-04-17T23:35:43Z)

~What kernel/s are you using? This doesn't bode well for #2993 -> #2939.~

Sorry, realised this is an issue with llvm, not amdgpu-dkms.

---

### 评论 #3 — ShNURoK42 (2024-04-18T14:39:45Z)

I have the same issue.
You can try this to slove it.
```
# sudo apt --fix-broken install
# sudo dpkg --force-all -i /var/cache/apt/archives/libllvm17.0-amdgpu_1%3a17.0.60100-1756574.20.04_amd64.deb
# sudo apt upgrade
```

---

### 评论 #4 — erkinalp (2024-04-27T13:22:27Z)

@ShNURoK42 don't do that if you have a GNOME desktop installed: https://bugs.launchpad.net/ubuntu/+bug/2060391

---

### 评论 #5 — ppanchad-amd (2024-07-04T18:18:16Z)

@ye-luo 

The issue may be due to incomplete uninstallation of graphics driver before installing a new driver. Please try the steps below before installing new amdgpu and rocm.

  sudo amdgpu-repo --clean
  sudo amdgpu-install --uninstall
  sudo apt autoremove
  sudo mv /etc/apt/sources.list.d/amdgpu.list /etc/apt/sources.list.d/amdgpu.list.$$
  sudo mv /etc/apt/sources.list.d/rocm.list /etc/apt/sources.list.d/rocm.list.$$

It is recommended to use amdgpu-install to install amdgpu and rocm. If you use apt, then you need to uninstall amdgpu and rocm before updating apt repo for new release of amdgpu and rocm, then install amdgpu and rocm since the apt repo changes.

Hope that helps!

---

### 评论 #6 — ye-luo (2024-07-05T21:14:20Z)

@ppanchad-amd thank you for the message. I understood a clean uninstall allows me to avoid hassles. However, the issue I raised here is to see if direct upgrading can be correctly handled specifically `libllvm17.0-amdgpu` package.

---

### 评论 #7 — schung-amd (2024-09-24T14:48:51Z)

Hi @ye-luo, have you experienced this in recent ROCm releases? I was unable to reproduce this issue with the upgrade from ROCm 6.2 to 6.2.1 on Ubuntu 22.04 with the following steps:

- Install ROCm 6.2 using the package manager according to https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.2.0/install/native-install/ubuntu.html
- Register the repository sources for both the kernel-mode driver and ROCm packages according to https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.2.1/install/native-install/ubuntu.html
- sudo apt update
- sudo apt dist-upgrade

The installation completes successfully. I see 
```
Preparing to unpack .../11-libllvm18.1-amdgpu_1%3a18.1.60201-2038383.22.04_amd64.deb ...
Unpacking libllvm18.1-amdgpu:amd64 (1:18.1.60201-2038383.22.04) over (1:18.1.60200-2009582.22.04) ...
```
which does not produce an error on my end.

---

### 评论 #8 — schung-amd (2024-10-08T14:09:27Z)

Closing as I cannot reproduce this on current versions of ROCm. Feel free to comment if you are still experiencing this issue with ROCm 6.2 and beyond and we can reopen it.

---
