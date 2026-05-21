# [Issue]: Update `amd-ttm` tool to configure `amd-ttm`/`ttm` module respectively based on architecture

> **Issue #5562**
> **状态**: closed
> **创建时间**: 2025-10-22T19:45:41Z
> **更新时间**: 2026-03-31T16:10:11Z
> **关闭时间**: 2026-03-31T16:09:41Z
> **作者**: ianbmacdonald
> **标签**: Feature Request, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5562

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

**Issue:** On Strix Halo, passing the usual amdttm.page_pool_size value no longer provided the requested amount of unified memory (125 GiB in our case, and shown below).   This problem was consistent with Debian 13 / Kernel 6.12 / amdgpu 6.14.14 and Ubuntu 25.10 / Kernel 6.17 / amdgpu 6.17.0 both with ROCm 7.0.2/noble apt repositories configured.   

With the recent ROCm 7.0.2 release, we rolled forwards our Debian from Bookworm (12) to Trixie (13), now that it is officially supported and GTT allocations for unified memory no longer worked as they previously did. 

The testing was performed on a Strix Halo, but likely extends to all ROCm platforms.   Users that are using the deprecated amdgpu.gttsize parameter will land on a working configuration, and may not notice both the deprecation and conficting value warnings in their dmesg.  Who knows how long that will work, and to avoid a bunch of uncessary issues down the road, documentation updates should be made as this change suggests full deprecation is likely to happen in the next version. 

Anyone using this properly today, also may not search sysfs looking for the new parameters when it stops working, so it would probably be a good idea to drop in the release notes (https://rocm.docs.amd.com/en/latest/about/release-notes.html and https://github.com/ROCm/ROCm/releases/tag/rocm-7.0.2) 

It would be good on these RTD pages too:
https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/system-optimization/mi300a.html (needs update)
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html (missing completely)


**Addition Observations:** Both partitions were upgraded from working Debian 12 / ROCm 7.0.1 and Ubuntu 25.04 / ROCm 7.0.1 respectively, from working configurations with no changes to kernel parameters, further suggesting the issue originates from the ROCm 7.0.1 to 7.0.2 upgrade. 

**Workaround:** Adding the deprecated amdgpu.gttsize value delivered the requested configuration, along with deprecation warnings, and warnings about conflicting values between parameters in the newer upstream version (amdgpu 6.17.0-5)

**Fix:** Migrate `amdttm.page_pool_size` to `ttm.page_pool_size` and `amdttm.pages_limit` to `ttm.pages_limit` and remove deprecated `amdgpu.gttsize` to clear noise during enumeration.

Additional outputs from amd-smi, dmesg follow the requested system information pattern below.



```
#   echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   

#   echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
OS:
NAME="Debian GNU/Linux"
VERSION="13 (trixie)"
ai2:~#   echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
CPU: 
model name	: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

#   echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic 
```





Below are the results from Debian 13 (Officially supported with ROCm 7.0.2) and Ubuntu 25.10 (Using upstream amdgpu with ROCm 7.0.2).   

```
# amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.0.2+39589fda      amdgpu version: Linuxver ROCm version: 7.0.2    |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0    AMD Radeon Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A              161/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```

Debian 13 - amdgpu.gttsize=amdttm.page_pool_size (125GiB) , no deprecation warning present, and GTT set correctly to 125GiB, and no warning of conflicting values.

```
[    0.000000] Linux version 6.12.48+deb13-amd64 (debian-kernel@lists.debian.org) (x86_64-linux-gnu-gcc-14 (Debian 14.2.0-19) 14.2.0, GNU ld (GNU Binutils for Debian) 2.44) #1 SMP PREE
MPT_DYNAMIC Debian 6.12.48-1 (2025-09-20)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.12.48+deb13-amd64 root=UUID=1a6903bb-2dec-435d-845d-4f6e21505860 ro transparent_hugepage=always numa_balancing=disable amdgpu.gt
tsize=128000 amdttm.pages_limit=32768000 amdttm.page_pool_size=32768000
...
[    3.635701] amdgpu 0000:c5:00.0: amdgpu: VRAM: 512M 0x0000008000000000 - 0x000000801FFFFFFF (512M used)
[    3.635703] amdgpu 0000:c5:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    3.636121] [drm] amdgpu: 512M of VRAM memory ready
[    3.636122] [drm] amdgpu: 128000M of GTT memory ready.
```

Debian 13 - amdttm.page_pool_size (125GiB), no deprecation warning, GTT not set correctly (63973MiB)

```
[    0.000000] Linux version 6.12.48+deb13-amd64 (debian-kernel@lists.debian.org) (x86_64-linux-gnu-gcc-14 (Debian 14.2.0-19) 14.2.0, GNU ld (GNU Binutils for Debian) 2.44) #1 SMP PREE
MPT_DYNAMIC Debian 6.12.48-1 (2025-09-20)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.12.48+deb13-amd64 root=UUID=1a6903bb-2dec-435d-845d-4f6e21505860 ro transparent_hugepage=always numa_balancing=disable amdttm.pa
ges_limit=32768000 amdttm.page_pool_size=32768000
...
[    3.657645] amdgpu 0000:c5:00.0: amdgpu: VRAM: 512M 0x0000008000000000 - 0x000000801FFFFFFF (512M used)
[    3.657647] amdgpu 0000:c5:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    3.657841] [drm] amdgpu: 512M of VRAM memory ready
[    3.657851] [drm] amdgpu: 63973M of GTT memory ready.
```

```
+------------------------------------------------------------------------------+
| AMD-SMI 26.0.2+39589fda      amdgpu version: 6.17.0-5 ROCm version: 7.0.2    |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0  Radeon 8060S Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A              161/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```

Ubuntu 25.10 - amdgpu.gttsize=amdttm.page_pool_size (125GiB) , deprecation warning present, and GTT set correctly to 125GiB, and also a warning about conflicting values.
```
[    0.000000] Linux version 6.17.0-5-generic (buildd@lcy02-amd64-035) (x86_64-linux-gnu-gcc (Ubuntu 15.2.0-4ubuntu2) 15.2.0, GNU ld (GNU Binutils for Ubuntu) 2.45) #5-Ubuntu SMP PREEM
PT_DYNAMIC Mon Sep 22 10:00:33 UTC 2025 (Ubuntu 6.17.0-5.5-generic 6.17.0-rc7)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.17.0-5-generic root=UUID=cea76f55-f802-4ef3-a1cd-ebda84150293 ro transparent_hugepage=always amdgpu.gttsize=128000 amdttm.pages_
limit=32768000 amdttm.page_pool_size=32768000 numa_balancing=disable quiet splash crashkernel=2G-4G:320M,4G-32G:512M,32G-64G:1024M,64G-128G:2048M,128G-:4096M vt.handoff=7
...
[    3.368748] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 512M of VRAM memory ready
[    3.368749] amdgpu 0000:c5:00.0: amdgpu: [drm] Configuring gttsize via module parameter is deprecated, please use ttm.pages_limit
[    3.368750] amdgpu 0000:c5:00.0: amdgpu: [drm] GTT size has been set as 134217728000 but TTM size has been set as 65867993088, this is unusual
[    3.368751] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 128000M of GTT memory ready.
```
Ubuntu 25.10 - amdttm.page_pool_size (125GiB), no deprecation warning, GTT not set correctly (62816MiB)
```
[    0.000000] Linux version 6.17.0-5-generic (buildd@lcy02-amd64-035) (x86_64-linux-gnu-gcc (Ubuntu 15.2.0-4ubuntu2) 15.2.0, GNU ld (GNU Binutils for Ubuntu) 2.45) #5-Ubuntu SMP PREEM
PT_DYNAMIC Mon Sep 22 10:00:33 UTC 2025 (Ubuntu 6.17.0-5.5-generic 6.17.0-rc7)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.17.0-5-generic root=UUID=cea76f55-f802-4ef3-a1cd-ebda84150293 ro transparent_hugepage=always amdttm.pages_limit=32768000 amdttm.
page_pool_size=32768000 numa_balancing=disable quiet splash crashkernel=2G-4G:320M,4G-32G:512M,32G-64G:1024M,64G-128G:2048M,128G-:4096M vt.handoff=7
...
[    3.309617] amdgpu 0000:c5:00.0: amdgpu: VRAM: 512M 0x0000008000000000 - 0x000000801FFFFFFF (512M used)
[    3.309619] amdgpu 0000:c5:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    3.310034] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 512M of VRAM memory ready
[    3.310035] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 62816M of GTT memory ready.
```

### Operating System

Debian,  Ubuntu

### CPU

Strix Halo

### GPU

gfx1151

### ROCm Version

7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — hammmmy (2025-10-22T23:13:52Z)

The [documentation ](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#configure-shared-memory) recommends downloading `amd-debug-tools` wheel from PyPi and using the `amd-ttm` as it uses the right interface for inbox kernel for Strix Halo.

---

### 评论 #2 — harkgill-amd (2025-10-27T16:23:06Z)

To piggyback off what @hammmmy mentioned, there are two separate modules being referred to here, `ttm` vs `amdttm`.

The `ttm` module is the generic memory management module used by the in-kernel `amdgpu` drivers. As Strix Halo uses these in-kernel drivers, the [Ryzen documentation](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#configure-shared-memory) recommends using the `amd-ttm` tool which will correctly configure the values at /sys/module/**ttm**/parameters/pages_limit. This is the same as manually setting the kernel boot parameter `ttm.pages_limit`.

As for the `amdttm` module, this is specific to our `amdgpu-dkms` package. Instinct APUs (MI300A) depend on this package/module therefore the [MI300A documentation](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/system-optimization/mi300a.html#operating-system-settings) points to configuring amdttm values at /sys/module/**amdttm**/parameters/pages_limit. One of the options to configure this is with the `amdttm.pages_limit` boot parameter.

This does just end up being a case of "do this for Ryzen" vs "do this for Instinct. We are working on cleaning up our documentation spaces to minimize issues such as this in the future. Hope this clears up any confusion on this topic - if you do have any questions feel free to leave a comment.

---

### 评论 #3 — ianbmacdonald (2025-10-28T15:41:40Z)

Okay, I think I understand.   The amdgpu-dkms is required to update older kernels with the modern amdgpu kernel module.  The forward path is the in-kernel module for >Debian 13, Ubuntu 25.04, etc. which seems like a pattern for any distribution >= linux-6.16 based on the versions available today.  

To propose using amd-debug-tools, with the amd-ttm executable for managing the amdgpu kernel module parameters, it should be properly packaged.  I propose this ticket be changed to a feature request to move in that direction.  Leverage the existing security managed python libraries in the distribution, and move away from a package with the name 'debug' in it to manage the amd-ttm executable used to manage system configuration. 

The reason being, that the amd-ttm tool requires setting up and maintaining a separate python environment or just installing a bunch of python modules statically and globally (which is never a good idea) that are likely to break as soon as they fall out of sync with the distribution libraries. 

In other words, the current pip install is just creating a mess of cruft, some 22 packages, against whatever version of python is being used in the moment.  This approach is unlikely to manage dependencies properly across an upgrade, and could be argued to to not really be suitable in a production environment, or for use with anything long term.  

An alternative approach for amd_ttm in its current state might be to create a reproducable uv.lock file across environments that you could also drag across upgrades and re-sync and/or update periodically. 

```
uv init --python 3.13
uv add amd-debug-tools
uv tool install amd-debug-tools
uv tool list 
```

For the Strix Halo, simply setting both amdttm.page_pool_size and ttm.page_pool_size to handle situations where you have workflow that needs to deal with both 6.14+dkms and >=6.16 in-kernel amdgpu is simpler, survives forward package and distribution upgrades and does not introduce unexpected outcomes that might occur from maintaining and depending on a random python venv to handle this configuration detail. 

Using `/etc/default/grub.d/amd_ttm.cfg` prevents the grub customization from triggering a user prompt during upgrades of grub of any kind.  This might include automated and periodic package security updates via apt.  It avoids the dependency on setting up and maintaining a python environment for the amd_ttm tool.

Below is what I currently use with the Strix Halo to generically pin the unified VRAM at 125 GiB (a bit of wiggle room to avoid crazy oom-killing) across all versions of Debian and Ubuntu with various kernels in the 6.12 -> 6.17 range, some with dkms, other using the in-kernel amdgpu. 

```
# /etc/default/grub.d/amd_ttm.cfg
GRUB_CMDLINE_LINUX="${GRUB_CMDLINE_LINUX:+$GRUB_CMDLINE_LINUX }ttm.pages_limit=32768000 ttm.page_pool_size=32768000 amdttm.pages_limit=32768000 amdttm.page_pool_size=32768000"


```




---

### 评论 #4 — ianbmacdonald (2025-10-29T15:11:59Z)

Here are a few ideas to improve amd-ttm, beyond making it a real, security maintained distribution package:
- emit a version, as it is difficult to know what you are dealing with from users, unless you expect dumps of python environments to come with any new issues
- handle the ttm and amdttm scenarios gracefully, including adding and removing the configuration based on which kernel modules are loaded and/or present (appears broken for 24.04 currently as noted in #5595 )
- use GiB instead of GB to be precise with the math, making outputs suitable for use with AI vibe configuration assistance
- be clear in the output on what has been set in configuration vs what is running in the current session
- trigger an `update-initramfs -u -k all` to make sure amd-ttm impacts all configured kernels;  perhaps if not, at least compare configuration file modification times with initramfs modification times and emit a warning to users that the configuration is newer than the deployed image


---

### 评论 #5 — chrismrutherford (2026-01-11T12:23:29Z)

I can confirm that the amd-ttm tool didn't work with Linux Mint 22.2 (based on Ubuntu 24.04) for updating my Strix Halo GPU kernel parameters. I saw that it updated /etc/modprobe.d/ttm.conf but didn't update grub or initramfs. I was able to manually set GTT using the command line parameters suggested. Thanks so much for this. Having to maintain a set of tools to update kernel parameters seems like a bad idea. More consistency and clearer documentation with driver options would be the better option. The kernel has more consistency across different distributions than python based user space tools

$ amd-ttm --version
0.2.11
$ cat /proc/cmdline 
BOOT_IMAGE=/boot/vmlinuz-6.14.0-1016-oem root=UUID=a605e3ba-f95e-4584-a20f-6f3a25fadef7 ro ttm.pages_limit=32768000 ttm.page_pool_size=32768000 amdttm.pages_limit=32768000 amdttm.page_pool_size=32768000
$ uname -a
Linux chris-evo 6.14.0-1016-oem #16-Ubuntu SMP PREEMPT_DYNAMIC Tue Oct 21 09:55:24 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
$ cat /etc/issue
Linux Mint 22.2 Zara \n \l
$ dmesg
[    3.680123] amdgpu: ATOM BIOS: 113-STRXLGEN-001
[    3.681747] amdgpu 0000:c6:00.0: amdgpu: VRAM: 1024M 0x0000008000000000 - 0x000000803FFFFFFF (1024M used)
[    3.681748] amdgpu 0000:c6:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    3.681834] [drm] amdgpu: 1024M of VRAM memory ready
[    3.681835] [drm] amdgpu: 128000M of GTT memory ready.
`
`



---

### 评论 #6 — harkgill-amd (2026-02-17T15:54:22Z)

https://github.com/ROCm/rocm-systems/pull/3103 will shift the functionality of amd-ttm to amd-smi allowing it to be consistently improved upon and managed by our smi team.

---

### 评论 #7 — harkgill-amd (2026-03-31T16:10:11Z)

A quick update here, https://github.com/ROCm/rocm-systems/pull/3636 has been merged successfully adding a VRAM and GTT tuning interface within `amd-smi`. With the latest TheRock nightlies, you can see the changes in effect with `amd-smi set -h`
```
amd-smi set -h
AMD System Management Interface | Version: 26.3.0+96e30b429c | ROCm version: 7.13.0 | Platform: Linux Baremetal
Set Arguments:
...
...
  -m, --mem-carveout INDEX                    Set VRAM carveout size by option index.
                                                Use `amd-smi static --mem-carveout` to see available options.
  -G, --gtt GB                                Set GTT (shared GPU memory) size in GB.
                                                This is a system-wide setting, not per-GPU.
```
This change comes alongside a few different QOL improvements that have also been discussed in this thread. We're also now dynamically checking whether the `ttm`/`amd-ttm` module needs to be configured based on what's available on the system at runtime, see https://github.com/ROCm/rocm-systems/blob/develop/projects/amdsmi/src/amd_smi/amd_smi.cc#L8241-L8254. I'm going to go ahead and close this issue out as we've resolved alot of the confusion around the `amd-ttm` tool and `amd-ttm`/`ttm` modules with the new user-friendly behaviour in `amd-smi`.

---
