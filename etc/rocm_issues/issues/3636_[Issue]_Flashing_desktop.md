# [Issue]: Flashing desktop

> **Issue #3636**
> **状态**: closed
> **创建时间**: 2024-08-22T16:25:22Z
> **更新时间**: 2024-10-08T14:11:42Z
> **关闭时间**: 2024-10-08T14:11:42Z
> **作者**: curvedinf
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3636

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

OS:
NAME="Ubuntu"
VERSION="24.04 LTS (Noble Numbat)"
CPU: 
model name	: AMD Ryzen 9 7900X3D 12-Core Processor
GPU:
bash: /opt/rocm/bin/rocminfo: No such file or directory

(ROCm is currently uninstalled from my system due to this bug)

### Operating System

Ubuntu 24.04

### CPU

Ryzen 7900x3d

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

Follow quick start guide ( https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html ) on a fresh install of 24.04 including post installation instructions.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

After installing ROCm as above, the upper half of my desktop flashed white at a very fast interval.

My monitor runs at 360 hz. Maybe related?

Similar issue reported on stack overflow (not me) for a 7900xtx:
https://askubuntu.com/questions/1522473/graphics-crash-after-installing-rocm-in-ubuntu-24-04

---

## 评论 (8 条)

### 评论 #1 — harkgill-amd (2024-08-23T19:49:36Z)

Hi @curvedinf, are you able to open the terminal window or access the system through ssh after installing ROCm? If so, could you please do the following 
```
sudo apt install mesa-utils
AMD_DEBUG=info glxinfo > glxinfo.log
```
and provide the output/corresponding log generated.


---

### 评论 #2 — 0seba (2024-08-26T02:35:22Z)

Hi, I think I had a similar problem, finally worked by following these instructions https://github.com/nktice/AMD-AI

---

### 评论 #3 — markawonge (2024-09-04T02:51:38Z)

I encountered the same issue.

---

### 评论 #4 — harkgill-amd (2024-09-04T20:51:14Z)

@curvedinf, @0seba and @markawonge. We have identified the root cause of this issue and are working towards getting a fix out. In the meantime, a temporary workaround would be to install with `--usecase=graphics, rocm` rather than just `rocm`. A complete install would look like this.

```
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.2/ubuntu/jammy/amdgpu-install_6.2.60200-1_all.deb
sudo apt install ./amdgpu-install_6.2.60200-1_all.deb
sudo apt update
sudo amdgpu-install --usecase=graphics,rocm
```
Please let me know if you are able to get this working.

---

### 评论 #5 — curvedinf (2024-09-04T21:46:28Z)

@harkgill-amd That fix is actually how I got it working. I spent some time reading about the different modes of amdgpu-install and gave that a shot. So I can confirm that your fix does work and has worked without issue for some time. Thank you for getting back to us and thank you for helping to make the tools of the future.

---

### 评论 #6 — 0seba (2024-09-15T22:07:07Z)

Do you know if it would be possible to use with kernel version 6.10.10 and 780m iGPU.
I read that it introduces possibility for memory allocation more suited to run LLMs so I wanted to try that version, but I haven't managed to make it run. I installed with this command `sudo amdgpu-install --usecase=graphics,rocm,hiplibsdk,rocmdev --no-dkms`, but after this commands like `rocm-smi`, `rocminfo`, `nvtop`, `radentop` do not show any information about the GPU, but before installing they did.
When I try to install amdgpu-dkms with either apt or amdgPU-installer it fails

Update:
At least managed to make it work with kernel 6.10.10, seems that amdgpu-dkms creates a blacklist file for amdgpu packages until it finishes installing, so it was never removed. Installing with `--no-dkms` and making sure there is no blacklist `sudo rm /etc/modprobe.d/blacklist-amdgpu.conf` works

Update 2:
Just for reference, current issue with installing `amdgpu-dkms` in 6.10.10 is this error 
```
In file included from ./include/trace/trace_events.h:419,
                 from ./include/trace/define_trace.h:102,
                 from /tmp/amd.3Qk44PwX/scheduler/gpu_scheduler_trace.h:114,
                 from /tmp/amd.3Qk44PwX/scheduler/sched_main.c:88:
/tmp/amd.3Qk44PwX/scheduler/./gpu_scheduler_trace.h:60:1: error: macro "__assign_str" passed 2 arguments, but takes just 1
   60 | );
      | ^~
In file included from ./include/trace/trace_events.h:375:
./include/trace/stages/stage6_event_callback.h:34:9: note: macro "__assign_str" defined here
   34 | #define __assign_str(dst)                                               \
      |         ^~~~~~~~~~~~
  CC [M]  /tmp/amd.3Qk44PwX/amd/amdgpu/amdgpu_device.o
/tmp/amd.3Qk44PwX/scheduler/./gpu_scheduler_trace.h: In function ‘trace_event_raw_event_drm_sched_job’:
/tmp/amd.3Qk44PwX/scheduler/./gpu_scheduler_trace.h:51:28: error: ‘__assign_str’ undeclared (first use in this function)
   51 |                            __assign_str(name, sched_job->sched->name);
      |                            ^~~~~~~~~~~~
./include/trace/trace_events.h:402:11: note: in definition of macro ‘DECLARE_EVENT_CLASS’
  402 |         { assign; }                                                     \
      |           ^~~~~~
/tmp/amd.3Qk44PwX/scheduler/./gpu_scheduler_trace.h:47:13: note: in expansion of macro ‘TP_fast_assign’
   47 |             TP_fast_assign(
      |             ^~~~~~~~~~~~~~
/tmp/amd.3Qk44PwX/scheduler/./gpu_scheduler_trace.h:51:28: note: each undeclared identifier is reported only once for each function it appears in
   51 |                            __assign_str(name, sched_job->sched->name);
      |                            ^~~~~~~~~~~~
```
Not sure if I should open a separate issue to report this

---

### 评论 #7 — harkgill-amd (2024-09-23T20:00:25Z)

@curvedinf a fix for this issue is present in the latest ROCm 6.2.1 release. Could you please give it a try and confirm if you're issue has been resolved?

---

### 评论 #8 — harkgill-amd (2024-10-08T14:11:42Z)

Hi @curvedinf, I will close out this ticket for now as the fix has been confirmed to resolve the flashing desktop issue in ROCm 6.2.1. If you encounter this issue with ROCm 6.2.1+, please leave a comment and I will re-open this ticket. Thanks!

---
