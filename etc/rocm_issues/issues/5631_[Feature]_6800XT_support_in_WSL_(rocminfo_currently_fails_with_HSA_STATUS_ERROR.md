# [Feature]: 6800XT support in WSL (rocminfo currently fails with HSA_STATUS_ERROR_OUT_OF_RESOURCES)

> **Issue #5631**
> **状态**: closed
> **创建时间**: 2025-11-05T20:50:10Z
> **更新时间**: 2025-11-11T20:45:06Z
> **关闭时间**: 2025-11-11T20:45:06Z
> **作者**: pajocar23
> **标签**: Feature Request, AMD Radeon RX 6800 XT, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5631

## 标签

- **Feature Request** (颜色: #fbca04)
- **AMD Radeon RX 6800 XT** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

### Summary

When following the official AMD guide for installing ROCm on WSL 2, the post-install verification check using `rocminfo` fails with an `HSA_STATUS_ERROR_OUT_OF_RESOURCES` error. This suggests the runtime is unable to allocate the necessary resources, even though the installation appears to have completed.

### System Environment

  * **GPU:** AMD Radeon RX 6800 XT
  * **Environment:** WSL 2
  * **WSL Distro:** Ubuntu 22.04.3 LTS
  * **ROCm Version:** 7.1.0 (installed via `apt`)

### Steps to Reproduce

1.  Set up a fresh Ubuntu 22.04.3 environment in WSL 2.
2.  Follow the official installation guide: [https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html)
3.  After installation, run the post-install verification check:
    ```bash
    rocminfo
    ```

### Expected Behavior

`rocminfo` should execute successfully and print a list of HSA agents and system information, confirming the GPU is recognized.

### Actual Behavior

The command fails with the following error:

```
WSL environment detected.
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:1324
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```

-----

### Diagnostic Information

**Installed ROCm Packages (`apt list --installed | grep rocm`):**

```
rocm-cmake/now 0.14.0.70100-20~22.04 amd64 [installed,upgradable to: 5.0.0-1]
rocm-core/now 7.1.0.70100-20~22.04 amd64 [installed,local]
rocm-dbgapi/now 0.77.4.70100-20~22.04 amd64 [installed,local]
rocm-debug-agent/now 2.1.0.70100-20~22.04 amd64 [installed,local]
rocm-developer-tools/now 7.1.0.70100-20~22.04 amd64 [installed,local]
rocm-device-libs/now 1.0.0.70100-20~22.04 amd64 [installed,upgradable to: 5.0.0-1]
rocm-gdb/now 16.3.70100-20~22.04 amd64 [installed,local]
rocm-hip/now 7.1.0.70100-20~22.04 amd64 [installed,local]
rocm-language-runtime/now 7.1.0.70100-20~22.04 amd64 [installed,local]
rocm-llvm/now 20.0.0.25425.70100-20~22.04 amd64 [installed,local]
rocm-opencl-dev/now 2.0.0.70100-20~22.04 amd64 [installed,local]
rocm-opencl-sdk/now 7.1.0.70100-20~22.04 amd64 [installed,local]
rocm-opencl/now 2.0.0.70100-20~22.04 amd64 [installed,local]
rocm-openmp/now 7.1.0.70100-20~22.04 amd64 [installed,local]
rocm-smi-lib/now 7.8.0.70100-20~22.04 amd64 [installed,local]
rocm/now 7.1.0.70100-20~22.04 amd64 [installed,local]
rocminfo/now 1.0.0.70100-20~22.04 amd64 [installed,upgradable to: 5.0.0-1]
```

**OS and Architecture (`uname -m && cat /etc/*release`):**

```
x86_64
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.3 LTS"
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

### Operating System

Ubuntu 22.04.03 LTS

### CPU

AMD Ryzen 9 5900X 12-Core Processor  (3.70 GHz)

### GPU

AMD Radeon RX 6800XT

### ROCm Version

ROCm latest, according to this guide https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html#post-install-verification-check

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — schung-amd (2025-11-05T21:58:50Z)

Thanks @pajocar23. Will look into it.

---

### 评论 #2 — schung-amd (2025-11-06T20:40:55Z)

@pajocar23 First of all, I think you may have missed some of the installation instructions. ROCm on WSL requires a specific combination of Adrenalin driver and ROCm versions, the latter of which should be 6.4.2 and not 7.1. 

Unfortunately, however, I think the real underlying issue here is that the 6800XT is not supported in WSL at this time; see https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html. I suspect that the error message is due to a known issue we're looking into where, if it cannot detect a compatible GPU on Windows, rocm_agent_enumerator hangs and then emits the HSA_STATUS_ERROR_OUT_OF_RESOURCES rather than a sensible error message; see https://github.com/ROCm/rocm-systems/issues/1153.

I'm not sure if we have plans to enable the 6800XT in ROCm + WSL at this time. I've marked this as a feature request for now and will rename appropriately. I'll leave this open for now but may close against a duplicate at some point (I'm sure there are several requests for 6800XT support floating around at the moment).

Normally I would refer issues such as these to TheRock (https://github.com/ROCm/TheRock) as we have expanded hardware support in that project (and builds for native Windows rather than needing to use WSL), but it doesn't look like we have passing builds for the 6800XT there either at this time. That being said, support for the 6800XT is definitely on our radar on that side of things; see https://github.com/ROCm/TheRock/pull/1629. 

---

### 评论 #3 — pajocar23 (2025-11-11T20:45:06Z)

@schung-amd Okay Schung.
It is not supported, i get it.
Thanks for your help anyway

---
