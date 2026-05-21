# [Issue]: Why hipmemcpy always copied wrong data?

> **Issue #4035**
> **状态**: closed
> **创建时间**: 2024-11-18T17:41:39Z
> **更新时间**: 2024-12-22T16:09:04Z
> **关闭时间**: 2024-12-17T17:07:13Z
> **作者**: scarsty
> **标签**: Under Investigation, ROCm 6.1.0, 7900xtx
> **URL**: https://github.com/ROCm/ROCm/issues/4035

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.1.0** (颜色: #ededed)
- **7900xtx** (颜色: #ededed)

## 描述

### Problem Description

I found hipmemcpy always copied wrong data, but if I insert a rocblas computing, the results seems become right. Is a synchronization process missing?

I have tried hipDeviceSynchronize but it is useless.

### Operating System

Windows

### CPU

R5

### GPU

7900xtx

### ROCm Version

ROCm 6.1.0

### ROCm Component

rocblas, miopen

### Steps to Reproduce

My program is very complicated. If someone need, I can supply the github repo and compilation method of it.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (11 条)

### 评论 #1 — ppanchad-amd (2024-11-18T18:01:22Z)

Hi @scarsty. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — darren-amd (2024-11-18T19:45:52Z)

Hi @scarsty,

Could you try running a basic example, such as the one [here](https://github.com/ROCm/rocm-examples/blob/14f07b9bde5cb4e9a679ef157a19fbc78702bb6b/HIP-Basic/shared_memory/main.hip#L111). Please let me know if this test passes, as I want to rule out if your HIP installation is broken. 

Also, to confirm, are you installing the HIP SDK as described in [these instructions](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/)?


---

### 评论 #3 — scarsty (2024-11-19T02:14:26Z)

I have tried some basic examples and passed.
This bug happened when continuous calculations are preforming. In my program (https://github.com/scarsty/cccc-lite/blob/a6c77fecaafc52762ce6451b0782cc5c635779b6/cccc/Net.cpp#L393), I compute MNIST in batches. Results of the first batch seem right, but for other batches, the results are the same to the first batch. If I insert some other "useless" computing (for example, rocblas_sdot) at the end of the loop, all results become right. 
And, when I want to copy the data from device to host, it is not right. If I insert a computing before the copying, that also becomes right. 
I make sure that this bug does not happen with rocm 5.5.

---

### 评论 #4 — darren-amd (2024-11-22T19:17:05Z)

Hi @scarsty,

Thanks for providing your code, its interesting that inserting a rocblas function after the code results in the correct copied data. Could you please provide me with a minimum reproduceable example so that I may try to replicate it on my end and investigate further? Thanks!

---

### 评论 #5 — scarsty (2024-11-25T05:13:46Z)

The reason might be that I use the APIs with dynamically loading (like this <https://github.com/scarsty/cccc-lite/blob/master/cccc/gpu_lib.cpp>). This not happens with classical linking method. But I still want to know the reason of it.

---

### 评论 #6 — scarsty (2024-11-25T06:47:35Z)

> Hi @scarsty,
> 
> Thanks for providing your code, its interesting that inserting a rocblas function after the code results in the correct copied data. Could you please provide me with a minimum reproduceable example so that I may try to replicate it on my end and investigate further? Thanks!

This is a minimum reproduceable example.


```c++
#define __HIP_DISABLE_CPP_FUNCTIONS__
#include <rocblas/rocblas.h>

#include <hip/hip_runtime_api.h>

#include <cstdlib>
#include <iostream>
#include <limits>
#include <numeric>
#include <vector>

#include "DynamicLibrary.h"

namespace ns
{

#define IMPORT(func, ...) \
    using func##_t = decltype(&func); \
    func##_t func = nullptr;

IMPORT(rocblas_create_handle)
IMPORT(rocblas_destroy_handle)
IMPORT(rocblas_sgemm)
IMPORT(rocblas_set_pointer_mode)
IMPORT(hipMalloc)
IMPORT(hipMemcpy)
IMPORT(hipFree)

#undef IMPORT

rocblas_handle handle{};

void gemm(const float* A, const float* B, float* C, const int m, const int n, const int k)
{
    const rocblas_float alpha = 1;
    const rocblas_float beta = 0;
    rocblas_sgemm(handle, rocblas_operation_none, rocblas_operation_none, m, n, k, &alpha, A, m, B, k, &beta, C, m);
}

void load_libs()
{
    std::vector<std::string> libs = {
        "rocblas.dll",
        "amdhip64",
    };
#define IMPORT(func, ...) \
    for (auto& lib : libs) \
    { \
        func = (func##_t)DynamicLibrary::getFunction(lib, #func); \
        if (func) { break; } \
    }

    IMPORT(rocblas_create_handle)
    IMPORT(rocblas_destroy_handle)
    IMPORT(rocblas_sgemm)
    IMPORT(rocblas_set_pointer_mode)
    IMPORT(hipMalloc)
    IMPORT(hipMemcpy)
    IMPORT(hipFree)
}

int run()
{
    load_libs();

    rocblas_create_handle(&handle);

    // Set sizes of matrices.
    const rocblas_int m = 100;
    const rocblas_int n = 100;
    const rocblas_int k = 100;

    auto size_a = m * k;
    auto size_b = k * n;
    auto size_c = m * n;

    // Allocate host data.
    std::vector<float> h_a(size_a * 3);
    for (int i = 0; i < size_a; i++)
    {
        h_a[i] = 1.0f;
        h_a[i + size_a] = 2.0f;
        h_a[i + size_a * 2] = 3.0f;
    }

    std::vector<float> h_b(size_b);
    for (int i = 0; i < k; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (i == j)
            {
                h_b[i * n + j] = 1.0f;
            }
            else
            {
                h_b[i * n + j] = 0.0f;
            }
        }
    }

    std::vector<float> h_c(size_c);

    float* d_a{};
    float* d_b{};
    float* d_c{};
    hipMalloc((void**)&d_a, size_a * 3 * sizeof(float));
    hipMalloc((void**)&d_b, size_b * sizeof(float));
    hipMalloc((void**)&d_c, size_c * sizeof(float));

    hipMemcpy(d_a, static_cast<void*>(h_a.data()), sizeof(float) * size_a * 3, hipMemcpyHostToDevice);
    hipMemcpy(d_b, static_cast<void*>(h_b.data()), sizeof(float) * size_b, hipMemcpyHostToDevice);
    rocblas_set_pointer_mode(handle, rocblas_pointer_mode_host);

    auto d_a1 = d_a;
    for (int i = 0; i < 3; i++)
    {
        gemm(d_a1, d_b, d_c, m, n, k);
        float sum = 0.0f;
        //rocblas_sdot(handle, size_c, d_c, 1, d_c, 1, &sum);    //discomment this line to make the results right
        d_a1 += size_a;
    }

    hipMemcpy(h_c.data(), d_c, sizeof(float) * size_c, hipMemcpyDeviceToHost);

    float sum = std::accumulate(h_c.begin(), h_c.end(), 0.0f);
    std::cout << "Sum: " << sum << std::endl;

    rocblas_destroy_handle(handle);

    hipFree(d_a);
    hipFree(d_b);
    hipFree(d_c);

    return 0;
}
};    //namespace ns

int main(const int argc, const char** argv)
{
    return ns::run();
}
```

---

### 评论 #7 — darren-amd (2024-11-25T15:41:09Z)

Hi @scarsty,

I don't have your `"DynamicLibrary.h"` file so I ran the code without dynamic loading which returned a sum of 30000 with or without the call to `rocblas_sdot`. Could you please provide me with this file so that I can try running it on my end? Thanks!

---

### 评论 #8 — scarsty (2024-11-25T15:43:28Z)

> Hi @scarsty,
> 
> I don't have your `"DynamicLibrary.h"` file so I ran the code without dynamic loading which returned a sum of 30000 with or without the call to `rocblas_sdot`. Could you please provide me with this file so that I can try running it on my end? Thanks!

It is here, thanks.
<https://github.com/scarsty/mlcc/blob/master/DynamicLibrary.h>

---

### 评论 #9 — darren-amd (2024-11-28T20:08:37Z)

Hi @scarsty,

I gave it a try with the linked `DynamicLibrary.h` file and wasn't able to reproduce any issue, as the resultant sum was still 30000. Could you please let me know how you are running the example, as well as your result from running with/without dynamic loading and the rocblas function? Could you also please try updating to the latest version of ROCm and giving that a try? Thanks!

---

### 评论 #10 — darren-amd (2024-12-17T17:07:13Z)

Hi @scarsty,

I'm going to close this ticket due to inactivity, but please feel free to create another one if the issue persists, thanks!

---

### 评论 #11 — scarsty (2024-12-22T16:08:46Z)

> Hi @scarsty,
> 
> I'm going to close this ticket due to inactivity, but please feel free to create another one if the issue persists, thanks!


The reason seems that amdhip64.dll is from rocm 5.5 but rocblas.dll is from rocm 6.1.


---
