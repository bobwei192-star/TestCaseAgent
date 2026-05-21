# [Issue]: cycles rendering not working with rx9070xt

> **Issue #4526**
> **状态**: closed
> **创建时间**: 2025-03-25T00:17:32Z
> **更新时间**: 2025-04-25T14:18:19Z
> **关闭时间**: 2025-04-24T19:45:09Z
> **作者**: ergo3d
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4526

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

i made report in
https://projects.blender.org/blender/blender/issues/136143
but i guess problem in rocm

cycles rendering not working in blender with rx9070xt 

System Information
os:arch linux 6.13.8
mesa 25.0.2-2
rocm-hip-runtime 6.3.3-1
gnome 48
windowing system wayland

GPU
RX 9070 XT

CPU
AMD Ryzen 7 9700X 

Blender Version
4.4.0 from official site

Exact steps for others to reproduce the error
open scene with textured object and press rendering
terminal says

Memory access fault by GPU node-1 (Agent handle: 0x7bc2d9de9e00) on address 0x2c95e7ee8000. Reason: Page not present or supervisor privilege.
Failed to read GPU memory: Input/output error

attaching scene with i have problem (actually i have problem in all my scenes)
https://projects.blender.org/attachments/0f9a2ba3-af6b-4b32-8899-17c16135ee52
no matter its just hip or hip rt, when selected igpu rdna2 there is no problems

also i tested lasted RadeonProRender in blender 4.3
and its also freezes and crashed with 9070 but not with igpu rdna2


---

## 评论 (13 条)

### 评论 #1 — Atephys (2025-03-27T21:04:40Z)

I'm experiencing the exact same issue.

**GPU**: RX 9070 XT 
**OS**: Arch Linux
**ROCm**: 6.3.3-1
**Blender**: 4.4.0 official release

Blender detects the GPU, but attempting to render with Cycles results in a crash after a few samples. Terminal output ends with:
```
Memory access fault by GPU node-1 (Agent handle: 0x75be70ecb700) on address 0x75bbd5ef2000. Reason: Page not present or supervisor privilege.
```

Rendering works fine when using the integrated RDNA2 GPU.

The same .blend file renders successfully on Windows 11 using the RX 9070 XT — so this is specific to the ROCm Linux stack.

---

### 评论 #2 — zichguan-amd (2025-04-01T20:39:24Z)

Hi @ergo3d @Atephys, in PR [#133129 - Cycles: HIP-RT 2.5 integration and gfx12 support - blender - Blender Projects](https://projects.blender.org/blender/blender/pulls/133129), description says "denoising will only be possible on CPU, or secondary gfx11 or below GPU".

After turning off denoising in View Layer > Passes > Data > Denoising Data, your scene renders correctly. Please check if you have denoising enabled anywhere in your project.

---

### 评论 #3 — ergo3d (2025-04-01T21:22:40Z)

> Hi [@ergo3d](https://github.com/ergo3d) [@Atephys](https://github.com/Atephys), in PR [#133129 - Cycles: HIP-RT 2.5 integration and gfx12 support - blender - Blender Projects](https://projects.blender.org/blender/blender/pulls/133129), description says "denoising will only be possible on CPU, or secondary gfx11 or below GPU".
> 
> After turning off denoising in View Layer > Passes > Data > Denoising Data, your scene renders correctly. Please check if you have denoising enabled anywhere in your project.

thanks a lot!!! rending works! but after some testing looks like problem still happens in viewport but error is little bit different 

IMB_ibImageFromMemory: unknown file-format (<packed data>)
Memory access fault by GPU node-1 (Agent handle: 0x7727fd438200) on address 0x772512ca4000. Reason: Page not present or supervisor privilege.
Failed to read GPU memory: Input/output error
GPU core dump failed
Aborted (core dumped)

now i can work
thanks again


---

### 评论 #4 — ergo3d (2025-04-01T22:45:41Z)

> Hi [@ergo3d](https://github.com/ergo3d) [@Atephys](https://github.com/Atephys), in PR [#133129 - Cycles: HIP-RT 2.5 integration and gfx12 support - blender - Blender Projects](https://projects.blender.org/blender/blender/pulls/133129), description says "denoising will only be possible on CPU, or secondary gfx11 or below GPU".
> 
> After turning off denoising in View Layer > Passes > Data > Denoising Data, your scene renders correctly. Please check if you have denoising enabled anywhere in your project.

sorry but i was too hasty, really large scenes with uses at least 7 and more gb vram rendering time to time 
after render completed (or i canceled in progress)i pressed render again and problem with memory error repeated
i do disabled all i found with denoise option, also tested fresh blender setting (by delete blender folder in .config)
after some  time work with active render in viewport, without denoise, scene crashes
problem also happens in second/third rendering by f12

https://cloud.blender.org/p/gallery/5dd6d7044441651fa3decb56
this one good to reproduce problem
after i disabled denoise it's successful rendered first times but freezes on second or third

---

### 评论 #5 — B4rr3l-Rid3r (2025-04-02T21:15:38Z)

Same here, denoise off did not fix it

---

### 评论 #6 — zichguan-amd (2025-04-24T18:05:57Z)

Hi @ergo3d @B4rr3l-Rid3r @Atephys, the issue should be fixed in the latest llvm codebase. Can you build clang on amd-staging branch and rebuild the gfx1201 kernel with the newer compiler? I've tested the junkshop scene with denoise disabled on llvm commit 0a0686f0dfd3ebdf7f1ff95912d4671414fae3f0 and observed no error.

Steps to build clang and blender kernels (similar to https://github.com/ROCm/llvm-project/issues/58.):
Build clang:
```
git clone https://github.com/ROCm/llvm-project.git && cd llvm-project
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="AMDGPU;X86" -DLLVM_ENABLE_PROJECTS="clang;lld"  ../llvm
make -j$(nproc)
```
Recompile the kernel
```
export LLVM_BIN_DIR=<your llvm-project dir>/build/bin
export BLENDER_DIR=<your blender directory>

HIP_CLANG_PATH=$LLVM_BIN_DIR hipcc -Wno-parentheses-equality -Wno-unused-value -ffast-math --offload-arch=gfx1201 -I "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source" --genco "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source/kernel/device/hip/kernel.cpp" -o kernel_gfx1201.fatbin -m64 -DHIPCC -I"$BLENDER_DIR/4.4/scripts/addons_core/cycles/source" -DWITH_NANOVDB 
```

Zip and move the kernel.
```
#backup or delete the original kernel
mv $BLENDER_DIR/4.4/scripts/addons_core/cycles/lib/kernel_gfx1201.fatbin.zst $BLENDER_DIR/4.4/scripts/addons_core/cycles/lib/kernel_gfx1201.fatbin.zst.bk
zstd kernel_gfx1201.fatbin && mv kernel_gfx1201.fatbin.zst $BLENDER_DIR/4.4/scripts/addons_core/cycles/lib/ 
```

Renders succefully using
```
./blender --verbose 2 -E CYCLES ../thejunkshopsplashscreen-35a35553b3dd4f8c8fb5a6ccc5065ff1.blend -b --debug-cycles -F PNG -f 0 -- --cycles-device HIP --cycles-print-stats
```

---

### 评论 #7 — ergo3d (2025-04-24T19:45:09Z)

tested with blender 4.5 rocm 6.3.3-1
HIP-RT still have same problem
just HIP gpu render works fine after compile kernel_gfx1201.fatbin.zst with your instruction
thanks a lot!

---

### 评论 #8 — zichguan-amd (2025-04-24T19:59:59Z)

I'll test out and let internal team know about RT still having issue.

---

### 评论 #9 — lamb-j (2025-04-24T20:21:06Z)

@zichguan-amd try setting these and re-running. I can help decipher the log:

export AMD_LOG_LEVEL=7
export AMD_COMGR_EMIT_VERBOSE_LOGS=1
export AMD_COMGR_REDIRECT_LOGS=stderr (or a file)

---

### 评论 #10 — zichguan-amd (2025-04-24T21:03:20Z)

@ergo3d I've recompiled the hiprt kernel with staging llvm and it's working. The compilation command is a bit different:
```
HIP_CLANG_PATH=$LLVM_BIN_DIR hipcc -Wno-parentheses-equality -Wno-unused-value -ffast-math -O3 -std=c++17 -D __HIPRT__ --offload-arch=gfx1201 -I "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source"  -I "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source/kernel/device/hiprt" --genco "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source/kernel/device/hiprt/kernel.cpp" -o kernel_rt_gfx1201.hipfb -DWITH_NANOVDB 
```
Replace the original `kernel_rt_gfx1201.hipfb.zst` with the new one should address the issue for RT.


@lamb-j I'll still get the logs you suggested and see if I can root cause the issue.

---

### 评论 #11 — ergo3d (2025-04-24T21:39:41Z)

now HIP-RT works fine too! 
actually i dont use HIP-RT because it unbelievable slow in "updating geometry" before starts rendering 
and its using more vram then HIP 
but thanks!

---

### 评论 #12 — Hadrianneue (2025-04-25T07:22:23Z)

> [@ergo3d](https://github.com/ergo3d) I've recompiled the hiprt kernel with staging llvm and it's working. The compilation command is a bit different:
> 
> ```
> HIP_CLANG_PATH=$LLVM_BIN_DIR hipcc -Wno-parentheses-equality -Wno-unused-value -ffast-math -O3 -std=c++17 -D __HIPRT__ --offload-arch=gfx1201 -I "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source"  -I "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source/kernel/device/hiprt" --genco "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source/kernel/device/hiprt/kernel.cpp" -o kernel_rt_gfx1201.hipfb -DWITH_NANOVDB 
> ```
> 
> Replace the original `kernel_rt_gfx1201.hipfb.zst` with the new one should address the issue for RT.
> 
> [@lamb-j](https://github.com/lamb-j) I'll still get the logs you suggested and see if I can root cause the issue.

Are there optimizations flags for it? just wondering because linux was around ~2 seconds slower than windows consistently (20 - 22.8 sec w/ hiprt and 26 - 28 sec w/ hip)

---

### 评论 #13 — zichguan-amd (2025-04-25T14:18:16Z)


> ```
> HIP_CLANG_PATH=$LLVM_BIN_DIR hipcc -Wno-parentheses-equality -Wno-unused-value -ffast-math -O3 -std=c++17 -D __HIPRT__ --offload-arch=gfx1201 -I "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source"  -I "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source/kernel/device/hiprt" --genco "$BLENDER_DIR/4.4/scripts/addons_core/cycles/source/kernel/device/hiprt/kernel.cpp" -o kernel_rt_gfx1201.hipfb -DWITH_NANOVDB 
> ```
The flags used there are taken from blender directly. You can experiment with different flags available to clang and hipcc (see https://clang.llvm.org/docs/ClangCommandLineReference.html and `hipcc --help`). You might get better results depending on your workload but I'm sure if there are more general optimizations available, blender would have included it.

---
