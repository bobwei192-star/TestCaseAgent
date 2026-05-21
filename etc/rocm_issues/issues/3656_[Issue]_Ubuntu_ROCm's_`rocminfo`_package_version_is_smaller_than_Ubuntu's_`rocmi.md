# [Issue]: Ubuntu ROCm's `rocminfo` package version is smaller than Ubuntu's `rocminfo` one, breaking `rocm-hip-runtime` installation

> **Issue #3656**
> **状态**: open
> **创建时间**: 2024-08-29T13:41:24Z
> **更新时间**: 2026-04-29T20:10:49Z
> **作者**: illwieckz
> **标签**: Under Investigation, ROCm 6.2.0, AMD Radeon Pro W7800
> **URL**: https://github.com/ROCm/ROCm/issues/3656

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.0** (颜色: #ededed)
- **AMD Radeon Pro W7800** (颜色: #ededed)

## 描述

### Problem Description

I'm running ROCm 6.2.0 on Ubuntu 24.4 Noble. The GPU is an `AMD Radeon PRO W7600` but it doesn't matter because the issue is a packaging issue affecting packages provided by [repo.radeon.com](https://repo.radeon.com).

Ubuntu provides a `rocminfo` package with version 5.7.1:

```
Get:1 http://archive.ubuntu.com/ubuntu noble/universe amd64 rocminfo amd64 5.7.1-3build1 [25.6 kB]
```

The AMD APT repository for ROCm 6.2 provides a `rocminfo` package with version 1.0.0:

```
Get:1 https://repo.radeon.com/rocm/apt/6.2 noble/main amd64 rocminfo amd64 1.0.0.60200-66~24.04 [29.3 kB]
```

The workstation was running Ubuntu 23.10 Jammy Jellyfish with ROCm 6.1.3 and was then updated to Ubuntu 24.04 Noble Numbat and then ROCm was updated to ROCm 6.2. It means the update from Ubuntu 23.10 to Ubuntu 24.04 was done before uptating ROCm from 6.1.3 to 6.2.

While updating Ubuntu from 23.10 to 24.04, the `rocminfo` package was upgraded with Ubuntu one with version `5.7`, meaning the system received a package older than the one from ROCm 6.2 but with an higher version and taking priority over.

Later, when upgrading to ROCm 6.2, it brokes the installation of `rocm-hip-runtime` as it depends on `rocminfo=1.0.0.60200-66~24.04` but an older package with a higher version number (`5.7.1-3build1`) is already installed:

```
# apt-get install rocm-hip-runtime
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 rocm-hip-runtime : Depends: rocminfo (= 1.0.0.60200-66~24.04) but 5.7.1-3build1 is to be installed
```


### Operating System

Ubuntu 24.04 Noble Numbat

### CPU

AMD Ryzen Threadripper PRO 3955WX 16-Cores

### GPU

AMD Radeon Pro W7800

### ROCm Version

ROCm 6.2.0

### ROCm Component

rocminfo

### Steps to Reproduce

1. Install Ubuntu 23.10
2. Install `rocm-hip-runtime` from ROCm 6.1.3
3. Upgrade to Ubuntu 24.04
4. Attempt to install `rocm-hip-runtime` from ROCm 6.2

Alternatively (untested):

1. Install Ubuntu 24.04
2. Install `rocm-hip-runtime` from Ubuntu repositories
3. Attempt to install `rocm-hip-runtime` from ROCm 6.2

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — illwieckz (2024-08-29T13:43:00Z)

I was able to manually fix the problem by uninstalling the old `rocminfo` 5.7 and packages depending on it, then reinstalling it by forcing the version of `rocminfo` with the one from ROCm 6.2, and restarted the installation of `rocm-hip-runtime`:

```
# apt-get autoremove --purge rocminfo
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages will be REMOVED:
  libhsa-runtime64-1* libhsakmt1* rocminfo*
0 upgraded, 0 newly installed, 3 to remove and 0 not upgraded.
After this operation, 2931 kB disk space will be freed.
Do you want to continue? [Y/n] 
(Reading database ... 1051616 files and directories currently installed.)
Removing rocminfo (5.7.1-3build1) ...
Removing libhsa-runtime64-1 (5.7.1-2build1) ...
Removing libhsakmt1:amd64 (5.7.0-1build1) ...
Processing triggers for man-db (2.12.0-4build2) ...
Processing triggers for libc-bin (2.39-0ubuntu8.3) ...

# apt-get install rocminfo=1.0.0.60200-66~24.04
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libhsa-runtime64-1 libhsakmt1
Use 'apt autoremove' to remove them.
The following packages will be DOWNGRADED:
  rocminfo
0 upgraded, 0 newly installed, 1 downgraded, 0 to remove and 0 not upgraded.
Need to get 0 B/29.3 kB of archives.
After this operation, 17.4 kB of additional disk space will be used.
Do you want to continue? [Y/n] 
dpkg: warning: downgrading rocminfo from 5.7.1-3build1 to 1.0.0.60200-66~24.04
(Reading database ... 1051617 files and directories currently installed.)
Preparing to unpack .../rocminfo_1.0.0.60200-66~24.04_amd64.deb ...
Unpacking rocminfo (1.0.0.60200-66~24.04) over (5.7.1-3build1) ...
Setting up rocminfo (1.0.0.60200-66~24.04) ...
Processing triggers for man-db (2.12.0-4build2) ...

# apt-get install -V rocm-hip-runtime
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
   hip-runtime-amd (6.2.41133.60200-66~24.04)
   rocminfo (1.0.0.60200-66~24.04)
The following NEW packages will be installed:
   hip-runtime-amd (6.2.41133.60200-66~24.04)
   rocm-hip-runtime (6.2.0.60200-66~24.04)
   rocminfo (1.0.0.60200-66~24.04)
0 upgraded, 3 newly installed, 0 to remove and 0 not upgraded.
Need to get 12.0 MB/12.0 MB of archives.
After this operation, 74.4 MB of additional disk space will be used.
Do you want to continue? [Y/n] 
Get:1 https://repo.radeon.com/rocm/apt/6.2 noble/main amd64 hip-runtime-amd amd64 6.2.41133.60200-66~24.04 [12.0 MB]                                          
Get:2 https://repo.radeon.com/rocm/apt/6.2 noble/main amd64 rocm-hip-runtime amd64 6.2.0.60200-66~24.04 [2034 B]                                              
Fetched 12.0 MB in 60s (200 kB/s)                                                                                                                             
Selecting previously unselected package rocminfo.
(Reading database ... 1051600 files and directories currently installed.)
Preparing to unpack .../rocminfo_1.0.0.60200-66~24.04_amd64.deb ...
Unpacking rocminfo (1.0.0.60200-66~24.04) ...
Selecting previously unselected package hip-runtime-amd.
Preparing to unpack .../hip-runtime-amd_6.2.41133.60200-66~24.04_amd64.deb ...
Unpacking hip-runtime-amd (6.2.41133.60200-66~24.04) ...
Selecting previously unselected package rocm-hip-runtime.
Preparing to unpack .../rocm-hip-runtime_6.2.0.60200-66~24.04_amd64.deb ...
Unpacking rocm-hip-runtime (6.2.0.60200-66~24.04) ...
Setting up rocminfo (1.0.0.60200-66~24.04) ...
Setting up hip-runtime-amd (6.2.41133.60200-66~24.04) ...
Setting up rocm-hip-runtime (6.2.0.60200-66~24.04) ...
update-alternatives: using /opt/rocm-6.2.0/bin/rocm_agent_enumerator to provide /usr/bin/rocm_agent_enumerator (rocm_agent_enumerator) in auto mode
update-alternatives: using /opt/rocm-6.2.0/bin/rocminfo to provide /usr/bin/rocminfo (rocminfo) in auto mode
```

---

### 评论 #2 — illwieckz (2024-08-29T13:45:16Z)

As written [here](https://github.com/ROCm/ROCm/issues/3654#issuecomment-2317301157) I can provide more help in a more efficient way:

> ℹ️ AMD has [publicly announced](https://www.phoronix.com/news/AMD-Unified-Linux-Jobs) in June they were looking for people to help them improve the Linux packaging of their ROCm stack. I'm ready to help either as an employee or as an external contractor (see my entreprise [rebatir.fr](https://rebatir.fr) and the [I love compute](https://gitlab.com/illwieckz/i-love-compute) initiative as reference). The AMD's application website is very limited and inefficient so I'm not surprised if my application got lost. It is obvious the need is still there at AMD and I'm still available for help.

---

### 评论 #3 — harkgill-amd (2024-09-04T17:17:44Z)

Hi @illwieckz, thank you for reporting this. I'll look into this issue and get back to you.

---

### 评论 #4 — MindOfCogsAndMetal (2024-09-20T18:48:28Z)

Any update on this? It's not possible to install ROCm on Ubuntu at this point.

---

### 评论 #5 — illwieckz (2024-09-20T20:56:56Z)

@MindOfCogsAndMetal The radeon repository provides some pinning to prefer their own rocminfo but it only works _if rocminfo is not already installed_.

So I suggest you to uninstall `rocminfo` first:

```
sudo apt-get autoremove rocminfo
```

If doing this also uninstalls ROCm, don't worry and proceed.

Then reinstall ROCm from the beginning.

ROCm updates are expected to be broken, but new installations should work.

If on your side it fails while ROCm was never installed before, please tell.

---

### 评论 #6 — harkgill-amd (2024-09-25T14:13:48Z)

@illwieckz, could you please confirm if prior to updating Ubuntu, the pinning for repo.radeon was present at `/etc/apt/preferences.d/`? It's possible that some of these entries were disabled during the Ubuntu upgrade process causing the rocminfo package from Ubuntu to be installed. 

We are also exploring a couple of different solutions to handle the versioning incompatibilities and will update this thread once a decision is made.

@MindOfCogsAndMetal as @illwieckz mentioned, please try uninstalling `rocminfo` version `5.7.1-3build1` and then reinstalling ROCm following the [quick start installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html). Please let me know if you encounter any issues during this process

---

### 评论 #7 — MindOfCogsAndMetal (2024-09-25T19:46:04Z)

Thank you both. Uninstalling the system package worked like a charm.

---

### 评论 #8 — TheRealFame (2026-04-29T20:10:49Z)


**Still reproducible on Kubuntu 26.04 (Noble) with ROCm 7.2.2**

System: AMD Ryzen 5 5500, RX 7600, Kubuntu 26.04, KDE Plasma 6.6.4

Hitting the same conflict — Ubuntu ships `rocminfo 7.1.1-0ubuntu1` which blocks `rocm-hip-runtime 7.2.2` from installing since it depends on `rocminfo=1.0.0.70202-86~24.04`.

Workaround that worked:
```bash
sudo apt remove rocminfo
sudo apt install rocminfo=1.0.0.70202-86~24.04
sudo apt install rocm-hip-runtime
```


---
