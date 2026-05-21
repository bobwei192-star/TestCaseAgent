# [Issue]: Invalid wheel filename. wrong number of parts

> **Issue #5898**
> **状态**: closed
> **创建时间**: 2026-01-24T03:03:41Z
> **更新时间**: 2026-04-10T02:24:38Z
> **关闭时间**: 2026-02-11T14:48:27Z
> **作者**: Nfams
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5898

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Windows 10 19045
7700x
9070 xt

I get this issue when using the commands from pytorch via pip in powershell

ERROR: Invalid wheel filename (wrong number of parts): for all 3 torch vision and audio

### Operating System

Windows 10 19045

### CPU

7700x

### GPU

9070 xt

### ROCm Version

7.1 or 2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Will try a reboot and execute but not sure it will change

---

## 评论 (7 条)

### 评论 #1 — harkgill-amd (2026-01-26T18:38:36Z)

Hi @Nfams, I just gave the ROCm and Torch pip install commands from https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html#install-pytorch-via-pip a try and wasn't able to repro the whl naming errors. Could you try pip installing a single wheel at a time to see if you hit any issues and share the entire error message if possible. For example, 
```
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl
```

---

### 评论 #2 — Nfams (2026-01-27T07:03:03Z)

> Hi [@Nfams](https://github.com/Nfams), I just gave the ROCm and Torch pip install commands from https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html#install-pytorch-via-pip a try and wasn't able to repro the whl naming errors. Could you try pip installing a single wheel at a time to see if you hit any issues and share the entire error message if possible. For example,
> 
> ```
> pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl
> ```

Yes i did just that. same result. would there be anywhere the log would be or just the response?

ERROR: Invalid wheel filename (wrong number of parts): 'torch-2.9.1--no-cache-dirBrocmsdk20260116-cp312-cp312-win_amd64'

---

### 评论 #3 — harkgill-amd (2026-01-27T21:20:36Z)

It looks like the `--no-cache-dir` flag is getting mixed into the wheel filename causing the error. Can you try copying/pasting the aforementioned command or just manually typing it out to see if that resolves the issue - also try removing the --no-cache-dir flag entirely if the issue keeps persisting.

---

### 评论 #4 — Nfams (2026-01-28T04:04:56Z)

same error with the no cache removed

"pip install https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchvision-0.24.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl"

Edit: 
I just went to that link and they seemed to work alright from python on that file.
so pip install the file but if i clicked the file maybe there is some conflicts or something with open ui.

---

### 评论 #5 — harkgill-amd (2026-01-28T15:19:50Z)

> same error with the no cache removed

That's odd. Let's stick with just the torch whl and see if we can get that installed. Can you run the following and share the exact error you're seeing on your end?
```
pip cache purge
pip install https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl
```

---

### 评论 #6 — harkgill-amd (2026-02-11T14:48:27Z)

Closing this out for now but feel free to leave a comment if the issue persists.

---

### 评论 #7 — Zalohin (2026-04-10T02:24:38Z)

Just replace "%2B"  to "+" in links.
I mean instead of "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl" use "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl"

---
