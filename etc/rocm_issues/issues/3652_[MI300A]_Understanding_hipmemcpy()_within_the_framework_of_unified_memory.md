# [MI300A] Understanding hipmemcpy() within the framework of unified memory 

> **Issue #3652**
> **状态**: closed
> **创建时间**: 2024-08-28T07:49:47Z
> **更新时间**: 2024-09-23T00:09:44Z
> **关闭时间**: 2024-09-23T00:09:44Z
> **作者**: vitduck
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3652

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Hi, 

According to MI300A official optimization guide: 
https://hipcub.readthedocs.io/en/rocm-6.2.0/how-to/system-optimization/mi300a.html 

The cpu-gpu bandwidth measured with `rocm_bandwidth` is ~ 58 GB/s for a 4-way MI300A node. 

![image](https://github.com/user-attachments/assets/a27c53ec-7db6-4762-9d49-8c6c5a8eedfb)

The above result is somewhat counter-intuitive.
If the data is located in APU's HBM3 and then loaded into the infinity cache, there should be no memory copy required. 
- How is memory copy defined in this case, i.e. the physical path through which data travels between CPU and GPU ? 
- Is it correct to assume that 0,1,2,3 correspond to the Zen4 CPUs ? 
    - Why is bandwidth between 0-1 pair, which corresponds to zen4-to-zen4 bandwidth, undefined ? 
- What is origin of lack of locality between MI300A ?  
    - 0-4 pair: CPU-GPU within same MI300A 
    - 0-5 pair: CPU-GPU across MI300A   
    - Yet, the bandwidth is uniformly ~ 58 GB/s  
- Conversely, what is the origin of discrepancy between HBMs across MI300A ? 
   - 0-5 pair: CPU-GPU across socket 
   - 4-5 pair : GPU-GPU across socket 
   - From an unified memory point of view, both are just a HBM-to-HBM bandwidth.  
     Yet, the  former is 58 GB/s, and the latter is 116 GB/s 

I appreciate if AMD engineer can help clarify these points. 
These number is underwhelmed in comparison to the theoretical 5.3 TB/s bandwidth of HBM3. 

Thanks. 

---

## 评论 (9 条)

### 评论 #1 — ppanchad-amd (2024-09-08T23:46:43Z)

Hi @vitduck, an internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2024-09-11T13:56:06Z)

Hi @vitduck, I reached out to our internal team and have a couple of insights that should help clarify this for you. The measurements you are seeing in this screenshot from the docs are measuring inter-device transfers, which means that memory access is occurring across the Infinity Fabric between different APUs. This connection is the bottleneck for such transfers, not the HBM, so the transfer speeds are not expected to approach the theoretical HBM bandwidth. The differences you are seeing between the bandwidths of various connection types is most likely tied to this as well

If you want to measure the bandwidth of copies in local HBM, i.e. without traversing the Infinity Fabric, the team suggests using BabelStream or a similar test instead. This should show much higher bandwidths which are more in line with theoretical HBM bandwidth.

> If the data is located in APU's HBM3 and then loaded into the infinity cache, there should be no memory copy required.

This is only true if the code is explicitly refactored to remove the memory copy, as the compiler does not detect and optimize for this.

---

### 评论 #3 — vitduck (2024-09-12T06:35:05Z)

@ppanchad-amd 
Thanks for passing the question forward. 

@schung-amd 
Thanks for your explanation. I have understood that this results reflecting the the performance of Infinity Fabrics (IF).
In comparison to MI250x, there is approximately 2x increase, which is good. 

However, the crux of my question is about the nature of `hipMemcpy()` in the context of MI300A. 
This slide is an excerpt from "Programming Model for MI200 and MI300 series" tutorial, by Gina Sitaraman (AMD). 

![image](https://github.com/user-attachments/assets/efcd2a8d-55c7-4e33-bc40-b5470594903d)

I know that `hipMemcpy()` is not required but remains valid when used in legacy code ported from CUDA.
1. Under normal circumstance, `malloc()` allocates N bytes in DDR5, `hipmalloc()` allocates N bytes in HBM3. 
    In case of MI300A, both physically share the same HBM domain. 
    Will the same amount of memory be allocated twice, i.e. 2N in total, effectively cutting the usable HBM memory in half ? 
    
2. Likewise, hipMemcpy() transfers data through PCIe between DDR5 and HBM. 
    In case of MI300A, when ROCm runtime encounters `hipMemcpy()`, what will happen ? 
    - `hipMemcpy()` will be silently ignored, or 
    - data will travels xGMI interconnect, which would be very strange to say the least. 
     
If it is not too bothersome, could you kindly ask your colleague for further clarification ?

For context, we are testing MI300A through collaboration with AAC. 
Robey kindly gave us his speculative answer in which `hipMalloc()` and `hipMemcpy()` would be no-ops. 
I also think this is the most natural way. 
But definite confirmation from AMD would be very much appreciated. 

Regards.  

---

### 评论 #4 — schung-amd (2024-09-12T14:10:33Z)

Followed up with the internal team, and yes, although it may seem illogical, the redundant copy in unified memory will not be optimized out because the compiler does not know that the copy is redundant. Invoking `hipMemcpy()` when the source and destination are both in unified memory will result in additional memory allocation, and the data will be copied. If the data is not local to the APU, then it will transfer via the coherent infinity fabric interconnect. This is not unique to this architecture; `A = B` on a CPU will also perform a redundant memory copy in DDR. If you want to optimize out these redundant memory copies, you'll have to manually remove them from the code.

I assume this is the presentation you've seen since the slide you've referenced is in it, but I'll link it anyway; the team suggests referring to https://nowlab.cse.ohio-state.edu/static/media/workshops/presentations/espm2_23/PublicSC23ESPM2ProgrammingAMDInstinctMI300A.pdf, which tries to detail these nuances. 

---

### 评论 #5 — vitduck (2024-09-13T01:49:55Z)

Thanks for clarification.  

I guess it does make sense for `hipMemcpy()` to behave this way to prevent unintended consequences. 

For users starting from scratch or porting CPU codes to HIP, the ability to use `malloc()` is highly appreciated.  
But for those who migrating large CUDA code to HIP, they might suddenly run into OOM due to redundant copies. 

Even within Instinct family, this presents an issue to make code run seamlessly on -A and new or older -X variants.  
The latter relies on page migration for `malloc()`, which I don't think is preferable in most cases (even with NVIDIA). 
And if user forgets to enable XNACK, it will further degrades to PCIe speed ! 

If I understand correctly, `hipcc` can automatically figure out the target ISA. 
Then it would be helpful if `hipcc` emits some warnings against the usage of `hipMemcpy()` with `gfx942` 

---

### 评论 #6 — schung-amd (2024-09-13T19:34:29Z)

I'll check with the internal team to see if they would want to add such a feature, but `hipcc` is just a thin wrapper around clang, so adding warnings here might not be appropriate. In my opinion this is more suited for documentation about optimizing legacy code on MI300, which probably doesn't exist yet. Have you run into practical issues with redundant memory copies in legacy code?

---

### 评论 #7 — vitduck (2024-09-18T13:43:59Z)

Hi again. 
Sorry for belated follow-up due to a technical issue on our end. 

Right now we are only conducting tests internally and officially supported benchmarks and scientific codes work seamlessly.
The legacy code would potentially come from our users' in-house written in CUDA.

For example, I try inducing an OOM by allocating large vectors on both host and device (MI300A) 
```
#include <iostream>
#include <hip/hip_runtime.h>

int main() {
    //  array of 2^32 elements
    size_t N = (size_t)1 << 32;

    // host
    double* A; 
    A = (double*)malloc(N*sizeof(double));  
    
    // device  
    double* d_A; 
    hipMalloc(&d_A, N*sizeof(double));

    // initialize
    for (auto i = 0; i < N; ++i) {
        A[i] = i; 
    }
    
    // host -> device  
    hipMemcpy(d_A, A, N*sizeof(double), hipMemcpyHostToDevice); 

    // free
    free(A); 
    hipFree(d_A);     

    return 0;
}
```
This corresponds to 32GB + 32GB allocation, which is half of the 128GB-VRAM of MI300A. 
```
$ hipcc test.cpp 
$ ./a.out 
Trace/breakpoint trap (core dumped)
```
Since we are under docker environment, there could be some restrictions. 
Once we have access to bare-metal node, I will try again. 

If optimization to remove redundant copy is absolutely required, as I have understood so far, we will make sure that users are aware of it.

---

### 评论 #8 — schung-amd (2024-09-18T14:03:13Z)

Thanks for the example! You don't need to verify this on baremetal, I was just personally curious if your workloads were performing enough redundant copies to run into this issue or if this was just futureproofing. Your understanding is correct; redundant memory copies will not be removed by the compiler, so if they are causing issues then they will have to be manually removed, and you can advise your users as such.

---

### 评论 #9 — vitduck (2024-09-20T14:10:08Z)

@ppanchad-amd @schung-amd 

Again thanks very much for your help. 
Your explanation has greatly helped us understand the issue.  

Unless you have further comments, which are always welcome, I will close this issue after a short while. 

---
