# [Issue]: rocm install results in "AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status"

> **Issue #5736**
> **状态**: closed
> **创建时间**: 2025-12-03T19:40:05Z
> **更新时间**: 2026-02-20T14:57:01Z
> **关闭时间**: 2026-02-20T14:57:01Z
> **作者**: leopold-grinberg
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5736

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- darren-amd

## 描述

### Problem Description

customer (Altair, **Jonathan Mozo <[jmozo@altair.com](mailto:jmozo@altair.com)>** ) is failing to install rocm and GPU driver. sees various errors:

"when I run sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)”, I get the following. 
 

E:Unable to locate package linux-modules-extra-5.18.2-mi300-build-140423-**ubuntu-22.04**
E: Couldn't find any package by glob 'linux-modules-extra-5.18.2-mi300-build-140423-ubuntu-22.04'

"
then customer was able to move forward a bit and ended up with 

rocm-smi
ERROR:root:Driver not initialized (amdgpu not found in modules)

then customer tried to reinstall rocm and ended up with 

I saw 7.1 was released so I just tried that version and same result when running rocm-smi.

mozo@us-midc-mi300a:/etc/modprobe.d$ rocm-smi


WARNING: No AMD GPUs specified
WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

===================================== ROCm System Management Interface =====================================
=============================================== Concise Info ===============================================
Device  Node  IDs           Temp    Power  Partitions          SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,  GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                              
============================================================================================================
============================================================================================================
=========================================== End of ROCm SMI Log ============================================
jmozo@us-midc-mi300a:/etc/modprobe.d$ 







### Operating System

Ubuntu 22.04

### CPU

NA

### GPU

NA

### ROCm Version

7

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — darren-amd (2025-12-03T19:50:05Z)

Hi @leopold-grinberg,

Thanks for reporting the issue, It looks like `amdgpu` is missing from the system. Could you please try installing it by following the instructions available [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#amdgpu-driver-installation) for ROCm 7.1.1, and see if installing ROCm works after that? Thanks!

---

### 评论 #2 — leopold-grinberg (2025-12-03T20:51:34Z)

[AMD Official Use Only - AMD Internal Distribution Only]

Darren,
Thank you for responding
I filed this on behalf of our customer. I am not the one installing. The ticket has customers contact.

Also - his system is MI300a Sh5 A0

Leopold

Get Outlook for iOS<https://aka.ms/o0ukef>
________________________________
From: darren-amd ***@***.***>
Sent: Wednesday, December 3, 2025 2:50:26 PM
To: ROCm/ROCm ***@***.***>
Cc: Grinberg, Leopold ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: rocm install results in "AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status" (Issue #5736)

Caution: This message originated from an External Source. Use proper caution when opening attachments, clicking links, or responding.

[https://avatars.githubusercontent.com/u/180982888?s=20&v=4]darren-amd left a comment (ROCm/ROCm#5736)<https://github.com/ROCm/ROCm/issues/5736#issuecomment-3608572953>

Hi @leopold-grinberg<https://github.com/leopold-grinberg>,

Thanks for reporting the issue, It looks like amdgpu is missing from the system. Could you please try installing it by following the instructions available here<https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#amdgpu-driver-installation> for ROCm 7.1.1, and see if installing ROCm works after that? Thanks!

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/5736#issuecomment-3608572953>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/ARALBXHUIWJR4METPNLPEIT3745IFAVCNFSM6AAAAACN6REQNCVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTMMBYGU3TEOJVGM>.
You are receiving this because you were mentioned.Message ID: ***@***.***>


---

### 评论 #3 — leopold-grinberg (2025-12-04T15:33:22Z)

I believe that gfx940 has been deprecated ... customer has sh5 socket, A0 HW .. which is gfx940
do we have any workaround ? can we present A0 card as GFX942 for some testing ?




---

### 评论 #4 — ianbmacdonald (2025-12-04T16:51:44Z)

maybe as simple as something like this (assuming the stack is in place)
```
export HSA_OVERRIDE_GFX_VERSION=9.4.2
export ROCR_VISIBLE_DEVICES=1 # If second GPU in system
```

---

### 评论 #5 — leopold-grinberg (2025-12-04T20:51:03Z)

export HSA_OVERRIDE_GFX_VERSION=9.4.2
did not help 

---

### 评论 #6 — briansp2020 (2025-12-13T14:46:25Z)

How did you resolve this issue? I did fresh install of Ubuntu 24.04 server to try out 7900XTX with ROCm 7.10 and noticed that I'm getting this message. The performance is much slower than when I was using 6.x


---

### 评论 #7 — talumbau (2026-01-14T23:04:23Z)

Re-opening since no resolution was provided here and the issue is still impacting users.

---

### 评论 #8 — darren-amd (2026-01-14T23:18:25Z)

Hi @talumbau,

Thanks for checking in, this issue was unrelated to the title and was resolved internally so the ticket was closed. If you are referring to the displayed message indicating a low power state, there is a separate issue reported here: https://github.com/ROCm/ROCm/issues/5849, with the fix linked in that ticket: https://github.com/ROCm/rocm-systems/pull/2510. 

---
