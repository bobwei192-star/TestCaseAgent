# [Bug]: Can't build Hunyuan3D's custom_rasterizer on windows

> **Issue #6184**
> **状态**: open
> **创建时间**: 2026-04-26T16:58:40Z
> **更新时间**: 2026-05-06T00:57:03Z
> **作者**: wrharper
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6184

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Suggestion Description

Fix the gaps in rocm! It is so close to doing everything. I can even do 3d meshes, but I can't do multi-view? LOL
You guys have done an amazing job. practically 99% of the way there now. Just fix the last remaining gaps or give an alternative that can!
You will probably say to go to them. They will say rocm can't do it. See the problem here?
https://github.com/kijai/ComfyUI-Hunyuan3DWrapper/issues/201
https://github.com/kijai/ComfyUI-Hunyuan3DWrapper/issues/204
https://huggingface.co/doang/ComfyUI-Wheels/tree/ab229dbc98920ab20fadfd7abc7bdf3426dc3db1
Every single HY3D works except this:
<img width="1440" height="662" alt="Image" src="https://github.com/user-attachments/assets/cd751864-55ec-440a-bb16-6891ef65606c" />
so something is missing.

### Operating System

_No response_

### GPU

7900 XTX

### ROCm Component

_No response_

---

## 评论 (6 条)

### 评论 #1 — schung-amd (2026-04-27T18:41:29Z)

> You will probably say to go to them. They will say rocm can't do it.

Do you have a source for this? If there's a specific reason this is incompatible with ROCm we'd be happy to look into getting that fixed. Otherwise this is on the HY3D wrapper devs to add ROCm support. I can poke around to see if there's a workaround when I have time.

---

### 评论 #2 — wrharper (2026-04-27T21:53:32Z)

https://huggingface.co/doang/ComfyUI-Wheels/tree/ab229dbc98920ab20fadfd7abc7bdf3426dc3db1
Message doang?


---

### 评论 #3 — wrharper (2026-04-27T21:56:14Z)

> > You will probably say to go to them. They will say rocm can't do it.
> 
> Do you have a source for this? If there's a specific reason this is incompatible with ROCm we'd be happy to look into getting that fixed. Otherwise this is on the HY3D wrapper devs to add ROCm support. I can poke around to see if there's a workaround when I have time.

I'm actually working on getting this to work in Linux ubuntu 22.04 which appears to the only way to most things to work together which does prove something is missing in windows rocm if it works in Linux and not Windows since this is all python based.

---

### 评论 #4 — wrharper (2026-04-28T01:46:47Z)

i found: https://github.com/ROCm/ROCm/issues/5981 which is also related to show the problem.

---

### 评论 #5 — schung-amd (2026-05-05T18:48:54Z)

I'm not seeing a technical issue with ROCm components here but simply the custom_rasterizer code (https://github.com/Tencent-Hunyuan/Hunyuan3D-2/tree/main/hy3dgen/texgen/custom_rasterizer) not being configured to build with HIP. Users have found ways to build custom_rasterizer on Linux; see discussion in https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/53. I have still not seen a source stating that there is some technical barrier to this working on AMD hardware. I'll see if I can hack together a workaround to build on Windows + TheRock.

---

### 评论 #6 — wrharper (2026-05-06T00:56:23Z)

I have tried to get this to compile on many versions of Linux and ROCm. It only seems to work with only one specific version and if you upgrade to newer ubuntu or use Linux mint it will not work. It doesn't work with newer Pythons or newer ROCm either. Hopefully this helps. I had issues with PyTorch lightning as well when trying to upgrade. https://lightning.ai/docs/pytorch/stable/
It seems like tons of things are breaking in newer versions of Linux, Python, and ROCm. It has been difficult to find a root cause.

---
