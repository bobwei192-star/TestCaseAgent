# [Issue]: amdgpu_gem_object_open leaks bo_va when amdgpu_eviction_fence_attach fails — surfaces as 'VM memory stats ... is non-zero when fini'

> **Issue #6214**
> **状态**: open
> **创建时间**: 2026-05-10T10:25:15Z
> **更新时间**: 2026-05-19T05:57:28Z
> **作者**: Deaththegrim
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6214

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述


### Summary

`amdgpu_gem_object_open` creates / refcounts a `bo_va` **before** calling `amdgpu_eviction_fence_attach`. If the fence attach fails (it can return `-ENOMEM` from `dma_resv_reserve_fences` under host RAM pressure), the failure path returns without undoing the `amdgpu_vm_bo_add` / refcount bump. The orphan `bo_va` lives in `vm->va` for the lifetime of the `amdgpu_vm` and `vm->stats[domain]` is leaked by 1.

User-visible signature is the `dmesg` line every Linux ROCm user sees if they leave a long-uptime box running short-lived GPU clients (Discord renderer, browser tab churn, etc.):

```
amdgpu 0000:03:00.0: VM memory stats for proc Discord(28374) task Discord:cs0(28320) is non-zero when fini
amdgpu 0000:03:00.0: VM memory stats for proc (0) task (0) is non-zero when fini
```

The cumulative leak eventually exhausts the GPU's VM-range table; the next sustained workload (ComfyUI, llama.cpp, anything with high CS-submission rate) gets a flood of:

```
amdgpu 0000:03:00.0: [drm] *ERROR* Not enough memory for command submission!
```

and the system freezes until reboot. In our test box, this occurred consistently around 25 hours of uptime.

### Root cause

`drivers/gpu/drm/amd/amdgpu/amdgpu_gem.c::amdgpu_gem_object_open`, ~line 300:

```c
amdgpu_vm_bo_update_shared(abo);
bo_va = amdgpu_vm_bo_find(vm, abo);
if (!bo_va)
    bo_va = amdgpu_vm_bo_add(adev, vm, abo);   /* +1 vm->stats */
else
    ++bo_va->ref_count;

r = amdgpu_eviction_fence_attach(&fpriv->evf_mgr, abo);
if (r) {
    amdgpu_bo_unreserve(abo);
    return r;                                   /* leaks */
}
```

### Fix

Reorder: attach fence first; only mutate `bo_va` after success. Pure reorder under the same `amdgpu_bo_reserve` window.

```diff
--- a/drivers/gpu/drm/amd/amdgpu/amdgpu_gem.c
+++ b/drivers/gpu/drm/amd/amdgpu/amdgpu_gem.c
@@ -300,12 +300,11 @@ static int amdgpu_gem_object_open(struct drm_gem_object *obj,
 	r = amdgpu_bo_reserve(abo, false);
 	if (r)
 		return r;

-	amdgpu_vm_bo_update_shared(abo);
-	bo_va = amdgpu_vm_bo_find(vm, abo);
-	if (!bo_va)
-		bo_va = amdgpu_vm_bo_add(adev, vm, abo);
-	else
-		++bo_va->ref_count;
-
-	/* attach gfx eviction fence */
 	r = amdgpu_eviction_fence_attach(&fpriv->evf_mgr, abo);
 	if (r) {
 		DRM_DEBUG_DRIVER("Failed to attach eviction fence to BO\n");
 		amdgpu_bo_unreserve(abo);
 		return r;
 	}

+	amdgpu_vm_bo_update_shared(abo);
+	bo_va = amdgpu_vm_bo_find(vm, abo);
+	if (!bo_va)
+		bo_va = amdgpu_vm_bo_add(adev, vm, abo);
+	else
+		++bo_va->ref_count;
+
 	amdgpu_bo_unreserve(abo);
```

### Test status

- 25-hour soak post-patch on RX 9070 XT: zero `is non-zero when fini` entries (previous boots: 3–10/24h).
- Failure-injection (`failslab`) test not yet run — straightforward to add if upstream wants quantitative coverage.

### Environment

- AMD RX 9070 XT (RDNA4, gfx1201, 17.1 GB VRAM)
- AMD Ryzen 9 9950X3D, 32 GB DDR5
- Linux 6.17.0-1020-oem (Ubuntu 24.04 / Mint 22.3)
- DKMS `amdgpu/6.18.4-2286447.24.04` (release 31.10), ROCm 7.2.3
- Userspace: routine desktop (Cinnamon, Firefox, Discord, Steam, ComfyUI, llama.cpp)

Mirroring this to gitlab.fd.o/drm/amd issues for the kernel maintainers.


---

## 评论 (1 条)

### 评论 #1 — amd-nicknick (2026-05-19T05:57:28Z)

Hi @Deaththegrim, thanks for reporting this issue! I have checked our source code & change list, this is actually resolved in our development branch and will be available to 6.19 dkms on next release.

---
