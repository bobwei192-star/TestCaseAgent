# [Issue]: gfx1201 (RDNA4) rejected by HIP runtime — "has 2 ISAs but can only support a single ISA"

> **Issue #6110**
> **状态**: closed
> **创建时间**: 2026-04-02T18:04:28Z
> **更新时间**: 2026-04-13T21:13:28Z
> **关闭时间**: 2026-04-13T21:13:28Z
> **作者**: mkoker
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6110

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem

HIP runtime fails to initialize on gfx1201 (RDNA4) GPUs. `hsa_agent_iterate_isas` returns two ISAs (`amdgcn-amd-amdhsa--gfx1201` and `amdgcn-amd-amdhsa--gfx12-generic`) but `rocdevice.cpp` rejects devices with more than one ISA.

### Reproduction

Any HIP program compiled for gfx1201:

```bash
hipcc test.hip -o test --offload-arch=gfx1201
AMD_LOG_LEVEL=3 ./test
```

Output:
```
rocdevice.cpp:442 : Initializing HSA stack.
rocdevice.cpp:590 : HSA device gfx1201 (PCI ID 7551) has 2 ISAs but can only support a single ISA
rocdevice.cpp:506 : Error creating new instance of Device.
free(): invalid pointer
```

### Root Cause

`rocdevice.cpp` around line 590 checks the ISA count returned by `hsa_agent_iterate_isas`. gfx1201 reports both `gfx1201` (specific) and `gfx12-generic`, but the code expects exactly one ISA per device.

The ISA table in `device.cpp:261` correctly has gfx1201 with `runtimeRocSupported = true`, but the device never reaches this lookup because it's rejected by the ISA count check.

### Workaround

LD_PRELOAD shim that intercepts `hsa_agent_iterate_isas` and filters out `gfx12-generic`:

```c
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>
#include <string.h>

typedef enum { HSA_STATUS_OK = 0 } hsa_status_t;
typedef struct { uint64_t handle; } hsa_agent_t;
typedef struct { uint64_t handle; } hsa_isa_t;
typedef hsa_status_t (*hsa_isa_callback_t)(hsa_isa_t isa, void *data);
typedef hsa_status_t (*iterate_isas_fn)(hsa_agent_t, hsa_isa_callback_t, void *);
typedef enum { HSA_ISA_INFO_NAME = 1 } hsa_isa_info_t;
typedef hsa_status_t (*isa_get_info_fn)(hsa_isa_t, hsa_isa_info_t, void *);

struct state { hsa_isa_callback_t cb; void *data; };

static hsa_status_t filter_cb(hsa_isa_t isa, void *data) {
    struct state *s = data;
    char name[256] = {0};
    static isa_get_info_fn gi = NULL;
    if (!gi) gi = (isa_get_info_fn)dlsym(RTLD_NEXT, "hsa_isa_get_info_alt");
    if (gi) gi(isa, HSA_ISA_INFO_NAME, name);
    if (strstr(name, "gfx1201")) return s->cb(isa, s->data);
    return HSA_STATUS_OK;
}

hsa_status_t hsa_agent_iterate_isas(hsa_agent_t agent, hsa_isa_callback_t cb, void *data) {
    static iterate_isas_fn real = NULL;
    if (!real) real = (iterate_isas_fn)dlsym(RTLD_NEXT, "hsa_agent_iterate_isas");
    struct state s = { .cb = cb, .data = data };
    return real(agent, filter_cb, &s);
}
```

```bash
gcc -shared -fPIC -o isa_filter.so isa_filter.c -ldl
LD_PRELOAD=./isa_filter.so ./your_hip_program
```

With the shim, gfx1201 initializes correctly and HIP compute works.

### Expected Fix

`rocdevice.cpp` should accept devices with multiple ISAs and use the most specific one (gfx1201 over gfx12-generic).

### Environment

- **GPU:** AMD Radeon AI PRO R9700 (gfx1201, RDNA4)
- **ROCm:** 7.2.0 and 7.2.1
- **OS:** Ubuntu 24.04, kernel 6.17.0
- **Impact:** Blocks all HIP compute on RDNA4 GPUs (RX 9070, 9060, R9700)

---

## 评论 (3 条)

### 评论 #1 — zichguan-amd (2026-04-08T19:34:20Z)

Hi @mkoker, can you provide a repro script? I'm not able to repro the issue on ubuntu 24.04 with ROCm 7.2.1.
```
$ hipcc test.hip -o test --offload-arch=gfx1201
test.hip:13:5: warning: ignoring return value of type 'hipError_t' declared with 'nodiscard' attribute [-Wunused-value]
   13 |     hipFree(d);
      |     ^~~~~~~~~~
1 warning generated when compiling for gfx1201.
test.hip:13:5: warning: ignoring return value of type 'hipError_t' declared with 'nodiscard' attribute [-Wunused-value]
   13 |     hipFree(d);
      |     ^~~~~~~~~~
1 warning generated when compiling for host.
$ AMD_LOG_LEVEL=3 ./test
:3:rocdevice.cpp            :415 : 13991775928 us:  Initalizing runtime stack, Enumerated GPU agents = 1
:3:rocdevice.cpp            :182 : 13991775966 us:  Numa selects cpu agent[0]=0x2bc60220(fine=0x2bc60440,coarse=0x2bc60d50) for gpu agent=0x2bc614c0 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :269 : 13991775973 us:  Using dev kernel arg wa = 0
:3:comgrctx.cpp             :126 : 13991778527 us:  Loaded COMGR library version 3.0.
:3:rocdevice.cpp            :1565: 13991778787 us:  addressableNumVGPRs=256, totalNumVGPRs=1536, vGPRAllocGranule=24, availableRegistersPerCU_=196608
:3:rocdevice.cpp            :1579: 13991778799 us:  imageSupport=1
:3:rocdevice.cpp            :1610: 13991778802 us:  Gfx Major/Minor/Stepping: 12/0/1
:3:rocdevice.cpp            :1612: 13991778803 us:  HMM support: 1, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1614: 13991778804 us:  Max SDMA Read Mask: 0x3, Max SDMA Write Mask: 0x3
:3:hip_context.cpp          :60  : 13991779591 us:  HIP Version: 7.2.53211.e1a6bc5663, Direct Dispatch: 1
:3:os_posix.cpp             :934 : 13991779600 us:  HIP Library Path: /opt/rocm-7.2.1/lib/libamdhip64.so.7
:3:hip_memory.cpp           :779 : 13991779629 us:   hipMalloc ( 0x7ffea9dd8e38, 4 )
:3:rocdevice.cpp            :2225: 13991779798 us:  Device=0x2bcc59d0, freeMem_ = 0x3fafffffc
:3:hip_memory.cpp           :781 : 13991779804 us:  hipMalloc: Returned hipSuccess : 0x7044f8200000: duration: 175 us
:3:hip_memory.cpp           :795 : 13991779810 us:   hipFree ( 0x7044f8200000 )
:3:rocdevice.cpp            :2225: 13991779823 us:  Device=0x2bcc59d0, freeMem_ = 0x3fb000000
:3:hip_memory.cpp           :797 : 13991779829 us:  hipFree: Returned hipSuccess :
HIP_OK
:1:rocdevice.cpp            :3339: 13991780601 us:  Unknown Event Type
$ cat test.hip
// Minimal HIP program: triggers device init (hipMalloc).
#include <hip/hip_runtime.h>
#include <cstdio>
#include <cstdlib>

int main() {
    void* d = nullptr;
    hipError_t err = hipMalloc(&d, sizeof(int));
    if (err != hipSuccess) {
        std::fprintf(stderr, "hipMalloc failed: %s\n", hipGetErrorString(err));
        return 1;
    }
    hipFree(d);
    std::puts("HIP_OK");
    return 0;
}
```

There's also no logging related to 
```
rocdevice.cpp:442 : Initializing HSA stack.
rocdevice.cpp:590 : HSA device gfx1201 (PCI ID 7551) has 2 ISAs but can only support a single ISA
rocdevice.cpp:506 : Error creating new instance of Device.
```
in 7.2.0 and 7.2.1 source code. They are really old code from ROCm 6.x, see https://github.com/ROCm/clr/commit/3387f48b5. Can you perform a clean install and try again?

---

### 评论 #2 — mkoker (2026-04-12T22:41:10Z)

@zichguan-amd I can reproduce this consistently. Here's the full repro:

```bash
$ cat test.hip
#include <hip/hip_runtime.h>
#include <cstdio>

__global__ void kernel(int *out) {
    out[threadIdx.x] = threadIdx.x;
}

int main() {
    int *d;
    hipMalloc(&d, 64 * sizeof(int));
    kernel<<<1, 64>>>(d);
    hipError_t err = hipDeviceSynchronize();
    if (err != hipSuccess) {
        printf("Error: %s\n", hipGetErrorString(err));
        return 1;
    }
    int h[64];
    hipMemcpy(h, d, 64 * sizeof(int), hipMemcpyDeviceToHost);
    printf("h[0]=%d h[63]=%d\n", h[0], h[63]);
    hipFree(d);
    return 0;
}

$ /opt/rocm/bin/hipcc test.hip -o test --offload-arch=gfx1201
# compiles with warnings only

$ AMD_LOG_LEVEL=4 ./test
:3:rocdevice.cpp            :442 : ... Initializing HSA stack.
:1:rocdevice.cpp            :590 : ... HSA device gfx1201 (PCI ID 7551) has 2 ISAs but can only support a single ISA
:1:rocdevice.cpp            :506 : ... Error creating new instance of Device.
free(): invalid pointer
Aborted (core dumped)
```

The binary only contains one ISA:
```
$ /opt/rocm/bin/roc-obj-ls test
1       host-x86_64-unknown-linux-gnu-       file:///tmp/test#offset=8192&size=0
1       hipv4-amdgcn-amd-amdhsa--gfx1201     file:///tmp/test#offset=8192&size=4080
```

So the binary is fine — the rejection is coming from the HIP runtime's device initialization in `rocdevice.cpp:590`. The runtime sees 2 ISAs reported by the HSA loader for the gfx1201 device and bails out.

Environment:
- Ubuntu 24.04.4 LTS
- ROCm 7.2.1 (`/opt/rocm-7.2.1`)
- AMD Radeon AI PRO R9700 (gfx1201, RDNA4)
- Also have the Ubuntu-packaged `libamdhip64-dev` 5.7.1 installed (see #6111), though that shouldn't affect runtime behavior
- `rocminfo` sees the device fine and reports `gfx1201`
- Our workaround is an LD_PRELOAD ISA filter shim that intercepts `hsa_agent_iterate_isas` and only returns the first ISA

Any idea what the second ISA is? Could it be a generic fallback ISA that the HSA loader is exposing for gfx1201?


---

### 评论 #3 — mkoker (2026-04-12T22:51:37Z)

Update: removing the Ubuntu-packaged `libamdhip64-dev` (5.7.1) and related stale packages (`libhsa-runtime-dev`, `libhsa-runtime64-1`, `libhsakmt1`, etc.) fixed this issue as well.

The "2 ISAs" rejection was coming from the old Ubuntu-packaged `libhsa-runtime64-1` (5.7.1) being loaded at runtime instead of the ROCm 7.2.1 one. After removal:

```
$ /opt/rocm/bin/hipcc test.hip -o test --offload-arch=gfx1201 && ./test
h[0]=0 h[63]=63
```

Kernel compiles and runs correctly on gfx1201. No ISA filter shim needed.

So all three issues (#6110, #6111, #6112) were caused by the same thing — Ubuntu's `rocm-hipamd` / `libamdhip64-dev` 5.7.1 packages conflicting with the AMD-repo ROCm 7.2.1 install. The stale packages put old headers in `/usr/include/hip/` and old shared libs that shadow the real ones.

Feel free to close this — the fix is just removing the Ubuntu-packaged ROCm packages when using the AMD repo install. Might be worth adding a note to the ROCm install docs about this conflict though.


---
