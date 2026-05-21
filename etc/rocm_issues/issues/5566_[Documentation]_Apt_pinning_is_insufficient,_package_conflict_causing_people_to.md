# [Documentation]: Apt pinning is insufficient, package conflict causing people to get stuck on buggy MES firmware

> **Issue #5566**
> **状态**: closed
> **创建时间**: 2025-10-24T04:32:36Z
> **更新时间**: 2025-10-29T11:00:21Z
> **关闭时间**: 2025-10-29T11:00:21Z
> **作者**: ianbmacdonald
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5566

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Description of errors

On the Strix Halo, there are updates to linux-firmware and linux-image making their way into various distributions to resolve the current hanging issues running long duration tasks, often identified by the dmesg output `amdgpu: MES failed to respond to msg=SUSPEND` 

On one popular distribution, Ubuntu 24.04 on Strix Halo, the kernel piece is already in place with package `linux-oem-24.04` but the [firmware piece](https://bugs.launchpad.net/ubuntu/+source/linux-firmware/+bug/2129150) is pending but should appear in proposed any day now.   

There are two problems that are going to cause issues 

1) amdgpu-dkms-firmware takes precedence over linux-firmware  

Even when the pending update to linux-firmware arrives, anybody with Instinct 30.10.2 amdgpu-dkms-firmware is going to be wondering why the problem still exists.   The workaournd ahead of Instinct 30.10.3 is going to be to purge the amdgpu-dkms-firmware package to allow the distribution update to flow through.  Unless there is some configuration to direct firmware priorities, I might expect an Instinct 30.10.3 out the door with just the firmware updates to avoid people purging the amdgpu-dkms-firmware packages.  There are a few open issues which look like they may be stepping through this issue .. I decided to write this after reading them. 

2) anyone running ROCm 6.4.x prior to ROCm 7 probably has a package policy issue becuase of how the new Instinct numbering scheme was implemented

If you upgrade from Instinct/ROCm 6.4.x to Instinct 30.10.2/ROCm 7.0.2, which supports the Strix Halo officially and expands support to Debian 13, prompting upgrades, you end up with an apt policy conflict that is not covered by the apt pinning prefences in the documentation, that simply set the repo.radeon.com to priority 600.   You end up stuck on amdgpu-dkms-firmware from 6.4.x and will never get newer firmware from a 30.10.3 release to fix this MES bug.   This is what the apt policy looks like in this scenario today.

```
# apt policy amdgpu-dkms-firmware

amdgpu-dkms-firmware:
  Installed: 1:6.12.12.60404-2202139.24.04
  Candidate: 1:6.12.12.60404-2202139.24.04
  Version table:
 *** 1:6.12.12.60404-2202139.24.04 100
        100 /var/lib/dpkg/status
     30.10.2.0.30100200-2226257.24.04 600
        600 https://repo.radeon.com/amdgpu/30.10.2/ubuntu noble/main amd64 Packages
```

Unless I missed something, a long-time ROCm 6.4.x user on 24.04 will not be using updated MES firmware even after upgrading both the linux-firmware and linux-kernel and updating repo.radeon.com to Instinct 30.10.3, when they are all released, leading to a bunch more unecessary issues opened on github.  

Maybe some hints on these pages would be helpful:
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/index.html
https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-6.4.4/docs/install/installryz/native_linux/install-ryzen.html

Anyone desperate for a quick fix on Ubuntu 24.04 can sideload the [Resolute linux-firmware](http://launchpadlibrarian.net/824969556/linux-firmware_20251009.git46a6999a-0ubuntu1_all.deb) and remove amdgpu-dkms-firmware, if they are running on a patched kernel.  Just be sure to restore things back to normal when the fixes come down the pipe

`$ sudo apt install linux-firmware/noble --reinstall`

When Instinct 30.10.3 drops with the update

`$ sudo apt install amdgpu-dkms-firmware`

I was surprised to learn how often the MES firmware changes, with no two versions of linux-firmware or amdgpu-dkms-firmware sharing a common version recently.  I have not found a changelog online.  I [documented](https://netstatz.com/strix_halo_lemonade/#Understanding_the_MES_Firmware) the half dozen versions I have seen on Ubuntu/Debian. 


### Attach any links, screenshots, or additional evidence you think will be helpful.

https://launchpad.net/ubuntu/+source/linux-firmware
https://bugs.launchpad.net/ubuntu/+source/linux-firmware/+bug/2129150
https://launchpad.net/ubuntu/+source/linux-oem-6.14
https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2125201
https://bugs-devel.debian.org/cgi-bin/bugreport.cgi?bug=1118658




---

## 评论 (5 条)

### 评论 #1 — tcgu-amd (2025-10-27T14:49:08Z)

Hi @ianbmacdonald, thanks for raising the issue! That is quite insightful. 

> amdgpu-dkms-firmware takes precedence over linux-firmware

Yes as far as I know, this is sort of a necessary evil. I will see if I can get the MES patch more visibility so it will get pushed through dkms updates faster. In the meantime, you can try to manually override dkms firmware versions as you said, but that could cause other potential bugs and wouldn't really be recommended. 

> anyone running ROCm 6.4.x prior to ROCm 7 probably has a package policy issue becuase of how the new Instinct numbering scheme was implemented

I am not quite sure if I understand what the issue is. With that being said, the recommended approach to "cleanly" update ROCm is generally to remove the old version completely then install the new version. 

Maybe we could update https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html. What would you like to see? 

---

### 评论 #2 — ianbmacdonald (2025-10-27T16:20:26Z)

Just trying to help.  I actually run newer kernels that ship with newer amdgpu modules in both my Debian and Ubuntu instances on my Strix Halo, which is why I can remove the amdgpu-dkms-firmware package to make way for linux-firmware to get to the MES 0x80 easily.  Unfortunately, I just realized that vanilla 24.04.3 users with amdgpu-dkms will have to wait for instinct 30.10.3 to ship the new firmware or do something else hacky to get the new firmware via linux-firmware, as amdgpu-dkms-firmware is required by amdgpu-dkms, so it can't be removed as I suggested, unless you are not using amdgpu-dkms.  

I think the simple solution is just to ship the current linux-firmware in amdgpu-dkms-firmware before people start looking for it elsewhere. 

On your note about removing first;  I do recall seeing a callout somewhere suggesting removing the old packages, before installing the new ones (can't seem to find it now);  I think mentioning 'why' would be helpful,  i.e. due to the renumbering snafu from 1:6.4 to 30.10.x, as anyone familiar with deb packaging will chalk that up to a documentation error, and would skip that instruction as I did.   It makes little sense in the deb/apt framework to have to remove a package, before an upgrade, as it should not be required if the package is built correctly.



---

### 评论 #3 — tcgu-amd (2025-10-27T18:33:17Z)

> Just trying to help

Thanks -- help from community members like you is what makes ROCm better, and we really do appreciate it! 

> I think the simple solution is just to ship the current linux-firmware in amdgpu-dkms-firmware before people start looking for it elsewhere

Yeah I agree, that would be ideal. Unfortunately this is not exactly practical due the difference in development and testing cadence between dkms and the main Linux kernel. We do try to make sure important patches go through as quickly as possible whenever we can. For now at least, this is the best we could do. 

> On your note about removing first; I do recall seeing a callout somewhere suggesting removing the old packages, before installing the new ones (can't seem to find it now); I think mentioning 'why' would be helpful, i.e. due to the renumbering snafu from 1:6.4 to 30.10.x, as anyone familiar with deb packaging will chalk that up to a documentation error, and would skip that instruction as I did. It makes little sense in the deb/apt framework to have to remove a package, before an upgrade, as it should not be required if the package is built correctly.

Yeah this is fair. I will see what we can do to update the docs. 

Thanks again for the help! :D


---

### 评论 #4 — ianbmacdonald (2025-10-28T00:22:17Z)

I posted a clean workaround for upstream firmware upgrades in Ubuntu 24.04 in https://github.com/ROCm/ROCm/issues/5151 with a few tweaks to follow apt policy more closely, and survive changing package version numbers, future upgrades that may be imperfect, etc.   

---

### 评论 #5 — ianbmacdonald (2025-10-29T11:00:21Z)

I am going to close this, as I think the docs are sufficient and any shortcomings can be handled by apt policies.  If you happen to just go right to the repo and grab the packages like I did, without fully uninstalling on the way from 6.x to 7.x, you can probably figure out and resolve the policy issues just as I did. 



---
