# [Issue]:

> **Issue #4474**
> **状态**: closed
> **创建时间**: 2025-03-10T16:16:59Z
> **更新时间**: 2025-04-16T20:28:19Z
> **关闭时间**: 2025-04-16T20:28:19Z
> **作者**: aureliendaut
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4474

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Hi, i am a new ROCm user trying to compile a project that use acceleration GPU thanks to ROCm and HIP and also using openMP. It does not work so i tried to compile the /hip/HIP-Examples/openmp-helloworld example which is still not working, leading to 
```
fatal error: hip/hip_runtime.h: No such file or directory
    1 | #include <hip/hip_runtime.h>
      |          ^~~~~~~~~~~~~~~~~~~
compilation terminated.

```

I find that some users also had this issue with some ROCm versions. Is it here also my issue.

Have a good day and thanks in advance.

### Operating System

Debian GNU/Linux 11 (bullseye)

### CPU

AMD EPYC 7642 48-Core Processor

### GPU

AMD EPYC 7642 48-Core Processor gfx906

### ROCm Version

ROCm 4.5.0

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (12 条)

### 评论 #1 — harkgill-amd (2025-03-10T18:41:30Z)

Hi @aureliendaut, how are you trying to compile the sample?

To compile and the run the code, you can simply run `make` from the `/HIP-Examples/openmp-helloworld` directory. 

Alternatively, you can build the sample with CMake
```
mkdir -p build
cd build
cmake ..
make
```
and then run the executable built with
```
./test_openmp_helloworld
```
You can find the aforementioned steps in the [README.md ](https://github.com/ROCm/HIP-Examples/blob/master/openmp-helloworld/README.md) associated with the sample. Please note that the HIP-Examples have been deprecated in favor of the [ROCm-Examples](https://github.com/ROCm/rocm-examples). 

---

### 评论 #2 — aureliendaut (2025-03-10T19:25:41Z)

Hi thanks for your answer, i tried using make as you mentioned in your answer. The example of vectorAdd perfectly worked, but not the Hello world one due to openMP i guess. Is it possible that just my version of ROCm is too old and can't support a framework using openMP and HIP together ?

---

### 评论 #3 — harkgill-amd (2025-03-10T20:47:38Z)

With make, are you still seeing the same error as originally reported? This points to the compiler failing to locate the `hip_runtime.h` header file. Could you please provide the output of `hipconfig` so we can locate the HIP installation, the exact steps you're using to compile and the corresponding errors? 

Also, could you directly try compiling directly with hipcc using 
```
hipcc -fopenmp openmp_helloworld.cpp -o openmp_sample
```

> Is it possible that just my version of ROCm is too old and can't support a framework using openMP and HIP together

I gave the example a try on my end with ROCm 4.5.0/gfx906 and was able to build the test successfully. 

---

### 评论 #4 — aureliendaut (2025-03-11T07:35:49Z)

Yes, i have the same issue using make or using the compile line you mentionned. For the exact steps, it is only 

```
cd openmp_helloworld
make
```
which leads to 
```
openmp_helloworld.cpp:33:10: fatal error: 'omp.h' file not found
#include <omp.h>
         ^~~~~~~
1 error generated when compiling for gfx906.
make: *** [Makefile:18: openmp_helloworld.exe] Error 1

```

Here is the output of hipconfig
```
HIP version  : 4.4.21401-bedc5f61

== hipconfig
HIP_PATH     : /opt/rocm-4.5.0/hip
ROCM_PATH    : /opt/rocm-4.5.0
HIP_COMPILER : clang
HIP_PLATFORM : amd
HIP_RUNTIME  : rocclr
CPP_CONFIG   :  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-4.5.0/hip/include -I/opt/rocm-4.5.0/llvm/bin/../lib/clang/13.0.0 -I/opt/rocm-4.5.0/hsa/include

== hip-clang
HSA_PATH         : /opt/rocm-4.5.0/hsa
HIP_CLANG_PATH   : /opt/rocm-4.5.0/llvm/bin
AMD clang version 13.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-4.5.0 21422 e2489b0d7ede612d6586c61728db321047833ed8)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-4.5.0/llvm/bin
AMD LLVM version 13.0.0git
  Optimized build.
  Default target: x86_64-unknown-linux-gnu
  Host CPU: znver2

  Registered Targets:
    amdgcn - AMD GCN GPUs
    r600   - AMD GPUs HD2XXX-HD6XXX
    x86    - 32-bit X86: Pentium-Pro and above
    x86-64 - 64-bit X86: EM64T and AMD64
hip-clang-cxxflags :  -std=c++11 -isystem "/opt/rocm-4.5.0/llvm/lib/clang/13.0.0/include/.." -isystem /opt/rocm-4.5.0/hsa/include -isystem "/opt/rocm-4.5.0/hip/include" -O3
hip-clang-ldflags  : --driver-mode=g++ -L"/opt/rocm-4.5.0/hip/lib" -O3 -lgcc_s -lgcc -lpthread -lm -lrt

=== Environment Variables
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/local/cuda/bin:/opt/rocm/bin:/opt/dell/srvadmin/bin

== Linux Kernel
Hostname     : my-machine
Linux my-machine 5.10.0-33-amd64 #1 SMP Debian 5.10.226-1 (2024-10-03) x86_64 GNU/Linux
No LSB modules are available.
Distributor ID:	Debian
Description:	Debian GNU/Linux 11 (bullseye)
Release:	11
Codename:	bullseye


```

Any basic program using openMP compiled with gfortran or g++ is working correctly.

---

### 评论 #5 — harkgill-amd (2025-03-11T14:38:22Z)

It looks like your no longer seeing errors related to `hip_runtime.h`, which should be found using `-I/opt/rocm-4.5.0/hip/include` in your `CPP_CONFIG`.

As for the current error with `omp.h`, could you run the following command to search for it's location,
```
find /opt/rocm-4.5.0 -name omp.h
```
If this returns a path to an `omp.h` file, you should be able to compile the sample with 
```
hipcc -fopenmp openmp_helloworld.cpp -o openmp_sample -I<omp.h directory>
```
If the find command does not return any paths, install the `openmp-extras` package and rerun the `make` command to compile.

---

### 评论 #6 — aureliendaut (2025-03-11T15:02:52Z)

Oh that was a miss write in my first message, my original problem is the location of this file `omp.h`.  Sadly no path given and i guess there is no way to work without it ? By `openmp-extras` you're refering to this one ?[https://aur.archlinux.org/packages/openmp-extras](openmp-extras). As i work on a cluster, i do not have all rights but will check out as i believe this will fix my issue, thanks ! 

---

### 评论 #7 — harkgill-amd (2025-03-11T15:32:55Z)

No worries. That link doesn't seem to be pointing to the correct URL, it would be this package specifically,
```
Package: openmp-extras
Version: 13.45.0.40500-56
Priority: optional
Section: devel
Maintainer: Openmp Extras Support <openmp-extras.support@amd.com>
Installed-Size: unknown
Depends: libstdc++6|libstdc++8, libstdc++-5-dev|libstdc++-7-dev, libgcc-5-dev|libgcc-7-dev, rocm-llvm, rocm-device-libs, rocm-core
Recommends: gcc, g++
Download-Size: 9694 kB
APT-Manual-Installed: no
APT-Sources: http://repo.radeon.com/rocm/apt/4.5 ubuntu/main amd64 Packages
Description: OpenMP Extras provides openmp and flang libraries.
  openmp-extras 13.45.0.40500 is based on LLVM 12 and is used for offloading to Radeon GPUs.
```
The `http://repo.radeon.com/rocm/apt/4.5` repo where this package comes from should already be set based on your ROCm installation. Let me know if you run into any issues getting this installed.

---

### 评论 #8 — aureliendaut (2025-03-11T15:49:13Z)

Thanks. Sadly, i can't sudo on my cluster to get it. This package is available as a module but using the version provided by `ROCm 5.2`. If i load this one i got this issue 

```
fatal error : cannot link module '�!4qUv1/opt/spack/linux-debian11-x86_64_v2/gcc-10.4.0/llvm-amdgpu-5.2.0-uvpr6qmfrfvobo5hopocpb7dn5gtmt2e/amdgcn/bitcode/ockl.bc': Invalid value (Producer: 'LLVM14.0.0git' Reader: 'LLVM 13.0.0git')
```

I guess it is a normal incompatibility between rocm `4.5` and `5.2` versions that have been used at the same time ?

---

### 评论 #9 — harkgill-amd (2025-03-13T14:00:46Z)

It look like there's a mismatch between LLVM versions. I see you're using spack for package management, would it be possible to update your complete installation to ROCm 5.5.0 or greater? This is listed as the minimum supported version for many components/packages including `openmp-extras` https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/spack.html#rocm-packages-in-spack.

---

### 评论 #10 — aureliendaut (2025-03-17T07:20:34Z)

In fact i'm not using directly spack, spack is used as module manager on my cluster, which means that using command `module load gcc` refers to spack command. So i can't really update this but i'll check out to try to build my own rocm installation using a more recent one to see if i can compile. 

---

### 评论 #11 — aureliendaut (2025-03-17T09:46:08Z)

If i try to install `openmp-extras` using the following line : 
```
wget http://repo.radeon.com/rocm/apt/4.5/pool/main/o/openmp-extras/openmp-extras_13.45.0.40500-56_amd64.deb
sudo dpkg -i openmp-extras_13.45.0.40500-56_amd64.deb
```
i'm getting this : 
```
 dependency problems prevent configuration of openmp-extras4.5.0:
 openmp-extras4.5.0 depends on libstdc++-5-dev | libstdc++-7-dev; however:
  Package libstdc++-5-dev is not installed.
  Package libstdc++-7-dev is not installed.
 openmp-extras4.5.0 depends on libgcc-5-dev | libgcc-7-dev; however:
  Package libgcc-5-dev is not installed.
  Package libgcc-7-dev is not installed.
 openmp-extras4.5.0 depends on rocm-llvm4.5.0; however:
  Package rocm-llvm4.5.0 is not installed.
 openmp-extras4.5.0 depends on rocm-device-libs4.5.0; however:
  Package rocm-device-libs4.5.0 is not installed.
 openmp-extras4.5.0 depends on rocm-core4.5.0; however:
  Package rocm-core4.5.0 is not installed.

```
After investigating, this is caused by my debian11 which can not support ``openmp-extras`` ?

---

### 评论 #12 — harkgill-amd (2025-03-19T18:18:34Z)

Those errors are due to the lack of Debian 11 support for ROCm and specifically the `openmp-extras` package. You can find a list of supported OSes in our [Supported operating systems](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems) table. If possible, I'd recommend upgrading to ROCm 6.3.3 which comes with Debian 12 support out of the box.

---
