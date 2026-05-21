# Cannot install AlphaPose using ROCm

> **Issue #2168**
> **状态**: closed
> **创建时间**: 2023-05-24T14:22:44Z
> **更新时间**: 2024-03-22T16:30:05Z
> **关闭时间**: 2024-03-22T16:30:05Z
> **作者**: kjm0202
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2168

## 描述

I'm trying to install AlphaPose on Ubuntu 22.04 following this method:
https://github.com/MVIG-SJTU/AlphaPose/blob/master/docs/INSTALL.md (using pip)

But when I execute this code
`python3 setup.py build develop --user`

Then these error happens. Seems like related to clang namespace but no idea how to solve it.
`/opt/rocm-5.5.0/hip/include/hip/amd_detail/../../../../include/hip/amd_detail/amd_hip_atomic.h:205:1: note: 'atomicAddNoRet' has been explicitly marked deprecated here
DEPRECATED("use atomicAdd instead")
^
/opt/rocm-5.5.0/hip/include/hip/../../../include/hip/hip_runtime_api.h:494:41: note: expanded from macro 'DEPRECATED'
#define DEPRECATED(msg) __attribute__ ((deprecated(msg)))
                                        ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:91:26: error: call to 'max' is ambiguous
    scalar_t roi_width = max(roi_end_w - roi_start_w, 0.1); //avoid 0
                         ^~~
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:301:29: note: in instantiation of function template specialization 'DeformablePSROIPoolForwardKernel<c10::Half>' requested here
       hipLaunchKernelGGL(( DeformablePSROIPoolForwardKernel), dim3(GET_BLOCKS(count)), dim3(CUDA_NUM_THREADS), 0, 0, 
                            ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:92:27: error: call to 'max' is ambiguous
    scalar_t roi_height = max(roi_end_h - roi_start_h, 0.1);
                          ^~~
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:131:17: error: call to 'max' is ambiguous
        w = min(max(w, 0.), width - 1.);
                ^~~
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:132:17: error: call to 'max' is ambiguous
        h = min(max(h, 0.), height - 1.);
                ^~~
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:184:26: error: call to 'max' is ambiguous
    scalar_t roi_width = max(roi_end_w - roi_start_w, 0.1); //avoid 0
                         ^~~
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:354:29: note: in instantiation of function template specialization 'DeformablePSROIPoolBackwardAccKernel<c10::Half>' requested here
       hipLaunchKernelGGL(( DeformablePSROIPoolBackwardAccKernel), dim3(GET_BLOCKS(count)), dim3(CUDA_NUM_THREADS), 0, 0, 
                            ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:185:27: error: call to 'max' is ambiguous
    scalar_t roi_height = max(roi_end_h - roi_start_h, 0.1);
                          ^~~
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:228:17: error: call to 'max' is ambiguous
        w = min(max(w, 0.), width - 1.);
                ^~~
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
alphapose/models/layers/dcn/src/deform_pool_hip_kernel.hip:229:17: error: call to 'max' is ambiguous
        h = min(max(h, 0.), height - 1.);
                ^~~
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1345:7: note: candidate function
float max(float __x, float __y) { return fmaxf(__x, __y); }
      ^
/opt/rocm-5.5.0/llvm/lib/clang/16.0.0/include/__clang_hip_math.h:1348:8: note: candidate function
double max(double __x, double __y) { return fmax(__x, __y); }
       ^
32 warnings and 8 errors generated when compiling for gfx1030.
error: command '/opt/rocm-5.5.0/bin/hipcc' failed with exit code 1`

![스크린샷 2023-05-24 23-24-53](https://github.com/RadeonOpenCompute/ROCm/assets/61281883/955a4b4a-6a39-43f2-93d1-d921f894e359)


---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-03-16T02:56:27Z)

Hi @kjm0202, apologies for the lack of response.  Can you please check latest ROCm 6.0.2 if your issue still exists?

---

### 评论 #2 — nartmada (2024-03-22T16:30:05Z)

Closing the ticket.  Please re-open if you still observe this issue in latest ROCm 6.0.2.  Thanks.

---
