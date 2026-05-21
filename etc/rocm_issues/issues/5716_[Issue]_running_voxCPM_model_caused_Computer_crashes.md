# [Issue]: running voxCPM model caused Computer crashes

> **Issue #5716**
> **状态**: closed
> **创建时间**: 2025-11-28T06:16:11Z
> **更新时间**: 2026-01-29T19:06:49Z
> **关闭时间**: 2026-01-29T19:06:49Z
> **作者**: gqyalh
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5716

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- lucbruni-amd

## 描述

### Problem Description


Running following code

```
import soundfile as sf
from voxcpm import VoxCPM

model = VoxCPM.from_pretrained("/home/gqy/.cache/modelscope/hub/models/OpenBMB/VoxCPM-0.5B")

wav = model.generate(
    text="哼…哼哈哈…哈哈哈！真是可笑啊！这污浊的世界，竟妄想用平凡的枷锁束缚本王？（缓缓抬头，指缝间露出锐利的目光）吾之右眼封印着混沌的深渊，左眼则倒映着星辰的终焉。当双眸再次同时睁开之时，便是因果逆转、法则重构之刻！凡人，庆幸吧——你此刻见证的，将是新纪元的第一缕曙光！碎裂吧，现实的幻象！降临吧，吾的‘寂灭永恒领域’！",
    prompt_wav_path=None,      # optional: path to a prompt speech for voice cloning
    prompt_text=None,          # optional: reference text
    cfg_value=2.0,             # LM guidance on LocDiT, higher for better adherence to the prompt, but maybe worse
    inference_timesteps=10,   # LocDiT inference timesteps, higher for better result, lower for fast speed
    normalize=True,           # enable external TN tool
    denoise=True,             # enable external Denoise tool
    retry_badcase=True,        # enable retrying mode for some bad cases (unstoppable)
    retry_badcase_max_times=3,  # maximum retrying times
    retry_badcase_ratio_threshold=6.0, # maximum length restriction for bad case detection (simple but effective), it could be adjusted for slow pace speech
)

sf.write("output2.wav", wav, 16000)
print("saved: output.wav")

```
success to output wav file, but   Computer crashes Shader Interpolator 100%。

### Operating System

Ubuntu 24

### CPU

AMD radeon AI max+395

### GPU

product: Strix Halo [Radeon Graphics / Radeon 8050S Graphics / Radeon 8060S Graphics]

### ROCm Version

ROCk module version 6.16.6 is loaded

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — gqyalh (2025-11-28T09:26:55Z)

![Image](https://github.com/user-attachments/assets/e1a06397-0530-46c5-a054-2485cb8835da)

---

### 评论 #2 — lucbruni-amd (2025-12-17T22:32:44Z)

Hi @gqyalh, thanks for opening this issue.

Could you you provide us with some more information about your system?

- Verbose system info (`uname -a`)
- Method of ROCm & Torch installation + versions
- Symptoms of the computer crash (did it require a reboot? was it completely frozen?)
- `dmesg` output (`sudo dmesg | tail -500`)
- Any crashes in system logs (`sudo journalctl -b -n 200`)
- After rebooting from the crash: `sudo journalctl -b -1 -k`

Thanks!

---

### 评论 #3 — gqyalh (2026-01-04T03:32:48Z)

uname -a
Linux gqy-GTR-Pro 6.14.0-37-generic #37~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 20 10:25:38 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

torch                      2.10.0.dev20251113+rocm7.1
torchaudio                 2.10.0.dev20251118+rocm7.1
torchvision                0.25.0.dev20251118+rocm7.1


---

### 评论 #4 — lucbruni-amd (2026-01-04T18:16:24Z)

Thanks @gqyalh. Please also provide the `dmesg` and `journalctl` logs as they could give hints as to what's going wrong.

---

### 评论 #5 — lucbruni-amd (2026-01-29T19:06:49Z)

Closing this issue as it has fallen inactive. If you are still encountering this issue, feel free to reopen the issue, and to provide your VoxCPM setup steps alongside `dmesg` output to ensure we are on the same page. Thanks!

---
