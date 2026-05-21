# [Issue]: Windows hip error 'no ROCm-capable device is detected'

> **Issue #2941**
> **状态**: closed
> **创建时间**: 2024-03-04T15:27:54Z
> **更新时间**: 2025-10-12T10:23:37Z
> **关闭时间**: 2024-06-28T19:10:01Z
> **作者**: EmotionIce
> **标签**: ROCm 5.7.1, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2941

## 标签

- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

After installing all HIP SDK with all its options successfully and setting up the system environment variables,
I get hipErrorNoDevice when running the `hipinfo` command or when trying to use hip:

```
:4:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\rocclr\platform\runtime.cpp:83  : 1256747841 us: [pid:20784 tid:0x9b0] init
:3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_context.cpp:48  : 1256747970 us: [pid:20784 tid:0x9b0] Direct Dispatch: 0
:3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:546 : 1256748073 us: [pid:20784 tid:0x9b0]  hipGetDeviceCount ( 0000000801EFFA3C )
:3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:548 : 1256748170 us: [pid:20784 tid:0x9b0] hipGetDeviceCount: Returned hipErrorNoDevice :
:3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:546 : 1256748258 us: [pid:20784 tid:0x9b0]  hipGetDeviceCount ( 0000000801EFFA3C )
:3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:548 : 1256748345 us: [pid:20784 tid:0x9b0] hipGetDeviceCount: Returned hipErrorNoDevice :
:3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:546 : 1256748410 us: [pid:20784 tid:0x9b0]  hipGetDeviceCount ( 0000000801EFFA3C )
:3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:548 : 1256748470 us: [pid:20784 tid:0x9b0] hipGetDeviceCount: Returned hipErrorNoDevice :
error: 'no ROCm-capable device is detected'(100) at C:\constructicon\builds\gfx\two\23.30\drivers\compute\hip-tests\samples\1_Utils\hipInfo\hipInfo.cpp:205
error: API returned error code.
error: TEST FAILED
```

The GPU is recognized by the system and usually works.

### Operating System

Windows 11 Pro 10.0.22621 (22H2)

### CPU

Intel(R) Core(TM) i7-8086K CPU @ 4.00GHz

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 5.7.1

### ROCm Component

HIP

### Steps to Reproduce

I uninstalled all existing HIP and AMD drivers and downgraded from windows 23H2 to 22H2 (attempting to fix this). 
Downloaded HIP SDK 5.7.1 for Windows 10 & 11 and installed it.
Then I set up the system environment variables to be `HIP_PATH=C:\Program Files\AMD\ROCm\5.7\`, `HIP_PATH_57=C:\Program Files\AMD\ROCm\5.7\`, `HIP_VISIBLE_DEVICES=1` and in the Path variable I added `C:\Program Files\AMD\ROCm\5.7\bin` and `%HIP_PATH%bin`.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — harkgill-amd (2024-06-10T20:11:20Z)

Hi @EmotionIce, are you still experiencing this issue with HIP SDK 5.7.1?

---

### 评论 #2 — harkgill-amd (2024-06-28T19:10:01Z)

Hi @EmotionIce, I was unable to reproduce this issue with an AMD Radeon RX 7900 XT on HIP SDK 5.7.1. I will close the issue for now, please re-open it if the issue persists. Thanks!

---

### 评论 #3 — V6ser (2024-07-23T10:37:30Z)

I 

> ### Problem Description
> After installing all HIP SDK with all its options successfully and setting up the system environment variables, I get hipErrorNoDevice when running the `hipinfo` command or when trying to use hip:
> 
> ```
> :4:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\rocclr\platform\runtime.cpp:83  : 1256747841 us: [pid:20784 tid:0x9b0] init
> :3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_context.cpp:48  : 1256747970 us: [pid:20784 tid:0x9b0] Direct Dispatch: 0
> :3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:546 : 1256748073 us: [pid:20784 tid:0x9b0]  hipGetDeviceCount ( 0000000801EFFA3C )
> :3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:548 : 1256748170 us: [pid:20784 tid:0x9b0] hipGetDeviceCount: Returned hipErrorNoDevice :
> :3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:546 : 1256748258 us: [pid:20784 tid:0x9b0]  hipGetDeviceCount ( 0000000801EFFA3C )
> :3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:548 : 1256748345 us: [pid:20784 tid:0x9b0] hipGetDeviceCount: Returned hipErrorNoDevice :
> :3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:546 : 1256748410 us: [pid:20784 tid:0x9b0]  hipGetDeviceCount ( 0000000801EFFA3C )
> :3:C:\constructicon\builds\gfx\two\23.30\drivers\compute\clr\hipamd\src\hip_device_runtime.cpp:548 : 1256748470 us: [pid:20784 tid:0x9b0] hipGetDeviceCount: Returned hipErrorNoDevice :
> error: 'no ROCm-capable device is detected'(100) at C:\constructicon\builds\gfx\two\23.30\drivers\compute\hip-tests\samples\1_Utils\hipInfo\hipInfo.cpp:205
> error: API returned error code.
> error: TEST FAILED
> ```
> 
> The GPU is recognized by the system and usually works.
> 
> ### Operating System
> Windows 11 Pro 10.0.22621 (22H2)
> 
> ### CPU
> Intel(R) Core(TM) i7-8086K CPU @ 4.00GHz
> 
> ### GPU
> AMD Radeon RX 7900 XT
> 
> ### ROCm Version
> ROCm 5.7.1
> 
> ### ROCm Component
> HIP
> 
> ### Steps to Reproduce
> I uninstalled all existing HIP and AMD drivers and downgraded from windows 23H2 to 22H2 (attempting to fix this). Downloaded HIP SDK 5.7.1 for Windows 10 & 11 and installed it. Then I set up the system environment variables to be `HIP_PATH=C:\Program Files\AMD\ROCm\5.7\`, `HIP_PATH_57=C:\Program Files\AMD\ROCm\5.7\`, `HIP_VISIBLE_DEVICES=1` and in the Path variable I added `C:\Program Files\AMD\ROCm\5.7\bin` and `%HIP_PATH%bin`.
> 
> ### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
> _No response_
> 
> ### Additional Information
> _No response_

Your issue will persist. This problem had bugged me for some time now. Trying to get WSL to work on my gfx1031 card, I made the same mistake as you.

If I hadn't seen that you also set "HIP_VISIBLE_DEVICES" > 1 as a variable then I wouldn't have known. By removing HIP_VISIBLE_DEVICES from the system variables hipInfo works again.

---

### 评论 #4 — harkgill-amd (2024-07-23T14:13:08Z)

I'll add this here for future reference if someone stumbles across this issue. The "HIP_VISIBLE_DEVICES" environment variable specifies which devices are exposed to HIP applications, in this case hipInfo. 

The variable should be set in the form of comma separated list, for example `HIP_VISIBLE_DEVICES="0,2"` This variable is not set by default during the installation so to check the device numbering schema, you run hipInfo on the Windows HIP SDK or rocminfo on Linux. 

Manually setting the value to "1" hid your GPU from hipInfo.exe causing the error `no ROCm-capable device is detected`. You can find more information on HIP_VISIBLE_DEVICES and other GPU isolation techniques [here](https://rocm.docs.amd.com/en/latest/conceptual/gpu-isolation.html).


---

### 评论 #5 — jtgladiator (2025-01-23T12:11:25Z)

> I'll add this here for future reference if someone stumbles across this issue. The "HIP_VISIBLE_DEVICES" environment variable specifies which devices are exposed to HIP applications, in this case hipInfo.
> 
> The variable should be set in the form of comma separated list, for example `HIP_VISIBLE_DEVICES="0,2"` This variable is not set by default during the installation so to check the device numbering schema, you run hipInfo on the Windows HIP SDK or rocminfo on Linux.
> 
> Manually setting the value to "1" hid your GPU from hipInfo.exe causing the error `no ROCm-capable device is detected`. You can find more information on HIP_VISIBLE_DEVICES and other GPU isolation techniques [here](https://rocm.docs.amd.com/en/latest/conceptual/gpu-isolation.html).

This just fixed it for me too. Thank you @harkgill-amd and @V6ser 

---

### 评论 #6 — chandujr (2025-10-09T17:58:34Z)

I did set the variable `export ROCR_VISIBLE_DEVICES=0,2` but even after that I'm getting the error:
```
HIP failure 100: no ROCm-capable device is detected ; GPU=-1 ;
```

Even though these returned proper values:
```
> python3 -c 'import torch; print(torch.cuda.device_count())'
2

> python3 -c 'import torch; print(torch.cuda.get_device_name(0))'
AMD Radeon RX 6800M

> python3 -c 'import torch; print(torch.cuda.get_device_name(1))'
AMD Radeon Graphics

> python3 -c 'import torch; print(hasattr(torch.version, \'hip\'))'
True
```

---

### 评论 #7 — harkgill-amd (2025-10-09T18:59:17Z)

@chandujr, that's odd - could you file a new ticket with this information + 

- command you're running when you encounter the error
- ROCm and or HIP SDK release(s) you have installed on your system
- Output of initial erroring command without the `ROCR_VISBILE_DEVICES` env variable set

---

### 评论 #8 — chandujr (2025-10-12T10:23:37Z)

@harkgill-amd This particular problem for me got resolved. It happened because Actually I was checking this inside a venv and I installed the wrong onnxruntime-rocm package. My system ROCm version is 6.3.1 and after installing the proper onnxruntime-rocm package for that, it is working now.

---
