# [Issue]: ROCm 7.1 /opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory

> **Issue #5943**
> **状态**: open
> **创建时间**: 2026-02-08T17:17:09Z
> **更新时间**: 2026-02-12T16:12:28Z
> **作者**: srmo
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5943

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

https://github.com/ROCm/ROCm/issues/2961 is closed without an obvious solution.
Just installed rocm and pytorch on CachyOS from the https://download.pytorch.org/whl/nightly/rocm7.1 index

```
python -c "import torch; print(torch.cuda.is_available())"
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
True
```
Now, in #2961 it is suggested to symlink to /opt/amdgpu but I'm wondering which source I should use.
I have
```
locate amdgpu.ids
/usr/share/libdrm/amdgpu.ids
```
and `venv/lib/python3.14/site-packages/torch/share/libdrm/amdgpu.ids` from my python venv installation.

I'm a bit lost here and very new to this whole rocm and torch party.



### Operating System

CachyOS Linux

### CPU

AMD Ryzen 9 7950X3D 16-Core Processor

### GPU

AMD Radeon RX 9070 XT 

### ROCm Version

ROCm 7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — huanrwan-amd (2026-02-11T21:34:04Z)

Hi @srmo thanks for posting, notice you are using CachyOS Linux which is not officially supported by ROCm: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html.
And ROCm is not in its default path.
It is suggested to sym link to use system libdrm first. If does not work. Then try pytorch one. 

---

### 评论 #2 — XanderBaatz (2026-02-12T16:12:28Z)

I'm running into the same issue using your `rocm/dev-ubuntu-24.04:7.1.1-complete` image on Fedora Silverblue. However, I am also running ROCM `torch` in a `venv` managed by `uv`.
However `docker pull rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.9.1` worked. It seems as though it needs a system-wide install of ROCM `torch` for it to also work in a `venv`? So the `venv` can't exclusively have a self-contained ROCM Pytorch instance.

---
