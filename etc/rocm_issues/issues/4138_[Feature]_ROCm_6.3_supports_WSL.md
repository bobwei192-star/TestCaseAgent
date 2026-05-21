# [Feature]: ROCm 6.3 supports WSL

> **Issue #4138**
> **状态**: closed
> **创建时间**: 2024-12-07T05:58:49Z
> **更新时间**: 2025-04-07T10:52:33Z
> **关闭时间**: 2025-03-06T21:44:54Z
> **作者**: githust66
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4138

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

ROCm 6.3 supports WSL

### Operating System

WSL2 Ubuntu 22.04

### GPU

7900xt

### ROCm Component

_No response_

---

## 评论 (11 条)

### 评论 #1 — tomkv (2024-12-09T23:59:57Z)

It does, but the amdgpu repo index is broken (intentionally?), so it cannot be installed with `amdgpu-install`.

As a workaround, install manually the `hsa-runtime-rocr4wsl-amdgpu` package for [22.04](https://repo.radeon.com/amdgpu/6.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_24.30-2089753.22.04_amd64.deb) or [24.04](https://repo.radeon.com/amdgpu/6.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_24.30-2089753.24.04_amd64.deb) and then run `amdgpu-install --usecase=...` as usual and  it will be ok.

---

### 评论 #2 — its-so-fluffy (2024-12-13T18:15:40Z)

I hope I am doing this right 
![image](https://github.com/user-attachments/assets/7ac7f26c-135c-41b1-9cb7-b43450d22c51)

run amdgpu-install --usecase=...
![image](https://github.com/user-attachments/assets/bf854152-4509-4c61-9807-998c272a08ed)

Doesn't seem to work I guess I will have to wait and use 6.2.3 until this is fixed


---

### 评论 #3 — tomkv (2024-12-13T20:41:33Z)

Make sure you are starting with clean state. Remove everything from the old install, *including* `amdgpu-install`. They are version-specific, so yours is setting up the 6.2.3 repository (see your second screenshot)

I just tried with a pristine ubuntu 24 image and this worked:

```
$ wget https://repo.radeon.com/amdgpu/6.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_24.30-2089753.24.04_amd64.deb https://repo.radeon.com/amdgpu-install/6.3/ubuntu/noble/amdgpu-install_6.3.60300-1_all.deb

$ sudo dpkg -i ./hsa-runtime-rocr4wsl-amdgpu_24.30-2089753.24.04_amd64.deb ./amdgpu-install_6.3.60300-1_all.deb
```

This will not end-up well, since `hsa-runtime-rocr4wsl-amdgpu` requuires `amdgpu-core` and it isn't installed. We have to fix it.

```
$ sudo apt --fix-broken install
```
and then finally:

```
$ sudo amdgpu-install --usecase=rocm --no-dkms --accept-eula
```

(no need to state `wsl`, it will be added automatically anyway).

Then, 2.4 GB later, rocm is installed:

```
$ rocminfo
WSL environment detected.
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES
...
```

---

### 评论 #4 — its-so-fluffy (2024-12-16T15:15:50Z)

This worked thank you! :) 

---

### 评论 #5 — xCentral (2024-12-22T06:17:32Z)

What's the best way to go on about removing previous amd-gpu's, it keeps installing 6.13 when I'm running amdgpu-install. Preferably without needing to reinstall ubuntu on wsl

Edit: Void on this, needed to use sudo apt-get purge amdgpu-install


---

### 评论 #6 — xCentral (2024-12-22T16:38:40Z)

So I fixed my previous problem but am running into this error when running rocminfo, with 6.3 installed on wsl. root@Power: rocminfo
WSL environment detected.
rocminfo: ./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:113: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed.
Aborted
Can't find anything pertaining to this on the issues.

---

### 评论 #7 — grebdioZ (2025-02-09T13:35:12Z)

> So I fixed my previous problem but am running into this error when running rocminfo, with 6.3 installed on wsl. root@Power: rocminfo WSL environment detected. rocminfo: ./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:113: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed. Aborted Can't find anything pertaining to this on the issues.

I have the exact same issue as @xCentral. Same config as the original poster, just with an xtx, 24.12 Adrenaline drivers installed. There were no error messages in the amdgpu-install output. Any hint on what may be wrong would be hugely appreciated!



---

### 评论 #8 — githust66 (2025-02-09T14:04:03Z)

> > So I fixed my previous problem but am running into this error when running rocminfo, with 6.3 installed on wsl. root@Power: rocminfo WSL environment detected. rocminfo: ./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:113: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed. Aborted Can't find anything pertaining to this on the issues.
> 
> I have the exact same issue as [@xCentral](https://github.com/xCentral). Same config as the original poster, just with an xtx, 24.12 Adrenaline drivers installed. There were no error messages in the amdgpu-install output. Any hint on what may be wrong would be hugely appreciated!

I installed it normally and used it normally, and I didn't find any errors

My installation steps: 
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.2/ubuntu/jammy/amdgpu-install_6.3.60302-1_all.deb
sudo apt install ./amdgpu-install_6.3.60302-1_all.deb
amdgpu-install -y --usecase=wsl,rocm --no-dkms

---

### 评论 #9 — grebdioZ (2025-02-09T15:33:21Z)

@githust66 Thanks for that, I repeated all your steps seemingly successfully, but still get the thunk_proxy error message afterwards.

---

### 评论 #10 — harkgill-amd (2025-03-06T21:44:54Z)

With the release of ROCm 6.3.4, support has now been extended to WSL! You can find the installation instructions for ROCm 6.3.4 on WSL over at [Install Radeon software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html).

---

### 评论 #11 — torehl (2025-04-04T12:52:11Z)

> With the release of ROCm 6.3.4, support has now been extended to WSL! You can find the installation instructions for ROCm 6.3.4 on WSL over at [Install Radeon software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html).

Is this a Radeon-only release?  Or can I install 6.3.4 rather than 6.3.3 on a cluster with Instinct Mi50,Mi100 and Mi210 GPGPUs? 

---
