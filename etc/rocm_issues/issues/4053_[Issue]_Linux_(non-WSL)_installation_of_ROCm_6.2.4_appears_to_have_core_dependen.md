# [Issue]: Linux (non-WSL) installation of ROCm 6.2.4 appears to have core dependencies upon libdxcore.so (WSL specific)

> **Issue #4053**
> **状态**: closed
> **创建时间**: 2024-11-23T19:00:20Z
> **更新时间**: 2026-02-03T17:51:52Z
> **关闭时间**: 2024-12-09T15:12:38Z
> **作者**: joelandman
> **标签**: Under Investigation, ROCm 6.2.3, Radeon 780M Graphics
> **URL**: https://github.com/ROCm/ROCm/issues/4053

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **Radeon 780M Graphics** (颜色: #ededed)

## 描述

### Problem Description

As the title suggests.   Attempts to build software that uses `amdgpu-arch` and other tooling, fails.

>>> joe@zap:~/build/rocHPL $ /opt/rocm-6.2.4/lib/llvm/bin/amdgpu-arch
Failed to 'dlopen' libhsa-runtime64.so
Failed to load libamdhip64.so: libdxcore.so: cannot open shared object file: No such file or directory

The requested info:joe@zap:~/build/rocHPL $   echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
  echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
  echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
OS:
NAME="Linux Mint"
VERSION="22 (Wilma)"
CPU:
model name      : AMD Ryzen 9 PRO 7940HS w/ Radeon 780M Graphics
GPU:
/opt/rocm/bin/rocminfo: error while loading shared libraries: libdxcore.so: cannot open shared object file: No such file or directory

More specifically
joe@zap:~/build/rocHPL $ dpkg -l | grep wsl
ii  hsa-runtime-rocr4wsl-amdgpu:amd64              1.14.0-2071946.24.04                       amd64        AMD Heterogeneous System Architecture HSA - Linux HSA Runtime for Boltzmann (ROCm) platforms in WSL environments.
ii  rocminfo4wsl-amdgpu:amd64                      1.14.0-2071946.24.04                       amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool for WSL environments.

Attempts to remove this are catastrophic for ROCm.

>>> joe@zap:~/build/rocHPL $ sudo apt remove hsa-runtime-rocr4wsl-amdgpu:amd64 rocminfo4wsl-amdgpu:amd64
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  amd-smi-lib comgr composablekernel-dev half hipfft hipfft-dev hipify-clang hiprand hiprand-dev
  hiptensor hiptensor-dev hsa-amd-aqlprofile hsakmt-roct-dev libasan6 libavcodec-dev
  libavformat-dev libavutil-dev libdrm-amdgpu-dev libelf-dev libfile-copy-recursive-perl
  libfile-which-perl libgcc-11-dev libset-scalar-perl libstdc++-11-dev libswresample-dev
  libswscale-dev libsystemd-dev libva-dev libva-glx2 rocfft rocfft-dev rocm-cmake rocm-core
  rocm-dbgapi rocm-debug-agent rocm-device-libs rocm-gdb rocm-llvm rocm-opencl-icd-loader
  rocm-smi-lib rocprofiler-register rocprofiler-sdk rocprofiler-sdk-roctx rocrand rocrand-dev
  roctracer roctracer-dev rocwmma-dev valgrind
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-dev hipblaslt hipblaslt-dev hipcc
  hipcub-dev hipfort-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt
  hipsparselt-dev hsa-rocr-dev hsa-runtime-rocr4wsl-amdgpu migraphx migraphx-dev miopen-hip
  miopen-hip-dev mivisionx mivisionx-dev openmp-extras-dev openmp-extras-runtime rccl rccl-dev
  rocalution rocalution-dev rocblas rocblas-dev rocdecode rocdecode-dev rocm rocm-dev
  rocm-developer-tools rocm-hip-libraries rocm-hip-runtime rocm-hip-runtime-dev rocm-hip-sdk
  rocm-language-runtime rocm-ml-libraries rocm-ml-sdk rocm-opencl rocm-opencl-dev
  rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-utils rocminfo4wsl-amdgpu rocprim-dev
  rocprofiler rocprofiler-dev rocprofiler-plugins rocsolver rocsolver-dev rocsparse rocsparse-dev
  rocthrust-dev rpp rpp-dev
0 upgraded, 0 newly installed, 63 to remove and 0 not upgraded.
After this operation, 25.4 GB disk space will be freed.
Do you want to continue? [Y/n]

Please do not include WSL dependencies in linux.  

It appears that the breakage is in the rocm-llvm package

>>> root@zap:/home/joe/build/rocHPL# dpkg-query -S /opt/rocm-6.2.4/lib/llvm/bin/amdgpu-arch
rocm-llvm: /opt/rocm-6.2.4/lib/llvm/bin/amdgpu-arch


>>> 

### Operating System

Linux Mint 22 (based upon Ubuntu 24.04)

### CPU

AMD Ryzen 9 PRO 7940HS 

### GPU

Radeon 780M Graphics

### ROCm Version

ROCm 6.2.3

### ROCm Component

ROCm

### Steps to Reproduce

Install 6.2.4 on Ubuntu 24.04 or rebuilds running on bare metal.  Try to run rocminfo.  Or /opt/rocm-6.2.4/lib/llvm/bin/amdgpu-arch

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

root@zap:/home/joe/build/rocHPL# /opt/rocm/bin/rocminfo --support
/opt/rocm/bin/rocminfo: error while loading shared libraries: libdxcore.so: cannot open shared object file: No such file or directory

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2024-11-25T15:48:14Z)

Hi @joelandman, WSL packages are only included in the installation when either a WSL environment is detected (presence of `/dev/dxg`, `libdxcore.so`.etc), or the `wsl` usecase is passed into the amdgpu-install command ([ref](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#wsl-usecase)).

It's important to note that the `hsa-runtime-rocr4wsl-amdgpu` package doesn't exist for ROCm 6.2.4.

https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/
https://repo.radeon.com/amdgpu/6.2.4/ubuntu/pool/main/h/

Whether autodetection is falsely triggering or the wsl usecase being added to the command, the package manager won't find the package and the ROCm installation should be free of it. I'd suggest removing your current installation with
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
This should remove all ROCm (6.2.4 and 6.2.3) packages including `hsa-runtime-rocr4wsl-amdgpu` and `rocminfo4wsl-amdgpu`. Then reinstall the ROCm 6.2.4 packages following the [quick start installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html).

---

### 评论 #2 — githust66 (2024-11-26T07:27:52Z)

> Hi @joelandman, WSL packages are only included in the installation when either a WSL environment is detected (presence of `/dev/dxg`, `libdxcore.so`.etc), or the `wsl` usecase is passed into the amdgpu-install command ([ref](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#wsl-usecase)).
> 
> It's important to note that the `hsa-runtime-rocr4wsl-amdgpu` package doesn't exist for ROCm 6.2.4.
> 
> https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/ https://repo.radeon.com/amdgpu/6.2.4/ubuntu/pool/main/h/
> 
> Whether autodetection is falsely triggering or the wsl usecase being added to the command, the package manager won't find the package and the ROCm installation should be free of it. I'd suggest removing your current installation with
> 
> ```
> sudo amdgpu-install --uninstall --rocmrelease=all
> sudo apt purge amdgpu-install
> sudo apt autoremove
> ```
> 
> This should remove all ROCm (6.2.4 and 6.2.3) packages including `hsa-runtime-rocr4wsl-amdgpu` and `rocminfo4wsl-amdgpu`. Then reinstall the ROCm 6.2.4 packages following the [quick start installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html).

hi,Can you help me take a look at this issue, rocm is installed correctly, but amdsmi recognition does not recognize the loading.
https://github.com/vllm-project/vllm/issues/10653
![image](https://github.com/user-attachments/assets/7c4c721b-dbcc-49b8-b685-395db1ce5922)


---

### 评论 #3 — harkgill-amd (2024-11-26T15:12:25Z)

> hi,Can you help me take a look at this issue, rocm is installed correctly, but amdsmi recognition does not recognize the loading.
https://github.com/vllm-project/vllm/issues/10653

Commented on https://github.com/ROCm/ROCm/issues/4055.

---

### 评论 #4 — harkgill-amd (2024-12-09T15:12:38Z)

@joelandman please give the suggestion in https://github.com/ROCm/ROCm/issues/4053#issuecomment-2498383776 a try when you get the chance. Will close out this issue for now, feel free to leave a comment if you're still encountering any issues.

---

### 评论 #5 — chrisaga (2026-02-03T17:51:51Z)

Just got the same issue with an upgrade to the latest Rocm (ver 7.2)
Long story short. I think that's not a regression and for whatever reason `hsa-runtime-rocr4wsl-amdgpu` was installed  on my system. I just removed it and installed `hsa-rocr` instead.
Problem fixed: `rocminfo` doesn't complain about `libdxcore.so` anymore.
Hope it could help someone.

---
