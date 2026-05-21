# [Issue]: amdgpu: trn=2 ACK should not assert! wait again ! with GPU Radeon Instinct MI50

> **Issue #6176**
> **状态**: open
> **创建时间**: 2026-04-22T20:22:23Z
> **更新时间**: 2026-05-06T16:15:50Z
> **作者**: camzilla1050
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6176

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Can't use GPU Radeon Instinct M150 32GB connected with pcie / Thunderbolt 3 on mini-desktop:

I followed official rocm documentation multiple times to install rocm with various versions. I try now with 6.2.4 version but no way, same issues,:

```
sudo dmesg
[ 3965.483045] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3965.487042] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3970.453973] xgpu_ai_mailbox_trans_msg: 1654 callbacks suppressed
[ 3970.453991] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
```

```
lshw
 *-display
        description: Display controller
        product: Vega 20 [Radeon Pro VII/Radeon Instinct MI50]
        vendor: Advanced Micro Devices, Inc. [AMD/ATI]
        physical id: 0
        bus info: pci@0000:08:00.0
        version: 01
        width: 64 bits
        clock: 33MHz
        capabilities: pm pciexpress msi bus_master cap_list rom
        configuration: driver=amdgpu latency=0
        resources: irq:17 memory:a0000000-a01fffff memory:c4100000-c417ffff memory:c4180000-c419ffff
```

### Operating System

Ubuntu 24.04.4 LTS

### CPU

Intel(R) Core(TM) i5-7260U CPU @ 2.20GHz   4 cores

### GPU

[AMD/ATI] Vega 20 [Radeon Pro VII/Radeon Instinct MI50]

### ROCm Version

version 6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

```
$ sudo dmesg
[ 3311.086975] xgpu_ai_mailbox_trans_msg: 1657 callbacks suppressed
[ 3311.086994] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.089949] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.093046] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.096033] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.099070] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.102057] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.105073] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.107890] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.110881] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !
[ 3311.113965] amdgpu 0000:08:00.0: amdgpu: trn=2 ACK should not assert! wait again !


```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
$  /opt/rocm/bin/rocminfo --support
mkdir: cannot create directory ‘/run/user/0’: Permission denied
ROCk module is loaded
Unable to open /dev/kfd read-write: Invalid argument
ubuntu is member of video group


### Additional Information

```
$ /opt/rocm/bin/amd-smi

/opt/rocm-6.2.4/libexec/amdsmi_cli/BDF.py:126: SyntaxWarning: invalid escape sequence '\.'
  bdf_regex = "(?:[0-6]?[0-9a-fA-F]{1,4}:)?[0-2]?[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}\.[0-7]"
ERROR: Unable to detect any GPU devices, check amdgpu version and module status
```
```
$ rocm-smi

 ROCm System Management Interface
WARNING: No AMD GPUs specified
Concise Info 
GPU  Temp (DieEdge)  AvgPwr  SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%  

------------- End of ROCm SMI Log -------------

```

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2026-04-24T20:11:56Z)

Hey @camzilla1050, your `lshw` output points to a rather small BAR allocation for your MI50, this is likely due to your Thunderbolt PCIe setup. Can you try configuring the following BIOS knobs so we can get a better starting point to investigate from,

1. Enable Above 4G Decoding
2. Disable CSM
3. Enable Resizable BAR

eGPU setups can be a bit tricky but we do have some precedent with ROCm working on them. If this doesn't seem to help, I'll try to get a repro setup on my end.

---

### 评论 #2 — harkgill-amd (2026-05-06T14:14:15Z)

@camzilla1050, did you get a chance to try out the BIOS settings?

---

### 评论 #3 — camzilla1050 (2026-05-06T16:15:50Z)

Hi @harkgill-amd . Sorry for this tardive response. I entered in BIOS and see max. 1024 M decoding. I didn't found CMS and BAR options. i'm waiting to test with another machine 

---
