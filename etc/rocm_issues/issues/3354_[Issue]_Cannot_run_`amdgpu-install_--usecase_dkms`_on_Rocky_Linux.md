# [Issue]: Cannot run `amdgpu-install --usecase dkms` on Rocky Linux

> **Issue #3354**
> **状态**: closed
> **创建时间**: 2024-06-24T13:54:52Z
> **更新时间**: 2024-07-31T20:59:30Z
> **关闭时间**: 2024-07-31T20:01:00Z
> **作者**: drew-viles
> **标签**: AMD Instinct MI250X, AMD Instinct MI250, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3354

## 标签

- **AMD Instinct MI250X** (颜色: #ededed)
- **AMD Instinct MI250** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I cannot get `amdgpu-install --usecase xxx` to work on Rocky Linux (at the moment I've only test 8). 
Granted, this could be a mess up on my side as It's been since the days of CentOS 6 that I last used anything RedHat based! However I thought I'd raise it as it looks a bit sucpicious either way that it's passing the flag down to dnf.

### Operating System

Rocky Linux 8.9

### CPU

AMD EPYC 7713 64-Core Processor

### GPU

AMD Instinct MI250X, AMD Instinct MI250

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

I'm using ROCm Version 6.1.2 at the moment but it's not available in the list above:

So, I'm running the following and it appears that the --usecase flag is being passed down to the dnf command. Other flags I've tried, such as `--list-usecase` work fine.

```
amdgpu-install --usecase=dkms
usage: dnf install [-c [config file]] [-q] [-v] [--version]
                   [--installroot [path]] [--nodocs] [--noplugins]
                   [--enableplugin [plugin]] [--disableplugin [plugin]]
                   [--releasever RELEASEVER] [--setopt SETOPTS]
                   [--skip-broken] [-h] [--allowerasing] [-b | --nobest] [-C]
                   [-R [minutes]] [-d [debug level]] [--debugsolver]
                   [--showduplicates] [-e ERRORLEVEL] [--obsoletes]
                   [--rpmverbosity [debug level name]] [-y] [--assumeno]
                   [--enablerepo [repo]] [--disablerepo [repo] | --repo
                   [repo]] [--enable | --disable] [-x [package]]
                   [--disableexcludes [repo]] [--repofrompath [repo,path]]
                   [--noautoremove] [--nogpgcheck] [--color COLOR] [--refresh]
                   [-4] [-6] [--destdir DESTDIR] [--downloadonly]
                   [--comment COMMENT] [--bugfix] [--enhancement]
                   [--newpackage] [--security] [--advisory ADVISORY]
                   [--bz BUGZILLA] [--cve CVES]
                   [--sec-severity {Critical,Important,Moderate,Low}]
                   [--forcearch ARCH]
                   PACKAGE [PACKAGE ...]
dnf install: error: unrecognized arguments: --usecase=dkms
```



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

This has worked fine on Ubuntu but only seems to affect my RockyLinux image builds. I'm just using a bit of Packer and Ansible to build the images and whilst this is all successful, when booting the image, I'm greeted with no `rocminfo` binary which lead me to try and manually run this, which resulted in these findings. 

Running it without the flag results in:
```
amdgpu-install
Last metadata expiration check: 0:04:41 ago on Mon Jun 24 13:52:47 2024.
All matches were filtered out by exclude filtering for argument: amdgpu-dkms
Error: Unable to find a match: amdgpu-dkms
```


It's also worth noting that my Ansible does a dnf upgrade at the end of the run, after the GPU section of Ansible passes. This upgrades it from 8.9 to 8.10 of Rocky Linux so I'm not sure if this is having an impact on functionality after the fact but as `rocminfo` isn't available, I suspect this isn't really of note. However the more information I can provide the better, right? 😄 

---

## 评论 (9 条)

### 评论 #1 — kentrussell (2024-06-24T15:50:19Z)

Your error says amdgpu-install --use-case=dkms
It's --usecase=dkms. 
Can you double-check without the hyphen in the middle of use and case?

---

### 评论 #2 — drew-viles (2024-06-24T15:59:48Z)

Sorry yeah that was a typo and I've copied the wrong test in 🤦 . But it doesn't work when using the `--usecase` flag. I'll update the issue to prevent any further confusion.

---

### 评论 #3 — kentrussell (2024-06-24T16:06:31Z)

Thanks. What's the error it throws when it runs? Or does it run "successfully" but is missing the packages you were looking at?

---

### 评论 #4 — drew-viles (2024-06-24T16:12:42Z)

So when I build using my Packer ansible, it just passes as successful. I then boot the image and I noticed `rocminfo` was missing. So that's when I thought "Hey, I'll run amdgpu-install again just to check what's going on" - that resulted in the above dnf error being thrown out.

For context, I'm just running this step in ansible which is all passing as successful.

```
 <snip epel repo enabling>

    - name: Install AMDGPU-Install
      ansible.builtin.dnf:
        name: "https://repo.radeon.com/amdgpu-install/{{ gpu_amd_version }}/rhel/{{ ansible_distribution_version }}/amdgpu-install-{{ gpu_amd_pkg_version }}.el{{ ansible_distribution_major_version }}.noarch.rpm"
        state: present

 <snip install kernel headers/devel>
```




---

### 评论 #5 — kentrussell (2024-06-24T16:18:58Z)

@mystro256 Any insight here? I know we don't support Rocky, but is this something that can easily be worked around?

---

### 评论 #6 — drew-viles (2024-06-24T16:21:40Z)

Yeah this is the other point - I know it's technically not supported so I'm happy to continue prodding my side if needs be - which I will do in the background. As I said in the inital blurb too, I've been in Debian land for so long now it's not completely unreasonable to think I've done something silly here too!

---

### 评论 #7 — drew-viles (2024-06-25T09:26:04Z)

For a touch more information, I've manually tried to go through this using the official documentation for RHEL and it hits the same issues. I wanted to rule out Ansible ordering to be the problem!

The only way I can get `rocm` installed is to do it via the package manager steps. So it could well be a bug in the script (I haven't had time to read through it yet) - but it's just the `amdgpu-install` script that's failing on Rocky.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/rhel.html

---

### 评论 #8 — ppanchad-amd (2024-07-31T20:01:00Z)

@drew-viles This appears to be an issue on Rocky Linux which is not a supported distro. Closing bug. Thanks!

---

### 评论 #9 — drew-viles (2024-07-31T20:59:29Z)

No problemo, I'll fork and fix myself when I get time then as it's passing the flag down to the dnf command which I suspect isn't just affecting this RH based distro. Thanks anyway!

---
