# [Issue]: Unable to generate random numbers from the GPU, although it is detected

> **Issue #3581**
> **状态**: closed
> **创建时间**: 2024-08-14T13:11:12Z
> **更新时间**: 2024-08-25T07:58:19Z
> **关闭时间**: 2024-08-14T17:50:24Z
> **作者**: mr-joshcrane
> **标签**: AMD Radeon RX 7900 XT, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3581

## 标签

- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description
Card: AMD Radeon RX 6800XT (gfx1030)

I've installed ROCm on WSL2, trying to get PyTorch to work, but when I try to talk to the GPU it always seems to hang indefinitely.

### Operating System
WSL - Windows Radeon Driver - 24.6.1
Subsystem - "Ubuntu" 22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 7 5700G with Radeon Graphics

### GPU

AMD Radeon RX 6800XT (gfx1030)

### ROCm Version

ROCm 6.1.3

### ROCm Component
ROCRand

### Steps to Reproduce

I've installed ROCm on WSL2, trying to get PyTorch to work, but when I try to talk to the GPU it always seems to hang indefinitely. Windows driver is 24.6.1

As far as I can tell, I've got PyTorch working, here is the output from  `python3 -m torch.utils.collect_env`

```
joshua@codex:~/code/gpustuff$ python3 -m torch.utils.collect_env
Collecting environment information...
PyTorch version: 2.1.2+rocm6.1.3
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.1.40093-bd86f1708

OS: Ubuntu 22.04.4 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.10.12 (main, Jul 29 2024, 16:56:48) [GCC 11.4.0] (64-bit runtime)
Python platform: Linux-5.15.153.1-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon RX 6800 XT
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.1.40093
MIOpen runtime version: 3.1.0
Is XNNPACK available: True
```

I even went so far as to write a C++ program to see if I could eliminate PyTorch from the equation (and I could!)

```main.cpp
#include <hip/hip_runtime.h>
#include <hiprand/hiprand.h>
#include <stdio.h>
#include <time.h>

int main() {
        int device_id;
        hipDeviceProp_t device_prop;
    
        hipGetDevice(&device_id);
        hipGetDeviceProperties(&device_prop, device_id);
    
        printf("Using device ID %d: %s\n", device_id, device_prop.name);
        printf("Total global memory: %zu MB\n", device_prop.totalGlobalMem / (1024 * 1024));
        printf("Shared memory per block: %zu KB\n", device_prop.sharedMemPerBlock / 1024);
        printf("Number of multiprocessors: %d\n", device_prop.multiProcessorCount);

        size_t n = 4;
        hipError_t err;
        hiprandStatus_t status;

        rocrand_generator gen;
        float *d_rand, *h_rand;

        h_rand = (float *)malloc(sizeof(float) * n);
        status = hiprandCreateGenerator(&gen, HIPRAND_RNG_PSEUDO_DEFAULT);
        if (status != HIPRAND_STATUS_SUCCESS) {
                printf("hitrandCreateGenerationFailed");
                return -1;
        }
        err = hipMalloc((void **)&d_rand, n  * sizeof(float));
        if (err != hipSuccess) {
                printf("hipMalloc failed: %s\n", hipGetErrorString(err));
                return -1;
        }
        status = hiprandSetPseudoRandomGeneratorSeed(gen, time(NULL));
        if (status != HIPRAND_STATUS_SUCCESS) {
                printf("seed fail");
                return -1;
        }

        // Program hangs here!
        status = hiprandGenerateNormal(gen, d_rand, n, 0.0f, 1.0f);
        if (status != HIPRAND_STATUS_SUCCESS) {
                printf("uniform fail");
                return -1;
        }

        err = hipMemcpy(h_rand, d_rand, n * sizeof(float), hipMemcpyDeviceToHost);
        if (err != hipSuccess) {
          printf("hipMemcpy failed: %s\n", hipGetErrorString(err));
          return -1;
        }
        for (int i = 0; i < n; i++) {
                printf("%f, ",  h_rand[i]);
        }
        printf("\n");
        hiprandDestroyGenerator(gen);
        hipFree(d_rand);

        return 0;
}
```

Compiles successfully, runs successfully, but hangs! It looks like its waiting for a futex to come back, but it never does.
You can see the strace output in additional information. It seems like it _wrote_ to /dev/random which is a bit unusual to me


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  ENABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    CPU
  Uuid:                    CPU-XX
  Marketing Name:          CPU
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
  Chip ID:                 0(0x0)
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16300380(0xf8b95c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16300380(0xf8b95c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1030
  Marketing Name:          AMD Radeon RX 6800 XT
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        16(0x10)
  Queue Min Size:          4096(0x1000)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L3:                      131072(0x20000) KB
  Chip ID:                 29631(0x73bf)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2065
  Internal Node ID:        1
  Compute Unit:            72
  SIMDs per CU:            2
  Shader Engines:          4
  Shader Arrs. per Eng.:   2
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 118
  SDMA engine uCode::      0
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16730340(0xff48e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1030
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
```

### Additional Information

strace output 
```
Using device ID 0: AMD Radeon RX 6800 XT
Total global memory: 16338 MB
Shared memory per block: 64 KB
Number of multiprocessors: 36

write(1, "Before hipMalloc\n", 17Before hipMalloc
)      = 17
write(1, "err: 0\n", 7err: 0
)                 = 7
write(1, "Before hiprandSetPseudoRandomGen"..., 43Before hiprandSetPseudoRandomGeneratorSeed
) = 43
write(1, "Status: 0\n", 10Status: 0
)             = 10
write(1, "Before hiprandGenerateUniform\n", 30Before hiprandGenerateUniform
) = 30
mmap(NULL, 2646016, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f15aa210000
mmap(NULL, 2646016, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f15a9f8a000
munmap(0x7f15aa210000, 2646016)         = 0
brk(0x55f1bf147000)                     = 0x55f1bf147000
brk(0x55f1bf195000)                     = 0x55f1bf195000
brk(0x55f1bf36e000)                     = 0x55f1bf36e000
brk(0x55f1bf41a000)                     = 0x55f1bf41a000
brk(0x55f1bf5f3000)                     = 0x55f1bf5f3000
brk(0x55f1bf641000)                     = 0x55f1bf641000
munmap(0x7f15a9f8a000, 2646016)         = 0
getpid()                                = 55558
brk(0x55f1bf8c6000)                     = 0x55f1bf8c6000
brk(0x55f1bfb4b000)                     = 0x55f1bfb4b000
brk(0x55f1bf641000)                     = 0x55f1bf641000
brk(0x55f1bf8c6000)                     = 0x55f1bf8c6000
openat(AT_FDCWD, "/dev/random", O_WRONLY) = 6
write(6, "\20", 1)                      = 1
close(6)                                = 0
openat(AT_FDCWD, "/dev/random", O_WRONLY) = 6
write(6, "\20", 1)                      = 1
close(6)                                = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x6, 0x48), 0x7ffdee7d06b0) = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0xc, 0x68), 0x7ffdee7d0690) = 259
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0xb, 0x30), 0x7ffdee7d06f0) = 259
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x3a, 0x28), 0x7ffdee7d0820) = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x8, 0x48), 0x7ffdee7d0820) = 0
mmap(0x7efd6c420000, 2584576, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS|MAP_NORESERVE|1<<MAP_HUGE_SHIFT, -1, 0) = 0x7efd6c420000
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x6, 0x48), 0x7ffdee7d06b0) = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0xc, 0x68), 0x7ffdee7d0690) = 259
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0xb, 0x30), 0x7ffdee7d06f0) = 259
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x3a, 0x28), 0x7ffdee7d0820) = 0
futex(0x55f1befdc318, FUTEX_WAKE_PRIVATE, 1) = 1
clock_nanosleep(CLOCK_REALTIME, 0, {tv_sec=0, tv_nsec=20000}, 0x7ffdee7d1380) = 0
clock_nanosleep(CLOCK_REALTIME, 0, {tv_sec=0, tv_nsec=20000}, 0x7ffdee7d1380) = 0
clock_nanosleep(CLOCK_REALTIME, 0, {tv_sec=0, tv_nsec=20000}, 0x7ffdee7d1380) = 0
```


---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-08-14T17:50:24Z)

Hi @mr-joshcrane, the AMD Radeon RX 6800XT is not supported for usage through WSL. The supported hardware list can be found at [Compatibility Matrices (WSL)](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#compatibility-matrices-wsl). It is expected that the 6800XT will be recognized when running `rocminfo` but will encounter hangs when executing programs.

I was, however, able to reproduce your issue on a supported configuration with a 7900XT. The symptoms of the failure closely resemble the issue currently under investigation at https://github.com/ROCm/ROCm/issues/3470. We can continue to reference this ongoing case as we explore these hang issues.

---

### 评论 #2 — schung-amd (2024-08-21T14:24:50Z)

Hi @mr-joshcrane, are you still experiencing this issue? We're collecting system information of users who are affected by similar hangs in WSL. It would be helpful if you could provide the following:

- Windows build
- Motherboard model, BIOS version/date and SMBIOS version (viewable in msinfo32)
- PCI bus/device/function of the GPU (viewable in Device Manager)
- PCIe version, lanes, which PCIe slot the GPU is plugged into (i.e. top or lower)

On our repro these hangs are caused by missing PCIe atomics support which is difficult to check for and set on Windows, so we'd like to figure out if there's something in common with the systems that we're seeing these hangs on. Thanks!


---

### 评论 #3 — mr-joshcrane (2024-08-25T06:27:18Z)

Windows Build: 
OS Name	Microsoft Windows 11 Pro
Version	10.0.22631 Build 22631

Motherboard:
BaseBoard Manufacturer	Gigabyte Technology Co., Ltd.
BaseBoard Product	X570S GAMING X
BIOS Version/Date	American Megatrends International, LLC. F3, 4/01/2022
SMBIOS Version	3.3

PCI bus 3, device 0, function 0
PCIe 4.0/3.0 x4 NVMe support

Interestingly, I ZGPU tells me my GPU is running at 3.0 PCI x16 rather than the supported 4.0 x16



---

### 评论 #4 — mr-joshcrane (2024-08-25T07:58:19Z)

I went on a bit of a rabbit hole trying to update my BIOS and also try and force my PCIe card to operate in 4.0 mode. Sadly I couldnt get it to work :\

---
