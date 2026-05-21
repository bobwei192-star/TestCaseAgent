# [Issue]: At the -O2 optimization level, the division computation result for uint64_t type is incorrect

> **Issue #5142**
> **状态**: closed
> **创建时间**: 2025-08-01T09:23:55Z
> **更新时间**: 2025-09-26T07:01:06Z
> **关闭时间**: 2025-09-26T07:01:06Z
> **作者**: 0oyyo0
> **标签**: Under Investigation, ROCm 6.3.1
> **URL**: https://github.com/ROCm/ROCm/issues/5142

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.1** (颜色: #ededed)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

①I tested the following code on gfx906 and found that the results were not as expected. The core of this code is to check whether the input string can be safely converted to a uint64_t integer.
②When compiled using the following command, the calculation result is incorrect. The cause of the error is located in the incorrect calculation result of the line "a2 / uint64_t{10}".
`hipcc demo.cpp -o demo -std=c++17 -O2`

<img width="1151" height="305" alt="Image" src="https://github.com/user-attachments/assets/dc1689e2-9826-455d-adf1-dc851cb5d6b4" />


③When DivExpand is disabled by adding the "disable-idiv-expansion" option, the calculation result is correct.
`hipcc demo.cpp -o demo -std=c++17 -O2 -mllvm -amdgpu-codegenprepare-disable-idiv-expansion=true`

<img width="1348" height="561" alt="Image" src="https://github.com/user-attachments/assets/8d64022c-1e13-44ca-a13f-761fadc79d31" />


④Current analysis: In the `amdgpu-codegenprepare` pass, `udiv` is converted to `fmul`.
⑤Please advise: What is the specific role of the expandDivRem32 function in the amdgpu-codegenprepare pass? Why does using it lead to incorrect computation results?


```
#include <hip/hip_runtime.h>
#include <iostream>
#include <limits>
#include <string>
#include <type_traits>

__device__ bool check_string(const char* d_str, size_t len) {
    auto iter = d_str;
    auto const iter_end = d_str + len;

    auto const bound_val = std::numeric_limits<uint64_t>::max();
    uint64_t value = 0;

    while (iter != iter_end) {
      auto const chr = *iter++;
      if (chr < '0' || chr > '9') { return false; }

      auto const digit = static_cast<uint64_t>(chr - '0');

      // auto const bound_check = (bound_val - sign * digit) / uint64_t{10} * sign;
      uint64_t const a1 = digit;
      uint64_t const a2 = bound_val - a1;
      uint64_t const bound_check = a2 / uint64_t{10};
      
      printf("bound_val: %llu, digit: %llu, value: %llu, bound_check: %llu\n", bound_val, digit, value, bound_check);

      if (value > bound_check) {
        return false;
      }

      value = value * uint64_t{10} + digit;
    }

    return true;
  
}

__global__ void check_string_kernel(const char* str, size_t len, bool* result) {
    if (threadIdx.x == 0 && blockIdx.x == 0) {
        result[0] = check_string(str, len);
    }
}

int main() {
    std::string input = "9223372036854775806";
    
    char* d_str;
    bool* d_result;
    hipMalloc(&d_str, input.size());
    hipMalloc(&d_result, sizeof(bool));
    
    hipMemcpy(d_str, input.c_str(), input.size(), hipMemcpyHostToDevice);
    
    check_string_kernel<<<1, 256>>>(d_str, input.size(), d_result);
    hipDeviceSynchronize();
    
    bool h_result;
    hipMemcpy(&h_result, d_result, sizeof(bool), hipMemcpyDeviceToHost);
    
    std::cout << (h_result ? "check passed" : "Got 'false' when checking if \"9223372036854775806\" is a uint64_t. Expect 'true'.") << std::endl;
    
    hipFree(d_str);
    hipFree(d_result);
    
    return 0;
}
```

### Operating System

rhel centos fedora 8.6

### CPU

x86_64

### GPU

gfx906

### ROCm Version

6.3.1

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

### 评论 #1 — ppanchad-amd (2025-08-05T18:30:08Z)

Hi @0oyyo0. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — lucbruni-amd (2025-08-11T17:41:42Z)

Hi @0oyyo0,

I am unable to see your attached images (on Chrome/Edge at least). Do you mind reposting them, or pasting the text of the test results here? These would help in the debugging process. Thanks!

---

### 评论 #3 — lucbruni-amd (2025-09-15T20:53:22Z)

Hi @0oyyo0,

Are you still encountering the issue? If so, refer to my previous comment so I can ensure we are on the same page.

Thanks!

---

### 评论 #4 — 0oyyo0 (2025-09-26T07:01:06Z)

> Hi [@0oyyo0](https://github.com/0oyyo0),
> 
> Are you still encountering the issue? If so, refer to my previous comment so I can ensure we are on the same page.
> 
> Thanks!

Subsequent versions of rocm have solved this problem.

Prevent shrinking udiv/urem if either operand exceeds signed max(Especially for unsigned numbers), and Use correct number of bits needed for div/rem shrinking.  Community commits:①https://github.com/ROCm/llvm-project/commit/e5638c5a00682243b1ee012d7dd8292aa221dff8#diff-bd14c07380de930aa1b564d8403ff604929e667e23aa803e0ae09071b93e7037 ②https://github.com/ROCm/llvm-project/commit/edf2376bca3ac3409b61bded1d231a0112e3eeea#diff-f41381955a38b43c81e4f973016801d8fa5cfb1800f1e6427dd6d2f062e5e932


---
