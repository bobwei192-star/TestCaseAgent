# WSL2 not detect Radeon 8060S

> **Issue #4809**
> **状态**: closed
> **创建时间**: 2025-05-27T13:15:57Z
> **更新时间**: 2026-02-03T18:42:53Z
> **关闭时间**: 2025-05-28T14:44:05Z
> **作者**: yaoman3
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4809

## 描述

**Description:**
After installing the AMD GPU driver for WSL2, the system fails to recognize the Radeon 8060S graphics card. The only hardware detected is the CPU, and there are no signs of the GPU functioning within the Windows Subsystem for Linux environment.

**Steps to Reproduce:**
1. Install WSL2 on Windows 11.
2. Update to the latest kernel and install the necessary dependencies for AMD GPU support.
3. Install the AMDGPU drivers following the official installation guide.
4. Launch the WSL2 terminal and run a command to list hardware details (e.g., `lspci` or `glxinfo`).

**Expected Behavior:**
The system should detect the Radeon 8060S and display relevant GPU information alongside the CPU.

**Actual Behavior:**
Only the CPU is detected, and there is no acknowledgment of the Radeon 8060S in the hardware listings.

**Environment:**
- WSL2 version: 2.4.13.0
- Windows version: Windows 11
- AMDGPU driver version: 25.5.1
- Radeon model: 8060S


---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-05-28T14:44:05Z)

Hi @yaoman3, the Radeon 8060S and other APUs are not yet supported by ROCm on WSL resulting in the failure to detect the card. You can find a list of supported GPUs over in our [GPU Support Matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix). 

---

### 评论 #2 — Marerc (2026-02-03T07:36:12Z)

Is there any news to Radeon 8060S, iGPUs

---

### 评论 #3 — harkgill-amd (2026-02-03T18:42:53Z)

Hey @Marerc, please see https://github.com/ROCm/ROCm/issues/4952#issuecomment-3819558396.

---
