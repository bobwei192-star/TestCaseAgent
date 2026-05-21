# [Issue]: Can't free any GPU memory if virtual address space is still reserved on Linux (but it works on Windows?)

> **Issue #6021**
> **状态**: closed
> **创建时间**: 2026-03-06T16:02:06Z
> **更新时间**: 2026-04-01T11:18:05Z
> **关闭时间**: 2026-04-01T11:18:05Z
> **作者**: asagi4
> **标签**: status: assessed, status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/6021

## 标签

- **status: assessed** (颜色: #e6d813)
- **status: fix submitted** (颜色: #75d97e)

## 负责人

- amd-nicknick

## 描述

### Problem Description

When trying to implement ROCm support in comfy-aimdo, I'm running into a problem with freeing memory.

aimdo first reserves virtual address space in a large chunk with hipMemAddressReserve, and then later maps actual memory reservations into the address space. Later, it will free individual chunks from the reserved address space (when it needs to offload GPU memory), and this apparently works on CUDA and reportedly on ROCm Windows, but on Linux, it seems that no GPU memory is freed until the *entire* address space is also freed with hipMemAddressFree, which makes comfy-aimdo unable to offload any memory.

My expectation is that memory would be freed at  `hipMemRelease`, which would allow keeping the address space reserved while freeing physical memory. but that does not happen.

### Operating System

RHEL 9, RHEL 10 (re-tested after OS upgrade, problem still occurs)

### CPU

Intel Haswell

### GPU

XTX 7900

### ROCm Version

Tested with 7.2 and 7.11-preview

### ROCm Component

HIP

### Steps to Reproduce

Small reproducer. Run without a parameter to use hipMemAddressRelease (which correctly frees memory but forces releasing the address space as well) and with a parameter to run without hipMemAddressRelease to observe that memory remains in use.

The allocs here allocate the address space in smaller chunks, but you could also allocate the whole address space in one go in the main function and let the allocs map physical memory into it in chunks, which matches what comfy-aimdo wants to do.
```
#include <hip/hip_runtime.h>
#include <stdio.h>
#include <stdbool.h>

static size_t alloc_count = 0;
static bool free_address = true;

typedef struct {
        void* ptr;
        hipMemGenericAllocationHandle_t h;
} alloc_t;

#define LOG(x, ...) printf(x "\n" __VA_OPT__(,) __VA_ARGS__)

static inline bool check_impl(hipError_t result, const char *label) {
        if (result != hipSuccess) {
                LOG("HIP ERROR (%s): %s", label, hipGetErrorString(result));
        }
        return (result == hipSuccess);
}

#define CHECK(x) check_impl((x), #x)
#define CHECK_RET(x) do { if (!CHECK(x)) return false; } while(0)
void print_mem() {
        size_t mem_free, mem_total;
        hipMemGetInfo(&mem_free, &mem_total);
        LOG("Memory free: %zuMiB in_use: %zuMiB", mem_free / (1024*1024), (mem_total-mem_free)/(1024*1024));
}

#define ALIGNMENT (1024*1024)
#define ALLOC_COUNT 1024
#define CHUNK (2ULL*1024*1024)
bool alloc(alloc_t* dest) {
        size_t s = CHUNK;
        hipMemAllocationProp p = {
                .type = hipMemAllocationTypePinned,
                .location.type = hipMemLocationTypeDevice,
                .location.id = 0,
        };
        CHECK_RET(hipMemAddressReserve(&dest->ptr, s, ALIGNMENT, 0, 0));
        CHECK_RET(hipMemCreate(&dest->h, s, &p, 0));
        CHECK_RET(hipMemMap(dest->ptr, s, 0, dest->h, 0));
        alloc_count++;
        return true;
}
bool dealloc(alloc_t* dest) {
        CHECK_RET(hipMemUnmap(dest->ptr, CHUNK));
        CHECK_RET(hipMemRelease(dest->h));
        if (free_address) CHECK_RET(hipMemAddressFree(dest->ptr, CHUNK));
        alloc_count--;
        return true;
}


void exercise() {
        size_t allocs = 0;
        alloc_t *allocations[ALLOC_COUNT] = {0};
        print_mem();
        for (size_t i = 0; i < ALLOC_COUNT; i++) {
                alloc_t *a = malloc(sizeof(*a));
                alloc(a);
                allocations[i] = a;
        }
        LOG("Alloc count: %zu", alloc_count);
        LOG("Finished allocating %d chunks", ALLOC_COUNT);
        print_mem();
        for (size_t i = 0; i < ALLOC_COUNT; i++) {
                if (i % 2) {
                        dealloc(allocations[i]);
                        free(allocations[i]);
                }
        }
        LOG("Freed half, alloc count: %zu", alloc_count);
        print_mem();

        for (size_t i = 0; i < ALLOC_COUNT; i++) {
                if (!(i % 2)) {
                        dealloc(allocations[i]);
                        free(allocations[i]);
                }
        }
        LOG("Finished freeing %d chunks", ALLOC_COUNT);
        LOG("Alloc count: %zu", alloc_count);
        print_mem();
}

int main(int argc, char** argv) {
        if (argc > 1) {
                LOG("Running without hipMemAddressFree");
                free_address = false;
        } else {
                LOG("Running with hipMemAddressFree");
        }
        for (int i = 0; i < 2; i++) exercise();
}
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Runs of the test code from my machine:
```
$ hipcc $(hipconfig -C) test.c && ./a.out test
Running without hipMemAddressFree
Memory free: 24524MiB in_use: 36MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 22330MiB in_use: 2230MiB
Freed half, alloc count: 512
Memory free: 22330MiB in_use: 2230MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 22330MiB in_use: 2230MiB
Memory free: 22330MiB in_use: 2230MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 20282MiB in_use: 4278MiB
Freed half, alloc count: 512
Memory free: 20282MiB in_use: 4278MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 20282MiB in_use: 4278MiB```

```$ hipcc $(hipconfig -C) test.c && ./a.out
Running with hipMemAddressFree
Memory free: 24524MiB in_use: 36MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 22330MiB in_use: 2230MiB
Freed half, alloc count: 512
Memory free: 23354MiB in_use: 1206MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 24378MiB in_use: 182MiB
Memory free: 24378MiB in_use: 182MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 22330MiB in_use: 2230MiB
Freed half, alloc count: 512
Memory free: 23354MiB in_use: 1206MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 24378MiB in_use: 182MiB```


---

## 评论 (13 条)

### 评论 #1 — 0xDELUXA (2026-03-06T17:01:28Z)

I can confirm that this issue doesn't occur on Windows ROCm (TheRock). Modified the reproducer script to [this](https://gist.github.com/0xDELUXA/4ac45fc91e9cdf4805c0bc2e7ff9b78a) version to be compatible with Windows, then compiled it using:
```
hipcc -I"C:\ComfyUI\venv\Lib\site-packages\_rocm_sdk_core\include" -D__HIP_PLATFORM_AMD__ hip_vmm_test.cpp -o hip_vmm_test.exe
```
### Execution Results
With `hipMemAddressFree`:
```
(venv) PS C:\ComfyUI> .\hip_vmm_test.exe
Running with hipMemAddressFree
Memory free: 16158MiB in_use: 145MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 14098MiB in_use: 2205MiB
Freed half, alloc count: 512
Memory free: 14162MiB in_use: 2141MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 16146MiB in_use: 157MiB
Memory free: 16146MiB in_use: 157MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 14098MiB in_use: 2205MiB
Freed half, alloc count: 512
Memory free: 14162MiB in_use: 2141MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 16146MiB in_use: 157MiB
```
Without it:
```
(venv) PS C:\ComfyUI> .\hip_vmm_test.exe 1
Running without hipMemAddressFree
Memory free: 16158MiB in_use: 145MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 14098MiB in_use: 2205MiB
Freed half, alloc count: 512
Memory free: 14162MiB in_use: 2141MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 16146MiB in_use: 157MiB
Memory free: 16146MiB in_use: 157MiB
Alloc count: 1024
Finished allocating 1024 chunks
Memory free: 14098MiB in_use: 2205MiB
Freed half, alloc count: 512
Memory free: 14162MiB in_use: 2141MiB
Finished freeing 1024 chunks
Alloc count: 0
Memory free: 16146MiB in_use: 157MiB
```
As seen above, memory usage behaves correctly on Windows ROCm in both modes.

---

### 评论 #2 — asagi4 (2026-03-16T16:11:05Z)

I did testing directly with the HSA API and the same problem happens with it. I'm not surprised, given that HIP is a pretty thin wrapper over the runtime, but it does seem like the problem is deeper in the stack.

---

### 评论 #3 — amd-nicknick (2026-03-18T12:39:01Z)

kfd tracks memory usage in [amdgpu_amdkfd_reserve_mem_limit](https://elixir.bootlin.com/linux/v6.17.8/C/ident/amdgpu_amdkfd_reserve_mem_limit), the required space is accounted during `hipMemCreate` -> [amdgpu_amdkfd_gpuvm_alloc_memory_of_gpu](https://elixir.bootlin.com/linux/v6.17.8/C/ident/amdgpu_amdkfd_gpuvm_alloc_memory_of_gpu).
This in turns create a GEM object, which registers a release notify [amdgpu_amdkfd_release_notify](https://elixir.bootlin.com/linux/v6.17.8/C/ident/amdgpu_amdkfd_release_notify).
Upon `hipMemRelease`, kfd put the reference to the object, but the object still has outstanding references. This reference is not cleared until vmunmap (Possibly due to ref held in mmap).
```
[13317.192670]  amdgpu_amdkfd_unreserve_mem_limit+0x33/0x390 [amdgpu]
[13317.193043]  amdgpu_amdkfd_release_notify+0x38/0x60 [amdgpu]
[13317.193401]  amdgpu_bo_release_notify+0xa3/0x1e0 [amdgpu]
[13317.193706]  ttm_bo_release+0x135/0x2d0 [amdttm]
[13317.193716]  amdttm_bo_put+0x3c/0x70 [amdttm]
[13317.193723]  amdgpu_gem_object_free+0x59/0x120 [amdgpu]
[13317.194023]  drm_gem_object_free+0x1d/0x40
[13317.194026]  amdttm_bo_vm_close+0x45/0x70 [amdttm]
[13317.194034]  remove_vma+0x2c/0x70
[13317.194037]  vms_complete_munmap_vmas+0xf5/0x1d0
[13317.194040]  do_vmi_align_munmap+0x17f/0x1b0
[13317.194049]  do_vmi_munmap+0xd3/0x190
[13317.194052]  __vm_munmap+0xbb/0x190
[13317.194055]  ? __schedule+0x315/0x7a0
[13317.194061]  __x64_sys_munmap+0x1b/0x30
[13317.194063]  x64_sys_call+0x25c4/0x2680
[13317.194066]  do_syscall_64+0x80/0xa30
[13317.194069]  ? dequeue_signal+0x80/0x190
[13317.194072]  ? srso_return_thunk+0x5/0x5f
[13317.194074]  ? get_signal+0x6de/0x840
[13317.194078]  ? srso_return_thunk+0x5/0x5f
[13317.194082]  ? srso_return_thunk+0x5/0x5f
[13317.194084]  ? restore_fpregs_from_fpstate+0x3d/0xc0
[13317.194087]  ? srso_return_thunk+0x5/0x5f
[13317.194089]  ? switch_fpu_return+0x5c/0x100
[13317.194092]  ? srso_return_thunk+0x5/0x5f
[13317.194094]  ? arch_exit_to_user_mode_prepare.isra.0+0xc2/0x100
[13317.194096]  ? srso_return_thunk+0x5/0x5f
[13317.194098]  ? irqentry_exit_to_user_mode+0x2d/0x1d0
[13317.194101]  ? srso_return_thunk+0x5/0x5f
[13317.194103]  ? exc_debug_user+0xc8/0x110
[13317.194106]  ? srso_return_thunk+0x5/0x5f
[13317.194108]  ? noist_exc_debug+0x3f/0x70
[13317.194113]  entry_SYSCALL_64_after_hwframe+0x76/0x7e
```

Next step: Trace out the object's lifecycle and see if it's possible to unmap the bo directly on release.

@asagi4, I created another repro script that might be closer to your intended use case. While it won't affect our debug progress, could you please help check if it's closer to your intended use case in ComfyUI? Thanks!

<details>
<summary>Reproducer</summary>

```
#include <hiplab.h>
#include <cmath>
#include <iostream>
#include <vector>

bool vmmSupported(int device) {
    int vmm = 0;
    HIP_CHECK(
        hipDeviceGetAttribute(
            &vmm, hipDeviceAttributeVirtualMemoryManagementSupported, device
        )
    );

    std::cout << "Virtual memory management support value: " << vmm << std::endl;

    if (vmm == 0) {
        std::cout << "GPU " << device << " doesn't support virtual memory management.";
        return false;
    }

    return true;
}

size_t getGranularity(int device) {
    hipMemAllocationProp prop = {};
    prop.type = hipMemAllocationTypePinned;
    prop.location.type = hipMemLocationTypeDevice;
    prop.location.id = device;

    size_t granularity = 0;
    HIP_CHECK(
        hipMemGetAllocationGranularity(
            &granularity,
            &prop,
            hipMemAllocationGranularityMinimum
        )
    );

    return granularity;
}

void printMem() {
    size_t mem_free, mem_total;
    HIP_CHECK(hipMemGetInfo(&mem_free, &mem_total));
    std::cout << "Memory free: " << mem_free / (1024 * 1024) << " MiB, in use: " << (mem_total - mem_free) / (1024 * 1024) << " MiB" << std::endl;
}

int main() {
    int device = 1;
    int granularity = getGranularity(device);
    int num_chunks = 16;
    size_t chunk_size = 1 * 1024 * 1024 * 1024, total_size = ((chunk_size * num_chunks) / granularity + 1) * granularity;

    printHipInfo();
    if(!vmmSupported(device)) return -1;
    printMem();
    std::cout << "Using chunk size: " << chunk_size << " bytes, number of chunks: " << num_chunks << ", total reserved size: " << total_size << " B, granularity: " << granularity << " B" << std::endl;

    void* vm_ptr = 0;

    HIP_CHECK(hipMemAddressReserve(&vm_ptr, total_size, granularity, nullptr, 0));
    std::cout << "Reserved virtual memory at address: " << vm_ptr << " with size: " << total_size << " bytes" << std::endl;
    printMem();

    std::vector<hipMemGenericAllocationHandle_t> handles(num_chunks);

    for(int i = 0; i < num_chunks; ++i) {
        void* chunk_ptr = static_cast<char*>(vm_ptr) + i * chunk_size;

        hipMemAllocationProp prop = {};
        prop.type = hipMemAllocationTypePinned;
        prop.location.type = hipMemLocationTypeDevice;
        prop.location.id = device;
        
        HIP_CHECK(hipMemCreate(&handles[i], chunk_size, &prop, 0));
        HIP_CHECK(hipMemMap(chunk_ptr, chunk_size, 0, handles[i], 0));
        std::cout << "Create & mapped chunk " << i << " at address: " << chunk_ptr << std::endl;
        printMem();
    }
    
    for(int i = 0; i < num_chunks; ++i) {
        void* chunk_ptr = static_cast<char*>(vm_ptr) + i * chunk_size;
        HIP_CHECK(hipMemUnmap(chunk_ptr, chunk_size));
        HIP_CHECK(hipMemRelease(handles[i]));
        std::cout << "Unmapped & released chunk " << i << " at address: " << chunk_ptr << std::endl;
        printMem();
    }
    
    HIP_CHECK(hipMemAddressFree(vm_ptr, total_size));
    std::cout << "Freed virtual memory at address: " << vm_ptr << " with size: " << total_size << " bytes" << std::endl;
    printMem();

    return 0;
}
```

</details>

EDIT: Fixed formatting, oops.

---

### 评论 #4 — asagi4 (2026-03-18T17:15:44Z)

@amd-nicknick looks like the code for your reproducer got mangled in the github comment, so it's difficult to read. But yeah, that seems closer to the actual use case.

---

### 评论 #5 — 0xDELUXA (2026-03-19T14:20:44Z)

A slightly modified version of the reproducer script (so it can run on Windows) reaffirms that ROCm on Windows doesn't have the issue in question.

---

### 评论 #6 — amd-nicknick (2026-03-24T15:03:12Z)

After looking through the flow & trace the object lifecycle. I discovered the issue actually came from ROCr  `MappedHandle`, which represents a VA mapped to a piece of memory handle.
During the construction of `MappedHandle`, it by default creates a CPU agent and mmap the underlying DRM FD to the VA. The causes the DRM FD to be opened and mapped.
However, when `hipMemUnmap` is called, this will destroy the `MappedHandle`, but won't re-mmap the VA back to an anonymous range, causing the FD to be kept opened.
It is when finally calling `hipMemRelease`, where the entire VA range is given to `munmap`, causing the FD to be closed.

Raised a PR in ROCr to address this: https://github.com/ROCm/rocm-systems/pull/4363, feel free to give this a try.
<details>

<summary>Reproducer output with the fix</summary>

```
Memory free: 30496 MiB, in use: 80 MiB
Using chunk size: 1073741824 bytes, number of chunks: 8, total reserved size: 8589938688 B, granularity: 4096 B
Reserved virtual memory at address: 0x7ff8dda00000 with size: 8589938688 bytes
Memory free: 30496 MiB, in use: 80 MiB
Create & mapped chunk 0 at address: 0x7ff8dda00000
Memory free: 29326 MiB, in use: 1250 MiB
Create & mapped chunk 1 at address: 0x7ff91da00000
Memory free: 28302 MiB, in use: 2274 MiB
Create & mapped chunk 2 at address: 0x7ff95da00000
Memory free: 27278 MiB, in use: 3298 MiB
Create & mapped chunk 3 at address: 0x7ff99da00000
Memory free: 26254 MiB, in use: 4322 MiB
Create & mapped chunk 4 at address: 0x7ff9dda00000
Memory free: 25230 MiB, in use: 5346 MiB
Create & mapped chunk 5 at address: 0x7ffa1da00000
Memory free: 24206 MiB, in use: 6370 MiB
Create & mapped chunk 6 at address: 0x7ffa5da00000
Memory free: 23182 MiB, in use: 7394 MiB
Create & mapped chunk 7 at address: 0x7ffa9da00000
Memory free: 22158 MiB, in use: 8418 MiB
Unmapped & released chunk 0 at address: 0x7ff8dda00000
Memory free: 23182 MiB, in use: 7394 MiB
Unmapped & released chunk 1 at address: 0x7ff91da00000
Memory free: 24206 MiB, in use: 6370 MiB
Unmapped & released chunk 2 at address: 0x7ff95da00000
Memory free: 25230 MiB, in use: 5346 MiB
Unmapped & released chunk 3 at address: 0x7ff99da00000
Memory free: 26254 MiB, in use: 4322 MiB
Unmapped & released chunk 4 at address: 0x7ff9dda00000
Memory free: 27278 MiB, in use: 3298 MiB
Unmapped & released chunk 5 at address: 0x7ffa1da00000
Memory free: 28302 MiB, in use: 2274 MiB
Unmapped & released chunk 6 at address: 0x7ffa5da00000
Memory free: 29326 MiB, in use: 1250 MiB
Unmapped & released chunk 7 at address: 0x7ffa9da00000
Memory free: 30350 MiB, in use: 226 MiB
Freed virtual memory at address: 0x7ff8dda00000 with size: 8589938688 bytes
Memory free: 30350 MiB, in use: 226 MiB
```

</details>

---

### 评论 #7 — asagi4 (2026-03-24T15:16:25Z)

@amd-nicknick I can try and see if I can get that built a bit later today. Hopefully I'll just be able to drop that on top of my existing ROCM install with some LD_PRELOAD magic... Do you have any idea when the fix would be picked up by a ROCm distribution (like TheRock nightlies) if/when it's merged?

---

### 评论 #8 — 0xDELUXA (2026-03-24T15:38:44Z)

> Do you have any idea when the fix would be picked up by a ROCm distribution (like TheRock nightlies) if/when it's merged?

Theoretically, after it is merged into `ROCm/rocm-systems` and TheRock's `rocm-systems` submodule is updated, the fix will be in the nightlies. Will take several days, I think.

---

### 评论 #9 — asagi4 (2026-03-24T16:01:09Z)

Building was easier than I expected, and things do seem to work now. I'll have to test what happens when I run comfy-aimdo with it.

EDIT: looks like things are working. I didn't stress-test yet, but I can run workflows that swap between models that previously triggered VRAM issues. It is much faster and memory usage behaviour is much better than before.

---

### 评论 #10 — Apophis3158 (2026-03-28T23:56:13Z)

> A slightly modified version of the reproducer script (so it can run on Windows) reaffirms that ROCm on Windows doesn't have the issue in question.

I assume you're using nightly ROCm. If possible, please take a test in the release version (7.2.0 or [7.2.1](https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/)). 

I didn't see `HIP Library Path: C:\WINDOWS\SYSTEM32\amdhip64_7.dll` in your print, so I guess you copied it to the directory.
It works fine on my side when I don't copy
```
❯ .\Reproducer.exe
HIP Library Path: C:\WINDOWS\SYSTEM32\amdhip64_7.dll
Virtual memory management support value: 1
Memory free: 16152 MiB, in use: 151 MiB
Using chunk size: 1073741824 bytes, number of chunks: 16, total reserved size: 17179934720 B, granularity: 65536 B
Reserved virtual memory at address: 0000000304000000 with size: 17179934720 bytes
Memory free: 16152 MiB, in use: 151 MiB
Create & mapped chunk 0 at address: 0000000304000000
...
```
but after copying the ROCm release version `amdhip64_7.dll`, I get the error `hipErrorNoDevice`:
```
❯ .\Reproducer.exe
Reproducer.cpp:46: HIP Error: no ROCm-capable device is detected
```
What I want to say is that there are still some issues with the release version of ROCm that make aimdo unusable (based on feedback from the community and my own testing). Should we just tell them to use nightly ROCm or try to work around it on the aimdo side?

---

### 评论 #11 — 0xDELUXA (2026-03-29T20:54:55Z)

Everyone should use TheRock. 

In the future, it will be:

> ... "official" and fully integrated with our QA, documentation, and other release channels (for drivers, etc).
(https://github.com/ROCm/TheRock/discussions/2845#discussioncomment-15477425)

I don’t even understand what’s up with these "release" versions, as they aren’t any more stable or better than TheRock. "Nightly" can’t be considered the exact same as "unstable".

Some people also think that the wheels at https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/ can’t really be considered official PyTorch wheels, because they aren’t listed in https://download.pytorch.org/whl/rocm7.2/. In fact, https://pytorch.org/ even notes:
> NOTE: ROCm is not available on Windows

So yes, we’re in a complicated state as of now.

---

### 评论 #12 — Apophis3158 (2026-03-30T20:27:41Z)

> Everyone should use TheRock.

You are right.

It's a pity that 7.x.x is the version of the official documentation guidelines, and basically ROCm users will follow the official installation (I was before).
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html

So before ROCm for Windows can be released to pytorch.org, people who have encountered problems with "release" versions should try TheRock.

---

### 评论 #13 — 0xDELUXA (2026-03-31T08:07:00Z)

Also, the [official](https://rocm.docs.amd.com/en/7.12.0-preview/#amd-rocm-rocm-version-preview) AMD website says:

> ROCm 7.12.0 is a technology preview release built with [TheRock](https://github.com/ROCm/TheRock), AMD’s new open build and release system. This preview introduces a new modular build workflow that will become standard in the near future. The existing monolithic release process will continue to be used in the production ROCm 7.0 stream during this transition period until the modular workflow fully replaces it.


---
