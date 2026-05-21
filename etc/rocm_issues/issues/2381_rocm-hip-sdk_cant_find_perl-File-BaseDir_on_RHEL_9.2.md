# rocm-hip-sdk cant find perl-File-BaseDir on RHEL 9.2

> **Issue #2381**
> **状态**: closed
> **创建时间**: 2023-08-15T18:53:45Z
> **更新时间**: 2024-07-09T08:31:18Z
> **关闭时间**: 2023-10-24T09:29:50Z
> **作者**: Arakendo
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2381

## 描述

Looks like the rocm-hip-sdk is having issues with the perl-File-BaseDir on RHEL 9.2 needed from "hipcc-1.0.0.50600-67.el9.x86_64" when trying to install 5.6

Looks like its there from trying to get file basedir from cpan as shown 

[arakendo@rhel-server ~]$ sudo cpan File::BaseDir
Loading internal logger. Log::Log4perl recommended for better logging
Reading '/root/.local/share/.cpan/Metadata'
  Database was generated on Tue, 15 Aug 2023 14:54:02 GMT
CPAN: Module::CoreList loaded ok (v5.20210320)
File::BaseDir is up to date (0.09).
[arakendo@rhel-server ~]$ sudo yum install rocm-hip-sdk
Updating Subscription Management repositories.
Last metadata expiration check: 0:45:34 ago on Tue 15 Aug 2023 10:49:01 AM EDT.
Error:
 Problem: package rocm-hip-sdk-5.6.0.50600-67.el9.x86_64 requires rocm-hip-runtime-devel = 5.6.0.50600-67.el9, but none of the providers can be installed
  - package rocm-hip-runtime-devel-5.6.0.50600-67.el9.x86_64 requires hipcc = 1.0.0.50600-67.el9, but none of the providers can be installed
  - conflicting requests
  - nothing provides perl-File-BaseDir needed by hipcc-1.0.0.50600-67.el9.x86_64
(try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
[arakendo@rhel-server ~]$

---

## 评论 (3 条)

### 评论 #1 — pramenku (2023-10-23T17:58:03Z)

@Arakendo 

Try below and see it helps. Below is documented at https://rocm.docs.amd.com/en/docs-5.7.1/deploy/linux/prerequisites.html

If helps, feel free to close this issue.

wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
sudo rpm -ivh epel-release-latest-9.noarch.rpm
2. Enable the CodeReady Linux Builder repository

Run the following command and follow the instructions.

sudo crb enable

---

### 评论 #2 — pramenku (2023-10-24T09:29:50Z)

Closing the issue. Please re-open if above doesn't work

---

### 评论 #3 — arunhk3 (2024-07-09T08:31:16Z)

@pramenku - It worked. Thanks!

---
