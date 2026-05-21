# [Issue]: Broken Dependencies in amdgpu-install due to `--accept-eula`

> **Issue #5625**
> **状态**: open
> **创建时间**: 2025-11-04T20:45:24Z
> **更新时间**: 2025-11-06T20:06:21Z
> **作者**: hazecodeio
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5625

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Attempting to run `amdgpu-install` after installing `amdgpu-install_7.1.70100-1_all.deb` throws this `apt` error:
<img width="1061" height="29" alt="Image" src="https://github.com/user-attachments/assets/c5b1a728-81f1-407e-995d-253f16a71f13" />

Tracing the dependencies I see broken dependency here:

https://repo.radeon.com/amdgpu/

<img width="700" height="58" alt="Image" src="https://github.com/user-attachments/assets/eb721e35-0c2a-4245-bfc9-72e4386edfa3" />

7.1 is missing..


### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

Intel(R) Xeon(R) CPU           X5675  @ 3.07GHz

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 7.1

### ROCm Component

_No response_

### Steps to Reproduce

- Just install  `amdgpu-install_7.1.70100-1_all.deb`
- Run `amdgpu-install -y --accept-eula`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — ianbmacdonald (2025-11-04T21:25:14Z)

I tripped over trying to use `latest` as well .. it used to work prior to the Instinct driver renumbering from 6.x to 30.x ;  There is some symbolic linking in the repo that just broke replacing '30.10' with 'latest' .. and it sounds like that may still be the case. 

There are two apt sources;  The ROCm use the `7.1` version.. you need to switch to `30.20` for amdgpu / Instinct.   You will see it is also there in the directory listing.  

---

### 评论 #2 — hazecodeio (2025-11-04T23:13:28Z)

@ianbmacdonald Thanks for suggesting that. I tried deb packages from both versions 7.1 and 3.20. Same issue!!

But I "think" I found the issue. Will update here once installation goes well.

---

### 评论 #3 — ianbmacdonald (2025-11-05T22:48:33Z)

There is no 7.1 for amdgpu/Instinct .. and there is no 30.20 for ROCm .. I really think you are just a bit confused.   The ROCm/Instinct apt wrapper (amdgpu-install) does not setup a source with the path you provided, and the version you provided, so I have to assume you just have some cruft you have added manually in your apt sources further conflating the issue.   

https://rocm.blogs.amd.com/ecosystems-and-partners/instinct-gpu-driver/README.html



---

### 评论 #4 — stevenlafl (2025-11-06T05:38:29Z)

I had the same problem. **AMD appears to have forgotten to symlink the 7.1 folder to 30.20.** They did this in the past with 7.0.2 being identical to 30.10 folders. And, **there is no upgrade path to 7.1 from 7.0.2.**

**I have a solution below** but this is my investigation into this. Whether or not 7.1 exists seems to be irrelevant. The 7.1 is from `amdgpu-proprietary.list` which is not installed by the `amdgpu-install` package. I have not yet been able to trace where it comes from. 

## Investigation

There is a mismatch here:
https://repo.radeon.com/amdgpu which only shows `7.0.2` and no `7.1` folder, but the `latest` folder contains an `InRelease` with `7.1`:
```
Origin: repo.radeon.com
Label: repo.radeon.com
Suite: noble
Codename: noble
Version: 7.1
Date: Wed, 29 Oct 2025 01:25:25 UTC
Architectures: i386 amd64
Components: main
Description: AMDGPU Ubuntu noble repository
```

The repo here https://repo.radeon.com/rocm/apt/ does show a `7.1` folder.

All I did was upgrade to 7.1 using these steps from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html:
```
wget https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb
sudo apt install ./amdgpu-install_7.1.70100-1_all.deb
sudo apt update
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm
```

It installs:

`/etc/apt/sources.list.d/rocm.list`:
```
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/7.1 noble main
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/graphics/7.1/ubuntu noble main
```
`/etc/apt/sources.list.d/amdgpu.list`
```
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.20/ubuntu noble main
#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.20/ubuntu noble main
```

### Local state
Locally my state matches the above. However, checking the sources.list.d folder, I do have an additional `/etc/apt/sources.list.d/amdgpu-proprietary.list`:
```
# Enabling this repository requires acceptance of the following license:
# /usr/share/amdgpu-install/AMDGPUPROEULA
deb https://repo.radeon.com/amdgpu/7.1/ubuntu noble proprietary
```

No package appears to install it, I have never added it (If I had, I would have put 7.0.2 because I was on 7.0.2 before the upgrade using the steps above. There should be no possible scenario for me to have PEBCAK because I never put 7.1 in that file):
```
dpkg -S /etc/apt/sources.list.d/amdgpu-proprietary.list
dpkg-query: no path found matching pattern /etc/apt/sources.list.d/amdgpu-proprietary.list
```

### Remote state
Running `apt upgrade` after `apt update` yields:

```
Err:22 https://repo.radeon.com/amdgpu/7.1/ubuntu noble Release      
  404  Not Found [IP: 23.221.22.179 443]
```

```
The following packages have been kept back:
  amd-smi-lib comgr composablekernel-dev half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev
  hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev
  hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev migraphx
  migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev openmp-extras-dev openmp-extras-runtime rccl rccl-dev rocalution
  rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools
  rocm-device-libs rocm-gdb rocm-hip rocm-hip-runtime rocm-hip-runtime-dev rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev
  rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler rocprofiler-compute rocprofiler-dev rocprofiler-plugins
  rocprofiler-register rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer
  roctracer-dev rocwmma-dev rpp rpp-dev
```

### Problem

If I try to do an `apt full-upgrade` I get:
```
The following packages were automatically installed and are no longer required:
  amd-smi-lib amdgpu-core comgr composablekernel-dev gcc-11-base half hip-dev hip-doc hip-runtime-amd hip-samples hipblas
  hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand
  hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile
  hsa-rocr hsa-rocr-dev libamd-comgr2 libamd3 libamdhip64-5 libasan6 libavcodec-dev libavformat-dev libavutil-dev libcamd3 libccolamd3
  libcholmod5 libdc1394-dev libdeflate-dev libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1
  libdrm-dev libdrm2-amdgpu libelf-dev libevent-pthreads-2.1-7t64 libexif-dev libexif-doc libfabric1 libfile-copy-recursive-perl
  libfile-which-perl libgcc-11-dev libgdcm-dev libgl-dev libgl2ps1.4 libglew2.2 libglx-dev libgphoto2-dev libhsa-runtime64-1 libhsakmt1
  libimath-dev libjbig-dev libjpeg-dev libjpeg-turbo8-dev libjpeg8-dev liblerc-dev liblzma-dev libmunge2 libnuma-dev
  libopencv-calib3d-dev libopencv-contrib-dev libopencv-core-dev libopencv-dev libopencv-dnn-dev libopencv-features2d-dev
  libopencv-flann-dev libopencv-highgui-dev libopencv-imgcodecs-dev libopencv-imgproc-dev libopencv-java libopencv-ml-dev
  libopencv-objdetect-dev libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev libopencv-shape406t64 libopencv-stitching-dev
  libopencv-stitching406t64 libopencv-superres-dev libopencv-superres406t64 libopencv-video-dev libopencv-videoio-dev
  libopencv-videoio406t64 libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni
  libopenexr-dev libopenmpi3t64 libpciaccess-dev libpmix2t64 libpng-dev libpng-tools libpsm-infinipath1 libpsm2-2 libpthread-stubs0-dev
  libraw1394-dev libraw1394-tools libsharpyuv-dev libstdc++-11-dev libswresample-dev libswscale-dev libtbb-dev libtiff-dev libtiffxx6
  libtsan0 libucx0 libvtk9.1t64 libwebp-dev libwebpdecoder3 libx11-dev libxau-dev libxcb1-dev libxdmcp-dev libzstd-dev mesa-common-dev
  migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev ocl-icd-opencl-dev opencl-c-headers opencl-clhpp-headers
  opencv-data openmp-extras-dev openmp-extras-runtime rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev
  rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent rocm-device-libs rocm-gdb rocm-hip rocm-hip-runtime rocm-hip-runtime-dev
  rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler
  rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-rocpd
  rocprofiler-sdk-roctx rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer
  roctracer-dev rocwmma-dev rpp rpp-dev valgrind x11proto-dev xorg-sgml-doctools xtrans-dev
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  rocm rocm-developer-tools
The following packages will be upgraded:
  amd-smi-lib comgr composablekernel-dev half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev
  hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev
  hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev migraphx
  migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev openmp-extras-dev openmp-extras-runtime rccl rccl-dev rocalution
  rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent rocm-device-libs rocm-gdb
  rocm-hip rocm-hip-runtime rocm-hip-runtime-dev rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev rocm-opencl-sdk
  rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler rocprofiler-compute rocprofiler-dev rocprofiler-plugins
  rocprofiler-register rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer
  roctracer-dev rocwmma-dev rpp rpp-dev
84 upgraded, 0 newly installed, 2 to remove and 0 not upgraded.
```

There's conflicts when you do this. `rocm`  becomes broken. So, **there is no upgrade path to 7.1 from 7.0.2.**

## Solution

Ignore the 7.1 warning. The packages are available within apt because of the sources files installed by the `amdgpu-install` deb.

If for whatever reason we need it, we can alter amdgpu-proprietary.list to use `30.20` or `latest` instead of 7.1 which appears to be the same as @ianbmacdonald mentioned. (proof: check https://repo.radeon.com/amdgpu/30.20/ubuntu/pool/main/a/amdgpu-install/ and https://repo.radeon.com/amdgpu/latest/ubuntu/pool/main/a/amdgpu-install/ . Both of these are NEWER than in the 7.0.2 folder which is the latest 7.x version in the folder list: https://repo.radeon.com/amdgpu/7.0.2/ubuntu/pool/main/a/amdgpu-install/)

So, **AMD appears to have forgotten to symlink the 7.1 folder to 30.20.**

Run:
```
# Remove the exhaustive list of all rocm packages
apt remove --purge rocm
apt autoremove
apt install rocm
reboot
```

### Testing:

<img width="1023" height="843" alt="Image" src="https://github.com/user-attachments/assets/4f2cdb21-0619-476d-9d4a-201948a5cd07" />

---

### 评论 #5 — hazecodeio (2025-11-06T18:18:16Z)

The issue appears to be around installing proprietary components. Triggered by the flag `--accept-eula`. Running `amdgpu-uninstall` won't reset/remove parts set by `--accept-eula`. I had to uninstall the previous `amdgpu-install` before installiing the amdgpu-install 7.1/30.20:

`apt purge amdgpu-install`

I unpacked/inspected the `amdgpu-install_7.1.70100-1_all.deb`, using:

`dpkg-deb -v -R amdgpu-install_7.0.2.70002-1_all.deb amdgpu-install_7.0.2.70002-1_all`


I found this file has a reference to repository that doesn't exists:

`./amdgpu-install_7.1.70100-1_all/DEBIAN/postinst:`
----

<img width="813" height="505" alt="Image" src="https://github.com/user-attachments/assets/f8d6fd9d-ec01-492a-99bd-56ee7d42ee29" />



So the outstanding question here is:

- Is the issue with the repository missing the link the Deb package is looking to resolve? 
- Or with the Deb package not referencing the correct repository?

- Should the Deb package in the above file reference this repository as it seems to contain the proprietary components?
`https://repo.radeon.com/rocm/apt/7.1/`

- Has there been any change around installing proprietary components?

---

### 评论 #6 — harkgill-amd (2025-11-06T19:12:40Z)

Hi @hazecodeio, the proprietary components have been removed making `--accept-eula` obsolete, see https://github.com/ROCm/ROCm/issues/5574#issuecomment-3452990296. We'll be dropping the flag in an upcoming release so this  won't be an issue going forward - sorry for the confusion. Please omit that flag for now and install with just `amdgpu-install  --usecase=graphics,rocm` for Radeon ([ref](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html)). Let me know if this works and if you have any questions.

---

### 评论 #7 — ianbmacdonald (2025-11-06T19:13:16Z)

Thanks for sharing .. I would have lost the bet that you were on to a legit issue.

 `/etc/apt/sources.list.d/amdgpu-proprietary.list`  ;  I have seen that before, and remember commenting it out on an Azure ND MI300X v5 node I upgraded to 24.04/HWE + ROCm 7 ahead of official Azure support.   Perhaps some cruft from ROCm <6.4.4 that the apt wrapper (amdgpu-install) does not handle well.   

I don't have all the answers, other than to say your two rocm.list and amdgpu.list sources are all you need for AI related workflows.   I might guess that the proprietary source is just some hangover from amdgpu-pro closed source opengl/vulkan add-ons.   I can't seem to find them in the current repo, similar [to 22.20] (https://repo.radeon.com/amdgpu/.22.20/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/) 

It is worth noting the [upgrade instructions are actually uninstallation instructions](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#upgrade-to-newer-ryzen-software-versions-for-linux) stating the `recommended method to upgrade is to uninstall` .   

To an apt native, it makes very little sense to not upgrade and rely on package policy and dependencies.  I chalk it up to having to support a wide variety of package frameworks and operating systems.  It is improving.  The current cadence of the packaging and the online documentation suggest a more effective upgrade strategy in the coming releases. 



---

### 评论 #8 — harkgill-amd (2025-11-06T19:18:59Z)

>  I might guess that the proprietary source is just some hangover from amdgpu-pro closed source

Yup, that's correct. The amdgpu-proprietary.list file is added during the regular install and only enabled once you call `--accept-eula`. Again, this'll all be dropped by amdgpu-install going forward as it's no longer relevant. 

---

### 评论 #9 — hazecodeio (2025-11-06T19:42:46Z)

Thank you all for working this out.

I'd like to add a case scenario in which `amdgpu-install  --usecase=graphics,rocm` would fail even if `--accept-eula` flag is not passed.
Running `amdgpu-uninstall` alone isn't enough. You still have to purge the `amdgpu-install` from the system so it'll remove the `amdgpu-proprietary.list` that was modified by a previous install  with `--accept-eula` flag.

---

### 评论 #10 — harkgill-amd (2025-11-06T20:06:21Z)

We can use this issue to track the removal of `amdgpu-proprietary.list` and `--accept-eula` from amdgpu-install.

---
