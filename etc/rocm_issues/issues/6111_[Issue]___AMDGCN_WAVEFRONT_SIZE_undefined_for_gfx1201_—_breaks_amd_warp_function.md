# [Issue]: __AMDGCN_WAVEFRONT_SIZE undefined for gfx1201 — breaks amd_warp_functions.h

> **Issue #6111**
> **状态**: closed
> **创建时间**: 2026-04-02T18:04:46Z
> **更新时间**: 2026-04-13T21:13:53Z
> **关闭时间**: 2026-04-13T21:13:53Z
> **作者**: mkoker
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6111

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem

Compiling any HIP program for `gfx1201` (RDNA4) fails because `amd_warp_functions.h:86` uses `__AMDGCN_WAVEFRONT_SIZE` which the compiler does not define for wave-variable RDNA4 architectures.

### Reproduction

```bash
hipcc test.hip -o test --offload-arch=gfx1201
```

Error:
```
/usr/include/hip/amd_detail/amd_warp_functions.h:86:33: error:
  use of undeclared identifier '__AMDGCN_WAVEFRONT_SIZE'
   86 | static constexpr int warpSize = __AMDGCN_WAVEFRONT_SIZE;
```

### Root Cause

The HIP 7.0 changelog documents that `warpSize` is "no longer a `constexpr`." However, `amd_warp_functions.h:86` still uses:

```cpp
static constexpr int warpSize = __AMDGCN_WAVEFRONT_SIZE;
```

The compiler defines neither `__AMDGCN_WAVEFRONT_SIZE` nor `__AMDGCN_WAVEFRONT_SIZE__` for gfx1201 because RDNA4 supports both wave32 and wave64 (wave-variable), so no compile-time constant exists.

Verified:
```bash
/opt/rocm/lib/llvm/bin/clang++ -x hip --cuda-device-only \
  --offload-arch=gfx1201 -dM -E - < /dev/null | grep WAVEFRONT
# returns nothing
```

### Workaround

Patch the header:

```diff
-static constexpr int warpSize = __AMDGCN_WAVEFRONT_SIZE;
+#ifdef __AMDGCN_WAVEFRONT_SIZE
+static constexpr int warpSize = __AMDGCN_WAVEFRONT_SIZE;
+#else
+static constexpr int warpSize = 32;
+#endif
```

Or pass `-D__AMDGCN_WAVEFRONT_SIZE=32` to hipcc.

### Expected Fix

The header should handle the case where `__AMDGCN_WAVEFRONT_SIZE` is not defined — either via `#ifdef` guard or by using a runtime query (as the HIP 7.0 changelog implies).

### Environment

- **GPU:** AMD Radeon AI PRO R9700 (gfx1201, RDNA4)
- **ROCm:** 7.2.0 and 7.2.1
- **OS:** Ubuntu 24.04, kernel 6.17.0
- **Impact:** Blocks compilation of all HIP programs targeting gfx1201

### Related

- #6110 (gfx1201 "2 ISAs" device rejection)

---

## 评论 (3 条)

### 评论 #1 — zichguan-amd (2026-04-07T21:03:32Z)

Hi @mkoker, this should be fixed by https://github.com/ROCm/rocm-systems/commit/dd3eaa86ffba3253749a748e0a244c8694f1bdbb since ROCm 7.1.0, your log shows header files included from `/usr/include/hip/amd_detail/amd_warp_functions.h` instead of `/opt/rocm-7.1.0/include/hip/amd_detail/amd_warp_functions.h`, while your llvm is in standard installation location `/opt/rocm`.  On a clean install of ROCm 7.1.0+, that constant shouldn't be there
```
# cat /opt/rocm-7.1.0/include/hip/amd_detail/amd_warp_functions.h | grep __AMDGCN_WAVEFRONT_SIZE
# 
```

Otherwise, you can also try TheRock nightly builds for gfx120X-all as python wheels: https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx120X-all.

This issue should be resolved with a clean install.

---

### 评论 #2 — mkoker (2026-04-12T22:40:50Z)

Thanks for looking into this @zichguan-amd.

You're right — I have the Ubuntu-packaged `libamdhip64-dev` (5.7.1) installed alongside ROCm 7.2.1 from the AMD repo. The old package puts headers in `/usr/include/hip/` which gets picked up before `/opt/rocm-7.2.1/include/hip/` in the system include search order.

```
$ dpkg -s libamdhip64-dev | grep Version
Version: 5.7.1-3

$ ls /usr/include/hip/amd_detail/amd_warp_functions.h
/usr/include/hip/amd_detail/amd_warp_functions.h   # <-- stale 5.7.1 header

$ ls /opt/rocm-7.2.1/include/hip/amd_detail/amd_warp_functions.h
/opt/rocm-7.2.1/include/hip/amd_detail/amd_warp_functions.h  # <-- correct 7.2.1 header
```

hipcc's `-v` output confirms `/usr/include/` is searched before the ROCm install:
```
-internal-externc-isystem /usr/include   # picks up stale 5.7.1 headers here
...
-idirafter /opt/rocm-7.2.1/lib/llvm/bin/../../../include  # correct headers, but lower priority
```

So the fix on my end is removing the old `libamdhip64-dev` 5.7.1 package. That said — it might be worth noting in the ROCm install docs that the Ubuntu-packaged `libamdhip64-dev` (from `rocm-hipamd` in the Ubuntu repos) conflicts with the AMD-repo ROCm install. The stale `/usr/include/hip/` headers silently shadow the correct ones and cause all kinds of confusing build failures.


---

### 评论 #3 — mkoker (2026-04-12T22:51:44Z)

Confirmed — removing the stale Ubuntu packages fixed this too. After `apt remove libamdhip64-dev libamdhip64-5 libhsa-runtime-dev libhsa-runtime64-1 libhsakmt1 libhiprtc-builtins5`, the `/usr/include/hip/` directory is gone and `hipcc` picks up the correct 7.2.1 headers from `/opt/rocm/include/hip/`.

The `__AMDGCN_WAVEFRONT_SIZE` issue and the `hipStreamWaitEvent` signature mismatch I was seeing in llama.cpp builds were both from the old 5.7.1 headers. Clean build now with no patches needed.

This can be closed. Thanks for pointing me in the right direction.


---
