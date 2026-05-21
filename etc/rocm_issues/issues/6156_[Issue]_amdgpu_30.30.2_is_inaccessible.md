# [Issue]: amdgpu 30.30.2 is inaccessible

> **Issue #6156**
> **状态**: closed
> **创建时间**: 2026-04-17T02:49:22Z
> **更新时间**: 2026-04-21T22:17:58Z
> **关闭时间**: 2026-04-21T22:17:58Z
> **作者**: Wedge009
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6156

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I'm surprised this hasn't been reported already since ROCm 7.2.2 has been out for a few days. On Ubuntu, at least, the `etc/apt/sources.list.d/amdgpu.list` contents declares:

```
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30.2/ubuntu noble main
```

Yet https://repo.radeon.com/amdgpu/30.30.2/ubuntu remains inaccessible, at least for me. Server returns 404 Not Found.

### Operating System

Ubuntu 24.04.4 LTS

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 7.2.2

### ROCm Component

_No response_

### Steps to Reproduce

Use https://repo.radeon.com/amdgpu-install/7.2.2/ubuntu/noble/amdgpu-install_7.2.2.70202-1_all.deb and attempt to install anything. https://repo.radeon.com/amdgpu/30.30.2/ubuntu returns 404.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

https://repo.radeon.com/amdgpu/30.30.1/ubuntu for ROCm 7.2.1 is accessible.

---

## 评论 (6 条)

### 评论 #1 — harkgill-amd (2026-04-17T21:00:43Z)

Hey @Wedge009, the decision was made to temporarily use the https://repo.radeon.com/amdgpu/30.30.1/ubuntu on release hence the `sed` commands in https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#register-repositories.

Looks like https://repo.radeon.com/amdgpu/30.30.2/ubuntu/ was just recently made available as well so the repo should work fine OOB now. I'd expect the docs to updated shortly to align with this.

---

### 评论 #2 — Wedge009 (2026-04-17T22:30:16Z)

Okay, but attempting a fresh installation previously failed because the source could not be accessed.

I just tried another update and now the failure is on https://repo.radeon.com/graphics/7.2.2. I remember there were two sources that were failing, now there is only one.

---

### 评论 #3 — harkgill-amd (2026-04-20T14:34:25Z)

For that one, you'll still need the `sed` command from the docs to downgrade to the 7.2.1 graphics repo.
```
sudo sed -i "s|graphics/7.2.2|graphics/7.2.1|" /etc/apt/sources.list.d/rocm.list
```

---

### 评论 #4 — Wedge009 (2026-04-20T21:49:26Z)

I don't recall having to make manual commands before. Is there any reason the 7.2.2 release has chosen this approach?

---

### 评论 #5 — harkgill-amd (2026-04-21T20:48:36Z)

These steps are included to ensure that when installing ROCm 7.2.2, the user's system points to the latest repos (rocm/graphics/amdgpu) available at the time of release. Not all repo versions were linearly bumped this release.

---

### 评论 #6 — Wedge009 (2026-04-21T22:17:58Z)

I finally found 'the docs' in https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html

```bash
wget https://repo.radeon.com/amdgpu-install/7.2.2/ubuntu/noble/amdgpu-install_7.2.2.70202-1_all.deb
sudo apt install ./amdgpu-install_7.2.2.70202-1_all.deb
sudo sed -i "s/\/30.30.2/\/30.30.1/" /etc/apt/sources.list.d/amdgpu.list
sudo sed -i "s|graphics/7.2.2|graphics/7.2.1|" /etc/apt/sources.list.d/rocm.list
sudo apt update
```

Seems very counter-intuitive, manually reverting 7.2.2 to 7.2.1 (and amdgpu is still being pushed back to 30.30.1). I think it would have probably been better to implement a symbolic link on the server. But anyway, given the issues I've been having with 7.2.x I haven't been keen to update yet anyway.

---
