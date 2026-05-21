# [Issue]:  brocken cp-command in half post-build script

> **Issue #3743**
> **状态**: closed
> **创建时间**: 2024-09-18T02:31:39Z
> **更新时间**: 2024-09-30T13:56:06Z
> **关闭时间**: 2024-09-30T13:56:05Z
> **作者**: jdumke
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3743

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

While trying to move package files, after building half, the cp command brakes in cause of incomplete filename-pattern.
I can't locate where the cp call takes place to fix it.

### Operating System

Debian 12 Bookworm with Backports

### CPU

 AMD Ryzen 5 5600G with Radeon Graphics

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.2.0

### ROCm Component

half

### Steps to Reproduce

Like described in README.md in ROCm.git 
local settings: export GPU_ARCHS="gfx803;gfx90c"

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

[all fine until …]
-- Install configuration: "Release"
-- Installing: /opt/rocm-6.2.0/include/half/half.hpp
-- Installing: /opt/rocm-6.2.0/share/doc/half/LICENSE.txt
gmake[1]: Leaving directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half'
+ rm -rf _CPack_Packages/
+ find -name '*.o' -delete
+ mkdir -p /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ cp '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/*.' /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
cp: cannot stat '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/*.': No such file or directory

real	0m2.276s
user	0m0.713s
sys	0m0.290s
+ mv /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/half.inprogress /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/half.errors
+ echo Error in half
Error in half
+ exit 1


---

## 评论 (14 条)

### 评论 #1 — harkgill-amd (2024-09-18T15:16:25Z)

Hi @jdumke, thanks for pointing this out. An internal ticket has been created to investigate this issue.

---

### 评论 #2 — schung-amd (2024-09-18T17:53:30Z)

Hi @jdumke, not sure if this is causing your issue, but at first glance I notice you're setting `export GPU_ARCHS="gfx803;gfx90c"`. If you're on a W7900, the correct setting is `export GPU_ARCHS="gfx1100"`. Also, you should disable your integrated graphics, as this can cause some issues. I'll try to repro your issue, but hopefully this helps.

---

### 评论 #3 — jdumke (2024-09-18T20:25:10Z)

I don't build for a W7900, I'm building for a W5100 instead, but I must choose a card from the drop down to open the issue and "Legacy" is not an option.

---

### 评论 #4 — schung-amd (2024-09-18T20:49:04Z)

I see, unfortunately that card/architecture is unsupported; see https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html for compatibility details. I'll still see if I can repro this for posterity, but I suspect the issue here is related to this lack of support.

---

### 评论 #5 — jdumke (2024-09-18T20:53:36Z)

The build it self works fine it's a post build issue which doesn't relate to the gpu I'm building for.

---

### 评论 #6 — schung-amd (2024-09-18T21:11:12Z)

Which docker are you using?

---

### 评论 #7 — jdumke (2024-09-18T21:13:44Z)

I don't use docker, I have another vm with a Debian Bookworm with backports.

---

### 评论 #8 — schung-amd (2024-09-19T14:15:44Z)

The guide you are following suggests the use of a docker to install prerequisites, but let's assume you have the prerequisites installed properly for now. I cannot reproduce this issue on Ubuntu 22.04 with supported hardware; half builds perfectly fine. 

The line that fails for you is `cp '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/.' /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half`; immediately this is suspicious to me because of the consecutive `/` in the path, and indeed on my system this directory ends with `out/ubuntu-22.04/22.04/deb/half`. 

Looking at the install script, this path is filled in with the package type installed, and on my end contains a `.deb` file as expected: `half_1.12.0.60200-9999~22.04_amd64.deb`. What this tells me is that the install scripts did not find a compatible package for your system, likely because we do not officially support Debian. You may be able to build this successfully if you attempt this in a Ubuntu docker as the guide suggests.


---

### 评论 #9 — jdumke (2024-09-20T14:49:08Z)

Yes, I installed the prequisites with the given script for Ubuntu22.
Maybe I oversee some in the build log, I'm posting the complete one:
+ source ROCm/tools/rocm-build/envsetup.sh
++ set_WORK_ROOT
++ '[' -n '' ']'
++ export WORK_ROOT=/home/builder/devel/amd/rocm-6.2
++ WORK_ROOT=/home/builder/devel/amd/rocm-6.2
++ :
++ '[' -d /home/builder/devel/amd/rocm-6.2/.repo/manifests ']'
++ return 0
++ '[' '' == '' ']'
+++ command -v nproc
++ '[' -x /usr/bin/nproc ']'
+++ nproc
++ export 'DASH_JAY=-j 6'
++ DASH_JAY='-j 6'
++ export JOB_NAME=release
++ JOB_NAME=release
++ export JOB_DESIGNATOR=
++ JOB_DESIGNATOR=
++ echo JOB_DESIGNATOR=
JOB_DESIGNATOR=
++ export SLES_BUILD_ID_PREFIX
++ echo SLES_BUILD_ID_PREFIX=
SLES_BUILD_ID_PREFIX=
++ '[' -z '' ']'
++ export BUILD_ID=9999
++ BUILD_ID=9999
++ '[' -n release ']'
++ export ROCM_BUILD_ID=release-9999
++ ROCM_BUILD_ID=release-9999
++ source /etc/os-release
+++ PRETTY_NAME='Debian GNU/Linux 12 (bookworm)'
+++ NAME='Debian GNU/Linux'
+++ VERSION_ID=12
+++ VERSION='12 (bookworm)'
+++ VERSION_CODENAME=bookworm
+++ ID=debian
+++ HOME_URL=https://www.debian.org/
+++ SUPPORT_URL=https://www.debian.org/support
+++ BUG_REPORT_URL=https://bugs.debian.org/
++ export DISTRO_NAME=debian
++ DISTRO_NAME=debian
++ export DISTRO_RELEASE=12
++ DISTRO_RELEASE=12
++ export DISTRO_ID=debian-12
++ DISTRO_ID=debian-12
++ case "${DISTRO_NAME}" in
++ export CPACK_DEBIAN_PACKAGE_RELEASE=9999~12
++ CPACK_DEBIAN_PACKAGE_RELEASE=9999~12
++ export CPACK_RPM_PACKAGE_RELEASE=9999
++ CPACK_RPM_PACKAGE_RELEASE=9999
++ OUT_DIR=/home/builder/devel/amd/rocm-6.2/out/debian-12/12
++ export OUT_DIR
++ export RT_TMP=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/tmp/rt
++ RT_TMP=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/tmp/rt
++ export SRC_TF_ROOT=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/srctf
++ SRC_TF_ROOT=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/srctf
++ '[' -f /home/builder/devel/amd/rocm-6.2/build/rocm_version.txt ']'
++ : 6.2.0
+++ get_rocm_libpatch_version 6.2.0
+++ rocm_version=6.2.0
+++ [[ 6.2.0 =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]
+++ libpatch_version=60200
+++ echo 60200
++ ROCM_LIBPATCH_VERSION=60200
++ echo ROCM_VERSION=6.2.0
ROCM_VERSION=6.2.0
++ echo ROCM_LIBPATCH_VERSION=60200
ROCM_LIBPATCH_VERSION=60200
++ export ROCM_VERSION ROCM_LIBPATCH_VERSION
++ export ROCM_INSTALL_PATH=/opt/rocm-6.2.0-9999
++ ROCM_INSTALL_PATH=/opt/rocm-6.2.0-9999
++ [[ release == *rel* ]]
++ export ROCM_INSTALL_PATH=/opt/rocm-6.2.0
++ ROCM_INSTALL_PATH=/opt/rocm-6.2.0
++ '[' -n '' ']'
++ echo 'Setting ROCM_INSTALL_PATH=/opt/rocm-6.2.0'
Setting ROCM_INSTALL_PATH=/opt/rocm-6.2.0
++ export ROCM_PATH=/opt/rocm-6.2.0
++ ROCM_PATH=/opt/rocm-6.2.0
++ export ROCM_LIBPATH=
++ ROCM_LIBPATH=
++ export 'DEVTOOLSET_LIBPATH=/opt/rh/devtoolset-7/root/usr/lib64;/opt/rh/devtoolset-7/root/usr/lib'
++ DEVTOOLSET_LIBPATH='/opt/rh/devtoolset-7/root/usr/lib64;/opt/rh/devtoolset-7/root/usr/lib'
++ export DIST_NO_DEBUG=yes
++ DIST_NO_DEBUG=yes
++ export OPENCL_MAINLINE=1
++ OPENCL_MAINLINE=1
++ export HSA_SOURCE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime
++ HSA_SOURCE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime
++ export HSA_OPENSOURCE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src
++ HSA_OPENSOURCE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src
++ export ROCRTST_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/rocrtst
++ ROCRTST_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/rocrtst
++ export HSA_CORE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src
++ HSA_CORE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src
++ export HSA_IMAGE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/hsa-ext-image
++ HSA_IMAGE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/hsa-ext-image
++ export HSA_FINALIZE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/hsa-ext-finalize
++ HSA_FINALIZE_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/hsa-ext-finalize
++ export HSA_TOOLS_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/hsa-runtime-tools
++ HSA_TOOLS_ROOT=/home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/hsa-runtime-tools
++ export OCL_RT_SRC_TF_ROOT=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/srctf/ocl_lc
++ OCL_RT_SRC_TF_ROOT=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/srctf/ocl_lc
++ export SCRIPT_ROOT=/home/builder/devel/amd/rocm-6.2/build
++ SCRIPT_ROOT=/home/builder/devel/amd/rocm-6.2/build
++ export THUNK_ROOT=/home/builder/devel/amd/rocm-6.2/ROCT-Thunk-Interface
++ THUNK_ROOT=/home/builder/devel/amd/rocm-6.2/ROCT-Thunk-Interface
++ '[' -d /home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/ROCT-Thunk-Interface ']'
++ export AQLPROFILE_ROOT=/home/builder/devel/amd/rocm-6.2/hsa/aqlprofile
++ AQLPROFILE_ROOT=/home/builder/devel/amd/rocm-6.2/hsa/aqlprofile
++ export OMNIPERF_ROOT=/home/builder/devel/amd/rocm-6.2/omniperf
++ OMNIPERF_ROOT=/home/builder/devel/amd/rocm-6.2/omniperf
++ export ROCPROFILER_ROOT=/home/builder/devel/amd/rocm-6.2/rocprofiler
++ ROCPROFILER_ROOT=/home/builder/devel/amd/rocm-6.2/rocprofiler
++ export ROCTRACER_ROOT=/home/builder/devel/amd/rocm-6.2/roctracer
++ ROCTRACER_ROOT=/home/builder/devel/amd/rocm-6.2/roctracer
++ export ROCPROFILER_REGISTER_ROOT=/home/builder/devel/amd/rocm-6.2/rocprofiler-register
++ ROCPROFILER_REGISTER_ROOT=/home/builder/devel/amd/rocm-6.2/rocprofiler-register
++ export ROCPROFILER_SDK_ROOT=/home/builder/devel/amd/rocm-6.2/rocprofiler-sdk
++ ROCPROFILER_SDK_ROOT=/home/builder/devel/amd/rocm-6.2/rocprofiler-sdk
++ export OMNITRACE_ROOT=/home/builder/devel/amd/rocm-6.2/omnitrace
++ OMNITRACE_ROOT=/home/builder/devel/amd/rocm-6.2/omnitrace
++ export RDC_ROOT=/home/builder/devel/amd/rocm-6.2/rdc
++ RDC_ROOT=/home/builder/devel/amd/rocm-6.2/rdc
++ export RDCTST_ROOT=/home/builder/devel/amd/rocm-6.2/rdc/tests/rdc_tests
++ RDCTST_ROOT=/home/builder/devel/amd/rocm-6.2/rdc/tests/rdc_tests
++ export UTILS_ROOT=/home/builder/devel/amd/rocm-6.2/rocm-utils
++ UTILS_ROOT=/home/builder/devel/amd/rocm-6.2/rocm-utils
++ export KFDTEST_ROOT=/home/builder/devel/amd/rocm-6.2/ROCT-Thunk-Interface/tests/kfdtest
++ KFDTEST_ROOT=/home/builder/devel/amd/rocm-6.2/ROCT-Thunk-Interface/tests/kfdtest
++ '[' -d /home/builder/devel/amd/rocm-6.2/ROCR-Runtime/src/tests/kfdtest ']'
++ export HIPIFY_ROOT=/home/builder/devel/amd/rocm-6.2/HIPIFY
++ HIPIFY_ROOT=/home/builder/devel/amd/rocm-6.2/HIPIFY
++ export AMD_SMI_LIB_ROOT=/home/builder/devel/amd/rocm-6.2/amdsmi
++ AMD_SMI_LIB_ROOT=/home/builder/devel/amd/rocm-6.2/amdsmi
++ export ROCM_SMI_LIB_ROOT=/home/builder/devel/amd/rocm-6.2/rocm_smi_lib
++ ROCM_SMI_LIB_ROOT=/home/builder/devel/amd/rocm-6.2/rocm_smi_lib
++ export RSMITST_ROOT=/home/builder/devel/amd/rocm-6.2/rocm_smi_lib/tests/rocm_smi_test
++ RSMITST_ROOT=/home/builder/devel/amd/rocm-6.2/rocm_smi_lib/tests/rocm_smi_test
++ export LLVM_PROJECT_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project
++ LLVM_PROJECT_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project
++ export LLVM_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/llvm
++ LLVM_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/llvm
++ export CLANG_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/clang
++ CLANG_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/clang
++ export LLD_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/lld
++ LLD_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/lld
++ export HIPCC_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/amd/hipcc
++ HIPCC_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/amd/hipcc
++ export DEVICELIBS_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/amd/device-libs
++ DEVICELIBS_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/amd/device-libs
++ export ROCM_CORE_ROOT=/home/builder/devel/amd/rocm-6.2/rocm-core
++ ROCM_CORE_ROOT=/home/builder/devel/amd/rocm-6.2/rocm-core
++ export ROCM_CMAKE_ROOT=/home/builder/devel/amd/rocm-6.2/rocm-cmake
++ ROCM_CMAKE_ROOT=/home/builder/devel/amd/rocm-6.2/rocm-cmake
++ export ROCM_BANDWIDTH_TEST_ROOT=/home/builder/devel/amd/rocm-6.2/rocm_bandwidth_test
++ ROCM_BANDWIDTH_TEST_ROOT=/home/builder/devel/amd/rocm-6.2/rocm_bandwidth_test
++ export ROCMINFO_ROOT=/home/builder/devel/amd/rocm-6.2/rocminfo
++ ROCMINFO_ROOT=/home/builder/devel/amd/rocm-6.2/rocminfo
++ export ROCR_DEBUG_AGENT_ROOT=/home/builder/devel/amd/rocm-6.2/rocr_debug_agent
++ ROCR_DEBUG_AGENT_ROOT=/home/builder/devel/amd/rocm-6.2/rocr_debug_agent
++ export COMGR_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/amd/comgr
++ COMGR_ROOT=/home/builder/devel/amd/rocm-6.2/llvm-project/amd/comgr
++ export COMGR_LIB_PATH=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/amd_comgr
++ COMGR_LIB_PATH=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/amd_comgr
++ export RCCL_ROOT=/home/builder/devel/amd/rocm-6.2/rccl
++ RCCL_ROOT=/home/builder/devel/amd/rocm-6.2/rccl
++ export ROCM_DBGAPI_ROOT=/home/builder/devel/amd/rocm-6.2/ROCdbgapi
++ ROCM_DBGAPI_ROOT=/home/builder/devel/amd/rocm-6.2/ROCdbgapi
++ export ROCM_GDB_ROOT=/home/builder/devel/amd/rocm-6.2/ROCgdb
++ ROCM_GDB_ROOT=/home/builder/devel/amd/rocm-6.2/ROCgdb
++ export HIP_ON_ROCclr_ROOT=/home/builder/devel/amd/rocm-6.2/HIP
++ HIP_ON_ROCclr_ROOT=/home/builder/devel/amd/rocm-6.2/HIP
++ export HIPAMD_ROOT=/home/builder/devel/amd/rocm-6.2/hipamd
++ HIPAMD_ROOT=/home/builder/devel/amd/rocm-6.2/hipamd
++ export HIP_CATCH_TESTS_ROOT=/home/builder/devel/amd/rocm-6.2/hip-tests
++ HIP_CATCH_TESTS_ROOT=/home/builder/devel/amd/rocm-6.2/hip-tests
++ export CLR_ROOT=/home/builder/devel/amd/rocm-6.2/clr
++ CLR_ROOT=/home/builder/devel/amd/rocm-6.2/clr
++ export AOMP_REPOS=/home/builder/devel/amd/rocm-6.2/openmp-extras
++ AOMP_REPOS=/home/builder/devel/amd/rocm-6.2/openmp-extras
++ export HIPOTHER_ROOT=/home/builder/devel/amd/rocm-6.2/hipother
++ HIPOTHER_ROOT=/home/builder/devel/amd/rocm-6.2/hipother
++ export 'ROCM_LIB_RPATH=$ORIGIN'
++ ROCM_LIB_RPATH='$ORIGIN'
++ export 'ROCM_EXE_RPATH=$ORIGIN/../lib'
++ ROCM_EXE_RPATH='$ORIGIN/../lib'
++ export 'ROCM_ASAN_LIB_RPATH=$ORIGIN:$ORIGIN/..'
++ ROCM_ASAN_LIB_RPATH='$ORIGIN:$ORIGIN/..'
++ export 'ROCM_ASAN_EXE_RPATH=$ORIGIN/../lib/asan:$ORIGIN/../lib'
++ ROCM_ASAN_EXE_RPATH='$ORIGIN/../lib/asan:$ORIGIN/../lib'
++ export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/builder/devel/amd/rocm-6.2/build
++ PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/builder/devel/amd/rocm-6.2/build
++ export LIBS_WORK_DIR=/home/builder/devel/amd/rocm-6.2
++ LIBS_WORK_DIR=/home/builder/devel/amd/rocm-6.2
++ export BUILD_ARTIFACTS=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/
++ BUILD_ARTIFACTS=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/
++ export 'HIPCC_COMPILE_FLAGS_APPEND=-O3 -Wno-format-nonliteral -parallel-jobs=4'
++ HIPCC_COMPILE_FLAGS_APPEND='-O3 -Wno-format-nonliteral -parallel-jobs=4'
++ export 'HIPCC_LINK_FLAGS_APPEND=-O3 -parallel-jobs=4'
++ HIPCC_LINK_FLAGS_APPEND='-O3 -parallel-jobs=4'
++ export PATH=/opt/rocm-6.2.0/bin:/opt/rocm-6.2.0/lib/llvm/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/builder/devel/amd/rocm-6.2/build
++ PATH=/opt/rocm-6.2.0/bin:/opt/rocm-6.2.0/lib/llvm/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/builder/devel/amd/rocm-6.2/build
++ export LC_ALL=C.UTF-8
++ LC_ALL=C.UTF-8
++ export LANG=C.UTF-8
++ LANG=C.UTF-8
+++ nproc
++ export PROC=6
++ PROC=6
++ export RELEASE_FLAG=-r
++ RELEASE_FLAG=-r
++ export SUDO=sudo
++ SUDO=sudo
++ export PATH=/usr/local/bin:/opt/rocm-6.2.0/bin:/opt/rocm-6.2.0/lib/llvm/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/builder/devel/amd/rocm-6.2/build:/home/builder/.local/bin
++ PATH=/usr/local/bin:/opt/rocm-6.2.0/bin:/opt/rocm-6.2.0/lib/llvm/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/builder/devel/amd/rocm-6.2/build:/home/builder/.local/bin
++ export CCACHE_DIR=/home/builder/.ccache
++ CCACHE_DIR=/home/builder/.ccache
+ rm -f /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/half.errors /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/half /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/half.repackaged
+ ROCm/tools/rocm-build/build_half.sh -c
++ dirname ROCm/tools/rocm-build/build_half.sh
+ source ROCm/tools/rocm-build/compute_helper.sh
++ set -e
++ set -o pipefail
++ ROCM_LLVMDIR=lib/llvm
++ export ADDRESS_SANITIZER=OFF
++ ADDRESS_SANITIZER=OFF
++ rocm_math_common_cmake_params=()
++ TARGET=build
+ set_component_src half
+ COMPONENT_SRC=/home/builder/devel/amd/rocm-6.2/half
+ BUILD_DIR=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half
+ DEB_PATH=/home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ RPM_PATH=/home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ PACKAGE_DIR=/home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ stage2_command_args -c
+ '[' -c '!=' '' ']'
+ case $1 in
+ TARGET=clean
+ shift 1
+ '[' '' '!=' '' ']'
+ case $TARGET in
+ clean_half
+ echo 'Cleaning half build directory: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half'
Cleaning half build directory: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ rm -rf /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ echo 'Done!'
Done!
+ source ROCm/tools/rocm-build/ccache-env-mathlib.sh
++ '[' '' == true ']'
+ bash -x ROCm/tools/rocm-build/build_half.sh -r
+ set -ex
++ dirname ROCm/tools/rocm-build/build_half.sh
+ source ROCm/tools/rocm-build/compute_helper.sh
++ set -e
++ set -o pipefail
++ ROCM_LLVMDIR=lib/llvm
++ export ADDRESS_SANITIZER=OFF
++ ADDRESS_SANITIZER=OFF
++ rocm_math_common_cmake_params=()
++ TARGET=build
+ set_component_src half
+ COMPONENT_SRC=/home/builder/devel/amd/rocm-6.2/half
+ BUILD_DIR=/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half
+ DEB_PATH=/home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ RPM_PATH=/home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ PACKAGE_DIR=/home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ stage2_command_args -r
+ '[' -r '!=' '' ']'
+ case $1 in
+ break
+ case $TARGET in
+ build_half
+ echo 'Start build'
Start build
+ '[' '' == true ']'
+ mkdir -p /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half
+ cd /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half
+ cmake -DCMAKE_INSTALL_PREFIX=/opt/rocm-6.2.0 -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF /home/builder/devel/amd/rocm-6.2/half
-- The C compiler identification is GNU 12.2.0
-- The CXX compiler identification is GNU 12.2.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- rocm-cmake: Set license file to /home/builder/devel/amd/rocm-6.2/half/LICENSE.txt.
-- Configuring done (0.6s)
-- Generating done (0.0s)
-- Build files have been written to: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half
+ cmake --build /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half -- -j6
gmake[1]: warning: -j6 forced in submake: resetting jobserver mode.
gmake[1]: Entering directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half'
gmake[1]: Leaving directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half'
+ cmake --build /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half -- package
gmake[1]: Entering directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half'
[36mRun CPack packaging tool...[0m
CPack: Create package using TGZ
CPack: Install projects
CPack: - Run preinstall target for: half
CPack: - Install project: half []
CPack: Create package
CPack: - package: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/half-1.12.0.60200-Linux.tar.gz generated.
CPack: Create package using ZIP
CPack: Install projects
CPack: - Run preinstall target for: half
CPack: - Install project: half []
CPack: Create package
CPack: - package: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/half-1.12.0.60200-Linux.zip generated.
CPack: Create package using RPM
CPack: Install projects
CPack: - Run preinstall target for: half
CPack: - Install project: half []
CPack: Create package
CPackRPM:Warning: CPACK_SET_DESTDIR is set (=ON) while requesting a relocatable package (CPACK_RPM_PACKAGE_RELOCATABLE is set): this is not supported, the package won't be relocatable.
CPackRPM: Will use GENERATED spec file: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/_CPack_Packages/Linux/RPM/SPECS/half.spec
CPack: - package: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/half-1.12.0.60200-9999.x86_64.rpm generated.
CPack: Create package using DEB
CPack: Install projects
CPack: - Run preinstall target for: half
CPack: - Install project: half []
CPack: Create package
CPack: - package: /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/half_1.12.0.60200-9999~12_amd64.deb generated.
gmake[1]: Leaving directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half'
+ cmake --build /home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half -- install
gmake[1]: Entering directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half'
[36mInstall the project...[0m
-- Install configuration: "Release"
-- Installing: /opt/rocm-6.2.0/include/half/half.hpp
-- Installing: /opt/rocm-6.2.0/share/doc/half/LICENSE.txt
gmake[1]: Leaving directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half'
+ rm -rf _CPack_Packages/
+ find -name '*.o' -delete
+ mkdir -p /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
+ cp '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/*.' /home/builder/devel/amd/rocm-6.2/out/debian-12/12//half
cp: cannot stat '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half/*.': No such file or directory

real	0m2.276s
user	0m0.713s
sys	0m0.290s
+ mv /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/half.inprogress /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/half.errors
+ echo Error in half
Error in half
+ exit 1

---

### 评论 #10 — schung-amd (2024-09-20T14:56:43Z)

Thanks for the build log, I'll check it against mine to see what's different.

---

### 评论 #11 — schung-amd (2024-09-27T17:26:45Z)

What are the contents of `/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/half` after you see this failure?

---

### 评论 #12 — schung-amd (2024-09-27T18:55:04Z)

Found the root cause; as I thought, this is because we do not officially support Debian: https://github.com/ROCm/ROCm/blob/681a98a59da3c7a937458c99e88f110150a024f2/tools/rocm-build/envsetup.sh#L45-L51

Because there is no entry with the distro name "debian", the package type is not set. The build script assembles a directory using the package type:
https://github.com/ROCm/ROCm/blob/681a98a59da3c7a937458c99e88f110150a024f2/tools/rocm-build/build_half.sh#L28

You can try to circumvent this by adding an entry for Debian (distro name "debian", but I don't know if this will install properly, let alone function. You can try this and see if it works, I'll leave this open for now if you'd like further guidance.

---

### 评论 #13 — jdumke (2024-09-28T18:51:14Z)

I found a working solution to the issue. I migrated build_half.sh from compute_helpers.sh to compute_utils.sh and call copy_if() instead of the direct cp calls, which all successfull runung build_*.sh scripts do in my environment. I also added support for the standard cmd-options so build_half.sh is now working properly with T_ and C_ make targets.

---

### 评论 #14 — schung-amd (2024-09-30T13:56:05Z)

Glad to hear this works on your end. We should probably error out of `envsetup.sh` when using an unsupported distro instead of just continuing since this will fail downstream anyway. I'll close this for now, if you have further questions or issues feel free to comment and we can reopen it. Thanks for bringing this to our attention!

---
