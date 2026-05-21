# RDNA4 / 1002:7551 amdgpu MES firmware version clarification

> **Issue #6155**
> **状态**: closed
> **创建时间**: 2026-04-16T00:40:55Z
> **更新时间**: 2026-05-12T07:17:28Z
> **关闭时间**: 2026-05-12T07:17:28Z
> **作者**: tamascode
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6155

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

I am seeing a persistent firmware/interface mismatch on two RDNA4 GPUs with PCI ID 1002:7551.

The issue reproduces on:
- 6.8.0-110-generic
- 6.17.0-20-generic

It also reproduces with both:
- AMD DKMS amdgpu 6.16.13
- the stock in-kernel amdgpu driver

With the stock driver loaded from:
/lib/modules/6.17.0-20-generic/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.zst

dmesg reports for both GPUs:
- SMU driver if version not matched
- smu driver if version = 0x0000002e
- smu fw if version = 0x00000032
- smu fw version = 0x00684a00 (104.74.0)

GPU 03:00.0 also reports:
- MES FW version must be >= 0x82 to enable LR compute workaround

The cards still initialize successfully, but the mismatch persists across kernels and driver paths, which suggests this is not just a DKMS packaging issue and is more likely related to firmware / upstream support for these GPUs.

---

## 评论 (12 条)

### 评论 #1 — amd-nicknick (2026-04-20T11:24:43Z)

Hi @tamascode, could you please provide the output of the following command?
```
sudo cat /sys/kernel/debug/dri/<Your GPU BDF>/amdgpu_firmware_info
```
Let's check the currently loaded firmware. 

Also, what distro are you using? If you're using Ubuntu, check for the firmware package installed:
```
sudo apt list --installed | grep amdgpu
sudo apt list --installed | grep firmware
```

---

### 评论 #2 — tamascode (2026-04-21T11:36:10Z)

@amd-nicknick,
Here is the info you requested. 

VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b18
PFP feature version: 29, firmware version: 0x00000b54
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000c44
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3804948, firmware version: 0x003a0f14
ASD feature version: 553648371, firmware version: 0x210000f3
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x17000046
TA DTM feature version: 0x00000000, firmware version: 0x12000019
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684a00 (104.74.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x09104001
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x00000000
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x00000081
MES feature version: 1, firmware version: 0x00000081
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-APM107573-101
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b18
PFP feature version: 29, firmware version: 0x00000b54
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000c44
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3804948, firmware version: 0x003a0f14
ASD feature version: 553648371, firmware version: 0x210000f3
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x17000046
TA DTM feature version: 0x00000000, firmware version: 0x12000019
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684a00 (104.74.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x09104001
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x00000000
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x00000081
MES feature version: 1, firmware version: 0x00000081
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-APM107573-101
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 38, firmware version: 0x0000000e
PFP feature version: 38, firmware version: 0x0000000e
CE feature version: 38, firmware version: 0x00000003
RLC feature version: 1, firmware version: 0x0000001f
RLC SRLC feature version: 1, firmware version: 0x00000001
RLC SRLG feature version: 1, firmware version: 0x00000001
RLC SRLS feature version: 1, firmware version: 0x00000001
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 38, firmware version: 0x00000014
MEC2 feature version: 38, firmware version: 0x00000014
IMU feature version: 0, firmware version: 0x00000000
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648327, firmware version: 0x210000c7
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x1700003c
TA DTM feature version: 0x00000000, firmware version: 0x12000016
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00624e00 (98.78.0)
SDMA0 feature version: 52, firmware version: 0x00000009
VCN feature version: 0, firmware version: 0x0311e004
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x00000000
TOC feature version: 0, firmware version: 0x00000007
MES_KIQ feature version: 0, firmware version: 0x00000000
MES feature version: 0, firmware version: 0x00000000
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 102-RAPHAEL-008

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

amdgpu-core/noble,noble,now 1:7.2.70200-2278374.24.04 all [installed,automatic]
libdrm-amdgpu-amdgpu1/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]
libdrm-amdgpu-common/noble,noble,now 1.0.0.70200-2278374.24.04 all [installed,automatic]
libdrm-amdgpu-dev/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]
libdrm-amdgpu-radeon1/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]
libdrm-amdgpu1/noble-updates,now 2.4.125-1ubuntu0.1~24.04.1 amd64 [installed,automatic]
libdrm2-amdgpu/noble,now 1:2.4.125.70200-2278374.24.04 amd64 [installed,automatic]

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

firmware-sof-signed/noble-updates,now 2023.12.1-1ubuntu1.10 all [installed,automatic]
linux-firmware/noble-updates,noble-security,now 20240318.git3b128b60-0ubuntu2.26 amd64 [installed]
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.4 LTS
Release:        24.04
Codename:       noble
6.17.0-20-generic


---

### 评论 #3 — amd-nicknick (2026-04-21T11:50:59Z)

@tamascode, yep that doesn't seem correct. Could you please try reinstalling all packages & deps for the dkms?
Purge the packages first:
```
sudo apt autoremove --purge amdgpu-dkms
sudo apt autoremove --purge amdgpu-core
```
Make sure amdgpu-dkms pkg source is present, check by 
```
apt-cache policy | grep amdgpu
# Command should output:
# 600 https://repo.radeon.com/amdgpu/30.30 (or 30.30.x) /ubuntu noble/main amd64 Packages
# If not, follow the steps in https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/install/detailed-install/package-manager/package-manager-ubuntu.html
```
Install amdgpu-dkms
```
sudo apt install amdgpu-dkms
```


---

### 评论 #4 — tamascode (2026-04-28T13:50:37Z)

@amd-nicknick 
I tested the reinstall mentioned above. It did not change the MES firmware.

Current system after reinstall:

Ubuntu 24.04.4
Kernel: 6.17.0-22-generic
amdgpu-dkms: 1:6.19.0.31200000-2307534.24.04
amdgpu-dkms-firmware: 31.20.0.0.31200000-2307534.24.04
GPU: AMD Radeon AI PRO R9700 / PCI ID 1002:7551

The MES firmware files are still the same March 6 blobs:

-rw-r--r-- 1 root root 34K Mar  6 10:03 /lib/firmware/amdgpu/gc_12_0_0_mes1.bin.zst
-rw-r--r-- 1 root root 46K Mar  6 10:03 /lib/firmware/amdgpu/gc_12_0_0_mes.bin.zst
-rw-r--r-- 1 root root 88K Mar  6 10:03 /lib/firmware/amdgpu/gc_12_0_0_uni_mes.bin.zst
-rw-r--r-- 1 root root 34K Mar  6 10:03 /lib/firmware/amdgpu/gc_12_0_1_mes1.bin.zst
-rw-r--r-- 1 root root 49K Mar  6 10:03 /lib/firmware/amdgpu/gc_12_0_1_mes.bin.zst
-rw-r--r-- 1 root root 88K Mar  6 10:03 /lib/firmware/amdgpu/gc_12_0_1_uni_mes.bin.zst

Hashes:

9ab7a403940348a16f86f0e7728ec035b6d345558daaef7bcff7a66b50660412  gc_12_0_0_mes1.bin.zst
e27cb59e809ca6db8fa3dbd0c5ba877674803e186dca74cb450e6244e921c465  gc_12_0_0_mes.bin.zst
2d2845ed50a33e57e13728a793999c80f362f94a6e79cd84de4753da1165b780  gc_12_0_0_uni_mes.bin.zst
3c5a3e87875eda8db258b918c4f8c1f1e269a0366e2e35a610686b29361532ba  gc_12_0_1_mes1.bin.zst
76af514082bd79f7e3f4d436e1a7aed4b62612e6eecdf96513a8154fc3ed3a07  gc_12_0_1_mes.bin.zst
e32883710e54a26da259ab2d98e3c96c30f0a4a0bd54dc510f395a13041354af  gc_12_0_1_uni_mes.bin.zst

After reboot, dmesg still reports:

[    8.235946] amdgpu 0000:0a:00.0: MES FW version must be >= 0x82 to enable LR compute workaround.

So reinstalling amdgpu-dkms-firmware does not appear to provide newer MES firmware for AI PRO R9700 / 1002:7551. Both 30.30.2 and 31.20 still appear to ship the same March 6 gc_12_0_*_mes blobs.

---

### 评论 #5 — amd-nicknick (2026-04-29T13:18:44Z)

I know what's going on here: You're looking at the wrong GPU.
Do you have a Ryzen CPU that contains an iGPU? The firmware output is for that integrated GPU.

Could you please try disabling the iGPU in BIOS, or run lspci to make sure you're picking out the correct BDF for the R9700?
Thanks!

---

### 评论 #6 — tamascode (2026-04-30T18:35:19Z)

@amd-nicknick 
Thanks — I thought about the same possibility, so I switched the test to my other server specifically to avoid that issue.

This second system is a Threadripper server and only has three gfx1201 / Radeon AI PRO R9700 cards installed. There is no Ryzen iGPU in this system.

Here is the DRM card to PCI BDF mapping:

card1  BDF=0000:0a:00.0  vendor=0x1002  device=0x7551
card2  BDF=0000:0d:00.0  vendor=0x1002  device=0x7551
card3  BDF=0000:45:00.0  vendor=0x1002  device=0x7551

The additional entries such as card1-DP-1, card1-DP-2, card1-Writeback-1, etc. are DRM connector paths under the same GPU cards, not additional GPUs.

The lspci output also shows the three VGA devices as:

0000:0a:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:7551] (rev c0)
0000:0d:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:7551] (rev c0)
0000:45:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Device [1002:7551] (rev c0)

So the firmware/MES/SMU output was collected from the gfx1201 / R9700 devices, not from an integrated GPU.

Could you please clarify what firmware version is expected for Radeon AI PRO R9700 / gfx1201 cards, and whether there is a supported way to update the firmware on these cards?

---

### 评论 #7 — amd-nicknick (2026-05-01T04:24:19Z)

@tamascode great! Could you capture the new output of `sudo cat /sys/kernel/debug/dri/<Your GPU BDF>/amdgpu_firmware_info` on the threadripper system?
The reason I suspect you're looking at iGPU is the VBIOS it has: `VBIOS version: 102-RAPHAEL-008`, that’s the iGPU.

---

### 评论 #8 — tamascode (2026-05-01T05:23:52Z)

@amd-nicknick 
Thanks — I reran the command on the Threadripper system using the BDF-named debugfs paths for the three gfx1201 / Radeon AI PRO R9700 cards.

The paths used were:

sudo cat /sys/kernel/debug/dri/0000:0a:00.0/amdgpu_firmware_info
sudo cat /sys/kernel/debug/dri/0000:0d:00.0/amdgpu_firmware_info
sudo cat /sys/kernel/debug/dri/0000:45:00.0/amdgpu_firmware_info

These are the three R9700 devices previously confirmed by lspci as PCI ID 1002:7551.

The new output no longer shows the Raphael iGPU VBIOS string. The three cards report:

0000:0a:00.0
MES_KIQ firmware version: 0x0000008b
MES firmware version:     0x0000008b
VBIOS version:            113-48WD6SHD1-P02

0000:0d:00.0
MES_KIQ firmware version: 0x0000008b
MES firmware version:     0x0000008b
VBIOS version:            113-APM107573-101

0000:45:00.0
MES_KIQ firmware version: 0x0000008b
MES firmware version:     0x0000008b
VBIOS version:            113-R9700AT-F40

Full amdgpu_firmware_info output is below:

============================================================
GPU BDF: 0000:0a:00.0
Path: /sys/kernel/debug/dri/0000:0a:00.0/amdgpu_firmware_info
============================================================
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b72
PFP feature version: 29, firmware version: 0x00000bc2
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000cb2
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3805204, firmware version: 0x003a1014
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684c00 (104.76.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x0910c011
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x0a000800
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x0000008b
MES feature version: 1, firmware version: 0x0000008b
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-48WD6SHD1-P02

============================================================
GPU BDF: 0000:0d:00.0
Path: /sys/kernel/debug/dri/0000:0d:00.0/amdgpu_firmware_info
============================================================
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b72
PFP feature version: 29, firmware version: 0x00000bc2
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000cb2
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3805204, firmware version: 0x003a1014
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684c00 (104.76.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x0910c011
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x0a000800
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x0000008b
MES feature version: 1, firmware version: 0x0000008b
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-APM107573-101

============================================================
GPU BDF: 0000:45:00.0
Path: /sys/kernel/debug/dri/0000:45:00.0/amdgpu_firmware_info
============================================================
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b72
PFP feature version: 29, firmware version: 0x00000bc2
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000cb2
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3805204, firmware version: 0x003a1014
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684c00 (104.76.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x0910c011
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x0a000800
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x0000008b
MES feature version: 1, firmware version: 0x0000008b
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-R9700AT-F40


---

### 评论 #9 — amd-nicknick (2026-05-04T11:01:49Z)

Yes, and the loaded MES FW for these 3 GPUs are 0x8B. This is the correct version to use on these GPU.
Could you please help clarify if you're encountering any specific issue with your setup here?

---

### 评论 #10 — tamascode (2026-05-05T03:50:49Z)

@amd-nicknick 

I found the source of the warning. The dmesg message is not checking the MES firmware version shown in amdgpu_firmware_info. It is checking:

(mes->adev->mes.sched_version & AMDGPU_MES_VERSION_MASK) >= 0x82

In debugfs all three GPUs report:

0000:0a:00.0: MES_KIQ 0x8B, MES 0x8B
0000:0d:00.0: MES_KIQ 0x8B, MES 0x8B
0000:45:00.0: MES_KIQ 0x8B, MES 0x8B

But dmesg still prints once:

MES FW version must be >= 0x82 to enable LR compute workaround.

So it looks like the warning is based on sched_version, not the actual loaded MES firmware version. Is this expected? Should sched_version also be 0x8B on AI PRO R9700, or is it normal for the LR compute workaround to stay disabled even when MES/MES_KIQ firmware is 0x8B?

Also, the 31.20 DKMS source still has:

mes_set_hw_res_pkt.oversubscription_timer = 50;

in mes_v12_0.c. Does amdgpu-dkms 6.19.0.31200000 include the gfx12 idle-power fix, or is that fix only in a newer kernel/amdgpu branch?

---

### 评论 #11 — amd-nicknick (2026-05-05T17:02:04Z)

Hi @tamascode, just checked the MES FW code, the idle power fix is actually in the MES firmware 0x8B, the code change in amdgpu is to prevent triggering it when FW is older than 0x8B.

For the log message, it's a sequence problem: The driver initializes the KIQ first, when setting the resources, it reads out the empty scheduler pipe FW version. On subsequent initialization of sched pipe, the LR compute WA is actually enabled.

The MES implements the LR compute WA in scheduler pipe, therefore the log message is spurious. I'll check internally to see the init sequence.

Please let me know if you have any further questions, thanks!

---

### 评论 #12 — tamascode (2026-05-12T07:17:28Z)

@amd-nicknick , The heigh gpu usage is mostly gone. I am still seeing 1 to 3 % gpu usage after the the request completed using llama.cpp but the fix I was looking for is now applied. 

---
