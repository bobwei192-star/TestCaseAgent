# [Issue]: HIPCC not executing, fails with path error

> **Issue #3680**
> **状态**: closed
> **创建时间**: 2024-09-04T22:15:03Z
> **更新时间**: 2025-02-10T20:13:42Z
> **关闭时间**: 2025-02-10T20:13:41Z
> **作者**: aaronsuydam
> **标签**: Under Investigation, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3680

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I am trying to compile some of the HIP samples on my computer, I downloaded and installed the HIP SDK and everything seemed fine, I had to install perl, as mentioned in #2713, but then I tried to compile the vector add samples, and I get this output: 
```
PS C:\Users\suyda\dev\school\research\GPU Frameworks Project\ROCm\HIP-Examples\vectorAdd> hipcc .\vectoradd_hip.cpp -o .\vectoradd_hip.exe
'C:\Program' is not recognized as an internal or external command,
operable program or batch file.

failed to execute:C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3\bin/nvcc  -Wno-deprecated-gpu-targets  -isystem C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3/include -isystem "include" -x cu  -Wno-deprecated-gpu-targets -lcuda -lcudart -LC:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3/lib64  .\vectoradd_hip.cpp -o ".\vectoradd_hip.exe"
PS C:\Users\suyda\dev\school\research\GPU Frameworks Project\ROCm\HIP-Examples\vectorAdd>
```

Not sure what to do. 

### Operating System

Windows 11

### CPU

AMD Ryzen 7 7600X

### GPU

AMD Instinct MI250

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIPCC

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

I don't actually have an MI250, it is making me pick a gpu anyway to report the issue. 

---

## 评论 (8 条)

### 评论 #1 — harkgill-amd (2024-09-05T13:57:29Z)

Hi @aaronsuydam, this may be due to `hipcc` not being added to the systems PATH. Could you try calling the executable directly from `C:\Program Files\AMD\ROCm\6.1\bin`? 

I see the nvcc compiler is being used in the second command, which GPU are you using specifically? I will remove the MI250 tag.

---

### 评论 #2 — aaronsuydam (2024-09-09T20:49:55Z)

I have a Ryzen 7600X which has built in Radeon Graphics. I tried executing from the same directory, and the bin dir is in my path. Same result. Sorry this took so long to get back on.

---

### 评论 #3 — aaronsuydam (2024-09-10T12:28:59Z)

Just adding onto this, I thought maybe reinstalling the HIP SDK would fix this, since sometimes things do go wrong in the install process. Unfortunately I get the exact same behavior. 

---

### 评论 #4 — harkgill-amd (2024-09-10T18:30:54Z)

@aaronsuydam, thanks for checking. 

There is currently a bug with how hipcc handles spaces in Windows paths. A fix will be available for this in the next Windows HIP SDK release though a temporary workaround may be to set the environment variable `HIP_PLATFORM=amd`. Could you please give this a try and let me know if the behavior differs. 

Please also note that the integrated graphics from the Ryzen 7600X are not currently supported for use with the Windows HIP SDK as highlighted at [System Requirements](https://rocm.docs.amd.com/projects/install-on-windows/en/develop/reference/system-requirements.html#windows-supported-gpus). This is not the cause of this specific issue but may result in different errors arising. 

---

### 评论 #5 — aaronsuydam (2024-09-10T20:19:46Z)

@harkgill-amd makes sense, another workaround that I found is running the bin/hipcc.pl perl script directly doesn't cause the error.

Theoretically if I wanted to enable my iGPU on my ryzen 7600x, is there a way to do that even though that means giving up the support and such? I know it isn't officially supported but I'm wondering if it's even possible.

---

### 评论 #6 — harkgill-amd (2024-09-13T14:45:56Z)

@aaronsuydam, there is no specific workaround to enable the iGPU for the Windows HIP SDK though there may still be some usability maintained. I will provide an update when the fix is made available and you can give it a try then to confirm.

---

### 评论 #7 — harkgill-amd (2025-01-29T16:33:19Z)

Hi @aaronsuydam, the 6.2.4 HIP SDK for Windows has been released which contains the fix for the handling of spaces in Windows paths. I can no longer reproduce the issues on my end. Could you please give this a try and confirm if the issue has been resolved?

---

### 评论 #8 — harkgill-amd (2025-02-10T20:13:41Z)

Closing this issue out due to a lack of response. If you're still experiencing the path errors on the latest HIP SDK, please leave a comment and I'll re-open this issue. Thanks!

---
