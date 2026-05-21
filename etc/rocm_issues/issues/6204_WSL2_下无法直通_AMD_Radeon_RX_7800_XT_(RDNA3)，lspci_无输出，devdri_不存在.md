# WSL2 下无法直通 AMD Radeon RX 7800 XT (RDNA3)，lspci 无输出，/dev/dri 不存在

> **Issue #6204**
> **状态**: open
> **创建时间**: 2026-05-08T11:00:41Z
> **更新时间**: 2026-05-13T16:49:13Z
> **作者**: lin636
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6204

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- mapatel-amd

## 描述

### Problem Description

在 WSL2 环境下，按照 AMD 官方指南安装 ROCm 7.2.0 和 Adrenalin 26.2.2 驱动，RX 7800 XT 无法被识别。lspci 看不到显卡，rocminfo 崩溃并提示 HSA_OVERRIDE_GFX_VERSION may be needed，即使设置了 HSA_OVERRIDE_GFX_VERSION=11.0.0 也无效。底层错误为 dxgkio_query_adapter_info: Ioctl failed: -22，怀疑是 WSL2 dxgkrnl 与 RDNA3 的兼容性问题。

### Operating System

Ubuntu 24.04.4 LTS (Noble)（WSL2）

### CPU

AMD Ryzen 5 7500F

### GPU

AMD Radeon RX 7800 XT (gfx1101, Navi 32, RDNA3)

### ROCm Version

ROCm 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

1. 全新安装 Windows 11 10.0.26200.8037，启用 Hyper-V 和虚拟机平台。
2. BIOS 中开启 SVM、IOMMU、Above 4G Decoding、ReBAR。
3. 安装 AMD Adrenalin 26.2.2 驱动（WSL 专用版）。
4. 安装 WSL 2.6.3，设置默认版本为 WSL 2。
5. 安装 Ubuntu 24.04：wsl --install -d Ubuntu-24.04
6. 在 Ubuntu 中安装 ROCm 7.2（WSL 模式）：
   wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/noble/amdgpu-install_7.2.70200-1_all.deb
   sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
   sudo amdgpu-install --usecase=wsl,rocm --no-dkms
7. 重启 WSL：wsl --shutdown，重新进入 Ubuntu。
8. 执行 lspci | grep -i vga；ls /dev/dri/；dmesg | grep -i dxg

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

运行 /opt/rocm/bin/rocminfo 直接崩溃，输出 assertion failed：
Assertion `props.EngineId.ui32.Major && "HSA_OVERRIDE_GFX_VERSION may be needed"' failed.
已设置 HSA_OVERRIDE_GFX_VERSION=11.0.0，问题依旧。

### Additional Information

dmesg 完整错误：
[    0.588472] PCI: System does not support PCI
[    0.868579] AMD-Vi: AMD IOMMUv2 functionality not available on this system
[    2.320100] misc dxg: dxgkio_query_adapter_info: Ioctl failed: -22
[    2.324405] misc dxg: dxgkio_query_adapter_info: Ioctl failed: -2

环境变量已设置：HSA_OVERRIDE_GFX_VERSION=11.0.0

ROCm 安装方式：sudo amdgpu-install --usecase=wsl,rocm --no-dkms

[新建 文本文档 (3).txt](https://github.com/user-attachments/files/27517163/3.txt)

---

## 评论 (1 条)

### 评论 #1 — fcui-amd (2026-05-13T07:50:40Z)

Is your ASIC’s device ID included in the support list?  https://github.com/ROCm/librocdxg/blob/develop/shared/src/utils.cpp#L6

---
