# [Issue]: Wrong version of 32bit dependencies on Debian 13

> **Issue #5927**
> **状态**: closed
> **创建时间**: 2026-02-03T17:32:23Z
> **更新时间**: 2026-02-05T23:23:32Z
> **关闭时间**: 2026-02-05T23:23:32Z
> **作者**: facorazza
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5927

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

```shell
sudo apt install rocm                            
[sudo] password for rocm: 
Installing:                     
  rocm

Installing dependencies:
  amd-smi-lib           hipsolver           libc6-dev-x32                libimath-dev              libopencv-shape-dev      libtbb-dev           ocl-icd-opencl-dev     rocm-openmp
  amdgpu-core           hipsolver-dev       libc6-x32                    libjbig-dev               libopencv-shape410       libtesseract5        opencl-c-headers       rocm-smi-lib
  comgr                 hipsparse           libcamd3                     libjpeg-dev               libopencv-stitching-dev  libtiff-dev          opencl-clhpp-headers   rocminfo
  composablekernel-dev  hipsparse-dev       libccolamd3                  libjpeg62-turbo-dev       libopencv-stitching410   libtiffxx6           openmp-extras-dev      rocprim-dev
  g++-14-multilib       hipsparselt         libcholmod5                  libleptonica6             libopencv-superres-dev   libucx0              openmp-extras-runtime  rocprofiler
  g++-multilib          hipsparselt-dev     libcolamd3                   liblerc-dev               libopencv-superres410    libvtk9.3            python3-pip            rocprofiler-compute
  gcc-14-multilib       hiptensor           libdc1394-dev                libllvm17t64              libopencv-video-dev      libwebp-dev          rccl                   rocprofiler-dev
  gcc-multilib          hiptensor-dev       libdeflate-dev               libmunge2                 libopencv-video410       libwebpdecoder3      rccl-dev               rocprofiler-plugins
  half                  hsa-amd-aqlprofile  libdrm-amdgpu-amdgpu1        libnuma-dev               libopencv-videoio-dev    libx32asan8          rocalution             rocprofiler-register
  hip-dev               hsa-rocr            libdrm-amdgpu-common         libopencv-calib3d-dev     libopencv-videoio410     libx32atomic1        rocalution-dev         rocprofiler-sdk
  hip-doc               hsa-rocr-dev        libdrm-amdgpu-dev            libopencv-contrib-dev     libopencv-videostab-dev  libx32gcc-14-dev     rocblas                rocprofiler-sdk-rocpd
  hip-runtime-amd       lib32asan8          libdrm-amdgpu-radeon1        libopencv-contrib410      libopencv-videostab410   libx32gcc-s1         rocblas-dev            rocprofiler-sdk-roctx
  hip-samples           lib32atomic1        libdrm-dev                   libopencv-core-dev        libopencv-viz-dev        libx32gomp1          rocfft                 rocprofiler-systems
  hipblas               lib32gcc-14-dev     libdrm2-amdgpu               libopencv-dev             libopencv-viz410         libx32itm1           rocfft-dev             rocrand
  hipblas-common-dev    lib32gomp1          libelf-dev                   libopencv-dnn-dev         libopencv410-jni         libx32quadmath0      rocm-cmake             rocrand-dev
  hipblas-dev           lib32itm1           libevent-pthreads-2.1-7t64   libopencv-features2d-dev  libopenexr-dev           libx32stdc++-14-dev  rocm-core              rocsolver
  hipblaslt             lib32quadmath0      libfabric1                   libopencv-flann-dev       libopenmpi40             libx32stdc++6        rocm-dbgapi            rocsolver-dev
  hipblaslt-dev         lib32stdc++-14-dev  libfile-copy-recursive-perl  libopencv-highgui-dev     libpciaccess-dev         libx32ubsan1         rocm-debug-agent       rocsparse
  hipcc                 lib32ubsan1         libfile-which-perl           libopencv-highgui410      libpmix2t64              libzstd-dev          rocm-developer-tools   rocsparse-dev
  hipcub-dev            libamd-comgr2       libgdcm-dev                  libopencv-imgcodecs-dev   libpsm2-2                mesa-common-dev      rocm-device-libs       rocthrust-dev
  hipfft                libamd3             libgl2ps1.4                  libopencv-imgproc-dev     libraw1394-dev           migraphx             rocm-gdb               roctracer
  hipfft-dev            libamdhip64-5       libglew2.2                   libopencv-java            libraw1394-tools         migraphx-dev         rocm-hip               roctracer-dev
  hipfort-dev           libavcodec-dev      libhsa-runtime64-1           libopencv-ml-dev          libsharpyuv-dev          miopen-hip           rocm-llvm              rocwmma-dev
  hipify-clang          libavformat-dev     libhsakmt1                   libopencv-objdetect-dev   libsuitesparseconfig7    miopen-hip-dev       rocm-opencl            rpp
  hiprand               libavutil-dev       libibmad5                    libopencv-photo-dev       libswresample-dev        mivisionx            rocm-opencl-dev        rpp-dev
  hiprand-dev           libc6-dev-i386      libibumad3                   libopencv-photo410        libswscale-dev           mivisionx-dev        rocm-opencl-sdk

Suggested packages:
  lib32stdc++6-14-dbg  libx32stdc++6-14-dbg  glew-utils  opencv-doc  libraw1394-doc  libtbb-doc  mpi-default-bin  vtk9-doc  vtk9-examples  opencl-clhpp-headers-doc
```

I'm not sure why the 32bit libraries are required, but they are referencing packets with the wrong version:
 
```shell
Error: Failed to fetch http://deb.debian.org/debian/pool/main/g/glibc/libc6-dev-i386_2.41-12_amd64.deb  404  Not Found
Error: Failed to fetch http://deb.debian.org/debian/pool/main/g/glibc/libc6-x32_2.41-12_amd64.deb  404  Not Found
Error: Failed to fetch http://deb.debian.org/debian/pool/main/g/glibc/libc6-dev-x32_2.41-12_amd64.deb  404  Not Found
```

The versions [available](https://deb.debian.org/debian/pool/main/g/glibc/) for libc6-dev-i386 are:

```shell
[ ]	libc6-dev-i386_2.41-12+deb13u1_amd64.deb	2026-01-01 11:17 	1.4M
[ ]	libc6-dev-i386_2.42-11+b1_amd64.deb	2026-02-02 22:52 	1.4M
[ ]	libc6-dev-i386_2.42-11_amd64.deb	2026-01-27 02:16 	1.4M
[ ]	libc6-dev-i386_2.43-1_amd64.deb	2026-01-28 23:54 	1.5M
```

This is somewhat related to #5806. I don't necessarily mind installing these libraries as long as I'm able to install ROCm in the first place.


### Operating System

Debian GNU/Linux

### CPU

AMD Ryzen 5 7640U w/ Radeon 760M Graphics

### GPU

Radeon 760M Graphics

### ROCm Version

7.2

### ROCm Component

rocm-core

### Steps to Reproduce

Follow the steps in the [documentation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-debian.html)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — schung-amd (2026-02-04T22:14:47Z)

Hi @facorazza, thanks for the report. Will try to repro when I get access to a Debian 13 system, but this looks like a Debian package tree issue and not on our end as we don't provide `libc-dev`; have you done an `apt update`?

---

### 评论 #2 — facorazza (2026-02-05T23:23:32Z)

After replicating in a vm I realized I had a weird cache state. After running

```shell
sudo apt clean
sudo rm -rf /var/lib/apt/lists/*
sudo apt update
sudo apt install libc6-dev-i386
```

It installed just fine.

---
