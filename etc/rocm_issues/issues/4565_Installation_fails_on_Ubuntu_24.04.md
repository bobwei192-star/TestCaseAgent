# Installation fails on Ubuntu 24.04

> **Issue #4565**
> **状态**: closed
> **创建时间**: 2025-04-06T05:13:50Z
> **更新时间**: 2025-04-23T19:25:44Z
> **关闭时间**: 2025-04-23T19:25:43Z
> **作者**: LostExcalibur
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4565

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

When trying to download rocm 6.3.3 (which I believe is the latest version) on Ubuntu 24.04 (fresh install from 2 days ago), all ways of installing fail when trying to install the `rocm` package with the following issues :
```
The following packages have unmet dependencies.
 libzstd-dev : Depends: libzstd1 (= 1.5.5+dfsg2-2build1) but 1.5.5+dfsg2-2build1.1 is to be installed
 mesa-common-dev : Depends: libdrm-dev (>= 2.4.95) but it is not installable
 python3-dev : Depends: python3 (= 3.12.3-0ubuntu1) but 3.12.3-0ubuntu2 is to be installed
 zlib1g-dev : Depends: zlib1g (= 1:1.3.dfsg-3.1ubuntu2) but 1:1.3.dfsg-3.1ubuntu2.1 is to be installed
```
Attached is the full output from the offline creator tool which is the last thing I tried.

[output.log](https://github.com/user-attachments/files/19619770/output.log)

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-04-07T13:27:26Z)

Hi @LostExcalibur. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — harkgill-amd (2025-04-16T15:12:43Z)

Hi @LostExcalibur, stepping away from the offline installer method. Could you try the following steps for a basic installation.

Remove all existing installation remnants with
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then reinstall ROCm 6.3.3 with
```
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/noble/amdgpu-install_6.3.60303-1_all.deb
sudo apt install ./amdgpu-install_6.3.60303-1_all.deb
sudo apt update
sudo apt install amdgpu-dkms rocm
```
The latest ROCm release is ROCm 6.4.0 but let's first try with ROCm 6.3.3 to isolate the cause of the errors. If you are still experiencing the errors after running the aforementioned commands, please share the error messages and the output of

1. `cat /etc/apt/sources.list.d/ubuntu.sources`
2. `cat /etc/apt/sources.list.d/rocm.list`
3. `cat /etc/apt/sources.list.d/amdgpu.list`

---

### 评论 #3 — LostExcalibur (2025-04-16T15:36:51Z)

Hi @harkgill-amd, I am currently away but I'll get back to you as soon as I'm able to try that. Thanks you very much in the meantime !

---

### 评论 #4 — LostExcalibur (2025-04-18T16:00:09Z)

Hi again @harkgill-amd,
I followed all the steps you mentioned, and the installation still fails at the last `apt` step, with the following error message :
```
❯ sudo apt install amdgpu-dkms rocm
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies.
 mesa-common-dev : Depends: libdrm-dev (>= 2.4.95) but it is not installable
 python3-dev : Depends: python3 (= 3.12.3-0ubuntu1) but 3.12.3-0ubuntu2 is to be installed
```

Here is the output of the 3 commands :
```
❯ cat /etc/apt/sources.list.d/ubuntu.sources
Types: deb
URIs: http://fr.archive.ubuntu.com/ubuntu/
Suites: noble
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: universe main multiverse restricted
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```
```
❯ cat /etc/apt/sources.list.d/rocm.list
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.3.3 noble main
```
```
❯ cat /etc/apt/sources.list.d/amdgpu.list
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble main
#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble main
```

---

### 评论 #5 — harkgill-amd (2025-04-21T15:58:02Z)

Noticing that you're missing the `noble-updates` and `noble-backports` suites. The former provides the latest versions of both the `libdrm-dev` and `python3` packages. Please modify the `/etc/apt/sources.list.d/ubuntu.sources` to include both suites with any text editor or the following command,
```
sudo tee /etc/apt/sources.list.d/ubuntu.sources > /dev/null <<EOF
Types: deb
URIs: http://fr.archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
EOF
```
After this, run `sudo apt update` and then `sudo apt install amdgpu-dkms rocm`. This should resolve the majority of errors you're seeing. If there are any packages that are still showing unmet dependencies, please provide the output of `apt-cache policy <package>`.

---

### 评论 #6 — LostExcalibur (2025-04-23T19:25:43Z)

That fixed it !
Perhaps consider including in the documentation that they are needed ? I don't know if they come enabled by default and I did something wrong to disable them, or if it is a necessary step.
Thank you very much anyway for your time !

---
