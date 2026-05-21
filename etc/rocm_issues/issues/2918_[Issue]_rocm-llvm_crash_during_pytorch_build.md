# [Issue]: rocm-llvm crash during pytorch build

> **Issue #2918**
> **状态**: closed
> **创建时间**: 2024-01-05T07:29:59Z
> **更新时间**: 2025-04-02T15:27:05Z
> **关闭时间**: 2025-04-02T15:27:04Z
> **作者**: tpkessler
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/2918

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

When compiling pytorch release candidate v2.2.0-rc6, I'm encountering the follwoing compiler crash:
```
clang-17: /usr/src/debug/rocm-llvm/llvm-project-rocm-6.0.0/llvm/lib/CodeGen/SplitKit.cpp:1648: void llvm::SplitEditor::splitLiveThroughBlock(unsigned int, unsigned int, llvm::SlotIndex, unsigned int, llvm::SlotIndex): Assertion `(!LeaveBefore || Idx <= LeaveBefore) && "Interference"' failed.
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace, preprocessed source, and associated run script.
Stack dump:
0.      Program arguments: /opt/rocm/lib/llvm/bin/clang-17 -cc1 -triple amdgcn-amd-amdhsa -aux-triple x86_64-pc-linux-gnu -emit-obj -disable-free -clear-ast-before-backend -main-file-name ReduceNormKernel.hip -mrelocation-model pic -pic-level 2 -fhalf-no-semantic-interposition -mframe-pointer=none -fno-rounding-math -mconstructor-aliases -aux-target-cpu x86-64 -fcuda-is-device -mllvm -amdgpu-internalize-symbols -fcuda-allow-variadic-functions -fvisibility=hidden -fapply-global-visibility-to-externs -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/hip.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/ocml.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/ockl.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/oclc_daz_opt_off.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/oclc_unsafe_math_off.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/oclc_finite_only_off.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/oclc_wavefrontsize64_on.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/oclc_isa_version_900.bc -mlink-builtin-bitcode /opt/rocm/amdgcn/bitcode/oclc_abi_version_500.bc -target-cpu gfx900 -debugger-tuning=gdb -resource-dir /opt/rocm/lib/llvm/lib/clang/17.0.0 -internal-isystem /opt/rocm/lib/llvm/lib/clang/17.0.0/include/cuda_wrappers -idirafter /opt/rocm/include -include __clang_hip_runtime_wrapper.h -c-isystem /opt/rocm/llvm/include/gpu-none-llvm -isystem /opt/rocm/include -D USE_NCCL -D USE_ROCM -D __HIP_PLATFORM_AMD__ -D USE_C10D_NCCL -D TORCH_HIP_BUILD_MAIN_LIB -D ROCM_VERSION=60000 -D TORCH_HIP_VERSION=600 -D ONNX_ML=1 -D ONNXIFI_ENABLE_EXT=1 -D ONNX_NAMESPACE=onnx_torch -D IDEEP_USE_MKL -D HAVE_MMAP=1 -D _FILE_OFFSET_BITS=64 -D HAVE_SHM_OPEN=1 -D HAVE_SHM_UNLINK=1 -D HAVE_MALLOC_USABLE_SIZE=1 -D USE_EXTERNAL_MZCRC -D MINIZ_DISABLE_ZIP_READER_CRC32_CHECKS -D GFLAGS_IS_A_DLL=0 -D GLOG_CUSTOM_PREFIX_SUPPORT -D AT_PER_OPERATOR_HEADERS -D USE_DISTRIBUTED -D USE_C10D_GLOO -D USE_C10D_MPI -D USE_RPC -D USE_TENSORPIPE -D PROTOBUF_USE_DLLS -D __HIP_PLATFORM_AMD__=1 -D USE_PROF_API=1 -D __HIP_PLATFORM_AMD__=1 -D CUDA_HAS_FP16=1 -D USE_ROCM -D __HIP_NO_HALF_OPERATORS__=1 -D __HIP_NO_HALF_CONVERSIONS__=1 -D TORCH_HIP_VERSION=600 -D CAFFE2_USE_MIOPEN -D THRUST_DEVICE_SYSTEM=THRUST_DEVICE_SYSTEM_HIP -I /build/python-pytorch/src/pytorch-rocm/build/aten/src -I /build/python-pytorch/src/pytorch-rocm/aten/src -I /build/python-pytorch/src/pytorch-rocm/build -I /build/python-pytorch/src/pytorch-rocm -I /opt/rocm/include -I /build/python-pytorch/src/pytorch-rocm/build/third_party/gloo -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/gloo -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/tensorpipe/third_party/libuv/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/googletest/googlemock/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/googletest/googletest/include -I /usr/include -I /opt/intel/oneapi/mkl/latest/include -I /build/python-pytorch/src/pytorch-rocm/third_party/gemmlowp -I /build/python-pytorch/src/pytorch-rocm/third_party/neon2sse -I /build/python-pytorch/src/pytorch-rocm/third_party/XNNPACK/include -I /usr/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/benchmark/include -I /usr/include/opencv4 -I /usr/include -I /build/python-pytorch/src/pytorch-rocm/third_party/ittapi/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/eigen -I /build/python-pytorch/src/pytorch-rocm/build/caffe2/contrib/aten -I /build/python-pytorch/src/pytorch-rocm/third_party/onnx -I /build/python-pytorch/src/pytorch-rocm/build/third_party/onnx -I /build/python-pytorch/src/pytorch-rocm/third_party/foxi -I /build/python-pytorch/src/pytorch-rocm/build/third_party/foxi -I /usr/include -I /build/python-pytorch/src/pytorch-rocm/third_party/ideep/include -I /usr/include/oneapi/dnnl -I /opt/intel/oneapi/mkl/latest/include -I /opt/rocm/include -I /opt/rocm/hcc/include -I /opt/rocm/rocblas/include -I /opt/rocm/hipsparse/include -I /build/python-pytorch/src/pytorch-rocm/aten/src/THH -I /build/python-pytorch/src/pytorch-rocm/aten/src/ATen/hip -I /build/python-pytorch/src/pytorch-rocm/aten/src -I /build/python-pytorch/src/pytorch-rocm/build/caffe2/aten/src -I /build/python-pytorch/src/pytorch-rocm/build/aten/src -I /build/python-pytorch/src/pytorch-rocm/build/vulkan -I /build/python-pytorch/src/pytorch-rocm/aten/../third_party/VulkanMemoryAllocator -I /build/python-pytorch/src/pytorch-rocm/aten/src -I /build/python-pytorch/src/pytorch-rocm/aten/src/ATen/.. -I /opt/rocm/include -I /build/python-pytorch/src/pytorch-rocm/c10/hip/../.. -I /build/python-pytorch/src/pytorch-rocm/build -I /build/python-pytorch/src/pytorch-rocm/c10/../ -I /build/python-pytorch/src/pytorch-rocm/build -I /usr/include -I /usr/include -I /build/python-pytorch/src/pytorch-rocm/torch/csrc/api -I /build/python-pytorch/src/pytorch-rocm/torch/csrc/api/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /usr/include -I /opt/intel/oneapi/mkl/latest/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include/hiprand -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /opt/rocm/include -I /build/python-pytorch/src/pytorch-rocm/build/aten/src -I /build/python-pytorch/src/pytorch-rocm/aten/src -I /build/python-pytorch/src/pytorch-rocm/build -I /build/python-pytorch/src/pytorch-rocm -I /opt/rocm/include -I /build/python-pytorch/src/pytorch-rocm/build/third_party/gloo -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/gloo -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/tensorpipe/third_party/libuv/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/googletest/googlemock/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/googletest/googletest/include -I /usr/include -I /opt/intel/oneapi/mkl/latest/include -I /build/python-pytorch/src/pytorch-rocm/third_party/gemmlowp -I /build/python-pytorch/src/pytorch-rocm/third_party/neon2sse -I /build/python-pytorch/src/pytorch-rocm/third_party/XNNPACK/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/benchmark/include -I /usr/include/opencv4 -I /build/python-pytorch/src/pytorch-rocm/third_party/ittapi/include -I /build/python-pytorch/src/pytorch-rocm/cmake/../third_party/eigen -I /build/python-pytorch/src/pytorch-rocm/build/caffe2/contrib/aten -I /build/python-pytorch/src/pytorch-rocm/third_party/onnx -I /build/python-pytorch/src/pytorch-rocm/build/third_party/onnx -I /build/python-pytorch/src/pytorch-rocm/third_party/foxi -I /build/python-pytorch/src/pytorch-rocm/build/third_party/foxi -I /build/python-pytorch/src/pytorch-rocm/third_party/ideep/include -I /usr/include/oneapi/dnnl -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../include/c++/13.2.1 -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../include/c++/13.2.1/x86_64-pc-linux-gnu -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../include/c++/13.2.1/backward -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../include/c++/13.2.1 -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../include/c++/13.2.1/x86_64-pc-linux-gnu -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../include/c++/13.2.1/backward -internal-isystem /opt/rocm/lib/llvm/lib/clang/17.0.0/include -internal-isystem /usr/local/include -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../x86_64-pc-linux-gnu/include -internal-externc-isystem /include -internal-externc-isystem /usr/include -internal-isystem /opt/rocm/lib/llvm/lib/clang/17.0.0/include -internal-isystem /usr/local/include -internal-isystem /usr/lib64/gcc/x86_64-pc-linux-gnu/13.2.1/../../../../x86_64-pc-linux-gnu/include -internal-externc-isystem /include -internal-externc-isystem /usr/include -source-date-epoch 1704351292 -O3 -Wno-shift-count-negative -Wno-shift-count-overflow -Wno-duplicate-decl-specifier -std=c++17 -fdeprecated-macro -fno-autolink -fdebug-compilation-dir=/build/python-pytorch/src/pytorch-rocm/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip -ferror-limit 19 -fhip-new-launch-api -fgnuc-version=4.2.1 -fcxx-exceptions -fexceptions -vectorize-loops -vectorize-slp -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -cuid=d2bba8ddd4887996 -fcuda-allow-variadic-functions -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o /tmp/ReduceNormKernel-gfx900-c2402b.o -x hip /build/python-pytorch/src/pytorch-rocm/aten/src/ATen/native/hip/ReduceNormKernel.hip
1.      <eof> parser at end of file
2.      Code generation
3.      Running pass 'CallGraph Pass Manager' on module '/build/python-pytorch/src/pytorch-rocm/aten/src/ATen/native/hip/ReduceNormKernel.hip'.
4.      Running pass 'Greedy Register Allocator' on function '@_ZN2at6native13reduce_kernelILi256ELi2ENS0_8ReduceOpIdNS0_7NormOpsIdddEEjdLi4EEEEEvT1_'
 #0 0x000055749ba43da3 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/rocm/lib/llvm/bin/clang-17+0x29b9da3)
 ROCm/aomp#1 0x000055749ba40f9f llvm::sys::RunSignalHandlers() (/opt/rocm/lib/llvm/bin/clang-17+0x29b6f9f)
 ROCm/aomp#2 0x000055749ba410ed (/opt/rocm/lib/llvm/bin/clang-17+0x29b70ed)
 ROCm/aomp#3 0x00007f14c0a5c710 (/usr/lib/libc.so.6+0x3e710)
 ROCm/aomp#4 0x00007f14c0aac83c (/usr/lib/libc.so.6+0x8e83c)
 ROCm/aomp#5 0x00007f14c0a5c668 gsignal (/usr/lib/libc.so.6+0x3e668)
 ROCm/aomp#6 0x00007f14c0a444b8 abort (/usr/lib/libc.so.6+0x264b8)
 ROCm/aomp#7 0x00007f14c0a443dc (/usr/lib/libc.so.6+0x263dc)
 ROCm/aomp#8 0x00007f14c0a54d26 (/usr/lib/libc.so.6+0x36d26)
 ROCm/aomp#9 0x000055749af61d80 (/opt/rocm/lib/llvm/bin/clang-17+0x1ed7d80)
ROCm/aomp#10 0x000055749aeba24a (/opt/rocm/lib/llvm/bin/clang-17+0x1e3024a)
ROCm/aomp#11 0x000055749aebaf2a (/opt/rocm/lib/llvm/bin/clang-17+0x1e30f2a)
ROCm/aomp#12 0x000055749aec4b00 (/opt/rocm/lib/llvm/bin/clang-17+0x1e3ab00)
ROCm/aomp#13 0x000055749aec4dd1 (/opt/rocm/lib/llvm/bin/clang-17+0x1e3add1)
ROCm/aomp#14 0x000055749aec8940 (/opt/rocm/lib/llvm/bin/clang-17+0x1e3e940)
ROCm/aomp#15 0x000055749aec94c9 (/opt/rocm/lib/llvm/bin/clang-17+0x1e3f4c9)
ROCm/aomp#16 0x000055749b17f4a8 llvm::RegAllocBase::allocatePhysRegs() (/opt/rocm/lib/llvm/bin/clang-17+0x20f54a8)
ROCm/aomp#17 0x000055749aec33a4 (/opt/rocm/lib/llvm/bin/clang-17+0x1e393a4)
ROCm/aomp#18 0x000055749ad52169 (/opt/rocm/lib/llvm/bin/clang-17+0x1cc8169)
ROCm/aomp#19 0x000055749b359f01 llvm::FPPassManager::runOnFunction(llvm::Function&) (/opt/rocm/lib/llvm/bin/clang-17+0x22cff01)
ROCm/aomp#20 0x000055749a928534 (/opt/rocm/lib/llvm/bin/clang-17+0x189e534)
ROCm/aomp#21 0x000055749b35a9bd llvm::legacy::PassManagerImpl::run(llvm::Module&) (/opt/rocm/lib/llvm/bin/clang-17+0x22d09bd)
ROCm/aomp#22 0x000055749bcb1fbe clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::IntrusiveRefCntPtr<llvm::vfs::FileSystem>, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>) (/opt/rocm/lib/llvm/bin/clang-17+0x2c27fbe)
ROCm/aomp#23 0x000055749cd3557d (/opt/rocm/lib/llvm/bin/clang-17+0x3cab57d)
ROCm/aomp#24 0x000055749dd11e61 clang::ParseAST(clang::Sema&, bool, bool) (/opt/rocm/lib/llvm/bin/clang-17+0x4c87e61)
ROCm/aomp#25 0x000055749c5433e9 clang::FrontendAction::Execute() (/opt/rocm/lib/llvm/bin/clang-17+0x34b93e9)
ROCm/aomp#26 0x000055749c4c6d01 clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/opt/rocm/lib/llvm/bin/clang-17+0x343cd01)
ROCm/aomp#27 0x000055749c61d434 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/opt/rocm/lib/llvm/bin/clang-17+0x3593434)
ROCm/aomp#28 0x0000557499eaea92 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/opt/rocm/lib/llvm/bin/clang-17+0xe24a92)
ROCm/aomp#29 0x0000557499ea9a91 (/opt/rocm/lib/llvm/bin/clang-17+0xe1fa91)
ROCm/aomp#30 0x0000557499eabf3b clang_main(int, char**, llvm::ToolContext const&) (/opt/rocm/lib/llvm/bin/clang-17+0xe21f3b)
ROCm/aomp#31 0x0000557499dd1584 main (/opt/rocm/lib/llvm/bin/clang-17+0xd47584)
ROCm/aomp#32 0x00007f14c0a45cd0 (/usr/lib/libc.so.6+0x27cd0)
ROCm/aomp#33 0x00007f14c0a45d8a __libc_start_main (/usr/lib/libc.so.6+0x27d8a)
ROCm/aomp#34 0x0000557499ea4225 _start (/opt/rocm/lib/llvm/bin/clang-17+0xe1a225)
clang: error: unable to execute command: Aborted (core dumped)
clang: error: clang frontend command failed due to signal (use -v to see invocation)
clang version 17.0.0
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm/llvm/bin
clang: note: diagnostic msg: Error generating preprocessed source(s).
CMake Error at torch_hip_generated_ReduceNormKernel.hip.o.cmake:200 (message):
  Error generating file
  /build/python-pytorch/src/pytorch-rocm/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/./torch_hip_generated_ReduceNormKernel.hip.o

```

This is the source file that triggers the bug:
```C++
// !!! This is a file automatically generated by hipify!!!
#define TORCH_ASSERT_NO_OPERATORS
#include <ATen/Dispatch.h>
#include <ATen/TensorIterator.h>
#include <ATen/native/hip/Reduce.cuh>
#include <ATen/native/DispatchStub.h>
#include <ATen/native/SharedReduceOps.h>
#include <ATen/native/ReduceOps.h>
#include <ATen/native/LinearAlgebra.h>
#include <c10/core/Scalar.h>

namespace at::native {

// This reduction accumulates results as the type `acc_t`. By default, when
// `scalar_t` is complex, `acc_t` is the downgraded real number type.
// Otherwise, `acc_t` and `scalar_t` are the same type.
template <typename scalar_t, typename acc_t=typename scalar_value_type<scalar_t>::type, typename out_t=typename scalar_value_type<scalar_t>::type>
void norm_kernel_cuda_impl(TensorIterator& iter, double p) {
  if (p == static_cast<double>(0)) {
    gpu_reduce_kernel<scalar_t, out_t>(iter, NormZeroOps<scalar_t, acc_t, out_t>(), 0);
  } else if (p == static_cast<double>(1)) {
    gpu_reduce_kernel<scalar_t, out_t>(iter, NormOneOps<scalar_t, acc_t, out_t>(), 0);
  } else if (p == static_cast<double>(2)) {
    gpu_reduce_kernel<scalar_t, out_t>(iter, NormTwoOps<scalar_t, acc_t, out_t>(), 0);
  } else if (p == static_cast<double>(INFINITY)) {
    gpu_reduce_kernel<scalar_t, out_t>(iter, AbsMaxOps<scalar_t, acc_t, out_t>(), 0);
  } else if (p == static_cast<double>(-INFINITY)) {
    gpu_reduce_kernel<scalar_t, out_t>(iter, AbsMinOps<scalar_t, acc_t, out_t>(), std::numeric_limits<acc_t>::infinity());
  } else {
    gpu_reduce_kernel<scalar_t, out_t>(iter, NormOps<scalar_t, acc_t, out_t>{acc_t(p)}, 0);
  }
}

void norm_launch_kernel(TensorIterator& iter, double ord) {
  if (iter.dtype(0) == kHalf) {
    return norm_kernel_cuda_impl<at::Half, float>(iter, ord);
  } else if (iter.input_dtype() == kHalf && iter.dtype(0) == kFloat) {
    // type promotion that does cast and reduction in a single kernel
    return norm_kernel_cuda_impl<at::Half, float, float>(iter, ord);
  }
  else if(iter.dtype(0) == kBFloat16) {
    return norm_kernel_cuda_impl<at::BFloat16, float>(iter, ord);
  } else if (iter.input_dtype() == kBFloat16 && iter.dtype(0) == kFloat) {
    // type promotion that does cast and reduction in a single kernel
    return norm_kernel_cuda_impl<at::BFloat16, float, float>(iter, ord);
  }
  AT_DISPATCH_FLOATING_AND_COMPLEX_TYPES(iter.input_dtype(), "norm_cuda", [&] {
    norm_kernel_cuda_impl<scalar_t>(iter, ord);
  });
}

} // namespace at::native

```

### Operating System

Arch Linux

### CPU

AMD EPYC 7502P

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

No GPU required to trigger this bug.

---

## 评论 (7 条)

### 评论 #1 — davispuh (2024-01-09T13:54:44Z)

I'm seeing this same crash also on Arch:
```
clang-17: /usr/src/debug/rocm-llvm/llvm-project-rocm-6.0.0/llvm/lib/CodeGen/SplitKit.cpp:1648: void llvm::SplitEditor::splitLiveThroughBlock(unsigned int, unsigned in t, llvm::SlotIndex, unsigned int, llvm::SlotIndex):
Assertion `(!LeaveBefore || Idx <= LeaveBefore) && "Interference"' failed.

Core was generated by `/opt/rocm/lib/llvm/bin/clang-17 -cc1 -triple amdgcn-amd-amdhsa -aux-triple x86_'.
Program terminated with signal SIGABRT, Aborted.
Thread 1 (Thread 0x7f4f8a4c30c0 (LWP 223468)):
#0  0x00007f4f89fbf83c in ?? () from /usr/lib/libc.so.6
ROCm/aomp#1  0x00007f4f89f6f668 in raise () from /usr/lib/libc.so.6
ROCm/aomp#2  0x00007f4f89f57542 in abort () from /usr/lib/libc.so.6
ROCm/aomp#3  0x00007f4f89f573dc in ?? () from /usr/lib/libc.so.6
ROCm/aomp#4  0x00007f4f89f67d26 in __assert_fail () from /usr/lib/libc.so.6
ROCm/aomp#5  0x00005637f56add80 in ?? ()
ROCm/aomp#6  0x00005637f560624a in ?? ()
ROCm/aomp#7  0x00005637f5606f2a in ?? ()
ROCm/aomp#8  0x00005637f5610b00 in ?? ()
ROCm/aomp#9  0x00005637f5610dd1 in ?? ()
ROCm/aomp#10 0x00005637f5614940 in ?? ()
ROCm/aomp#11 0x00005637f56154c9 in ?? ()
ROCm/aomp#12 0x00005637f58cb4a8 in llvm::RegAllocBase::allocatePhysRegs() ()
ROCm/aomp#13 0x00005637f560f3a4 in ?? ()
ROCm/aomp#14 0x00005637f549e169 in ?? ()
ROCm/aomp#15 0x00005637f5aa5f01 in llvm::FPPassManager::runOnFunction(llvm::Function&) ()
ROCm/aomp#16 0x00005637f5074534 in ?? ()
ROCm/aomp#17 0x00005637f5aa69bd in llvm::legacy::PassManagerImpl::run(llvm::Module&) ()
ROCm/aomp#18 0x00005637f63fdfbe in clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::IntrusiveRefCntPtr<llvm::vfs::FileSystem>, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream> >) ()
ROCm/aomp#19 0x00005637f748157d in ?? ()
ROCm/aomp#20 0x00005637f845de61 in clang::ParseAST(clang::Sema&, bool, bool) ()
ROCm/aomp#21 0x00005637f6c8f3e9 in clang::FrontendAction::Execute() ()
ROCm/aomp#22 0x00005637f6c12d01 in clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) ()
ROCm/aomp#23 0x00005637f6d69434 in clang::ExecuteCompilerInvocation(clang::CompilerInstance*) ()
ROCm/aomp#24 0x00005637f45faa92 in cc1_main(llvm::ArrayRef<char const*>, char const*, void*) ()
ROCm/aomp#25 0x00005637f45f5a91 in ?? ()
ROCm/aomp#26 0x00005637f45f7f3b in clang_main(int, char**, llvm::ToolContext const&) ()
ROCm/aomp#27 0x00005637f451d584 in main ()
```


---

### 评论 #2 — tpkessler (2024-01-20T08:17:00Z)

I did some further testing and seems like only certain amdgpu targets like `gfx906` or specifying more than one target trigger this bug. A build with only `gfx1030` was successful. @ronlieb do you need more information? This bug is currently blocking the ROCm 6 release on Arch Linux.

---

### 评论 #3 — tpkessler (2024-01-30T14:47:05Z)

I performed `git bisect` on AMD's llvm-project fork. Here's the commit (with the relevant diff) that introduced the bug.
```patch
commit de830efbab42162cbb13f41207734dfd0f92270d
Author: Christudasan Devadasan <Christudasan.Devadasan@amd.com>
Date:   Thu Nov 16 14:38:56 2023 +0530

    [AMDGPU] Try to fix the block prologs broken by RA inserted instructions (#69924)

    The insertion point determined by RA while attempting spills and liverange
    split at the beginning of a block goes wrong at times, and the newly
    inserted vector instructions are placed before the exec-mask restore
    instruction which is wrong. It occurs mainly due to the dependency on
    isBasicBlockPrologue that doesn't account early inserted instructions
    (spills and splits) during RA and causes the block prolog break.

    A better approach for deciding the insertion point should be worked out.
    For now, improving the helper function to consider all possible early
    insertions. This patch includes the spill instructions. The copies
    associated with liverange split should also be included in the block
    prolog.

    Change-Id: I84ce856add0028b5dadf5a518f750a35bb27ecf3

diff --git a/llvm/lib/Target/AMDGPU/SIInstrInfo.cpp b/llvm/lib/Target/AMDGPU/SIInstrInfo.cpp
index 33e1a5f9df71..e3716090d5d9 100644
--- a/llvm/lib/Target/AMDGPU/SIInstrInfo.cpp
+++ b/llvm/lib/Target/AMDGPU/SIInstrInfo.cpp
@@ -7988,8 +7988,16 @@ SIInstrInfo::getSerializableMachineMemOperandTargetFlags() const {
 }

 bool SIInstrInfo::isBasicBlockPrologue(const MachineInstr &MI) const {
-  return !MI.isTerminator() && !MI.isCopy() &&
-         MI.modifiesRegister(AMDGPU::EXEC, &RI);
+  // We need to handle instructions which may be inserted during register
+  // allocation to handle the prolog. The initial prolog instruction may have
+  // been separated from the start of the block by spills and copies inserted
+  // needed by the prolog.
+  uint16_t Opc = MI.getOpcode();
+
+  // FIXME: Copies inserted in the block prolog for live-range split should also
+  // be included.
+  return (isSpillOpcode(Opc) || (!MI.isTerminator() && !MI.isCopy() &&
+                                 MI.modifiesRegister(AMDGPU::EXEC, &RI)));
 }
```
I reverted the change and can confirm that pytorch builds now. Note that the current HEAD is also affected by this bug.

---

### 评论 #4 — jplehr (2024-02-21T19:25:42Z)

Thank you for the report. I'll move this to the top-level ROCm issue tracker to give it some more visibility.

---

### 评论 #5 — cdevadas (2024-02-22T04:52:32Z)

The issue is identified in the internal testing and we're in the process of fixing it.
The liverange split copies and the spill restores inserted at certain blocks where we restore the EXEC mask to handle the divergent control flow is constantly troubling our codegen. These RA inserted instructions in those blocks in question should have been inserted post the EXEC manipulation instruction. The current approach to incorporate the target specific hook to recompute the insertion point for such insertions in the generic core LLVM code is constantly hitting badly. This reported assertion, for instance, is a result when we try to identify a new insertion point while the SplitKit code prohibits that. 
We are taking a new approach to overcome the current restrictions imposed during RA. It will need a significant effort to implement and test it fully.

---

### 评论 #6 — harkgill-amd (2025-01-29T16:05:57Z)

Hi @tpkessler, this issue was resolved with a series of patches, including https://github.com/llvm/llvm-project/pull/109439, that made their way into ROCm 6.3. I was not able to reproduce this crash when building v2.3.0 with ROCm 6.3.2. Could you please give this a try and confirm if you no longer see the errors on your end as well? 

---

### 评论 #7 — tpkessler (2025-04-02T15:27:04Z)

I can confirm this. With ROCm 6.3.3, I'm can compile pytorch without patching LLVM.

---
