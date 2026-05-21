# [Issue]: /var/lib/dkms/amdgpu isn't removed on uninstall and caused dkms.conf error

> **Issue #4197**
> **状态**: closed
> **创建时间**: 2024-12-24T17:36:33Z
> **更新时间**: 2025-01-20T14:51:35Z
> **关闭时间**: 2025-01-20T14:51:33Z
> **作者**: asvishnyakov
> **标签**: Under Investigation, N/A, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4197

## 标签

- **Under Investigation** (颜色: #0052cc)
- **N/A** (颜色: #ededed)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

amgpu-install 6.2.4 and later causes

```
Error! Could not locate dkms.conf file.
File: /var/lib/dkms/amdgpu/6.8.5-2041575.24.04/source/dkms.conf does not exist.
```

error when trying to install dkms


### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

1. Install Ubuntu 24.04.1
2. Install amggpu 6.2.4 or later (this issue was originally about 6.3.1, but I learned only 6.2.* compatible with Ubuntu 24.04.1) following https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html
3. Run `sudo amdgpu-install --usecase=dkms`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2024-12-24T17:41:51Z)

Hi @asvishnyakov. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — asvishnyakov (2024-12-24T17:43:11Z)

Oh ok, it looks like I should still use 6.2.* with 24.04.1. That's strange, because 24.04.2 isn't released yet

---

### 评论 #3 — asvishnyakov (2024-12-24T18:05:33Z)

@ppanchad-amd I reopen this issue as downgrading to 6.2.4 changed nothing, even with all cleanups

---

### 评论 #4 — asvishnyakov (2024-12-24T18:37:02Z)

This looks like duplicate of #3608, but instructions specified there didn't help me, `/var/lib/dkms/amdgpu` was left after uninstallation even with all uninstall/purge/autoremove commands and flags. I was able to install dkms of 6.2.4 version for my Ubuntu 24.04.1 successfully only after I manually removed full folder with it content. 

---

### 评论 #5 — lucbruni-amd (2024-12-24T19:40:02Z)

Hi @asvishnyakov, thank you for creating this issue and reopening after further investigation. An internal ticket has been created for this and we are investigating.

---

### 评论 #6 — lucbruni-amd (2024-12-30T19:37:00Z)

Hi @asvishnyakov, I can indeed see that running the following: 

`sudo apt purge amdgpu-install`
`sudo apt autoremove`

does not remove the corresponding version entry like such: `/var/lib/dkms/amdgpu/<entry>`, but does remove everything inside the entry. Despite having a second entry, albeit empty, running `sudo dkms status` does not yield `Error! Could not locate dkms.conf file.` as it did in #3608, and instead displays the expected output. Could you confirm whether after all the cleanups, the old version is empty?

When installing an older version, cleaning, then upgrading, I am not able to reproduce on Ubuntu 24.04.1 LTS (Noble Numbat).
Could you also kindly provide the specific steps (commands, in order) you took to:
1. Install the initial version you later uninstalled
2. Uninstall said version
3. Attempt to upgrade to a later but different version, causing the error you encountered

Thank you!

---

### 评论 #7 — lucbruni-amd (2025-01-13T21:43:00Z)

Hi @asvishnyakov, are you still encountering this issue? If so, please let me know the steps mentioned in my previous comment. Thanks!

---

### 评论 #8 — lucbruni-amd (2025-01-20T14:51:33Z)

Closing this issue due to inactivity. If the issue persists, feel free to open another ticket with detailed steps taken to reproduce the issue. Thanks!

---
