# [Issue]: Ubuntu 24.04 LTS Docker image dependencies fail

> **Issue #5831**
> **状态**: closed
> **创建时间**: 2026-01-03T18:31:40Z
> **更新时间**: 2026-01-15T15:39:30Z
> **关闭时间**: 2026-01-15T15:39:30Z
> **作者**: tedbrosby
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5831

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I already reviewed: https://github.com/ROCm/ROCm/issues/5797 
And the suggested solutions don't help me. 

I've tried: 
`RUN echo "Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600\n" > /etc/apt/preferences.d/rocm-pin-600` 

And I get `bash: /etc/apt/preferences.d/rocm-pin-600: Permission denied` 

I ran it on sudo with 
`echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' | sudo tee /etc/apt/preferences.d/rocm-pin-600` 
And got the following output 
```
Package: *
Pin: release o=repo.radeon.com
Pin-Priority: 600
```
I still get the following output:
```
16.16 The following packages have unmet dependencies:
16.20  rocm-dev : Depends: rocm-cmake (= 0.14.0.60401-83~22.04) but 5.0.0-1 is to be installed
16.20             Depends: rocm-device-libs (= 1.0.0.60401-83~22.04) but 5.0.0-1 is to be installed
16.20             Depends: rocm-utils (= 6.4.1.60401-83~22.04) but it is not going to be installed
16.20 E: Unable to correct problems, you have held broken packages.
------

 1 warning found (use docker --debug to expand):
 - LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format (line 55)
Dockerfile:23
--------------------
  22 |     RUN echo "$APT_PREF" > /etc/apt/preferences.d/rocm-pin-600
  23 | >>> RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
  24 | >>>   curl -sL http://repo.radeon.com/rocm/rocm.gpg.key | apt-key add - && \
  25 | >>>   sh -c 'echo deb [arch=amd64] http://repo.radeon.com/rocm/apt/$ROCM_VERSION/ jammy main > /etc/apt/sources.list.d/rocm.list' && \
  26 | >>>   sh -c 'echo deb [arch=amd64] https://repo.radeon.com/amdgpu/$AMDGPU_VERSION/ubuntu jammy main > /etc/apt/sources.list.d/amdgpu.list' && \
  27 | >>>   apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  28 | >>>   sudo \
  29 | >>>   libelf1 \
  30 | >>>   libnuma-dev \
  31 | >>>   build-essential \
  32 | >>>   git \
  33 | >>>   vim-nox \
  34 | >>>   cmake-curses-gui \
  35 | >>>   kmod \
  36 | >>>   file \
  37 | >>>   python3 \
  38 | >>>   python3-pip \
  39 | >>>   rocm-dev && \
  40 | >>>   apt-get clean && \
  41 | >>>   rm -rf /var/lib/apt/lists/*
  42 |     
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl gnupg &&   curl -sL http://repo.radeon.com/rocm/rocm.gpg.key | apt-key add - &&   sh -c 'echo deb [arch=amd64] http://repo.radeon.com/rocm/apt/$ROCM_VERSION/ jammy main > /etc/apt/sources.list.d/rocm.list' &&   sh -c 'echo deb [arch=amd64] https://repo.radeon.com/amdgpu/$AMDGPU_VERSION/ubuntu jammy main > /etc/apt/sources.list.d/amdgpu.list' &&   apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends   sudo   libelf1   libnuma-dev   build-essential   git   vim-nox   cmake-curses-gui   kmod   file   python3   python3-pip   rocm-dev &&   apt-get clean &&   rm -rf /var/lib/apt/lists/*" did not complete successfully: exit code: 100
```
Please don't mark this as assessed unless I verify a solution has worked... The last ticket hasn't gotten responses after the status changed. 

### Operating System

Ubuntu 24.04.3 LTS

### CPU

AMD Ryzen 7 9700x

### GPU

AMD Radeon R9700 AI Pro

### ROCm Version

7.1.1

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

### 评论 #1 — harkgill-amd (2026-01-05T15:29:12Z)

Hey @tedbrosby, I see you're using the build argument `$APT_PREF` as done in our [Dockerfile-ubuntu-24.04-complete image](https://github.com/ROCm/ROCm-docker/blob/master/dev/Dockerfile-ubuntu-24.04-complete) image. When configuring your dockerfile in this way, you'd have to pass in the actual value for this argument in your docker build command - for example,
```
sudo docker build --build-arg APT_PREF=$'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600\n' -t rocm-dev .
```
If you'd rather a hardcoded image where you don't have to pass in any parameters, here's the working dockerfile I ended up with after https://github.com/ROCm/ROCm/issues/5797,
```
FROM ubuntu:24.04

ARG ROCM_VERSION=7.1.1
ARG AMDGPU_VERSION=30.20.1

RUN apt-get clean && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y wget ca-certificates curl  \
    build-essential  software-properties-common cmake g++-12 libstdc++-12-dev rpm libelf-dev libnuma-dev sudo  \
    libdw-dev git python3 python3-pip gnupg unzip ripgrep libelf1 file pkg-config xxd ninja-build zsh git npm  \
    python3.12-venv nodejs kmod
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 20 --slave /usr/bin/g++ g++ /usr/bin/g++-12

RUN echo "Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600\n" > /etc/apt/preferences.d/rocm-pin-600
RUN curl -sL https://repo.radeon.com/rocm/rocm.gpg.key | apt-key add - \
  && printf "deb [arch=amd64] https://repo.radeon.com/rocm/apt/$ROCM_VERSION/ noble main" |  \
    tee --append /etc/apt/sources.list.d/rocm.list \
  && printf "deb [arch=amd64] https://repo.radeon.com/amdgpu/$AMDGPU_VERSION/ubuntu noble main" |  \
    tee /etc/apt/sources.list.d/amdgpu.list \
  && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends  \
    rocm-libs  \
    rocm-dev  \
    rocm-llvm-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
```
Let me know if either of these solutions work out on your end. If the error still persists, please share your complete dockerfile and your docker build command.

---

### 评论 #2 — harkgill-amd (2026-01-15T15:39:30Z)

Closing this one out for now but if the issue does persist, please leave a comment and I'll reopen this ticket. 

---
