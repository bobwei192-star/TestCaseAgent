# [Issue]: HIPCC_LINK_FLAGS_APPEND / HIPCC_COMPILE_FLAGS_APPEND prepending flags instead of appending them

> **Issue #3912**
> **状态**: closed
> **创建时间**: 2024-10-17T13:22:41Z
> **更新时间**: 2024-11-05T15:12:36Z
> **关闭时间**: 2024-11-05T15:09:13Z
> **作者**: Thyre
> **标签**: Under Investigation, ROCm 6.0.0, ROCm 6.1.0, ROCm 6.2.0, ROCm 6.2.3, RX 7700 XT / MI250X, ROCm 6.2.2, ROCm 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/3912

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)
- **ROCm 6.2.3** (颜色: #ededed)
- **RX 7700 XT / MI250X** (颜色: #ededed)
- **ROCm 6.2.2** (颜色: #ededed)
- **ROCm 6.2.1** (颜色: #ededed)

## 描述

### Problem Description

While trying to build [CloverLeaf](https://github.com/UoB-HPC/CloverLeaf) with HIP and MPI on LUMI, I ran into issues when trying to instrument CloverLeaf with [Score-P](https://www.vi-hps.org/projects/score-p). Since building via the Cray compiler wrappers did not work as expected, I followed their documentation and ended up with using `hipcc` directly (see [doc](https://docs.lumi-supercomputer.eu/development/compiling/prgenv/#using-hipcc)):

```console
$ module load PrgEnv-amd

$ export HIPCC_COMPILE_FLAGS_APPEND="--offload-arch=gfx90a $(CC --cray-print-opts=cflags)"
$ export HIPCC_LINK_FLAGS_APPEND=$(CC --cray-print-opts=libs)

$ SCOREP_WRAPPER=OFF cmake -S . -B _build-scorep -DCMAKE_CXX_COMPILER=scorep-hipcc -DCMAKE_C_COMPILER=scorep-cc -DMODEL=hip -DENABLE_MPI=On
$ SCOREP_WRAPPER_INSTRUMENTER_FLAGS="--thread=pthread --hip --mpp=mpi" cmake --build _build-scorep
```

I was able to build CloverLeaf, but when I ran the application, I noticed that Score-P failed to create an experiment directory.
After some digging, I found out why: `HIPCC_LINK_FLAGS_APPEND` ( and likely also `HIPCC_COMPILE_FLAGS_APPEND` ) did not append the flags, but actually prepended them.

This caused `CC --cray-print-opts=libs` to link MPI libraries before the ones of Score-P and therefore fail to link the correct library order.

---

The issue basically boils down to `HIPCC_COMPILE_FLAGS_APPEND` and `HIPCC_LINK_FLAGS_APPEND` prepending flags instead of appending them. I would expect to see these flags appended, similar to what CUDA is doing with `NVCC_PREPEND_FLAGS` and `NVCC_APPEND_FLAGS` (see [here](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/#nvcc-environment-variables)). `hipcc` should probably include similar options to both prepend and append flags.

### Operating System

Ubuntu 22.04 LTS / SLES 15

### CPU

Intel Core i7-12700 / AMD EPYC 7742

### GPU

RX 7700 XT / MI250X

### ROCm Version

ROCm 6.2.3, ROCm 6.2.2, ROCm 6.2.1, ROCm 6.2.0, ROCm 6.1.0, ROCm 6.0.0

### ROCm Component

HIP, HIPCC

### Steps to Reproduce

On a system where ROCm is available:

```console
$ echo "int main(){}" > test.cpp
$ HIPCC_LINK_FLAGS_APPEND="-lappended_flag" hipcc -lcommand_line_flag test.cpp
ld.lld: error: unable to find library -lappended_flag
ld.lld: error: unable to find library -lcommand_line_flag
clang++: error: linker command failed with exit code 1 (use -v to see invocation)
failed to execute:/opt/apps/software/ROCm/6.2.0/lib/llvm/bin/clang++  --offload-arch=gfx1101 -O3 --driver-mode=g++ -O3 --hip-link -lappended_flag   -lcommand_line_flag -x hip test.cpp
```

As one can see, the flag `-lappended_flag` shows up before the `-lcommand_line_flag`, even though `HIPCC_LINK_FLAGS_APPEND` suggests that the flag should be _appended_. 

The same is true for `HIPCC_COMPILE_FLAGS_APPEND`:

```console
$ HIPCC_COMPILE_FLAGS_APPEND="-appended_flag" hipcc -command_line_flag test.cpp
clang++: error: unknown argument: '-appended_flag'
clang++: error: unknown argument: '-command_line_flag'
failed to execute:/opt/apps/software/ROCm/6.2.0/lib/llvm/bin/clang++  --offload-arch=gfx1101 -O3 -appended_flag  --driver-mode=g++ -O3 --hip-link  -command_line_flag -x hip test.cpp
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

It's also worth noting that there's no documentation for both flags. This should probably get fixed as well.

See [this search queue](https://rocm.docs.amd.com/projects/HIP/en/develop/search.html?q=HIPCC_COMPILE_FLAGS_APPEND)

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-10-17T14:56:02Z)

Hi @Thyre, thank you for reporting this issue. I was able to reproduce it using the steps you provided and have opened an internal ticket to address this. I'll also look into getting these environment variables documented. 

---

### 评论 #2 — darren-amd (2024-10-22T14:23:11Z)

Hi @Thyre,

Thanks for reporting this issue. I found that this issue does not occur with hipcc built from the amd-staging branch of [ROCm LLVM](https://github.com/ROCm/llvm-project), as there is a patch for this here: [Append Fix](https://github.com/ROCm/llvm-project/commit/b5e58de141e25825a49dec0199c57ffd8f0140a3).

I spoke with the internal team and this fix will be scheduled for release soon. In the meantime, I suggest building hipcc from source by following these instructions: [Build HIPCC from Source](https://github.com/ROCm/llvm-project/blob/amd-staging/amd/hipcc/README.md) with the fix above included, for example from the branch amd-staging.

---

### 评论 #3 — Thyre (2024-11-05T15:12:35Z)

> Hi @Thyre,
> 
> Thanks for reporting this issue. I found that this issue does not occur with hipcc built from the amd-staging branch of [ROCm LLVM](https://github.com/ROCm/llvm-project), as there is a patch for this here: [Append Fix](https://github.com/ROCm/llvm-project/commit/b5e58de141e25825a49dec0199c57ffd8f0140a3).
> 
> I spoke with the internal team and this fix will be scheduled for release soon. In the meantime, I suggest building hipcc from source by following these instructions: [Build HIPCC from Source](https://github.com/ROCm/llvm-project/blob/amd-staging/amd/hipcc/README.md) with the fix above included, for example from the branch amd-staging.

Thanks a lot for the update. Great to see that this issue is fixed with the latest `hipcc` :smile: 

---
