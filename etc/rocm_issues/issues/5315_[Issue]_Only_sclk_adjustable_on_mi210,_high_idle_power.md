# [Issue]: Only sclk adjustable on mi210, high idle power

> **Issue #5315**
> **状态**: open
> **创建时间**: 2025-09-16T00:39:14Z
> **更新时间**: 2025-10-31T17:46:13Z
> **作者**: 65a
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5315

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

mi210 cards have `mclk` locked at max even with low power. Kernel is `6.16.6`

```
[user@machine ~]$ rocm-smi -s


============================ ROCm System Management Interface ============================
============================== Supported clock frequencies ===============================
GPU[0]		: 
GPU[0]		: Supported fclk frequencies on GPU0
GPU[0]		: 0: 400Mhz *
GPU[0]		: 
GPU[0]		: Supported mclk frequencies on GPU0
GPU[0]		: 0: 400Mhz
GPU[0]		: 1: 700Mhz
GPU[0]		: 2: 1200Mhz
GPU[0]		: 3: 1600Mhz *
GPU[0]		: 
GPU[0]		: Supported sclk frequencies on GPU0
GPU[0]		: 0: 500Mhz *
GPU[0]		: 1: 500Mhz
GPU[0]		: 
GPU[0]		: Supported socclk frequencies on GPU0
GPU[0]		: 0: 666Mhz
GPU[0]		: 1: 857Mhz
GPU[0]		: 2: 1000Mhz
GPU[0]		: 3: 1090Mhz *
GPU[0]		: 4: 1333Mhz
GPU[0]		: 
GPU[0]		: 
------------------------------------------------------------------------------------------
GPU[1]		: 
GPU[1]		: Supported fclk frequencies on GPU1
GPU[1]		: 0: 400Mhz *
GPU[1]		: 
GPU[1]		: Supported mclk frequencies on GPU1
GPU[1]		: 0: 400Mhz
GPU[1]		: 1: 700Mhz
GPU[1]		: 2: 1200Mhz
GPU[1]		: 3: 1600Mhz *
GPU[1]		: 
GPU[1]		: Supported sclk frequencies on GPU1
GPU[1]		: 0: 500Mhz *
GPU[1]		: 1: 500Mhz
GPU[1]		: 
GPU[1]		: Supported socclk frequencies on GPU1
GPU[1]		: 0: 666Mhz
GPU[1]		: 1: 857Mhz
GPU[1]		: 2: 1000Mhz
GPU[1]		: 3: 1090Mhz *
GPU[1]		: 4: 1333Mhz
GPU[1]		: 
GPU[1]		: 
------------------------------------------------------------------------------------------
==========================================================================================
================================== End of ROCm SMI Log ===================================
```
Trying to set `mclk` to 0 and save power:
```
[user@machine ~]$ sudo rocm-smi --setclock mclk 0


============================ ROCm System Management Interface ============================
=================================== Set mclk Frequency ===================================
GPU[0]		: Performance level was set to manual
GPU[0]		: set_gpu_clk_freq_mclk, Permission denied
ERROR: GPU[0]	: Unable to set mclk bitmask to: 0x1
GPU[1]		: Performance level was set to manual
GPU[1]		: set_gpu_clk_freq_mclk, Permission denied
ERROR: GPU[1]	: Unable to set mclk bitmask to: 0x1
==========================================================================================
================================== End of ROCm SMI Log ===================================
```
Setting or unsetting overdrive bit doesn't seem to change this. Auto and low performance modes are also like this.

Idle power is 38-42W per card, I believe this is primarily because of the memory speed. It does not seem usual methods let me adjust the mclk or other card parameters than sclk. Please advise, as this uses much more power than expected because the card is not idling on linux.

Please advise if this should be filed elsewhere.

### Operating System

Linux

### CPU

Xeon 4th Generation

### GPU

2x Instinct Mi210

### ROCm Version

6.4.3

### ROCm Component

_No response_

### Steps to Reproduce

Install 2x Mi210, set power profile to low. Inspect power consumption with lm-sensors or other tool, inspect clock frequencies. Note that mclk is locked at highest value and does not reduce.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Enabling aspm in driver and kernel does not help. Enabling overdrive does not help (e.g. ppfeaturemask).

---

## 评论 (12 条)

### 评论 #1 — 65a (2025-09-16T01:10:53Z)

Sort of similar to [#2844](https://github.com/ROCm/ROCm/issues/2844) except in this case, lower mclk states are listed, but neither used nor reached even when ROCm SMI is used to configure the lowest possible clocks.

---

### 评论 #2 — 65a (2025-09-16T01:12:44Z)

I believe I am using the latest VBIOS:
```
[user@machine ~]$ rocm-smi --showhw


===================================== ROCm System Management Interface =====================================
========================================== Concise Hardware Info ===========================================
GPU  NODE  DID     GUID   GFX VER  GFX RAS  SDMA RAS  UMC RAS  VBIOS            BUS           PARTITION ID  
0    1     0x740f  544XX  gfx90a   N/A      N/A       N/A      113-D67301V-074  0000:18:00.0  0             
1    2     0x740f  202XX  gfx90a   N/A      N/A       N/A      113-D67301V-074  0000:42:00.0  0             
============================================================================================================
=========================================== End of ROCm SMI Log ============================================
```

---

### 评论 #3 — IMbackK (2025-09-16T13:06:31Z)

Unfortunately i investigated in the kernel for arcturus (mi100)  and it looks like this is simply not implemented at all at the kernel level, with some evidence that this is due to hardware errata, but im not sure about the last bit.

Theoretically on a compute gpu, you would not have downside to using runtime-pm to fully turn off the gpu when its not used. unfortunately this is also broken see https://github.com/ROCm/amdgpu/issues/183

Anyhow the idle behavior of mi series gpus after mi60 is absolutely horrendous with nodes often idling above 500W



---

### 评论 #4 — 65a (2025-09-16T14:46:24Z)

@IMbackK this is for the Mi210, not the Mi100. Hoping the story is different here, being a newer card (Aldebaran vs Arcturus). 

---

### 评论 #5 — IMbackK (2025-09-16T15:14:40Z)

I know, however i dont believe its any different. you can try runtime-pm and report back if it works. switching the uclk clock domain is defiantly not supported on the kernel side.
I can also report that this problem still exists in mi3xx


---

### 评论 #6 — 65a (2025-09-17T00:25:03Z)

@IMbackK by `runtime-pm` do you mean `amdgpu.runpm=N` or something else? I noticed that some of the kernel runpm code will default to r/o for sysfs entries unless runpm is either disabled, or automatically found. I don't believe the auto setting would work correctly on this card, so I may test amdgpu.runpm=0 to see if that opens up any of the sysfs settings. Do you know if the powerplay table version for this card exists in any open form? Sometimes that might help other parameters...

---

### 评论 #7 — 65a (2025-09-17T01:27:17Z)

This seems relevant: https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/amd/pm/swsmu/smu13/aldebaran_ppt.h
https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/amd/pm/swsmu/smu13/aldebaran_ppt.c

runpm=0 doesn't help, I'll look at pptable stuff next, unless AMD has some better guidance.

---

### 评论 #8 — IMbackK (2025-09-17T07:31:19Z)

You need to set amdgpu.runpm=1 and set power/control to auto in device sysfs. Note that you won't see the device suspended in SMI as reading any of the values that SMI dose actually resumes the device. When runtime suspended the GPU is fully off (like in system wide s3 suspend). You can check that this is happening by looking at the suspend count in sysfs. This is a different (and a much lower power state) than idle with uclk lowered.

---

### 评论 #9 — LunNova (2025-09-17T21:02:10Z)

runpm=1 results in a hang trying to resume the SMU on MI100 and MI210 for me so not really expecting much success there. Awkward that idle power is so bad on the instinct series.

---

### 评论 #10 — 65a (2025-09-18T01:20:34Z)

`amdgpu.aspm=1 amdgpu.runpm=1` boots fine for me (6.16.6), but the dmesg says `amdgpu: Runtime PM not available` which doesn't sound promising. I also tried /sys/bus/pci/slots/N/power, which doesn't register any change on the kill-a-watt meter I have installed. I am still trying to understand what is user controllable in the pptable code above, since the SMU is in charge.

---

### 评论 #11 — harkgill-amd (2025-10-24T15:54:14Z)

Hi @65a, unfortunately, both runtime PM and `mclk` configuration w/rocm-smi are not supported at the driver level for MI200, see https://github.com/ROCm/rocm_smi_lib/issues/117 for a similar issue.
 
> Idle power is 38-42W per card, I believe this is primarily because of the memory speed. It does not seem usual methods let me adjust the mclk or other card parameters than sclk. Please advise, as this uses much more power than expected because the card is not idling on linux.

I spoke with the folks on the driver team and ~40W is an appropriate power usage when idling for MI2XX. You can always check the gfx activity and memory utilization with either amd-smi or rocm-smi to confirm if the card is actually idling - both would be close to 0 in this case.

---

### 评论 #12 — IMbackK (2025-10-25T14:42:47Z)

> Hi [@65a](https://github.com/65a), unfortunately, both runtime PM and `mclk` configuration w/rocm-smi are not supported at the driver level for MI200, see [ROCm/rocm_smi_lib#117](https://github.com/ROCm/rocm_smi_lib/issues/117) for a similar issue.
> 
> > Idle power is 38-42W per card, I believe this is primarily because of the memory speed. It does not seem usual methods let me adjust the mclk or other card parameters than sclk. Please advise, as this uses much more power than expected because the card is not idling on linux.
> 
> I spoke with the folks on the driver team and ~40W is an appropriate power usage when idling for MI2XX. You can always check the gfx activity and memory utilization with either amd-smi or rocm-smi to confirm if the card is actually idling - both would be close to 0 in this case.

Right its not supported on the kernel level. It would however be good to support it or alternatively since it would be even better on a compute only card, fix runtime pm to not crash on resume.

Runpm would bring the effective idle power consumption to almost zero.
The hardware can do it, let's not waste a bunch of electricity on this software deficiency.

Mi100, mi2xx and mi3xx are in the same boat on this.

---
