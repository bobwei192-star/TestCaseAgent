# [Issue]: build script breaks the host system

> **Issue #4752**
> **状态**: closed
> **创建时间**: 2025-05-19T05:36:58Z
> **更新时间**: 2025-06-10T03:37:26Z
> **关闭时间**: 2025-06-10T03:37:25Z
> **作者**: fwyzard
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4752

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

The build makefile `make -f ROCm/tools/rocm-build/ROCm.mk ...` and the individual makefiles launched form it make various assumptions that break the host system:

1. the build makes frequent use of `sudo` to alter the system.
This _might_ be fine in a throw-away container, though it is a bad approach and a symptom of lack of separation between the preparation of the environment, the build process, and the install process.
It is a _terrible_ approach when used on a non-containerised system:
  - if the user does not have `sudo` rights, the process will fail
  - worse, if the user _does have_ `sudo` rights, it will alter the host system; see for example the use of `sudo chown ... /opt`.
The build system should decouple the "build" part, that should happen by a non-`root` process in a non-`root` owned directory, and the "install" process, that _may_ be invoked by a `root` user to install under `/opt`. In any case it should not try to call `sudo` itself.

2. (some of) the build ignores the `$CCACHE_DIR` environment variable and overrides it with `$HOME/.ccache`.
This leads to much worse performance (and possible other issues) on a system where the `$HOME` is on a network filesystem.

3. the build does not let the user specify the install directory. Instead, it assumes that the installation will always be in `/opt/rocm-6.4.0` (or other version).
This breaks many uses cases where a user would install ROCm in a user-specified, non -system directory.
One example is the utilisation on the LUMI supercomputer.

### Operating System

any

### CPU

any

### GPU

any

### ROCm Version

6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

Follow the instructions at https://github.com/ROCm/ROCm/blob/rocm-6.4.0/README.md#build-rocm-from-source , in particular the "Option 2" to use the host system.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-05-22T13:47:24Z)

Hi @fwyzard. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-05-22T13:52:52Z)

Hi @fwyzard, thank you for reaching out to us, and I am sorry that you are experiencing issues with our ROCm build tool. The tool was initially designed to suit the needs of our internal build pipeline, and we are in the process of optimizing it for broader, more generalized use. We will look into your concerns and see if we can address them. In the mean time, you might be interested in checking out [The Rock](https://github.com/ROCm/TheRock), which is our newest customer-facing build tool for ROCm that is under active development. It is designed to address many problems with the rocm-build tools and will hopefully address some of your concerns. Thanks! 

---

### 评论 #3 — fwyzard (2025-05-22T13:54:50Z)

Thanks @tcgu-amd, I will give it a try.

---

### 评论 #4 — ObiWahn (2025-05-24T16:35:18Z)

relates to: https://github.com/ROCm/ROCm/issues/4624

---

### 评论 #5 — stellaraccident (2025-06-10T03:37:25Z)

While it does not support all of ROCm, and it will only support building against release tags that come into existence from this point forward, we are addressing most of this feedback with the new TheRock build system.

Specifically, per your comment:

* Just git and submodules (although we do have to use a fetch_sources.py right now which also applies some patches locally while we get everything caught up -- sorry... best we can do for the moment).
* Aims to be compatible with arbitrary Linux (and Windows) systems (while most current CI is based off of an AlmaLinux container, it has minimal additions).
* Avoids all AMD shell script based solutions and does not modify system state.
* Defaults to build from source for dependencies which usually come from the system and can vary wildly (can be overridden for OS packagers in order to use system packages) so that the default experience should work.
* If using build-from-source deps, the default is to use fetch content to source bundles that we mirror with SHA hashes, third party deps are centrally managed so that external fetches can be disabled completely if needed (some ROCm sub-projects currently also do secondary fetches, but we are working to eliminate these).
* It is just a build system. Packaging exists separately, and we do not rely on packaging to build.
* We have reference PyTorch build scripts in the repo with patch sets for HEAD (currently requires no patches) and current stable 2.7 (with patches).

Various individual ROCm projects are being upgraded to meet many of the standards you are asking for, but this involves several large scale changes that we are still working through, so the present state is not yet perfect.

Closing this and several other related issue in favor of this one: https://github.com/ROCm/TheRock/issues/797

New build system: https://github.com/ROCm/TheRock

I apologize for the poor experience so far and hope that the new approaches will meet your needs as they mature.

---
