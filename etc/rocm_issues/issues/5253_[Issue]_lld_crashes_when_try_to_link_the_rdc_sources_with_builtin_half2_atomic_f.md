# [Issue]: lld crashes when try to link the rdc sources with builtin half2 atomic function

> **Issue #5253**
> **状态**: closed
> **创建时间**: 2025-09-04T06:30:27Z
> **更新时间**: 2025-10-14T14:29:01Z
> **关闭时间**: 2025-10-14T14:29:01Z
> **作者**: zhang-hui-yulo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5253

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- tcgu-amd

## 描述

### Problem Description

lld will crash when try to link my compiled source code has "__builtin_amdgcn_global_atomic_fadd_v2f16" with -fgpu-rdc flag, looks like a bug in ROCm linker, same issue with "__builtin_amdgcn_flat_atomic_fadd_v2f16".

unsafeAtomicAdd works fine with -fgpu-rdc, no crash when use __builtin_amdgcn_global_atomic_fadd_v2f16 without -fgpu-rdc

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 7900X3D 12-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 7.0.0 rc1

### ROCm Component

HIP

### Steps to Reproduce

main.hip
```
#include <hip/hip_runtime.h>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>


extern "C" void test_kernel(half* ptr);

__constant__ half g_count[2];

void set_g_count(half2 count) {
    hipMemcpyToSymbol(g_count, &count, sizeof(g_count));
}

int main() {
    half2 data {2, 3};
    set_g_count(data);
    thrust::host_vector<half> h_arr(2, 0);
    thrust::device_vector<half> d_arr = h_arr;
    
    test_kernel(d_arr.data().get());
    
    h_arr = d_arr;
    
    printf("%f %f\n", (float)h_arr[0], (float)h_arr[1]);
    
    return 0;
}
```

kernel.hip
```
#include <hip/hip_runtime.h>
#include <hip/hip_fp16.h>


extern __constant__ half g_count[2];

__global__ void test(half* data) {
    half2 h2{g_count[0], g_count[1]};
    __builtin_amdgcn_global_atomic_fadd_v2f16(data, h2, __ATOMIC_RELAXED, __OPENCL_MEMORY_SCOPE_WORK_GROUP);
    // this works
    //unsafeAtomicAdd((half2*)data, h2);
}

extern "C" void test_kernel(half* ptr) {
    test<<<1, 64>>>(ptr);
}
```

build command
```
/opt/rocm/lib/llvm/bin/clang++ --offload-arch=gfx1201 -fgpu-rdc -xhip main.hip kernel.hip -o main
```

the linker crash message
```
atomicrmw fadd operand must have floating-point or fixed vector of floating-point type!
  %12 = atomicrmw fadd ptr addrspace(1) %10, %struct.__half2 %11 syncscope("agent") monotonic, align 2, !amdgpu.no.fine.grained.memory !33
 %struct.__half2 = type { %union.anon.1 }LLVM ERROR: Broken module found, compilation aborted!
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace.
Stack dump:
0.	Program arguments: /opt/rocm-7.0.0/lib/llvm/bin/lld -flavor gnu -m elf64_amdgpu --no-undefined -shared -plugin-opt=-amdgpu-internalize-symbols --lto-partitions=8 -plugin-opt=mcpu=gfx1201 --whole-archive -o /tmp/main-gfx1201-627813.out /tmp/main-gfx1201-49bea4.bc /tmp/kernel-gfx1201-b664b3.bc --no-whole-archive
1.	Running pass "verify" on module "ld-temp.o"
 #0 0x000061ecbf2c4310 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x6a4310)
 #1 0x000061ecbf2c18e1 SignalHandler(int) Signals.cpp:0:0
 #2 0x000077b619c45330 (/lib/x86_64-linux-gnu/libc.so.6+0x45330)
 #3 0x000077b619c9eb2c __pthread_kill_implementation ./nptl/pthread_kill.c:44:76
 #4 0x000077b619c9eb2c __pthread_kill_internal ./nptl/pthread_kill.c:78:10
 #5 0x000077b619c9eb2c pthread_kill ./nptl/pthread_kill.c:89:10
 #6 0x000077b619c4527e raise ./signal/../sysdeps/posix/raise.c:27:6
 #7 0x000077b619c288ff abort ./stdlib/abort.c:81:7
 #8 0x000061ecbf13b823 llvm::DisplayGraph(llvm::StringRef, bool, llvm::GraphProgram::Name) (.cold) GraphWriter.cpp:0:0
 #9 0x000061ecbf25989e (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x63989e)
#10 0x000061ecc27cfe56 (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x3bafe56)
#11 0x000061ecc08150c6 llvm::detail::PassModel<llvm::Module, llvm::VerifierPass, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x1bf50c6)
#12 0x000061ecc27862c8 llvm::PassManager<llvm::Module, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x3b662c8)
#13 0x000061ecc081c58f runNewPMPasses(llvm::lto::Config const&, llvm::Module&, llvm::TargetMachine*, unsigned int, bool, llvm::ModuleSummaryIndex*, llvm::ModuleSummaryIndex const*) LTOBackend.cpp:0:0
#14 0x000061ecc081edb7 llvm::lto::opt(llvm::lto::Config const&, llvm::TargetMachine*, unsigned int, llvm::Module&, bool, llvm::ModuleSummaryIndex*, llvm::ModuleSummaryIndex const*, std::vector<unsigned char, std::allocator<unsigned char>> const&) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x1bfedb7)
#15 0x000061ecc0821bda llvm::lto::backend(llvm::lto::Config const&, std::function<llvm::Expected<std::unique_ptr<llvm::CachedFileStream, std::default_delete<llvm::CachedFileStream>>> (unsigned int, llvm::Twine const&)>, unsigned int, llvm::Module&, llvm::ModuleSummaryIndex&) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x1c01bda)
#16 0x000061ecc0810592 llvm::lto::LTO::runRegularLTO(std::function<llvm::Expected<std::unique_ptr<llvm::CachedFileStream, std::default_delete<llvm::CachedFileStream>>> (unsigned int, llvm::Twine const&)>) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x1bf0592)
#17 0x000061ecc0814355 llvm::lto::LTO::run(std::function<llvm::Expected<std::unique_ptr<llvm::CachedFileStream, std::default_delete<llvm::CachedFileStream>>> (unsigned int, llvm::Twine const&)>, llvm::FileCache) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x1bf4355)
#18 0x000061ecbf4ac606 lld::elf::BitcodeCompiler::compile() (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x88c606)
#19 0x000061ecbf3f5be7 void lld::elf::LinkerDriver::compileBitcodeFiles<llvm::object::ELFType<(llvm::endianness)1, true>>(bool) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x7d5be7)
#20 0x000061ecbf425afa void lld::elf::LinkerDriver::link<llvm::object::ELFType<(llvm::endianness)1, true>>(llvm::opt::InputArgList&) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x805afa)
#21 0x000061ecbf42d947 lld::elf::LinkerDriver::linkerMain(llvm::ArrayRef<char const*>) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x80d947)
#22 0x000061ecbf42e5c4 lld::elf::link(llvm::ArrayRef<char const*>, llvm::raw_ostream&, llvm::raw_ostream&, bool, bool) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x80e5c4)
#23 0x000061ecbf2f7906 lld::unsafeLldMain(llvm::ArrayRef<char const*>, llvm::raw_ostream&, llvm::raw_ostream&, llvm::ArrayRef<lld::DriverDef>, bool) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x6d7906)
#24 0x000061ecbf23a99e lld_main(int, char**, llvm::ToolContext const&) (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x61a99e)
#25 0x000061ecbf164cab main (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x544cab)
#26 0x000077b619c2a1ca __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:74:3
#27 0x000077b619c2a28b call_init ./csu/../csu/libc-start.c:128:20
#28 0x000077b619c2a28b __libc_start_main ./csu/../csu/libc-start.c:347:5
#29 0x000061ecbf23a235 _start (/opt/rocm-7.0.0/lib/llvm/bin/lld+0x61a235)
clang++: error: unable to execute command: Aborted (core dumped)
clang++: error: amdgcn-link command failed due to signal (use -v to see invocation)
AMD clang version 20.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-7.0.0 25293 a74b2f2e8c5cc3c88c0325b7554b39a635b7bec3)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-7.0.0/lib/llvm/bin
Configuration file: /opt/rocm-7.0.0/lib/llvm/bin/clang++.cfg
clang++: note: diagnostic msg: Error generating preprocessed source(s).
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — tcgu-amd (2025-09-04T18:33:30Z)

Hi @zhang-hui-yulo, thanks for reaching out and reporting the bug! From the log it seems like during LTO, half is getting lowered to the struct.__half2, causing it to get rejected by the atomicrmw operation which expects a vector type.  Will investigate to see why this happens. Thanks!

Edit: for now, explicitly passing a true vector type (e.g. `_Float16 __attribute__((ext_vector_type(2)));` should fix it)


---

### 评论 #2 — tcgu-amd (2025-09-18T20:31:12Z)

Hi @zhang-hui-yulo, so it seems like the issue that sema checking for the builtin is not correctly configured. So you shouldn't be passing in a half2 type and clang should've caught that during compilation instead of during LTO. I created https://github.com/llvm/llvm-project/pull/158145 to address this. Thanks! 

---

### 评论 #3 — tcgu-amd (2025-10-14T14:29:01Z)

Hi @zhang-hui-yulo, the fix for theclang sema has been completed in the PR. However, the PR is being expanded in scope to address some other bugs as well. I will close this issue for now since the issue itself has been addressed. Thanks! 

---
