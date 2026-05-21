# How to disable creation of unneeded packages

> **Issue #3742**
> **状态**: closed
> **创建时间**: 2024-09-18T02:01:46Z
> **更新时间**: 2024-09-29T19:23:07Z
> **关闭时间**: 2024-09-29T19:23:07Z
> **作者**: jdumke
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3742

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

With the default build cmd:
make -f ROCm/tools/ROCm.mk  all
all variants of packages will be created, which I don't need respectively use, I only need DEB. How can I disable the creation of all other, espacially RPM, which fails due an outdated rpmbuild in Debian stable.

Thanks for helping.

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-09-18T15:18:09Z)

Hi @jdumke, let me confirm if this is possible with the current scripts and get back to you.

---

### 评论 #2 — harkgill-amd (2024-09-19T14:55:23Z)

@jdumke, by default the CPACKGEN is set to DEB, allowing for only Debian packages to be created. Could you please point out which RPM packages are being created?

---

### 评论 #3 — jdumke (2024-09-29T19:23:07Z)

In my case it were the rpm for amd_smi_lib, but it seems that the workaround given to me in #3743 solves this issue too. I added Debian to list distro list in envsetup.sh and all works fine.

---
