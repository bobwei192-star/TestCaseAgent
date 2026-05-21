# [Ask for Assistance] There seems to be an issue with calling amdhip64_6.DLL in HIP SDK versions 6.1.2~6.2.4 under Ollama.

> **Issue #5693**
> **状态**: closed
> **创建时间**: 2025-11-25T16:55:18Z
> **更新时间**: 2025-11-26T11:15:26Z
> **关闭时间**: 2025-11-26T11:15:26Z
> **作者**: LaoDi-Sama
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5693

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

When I using Ollama(Compared to the main branch, this branch only adds a few GPUs that are not officially supported by Ollama, but HIP is officially supported.) , I noticed few strange [issues1](https://github.com/likelovewant/ollama-for-amd/issues/89)  [issues2](https://github.com/likelovewant/ollama-for-amd/issues/112)

The problems all seem to point to amdhip64_6.dll , but i vaguely remember not encountering this problem when using HIPSDK 5.7 

### Operating System

Windows 10 Pro 22H2 19045.5274

### CPU

Ryzen 5 5600G

### GPU

Radeon RX 6600

### ROCm Version

amdhip64_6.dll (3640.0, 3628.0, 3617.0）  HIP SDK (6.2.4)

### ROCm Component

HIP

### Steps to Reproduce

1.download exe installer from [here](https://github.com/likelovewant/ollama-for-amd/releases/tag/v0.9.2)
2.install it in a certain folder.
3.install HIP SDK 6.2.4 without Ray Tracing (Also checked Install GPU Driver in the install program)
4.download from [rocm.gfx1032.for.hip.sdk.6.2.4.navi21.logic.7z](https://github.com/likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU/releases/download/v0.6.2.4/rocm.gfx1032.for.hip.sdk.6.2.4.navi21.logic.7z)
5. replace all files into the _E:\Ollama0.9.2\lib\ollama\rocm\rocblas_ 
6. tried advice in  [issues1](https://github.com/likelovewant/ollama-for-amd/issues/89)






I'm wondering if this DLL wasn't correctly replaced somewhere during the HIP SDK update (I tried cross-replacing the DLLs from the three versions described in the [ROCm Version] section, but it didn't solve the strange problem I encountered in the aforementioned issue). If I need to replace or reinstall the HIP SDK or ollama, which locations should I pay attention to replacing? (\system32, AMD\rocm\6.2\bin OR ollama\lib\ollama\rocm\rocblas)

(OR Am I wrong? The real problem isn't caused by this?)

my garphic driver is 

<img width="668" height="357" alt="Image" src="https://github.com/user-attachments/assets/524a3871-56f8-4f0f-88d6-d71015ec9432" />

<img width="370" height="100" alt="Image" src="https://github.com/user-attachments/assets/27fb71bd-9763-42c7-9d56-db3104120b1a" />


Looking forward your help, if you need more info please let me know, i will reply in my spare time as quickly as i can.
thx


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

btw, while running a model with ollama, i can't see any usage(only around 3%) in taskmgr, but in the "amd software" i can see the true usage and power usage ()
