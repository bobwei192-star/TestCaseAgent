# [Issue]: (Windows) Strix Halo: Memory allocations not going to VRAM

> **Issue #5940**
> **状态**: closed
> **创建时间**: 2026-02-06T23:44:01Z
> **更新时间**: 2026-02-12T19:48:50Z
> **关闭时间**: 2026-02-12T19:48:50Z
> **作者**: benrichard-amd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5940

## 负责人

- benrichard-amd

## 描述

### Problem Description

When VRAM is set to 96GB in BIOS, calls to `hipMalloc` allocate shared memory even though there is room in VRAM.

### Operating System

Windows 11

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD Radeon (TM) 8060S Graphics

### ROCm Version

ROCm 7.12.0a20260206

### ROCm Component

_No response_

### Steps to Reproduce

1. Set VRAM to 96GB in BIOS
2. Allocate memory with `hipMalloc`
3. Observe memory usage

Even though the VRAM is 96GB, the allocations spill into shared memory while there is still lots of VRAM remaining. 

The behavior seems to be:
```
if current VRAM allocation < 32GB
    allocate in VRAM
else
    allocate in shared memory
```

Examples:

|Allocations|VRAM|Shared Memory|
|---|---|---|
|24GB + 24GB + 8GB|48GB|8GB|
|16GB + 16GB + 16GB|32GB|16GB|
|64GB|64GB|0GB|

e.g. this is the 16GB + 16GB + 16GB case:

<img width="957" height="696" alt="Image" src="https://github.com/user-attachments/assets/bb805269-aa63-439e-b29c-4994a703563b" />

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Driver details:

<img width="610" height="735" alt="Image" src="https://github.com/user-attachments/assets/d5fcfedf-b522-4048-98ae-328c978ae408" />


Sample program to test memory allocations (enter allocation amounts in MB, 0 to exit):

```
#include <hip/hip_runtime.h>
#include <iostream>
#include <vector>
#include <limits>

int main() {
    std::cout << "HIP Device Memory Allocation Tool (persistent allocations)\n";
    std::cout << "Enter memory size in MB to allocate on the GPU.\n";
    std::cout << "Enter 0 to free all allocations and exit.\n";

    // Select device 0 (change if needed)
    int device = 0;
    hipError_t err = hipSetDevice(device);
    if (err != hipSuccess) {
        std::cerr << "hipSetDevice failed: " << hipGetErrorString(err) << "\n";
        return 1;
    }
    hipDeviceProp_t props{};
    err = hipGetDeviceProperties(&props, device);
    if (err == hipSuccess) {
        std::cout << "Using device " << device << ": " << props.name << "\n";
    }

    const unsigned long long MB = 1024ULL * 1024ULL;
    std::vector<void*> allocations;
    std::vector<size_t> sizes;
    unsigned long long totalAllocatedBytes = 0;

    while (true) {
        std::cout << "\nEnter memory size (MB): ";
        long long mbInput;
        if (!(std::cin >> mbInput)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cerr << "Invalid input. Please enter an integer number of MB.\n";
            continue;
        }

        if (mbInput == 0) {
            std::cout << "Exiting. Freeing all allocations...\n";
            // Optional: synchronize before free
            hipDeviceSynchronize();

            // Free all allocations
            for (size_t i = 0; i < allocations.size(); ++i) {
                if (allocations[i]) {
                    err = hipFree(allocations[i]);
                    if (err != hipSuccess) {
                        std::cerr << "hipFree failed: " << hipGetErrorString(err) << "\n";
                    }
                }
            }
            std::cout << "Freed " << (totalAllocatedBytes / MB) << " MB in total.\n";
            break;
        }

        size_t bytes = static_cast<size_t>(mbInput * MB);

        // Show free/total memory before allocation
        size_t freeBefore = 0, total = 0;
        err = hipMemGetInfo(&freeBefore, &total);
        if (err == hipSuccess) {
            std::cout << "Device memory before allocation: "
                      << (freeBefore / MB) << " MB free / "
                      << (total / MB) << " MB total\n";
        } else {
            std::cerr << "hipMemGetInfo failed: " << hipGetErrorString(err) << "\n";
        }

        void* d_ptr = nullptr;
        err = hipMalloc(&d_ptr, bytes);
        if (err != hipSuccess) {
            std::cerr << "hipMalloc failed for " << mbInput << " MB: "
                      << hipGetErrorString(err) << "\n";
            continue;
        }

        // Touch the memory to ensure it's committed
        err = hipMemset(d_ptr, 0, bytes);
        if (err != hipSuccess) {
            std::cerr << "hipMemset failed: " << hipGetErrorString(err) << "\n";
        }

        // Track persistent allocation
        allocations.push_back(d_ptr);
        sizes.push_back(bytes);
        totalAllocatedBytes += bytes;

        std::cout << "Successfully allocated " << mbInput << " MB on device.\n";
        std::cout << "Total kept allocations: " << allocations.size()
                  << " | Total allocated: " << (totalAllocatedBytes / MB) << " MB\n";

        // Show free/total memory after allocation
        size_t freeAfterAlloc = 0;
        err = hipMemGetInfo(&freeAfterAlloc, &total);
        if (err == hipSuccess) {
            std::cout << "Device memory after allocation: "
                      << (freeAfterAlloc / MB) << " MB free / "
                      << (total / MB) << " MB total\n";
        }
    }

    return 0;
}
```

---

## 评论 (2 条)

### 评论 #1 — benrichard-amd (2026-02-09T15:04:20Z)

Same behavior when `OCL_SET_SVM_SIZE=262144` except the max allocatable size from a single `hipMalloc` is 96GB instead of 64GB.

---

### 评论 #2 — benrichard-amd (2026-02-12T19:48:50Z)

Fixed in upcoming driver release.

---
