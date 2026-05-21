# RX 9070 XT (GFX1201): Boot warnings - REG_WAIT timeout, SMU version mismatch, HDMI infoframe failure

> **Issue #6073**
> **状态**: closed
> **创建时间**: 2026-03-27T10:35:06Z
> **更新时间**: 2026-04-13T02:59:38Z
> **关闭时间**: 2026-04-13T02:59:38Z
> **作者**: chardric
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6073

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

## Description

Multiple amdgpu driver warnings appear at every boot with an AMD Radeon RX 9070 XT (device 0x7550, GFX1201/RDNA 4). The system is functional but these indicate driver/firmware interface gaps for this GPU.

## Warnings Observed (from dmesg)

### 1. SMU Driver Interface Version Mismatch
```
amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000033, smu fw program = 0, smu fw version = 0x00684c00 (104.76.0)
amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
```
The kernel driver expects SMU interface 0x2e but the GPU firmware reports 0x33.

### 2. REG_WAIT Timeout (occurs twice during boot)
```
amdgpu 0000:03:00.0: [drm] REG_WAIT timeout 1us * 150000 tries - optc401_disable_crtc line:235
```
Display controller timing issue during CRTC disable — happens during initial mode setting.

### 3. HDMI Vendor Infoframe Setup Failure
```
amdgpu 0000:03:00.0: amdgpu: [drm] Failed to setup vendor infoframe on connector HDMI-A-1: -22
```
HDMI metadata/infoframe negotiation failing with error -EINVAL on one of two connected HDMI monitors.

### 4. MES Firmware Version Notice
```
amdgpu 0000:03:00.0: amdgpu: MES FW version must be >= 0x82 to enable LR compute workaround.
```

## System Information

| Component | Details |
|-----------|---------|
| **GPU** | AMD Radeon RX 9070 XT (0x1002:0x7550, subsystem 0x1458:0x2424) |
| **Architecture** | RDNA 4 / GFX1201 |
| **VRAM** | 16304 MB |
| **Motherboard** | MSI B650M GAMING PLUS WIFI (MS-7E24) v1.0 |
| **CPU** | AMD (Zen-based, 16 threads) |
| **Distro** | Linux Mint 22.3 (Zena), based on Ubuntu 24.04 |
| **Kernel** | 6.17.0-19-generic (HWE) |
| **amdgpu driver** | 3.64.0 |
| **Mesa** | 25.2.8-0ubuntu0.24.04.1 |
| **Vulkan** | 1.4.318 (RADV) |
| **LLVM** | 20.1.2 |
| **linux-firmware** | 20240318.git3b128b60-0ubuntu2.25 |
| **Display Controller** | DCN 4.0.1 |
| **DMUB firmware** | 0x0A000800 |
| **Displays** | 2x HDMI (both 1366x768) |

## Kernel Boot Parameters

```
BOOT_IMAGE=/boot/vmlinuz-6.17.0-19-generic root=UUID=... ro quiet splash amdgpu.dcdebugmask=0x10
```

Note: `amdgpu.dcdebugmask=0x10` is already applied as a workaround for known RDNA 4 display issues.

## Impact

- System is functional and displays work correctly after boot
- No GPU hangs or crashes observed during normal use
- Warnings appear on every boot
- SMU mismatch may prevent optimal power management behavior
- HDMI infoframe failure may affect HDR or advanced HDMI features

## Related Issues

- #5908 — SMU mismatch reported with ROCm on RDNA 4
- https://gitlab.freedesktop.org/drm/amd/-/issues/3368 — Similar REG_WAIT timeout pattern
- LKML patch discussion on vendor infoframe error handling (2025-04-07)

## Expected Behavior

All three warnings should be resolved:
1. SMU driver interface version should match firmware interface version
2. CRTC disable should complete without REG_WAIT timeout
3. HDMI vendor infoframe should be set up successfully or gracefully skipped

---

## 评论 (2 条)

### 评论 #1 — amd-nicknick (2026-03-30T10:23:52Z)

Hi @chardric, please install amdgpu DKMS for RX 9070 XT.
See this doc: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html
If you're not expecting to use ROCm, feel free to skip the ROCm packages / use cases. Thanks!

---

### 评论 #2 — amd-nicknick (2026-04-13T02:59:38Z)

Closing this issue due to inactivity, feel free to reopen if you're still encountering any problem. Thanks!

---
