# [Issue]: amdgpu-dkms configure script broken when `libpam-tmpdir` installed on Ubuntu

> **Issue #4204**
> **状态**: closed
> **创建时间**: 2024-12-28T00:05:00Z
> **更新时间**: 2025-03-05T15:32:03Z
> **关闭时间**: 2025-03-05T15:32:02Z
> **作者**: mvastola
> **标签**: Under Investigation, ROCm 6.3.0, AMD Radeon RX 6600
> **URL**: https://github.com/ROCm/ROCm/issues/4204

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)
- **AMD Radeon RX 6600** (颜色: #ededed)

## 描述

### Problem Description

Basically, I was encountering the same compile errors as #4164 (except on Ubuntu 24.04 LTS) and I was pulling my hair out. 

See below for details

### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

AMD Ryzen Threadripper 2950X 16-Core Processor

### GPU

AMD Radeon RX 6600

### ROCm Version

ROCm 6.3.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Install `libpam-tmpdir` package
2. Run `pam-auth-update` and enable "per-user temp directories" (if not already enabled)
3. Log out, or reboot to ensure the `TMPDIR` env var is set.
4. Follow instructions at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

Not applicable

### Additional Information

Following a deep dive into `amdgpu-dkms`, it seems there is a incompatibility (bug?) in DKMS module's `amd/dkms/configure` script, which (when `libpam-tmpdir` is active) generates an incorrect `amd/dkms/config/config.h` file that won't compile.

In particular, when the `configure` script runs test compilations, it creates a temporary build directory a la:

```bash
build_dir=$(mktemp -d -t build_XXXXXXXX -p $build_dir_root)
```
.. where `$build_dir_root` is `/var/lib/dkms/amdgpu/6.10.5-2095006.24.04/build` (or similar, depending on your system).

The problem is that, according to `mktemp --help`, the presence of the `-d` switch in the call to `mktemp` means that the `-p $build_dir_root` argument is ignored in favor of the `TMPDIR` environment variable, if it exists.  Setting `TMPDIR`, meanwhile, is the entire purpose of the `libpam-tmpdir` pam module. 

In some test compilations, however, the `./configure` script adds `-I../tiny_wrapper/include` to `CFLAGS`, meaning correct results are contingent on `$build_dir` being a subdirectory of `$build_dir_root`. 

False negatives in these test compilations lead to several macros not being defined in `config.h`, which causes the inclusion of code that won't compile, leading to the errors seen in #4164.

As a temporary workaround, I was able to get the module to build by adding `unset TMPDIR` right after the shebang in the `./configure` script. 

Potential permanent fixes include: 

1) setting `TMPDIR` to `$build_dir_root` in the `./configure` script (or in `pre-build.sh`), 
2) unsetting `TMPDIR` in the `./configure` script (or in `pre-build.sh`),
3) replacing all usages of relative paths (e.g. `-I../tiny_wrapper/include` and similar) in test compiles with their respective absolute paths,
4) if this is a 'wontfix', `libpam-tmpdir` should at least be added as a conflicting package in `amdgpu-dkms`'s `debian/control` file

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2024-12-30T15:25:26Z)

Hi @mvastola. Internal ticket has been created to fix this issue. Thanks!

---

### 评论 #2 — lucbruni-amd (2024-12-30T20:40:34Z)

Hi @mvastola, just wanted to let you know that I was able to reproduce your issue on my Ubuntu 24.04.1 LTS (Noble Numbat) system, and I appreciate you providing not only sufficient reproduction steps, but an in-depth analysis of the problem including workarounds and possible fixes. I'm happy you were able to move forward with the workaround for now, and I am currently discussing the possible solutions with the team. Once a decision is made, I'll update you on its progress in subsequent comments. Thank you!

---

### 评论 #3 — klrkdekira (2025-01-03T15:23:56Z)

I thought I was going crazy unable to install amdgpu-dkms when everyone around me able to do it. 
The dkms module installs correctly after I've turnt off "per-user temp directories".
Huge thanks! Hope this will be fixed at the upstream soon.

---

### 评论 #4 — lucbruni-amd (2025-03-05T15:32:02Z)

Closing this issue as I merged in the fix internally (almost identical to [#182](https://github.com/ROCm/ROCK-Kernel-Driver/pull/182)). You can expect to see this upstream in a future release. 

For those encountering this issue at the moment, either disable "per-user temp directories" or include the change above in `/usr/src/amdgpu-<ver>/amd/dkms/pre-build.sh` **before** `./configure` is called as a temporary fix before installing ROCm.

Feel free to open a new issue if you have any related questions/concerns. Thanks!

---
