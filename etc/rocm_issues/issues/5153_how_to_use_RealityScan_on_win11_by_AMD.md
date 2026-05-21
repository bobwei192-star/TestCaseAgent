# how to use RealityScan on win11 by AMD

> **Issue #5153**
> **状态**: closed
> **创建时间**: 2025-08-05T06:43:56Z
> **更新时间**: 2025-08-05T17:59:49Z
> **关闭时间**: 2025-08-05T17:59:49Z
> **作者**: homuragachi
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/5153

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

did anyone successful? It took my hole day ,but I could'n solve that .
i use **zluda** to change my system32 nvcuda.dll , but zluda does **not have the function :cuLaunchKernel**

then i change way; i try to use HIP and ROCm on windows

in my windows file ,ROCm\6.2\**libexec\rocm_smi**  the {libexec\rocm_smi}could't find 
there also can't find 6.2\bin\rocminfo.exe

if u know how to fix that, please help me .


### Operating System

windows11

### CPU

amd 7600

### GPU

7900XTX

### ROCm Version

ROCm 6.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-08-05T15:27:28Z)

Hi @homuragachi. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-08-05T15:56:02Z)

Hi @homuragachi, it doesn't look like RealityScan has support for AMD cards at the moment, so I don't think there are any fixes or workarounds possible on our end.

Regarding the missing rocm_smi and rocminfo on Windows, these are Linux-specific and are not included in the HIP SDK; see https://rocm.docs.amd.com/projects/install-on-windows/en/develop/reference/component-support.html. Is there a reason you need these?

---

### 评论 #3 — homuragachi (2025-08-05T16:45:35Z)

First of all, thank you for answering my question

at the firsst ,i choose zluda, then failed. so I ask deepseek, he told me there is###  another way:

graph LR
A[RealityScan] --> B{ROCm兼容层}
B --> C[HIPIFY转换]
B --> D[OpenCL后端]
C --> E[修改后的执行文件]
D --> F[CPU/GPU混合计算]

powershell
```
# 安装最新AMD显卡驱动（必需基础）
winget install AMD.RadeonSoftware.Adrenalin

# 安装ROCm Windows版（含HIP工具链）
Invoke-WebRequest -Uri "https://repo.radeon.com/rocm/rocm-windows/latest/rocm-win-installer.exe" -OutFile rocm_installer.exe
Start-Process rocm_installer.exe -ArgumentList "/S" -Wait

# 验证安装
& "C:\Program Files\AMD\ROCm\bin\rocminfo.exe" | Select-String "gfx"  # 应显示显卡代号（如gfx1030）
```

then i told deepseek my GPU is 7900xtx , he gave some advise on the  below

🚀 7900 XTX 专用配置方案（无需复杂步骤）
第一步：创建转换脚本
桌面新建文本文件 → 命名为 Convert_RealityScan.ps1

完整复制 以下内容：

powershell
```
# 设置7900 XTX专用参数
$rocmPath = "C:\Program Files\AMD\ROCm\6.2"
$realityScanPath = "C:\Program Files\Epic Games\RealityScan\RealityScan.exe"
$outputPath = "C:\RealityScan_HIP\RealityScan_HIP.exe"

# 执行转换（7900 XTX使用gfx1100架构）
& "$rocmPath\bin\hipify-clang.exe" `
  --cuda-path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2" `
  --hip-device-lib-path "$rocmPath\lib" `
  --offload-arch=gfx1100 `  # 7900 XTX专用架构
  -o $outputPath `
  $realityScanPath

Write-Host "转换完成！双击Run_RealityScan.bat启动程序"
pause
```
第二步：创建一键启动脚本
桌面新建文本文件 → 命名为 Run_RealityScan.bat

完整复制 以下内容：

batch
```
@echo off
setlocal

:: === 7900 XTX专用配置 ===
set "ROCM_PATH=C:\Program Files\AMD\ROCm\6.2"
set "PATH=%ROCM_PATH%\bin;%PATH%"
set HSA_OVERRIDE_GFX_VERSION=11.0.0
set GPU_MAX_HEAP_SIZE=100
set HIP_IGNORE_DEVICE_MAP=1

:: === 启动转换后的程序 ===
start "" "C:\RealityScan_HIP\RealityScan_HIP.exe"

endlocal
```
第三步：执行操作流程
创建输出目录：

按 Win+R 输入 cmd

执行：mkdir C:\RealityScan_HIP

运行转换脚本：

右键 Convert_RealityScan.ps1 → 使用 PowerShell 运行

等待完成（约2-5分钟）

启动程序：

双击 Run_RealityScan.bat


### Of course, it still failed.
so i have no choice..
and now i have already bought 2080ti22g, and it will both used on my computer. i have doulbe system(both windows and linux on different ssd)and my linux have rocm and rocm/pytorch ;  is there any question will happen when i both run nv and amd?

---

### 评论 #4 — schung-amd (2025-08-05T17:59:49Z)

`hipify-clang` is meant for source code; see https://rocm.docs.amd.com/projects/HIPIFY/en/latest/how-to/hipify-clang.html.

Regarding having both Nvidia and AMD GPUs installed in the same machine, I don't think we have any guidance that explicitly forbids this but I also don't think we test on this configuration so I wouldn't be surprised if issues arise. If you run into problems with that configuration please comment here or submit them as new issues and we can take a look.

Closing this for now as RealityScan needs added AMD support to resolve the primary issue, but feel free to continue commenting here if you need further guidance.

---
