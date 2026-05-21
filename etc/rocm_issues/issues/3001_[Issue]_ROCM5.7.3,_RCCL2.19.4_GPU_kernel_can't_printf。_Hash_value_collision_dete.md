# [Issue]: ROCM5.7.3, RCCL2.19.4 GPU kernel can't printf。 Hash value collision detected

> **Issue #3001**
> **状态**: closed
> **创建时间**: 2024-04-09T05:07:47Z
> **更新时间**: 2024-10-01T20:02:30Z
> **关闭时间**: 2024-10-01T20:02:30Z
> **作者**: yangyangv8
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 5.7.0
> **URL**: https://github.com/ROCm/ROCm/issues/3001

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 5.7.0** (颜色: #ededed)

## 描述

### Problem Description
In the rccl file prims_simple.h，I have added a section of printf in this kernel function， such as :

> __device__ __forceinline__ void genericOp(
>       intptr_t srcIx, intptr_t dstIx, int nelem, bool postOp
>     ) {
>     constexpr int DirectRecv = /*1 &&*/ Direct && DirectRecv1;
>     constexpr int DirectSend = /*1 &&*/ Direct && DirectSend1;
>     constexpr int Src = SrcBuf != -1;
>     constexpr int Dst = DstBuf != -1;
>     nelem = nelem < 0 ? 0 : nelem;
>     int sliceSize = stepSize*StepPerSlice;
>     sliceSize = max(divUp(nelem, 16*SlicePerChunk)*16, sliceSize/32);
>     int slice = 0;
>     int offset = 0;
>     if(tid == 0) {
>         printf("in genericOp \n");
>     }
> 


**when i run rccl test,  Use this command ./build/sendrecv_perf -b 8 -e 128M -f 2 -t 1 -g 2，will report this error：** 


> enquence.cc Current function: ncclLaunchKernel line 1090
> :1:rocvirtual.cpp           :2945: 74877529363 us: [pid:44406 tid:0x7f26f4922c00] Pcie atomics not enabled, hostcall not supported
> :1:rocvirtual.cpp           :3280: 74877529375 us: [pid:44406 tid:0x7f26f4922c00] AQL dispatch failed!
> yz-adm3: Test NCCL failure /home/yang.yang/yy/work/test-rccl/build/src/hipify/common.cu.cpp:451 'unhandled cuda error (run with NCCL_DEBUG=INFO for details) / '


After seeing the explanation here  https://rocm.docs.amd.com/en/latest/about/CHANGELOG.html#non-hostcall-hip-printf, I have added the following settings in the RCCL CMakelists.txt file : 

target_compile_options(rccl PRIVATE -mprintf-kind=buffered)

makefiles/common.mk: 
CXXFLAGS   := -DCUDA_MAJOR=$(CUDA_MAJOR) -DCUDA_MINOR=$(CUDA_MINOR) -fPIC -fvisibility=hidden \
              -Wall -mprintf-kind=buffered -g -Wno-unused-function -Wno-sign-compare -std=c++11 -Wvla \
              -I $(CUDA_INC) \
              $(CXXFLAGS)

**After compiling RCCL, reported this error :**

> enquence.cc Current function: ncclLaunchKernel line 1090
> :1:devhcprintf.cpp          :265 : 81559524344 us: [pid:65800 tid:0x7f0d2c53d440] Hash value collision detected, printf buffer ill formed
> :1:rocvirtual.cpp           :3188: 81559524353 us: [pid:65800 tid:0x7f0d2c53d440]
> Could not print data from the printf buffer!
> :1:rocvirtual.cpp           :3280: 81559524355 us: [pid:65800 tid:0x7f0d2c53d440] AQL dispatch failed!
> :1:devhcprintf.cpp          :265 : 81559524402 us: [pid:65799 tid:0x7ff8fd860440] Hash value collision detected, printf buffer ill formed
> :1:rocvirtual.cpp           :3188: 81559524410 us: [pid:65799 tid:0x7ff8fd860440]
> Could not print data from the printf buffer!
> :1:rocvirtual.cpp           :3280: 81559524416 us: [pid:65799 tid:0x7ff8fd860440] AQL dispatch failed!
> [rank0]: RuntimeError: NCCL Error 1: unhandled cuda error (run with NCCL_DEBUG=INFO for details)
> [rank1]: RuntimeError: NCCL Error 1: unhandled cuda error (run with NCCL_DEBUG=INFO for details)

I have set these environment variables
export HIP_KERNEL_PRINTF=1
export HIP_ENABLE_PRINTF=1
export HCC_ENABLE_PRINTF=1
export AMD_LOG_LEVEL=1

Using a Linux server with two GPU cards,  **without printf, the program executes normally**, How should I solve this problem?




### Operating System

22.04.1 LTS (Jammy Jellyfish)

### CPU

12th Gen Intel(R) Core(TM) i7-12700

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 5.7.0

### ROCm Component

HIP, HIPCC, rccl

---

## 评论 (10 条)

### 评论 #1 — nartmada (2024-04-10T03:06:05Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — yangyangv8 (2024-04-10T05:06:48Z)

@nartmada Thanks, I hope to receive a response as soon as possible

---

### 评论 #3 — yangyangv8 (2024-04-15T01:39:08Z)

@nartmada hello Is there any outcome to this issue now?

---

### 评论 #4 — akondrat-amd (2024-04-19T03:22:19Z)

@yangyangv8 We are working on it.

---

### 评论 #5 — yangyangv8 (2024-04-26T03:01:26Z)

RCCL version 2.19.4

---

### 评论 #6 — yangyangv8 (2024-05-07T09:35:53Z)

@alexeykondrat @nartmada  Hello, is there any outcome to this issue now?

---

### 评论 #7 — nartmada (2024-06-14T04:25:59Z)

@yangyangv8, sorry for the delay in response.  I have reassigned the internal ticket to another developer for investigation.  We will have an update soon.  Thanks.

---

### 评论 #8 — jamesxu2 (2024-06-17T19:47:41Z)

Hi @yangyangv8 , thanks for your patience.

I was able to reproduce the PCIe atomics error on ROCm 5.7.3 and you can observe that the workaround of applying the target_compile_options(rccl PRIVATE **-mprintf-kind=buffered**) flag does work. You can try this simple test program to verify:

```cpp
#include <iostream>
#include <hip/hip_runtime.h>

__device__ void test(int tid){
    printf("Hello world from thread %d \n",tid);
}

__global__ void gpuHelloWorld()
{
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    test(tid);
}

void cpuHelloWorld()
{
    std::cout << "Hello world from the CPU!" << std::endl;
}

int main()
{
    cpuHelloWorld();
    gpuHelloWorld <<<1,16>>>();
    return 0;
}
```
And observe that only "Hello world from the CPU!" is printed but none of the other prints appear as when you compile using `hipcc helloworld.cpp -o helloworld`

However, if you compile this small program using `hipcc test.cpp -o test  -mprintf-kind=buffered` you should see all the expected print outputs from both the __global__ and __device__ functions. Please let me know if this is not the case for your system.

---

I am assuming you have installed ROCm, with some default version of RCCL, then built the RCCL library from source to replace whatever base files were there. 

Following the instructions on https://github.com/ROCm/rccl to install:
1. Cleanup the existing install rccl files by running the following as superuser
```bash
rm -rf /opt/rocm/lib/librccl.so.1.0
rm -rf /opt/rocm/lib/librccl.so.1
rm -rf /opt/rocm/include/rccl/
rm -rf /opt/rocm/share/rccl/
rm -rf /opt/rocm/lib/cmake/rccl/
```
3. Modify the CMakeLists.txt to include target_compile_options(rccl PRIVATE -mprintf-kind=buffered)
4. Perform the modifications in any source headers in the rccl repo to add your print functions
5. Run, in the rccl base directory ```./install.sh -fi``` to rebuild rccl and install it in the default location /opt/rocm/... (the same files deleted in (1))
6. Rerun the test from the rccl-tests directory

Let me know if this resolves your issue.

---

### 评论 #9 — jamesxu2 (2024-07-08T15:04:55Z)

Hi @yangyangv8 , do you have any updates? 

---

### 评论 #10 — jamesxu2 (2024-10-01T20:02:30Z)

Hi @yangyangv8 , I'm going to close this ticket due to lack of activity - you are welcome to reopen it if you do come back it.

---
