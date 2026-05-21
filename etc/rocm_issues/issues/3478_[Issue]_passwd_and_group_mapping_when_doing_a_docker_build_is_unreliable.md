# [Issue]: passwd and group mapping when doing a docker build is unreliable

> **Issue #3478**
> **状态**: open
> **创建时间**: 2024-07-31T10:26:46Z
> **更新时间**: 2024-08-07T15:18:07Z
> **作者**: sogartar
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3478

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

In the [instructions ](https://github.com/ROCm/ROCm/tree/62dd3820a2db180885306b3546cc9dfd82c787dc?tab=readme-ov-file#build-rocm-from-source) for building inside docker `/etc/passwd` and `/etc/group` are mapped from the host into the docker image. This is done in order to produce artifacts that match the current user on the host machine.

```
docker run -ti \
    -e ROCM_VERSION=${ROCM_VERSION} \
    -e CCACHE_DIR=$HOME/.ccache \
    -e CCACHE_ENABLED=true \
    -e DOCK_WORK_FOLD=/src \
    -w /src \
    -v $PWD:/src \
    -v /etc/passwd:/etc/passwd \
    -v /etc/shadow:/etc/shadow \
    -v ${HOME}/.ccache:${HOME}/.ccache \
    -u $(id -u):$(id -g) \
    rocm/rocm-build-ubuntu-22.04:6.1 bash
```

On some systems the user and group information is not available there but is dynamically generated. Then inside the container for example this fails

```
I have no name!@d74b9c0258ac:/src$ whoami
whoami: cannot find name for user ID 10116
I have no name!@d74b9c0258ac:/src$ echo $?
1
```
Having such a central thing fail means that all bets are off after that.

What needs to happen is something like

```
fake_group="$PWD/group"
fake_passwd="$PWD/passwd"

getent group > "${fake_group}"
getent passwd > "${fake_passwd}"

docker run -ti \
    -e ROCM_VERSION=${ROCM_VERSION} \
    -e CCACHE_DIR=$HOME/.ccache \
    -e CCACHE_ENABLED=true \
    -e DOCK_WORK_FOLD=/src \
    -w /src \
    -v $PWD:/src \
    --mount="type=bind,src=${fake_group},dst=/etc/group,readonly" \
    --mount="type=bind,src=${fake_passwd},dst=/etc/passwd,readonly" \
    -v ${HOME}/.ccache:${HOME}/.ccache \
    -u $(id -u):$(id -g) \
    rocm/rocm-build-ubuntu-22.04:6.1 bash
```

For more info on the source of that pattern see [this](https://github.com/iree-org/iree/blob/97fbe5f36d7a82a85838b68622d64ab43790d749/build_tools/docker/docker_run.sh#L41).

### Operating System

Ubuntu 22.04

### CPU

AMD EPYC 9454 48-Core Processor

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.1.0

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

### 评论 #1 — ppanchad-amd (2024-08-07T15:18:06Z)

@sogartar Internal ticket has been created to fix this issue. Thanks!

---
