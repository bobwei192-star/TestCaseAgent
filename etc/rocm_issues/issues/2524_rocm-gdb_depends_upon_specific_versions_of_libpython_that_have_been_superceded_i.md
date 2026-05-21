# rocm-gdb depends upon specific versions of libpython that have been superceded in latest Ubuntu

> **Issue #2524**
> **状态**: closed
> **创建时间**: 2023-10-04T18:03:59Z
> **更新时间**: 2024-11-27T15:29:20Z
> **关闭时间**: 2024-10-07T18:07:23Z
> **作者**: joelandman-amd
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2524

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

In short, while starting debugging efforts for some code I am working on

``` 
jlandman@SCS-L-JLANDMAN:~$ ssh -X scruffy
Linux scruffy 6.1.0-10-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.38-1 (2023-07-14) x86_64
+---------------------------------------------------------------------+
|                                                                     |
|  ____                   __  __        scruffy.scalability.org       |
| / ___|  ___ _ __ _   _ / _|/ _|_   _                                |
| \___ \ / __| '__| | | | |_| |_| | | | 16 core threadripper +        |
|  ___) | (__| |  | |_| |  _|  _| |_| | AMD MI50 GPU         +        |
| |____/ \___|_|   \__,_|_| |_|  \__, | AMD 6600XT RDNA2 GPU          |
|                                 |___/                               |
|                                                                     |
+---------------------------------------------------------------------+

Last login: Wed Oct  4 13:46:15 2023 from 192.168.5.125
joe@scruffy:~$ sudo -s

root@scruffy:/home/joe# apt-get install  rocm-gdb
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 rocm-gdb : Depends: libpython3.10 but it is not installable or
                     libpython3.8 but it is not installable
E: Unable to correct problems, you have held broken packages.

root@scruffy:/home/joe# dpkg -l | grep libpython3 | grep Shared
ii  libpython3.11:amd64                     3.11.2-6                            amd64        Shared Python runtime library (version 3.11)

```

It seems that the requirement for libpython3.x should be for `.x >= 8`

---

## 评论 (8 条)

### 评论 #1 — suamor (2023-10-07T10:01:02Z)

According to https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html the latest supported version is Ubuntu LTS 22.04. On this Ubuntu said libpython 3.10 and 3.8 is available. Also it requires kernel 6.2.

As I see it for other distributions you are on your own. You can use a docker image, install the older libpython from ppa or rebuild rocgdb debian package with the latest libpython (development + dependencies) package(s). 


---

### 评论 #2 — ppanchad-amd (2024-05-14T20:29:32Z)

@joelandman-amd Has your issue been resolved? If so, please close the ticket. Thanks!

---

### 评论 #3 — nairboon (2024-05-18T13:37:05Z)

> @joelandman-amd Has your issue been resolved? If so, please close ticket. Thanks!

@ppanchad-amd this issue is not resolved and it seems to prevent users to install rocm on the latest ubuntu 24.4, see #2939 

---

### 评论 #4 — suparious (2024-07-29T00:10:15Z)

python 3.10 is about 30% slower, and no longer supported in ubuntu 24.04 or Debian 12.

---

### 评论 #5 — tcgu-amd (2024-09-16T21:30:51Z)

@nairboon Hi there! The issue seem to be fixed -- here's the result of `apt-cache show rocm-gdb` for 24.04:
![image](https://github.com/user-attachments/assets/9d38a30e-e249-4314-b78f-5f5902240583)
and for 22.04
![image](https://github.com/user-attachments/assets/10776c88-9ad2-4f4d-8a59-5c5c8f422d4e)

You might want to follow this tutorial here https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html to set up the repository and dependencies correctly for 22.04 and 24.04. 

Thanks!

---

### 评论 #6 — tcgu-amd (2024-10-07T18:07:23Z)

Closing this issue since a fix has been implemented internally and will be shipped with ROCm 6.3. Please feel free to reopen if issue persists after release. Thanks!

---

### 评论 #7 — banderlog (2024-11-27T15:11:32Z)

Now it 3.10 hardcoded

https://scalability.org/a-workaround-for-a-problem/

---

### 评论 #8 — tcgu-amd (2024-11-27T15:29:19Z)

Hi @banderlog thanks for reaching out. We are aware of the issue and are working on getting the fix out as soon as possible. Thanks! 

---
