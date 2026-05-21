# [Issue]: HIPCC: Unusual performance drop when copying an array of struct and not going through a local variable

> **Issue #4331**
> **状态**: open
> **创建时间**: 2025-02-03T15:25:36Z
> **更新时间**: 2025-02-04T15:17:42Z
> **作者**: TomClabault
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4331

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

HIPCC seems to be producing slower code when loading/storing a structure from/to global memory directly vs. going through a local variable before storing to gmem.

The first example (top row of editor/compiler pair) loads the structure from global memory (from `input`) and directly stores to `output`.
The second (bottom row) example does the same but it goes through a local variable before storing to `output`.

The second example is ~3x faster on my machine. Is that expected?

RGP profiler captures of the code on my machine (ROCm 5.7.1):

Slower example:
![Image](https://github.com/user-attachments/assets/6d80dfca-7433-409b-87d2-ffbaec4f57bc)

Faster example with a local variable:
![Image](https://github.com/user-attachments/assets/79bc4efa-3d20-4af4-aa15-d8ed96605ccc)

### Operating System

Windows 11

### CPU

Intel i5 13600KF

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 5.7.1 (local machine), ROCm 6.1.2 (through [Compiler Explorer](https://godbolt.org/))

### ROCm Component

HIP, HIPCC

### Steps to Reproduce

ROCm 6.1.2 compiler explorer reproducer: https://godbolt.org/z/MME7z5Pj5

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2025-02-03T16:34:39Z)

Hi @TomClabault. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-02-03T20:58:08Z)

Hi @TomClabault, thanks for reporting this! In the first case, the compiler is reusing the same registers for each global load, and has to perform the corresponding global store to empty the registers before loading the next chunk of memory. This means that the global loads here are executing synchronously, as seen by the `waitcnt` instructions between each pair of load/store. In contrast, in the second case, the compiler uses extra registers and is therefore able to group the global loads. Having multiple global loads in flight at once results in the speed increase you observe.

This is an interesting case as this seemingly redundant local variable appears to act as a compiler hint. In fact, simply adding what seems to be a redundant typecast also fixes the issue: https://godbolt.org/z/Ybs3esaTK. For similar reasons, I suspect this issue would be masked if any work was done on the input before assigning to the output, but the compiler seems to be blind to the potential optimization in this case where only assignment is performed.

While I'm not entirely sure of the cause of this at the moment, this seems to be fixed in upstream clang already: https://gcc.godbolt.org/z/8jdbzsbcq. This is fixed in our latest internal ROCm builds as well, so it should land in the next minor version. In the meantime, you can use a redundant local variable or typecast as a workaround for cases like this, although you'd have to inspect the assembly to check if the issue exists for a given kernel. You can also try compiling with upstream clang instead, either through [aomp](https://github.com/ROCm/aomp) or via LLVM directly.

---
