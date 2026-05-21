# [Issue]: DKMS 6.18 kernel support

> **Issue #6121**
> **状态**: open
> **创建时间**: 2026-04-06T04:11:06Z
> **更新时间**: 2026-04-10T22:21:41Z
> **作者**: Qubitium
> **标签**: AMD Radeon RX 7900 XTX, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6121

## 标签

- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

Please add support the latest `stable` Linux `6.18` kernel.

```py
In file included from ./amd/amdgpu/../backport/backport.h:30,
                 from <command-line>:
././include/kcl/kcl_preempt.h:57:29: error: static declaration of ‘migrate_disable’ follows non-static declaration
   57 | static __always_inline void migrate_disable(void)
      |                             ^~~~~~~~~~~~~~~
In file included from /home/diego/linux-6.18.15/include/linux/percpu.h:12,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/msr.h:16,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/tsc.h:11,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/timex.h:6,
                 from /home/diego/linux-6.18.15/include/linux/timex.h:67,
                 from /home/diego/linux-6.18.15/include/linux/time32.h:13,
                 from /home/diego/linux-6.18.15/include/linux/time.h:60,
                 from /home/diego/linux-6.18.15/include/linux/stat.h:19,
                 from /home/diego/linux-6.18.15/include/linux/module.h:13,
                 from ././include/kcl/kcl_moduleparam.h:5,
                 from ./amd/amdgpu/../backport/backport.h:7:
/home/diego/linux-6.18.15/include/linux/sched.h:2430:13: note: previous declaration of ‘migrate_disable’ with type ‘void(void)’
 2430 | extern void migrate_disable(void);
      |             ^~~~~~~~~~~~~~~
././include/kcl/kcl_preempt.h:61:29: error: static declaration of ‘migrate_enable’ follows non-static declaration
   61 | static __always_inline void migrate_enable(void)
      |                             ^~~~~~~~~~~~~~
/home/diego/linux-6.18.15/include/linux/sched.h:2431:13: note: previous declaration of ‘migrate_enable’ with type ‘void(void)’
 2431 | extern void migrate_enable(void);
      |             ^~~~~~~~~~~~~~
  CC [M]  amd/amdgpu/aldebaran.o
  CC [M]  amd/amdgpu/soc21.o
  CC [M]  amd/amdgpu/soc24.o
In file included from ./amd/amdgpu/../backport/backport.h:30,
                 from <command-line>:
././include/kcl/kcl_preempt.h:57:29: error: static declaration of ‘migrate_disable’ follows non-static declaration
   57 | static __always_inline void migrate_disable(void)
      |                             ^~~~~~~~~~~~~~~
In file included from /home/diego/linux-6.18.15/include/linux/percpu.h:12,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/msr.h:16,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/tsc.h:11,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/timex.h:6,
                 from /home/diego/linux-6.18.15/include/linux/timex.h:67,
                 from /home/diego/linux-6.18.15/include/linux/time32.h:13,
                 from /home/diego/linux-6.18.15/include/linux/time.h:60,
                 from /home/diego/linux-6.18.15/include/linux/stat.h:19,
                 from /home/diego/linux-6.18.15/include/linux/module.h:13,
                 from ././include/kcl/kcl_moduleparam.h:5,
                 from ./amd/amdgpu/../backport/backport.h:7:
/home/diego/linux-6.18.15/include/linux/sched.h:2430:13: note: previous declaration of ‘migrate_disable’ with type ‘void(void)’
 2430 | extern void migrate_disable(void);
      |             ^~~~~~~~~~~~~~~
././include/kcl/kcl_preempt.h:61:29: error: static declaration of ‘migrate_enable’ follows non-static declaration
   61 | static __always_inline void migrate_enable(void)
      |                             ^~~~~~~~~~~~~~
/home/diego/linux-6.18.15/include/linux/sched.h:2431:13: note: previous declaration of ‘migrate_enable’ with type ‘void(void)’
 2431 | extern void migrate_enable(void);
      |             ^~~~~~~~~~~~~~
  CC [M]  amd/amdgpu/sienna_cichlid.o
In file included from ./amd/amdgpu/../backport/backport.h:30,
                 from <command-line>:
././include/kcl/kcl_preempt.h:57:29: error: static declaration of ‘migrate_disable’ follows non-static declaration
   57 | static __always_inline void migrate_disable(void)
      |                             ^~~~~~~~~~~~~~~
In file included from /home/diego/linux-6.18.15/include/linux/percpu.h:12,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/msr.h:16,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/tsc.h:11,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/timex.h:6,
                 from /home/diego/linux-6.18.15/include/linux/timex.h:67,
                 from /home/diego/linux-6.18.15/include/linux/time32.h:13,
                 from /home/diego/linux-6.18.15/include/linux/time.h:60,
                 from /home/diego/linux-6.18.15/include/linux/stat.h:19,
                 from /home/diego/linux-6.18.15/include/linux/module.h:13,
                 from ././include/kcl/kcl_moduleparam.h:5,
                 from ./amd/amdgpu/../backport/backport.h:7:
/home/diego/linux-6.18.15/include/linux/sched.h:2430:13: note: previous declaration of ‘migrate_disable’ with type ‘void(void)’
 2430 | extern void migrate_disable(void);
      |             ^~~~~~~~~~~~~~~
././include/kcl/kcl_preempt.h:61:29: error: static declaration of ‘migrate_enable’ follows non-static declaration
   61 | static __always_inline void migrate_enable(void)
      |                             ^~~~~~~~~~~~~~
/home/diego/linux-6.18.15/include/linux/sched.h:2431:13: note: previous declaration of ‘migrate_enable’ with type ‘void(void)’
 2431 | extern void migrate_enable(void);
      |             ^~~~~~~~~~~~~~
amd/amdkcl/kcl_suspend.c:32:6: warning: no previous prototype for ‘amdkcl_suspend_init’ [-Wmissing-prototypes]
   32 | void amdkcl_suspend_init(void)
      |      ^~~~~~~~~~~~~~~~~~~
  CC [M]  amd/amdgpu/smu_v13_0_10.o
In file included from ./amd/amdgpu/../backport/backport.h:30,
                 from <command-line>:
././include/kcl/kcl_preempt.h:57:29: error: static declaration of ‘migrate_disable’ follows non-static declaration
   57 | static __always_inline void migrate_disable(void)
      |                             ^~~~~~~~~~~~~~~
In file included from /home/diego/linux-6.18.15/include/linux/percpu.h:12,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/msr.h:16,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/tsc.h:11,
                 from /home/diego/linux-6.18.15/arch/x86/include/asm/timex.h:6,
                 from /home/diego/linux-6.18.15/include/linux/timex.h:67,
                 from /home/diego/linux-6.18.15/include/linux/time32.h:13,
                 from /home/diego/linux-6.18.15/include/linux/time.h:60,
                 from /home/diego/linux-6.18.15/include/linux/stat.h:19,
                 from /home/diego/linux-6.18.15/include/linux/module.h:13,
                 from ././include/kcl/kcl_moduleparam.h:5,
                 from ./amd/amdgpu/../backport/backport.h:7:
/home/diego/linux-6.18.15/include/linux/sched.h:2430:13: note: previous declaration of ‘migrate_disable’ with type ‘void(void)’
 2430 | extern void migrate_disable(void);
      |             ^~~~~~~~~~~~~~~
././include/kcl/kcl_preempt.h:61:29: error: static declaration of ‘migrate_enable’ follows non-static declaration
   61 | static __always_inline void migrate_enable(void)
      |                             ^~~~~~~~~~~~~~
/home/diego/linux-6.18.15/include/linux/sched.h:2431:13: note: previous declaration of ‘migrate_enable’ with type ‘void(void)’
```



### Operating System

Ubuntu 24.0

### CPU

AMD ZEN3

### GPU

7900 XTX

### ROCm Version

Latest Stable

### ROCm Component

_No response_

### Steps to Reproduce

Install amdgpu-dkms under LInux 6.18.*


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — schung-amd (2026-04-08T18:15:55Z)

amdgpu-dkms should be supported on kernel 6.18+ soon as part of mainline ROCm enablement for Ubuntu 26.04. In the meanwhile you should be able to use ROCm without installing the DKMS driver. Are there any issues with doing so?

---

### 评论 #2 — Qubitium (2026-04-09T01:16:41Z)

> amdgpu-dkms should be supported on kernel 6.18+ soon as part of mainline ROCm enablement for Ubuntu 26.04. In the meanwhile you should be able to use ROCm without installing the DKMS driver. Are there any issues with doing so?

@schung-amd Do you have a link or short guide to this dkms-less driver install? I just followed the normal `ubuntu/debian1` doc and it was installed by default through all the inter-apt depends. 

Update: Your're right, the dkms driver is not required:

```bash
> sudo rocm-smi --showproductname

============================ ROCm System Management Interface ============================
====================================== Product Info ======================================
GPU[0]		: Card Series: 		Radeon RX 7900 XTX
GPU[0]		: Card Model: 		0x744c
GPU[0]		: Card Vendor: 		Advanced Micro Devices, Inc. [AMD/ATI]
GPU[0]		: Card SKU: 		D7020100
GPU[0]		: Subsystem ID: 	0x0e3b
GPU[0]		: Device Rev: 		0xc8
GPU[0]		: Node ID: 		2
GPU[0]		: GUID: 		21373
GPU[0]		: GFX Version: 		gfx1100
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

Now I am little confused. If the `amdgpu-dkms` is not required and there is no per-kernel driver built, how is the rocm loading the gpu? Does the dkms driver provide something extra? I am not exactly sure how it can see the gpu without the amdgpu-firmware and amdgpu-driver installed. 

I always assumed, from nvidia gpu user pov, that these are required:

```
amdgpu-dkms
amdgpu-dkms-firmware
```

Is the currenlty loaded amdgpu driver on my 6.18.15 provided by the Linux kernel itself?

dmesg
```
[249056.640655] amdgpu 0000:2e:00.0: amdgpu: PSP is resuming...
[249056.701289] amdgpu 0000:2e:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[249056.850705] amdgpu 0000:2e:00.0: amdgpu: RAP: optional rap ta ucode is not available
[249056.850713] amdgpu 0000:2e:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[249056.850718] amdgpu 0000:2e:00.0: amdgpu: SMU is resuming...
[249056.850723] amdgpu 0000:2e:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8200 (78.130.0)
[249056.850730] amdgpu 0000:2e:00.0: amdgpu: SMU driver if version not matched
[249057.005665] amdgpu 0000:2e:00.0: amdgpu: SMU is resumed successfully!
[249057.014832] amdgpu 0000:2e:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002F00
[249057.021621] amdgpu 0000:2e:00.0: [drm] Cannot find any crtc or sizes
[249057.021633] amdgpu 0000:2e:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[249057.021636] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[249057.021638] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[249057.021639] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[249057.021640] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[249057.021641] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[249057.021642] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[249057.021643] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[249057.021644] amdgpu 0000:2e:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[249057.021645] amdgpu 0000:2e:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[249057.021646] amdgpu 0000:2e:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[249057.021647] amdgpu 0000:2e:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[249057.021648] amdgpu 0000:2e:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[249057.021649] amdgpu 0000:2e:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[249057.021650] amdgpu 0000:2e:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[249057.024839] amdgpu 0000:2e:00.0: [drm] Cannot find any crtc or sizes
```

---

### 评论 #3 — Only8Bits (2026-04-09T07:43:42Z)

I'd like to hear what dkms driver does better from official AMD source too but AFAIK it's just a somewhat newer version with changes/patches that have not hit the kernel driver (due to long chain of acceptance?). It's also built against different kernel patch level, and that actually made it quite unstable on my system. So from my perspective, as things stand right now, the non-dkms driver is much more preferable (for RDNA3 on Kubuntu at least) because:
- way more stable, random crashes due to compute running along graphics tasks are very rare
- doesn't crash system hard (or way less) when compute job hits the VRAM limit and starves graphics subsystem of it
- introduces less lag/latency when running heavy compute and trying to use the desktop GUI at the same time (depends on the compute job, it's still there but feels more responsive)
- performance seems to be identical for both, at least I have not seen anything going slower/faster to worth mentioning

TL;DR: For Radeon cards if you are also using your PC with GUI it's better to stick to non-dkms driver for now, otherwise compute jobs will either annoy you or crash, or both. Gaming seems to work OK (and stable) on either driver.

---

### 评论 #4 — schung-amd (2026-04-09T14:40:16Z)

> Do you have a link or short guide to this dkms-less driver install?

After installing `amdgpu-install`, run `amdgpu-install -y --usecase=rocm,graphics --no-dkms` instead of `sudo apt install rocm`. You can refer to the Strix Halo install instructions as the DKMS driver is not currently supported there:  https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html.

> Is the currenlty loaded amdgpu driver on my 6.18.15 provided by the Linux kernel itself?

> AFAIK it's just a somewhat newer version with changes/patches that have not hit the kernel driver

Yep, the Linux kernel contains `amdgpu` and from what I understand the DKMS driver exists so we can have control over per-ROCm version driver releases and work in required patches and fixes. This driver is tested extensively for the Ubuntu LTS kernel, which is what we support with the mainline ROCm releases.

It's tricky to say whether DKMS should be used for "exotic" configurations (i.e. anything outside of our compatibility matrix). The patches in the DKMS driver are upstreamed eventually, so they should be present in the in-kernel driver in newer kernel versions, but it's hard to say when "eventually" is precisely without inspecting the kernel commit history. 

On the other hand we have seen incompatibility issues with newer kernels; not just compilation of the DKMS driver, but also as @Only8Bits mentions there have been some issues with graphical environments and stability that present with the DKMS driver and "future" (from the POV of the currently supported Ubuntu LTS version) kernel versions, and which are already fixed in those "future" in-kernel driver versions. 

Generally I recommend using the DKMS driver if your kernel version aligns with the kernel version stated in our compatibility matrix, but if there is significant misalignment you can try using the in-kernel driver instead. In this case you are blocked from even trying DKMS, but even when it does build there may be stability and performance improvements in the "future" in-kernel driver.

I'd like to close this since this should be on track for eventual delivery and there isn't any additional work to do here, but I don't mind leaving it open until the DKMS support is added; that might be a month or two away though. Let me know if you run into any issues with the in-kernel driver.

---

### 评论 #5 — Qubitium (2026-04-09T15:32:53Z)

@ppanchad-amd As @Only8Bits mentioned, it would be good to get some visibilty to change log for the `dkms` kernel. The upstreamed linux kernel at least has patchsets with review and git history. Is there something siimilar, accesible online changelog, for the `dkms` kernel as they are updated? 

---

### 评论 #6 — schung-amd (2026-04-10T21:44:35Z)

There are release tags in the `amdgpu` repo (e.g. https://github.com/ROCm/amdgpu/tree/rocm-7.2.1) which should correspond to the DKMS releases.

---

### 评论 #7 — Qubitium (2026-04-10T22:20:49Z)

@schung-amd  Thanks. That helps, a lot but can be much better. The amdgpu repo hsa `tags`, no actual release cuts for the `rcom`/driver releases. Which forces users to do manual diff between tagged branches to check for changelog between `tags`.  Please alert repo-maintainer to cut releases based on the rcom `tags` and auto generate change log.

<img width="2788" height="1802" alt="Image" src="https://github.com/user-attachments/assets/949585d6-3a4b-489d-911b-2adc082797b0" />

https://github.com/ROCm/amdgpu/releases

---
