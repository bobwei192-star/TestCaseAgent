# [Issue]: Cannot checkout rocm-core: ManifestInvalidRevisionError: revision refs/tags/rocm-6.4.1

> **Issue #4798**
> **状态**: closed
> **创建时间**: 2025-05-24T16:06:02Z
> **更新时间**: 2025-06-09T14:13:50Z
> **关闭时间**: 2025-06-09T14:13:49Z
> **作者**: ObiWahn
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4798

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

I think the problem was due to the fact that i did not add my ssh-key before running the command. It maybe you could let the user know:)

The next hurdle is this:

```
» ../repo sync
Fetching:  0% (0/65) 0:00 | ..working..Host key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU
+--[ED25519 256]--+
|                 |
|     .           |
|      o          |
|     o o o  .    |
|     .B S oo     |
|     =+^ =...    |
|    oo#o@.o.     |
|    E+.&.=o      |
|    ooo.X=.      |
+----[SHA256]-----+
Fetching: 93% (61/65) 24:08 | 4 jobs | 24:07 MIOpen @ MIOpenerror.GitError: Cannot fetch git config ('--replace-all', 'remote.rocm-org.projectname', 'rocm-core'): error: could not lock config file /home/yolo/machine-learning/rocm/ROCm/.repo/projects/rocm-core.git/config: File exists

Fetching: 100% (65/65), done in 40m4.151s
Fetching:  0% (0/1) 0:00 | ..working..error.GitError: Cannot fetch git config ('--replace-all', 'remote.rocm-org.projectname', 'rocm-core'): error: could not lock config file /home/yolo//machine-learning/rocm/ROCm/.repo/projects/rocm-core.git/config: File exists

Fetching: 100% (1/1), done in 0.031s
Updating files: 100% (6591/6591), done.SuiteUpdating files:  91% (5998/6591)
Updating files: 100% (40470/40470), done.g files:  59% (23878/40470)
Updating files: 100% (23240/23240), done.ting files:  21% (569/2707)
Updating files: 100% (87340/87340), done.ing files:  34% (50161/147530)
Updating files: 100% (3192/3192), done.ting files:  73% (2331/3192)
Checking out: 72% (47/65) rocWMMAerror: Cannot checkout rocm-core: ManifestInvalidRevisionError: revision refs/tags/rocm-6.4.1 in rocm-core not found
Checking out:  73% (48/65), done in 12.514s
error: in `sync`: revision refs/tags/rocm-6.4.1 in rocm-core not found
```

6.4.1 is the latest tag in this repository. I think it is something that should work.

### Operating System

Debian/SID

### CPU

AMD Ryzen Threadripper 2970WX

### GPU

7900 XTX

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

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-05-26T18:08:01Z)

Hi @ObiWahn, I'm assuming you're running into this error while trying to [build ROCm from source](https://github.com/ROCm/ROCm?tab=readme-ov-file#build-rocm-from-source). I wasn't able to reproduce it on my end with the steps from the README. 

The `rocm-core` repo does in fact have the `rocm-6.4.1` tag as you mentioned so this may have been an intermittent failure with the tool. Are you able to consistently reproduce this failure?

---

### 评论 #2 — ObiWahn (2025-06-09T14:13:49Z)

Checking out: 100% (65/65), done in 22.567s
repo sync has finished successfully.

Yeahy - I started over and this time the sync completed.

---
