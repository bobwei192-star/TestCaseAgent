# [Documentation]: The build from source is missing multiple dependencies

> **Issue #3411**
> **状态**: closed
> **创建时间**: 2024-07-10T18:52:25Z
> **更新时间**: 2025-06-23T14:45:16Z
> **关闭时间**: 2025-06-23T14:45:16Z
> **作者**: JonChesterfield
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/3411

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

I've been trying to follow "option 2", the non-docker build, and there are multiple packages that it requires that do not seem to be documented. I was trying to build on Ubuntu 22.04.

git requires curl/curl.h. This seems to collide with Ubuntu's packaging system badly, I ended up installing multiple curl related packages and am unsure which fixed it. Since the instructions use git to clone and install git's large file handling from repos, this is probably best fixed by not building git from source.

ninja's build uses `/usr/bin/env python` where there is no python. The most likely fix seems to be `apt install python-is-python3` but much safer would be installing ninja from apt instead of from source.

Boost required `apt install lbzip2`. Otherwise `command -f lbzip2` returns the empty string.

cp /tmp/local-pin-600 fails as the file doesn't exist, don't know what is supposed to be in it.

HIP fails to build without rpmbuild, found in `apt install rpm`

rocm-dbgapi fails to build on "no rule to make target doc". It looks like the cmake understands that doxygen is optional but other things do not. Installing doxygen gets as far as missing pdflatex. `apt install doxygen texlive` resolves those errors.

That's as far as I've got before giving up and trying docker, which seems to go into a busy loop on start that it does not recover from.

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-07-10T20:52:23Z)

Hi @JonChesterfield, could you please provide a link to the documentation that you are referencing. Thanks!

---

### 评论 #2 — JonChesterfield (2024-07-10T23:12:26Z)

Sure. https://github.com/ROCm/ROCm/blob/develop/README.md#build-rocm-from-source

---

### 评论 #3 — harkgill-amd (2024-07-11T19:15:57Z)

I will relay the missing dependencies over to the internal team so they can further investigate this issue. Thanks again!

---

### 评论 #4 — harkgill-amd (2025-06-23T14:45:16Z)

Hi @JonChesterfield, apologies for the lack of response on this issue. We've shifted away from using the build scripts as our primary build from source recipe and now recommend using TheRock - https://github.com/ROCm/TheRock. Since the build scripts are likely to be deprecated moving forward, I'll go ahead and close this issue. Feel free to leave a comment if you have any questions regarding the new build system.

---
