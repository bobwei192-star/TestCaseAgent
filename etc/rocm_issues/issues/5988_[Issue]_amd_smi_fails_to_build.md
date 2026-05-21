# [Issue]: amd_smi fails to build

> **Issue #5988**
> **状态**: closed
> **创建时间**: 2026-02-22T22:03:27Z
> **更新时间**: 2026-03-09T14:38:22Z
> **关闭时间**: 2026-03-09T14:38:22Z
> **作者**: mcurtis789
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5988

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- darren-amd

## 描述

### Problem Description

I am following Steps to install vLLM here. 
https://community.frame.work/t/how-to-compiling-vllm-from-source-on-strix-halo/77241/46

however because amd-smi fails to install i cannot get vLLM to start.

```
(vllm) mike@ms-s1-max:~/vllm/vllm$ uv pip install /opt/rocm/share/amd_smi
Using Python 3.13.12 environment at: /home/mike/vllm/.venv
Resolved 1 package in 2ms
  × Failed to build `amdsmi @ file:///opt/rocm/share/amd_smi`
  ├─▶ The build backend returned an error
  ╰─▶ Call to `setuptools.build_meta.build_wheel` failed (exit status: 1)

      [stdout]
      running egg_info

      [stderr]
      /home/mike/.cache/uv/builds-v0/.tmpxiQoMM/lib/python3.13/site-packages/setuptools/config/_apply_pyprojecttoml.py:82:
      SetuptoolsDeprecationWarning: `project.license` as a TOML table is deprecated
      !!

              ********************************************************************************
              Please use a simple string containing a SPDX expression for `project.license`. You can also use
      `project.license-files`. (Both options available on setuptools>=77.0.0).

              By 2027-Feb-18, you need to update your project and remove deprecated calls
              or your builds will no longer be supported.

              See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
              ********************************************************************************

      !!
        corresp(dist, value, root_dir)
      error: Cannot update time stamp of directory 'amdsmi.egg-info'

      hint: This usually indicates a problem with the package or the build environment.
```

```
OS:
NAME="Ubuntu"
VERSION="24.04.4 LTS (Noble Numbat)"
CPU:
model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151
  Marketing Name:          AMD Radeon Graphics
      Name:                    amdgcn-amd-amdhsa--gfx1151
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
  Name:                    aie2p
  Marketing Name:          RyzenAI-npu5
```

### Operating System

Ubuntu 24.04.4 

### CPU

AMD RYZEN AI MAX+ 395 

### GPU

Radeon 8060S

### ROCm Version

7.1

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

### 评论 #1 — darren-amd (2026-02-23T16:21:23Z)

Hi @mcurtis789,

Thanks for reporting the issue. It looks like a permission related issue on your end where your current user cannot write to the /opt directory (presumably because it is owned by root). Could you try copying to a temp directory and installing: `cp -r /opt/rocm/share/amd_smi /tmp/amd_smi && uv pip install /tmp/amd_smi && rm -rf /tmp/amd_smi` and let me know if the issue persists? Thanks!

---

### 评论 #2 — darren-amd (2026-03-09T14:38:22Z)

Going to close this out, please feel free to reopen if the above doesn't fix the issue, thanks!

---
