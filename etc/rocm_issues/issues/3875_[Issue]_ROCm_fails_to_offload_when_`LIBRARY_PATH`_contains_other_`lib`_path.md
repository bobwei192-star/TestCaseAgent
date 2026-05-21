# [Issue]: ROCm fails to offload when `LIBRARY_PATH` contains other `lib` path

> **Issue #3875**
> **状态**: closed
> **创建时间**: 2024-10-09T11:02:51Z
> **更新时间**: 2024-11-12T21:45:48Z
> **关闭时间**: 2024-11-12T21:45:48Z
> **作者**: Thyre
> **标签**: Under Investigation, AMD Instinct MI250X, ROCm 6.0.0, ROCm 5.7.1, ROCm 5.7.0, ROCm 6.1.0, ROCm 6.2.0, AMD Radeon RX 7900 GRE
> **URL**: https://github.com/ROCm/ROCm/issues/3875

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI250X** (颜色: #ededed)
- **ROCm 6.0.0** (颜色: #ededed)
- **ROCm 5.7.1** (颜色: #ededed)
- **ROCm 5.7.0** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)
- **AMD Radeon RX 7900 GRE** (颜色: #ededed)

## 描述

### Problem Description

HPC systems commonly like to use some kind of system to manage programs and libraries and offer them to users. 
Some of these options include OpenHPC, EasyBuild and Spack. However, users can also manually write and maintain their modules with something like `Lmod`.

---

When trying to do offloading on such a system, the chance is high that it will simply fail. The error message on older ROCm versions is completely confusing, newer ones are a bit better in that regard.

ROCm 5.7.0:
```console
$ amdclang -fopenmp --offload-arch=gfx90a test.c
/opt/apps/software/ROCm/5.7.0/llvm/bin/llvm-link: No such file or directory
clang: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)
```

ROCm 6.2.0:
```console
$ amdclang -fopenmp --offload-arch=gfx90a test.c
/opt/apps/software/ROCm/6.2.0/lib/llvm/bin/llvm-link: No such file or directory: '[SOME_OTHER_MODULE_PREFIX]/lib/libomptarget-amdgpu-gfx90a.bc'
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

ROCm will not choose the library folder of ROCm itself. Instead, the bytecode file is searched in the _first_ path in `LIBRARY_PATH` which contains `/lib` in its folder name. This breaks for EasyBuild easily.

On [LUMI](https://lumi-supercomputer.eu/) for example, just doing the following commands is sufficient to trigger the issue:

```console
$ module load LUMI/24.03 partition/G PrgEnv-amd

Lmod is automatically replacing "craype-x86-rome" with "craype-x86-trento".


Lmod is automatically replacing "craype-accel-host" with "craype-accel-amd-gfx90a".


Lmod is automatically replacing "cce/17.0.1" with "amd/6.0.3".


Lmod is automatically replacing "PrgEnv-cray/8.5.0" with "PrgEnv-amd/8.5.0".


Due to MODULEPATH changes, the following have been reloaded:
  1) cray-libsci/24.03.0

The following have been reloaded with a version change:
  1) cray-mpich/8.1.29 => cray-mpich/8.1.28

$ module load libunwind/1.6.2-cpeAMD-24.03

Lmod is automatically replacing "PrgEnv-amd/8.5.0" with "cpeAMD/24.03".


The following have been reloaded with a version change:
  1) cray-mpich/8.1.28 => cray-mpich/8.1.29

$ cc -fopenmp test.c
/opt/rocm-6.0.3/lib/llvm/bin/llvm-link: No such file or directory
clang: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)
```

### Operating System

Ubuntu 22.04 / SLES

### CPU

-/-

### GPU

AMD Instinct MI250X, AMD Radeon RX 7900 GRE

### ROCm Version

ROCm 6.2.0, ROCm 6.1.0, ROCm 6.0.0, ROCm 5.7.1, ROCm 5.7.0

### ROCm Component

llvm-project, ROCm

### Steps to Reproduce

This is extremely easy to reproduce.

#### On a system with an environment system and a ROCm module

With a ROCm module loaded, e.g. 
```lua
------------------------------------------------------------------------------
   /opt/cray/pe/lmod/modulefiles/core/rocm/6.0.3.lua:
------------------------------------------------------------------------------
unsetenv("CRAY_LMOD_AMD_CONTROL_TK_LOAD")
help([[6.0.3
/opt/rocm-6.0.3
This modulefile defines the system paths and environment
variables needed to use the ROCm Toolkit. The ROCm modulefile
enables ROC Profiler, ROC Tracer, HIP, and ROCr.

This module is required to interface with AMD accelerators for
all programming environments.

To use CPE's AMD environment with amd libraries, load the amd
modulefile. The core "amd" compiler modulefile is required if access
to AMD compatible libraries is necessary.

Mixed compiler modules (such as amd-mixed) do not extend the CPE Lmod
hierarchy and can be loaded with core compilers (such as cce).

===================================================================
To see AMD/6.0.3 release information,
  visit https://rocmdocs.amd.com/en/latest
===================================================================

To make this the default version, execute:
/opt/admin-pe/set_default_craypkg/set_default_rocm_6.0.3

Certain components, files or programs contained within this package or
product are Copyright 2021-2023 Hewlett Packard Enterprise Development LP.

]])
whatis("Defines the system paths and environment variables required for the ROCm Toolkit.")
setenv("CRAY_ROCM_DIR","/opt/rocm-6.0.3")
setenv("CRAY_ROCM_PREFIX","/opt/rocm-6.0.3")
setenv("CRAY_ROCM_VERSION","6.0.3")
setenv("ROCM_PATH","/opt/rocm-6.0.3")
setenv("HIP_LIB_PATH","/opt/rocm-6.0.3/lib")
prepend_path("PATH","/opt/rocm-6.0.3/bin")
prepend_path("MANPATH","/opt/rocm-6.0.3/share/man")
prepend_path("CMAKE_PREFIX_PATH","/opt/rocm-6.0.3/lib/cmake/hip")
setenv("CRAY_ROCM_INCLUDE_OPTS","-I/opt/rocm-6.0.3/include -I/opt/rocm-6.0.3/include/rocprofiler -I/opt/rocm-6.0.3/include/roctracer -I/opt/rocm-6.0.3/include/hip -D__HIP_PLATFORM_AMD__")
setenv("CRAY_ROCM_POST_LINK_OPTS"," -L/opt/rocm-6.0.3/lib -L/opt/rocm-6.0.3/lib/rocprofiler -L/opt/rocm-6.0.3/lib/roctracer -lamdhip64")
prepend_path("LD_LIBRARY_PATH","/opt/rocm-6.0.3/lib")
prepend_path("LD_LIBRARY_PATH","/opt/rocm-6.0.3/lib/rocprofiler")
prepend_path("LD_LIBRARY_PATH","/opt/rocm-6.0.3/lib/roctracer")
append_path("PE_PRODUCT_LIST","CRAY_ROCM")
prepend_path("PKG_CONFIG_PATH","/usr/lib64/pkgconfig")
prepend_path("PE_PKGCONFIG_LIBS","rocm-6.0.3")
```

try the following steps:

```console
$ export LIBRARY_PATH=/lib:${LIBRARY_PATH}
$ echo "int main(){return 0;}" >> test.c
$ amdclang -fopenmp --offload-arch=gfx90a test.c
```

This will end in the error message shown above.

#### In the ROCm Docker container

One is not required to have any environment system present. The issue can also be triggered completely manually with the following steps.

```console
$ docker run -it rocm/dev-ubuntu-22.04:6.2.1
$ echo "int main(){return 0;}" > test.c
$ env
HOSTNAME=81f80725142e
PWD=/
HOME=/root
LS_COLORS=[...]
TERM=xterm
SHLVL=1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env
$ # First, show that building works fine when not changing the environment.
$ # ROCm is not in PATH by default, so use absolute path
$ /opt/rocm/bin/amdclang -fopenmp --offload-arch=gfx90a test.c && echo "Success"
Success
$ export LIBRARY_PATH=/lib:${LIBRARY_PATH}
$ /opt/rocm/bin/amdclang -fopenmp --offload-arch=gfx90a test.c && echo "Success"
/opt/rocm-6.2.1/lib/llvm/bin/llvm-link: No such file or directory: '/lib/libomptarget-amdgpu-gfx90a.bc'
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

It's worth noting that only ROCm has this issue. Upstream LLVM works completely fine:

```console
$ module load Clang/18.1.8 ROCm
$ export LIBRARY_PATH=/lib:${LIBRARY_PATH}
$ clang -fopenmp --offload-arch=gfx1101 test.c 
$ echo $?
0
```

---

## 评论 (13 条)

### 评论 #1 — ronlieb (2024-10-09T16:40:36Z)

slightly related : 
-Wl,--disable-new-dtags <- RPATH
-Wl,--enable-new-dtags <- RUNPATH

---

### 评论 #2 — ye-luo (2024-10-09T17:12:52Z)

I'm also suffering from this issue. No problem with upstream llvm.
My computer has hdf5 module setting
```
prepend-path    LIBRARY_PATH /soft/packaging/spack-builds/linux-opensuse_leap15-x86_64/gcc-10.2.0/hdf5-1.10.7-uapcktd3szlmtouy63p4o3nofnsj5au6/lib
```
The above reproducer complains.
```
yeluo@jlselogin7:~> amdclang -fopenmp --offload-arch=gfx90a test.c
/soft/compilers/rocm/rocm-6.2.0/lib/llvm/bin/llvm-link: No such file or directory: '/soft/packaging/spack-builds/linux-opensuse_leap15-x86_64/gcc-10.2.0/hdf5-1.10.7-uapcktd3szlmtouy63p4o3nofnsj5au6/lib/libomptarget-amdgpu-gfx90a.bc'
```

---

### 评论 #3 — Thyre (2024-10-10T07:48:02Z)

As a workaround, one can manually prepend the required path to `LIBRARY_PATH`, but that is cumbersome and fails again once one loads a module prepending something to `LIBRARY_PATH` again.

```console
reuterja@uan01:~> env | grep ^LIBRARY_PATH
LIBRARY_PATH=/appl/lumi/SW/LUMI-24.03/G/EB/libunwind/1.6.2-cpeAMD-24.03/lib:/appl/lumi/SW/LUMI-24.03/G/EB/XZ/5.4.4-cpeAMD-24.03/lib
reuterja@uan01:~> cat test.c
#include <omp.h>

int main( void )
{
    return omp_get_num_threads();
}
reuterja@uan01:~> amdclang -fopenmp --offload-arch=gfx90a test.c
/opt/rocm-6.0.3/lib/llvm/bin/llvm-link: No such file or directory
clang: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)
reuterja@uan01:~> export LIBRARY_PATH=/opt/rocm/llvm/lib:${LIBRARY_PATH}
reuterja@uan01:~> amdclang -fopenmp --offload-arch=gfx90a test.c
reuterja@uan01:~> echo $?
0
```

---

### 评论 #4 — sohaibnd (2024-10-10T23:07:56Z)

Hi @Thyre, it seems LUMI uses the proprietary HPE Cray Operating System which is only available on HPE supercomputers. Could you provide the **full** steps needed to reproduce this using a more easily accessible build framework like EasyBuild (along with steps to access the necessary modules)?

---

### 评论 #5 — Thyre (2024-10-11T05:44:47Z)

Sure. Maybe the issue description was a bit unclear, but there's no module / build system required to reproduce the issue. However, users are most likely to run into this issue with such build & module systems.

Here are some instructions to reproduce the issue with the ROCm Docker container. I'll also add them to the initial issue description:

```console
$ docker run -it rocm/dev-ubuntu-22.04:6.2.1
$ echo "int main(){return 0;}" > test.c
$ env
HOSTNAME=81f80725142e
PWD=/
HOME=/root
LS_COLORS=[...]
TERM=xterm
SHLVL=1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env
$ # First, show that building works fine when not changing the environment.
$ # ROCm is not in PATH by default, so use absolute path
$ /opt/rocm/bin/amdclang -fopenmp --offload-arch=gfx90a test.c && echo "Success"
Success
$ export LIBRARY_PATH=/lib:${LIBRARY_PATH}
$ /opt/rocm/bin/amdclang -fopenmp --offload-arch=gfx90a test.c && echo "Success"
/opt/rocm-6.2.1/lib/llvm/bin/llvm-link: No such file or directory: '/lib/libomptarget-amdgpu-gfx90a.bc'
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

---

### 评论 #6 — sohaibnd (2024-10-18T16:02:10Z)

Thanks @Thyre, I was able to reproduce the issue. There seems to be a problem with the compiler checking for the existence of files (possible a permissions issue). Can you try running with `sudo` as a temporary fix and see if that works? 

`sudo /opt/rocm/bin/amdclang -fopenmp --offload-arch=gfx90a test.c && echo "Success"`

---

### 评论 #7 — Thyre (2024-10-18T16:31:51Z)

Like you mentioned, this is an issue with checking for the existence of files. However, the issue is not related to permissions, but instead related to the directory which gets checked. 

Adding `sudo` certainly changes the behavior, since the whole environment changes. Therefore, if ROCm is in the path for `root`, the issue will not be encountered. This will not solve the issue though, as this has nothing to do with permissions.

The same thing can be reproduced as a `root` user, as one is already in the Docker container.

---

Looking at the argument which is broken in particular:

```
"/opt/apps/software/ROCm/6.2.0/lib/llvm/bin/llvm-link" /tmp/test-openmp-amdgcn-amd-amdhsa-prelinked-7938e4.bc --internalize --only-needed /lib/libomptarget-amdgpu-gfx1101.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/ocml.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/oclc_daz_opt_off.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/oclc_unsafe_math_off.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/oclc_finite_only_off.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/oclc_wavefrontsize64_off.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/oclc_isa_version_1101.bc /opt/apps/software/ROCm/6.2.0/lib/llvm/lib/clang/18/lib/amdgcn/bitcode/oclc_abi_version_500.bc -o /tmp/test-openmp-amdgcn-amd-amdhsa-linked-ab0e83.bc
```

We can simply check for the argument `--only-needed`. We end up in [`clang/lib/Driver/ToolChains/AMDGPUOpenMP.cpp#L208`](https://github.com/ROCm/llvm-project/blob/f0facc9b101ef21e9fc58389280987a7ed256b64/clang/lib/Driver/ToolChains/AMDGPUOpenMP.cpp#L208). 

The final path for the library seems to be created [here](https://github.com/ROCm/llvm-project/blob/f0facc9b101ef21e9fc58389280987a7ed256b64/clang/lib/Driver/ToolChains/AMDGPUOpenMP.cpp#L263), based on [libpath](https://github.com/ROCm/llvm-project/blob/f0facc9b101ef21e9fc58389280987a7ed256b64/clang/lib/Driver/ToolChains/AMDGPUOpenMP.cpp#L236) and [LibDeviceName](https://github.com/ROCm/llvm-project/blob/f0facc9b101ef21e9fc58389280987a7ed256b64/clang/lib/Driver/ToolChains/AMDGPUOpenMP.cpp#L261). Based on that `C.getDriver().Dir` is likely the culprit.

---

### 评论 #8 — Thyre (2024-10-18T16:43:07Z)

The issue was fixed in AOMP between AOMP 19.0-0 and AOMP 19.0-2. Therefore, the pointers in my last comment likely do not apply for ROCm 6.2.x (or something has changed in the calling tools).

```console
$ module load aomp/19.0-0 && export LIBRARY_PATH=/lib:${LIBRARY_PATH}
$ amdclang --version
AOMP_STANDALONE_19.0-0 clang version 19.0.0_AOMP_STANDALONE_19.0-0 (https://github.com/ROCm/llvm-project 486c9004b23449106348b483d9715c5f25814977)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/aomp/19.0-0/bin
$ amdclang -fopenmp --offload-arch=gfx1101 test.c
/opt/apps/software/aomp/19.0-0/bin/llvm-link: No such file or directory: '/lib/../runtimes/runtimes-bins/openmp/libomptarget/libomptarget-amdgpu-gfx1101.bc'
clang: error: linker command failed with exit code 1 (use -v to see invocation)
$ module load aomp/19.0-2 && export LIBRARY_PATH=/lib:${LIBRARY_PATH}
$ amdclang --version
AOMP_STANDALONE_19.0-2 clang version 19.0.0_AOMP_STANDALONE_19.0-2 (https://github.com/ROCm/llvm-project c3a455408b118b8c22f23c7a65d2b5dbf491ab56)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/aomp/19.0-2/bin
Build config: +assertions
$ amdclang -fopenmp --offload-arch=gfx1101 test.c && echo "Success"                                                                                                                                        
Success
```

---

### 评论 #9 — sohaibnd (2024-10-18T19:39:18Z)

@Thyre You're right that `sudo` does not address the root cause. I've continued investigating the issue and the problem is not related to permissions or  `C.getDriver().Dir`.

Usually, the libomptarget file that needs to be linked is in `<amdclang path>/../lib` which the libpath variable you mentioned gets set to by default. However, libpath can be overwritten in FindDebugPerfInLibraryPath.  FindDebugPerfInLibraryPath looks for the first directory in LIBRARY_PATH that ends with "lib" and if one exists, it replaces libpath with this directory's path (without checking for the existence of the libomptarget file). This is not the intended behaviour and will probably have to be changed. I'll keep you updated on the progress of that.

It's interesting that the problem is not present in AOMP 19.0-2 since the potential bug is still present in the source code, can you share the `env` after `module load aomp/19.0-2 && export LIBRARY_PATH=/lib:${LIBRARY_PATH}`?

---

### 评论 #10 — Thyre (2024-10-19T09:11:22Z)

Thanks a lot for the quick update and detailed explanation @sohaibnd.

Regarding the environment, sure! Here's a reproducer with my environment and the output. I installed AOMP 19.0-2 (and all other versions aside from trunk) via the Ubuntu packages you provide:

```console
$ module load aomp/19.0-2                                                                                                                    
$ module show aomp/19.0-2                                                                                                                    
----------------------------------------------------------------------------------------------------------------------------------------------------------
   /opt/apps/modules/Core/Compilers/aomp/19.0-2.lua:
----------------------------------------------------------------------------------------------------------------------------------------------------------
conflict("aomp")
prepend_path("MODULEPATH","/opt/apps/modules/Compiler/MPI/aomp/19.0-2/")
prepend_path("PATH","/opt/apps/software/aomp/19.0-2/bin:/opt/apps/software/aomp/19.0-2/llvm/bin")
prepend_path("LD_LIBRARY_PATH","/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib")
prepend_path("LIBRARY_PATH","/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib")
prepend_path("CPATH","/opt/apps/software/aomp/19.0-2/include:/opt/apps/software/aomp/19.0-2/llvm/include")
prepend_path("MANPATH","/opt/apps/software/aomp/19.0-2/share/man")
family("Compiler")
$ amdclang --version
AOMP_STANDALONE_19.0-2 clang version 19.0.0_AOMP_STANDALONE_19.0-2 (https://github.com/ROCm/llvm-project c3a455408b118b8c22f23c7a65d2b5dbf491ab56)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/aomp/19.0-2/bin
Build config: +assertions
$ env | grep LIBRARY_PATH                                                                                                                    
__LMOD_REF_COUNT_LD_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:1;/opt/apps/software/aomp/19.0-2/llvm/lib:1
LD_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib
__LMOD_REF_COUNT_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:1;/opt/apps/software/aomp/19.0-2/llvm/lib:1
LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib
$ amdclang -fopenmp --offload-arch=gfx1101 test.c && echo "Success"                                                                          
Success
$ export LIBRARY_PATH=/lib:${LIBRARY_PATH}                                                                                                   
$ env | grep LIBRARY_PATH                                                                                                                    
__LMOD_REF_COUNT_LD_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:1;/opt/apps/software/aomp/19.0-2/llvm/lib:1
LD_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib
__LMOD_REF_COUNT_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:1;/opt/apps/software/aomp/19.0-2/llvm/lib:1
LIBRARY_PATH=/lib:/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib
$ amdclang -fopenmp --offload-arch=gfx1101 test.c && echo "Success"                                                                          
Success
$ env                                                                                                                                        
LC_MONETARY=de_DE.UTF-8
LC_TELEPHONE=de_DE.UTF-8
LC_MEASUREMENT=de_DE.UTF-8
LANG=en_US.UTF-8
LC_PAPER=de_DE.UTF-8
LC_NAME=de_DE.UTF-8
LC_ADDRESS=de_DE.UTF-8
LC_IDENTIFICATION=de_DE.UTF-8
LC_NUMERIC=de_DE.UTF-8
LC_TIME=de_DE.UTF-8
USER=jreuter
LOGNAME=jreuter
HOME=/home/jreuter
PATH=/opt/apps/software/aomp/19.0-2/bin:/opt/apps/software/aomp/19.0-2/llvm/bin:/home/jreuter/.local/bin:/home/jreuter/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
SHELL=/bin/zsh
TERM=xterm-256color
XDG_SESSION_ID=244
XDG_RUNTIME_DIR=/run/user/1000
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
XDG_SESSION_TYPE=tty
XDG_SESSION_CLASS=user
MOTD_SHOWN=pam
SSH_TTY=/dev/pts/0
SHLVL=1
PWD=/home/jreuter
OLDPWD=/home/jreuter
EDITOR=vim
ARCHFLAGS=-arch x86_64
PAGER=less
LESS=-R
LMOD_sys=Linux
MODULEPATH_ROOT=/opt/apps/modules
LMOD_PACKAGE_PATH=/opt/apps/config
LMOD_AVAIL_STYLE=en_grouped
MODULEPATH=/opt/apps/modules/Compiler/MPI/aomp/19.0-2:/opt/apps/modules/Core/Compilers:/opt/apps/modules/Core/Tools:/opt/apps/modules/Core/Libraries:/opt/apps/modules/Core/SWAT
BASH_ENV=/opt/apps/lmod/lmod/init/bash
MANPATH=/opt/apps/software/aomp/19.0-2/share/man:/opt/apps/lmod/lmod/share/man::
LMOD_ROOT=/opt/apps/lmod
LMOD_PKG=/opt/apps/lmod/lmod
LMOD_DIR=/opt/apps/lmod/lmod/libexec
LMOD_CMD=/opt/apps/lmod/lmod/libexec/lmod
MODULESHOME=/opt/apps/lmod/lmod
LMOD_SETTARG_FULL_SUPPORT=no
LMOD_VERSION=8.7
__LMOD_REF_COUNT_CPATH=/opt/apps/software/aomp/19.0-2/include:1;/opt/apps/software/aomp/19.0-2/llvm/include:1
CPATH=/opt/apps/software/aomp/19.0-2/include:/opt/apps/software/aomp/19.0-2/llvm/include
__LMOD_REF_COUNT_LD_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:1;/opt/apps/software/aomp/19.0-2/llvm/lib:1
LD_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib
__LMOD_REF_COUNT_LIBRARY_PATH=/opt/apps/software/aomp/19.0-2/lib:1;/opt/apps/software/aomp/19.0-2/llvm/lib:1
LIBRARY_PATH=/lib:/opt/apps/software/aomp/19.0-2/lib:/opt/apps/software/aomp/19.0-2/llvm/lib
LMOD_FAMILY_COMPILER=aomp
LMOD_FAMILY_COMPILER_VERSION=19.0-2
LOADEDMODULES=aomp/19.0-2
__LMOD_REF_COUNT_MANPATH=/opt/apps/software/aomp/19.0-2/share/man:1;/opt/apps/lmod/lmod/share/man:1
__LMOD_REF_COUNT_MODULEPATH=/opt/apps/modules/Compiler/MPI/aomp/19.0-2:1;/opt/apps/modules/Core/Compilers:1;/opt/apps/modules/Core/Tools:1;/opt/apps/modules/Core/Libraries:1;/opt/apps/modules/Core/SWAT:1
__LMOD_REF_COUNT_PATH=/opt/apps/software/aomp/19.0-2/bin:1;/opt/apps/software/aomp/19.0-2/llvm/bin:1;/home/jreuter/.local/bin:1;/home/jreuter/bin:1;/usr/local/bin:2;/usr/local/sbin:1;/usr/sbin:1;/usr/bin:1;/sbin:1;/bin:1;/usr/games:1;/usr/local/games:1;/snap/bin:1
_LMFILES_=/opt/apps/modules/Core/Compilers/aomp/19.0-2.lua
_ModuleTable001_=X01vZHVsZVRhYmxlXyA9IHsKTVR2ZXJzaW9uID0gMywKY19yZWJ1aWxkVGltZSA9IGZhbHNlLApjX3Nob3J0VGltZSA9IGZhbHNlLApkZXB0aFQgPSB7fSwKZmFtaWx5ID0gewpDb21waWxlciA9ICJhb21wIiwKfSwKbVQgPSB7CmFvbXAgPSB7CmZuID0gIi9vcHQvYXBwcy9tb2R1bGVzL0NvcmUvQ29tcGlsZXJzL2FvbXAvMTkuMC0yLmx1YSIsCmZ1bGxOYW1lID0gImFvbXAvMTkuMC0yIiwKbG9hZE9yZGVyID0gMSwKcHJvcFQgPSB7fSwKc3RhY2tEZXB0aCA9IDAsCnN0YXR1cyA9ICJhY3RpdmUiLAp1c2VyTmFtZSA9ICJhb21wLzE5LjAtMiIsCndWID0gIjAwMDAwMDAxOS4qemZpbmFsLS4wMDAwMDAwMDIuKnpmaW5hbCIsCn0sCn0sCm1wYXRoQSA9IHsKIi9vcHQvYXBwcy9t
_ModuleTable002_=b2R1bGVzL0NvbXBpbGVyL01QSS9hb21wLzE5LjAtMiIsICIvb3B0L2FwcHMvbW9kdWxlcy9Db3JlL0NvbXBpbGVycyIsICIvb3B0L2FwcHMvbW9kdWxlcy9Db3JlL1Rvb2xzIiwgIi9vcHQvYXBwcy9tb2R1bGVzL0NvcmUvTGlicmFyaWVzIiwgIi9vcHQvYXBwcy9tb2R1bGVzL0NvcmUvU1dBVCIsCn0sCnN5c3RlbUJhc2VNUEFUSCA9ICIvb3B0L2FwcHMvbW9kdWxlcy9Db3JlL0NvbXBpbGVyczovb3B0L2FwcHMvbW9kdWxlcy9Db3JlL1Rvb2xzOi9vcHQvYXBwcy9tb2R1bGVzL0NvcmUvTGlicmFyaWVzOi9vcHQvYXBwcy9tb2R1bGVzL0NvcmUvU1dBVCIsCn0K
_ModuleTable_Sz_=2
_=/usr/bin/env
```

---

### 评论 #11 — estewart08 (2024-10-23T17:16:09Z)

If a user passes `LIBRARY_PATH` that does not contain a valid path for the openmp bitcode files you definitely will see this error. As a workaround you would need to append a fallback path: `LIBRARY_PATH=/lib:<path-to-rocm/lib/llvm/lib:$LIBRARY_PATH`. We are currently looking into ensuring a known good path will be searched by default if the user provided `LIBRARY_PATH` does not contain one to avoid this workaround.

---

### 评论 #12 — sohaibnd (2024-11-12T21:41:40Z)

@Thyre Thanks for the info, just an update: As you noted the issue had been fixed partially in AOMP 19.0-2 (with [this commit](https://github.com/ROCm/llvm-project/commit/2085f88e5456a9d4ff6abbbe1e9f23e81c30f9e1)). However, as @estewart08 mentioned, if for some reason the directories in `LIBRARY_PATH` do not contain the libomptarget bitcode file, we would still see the error. Another fix has been put in to default to `<clang path>/../lib` for this case (see [commit](https://github.com/ROCm/llvm-project/commit/e3ea27822c6bf53554a93ac777de4fb430227f29)). This should be available in upcoming releases of ROCm and AOMP.

Please let me know if you have any other questions, otherwise I can close this issue as resolved! 

---

### 评论 #13 — Thyre (2024-11-12T21:45:48Z)

Great, thanks a lot for resolving the issue quickly :smile: 

---
