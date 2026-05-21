# `hipMemcpy` from device to host stuck on device 1

> **Issue #2418**
> **状态**: closed
> **创建时间**: 2023-08-29T21:49:58Z
> **更新时间**: 2023-09-04T15:39:44Z
> **关闭时间**: 2023-09-04T15:39:44Z
> **作者**: MasterJH5574
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2418

## 描述

## Description

Our workstation has two Radeon RX 7900 XTX cards. Today we tried the following code stuck on the `hipMemcpy` line at the end.

```c++
#include <hip/hip_runtime.h>

#include <cstdlib>
#include <iostream>
#include <vector>

constexpr int error_exit_code = -1;

/// \brief Checks if the provided error code is \p hipSuccess and if not,
/// prints an error message to the standard error output and terminates the program
/// with an error code.
#define HIP_CHECK(condition)                                                                \
    {                                                                                       \
        const hipError_t error = condition;                                                 \
        if(error != hipSuccess)                                                             \
        {                                                                                   \
            std::cerr << "An error encountered: \"" << hipGetErrorString(error) << "\" at " \
                      << __FILE__ << ':' << __LINE__ << std::endl;                          \
            std::exit(error_exit_code);                                                     \
        }                                                                                   \
    }

int main(const int argc, const char** argv)
{
    int                dev_id = 1;      // <==== use device id 1
    float*             d_a{};
    std::vector<float> h_a(10);
    HIP_CHECK(hipSetDevice(dev_id));

    HIP_CHECK(hipMalloc(&d_a, 10 * sizeof(float)));

    std::cout << "start to copy from device to host\n";
    HIP_CHECK(hipMemcpy(h_a.data(), d_a, sizeof(float) * 10, hipMemcpyDeviceToHost));    //  <==== stuck here
    std::cout << "finish copying from device to host\n";
    return 0;
}
```

The code simply allocates memory on GPU 1, and copies the memory content back to host, and it gets stuck on `hipMemcpy`.

NOTE: If we use GPU 0 by setting `dev_id` to 0, the code works perfectly and does not get stuck on `hipMemcpy`. **It only gets stuck for GPU 1.** Using env variable `ROCR_VISIBLE_DEVICES=1` and make `dev_id = 0` does not resolve the issue.

We further test the official matrix multiplication examples at https://github.com/amd/rocm-examples/blob/develop/HIP-Basic/matrix_multiplication/main.hip. If we don’t change anything, the program happen for GPU 0 and work smoothly. When we change to use GPU 1 by either `hipSetDevice(1)` or `ROCR_VISIBLE_DEVICES=1`, the program gets stuck. So we suppose there might be some internal issue of ROCm when it comes with multiple GPUs.

------

## Workstation Environment

* CPU: AMD Ryzen 9 7950X
* GPU: 2 x AMD Radeon RX 7900 XTX
* OS: Ubuntu 22.04
* ROCm Driver: ROCm 5.6 (installed following https://docs.amd.com/en/docs-5.6.0/deploy/linux/installer/install.html)

---

## 评论 (15 条)

### 评论 #1 — MasterJH5574 (2023-08-30T00:04:11Z)

To add up a bit,
* `rocm-smi` can find both GPU 0 and GPU 1,
* Vulkan works for both GPU 0 and GPU 1,
so we suppose it is not the matter of GPU 1 not being installed properly.

---

### 评论 #2 — MasterJH5574 (2023-08-30T00:11:24Z)

Furthermore, `hipMemcpyHostToDevice` for GPU 1 is also broken (hanging forever).

---

### 评论 #3 — langyuxf (2023-08-30T02:47:40Z)

Can you use AMD_LOG_LEVEL=5 to run your test, then put the log and full dmesg here? 

You can also use HSA_ENABLE_SDMA=0 to see if it works.


---

### 评论 #4 — briansp2020 (2023-08-30T04:08:05Z)

What motherboard are you using? Do both PCIe slots support PCIe atomic? I think ROCm still requires PCIe atomic support and many motherboards do not support it in their second PCIe slot. 

---

### 评论 #5 — MasterJH5574 (2023-08-30T04:13:08Z)

> Can you use AMD_LOG_LEVEL=5 to run your test, then put the log and full dmesg here?
> 
> You can also use HSA_ENABLE_SDMA=0 to see if it works.

@xfyucg `HSA_ENABLE_SDMA=0` doesn’t work. And below is the log with `AMD_LOG_LEVEL=5` when running the code above:

```
:3:rocdevice.cpp            :434 : 99441719306 us: 350457: [tid:0x7f02e57efc00] Initializing HSA stack.
:3:comgrctx.cpp             :33  : 99442498221 us: 350457: [tid:0x7f02e57efc00] Loading COMGR library.
:3:rocdevice.cpp            :200 : 99442498253 us: 350457: [tid:0x7f02e57efc00] Numa selects cpu agent[0]=0xf53d20(fine=0xcd46d0,coarse=0xf56510) for gpu agent=0xf64ea0
:3:rocdevice.cpp            :1634: 99442498491 us: 350457: [tid:0x7f02e57efc00] HMM support: 1, xnack: 0, direct host access: 0

:4:rocdevice.cpp            :2012: 99442498670 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f0145400000, size 0x101000
:4:rocdevice.cpp            :2012: 99442498894 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f0145200000, size 0x101000
:3:rocdevice.cpp            :200 : 99442498950 us: 350457: [tid:0x7f02e57efc00] Numa selects cpu agent[0]=0xf53d20(fine=0xcd46d0,coarse=0xf56510) for gpu agent=0xf69340
:3:rocdevice.cpp            :1634: 99442499018 us: 350457: [tid:0x7f02e57efc00] HMM support: 1, xnack: 0, direct host access: 0

:4:rocdevice.cpp            :2012: 99442499192 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f0145000000, size 0x101000
:4:rocdevice.cpp            :2012: 99442499394 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f0144e00000, size 0x101000
:3:rocdevice.cpp            :200 : 99442499446 us: 350457: [tid:0x7f02e57efc00] Numa selects cpu agent[0]=0xf53d20(fine=0xcd46d0,coarse=0xf56510) for gpu agent=0xf6d320
:3:rocdevice.cpp            :1634: 99442499507 us: 350457: [tid:0x7f02e57efc00] HMM support: 1, xnack: 0, direct host access: 0

:4:rocdevice.cpp            :2012: 99442499532 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f02e57e9000, size 0xa8
:4:rocdevice.cpp            :2012: 99442499721 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f0144c00000, size 0x101000
:4:rocdevice.cpp            :2012: 99442499925 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f0144a00000, size 0x101000
:4:runtime.cpp              :83  : 99442499970 us: 350457: [tid:0x7f02e57efc00] init
:3:hip_context.cpp          :48  : 99442499973 us: 350457: [tid:0x7f02e57efc00] Direct Dispatch: 1
:1:hip_code_object.cpp      :505 : 99442499995 us: 350457: [tid:0x7f02e57efc00] hipErrorNoBinaryForGpu: Unable to find code object for all current devices!
:1:hip_code_object.cpp      :507 : 99442499997 us: 350457: [tid:0x7f02e57efc00]   Devices:
:1:hip_code_object.cpp      :509 : 99442499998 us: 350457: [tid:0x7f02e57efc00]     amdgcn-amd-amdhsa--gfx1100 - [Found]
:1:hip_code_object.cpp      :509 : 99442499999 us: 350457: [tid:0x7f02e57efc00]     amdgcn-amd-amdhsa--gfx1100 - [Found]
:1:hip_code_object.cpp      :509 : 99442500001 us: 350457: [tid:0x7f02e57efc00]     amdgcn-amd-amdhsa--gfx1036 - [Not Found]
:1:hip_code_object.cpp      :514 : 99442500003 us: 350457: [tid:0x7f02e57efc00]   Bundled Code Objects:
:1:hip_code_object.cpp      :530 : 99442500004 us: 350457: [tid:0x7f02e57efc00]     host-x86_64-unknown-linux - [Unsupported]
:1:hip_code_object.cpp      :527 : 99442500006 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1010 - [code object targetID is amdgcn-amd-amdhsa--gfx1010]
:1:hip_code_object.cpp      :527 : 99442500009 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1030 - [code object targetID is amdgcn-amd-amdhsa--gfx1030]
:1:hip_code_object.cpp      :527 : 99442500011 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1100 - [code object targetID is amdgcn-amd-amdhsa--gfx1100]
:1:hip_code_object.cpp      :527 : 99442500012 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1101 - [code object targetID is amdgcn-amd-amdhsa--gfx1101]
:1:hip_code_object.cpp      :527 : 99442500015 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1102 - [code object targetID is amdgcn-amd-amdhsa--gfx1102]
:1:hip_code_object.cpp      :527 : 99442500017 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx803 - [code object targetID is amdgcn-amd-amdhsa--gfx803]
:1:hip_code_object.cpp      :527 : 99442500019 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx900 - [code object targetID is amdgcn-amd-amdhsa--gfx900]
:1:hip_code_object.cpp      :527 : 99442500020 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx906:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx906:xnack-]
:1:hip_code_object.cpp      :527 : 99442500022 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx908:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx908:xnack-]
:1:hip_code_object.cpp      :527 : 99442500023 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack+]
:1:hip_code_object.cpp      :527 : 99442500026 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack-]
:1:hip_code_object.cpp      :534 : 99442500027 us: 350457: [tid:0x7f02e57efc00] hipErrorNoBinaryForGpu: Unable to find code object for all current devices! - 209
:1:hip_fatbin.cpp           :265 : 99442500029 us: 350457: [tid:0x7f02e57efc00] hipErrorNoBinaryForGpu: Couldn't find binary for current devices! - 209
:3:hip_platform.cpp         :670 : 99442500035 us: 350457: [tid:0x7f02e57efc00] init: Returned hipErrorNoBinaryForGpu : 
:3:hip_device_runtime.cpp   :565 : 99442500042 us: 350457: [tid:0x7f02e57efc00] hipSetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :562 : 99442500051 us: 350457: [tid:0x7f02e57efc00]  hipMalloc ( 0x7ffdc3cfa710, 40 ) 
:4:rocdevice.cpp            :2141: 99442500072 us: 350457: [tid:0x7f02e57efc00] Allocate hsa device memory 0x7f0144600000, size 0x28
:3:rocdevice.cpp            :2180: 99442500074 us: 350457: [tid:0x7f02e57efc00] device=0xf7aab0, freeMem_ = 0x5feffffd8
:3:hip_memory.cpp           :564 : 99442500076 us: 350457: [tid:0x7f02e57efc00] hipMalloc: Returned hipSuccess : 0x7f0144600000: duration: 25 us
start to copy from device to host
:3:hip_memory.cpp           :637 : 99442500087 us: 350457: [tid:0x7f02e57efc00]  hipMemcpy ( 0xdc2150, 0x7f0144600000, 40, hipMemcpyDeviceToHost ) 
:3:rocdevice.cpp            :2818: 99442500092 us: 350457: [tid:0x7f02e57efc00] number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:3:rocdevice.cpp            :2896: 99442506769 us: 350457: [tid:0x7f02e57efc00] created hardware queue 0x7f02e57cc000 with size 16384 with priority 1, cooperative: 0
:3:rocdevice.cpp            :2963: 99442506774 us: 350457: [tid:0x7f02e57efc00] acquireQueue refCount: 0x7f02e57cc000 (1)

:4:rocdevice.cpp            :2012: 99442506952 us: 350457: [tid:0x7f02e57efc00] Allocate hsa host memory 0x7f0144200000, size 0x100000
:3:devprogram.cpp           :2684: 99442607884 us: 350457: [tid:0x7f02e57efc00] Using Code Object V5.
(STUCK HERE)
```

---

### 评论 #6 — MasterJH5574 (2023-08-30T04:16:11Z)

> What motherboard are you using? Do both PCIe slots support PCIe atomic? I think ROCm still requires PCIe atomic support and many motherboards do not support it in their second PCIe slot.

@briansp2020 The motherboard we are using is ROG X670E-E https://rog.asus.com/motherboards/rog-strix/rog-strix-x670e-e-gaming-wifi-model/. I don’t know if the second PCIe slot has the atomic support. If it is mentioned in the motherboard manual, I can look it up tomorrow.

Update: the word “atomic” does not appear in the manual https://dlcdnets.asus.com/pub/ASUS/mb/Socket%20AM5/ROG_STRIX_X670E-E_GAMING_WIFI/E21210_ROG_STRIX_X670E-E_GAMING_WIFI_UM_V3_WEB.pdf?model=ROG%20STRIX%20X670E-E%20GAMING%20WIFI.

---

### 评论 #7 — briansp2020 (2023-08-30T04:50:47Z)

Are your GPUs both plugged into the PCIe5 slots (slots with metal outline)? If so, they should both support PCIe atomic since they are coming directly out of CPU. If the second GPU is plugged into the bottom PCIe slot with plastic connector, you may want to try plugging it in the other slot and see if that helps.

---

### 评论 #8 — MasterJH5574 (2023-08-30T14:17:43Z)

> Are your GPUs both plugged into the PCIe5 slots (slots with metal outline)? If so, they should both support PCIe atomic since they are coming directly out of CPU. If the second GPU is plugged into the bottom PCIe slot with plastic connector, you may want to try plugging it in the other slot and see if that helps.

@briansp2020 Yes by reading the manual I think both GPUs are in the PCIe5 slots with metal outline (the top 2 in the photo below). The difference is that GPU 0 runs with x8 and GPU 1 runs with x4, but both are indeed PCIe5 (we don’t have M.2 SSD).

<img width="70%" alt="image" src="https://github.com/RadeonOpenCompute/ROCm/assets/45167100/ce3f4d65-7446-45fb-9dcf-7b912b144e70">

<img width="70%" alt="image" src="https://github.com/RadeonOpenCompute/ROCm/assets/45167100/74ae5f97-6f09-4658-bde5-7dda2a873ee5">

---

### 评论 #9 — briansp2020 (2023-08-30T14:43:23Z)

Then, I don't have any more ideas. If you have access to a professional platform with more PCIe lanes (ThreadRipper/EPYC/Xeon/etc), you might try them and see if you still have the same issue. But that's just me taking a shot in the dark...

---

### 评论 #10 — MasterJH5574 (2023-08-30T17:45:22Z)

@briansp2020 Thanks for the suggestions and help. Though it's a bit hard to get that and try :-(

---

### 评论 #11 — langyuxf (2023-08-31T02:59:00Z)


1. Actually there are 3 GPUs in your system, gfx1100, gfx1100, gfx1036. 
Following log shows that the executable doesn't contain code object for gfx1036.
How do you build your test?

```
:1:hip_code_object.cpp      :505 : 99442499995 us: 350457: [tid:0x7f02e57efc00] hipErrorNoBinaryForGpu: Unable to find code object for all current devices!
:1:hip_code_object.cpp      :507 : 99442499997 us: 350457: [tid:0x7f02e57efc00]   Devices:
:1:hip_code_object.cpp      :509 : 99442499998 us: 350457: [tid:0x7f02e57efc00]     amdgcn-amd-amdhsa--gfx1100 - [Found]
:1:hip_code_object.cpp      :509 : 99442499999 us: 350457: [tid:0x7f02e57efc00]     amdgcn-amd-amdhsa--gfx1100 - [Found]
:1:hip_code_object.cpp      :509 : 99442500001 us: 350457: [tid:0x7f02e57efc00]     amdgcn-amd-amdhsa--gfx1036 - [Not Found]
:1:hip_code_object.cpp      :514 : 99442500003 us: 350457: [tid:0x7f02e57efc00]   Bundled Code Objects:
:1:hip_code_object.cpp      :530 : 99442500004 us: 350457: [tid:0x7f02e57efc00]     host-x86_64-unknown-linux - [Unsupported]
:1:hip_code_object.cpp      :527 : 99442500006 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1010 - [code object targetID is amdgcn-amd-amdhsa--gfx1010]
:1:hip_code_object.cpp      :527 : 99442500009 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1030 - [code object targetID is amdgcn-amd-amdhsa--gfx1030]
:1:hip_code_object.cpp      :527 : 99442500011 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1100 - [code object targetID is amdgcn-amd-amdhsa--gfx1100]
:1:hip_code_object.cpp      :527 : 99442500012 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1101 - [code object targetID is amdgcn-amd-amdhsa--gfx1101]
:1:hip_code_object.cpp      :527 : 99442500015 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx1102 - [code object targetID is amdgcn-amd-amdhsa--gfx1102]
:1:hip_code_object.cpp      :527 : 99442500017 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx803 - [code object targetID is amdgcn-amd-amdhsa--gfx803]
:1:hip_code_object.cpp      :527 : 99442500019 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx900 - [code object targetID is amdgcn-amd-amdhsa--gfx900]
:1:hip_code_object.cpp      :527 : 99442500020 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx906:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx906:xnack-]
:1:hip_code_object.cpp      :527 : 99442500022 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx908:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx908:xnack-]
:1:hip_code_object.cpp      :527 : 99442500023 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack+]
:1:hip_code_object.cpp      :527 : 99442500026 us: 350457: [tid:0x7f02e57efc00]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack-]
:1:hip_code_object.cpp      :534 : 99442500027 us: 350457: [tid:0x7f02e57efc00] hipErrorNoBinaryForGpu: Unable to find code object for all current devices! - 209
:1:hip_fatbin.cpp           :265 : 99442500029 us: 350457: [tid:0x7f02e57efc00] hipErrorNoBinaryForGpu: Couldn't find binary for current devices! - 209
:3:hip_platform.cpp         :670 : 99442500035 us: 350457: [tid:0x7f02e57efc00] init: Returned hipErrorNoBinaryForGpu :  
```
2. It seems stuck when copying code object from host to device. 
You can try to disable power feature when loading amdgpu driver, then run your test.

```
$ sudo vim /etc/default/grub
add "amdgpu.ppfeaturemask=0xffff3fff amdgpu.runpm=0x0" into GRUB_CMDLINE_LINUX_DEFAULT
$ sudo update-grub
$ reboot
$ cat /proc/cmdline
see if the modification takes effect

```

---

### 评论 #12 — MasterJH5574 (2023-08-31T19:19:21Z)

> 1. Actually there are 3 GPUs in your system, gfx1100, gfx1100, gfx1036.
> Following log shows that the executable doesn't contain code object for gfx1036.
> How do you build your test?

@xfyucg Thanks. Yes the gfx1036 one is the integrated GPU, as our CPU is AMD Ryzen 9 7950X.

The way we built the test is use the `CMakeLists.txt` under the official ROCm example repo https://github.com/amd/rocm-examples/tree/develop/HIP-Basic/matrix_multiplication. Specifically, we replace the content of `main.hip` with the code above, and run `cmake .` and `make` to build the test. I don’t know if it is normal that no code object for gfx1036 is found in this case.

---

### 评论 #13 — MasterJH5574 (2023-08-31T19:34:59Z)

> 2. It seems stuck when copying code object from host to device.
>     You can try to disable power feature when loading amdgpu driver, then run your test.
> 
> ```
> $ sudo vim /etc/default/grub
> add "amdgpu.ppfeaturemask=0xffff3fff amdgpu.runpm=0x0" into GRUB_CMDLINE_LINUX_DEFAULT
> $ sudo update-grub
> $ reboot
> $ cat /proc/cmdline
> see if the modification takes effect
> ```

It works!!! Thank you @xfyucg, I appreciate it so much. Now no stuck happens again for GPU 0 and 1.

I’m also curious about how the “power feature” can affect this? Would you mind sharing a bit more about the reason behind?

---

### 评论 #14 — langyuxf (2023-09-01T09:02:45Z)

> > 2. It seems stuck when copying code object from host to device.
> >    You can try to disable power feature when loading amdgpu driver, then run your test.
> > 
> > ```
> > $ sudo vim /etc/default/grub
> > add "amdgpu.ppfeaturemask=0xffff3fff amdgpu.runpm=0x0" into GRUB_CMDLINE_LINUX_DEFAULT
> > $ sudo update-grub
> > $ reboot
> > $ cat /proc/cmdline
> > see if the modification takes effect
> > ```
> 
> It works!!! Thank you @xfyucg, I appreciate it so much. Now no stuck happens again for GPU 0 and 1.
> 
> I’m also curious about how the “power feature” can affect this? Would you mind sharing a bit more about the reason behind?

Simply speaking, to save power, GPU will enter a sleeping state when it is idle and wake up when there is work need to do.
That is a collaboration of driver, firmware and hardware. In your case, GPU 1 doesn't wake up as expected to process copy work.
See https://lpc.events/event/9/contributions/633/ for more details.


---

### 评论 #15 — MasterJH5574 (2023-09-04T15:39:41Z)

@xfyucg Thanks for sharing the knowledge! I appreciate it :-)

---
