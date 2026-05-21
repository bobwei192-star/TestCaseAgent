# [Issue]: ROCm 6.2.2 couldn't query GPU power and temperature monitor

> **Issue #4268**
> **状态**: closed
> **创建时间**: 2025-01-17T18:52:21Z
> **更新时间**: 2025-04-10T17:25:02Z
> **关闭时间**: 2025-04-10T17:25:00Z
> **作者**: LiweiPeng
> **标签**: Under Investigation, ROCm 6.2.2
> **URL**: https://github.com/ROCm/ROCm/issues/4268

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.2** (颜色: #ededed)

## 描述

### Problem Description

On the system below using ROCm 6.2.2, rocm-smi couldn't query one GPU's Temp and Power. Rebooting the node fixed the issue.
**My questions are:**
1) How does this monitor query error affect the GPU functionality?
2) What's the root cause of this monitor query error?

Ubuntu 22.04.5 LTS
ROCm version: 6.2.2-116
Hardware: MI300
```
$ rocm-smi
 
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
=============================================== ROCm System Management Interface ===============================================
========================================================= Concise Info =========================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK     MCLK     Fan  Perf  PwrCap       VRAM%  GPU%
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)
================================================================================================================================
0       2     0x74b5,   65402  56.0°C      321.0W    NPS1, N/A, 0        2074Mhz  1300Mhz  0%   auto  750.0W       90%    58%
1       3     0x74b5,   27175  54.0°C      322.0W    NPS1, N/A, 0        2077Mhz  1300Mhz  0%   auto  750.0W       90%    84%
2       4     0x74b5,   16561  53.0°C      308.0W    NPS1, N/A, 0        2084Mhz  1300Mhz  0%   auto  750.0W       90%    97%
3       5     0x74b5,   54764  51.0°C      311.0W    NPS1, N/A, 0        2083Mhz  1300Mhz  0%   auto  750.0W       90%    78%
4       6     0x74b5,   10760  38.0°C      136.0W    NPS1, N/A, 0        132Mhz   900Mhz   0%   auto  750.0W       0%     0%
5       7     0x74b5,   48981  39.0°C      136.0W    NPS1, N/A, 0        131Mhz   900Mhz   0%   auto  750.0W       0%     0%
6       8     0x74b5,   32548  37.0°C      137.0W    NPS1, N/A, 0        132Mhz   900Mhz   0%   auto  750.0W       0%     0%
7       9     0x74b5,   60025  N/A         N/A       NPS1, N/A, 0        None     None     0%   auto  Unsupported  0%     0%
================================================================================================================================
===================================================== End of ROCm SMI Log ======================================================

```

### Operating System

Ubuntu 22.04.5 LTS

### CPU

Intel Xeon

### GPU

AMD MI300x

### ROCm Version

ROCm 6.2.2

### ROCm Component

ROCm

### Steps to Reproduce

not sure how this occurred.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (15 条)

### 评论 #1 — ppanchad-amd (2025-01-17T19:09:13Z)

Hi @LiweiPeng. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — LiweiPeng (2025-01-17T20:03:57Z)

Thanks @ppanchad-amd  for the quick response

---

### 评论 #3 — jamesxu2 (2025-01-20T18:30:25Z)

Hi @LiweiPeng, under what circumstances do you see this issue (eg. what workload did you run to cause this failure)? It would be hard to answer your questions without being able to reproduce the issue. 



---

### 评论 #4 — LiweiPeng (2025-01-20T21:34:21Z)

@jamesxu2, it is not clear what workloads caused the issue. In general, if rocm-smi couldn't query temperature and power monitor data, how will it impact GPU functionality?

---

### 评论 #5 — jamesxu2 (2025-01-20T21:39:48Z)

@LiweiPeng Sorry, but I can't give you a general answer for that. There are many ways and many points along the rocm-smi codepaths that _could_ fail, but without knowing which exactly, we can't diagnose a general GPU failure or really give any general functionality impact assessment. It's possible for example that a GPU encountered a critical failure, failed to reset, and then corrupted the sysfs files we use to query these metrics, or maybe you just have some permissions issue in your environment or another process is interfering with rocm-smi. It's really quite hard to tell from this error signature alone.

If you do observe this issue again, please let us know how you induced it. 

Sorry I can't be more helpful here.

---

### 评论 #6 — LiweiPeng (2025-02-11T18:32:56Z)

@jamesxu2 , I continue seeing nodes with the original power monitor error. In a recent MI300 node, from kernel log, I saw many amdgpu errors like below. During 2 hours, there are thousands of errors for each of the below.

Does this mean the node needs to be fixed like reboot?

AmdGpuErr                                      ErrCount
amdgpu: failed to read reg:1629a    37896
amdgpu: Failed to export SMU metrics table! 34452
amdgpu: failed to write reg:2022    25326
amdgpu: failed to read reg:10af 24914
amdgpu: failed to read reg:3248 24912
amdgpu: SMU: response:0xFFFFFFFF for index:9 param:0x00000000 message:GetMetricsTable?  5764

---

### 评论 #7 — lucbruni-amd (2025-02-11T18:54:44Z)

Hi @LiweiPeng,

How soon after you reboot the node do you start seeing these logs? Is it immediately, or some time after?

---

### 评论 #8 — LiweiPeng (2025-02-11T19:13:56Z)

These errors were not after reboot. These errors were in kern.log when rocm-smi failed to query the power monitor data, before the node reboot.
  Expected integer value from monitor, but got ""


---

### 评论 #9 — lucbruni-amd (2025-02-11T19:30:05Z)

Thanks for letting me know! Regarding this:

> I continue seeing nodes with the original power monitor error.

How often has this occurred since you opened the issue? Is it very frequent?

---

### 评论 #10 — LiweiPeng (2025-02-12T14:21:04Z)

This problem occurred every day on different nodes. Can AMD prioritize the work and provide the solution or mitigation plan?

---

### 评论 #11 — lucbruni-amd (2025-02-12T17:04:15Z)

Hi @LiweiPeng, just wanted to assure you that I am prioritizing this issue and working with the team to get to the bottom of this. Thank you for your patience and for providing me additional information thus far!

---

### 评论 #12 — lucbruni-amd (2025-02-25T16:35:02Z)

Hi @LiweiPeng,

At the very least, `Expected integer value from monitor, but got ""` should not be printing like that - thanks for reporting.

We have not been able to reproduce your error across a few systems with multiple MI300s, so it is not possible to determine the exact root cause of your issue as there are multiple paths which lead to the `Failed to export SMU metrics table` error log. This is from amdgpu contacting the PMFW and failing to receive the metrics table which contains info like temperature, etc.

As for your GPU functionality/performance concerns- this depends on the state of the PMFW/SMU. It is possible that the PMFW may be in a deadlocked state, then the GPU may be unable to dynamically adjust its clock speeds based on workload demands. But the other MI300s have metric data populated as per your `rocm-smi` output, meaning this could be isolated to a GPU-specific issue.

Here's a couple quick recommendations we can try to resolve this:

1. If it is not too inconvenient, update ROCm/amdgpu (uninstall [ROCm](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html#uninstalling-rocm), [amdgpu-install](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html#uninstalling-amdgpu-install), and [re-install](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html#ubuntu) with the final installer command `sudo amdgpu-install --usecase=rocm,dkms`). It is the least invasive step we can take for your system.

2. Since this could be isolated to the one GPU, try reseating the card and check the cable connections to make sure they are secure. I'd also recommend swapping this card to another bus and see if the issue persists for that card specifically. It is a possibility that the GPU is damaged and needs replacing, which I cannot confirm as we cannot reproduce the issues at this time.

Please let me know if you have further information that may help us to reproduce this, and whether the steps above help in mitigating this issue. Thanks!

---

### 评论 #13 — LiweiPeng (2025-02-25T18:40:21Z)

Thanks for the update. This is very helpful.

---

### 评论 #14 — lucbruni-amd (2025-03-04T15:49:10Z)

No problem. Did those two comments above help with resolving the issue? I still have not been able to reproduce. Thanks!

---

### 评论 #15 — lucbruni-amd (2025-04-10T17:25:00Z)

Closing this issue due to inactivity. If the issue still persists after the suggestions above, please feel free to reopen this ticket or open a new one. Thanks!

---
