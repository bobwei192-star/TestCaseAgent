# [Feature]:  request __shfl_xor_sync  in rocm

> **Issue #3917**
> **状态**: closed
> **创建时间**: 2024-10-18T02:21:09Z
> **更新时间**: 2025-05-04T14:11:24Z
> **关闭时间**: 2024-10-18T18:05:44Z
> **作者**: ZJLi2013
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3917

## 描述



hi, rocm expert, 
 during our recent project, we need a same function as cuda, __shfl_xor_sync().

however looks recent [rocm 6.2.2](https://rocm.docs.amd.com/projects/HIPIFY/en/latest/tables/CUDA_Device_API_supported_by_HIP.html) has not supported yet:

|   |     |    |    | 
|---|---|---|---|
__shfl_xor | 9.0 |      __shfl_xor | 1.6.0 | 
__shfl_xor_sync |   |   |   |  


is there other primitives as quick replacement ? 

Thanks
David 



### Operating System

_No response_

### GPU

mi300

### ROCm Component

6.2.2

---

## 评论 (4 条)

### 评论 #1 — ZJLi2013 (2024-10-18T02:27:26Z)

chatgpt gave a solution:

```c++
inline int custom_shfl_xor_sync(unsigned mask, int val, int laneMask) {
    // 使用 ROCm intrinsic 来模拟 __shfl_xor_sync 的行为
    // __builtin_amdgcn_permlane_xor 可以在 wavefront 中根据 XOR 掩码交换值
    int result = __builtin_amdgcn_permlane_xor(val, laneMask, 0);
    return result;
}
``` 

thanks for clarifying 

---

### 评论 #2 — harkgill-amd (2024-10-18T18:05:44Z)

Hi @ZJLi2013, `__shfl_xor_sync` is supported as of ROCm 6.2, you can find it's definition [here](https://github.com/ROCm/clr/blob/amd-staging/hipamd/include/hip/amd_detail/amd_warp_sync_functions.h#L271-L282).

For more information regarding it's usage, please see [Warp shuffle functions](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/cpp_language_extensions.html#warp-shuffle-functions). You can also find the example [hipShflSyncXorTests ](https://github.com/ROCm/hip-tests/blob/develop/catch/unit/warp/hipShflSyncXorTests.cc)in our hip-tests repo.

---

### 评论 #3 — harkgill-amd (2024-10-18T18:28:16Z)

Will work on getting the HIPIFY docs updated to remove any confusion. Thanks for pointing this out!

---

### 评论 #4 — ZJLi2013 (2024-10-21T05:58:21Z)

> Hi @ZJLi2013, `__shfl_xor_sync` is supported as of ROCm 6.2, you can find it's definition [here](https://github.com/ROCm/clr/blob/amd-staging/hipamd/include/hip/amd_detail/amd_warp_sync_functions.h#L271-L282).
> 
> For more information regarding it's usage, please see [Warp shuffle functions](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/cpp_language_extensions.html#warp-shuffle-functions). You can also find the example [hipShflSyncXorTests ](https://github.com/ROCm/hip-tests/blob/develop/catch/unit/warp/hipShflSyncXorTests.cc)in our hip-tests repo.

hi, @harkgill-amd , thanks. looks the following header files are enough

```c++
#define HIP_ENABLE_WARP_SYNC_BUILTINS

#include <hip/hip_runtime.h>
#include <hip/hip_runtime_api.h>
```

now it works !

---
