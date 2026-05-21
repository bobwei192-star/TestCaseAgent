# Build of pytorch fails with Rocm 5.5 (linker error)

> **Issue #2121**
> **状态**: closed
> **创建时间**: 2023-05-08T15:59:41Z
> **更新时间**: 2023-05-24T15:13:42Z
> **关闭时间**: 2023-05-08T19:23:37Z
> **作者**: nob13
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2121

## 描述

Trying to build bleeding edge of pytorch, following the [manual](https://github.com/pytorch/pytorch#install-dependencies) on Github.

My spec: Ryzen 5950x, 7900 XT on Ubuntu 22.04, Kernel 6.2.11 using Conda 23.3.1

I had to install quite a lot of rocm/hip packages in order to get it compile everything, but in the end it fails with a linker error:

```
7/465] Linking CXX executable bin/test_edge_op_registration
FAILED: bin/test_edge_op_registration 
: && /usr/bin/c++ -D_GLIBCXX_USE_CXX11_ABI=1 -fvisibility-inlines-hidden -DUSE_PTHREADPOOL -DNDEBUG -DUSE_KINETO -DLIBKINETO_NOCUPTI -DUSE_FBGEMM -DUSE_QNNPACK -DUSE_PYTORCH_QNNPACK -DUSE_XNNPACK -DSYMBOLICATE_MOBILE_DEBUG_HANDLE -O2 -fPIC -Wall -Wextra -Werror=return-type -Werror=non-virtual-dtor -Werror=range-loop-construct -Werror=bool-operation -Wnarrowing -Wno-missing-field-initializers -Wno-type-limits -Wno-array-bounds -Wno-unknown-pragmas -Wno-unused-parameter -Wno-unused-function -Wno-unused-result -Wno-strict-overflow -Wno-strict-aliasing -Wno-stringop-overflow -Wno-psabi -Wno-error=pedantic -Wno-error=old-style-cast -Wno-invalid-partial-specialization -Wno-unused-private-field -Wno-aligned-allocation-unavailable -Wno-missing-braces -fdiagnostics-color=always -faligned-new -Wno-unused-but-set-variable -Wno-maybe-uninitialized -fno-math-errno -fno-trapping-math -Werror=format -Werror=cast-function-type -Wno-stringop-overflow -DHAVE_AVX2_CPU_DEFINITION -O3 -DNDEBUG -DNDEBUG -rdynamic    -rdynamic  -Wl,--whole-archive,/data/nos/compiling/pytorch/build/lib/libunbox_lib.a,--no-whole-archive test_edge_op_registration/CMakeFiles/test_edge_op_registration.dir/test_operator_registration.cpp.o test_edge_op_registration/CMakeFiles/test_edge_op_registration.dir/test_main.cpp.o -o bin/test_edge_op_registration  -Wl,-rpath,/data/nos/compiling/pytorch/build/lib:/data/nos/anaconda3/lib:  lib/libgtest.a  lib/libunbox_lib.a  lib/libtorch_cpu.so  lib/libprotobuf.a  lib/libc10.so  /data/nos/anaconda3/lib/libmkl_intel_lp64.so  /data/nos/anaconda3/lib/libmkl_gnu_thread.so  /data/nos/anaconda3/lib/libmkl_core.so  -fopenmp  -Wl,-Bstatic  -lpthread  -Wl,-Bdynamic  -lm  -Wl,-Bstatic  -ldl  -Wl,-Bdynamic && :
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `tigetnum@NCURSES6_TINFO_5.0.19991023'
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `del_curterm@NCURSES6_TINFO_5.0.19991023'
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `set_curterm@NCURSES6_TINFO_5.0.19991023'
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `setupterm@NCURSES6_TINFO_5.0.19991023'
collect2: error: ld returned 1 exit status
```


---

## 评论 (2 条)

### 评论 #1 — nob13 (2023-05-08T19:23:37Z)

Could build it with 

```
export LDFLAGS=-lcurses
```

Seems not yet usable, but I still trying to figure out if it's my fault.


---

### 评论 #2 — shelbydavis (2023-05-24T15:13:42Z)

I was not able to get the ``export LDFLAGS=-lncurses`` to work, but after ensuring that ncurses-dev is installed, I changed the following lines in ``pytorch/cmake/Dependencies.cmake`` (starting line 1310 as of commit 30cecc0)
```
    if(ROCM_VERSION_DEV VERSION_GREATER_EQUAL "4.1.0")
      list(APPEND Caffe2_PUBLIC_HIP_DEPENDENCY_LIBS
        roc::rocblas hip::hipfft hip::hiprand roc::hipsparse)
```
to 
```
    if(ROCM_VERSION_DEV VERSION_GREATER_EQUAL "4.1.0")
      list(APPEND Caffe2_PUBLIC_HIP_DEPENDENCY_LIBS
        roc::rocblas hip::hipfft hip::hiprand roc::hipsparse ncurses)
```

---
