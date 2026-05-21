# [Issue]: rhel9 repo full of .el8 rpm packages for ROCm versions 7.1 and 7.1.1

> **Issue #5774**
> **状态**: closed
> **创建时间**: 2025-12-15T12:50:47Z
> **更新时间**: 2025-12-16T21:36:46Z
> **关闭时间**: 2025-12-16T21:36:46Z
> **作者**: tristancalsbull
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5774

## 负责人

- harkgill-amd

## 描述

### Problem Description

Incorrect distribution RPMs on RHEL9, these are RHEL8 RPMs.

https://repo.radeon.com/rocm/rhel9/7.1.1/main/ => amd-smi-lib-26.2.0.70101-38.el8.x86_64.rpm
```
$ rpm -qi amd-smi-lib-26.2.0.70101-38.el8.x86_64.rpm
warning: amd-smi-lib-26.2.0.70101-38.el8.x86_64.rpm: Header V4 RSA/SHA512 Signature, key ID 1a693c5c: NOKEY
Name        : amd-smi-lib
Version     : 26.2.0.70101
Release     : 38.el8
Architecture: x86_64
Install Date: (not installed)
Group       : unknown
Size        : 7458867
License     : MIT
Signature   : RSA/SHA512, Mon Nov 24 20:42:33 2025, Key ID 9386b48a1a693c5c
Source RPM  : amd-smi-lib-26.2.0.70101-38.el8.src.rpm
Build Date  : Thu Nov 20 21:47:06 2025
Build Host  : 0c84819e1f08
Relocations : /opt/rocm-7.1.1
Vendor      : Advanced Micro Devices, Inc.
URL         : https://github.com/ROCm/amdsmi
Summary     : AMD System Management libraries
Description :
Runtime components of the library
```

https://repo.radeon.com/rocm/rhel8/7.1.1/main/ => amd-smi-lib-26.2.0.70101-38.el8.x86_64.rpm
```
$ rpm -qi amd-smi-lib-26.2.0.70101-38.el8.x86_64.rpm
warning: amd-smi-lib-26.2.0.70101-38.el8.x86_64.rpm: Header V4 RSA/SHA512 Signature, key ID 1a693c5c: NOKEY
Name        : amd-smi-lib
Version     : 26.2.0.70101
Release     : 38.el8
Architecture: x86_64
Install Date: (not installed)
Group       : unknown
Size        : 7458867
License     : MIT
Signature   : RSA/SHA512, Mon Nov 24 20:42:44 2025, Key ID 9386b48a1a693c5c
Source RPM  : amd-smi-lib-26.2.0.70101-38.el8.src.rpm
Build Date  : Thu Nov 20 21:47:06 2025
Build Host  : 0c84819e1f08
Relocations : /opt/rocm-7.1.1
Vendor      : Advanced Micro Devices, Inc.
URL         : https://github.com/ROCm/amdsmi
Summary     : AMD System Management libraries
Description :
Runtime components of the library
```

same source rpm and same build host.. 

https://repo.radeon.com/rocm/rhel9/7.1.1/main/ and https://repo.radeon.com/rocm/rhel9/7.1/main/ are full of rpm .el8

### Operating System

RHEL

### CPU

None

### GPU

None

### ROCm Version

ROCm 7.1.1 and 7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2025-12-16T21:36:46Z)

Hi @tristancalseviden, the packages at https://repo.radeon.com/rocm/rhel9/7.1.1/main/ do work for RHEL 9 - they're simply built in an RHEL 8 environment leading to the `el8` suffix. If you do encounter any issues when using these packages, feel free to leave a comment and I'll reopen this ticket.

---
