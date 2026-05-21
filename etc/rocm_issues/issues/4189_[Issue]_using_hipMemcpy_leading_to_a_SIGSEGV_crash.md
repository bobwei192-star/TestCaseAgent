# [Issue]: using hipMemcpy leading to a SIGSEGV crash

> **Issue #4189**
> **状态**: closed
> **创建时间**: 2024-12-23T08:18:07Z
> **更新时间**: 2025-05-22T13:55:11Z
> **关闭时间**: 2025-05-07T19:17:16Z
> **作者**: DarkMatter-999
> **标签**: Under Investigation, ROCm 6.1.0, AMD Radeon RX 570 Series
> **URL**: https://github.com/ROCm/ROCm/issues/4189

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.1.0** (颜色: #ededed)
- **AMD Radeon RX 570 Series** (颜色: #ededed)

## 描述

### Problem Description

When executing a program compiled with `hipcc` it crashes after attempting to call hipMemcpy

```bash
$ hipcc test.cu
$ AMD_LOG_LEVEL=7  ./a.out
Max size: 4096
:3:rocdevice.cpp            :468 : 0865319405 us: [pid:3017  tid:0x7782cc1ff180] Initializing HSA stack.
:3:rocdevice.cpp            :554 : 0865326945 us: [pid:3017  tid:0x7782cc1ff180] Enumerated GPU agents = 1
:3:rocdevice.cpp            :232 : 0865326984 us: [pid:3017  tid:0x7782cc1ff180] Numa selects cpu agent[0]=0x55e59ce8df10(fine=0x55e59ce89ac0,coarse=0x55e59ce89fe0) for gpu agent=0x55e59ce8a880 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :290 : 0865326992 us: [pid:3017  tid:0x7782cc1ff180] Using dev kernel arg wa = 0
:3:comgrctx.cpp             :33  : 0865326997 us: [pid:3017  tid:0x7782cc1ff180] Loading COMGR library.
:3:comgrctx.cpp             :126 : 0865327028 us: [pid:3017  tid:0x7782cc1ff180] Loaded COMGR library version 2.8.
:3:rocdevice.cpp            :1809: 0865327202 us: [pid:3017  tid:0x7782cc1ff180] Gfx Major/Minor/Stepping: 8/0/3
:3:rocdevice.cpp            :1811: 0865327209 us: [pid:3017  tid:0x7782cc1ff180] HMM support: 0, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1813: 0865327214 us: [pid:3017  tid:0x7782cc1ff180] Max SDMA Read Mask: 0x3, Max SDMA Write Mask: 0x3
:4:rocdevice.cpp            :2221: 0865327682 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa host memory 0x5003ff000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2221: 0865328294 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa host memory 0x5006ff000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2221: 0865329215 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa host memory 0x500c00000, size 0x400000, numa_node = 0
:4:rocdevice.cpp            :2221: 0865329377 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa host memory 0x204000, size 0x38, numa_node = 0
:4:runtime.cpp              :85  : 0865329459 us: [pid:3017  tid:0x7782cc1ff180] init
:3:hip_context.cpp          :49  : 0865329465 us: [pid:3017  tid:0x7782cc1ff180] Direct Dispatch: 1
:3:hip_event.cpp            :333 : 0865329614 us: [pid:3017  tid:0x7782cc1ff180]  hipEventCreate ( 0x7fff7f99f7e0 )
:3:hip_event.cpp            :339 : 0865329630 us: [pid:3017  tid:0x7782cc1ff180] hipEventCreate: Returned hipSuccess : event:0x55e59cebf370
:3:hip_event.cpp            :333 : 0865329636 us: [pid:3017  tid:0x7782cc1ff180]  hipEventCreate ( 0x7fff7f99f7d8 )
:3:hip_event.cpp            :339 : 0865329642 us: [pid:3017  tid:0x7782cc1ff180] hipEventCreate: Returned hipSuccess : event:0x55e59cebf640
:3:hip_memory.cpp           :615 : 0867968592 us: [pid:3017  tid:0x7782cc1ff180]  hipMalloc ( 0x7fff7f99f768, 67108864 )
:4:rocdevice.cpp            :2379: 0867969348 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa device memory 0x501400000, size 0x4000000
:3:rocdevice.cpp            :2418: 0867969356 us: [pid:3017  tid:0x7782cc1ff180] Device=0x55e59ceb7330, freeMem_ = 0xfc000000
:3:hip_memory.cpp           :617 : 0867969368 us: [pid:3017  tid:0x7782cc1ff180] hipMalloc: Returned hipSuccess : 0x501400000: duration: 776 us
:3:hip_memory.cpp           :615 : 0867969374 us: [pid:3017  tid:0x7782cc1ff180]  hipMalloc ( 0x7fff7f99f760, 67108864 )
:4:rocdevice.cpp            :2379: 0867969806 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa device memory 0x505800000, size 0x4000000
:3:rocdevice.cpp            :2418: 0867969814 us: [pid:3017  tid:0x7782cc1ff180] Device=0x55e59ceb7330, freeMem_ = 0xf8000000
:3:hip_memory.cpp           :617 : 0867969818 us: [pid:3017  tid:0x7782cc1ff180] hipMalloc: Returned hipSuccess : 0x505800000: duration: 444 us
:3:hip_memory.cpp           :615 : 0867969826 us: [pid:3017  tid:0x7782cc1ff180]  hipMalloc ( 0x7fff7f99f710, 67108864 )
:4:rocdevice.cpp            :2379: 0867970266 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa device memory 0x509c00000, size 0x4000000
:3:rocdevice.cpp            :2418: 0867970274 us: [pid:3017  tid:0x7782cc1ff180] Device=0x55e59ceb7330, freeMem_ = 0xf4000000
:3:hip_memory.cpp           :617 : 0867970279 us: [pid:3017  tid:0x7782cc1ff180] hipMalloc: Returned hipSuccess : 0x509c00000: duration: 453 us
:3:hip_memory.cpp           :615 : 0867970285 us: [pid:3017  tid:0x7782cc1ff180]  hipMalloc ( 0x7fff7f99f7d0, 67108864 )
:4:rocdevice.cpp            :2379: 0867970647 us: [pid:3017  tid:0x7782cc1ff180] Allocate hsa device memory 0x50e000000, size 0x4000000
:3:rocdevice.cpp            :2418: 0867970654 us: [pid:3017  tid:0x7782cc1ff180] Device=0x55e59ceb7330, freeMem_ = 0xf0000000
:3:hip_memory.cpp           :617 : 0867970658 us: [pid:3017  tid:0x7782cc1ff180] hipMalloc: Returned hipSuccess : 0x50e000000: duration: 373 us
:3:hip_memory.cpp           :690 : 0867970676 us: [pid:3017  tid:0x7782cc1ff180]  hipMemcpy ( 0x501400000, 0x7782affff010, 67108864, hipMemcpyHostToDevice )
:3:rocdevice.cpp            :3026: 0867970693 us: [pid:3017  tid:0x7782cc1ff180] Number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:4:command.cpp              :347 : 0868002516 us: [pid:3017  tid:0x7782cc1ff180] Command (CopyHostToDevice) enqueued: 0x55e59cec0ef0
fish: Job 1, 'AMD_LOG_LEVEL=7  ./a.out' terminated by signal SIGSEGV (Address boundary error)

$ sudo dmesg | tail
[  867.972499] a.out[3017]: segfault at 18 ip 00007782ccbca89d sp 00007fff7f99ef40 error 4 in libamdhip64.so.6.2.41134-65d174c3e[3ca89d,7782cc824000+430000] likely on CPU 10 (core 5, socket 0)
[  867.972514] Code: 00 31 f6 48 83 c5 08 e8 31 04 00 00 49 39 ec 75 ec 48 8b 83 48 01 00 00 48 8b a8 a0 01 00 00 48 8b 05 f7 64 1c 00 64 48 8b 10 <48> 8b 45 18 4c 8d 65 18 a8 01 0f 85 9b 03 00 00 48 89 c1 48 83 c9
[ 1561.179983] a.out[3682]: segfault at 18 ip 00007a57651b0f3d sp 00007ffce2aba720 error 4 in libamdhip64.so.6.1.40093-bd86f1708[3b0f3d,7a5764e23000+416000] likely on CPU 11 (core 6, socket 0)
[ 1561.179998] Code: 00 31 f6 48 83 c5 08 e8 61 04 00 00 49 39 ec 75 ec 48 8b 83 48 01 00 00 48 8b a8 a0 01 00 00 48 8b 05 67 de 1b 00 64 48 8b 10 <48> 8b 45 18 4c 8d 65 18 a8 01 0f 85 9b 03 00 00 48 89 c1 48 83 c9

```

The same program when run on `gfx90c` runs successfully.

I attempted to try to use the patch at [clr:pull#97](https://github.com/ROCm/clr/pull/97) but it still doesnt work.

I know `gfx803` is long deprecated but thats what I have at the moment, also I have successfully used the same device earlier(3-4 months) to run similar code which compiled and worked right away then.   


This is the program I was running, it fails at `line:78` at `hipMemcpy`  
```c
#include <hip/hip_runtime.h>
#include <stdio.h>
#include <stdlib.h>

#define CEIL_DIV(a, b) (((a) + (b) - 1) / (b))

#define hipCheck(ans) { hipAssert((ans), __FILE__, __LINE__); }
inline void hipAssert(hipError_t code, const char *file, int line, bool abort = true) {
    if (code != hipSuccess) {
        printf("HIP error: %s in file %s at line %d\n", hipGetErrorString(code), file, line);
        if (abort) exit(code);
    }
}

__global__ void sgemm_naive(int M, int N, int K, float alpha, const float *A,
                            const float *B, float beta, float *C) {
  const uint x = blockIdx.x * blockDim.x + threadIdx.x;
  const uint y = blockIdx.y * blockDim.y + threadIdx.y;

  // if statement is necessary to make things work under tile quantization
  if (x < M && y < N) {
    float tmp = 0.0;
    for (int i = 0; i < K; ++i) {
      tmp += A[x * K + i] * B[i * N + y];
    }
    // C = α*(A@B)+β*C
    C[x * N + y] = alpha * tmp + beta * C[x * N + y];
  }
}
void run_sgemm_naive(int M, int N, int K, float alpha, float *A, float *B,
                     float beta, float *C) {
  dim3 gridDim(CEIL_DIV(M, 32), CEIL_DIV(N, 32));
  dim3 blockDim(32, 32);
  sgemm_naive<<<gridDim, blockDim>>>(M, N, K, alpha, A, B, beta, C);
}

void randomize_matrix(float *mat, int N) {
	for (int i = 0; i < N; i++) {
		float tmp = (float)(rand() % 5) + 0.01 * (rand() % 5);
		tmp = (rand() % 2 == 0) ? tmp : tmp * (-1.);
		mat[i] = tmp;
	}
}

int main() {
	int N = 6;
        int SIZE[] = {128, 256, 512, 1024, 2048, 4096};

	long m, n, k, max_size;
	max_size = SIZE[N - 1];
	printf("Max size: %ld\n", max_size);

	float alpha = 0.5, beta = 3.0; // GEMM input parameters, C=α*AB+β*C

	float *A = nullptr, *B = nullptr, *C = nullptr, *C_ref = nullptr; // host matrices
	float *dA = nullptr, *dB = nullptr, *dC = nullptr, *dC_ref = nullptr; // device matrices

	float elapsed_time;
	hipEvent_t beg, end;
	hipCheck(hipEventCreate(&beg));
	hipCheck(hipEventCreate(&end));

	A = (float *)malloc(sizeof(float) * max_size * max_size);
	B = (float *)malloc(sizeof(float) * max_size * max_size);
	C = (float *)malloc(sizeof(float) * max_size * max_size);
	C_ref = (float *)malloc(sizeof(float) * max_size * max_size);


	randomize_matrix(A, max_size * max_size);
	randomize_matrix(B, max_size * max_size);
	randomize_matrix(C, max_size * max_size);

	hipCheck(hipMalloc(&dA, sizeof(float) * max_size * max_size));
	hipCheck(hipMalloc(&dB, sizeof(float) * max_size * max_size));
	hipCheck(hipMalloc(&dC, sizeof(float) * max_size * max_size));
	hipCheck(hipMalloc(&dC_ref, sizeof(float) * max_size * max_size));

	hipCheck(hipMemcpy(dA, A, sizeof(float) * max_size * max_size, hipMemcpyHostToDevice));
	hipCheck(hipMemcpy(dB, B, sizeof(float) * max_size * max_size, hipMemcpyHostToDevice));
	hipCheck(hipMemcpy(dC, C, sizeof(float) * max_size * max_size, hipMemcpyHostToDevice));
	hipCheck(hipMemcpy(dC_ref, C_ref, sizeof(float) * max_size * max_size, hipMemcpyHostToDevice));

	int repeat_times = 5;
	for (int s=0; s<N; s++) {
		int size = SIZE[s];
		m = n = k = size;
		
		printf("dimensions(m=n=k) %ld, alpha: %f, beta: %f\n", m, alpha, beta);
		
		hipCheck(hipEventRecord(beg));

		for (int j = 0; j < repeat_times; j++) {
			// We don't reset dC between runs to save time
			run_sgemm_naive(m, n, k, alpha, dA, dB, beta, dC);
		}

		hipCheck(hipEventRecord(end));
		hipCheck(hipEventSynchronize(beg));
		hipCheck(hipEventSynchronize(end));
		hipCheck(hipEventElapsedTime(&elapsed_time, beg, end));
		elapsed_time /= 1000.; // Convert to seconds

		long flops = 2 * m * n * k;
		printf(
        "Average elapsed time: (%7.6f) s, performance: (%7.1f) GFLOPS. size: "
        "(%ld).\n",
        elapsed_time / repeat_times,
        (repeat_times * flops * 1e-9) / elapsed_time, m);
	    fflush(stdout);

		hipCheck(hipMemcpy(dC, dC_ref, sizeof(float) * m * n, hipMemcpyDeviceToDevice));

	}

	free(A);
	free(B);
	free(C);
	free(C_ref);
	hipCheck(hipFree(dA));
	hipCheck(hipFree(dB));
	hipCheck(hipFree(dC));
	hipCheck(hipFree(dC_ref));

    return 0;
}
```

### Operating System

Arch Linux

### CPU

AMD Ryzen 5 1600 Six-Core Processor

### GPU

AMD Radeon RX 570 Series

### ROCm Version

ROCm 6.1.0

### ROCm Component

clr

### Steps to Reproduce

1. Compile a program with hipMemcpy using `hipcc`
```
	hipCheck(hipMemcpy(dA, A, sizeof(float) * max_size * max_size, hipMemcpyHostToDevice));
```
2. Execute the program

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 5 1600 Six-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 5 1600 Six-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3200
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            12
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    16322532(0xf90fe4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16322532(0xf90fe4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16322532(0xf90fe4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx803
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon RX 570 Series
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
  Chip ID:                 26591(0x67df)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1244
  BDFID:                   10496
  Internal Node ID:        1
  Compute Unit:            32
  SIMDs per CU:            4
  Shader Engines:          4
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        40(0x28)
  Max Work-item Per CU:    2560(0xa00)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 730
  SDMA engine uCode::      58
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    4194304(0x400000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    4194304(0x400000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx803
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — DarkMatter-999 (2024-12-23T12:21:41Z)

upon further exploration it turns out the HSA queue creation fails and that throws off memcpy

```
:3:hip_memory.cpp           :615 : 3396916408 us: [pid:65053 tid:0x7fffebfa3180]  hipMalloc ( 0x7fffffffe288, 4000000 )
:4:rocdevice.cpp            :2379: 3396916516 us: [pid:65053 tid:0x7fffebfa3180] Allocate hsa device memory 0x502400000, size 0x3d0900
:3:rocdevice.cpp            :2418: 3396916524 us: [pid:65053 tid:0x7fffebfa3180] Device=0x5555556a82c0, freeMem_ = 0xff48e500
:3:hip_memory.cpp           :617 : 3396916528 us: [pid:65053 tid:0x7fffebfa3180] hipMalloc: Returned hipSuccess : 0x502400000: duration: 120 us
:3:hip_memory.cpp           :690 : 3396923487 us: [pid:65053 tid:0x7fffebfa3180]  hipMemcpy ( 0x501400000, 0x7fffeb82f010, 4000000, hipMemcpyHostToDevice )
:3:rocdevice.cpp            :3026: 3396923501 us: [pid:65053 tid:0x7fffebfa3180] Number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:1:rocdevice.cpp            :3089: 3396952770 us: [pid:65053 tid:0x7fffebfa3180] Device::acquireQueue: hsa_queue_create failed!
:4:command.cpp              :347 : 3396952804 us: [pid:65053 tid:0x7fffebfa3180] Command (CopyHostToDevice) enqueued: 0x5555556b1520
```

---

### 评论 #2 — ppanchad-amd (2024-12-23T13:35:21Z)

Hi @DarkMatter-999. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #3 — jamesxu2 (2024-12-30T20:09:13Z)

Hi @DarkMatter-999, I don't see this happening on a gfx1100 (7900XT) device either, so its probably a codepath associated with gfx8 that hasn't been maintained since it got deprecated. I'll get a hold of a gfx8 device and assess this further.

Thanks for providing a clear reproducer!

---

### 评论 #4 — DarkMatter-999 (2024-12-31T04:58:00Z)

I also tried to install on Ubuntu 24.04 using the recommended [quick start instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html). It behaved exactly similarly there too leading to crash on `hipMemcpy`. However, after uninstalling the `amdgpu-dkms` package the ROCm stack starts to work as expected. So maybe there is some incompatibility between these.

---

### 评论 #5 — jamesxu2 (2025-01-02T21:24:34Z)

Hi @DarkMatter-999 thanks for that detail. It is surprising this works for you without the `amdgpu-dkms` package as that's an essential part of the stack. 

I do see the `hsa_queue_create` failing at a driver call (the amdgpu-dkms is the driver!) as it tries to create a new queue, but only on gfx8. I also note that this appears to be a driver regression because I don't see this issue with rocm 6.1 or rocm 6.2 (up to 6.2.4). It seems to only appear on ROCm >= 6.3.0 . Will keep you updated.
  

---

### 评论 #6 — IMbackK (2025-01-10T12:01:42Z)

> Hi @DarkMatter-999 thanks for that detail. It is surprising this works for you without the `amdgpu-dkms` package as that's an essential part of the stack.

Not really, as long KFD is not used amdgpu-dkms is not required. KFD is only required for p2p copies so if only one gpu is present or pcie p2p is disabled in kernel or not available due to hardware configuration mainline amdgpu will work fine.



---

### 评论 #7 — darren-amd (2025-05-07T19:17:16Z)

Hi @DarkMatter-999,

We have a patch that fixes the issue here: https://github.com/ROCm/ROCK-Kernel-Driver/commit/e29d35e1218d685623d52a1f5de62dc0d5c3c5f2 that landed in 6.4, thanks for reporting the issue!

---

### 评论 #8 — DarkMatter-999 (2025-05-22T13:55:10Z)

Thanks for the update. Glad to hear that. 🚀

---
