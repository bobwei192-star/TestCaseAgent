# [Issue]: Ubuntu `rocm-hip-runtime` package depends on both `hsa-rocr-dev` and `libhsa-runtime-dev` and provide two incompatible `hsa.h`

> **Issue #3306**
> **状态**: closed
> **创建时间**: 2024-06-17T04:50:26Z
> **更新时间**: 2024-08-29T13:44:38Z
> **关闭时间**: 2024-08-29T13:25:26Z
> **作者**: illwieckz
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3306

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I'm running ROCm 6.1.2 on Ubuntu 23.10 Mantic. The GPU is an `AMD Radeon PRO W7600` but it doesn't matter because the issue is a packaging issue affecting packages provided by [repo.radeon.com](https://repo.radeon.com).

- The `/usr/include/hsa/hsa.h` file is provided by the stock Ubuntu `libhsa-runtime-dev` package.
- The `/opt/rocm-6.1.2/include/hsa/hsa.h` file is provided by the AMD `hsa-rocr-dev` package.
- The AMD `rocm-hip-runtime` package depends on both `hsa-rocr-dev` and `libhsa-runtime-dev`…

We can see the dependency relation here:

```
$ debtree rocm-hip-runtime 2>/dev/null | grep -E -- '-> "hip-runtime-amd|-> "hsa-rocr-dev|-> "hipcc|-> "libamdhip64-dev|-> "libhsa-runtime-dev'
	"rocm-hip-runtime" -> "hip-runtime-amd" [color=blue,label="(= 6.1.40093.60102-119~22.04)"];
	"hip-runtime-amd" -> "hsa-rocr-dev" [color=blue,label="(>= 1.3)"];
	"hip-runtime-amd" -> "hipcc" [color=blue];
	"hipcc" -> "libamdhip64-dev" [color=blue];
	"libamdhip64-dev" -> "libhsa-runtime-dev" [color=blue];
```

Here can be see the origin of each packages:

```
$ apt-get install --reinstall rocm-hip-runtime hip-runtime-amd hsa-rocr-dev hipcc libhsa-runtime-dev
Get:1 http://archive.ubuntu.com/ubuntu mantic/universe amd64 hipcc amd64 5.2.3-12 [25,1 kB]
Get:2 http://archive.ubuntu.com/ubuntu mantic/universe amd64 libhsa-runtime-dev amd64 5.2.3-5 [73,3 kB]
Get:3 https://repo.radeon.com/rocm/apt/6.1.2 jammy/main amd64 hip-runtime-amd amd64 6.1.40093.60102-119~22.04 [27,1 MB]
Get:4 https://repo.radeon.com/rocm/apt/6.1.2 jammy/main amd64 hsa-rocr-dev amd64 1.13.0.60102-119~22.04 [102 kB]
Get:5 https://repo.radeon.com/rocm/apt/6.1.2 jammy/main amd64 rocm-hip-runtime amd64 6.1.2.60102-119~22.04 [2 042 B]
```

A more readable dependency tree can be:

```
─ rocm-hip-runtime 6.1.2.60102-119~22.04 (AMD repository)
  └ hip-runtime-amd 6.1.40093.60102-119~22.04 (AMD repository)
    ├ hsa-rocr-dev 1.13.0.60102-119~22.04 (AMD repository)
    │ └ /opt/rocm-6.1.2/include/hsa/hsa.h
    └ hipcc 1.0.0.60102-119~22.04 (Ubuntu repository)
      └ libhsa-runtime-dev 5.0.0-1 (Ubuntu repository)
        └ /usr/include/hsa/hsa.h
```

The `/opt/rocm-6.1.2/include/hsa/hsa.h` file provides `hsa_amd_agent_info_s::HSA_AMD_AGENT_INFO_TIMESTAMP_FREQUENCY` but `/usr/include/hsa/hsa.h` isn't.

This is something I found while debugging a build problem with LLVM:

- https://github.com/llvm/llvm-project/pull/95484

### Operating System

Ubuntu 23.10 Mantic Minautor

### CPU

AMD Ryzen Threadripper PRO 3955WX 16-Cores

### GPU

AMD Radeon Pro W7600

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

```
apt-get install --reinstall rocm-hip-runtime
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2024-07-17T18:24:28Z)

@illwieckz Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — ppanchad-amd (2024-08-14T14:32:21Z)

@illwieckz Looks like hipcc is getting installed from default Ubuntu repo instead of ROCm repo. 

Please follow the steps given in our documentation, especially setting the repo priority.
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/ubuntu.html

Specifically the following step: 
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' \
    | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update

Please let us know if that solves your issue. Thanks!

---

### 评论 #3 — illwieckz (2024-08-29T13:25:26Z)

In ROCm 6.2 on Ubuntu, the `rocm-hip-runtime` package no longer depends on `hipcc`, and then doesn't depend on `libhsa-runtime-dev` and then `/usr/include/hsa/hsa.h` doesn't exist.

I assume the bug is now fixed.

As written [here](https://github.com/ROCm/ROCm/issues/3654#issuecomment-2317301157) I can provide more help in a more efficient way:

> ℹ️ AMD has [publicly announced](https://www.phoronix.com/news/AMD-Unified-Linux-Jobs) in June they were looking for people to help them improve the Linux packaging of their ROCm stack. I'm ready to help either as an employee or as an external contractor (see my entreprise [rebatir.fr](https://rebatir.fr) and the [I love compute](https://gitlab.com/illwieckz/i-love-compute) initiative as reference). The AMD's application website is very limited and inefficient so I'm not surprised if my application got lost. It is obvious the need is still there at AMD and I'm still available for help.

---
