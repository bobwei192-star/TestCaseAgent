# [Issue]: Porting nvdiffrast to AMD Radeon W7900 (gfx1100) - Compilation and Linking Issues

> **Issue #3471**
> **状态**: closed
> **创建时间**: 2024-07-29T09:45:49Z
> **更新时间**: 2024-08-15T13:32:27Z
> **关闭时间**: 2024-08-15T13:32:27Z
> **作者**: yttbgf
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3471

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I am in the process of porting nvdiffrast to support the AMD Radeon W7900 (gfx1100).
Here are the translations of your questions into English:
 Can you answer the following questions:
1.
- What are the equivalents of CUDA functions in HIP? Are there any alternative versions? What are the names of the header files and the linking libraries? (The official documentation section 6.1.3 states support, but compilation does not recognize them)
- `__all_sync`
- `__ballot_sync`
- `__syncwarp`
- `__any_sync`

The grep command output:
```
./lib/llvm/lib/clang/17/include/__clang_cuda_intrinsics.h:inline __device__ int __all_sync(unsigned int mask, int pred) {
./include/hipify/include/__clang_cuda_intrinsics.h:inline __device__ int __all_sync(unsigned int mask, int pred)
```
The header file indicates that it is only CUDA compatibility code, what does that mean?

2. ROCM supports inline assembly, but I don't know how to find the corresponding strings? The following are just compilation checks that do not support it, and I don't know if the CUDA instructions can be directly migrated to AMD cards without changes?
Inline assembly string for ROCM
Inline ASM statements
Util.inl:23:105: error: invalid % escape in inline assembly string
23 | __device__ __inline__ U32 getLaneMaskLt(void) { U32 r; asm("mov.u32 %0, %lanemask_lt;" : "=r"(r)); return r; }
| ~~~~~~~~~~~~~~~^~~~~~~~~~~~
... (similar errors for other lines)

3. Is there a linking error with the function `float __frcp_rz(float __x) { return __ocml_div_rtz_f32(1.0f, __x); }`?
Error message:
```
lld: error: undefined hidden symbol: __ocml_div_rtz_f32
>>> referenced by __clang_hip_math.h:667 (/opt/rocm-6.1.3/lib/llvm/lib/clang/17/include/__clang_hip_math.h:667)
>>> /tmp/texture-gfx1100-c578c2.o:(TextureFwdKernelCubeNearest1(TextureKernelParams))
... (similar references for other instances)
```

Compilation and linking options:

```python
compile_opts = [
'-DROCM_TORCH', '-DOCML_BASIC_ROUNDED_OPERATIONS'
'-mprintf-kind=buffered', '-g', '-O3', '-w'
'-locml',
'-lamdhip64'
]

link_opts = [
#'-Wl,--no-as-needed',
'-locml',
#'-lhip_hcc',
'-lamdhip64'
]

CUDAExtension(
name="nvdiffrast._C",
sources=source_paths,
extra_compile_args={"nvcc": compile_opts, "hipcc": compile_opts, "cxx": cxx_compiler_flags},
#extra_link_flags={"nvcc": link_opts, "hipcc": link_opts, "cxx": link_opts},
extra_link_flags=link_opts,
extra_link_args=link_opts,
)
```

Please note that the translation provided is a direct translation of the text as requested. However, for technical support or detailed explanations regarding the CUDA and HIP functions, it would be best to consult the official documentation or reach out to the respective communities or support channels.

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

Intel(R) Xeon(R) E-2176M  CPU @ 2.70GHz

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2024-07-29T14:37:46Z)

@yttbgf Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — jamesxu2 (2024-07-30T17:45:15Z)

Hello @yttbgf, thanks for the detailed questions. I'll try to answer them here but let me know if you want to clarify anything.

1.  ```__all_sync```,```__any_sync``` and ```ballot_sync``` will be implemented in ROCm 6.2 and are documented here: https://rocm.docs.amd.com/projects/HIP/en/latest/reference/cpp_language_extensions.html#warp-vote-and-ballot-functions. In ROCm 6.2, you'll need to ```#define HIP_ENABLE_WARP_SYNC_BUILTINS``` to enable these functions. Also, per the same documentation which goes over several caveats:
> Applications can test whether the target platform supports the __ballot or __activemask instructions using the hasWarpBallot device property in host code or the HIP_ARCH_HAS_WARP_BALLOT macro defined by the compiler for device code. 

- ```__ballot``` is used in the underlying implementation of each of these ```*_sync``` functions so make sure it's supported by your hardware using the above macro
- __syncwarp does not exist in ROCm and there isn't a drop-in equivalent. You may try moving to cooperative groups as in [this issue](https://github.com/ROCm/HIP/issues/2798) for finer warp-level synchronization, or use [__syncthreads](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/cpp_language_extensions.html#synchronization-functions) which enforces block-level and may incur a performance hit  
- I'm not sure where you see the phrase "CUDA compatibility code" in the header you're referencing, but that phrase usually refers to designing the HIP API so it can be a drop-in replacement for CUDA code through matching naming and function signatures. There are often key differences between CUDA and HIP code though, so please carefully consult the API reference to learn about the details
- If you compile using hipcc you will need to include the hip/hip_runtime.h header, but otherwise everything is linked by hipcc so something like ``` hipcc main.cpp -o main``` will work. The actual header file on github is called [amd_warp_sync_functions](https://github.com/ROCm/clr/blob/cda4b7db1cf27e6214e34b81e4867aea021226be/hipamd/include/hip/amd_detail/amd_warp_sync_functions.h#L125), and will be installed alongside other rocm includes, in ```/<path-to-rocm>/include/hip/amd_detail/``` in ROCm 6.2+ (This header does not exist in ROCm 6.1.2)
2. ROCm does indeed support inline assembly, but translating from CUDA assembly ("PTX") is not trivial. For instance, in the error you quote, you're referencing ```%lanemask_lt``` which is a special register in the CUDA case but undefined in ROCm. You can find the CUDA definition for this in their [CUDA PTX ISA guide](https://docs.nvidia.com/cuda/archive/12.2.1/pdf/ptx_isa_8.2.pdf#page=524). 
- To look for equivalent symbols, AMD maintains its own ISA guides which you can conveniently find in the [LLVM AMDGPU docs](https://llvm.org/docs/AMDGPUUsage.html#additional-documentation) for many architectures. The docs for your specific gfx architecture are found under the [RDNA3 ISA documentation](https://www.amd.com/content/dam/amd/en/documents/radeon-tech-docs/instruction-set-architectures/rdna3-shader-instruction-set-architecture-feb-2023_0.pdf). 
- In your specific case, you can access the lanemask value through the [__lanemask_lt() function](https://github.com/ROCm/clr/blob/cda4b7db1cf27e6214e34b81e4867aea021226be/hipamd/include/hip/amd_detail/amd_device_functions.h#L701) 
3. ``` __frcp_rz(float __x)``` is not supported. You can find a list of math functions and our support for them here: https://rocm.docs.amd.com/projects/HIP/en/docs-5.2.3/reference/math_api.html#frcp-rz

---

### 评论 #3 — jamesxu2 (2024-08-09T18:28:11Z)

Hi @yttbgf , just an update to this - ROCm 6.2 has been released so you will be able to use those *_sync functions once you update. Please close this ticket if I've answered your questions.

---

### 评论 #4 — yttbgf (2024-08-15T06:41:45Z)

> Hi @yttbgf , just an update to this - ROCm 6.2 has been released so you will be able to use those *_sync functions once you update. Please close this ticket if I've answered your questions.

this problem has been solved,thks

---
