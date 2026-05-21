# [Documentation]: Installation error Ubuntu 22.04 workaround

> **Issue #2933**
> **状态**: closed
> **创建时间**: 2024-02-27T11:10:37Z
> **更新时间**: 2024-08-27T16:08:19Z
> **关闭时间**: 2024-08-27T16:08:19Z
> **作者**: FabianWildgrube
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2933

## 描述

### Description of errors

I ran into an issue with ROCm installation on Ubuntu 22.04 with a multi-version setup.
The following commands:
```
sudo apt update                                       
wget https://repo.radeon.com/amdgpu-install/6.0.2/ubuntu/jammy/amdgpu-install_6.0.60002-1_all.deb
sudo apt install ./amdgpu-install_6.0.60002-1_all.deb
sudo amdgpu-install --rocmrelease=6.0.2 --usecase=rocm
```
resulted in the following error during the `amdgpu-install` command:
```
Processing triggers for man-db (2.10.2-1) ...
Error! Could not locate dkms.conf file.
File: /var/lib/dkms/amdgpu/5.18.13-1577590.22.04/source/dkms.conf does not exist.
WARNING: amdgpu dkms failed for running kernel
```

I had seen this error before on older ROCm versions, so luckily I knew what to do:
```
sudo dpkg-reconfigure amdgpu-dkms
```

This could be added to the official documentation in a "Common issues" section or something similar.

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (11 条)

### 评论 #1 — phubner (2024-02-28T04:00:52Z)

I am running into this with WSL2 on Windows 11. You can run with `--no-dkms` but that really doesn't solve anything. I have not found any way of getting dkms loaded on my ubuntu 22.04.04 instance.

---

### 评论 #2 — preda (2024-02-28T06:49:04Z)

But you don't need dkms on Ubuntu 22.04 (it runs perfectly well with the amdgpu driver that's included in the stock kernel).


---

### 评论 #3 — FabianWildgrube (2024-02-28T09:34:51Z)

> But you don't need dkms on Ubuntu 22.04 (it runs perfectly well with the amdgpu driver that's included in the stock kernel).

The [installation docs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html#skipping-kernel-mode-driver-installation) only say this:
> The installer script tries to install the kernel mode driver along with the requested use cases. This might be unnecessary as in the case of docker containers or you may wish to keep a specific version when using multi-version installation, and not have the last installed version overwrite the kernel mode driver.
> 
> To skip the installation of the kernel-mode driver add the `--no-dkms` option when calling the installer script.

Maybe this could be extended with a note that mentions --no-dkms is recommended for Ubuntu 22.04?

---

### 评论 #4 — phubner (2024-02-28T16:38:43Z)

So after running  `sudo amdgpu-install --usecase=rocm -y` and the dkms failing to install. I try to run `rocminfo` with this result 
```
rocminfo
ROCk module is NOT loaded, possibly no GPU devices
```

This is repeatable with `--no-dkms` in the `amdgpu-install` step.

Again this is ubuntu 22.04.04 kernel 15.5 on WSL2 windows 11.

I have a RX 7900 XTX and the latest drivers installed on the host machine. Also running a 7800X3D.

---

### 评论 #5 — phubner (2024-03-01T19:05:02Z)

Any follow up here? I would love some verification that room on WSL2 ubuntu 22.04.04 does indeed work. 

---

### 评论 #6 — harkgill-amd (2024-06-26T14:13:53Z)

Hi @phubner, have you tried installing with the wsl usecase and --no-dkms specified?
```
amdgpu-install -y --usecase=wsl,rocm --no-dkms
```

---

### 评论 #7 — phubner (2024-06-26T14:18:46Z)

Hi @harkgill-amd, I will double check but when I used the `--no-dkms` previously the `rocm` commands wouldn't work. For example, running `rocm-info` did not work. 

(I will follow up)

---

### 评论 #8 — xaxaxa7b9 (2024-07-08T21:22:48Z)

any update on this? @phubner 

---

### 评论 #9 — phubner (2024-07-08T22:37:13Z)

Hey @xaxaxa7b9 I did verify that with `https://repo.radeon.com/amdgpu-install/6.1.3/ubuntu/jammy/` on `22.04` I can now, at a minimum, see my RTX 7900 xtx with `rocminfo`

```
*******
Agent 2
*******
  Name:                    gfx1100
  Marketing Name:          AMD Radeon RX 7900 XTX
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
```

I have not tried to run pytorch or any code yet. But this is an improvement.

---

### 评论 #10 — harkgill-amd (2024-07-11T18:54:15Z)

Hi @phubner, the beta release for WSL with ROCm is now out. Please find instructions on how to install ROCm and run PyTorch on WSL below.

1. [Install Radeon software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html)
2. [Install PyTorch for Radeon GPUs on WSL](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html)

@FabianWildgrube Are you still running into this issue with the multi-version setup on ROCm 6.1.2?

---

### 评论 #11 — harkgill-amd (2024-08-27T16:08:19Z)

Hi @FabianWildgrube, I tried to reproduce this issue by installing 6.2.0 and 6.1.2 in a multi-version environment but did not encounter any dkms conflicts. There are also new instructions on how to configure a multi-version installation at [Installing multiple ROCm versions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/multi-version-install.html#using-your-package-manager). I will close this issue for now, if you experience any issues with this new documentation, please leave a comment and I will re-open this ticket.

---
