# [Issue]: Dotted I errors in amdgpu-install if one has Turkish or Azerbaijani as the locale 

> **Issue #2888**
> **状态**: closed
> **创建时间**: 2024-02-08T20:29:54Z
> **更新时间**: 2024-10-10T14:20:39Z
> **关闭时间**: 2024-10-10T14:20:38Z
> **作者**: erkinalp
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/2888

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

` /usr/bin/amdgpu-install: satır 436: ${USECASE_GRAPHİCS_PACKAGES[*]}: hatalı ikame`

### Operating System

Ubuntu 22.04.3

### CPU

Amd Ryzen 9 5950X

### GPU

not relevant as this happens at ROCm installation

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

 Run `sudo amdgpu-install`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

Not relevant for this issue, as it happens while running the installer

### Additional Information

_No response_

---

## 评论 (25 条)

### 评论 #1 — nartmada (2024-02-14T02:15:02Z)

Hi @erkinalp, please provide the GPU info so that we can investigate the issue properly.  Thank you.

---

### 评论 #2 — erkinalp (2024-02-14T07:39:04Z)

RX 5500, but not relevant to reproduce this particular issue; the issue kicks in before any GPU code execution or even a GPU detection happens, thereby preventing installation in the first place.

---

### 评论 #3 — erkinalp (2024-02-14T07:43:05Z)

More particularly, it sees `USECASE_GRAPHİCS_PACKAGES` instead of `USECASE_GRAPHICS_PACKAGES` (see the "İ" instead of "I"), and the former is a nonexistent variable.

---

### 评论 #4 — kentrussell (2024-02-14T13:49:50Z)

@Mystro256 any thoughts?

---

### 评论 #5 — slava-abramov (2024-03-05T22:19:34Z)

How the driver has been installed?  Specifically, where does the installer package comes from?

---

### 评论 #6 — erkinalp (2024-03-06T20:40:58Z)

This applies to both .deb and compiled-from-source versions.

---

### 评论 #7 — erkinalp (2024-03-06T20:41:27Z)

Status of the .rpm version unknown as I do not have a RPM-based testing machine.

---

### 评论 #8 — nartmada (2024-03-22T02:22:49Z)

Hi @erkinalp, can you please clarify (as requested by Slava) where did the installer package come from?  Thanks.

---

### 评论 #9 — erkinalp (2024-03-22T03:17:26Z)

In my case, it is the .deb version from repo.radeon.com

---

### 评论 #10 — nartmada (2024-03-22T03:20:50Z)

Are you using this one?
![image](https://github.com/ROCm/ROCm/assets/144284448/f58062a4-ceb2-4810-a1b8-a64a6ffe220c)


---

### 评论 #11 — slava-abramov (2024-03-22T14:42:35Z)

URL of the installer package would be more helpful.
Also, please upgrade the target system to Ubuntu 22.04.4.

---

### 评论 #12 — erkinalp (2024-03-22T16:48:38Z)

> Are you using this one?

Yes

> Also, please upgrade the target system to Ubuntu 22.04.4.

Too late, already upgraded to 24.04 pre-release, but that detail is not relevant to the issue in hand, because shell expansions still work the same way as before, and there is still no variable called `$USECASE_GRAPHİCS_PACKAGES`

---

### 评论 #13 — slava-abramov (2024-03-22T17:07:11Z)

Agree, just wanted to make sure we will use the same package for repro.

---

### 评论 #14 — nartmada (2024-04-21T14:56:33Z)

@erkinalp, can you please check if your issue still exists with ROCm 6.1.0?  Thanks.

---

### 评论 #15 — erkinalp (2024-04-22T05:21:49Z)

yes, still persists in 6.1

---

### 评论 #16 — erkinalp (2024-04-22T05:22:50Z)

offended line numbers changed but the error is still the same

`/usr/bin/amdgpu-install: satır 490: ${USECASE_GRAPHİCS_PACKAGES[*]}: hatalı ikame`

---

### 评论 #17 — Mystro256 (2024-04-24T01:43:04Z)

Sorry I didn't forget about this, I was just a bit busy. I'm not 100% sure why it's replacing the I with İ.

I opened the script with my system and it's clearly an "I".

---

### 评论 #18 — erkinalp (2024-04-24T16:16:18Z)

> not 100% sure why it's replacing the I with İ.

in Turkish and Azerbaijani, the uppercase form of i is İ and the lowercase form of I is ı.

---

### 评论 #19 — slava-abramov (2024-04-25T14:08:37Z)

I wonder whether the following commands help if added into beginning of the script:

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales

---

### 评论 #20 — erkinalp (2024-04-25T19:27:14Z)

> sudo dpkg-reconfigure locales

I get the first two, but why should I regenerate my locale?

---

### 评论 #21 — slava-abramov (2024-04-25T19:36:04Z)

> > sudo dpkg-reconfigure locales
> 
> I get the first two, but why should I regenerate my locale?

Fair enough.  

Though does it help if you just set LC_ALL and LC_CTYPE?


---

### 评论 #22 — ppanchad-amd (2024-07-17T19:26:52Z)

@erkinalp Has this issue been resolved for you? Thanks!

---

### 评论 #23 — erkinalp (2024-07-17T20:23:17Z)

No, still the same issue, although the workaround listed above temporarily works around.

---

### 评论 #24 — erkinalp (2024-08-03T08:28:34Z)

persists in 6.2

---

### 评论 #25 — sohaibnd (2024-10-10T14:20:39Z)

Hi @erkinalp, this issue has been fixed and should be part of the upcoming ROCm 6.3 release. If the issue has not been fixed by then, please feel free to re-open this ticket. In the meantime, you can use the workaround (setting LC_ALL and LC_CTYPE) @slava-abramov has suggested.

---
