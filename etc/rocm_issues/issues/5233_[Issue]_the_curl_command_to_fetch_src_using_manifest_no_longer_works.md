# [Issue]: the curl command to fetch src using manifest no longer works

> **Issue #5233**
> **状态**: closed
> **创建时间**: 2025-08-27T20:45:51Z
> **更新时间**: 2025-09-01T15:58:28Z
> **关闭时间**: 2025-08-28T22:39:41Z
> **作者**: ggankhuy
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5233

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

curl https://storage.googleapis.com/git-repo-downloads/repo | $SUDO tee ~/bin/repo
chmod a+x ~/bin/repo
~/bin/repo init -u https://github.com/RadeonOpenCompute/ROCm.git -b roc-$CONFIG_VERSION.x

Used to work in 6.x or before but broken in 7.0.0. Got this error: 

Fatal: couldn't find remote ref refs/heads/roc-7.0.x
manifests: sleeping 4.0 seconds before retrying
fatal: cannot obtain manifest https://github.com/RadeonOpenCompute/ROCm.git
================================================================================
Repo command failed: UpdateManifestError
        Unable to sync manifest default.xml
Error: Unable to do initialize repo.




### Operating System

Linux

### CPU

AMD

### GPU

MI300

### ROCm Version

7.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

curl https://storage.googleapis.com/git-repo-downloads/repo | $SUDO tee ~/bin/repo
chmod a+x ~/bin/repo
~/bin/repo init -u https://github.com/RadeonOpenCompute/ROCm.git -b roc-$CONFIG_VERSION.x
There CONFIG_VERSION used to have consistent format: <major>.<minor> i.e. 6.3 For ROCm6.3.

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-08-28T14:39:32Z)

Hi @ggankhuy. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — lucbruni-amd (2025-08-28T18:28:30Z)

Hi @ggankhuy,

Thanks for opening an issue with us and sorry for the inconvenience this has caused you.

These `roc-<major-version>.<minor-version>.x` branches (for example, `roc-6.4.x` - the most recent one) are published with each official minor or major version release. Since ROCm 7.0 has not been officially released yet, the corresponding `roc-7.0.x` branch has not been published yet. That's why you're seeing the error `Fatal: couldn't find remote ref refs/heads/roc-7.0.x` for the https://github.com/ROCm/ROCm repository.

You will need to wait until the official release for this branch to become available, and subsequently for those set of commands to work with the `roc-7.0.x` branch. I will update this issue when that happens!

---

### 评论 #3 — ggankhuy (2025-08-28T22:39:41Z)

Oh ok, i did not realize 7.0.0 is not realized. I will check once released. thx! 

---

### 评论 #4 — lucbruni-amd (2025-09-01T15:58:28Z)

No worries! Please don't hesitate to reopen this issue or open a new one if you encounter any issues with the 7.0.0 release. Thanks!

---
