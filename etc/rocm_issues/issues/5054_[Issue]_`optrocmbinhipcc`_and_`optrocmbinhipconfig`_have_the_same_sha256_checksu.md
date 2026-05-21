# [Issue]: `/opt/rocm/bin/hipcc` and `/opt/rocm/bin/hipconfig` have the same sha256 checksum

> **Issue #5054**
> **状态**: closed
> **创建时间**: 2025-07-16T15:38:51Z
> **更新时间**: 2025-08-28T13:47:33Z
> **关闭时间**: 2025-08-28T13:47:33Z
> **作者**: fxmarty-amd
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5054

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Hi,

As per tile.

Repro: `docker run -it --rm --device /dev/kfd --device /dev/dri --security-opt seccomp=unconfined --shm-size=64g --net host rocm/dev-ubuntu-22.04:6.4.1 /bin/bash`

And:

```bash
sha256sum /opt/rocm/bin/hipconfig
sha256sum /opt/rocm/bin/hipcc
```

yielding the same:
```
a2e73caf4d75e85960ea4fd6cac9012eb91d2a60facb26d4ec8b23921ca1add1  /opt/rocm/bin/hipconfig
a2e73caf4d75e85960ea4fd6cac9012eb91d2a60facb26d4ec8b23921ca1add1  /opt/rocm/bin/hipcc
```

although these two binaries should be different, and e.g. `hipcc --version` and `hipconfig --version` produce a different output.

`ls -la /opt/rocm/bin` shows that these two are not symlinks or hard links.

### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD EPYC 9554 64-Core Processor

### GPU

AMD Instinct MI300X

### ROCm Version

6.4.1

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

### 评论 #1 — harkgill-amd (2025-08-01T14:37:14Z)

That's odd. Will get some clarification on this and get back to you.

---

### 评论 #2 — harkgill-amd (2025-08-11T19:14:10Z)

Both `hipcc` and `hipconfig` are built from the same code resulting in identical executables - https://github.com/ROCm/llvm-project/blob/amd-staging/amd/hipcc/CMakeLists.txt#L21-L33. They are in fact the same files.

The difference in output is the result of https://github.com/ROCm/llvm-project/blob/amd-staging/amd/hipcc/src/hipBin.cpp#L92-L103. The filename determines which code flow to execute. You can test this yourself by renaming either executable to its counterpart and checking the output. I believe the files used to be slightly different prior to the perl versions of these commands being deprecated. Will check if we can simply utilize a symlink now.


---

### 评论 #3 — fxmarty-amd (2025-08-12T07:16:28Z)

Thank you @harkgill-amd. Indeed could we make it so that these files have a different hash, and/or are symlinks, as they do not do the same thing? I wished to run `rdfind` on `/opt/rocm` and ran into issues due to this.

---

### 评论 #4 — harkgill-amd (2025-08-14T15:32:02Z)

Spoke to the component team regarding this and it was decided to separate these two binaries rather just using a symlink. With the change https://github.com/ROCm/llvm-project/commit/4f229eb449460b7aca2c335cd6f0dc648b4a0fcb in place, you shouldn't run into anymore duplicate hash issues. Thanks for bringing this up and let me know if you have any other questions.

---

### 评论 #5 — harkgill-amd (2025-08-28T13:47:33Z)

Fix has been merged which decouples these two executables, resulting in different checksums.

---
