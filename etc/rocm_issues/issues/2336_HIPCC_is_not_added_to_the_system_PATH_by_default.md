# HIPCC is not added to the system PATH by default

> **Issue #2336**
> **状态**: open
> **创建时间**: 2023-07-27T15:23:12Z
> **更新时间**: 2026-01-25T03:58:01Z
> **作者**: saadrahim
> **标签**: Verified Issue, Windows, 5.5.1
> **URL**: https://github.com/ROCm/ROCm/issues/2336

## 标签

- **Verified Issue** (颜色: #0052cc)
- **Windows** (颜色: #c2e0c6)
- **5.5.1** (颜色: #bfd4f2)

## 描述

 HIPCC can be used to compile and build applications using the AMD HIP SDK. HIPCC is not added to the system path due to security concerns. Values should be added to the PATH manually.
-	Add Hip SDK Hipcc path to System variables(path) C:\Program Files\AMD\ROCm\5.5\bin, this allows users to compile without providing absolute path.
-	Add HIP_ROCCLR_HOME = C:\Program Files\AMD\ROCm\5.5\, It Enables GPU Visibility to Hip based ISV’s/apps


---

## 评论 (5 条)

### 评论 #1 — keryell (2023-08-16T02:07:36Z)

I am curious about the "security concerns".
Can you elaborate?
At the end what is the problem? Someone types by error on the keyboard `hipcc` by error and havoc happens?

---

### 评论 #2 — nartmada (2024-04-21T15:26:50Z)

@saadrahim, please confirm if the issue has been fixed.  Thanks.

---

### 评论 #3 — nazar-pc (2024-09-26T16:17:41Z)

Just installed `AMD-Software-PRO-Edition-24.Q3-WinSvr2022-For-HIP.exe` (6.1.2) and it still didn't add itself to `PATH` :confused: 

---

### 评论 #4 — nazar-pc (2024-09-27T05:50:07Z)

Adding `C:\Program Files\AMD\ROCm\6.1\bin` to `Path` manually is also problematic (at least with above mentioned 6.1.2 verison) because it contains clang and llvm of unexpected versions that causes other software fail to compile because of it (looks like clang is compiled without wasm32 supports, etc.).

This is a very painful experience for developers.

---

### 评论 #5 — martinhavens (2026-01-25T03:56:54Z)

follow up same here. hipcc in a shell does nothing so it's not on my path, going to Program Files/rocm.../bin has hipcc.exe

Get-ComputerInfo | Format-Table CsSystemType,OSName,OSDisplayVersion

CsSystemType OsName                   OSDisplayVersion
------------ ------                   ----------------
x64-based PC Microsoft Windows 11 Pro 25H2


9070 XT
7800X3D

but i do have HIP_PATH as C:\Program Files\AMD\ROCm\7.1\

---
