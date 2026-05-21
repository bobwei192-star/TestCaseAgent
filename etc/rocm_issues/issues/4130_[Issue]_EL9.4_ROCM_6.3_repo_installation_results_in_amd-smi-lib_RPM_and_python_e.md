# [Issue]: EL9.4 ROCM 6.3 repo installation results in amd-smi-lib RPM and python errors

> **Issue #4130**
> **状态**: closed
> **创建时间**: 2024-12-06T18:33:09Z
> **更新时间**: 2025-04-04T10:08:24Z
> **关闭时间**: 2025-01-13T20:08:19Z
> **作者**: prarit
> **标签**: Under Investigation, ROCm 6.2.3, N/A
> **URL**: https://github.com/ROCm/ROCm/issues/4130

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **N/A** (颜色: #ededed)

## 描述

### Problem Description

Following the published Quick start installation guide instructs results in rpm and python errors.

### Operating System

RHEL9.4

### CPU

n/a

### GPU

n/a

### ROCm Version

ROCm 6.2.3

### ROCm Component

amdsmi

### Steps to Reproduce

1.  Follow the instruction for RHEL 9.4 here: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html
2. To take a shortcut, do 'dnf -y install amd-smi-lib' ... bug will reproduce either way but easier to just install the offending package and its two dependencies.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

PLEASE NOTE THAT THIS BUG IS AGAINST ROCM _6.3_ -- the ROCm Version drop down in the issue reporting tool does not have a 6.3 available.

[root@vm-10-0-186-164 ~]# dnf -y install amd-smi-lib
Updating Subscription Management repositories.
Unable to read consumer identity

This system is not registered with an entitlement server. You can use "rhc" or "subscription-manager" to register.

Last metadata expiration check: 0:08:08 ago on Fri 06 Dec 2024 01:07:51 PM EST.
Dependencies resolved.
====================================================================================================
 Package              Architecture    Version                         Repository               Size
====================================================================================================
Installing:
 amd-smi-lib          x86_64          24.7.1.60300-39.el9             amdgpu-6.3              1.3 M
Installing dependencies:
 python3-pip          noarch          21.2.3-8.el9                    rhel-AppStream          2.0 M
 rocm-core            x86_64          6.3.0.60300-39.el9              amdgpu-6.3               25 k

Transaction Summary
====================================================================================================
Install  3 Packages

Total download size: 3.3 M
Installed size: 13 M
Downloading Packages:
(1/3): python3-pip-21.2.3-8.el9.noarch.rpm                          5.3 MB/s | 2.0 MB     00:00    
(2/3): rocm-core-6.3.0.60300-39.el9.x86_64.rpm                       41 kB/s |  25 kB     00:00    
(3/3): amd-smi-lib-24.7.1.60300-39.el9.x86_64.rpm                   1.8 MB/s | 1.3 MB     00:00    
----------------------------------------------------------------------------------------------------
Total                                                               4.7 MB/s | 3.3 MB     00:00     
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                            1/1 
  Installing       : rocm-core-6.3.0.60300-39.el9.x86_64                                        1/3 
  Running scriptlet: rocm-core-6.3.0.60300-39.el9.x86_64                                        1/3 
  Installing       : python3-pip-21.2.3-8.el9.noarch                                            2/3 
  Installing       : amd-smi-lib-24.7.1.60300-39.el9.x86_64                                     3/3 
  Running scriptlet: amd-smi-lib-24.7.1.60300-39.el9.x86_64                                     3/3 
Using pyproject.toml for installation due to setuptools version 53.0.0
  DEPRECATION: A future pip version will change local packages to be built in-place without first copying to a temporary directory. We recommend you use --use-feature=in-tree-build to test your packages with this new behavior before it becomes the default.
   pip 21.3 will remove support for this functionality. You can find discussion regarding this at https://github.com/pypa/pip/issues/7555.
    ERROR: Command errored out with exit status 1:
     command: /bin/python3 /usr/lib/python3.9/site-packages/pip/_vendor/pep517/in_process/_in_process.py prepare_metadata_for_build_wheel /tmp/tmpfq576nu4
         cwd: /tmp/pip-req-build-x_y8503g
    Complete output (11 lines):
    running dist_info
    creating /tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info
    writing /tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info/PKG-INFO
    writing dependency_links to /tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info/dependency_links.txt
    writing requirements to /tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info/requires.txt
    writing top-level names to /tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info/top_level.txt
    writing manifest file '/tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info/SOURCES.txt'
    reading manifest file '/tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info/SOURCES.txt'
    writing manifest file '/tmp/pip-modern-metadata-fcs9_3es/amdsmi.egg-info/SOURCES.txt'
    creating '/tmp/pip-modern-metadata-fcs9_3es/amdsmi.dist-info'
    error: invalid command 'bdist_wheel'
    ----------------------------------------
WARNING: Discarding file:///opt/rocm-6.3.0/share/amd_smi. Command errored out with exit status 1: /bin/python3 /usr/lib/python3.9/site-packages/pip/_vendor/pep517/in_process/_in_process.py prepare_metadata_for_build_wheel /tmp/tmpfq576nu4 Check the logs for full command output.
ERROR: Command errored out with exit status 1: /bin/python3 /usr/lib/python3.9/site-packages/pip/_vendor/pep517/in_process/_in_process.py prepare_metadata_for_build_wheel /tmp/tmpfq576nu4 Check the logs for full command output.
[WARNING] Could not find argcomplete or argcomplete3.  Argument completion will not work...
Removed "/etc/systemd/system/timers.target.wants/logrotate.timer".
Created symlink /etc/systemd/system/timers.target.wants/logrotate.timer → /usr/lib/systemd/system/logrotate.timer.

  Verifying        : python3-pip-21.2.3-8.el9.noarch                                            1/3 
  Verifying        : amd-smi-lib-24.7.1.60300-39.el9.x86_64                                     2/3 
  Verifying        : rocm-core-6.3.0.60300-39.el9.x86_64                                        3/3 
Installed products updated.

Installed:
  amd-smi-lib-24.7.1.60300-39.el9.x86_64               python3-pip-21.2.3-8.el9.noarch              
  rocm-core-6.3.0.60300-39.el9.x86_64                 

Complete!
[root@vm-10-0-186-164 ~]# 



---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-12-09T16:29:45Z)

Hi @prarit, thanks for the report. Was able to reproduce this issue am looking into this further.

---

### 评论 #2 — harkgill-amd (2024-12-12T19:27:01Z)

@prarit, the error during amd-smi installation is caused by missing `python3-setuptools` and `python3-wheel` packages. As a temporary workaround, you can install these packages prior to ROCm/amd-smi installation as highlighted [here](https://github.com/ROCm/amdsmi?tab=readme-ov-file#required-software). We will be adding these packages as dependencies for amd-smi in an upcoming patch and also temporarily updating our ROCm installation documentation to notify users of this requirement.

---

### 评论 #3 — harkgill-amd (2025-01-13T20:08:19Z)

The `python3-setuptools` and `python3-wheel` packages have been added as both a [prerequisite](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#kernel-headers-and-development-packages) and in the [quick start installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html), resolving the `error: invalid command 'bdist_wheel'` errors.

There are also fixes planned for a future ROCm release that will no longer require that these packages be installed prior to installation. I will close out this issue as with the current documentation updates, the errors are on longer seen. If you have any questions or concerns, please leave a comment and I'll re-open this ticket. Thanks!

---

### 评论 #4 — dtrifiro (2025-04-04T10:06:52Z)

@harkgill-amd this is still broken in 6.3.4:


```Dockerfile
# syntax=docker/dockerfile:1
FROM registry.access.redhat.com/ubi9/ubi-minimal:9.5 AS rocm_base
ARG ROCM_VERSION=6.3.4

RUN printf "[amdgpu]\n\
name=amdgpu\n\
baseurl=https://repo.radeon.com/amdgpu/${ROCM_VERSION}/rhel/9.5/main/x86_64/\n\
enabled=1\n\
priority=50\n\
gpgcheck=1\n\
gpgkey=https://repo.radeon.com/rocm/rocm.gpg.key\n\
[ROCm-${ROCM_VERSION}]\n\
name=ROCm${ROCM_VERSION}\n\
baseurl=https://repo.radeon.com/rocm/rhel9/${ROCM_VERSION}/main\n\
enabled=1\n\
priority=50\n\
gpgcheck=1\n\
gpgkey=https://repo.radeon.com/rocm/rocm.gpg.key"> /etc/yum.repos.d/amdgpu.repo

FROM rocm_base as amdsmi_only_failure
RUN microdnf -y install amd-smi-lib


FROM rocm_base as install_failure
RUN microdnf -y install python-setuptools python-wheel python-pip amd-smi-lib


FROM install_failure as retry_success
RUN microdnf -y reinstall amd-smi-lib


FROM rocm_base as install_success
RUN microdnf -y install python-setuptools python-wheel python-pip && \
    microdnf -y install amd-smi-lib
```

if you build the `amdsmi_only_failure` stage, `microdnf` will return `0` but it will fail to install `amdsmi` with:

```
#9 11.90 Using pyproject.toml for installation due to setuptools version 53.0.0
#9 12.11   ERROR: Command errored out with exit status 1:
#9 12.11    command: /bin/python3 /usr/lib/python3.9/site-packages/pip/_vendor/pep517/in_process/_in_process.py prepare_metadata_for_build_wheel /tmp/tmpzihg6y9w
#9 12.11        cwd: /opt/rocm-6.3.4/share/amd_smi
#9 12.11   Complete output (11 lines):
#9 12.11   running dist_info
#9 12.11   creating /tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info
#9 12.11   writing /tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info/PKG-INFO
#9 12.11   writing dependency_links to /tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info/dependency_links.txt
#9 12.11   writing requirements to /tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info/requires.txt
#9 12.11   writing top-level names to /tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info/top_level.txt
#9 12.11   writing manifest file '/tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info/SOURCES.txt'
#9 12.11   reading manifest file '/tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info/SOURCES.txt'
#9 12.11   writing manifest file '/tmp/pip-modern-metadata-bp9brwrp/amdsmi.egg-info/SOURCES.txt'
#9 12.11   creating '/tmp/pip-modern-metadata-bp9brwrp/amdsmi.dist-info'
#9 12.11   error: invalid command 'bdist_wheel'
#9 12.11   ----------------------------------------
#9 12.11 WARNING: Discarding file:///opt/rocm-6.3.4/share/amd_smi. Command errored out with exit status 1: /bin/python3 /usr/lib/python3.9/site-packages/pip/_vendor/pep517/in_process/_in_process.py prepare_metadata_for_build_wheel /tmp/tmpzihg6y9w Check the logs for full command output.
#9 12.11 ERROR: Command errored out with exit status 1: /bin/python3 /usr/lib/python3.9/site-packages/pip/_vendor/pep517/in_process/_in_process.py prepare_metadata_for_build_wheel /tmp/tmpzihg6y9w Check the logs for full command output.
#9 12.14 [WARNING] Could not find argcomplete or argcomplete3.  Argument completion will not work...
#9 12.15 [WARNING] Detected logrotate is not installed. amd-smi-lib logs (when turned on) will not rotate properly.
#9 12.15 Installing: python3-wheel;1:0.36.2-8.el9;noarch;ubi-9-codeready-builder-rpms
#9 12.25 Complete.
```


if you build the `install_failure` stage, it will also fails with the above error.

Installing the dependencies before installing the package itself will succeed though (see `retry_success` and `install_success` stages)

---
