# [Feature]: A method to automatically determine the latest ROCm release that supports ROCm on WSL

> **Issue #5557**
> **状态**: closed
> **创建时间**: 2025-10-22T00:42:30Z
> **更新时间**: 2025-11-06T20:18:18Z
> **关闭时间**: 2025-11-06T20:18:18Z
> **作者**: sbates130272
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5557

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Suggestion Description

I have written a simple bash script called [rocm-latest][ref-script] that parses the repo.radeon.com website to find the latest version of ROCm. It works well but I wanted to add a mode that detects the same for WSL and this is tricky. Can you advise or create a easier way to determine which release of ROCm is the most recent that includes WSL support? Right now I walk the repo looking for versions that have the wsl version of the ROCr runtime library. But that seems to generate results that do not line up with the documentation [here][ref-docs].

[ref-script]: https://github.com/sbates130272/batesste-ansible/blob/main/roles/rocm_setup/files/rocm-latest
[ref-docs]: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html

### Operating System

Ubuntu (and others)

### GPU

All

### ROCm Component

All

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-10-22T15:09:51Z)

Hey @sbates130272, 

> Right now I walk the repo looking for versions that have the wsl version of the ROCr runtime library. But that seems to generate results that do not line up with the documentation [here](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html).

Could you expand on this a bit more - which versions are you seeing a mismatch with specifically? All versions from the docs should have a corresponding `rocr4wsl` runtime package. 

---

### 评论 #2 — sbates130272 (2025-10-28T20:32:42Z)

@harkgill-amd as of the time of writing I see the web-link states 6.4.2 is the most recent version of ROCm that supports WSL. However when I run my script I see the newest release that has that `rocr4wsl` package is 6.4.4.
```
$ WSL_INSTALL=true rocm-latest
ROCm latest (wsl): 6.4.4.
AMDGPU latest (wsl): none.
```

---

### 评论 #3 — harkgill-amd (2025-11-04T19:05:19Z)

So the 6.4.4 package is a little bit of a tricky situation. While it's not an official WSL release and hasn't gone through our standard testing, the package was still uploaded and should be treated as more of a preview. 

In the context of your script, I'd still use the latest package on repo.radeon.com. If a package is uploaded but doesn't have a docs release, you can assume that there isn't much difference in terms of feature set between it and the last documented package. If you'd like to err on the side of caution, you can stick with the fully tested/verified official packages following the documentation.

---
