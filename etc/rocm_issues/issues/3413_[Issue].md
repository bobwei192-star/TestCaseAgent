# [Issue]: 

> **Issue #3413**
> **状态**: closed
> **创建时间**: 2024-07-11T23:11:24Z
> **更新时间**: 2025-01-10T16:04:44Z
> **关闭时间**: 2024-07-12T13:21:36Z
> **作者**: FLAKDaddy
> **标签**: AMD Radeon RX 7900 XT, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3413

## 标签

- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

when I run `rocminfo`
I got back this result:
`ROCR: unsupported GPU`
`hsa api call failure at: ./sources/wsl/tools/rocminfo/rocminfo.cc:1087
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.`

Using WSL
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"

GPU: 7600XT

### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD 5600x

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

Using WSL
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"

GPU: 7600XT

Attempted install of ollama docker rocm
pulled image but upon running...
`docker: Error response from daemon: error gathering device information while adding custom device "/dev/kfd": no such file or directory.`

So I followed this doc: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#post-install-verification-check

used the WSL usecase

Install seemed okay, only hiccup was:
`"WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"`

BUT when I ran `rocminfo`
I got back this result:
`ROCR: unsupported GPU`
`hsa api call failure at: ./sources/wsl/tools/rocminfo/rocminfo.cc:1087
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.`


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

I couldn't select my GPU but afaik the 7600xt is supported?

---

## 评论 (6 条)

### 评论 #1 — FLAKDaddy (2024-07-11T23:22:49Z)

oh, looks like a shorter list for WSL
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html

---

### 评论 #2 — harkgill-amd (2024-07-12T13:21:36Z)

Hi @FLAKDaddy , the beta release of ROCm on WSL only supports the GPUs listed under [compatibility matrices](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html). Unfortunately, the 7600XT is not currently supported for WSL.

---

### 评论 #3 — Jameson-Crate (2024-07-13T00:48:02Z)

I saw for previous versions of ROCm people were able to use HSA_OVERRIDE_GFX_VERSION=10.3.0 as a work around, is there anything similar for this version of ROCm or do we just have to wait for support?

---

### 评论 #4 — A-Ghorab (2024-07-18T08:29:41Z)

> I saw for previous versions of ROCm people were able to use HSA_OVERRIDE_GFX_VERSION=10.3.0 as a work around, is there anything similar for this version of ROCm or do we just have to wait for support?

nope, https://github.com/ROCm/ROCm/issues/3402#issuecomment-2218312649

but according to that post soon more SKU will be supported

---

### 评论 #5 — brianangulo (2024-12-29T23:55:31Z)

> Hi @FLAKDaddy , the beta release of ROCm on WSL only supports the GPUs listed under [compatibility matrices](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html). Unfortunately, the 7600XT is not currently supported for WSL.

Hey @harkgill-amd sorry to be a bug. But just curious on the reason for limiting to certain SKUs only? Is this a sort of soft limitation due to lack of testing on these other GPUs? Just wondering if maybe there is some setting or configuration that by building rocm from source could be altered to allow support for something like a 7800 (which is kinda crazy is not supported to begin with tbh). Thankful for any guidance you can share on this 🙏.

---

### 评论 #6 — harkgill-amd (2025-01-10T16:03:11Z)

Hi @brianangulo, unfortunately this is a hard limitation in WSL and cannot be worked around. Please refer to https://github.com/ROCm/ROCm/discussions/2599 where updates will be provided on the support status going forward.

---
