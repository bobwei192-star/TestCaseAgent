# ROCm installation repeatedly crashing.

> **Issue #4730**
> **状态**: closed
> **创建时间**: 2025-05-10T22:39:05Z
> **更新时间**: 2025-05-11T11:21:40Z
> **关闭时间**: 2025-05-11T11:21:39Z
> **作者**: chowdri
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4730

## 描述

I'm installing rocm 6.4 on my system (elementary OS 8/ ubuntu 24.04) using amdgpu-install_6.4.60400-1_all.deb that I downloaded from : https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html

It used to work perfectly fine when my os was installed on a sata ssd. But now that I moved my system to an nvme drive (Samsung 9100 Pro), I'm having problems with this installation.

after using dpkg to install amdgpu-install, I execute the installer:

`$ amdgpu-install -y --usecase=rocm`

However, midway through the installation, the system crashes and restarts. When I check dkms after restart, the driver is added and not installed.

```
$ dkms status

amdgpu/6.12.12-2147987.24.04: added

```
When I try to install the kernel module:

```
$ sudo dkms install -m amdgpu -v 6.12.12-2147987.24.04 

[sudo] password for:            
Sign command: /usr/bin/kmodsign
Signing key: /var/lib/shim-signed/mok/MOK.priv
Public certificate (MOK): /var/lib/shim-signed/mok/MOK.der

Building module:
Cleaning build area...
'make' KERNELVER=6.11.0-25-generic.....
```

It goes this far and crashes and restarts. 

When I try the following:

`$ sudo dpkg --configure -a`

The installation resumes and then crashes again and then the system restarts again.

After this restart, I cant see the GPUs on hwmon, the colors are all off and the resolution is reduced. 

I've tried re-installing the os on the nvme, but this outcome takes place again and again.

Is there a list of pre-requisites that I can check?

Any insights and guidance in the matter is much appreciated.

---

## 评论 (1 条)

### 评论 #1 — chowdri (2025-05-11T11:21:39Z)

nevermind I didnt have the following packages:

`$ sudo apt install python3-setuptools python3-wheel`

---
