# [Issue]: Insufficient documentation on the repo tool and associated manifest.xml file

> **Issue #2615**
> **状态**: closed
> **创建时间**: 2023-10-30T20:45:07Z
> **更新时间**: 2024-07-25T18:21:39Z
> **关闭时间**: 2024-07-25T18:20:40Z
> **作者**: amd-isparry
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2615

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- saadrahim

## 描述

### Problem Description

The top level README.md was altered in https://github.com/RadeonOpenCompute/ROCm/commit/1ae99c5e4bc77dd1dc4760eb29edfeb76c833229 to mention the manifest.xml file. However all it says is `The default.xml file uses the repo Manifest format.`.

There should be a link to the specification of this format.

There should be a link to the `repo` tool.

Ubuntu 20 didn't package the repo tool, apparently because of python2 to python3 changes. There should be a link to the repo tool site explaining how to install the tool.


### Operating System

N/A

### CPU

N/A

### GPU

N/A

### ROCm Version

5.7.x

### ROCm Component

Documentation

### Steps to Reproduce

_No response_

### Output of /opt/rocm/bin/rocminfo --support

Not applicable.

---

## 评论 (4 条)

### 评论 #1 — nartmada (2024-02-14T03:30:12Z)

Hi @saadrahim and @amd-isparry, do we still need this ticket to be opened?  Thanks.

---

### 评论 #2 — amd-isparry (2024-02-14T03:34:23Z)

I have not seen any mention that the documentation has been improved, so there is no reason to close it yet, the documentation does need to be improved.

---

### 评论 #3 — nartmada (2024-02-14T03:37:20Z)

I will create an internal ticket to track any progress.

---

### 评论 #4 — harkgill-amd (2024-07-25T18:20:40Z)

Hi @amd-isparry, the [README.md](https://github.com/ROCm/ROCm/blob/develop/README.md) file has since been updated and now provides information on how to install the repo tool.  Please see the excerpts below:
```
Installing the repo tool
The repo tool from Google allows you to manage multiple git repositories simultaneously. Run the following commands to install the repo tool:

mkdir -p ~/bin/
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```
Information on how to use the tool to download the ROCm source code is also now present.
```
Downloading the ROCm source code
The following example shows how to use the repo tool to download the ROCm source code. If you choose a directory other than ~/bin/ to install the repo tool, you must use that chosen directory in the code as shown below:

mkdir -p ~/ROCm/
cd ~/ROCm/
~/bin/repo init -u http://github.com/ROCm/ROCm.git -b roc-6.0.x
~/bin/repo sync
```
I will close this ticket for now. If you feel these changes do not completely address the issue, please re-open this ticket. Thanks!

---
