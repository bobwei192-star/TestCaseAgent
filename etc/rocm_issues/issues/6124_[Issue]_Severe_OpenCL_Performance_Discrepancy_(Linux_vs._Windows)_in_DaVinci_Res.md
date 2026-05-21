# [Issue]: Severe OpenCL Performance Discrepancy (Linux vs. Windows) in DaVinci Resolve Studio

> **Issue #6124**
> **状态**: open
> **创建时间**: 2026-04-07T10:29:19Z
> **更新时间**: 2026-04-20T13:55:15Z
> **作者**: lseurttyuu
> **标签**: status: triage, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6124

## 标签

- **status: triage** (颜色: #585dd7)
- **status: assessed** (颜色: #e6d813)

## 负责人

- tcgu-amd

## 描述

### Problem Description

Hi everyone,

I am opening this issue to report a massive performance discrepancy I’ve observed in OpenCL compute workloads when comparing the Windows and Linux AMD drivers.

I recently transitioned to Linux as my daily driver and use DaVinci Resolve Studio professionally. However, compute-heavy tasks, specifically image noise reduction, are running nearly 3x slower on Linux with ROCm compared to the official Windows drivers on the exact same hardware.

To ensure an exact 1:1 comparison, both environments were configured in the same way, and both projects were exported using the Avid DNxHR codec.

**Hardware & Software Environment**
- CPU: AMD Ryzen 9 5950X
- GPU: AMD Radeon RX 7900 XTX
- RAM: 64GB DDR4 3600 MT/s
- Linux OS: Debian 13 (Kernel 6.12) with ROCm 7.2.1 (+ open-source amdgpu kernel driver)
- Windows OS: Windows 10 Professional 64-bit (Latest AMD Adrenalin drivers)
- Software: DaVinci Resolve Studio 20.3.2
- API: OpenCL (Both OSs)
- Export Codec: Avid DNxHR (Both OSs)

**Test Scenarios & Render Times**
**Project A:** A single 33-minute 4K MP4/AVC file. Light color grading (gain, temp, LUTs). Heavy noise reduction:
- Temporal NR: 3 Frames, Motion Est: Better, Motion Range: Medium, Threshold Luma/Chroma: 58.5
- Spatial NR: Mode Enhanced, Threshold Luma/Chroma: 27.6
- **Windows Render Time: 87 minutes**
- **Linux Render Time: 208 minutes** _(2.4x slower)_

**Project B** (Real-World): A 15-minute short film. Multiple 6K BRAW files output to a 4K timeline. Heavy color grading and heavy noise reduction:
- Temporal NR: 2 Frames, Motion Est: Better, Motion Range: Medium, Threshold Luma/Chroma: 10.6
- Spatial NR: Mode Better, Threshold Luma/Chroma: 5.7
- **Windows Render Time: 27 minutes**
- **Linux Render Time: 79 minutes** _(2.9x slower)_

**Hardware Telemetry Anomalies**
While rendering Project B, I monitored system resources, and the hardware behavior on Linux points directly to GPU starvation:
- **Windows Telemetry:** ~17% CPU utilization | 90-95% GPU utilization. The GPU pulled ~350W (100°C hotspot) with clocks hovering around 2600 MHz.
- **Linux Telemetry:** ~8% CPU utilization | ~80% reported GPU utilization. The GPU pulled only ~195W on average (85°C hotspot), despite the clocks sitting significantly higher at ~2950 MHz.


**Discussion / Questions**
The combination of incredibly high clock speeds (2950 MHz) but severely reduced board power (195W) on Linux suggests the GPU is being starved of work - waiting on memory transfers or API queues rather than actively computing.

I understand DaVinci Resolve is proprietary software, making diagnosis from the driver side difficult, but I would appreciate any technical insights into the source of this huge discrepancy.

1. Is ROCm's OpenCL implementation known to be heavily unoptimized for these specific types of image processing workloads compared to the Windows OpenCL stack?
2. Could this be caused by how the Linux version of Resolve interfaces with AMD GPUs? For example, the Linux version lacks the "Neural Engine Optimization" option found on Windows. Could missing software optimizations like this lead to the driver starvation seen in the telemetry?
3. Is this fixable via any known driver-level tweaks or environment variables on Linux, or is this completely reliant on Blackmagic Design rewriting their OpenCL implementation for Linux/ROCm?

I'm ready to provide any additional logs or information if necessary. Thank you for your time.

### Operating System

Debian 13 (trixie)

### CPU

AMD Ryzen 9 5950X

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

7.2.1

### ROCm Component

_No response_

### Steps to Reproduce

1. Open Davinci Resolve Studio on exact same hardware on Windows and on Linux.
2. Put a video file on a timeline, configure temporal noise reduction in "Color" tab.
3. Render the timeline, observe the render times & resource usages differences between Windows and Linux.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[rocminfo_support.txt](https://github.com/user-attachments/files/26534224/rocminfo_support.txt)

### Additional Information

(**EDIT**) For additional context, I observed these exact same performance discrepancies using an older software stack (ROCm 7.1 + DaVinci Resolve Studio 19). This indicates that the bottleneck is not a recent regression in the latest software versions, but rather a long-standing issue.

(**EDIT 2**) I ran an additional test on Windows for Project B to see if the "Neural engine optimization" feature was responsible for the performance gap. Comparing render times with this feature toggled On versus Off yielded no significant difference. This effectively rules out the missing Linux feature as the primary cause of the severe performance discrepancy.
