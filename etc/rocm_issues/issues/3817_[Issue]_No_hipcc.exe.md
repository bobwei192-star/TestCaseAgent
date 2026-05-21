# [Issue]: No hipcc.exe

> **Issue #3817**
> **状态**: closed
> **创建时间**: 2024-09-26T17:27:24Z
> **更新时间**: 2024-09-30T13:57:15Z
> **关闭时间**: 2024-09-30T13:48:12Z
> **作者**: nazar-pc
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3817

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I expected HIP SDK to contain `hipcc.exe`, but it is not there. Instead there is `hipcc`, which is a perl script and there is `hipcc.bin.exe`, which is a very confusing name instead of the normal one. Together with https://github.com/ROCm/ROCm/issues/2336 this results in a very frustrating experience on Windows.

### Operating System

Windows 11 (10.0.22631)

### CPU

AMD 7970X

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.2 (installed using `AMD-Software-PRO-Edition-24.Q3-WinSvr2022-For-HIP.exe`)

### ROCm Component

HIPCC


---

## 评论 (5 条)

### 评论 #1 — nazar-pc (2024-09-27T04:55:15Z)

After manually updating `PATH` I'm getting this:
>   Output { status: ExitStatus(ExitStatus(1)), stdout: "", stderr: "'perl' is not recognized as an internal or external command,\r\noperable program or batch file.\r\n" }

Of course I don't have `perl` installed, this is 2024! Official documentation at https://rocm.docs.amd.com/projects/HIPCC/en/latest/ says:
> There are both Perl and C++ executable versions of the hipcc and hipconfig compiler driver utilities provided. By default the C++ version is used when hipcc is run. To enable the Perl versions of these commands set the environment variable HIP_USE_PERL_SCRIPTS=1.

Which in my case is exactly the opposite!

The page seems to correspond to ROCm 6.2.1, but that doesn't seem to exist for Windows (the latest on downloads page is 6.1.2 for some reason).

Very frustrating experience so far.

---

### 评论 #2 — ppanchad-amd (2024-09-27T15:17:23Z)

Hi @nazar-pc, internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #3 — jamesxu2 (2024-09-30T13:48:12Z)

Hi @nazar-pc , thanks for bringing this up. 

The HIPCC team is aware that the naming of hipcc.bin.exe is clunky and it will be changed to hipcc.exe in a future release. 

Regarding the [statement in our documentation](https://rocm.docs.amd.com/projects/HIPCC/en/latest/), I agree that it is a bit confusing. The "hipcc" command is a Perl script that wraps the actual hipcc compiler, and based on environment variable HIP_USE_PERL_SCRIPTS invokes either the Perl hipcc.pl or C++ hipcc.bin (hipcc.bin.exe on Windows). I interpreted that statement the same way you did initially, and I've brought it up the docs team. For now though, you will unfortunately have to [install Perl](https://strawberryperl.com/) to run hipcc. 

We're in the middle of a general effort to clean up hipcc packaging and move away from perl (as you say, it is somewhat antiquated). This should be resolved in a future release. Things are a work-in-progress, so we appreciate your patience.  



---

### 评论 #4 — nazar-pc (2024-09-30T13:51:29Z)

It'd be better if `hipcc` was not a Perl script, so Perl if not required unless `HIP_USE_PERL_SCRIPTS` is used, but hopefully Perl version will go away altogether soon.

---

### 评论 #5 — jamesxu2 (2024-09-30T13:57:13Z)

> It'd be better if `hipcc` was not a Perl script, so Perl i[s] not required unless `HIP_USE_PERL_SCRIPTS` is used, but hopefully Perl version will go away altogether soon.

@nazar-pc , I agree with you, and this is in the roadmap for hipcc. You can look forward to this change being implemented in a future ROCm release. Thanks for the feedback! 


---
