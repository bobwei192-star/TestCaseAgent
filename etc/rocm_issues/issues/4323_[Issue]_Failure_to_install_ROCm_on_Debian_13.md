# [Issue]: Failure to install ROCm on Debian 13

> **Issue #4323**
> **状态**: closed
> **创建时间**: 2025-01-31T20:19:54Z
> **更新时间**: 2025-10-18T17:39:46Z
> **关闭时间**: 2025-01-31T21:52:54Z
> **作者**: adamroyjones
> **标签**: 6.3.1, AMD Radeon RX 7800 XT
> **URL**: https://github.com/ROCm/ROCm/issues/4323

## 标签

- **6.3.1** (颜色: #D28178)
- **AMD Radeon RX 7800 XT** (颜色: #ededed)

## 描述

### Problem Description

I was a Debian 12 user who recently bought an RX 7800 XT. Version 6.1 of the kernel was too old for this, so I decided to upgrade to Debian 13 (trixie). 

I was hoping to install ROCm. I tried to go through the instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.1/install/quick-start.html) (hoping they'd work for 13 as well as they presumably work for 12) but I was scuppered by this:

```
$ sudo apt install amdgpu-dkms rocm
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

Unsatisfied dependencies:
 rocm-llvm : Depends: libstdc++-5-dev but it is not installable or
                      libstdc++-7-dev but it is not installable or
                      libstdc++-11-dev but it is not installable
             Depends: libgcc-5-dev but it is not installable or
                      libgcc-7-dev but it is not installable or
                      libgcc-11-dev but it is not installable
             Recommends: gcc-multilib but it is not going to be installed
             Recommends: g++-multilib but it is not going to be installed
```

This is related to https://github.com/ROCm/ROCm/issues/4272, but approached differently.

### Operating System

Debian 13 (trixie)

### CPU

AMD Ryzen 9 5950X

### GPU

AMD Radeon RX 7800 XT

### ROCm Version

6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

On Debian 13:

```
sudo apt update
sudo apt install "linux-headers-$(uname -r)"
sudo apt install -y python3-setuptools python3-wheel libpython3.11
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.3.1/ubuntu/jammy/amdgpu-install_6.3.60301-1_all.deb
sudo apt install ./amdgpu-install_6.3.60301-1_all.deb
sudo apt update
sudo apt install amdgpu-dkms rocm
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — harkgill-amd (2025-01-31T21:52:54Z)

Hi @adamroyjones, have you given the Ubuntu 24.04/noble amdgpu-installer a try? It should be a better comparison as Ubuntu 24.04 is based off of trixie/sid. 

In any case, ROCm does not currently support Debian 13. For a complete list of supported OSes and their corresponding Linux Kernels, please refer to the [Supported Operating Systems](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems) page. 

---

### 评论 #2 — adamroyjones (2025-01-31T22:31:45Z)

Thanks for the quick response. I've just given it a try now. It leads to the same error:

```
$ sudo apt install amdgpu-dkms rocm
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

Unsatisfied dependencies:
 rocm-llvm : Depends: libstdc++-5-dev but it is not installable or
                      libstdc++-7-dev but it is not installable or
                      libstdc++-11-dev but it is not installable
             Depends: libgcc-5-dev but it is not installable or
                      libgcc-7-dev but it is not installable or
                      libgcc-11-dev but it is not installable
             Recommends: gcc-multilib but it is not going to be installed
             Recommends: g++-multilib but it is not going to be installed
Error: Unable to correct problems, you have held broken packages.
```

A pity, but I guess things may change after trixie becomes stable?

---

### 评论 #3 — harkgill-amd (2025-02-03T15:55:29Z)

Yes. If support is announced once trixie is more stable, these errors will be addressed.

---

### 评论 #4 — DiegoRioboCabot (2025-08-16T16:05:43Z)

Hi. Trixie stable has been released and this error persists. Any fixes?

---

### 评论 #5 — blackmennewstyle (2025-08-24T12:28:19Z)

Hello beautiful devs,

I can confirm that the issue is still there with other minor issues:
```
apt-get update
Get:1 http://security.debian.org/debian-security trixie-security InRelease [43.4 kB]
Get:2 https://repo.radeon.com/amdgpu/6.4.3/ubuntu noble InRelease [5,465 B]    
Get:3 https://repo.radeon.com/rocm/apt/6.4.3 noble InRelease [2,605 B]
Hit:4 http://deb.debian.org/debian trixie-backports InRelease
Hit:5 http://deb.debian.org/debian trixie InRelease
Hit:6 http://deb.debian.org/debian trixie-updates InRelease
Get:7 https://repo.radeon.com/amdgpu/6.4.3/ubuntu noble/main amd64 Packages [14.3 kB]
Get:8 https://repo.radeon.com/amdgpu/6.4.3/ubuntu noble/main i386 Packages [12.2 kB]
Get:9 https://repo.radeon.com/rocm/apt/6.4.3 noble/main amd64 Packages [60.6 kB]
Fetched 138 kB in 1s (236 kB/s)     
Reading package lists... Done
W: https://repo.radeon.com/amdgpu/6.4.3/ubuntu/dists/noble/InRelease: Policy will reject signature within a year, see --audit for details
W: https://repo.radeon.com/rocm/apt/6.4.3/dists/noble/InRelease: Policy will reject signature within a year, see --audit for details
```

Lastly when trying to install `rocm`:
```
 apt-get install rocm
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Solving dependencies... Error!
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 rocm-llvm : Depends: libstdc++-5-dev but it is not installable or
                      libstdc++-7-dev but it is not installable or
                      libstdc++-11-dev but it is not installable
             Depends: libgcc-5-dev but it is not installable or
                      libgcc-7-dev but it is not installable or
                      libgcc-11-dev but it is not installable
             Recommends: gcc-multilib but it is not going to be installed
             Recommends: g++-multilib but it is not going to be installed
E: Unable to correct problems, you have held broken packages.
E: The following information from --solver 3.0 may provide additional context:
   Unable to satisfy dependencies. Reached two conflicting decisions:
   1. rocm-llvm:amd64 is selected for install because:
      1. rocm:amd64=6.4.3.60403-128~24.04 is selected for install
      2. rocm:amd64 Depends rocm-openmp-sdk (= 6.4.3.60403-128~24.04)
      3. rocm-openmp-sdk:amd64 Depends rocm-llvm (= 19.0.0.25224.60403-128~24.04)
   2. rocm-llvm:amd64 Depends libstdc++-5-dev | libstdc++-7-dev | libstdc++-11-dev
      but none of the choices are installable:
      [no choices]
```
Debian 13 indeed does not have these version of `libstdc` it has `6`, `12`, `13` & `14`.

---

### 评论 #6 — yodaxtah (2025-10-18T17:39:46Z)

I have not yet retried the above, but if anybody finds a way to install it, I'm all ears! :)

I can only contribute saying that [this table](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus) could use a list of distributions in those rows, because I kinda missed the footnote in that table

> AMD Radeon PRO (...) and AMD Radeon (RX 9070 XT, RX 9070 GRE, RX 9070, RX 9060 XT, RX 9060, RX 7900 XTX, RX 7900 XT, RX 7900 GRE, **RX 7800 XT**, and RX 7700 XT) are supported **only on Ubuntu 24.04.3, Ubuntu 22.04.5, RHEL 10.0, and RHEL 9.6**.

and, unknowingly followed the quick-install for Debian 13. I (of course?) ran into issues with the last step, installing ROCm:

```
$ sudo apt install rocm
...
Continue? [Y/n] Y
Err:1 http://deb.debian.org/debian trixie/main amd64 mariadb-common all 1:11.8.2-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Err:2 http://deb.debian.org/debian trixie/main amd64 libmariadb3 amd64 1:11.8.2-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Err:3 http://deb.debian.org/debian trixie/main amd64 libpq5 amd64 17.5-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/m/mariadb/mariadb-common_11.8.2-1_all.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/m/mariadb/libmariadb3_11.8.2-1_amd64.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/p/postgresql-17/libpq5_17.5-1_amd64.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
```

---
