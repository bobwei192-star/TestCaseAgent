# [Issue]: Ubuntu 24.04 APT Issues

> **Issue #5797**
> **状态**: closed
> **创建时间**: 2025-12-19T14:41:37Z
> **更新时间**: 2026-01-05T15:31:26Z
> **关闭时间**: 2026-01-05T15:31:26Z
> **作者**: matinraayai
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5797

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Hi,
I've been having issues installing packages using the ROCm APT repositories for quite some time now.
I use the following `Dockerfile`:
```docker

# Build Arguments
ARG ROCM_VERSION=7.1.1
# Install dependencies
RUN apt-get clean && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y wget ca-certificates curl  \
    build-essential  software-properties-common cmake g++-12 libstdc++-12-dev rpm libelf-dev libnuma-dev sudo  \
    libdw-dev git python3 python3-pip gnupg unzip ripgrep libelf1 file pkg-config xxd ninja-build zsh git npm  \
    python3.12-venv nodejs kmod
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 20 --slave /usr/bin/g++ g++ /usr/bin/g++-12

# ROCm installation
RUN echo "Package: *\nPin: origin ""\nPin-Priority: 600" > /etc/apt/preferences.d/rocm-pin-600
RUN curl -sL https://repo.radeon.com/rocm/rocm.gpg.key | apt-key add - \
  && printf "deb [arch=amd64] https://repo.radeon.com/rocm/apt/$ROCM_VERSION/ noble main" |  \
    tee --append /etc/apt/sources.list.d/rocm.list \
  && printf "deb [arch=amd64] https://repo.radeon.com/amdgpu/$ROCM_VERSION/ubuntu noble main" |  \
    tee /etc/apt/sources.list.d/amdgpu.list \
  && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends  \
    rocm-libs$ROCM_VERSION  \
    rocm-dev$ROCM_VERSION  \
    rocm-llvm-dev$ROCM_VERSION && apt-get clean && rm -rf /var/lib/apt/lists/*
```

As you can see I install ROCm packages with their version name appended at the end (e.g. rocm-libs7.1.1 instead of installing rocm-libs) because otherwise I would get broken dependencies:
```
5.821 The following packages have unmet dependencies:
5.932  rocm-dev : Depends: hipcc (= 1.1.1.70101-38~24.04) but 5.7.1-3 is to be installed
5.932             Depends: rocm-cmake (= 0.14.0.70101-38~24.04) but 6.0.0-1 is to be installed
5.932             Depends: rocm-utils (= 7.1.1.70101-38~24.04) but it is not going to be installed
5.939 E: Unable to correct problems, you have held broken packages.
```

Please fix the broken dependency issue in next ROCm releases.

Thank you

### Operating System

Ubuntu 24.04

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

Simply remove the $ROCM_VERSION from the package name and attempt to build the container.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2025-12-22T17:38:22Z)

Hi @matinraayai, the errors you're seeing without the `$ROCM_VERSION` are due to faulty pinning at,
```
RUN echo "Package: *\nPin: origin ""\nPin-Priority: 600" > /etc/apt/preferences.d/rocm-pin-600
```
In theory, this pinning should override the Ubuntu packages and always select the ROCm repo packages but it's failing and causing the "`but <Ubuntu Package version> is to be installed`" errors. Switching this line to the following succesfully pins the ROCm repo,
```
RUN echo "Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600\n" > /etc/apt/preferences.d/rocm-pin-600
```

Related to https://github.com/ROCm/ROCm/issues/5798, the `amdgpu` repo should also be setup as the following,
```
ARG AMDGPU_VERSION=30.20.1
...
&& printf "deb [arch=amd64] https://repo.radeon.com/amdgpu/$AMDGPU_VERSION/ubuntu noble main"
```
With these changes, I was able to build your image without the rocm version suffixes on the packages. Give this a try and let me know if you have any questions. As a side note, you can always refer to our release docker images for guidance on how to build your own image or pull these instead.
- https://github.com/ROCm/ROCm-docker/blob/master/dev/Dockerfile-ubuntu-24.04-complete. 
- https://hub.docker.com/layers/rocm/dev-ubuntu-24.04/7.1/images/sha256-ee3f9aaaadb53c865cc06c8b570e201179191e56f5ed366d365e16581533c6e8

---

### 评论 #2 — cvocvo (2025-12-23T20:18:41Z)

Notably I'm running into a nearly identical version of this problem on a regular, fresh install of Ubuntu 24.04.3 LTS on bare metal hardware (no docker).

Configuring the pin priority as you suggested seems to have resolved the issue and allowed ROCm 7.1.1 to install correctly:
```
sudo tee /etc/apt/preferences.d/rocm-pin-600 <<EOF
Package: *
Pin: release o=repo.radeon.com
Pin-Priority: 600
EOF
```
After running that, I was able to verify via `apt-cache policy rocm` and then re-run the installer like this:
```
sudo apt update
sudo apt --fix-broken install
sudo apt install rocm
```


---

### 评论 #3 — tedbrosby (2026-01-03T17:57:40Z)

I'm having the exact same problem as above, unfortunately the sudo tee information didn't resolve it for me. 

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

Here's my output from apt-cache policy rocm

```
rocm:
  Installed: 7.1.1.70101-38~24.04
  Candidate: 7.1.1.70101-38~24.04
  Version table:
 *** 7.1.1.70101-38~24.04 600
        600 https://repo.radeon.com/rocm/apt/7.1.1 noble/main amd64 Packages
        100 /var/lib/dpkg/status
```

I'm honestly regretting buying this R9700 Pro AI and thankfully I'm in the return policy. 

---

### 评论 #4 — harkgill-amd (2026-01-05T15:31:26Z)

Just left a reply on https://github.com/ROCm/ROCm/issues/5831. Will close this issue out in favor of the newly opened ticket. If anyone else does still see these errors after applying the pinning, feel free to leave a comment on either of the tickets. 

---
