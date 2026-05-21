# [Issue]: amdgpu-install failed on Ubuntu 24.04.4 LTS because of missing Release file

> **Issue #5968**
> **状态**: closed
> **创建时间**: 2026-02-15T15:20:31Z
> **更新时间**: 2026-02-23T15:08:01Z
> **关闭时间**: 2026-02-23T15:08:01Z
> **作者**: SitronNO
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5968

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Installing amdgpu-install_7.2.70200-1_all.deb works on my Ubuntu 24.04.4 LTS, but running amdgpu-install failes because of the repository 'https://repo.radeon.com/amdgpu/7.2/ubuntu noble Release' does not have a Release file.

### Operating System

24.04.4 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 5900X 12-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

First I run: (based on https://github.com/ROCm/ROCm/issues/5881#issuecomment-3786689561)
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then I reboot.

Then I verify I do not have any old releases or repos laying around:
```
$ sudo grep amdgpu /etc/apt/sources.list /etc/apt/sources.list.d/*
# Returns nothing

$ sudo grep rocm /etc/apt/sources.list /etc/apt/sources.list.d/*
# Returns nothing

$ dpkg -l | grep amdgpu
ii  libdrm-amdgpu1:amd64                           2.4.125-1ubuntu0.1~24.04.1               amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm-amdgpu1:i386                            2.4.125-1ubuntu0.1~24.04.1               i386         Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  xserver-xorg-video-amdgpu                      23.0.0-1ubuntu0.24.04.1                  amd64        X.Org X server -- AMDGPU display driver

$ dpkg -l | grep rocm
# Returns nothing
```
Then I try to install, where it fails:
```
$ sudo dpkg -i ./amdgpu-install_7.2.70200-1_all.deb
Selecting previously unselected package amdgpu-install.
(Reading database ... 498529 files and directories currently installed.)
Preparing to unpack .../amdgpu-install_7.2.70200-1_all.deb ...
Unpacking amdgpu-install (30.30.0.0.30300000-2278356.24.04) ...
Setting up amdgpu-install (30.30.0.0.30300000-2278356.24.04) ...

$ sudo amdgpu-install --usecase=graphics,opencl --accept-eula
Hit:1 http://no.archive.ubuntu.com/ubuntu noble InRelease
Hit:2 http://no.archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:3 http://no.archive.ubuntu.com/ubuntu noble-backports InRelease
Hit:4 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:5 https://repo.jotta.cloud/debian debian InRelease
Hit:6 https://deb.nodesource.com/node_22.x nodistro InRelease
Hit:7 http://download.opensuse.org/repositories/graphics:/darktable/xUbuntu_24.04  InRelease
Hit:8 http://linux.dropbox.com/ubuntu noble InRelease
Ign:9 https://repo.radeon.com/amdgpu/7.2/ubuntu noble InRelease
Hit:10 https://repo.radeon.com/amdgpu/30.30/ubuntu noble InRelease
Get:11 https://repo.radeon.com/rocm/apt/7.2 noble InRelease [2 603 B]
Get:12 https://repo.radeon.com/graphics/7.2/ubuntu noble InRelease [3 192 B]
Hit:13 https://ppa.launchpadcontent.net/mozillateam/ppa/ubuntu noble InRelease
Hit:14 https://ppa.launchpadcontent.net/obsproject/obs-studio/ubuntu noble InRelease
Err:15 https://repo.radeon.com/amdgpu/7.2/ubuntu noble Release
  404  Not Found [IP: 2a02:26f0:a300::1721:7773 443]
Get:16 https://repo.radeon.com/rocm/apt/7.2 noble/main amd64 Packages [60,9 kB]
Get:17 https://repo.radeon.com/graphics/7.2/ubuntu noble/main i386 Packages [8 849 B]
Get:18 https://repo.radeon.com/graphics/7.2/ubuntu noble/main amd64 Packages [10,6 kB]
Reading package lists... Done
E: The repository 'https://repo.radeon.com/amdgpu/7.2/ubuntu noble Release' does not have a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — harkgill-amd (2026-02-17T16:20:15Z)

Hey @SitronNO, this looks like the same issues as https://github.com/ROCm/ROCm/issues/5625. Could you try the installer without the `--accept-eula` flag? Make sure to run the uninstall commands first to remove the existing repos before retrying the install without the flag.

---

### 评论 #2 — festinalente (2026-02-17T18:32:28Z)

@harkgill-amd  I have the same issue, and tried without --accept-eula, no luck: 

```
$ sudo amdgpu-install --usecase=graphics,opencl
Hit:1 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:2 http://archive.ubuntu.com/ubuntu noble InRelease
Hit:3 https://repo.radeon.com/amdgpu/30.30/ubuntu noble InRelease
Ign:4 https://repo.radeon.com noble InRelease
Hit:5 https://repo.radeon.com/rocm/apt/7.2 noble InRelease
Hit:6 https://repo.radeon.com/graphics/7.2/ubuntu noble InRelease
Err:7 https://repo.radeon.com noble Release
  404  Not Found [IP: 2a02:26f0:1380:2c::5f65:269a 443]
Reading package lists... Done
E: The repository 'https://repo.radeon.com noble Release' does not have a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.

```



---

### 评论 #3 — harkgill-amd (2026-02-17T18:34:59Z)

@festinalente, you have to first run the following which will remove the faulty repos set up by `--accept-eula`,
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then you can proceed with,
```
wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/noble/amdgpu-install_7.2.70200-1_all.deb
sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
sudo amdgpu-install --usecase=graphics,opencl
```


---

### 评论 #4 — festinalente (2026-02-17T20:06:30Z)

@harkgill-amd yes I tried that previously as per your first comment. I tried again exactly as you detailed above and got the same result. 

The sources were all in etc/apt/sources.list.d so I did sudo apt install amdgpu-dkms rocm-opencl mesa-vulkan-drivers with secure boot enabled which seems to have worked: 

```
lsmod | grep amdgpu
amdgpu              17149952  23
amdxcp                 12288  1 amdgpu
drm_exec               12288  1 amdgpu
gpu_sched              61440  1 amdgpu
drm_buddy              20480  1 amdgpu
drm_suballoc_helper    16384  1 amdgpu
drm_ttm_helper         12288  1 amdgpu
ttm                   110592  2 amdgpu,drm_ttm_helper
drm_display_helper    237568  1 amdgpu
i2c_algo_bit           16384  1 amdgpu
video                  77824  2 amdgpu,ideapad_laptop

```

Tested it with a WebGL workload and seems to work... Not a fix for amdgpu-install issue, but a work around. 


---

### 评论 #5 — harkgill-amd (2026-02-18T15:11:05Z)

Another workaround is to simply remove or disable `/etc/apt/sources.list.d/amdgpu-proprietary.list`. This is the faulty repo that's activated by running amdgpu-install with `--accept-eula`.

Also just noticed, your issue is slightly different as the `accept-eula` based issue is identifiable with this repo failing to be found
```
Err:15 https://repo.radeon.com/amdgpu/7.2/ubuntu noble Release
  404  Not Found [IP: 2a02:26f0:a300::1721:7773 443]
```
Whereas you're seeing the generic `repo.radeon` repo failing.
```
Err:7 https://repo.radeon.com noble Release
  404  Not Found [IP: 2a02:26f0:1380:2c::5f65:269a 443]
```
Could you please share the output of  `grep -r "repo.radeon.com" /etc/apt/sources.list /etc/apt/sources.list.d/` to narrow down where this entry is sourced from? There shouldn't be any direct references to `repo.radeon` - they should come with a relevant subpath like https://repo.radeon.com/amdgpu/... or https://repo.radeon.com/rocm/...

---

### 评论 #6 — SitronNO (2026-02-18T16:17:14Z)

@harkgill-amd I have now tested your suggestion, and it did work. I did everything as before (in the section "Steps to Reproduce"), but I did not add the argument `--accept-eula`

So this solves my problem!

I also noted that `/etc/apt/sources.list.d/amdgpu-proprietary.list` is still installed, but the contents is different than before. The repo is commented out.

---

### 评论 #7 — festinalente (2026-02-18T16:24:19Z)

@harkgill-amd IIRC I came to the same conclusion and tried manually removing/disabling .proprietary.list and then running amdgpu-install and it didn't work, hence going with the direct installation. Today however the computer would boot with the fall back drivers unless booted in "unsafe" mode, which would load the AMD drivers normally (and work without crashes as was happening before). 

Here's the output you requested: 

```
grep -r "repo.radeon.com" /etc/apt/sources.list /etc/apt/sources.list.d/
/etc/apt/sources.list.d/amdgpu-proprietary.list.save:# deb https://repo.radeon.com/amdgpu/7.2/ubuntu noble proprietary
/etc/apt/sources.list.d/amdgpu.list:deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30/ubuntu noble main
/etc/apt/sources.list.d/amdgpu.list:#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30/ubuntu noble main
/etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list.save:# deb https://repo.radeon.com noble noble main
/etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list.save:deb-src https://repo.radeon.com noble noble main
/etc/apt/sources.list.d/amdgpu.list.save:deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30/ubuntu noble main
/etc/apt/sources.list.d/amdgpu.list.save:#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30/ubuntu noble main
/etc/apt/sources.list.d/rocm.list:deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/7.2 noble main
/etc/apt/sources.list.d/rocm.list:deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/graphics/7.2/ubuntu noble main
/etc/apt/sources.list.d/amdgpu-proprietary.list:# deb https://repo.radeon.com/amdgpu/7.2/ubuntu noble proprietary
/etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list:# deb https://repo.radeon.com noble noble main
/etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list:# deb-src https://repo.radeon.com noble noble main
/etc/apt/sources.list.d/rocm.list.save:deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/7.2 noble main
/etc/apt/sources.list.d/rocm.list.save:deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/graphics/7.2/ubuntu noble main

```


---

### 评论 #8 — harkgill-amd (2026-02-18T16:34:03Z)

Ok so you have alot more than just the default repos setup from amdgpu-install. For reference, here's what the output looks like after a clean install,
```
grep -r "repo.radeon.com" /etc/apt/sources.list /etc/apt/sources.list.d/
/etc/apt/sources.list.d/amdgpu-proprietary.list:#deb https://repo.radeon.com/amdgpu/7.2/ubuntu noble proprietary
/etc/apt/sources.list.d/amdgpu.list:deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30/ubuntu noble main
/etc/apt/sources.list.d/amdgpu.list:#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30/ubuntu noble main
/etc/apt/sources.list.d/rocm.list:deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/7.2 noble main
/etc/apt/sources.list.d/rocm.list:deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/graphics/7.2/ubuntu noble main
```
First step would be to remove the ones directly causing your errors and see if that resolves the issue,
```
sudo rm /etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list
sudo rm /etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list.save
sudo apt update
```

---

### 评论 #9 — festinalente (2026-02-19T11:03:08Z)

@harkgill-amd Yes, that worked, amdgpu-install worked normally after:  

```
sudo rm /etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list
sudo rm /etc/apt/sources.list.d/archive_uri-https_repo_radeon_com-noble.list.save
sudo apt update
``` 

---

### 评论 #10 — harkgill-amd (2026-02-23T15:08:01Z)

Glad to hear it's working on your end. Will close out this issue but feel free to leave a comment if you run into any further issues.

---
