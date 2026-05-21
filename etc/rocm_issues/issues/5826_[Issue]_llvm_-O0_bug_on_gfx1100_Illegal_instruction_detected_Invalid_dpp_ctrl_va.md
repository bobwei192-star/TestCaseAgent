# [Issue]: llvm -O0 bug on gfx1100: Illegal instruction detected: Invalid dpp_ctrl value: wavefront shifts are not supported on GFX10+

> **Issue #5826**
> **状态**: closed
> **创建时间**: 2026-01-02T15:55:44Z
> **更新时间**: 2026-02-11T20:04:56Z
> **关闭时间**: 2026-02-11T20:04:56Z
> **作者**: yanite
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5826

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- zichguan-amd

## 描述

### Problem Description

Git commit
commit https://github.com/ggml-org/llama.cpp/commit/b96b82fc852b83ea6f58ffcdc264308f60f79211

Operating systems
Windows

GGML backends
HIP

Problem description & steps to reproduce
Environment

OS: Windows 11
GPU: AMD Radeon RX 7900 XTX (gfx1100 / RDNA3)
HIP SDK / ROCm: 6.4
Compiler: clang++ from ROCm 6.4
Build system: CMake + Ninja
Summary

When building llama.cpp with HIP enabled on Windows using Debug configuration, compilation fails with an illegal DPP instruction error targeting gfx1100.
The same configuration builds successfully in Release mode.

This appears to be a compiler/backend issue triggered only in Debug builds (-O0), where LLVM emits unsupported DPP wavefront shift instructions for GFX10+ GPUs.

CMake Configuration

cmake .. -G Ninja ^
  -DCMAKE_BUILD_TYPE=Debug ^
  -DLLAMA_CURL=OFF ^
  -DCMAKE_C_COMPILER="D:/AMD/ROCm/6.4/bin/clang.exe" ^
  -DCMAKE_CXX_COMPILER="D:/AMD/ROCm/6.4/bin/clang++.exe" ^
  -DCMAKE_CXX_FLAGS="-Og -g -Wno-everything" ^
  -DCMAKE_C_FLAGS="-Og -g -Wno-everything" ^
  -DGGML_HIP=ON ^
  -DGGML_HIPBLAS=ON ^
  -DGGML_HIP_ROCWMMA_FATTN=OFF ^
  -DGGML_HIP_CXX_FLAGS="-w" ^
  -DGPU_TARGETS="gfx1100"
Build Failure

The build fails while compiling a HIP source file:

ggml/src/ggml-cuda/mmf.cu

with the following error:

error: Illegal instruction detected: Invalid dpp_ctrl value:
wavefront shifts are not supported on GFX10+

renamable $vgpr2 = V_MOV_B32_dpp $vgpr2(tied-def 0), $vgpr1,
dpp_ctrl:304, row_mask:15, bank_mask:15

16 warnings and 1 error generated when compiling for gfx1100.

This happens only in Debug builds.
Release builds succeed without any issues.

Additional Observations

GGML_HIP_ROCWMMA_FATTN is explicitly disabled, so this does not appear to be related to ROCWMMA attention kernels.

The error is triggered during compilation, not at runtime.

The generated instruction uses a DPP wavefront shift, which is not supported on GFX10+ (including GFX11 / gfx1100).

This strongly suggests a LLVM/HIP codegen issue under Debug / -O0, where unsupported DPP instructions are emitted.

Using optimization levels like -Og or -O1 avoids similar issues elsewhere, but the Debug configuration still ends up passing -O0 to the HIP compilation.

Expected Behavior

Debug builds with HIP enabled should not emit illegal DPP instructions for GFX10+ GPUs, and should compile successfully, similar to Release builds.

Actual Behavior

Debug build fails during HIP compilation due to illegal DPP wavefront shift instructions.

Possible Cause (Speculation)

LLVM HIP backend appears to emit legacy DPP wavefront shift instructions when compiling with -O0 for gfx1100, which are invalid on GFX10+ architectures.
Release builds likely optimize away or rewrite the affected IR paths.

Please let me know if additional logs, compiler flags, or a minimal reproduction would be helpful.

Thank you for your work on llama.cpp.

First Bad Commit
No response

Compile command
cmake .. -G Ninja ^
  -DCMAKE_BUILD_TYPE=Debug ^
  -DLLAMA_CURL=OFF ^
  -DCMAKE_C_COMPILER="D:/AMD/ROCm/6.4/bin/clang.exe" ^
  -DCMAKE_CXX_COMPILER="D:/AMD/ROCm/6.4/bin/clang++.exe" ^
  -DCMAKE_CXX_FLAGS="-Og -g -Wno-everything" ^
  -DCMAKE_C_FLAGS="-Og -g -Wno-everything" ^
  -DGGML_HIP=ON ^
  -DGGML_HIPBLAS=ON ^
  -DGGML_HIP_ROCWMMA_FATTN=OFF ^
  -DGGML_HIP_CXX_FLAGS="-w" ^
  -DGPU_TARGETS="gfx1100"
Relevant log output
[383/462] Building CXX object ggml/src/ggml-hip/CMakeFiles/ggml-hip.dir/__/ggml-cuda/mmf.cu.obj
FAILED: ggml/src/ggml-hip/CMakeFiles/ggml-hip.dir/__/ggml-cuda/mmf.cu.obj
ccache D:\AMD\ROCm\6.4\bin\clang++.exe -DGGML_BACKEND_BUILD -DGGML_BACKEND_SHARED -DGGML_HIP_NO_VMM -DGGML_SCHED_MAX_COPIES=4 -DGGML_SHARED -DGGML_USE_HIP -DUSE_PROF_API=1 -D_CRT_SECURE_NO_WARNINGS -D_XOPEN_SOURCE=600 -D__HIP_PLATFORM_AMD__=1 -Dggml_hip_EXPORTS -IU:/cpp/llama.cpp/ggml/src/ggml-hip/.. -IU:/cpp/llama.cpp/ggml/src/../include -isystem D:/AMD/ROCm/6.4/include -Og -g -Wno-everything -O0 -g -Xclang -gcodeview -D_DEBUG -D_DLL -D_MT -Xclang --dependent-lib=msvcrtd -std=gnu++17 -Wmissing-declarations -Wmissing-noreturn -Wall -Wextra -Wpedantic -Wcast-qual -Wno-unused-function -Wunreachable-code-break -Wunreachable-code-return -Wmissing-prototypes -Wextra-semi -x hip --offload-arch=gfx1100 -MD -MT ggml/src/ggml-hip/CMakeFiles/ggml-hip.dir/__/ggml-cuda/mmf.cu.obj -MF ggml\src\ggml-hip\CMakeFiles\ggml-hip.dir\__\ggml-cuda\mmf.cu.obj.d -o ggml/src/ggml-hip/CMakeFiles/ggml-hip.dir/__/ggml-cuda/mmf.cu.obj -c U:/cpp/llama.cpp/ggml/src/ggml-cuda/mmf.cu
In file included from U:/cpp/llama.cpp/ggml/src/ggml-cuda/mmf.cu:2:
In file included from U:/cpp/llama.cpp/ggml/src/ggml-cuda\mmf.cuh:3:
In file included from U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:19:
In file included from U:/cpp/llama.cpp/ggml/src/ggml-cuda\common.cuh:21:
U:/cpp/llama.cpp/ggml/src/ggml-hip/..\ggml-common.h:180:9: warning: anonymous types declared in an anonymous union are an extension [-Wnested-anon-types]
  180 |         struct {
      |         ^
U:/cpp/llama.cpp/ggml/src/ggml-hip/..\ggml-common.h:208:9: warning: anonymous types declared in an anonymous union are an extension [-Wnested-anon-types]
  208 |         struct {
      |         ^
U:/cpp/llama.cpp/ggml/src/ggml-hip/..\ggml-common.h:229:9: warning: anonymous types declared in an anonymous union are an extension [-Wnested-anon-types]
  229 |         struct {
      |         ^
U:/cpp/llama.cpp/ggml/src/ggml-hip/..\ggml-common.h:270:9: warning: anonymous types declared in an anonymous union are an extension [-Wnested-anon-types]
  270 |         struct {
      |         ^
U:/cpp/llama.cpp/ggml/src/ggml-hip/..\ggml-common.h:297:9: warning: anonymous types declared in an anonymous union are an extension [-Wnested-anon-types]
  297 |         struct {
      |         ^
U:/cpp/llama.cpp/ggml/src/ggml-hip/..\ggml-common.h:314:9: warning: anonymous types declared in an anonymous union are an extension [-Wnested-anon-types]
  314 |         struct {
      |         ^
In file included from U:/cpp/llama.cpp/ggml/src/ggml-cuda/mmf.cu:2:
In file included from U:/cpp/llama.cpp/ggml/src/ggml-cuda\mmf.cuh:3:
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:754:87: warning: function 'load_ldmatrix' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
  754 |             tile<32, 4, half2> & t, const half2 * __restrict__ xs0, const int stride) {
      |                                                                                       ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:779:90: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
  779 |             tile<16, 8, int> & D, const tile<16, 4, int> & A, const tile<8, 4, int> & B) {
      |                                                                                          ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:801:90: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
  801 |             tile<16, 8, int> & D, const tile<16, 8, int> & A, const tile<8, 8, int> & B) {
      |                                                                                          ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:829:96: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
  829 |             tile<16, 4, half2> & D, const tile<16, 8, half2> & A, const tile<8, 8, half2> & B) {
      |                                                                                                ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:854:97: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
  854 |             tile<16, 8, half2> & D, const tile<16, 8, half2> & A, const tile<16, 8, half2> & B) {
      |                                                                                                 ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:925:96: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
  925 |             tile<16, 8, float> & D, const tile<16, 8, half2> & A, const tile<8, 8, half2> & B) {
      |                                                                                                ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:950:110: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
  950 |             tile<16, 8, float> & D, const tile<16, 8, nv_bfloat162> & A, const tile<8, 8, nv_bfloat162> & B) {
      |                                                                                                              ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:1127:92: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
 1127 |             tile<32, 32, int> & D, const tile<32, 4, int> & A, const tile<32, 4, int> & B) {
      |                                                                                            ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:1163:126: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
 1163 |             tile<32, 8, float> & D, const tile<32, 4, half2> & A, const tile<8, 4, half2, DATA_LAYOUT_I_MAJOR_MIRRORED> & B) {
      |                                                                                                                              ^
U:/cpp/llama.cpp/ggml/src/ggml-cuda\mma.cuh:1183:126: warning: function 'mma' could be declared with attribute 'noreturn' [-Wmissing-noreturn]
 1183 |             tile<32, 4, half2> & D, const tile<32, 4, half2> & A, const tile<8, 4, half2, DATA_LAYOUT_J_MAJOR_MIRRORED> & B) {
      |                                                                                                                              ^
error: Illegal instruction detected: Invalid dpp_ctrl value: wavefront shifts are not supported on GFX10+
renamable $vgpr2 = V_MOV_B32_dpp $vgpr2(tied-def 0), $vgpr1, 304, 15, 15, -1, implicit $exec
16 warnings and 1 error generated when compiling for gfx1100.
ninja: build stopped: subcommand failed.

### Operating System

Windows

### CPU

AMD 7950x

### GPU

AMD Radeon RX 7900xtx

### ROCm Version

ROCm 6.4

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — zichguan-amd (2026-01-02T19:22:32Z)

Hi @yanite, thanks for bringing this to our attention. This indeed looks like a Windows O0 issue, and I can reproduce it with latest TheRock nightly as well. I'll let the compiler team to look further into this.

---

### 评论 #2 — IMbackK (2026-01-05T12:46:55Z)

this problem is also repoduceable on linux 

---

### 评论 #3 — zichguan-amd (2026-01-05T15:30:09Z)

@IMbackK do you have any repro steps on Linux? I've been able to build debug llama.cpp recently on Linux without any issues.

---

### 评论 #4 — IMbackK (2026-01-05T15:52:22Z)

`cmake -DGGML_HIP=On -DCMAKE_BUILD_TYPE=Debug -DGPU_TARGETS=gfx1100 ; make` is sufficient to reproduce the problem here.

its specific to gfx11, building for other architectures works fine.

llamacpp @da143b99403fd526e61f080dcc27aed88b97a914
amdclang: AMD clang version 20.0.0git (/srcdest/rocm-llvm 1b0eada6b0ee93e2e694c8c146d23fca90bc11c5)
i also tested upstream clang version 21.1.6 with the same result.


---

### 评论 #5 — zichguan-amd (2026-01-06T19:33:16Z)

I managed to repro on Linux by building the specific file `ggml/src/ggml-cuda/mmf.cu` directly with `-O0`. Same issue happens when building https://github.com/ROCm/rocm-systems/blob/develop/projects/hip-tests/catch/unit/deviceLib/syncthreadscount.cc with `O0`.

---

### 评论 #6 — zichguan-amd (2026-01-22T23:04:03Z)

The internal team has decided to not fix this particular O0 issue due to significant restructuring needed. That being said, unless you absolutely need to compile with `-O0`, you can work around it and still get a debug build with `-O1` or `-Og` or any other optimization level.

The reason why you still see `-O0` being used with debug build is `CMAKE_CXX_FLAGS` only appends to existing per config flags. See https://cmake.org/cmake/help/latest/variable/CMAKE_LANG_FLAGS.html#variable:CMAKE_%3CLANG%3E_FLAGS. So you need to set 
`CMAKE_CXX_FLAGS_DEBUG` specifically to remove `-O0` for debug builds.

`grep "CMAKE_CXX_FLAGS_DEBUG" build/CMakeCache.txt` will show you the default value after you configure, use that value and replace `-O0` with any optimization level of your liking. I found that `DCMAKE_CXX_FLAGS_DEBUG="-Og -g -Xclang -gcodeview -D_DEBUG -D_DLL -D_MT -Xclang --dependent-lib=msvcrtd"` worked for me. 

Of course you can also use other build types such as RelWithDebInfo.

---

### 评论 #7 — IMbackK (2026-01-22T23:08:14Z)

Wait what?
You are simply going to leave the compiler generating instructions that are not valid for target isa? Im sorry, thats completely absurd and unacceptable. 

---

### 评论 #8 — mgehre-amd (2026-02-04T07:50:07Z)

@zichguan-amd, did you consider
1) changing clang to internally use -O1, even if the user specified -O0
or
2) erroring out in the clang driver with a clear message that says "-O0 is not supported on this GPU target" instead of failing in the backend?

---

### 评论 #9 — zichguan-amd (2026-02-04T16:37:46Z)

Hi @mgehre-amd, I'm sure the compiler team considered various factors when making that decision.

For 1. that would be the same as disabling O0 flag entirely which is not what we want, O0 works in other scenarios, and this issue will be documented as a known issue in future release notes. 

For 2. it's more complicated, I believe catching it in the driver would require similar effort as fixing it and it would still error out. Again, O0 works for gfx10+ in most cases, this issue happens in particular for code that rely on llvm's `ockl_wfred_*` functions, such as wavefront and synchronization operations. There are ISA-specific code branches that don't get eliminated at O0 because the target ISA would be unknown until a project relying on these device libraries is compiled for a particular target. So, it attempts to compile for other branches (with unsupported ISA) as well.
One way to fix this would be to leverage [AMDGPURemoveIncompatibleFunctions](https://github.com/llvm/llvm-project/blob/a71ca9b27c675a6b37c64089f6d742206ad7e8d0/llvm/lib/Target/AMDGPU/AMDGPURemoveIncompatibleFunctions.cpp) which runs at O0 to eliminate that code. This will require an interface change and thus significant restructuring effort.

If you have any alternative suggestions, I'm happy to forward it to the compiler team.

---

### 评论 #10 — zichguan-amd (2026-02-11T20:04:56Z)

Please find the known issue documented in 7.11 preview release notes here https://rocm.docs.amd.com/en/7.11.0-preview/about/release-notes.html#clang-illegal-instruction-error-on-radeon-gpus.

---
