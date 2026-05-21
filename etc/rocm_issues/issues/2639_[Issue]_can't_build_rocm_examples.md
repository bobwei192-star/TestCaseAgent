# [Issue]: can't build rocm examples 

> **Issue #2639**
> **状态**: closed
> **创建时间**: 2023-11-13T10:07:27Z
> **更新时间**: 2024-02-20T07:35:03Z
> **关闭时间**: 2023-11-13T17:59:56Z
> **作者**: bog-dan-ro
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2639

## 描述

### Problem Description

I can not compile any hip samples, it seems either I didn't install something or the sdk is missing something.
These are the rocm packages that I have installed:
```
# dpkg -l | grep -i rocm
ii  comgr                                      2.5.0.50701-98~22.04                    amd64        Library to provide support functions for ROCm code objects.
ii  hipfft                                     1.0.12.50701-98~22.04                   amd64        ROCm FFT marshalling library
ii  hipfft-dev                                 1.0.12.50701-98~22.04                   amd64        ROCm FFT marshalling library
ii  hsa-rocr                                   1.11.0.50701-98~22.04                   amd64        AMD Heterogeneous System Architecture HSA - Linux HSA Runtime for Boltzmann (ROCm) platforms
ii  libhsa-runtime-dev                         5.0.0-1ubuntu0.1                        amd64        HSA Runtime API and runtime for ROCm - development files
ii  libhsa-runtime64-1                         5.0.0-1ubuntu0.1                        amd64        HSA Runtime API and runtime for ROCm
ii  rccl                                       2.17.1.50701-98~22.04                   amd64        ROCm Communication Collectives Library
ii  rccl-dev                                   2.17.1.50701-98~22.04                   amd64        ROCm Communication Collectives Library
ii  rocblas                                    3.1.0.50701-98~22.04                    amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
ii  rocblas-dev                                3.1.0.50701-98~22.04                    amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
ii  rocfft                                     1.0.23.50701-98~22.04                   amd64        ROCm FFT library
ii  rocfft-dev                                 1.0.23.50701-98~22.04                   amd64        ROCm FFT library
ii  rocm-clang-ocl                             0.5.0.50701-98~22.04                    amd64        OpenCL compilation with clang compiler.
ii  rocm-cmake                                 0.10.0.50701-98~22.04                   amd64        rocm-cmake built using CMake
ii  rocm-core                                  5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-dbgapi                                0.70.1.50701-98~22.04                   amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent                           2.0.3.50701-98~22.04                    amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-dev                                   5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                           1.0.0.50701-98~22.04                    amd64        Radeon Open Compute - device libraries
ii  rocm-gdb                                   13.2.50701-98~22.04                     amd64        ROCgdb
ii  rocm-hip-libraries                         5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime                           5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev                       5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-sdk                               5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime                      5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm                                  17.0.0.23382.50701-98~22.04             amd64        ROCm compiler
ii  rocm-ml-libraries                          5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ml-sdk                                5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ocl-icd                               2.0.0.50701-98~22.04                    amd64        clr built using CMake
ii  rocm-opencl                                2.0.0.50701-98~22.04                    amd64        clr built using CMake
ii  rocm-opencl-dev                            2.0.0.50701-98~22.04                    amd64        clr built using CMake
ii  rocm-opencl-runtime                        5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl-sdk                            5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp-sdk                            5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
ii  rocm-smi-lib                               5.0.0.50701-98~22.04                    amd64        AMD System Management libraries
ii  rocm-utils                                 5.7.1.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocminfo                                   1.0.0.50701-98~22.04                    amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool
ii  rocsolver                                  3.23.0.50701-98~22.04                   amd64        AMD ROCm SOLVER library

```

### Operating System

22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 7950X3D

### GPU

Radeon RX 7900 XT

### ROCm Version

5.7.1

### ROCm Component

hip

### Steps to Reproduce

```
root@ubuntu:/opt/rocm/share/hip/samples/0_Intro/square# make
/opt/rocm//hip/bin/hipify-perl square.cu > square.cpp
/opt/rocm//hip/bin/hipcc  square.cpp -o square.out
In file included from <built-in>:1:
In file included from /opt/rocm-5.7.1/llvm/lib/clang/17.0.0/include/__clang_hip_runtime_wrapper.h:50:
/opt/rocm-5.7.1/llvm/lib/clang/17.0.0/include/cuda_wrappers/cmath:27:15: fatal error: 'cmath' file not found
#include_next <cmath>
              ^~~~~~~
1 error generated when compiling for gfx1100.
make: *** [Makefile:44: square.out] Error 1
```

```
root@ubuntu:/opt/rocm/share/hip/samples/0_Intro/square# 
root@ubuntu:/opt/rocm/share/hip/samples/0_Intro/square/b# cmake ..
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
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
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE  
-- hip::amdhip64 is SHARED_LIBRARY
-- /usr/bin/c++: CLANGRT compiler options not supported.
-- Configuring done
-- Generating done
-- Build files have been written to: /opt/rocm/share/hip/samples/0_Intro/square/b
root@ubuntu:/opt/rocm/share/hip/samples/0_Intro/square/b# make
[ 50%] Building CXX object CMakeFiles/square.dir/square.cpp.o
In file included from <built-in>:1:
In file included from /opt/rocm-5.7.1/llvm/lib/clang/17.0.0/include/__clang_hip_runtime_wrapper.h:50:
/opt/rocm-5.7.1/llvm/lib/clang/17.0.0/include/cuda_wrappers/cmath:27:15: fatal error: 'cmath' file not found
#include_next <cmath>
              ^~~~~~~
1 error generated when compiling for gfx1100.
make[2]: *** [CMakeFiles/square.dir/build.make:76: CMakeFiles/square.dir/square.cpp.o] Error 1
make[1]: *** [CMakeFiles/Makefile2:83: CMakeFiles/square.dir/all] Error 2
make: *** [Makefile:91: all] Error 2
```


### Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 9 7950X3D 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X3D 16-Core Processor
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    0                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5759                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65564048(0x3e86d90) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65564048(0x3e86d90) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65564048(0x3e86d90) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-0003d08c00000000               
  Marketing Name:          Radeon RX 7900 XT                  
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      6144(0x1800) KB                    
    L3:                      81920(0x14000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2075                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            84                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          32(0x20)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    1024(0x400)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 494                                
  SDMA engine uCode::      19                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20955136(0x13fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    20955136(0x13fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1100         
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***  

---

## 评论 (5 条)

### 评论 #1 — yxsamliu (2023-11-13T14:29:08Z)

can you recompile the code with -v -H and paste the output? Thanks.

---

### 评论 #2 — bog-dan-ro (2023-11-13T15:21:15Z)

```
/opt/rocm//hip/bin/hipcc  -v -H square.cpp -o square.out
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-5.7.0 23352 d1e13c532a947d0cbfc94759c00dcf152294aa13)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-5.7.0/llvm/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/12
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/12
Candidate multilib: .;@m64
Selected multilib: .;@m64
Found HIP installation: /opt/rocm-5.7.0, version 5.7.31921
 "/opt/rocm-5.7.0/llvm/bin/clang-17" -cc1 -triple amdgcn-amd-amdhsa -aux-triple x86_64-unknown-linux-gnu -emit-obj -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name square.cpp -mrelocation-model pic -pic-level 2 -fhalf-no-semantic-interposition -mframe-pointer=none -fno-rounding-math -mconstructor-aliases -aux-target-cpu x86-64 -fcuda-is-device -mllvm -amdgpu-internalize-symbols -fcuda-allow-variadic-functions -fvisibility=hidden -fapply-global-visibility-to-externs -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/hip.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/ocml.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/ockl.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/oclc_daz_opt_off.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/oclc_unsafe_math_off.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/oclc_finite_only_off.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/oclc_wavefrontsize64_off.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/oclc_isa_version_1100.bc -mlink-builtin-bitcode /opt/rocm-5.7.0/amdgcn/bitcode/oclc_abi_version_500.bc -target-cpu gfx1100 -debugger-tuning=gdb -v -H -sys-header-deps -resource-dir /opt/rocm-5.7.0/llvm/lib/clang/17.0.0 -internal-isystem /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/cuda_wrappers -idirafter /opt/rocm-5.7.0/include -include __clang_hip_runtime_wrapper.h -c-isystem /opt/rocm-5.7.0/llvm/include/gpu-none-llvm -isystem /opt/rocm-5.7.0/include -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++ -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/x86_64-linux-gnu -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/backward -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++ -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/x86_64-linux-gnu -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/backward -internal-isystem /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include -internal-isystem /usr/local/include -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../x86_64-linux-gnu/include -internal-externc-isystem /usr/include/x86_64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -internal-isystem /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include -internal-isystem /usr/local/include -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/12/../../../../x86_64-linux-gnu/include -internal-externc-isystem /usr/include/x86_64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -fdeprecated-macro -fno-autolink -fdebug-compilation-dir=/opt/rocm/share/hip/samples/0_Intro/square -ferror-limit 19 -fhip-new-launch-api -fgnuc-version=4.2.1 -fcxx-exceptions -fexceptions -fcolor-diagnostics -vectorize-loops -vectorize-slp -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -cuid=9abd41d3e95a5ad4 -fcuda-allow-variadic-functions -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o /tmp/square-gfx1100-6156f6.o -x hip square.cpp
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-unknown-linux-gnu
ignoring nonexistent directory "/opt/rocm-5.7.0/llvm/include/gpu-none-llvm"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/x86_64-linux-gnu"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/backward"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/x86_64-linux-gnu"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++/backward"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/12/../../../../x86_64-linux-gnu/include"
ignoring nonexistent directory "/include"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/12/../../../../x86_64-linux-gnu/include"
ignoring nonexistent directory "/include"
ignoring duplicate directory "/usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++"
ignoring duplicate directory "/opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include"
ignoring duplicate directory "/usr/local/include"
ignoring duplicate directory "/usr/include/x86_64-linux-gnu"
ignoring duplicate directory "/usr/include"
ignoring duplicate directory "/usr/local/include"
ignoring duplicate directory "/opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include"
ignoring duplicate directory "/usr/include"
ignoring duplicate directory "/opt/rocm-5.7.0/include"
#include "..." search starts here:
#include <...> search starts here:
 /opt/rocm-5.7.0/include
 /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/cuda_wrappers
 /usr/lib/gcc/x86_64-linux-gnu/12/../../../../include/c++
 /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include
 /usr/local/include
 /usr/include/x86_64-linux-gnu
 /usr/include
End of search list.
In file included from <built-in>:1:
In file included from /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/__clang_hip_runtime_wrapper.h:50:
/opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/cuda_wrappers/cmath:27:15: fatal error: 'cmath' file not found
#include_next <cmath>
              ^~~~~~~
. /opt/rocm-5.7.0/include/hip/hip_runtime.h
.. /usr/include/stdio.h
... /usr/include/x86_64-linux-gnu/bits/libc-header-start.h
... /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/stddef.h
... /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/stdarg.h
... /usr/include/x86_64-linux-gnu/bits/types/__fpos_t.h
.... /usr/include/x86_64-linux-gnu/bits/types/__mbstate_t.h
... /usr/include/x86_64-linux-gnu/bits/types/__fpos64_t.h
... /usr/include/x86_64-linux-gnu/bits/types/__FILE.h
... /usr/include/x86_64-linux-gnu/bits/types/FILE.h
... /usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h
... /usr/include/x86_64-linux-gnu/bits/types/cookie_io_functions_t.h
... /usr/include/x86_64-linux-gnu/bits/stdio_lim.h
... /usr/include/x86_64-linux-gnu/bits/stdio.h
.. /usr/include/assert.h
.. /opt/rocm-5.7.0/include/hip/hip_common.h
.. /opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_runtime.h
... /opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_common.h
... /opt/rocm-5.7.0/include/hip/hip_runtime_api.h
.... /usr/include/string.h
..... /usr/include/x86_64-linux-gnu/bits/libc-header-start.h
..... /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/stddef.h
..... /usr/include/strings.h
...... /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/stddef.h
.... /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/stddef.h
..... /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/__stddef_max_align_t.h
.... /opt/rocm-5.7.0/include/hip/amd_detail/host_defines.h
.... /opt/rocm-5.7.0/include/hip/driver_types.h
.... /opt/rocm-5.7.0/include/hip/texture_types.h
..... /opt/rocm-5.7.0/include/hip/channel_descriptor.h
...... /opt/rocm-5.7.0/include/hip/amd_detail/amd_channel_descriptor.h
....... /opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_vector_types.h
.... /opt/rocm-5.7.0/include/hip/surface_types.h
.... /opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_runtime_pt_api.h
... /opt/rocm-5.7.0/include/hip/amd_detail/hip_ldg.h
... /opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_atomic.h
.... /opt/rocm-5.7.0/include/hip/amd_detail/amd_device_functions.h
..... /opt/rocm-5.7.0/include/hip/amd_detail/math_fwd.h
..... /opt/rocm-5.7.0/include/hip/hip_runtime_api.h
..... /opt/rocm-5.7.0/llvm/lib/clang/17.0.0/include/stddef.h
..... /opt/rocm-5.7.0/include/hip/hip_vector_types.h
..... /opt/rocm-5.7.0/include/hip/amd_detail/device_library_decls.h
..... /opt/rocm-5.7.0/include/hip/amd_detail/amd_warp_functions.h
.... /opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_unsafe_atomics.h
... /opt/rocm-5.7.0/include/hip/amd_detail/amd_surface_functions.h
.... /opt/rocm-5.7.0/include/hip/amd_detail/texture_fetch_functions.h
..... /opt/rocm-5.7.0/include/hip/hip_texture_types.h
..... /opt/rocm-5.7.0/include/hip/amd_detail/ockl_image.h
... /opt/rocm-5.7.0/include/hip/amd_detail/texture_indirect_functions.h
... /opt/rocm-5.7.0/include/hip/hip_runtime_api.h
... /opt/rocm-5.7.0/include/hip/amd_detail/amd_math_functions.h
.... /opt/rocm-5.7.0/include/hip/amd_detail/hip_fp16_math_fwd.h
.... /opt/rocm-5.7.0/include/hip/amd_detail/amd_hip_runtime.h
.. /opt/rocm-5.7.0/include/hip/hip_runtime_api.h
.. /opt/rocm-5.7.0/include/hip/library_types.h
1 error generated when compiling for gfx1100.
```
@yxsamliu is this ^ what you're looking for?

---

### 评论 #3 — yxsamliu (2023-11-13T16:34:26Z)

The compiler founds gcc12 at /usr/lib/gcc/x86_64-linux-gnu/12 and it assumes there is /usr/include/c++/12 but it cannot.

This could be due to gcc-12 is installed but libstdc++-12-dev is not installed, which is required by clang. This can be fixed by either installing libstdc++-12 or g++-12.

---

### 评论 #4 — bog-dan-ro (2023-11-13T17:59:56Z)

It works, thanks a lot. Now all the examples are building without errors.

After I run a few of them I noticed some GPU errors in dmesg. I'll create another bug report tomorrow after I'll do more tests.

---

### 评论 #5 — Denizdius (2024-02-20T07:33:45Z)

Hi I have an same issue with this then I applied the solutions but I get an error ::

denizdius@denizdius-Precision-3561:~/Documents/hip-tests/samples/0_Intro/square$ /opt/rocm/bin/hipify-perl square.cu > square.cpp
denizdius@denizdius-Precision-3561:~/Documents/hip-tests/samples/0_Intro/square$ /opt/rocm/bin/hipcc square.cpp -o square.out.static
denizdius@denizdius-Precision-3561:~/Documents/hip-tests/samples/0_Intro/square$ /opt/rocm/bin/hipcc -use-staticlib square.cpp -o square.out.static
Warning: The -use-staticlib option has been deprecated and is no longer needed.
denizdius@denizdius-Precision-3561:~/Documents/hip-tests/samples/0_Intro/square$ ./square.out
error: 'invalid device ordinal'(101) at square.cpp:61

I am try to use hipfy to convert cuda program to HIP and run on my nvidia gpu.



---
