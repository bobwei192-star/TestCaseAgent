# [Issue]: Wrong return result from cooperative_groups::grid_group::group_dim on 9070XT

> **Issue #5236**
> **状态**: closed
> **创建时间**: 2025-08-29T08:06:48Z
> **更新时间**: 2025-09-15T14:04:51Z
> **关闭时间**: 2025-09-15T14:04:51Z
> **作者**: zhang-hui-yulo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5236

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- harkgill-amd

## 描述

### Problem Description

cooperative_groups::grid_group::group_dim returns  blockDim not gridDim on 9070XT, this let the behavior of cooperative_groups::grid_group::group_dim same as cooperative_groups::thread_block::group_dim.

cooperative_groups::grid_group::group_dim shall return gridDim to align the behavior of described in ROCm document https://rocm.docs.amd.com/projects/HIP/en/latest/doxygen/html/group___cooperative_g.html#ga33c3fba456790c2addf3bfa4be211053

The dim of grid group shall be gridDim not blockDim or the functionality totally doesn't make sense.

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

Sample code:

```
#include <hip/hip_runtime.h>
#include <hip/hip_cooperative_groups.h>


__global__ void test() {
    auto grid = cooperative_groups::this_grid();
    auto thread_block = cooperative_groups::this_thread_block();
    
    if(grid.thread_rank() == 0 && blockIdx.x == 0 && blockIdx.y == 0) {
        printf("grid group_dim x: %i, y: %i, z: %i\n", grid.group_dim().x, grid.group_dim().y, grid.group_dim().z);
        printf("block group_dim x: %i, y: %i, z: %i\n", thread_block.group_dim().x, thread_block.group_dim().y, thread_block.group_dim().z);
    }
}

int main(int argc, char* argv[]) {
    test<<<dim3(32, 16, 1), dim3(32, 4, 1), 0, 0>>>();
    return 0;
} 
```

Compile command:
```
/opt/rocm/lib/llvm/bin/clang++ --offload-arch=gfx1201 -xhip main.hip -o main
```

Output:
```
grid group_dim x: 32, y: 4, z: 1
block group_dim x: 32, y: 4, z: 1
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-09-02T16:01:24Z)

Hi @zhang-hui-yulo, I was able to reproduce this behaviour on a MI system as well. Digging into the source code shows that both group_dim methods for `grid_group` and `thread_block` return the same block_dim() value - which as you mentioned doesn't seem to be correct.

[rocm-systems/projects/clr/hipamd/include/hip/amd_detail/amd_hip_cooperative_groups.h at develop · ROCm/rocm-systems](https://github.com/ROCm/rocm-systems/blob/develop/projects/clr/hipamd/include/hip/amd_detail/amd_hip_cooperative_groups.h#L210)
[rocm-systems/projects/clr/hipamd/include/hip/amd_detail/amd_hip_cooperative_groups.h at develop · ROCm/rocm-systems](https://github.com/ROCm/rocm-systems/blob/develop/projects/clr/hipamd/include/hip/amd_detail/amd_hip_cooperative_groups.h#L289)

I've drafted https://github.com/ROCm/rocm-systems/pull/823 which should resolve this issue.

---

### 评论 #2 — harkgill-amd (2025-09-15T14:04:51Z)

Changes have been merged - https://github.com/ROCm/rocm-systems/commit/d1b2b5ed44d37bd3765098ec7a6d018d879f7545. The changes will be apart of an upcoming ROCm release. In the meantime, you can pickup these changes by building clr from source with the steps from https://github.com/ROCm/clr/tree/amd-staging?tab=readme-ov-file#linux. 

Make sure to use the source code from https://github.com/ROCm/rocm-systems/tree/develop/projects/clr as https://github.com/ROCm/clr/ has been deprecated.

---
