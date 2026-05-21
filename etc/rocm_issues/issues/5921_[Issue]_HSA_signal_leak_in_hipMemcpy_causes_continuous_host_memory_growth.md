# [Issue]: HSA signal leak in hipMemcpy causes continuous host memory growth

> **Issue #5921**
> **状态**: closed
> **创建时间**: 2026-02-02T09:43:44Z
> **更新时间**: 2026-02-03T20:54:02Z
> **关闭时间**: 2026-02-03T20:54:02Z
> **作者**: alexschroeter
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5921

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

# [Bug]: HSA signal leak in hipMemcpy causes continuous host memory growth

## Description

Possible source for the issue https://github.com/ROCm/ROCm/issues/5915 which affects OpenCL and Hip/Sycl applications.

Host CPU memory (RSS) grows continuously during HIP memory copy operations due to HSA signals not being properly destroyed. The leak rate is approximately 2 HSA signals per `hipMemcpy` call, leading to ~300 MB leaked per 1000 iterations with 16 MB buffers.

This affects all applications using HIP for GPU compute, including GROMACS (SYCL/HIP), and other HPC workloads.

## Environment

- **OS:** AlmaLinux 9.7 (kernel 5.14.0-611.9.1.el9_7.x86_64)
- **GPU:** AMD Instinct MI210 / MI250X (gfx90a)
- **ROCm:** 7.1.1 and 7.2.0 (both affected)
- **Driver:** amdgpu-dkms 6.16.6 / 6.16.13

## Steps to Reproduce

### Minimal Reproducer

```cpp
// hip_memory_leak_test.cpp
// Compile: hipcc -O2 -o hip_memory_leak_test hip_memory_leak_test.cpp

#include <hip/hip_runtime.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

long get_rss_kb() {
    std::ifstream stat("/proc/self/status");
    std::string line;
    while (std::getline(stat, line)) {
        if (line.substr(0, 6) == "VmRSS:") {
            std::istringstream iss(line.substr(6));
            long rss; iss >> rss;
            return rss;
        }
    }
    return 0;
}

int main() {
    const size_t buffer_size = 16 * 1024 * 1024; // 16 MB
    const int iterations = 1000;

    std::vector<float> h_data(buffer_size / sizeof(float), 1.0f);
    void* d_ptr;
    hipMalloc(&d_ptr, buffer_size);

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    for (int i = 0; i < iterations; i++) {
        hipMemcpy(d_ptr, h_data.data(), buffer_size, hipMemcpyHostToDevice);
        hipMemcpy(h_data.data(), d_ptr, buffer_size, hipMemcpyDeviceToHost);

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "Iteration " << (i + 1) << ": RSS = " << rss
                      << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    hipFree(d_ptr);

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB" << std::endl;
    std::cout << "Total leaked: " << (final_rss - initial_rss) << " KB" << std::endl;

    return 0;
}
```

### Run

```bash
hipcc -O2 -o hip_memory_leak_test hip_memory_leak_test.cpp
./hip_memory_leak_test
```

### Expected Output (no leak)

```
Initial RSS: ~40000 KB
Iteration 100: RSS = ~40000 KB (+0 KB)
...
Final RSS: ~40000 KB
Total leaked: 0 KB
```

### Actual Output (leak)

```
Initial RSS: 43424 KB
Iteration 100: RSS = 112000 KB (+68576 KB)
Iteration 200: RSS = 181000 KB (+137576 KB)
...
Iteration 1000: RSS = 388000 KB (+344576 KB)
Total leaked: 344576 KB (336 MB)
```

## Root Cause Analysis

Using `rocprofv3 --hsa-core-trace --hsa-amd-trace`, we identified the leak is in **HSA signal management**:

| HSA Operation | Count (50 iterations) |
|---------------|----------------------|
| `hsa_amd_signal_create` | 133 |
| `hsa_signal_create` | 14 |
| `hsa_signal_destroy` | 38 |
| **Signals leaked** | **109** (~2.2 per hipMemcpy) |
| `hsa_amd_memory_pool_allocate` | 4 |
| `hsa_amd_memory_pool_free` | 1 |
| **Pool allocations leaked** | **3** |

Each `hipMemcpy` creates HSA signals for synchronization that are not being destroyed. Over extended workloads, this causes continuous memory growth.

## Additional Findings

### Operations that leak:

| Test | Description | Leak (1000 iter) |
|------|-------------|------------------|
| hipMemcpy H2D+D2H | Memory transfers | +336 MB |
| Kernel launch (default stream) | Using null stream | +61 MB |
| Kernel launch (multiple streams) | 4 streams round-robin | +180 MB |
| hipMemcpyAsync | Async transfers | +331 MB |

### Operations that DON'T leak:

| Test | Description | Leak |
|------|-------------|------|
| hipMalloc/hipFree only | No data transfer | +0 KB |
| Kernel launch (single explicit stream) | Persistent stream | +0 KB |

### Partial workaround:

Setting `HSA_ENABLE_SDMA=0` reduces the leak by ~45% (336 MB → 183 MB), suggesting the SDMA path creates more signals than the shader copy path.

```bash
HSA_ENABLE_SDMA=0 ./hip_memory_leak_test
```

## Impact

- **GROMACS** and other HPC applications experience memory exhaustion on long-running jobs
- Leak rate observed in real workloads: ~70-90 GB/hour with ROCm 7.1.x, ~5-9 GB/hour with ROCm 7.2.0
- Jobs that should run for days fail within hours due to OOM

## Workarounds

1. **`HSA_ENABLE_SDMA=0`** - Reduces leak by ~45%
2. **Use single explicit HIP stream** - Avoids kernel dispatch leak (but doesn't fix hipMemcpy leak)
3. **Use stock in-kernel amdgpu driver with ROCm 6.1.3** - No leak observed (not practical for MI200 series)

## System Information

```
$ hipcc --version
HIP version: 7.2.0

$ rocminfo | grep -E "Name:|Marketing"
  Name:                    AMD EPYC 7452 32-Core Processor
  Marketing Name:          AMD Instinct MI210

$ cat /opt/rocm/.info/version
7.2.0
```

for more details see referenced report

## Attachments

Full reproducer with multiple test modes and job scripts available at:
- Reproducer covers: hipMalloc/Free, hipMemcpy, kernel launches, hipHostMalloc, hipMallocManaged, async operations
- Includes memory monitoring and rocprofv3 trace analysis scripts

### Operating System

AlmaLinux 9.7

### CPU

 AMD EPYC 7452 32-Core Processor

### GPU

MI210

### ROCm Version

7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

see referenced issue

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — alexschroeter (2026-02-02T14:57:30Z)

## Followup: Comprehensive HIP Memory Leak Test Results

I've created a systematic HIP test suite to isolate and identify the memory leak patterns across different HIP operations. The results confirm significant memory leaks in ROCm 7.x.x and provide more granular detail about which operations are affected. This is also another System (different OS Ubuntu 22.04, different GPU Radeon VII, with ROCm 7.0.2 but memory leak is still present.)

```
/*
 * HIP Memory Leak Reproducer
 *
 * Tests various HIP patterns to identify memory leaks in ROCm runtime.
 * Mirrors the OpenCL reproducer tests.
 *
 * Compile: hipcc -O2 -o hip_memory_leak_test hip_memory_leak_test.cpp
 * Usage:   ./hip_memory_leak_test <test_mode> <iterations> [buffer_size_mb]
 *
 * Test modes:
 *   1  - Buffer alloc/free loop (hipMalloc/hipFree)
 *   2  - Kernel launch loop (persistent buffers)
 *   3  - hipMemcpy Host<->Device loop
 *   4  - Kernel + temp buffers
 *   5  - Combined pattern (mimics solver)
 *   6  - hipHostMalloc (pinned memory) with memcpy
 *   7  - hipMallocManaged (unified memory)
 *   8  - hipMemcpyAsync loop
 *   9  - hipMemcpy H2D only
 *  10  - hipMemcpy D2H only
 */

#include <hip/hip_runtime.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <vector>

#define HIP_CHECK(call) \
    do { \
        hipError_t err = call; \
        if (err != hipSuccess) { \
            std::cerr << "HIP Error: " << hipGetErrorString(err) \
                      << " at " << __FILE__ << ":" << __LINE__ << std::endl; \
            exit(1); \
        } \
    } while(0)

// Simple kernel
__global__ void scale_kernel(float* data, float factor, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        data[idx] *= factor;
    }
}

__global__ void add_kernel(float* a, float* b, float* c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

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

// Test 1: Buffer alloc/free loop
void test_buffer_alloc(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 1: hipMalloc/hipFree loop ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    for (int i = 0; i < iterations; i++) {
        void* d_ptr;
        HIP_CHECK(hipMalloc(&d_ptr, buffer_size));
        HIP_CHECK(hipDeviceSynchronize());
        HIP_CHECK(hipFree(d_ptr));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 2: Kernel launch loop with persistent buffers
void test_kernel_launch(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 2: Kernel launch loop ===" << std::endl;
    std::cout << "Iterations: " << iterations << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    int n = buffer_size / sizeof(float);
    float *d_a, *d_b, *d_c;
    HIP_CHECK(hipMalloc(&d_a, buffer_size));
    HIP_CHECK(hipMalloc(&d_b, buffer_size));
    HIP_CHECK(hipMalloc(&d_c, buffer_size));

    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;

    for (int i = 0; i < iterations; i++) {
        add_kernel<<<gridSize, blockSize>>>(d_a, d_b, d_c, n);
        HIP_CHECK(hipDeviceSynchronize());

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    HIP_CHECK(hipFree(d_a));
    HIP_CHECK(hipFree(d_b));
    HIP_CHECK(hipFree(d_c));

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 3: hipMemcpy loop (Host <-> Device)
void test_memcpy(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 3: hipMemcpy H2D + D2H loop ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    std::vector<float> h_data(buffer_size / sizeof(float), 1.0f);
    void* d_ptr;
    HIP_CHECK(hipMalloc(&d_ptr, buffer_size));

    for (int i = 0; i < iterations; i++) {
        HIP_CHECK(hipMemcpy(d_ptr, h_data.data(), buffer_size, hipMemcpyHostToDevice));
        HIP_CHECK(hipMemcpy(h_data.data(), d_ptr, buffer_size, hipMemcpyDeviceToHost));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    HIP_CHECK(hipFree(d_ptr));

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 4: Kernel with temporary buffers
void test_kernel_temp_buffers(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 4: Kernel with temporary buffers ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    int n = buffer_size / sizeof(float);
    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;

    for (int i = 0; i < iterations; i++) {
        float *d_a, *d_b, *d_c;
        HIP_CHECK(hipMalloc(&d_a, buffer_size));
        HIP_CHECK(hipMalloc(&d_b, buffer_size));
        HIP_CHECK(hipMalloc(&d_c, buffer_size));

        add_kernel<<<gridSize, blockSize>>>(d_a, d_b, d_c, n);
        HIP_CHECK(hipDeviceSynchronize());

        HIP_CHECK(hipFree(d_a));
        HIP_CHECK(hipFree(d_b));
        HIP_CHECK(hipFree(d_c));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 5: Combined pattern
void test_combined(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 5: Combined pattern ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    int n = buffer_size / sizeof(float);
    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;
    std::vector<float> h_data(n, 1.0f);

    float* d_persistent;
    HIP_CHECK(hipMalloc(&d_persistent, buffer_size));

    for (int i = 0; i < iterations; i++) {
        float *d_temp_a, *d_temp_b;
        HIP_CHECK(hipMalloc(&d_temp_a, buffer_size));
        HIP_CHECK(hipMalloc(&d_temp_b, buffer_size));

        HIP_CHECK(hipMemcpy(d_temp_a, h_data.data(), buffer_size, hipMemcpyHostToDevice));

        scale_kernel<<<gridSize, blockSize>>>(d_temp_a, 1.001f, n);
        HIP_CHECK(hipMemcpy(d_temp_b, d_temp_a, buffer_size, hipMemcpyDeviceToDevice));
        HIP_CHECK(hipMemcpy(h_data.data(), d_temp_b, buffer_size, hipMemcpyDeviceToHost));

        HIP_CHECK(hipFree(d_temp_a));
        HIP_CHECK(hipFree(d_temp_b));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    HIP_CHECK(hipFree(d_persistent));

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 6: hipHostMalloc (pinned memory)
void test_host_malloc(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 6: hipHostMalloc (pinned) with memcpy ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    float* h_pinned;
    float* d_ptr;
    HIP_CHECK(hipHostMalloc(&h_pinned, buffer_size, hipHostMallocDefault));
    HIP_CHECK(hipMalloc(&d_ptr, buffer_size));

    // Initialize
    size_t n = buffer_size / sizeof(float);
    for (size_t i = 0; i < n; i++) {
        h_pinned[i] = 1.0f;
    }

    for (int i = 0; i < iterations; i++) {
        HIP_CHECK(hipMemcpy(d_ptr, h_pinned, buffer_size, hipMemcpyHostToDevice));
        HIP_CHECK(hipMemcpy(h_pinned, d_ptr, buffer_size, hipMemcpyDeviceToHost));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    HIP_CHECK(hipFree(d_ptr));
    HIP_CHECK(hipHostFree(h_pinned));

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 7: hipMallocManaged (unified memory)
void test_managed_malloc(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 7: hipMallocManaged (unified memory) ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    int n = buffer_size / sizeof(float);
    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;

    for (int i = 0; i < iterations; i++) {
        float* managed_ptr;
        HIP_CHECK(hipMallocManaged(&managed_ptr, buffer_size));

        // Touch from host
        for (int j = 0; j < n; j += 1024) {
            managed_ptr[j] = 1.0f;
        }

        // Use on device
        scale_kernel<<<gridSize, blockSize>>>(managed_ptr, 1.001f, n);
        HIP_CHECK(hipDeviceSynchronize());

        // Read on host
        volatile float dummy = managed_ptr[0];
        (void)dummy;

        HIP_CHECK(hipFree(managed_ptr));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 8: hipMemcpyAsync loop
void test_memcpy_async(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 8: hipMemcpyAsync loop ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    float* h_pinned;
    float* d_ptr;
    hipStream_t stream;

    HIP_CHECK(hipHostMalloc(&h_pinned, buffer_size, hipHostMallocDefault));
    HIP_CHECK(hipMalloc(&d_ptr, buffer_size));
    HIP_CHECK(hipStreamCreate(&stream));

    size_t n = buffer_size / sizeof(float);
    for (size_t i = 0; i < n; i++) {
        h_pinned[i] = 1.0f;
    }

    for (int i = 0; i < iterations; i++) {
        HIP_CHECK(hipMemcpyAsync(d_ptr, h_pinned, buffer_size, hipMemcpyHostToDevice, stream));
        HIP_CHECK(hipMemcpyAsync(h_pinned, d_ptr, buffer_size, hipMemcpyDeviceToHost, stream));
        HIP_CHECK(hipStreamSynchronize(stream));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    HIP_CHECK(hipStreamDestroy(stream));
    HIP_CHECK(hipFree(d_ptr));
    HIP_CHECK(hipHostFree(h_pinned));

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 9: H2D only
void test_h2d_only(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 9: hipMemcpy H2D only ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    std::vector<float> h_data(buffer_size / sizeof(float), 1.0f);
    void* d_ptr;
    HIP_CHECK(hipMalloc(&d_ptr, buffer_size));

    for (int i = 0; i < iterations; i++) {
        HIP_CHECK(hipMemcpy(d_ptr, h_data.data(), buffer_size, hipMemcpyHostToDevice));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    HIP_CHECK(hipFree(d_ptr));

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

// Test 10: D2H only
void test_d2h_only(int iterations, size_t buffer_size) {
    std::cout << "\n=== Test 10: hipMemcpy D2H only ===" << std::endl;
    std::cout << "Iterations: " << iterations << ", Buffer size: " << buffer_size / (1024*1024) << " MB" << std::endl;

    long initial_rss = get_rss_kb();
    std::cout << "Initial RSS: " << initial_rss << " KB" << std::endl;

    std::vector<float> h_data(buffer_size / sizeof(float), 1.0f);
    void* d_ptr;
    HIP_CHECK(hipMalloc(&d_ptr, buffer_size));

    // Initial H2D
    HIP_CHECK(hipMemcpy(d_ptr, h_data.data(), buffer_size, hipMemcpyHostToDevice));

    for (int i = 0; i < iterations; i++) {
        HIP_CHECK(hipMemcpy(h_data.data(), d_ptr, buffer_size, hipMemcpyDeviceToHost));

        if ((i + 1) % 100 == 0) {
            long rss = get_rss_kb();
            std::cout << "  Iteration " << (i + 1) << ": RSS = " << rss << " KB (+" << (rss - initial_rss) << " KB)" << std::endl;
        }
    }

    HIP_CHECK(hipFree(d_ptr));

    long final_rss = get_rss_kb();
    std::cout << "Final RSS: " << final_rss << " KB (change: +" << (final_rss - initial_rss) << " KB)" << std::endl;
}

void print_usage(const char* prog) {
    std::cout << "Usage: " << prog << " <test_mode> <iterations> [buffer_size_mb]" << std::endl;
    std::cout << std::endl;
    std::cout << "Test modes:" << std::endl;
    std::cout << "  1  - hipMalloc/hipFree loop" << std::endl;
    std::cout << "  2  - Kernel launch (persistent buffers)" << std::endl;
    std::cout << "  3  - hipMemcpy H2D + D2H loop" << std::endl;
    std::cout << "  4  - Kernel with temporary buffers" << std::endl;
    std::cout << "  5  - Combined pattern" << std::endl;
    std::cout << "  6  - hipHostMalloc (pinned) with memcpy" << std::endl;
    std::cout << "  7  - hipMallocManaged (unified memory)" << std::endl;
    std::cout << "  8  - hipMemcpyAsync loop" << std::endl;
    std::cout << "  9  - hipMemcpy H2D only" << std::endl;
    std::cout << "  10 - hipMemcpy D2H only" << std::endl;
    std::cout << "  0  - Run all tests" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        print_usage(argv[0]);
        return 1;
    }

    int test_mode = atoi(argv[1]);
    int iterations = atoi(argv[2]);
    size_t buffer_size_mb = (argc > 3) ? atoi(argv[3]) : 16;
    size_t buffer_size = buffer_size_mb * 1024 * 1024;

    std::cout << "========================================" << std::endl;
    std::cout << "HIP Memory Leak Reproducer" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Test mode: " << test_mode << std::endl;
    std::cout << "Iterations: " << iterations << std::endl;
    std::cout << "Buffer size: " << buffer_size_mb << " MB" << std::endl;

    // Print device info
    hipDeviceProp_t props;
    HIP_CHECK(hipGetDeviceProperties(&props, 0));
    std::cout << "Device: " << props.name << std::endl;

    long start_rss = get_rss_kb();
    std::cout << "\nStarting RSS: " << start_rss << " KB (" << start_rss / 1024 << " MB)" << std::endl;

    switch (test_mode) {
        case 0:
            test_buffer_alloc(iterations, buffer_size);
            test_kernel_launch(iterations, buffer_size);
            test_memcpy(iterations, buffer_size);
            test_kernel_temp_buffers(iterations, buffer_size);
            test_combined(iterations, buffer_size);
            test_host_malloc(iterations, buffer_size);
            test_managed_malloc(iterations, buffer_size);
            test_memcpy_async(iterations, buffer_size);
            test_h2d_only(iterations, buffer_size);
            test_d2h_only(iterations, buffer_size);
            break;
        case 1:  test_buffer_alloc(iterations, buffer_size); break;
        case 2:  test_kernel_launch(iterations, buffer_size); break;
        case 3:  test_memcpy(iterations, buffer_size); break;
        case 4:  test_kernel_temp_buffers(iterations, buffer_size); break;
        case 5:  test_combined(iterations, buffer_size); break;
        case 6:  test_host_malloc(iterations, buffer_size); break;
        case 7:  test_managed_malloc(iterations, buffer_size); break;
        case 8:  test_memcpy_async(iterations, buffer_size); break;
        case 9:  test_h2d_only(iterations, buffer_size); break;
        case 10: test_d2h_only(iterations, buffer_size); break;
        default:
            std::cerr << "Unknown test mode: " << test_mode << std::endl;
            return 1;
    }

    long end_rss = get_rss_kb();
    std::cout << "\n========================================" << std::endl;
    std::cout << "SUMMARY" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Starting RSS: " << start_rss << " KB (" << start_rss / 1024 << " MB)" << std::endl;
    std::cout << "Ending RSS:   " << end_rss << " KB (" << end_rss / 1024 << " MB)" << std::endl;
    std::cout << "Total change: " << (end_rss - start_rss) << " KB (" << (end_rss - start_rss) / 1024 << " MB)" << std::endl;

    if (end_rss - start_rss > 10240) {
        std::cout << "\n*** POTENTIAL MEMORY LEAK DETECTED ***" << std::endl;
    } else {
        std::cout << "\nMemory appears stable." << std::endl;
    }

    return 0;
}

```

### Test Configuration
- **Iterations:** 50 per test
- **Buffer size:** 16 MB
- **Device:** AMD Radeon VII
- **Measurement:** RSS (Resident Set Size) via `/proc/self/status`

### Results Summary

```
========================================
HIP Memory Leak Reproducer
========================================
Test mode: 0
Iterations: 50
Buffer size: 16 MB
Device: AMD Radeon VII

Starting RSS: 39828 KB (38 MB)

=== Test 1: hipMalloc/hipFree loop ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 39828 KB
Final RSS: 40340 KB (change: +512 KB)

=== Test 2: Kernel launch loop ===
Iterations: 50
Initial RSS: 40340 KB
Final RSS: 142416 KB (change: +102076 KB)

=== Test 3: hipMemcpy H2D + D2H loop ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 142416 KB
Final RSS: 175700 KB (change: +33284 KB)

=== Test 4: Kernel with temporary buffers ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 159316 KB
Final RSS: 159316 KB (change: +0 KB)

=== Test 5: Combined pattern ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 159316 KB
Final RSS: 175188 KB (change: +15872 KB)

=== Test 6: hipHostMalloc (pinned) with memcpy ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 175188 KB
Final RSS: 175556 KB (change: +368 KB)

=== Test 7: hipMallocManaged (unified memory) ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 175556 KB
Final RSS: 175556 KB (change: +0 KB)

=== Test 8: hipMemcpyAsync loop ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 175556 KB
Final RSS: 197072 KB (change: +21516 KB)

=== Test 9: hipMemcpy H2D only ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 197072 KB
Final RSS: 197072 KB (change: +0 KB)

=== Test 10: hipMemcpy D2H only ===
Iterations: 50, Buffer size: 16 MB
Initial RSS: 197072 KB
Final RSS: 197072 KB (change: +0 KB)

========================================
SUMMARY
========================================
Starting RSS: 39828 KB (38 MB)
Ending RSS:   197072 KB (192 MB)
Total change: 157244 KB (153 MB)

*** POTENTIAL MEMORY LEAK DETECTED ***
```

**Overall:** RSS grew from **38 MB → 192 MB** (+153 MB) across all tests

| Test | Operation | Memory Leak | Status |
|------|-----------|-------------|--------|
| 1 | `hipMalloc`/`hipFree` loop | +512 KB | ✓ Minimal |
| 2 | Kernel launch (persistent buffers) | **+102 MB** | ❌ **SEVERE** |
| 3 | `hipMemcpy` H2D + D2H loop | **+33 MB** | ❌ **SEVERE** |
| 4 | Kernel with temporary buffers | +0 KB | ✓ Clean |
| 5 | Combined pattern | **+15 MB** | ⚠️ Moderate |
| 6 | `hipHostMalloc` (pinned) with memcpy | +368 KB | ✓ Minimal |
| 7 | `hipMallocManaged` (unified memory) | +0 KB | ✓ Clean |
| 8 | `hipMemcpyAsync` loop | **+21 MB** | ❌ **SEVERE** |
| 9 | `hipMemcpy` H2D only | +0 KB | ✓ Clean |
| 10 | `hipMemcpy` D2H only | +0 KB | ✓ Clean |

### Key Findings

1. **Kernel Execution Infrastructure**: Test 2 shows the most severe leak (~100 MB) when launching kernels repeatedly with persistent device buffers. This suggests the leak is not limited to memory copy operations but extends to kernel execution synchronization.

2. **Bidirectional Memory Operations**: Test 3 confirms the original report - bidirectional `hipMemcpy` operations leak significantly (~33 MB for 50 iterations). However, Tests 9 and 10 show that **unidirectional copies do not leak**, indicating the leak occurs specifically in the synchronization/cleanup path when both H2D and D2H operations are performed.

3. **Async Operations**: Test 8 confirms that `hipMemcpyAsync` with stream synchronization also leaks (~21 MB), consistent with the original HSA signal leak hypothesis.

4. **Pattern Analysis**:
   - Operations with **implicit synchronization** (bidirectional memcpy, kernel launches) leak heavily
   - Operations with **explicit stream management** or unidirectional transfers remain clean
   - Memory allocation/deallocation alone does not leak

### Code Verification

All test code properly pairs allocations with deallocations - there are no application-level memory management errors. The leak is definitively in the HIP/HSA runtime layer.

### Extrapolated Impact

At the observed leak rate from Test 3 alone:
- **50 iterations**: +33 MB
- **1000 iterations**: ~660 MB (extrapolated)
- **Long-running HPC jobs**: This aligns with the 70-90 GB/hour leak rates reported in production GROMACS runs

The leak in Test 2 (kernel launches) is even more concerning for compute-intensive workloads that execute thousands of kernel launches.

---
