# The xnack feature of gfx90a of different roc* libs are inconsistent

> **Issue #2358**
> **状态**: closed
> **创建时间**: 2023-07-31T06:26:25Z
> **更新时间**: 2026-03-06T20:36:46Z
> **关闭时间**: 2026-03-06T20:36:45Z
> **作者**: littlewu2508
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2358

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- lamikr
- cgmb
- Naraenda

## 描述

I'm maintainer of Gentoo ROCm packages, and I'm confused about the xnack feature of gfx90a.

By grepping strings from binary packages hosted on https://repo.radeon.com/rocm/apt/debian/pool/main/, it seems that some libs (like rocBLAS, rocRAND, rocSOLVER, rocSPARSE) ships with `gfx90a:xnack-` and `gfx90a:xnack+` kernels; while rocFFT only ships `gfx90a` without specifying xnack feature. What's more, the Tensile library of rocBLAS contains both `gfx90a`, `gfx90a:xnack-`, and `gfx90a:xnack+` ! While `gfx908` seems to be only xnack disabled.

On a MI210 PCIe card, I also found out that it's always xnack- in `rocminfo`, despite setting `HSA_XNACK=1` and `amdgpu.noretry=0`

According to https://docs.olcf.ornl.gov/systems/crusher_quick_start_guide.html#compiling-hip-kernels-for-specific-xnack-modes, it seems that there's performance difference. So is there detailed documents and guides on xnack feature?

---

## 评论 (9 条)

### 评论 #1 — littlewu2508 (2023-07-31T06:31:10Z)

It seems that rocFFT thinks there no performance punishment to drop xnack feature flag: https://github.com/ROCmSoftwarePlatform/rocFFT/commit/cd2689360ba3b3579d044d8925838ff307b4b4cf#diff-4517c202da080822e40869fbf0b23ecf4ade04b0a47d8ed80decbb52a3664bc7

---

### 评论 #2 — saadrahim (2023-08-01T13:32:19Z)

@cgmb Can you help assign this issue to the appropriate people?

---

### 评论 #3 — cgmb (2023-08-01T20:42:35Z)

[The LLVM Offload Bundler docs on target id notation](https://clang.llvm.org/docs/ClangOffloadBundler.html#target-id) explain a bit about the syntax. When a code object is built for `gfx90a:xnack-`, it will only run on GPUs in the xnack off mode and the compiler can therefore specialized the generated code for that case. When a code object is built for `gfx90a:xnack+`, it will only run on GPUs in the xnack on mode. And, when a code object is built for `gfx90a`, it can run on GPUs that are in either mode.

I'm not sure that any libraries aside from rocFFT have verified that there actually is a performance benefit to building with gfx90a:xnack- and gfx90a:xnack+ vs. just gfx90a. I expect that most libraries are built for gfx90a:xnack- and gfx90a:xnack+ because that was what they were told to build for.

You might also find these articles useful:
- [AMD Instinct™ MI200 GPU memory space overview](https://gpuopen.com/learn/amd-lab-notes/amd-lab-notes-mi200-memory-space-overview/) from AMD GPUOpen
- [What is XNACK on AMD GPUs, and How to Enable the Feature](https://niconiconi.neocities.org/tech-notes/xnack-on-amd-gpus/) written by another ROCm user

I'm not entirely sure who should be writing official documentation about xnack. Maybe @AlexVlx has suggestions?

> On a MI210 PCIe card, I also found out that it's always xnack- in rocminfo, despite setting HSA_XNACK=1 and amdgpu.noretry=0

I'm not sure if it's relevant, but [there's a comment in KFD](https://elixir.bootlin.com/linux/v6.4.3/source/drivers/gpu/drm/amd/amdkfd/kfd_process.c#L1355) that mentions,

```
/* On most GFXv9 GPUs, the retry mode in the SQ must match the 
 * boot time retry setting. Mixing processes with different
 * XNACK/retry settings can hang the GPU.
 *
 * Different GPUs can have different noretry settings depending
 * on HW bugs or limitations. We need to find at least one 
 * XNACK mode for this process that's compatible with all GPUs.
 * Fortunately GPUs with retry enabled (noretry=0) can run code
 * built for XNACK-off. On GFXv9 it may perform slower.
 *
 * Therefore applications built for XNACK-off can always be
 * supported and will be our fallback if any GPU does not 
 * support retry.
 */
```


---

### 评论 #4 — littlewu2508 (2023-08-06T05:08:26Z)

Thank you @cgmb !

> [What is XNACK on AMD GPUs, and How to Enable the Feature](https://niconiconi.neocities.org/tech-notes/xnack-on-amd-gpus/) written by another ROCm user

This is the best explanation about xnack I've seen. Really helpful.

> I'm not sure if it's relevant, but [there's a comment in KFD](https://elixir.bootlin.com/linux/v6.4.3/source/drivers/gpu/drm/amd/amdkfd/kfd_process.c#L1355) that mentions,

Maybe I should try rebooting, rather than reloading amdgpu kernel module with changed parameters.

---

### 评论 #5 — littlewu2508 (2023-08-06T05:10:27Z)

For ROCm math libraries Since only gfx90a are built with :xnack- and other gfx90? are :xnack- only, what happened if some one is running on xnack enabled GPUs? Or does that mean there aren't a use case to run math libraries on these GPUs with xnack enabled?

---

### 评论 #6 — cgmb (2023-08-06T06:37:26Z)

> Since only gfx90a are built with :xnack- and other gfx90? are :xnack- only, what happened if some one is running on xnack enabled GPUs?

The rocr-runtime will not let you load code objects built for xnack- on hardware that is in the xnack+ state. I believe that HIP will crash with a hipErrorNoBinaryForGpu error.

> Or does that mean there aren't a use case to run math libraries on these GPUs with xnack enabled?

I'm not an expert, but it's my understanding that gfx906 was the first hardware to support xnack and there are some big caveats to using xnack+ on that architecture. I don't recall the details, but the end result is that xnack+ on gfx906 is not very useful.

In the case of gfx908, I think most of the limitations of xnack+ had been addressed. However, the hardware xnack state was still a boot-time parameter (and I assume it had a performance cost), so it probably did not see much use.

I think you can generally view this as reflecting the progressive development of a hardware feature that finally reached sufficient maturity to be widely useful in the gfx90a generation.

---

### 评论 #7 — cgmb (2023-08-06T06:59:20Z)

Hmm... the existence of xnack on much older GPUs confuses me. I was under the impression that there was progressive development on this feature from GCN to CDNA 1 to CDNA 2, but I think I'm out of my depth.

@jlgreathouse is the real expert. He is _far_ more qualified than me to explain why gfx906 and gfx908 are built only for xnack- in the binary releases of the ROCm libraries.

---

### 评论 #8 — littlewu2508 (2024-04-07T03:57:13Z)

@jlgreathouse Do you have any idea on this? Now I'm still bothered by this issue.

---

### 评论 #9 — lamikr (2026-03-06T20:36:45Z)

Therock 7.12 daily builds does the rocm binaries with xnack+ support only for the gfx942 and gfx950 gpu targets at the moment.
For gfx942 and gfx950 the xnack+ binaries can be produced by enabling the asan-sanitizer feature during therock configure time with flag:

`--preset linux-release-asan
`

as documented here:

https://github.com/ROCm/TheRock/blob/main/docs/development/sanitizers.md

The gfx906, gfx908 and gfx90a could also support xnack+ binaries but that feature is not enabled at the moment on therock. In theory that could be enabled also for those targets by creating a separate issue/pr per target.

Supported GPU targets can contain binaries both for the xnack- and xnack+ feature. Depending from the mode (xnack-/xnack+) where the GPU has been booted,  rocm will on runtime decide which version of kernels it will load.

For example following would enable the the xnack+ mode on next boot in Ubuntu.

```
sudo nano /etc/default/grub
# edit this line by adding amdgpu arguments.
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.noretry=0 amdgpu.xnack=1"
sudo update-grub
export HSA_XNACK=1
```

To boot on xnack- mode, those settings would then need to be disabled.

---
