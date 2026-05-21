# [Issue]: rocminfo - Unable to open /dev/kfd read-write: Invalid argument

> **Issue #4043**
> **状态**: closed
> **创建时间**: 2024-11-20T13:10:21Z
> **更新时间**: 2025-09-18T11:07:55Z
> **关闭时间**: 2024-12-09T15:10:08Z
> **作者**: segeljakt
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 5.7.0, ROCm 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/4043

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 5.7.0** (颜色: #ededed)
- **ROCm 6.2.1** (颜色: #ededed)

## 描述

### Problem Description

`rocminfo` produces the output:

```
root:~# rocminfo
ROCk module version 6.7.0 is loaded
Unable to open /dev/kfd read-write: Invalid argument
root is member of nogroup group
```

As a consequence, libraries like Pytorch does seem not detect and use ROCm.

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD EPYC 9474F 48-Core Processor

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.2.1, ROCm 5.7.0

### ROCm Component

rocminfo

### Steps to Reproduce

I installed ROCm 6.2.1 (also happens for ROCm 5.7.0) inside a Ubuntu 22.0.4 Docker container that runs on a host machine with a MI300X GPU. I then added `root` to `render`, `video`, and `nogroup` groups:

```sh
root:~# groups root
root : root video nogroup render
```

The GPU seems to be present:

```
root:/workspace/rocm# rocm-smi --showallinfo

============================ ROCm System Management Interface ============================
============================== Version of System Component ===============================
Driver version: 6.7.0
==========================================================================================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		AMD Instinct MI300X OAM
GPU[0]		: Device ID: 		0x74a1
GPU[0]		: Device Rev: 		0x00
GPU[0]		: Subsystem ID: 	0x74a1
GPU[0]		: GUID: 		8554
...
root:~# rocm_agent_enumerator
gfx000
gfx942
```

However, when I run `rocmsmi` I get this output:

```
root:~# rocminfo
ROCk module version 6.7.0 is loaded
Unable to open /dev/kfd read-write: Invalid argument
root is member of nogroup group
```
In general, it seems like I can't access `/dev/kfd`, even though I'm in the groups:
```
root:~# cat /dev/kfd
Unable to open /dev/kfd read-write: Invalid argument
root:~# /dev/kfd
-bash: /dev/kfd: Permission denied
root:~# ls -l /dev/kfd
crw-rw-rw- 1 nobody nogroup 511, 0 Nov 15 17:12 /dev/kfd
```

Am I missing something?

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
root:~# /opt/rocm/bin/rocminfo --support
ROCk module version 6.7.0 is loaded
Unable to open /dev/kfd read-write: Invalid argument
root is member of nogroup group
```

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2024-11-20T15:53:49Z)

Hi @segeljakt, the presence of the `nogroup` group and it's ownership of `/dev/kfd/` may be causing the permission errors. Could you try updating the permissions of `/dev/kfd` on your host with the following udev rule.
```
echo -e 'KERNEL=="kfd", MODE="0666"\nSUBSYSTEM=="drm", KERNEL=="renderD*", MODE="0666"' | sudo tee /etc/udev/rules.d/70-amdgpu.rules > /dev/null
sudo udevadm control --reload-rules && sudo udevadm trigger
```
Then launch the docker container with 
```
docker run -it --device=/dev/kfd --device=/dev/dri --group-add video <Image Name>
```

If you're still seeing an error running `rocminfo` and nogroup ownership of `/dev/kfd`, apply the aforementioned udev rule again within the container. 

---

### 评论 #2 — Bazza-63 (2024-12-09T00:23:43Z)

If you're still experiencing this problem, simply log in as root and navigate to the kfd folder. Right click on it and set the access permission to allow other users to access it. Solved it for me.

---

### 评论 #3 — harkgill-amd (2024-12-09T15:10:08Z)

@segeljakt, please give both the above suggestions a try when you get a chance. Closing this issue out for now, feel free to leave a comment if you're still encountering any errors and I will re-open this issue. 

---

### 评论 #4 — segeljakt (2024-12-23T10:50:50Z)

Hi, sorry for the late response. I was running ROCm in a Docker container provided by a cloud provider. I did not have access to make modifications on the host machine itself, but everything started working again after starting a new clean container.

---

### 评论 #5 — AndreasMurk (2025-09-18T11:07:55Z)

Hi! I'm facing a similar issue on an unprivileged LXC Container under Proxmox with latest ROCm 7.0.1 and AMD 9070 XT:

I have the right permissions set already (root is both in video and render group).

root@gpu-test-2:~# groups
root video render

I can see both /dev/kfd and /dev/dri*:
```
root@gpu-test-2:~# ls -la /dev/kfd /dev/dri*
crw-rw-rw- 1 root render 511, 0 Sep 18 11:04 /dev/kfd

/dev/dri:
total 0
drwxr-xr-x 2 root root        80 Sep 18 11:04 .
drwxr-xr-x 7 root root       520 Sep 18 11:04 ..
crw-rw---- 1 root video 226, 128 Sep 18 11:04 renderD128
crw-rw---- 1 root video 226, 129 Sep 18 11:04 renderD129
```

I have installed it using the [official instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)

I'm running Ubuntu 24.04 with Kernel 6.14.11-1:

```
root@gpu-test-2:~# uname -srmv
Linux 6.14.11-1-pve #1 SMP PREEMPT_DYNAMIC PMX 6.14.11-1 (2025-08-26T16:06Z) x86_64
```

```
root@gpu-test-2:~# uname -m && cat /etc/*release
x86_64
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04 LTS"
PRETTY_NAME="Ubuntu 24.04 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
```

However, whenever I'm trying to access it using `rocminfo` I keep getting:

```
root@gpu-test-2:~# rocminfo
ROCk module is loaded
Unable to open /dev/kfd read-write: Invalid argument
root is member of render group
```

I am clueless and this point unfortunately

---
