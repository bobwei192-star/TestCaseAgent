# printf on device fails to print some elements after string justification

> **Issue #5425**
> **状态**: closed
> **创建时间**: 2025-09-24T16:47:58Z
> **更新时间**: 2026-01-14T18:09:02Z
> **关闭时间**: 2026-01-14T18:05:28Z
> **作者**: misos1
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5425

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- lucbruni-amd

## 描述

a.cpp:
``` hip
#include <hip/hip_runtime.h>

__global__ void kernel()
{
	printf("device\n");
	printf("  %10s %i\n", "123", 1);
	printf("  %10s %i\n", "12345678", 1);
}

int main()
{
	printf("host\n");
	printf("  %10s %i\n", "123", 1);
	printf("  %10s %i\n", "12345678", 1);
	hipLaunchKernelGGL(kernel, 1, 1, 0, 0);
	hipDeviceSynchronize();
}
```

```
hipcc a.cpp
```

output:
```
host
         123 1
    12345678 1
device
         123     12345678 1
```

rocm 6.4.3

---

## 评论 (5 条)

### 评论 #1 — b-sumner (2025-09-24T17:09:40Z)

@misos1 your code is exiting immediately after launching the kernel.  Try adding a hipDeviceSynchronize() call before exiting.

---

### 评论 #2 — misos1 (2025-09-24T17:13:54Z)

@b-sumner I updated the sample code (same result).


---

### 评论 #3 — b-sumner (2025-09-24T17:40:14Z)

@misos1 thanks.  I see the same.   We should open an internal ticket for this.

---

### 评论 #4 — ppanchad-amd (2025-09-24T18:54:25Z)

Hi @misos1. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #5 — lucbruni-amd (2026-01-14T18:09:02Z)

I've merged the linked pull request which resolves this issue. If you encounter any unexpected behaviour with device `printf`, feel free to reopen this issue or open a new one. Thanks for helping us find issues!

---
