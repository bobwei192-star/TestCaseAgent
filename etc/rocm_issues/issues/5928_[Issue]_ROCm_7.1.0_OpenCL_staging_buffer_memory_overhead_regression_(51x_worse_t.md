# [Issue]: ROCm 7.1.0 OpenCL staging buffer memory overhead regression (51x worse than 6.1.3)

> **Issue #5928**
> **状态**: closed
> **创建时间**: 2026-02-03T22:15:24Z
> **更新时间**: 2026-03-18T14:51:46Z
> **关闭时间**: 2026-03-18T14:51:46Z
> **作者**: alexschroeter
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5928

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

## Summary

We have issues with memory leaks on the new ROCm 7. One of the examples is an OpenCL code for which I was able to identify "a fix". Changing `const cl_mem_flags mem_flags = (place_on_host ? CL_MEM_ALLOC_HOST_PTR : 0) | extra_flags;` to this `const cl_mem_flags mem_flags = CL_MEM_ALLOC_HOST_PTR  | extra_flags;` did the trick, but I believe it just masks the issue. In my opinion, ROCm 7.x introduces a severe memory overhead regression in OpenCL when using device-only buffers with host↔device transfers. Staging buffer overhead increased from 3 MB (ROCm 6.1.3) to 153 MB (ROCm 7.1.0) - a **51x regression**. I also see a big memory leak in the SYCL version of GROMACS, which I am unable to pin down. But using ROCm 6.1.3 also fixes the leak there.

## Environment

**ROCm 6.1.3 (Working):**
- Version: 6.1.3-122
- Device: AMD Instinct MI210 (gfx90a)
- OpenCL: 2.1 AMD-APP (3614.0)
- Result: 3 MB overhead ✅

**ROCm 7.1.0 (Regression):**
- Version: 7.1.0-52802
- Device: AMD Instinct MI210 (gfx90a)
- OpenCL: 2.0 AMD-APP (3614.0)
- Result: 153 MB overhead ❌ (51x worse)

**Pattern tested:**
```c
// Create device-only buffer (no CL_MEM_ALLOC_HOST_PTR)
cl_mem buffer = clCreateBuffer(context, CL_MEM_READ_WRITE, size, NULL, &err);

// Transfer Host → Device (triggers staging buffer allocation)
clEnqueueWriteBuffer(queue, buffer, CL_TRUE, 0, size, host_data, ...);

// Transfer Device → Host (uses staging buffer)
clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, size, host_data, ...);

// Release buffer
clReleaseMemObject(buffer);
```

**Expected (ROCm 6.1.3):** ~3 MB overhead
**Actual (ROCm 7.1.0):** ~153 MB overhead

## Results

### Device-Only Buffers (Regression)

```
ROCm 6.1.3:
  Iteration 100:  RSS = +3 MB    ✅
  Iteration 1000: RSS = +3 MB    (stable)

ROCm 7.1.0:
  Iteration 100:  RSS = +153 MB  ❌ REGRESSION
  Iteration 1000: RSS = +153 MB  (stable, not a leak)
```

### With CL_MEM_ALLOC_HOST_PTR (Workaround)

```
ROCm 6.1.3:  +0.1 MB  ✅
ROCm 7.1.0:  +0.09 MB ✅ (workaround effective)
```

## Root Cause

ROCm 7.x appears to allocate a much larger staging buffer pool (~153 MB) compared to ROCm 6.x (~3 MB) for handling pageable host memory transfers. The memory plateaus immediately rather than growing linearly, indicating a one-time pool allocation that is 51x larger than necessary.

## Workaround

Use `CL_MEM_ALLOC_HOST_PTR` to allocate host-accessible memory upfront, avoiding staging buffers:

```c
cl_mem buffer = clCreateBuffer(context, 
    CL_MEM_ALLOC_HOST_PTR | CL_MEM_READ_WRITE, size, NULL, &err);
```

This reduces overhead from 153 MB to ~0.1 MB on ROCm 7.1.0.

### Operating System

Alma 9.7

### CPU

AMD EPYC 7452 32-Core Processor

### GPU

MI210

### ROCm Version

6.1.3, 7.1.0

### ROCm Component

_No response_

### Steps to Reproduce


```bash
# Compile
g++ -O2 -o opencl_staging_leak opencl_staging_leak.cpp -lOpenCL

# Run test (1000 iterations, 16 MB buffers, device-only mode)
./opencl_staging_leak 1000 16 0

./opencl_staging_leak 1000 16 1
```

```
/*
 * Minimal OpenCL Staging Buffer Leak Reproducer
 *
 * Demonstrates memory leak in AMD ROCm OpenCL when using device-only buffers
 * with clEnqueueReadBuffer/clEnqueueWriteBuffer (implicit staging).
 *
 * Compile: g++ -O2 -o opencl_staging_leak opencl_staging_leak.cpp -lOpenCL
 * Usage:   ./opencl_staging_leak <iterations> [buffer_size_mb] [use_host_ptr]
 *
 * Example:
 *   ./opencl_staging_leak 1000 16 0    # Device-only (leaks)
 *   ./opencl_staging_leak 1000 16 1    # CL_MEM_ALLOC_HOST_PTR (no leak)
 */

#include <CL/cl.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <cstring>

#define CL_CHECK(call) \
    do { \
        cl_int err = call; \
        if (err != CL_SUCCESS) { \
            std::cerr << "OpenCL Error: " << err \
                      << " at " << __FILE__ << ":" << __LINE__ << std::endl; \
            exit(1); \
        } \
    } while(0)

// Get current RSS memory in KB
long get_rss_kb() {
    std::ifstream stat("/proc/self/status");
    std::string line;
    while (std::getline(stat, line)) {
        if (line.substr(0, 6) == "VmRSS:") {
            std::istringstream iss(line.substr(6));
            long rss;
            iss >> rss;
            return rss;
        }
    }
    return 0;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " <iterations> [buffer_size_mb] [use_host_ptr]" << std::endl;
        std::cout << "  use_host_ptr: 0 = device-only (leaks), 1 = CL_MEM_ALLOC_HOST_PTR (no leak)" << std::endl;
        return 1;
    }

    int iterations = atoi(argv[1]);
    size_t buffer_size_mb = (argc > 2) ? atoi(argv[2]) : 16;
    bool use_host_ptr = (argc > 3) ? (atoi(argv[3]) != 0) : false;
    size_t buffer_size = buffer_size_mb * 1024 * 1024;

    std::cout << "========================================" << std::endl;
    std::cout << "OpenCL Staging Buffer Leak Reproducer" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Iterations: " << iterations << std::endl;
    std::cout << "Buffer size: " << buffer_size_mb << " MB" << std::endl;
    std::cout << "Mode: " << (use_host_ptr ? "CL_MEM_ALLOC_HOST_PTR (no leak)" : "Device-only (leaks)") << std::endl;

    // Setup OpenCL
    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;

    // Find AMD platform (not POCL)
    cl_uint num_platforms;
    CL_CHECK(clGetPlatformIDs(0, nullptr, &num_platforms));
    
    cl_platform_id platforms[10];
    CL_CHECK(clGetPlatformIDs(num_platforms, platforms, nullptr));
    
    bool found_amd = false;
    for (cl_uint i = 0; i < num_platforms; i++) {
        char vendor[256];
        CL_CHECK(clGetPlatformInfo(platforms[i], CL_PLATFORM_VENDOR, sizeof(vendor), vendor, nullptr));
        
        if (strstr(vendor, "Advanced Micro Devices") || strstr(vendor, "AMD")) {
            platform = platforms[i];
            found_amd = true;
            
            char name[256];
            clGetPlatformInfo(platform, CL_PLATFORM_NAME, sizeof(name), name, nullptr);
            std::cout << "Using platform: " << name << std::endl;
            break;
        }
    }
    
    if (!found_amd) {
        std::cerr << "ERROR: No AMD OpenCL platform found!" << std::endl;
        return 1;
    }
    
    CL_CHECK(clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, nullptr));
    
    char device_name[256];
    CL_CHECK(clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(device_name), device_name, nullptr));
    std::cout << "Device: " << device_name << std::endl;

    cl_int err;
    context = clCreateContext(nullptr, 1, &device, nullptr, nullptr, &err);
    CL_CHECK(err);
    
    queue = clCreateCommandQueue(context, device, 0, &err);
    CL_CHECK(err);

    // Allocate host buffer
    std::vector<char> host_data(buffer_size, 0xAB);

    long initial_rss = get_rss_kb();
    std::cout << "\nInitial RSS: " << initial_rss << " KB (" << initial_rss / 1024 << " MB)" << std::endl;
    std::cout << "\nRunning test..." << std::endl;

    // Main test loop
    for (int i = 0; i < iterations; i++) {
        // Create buffer with appropriate flags
        cl_mem_flags mem_flags = use_host_ptr ? CL_MEM_ALLOC_HOST_PTR : 0;
        cl_mem buffer = clCreateBuffer(context, mem_flags | CL_MEM_READ_WRITE, 
                                       buffer_size, nullptr, &err);
        CL_CHECK(err);

        // Write to device (creates implicit staging if device-only)
        CL_CHECK(clEnqueueWriteBuffer(queue, buffer, CL_FALSE, 0, buffer_size, 
                                      host_data.data(), 0, nullptr, nullptr));

        // Read from device (creates implicit staging if device-only)
        CL_CHECK(clEnqueueReadBuffer(queue, buffer, CL_FALSE, 0, buffer_size, 
                                     host_data.data(), 0, nullptr, nullptr));

        // Wait for completion
        CL_CHECK(clFinish(queue));

        // Release buffer (should release staging buffers too, but doesn't in AMD runtime)
        CL_CHECK(clReleaseMemObject(buffer));

        // Print progress
        if ((i + 1) % 100 == 0) {
            long current_rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) 
                      << ": RSS = " << current_rss << " KB"
                      << " (+" << (current_rss - initial_rss) << " KB / +"
                      << (current_rss - initial_rss) / 1024 << " MB)" << std::endl;
        }
    }

    long final_rss = get_rss_kb();

    // Cleanup
    CL_CHECK(clReleaseCommandQueue(queue));
    CL_CHECK(clReleaseContext(context));

    std::cout << "\n========================================" << std::endl;
    std::cout << "RESULTS" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Initial RSS: " << initial_rss << " KB (" << initial_rss / 1024 << " MB)" << std::endl;
    std::cout << "Final RSS:   " << final_rss << " KB (" << final_rss / 1024 << " MB)" << std::endl;
    std::cout << "Change:      " << (final_rss - initial_rss) << " KB (" 
              << (final_rss - initial_rss) / 1024 << " MB)" << std::endl;

    // Calculate expected leak if it's per-iteration
    long change_kb = final_rss - initial_rss;
    double kb_per_iter = (double)change_kb / iterations;
    
    std::cout << "\nPer-iteration average: " << kb_per_iter << " KB" << std::endl;

    if (change_kb > 10240) {  // More than 10 MB growth
        std::cout << "\n*** MEMORY LEAK DETECTED ***" << std::endl;
        if (!use_host_ptr) {
            std::cout << "This is the expected leak with device-only buffers." << std::endl;
            std::cout << "Run with use_host_ptr=1 to see the fix." << std::endl;
        }
    } else {
        std::cout << "\nMemory appears stable - no leak detected." << std::endl;
        if (use_host_ptr) {
            std::cout << "CL_MEM_ALLOC_HOST_PTR prevents the staging buffer leak." << std::endl;
        }
    }

    return 0;
}
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — tcgu-amd (2026-02-09T20:15:28Z)

Hi @alexschroeter Thanks for bringing this issue to our attention! Is this issue specific to MI210? I tried to run your reproducer on 7900XT with the latest ROCm 7.2 and so far it seems like no matter how many iterations the staging buffer is consistently 16 MB. 

---

### 评论 #2 — alexschroeter (2026-02-10T14:51:22Z)

Thanks for testing on the 7900XT. The 16 MB you're seeing there is actually the expected/correct behavior — it matches the buffer size used in the test.

The issue seems to maybe be specific to MI-series (CDNA) hardware. I've now tested across four ROCm versions on MI210 (gfx90a), and the regression was introduced between 6.1.3 and 6.4.4:

| ROCm Version | Device-only Staging Overhead | With CL_MEM_ALLOC_HOST_PTR |
|---|---|---|
| 6.1.3 | 3 MB ✅ | 0.1 MB |
| 6.4.4 | 123 MB ❌ | 0.07 MB |
| 7.1.0 | 153 MB ❌ | 0.09 MB |
| 7.2.0 | 153 MB ❌ | 0.02 MB |

All tests: (gfx90a:sramecc+:xnack-), 1000 iterations, 16 MB buffers.

To clarify: this isn't a traditional memory leak — the memory doesn't grow over time. It's a one-time staging buffer pool allocation that's ~40-50 larger on ROCm ≥6.4.4 compared to 6.1.3. The pool plateaus immediately and stays stable. 

My initial concern that this overhead might scale with the buffer size is not true so I don't believe this is responsible for the OOM issues.

The fact that the 7900XT (RDNA3) shows only 16 MB overhead on the same ROCm 7.2 suggests a CDNA-specific code path for the staging buffer pool sizing changed between 6.1.3 and 6.4.4.

Could you test the reproducer on MI-series hardware (MI210/MI250/MI300) to confirm? Also, is there an environment variable in the ROCr/HSA runtime to control the staging buffer pool size?

---

### 评论 #3 — tcgu-amd (2026-02-10T16:41:29Z)

@alexschroeter Thanks for the updates! Will try to reproduce on MI series! You can try control the staging buffer size though ~~GPU_STAGING_BUFFER_SIZE~~ maybe? 

Edit: tested that env var appeared to have no effect...

---

### 评论 #4 — tcgu-amd (2026-02-10T19:51:35Z)

@alexschroeter Managed to reproduce on MI300 for ROCm 7.1.1, both 100 and 1000 iterations yield around +193 MB of change. 

---

### 评论 #5 — tcgu-amd (2026-02-10T22:00:21Z)

@alexschroeter, with `HSAKMT_DEBUG_LEVEL=7`, I see the hsa log allocates around 185 MB of memory for CWSR, and there seems to be 8 MB of host staging buffer as well, which adds up. 

```
Allocating GTT for CWSR
hsaKmtSVMSetAttr: address 0x0x7ef478e00000 size 0xb167000
```

Can you try adding the kernel module parameter `amdgpu.cwsr_enable=0`, reboot your system, and see if the memory leak is still there? 

I have attached the full log below. Thanks!

[log.txt](https://github.com/user-attachments/files/25221017/log.txt)

---

### 评论 #6 — alexschroeter (2026-02-11T08:19:06Z)

I can try to verify later today with amdgpu.cwsr_enable=0, but I would expect the overall memory footprint to go down, and the real leak to still be there.

---

### 评论 #7 — tcgu-amd (2026-02-17T15:15:37Z)

Hi @alexschroeter were you able to give it a try yet? Thanks! 

---

### 评论 #8 — alexschroeter (2026-02-17T15:19:46Z)

Sry, no. We are focusing on getting the system back to a working state. But this is in the backlog.

---

### 评论 #9 — tcgu-amd (2026-03-18T14:51:46Z)

Hi @alexschroeter since this issue appears not to be the main culprit behind the GROMACS case and is off the focus, I'm just going to close it here. Please do let me know if you want further assistance on this. Thanks! 

---
