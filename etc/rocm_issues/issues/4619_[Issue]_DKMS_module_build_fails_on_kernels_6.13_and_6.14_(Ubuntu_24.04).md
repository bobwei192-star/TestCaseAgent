# [Issue]: DKMS module build fails on kernels 6.13 and 6.14 (Ubuntu 24.04)

> **Issue #4619**
> **状态**: closed
> **创建时间**: 2025-04-13T05:50:20Z
> **更新时间**: 2025-07-25T20:20:25Z
> **关闭时间**: 2025-07-22T13:52:31Z
> **作者**: bleedingedgedebian
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4619

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

DKMS modules provided by AMD's amdgpu-dkms package consistently fail to build against mainline Linux kernels 6.13 and 6.14 on Ubuntu 24.04. This issue prevents users with new hardware, which explicitly requires newer kernel features, from benefiting from GPU acceleration, ROCm, Vulkan, and OpenCL capabilities provided by AMDGPU.

### Operating System

Ubuntu 24.04.2 with mainline kernels

### CPU

AMD Ryzen 9950x

### GPU

AMD Radeon 9070 XT

### ROCm Version

ROCm 6.4

### ROCm Component

_No response_

### Steps to Reproduce

**Expected Behavior**

The DKMS modules (e.g., amdgpu.ko) should compile and install successfully against newer kernels, enabling full GPU acceleration and ROCm support on recent AMD hardware.

**Actual Behavior**

DKMS fails to build against kernels 6.13/6.14, producing errors similar to:

```
ERROR (dkms apport): kernel package linux-headers-6.14.0-061400-generic is not supported
make[1]: Entering directory '/usr/src/linux-headers-6.14.0-061400-generic'
...
amd/amdgpu/amdgpu_drv.c:3098:10: error: ‘const struct drm_driver’ has no member named ‘date’
```

**Detailed Technical Explanation**

The root cause appears to be API changes introduced in kernels 6.13/6.14, specifically DRM subsystem changes, which the AMDGPU DKMS driver (amdgpu-dkms version 6.4.x) has not adapted to.

Errors indicate structural changes in drm_driver, causing compilation errors (no member named ‘date’, implicit declaration of functions).

Additional build errors due to missing or altered kernel headers, or incompatibilities in the driver code with these kernels.

**Impact**

Users with new hardware (e.g., AMD Radeon RX 7000 series GPUs) are effectively forced to choose between hardware support (newer kernels) and GPU acceleration (AMD's official drivers and ROCm).

**Workarounds**

Currently, no stable workaround exists other than using older kernels (≤ 6.12), which do not fully support newer hardware platforms (e.g., networking issues, lack of full GPU functionality).

**Proposed Solutions**

AMD should update the DKMS drivers explicitly to handle new DRM and kernel API changes in kernels 6.13/6.14.

**Environment**

Ubuntu 24.04 (Noble Numbat)

AMD Radeon 9070 XT

Linux kernels: 6.13.x, 6.14.x

AMDGPU DKMS package: version 6.4

**Additional Information**

This issue explicitly limits users from fully utilizing new AMD hardware, pushing them toward unsupported or unstable configurations.

**Requested Action**

Update the AMDGPU DKMS driver codebase to support Linux kernels 6.13 and 6.14.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (53 条)

### 评论 #1 — ppanchad-amd (2025-04-14T13:50:18Z)

Hi @bleedingedgedebian. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-04-15T15:39:07Z)

Hi @bleedingedgedebian, sorry for the inconvenience. We're working on amdgpu-dkms support for kernel version 6.14. We have this in internal builds at the moment, but not sure when it will make it into a release. I'll update when I have more information.

---

### 评论 #3 — bleedingedgedebian (2025-04-15T18:48:38Z)

That's wonderful, thank you! I will wait patiently.

---

### 评论 #4 — x9q (2025-05-01T15:28:31Z)

Hello, any update on this? Thanks

---

### 评论 #5 — schung-amd (2025-05-01T15:37:24Z)

Sorry for the delay, this should land in the next minor release (6.5 at the time of writing).

---

### 评论 #6 — luispabon (2025-05-08T09:46:23Z)

Hi, any idea when the next minor release will be cut?


---

### 评论 #7 — schung-amd (2025-05-08T20:48:48Z)

Unfortunately I don't have any specific timeline information.

---

### 评论 #8 — BPowell76 (2025-05-08T22:37:08Z)

I hope this is fixed soon. I didn't know this was an issue and everytime it fails I have to reinstall to OS because it breaks the display settings.

---

### 评论 #9 — ChrisSo-DE (2025-05-12T07:43:56Z)

Hi, thank you all for addressing this issue.

I have the same problem here.

Running on **Ubuntu 25.04 Plucky Puffin** with **Kernel 6.14.4** (Mainline) and a **Sapphire Pulse Radeon 9070 XT**.

When using amdgpu-install it throws the same errors as stated by @bleedingedgedebian.

For gaming purposes fortunately Plucky delivers functional drivers for the 9070 XT out of the box so I can use it for the majority of games. However, Cyberpunk is unplayable since it does a hard freeze of the system after 5-30 minutes into the game. Presumably caused by the GPU.
Futhermore, nvtop only shows [AMD GPU] as GPU and no model name or whatsoever.

---

### 评论 #10 — bleedingedgedebian (2025-05-14T04:28:43Z)

Given your release cadence it seems that ROCm 6.5 is still likely 3-6 months away (assuming there are 3-4 point releases on top of 6.4). Kernel 6.15 should be canon in about 2 weeks and is, at least in my testing, basically stable now. Would you kindly test the new ROCm/AMDGPU against kernel 6.15 and perhaps by that time 6.16 as well? I can live on a kernel as "old" as 6.14, I just worry after folks in the future spending on new hardware they cannot utilize without constraints.

---

### 评论 #11 — BPowell76 (2025-05-14T11:04:46Z)

> Given your release cadence it seems that ROCm 6.5 is still likely 3-6 months away (assuming there are 3-4 point releases on top of 6.4). Kernel 6.15 should be canon in about 2 weeks and is, at least in my testing, basically stable now. Would you kindly test the new ROCm/AMDGPU against kernel 6.15 and perhaps by that time 6.16 as well? I can live on a kernel as "old" as 6.14, I just worry after folks in the future spending on new hardware they cannot utilize without constraints.

Unless Ubuntu 25.04 is going to use version 6.15, I really just want it to work with 6.14. But in about 5 months time we'll have 25.10 and I suspect a newer kernel version will be used since Ubuntu is using the latest kernel at the time of the development lock-in date now.

The mesa drivers work, but compared to other projects AMD needs to pick up the pace as most others have newer OS support in a 1 to 2 week period post launch (referring to pgAdmin 4 here).

---

### 评论 #12 — AbelVM (2025-05-14T11:30:38Z)

Strix Point series is only supported in kernel 6.14 +, but there is no ROCm for this kernel. So the "AI" branding is of no use.

---

### 评论 #13 — dominikschnitzer (2025-05-18T19:32:31Z)

Also hit this - I have just patched `amdgpu-dkms_6.12.12.60400-2147987.24.04` so it compiles on 6.14. hope its useful for you. It works fine on my Ubuntu 25.04 system: https://github.com/dominikschnitzer/amdgpu-dkms
The relevant patch is [here](https://github.com/dominikschnitzer/amdgpu-dkms/commit/5f9c8bc4150749eedd912c5b684f8d5f909ed8c4), a deb is [here](https://github.com/dominikschnitzer/amdgpu-dkms/releases/tag/amdgpu-dkms_6.12.12.60400-2147987.24.04-2).

---

### 评论 #14 — JanneM (2025-05-25T09:39:38Z)

The RX9000 series is still new. I guess that once Ubuntu LTS catches up with the recent kernels (6.15+) and Mesa this will become a non-issue, and we can have both ROCm and gaming fully supported. But that is a year away. And soon after, the next series of GPUs are probably on their way, and their owners will face the same issue.

It would probably help a lot if there could be interim source releases or similar so people feeling adventurous could build the bleeding edge software against their own distro, and even third-party PPAs.

The *ideal* would be if ROCm gets included into the distro repository, like CUDA already is. But I realize that is a long-term project, if it is even feasible.


---

### 评论 #15 — SkyAgency (2025-05-28T07:51:22Z)

> Also hit this - I have just patched `amdgpu-dkms_6.12.12.60400-2147987.24.04` so it compiles on 6.14. hope its useful for you. It works fine on my Ubuntu 25.04 system: https://github.com/dominikschnitzer/amdgpu-dkms The relevant patch is [here](https://github.com/dominikschnitzer/amdgpu-dkms/commit/5f9c8bc4150749eedd912c5b684f8d5f909ed8c4), a deb is [here](https://github.com/dominikschnitzer/amdgpu-dkms/releases/tag/amdgpu-dkms_6.12.12.60400-2147987.24.04-2).

Thanks for the fix and package, but I have a problem with dependencies:

`amdgpu-dkms : Wymaga: amdgpu-dkms-firmware (= 1:6.12.12.60400-2147987.24.04) ale 1:6.12.12.60401-2164967.24.04 jest zainstalowany`

maybe you need to rebuild the package with the latest amdgpu-dkms-firmware package? I installed it without dependencies and everything works fine, but I still have a dependency error in system.

---

### 评论 #16 — dominikschnitzer (2025-05-29T12:57:31Z)

> maybe you need to rebuild the package with the latest amdgpu-dkms-firmware package? I installed it without dependencies and everything works fine, but I still have a dependency error in system.

I've just updated the package. Hope it works for you. Not sure how to keep things updated automatically.

---

### 评论 #17 — SkyAgency (2025-06-03T08:22:56Z)

> > maybe you need to rebuild the package with the latest amdgpu-dkms-firmware package? I installed it without dependencies and everything works fine, but I still have a dependency error in system.
> 
> I've just updated the package. Hope it works for you. Not sure how to keep things updated automatically.

Thank you! It works perfectly now.

---

### 评论 #18 — mzymon (2025-06-11T11:55:51Z)

> Unfortunately I don't have any specific timeline information.

@schung-amd Do you have any updates about the new release that will address that issue?

---

### 评论 #19 — schung-amd (2025-06-11T15:25:40Z)

No new info unfortunately, likely still a few months out.

---

### 评论 #20 — cscd98 (2025-06-13T14:50:20Z)

@dominikschnitzer I'm trying this on Ubuntu 25.04 and I get the following errors:

```
Errors were encountered while processing:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

I've tried the deb shared above but has errors also:

sudo dpkg -i amdgpu-dkms_6.12.12.60400-2147987.24.04-2_all.deb 
```
dpkg: warning: downgrading amdgpu-dkms (1:6.12.12.60401-2164967.24.04) to (1:6.12.12.60400-2147987.24.04-2)
(Reading database ... 244292 files and directories currently installed.)
Preparing to unpack amdgpu-dkms_6.12.12.60400-2147987.24.04-2_all.deb ...
Deleting module amdgpu-6.12.12-2164967.24.04 completely from the DKMS tree.
Unpacking amdgpu-dkms (1:6.12.12.60400-2147987.24.04-2) over (1:6.12.12.60401-2164967.24.04) ...
dpkg: dependency problems prevent configuration of amdgpu-dkms:
 amdgpu-dkms depends on amdgpu-dkms-firmware (= 1:6.12.12.60400-2147987.24.04); however:
  Version of amdgpu-dkms-firmware on system is 1:6.12.12.60401-2164967.24.04.

dpkg: error processing package amdgpu-dkms (--install):
 dependency problems - leaving unconfigured
Errors were encountered while processing:
 amdgpu-dkms
```

---

### 评论 #21 — SkyAgency (2025-06-13T23:14:19Z)

> [@dominikschnitzer](https://github.com/dominikschnitzer) I'm trying this on Ubuntu 25.04 and I get the following errors:
> 
> ```
> Errors were encountered while processing:
>  amdgpu-dkms
> E: Sub-process /usr/bin/dpkg returned an error code (1)
> ```
> 
> I've tried the deb shared above but has errors also:
> 
> sudo dpkg -i amdgpu-dkms_6.12.12.60400-2147987.24.04-2_all.deb
> 
> ```
> dpkg: warning: downgrading amdgpu-dkms (1:6.12.12.60401-2164967.24.04) to (1:6.12.12.60400-2147987.24.04-2)
> (Reading database ... 244292 files and directories currently installed.)
> Preparing to unpack amdgpu-dkms_6.12.12.60400-2147987.24.04-2_all.deb ...
> Deleting module amdgpu-6.12.12-2164967.24.04 completely from the DKMS tree.
> Unpacking amdgpu-dkms (1:6.12.12.60400-2147987.24.04-2) over (1:6.12.12.60401-2164967.24.04) ...
> dpkg: dependency problems prevent configuration of amdgpu-dkms:
>  amdgpu-dkms depends on amdgpu-dkms-firmware (= 1:6.12.12.60400-2147987.24.04); however:
>   Version of amdgpu-dkms-firmware on system is 1:6.12.12.60401-2164967.24.04.
> 
> dpkg: error processing package amdgpu-dkms (--install):
>  dependency problems - leaving unconfigured
> Errors were encountered while processing:
>  amdgpu-dkms
> ```

Try this new package: [https://github.com/dominikschnitzer/amdgpu-dkms/releases/download/amdgpu-dkms_amdgpu-6.12.12-2164967.24.04-2/amdgpu-dkms_6.12.12.60401-2164967.24.04-2_all.deb](https://github.com/dominikschnitzer/amdgpu-dkms/releases/download/amdgpu-dkms_amdgpu-6.12.12-2164967.24.04-2/amdgpu-dkms_6.12.12.60401-2164967.24.04-2_all.deb)

---

### 评论 #22 — cscd98 (2025-06-14T20:06:28Z)

New package installed fine thanks 👍 

---

### 评论 #23 — asvishnyakov (2025-07-17T20:24:21Z)

And now 6.14 is official HWE kernel for 24.04, yet there is still no fix...

---

### 评论 #24 — IAALAI (2025-07-17T21:40:00Z)

Yes, this problem still exists... I run upgrade failed...

---

### 评论 #25 — ChihweiLHBird (2025-07-18T08:36:19Z)

Just got shocked by a kernel panic after an upgrade, and then realized it's an AMD driver issue. Please fix it ASAP if AMD still plan to support Ubuntu 24.04 LTS

---

### 评论 #26 — reginaldbondoc (2025-07-18T09:18:21Z)

@dominikschnitzer 

Thanks for your patch!

I tried installing your [latest package](https://github.com/dominikschnitzer/amdgpu-dkms/releases/download/amdgpu-dkms_amdgpu-6.12.12-2164967.24.04-2/amdgpu-dkms_6.12.12.60401-2164967.24.04-2_all.deb) but I get:

```
Preparing to unpack .../amdgpu-dkms_6.12.12.60401-2164967.24.04-2_all.deb ...
Unpacking amdgpu-dkms (1:6.12.12.60401-2164967.24.04-2) ...
dpkg: dependency problems prevent configuration of amdgpu-dkms:
 amdgpu-dkms depends on amdgpu-dkms-firmware (= 1:6.12.12.60401-2164967.24.04); however:
  Package amdgpu-dkms-firmware is not installed.

dpkg: error processing package amdgpu-dkms (--install):
 dependency problems - leaving unconfigured
Errors were encountered while processing:
 amdgpu-dkms
```

Where can I get this dependency firmware?

Thanks!

---

### 评论 #27 — FranzXaver (2025-07-18T11:36:26Z)

>   Package amdgpu-dkms-firmware is not installed.
> 
> Where can I get this dependency firmware?
> 
> Thanks!

You can download it here manually:
https://repo.radeon.com/amdgpu/6.4.1/ubuntu/pool/main/a/amdgpu-dkms/

Or you can add this repository in your apt sources (/etc/apt/sources.list.d/amdgpu.list) (change noble to your release):
`deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.4.1/ubuntu noble main`

Better yet, install it with the official installer:
https://www.amd.com/en/support/download/linux-drivers.html

---

### 评论 #28 — asvishnyakov (2025-07-18T14:54:50Z)

You can hold linux kernel update using this command:

```bash
sudo apt-mark hold linux-image-6.14.0-24-generic linux-headers-6.14.0-24-generic linux-modules-6.14.0-24-generic linux-modules-extra-6.14.0-24-generic
```

But for sure we're all awaiting fix from AMD, especially considering it says 6.14 is supported on 25.10

--

Also seems like issue not ROCm specific and all graphic drivers from AMD site fail with the same error

---

### 评论 #29 — hazecodeio (2025-07-18T22:47:22Z)

I'm on Ubuntu 24.04. Linux-6.14 has just been pushed to it.  So the install failed as noted by the folx above.

The solution offered by @dominikschnitzer (thank you for your efforts) fixed the problem. However, since I already have a running Linux-6.11, the deb package offered by @dominikschnitzer failed when it came to rebuild the previous Linux (<= 6.11) images with this deb.

After wrestling with the dilemma, I figured modifying **dkms.conf** with  **BUILD_EXCLUSIVE_KERNEL="^(6\.14\.[0-9]+.*)"** did the trick for me.

Link to Commit: https://github.com/hazecodeio/amdgpu-dkms-schnitzer/commit/afaaadc1a93518d6e3159c1b7036067d80ee00aa

I also created a PR for @dominikschnitzer (feel free to either accept, reject, or recommend modification).

I hope this helps those going through the same issue.

NOTE: My intent is to catch up with latest Linux Image pushed on the distro. If your priorities is to keep the AMDGPU as functional as possible, you should follow @asvishnyakov approach by suspending the upgrad to Linux-6.14.

---

### 评论 #30 — hazecodeio (2025-07-18T23:05:37Z)

Question: Is it possible to create multiple **amdgpu-dkm.deb** packages each of which intended for a particular Linux Image on the system??

I wanted to create two **amdgpu-dkms.deb**. One for Linux (>= 6.14) and the other one for Linux (<= 6.11). Every time I trigger one deb, it removes everything related to a **PACKAGE_NAME="amdgpu"**

Is it even doable?

---

### 评论 #31 — SharkMachine (2025-07-19T19:56:32Z)

Ubuntu has started shipping 6.14 as part of HWE. I cannot install that kernel because of this.

---

### 评论 #32 — SharkMachine (2025-07-19T20:07:57Z)

I switched to team red because it was supposed to have better support for Linux. Now I'm thinking I made a mistake and I should have bought RTX 5060 TI instead :(

---

### 评论 #33 — ChihweiLHBird (2025-07-19T21:34:49Z)

Hi @schung-amd, update anytime soon as Ubuntu pushed 6.14 kernel to 24.04 LTS HWE?

---

### 评论 #34 — ChihweiLHBird (2025-07-19T21:44:22Z)

> I switched to team red because it was supposed to have better support for Linux. Now I'm thinking I made a mistake and I should have bought RTX 5060 TI instead :(

Intel Arc drivers are getting consistent improvements on Linux in my observation. 😉

---

### 评论 #35 — BPowell76 (2025-07-20T21:56:20Z)

> I switched to team red because it was supposed to have better support for Linux. Now I'm thinking I made a mistake and I should have bought RTX 5060 TI instead :(

AMD has native support in the kernel with the Mesa drivers. AMD's own drivers, though, seem to only work with the LTS Ubuntu versions. Though this isn't really just an AMD issue. I have had this issue with other software using the non-LTS version of Ubuntu.

---

### 评论 #36 — danjaredg (2025-07-21T01:21:37Z)

I confirm this [patch](https://github.com/dominikschnitzer/amdgpu-dkms/commit/5f9c8bc4150749eedd912c5b684f8d5f909ed8c4) for kernel 6.14.0-24 on Ubuntu 24.04.2 is working and it is stable.

You can download the package on this [link](https://github.com/dominikschnitzer/amdgpu-dkms/releases/tag/amdgpu-dkms_amdgpu-6.12.12-2164967.24.04-2)

---

### 评论 #37 — fighter3005 (2025-07-21T08:27:39Z)

> I confirm this [patch](https://github.com/dominikschnitzer/amdgpu-dkms/commit/5f9c8bc4150749eedd912c5b684f8d5f909ed8c4) for kernel 6.14.0-24 on Ubuntu 24.04.2 is working and it is stable.
> 
> You can download the package on this [link](https://github.com/dominikschnitzer/amdgpu-dkms/releases/tag/amdgpu-dkms_amdgpu-6.12.12-2164967.24.04-2)

Will this eventually end up in the amd repository, so I can just sudo apt install it? (also just upgraded, without checking for compatibility issues, haha)

---

### 评论 #38 — cscd98 (2025-07-21T08:42:33Z)

I'm already on 6.15 and sure enough 6.16 is around the corner very soon. AMD you need to keep up tracking Linux kernel's much quicker than this!

---

### 评论 #39 — schung-amd (2025-07-21T15:06:20Z)

Hi all, sorry for the delay. The fix for this should land in ROCm 6.4.2, hopefully early this week if not today.


---

### 评论 #40 — dtl131 (2025-07-21T21:42:21Z)

@schung-amd , either ROCm 6.4.2 does not support 6.14 HWE or you forgot to put it in the release notes:
https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.4.2/reference/system-requirements.html

---

### 评论 #41 — Wedge009 (2025-07-21T23:16:53Z)

May be just documentation oversight. I am running Ubuntu kernel 6.14.0-24 with ROCm 6.4.2 on all my machines as of < 15 minutes before time of writing.

---

### 评论 #42 — andrioid (2025-07-22T08:17:23Z)

Just remember to do a `sudo apt update` before installing the "linux-image-generic-hwe-24.04" again. I mistakenly fetched the latest AMD deb and assumed I was up to date. But, it needs to update the APT sources too.

But, I can confirm that it works now with Linux Kernel 6.14 and ROCm 6.4.2 

---

### 评论 #43 — schung-amd (2025-07-22T13:52:31Z)

@dtl131 Thanks for bringing that to our attention, I'll reach out to the docs team to get that fixed.

Closing this for now, but if anyone runs into trouble with kernel 6.14 and ROCm 6.4.2 or later, feel free to comment here and we can reopen if necessary. Sorry again that this took so long!

---

### 评论 #44 — Blaze-Leo (2025-07-22T15:22:57Z)

So I got a 9000 series card, and to be able to control the fan curves (very bad premade curve, literally at 50% when junction temperature reaches 100), but I need 6.15 to run on LACT. Is there any update on when 6.15 will be supported? Also I have the adrenaline software on Windows as dual boot. Is there any way to load a custom fan profile as the default into the GPU? that would save a little trouble.

---

### 评论 #45 — dtl131 (2025-07-22T16:53:47Z)

@Blaze-Leo : please start a new issue for 6.15

---

### 评论 #46 — sjjh (2025-07-23T16:28:40Z)

I was hoping to use the updated package, but somehow even after an `apt update` I'm still only seeing the old version `6.10.5.60300-2084815.24.04`. What am I doing wrong?

```
user@laptop:~$ uname --all
Linux laptop 6.11.0-29-generic #29~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Jun 26 14:16:59 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
user@laptop:~$ sudo apt update
OK:1 http://download.opensuse.org/repositories/graphics:/darktable/xUbuntu_24.04  InRelease
OK:2 http://security.ubuntu.com/ubuntu noble-security InRelease                                                                                                        
OK:3 https://repo.radeon.com/amdgpu/6.3/ubuntu noble InRelease                                                                                                         
OK:4 https://updates.signal.org/desktop/apt xenial InRelease                                                                                   
OK:5 https://repo.radeon.com/rocm/apt/6.3 noble InRelease                                                              
OK:6 http://archive.ubuntu.com/ubuntu noble InRelease                                                        
OK:7 https://ppa.launchpadcontent.net/inkscape.dev/stable/ubuntu noble InRelease
OK:8 https://ppa.launchpadcontent.net/libreoffice/ppa/ubuntu noble InRelease
OK:9 https://ppa.launchpadcontent.net/pbek/qownnotes/ubuntu noble InRelease
OK:10 http://archive.ubuntu.com/ubuntu noble-updates InRelease
OK:11 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Paketlisten werden gelesen… Fertig
Abhängigkeitsbaum wird aufgebaut… Fertig
Statusinformationen werden eingelesen… Fertig
Aktualisierung für 1 Paket verfügbar. Führen Sie »apt list --upgradable« aus, um es anzuzeigen.
user@laptop:~$ apt-cache policy amdgpu-dkms
amdgpu-dkms:
  Installiert:           1:6.10.5.60300-2084815.24.04
  Installationskandidat: 1:6.10.5.60300-2084815.24.04
  Versionstabelle:
 *** 1:6.10.5.60300-2084815.24.04 600
        600 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 Packages
        100 /var/lib/dpkg/status
```

---

### 评论 #47 — Blaze-Leo (2025-07-23T16:35:51Z)

@sjjh it's better if you just go to the official site and re follow the instructions, just the apt update won't work. I see you have the amdgpu-dkms installed, so I would suggest that you first do a `apt purge amdgpu-dkms` then install the 6.14 kernel using `mainline` then execute these, make sure you do all these in one session without logging out.

```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.4.2/ubuntu/noble/amdgpu-install_6.4.60402-1_all.deb
sudo apt install ./amdgpu-install_6.4.60402-1_all.deb
sudo amdgpu-install -y --usecase=graphics,rocm
sudo usermod -a -G render,video $LOGNAME
```

---

### 评论 #48 — sjjh (2025-07-23T16:43:26Z)

thx for your reply. After `purge`ing it, shouldn't a simple `apt install amdgpu-dkms` install the updated version? If I use `wget` and install the `deb` manually, I'll miss future updates, wouldn't I?

---

### 评论 #49 — Blaze-Leo (2025-07-23T16:46:05Z)

@sjjh Completely saying out of experience, rocm updates come in big time intervals, and it isn't that time consuming to just run a wget everytime you run into a problem, after all why bother updating if it works

---

### 评论 #50 — ChihweiLHBird (2025-07-23T19:48:04Z)

> thx for your reply. After `purge`ing it, shouldn't a simple `apt install amdgpu-dkms` install the updated version? If I use `wget` and install the `deb` manually, I'll miss future updates, wouldn't I?

AMD official ppa repository is like one repository per version. Meaning you won't get the newer version with a simple `apt upgrade`, and you will have to add a new repository for the upgrade.

---

### 评论 #51 — asvishnyakov (2025-07-23T20:03:29Z)

@ChihweiLHBird Yep, and the reason for that is AMD's recommendation to completely remove the previous version before installing a new one, as they don't support in-place upgrades

---

### 评论 #52 — justinlietz93 (2025-07-24T04:31:09Z)

> Just got shocked by a kernel panic after an upgrade, and then realized it's an AMD driver issue. Please fix it ASAP if AMD still plan to support Ubuntu 24.04 LTS

this happened to me, and it caused my boot drive to be corrupted after a system update conflicted with the drivers. Had no boot loader, no grub, and it left a lot of system files broken.

Took me hours debugging and troubleshooting in live usb to get it fixed, then created a timeshift snapshot.

---

### 评论 #53 — schung-amd (2025-07-25T20:20:25Z)

An update re: compatibility matrix, this won't be updated to reflect 6.14 kernel support until after the official Ubuntu 24.04.3 HWE kernel release (scheduled for August 7th), but this is purely on the docs end.

---
