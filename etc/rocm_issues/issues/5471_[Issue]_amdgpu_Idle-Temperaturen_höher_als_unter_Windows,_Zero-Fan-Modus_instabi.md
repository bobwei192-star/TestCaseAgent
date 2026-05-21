# [Issue]: amdgpu: Idle-Temperaturen höher als unter Windows, Zero-Fan-Modus instabil (Sapphire RX 570 Nitro+)

> **Issue #5471**
> **状态**: closed
> **创建时间**: 2025-10-05T12:50:11Z
> **更新时间**: 2025-10-21T14:28:18Z
> **关闭时间**: 2025-10-21T14:28:18Z
> **作者**: forrestkuen
> **标签**: ROCm 6.3.1, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5471

## 标签

- **ROCm 6.3.1** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

Description:
My AMD Sapphire Radeon RX 570 Nitro+ 8GB GDDR5 graphics card gets warmer when idle under Linux (kernel 6.8.0-85-generic) than under Windows.

Idle temperatures: Linux ~53°C, Windows ~44°C

Without dynamic fan control, the fans constantly cycle on/off.

With LACT, temperatures remain normal, but the fans produce an audible whirring noise shortly before shutdown.

Expected behavior:

GPU idle temperature should not be higher than under Windows.

Zero-fan mode should work reliably without fans speeding up unnecessarily.

Steps to reproduce:

Boot the system without load.

Monitor idle temperatures (e.g., sensors or /sys/class/drm/card0/device/hwmon/hwmon*/temp1_input).

Compare with Windows idle temperatures on the same system.

Additional information:

LACT corrects the temperature issue, but causes shutdown noise.

Improving zero-fan support and fan control in the amdgpu driver may resolve the issue.

### Operating System

Linux Mint 22.2

### CPU

Ryzen 5 1600

### GPU

AMD Sapphire Nitro RX 570 8 GB

### ROCm Version

6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-10-08T15:12:36Z)

Hi @forrestkuen. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — HUSRCF (2025-10-14T07:55:24Z)

Addition: Same problems with new AMD cards. I encountered the same problems with W7900, RX 7900 XTX, 7900GRE and RX590. I guess this might caused by poor support for DPM and fixed MCLK. On Linux, MCLK seems to be locked at a higher level compared to that on windows. Also, the power management of PCIe seems not to be well supported by Linux and keeps at the normal state even there's no burden.

---

### 评论 #3 — HUSRCF (2025-10-14T07:59:11Z)

For a quick solution, you might consider using corectrl to regulate the power setting or something according to your need. But this is a rude method and might cause problems if you forget to turn it back.

---

### 评论 #4 — tcgu-amd (2025-10-14T17:18:52Z)

Hi @HUSRCF, thanks for reaching out! The temperature difference does seems to fall within reasonable range. Different systems have different default power-settings, so it is quite normal to see power/temperature difference across systems. For the fan whirling, that's likely the due to how the driver teardown process occurs on the Linux systems. A lot of fans' default setting in undriven state is full-speed, so the fans will be turned on briefly during the gap between driver teardown and power cut-off. This should be normal. Windows often have tighter integration with BIOS for fan control that can ensure the fans are driven throughout the shutdown, hence the difference. Both cases are normal, and the driver is behaving expectedly in either cases. 

---

### 评论 #5 — forrestkuen (2025-10-17T10:31:58Z)

I found a solution with the Application "LACT". I have created a profile "Powersave". The GPU only reaches temperatures near 50 degress. And i use an own fan-curve. So the fans start at 55 degrees...

---

### 评论 #6 — tcgu-amd (2025-10-21T14:28:18Z)

Hi @HUSRCF, I will be closing this issue for now since the described behaviors appears to be normal and there hasn't been any further follow ups from you. @forrestkuen, thank you for chiming in! Please let me know if any of you require further assistance and I will reopen the issue. Thanks!  

---
