# [Issue]: When the AMD 7840HS GPU crashes, how do I diagnose what is going wrong?

> **Issue #5180**
> **状态**: open
> **创建时间**: 2025-08-11T20:34:05Z
> **更新时间**: 2026-03-04T14:50:26Z
> **作者**: jcdutton
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5180

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU: 
model name	: AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
GPU:
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Name:                    gfx1103                            
  Marketing Name:          AMD Radeon 780M                    
      Name:                    amdgcn-amd-amdhsa--gfx1103         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   


When the AMD 7840HS GPU crashes, how do I diagnose what is going wrong?
I have a simple program that multiplies 2 matrix together using rocblas cgemm.
I can run up to 30000 x 30000 OK, but when I get to 50000 x 50000 the GPU crashes.
I have set the gtt/ttm to be 60 GBytes, and the 50000 x 50000 sits at about 58 GB when viewed on amdgpu_top.
When it crashes, the display goes blank for about 60 seconds, but then recovers and works again, without any applications exiting.
I have compiled rocm from source, probably most recent git version, with gfx1103 as the target.
I don't mind if it is officially supported or not on the gfx1103. I wish to track down the cause and fix it.
Please can you point me to some instruction on how to diagnose the problem on the GPU ?

Note rocm 6.3.1 completed the 50000 x 50000 OK.
rocm 6.3.3 failed.
rocm 6.4.1 failed.
rocm 7.rcX failed.

An example program to reproduce the problem is here:
git@github.com:jcdutton/rocm-rust.git


### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 7 7840HS w/ Radeon 780M Graphics

### GPU

AMD Ryzen 7 7840HS w/ Radeon 780M Graphics

### ROCm Version

Latest git version. Probably version 7rc something.

### ROCm Component

rocBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (17 条)

### 评论 #1 — darren-amd (2025-08-12T19:33:24Z)

Hi @jcdutton,

Thanks for reporting the issue. As you mentioned, we don't officially support gfx1103 on ROCm, however I'd recommend trying TheRock which does have support and seeing if the issue persists there (https://github.com/ROCm/TheRock). If it does then I would recommend you open a ticket there for further support. You could also try running with `AMD_LOG_LEVEL=7` which could reveal more about the issue you are facing. 

---

### 评论 #2 — jcdutton (2025-08-12T21:20:06Z)

With AMD_LOG_LEVEL=7
For a working 10000 x 10000 matrix mult:
Good with 10000 x 10000
```
Start sync -------------------
:3:hip_device_runtime.cpp   :667 : 48408751212 us: [pid:77513 tid: 0x7f0bd3392640]  hipDeviceSynchronize (  ) 
:4:commandqueue.cpp         :183 : 48408751216 us: [pid:77513 tid: 0x7f0bd3392640] Marker queued to 0x564331800a90 for finish
:4:command.cpp              :357 : 48408751219 us: [pid:77513 tid: 0x7f0bd3392640] Command (InternalMarker) enqueued: 0x564333fef350 to queue: 0x564331800a90
:3:rocvirtual.cpp           :551 : 48408751240 us: [pid:77513 tid: 0x7f0bd3392640] Set Handler: handle(0x7f0bc15fd600), timestamp(0x564333fe6260)
:4:rocvirtual.cpp           :1260: 48408751245 us: [pid:77513 tid: 0x7f0bd3392640] SWq=0x7f0bd1848000, HWq=0x7f0ab9c00000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7f0bc15fd600, rptr=0, wptr=1
:4:commandqueue.cpp         :209 : 48413403687 us: [pid:77513 tid: 0x7f0bd3392640] All commands finished for host queue : 0x564331800a90
:3:hip_device_runtime.cpp   :671 : 48413403702 us: [pid:77513 tid: 0x7f0bd3392640] hipDeviceSynchronize: Returned hipSuccess : 
hipSyncError: 0
End sync -------------------

```

For a failing 50000 x 50000
```
Start sync -------------------
:3:hip_device_runtime.cpp   :667 : 48514917689 us: [pid:77544 tid: 0x7fd5bfa8d640]  hipDeviceSynchronize (  ) 
:4:commandqueue.cpp         :183 : 48514917705 us: [pid:77544 tid: 0x7fd5bfa8d640] Marker queued to 0x5639ebc5da90 for finish
:4:command.cpp              :357 : 48514917711 us: [pid:77544 tid: 0x7fd5bfa8d640] Command (InternalMarker) enqueued: 0x5639ee47d1e0 to queue: 0x5639ebc5da90
:3:rocvirtual.cpp           :551 : 48514917763 us: [pid:77544 tid: 0x7fd5bfa8d640] Set Handler: handle(0x7fd5af7fd600), timestamp(0x5639ee2f81f0)
:4:rocvirtual.cpp           :1260: 48514917772 us: [pid:77544 tid: 0x7fd5bfa8d640] SWq=0x7fd5bfa36000, HWq=0x7fc6a5000000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7fd5af7fd600, rptr=0, wptr=1
:1:rocdevice.cpp            :3438: 48517558015 us: [pid:77544 tid: 0x7fd5af5ff6c0] HW Exception Error
:3:rocvirtual.hpp           :80  : 48517561884 us: [pid:77544 tid: 0x7fd5bfa8d640] Device not Stable, while waiting for Signal =(0x7fd5af7fd600) for 4000000 ns
:4:commandqueue.cpp         :209 : 48517561904 us: [pid:77544 tid: 0x7fd5bfa8d640] All commands finished for host queue : 0x5639ebc5da90
:3:hip_device_runtime.cpp   :671 : 48517561912 us: [pid:77544 tid: 0x7fd5bfa8d640] hipDeviceSynchronize: Returned hipErrorLaunchFailure : 
hipSyncError: 719
:3:hip_module.cpp           :47  : 48517562042 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562047 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562052 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562055 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562063 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562067 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562071 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562076 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562081 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562087 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562094 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562099 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562103 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562107 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562112 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562115 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562119 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562122 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562126 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562129 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562133 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562138 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562141 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562145 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562148 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562152 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562156 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562159 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562162 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562166 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562169 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562173 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562176 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562180 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562184 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562187 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562191 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562195 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562198 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562201 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562205 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562208 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562211 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562215 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562218 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562222 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562226 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562231 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562234 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562238 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562242 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562244 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562248 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562252 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:hip_module.cpp           :47  : 48517562256 us: [pid:77544 tid: 0x7fd5bfa8d640] hipModuleUnload: Returned hipErrorLaunchFailure : 
:3:rocvirtual.hpp           :63  : 48517596268 us: [pid:77544 tid: 0x7fd5bfa8d640] Host active wait for Signal = (0x7fd5af7fd600) for 100000 ns
:3:rocvirtual.hpp           :68  : 48517596383 us: [pid:77544 tid: 0x7fd5bfa8d640] Device not Stable, while waiting for Signal =(0x7fd5af7fd600) for 100000 ns
:4:rocdevice.cpp            :2304: 48517596391 us: [pid:77544 tid: 0x7fd5bfa8d640] Free hsa memory (nil)
:3:rocdevice.cpp            :3173: 48517596394 us: [pid:77544 tid: 0x7fd5bfa8d640] releaseQueue refCount:0x7fc6a5000000 (0)
:4:rocdevice.cpp            :2304: 48517597539 us: [pid:77544 tid: 0x7fd5bfa8d640] Free hsa memory 0x7fc6a4800000
:4:rocdevice.cpp            :2304: 48517597969 us: [pid:77544 tid: 0x7fd5bfa8d640] Free hsa memory 0x7fc6a4200000
:4:rocvirtual.cpp           :633 : 48517597974 us: [pid:77544 tid: 0x7fd5bfa8d640] Host wait on completion_signal=0x7fd5af7fd600
:3:rocvirtual.hpp           :80  : 48517601979 us: [pid:77544 tid: 0x7fd5bfa8d640] Device not Stable, while waiting for Signal =(0x7fd5af7fd600) for 4000000 ns
:4:rocdevice.cpp            :2304: 48517602095 us: [pid:77544 tid: 0x7fd5bfa8d640] Free hsa memory 0x7fd4ade00000
:4:rocdevice.cpp            :2304: 48517602132 us: [pid:77544 tid: 0x7fd5bfa8d640] Free hsa memory 0x7fd5c2ecc000
:3:rocdevice.cpp            :286 : 48517602137 us: [pid:77544 tid: 0x7fd5bfa8d640] Deleting hardware queue 0x7fc6a5000000 with refCount 0

```

---

### 评论 #3 — darren-amd (2025-08-14T17:33:15Z)

Hi @jcdutton,

Thanks for providing the logs above. Did you have a chance to try TheRock and see if the issue persists there? 

---

### 评论 #4 — jcdutton (2025-08-14T17:55:33Z)

Hi.
I was doing all the tests on TheRock. I found it is pretty much impossible to compile ROCm without it.

From the logs, the first thing that is different between the OK and the FAILED runs is:
HW Exception Error

Is there anything I can do to find out more why or even where, which line of code, caused the exception.

Note: The same crash happens when using the pre-compiled binaries from here:
https://repo.radeon.com/rocm/apt/6.4.1



---

### 评论 #5 — darren-amd (2025-08-14T18:15:49Z)

Hi @jcdutton,

Thanks for the update, in that case I'd recommend opening a ticket in TheRock repository for further assistance (https://github.com/ROCm/TheRock). In the meantime, I'd suggesting taking a look at the `dmesg` logs around the time of the failure (Please also attach this to the new ticket). That should give more insight on the failure point. 

---

### 评论 #6 — jcdutton (2025-08-15T12:12:40Z)

What is the relationship between ROCm and TheRock ?  I thought TheRock is only a build environment for ROCm which is why I came here with questions.


Here is the dmesg logs during the crash:
```
2025-08-10T19:55:33.635860+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
2025-08-10T19:55:33.637490+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
2025-08-10T19:55:33.637492+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
2025-08-10T19:55:33.637494+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: Failed to evict queue 1
2025-08-10T19:55:33.637494+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: GPU reset begin! 
2025-08-10T19:55:33.637495+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: Failed to evict process queues
2025-08-10T19:55:33.637495+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: Dumping IP State
2025-08-10T19:55:33.637496+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: Dumping IP State Completed
2025-08-10T19:55:35.653664+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
2025-08-10T19:55:35.653676+01:00 hostname kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
2025-08-10T19:55:37.657712+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
2025-08-10T19:55:37.657811+01:00 hostname kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
2025-08-10T19:55:37.661682+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: MODE2 reset
2025-08-10T19:55:37.689695+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: GPU reset succeeded, trying to resume
2025-08-10T19:55:37.689705+01:00 hostname kernel: [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
2025-08-10T19:55:37.689707+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
2025-08-10T19:55:37.689707+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: [drm] Check your /sys/class/drm/card0/device/devcoredump/data
2025-08-10T19:55:37.689708+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
2025-08-10T19:55:37.693688+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
2025-08-10T19:55:37.697695+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005000
2025-08-10T19:55:38.037721+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0 
2025-08-10T19:55:38.037746+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0 
2025-08-10T19:55:38.037747+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
2025-08-10T19:55:38.037750+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0 
2025-08-10T19:55:38.037751+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
2025-08-10T19:55:38.037752+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
2025-08-10T19:55:38.037752+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
2025-08-10T19:55:38.037753+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
2025-08-10T19:55:38.037754+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
2025-08-10T19:55:38.037754+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
2025-08-10T19:55:38.037755+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
2025-08-10T19:55:38.037755+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
2025-08-10T19:55:38.037756+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
2025-08-10T19:55:38.037756+01:00 hostname kernel: amdgpu 0000:c1:00.0: amdgpu: GPU reset(2) succeeded!
2025-08-10T19:55:38.037757+01:00 hostname kernel: amdgpu 0000:c1:00.0: [drm] device wedged, but recovered through reset

```

---

### 评论 #7 — jcdutton (2025-08-17T10:48:44Z)

I have found something more.
Previously, as per the example linked to above.
I used hipMalloc  to allocate the 50000 x 50000 matrix.
I then did the calculation on the 50000 x 50000 matrix.
That results in the crash.
If I instead hipMalloc that size + 512. I.e. a 50512 x 50512, but then only do the calculation on the 50000 x 50000 matrix, it actually works, and completes.
This therefore points to a buffer overflow bug somewhere in the ROCm software.
While I have all the debugging tools I need when debugging x86 software, I don't know what to use to identify the line of GPU code that is causing this buffer overflow.

So, that is essentially all I need. What methods or tools do I use to debug this GPU ROCm software bug?


---

### 评论 #8 — jcdutton (2025-09-20T09:15:36Z)

I have a way to reliably reproduce this.
I have a Framework 16 laptop with 64GB RAM that has the "AMD Ryzen 7 7840HS w/ Radeon 780M Graphics". I am guessing any laptop with the same CPU will hopefully reproduce this problem.
Use ROCM 7.0.1 from "https://repo.radeon.com/rocm/apt/7.0.1"
checkout this git repo for a test program to reproduce the problem:
Using linux kernel 6.16.5 from mainline.
Get the example test program:
git clone https://github.com/jcdutton/rocm-rust.git

Copy a file with the following content to /etc/modprobe.d:
```
options amdgpu gttsize=60000 #in MB
options ttm pages_limit=15728640 #4k per page, 60GB total
options ttm page_pool_size=15728640 

```

This makes the gttsize / ttm size 60GB.
You need to reboot for the settings to take affect.

I have tried gttsize / ttm with different sizes, e.g. 30GB and a smaller matrix size, but can only reproduce it with the 60GB gttsize vs 64GB total RAM. So, the having 64GB RAM in the laptop is also important.

Run the example program (written in rust) from the above git repo.

do:
```
cargo build
export HSA_OVERRIDE_GFX_VERSION=11.0.0
./target/debug/rocm-rust 50000
```
After a long while while it tries to calculated a 50000 x 50000 matrix multiply. It will fail with:
```
init done
status of create_handle: 0
handle: 0x5603fd821a40 
46 42 41 40 00 00 40 40 
46 42 41 40 00 00 40 40 
matrix rows: 50000 cols: 50000 size: 2500000000 ram: 20000 MB
hipMalloc1: 0
hipMalloc2: 0
hipMalloc3: 0
Matrix A (input): 
2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 
00 00 00 40 00 00 00 00 
Matrix B (input): 
2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 
00 00 00 40 00 00 00 00 
Matrix C (input): 
0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 
elem_size for a complex f32: 8
elem_size for cgemm: 8
matrix rows: 50000 cols: 50000 size: 2500000000 ram: 20000 MB
Start calc1 -------------------
End calc1 -------------------
Start sync -------------------
hipSyncError: 719


```

A successful run with a 49999 x 49999 matrix does this:
```
./target/debug/rocm-rust 49999
init done
status of create_handle: 0
handle: 0x5628fb17fa40 
46 42 41 40 00 00 40 40 
46 42 41 40 00 00 40 40 
matrix rows: 49999 cols: 49999 size: 2499900001 ram: 19999.2 MB
hipMalloc1: 0
hipMalloc2: 0
hipMalloc3: 0
Matrix A (input): 
2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 
00 00 00 40 00 00 00 00 
Matrix B (input): 
2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 2+0i 
00 00 00 40 00 00 00 00 
Matrix C (input): 
0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 0+0i 
elem_size for a complex f32: 8
elem_size for cgemm: 8
matrix rows: 49999 cols: 49999 size: 2499900001 ram: 19999.2 MB
Start calc1 -------------------
End calc1 -------------------
Start sync -------------------
hipSyncError: 0
End sync -------------------
Start get results -------------------
End get results -------------------
199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 199996+0i 
calc1:       148.755787ms
sync:        1191.625183923s

```
It takes about 20 minutes to run the 49999 x 49999 matrix case.

Hopefully this is enough for someone at AMD to reproduce the problem and find a fix.
Note: I think this bug is also preventing some ML models from running on this APU.
e.g. whisper   audio to text conversion.

Also, if one hipalloc 50512 x 50512 matrix, but then only calculated a 50000 x 50000 matrix, it works and completes OK.
So, this is a bug with regards to memory allocation, maybe GPU accessing memory outside that allocation when running the blas cgemm task.


---

### 评论 #9 — jcdutton (2025-09-20T12:49:30Z)

Some more information. If I use runlevel 3 (no GUI, just text console)  the 50000 x 50000 matrix multiply completes.
I have disabled OOM and overcommit with "vm.overcommit_memory = 2".
While running the "rocm-rust 50000", if I also open a non-rocm application that needs more memory, rather than that application failing due to failed malloc requests, the rocm application dies with the usual "amdgpu: MES failed to respond to msg=REMOVE_QUEUE".
So, there is probably a malloc failing silently somewhere, and rocm not dealing with it gracefully.


---

### 评论 #10 — jcdutton (2025-09-20T13:14:19Z)

After trying   "amdgpu.mcbp=0" A newer dmesg output, in case it helps:
```
[  267.026861] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State
[  267.027339] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State Completed
[  267.027406] amdgpu 0000:c1:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[  267.027408] amdgpu 0000:c1:00.0: amdgpu: [drm] Check your /sys/class/drm/card0/device/devcoredump/data
[  267.037414] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 timeout, signaled seq=522, emitted seq=523
[  267.037418] amdgpu 0000:c1:00.0: amdgpu: Process information: process Xorg pid 2788 thread Xorg:cs0 pid 2842
[  267.037420] amdgpu 0000:c1:00.0: amdgpu: Starting comp_1.1.0 ring reset
[  267.037453] amdgpu 0000:c1:00.0: amdgpu: reset compute queue (1:1:0)
[  267.242688] amdgpu 0000:c1:00.0: amdgpu: Ring comp_1.1.0 reset failed
[  267.242692] amdgpu 0000:c1:00.0: amdgpu: GPU reset begin!
[  267.242725] amdgpu 0000:c1:00.0: amdgpu: Failed to evict queue 1
[  267.242729] amdgpu 0000:c1:00.0: amdgpu: Failed to evict queue 0
[  267.242732] amdgpu: Failed to suspend process pid 5161
[  267.275734] amdgpu 0000:c1:00.0: amdgpu: MODE2 reset
[  267.305949] amdgpu 0000:c1:00.0: amdgpu: GPU reset succeeded, trying to resume
[  267.306363] [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
[  267.306441] amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
[  267.308891] amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
[  267.309751] amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER)
[  267.309756] [drm:amdgpu_mes_set_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
[  267.314852] amdgpu 0000:c1:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005300
[  267.932920] amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  267.932927] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  267.932929] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  267.932931] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  267.932933] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  267.932934] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  267.932936] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  267.932937] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  267.932939] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  267.932941] amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  267.932942] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  267.932944] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[  267.932946] amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  267.935504] amdgpu 0000:c1:00.0: amdgpu: GPU reset(1) succeeded!
[  267.935518] amdgpu 0000:c1:00.0: [drm] device wedged, but recovered through reset
[  267.944834] [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!

```

---

### 评论 #11 — jcdutton (2025-10-08T16:26:07Z)

We found something that helps.
I can confirm that “amdgpu.cwsr_enable=0" helps.
After a new reboot.
my “rocm-rust 50000” test program crashes amdgpu the first time one runs it after rebooting, but then, after that, it succeeds each time.
Without the “amdgpu.cwsr_enable=0" it fails every time.

Some more details here:
https://github.com/ROCm/TheRock/issues/1264


---

### 评论 #12 — zw963 (2025-12-10T12:50:45Z)

Set `amdgpu.cwsr_enable=0` works for me, I run gemma3n locally for translate, use 100% GPU 780M,  it happen `MES failed to respond to msg=REMOVE_QUEUE + GPU reset` frequently before disable CWSR.

I even test on following two edge linux kernel, not work.

```
linux-amd-drm-fixes 6.18.2025.11.26-1
linux-amd-drm-next 6.19.2025.12.02-1
```

After this hack, I can translate many long blog post (MES failed and GPU reset happen very frequently if translate on long post before) but never GPU reset, with `linux-xanmod 6.17.11`.

I test on Arch linux latest use `ollama + gemini3n`, following is my package version:

```
 ╰──➤ $ pacman -Q |grep 'rocm'
ollama-rocm 0.13.1-1
python-pytorch-rocm 2.9.1-5
rocm-cmake 7.1.1-1
rocm-core 7.1.1-1
rocm-device-libs 2:7.1.1-1
rocm-hip-libraries 7.1.1-1
rocm-hip-runtime 7.1.1-1
rocm-hip-sdk 7.1.1-1
rocm-language-runtime 7.1.1-1
rocm-llvm 2:7.1.1-1
rocm-opencl-runtime 7.1.1-1
rocm-opencl-sdk 7.1.1-1
rocm-smi-lib 7.1.1-1
rocminfo 7.1.1-1
```

```
 ╰──➤ $ uname -a
Linux mingfan 6.17.11-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Sun, 07 Dec 2025 21:10:38 +0000 x86_64 GNU/Linux
```

```
 ╰──➤ $ \cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap sysrq_always_enabled=1 amdgpu.cwsr_enable=0 amdgpu.gpu_recovery=1 initrd=\boot\initramfs-linux-xanmod.img
```

```
 ╰──➤ $ ollama ps
NAME              ID              SIZE      PROCESSOR    CONTEXT    UNTIL
gemma3n:latest    15cb39fd9394    8.3 GB    100% GPU     4096       Forever
```

```service
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
# Environment="OLLAMA_NUM_GPU=0"
# Environment="OLLAMA_CONTEXT_LENGTH=2048"
Environment="OLLAMA_KEEP_ALIVE=-1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_QUEUE=1"
Environment="OLLAMA_FLASH_ATTENTION=1"
ExecStart=/usr/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

---

### 评论 #13 — zw963 (2025-12-17T10:08:24Z)

I saw Arch linux release 6.18.1 kernel,  so tested on it WITHOUT set `amdgpu.cwsr_enable=0`,  but still meet MES hung issue.

```
[   25.939312] logitech-hidpp-device 0003:046D:406B.0007: HID++ 4.5 device connected.
[  811.414674] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[  811.414680] amdgpu 0000:c5:00.0: amdgpu: failed to suspend all gangs
[  811.414682] amdgpu 0000:c5:00.0: amdgpu: failed to suspend gangs from MES
[  811.414684] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  811.414687] amdgpu 0000:c5:00.0: amdgpu: Suspending all queues failed
[  811.414689] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[  811.414720] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[  811.417091] amdgpu 0000:c5:00.0: amdgpu: Failed to restore queue 5
[  811.417095] amdgpu 0000:c5:00.0: amdgpu: Failed to restore process queues
[  811.729514] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 5 for dev 20553
[  811.729557] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[  811.731525] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[  813.831549] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  813.831556] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[  814.039051] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[  814.040578] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[  814.072257] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[  814.072949] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[  814.073058] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[  814.073060] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[  814.073062] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[  814.073959] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[  814.080610] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005400
[  814.202913] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  814.202922] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  814.202925] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  814.202927] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  814.202928] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  814.202930] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  814.202931] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  814.202933] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  814.202934] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  814.202936] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  814.202938] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  814.202939] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[  814.202941] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  814.205285] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[  814.205298] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[  814.252360] amdgpu: Freeing queue vital buffer 0x7f16e5800000, queue evicted
[  814.252365] amdgpu: Freeing queue vital buffer 0x7f16e6800000, queue evicted
[  814.252367] amdgpu: Freeing queue vital buffer 0x7f172a400000, queue evicted
[  814.252369] amdgpu: Freeing queue vital buffer 0x7f197c800000, queue evicted
[  814.252371] amdgpu: Freeing queue vital buffer 0x7f197d800000, queue evicted
[  814.276836] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  814.276846] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1202
[  814.276851] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  814.276860] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 3
[  814.276886] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[  814.276944] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 1
[  814.276948] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[  814.276977] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[  814.277766] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[  814.372424] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[  814.405501] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[  814.406005] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
```

Following is the related packages.

```
linux 6.18.1.arch1-2
linux-amd-drm-fixes 6.19.2025.12.11-1
linux-amd-drm-fixes-headers 6.19.2025.12.11-1
linux-amd-drm-next 6.19.2025.12.02-1
linux-amd-drm-next-headers 6.19.2025.12.02-1
linux-api-headers 6.17-1
linux-firmware 20251125-2
linux-firmware-amdgpu 20251125-2
linux-firmware-atheros 20251125-2
linux-firmware-broadcom 20251125-2
linux-firmware-cirrus 20251125-2
linux-firmware-intel 20251125-2
linux-firmware-mediatek 20251125-2
linux-firmware-nvidia 20251125-2
linux-firmware-other 20251125-2
linux-firmware-radeon 20251125-2
linux-firmware-realtek 20251125-2
linux-firmware-whence 20251125-2
linux-headers 6.18.1.arch1-2
```

```
╰──➤ $ 130  uname -a
Linux mingfan 6.18.1-arch1-2 #1 SMP PREEMPT_DYNAMIC Sat, 13 Dec 2025 18:23:21 +0000 x86_64 GNU/Linux
```

```
 ╰──➤ $ pacman -Q |grep rocm
ollama-rocm 0.13.4-1
python-pytorch-rocm 2.9.1-6
rocm-cmake 7.1.1-1
rocm-core 7.1.1-1
rocm-device-libs 2:7.1.1-1
rocm-hip-libraries 7.1.1-1
rocm-hip-runtime 7.1.1-1
rocm-hip-sdk 7.1.1-1
rocm-language-runtime 7.1.1-1
rocm-llvm 2:7.1.1-1
rocm-opencl-runtime 7.1.1-1
rocm-opencl-sdk 7.1.1-1
rocm-smi-lib 7.1.1-1
rocminfo 7.1.1-1
```

Thanks

---

### 评论 #14 — zw963 (2025-12-30T15:30:58Z)

 I use Arch linux,  , with following `amd-drm-fixes` kernel (6.19) WITHOUT `cwsr_enable=0` hack.


```
Linux mingfan 6.19.0-rc1-1-amd-drm-fixes-g969faea4e9d0 #1 SMP PREEMPT_DYNAMIC Wed, 17 Dec 2025 21:57:13 +0000 x86_64 GNU/Linux
```

I can still reproduce MES failing issue use this new patched kernal (Although, it happen rarely compare to the main-stream kernel)

<details>
<summary>dmesg log</summary>

```
[86254.411250] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[86254.412954] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[86254.413000] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[86254.413002] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[86254.413003] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 timeout, signaled seq=6970, emitted seq=6971
[86254.413007] amdgpu 0000:c5:00.0: amdgpu:  Process gnome-shell pid 1433 thread gnome-shel:cs0 pid 1464
[86254.413009] amdgpu 0000:c5:00.0: amdgpu: Starting comp_1.3.0 ring reset
[86254.712544] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[86254.712550] amdgpu 0000:c5:00.0: amdgpu: failed to suspend all gangs
[86254.712552] amdgpu 0000:c5:00.0: amdgpu: failed to suspend gangs from MES
[86254.712554] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[86254.712557] amdgpu 0000:c5:00.0: amdgpu: Suspending all queues failed
[86254.712559] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[86254.712560] amdgpu: Failed to quiesce KFD
[86255.041177] amdgpu 0000:c5:00.0: amdgpu: reset compute queue (1:3:0)
[86255.249756] amdgpu 0000:c5:00.0: amdgpu: Ring comp_1.3.0 reset failed
[86255.249762] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  1
[86257.898714] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[86257.898719] amdgpu 0000:c5:00.0: amdgpu: failed to suspend all gangs
[86257.898723] amdgpu 0000:c5:00.0: amdgpu: failed to suspend gangs from MES
[86257.898724] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[86257.898727] amdgpu 0000:c5:00.0: amdgpu: Suspending all queues failed
[86257.898729] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[86257.898731] amdgpu: Failed to quiesce KFD
[86257.898738] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 5 for dev 22192
[86260.677546] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[86260.677552] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[86263.232472] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[86263.232478] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[86263.234021] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[86263.265252] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[86263.265717] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[86263.265799] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[86263.266843] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[86263.272849] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005400
[86263.418490] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[86263.418497] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[86263.418498] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[86263.418500] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[86263.418501] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[86263.418502] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[86263.418504] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[86263.418505] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[86263.418507] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[86263.418508] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[86263.418510] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[86263.418512] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[86263.418513] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[86263.420582] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[86263.420594] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[86263.494491] amdgpu 0000:c5:00.0: amdgpu: [drm] *ERROR* Failed to initialize parser -125!
[86267.094795] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[86267.094800] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1202
[86267.094802] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[86267.094807] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 4
[86267.094813] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[86267.094879] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 2
[86267.094880] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 1
[86267.094882] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[86267.094907] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[86267.097355] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[86267.186371] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[86267.218204] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[86267.218718] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[86267.218814] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[86267.218831] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[86267.218847] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[86267.219770] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
```

</details>


<details>
<summary>package version</summary>

```
 ╰──➤ $ 1  pacman -Q |grep 'rocm\|amd'
amd-ucode 20251125-2
amdgpu_top-git 0.11.0.r18.g7b35143-1
hip-runtime-amd 7.1.1-1
lib32-vulkan-amdgpu-pro 25.10_2202160-1
linux-amd-drm-fixes 6.19.2025.12.17-1
linux-amd-drm-fixes-headers 6.19.2025.12.17-1
linux-amd-drm-next 6.19.2025.12.02-1
linux-amd-drm-next-headers 6.19.2025.12.02-1
linux-firmware-amdgpu 20251125-2
ollama-rocm 0.13.5-1
python-pytorch-rocm 2.9.1-6
rocm-cmake 7.1.1-1
rocm-core 7.1.1-1
rocm-device-libs 2:7.1.1-2
rocm-hip-libraries 7.1.1-1
rocm-hip-runtime 7.1.1-1
rocm-hip-sdk 7.1.1-1
rocm-language-runtime 7.1.1-1
rocm-llvm 2:7.1.1-2
rocm-opencl-runtime 7.1.1-1
rocm-opencl-sdk 7.1.1-1
rocm-smi-lib 7.1.1-1
rocminfo 7.1.1-1
vulkan-amdgpu-pro 25.10_2202160-1
xf86-video-amdgpu 25.0.0-1
```

</details>



<details>
<summary>rocminfo</summary>

```
 ╰──➤ $ rocminfo
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.14
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5137
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    49112548(0x2ed65e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49112548(0x2ed65e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49112548(0x2ed65e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    49112548(0x2ed65e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1103
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon 780M Graphics
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      2048(0x800) KB
  Chip ID:                 5567(0x15bf)
  ASIC Revision:           7(0x7)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2700
  BDFID:                   50432
  Internal Node ID:        1
  Compute Unit:            12
  SIMDs per CU:            2
  Shader Engines:          1
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 67
  SDMA engine uCode::      23
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    24556272(0x176b2f0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24556272(0x176b2f0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1103
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*******
Agent 3
*******
  Name:                    aie2
  Uuid:                    AIE-XX
  Marketing Name:          AIE-ML
  Vendor Name:             AMD
  Feature:                 AGENT_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        1(0x1)
  Queue Min Size:          64(0x40)
  Queue Max Size:          64(0x40)
  Queue Type:              SINGLE
  Node:                    0
  Device Type:             DSP
  Cache Info:
    L2:                      2048(0x800) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          0(0x0)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            0
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:0
  Memory Properties:
  Features:                AGENT_DISPATCH
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    49112548(0x2ed65e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65536(0x10000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    49112548(0x2ed65e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
```

</details>



---

### 评论 #15 — zw963 (2026-01-06T16:20:58Z)

Happen again, same env as my previous reply.

```
[107000.403601] overlayfs: upper fs does not support file handles, falling back to index=off.
[107000.403607] overlayfs: fs on '/home/zw963/.local/share/containers/storage/overlay/compat424659714/lower1' does not support file handles, falling back to xino=off.
[107000.592860] overlayfs: upper fs does not support file handles, falling back to index=off.
[107000.592870] overlayfs: fs on '/home/zw963/.local/share/containers/storage/overlay/metacopy-check4262026626/l1' does not support file handles, falling back to xino=off.
[107000.599775] overlayfs: upper fs does not support file handles, falling back to index=off.
[107000.599783] overlayfs: fs on '/home/zw963/.local/share/containers/storage/overlay/opaque-bug-check1750751682/l2' does not support file handles, falling back to xino=off.
[107001.184187] overlayfs: upper fs does not support file handles, falling back to index=off.
[107001.184193] overlayfs: fs on '/run/user/1000/libpod/tmp/infra-container' does not support file handles, falling back to xino=off.
[107001.202850] tun: Universal TUN/TAP device driver, 1.6
[107001.276661] overlayfs: upper fs does not support file handles, falling back to index=off.
[107001.276665] overlayfs: fs on '/home/zw963/.local/share/containers/storage/overlay/l/4RNZ2JQAINX7ROIT5XDHNDOIVE' does not support file handles, falling back to xino=off.
[107001.322416] overlayfs: upper fs does not support file handles, falling back to index=off.
[107001.322420] overlayfs: fs on '/home/zw963/.local/share/containers/storage/overlay/l/DXFPHGHUUGOI6ENIARBNVP2WFT' does not support file handles, falling back to xino=off.
[110526.231997] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[110526.232003] amdgpu 0000:c5:00.0: amdgpu: failed to suspend all gangs
[110526.232005] amdgpu 0000:c5:00.0: amdgpu: failed to suspend gangs from MES
[110526.232007] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[110526.232011] amdgpu 0000:c5:00.0: amdgpu: Suspending all queues failed
[110526.232013] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[110526.232015] amdgpu: Failed to quiesce KFD
[110526.232020] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[110526.232040] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 5 for dev 22192
[110526.232077] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[110526.233804] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[110526.561636] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[110526.594391] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[110526.594945] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[110526.595106] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[110526.595109] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[110526.595112] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[110526.595962] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[110526.601872] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005400
[110526.747653] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[110526.747660] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[110526.747662] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[110526.747663] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[110526.747665] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[110526.747666] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[110526.747668] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[110526.747669] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[110526.747671] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[110526.747673] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[110526.747675] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[110526.747677] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[110526.747678] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[110526.749783] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[110526.749802] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[110529.680168] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[110529.680173] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1202
[110529.680175] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[110529.680179] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 4
[110529.680199] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[110529.680240] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 2
[110529.680242] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 1
[110529.680243] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[110529.680264] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[110529.682516] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[110529.782348] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[110529.815180] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[110529.815716] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[110529.815817] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[110529.815828] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[110529.815838] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[110529.816798] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[110529.822705] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005400
[110530.344672] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[110530.344678] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[110530.344681] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[110530.344683] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[110530.344685] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[110530.344687] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[110530.344689] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[110530.344690] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[110530.344693] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[110530.344695] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[110530.344697] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[110530.344699] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[110530.344701] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[110530.346931] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[110530.346954] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
```

---

### 评论 #16 — zw963 (2026-02-23T18:07:02Z)

MES hang issue fixed on my 780M, I use Arch linux, following is my package version:

```
 ╰──➤ $ pacman -Q |grep 'rocm\|amd'
amd-ucode 20260110-1
amdgpu_top 0.11.2-1
hip-runtime-amd 7.2.0-1
lib32-vulkan-amdgpu-pro 25.10_2202160-1
linux-amd-drm-fixes 6.19.2026.02.05-1
linux-amd-drm-fixes-headers 6.19.2026.02.05-1
linux-firmware-amdgpu 20260110-1
ollama-rocm 0.17.0-1
python-pytorch-rocm 2.10.0-2
python-torchaudio-rocm 2.10.0-3
rocm-cmake 7.2.0-1
rocm-core 7.2.0-2
rocm-device-libs 2:7.2.0-1
rocm-hip-libraries 7.2.0-1
rocm-hip-runtime 7.2.0-1
rocm-hip-sdk 7.2.0-1
rocm-language-runtime 7.2.0-1
rocm-llvm 2:7.2.0-1
rocm-opencl-runtime 7.2.0-1
rocm-opencl-sdk 7.2.0-1
rocm-smi-lib 7.2.0-1
rocminfo 7.2.0-1
vulkan-amdgpu-pro 25.10_2202160-1
xf86-video-amdgpu 25.0.0-1
```

```
 ╰──➤ $ uname -a
Linux mingfan 6.18.13-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Fri, 20 Feb 2026 05:25:15 +0000 x86_64 GNU/Linux
```

```
 ╰──➤ $ \cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap zswap.enabled=0 sysrq_always_enabled=1 amdgpu.gpu_recovery=1 amdgpu.gttsize=24576 ttm.pages_limit=6291456 initrd=\boot\initramfs-linux-xanmod.img
```

---

### 评论 #17 — zw963 (2026-03-04T14:50:26Z)

probably still not fixed?

```
[73314.889668] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73314.889675] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[73314.889677] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73314.889681] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[73314.889682] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[73314.889684] amdgpu: Failed to quiesce KFD
[73314.889701] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73314.891684] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 49700
[73314.891708] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73314.893432] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73316.994500] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73316.994507] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.998481] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73318.998487] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.999856] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73319.031470] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73319.031938] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73319.032193] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73319.032198] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73319.032202] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73319.033702] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73319.039404] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73319.185138] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73319.185150] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73319.185153] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73319.185155] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73319.185157] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73319.185158] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73319.185160] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73319.185162] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73319.185163] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73319.185165] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73319.185167] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73319.185169] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73319.185171] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73319.187263] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[73319.187276] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[73327.541061] amdgpu: Freeing queue vital buffer 0x7f2e27400000, queue evicted
[73327.541067] amdgpu: Freeing queue vital buffer 0x7f3041200000, queue evicted
[73327.541070] amdgpu: Freeing queue vital buffer 0x7f3047400000, queue evicted
[73327.541071] amdgpu: Freeing queue vital buffer 0x7f3047a00000, queue evicted
[73327.541075] amdgpu: Freeing queue vital buffer 0x7f3196600000, queue evicted
[73327.649199] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73327.649205] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[73327.649207] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73327.649211] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[73327.649212] amdgpu: Resetting wave fronts (cpsch) on dev 0000000058c303b6
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73327.649312] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73327.652804] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73327.758867] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73327.793270] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73327.793923] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73327.793983] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73327.793985] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73327.793988] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73327.796093] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73327.803519] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73328.541797] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73328.541804] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73328.541807] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73328.541808] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73328.541810] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73328.541811] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73328.541813] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73328.541814] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73328.541815] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73328.541817] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73328.541819] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73328.541820] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73328.541822] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73328.543914] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[73328.543927] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
```

---
