# [Issue]: Unless HIP_VISIBLE_DEVICES specified, initializing HIP runtime takes 10 seconds (strace attached).

> **Issue #4152**
> **状态**: closed
> **创建时间**: 2024-12-12T20:35:45Z
> **更新时间**: 2024-12-16T21:52:13Z
> **关闭时间**: 2024-12-16T21:52:13Z
> **作者**: bjacob
> **标签**: Under Investigation, ROCm 6.2.0, 8x  MI300X in CPX mode (total 64 logical devices).
> **URL**: https://github.com/ROCm/ROCm/issues/4152

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.0** (颜色: #ededed)
- **8x  MI300X in CPX mode (total 64 logical devices).** (颜色: #ededed)

## 描述

### Problem Description

This simple test program doing just a 1-byte `hipMalloc` takes 10 seconds to run:
```c++
#include <hip/hip_runtime.h>

int main() {
  char* p;
  (void)hipMalloc(&p, 1);
}
```

But if I specify `HIP_VISIBLE_DEVICES=63` to pin to one specific GPU, then it runs in under 1 second.

I `strace`'d it and a difference that stood out was the `AMDKFD_IOC_MAP_MEMORY_TO_GPU` `ioctl`'s. These often have latency over 60ms.

By default (when the program takes 10 seconds), there are 260 such `ioctl`'s.
With `HIP_VISIBLE_DEVICES=63`, there are 135 such `ioctl's`.

Why is the number of `AMDKFD_IOC_MAP_MEMORY_TO_GPU` `ioctl`'s 2x higher when not pinned to a GPU? I thought that once a device has been picked, `HIP_VISIBLE_DEVICES` shouldn't make a difference anymore.

### Operating System

Ubuntu 22.04

### CPU

2x AMD EPYC 9454 48-Core Processor

### GPU

8x  MI300X in CPX mode (total 64 logical devices).

### ROCm Version

ROCm 6.2.0

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — bjacob (2024-12-12T20:44:29Z)

[strace.zip](https://github.com/user-attachments/files/18117284/strace.zip)


---

### 评论 #2 — bjacob (2024-12-12T20:48:28Z)

Another thing that stands out is that when not defining `HIP_VISIBLE_DEVICES`, strace attached above 👆 does 130 times this:

```
14:09:38.165070 openat(AT_FDCWD, "/dev/random", O_WRONLY) = 5
14:09:38.165108 write(5, "\230", 1)     = 1
14:09:38.165137 close(5)                = 0
```

(With the same value `\230` each time).

When `HIP_VISIBLE_DEVICES` is defined, it does that only 4 times instead of 130.

Browsing code, the writes could be made by `IsAccessibleMemoryAddress` (https://github.com/ROCm/ROCR-Runtime/blob/e93efba9cc892e8ef878ef25ddea16c7773af51a/runtime/hsa-runtime/libamdhsacode/amd_hsa_code_util.cpp#L114) just to test if an address is accessible, so the byte `\230` might be just whatever was at that address?  Mysterious though what role is being played by writing to `/dev/random`. Is there a special case in the `write` syscall where reading from an unmapped address into that file doesn't segfault? EDIT - browsed some Linux code, IIUC the `/dev/random` driver's implementation of writes tolerates out-of-bounds reads and then returns 0 bytes written, so this code takes advantage of that - fascinating!  Still better to do that only 4 times vs 130.



---

### 评论 #3 — ppanchad-amd (2024-12-12T21:23:11Z)

Hi @bjacob. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #4 — bjacob (2024-12-16T21:52:13Z)

Closing this issue, as it only reproduced on one machine, and doesn't reproduce anymore today, so that was just a machine in a bad state.

---
