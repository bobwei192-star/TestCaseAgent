# missing hip_ostream_ops.h and unable to find library -lrocm_smi64

> **Issue #2326**
> **状态**: closed
> **创建时间**: 2023-07-19T06:55:39Z
> **更新时间**: 2023-07-19T06:57:48Z
> **关闭时间**: 2023-07-19T06:57:48Z
> **作者**: Cydia2018
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2326

## 描述

In file included from /workspace/rocprofiler/src/core/session/tracer/src/roctracer.h:24,
                 from /workspace/rocprofiler/src/core/hsa/hsa_support.h:106,
                 from /workspace/rocprofiler/src/core/rocprofiler.cpp:42:
/opt/rocm/include/hip/hip_runtime.h:66:2: error: #error ("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
   66 | #error("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
      |  ^~~~~
In file included from /opt/rocm/include/hip/hip_runtime.h:113,
                 from /workspace/rocprofiler/src/core/session/tracer/src/roctracer.h:24,
                 from /workspace/rocprofiler/src/core/hsa/hsa_support.h:106,
                 from /workspace/rocprofiler/src/core/rocprofiler.cpp:42:
/opt/rocm/include/hip/hip_runtime_api.h:6926:2: error: #error ("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
 6926 | #error("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
      |  ^~~~~
In file included from /opt/rocm/include/hip/hip_runtime.h:114,
                 from /workspace/rocprofiler/src/core/session/tracer/src/roctracer.h:24,
                 from /workspace/rocprofiler/src/core/hsa/hsa_support.h:106,
                 from /workspace/rocprofiler/src/core/rocprofiler.cpp:42:
/opt/rocm/include/hip/library_types.h:48:2: error: #error ("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
   48 | #error("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
      |  ^~~~~
In file included from /opt/rocm/include/hip/hip_runtime.h:116,
                 from /workspace/rocprofiler/src/core/session/tracer/src/roctracer.h:24,
                 from /workspace/rocprofiler/src/core/hsa/hsa_support.h:106,
                 from /workspace/rocprofiler/src/core/rocprofiler.cpp:42:
/opt/rocm/include/hip/hip_vector_types.h:38:2: error: #error ("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
   38 | #error("Must define exactly one of __HIP_PLATFORM_AMD__ or __HIP_PLATFORM_NVIDIA__");
      |  ^~~~~
In file included from /workspace/rocprofiler/src/core/hsa/hsa_support.h:106,
                 from /workspace/rocprofiler/src/core/rocprofiler.cpp:42:
/workspace/rocprofiler/src/core/session/tracer/src/roctracer.h:33:10: fatal error: hip_ostream_ops.h: No such file or directory
   33 | #include "hip_ostream_ops.h"
      |          ^~~~~~~~~~~~~~~~~~~
compilation terminated.

----------------------------------------------

[ 40%] Linking HIP executable pcie_bw_test
ld.lld: error: unable to find library -lrocm_smi64
clang-15: error: linker command failed with exit code 1 (use -v to see invocation)
make[2]: *** [tests/microbenchmarks/CMakeFiles/pcie_bw_test.dir/build.make:91: tests/microbenchmarks/pcie_bw_test] Error 1
make[2]: Leaving directory '/workspace/rocprofiler/build'
make[1]: *** [CMakeFiles/Makefile2:1587: tests/microbenchmarks/CMakeFiles/pcie_bw_test.dir/all] Error 2


I have pip install Cppheaderparser, but still encountered above problem.
