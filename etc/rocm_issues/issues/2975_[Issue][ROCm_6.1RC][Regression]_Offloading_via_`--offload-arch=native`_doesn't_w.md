# [Issue][ROCm 6.1RC][Regression]: Offloading via `--offload-arch=native` doesn't work or falls back to CPU

> **Issue #2975**
> **状态**: closed
> **创建时间**: 2024-03-25T10:33:45Z
> **更新时间**: 2025-09-09T14:44:57Z
> **关闭时间**: 2025-09-09T14:44:57Z
> **作者**: Thyre
> **标签**: Under Investigation, AMD Instinct MI250X, ROCm 6.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/2975

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI250X** (颜色: #ededed)
- **ROCm 6.0.0** (颜色: #ededed)

## 描述

### Problem Description

This is a simple, but quite annoying regression:

Starting with ROCm 6.1RC, one can not offload a program using the compiler flag `--offload-arch=native` anymore. 
The flag `--offload-arch=gfx90a` still works. ROCm was always quite flaky with that flag, specifically forcing to have `LIBRARY_PATH` to set up a certain way so that the respective offloading files get found (in contrast to LLVM, where it always works as expected).

Here's an easy reproducer:

```console
$ cat minimal.c
int main( void )
{

}
$ amdclang --version
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.0 24095 dd8a9741464a2adf616a8ca3cc75494392c26db3)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.1.0/lib/llvm/bin
Configuration file: /opt/rocm-6.1.0/lib/llvm/bin/clang.cfg
$ amdclang -fopenmp --offload-arch=native minimal.c 
clang: error: unable to execute command: Executable "clang-linker-wrapper" doesn't exist!
clang: error: linker command failed with exit code 1 (use -v to see invocation)
$ which clang-linker-wrapper
$ find /opt/rocm -name "clang-linker-wrapper"
```

compared to ROCm 6.0.2:

```console
$ amdclang --version
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.0.2 24012 af27734ed982b52a9f1be0f035ac91726fc697e4)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.0.2/lib/llvm/bin
Configuration file: /opt/rocm-6.0.2/lib/llvm/bin/clang.cfg
$ amdclang -fopenmp --offload-arch=native minimal.c 
$ echo $?
0
```

### Operating System

Apptainer -- Ubuntu 22.04.3 LTS on JURECA-DC Evaluation Platform

### CPU

2x AMD EPYC 7443 24-Core Processor

### GPU

4x AMD Instinct MI250X

### ROCm Version

ROCm 6.1.0 RC

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — Thyre (2024-03-25T10:53:01Z)

I have installed ROCm via `amdgpu-install --usecase=rocm`. Maybe something is missing in these packages?
In another installation, where all packages of the repositories are installed, `--offload-arch=native` is working fine. 

---

### 评论 #2 — Thyre (2024-03-25T11:08:04Z)

> I have installed ROCm via `amdgpu-install --usecase=rocm`. Maybe something is missing in these packages? In another installation, where all packages of the repositories are installed, `--offload-arch=native` is working fine.

Even though `--offload-arch=native` works in another installation, it is still broken as it chooses the CPU instead of the present GPU, which can be selected via `--offload-arch=gfx1101`!

```console
$ cat reproducer.c
#include <stdio.h>
#include <omp.h>

int main( void )
{
    #pragma omp target teams num_teams(2)
        {
            printf("omp_is_initial_device() = %d | omp_get_team_num() = %d\n", omp_is_initial_device(), omp_get_team_num());
        }
}
$ amdclang --version
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.0 24095 dd8a9741464a2adf616a8ca3cc75494392c26db3)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/ROCm/6.1.0/lib/llvm/bin
Configuration file: /opt/apps/software/ROCm/6.1.0/lib/llvm/bin/clang.cfg
$ amdclang -fopenmp --offload-arch=native reproducer.c
$ LIBOMPTARGET_DEBUG=-1 OMP_TARGET_OFFLOAD=mandatory ./a.out                                                                                                                                                                                                 
Libomptarget --> Init target library!
Libomptarget --> OMPT: Entering ompt_init
Libomptarget --> OMPT: Trying to load library libomp.so
Libomptarget --> OMPT: Trying to get address of connection routine libomp_ompt_connect
Libomptarget --> OMPT: Library connection handle = 0x733446afb260
Libomptarget --> OMPT: Exit ompt_init
Libomptarget --> Loading RTLs...
Libomptarget --> Loading library 'libomptarget.rtl.amdgpu.nextgen.so'...
Libomptarget --> Successfully loaded library 'libomptarget.rtl.amdgpu.nextgen.so'!
OMPT --> OMPT: Entering OmptCallbackInit
OMPT --> OMPT: Trying to load library libomptarget.so
OMPT --> OMPT: Trying to get address of connection routine libomptarget_ompt_connect
OMPT --> OMPT: Library connection handle = 0x7334469c7940
Libomptarget --> OMPT: Enter libomptarget_ompt_connect: OMPT enabled == 0
Libomptarget --> OMPT: Leave libomptarget_ompt_connect
OMPT --> OMPT: Exiting OmptCallbackInit
Libomptarget --> Registering RTL libomptarget.rtl.amdgpu.nextgen.so supporting 1 devices!
Libomptarget --> Loading library 'libomptarget.rtl.cuda.nextgen.so'...
Libomptarget --> Successfully loaded library 'libomptarget.rtl.cuda.nextgen.so'!
TARGET CUDA RTL --> Unable to load library 'libcuda.so': libcuda.so: cannot open shared object file: No such file or directory!
TARGET CUDA RTL --> Failed to load CUDA shared library
Libomptarget --> No devices supported in this RTL
Libomptarget --> Falling back to original plugin...
Libomptarget --> Loading library 'libomptarget.rtl.cuda.so'...
Target CUDA RTL --> Start initializing CUDA
Target CUDA RTL --> Unable to load library 'libcuda.so': libcuda.so: cannot open shared object file: No such file or directory!
Target CUDA RTL --> Failed to load CUDA shared library
Libomptarget --> Successfully loaded library 'libomptarget.rtl.cuda.so'!
Libomptarget --> Invalid plugin as necessary interface is not found.
Libomptarget --> Loading library 'libomptarget.rtl.x86_64.nextgen.so'...
Libomptarget --> Successfully loaded library 'libomptarget.rtl.x86_64.nextgen.so'!
Libomptarget --> Registering RTL libomptarget.rtl.x86_64.nextgen.so supporting 4 devices!
Libomptarget --> Loading library 'libomptarget.rtl.ppc64.nextgen.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.ppc64.nextgen.so': libomptarget.rtl.ppc64.nextgen.so: cannot open shared object file: No such file or directory!
Libomptarget --> Falling back to original plugin...
Libomptarget --> Loading library 'libomptarget.rtl.ppc64.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.ppc64.so': libomptarget.rtl.ppc64.so: cannot open shared object file: No such file or directory!
Libomptarget --> Loading library 'libomptarget.rtl.aarch64.nextgen.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.aarch64.nextgen.so': libomptarget.rtl.aarch64.nextgen.so: cannot open shared object file: No such file or directory!
Libomptarget --> Falling back to original plugin...
Libomptarget --> Loading library 'libomptarget.rtl.aarch64.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.aarch64.so': libomptarget.rtl.aarch64.so: cannot open shared object file: No such file or directory!
Libomptarget --> RTLs loaded!
Libomptarget --> Image 0x0000000000200378 is NOT compatible with RTL libomptarget.rtl.amdgpu.nextgen.so!
PluginInterface --> Image is compatible with current environment: 
Libomptarget --> Image 0x0000000000200378 is compatible with RTL libomptarget.rtl.x86_64.nextgen.so!
Libomptarget --> RTL 0x000000000048fb10 has index 0!
Libomptarget --> Registering image 0x0000000000200378 with RTL libomptarget.rtl.x86_64.nextgen.so!
Libomptarget --> Done registering entries!
Libomptarget --> Entering target region for device -1 with entry point 0x0000000000202490
Libomptarget --> Use default device id 0
Libomptarget --> Call to omp_get_num_devices returning 4
Libomptarget --> Call to omp_get_num_devices returning 4
Libomptarget --> Call to omp_get_initial_device returning 4
Libomptarget --> Checking whether device 0 is ready.
Libomptarget --> Is the device 0 (local ID 0) initialized? 0
Libomptarget --> Initialization returned 0
Libomptarget --> Device 0 is ready to use.
PluginInterface --> Load data from image 0x0000000000200378
PluginInterface --> Entry point 0x0000000000000000 maps to __omp_offloading_803_3586df7_main_l6 (0x00000000004b55e0)
Libomptarget --> loop trip count is 0.
Libomptarget --> Launching target execution __omp_offloading_803_3586df7_main_l6 with pointer 0x00000000004b55e0 (index=0).
PluginInterface --> Launching kernel __omp_offloading_803_3586df7_main_l6 with 1 blocks and 1 threads in Generic mode
omp_is_initial_device() = 0 | omp_get_team_num() = 0
omp_is_initial_device() = 0 | omp_get_team_num() = 1
Libomptarget --> Unloading target library!
Libomptarget --> Unregistered image 0x0000000000200378 from RTL 0x000000000048fb10!
Libomptarget --> Done unregistering images!
Libomptarget --> Removing translation table for descriptor 0x00000000002023f8
Libomptarget --> Done unregistering library!
Libomptarget --> Deinit target library!
$ amdclang -fopenmp --offload-arch=gfx1101 reproducer.c
$ LIBOMPTARGET_DEBUG=-1 OMP_TARGET_OFFLOAD=mandatory ./a.out                                                                                                                                                                                                  jreuter@zam226
Libomptarget --> Init target library!
Libomptarget --> OMPT: Entering ompt_init
Libomptarget --> OMPT: Trying to load library libomp.so
Libomptarget --> OMPT: Trying to get address of connection routine libomp_ompt_connect
Libomptarget --> OMPT: Library connection handle = 0x7a70b345d260
Libomptarget --> OMPT: Exit ompt_init
Libomptarget --> Loading RTLs...
Libomptarget --> Loading library 'libomptarget.rtl.amdgpu.nextgen.so'...
Libomptarget --> Successfully loaded library 'libomptarget.rtl.amdgpu.nextgen.so'!
OMPT --> OMPT: Entering OmptCallbackInit
OMPT --> OMPT: Trying to load library libomptarget.so
OMPT --> OMPT: Trying to get address of connection routine libomptarget_ompt_connect
OMPT --> OMPT: Library connection handle = 0x7a70b3329940
Libomptarget --> OMPT: Enter libomptarget_ompt_connect: OMPT enabled == 0
Libomptarget --> OMPT: Leave libomptarget_ompt_connect
OMPT --> OMPT: Exiting OmptCallbackInit
Libomptarget --> Registering RTL libomptarget.rtl.amdgpu.nextgen.so supporting 1 devices!
Libomptarget --> Loading library 'libomptarget.rtl.cuda.nextgen.so'...
Libomptarget --> Successfully loaded library 'libomptarget.rtl.cuda.nextgen.so'!
TARGET CUDA RTL --> Unable to load library 'libcuda.so': libcuda.so: cannot open shared object file: No such file or directory!
TARGET CUDA RTL --> Failed to load CUDA shared library
Libomptarget --> No devices supported in this RTL
Libomptarget --> Falling back to original plugin...
Libomptarget --> Loading library 'libomptarget.rtl.cuda.so'...
Target CUDA RTL --> Start initializing CUDA
Target CUDA RTL --> Unable to load library 'libcuda.so': libcuda.so: cannot open shared object file: No such file or directory!
Target CUDA RTL --> Failed to load CUDA shared library
Libomptarget --> Successfully loaded library 'libomptarget.rtl.cuda.so'!
Libomptarget --> Invalid plugin as necessary interface is not found.
Libomptarget --> Loading library 'libomptarget.rtl.x86_64.nextgen.so'...
Libomptarget --> Successfully loaded library 'libomptarget.rtl.x86_64.nextgen.so'!
Libomptarget --> Registering RTL libomptarget.rtl.x86_64.nextgen.so supporting 4 devices!
Libomptarget --> Loading library 'libomptarget.rtl.ppc64.nextgen.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.ppc64.nextgen.so': libomptarget.rtl.ppc64.nextgen.so: cannot open shared object file: No such file or directory!
Libomptarget --> Falling back to original plugin...
Libomptarget --> Loading library 'libomptarget.rtl.ppc64.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.ppc64.so': libomptarget.rtl.ppc64.so: cannot open shared object file: No such file or directory!
Libomptarget --> Loading library 'libomptarget.rtl.aarch64.nextgen.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.aarch64.nextgen.so': libomptarget.rtl.aarch64.nextgen.so: cannot open shared object file: No such file or directory!
Libomptarget --> Falling back to original plugin...
Libomptarget --> Loading library 'libomptarget.rtl.aarch64.so'...
Libomptarget --> Unable to load library 'libomptarget.rtl.aarch64.so': libomptarget.rtl.aarch64.so: cannot open shared object file: No such file or directory!
Libomptarget --> RTLs loaded!
TARGET AMDGPU RTL --> Compatible: Exact match   [Image: gfx1101]        :       [Env: gfx1101]
PluginInterface --> Image is compatible with current environment: gfx1101
Libomptarget --> Image 0x0000000000200380 is compatible with RTL libomptarget.rtl.amdgpu.nextgen.so!
Libomptarget --> RTL 0x0000000001b0ab90 has index 0!
Libomptarget --> Registering image 0x0000000000200380 with RTL libomptarget.rtl.amdgpu.nextgen.so!
Libomptarget --> Done registering entries!
Libomptarget --> Entering target region for device -1 with entry point 0x00000000002072d0
Libomptarget --> Use default device id 0
Libomptarget --> Call to omp_get_num_devices returning 1
Libomptarget --> Call to omp_get_num_devices returning 1
Libomptarget --> Call to omp_get_initial_device returning 1
Libomptarget --> Checking whether device 0 is ready.
Libomptarget --> Is the device 0 (local ID 0) initialized? 0
TARGET AMDGPU RTL --> Using a maximum of 4 HSA queues
Libomptarget --> Initialization returned 0
Libomptarget --> Device 0 is ready to use.
PluginInterface --> Load data from image 0x0000000000200380
TARGET AMDGPU RTL --> ELFABIVERSION Version: 3
TARGET AMDGPU RTL --> MemoryManagerTy::allocate: size 24 with host pointer 0x0000000000000000.
TARGET AMDGPU RTL --> findBucket: Size 24 is floored to 16.
TARGET AMDGPU RTL --> Cannot find a node in the FreeLists. Allocate on device.
TARGET AMDGPU RTL --> Node address 0x0000000001c71c70, target pointer 0x00007a70b2e42000, size 24
TARGET AMDGPU RTL --> MemoryManagerTy::free: target memory 0x00007a70b2e42000.
TARGET AMDGPU RTL --> findBucket: Size 24 is floored to 16.
TARGET AMDGPU RTL --> Found its node 0x0000000001c71c70. Insert it to bucket 3.
PluginInterface --> Succesfully write 24 bytes associated with global symbol '__omp_rtl_device_environment' to the device (0x7a70b2e40e68 -> 0x7fff0ce33410).
PluginInterface --> Global symbol '__omp_offloading_803_3586df7_main_l6_exec_mode' was found in the ELF image and 1 bytes will copied from 0x200f0a to 0x7fff0ce33328.
PluginInterface --> Global symbol '__omp_offloading_803_3586df7_main_l6_wg_size' was found in the ELF image and 2 bytes will copied from 0x200f08 to 0x1bcd280.
TARGET AMDGPU RTL --> ELFABIVersion: 3
PluginInterface --> Entry point 0x0000000000000000 maps to __omp_offloading_803_3586df7_main_l6 (0x0000000001bcd1f0)
Libomptarget --> loop trip count is 0.
Libomptarget --> Launching target execution __omp_offloading_803_3586df7_main_l6 with pointer 0x0000000001bcd1f0 (index=0).
PluginInterface --> Launching kernel __omp_offloading_803_3586df7_main_l6 with 2 blocks and 257 threads in Generic mode
TARGET AMDGPU RTL --> MemoryManagerTy::allocate: size 256 with host pointer 0x0000000000000000.
TARGET AMDGPU RTL --> findBucket: Size 256 is floored to 256.
TARGET AMDGPU RTL --> Cannot find a node in the FreeLists. Allocate on device.
TARGET AMDGPU RTL --> Node address 0x0000000001c71c40, target pointer 0x00007a70b2e34000, size 256
TARGET AMDGPU RTL --> MemoryManagerTy::allocate: size 8 with host pointer 0x0000000000000000.
TARGET AMDGPU RTL --> findBucket: Size 8 is floored to 8.
TARGET AMDGPU RTL --> Cannot find a node in the FreeLists. Allocate on device.
TARGET AMDGPU RTL --> Node address 0x0000000001c71ca0, target pointer 0x00007a70b2e32000, size 8
TARGET AMDGPU RTL --> MemoryManagerTy::free: target memory 0x00007a70b2e32000.
TARGET AMDGPU RTL --> findBucket: Size 8 is floored to 8.
TARGET AMDGPU RTL --> Found its node 0x0000000001c71ca0. Insert it to bucket 2.
PluginInterface --> Succesfully write 8 bytes associated with global symbol 'service_thread_buf' to the device (0x7a70b2e40e80 -> 0x7fff0ce330c8).
TARGET AMDGPU RTL --> Hostrpc buffer allocated at 0x7a6f9ac00000 and service thread started
TARGET AMDGPU RTL --> Setting fields of ImplicitArgs for COV5
TARGET AMDGPU RTL --> Using Queue: 0x1c32460 with HSA Queue: 0x7a70b2e5c000
omp_is_initial_device() = 0 | omp_get_team_num() = 0
omp_is_initial_device() = 0 | omp_get_team_num() = 1
TARGET AMDGPU RTL --> MemoryManagerTy::free: target memory 0x00007a70b2e34000.
TARGET AMDGPU RTL --> findBucket: Size 256 is floored to 256.
TARGET AMDGPU RTL --> Found its node 0x0000000001c71c40. Insert it to bucket 7.
Libomptarget --> Unloading target library!
Libomptarget --> Unregistered image 0x0000000000200380 from RTL 0x0000000001b0ab90!
Libomptarget --> Done unregistering images!
Libomptarget --> Removing translation table for descriptor 0x0000000000207308
Libomptarget --> Done unregistering library!
Libomptarget --> Deinit target library!
```

Note the difference between `--offload-arch=native` and `--offload-arch=gfx1101`

**With `native`**:
```
Libomptarget --> Image 0x0000000000200378 is NOT compatible with RTL libomptarget.rtl.amdgpu.nextgen.so!
PluginInterface --> Image is compatible with current environment: 
Libomptarget --> Image 0x0000000000200378 is compatible with RTL libomptarget.rtl.x86_64.nextgen.so!
Libomptarget --> RTL 0x000000000048fb10 has index 0!
Libomptarget --> Registering image 0x0000000000200378 with RTL libomptarget.rtl.x86_64.nextgen.so!
```

**With `gfx1101`**:
```
Libomptarget --> RTLs loaded!
TARGET AMDGPU RTL --> Compatible: Exact match   [Image: gfx1101]        :       [Env: gfx1101]
PluginInterface --> Image is compatible with current environment: gfx1101
Libomptarget --> Image 0x0000000000200380 is compatible with RTL libomptarget.rtl.amdgpu.nextgen.so!
Libomptarget --> RTL 0x0000000001b0ab90 has index 0!
Libomptarget --> Registering image 0x0000000000200380 with RTL libomptarget.rtl.amdgpu.nextgen.so!
```

---

### 评论 #3 — estewart08 (2024-03-27T21:22:28Z)

clang-linker-wrapper is currently in the ```rocm-llvm-dev``` package. This is going to be moved to the default ```rocm-llvm``` package. Looking at ROCm 6.0.0 and 5.7.0 ```--offload-arch=native``` has the same behavior where the cpu is being used, but show slightly different debug output. Do you have a current ROCm version where you are seeing native offload to the GPU?

---

### 评论 #4 — Thyre (2024-03-28T05:24:14Z)

I've had another close look at what's happening with older ROCm versions and can confirm that these also offload to the host instead of a GPU. This is in contrast to Clang/LLVM, where GPUs are targeted by default for both NVIDIA and AMD GPUs.

---

### 评论 #5 — ppanchad-amd (2024-07-04T19:07:31Z)

@Thyre Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #6 — elsampsa (2024-08-22T13:32:36Z)

As of today and with rocm-6.2.0:
this works:
```bash
/opt/rocm-6.2.0/lib/llvm/bin/clang++ -D__HIP_ROCclr__=1 --offload-arch=gfx908 -o CMakeFiles/hip_comp.dir/src/vector_add.hip.o -x hip -c /home/sampsa/amd/doodles/hip_doodle0/src/vector_add.hip
```
but this still does not:
```
/opt/rocm-6.2.0/lib/llvm/bin/clang++ -D__HIP_ROCclr__=1 --offload-arch=native -o CMakeFiles/hip_comp.dir/src/vector_add.hip.o -x hip -c /home/sampsa/amd/doodles/hip_doodle0/src/vector_add.hip
clang++: error: cannot determine amdgcn architecture: /opt/rocm-6.2.0/lib/llvm/bin/amdgpu-arch: ; consider passing it via '--offload-arch'
```
so the `--offload-arch=native` seems to be broken.


---

### 评论 #7 — adanalis (2025-01-31T17:45:09Z)

It works for me with rocm-6.3.2

/opt/rocm/bin/amdclang++ -D__HIP_ROCclr__=1 -O2 -g -DNDEBUG --offload-arch=native -W -Wall -Wextra -Wshadow -o kernel.o -x hip -c kernel.cpp


---

### 评论 #8 — Thyre (2025-05-06T06:37:20Z)

With ROCm 6.4.0, I get the following error message:

```console
$ amdclang -fopenmp --offload-arch=native minimal.c
clang-offload-wrapper: Not enough positional command line arguments specified!
Must specify at least 1 positional argument: See: /opt/apps/software/ROCm/6.4.0/lib/llvm/bin/clang-offload-wrapper --help
clang: error: linker command failed with exit code 1 (use -v to see invocation)
$ which clang-offload-wrapper
/opt/apps/software/ROCm/6.4.0/llvm/bin/clang-offload-wrapper
```

Checking ROCm 6.3.0, `native` still targets the host and not the GPU:

```console
$ amdclang -fopenmp --offload-arch=native minimal.c
$ LIBOMPTARGET_DEBUG=-1 OMP_TARGET_OFFLOAD=mandatory ./a.out
[...]
omptarget --> Registered 'libomptarget.rtl.amdgpu.so' with 1 plugin visible devices!
omptarget --> Attempting to load library 'libomptarget.rtl.cuda.so'...
omptarget --> Successfully loaded library 'libomptarget.rtl.cuda.so'!
TARGET CUDA RTL --> Unable to load library 'libcuda.so': libcuda.so: cannot open shared object file: No such file or directory!
TARGET CUDA RTL --> Failed to load CUDA shared library
omptarget --> No devices supported in this RTL
omptarget --> Attempting to load library 'libomptarget.rtl.x86_64.so'...
omptarget --> Successfully loaded library 'libomptarget.rtl.x86_64.so'!
OMPT --> Entering connectLibrary (libomptarget)
OMPT --> Trying to load library libomptarget.so
OMPT --> Trying to get address of connection routine ompt_libomptarget_connect
OMPT --> Library connection handle = 0x758ac2781660
OMPT --> Enter ompt_libomptarget_connect
OMPT --> Leave ompt_libomptarget_connect
OMPT --> Exiting connectLibrary (libomptarget)
omptarget --> Registered 'libomptarget.rtl.x86_64.so' with 4 plugin visible devices!
omptarget --> RTLs loaded!
omptarget --> Image 0x0000000000200378 is NOT compatible with RTL libomptarget.rtl.amdgpu.so!
omptarget --> Image 0x0000000000200378 is compatible with RTL libomptarget.rtl.x86_64.so!
[...]
```

---

### 评论 #9 — harkgill-amd (2025-07-18T14:45:56Z)

Hi @Thyre, the `clang-offload-wrapper` is from the "old driver" and has since been deleted upstream. In place of this, the "new driver" now uses the `clang-linker-wrapper` which successfully offloads with `--offload-arch=native`.

Future releases of ROCm will use this new driver OOB. As a workaround in ROCm 6.4.1, you can pass the `--no-opaque-offload-linker` flag to force the use of the new driver for OpenMP. The following compiles successfully on my end and targets the GPU,
```
amdclang -fopenmp --offload-arch=native --no-opaque-offload-linker reproducer.c 
```

---
