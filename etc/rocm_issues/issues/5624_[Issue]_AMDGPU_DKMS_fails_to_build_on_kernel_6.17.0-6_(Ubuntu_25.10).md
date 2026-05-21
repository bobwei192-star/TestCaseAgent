# [Issue]: AMDGPU DKMS fails to build on kernel 6.17.0-6 (Ubuntu 25.10)

> **Issue #5624**
> **状态**: closed
> **创建时间**: 2025-11-04T20:13:23Z
> **更新时间**: 2026-03-02T16:57:22Z
> **关闭时间**: 2026-03-02T16:57:22Z
> **作者**: Battlesheepu
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5624

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

## Similar, past issue
https://github.com/ROCm/ROCm/issues/5111

## Problem description

Per the title - after upgrading to Ubuntu 25.10 from Ubuntu 25.04, the amdgpu-dkms no longer compiles via DKMS. The compilation worked perfectly for the 6.14 kernel. 

Is the lack of support expected? If so, is there any timeline as to when will the 6.17 kernel supported (if at all)?


### Operating System

NAME="Ubuntu" VERSION="25.10 (Questing Quokka)"

### CPU

AMD Ryzen 7 5800X 8-Core Processor

### GPU

AMD Radeon RX 9070 XT (radeonsi, gfx1201, ACO, DRM 3.64, 6.17.0-6-generic)

### ROCm Version

ROCm 6.4.4.60404-129~24.04

### ROCm Component

_No response_

### Steps to Reproduce

```bash
sudo amdgpu-install --usecase=graphics,opencl,hip,rocm
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

For more detail, the beginning of the make log:
```
DKMS (dkms-3.2.0) make.log for amdgpu/6.12.12-2202139.24.04 for kernel 6.17.0-6-generic (x86_64)
Tue Nov  4 11:45:31 CET 2025
```

I do have the full output, along a full suite of logs (per the recommendations in the `amdgpu-install` documentation), which I can provide if needed.

### Other info

Thanks for all the hard work you do :) 

---

## 评论 (13 条)

### 评论 #1 — ianbmacdonald (2025-11-04T21:16:14Z)

You will need to update your system to use ROCm 7.1 and Instinct 30.20 if you want to use Ubuntu 25.10.    Strictly speaking it isn't [officially supported](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems), but it is compatible. 

ROCm 6.4.4 (September) actually pre-dates the Ubuntu 25.10 release (October 2025), and did work with 25.04 (unofficially).   

Here is the path forwards:

Pin the radeon repo ahead of the distribution packages using 1001, to avoid any apt policy confusion resulting from Instinct drivers changing the version scheme from 1:6.4.4 to 30.20 (this avoids an apt policy snafu where apt thinks 6.4.4 is more current than 30.20). 

```
# /etc/apt/preferences.d/93-repo-radeon-pin 
Package: *
Pin: release o=repo.radeon.com
Pin-Priority: 1001
```
This pin for the radeon repo also works around a conflict with the rocprofiler package, which is newer in Questing than ROCm 7.1, and due to hard pinning of the version in dependencies, will prevent the upgrade.  

With the pin in place the new apt installation wrapper should do the rest. 

```
wget https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb
sudo apt install ./amdgpu-install_7.1.70100-1_all.deb
```

For a short time, you still need to pull in the [proposed kernel](https://launchpad.net/ubuntu/+source/linux) to get the MES firmware hooks from 6.17.2.  This pin below will additionally do that for you as well.

```
# /etc/apt/preferences.d/91-quest-proposed-kernel-pin 

### Block everything from questing-proposed by default
Package: *
Pin: release a=questing-proposed
Pin-Priority: 1

### Allow only the updated kernel packages from questing-proposed
Package: linux-image-* linux-headers-* linux-libc-dev linux-modules-* linux-perf linux-tools-* linux-source*
Pin: release a=questing-proposed
Pin-Priority: 600
```

With the above pin in place, you can add questing-proposed to your apt ubuntu.sources or check the `Pre-released updates (questing-proposed)` option in the Developer Options of the Software & Updates dialogue box and your kernel will move forwards.  I keep this [page uptodate](https://netstatz.com/strix_halo_lemonade/) until support is formal for those looking to use the lastest Ubuntu desktop on their Strix Halo. 

You can verify that you are current (or newer) by checking that you see the MES patched kernel, the latest Strix Halo Firmware, and the current amdgpu drivers all in place.

```
$ uname -a
Linux ai2 6.17.0-7-generic #7-Ubuntu SMP PREEMPT_DYNAMIC Sat Oct 18 10:10:29 UTC 2025 x86_64 GNU/Linux

$ modinfo amdgpu | head -n 3
filename:       /lib/modules/6.17.0-7-generic/updates/dkms/amdgpu.ko.zst
version:        6.16.6
license:        GPL and additional rights

$ sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
```


---

### 评论 #2 — ianbmacdonald (2025-11-05T23:05:27Z)

Adding to the 25.10 recipe;  There is a missing dependency for `rocm-hip-runtime-dev` noted here https://github.com/ROCm/ROCm/issues/5610 (I didn't notice since I have been evergreening since 25.04/6.4.4 so mine just upgraded) but it does stand alone:

```
$sudo apt-cache rdepends rocm-hip-runtime-dev
rocm-hip-runtime-dev
Reverse Depends:

```

As of today, I noticed there is also functional set of pytorch wheels for ROCm 7 that appears to have both memory efficient flash attention, and [avoid the MES crash/hang](https://github.com/ROCm/ROCm/issues/5590#issuecomment-3493419342), at least with Qwen-Image-Edit-2509.   

```
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
uv init --python 3.13
uv add --index rocm7_nightly=https://download.pytorch.org/whl/nightly/rocm7.0/ --index-strategy unsafe-best-match --prerelease allow "torch==2.10.0.dev20251102+rocm7.0" "torchvision==0.25.0.dev20251105+rocm7.0" "torchaudio==2.10.0.dev20251105+rocm7.0"
```

---

### 评论 #3 — tareko (2025-11-27T18:22:51Z)

The above method worked for me a couple of weeks ago, but now results in the error message "key was rejected by service". Is the current DKMS broken with 25.10?

---

### 评论 #4 — lucbruni-amd (2025-12-03T19:36:19Z)

> The above method worked for me a couple of weeks ago, but now results in the error message "key was rejected by service". Is the current DKMS broken with 25.10?

@tareko, could you provide me with your complete set of commands?

---

### 评论 #5 — lucbruni-amd (2026-01-14T20:09:58Z)

I tested this with ROCm `7.1.1`, Ubuntu `25.10` (Questing Quokka), and the `6.17.0-8-generic` kernel (slightly newer), and the issue appears to be resolved:

```
$ sudo dkms status
amdgpu/6.16.6-2255209.24.04, 6.17.0-5-generic, x86_64: installed (Original modules exist)
amdgpu/6.16.6-2255209.24.04, 6.17.0-8-generic, x86_64: installed (Original modules exist)

$ lsmod | grep amdgpu
amdgpu              20152320  0
amddrm_ttm_helper      12288  1 amdgpu
amdttm                135168  2 amdgpu,amddrm_ttm_helper
amddrm_buddy           28672  1 amdgpu
amdxcp                 12288  1 amdgpu
amddrm_exec            12288  1 amdgpu
amd_sched              61440  1 amdgpu
amdkcl                 32768  4 amd_sched,amdttm,amddrm_exec,amdgpu
drm_panel_backlight_quirks    12288  1 amdgpu
drm_suballoc_helper    24576  1 amdgpu
drm_display_helper    294912  1 amdgpu
cec                   106496  2 drm_display_helper,amdgpu
i2c_algo_bit           16384  1 amdgpu
video                  77824  1 amdgpu
drm_ttm_helper         16384  2 qxl,amdgpu

$ sudo dmesg | grep -i amdgpu
[ 1418.773212] [drm] amdgpu kernel modesetting enabled.
[ 1418.773215] [drm] amdgpu version: 6.16.6
[ 1418.773296] amdgpu: Virtual CRAT table created for CPU
[ 1418.773302] amdgpu: Topology: Add CPU node
```

Installation steps:
```
sudo usermod -a -G video,render $LOGNAME

sudo apt update
wget https://repo.radeon.com/amdgpu-install/7.1.1/ubuntu/noble/amdgpu-install_7.1.1.70101-1_all.deb
sudo apt install ./amdgpu-install_7.1.1.70101-1_all.deb
sudo apt update

sudo amdgpu-install --usecase=graphics,opencl,hip,rocm
```

Closing this issue due to inactivity, and as this seems resolved on latest versions. Please feel free to reopen this issue or open a new one if your use case requires this particular versioning. Thanks!


---

### 评论 #6 — borfast (2026-02-05T13:01:18Z)

I am on Linux Mint 22.3, based on Ubuntu 24.04, which just received an upgrade from Linux 6.14 to 6.17, and due to that, I am now having this problem as well, but with ROCm 7.2

Using version 7.1.1, as suggested by @lucbruni-amd, works. But the latest 7.2 version fails to compile the DKMS module.

---

### 评论 #7 — lucbruni-amd (2026-02-05T15:01:42Z)

Reopening this issue as it appears to have re-emerged in ROCm 7.2 per @borfast. Will look into this - thanks for the report.

---

### 评论 #8 — borfast (2026-02-05T15:17:49Z)

Thanks. Let me know if I can help in any way. 

---

### 评论 #9 — lucbruni-amd (2026-02-05T15:32:54Z)

If you have any environment setup/installation steps to provide, those would be a great help - but not required!

---

### 评论 #10 — borfast (2026-02-05T15:47:46Z)

There's nothing special, I think. It's a normal Linux Mint 22.3 / Ubuntu 24.04 installation, running the Linux kernel version 6.14 (and now, 6.17).

The only possibly relevant thing I can think of is that I had ROCm 6.2 installed previously, and when I updated the system, as I normally do every day, the system got the new 6.17 kernel. That's when the DKMS module errors popped up, when trying to compile for 6.17. I figured it could be due to some incompatibility with the newer kernel, so I tried upgrading to ROCm 7.2, but also got the DKMS errors. That's when I searched online and found this GitHub issue.

---

### 评论 #11 — lucbruni-amd (2026-02-11T19:58:47Z)

> There's nothing special, I think. It's a normal Linux Mint 22.3 / Ubuntu 24.04 installation, running the Linux kernel version 6.14 (and now, 6.17).
> 
> The only possibly relevant thing I can think of is that I had ROCm 6.2 installed previously, and when I updated the system, as I normally do every day, the system got the new 6.17 kernel. That's when the DKMS module errors popped up, when trying to compile for 6.17. I figured it could be due to some incompatibility with the newer kernel, so I tried upgrading to ROCm 7.2, but also got the DKMS errors. That's when I searched online and found this GitHub issue.

I cannot reproduce this with 7.2 and `6.17.0-5-generic`, `6.17.0-8-generic` or `6.17.0-14-generic`. Could you please provide me with your exact kernel, ROCm installation steps and the resulting log(s)?

---

### 评论 #12 — borfast (2026-02-12T00:21:20Z)

@lucbruni-amd, it seems the problem may have been only on my side. I tried running the same installation commands as before (I followed the instructions at https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html) and this time it seems to have worked.

Sorry for the waste of time, and thank you for looking into it anyway.

---

### 评论 #13 — lucbruni-amd (2026-02-12T14:46:54Z)

That's great to hear @borfast - and not a waste of time at all. We really appreciate your help in finding and reporting issues with ROCm. I'll leave this issue open for a little while in case it is encountered by others.

---
