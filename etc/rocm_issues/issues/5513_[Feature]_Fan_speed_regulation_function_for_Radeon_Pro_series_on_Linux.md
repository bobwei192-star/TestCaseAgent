# [Feature]: Fan speed regulation function for Radeon Pro series on Linux

> **Issue #5513**
> **状态**: closed
> **创建时间**: 2025-10-14T07:25:04Z
> **更新时间**: 2026-01-02T18:25:26Z
> **关闭时间**: 2025-10-21T14:21:09Z
> **作者**: HUSRCF
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5513

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Suggestion Description

**Fan regulation function needed!**
Fan speed could affect the performance hugely! When conducting AI training, I notice that the temperature of my W7900 is extremely high, with a junction temperature up to 90 degrees while the fan speed is just about 50%. High temperatures would have a serious negative on the lifetime of the card and might lead to stability issues.
**Linux is not yet supported through rocm-smi**
I notice that the current fan regulation function is only limited to windows system. ROCm-smi on Linux seems to be banned for pro series. When setting fan speed, an output shows that regulate successfully will be given. But there's no actual difference. The output is as follows.

<img width="975" height="512" alt="Image" src="https://github.com/user-attachments/assets/cfeafbd6-11c8-4581-8fce-49030a48c56d" />


### Operating System

Ubuntu 24.04.5 LTS

### GPU

Radeon Pro W7900/W7900 Dual Slot

### ROCm Component

_No response_

---

## 评论 (6 条)

### 评论 #1 — tcgu-amd (2025-10-14T19:00:57Z)

Hi @HUSRCF, yeah unfortunately the fan speeds can only be controlled through the overdrive interface iirc. It is an old thread, but I have provided instructions in the past https://github.com/ROCm/amdgpu/issues/162#issuecomment-2690986760. Can you please take a look and let me know if it works for you? Thanks! 

---

### 评论 #2 — HUSRCF (2025-10-15T03:00:34Z)

@tcgu-amd Thanks a lot for your time and attention to this problem. I had to acknowledge I forgot to refer to similar issues proposed since I guess few would require such operation. However, after operating as your instruction in mentioned link. I encountered some problems. It seems that the folder mentioned does not exist in new version program.
Here's your instruction to open the folder with configure file:
<img width="837" height="302" alt="Image" src="https://github.com/user-attachments/assets/205534c1-97ef-4a2b-8342-4efb11ca0927" />
However, after operation, the expected folder doesn't exist and the output is as follows. Besides, it seems that there' re a folder with simliar structure _drm/card0/device_ under _/sys/class/drm/card0/device_. Is this the correct case?

<img width="765" height="822" alt="Image" src="https://github.com/user-attachments/assets/f8f4c961-df8d-492d-aaa6-f6d60f280e87" />

If there's any change in the target folder's position or any parameter left, please @ me, thanks for your time and attention once again!

---

### 评论 #3 — HUSRCF (2025-10-15T03:03:35Z)

Addition: I would give it a try on another device with a 7900XTX card, whose core is similar to this one. If there's any progress, I would leave new comment here.

---

### 评论 #4 — tcgu-amd (2025-10-15T13:16:26Z)

Hi @HUSRCF, perhaps your amdgpu driver is auto loaded on boot. Try this

```
sudo modprobe -r amdgpu
sudo modprobe amdgpu ppfeaturemask=0xfff7ffff
```

To make it hassle free, you can add  `amdgpu.ppfeaturemask=0xfff7ffff` into the kernel command line, which should allow od to be enabled automatically on boot. 

Let me know if this works!

Thanks!

---

### 评论 #5 — tcgu-amd (2025-10-21T14:21:09Z)

Hi @HUSRCF, I will be closing this issue for now due to inactivity. Please feel free to update the issue when you are ready, and I will re-open if the problem persists. Thanks! 

---

### 评论 #6 — HUSRCF (2026-01-02T18:25:26Z)

Sorry for my interruption once again. Now I've met a new question. I just add one W7900 card to my system on the original basis of a W7900DS. Now the newly-added W7900 failed to be regulated with the fan curve like this:

<img width="1651" height="446" alt="Image" src="https://github.com/user-attachments/assets/c8b83417-0f73-401a-aedb-00737d7ee771" />

And for another original W7900DS card everything just work well according to https://github.com/ROCm/amdgpu/issues/162#issuecomment-2690986760. 

<img width="1170" height="451" alt="Image" src="https://github.com/user-attachments/assets/89d64bf3-d88f-4743-9033-b55c6f688ac7" />

In addition, the fan_target_temperature and fan_minimum_pwm are modified successfully. 

<img width="1043" height="103" alt="Image" src="https://github.com/user-attachments/assets/70a8a2c5-aae9-47bf-b56c-11cdf248debc" />

If there's any solution, please inform me. Tks very much!

Addition of sys info: W7900DS is with a screen while the other one W7900 is just for computation. BIOS version are:

/sys/class/drm/card0/device/vbios_version:113-D7070600-103
/sys/class/drm/card1/device/vbios_version:113-D7070100-101


---
