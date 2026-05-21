# [Issue]: Can't install `rocm-hip-runtime-dev` on `ubuntu:22.04` in GitHub Actions

> **Issue #3946**
> **状态**: closed
> **创建时间**: 2024-10-25T16:20:23Z
> **更新时间**: 2024-10-25T18:11:21Z
> **关闭时间**: 2024-10-25T18:11:20Z
> **作者**: nazar-pc
> **标签**: ROCm 6.2.2, -
> **URL**: https://github.com/ROCm/ROCm/issues/3946

## 标签

- **ROCm 6.2.2** (颜色: #ededed)
- **-** (颜色: #ededed)

## 描述

### Problem Description

I'm not exactly sure why, but this doesn't work on GitHub Actions official runners:
```
sudo mkdir -p --mode=0755 /etc/apt/keyrings
curl -L https://repo.radeon.com/rocm/rocm.gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/rocm.gpg > /dev/null
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/$ROCM_VERSION jammy main" | sudo tee /etc/apt/sources.list.d/rocm.list > /dev/null
echo "Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600" | sudo tee /etc/apt/preferences.d/rocm-pin-600 > /dev/null
sudo apt-get update
DEBIAN_FRONTEND=noninteractive sudo apt-get -o Debug::pkgProblemResolver=true install -y --no-install-recommends rocm-hip-runtime-dev
```

Similar commands work on Ubuntu 20.04 and also work inside of Ubuntu 22.04 container image, but not on GitHub Actions host.

Not sure if this is an issue in GitHub Actions runner image because I don't have such problems with other software.

Here is what the output looks like:
```
Reading package lists...
Building dependency tree...
Reading state information...
Starting pkgProblemResolver with broken count: 1
Starting 2 pkgProblemResolver with broken count: 1
Investigating (0) rocm-hip-runtime-dev:amd64 < none -> 6.2.2.60202-116~22.04 @un puN Ib >
Broken rocm-hip-runtime-dev:amd64 Depends on rocm-core:amd64 < none | 6.2.2.60202-116~22.04 @un uH > (= 6.2.2.60202-116~22.04)
  Considering rocm-core:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated rocm-core:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on rocm-device-libs:amd64 < none | 5.0.0-1 @un uH > (= 1.0.0.60202-116~22.04)
  Considering rocm-device-libs:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated rocm-device-libs:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on rocm-hip-runtime:amd64 < none | 6.2.2.60202-116~22.04 @un uH > (= 6.2.2.60202-116~22.04)
  Considering rocm-hip-runtime:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated comgr:amd64
  Re-Instated rocprofiler-register:amd64
  Re-Instated hsa-rocr:amd64
  Re-Instated openmp-extras-runtime:amd64
  Re-Instated rocm-language-runtime:amd64
    Reinst Failed early because of rocminfo:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on rocm-cmake:amd64 < none | 5.0.0-1 @un uH > (= 0.13.0.60202-116~22.04)
  Considering rocm-cmake:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated rocm-cmake:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on rocm-llvm:amd64 < none | 18.0.0.24355.60202-116~22.04 @un uH > (= 18.0.0.24355.60202-116~22.04)
  Considering rocm-llvm:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated rocm-llvm:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on hipcc:amd64 < none | 1.1.1.60202-116~22.04 @un uH > (= 1.1.1.60202-116~22.04)
  Considering hipcc:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated libfile-copy-recursive-perl:amd64
  Re-Instated libfile-listing-perl:amd64
  Re-Instated libfile-which-perl:amd64
  Re-Instated libhsakmt1:amd64
  Re-Instated libhsa-runtime64-1:amd64
  Re-Instated rocminfo:amd64
  Re-Instated hip-runtime-amd:amd64
    Reinst Failed early because of libdrm-amdgpu-dev:amd64
  Re-Instated libpciaccess-dev:amd64
  Re-Instated libdrm-dev:amd64
  Re-Instated hsakmt-roct-dev:amd64
  Re-Instated hsa-rocr-dev:amd64
  Re-Instated hip-dev:amd64
  Re-Instated hipcc:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on hipify-clang:amd64 < none | 18.0.0.60202-116~22.04 @un uH > (= 18.0.0.60202-116~22.04)
  Considering hipify-clang:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated hipify-clang:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on hip-doc:amd64 < none | 6.2.41134.60202-116~22.04 @un uH > (= 6.2.41134.60202-116~22.04)
  Considering hip-doc:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated hip-doc:amd64
Broken rocm-hip-runtime-dev:amd64 Depends on hip-samples:amd64 < none | 6.2.41134.60202-116~22.04 @un uH > (= 6.2.41134.60202-116~22.04)
  Considering hip-samples:amd64 0 as a solution to rocm-hip-runtime-dev:amd64 9999
  Re-Instated hip-samples:amd64
Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 rocm-hip-runtime-dev : Depends: rocm-device-libs (= 1.0.0.60202-116~22.04) but 5.0.0-1 is to be installed
                        Depends: rocm-hip-runtime (= 6.2.2.60202-116~22.04) but it is not going to be installed
                        Depends: rocm-cmake (= 0.13.0.60202-116~22.04) but 5.0.0-1 is to be installed
E: Unable to correct problems, you have held broken packages.
```

CI run logs: https://github.com/nazar-pc/subspace/actions/runs/11521636442/job/32075733370

### Operating System

Ubuntu 22.04

### ROCm Version

ROCm 6.2.2


---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-10-25T18:09:37Z)

Hi, @nazar-pc, I was able to reproduce your issue following the steps you provided. It looks like the pinning done by 
```
echo "Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600" | sudo tee /etc/apt/preferences.d/rocm-pin-600 > /dev/null
```
```
cat /etc/apt/preferences.d//rocm-pin-600
Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600
```

does not correctly set the priority of repo.radeon.com resulting in the ROCm packages hosted in the Ubuntu's repo being set as the installation candidates.

When setting the pinning priority correctly as done below ([ref](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/ubuntu.html#register-rocm-packages)), the correct versions of the package are installed and the dependency issues are resolved.

```
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' \
    | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update
```
```
cat /etc/apt/preferences.d//rocm-pin-600
Package: *
Pin: release o=repo.radeon.com
Pin-Priority: 600
```
You can also check if the pinning was successful by running `apt policy` which should show the following.
```
 600 https://repo.radeon.com/rocm/apt/6.2.2 jammy/main amd64 Packages
     release v=6.2.2,o=repo.radeon.com,a=jammy,n=jammy,l=repo.radeon.com,c=main,b=amd64
     origin repo.radeon.com
```

---

### 评论 #2 — nazar-pc (2024-10-25T18:11:20Z)

Right, I forgot that Dockerfile has a special syntax that is different from regular shell when I copy-pasted it.
Thanks!

---
