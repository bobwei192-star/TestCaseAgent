# [Issue]: ROCm completely stopped working after version 6.14.0-202 on Linux.

> **Issue #4919**
> **状态**: closed
> **创建时间**: 2025-06-12T17:07:28Z
> **更新时间**: 2025-07-31T19:46:33Z
> **关闭时间**: 2025-07-31T19:46:33Z
> **作者**: mikosenigma
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4919

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Hi. Is there any chance at all of getting ROCm support (including OpenCL, HIP and HIP RT, and PyTorch) fixed on Nobara Linux with RDNA2 RX 6000 series cards? ROCm completely stopped working after version 6.14.0-202, and we're now on 6.15.1 and it still doesn't work. I know this isn't Nobara's fault, but it's incredible that no one has fixed it yet. I can't fix it myself.

### Operating System

Nobara Linux 42

### CPU

ryzen 5 5600 X

### GPU

RX 6800 XT

### ROCm Version

6.3

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — Matthew-Jenkins (2025-06-13T14:58:04Z)

Have you checked this? https://wiki.nobaraproject.org/graphics/amd/opencl-rocm-support 

It says it is just using fedoras rocm packages and you need to install the rocm-meta package to get support. Looks like it snapshotted the F42 repos. The spec file for rocm-meta is for 6.3.1.

You should *also* make sure you're using the amdgpu driver. 

---

### 评论 #2 — ppanchad-amd (2025-06-16T15:22:57Z)

Hi @mikosenigma. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — chboishabba (2025-06-20T01:14:34Z)

It is my first time compiling a kernel to bisect. I am attempting to get up to speed to do so, if you could confirm if this is helpful please :) I will continue to familiarise myself. guess we will see if I complete by the time you return :)

@ppanchad-amd https://github.com/robertrosenbusch/gfx803_rocm/issues/35

It appears kernels either side of 6.14 are causing issues. 

```
Linux archb 6.15.2-arch1-1 #1 SMP PREEMPT_DYNAMIC Tue, 10 Jun 2025 21:32:33 +0000 x86_64 GNU/Linux
```

![Image](https://github.com/user-attachments/assets/28781fd8-5e17-4615-81dd-3b6e69626cdb)
https://github.com/robertrosenbusch/gfx803_rocm
https://github.com/ROCm/ROCm/issues/4619
https://github.com/lamikr/rocm_sdk_builder/issues/254
https://github.com/pytorch/pytorch/issues/145608

Possibly
https://shatsky.github.io/posts/2020-01-22_linux-amdgpu-reset-bug-polaris-workaround.html?utm_source=chatgpt.com

https://lore.kernel.org/amd-gfx/CY8PR12MB70998BEFD1B9DA50A2F1669E8C73A@CY8PR12MB7099.namprd12.prod.outlook.com/T/#t
https://lore.kernel.org/amd-gfx/20250617030815.5785-1-alexander.deucher@amd.com/T/#t

#AI from https://github.com/robertrosenbusch/gfx803_rocm/issues/35

<p data-start="0" data-end="708">**TL;DR — Your snippets <em data-start="24" data-end="29">are</em> useful: the repeated<br data-start="50" data-end="53">
<code data-start="53" data-end="104">[drm] scheduler comp_1.1.1 is not ready, skipping</code> lines in <code data-start="114" data-end="128">/tmp/gpu.log</code> point to an <strong data-start="141" data-end="172">amdgpu ring-scheduler stall</strong>, a failure the kernel raises when the compute queue on Polaris-class GPUs (RX 470/480/570/580, ID 0x67DF) stops making forward progress. This is almost always a driver/firmware regression, power-management corner case or ROCm-compute quirk rather than an outright hardware defect. Below you’ll find (1) what the message means, (2) the most common root-causes on Arch, (3) quick checks you can run right now, (4) a “safe-bisect” recipe that won’t endanger your main install, and (5) longer-term options if the card itself is marginal.</p>
<hr data-start="710" data-end="713">
<h2 data-start="715" data-end="759">1  What the key log lines actually mean</h2>
<div class="_tableContainer_16hzy_1"><div tabindex="-1" class="_tableWrapper_16hzy_14 group flex w-fit flex-col-reverse">
Log line | Meaning | Why it matters
-- | -- | --
scheduler comp_1.1.1 is not ready, skipping | Kernel scheduler can’t wake the compute ring comp_1 after a job timeout. | GPU is wedged; driver refuses to submit new work, causing the UI freeze you observed. bbs.archlinux.org
amdgpu_job_timedout + GPU reset begin! | Kernel tried a soft reset of the affected ring. | If the reset also stalls, the card hard-locks and takes Xorg/Wayland with it. lore.kernel.org
Polaris10 / PCI ID 0x67DF | Confirms you are on a Polaris-class desktop card (RX 570/580). | Important because many newer ROCm builds and some recent kernels drop full Polaris support. techpowerup.com

</div></div>**TL;DR — Your snippets are useful: the repeated
[drm] scheduler comp_1.1.1 is not ready, skipping lines in /tmp/gpu.log point to an amdgpu ring-scheduler stall, a failure the kernel raises when the compute queue on Polaris-class GPUs (RX 470/480/570/580, ID 0x67DF) stops making forward progress. This is almost always a driver/firmware regression, power-management corner case or ROCm-compute quirk rather than an outright hardware defect. Below you’ll find (1) what the message means, (2) the most common root-causes on Arch, (3) quick checks you can run right now, (4) a “safe-bisect” recipe that won’t endanger your main install, and (5) longer-term options if the card itself is marginal.
1 What the key log lines actually mean
Log line	Meaning	Why it matters
scheduler comp_1.1.1 is not ready, skipping	Kernel scheduler can’t wake the compute ring comp_1 after a job timeout.	GPU is wedged; driver refuses to submit new work, causing the UI freeze you observed.
[bbs.archlinux.org](https://bbs.archlinux.org/viewtopic.php?id=302729&utm_source=chatgpt.com)
amdgpu_job_timedout + GPU reset begin!	Kernel tried a soft reset of the affected ring.	If the reset also stalls, the card hard-locks and takes Xorg/Wayland with it.
[lore.kernel.org](https://lore.kernel.org/all/bug-219895-2300-sna5i9njlR%40https.bugzilla.kernel.org%2F/?utm_source=chatgpt.com)
Polaris10 / PCI ID 0x67DF	Confirms you are on a Polaris-class desktop card (RX 570/580).	Important because many newer ROCm builds and some recent kernels drop full Polaris support.
[techpowerup.com](https://www.techpowerup.com/forums/threads/amd-rocm-4-5-drops-polaris-architecture-support.288864/?utm_source=chatgpt.com)
2 Why Polaris cards hit this bug in 2024

    Regression in 6.8/6.9 DRM scheduler – Several reports show the new out-of-order job logic mis-handles ring timeouts on GFX8 GPUs, producing the exact comp_1.* warning you see.
    bbs.archlinux.org
    shatsky.github.io

    ROCm ≥ 5.x no longer ships Polaris firmware – When a compute workload tries to initialise HIP/ROCm on an unsupported card the KFD layer wedges, leading to the stall.
    techpowerup.com

    Aggressive runtime-PM – The default amdgpu.runpm=1 path powers the card down between frames; on some boards it never wakes correctly after heavy load.

3 Quick triage steps (5 min each)

    Boot the LTS kernel (6.6-LTS on Arch) – Many users confirm 6.6 does not trigger the comp_1 stall.

    Disable runtime-PM for one session:

    sudo grub-editenv - set \"amdgpu.runpm=0 amdgpu.gpu_recovery=1\"

    → prevents the card from fully powering down and enables early ring reset logic.
    bbs.archlinux.org

    Update Polaris firmware (pacman -S linux-firmware) – AMD pushed a new polaris10_k_smc.bin that fixes power-gate sequences.
    docs.kernel.org

    Stress-test underclock vs. default – If a mild core/mem down-clock stops the stall, the issue is voltage-margin rather than software.
    github.com

    Confirm no ROCm workloads – rocm-smi --showpids; if anything is listed, kill it or install ROCm 4.5 (the last version that supports Polaris).
    techpowerup.com

If any single step eliminates the hang you’ve found the trigger; keep that workaround while you investigate a permanent fix.
4 Capturing better diagnostics
What to capture	How	Why
Verbose DRM trace	add drm.debug=0x1ff log_buf_len=4M on the kernel cmd-line	Gives per-ring timeline, invaluable when filing bugs.
kernel.org
Full GPU reset trace	`echo 'w'	sudo tee /sys/kernel/debug/dri/0/amdgpu_debugfs_gpu_reset` after a freeze
Power / temp history	watch -n1 rocm-smi -a or watch -n1 sensors	Over-temp throttling can masquerade as a scheduler hang.
lore.kernel.org



Investigating ROCm 6.4 Failures on GFX803 (Polaris RX580) with Linux 6.15.2
Overview of the Issue

Running ROCm 6.4 (via WhisperX/Ollama containers) on a Polaris GPU (AMD RX580, GFX803) under an Arch Linux kernel 6.15.2-arch1-1 (PREEMPT_DYNAMIC) has led to reproducible GPU failures. Users have reported frequent segmentation faults in ROCm applications or sudden GPU resets, especially when using Docker containers for WhisperX (ASR) or Ollama (LLM inference). These failures appear tightly linked to the kernel version – multiple community reports indicate that certain kernel versions cause /dev/kfd (the ROCm kernel driver interface) to crash, while others work reliably. In particular, Arch Linux’s 6.15.x kernel (also Fedora 41’s kernel in early 2025) was flagged as “suspicious” for such crashes. The goal of this investigation is to pinpoint the root cause (kernel bug, compatibility break, or configuration issue) and recommend a solution or workaround.
Symptoms and Confirmed Reports

Affected systems show segfaults when initializing HIP/ROCm programs or heavy GPU workloads. For example, launching the WhisperX container may terminate unexpectedly, and dmesg logs on the host show GPU reset messages or KFD errors. In some cases the GPU may hang and recover (or require driver reload). Notably, a maintainer of the GFX803 ROCm project observed that on certain kernels “the devices /dev/dri and /dev/kfd crashed with SegFaults” when running Ollama or PyTorch inside the container. The project’s documentation advises users to check their Linux kernel version and switch to a known-working version if they encounter these crashes.

Multiple community sources corroborate this kernel-dependent failure:

    Robert Rosenbusch’s gfx803_rocm repo: Provides Dockerfiles for ROCm on Polaris and includes a compatibility table. It notes that as of April 2025, Fedora 41, Arch, and Debian 13 were shipping kernels that trigger ROCm segfaults, and that kernels 6.12.x and later had a fix for this issue. In the table, kernels 6.13, 6.14, 6.15 were marked as tested/working for ROCm 6.3.4/6.4.0 on Polaris, whereas some earlier kernels were not. (This aligns with user feedback that upgrading above Linux 6.12.21 resolved their GPU crashes.) Despite the table showing 6.15 as “working,” real-world results on Arch 6.15.2 suggest otherwise – indicating that additional factors (or subsequent regressions) are at play.

    Reddit (Nobara/Fedora users): One RX 6800XT user reported that ROCm worked flawlessly on kernel 6.14.0 but completely broke starting with 6.14.1, causing hipinfo to fail and any HIP apps to crash. Rolling back to 6.14.0 immediately restored functionality. Others in the thread confirmed the same issue on RDNA2 GPUs and resorted to downgrading kernels (one even fell back to 6.11). Notably, this is an officially-supported GPU on ROCm, implying the problem is not due to Polaris hacks but a broader ROCm+kernel regression. Indeed, an issue filed on ROCm’s GitHub by an affected user states “ROCm completely stopped working after kernel 6.14.0-202, and we’re now on 6.15.1 and it still doesn’t work.”. AMD’s team acknowledged it (though curiously labeled it a “Feature Request”), confirming that something in the 6.14.x→6.15 kernels disrupted ROCm on Linux.

    Docker/Frigate issue: In a related context, users running AMD GPUs in containers (e.g. for Frigate CCTV or Stable Diffusion) have encountered amdgpu crashes with newer kernels. One GitHub issue describes ROCm usage in Docker leading to amdgpu resets, which might be the same class of problem. This reinforces that the kernel’s amdgpu/AMDKFD drivers are the common denominator in these failures.

Symptoms in logs: When the failure occurs, you may see in dmesg output lines such as amdgpu: GPU reset begin... followed by a GPU halt and recovery sequence, or amdkfd: Failed to initialize queue errors. In some cases (especially if the process segfaults quickly), you might only see an HSA user-space error (e.g. a HIP runtime exception) and a generic segfault at IP… in syslog. Checking dmesg for KFD errors or GPU hangs is crucial. One user hint is to run dmesg | grep -i kfd – if there’s an issue like missing PCIe atomics (see next section) or a driver bug, it often appears there. For instance, failing to open /dev/kfd can log “Unable to open /dev/kfd read-write: Bad address” if prerequisites aren’t met.
Kernel Changes Impacting ROCm (Root Cause)

The timing of these regressions strongly suggests a kernel-side bug or interface change in the Linux 6.14 series. During the 6.14 development cycle, AMD’s graphics driver team made significant updates to the AMDGPU and AMDKFD components. A review of kernel patches reveals at least one fix directly relevant to GFX8 (Polaris): “drm/amdkfd: Fix user queue validation on Gfx7/8”. This patch, authored by AMD engineer Philip Yang, landed in Linux 6.14.0 and addresses how the kernel validates user-mode queues for GFX7/GFX8 GPUs. In practical terms, prior to this fix the KFD driver likely mis-identified or rejected compute queues on Polaris, which could cause segmentation faults when ROCm programs try to create GPU queues or submit work. It’s plausible that kernels before 6.14 had a bug causing Polaris-specific crashes in ROCm, and that 6.14.0 officially fixed that issue. This aligns with the gfx803_rocm maintainer’s note that “on Kernel version 6.12 it seems to be fixed” – in fact the fix was merged by 6.14, but might have been backported to some 6.12.x stable updates or simply observed by users once they jumped to 6.13/6.14.

However, the story doesn’t end there. The new breakage in 6.14.1+ (impacting even RDNA2) suggests that another change came with a stable update or in 6.15. Between 6.14.0 and 6.14.1, some modifications (perhaps to memory management or reset behavior) were introduced. Indeed, looking at the stable kernel changelogs: in Linux 6.14.9 there’s a fix for “amdkfd: Fix error handling for missing PASID in kfd_process_device_init_vm” and another for a “mode1 reset crash” in KFD. These hints imply that initial 6.14 code had issues with GPU VM initialization and reset handling. A PASID is a Process Address Space ID used by KFD; if the kernel erroneously handled a missing PASID, ROCm calls might crash or fail. The “mode1 reset” refers to GPU reset procedure – a bug there could easily cause unstable behavior when a GPU hang occurs. AMD did issue fixes for these in the stable series. By kernel 6.15.2 (the Arch version in question), one would expect those patches to be included (since 6.15 would incorporate 6.14 stable fixes). Yet, the ROCm failure persists on 6.15.2 for Polaris, likely because the user-space ROCm stack (6.4.0) hasn’t adapted to some kernel changes. In other words, even though the kernel might have fixed its internal bugs, it may have changed an interface or behavior that ROCm 6.4 wasn’t expecting, leading to a mismatch until ROCm is updated. AMD’s own response on the issue was that this might be resolved in a future ROCm release that aligns with the newer kernels (the user speculated ROCm 6.5 with Radeon 7000 support might solve it).

To summarize the root cause:

    Polaris support was broken in older kernels (possibly anything between 5.19 and 6.13) due to a KFD queue validation bug. This caused segfaults when using ROCm on GFX803 unless a patch or newer kernel was used. Kernel 6.14.0 introduced a fix for this.
    A regression for all ROCm GPUs appeared in kernel 6.14.1 (and persisted through 6.15), likely related to KFD’s VM/pasid management. This made ROCm user-space calls (HIP, OpenCL) fail or crash on otherwise supported devices. The kernel stable updates have addressed some of these issues by 6.15.x, but full functionality might require ROCm 6.4.1+ user-space to match. (ROCm 6.4.1 was released in May 2025, primarily adding RDNA4 support, but its release notes do not explicitly mention a fix for this issue – it’s something to watch in change logs of ROCr/HIP runtime components.)

Another kernel-related consideration is the introduction of GPU reset recovery. Linux kernels in recent years have improved AMDGPU’s ability to reset a hung GPU without rebooting the system. In fact, the reset-recovery code was enabled by default on many GPUs (Polaris included) around this time. This means on 6.15, if the RX580 encounters a computation hang, the driver will attempt a soft reset of the card. While generally positive, this could manifest to the user as a momentary freeze or error, whereas on older kernels the process might have just hung or died silently. The Phoronix coverage noted that GPU reset support was being flipped “on” by default for Polaris family GPUs (GCN4) after testing showed it works “for the most part”. It’s possible that under heavy load (e.g. running large WhisperX models or stable diffusion in ComfyUI), Polaris is more prone to hangs, and with resets enabled, the kernel will log a GPU reset and the ROCm runtime might see a device loss. If these resets happen frequently on 6.15, it could be perceived as instability. Undervolting/overclock settings can exacerbate this – indeed one user found their long-stable RX6000 undervolt became unstable on 6.15 (pointing to changes in power management in the driver). In short, kernel 6.15’s amdgpu driver might be less forgiving to any GPU instability, causing more frequent resets on Polaris.

Lastly, the PREEMPT_DYNAMIC kernel feature in use shouldn’t directly break ROCm, but it’s worth noting. PREEMPT_DYNAMIC allows the kernel to switch between full preemption and voluntary preemption modes at runtime. There are no known ROCm-specific issues with dynamic preemption in Linux 6.15; however, because it alters scheduling, it’s theoretically possible that timing-sensitive bugs (races in driver or user code) could surface. No evidence in our research points to PREEMPT_DYNAMIC as a root cause, so we do not suspect it here. (If needed, one could test a standard PREEMPT=none kernel to rule it out, but again, the widespread reports implicating specific kernel versions suggest it’s a code issue, not the preemption model.)
PCIe Atomics Requirement (Hardware Compatibility)

It’s important to confirm that the system itself meets ROCm’s hardware requirements, since Polaris GPUs are notorious in this regard. AMD ROCm requires PCI Express Atomics (a feature of PCIe 3.0) to be supported by both the CPU and motherboard/chipset for all GPUs GFX8 and newer. Polaris (RX 570/580) does support PCIe atomics at the GPU level, but if your platform (e.g., older Intel CPUs or consumer motherboards with limited firmware) doesn’t advertise this capability, the ROCm driver will refuse to initialize the GPU for computing. The error for this in dmesg is typically something like: “amdkfd: skipped device bus:device because PCIe atomics not supported” or the rocminfo output failing with “Unable to open /dev/kfd read-write: Bad address”.

Given that you have been running WhisperX/Ollama, you likely have already cleared this hurdle (otherwise ROCm wouldn’t have worked at all). But if the segfaults are happening very early (e.g., even rocminfo crashes), double-check that in your BIOS “Above 4G Decoding” or “Enable PCIe atomics” is turned on. On consumer motherboards, enabling 64-bit BAR support (4G decoding) is often necessary for atomics to function. You can verify support by running dmesg | grep -i atomic – successful initialization will log something about atomics enabled. As the ROCm GitHub issue #1205 succinctly states: “gfx803 (RX580) need PCIe Atomic support with both CPU and MotherBoard” – lacking this will cause a hard failure on opening /dev/kfd. This is not a software bug per se, but a requirement. (Atomics have been required since ROCm 1.x; Polaris was officially supported up to ROCm 4.3 provided this was in place.) In our context, since the containers did run and only started crashing on a new kernel, the PCIe setup is probably fine – the issue is software. But it’s worth mentioning to ensure no stone is left unturned.
GCC 15 and ABI Compatibility Concerns

Your environment features GCC 15.1.1 (as on Arch or bleeding-edge Fedora). Such a new compiler can introduce two types of problems: (1) compiling the ROCm software stack (or PyTorch, etc.) with it may require code changes, and (2) ABI mismatches if binaries were built with older compiler assumptions. Let’s break down the impact:

    Building ROCm/PyTorch with GCC 15: GCC 15 is a major update and has changes in the C++ standard library and default flags that affected ROCm code. A concrete example is libstdc++ enabling _GLIBCXX_ASSERTIONS by default on some distros. This inserts runtime bounds-checking asserts in container operations. When compiling device kernels for HIP, such asserts are not allowed (they call host functions). Indeed, when PyTorch was compiled for ROCm on Fedora 42 (with GCC 15), it triggered compile-time errors in HIP kernels – e.g. reference to host function '__glibcxx_assert_fail' in device function in ROCm’s OffsetCalculator.cuh. Essentially, GCC15’s std::array operator[] began calling an assert, which the HIP compiler caught as illegal. A PyTorch developer opened an issue about this, and it requires either disabling those debug asserts or updating the code to avoid triggering them. This kind of issue is likely to affect any ROCm component built from source with GCC 15: portions of HIP runtime, ROCm libraries, or even the LLVM-based ROCm compiler might need small fixes. Linux distributions have begun applying patches – for instance, Gentoo/Redcore Linux added a patch to update PyTorch’s bundled fmt library to v11 to fix GCC 15 build errors (since older fmt code wasn’t GCC15-compatible). If your Docker build is based on Ubuntu 24.04 (which probably uses GCC 13 or 14), you might not hit these compile issues inside the container. But if you ever rebuild ROCm or PyTorch on the host with GCC 15, be prepared for potential breaks until upstream addresses them. The key point: GCC 15 is new, and ROCm 6.4/PyTorch 2.4 were not developed against it, so minor build failures or warnings (treated as errors) can occur. These manifest at compile time, not as runtime segfaults, so they’re a secondary concern here.

    Kernel modules and GCC 15: The Linux kernel itself was compiled with GCC 15 in your case (Arch). Normally, this is fine – kernel and driver code is regularly updated for new compiler versions. AMD’s out-of-tree amdgpu-dkms module (used on Ubuntu for proprietary driver stacks) did fail to build on 6.13+ kernels – but that was due to code changes in the kernel, not the compiler. As long as you use the in-tree amdgpu (which Arch does), this isn’t an issue. No known ABI break was introduced by GCC 15 for the kernel <-> userland ROCm interface. (If anything, the break came from the kernel source changes, as discussed.) Therefore, we do not suspect that GCC 15 on the host is causing the runtime segfaults directly. The segmentation faults are occurring within ROCm/HIP runtime in user space, rather than symbol linkage errors or C++ ABI mismatches (those would typically cause compile or link errors, not segfaults at runtime for an already-built container).

In summary, GCC 15 primarily impacts developers building ROCm/PyTorch: you may need patches to compile successfully. It’s wise to use distro packages or containers for these big projects to avoid toolchain headaches on Arch. The Arch community repositories as of early 2025 were still on ROCm 6.2.4 (with PyTorch 2.1) partly due to the rapid changes – moving to 6.4 requires ensuring all these new compiler issues are resolved. Arch packagers or AUR maintainers might include fixes (for example, patching ROCm’s rocm-core or hipblt for GCC 15 if needed). If you encounter build problems, searching the Arch forums or GitHub for the specific error is recommended; chances are someone submitted a patch or PKGBUILD tweak. For the scope of this failure though, GCC 15 is not the culprit of the segfaults, but rather the kernel behavior is.
Workarounds and Recommendations
1. Use a Known Good Kernel Version

Downgrading the kernel is the most straightforward way to restore stability in the short term. All evidence points to kernel 6.15 (and late 6.14) being problematic, whereas earlier 6.12–6.13 and some LTS kernels are stable with ROCm:

    The GFX803 community suggests that Linux 6.9 through 6.12 were reliably working with ROCm 6.3.4/6.4.0 on Polaris. In fact, many users had success once they moved off the “bad” kernel. In your case, since you’re on Arch, you have access to the linux-lts package (which as of 2025 is likely tracking 6.1.x LTS). Kernel 6.1 LTS is older than the 6.14 regression and should be free of that issue. It may not include the Polaris queue fix that 6.14 had, but interestingly some users report ROCm worked on 6.1 for them – possibly because AMD never officially supported Polaris beyond ROCm 4.x, the newer queue feature might not be exercised in the same way. If you do try 6.1 LTS and still see segfaults on Polaris, then the queue fix patch might be missing there; in that case, going to 6.12.19 (the last 6.12 stable, if available) or 6.13.x could be an option. Arch doesn’t provide those older kernels pre-packaged, but you can compile a custom kernel or use the linux-mainline AUR for testing specific versions.

    For a quick test, consider booting into an Arch Linux LTS kernel (6.1). Ensure you also install matching kernel headers if needed by the container (usually not required, since the container uses user-space only). Users have reported that using an older kernel immediately fixed ROCm failures – e.g. Nobara (Fedora) users locked to 6.14.0 to keep ROCm running, and one went back to the 6.11 series with success. These versions predate whatever interface change broke ROCm.

    Looking forward, keep an eye on Linux 6.16+. It’s possible that by 6.16 or 6.17, AMD and the kernel community addressed the ROCm regression. For instance, there was mention that AMDKFD fixes were submitted during the 6.16 merge window (including support for new hardware and presumably bug fixes). Upgrading to 6.16 (once it’s stable) might resolve the issue without needing a permanent downgrade – but only test this after confirming a stable baseline on a known-good kernel. In other words, first get a working config (so you know how it behaves when fixed), then experiment with newer kernels to see if the fix has landed.

    Why not stay on 6.15? At the moment, 6.15.x requires a matching ROCm userland that isn’t out yet (ROCm 6.5 perhaps). Unless you have a pressing reason to use 6.15 (new hardware or feature), it’s safer to avoid it for ROCm on Polaris. The Arch kernel will move on fairly quickly anyway (6.16 will replace it in a few weeks given the kernel release cadence). So this is a temporary regression window to sidestep.

2. Patch or Rebuild ROCm Components (Advanced)

If kernel downgrade is not desirable, another approach is to try and rebuild the ROCm runtime from source with patches that make it compatible with newer kernels. This is non-trivial, but here are some pointers:

    AMD’s ROCm GitHub has the source for the runtime (ROCR), HIP, etc. If the issue is in user-space (e.g., assuming an old PASID handling), a patch could potentially be applied there. However, given that even RDNA2 users were affected, it suggests the user-space needed changes that likely only AMD knows in detail. Without an official patch from AMD, this path is guesswork.

    One thing you can do is run a simple ROCm program under gdb to see where it segfaults. For example, inside the container: HIP_VISIBLE_DEVICES=0 /opt/rocm/bin/rocminfo (or the WhisperX initialization) under gdb. A common point of failure could be at HSA queue creation or memory allocation. If it’s a null-pointer dereference in the ROCm user library, that confirms a software bug that might be worked around.

    Considering Polaris is unofficial, the community-maintained Docker already rebuilds many pieces (HIP, rocBLAS, PyTorch) to add GFX803 support. It’s possible the maintainers will update their Dockerfiles if a known fix emerges. Check the robertrosenbusch/gfx803_rocm issues for any mention of 6.15 – as of mid-June 2025, new issues (

https://github.com/robertrosenbusch/gfx803_rocm/issues/35,

    https://github.com/robertrosenbusch/gfx803_rocm/issues/36) were opened by users about container instability. The maintainer might respond with kernel-related advice or even a code workaround.

    Container runtime settings: Ensure you’re already using the recommended flags when launching the container. From the gfx803_rocm guide, the correct invocation is, for example:

    docker run -it --device=/dev/kfd --device=/dev/dri --group-add video \
               --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
               --name rocm64_whisperx ...

    This grants the container access to the GPU computing device and disables seccomp filtering and IPC isolation, which is needed for ROCm/HIP to function. If any of these options were missing, it could cause failures. (Your description indicates you did use --device and group video – just double-check all flags match the above.)

    Environment variables: Some environment tweaks can improve stability on the margin. For Polaris, one known quirk is limited SDMA engines (DMA copy engines). If you suspect issues during large data transfers, you can try disabling SDMA in ROCm by setting:

    export HSA_ENABLE_SDMA=0

    inside the container before running the workload. This forces ROCm to use PCIe for transfers instead of the GPU’s DMA engines. It might avoid certain hangs at the cost of performance. Another var is HSA_NO_SCRATCH_RECLAIM=1, which disables a memory optimization that sometimes causes problems on smaller VRAM GPUs. These are not guaranteed fixes for the segfault, but they are safe to experiment with and have helped in some ROCm scenarios. Also, since you use PyTorch in WhisperX, setting MIOPEN_LOG_LEVEL=3 will suppress benign warnings (unrelated to crashes, but cleans the log).

    Use ROCm 5.4.3 as a fallback: If nothing in ROCm 6.x will run on your setup with newer kernels, an alternative is to run the older ROCm stack that officially supported Polaris (ROCm 4.3 or the community-continued 5.4.x for GFX8). For example, Sunjay’s blog and others provided Docker images for ROCm 5.4.2 on Polaris. These might not have the latest features but could be more stable. However, mixing that with WhisperX/Ollama (which likely require newer PyTorch and HIP) may be infeasible. Thus, this is a last resort for basic OpenCL or older PyTorch models.

3. Reporting and Escalation

Since this issue spans kernel and ROCm user-space, you’ll want to escalate it through multiple channels to ensure it gets the necessary attention:

    Upstream Linux kernel: A bug that causes crashes or resets on supported GPUs (even though Polaris isn’t officially supported, the RX 6800XT case shows supported hardware is affected) should be reported to the kernel developers. The proper venue is the [[kernel bug tracker on kernel.org](https://bugzilla.kernel.org/enter_bug.cgi?product=Drivers&component=DRM/AMD)](https://bugzilla.kernel.org/enter_bug.cgi?product=Drivers&component=DRM/AMD) or the amd-gfx mailing list. Provide a clear description that “ROCm workloads crash on kernels 6.14.1+” and include logs. Key data to attach: the output of dmesg around the failure (with AMDGPU and KFD messages), the exact kernel version, and steps to reproduce (for instance, “run rocminfo or start this public Docker image on a Polaris GPU”). Mention the specific commits if you know them – e.g., “possibly related to amdkfd user queue validation on GFX8 and subsequent PASID handling changes.” Kernel developers respond well to regressions that are bisected; if you have the time, performing a bisection between 6.14.0 and 6.14.1 could identify the offending patch. But even without that, linking to the public reports (Reddit/GitHub issues) like the Nobara user’s experience helps validate the problem. Since this might have been fixed in code already (just not in your user-space), the kernel devs might say “update your ROCm” – but it’s still useful to ensure they’re aware if any kernel bug is lurking.

    ROCm GitHub and AMD support: You’ve seen one issue (#4919) already filed on the ROCm GitHub. It wouldn’t hurt to add your information there – especially that you’re using Polaris, which adds another dimension. (They may not officially support it, but if the root problem is same, it’s still data.) If no one has filed a bug report on the AMD Community forums or Fedora Bugzilla for this, consider doing so. For Fedora, since ROCm 6.3.1 is packaged, a bug report could be filed in Red Hat Bugzilla under the ROCm component or the kernel component. Fedora maintainers might coordinate with AMD on a backported fix or at least document the issue for F42 release notes. Arch Linux, being community-driven, has an [[Arch Bug Tracker](https://bugs.archlinux.org/)](https://bugs.archlinux.org/) – you could open an issue under “Community Packages” for rocm or even under “Kernel” since it’s a kernel regression. Arch devs might not do much beyond possibly adding a warning in the package or forum post, but it alerts Arch users to the problem.

    Issue priority and follow-up: The fact that AMD labeled the GitHub issue a feature request suggests they might be rolling any fix into the next ROCm release rather than patching 6.4.x. That means we could expect ROCm 6.5 (or an hypothetical 6.4.2) to work properly with kernels ≥6.15. It’s worth watching the ROCm release notes and testing new versions when they drop. In the meantime, by reporting to the above channels, you ensure the problem isn’t forgotten. If you do report to kernel or distro, include references (for traceability) to others hitting the same issue – e.g., Debian bug #1093124 was apparently filed for Polaris ROCm and got resolved by the GFX8 queue patch. Mentioning that in your report shows prior art. Likewise, cite the Nobara/Fedora experiences so maintainers see it’s a cross-distro issue.

    Collecting logs and info for reports: You asked about log formatting – here are some tips:
        Use dmesg -T > kernel_log.txt after a crash to get human-readable timestamps in the log. Trim that to the relevant portion (grep for amdgpu or kfd to find the errors). Attach this log to any bug report.
        Run /opt/rocm/bin/rocminfo and /opt/rocm/bin/hipinfo (if available in the container) and capture their output. Even if they segfault, sometimes they print some info first. This helps identify ROCm version, HSA driver version, etc.
        State your exact GPU model and driver in use. For instance: “AMD Radeon RX 580 (Polaris10, gfx803), using upstream amdgpu driver (LLVM 16 for shader compiler, firmware from linux-firmware 2025-01-10, etc).” You can get some of this from dmesg (look for “Virtual CRAT table created for GPU” which indicates KFD enabled the GPU, and “amdgpu: Topology: Add dGPU node [0x67df:…]” which identifies the chip).
        If you managed to capture a stack trace from the segfault (e.g., using gdb or from /var/log/core with coredump), include that. It could show if the crash is in libhsa-runtime64.so or libhip.so etc., and what call might be failing.
        Emphasize the reproduction steps: for example, “Start the WhisperX container and load a model, or run a simple HIP sample like vector_copy.” The easier you can make it for maintainers to reproduce the issue, the faster it will get addressed. Since not everyone has an RX580 on hand, they may try with a similar GFX8 card or even an RX6800 to see if any crash occurs.

4. Container-Specific Workaround

If you absolutely must continue using kernel 6.15 (say, due to other hardware requiring it) and cannot wait for a fix, one approach is to run a VM or container that encapsulates an older kernel. For example, you could use something like Docker with --privileged to run a lightweight VM (with KVM) that has Ubuntu 22.04 and a 5.x kernel, passing through the GPU. This is complex and not always worth it, but technologies like Kata Containers or even just running a second OS in a dual-boot might be considered. Most would find it easier to simply downgrade the host kernel, but I mention this for completeness.

In the context of Docker, ensure you’re using the updated images from the gfx803_rocm project. The maintainer recently uploaded pre-built images for the base and WhisperX containers to Docker Hub (issues https://github.com/robertrosenbusch/gfx803_rocm/issues/34 and https://github.com/robertrosenbusch/gfx803_rocm/issues/35 hint at that). Using those might save you build time and potentially include minor fixes. Always match the container’s expectation with the host: the host kernel must have /dev/kfd support and GPU drivers loaded – which you do – and the container’s ROCm stack version should not greatly exceed the host driver’s capabilities. (ROCm generally maintains backwards compatibility in user-space vs kernel, but there are limits.)
Conclusion

Root Cause Summary: The failures are caused by a combination of kernel regressions in Linux 6.14/6.15 affecting the AMD GPU compute driver (AMDKFD) and the fact that ROCm 6.4’s user-space isn’t aligned with those kernel changes. Polaris (gfx803) users were additionally hampered by historically missing support that was only recently patched in the kernel. The net effect under kernel 6.15.2 is that ROCm workloads trigger segfaults or GPU resets, whereas stable operation can be achieved on certain earlier kernels. GCC 15 and PREEMPT_DYNAMIC are ancillary factors – important for development and performance, but not the direct cause of the crashes. The fundamental issue lies in the kernel-driver <-> user-space ROCm interface.

Recommended Action: Run a kernel version known to work (e.g. downgrade to 6.12.x or 6.14.0, or use Arch’s 6.1 LTS), and/or await an update from AMD (ROCm 6.5 or a patched 6.4.x) that explicitly fixes compatibility with >6.14 kernels. In parallel, report the issue through appropriate channels (kernel bugzilla, Fedora/Arch bug trackers, ROCm GitHub) with logs to help expedite a permanent fix. By doing so, you not only solve your immediate problem by using a compatible kernel, but also contribute to the resolution for all users in the long run.

Environment Setup to Reproduce: To aid others in reproducing or debugging this, document your environment as follows:

    Distro/Kernel: “Arch Linux, kernel 6.15.2-arch1-1, CONFIG_PREEMPT_DYNAMIC=y (using default dynamic preemption).”
    GPU: “AMD RX 580 (Polaris 20, GFX803), 8GB VRAM, connected via PCIe 3.0 x16, motherboard supports atomics = yes.”
    ROCm Container: “Docker image rocm64_gfx803_whisperx:latest (based on Ubuntu 24.04, ROCm 6.4.0 userland, PyTorch 2.6.0 built for gfx803). Run with --device=/dev/kfd --device=/dev/dri --group-add video etc.”
    Reproduce by: “Inside container, run WhisperX’s transcription on a sample audio, or simply execute /opt/rocm/bin/rocminfo. Expected: rocminfo lists device. Observed: Segmentation fault (core dumped) after printing GPU name, accompanied by kernel log messages about KFD or a GPU reset.”

Such a block of information in a bug report will be extremely useful for developers to trace the problem.
Sources

    AMD GFX803 ROCm project documentation (Robert Rosenbusch) – notes on kernel version stability
    User reports on Reddit (r/NobaraProject) – confirmation that ROCm fails on 6.14.1+ and works on 6.14.0, user workarounds by downgrading
    Issue report on ROCm GitHub – “ROCm stopped working after 6.14.0, still broken on 6.15.1”
    Linux kernel commit logs (LWN.net) – fix for GFX7/GFX8 in amdkfd and references to KFD fixes in stable series
    AMD ROCm documentation / community notes – requirement of PCIe 3.0 + atomics for GFX8 GPUs
    PyTorch issue tracker – build failures of ROCm components with GCC 15 (libstdc++ assertions)
    Gfx803_rocm Docker guide – showing container run flags and notes on rebuilding PyTorch/rocBLAS for Polaris.

---

### 评论 #4 — chboishabba (2025-06-20T01:53:06Z)

https://chatgpt.com/share/6854bef2-c69c-8002-a243-a06c67a2c066

[rocminfo.txt](https://github.com/user-attachments/files/20827777/rocminfo.txt)

[gpu-live-6.15.2-arch1-1.log](https://github.com/user-attachments/files/20827788/gpu-live-6.15.2-arch1-1.log)

[gpu.log](https://github.com/user-attachments/files/20827789/gpu.log)

[gpu.boot.log](https://github.com/user-attachments/files/20827790/gpu.boot.log)

---

### 评论 #5 — chboishabba (2025-06-20T05:02:41Z)

```
Jun 18 16:36:53 archb kernel: ACPI: bus type drm_connector registered
Jun 18 16:36:53 archb kernel: simple-framebuffer simple-framebuffer.0: [drm] Registered 1 planes with drm panic
Jun 18 16:36:53 archb kernel: [drm] Initialized simpledrm 1.0.0 for simple-framebuffer.0 on minor 0
Jun 18 16:36:53 archb kernel: simple-framebuffer simple-framebuffer.0: [drm] fb0: simpledrmdrmfb frame buffer device
Jun 18 16:36:53 archb kernel: [drm] amdgpu kernel modesetting enabled.
Jun 18 16:36:53 archb kernel: [drm] initializing kernel modesetting (POLARIS10 0x1002:0x67DF 0x1043:0x0519 0xE7).
Jun 18 16:36:53 archb kernel: [drm] register mmio base: 0xDFA00000
Jun 18 16:36:53 archb kernel: [drm] register mmio size: 262144
Jun 18 16:36:53 archb kernel: [drm] UVD is enabled in VM mode
Jun 18 16:36:53 archb kernel: [drm] UVD ENC is enabled in VM mode
Jun 18 16:36:53 archb kernel: [drm] VCE enabled in VM mode
Jun 18 16:36:53 archb kernel: [drm] vm size is 128 GB, 2 levels, block size is 10-bit, fragment size is 9-bit
Jun 18 16:36:53 archb kernel: [drm] Detected VRAM RAM=8192M, BAR=256M
Jun 18 16:36:53 archb kernel: [drm] RAM width 256bits GDDR5
Jun 18 16:36:53 archb kernel: [drm] amdgpu: 8192M of VRAM memory ready
Jun 18 16:36:53 archb kernel: [drm] amdgpu: 16029M of GTT memory ready.
Jun 18 16:36:53 archb kernel: [drm] GART: num cpu pages 65536, num gpu pages 65536
Jun 18 16:36:53 archb kernel: [drm] PCIE GART of 256M enabled (table at 0x000000F400300000).
Jun 18 16:36:53 archb kernel: [drm] Chained IB support enabled!
Jun 18 16:36:53 archb kernel: [drm] Found UVD firmware Version: 1.130 Family ID: 16
Jun 18 16:36:53 archb kernel: [drm] Found VCE firmware Version: 53.26 Binary ID: 3
Jun 18 16:36:53 archb kernel: [drm] Display Core v3.2.325 initialized on DCE 11.2
Jun 18 16:36:53 archb kernel: [drm] UVD and UVD ENC initialized successfully.
Jun 18 16:36:53 archb kernel: [drm] VCE initialized successfully.
Jun 18 16:36:53 archb kernel: amdgpu 0000:01:00.0: [drm] Registered 6 planes with drm panic
Jun 18 16:36:53 archb kernel: [drm] Initialized amdgpu 3.63.0 for 0000:01:00.0 on minor 1
Jun 18 16:36:53 archb kernel: fbcon: amdgpudrmfb (fb0) is primary device
Jun 18 16:36:53 archb kernel: amdgpu 0000:01:00.0: [drm] fb0: amdgpudrmfb frame buffer device
Jun 18 16:36:53 archb systemd[1]: Starting Load Kernel Module drm...
Jun 18 16:36:53 archb systemd[1]: modprobe@drm.service: Deactivated successfully.
Jun 18 16:36:53 archb systemd[1]: Finished Load Kernel Module drm.
Jun 18 16:38:09 archb kwin_wayland[2143]: No backend specified, automatically choosing drm
Jun 19 12:55:51 archb kernel: [drm] PCIE GART of 256M enabled (table at 0x000000F400300000).
Jun 19 12:55:51 archb kernel: [drm] UVD and UVD ENC initialized successfully.
Jun 19 12:55:51 archb kernel: [drm] VCE initialized successfully.
Jun 20 08:50:16 archb kernel: [drm] PCIE GART of 256M enabled (table at 0x000000F400300000).
Jun 20 08:50:16 archb kernel: amdgpu 0000:01:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring comp_1.1.1 test failed (-110)
Jun 20 08:50:16 archb kernel: [drm] UVD and UVD ENC initialized successfully.
Jun 20 08:50:16 archb kernel: [drm] VCE initialized successfully.
Jun 20 08:50:18 archb kernel: [drm] scheduler comp_1.1.1 is not ready, skipping
Jun 20 08:50:18 archb kernel: [drm] scheduler comp_1.1.1 is not ready, skipping
Jun 20 08:50:18 archb kernel: [drm] scheduler comp_1.1.1 is not ready, skipping
Jun 20 08:50:18 archb kernel: [drm] scheduler comp_1.1.1 is not ready, skipping
Jun 20 08:50:18 archb kernel: [drm] scheduler comp_1.1.1 is not ready, skipping
Jun 20 08:50:18 archb kernel: [drm] scheduler comp_1.1.1 is not ready, skipping

...

Jun 20 14:56:09 archb kwin_wayland[2143]: kwin_wayland_drm: atomic commit failed: Permission denied
Jun 20 14:56:09 archb kernel: [drm] scheduler comp_1.1.1 is not ready, skipping
```

```
/Whisper-WebUI/venv/lib/python3.12/site-packages/torch/cuda/memory.py:391: FutureWarning: torch.cuda.reset_max_memory_allocated now calls torch.cuda.reset_peak_memory_stats, which resets /all/ peak memory stats.
  warnings.warn(
HW Exception by GPU node-1 (Agent handle: 0x18c30940) reason :GPU Hang
```

on host
```
(Fri Jun 20 15:26:22) c@archb ~$ rocminfo
ROCk module is loaded


(Fri Jun 20 15:26:22) c@archb ~$ rocminfo
ROCk module is loaded
(hangs here)
^C^C^C^C^C^C^C^C^C
(continue hanging)
```

---

### 评论 #6 — chboishabba (2025-06-20T05:33:07Z)

```
(Fri Jun 20 15:31:53) c@archb ~$ sudo dmesg -w
[    0.000000] Linux version 6.14.0-rc4-bisect-01301-g0747acf33112 (c@archb) (gcc (GCC) 15.1.1 20250425, GNU ld (GNU Binutils) 2.44.0) #1 SMP PREEMPT_DYNAMIC Fri Jun 20 13:51:55 AEST 2025
[    0.000000] Command line: initrd=\7fb887b1d7f44e9d993f12e5d6b5967d\6.14.0-rc4-bisect-01301-g0747acf33112\initramfs-6.14.0-rc4-bisect-01301-g0747acf33112.img initrd=\7fb887b1d7f44e9d993f12e5d6b5967d\6.14.0-rc4-bisect-01301-g0747acf33112\initrd root=PARTUUID=89e4eb30-832d-4824-a82b-9e5f92d79936 zswap.enabled=0 rootflags=subvol=@ rw rootfstype=btrfs systemd.machine_id=7fb887b1d7f44e9d993f12e5d6b5967d
[    0.000000] BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x0000000000057fff] usable
[    0.000000] BIOS-e820: [mem 0x0000000000058000-0x0000000000058fff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000059000-0x000000000009dfff] usable
[    0.000000] BIOS-e820: [mem 0x000000000009e000-0x00000000000fffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x0000000087ad8fff] usable
[    0.000000] BIOS-e820: [mem 0x0000000087ad9000-0x0000000087b1cfff] ACPI NVS
[    0.000000] BIOS-e820: [mem 0x0000000087b1d000-0x0000000087efafff] usable
[    0.000000] BIOS-e820: [mem 0x0000000087efb000-0x0000000087efbfff] ACPI NVS
[    0.000000] BIOS-e820: [mem 0x0000000087efc000-0x0000000087efcfff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000087efd000-0x000000008f002fff] usable
[    0.000000] BIOS-e820: [mem 0x000000008f003000-0x000000008f49ffff] reserved
[    0.000000] BIOS-e820: [mem 0x000000008f4a0000-0x000000008f4d3fff] ACPI data
[    0.000000] BIOS-e820: [mem 0x000000008f4d4000-0x000000008f544fff] ACPI NVS
[    0.000000] BIOS-e820: [mem 0x000000008f545000-0x000000008fbfefff] reserved
[    0.000000] BIOS-e820: [mem 0x000000008fbff000-0x000000008fbfffff] usable
[    0.000000] BIOS-e820: [mem 0x000000008fc00000-0x000000008fffffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000e0000000-0x00000000efffffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fe000000-0x00000000fe010fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fed00000-0x00000000fed00fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fee00000-0x00000000fee00fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000ff000000-0x00000000ffffffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000100000000-0x000000086effffff] usable
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] APIC: Static calls initialized
[    0.000000] e820: update [mem 0x86bf4018-0x86c10e57] usable ==> usable
[    0.000000] e820: update [mem 0x86be3018-0x86bf3e57] usable ==> usable
[    0.000000] extended physical RAM map:
[    0.000000] reserve setup_data: [mem 0x0000000000000000-0x0000000000057fff] usable
[    0.000000] reserve setup_data: [mem 0x0000000000058000-0x0000000000058fff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000000059000-0x000000000009dfff] usable
[    0.000000] reserve setup_data: [mem 0x000000000009e000-0x00000000000fffff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000000100000-0x0000000086be3017] usable
[    0.000000] reserve setup_data: [mem 0x0000000086be3018-0x0000000086bf3e57] usable
[    0.000000] reserve setup_data: [mem 0x0000000086bf3e58-0x0000000086bf4017] usable
[    0.000000] reserve setup_data: [mem 0x0000000086bf4018-0x0000000086c10e57] usable
[    0.000000] reserve setup_data: [mem 0x0000000086c10e58-0x0000000087ad8fff] usable
[    0.000000] reserve setup_data: [mem 0x0000000087ad9000-0x0000000087b1cfff] ACPI NVS
[    0.000000] reserve setup_data: [mem 0x0000000087b1d000-0x0000000087efafff] usable
[    0.000000] reserve setup_data: [mem 0x0000000087efb000-0x0000000087efbfff] ACPI NVS
[    0.000000] reserve setup_data: [mem 0x0000000087efc000-0x0000000087efcfff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000087efd000-0x000000008f002fff] usable
[    0.000000] reserve setup_data: [mem 0x000000008f003000-0x000000008f49ffff] reserved
[    0.000000] reserve setup_data: [mem 0x000000008f4a0000-0x000000008f4d3fff] ACPI data
[    0.000000] reserve setup_data: [mem 0x000000008f4d4000-0x000000008f544fff] ACPI NVS
[    0.000000] reserve setup_data: [mem 0x000000008f545000-0x000000008fbfefff] reserved
[    0.000000] reserve setup_data: [mem 0x000000008fbff000-0x000000008fbfffff] usable
[    0.000000] reserve setup_data: [mem 0x000000008fc00000-0x000000008fffffff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000e0000000-0x00000000efffffff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000fe000000-0x00000000fe010fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000fed00000-0x00000000fed00fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000fee00000-0x00000000fee00fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000ff000000-0x00000000ffffffff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000100000000-0x000000086effffff] usable
[    0.000000] efi: EFI v2.6 by American Megatrends
[    0.000000] efi: ACPI 2.0=0x87ad9000 ACPI=0x87ad9000 SMBIOS=0x8fa67000 ESRT=0x89d22f98 MEMATTR=0x89d14018 RNG=0x8f4d3018 INITRD=0x87fcc798 
[    0.000000] random: crng init done
[    0.000000] efi: Remove mem36: MMIO range=[0xe0000000-0xefffffff] (256MB) from e820 map
[    0.000000] e820: remove [mem 0xe0000000-0xefffffff] reserved
[    0.000000] efi: Not removing mem37: MMIO range=[0xfe000000-0xfe010fff] (68KB) from e820 map
[    0.000000] efi: Not removing mem38: MMIO range=[0xfec00000-0xfec00fff] (4KB) from e820 map
[    0.000000] efi: Not removing mem39: MMIO range=[0xfed00000-0xfed00fff] (4KB) from e820 map
[    0.000000] efi: Not removing mem40: MMIO range=[0xfee00000-0xfee00fff] (4KB) from e820 map
[    0.000000] efi: Remove mem41: MMIO range=[0xff000000-0xffffffff] (16MB) from e820 map
[    0.000000] e820: remove [mem 0xff000000-0xffffffff] reserved
[    0.000000] SMBIOS 3.0 present.
[    0.000000] DMI: MSI MS-7A69/Z270M MORTAR (MS-7A69), BIOS 1.60 06/29/2018
[    0.000000] DMI: Memory slots populated: 2/4
[    0.000000] tsc: Detected 4200.000 MHz processor
[    0.000925] e820: update [mem 0x00000000-0x00000fff] usable ==> reserved
[    0.000926] e820: remove [mem 0x000a0000-0x000fffff] usable
[    0.000932] last_pfn = 0x86f000 max_arch_pfn = 0x400000000
[    0.000935] MTRR map: 4 entries (3 fixed + 1 variable; max 23), built from 10 variable MTRRs
[    0.000936] x86/PAT: Configuration [0-7]: WB  WC  UC- UC  WB  WP  UC- WT  
[    0.001213] last_pfn = 0x8fc00 max_arch_pfn = 0x400000000
[    0.010521] esrt: Reserving ESRT space from 0x0000000089d22f98 to 0x0000000089d22fd0.
[    0.010524] e820: update [mem 0x89d22000-0x89d22fff] usable ==> reserved
[    0.010535] Using GB pages for direct mapping
[    0.011012] Secure boot disabled
[    0.011013] RAMDISK: [mem 0x2df5b000-0x4a01cfff]
[    0.011127] ACPI: Early table checksum verification disabled
[    0.011129] ACPI: RSDP 0x0000000087AD9000 000024 (v02 ALASKA)
[    0.011131] ACPI: XSDT 0x0000000087AD90B0 0000DC (v01 ALASKA A M I    01072009 AMI  00010013)
[    0.011135] ACPI: FACP 0x0000000087B01FA8 000114 (v06 ALASKA A M I    01072009 AMI  00010013)
[    0.011138] ACPI: DSDT 0x0000000087AD9220 028D84 (v02 ALASKA A M I    01072009 INTL 20160422)
[    0.011141] ACPI: FACS 0x000000008F544D80 000040
[    0.011142] ACPI: APIC 0x0000000087B020C0 0000BC (v03 ALASKA A M I    01072009 AMI  00010013)
[    0.011144] ACPI: FPDT 0x0000000087B02180 000044 (v01 ALASKA A M I    01072009 AMI  00010013)
[    0.011146] ACPI: FIDT 0x0000000087B021C8 00009C (v01 ALASKA A M I    01072009 AMI  00010013)
[    0.011147] ACPI: MCFG 0x0000000087B02268 00003C (v01 ALASKA A M I    01072009 MSFT 00000097)
[    0.011149] ACPI: SSDT 0x0000000087B022A8 0003A3 (v01 SataRe SataTabl 00001000 INTL 20160422)
[    0.011151] ACPI: SSDT 0x0000000087B02650 003176 (v02 SaSsdt SaSsdt   00003000 INTL 20160422)
[    0.011153] ACPI: SSDT 0x0000000087B057C8 0025A5 (v02 PegSsd PegSsdt  00001000 INTL 20160422)
[    0.011155] ACPI: HPET 0x0000000087B07D70 000038 (v01 INTEL  KBL      00000001 MSFT 0000005F)
[    0.011156] ACPI: SSDT 0x0000000087B07DA8 000DE5 (v02 INTEL  Ther_Rvp 00001000 INTL 20160422)
[    0.011158] ACPI: SSDT 0x0000000087B08B90 000A2D (v02 INTEL  xh_rvp08 00000000 INTL 20160422)
[    0.011160] ACPI: UEFI 0x0000000087B095C0 000042 (v01 ALASKA A M I    00000002      01000013)
[    0.011162] ACPI: SSDT 0x0000000087B09608 000EDE (v02 CpuRef CpuSsdt  00003000 INTL 20160422)
[    0.011164] ACPI: LPIT 0x0000000087B0A4E8 000094 (v01 INTEL  KBL      00000000 MSFT 0000005F)
[    0.011165] ACPI: SSDT 0x0000000087B0A580 000141 (v02 INTEL  HdaDsp   00000000 INTL 20160422)
[    0.011167] ACPI: SSDT 0x0000000087B0A6C8 00029F (v02 INTEL  sensrhub 00000000 INTL 20160422)
[    0.011169] ACPI: SSDT 0x0000000087B0A968 003002 (v02 INTEL  PtidDevc 00001000 INTL 20160422)
[    0.011171] ACPI: SSDT 0x0000000087B0D970 000517 (v02 INTEL  TbtTypeC 00000000 INTL 20160422)
[    0.011172] ACPI: DBGP 0x0000000087B0DE88 000034 (v01 INTEL           00000002 MSFT 0000005F)
[    0.011174] ACPI: DBG2 0x0000000087B0DEC0 000054 (v00 INTEL           00000002 MSFT 0000005F)
[    0.011176] ACPI: VFCT 0x0000000087B0DF18 00E884 (v01 ALASKA A M I    00000001 AMD  31504F47)
[    0.011178] ACPI: BGRT 0x0000000087B1C7A0 000038 (v01 ALASKA A M I    01072009 AMI  00010013)
[    0.011180] ACPI: WSMT 0x0000000087B1C7D8 000028 (v01 ALASKA A M I    01072009 AMI  00010013)
[    0.011181] ACPI: Reserving FACP table memory at [mem 0x87b01fa8-0x87b020bb]
[    0.011182] ACPI: Reserving DSDT table memory at [mem 0x87ad9220-0x87b01fa3]
[    0.011183] ACPI: Reserving FACS table memory at [mem 0x8f544d80-0x8f544dbf]
[    0.011183] ACPI: Reserving APIC table memory at [mem 0x87b020c0-0x87b0217b]
[    0.011184] ACPI: Reserving FPDT table memory at [mem 0x87b02180-0x87b021c3]
[    0.011184] ACPI: Reserving FIDT table memory at [mem 0x87b021c8-0x87b02263]
[    0.011184] ACPI: Reserving MCFG table memory at [mem 0x87b02268-0x87b022a3]
[    0.011185] ACPI: Reserving SSDT table memory at [mem 0x87b022a8-0x87b0264a]
[    0.011185] ACPI: Reserving SSDT table memory at [mem 0x87b02650-0x87b057c5]
[    0.011186] ACPI: Reserving SSDT table memory at [mem 0x87b057c8-0x87b07d6c]
[    0.011186] ACPI: Reserving HPET table memory at [mem 0x87b07d70-0x87b07da7]
[    0.011186] ACPI: Reserving SSDT table memory at [mem 0x87b07da8-0x87b08b8c]
[    0.011187] ACPI: Reserving SSDT table memory at [mem 0x87b08b90-0x87b095bc]
[    0.011187] ACPI: Reserving UEFI table memory at [mem 0x87b095c0-0x87b09601]
[    0.011188] ACPI: Reserving SSDT table memory at [mem 0x87b09608-0x87b0a4e5]
[    0.011188] ACPI: Reserving LPIT table memory at [mem 0x87b0a4e8-0x87b0a57b]
[    0.011189] ACPI: Reserving SSDT table memory at [mem 0x87b0a580-0x87b0a6c0]
[    0.011189] ACPI: Reserving SSDT table memory at [mem 0x87b0a6c8-0x87b0a966]
[    0.011189] ACPI: Reserving SSDT table memory at [mem 0x87b0a968-0x87b0d969]
[    0.011190] ACPI: Reserving SSDT table memory at [mem 0x87b0d970-0x87b0de86]
[    0.011190] ACPI: Reserving DBGP table memory at [mem 0x87b0de88-0x87b0debb]
[    0.011191] ACPI: Reserving DBG2 table memory at [mem 0x87b0dec0-0x87b0df13]
[    0.011191] ACPI: Reserving VFCT table memory at [mem 0x87b0df18-0x87b1c79b]
[    0.011192] ACPI: Reserving BGRT table memory at [mem 0x87b1c7a0-0x87b1c7d7]
[    0.011192] ACPI: Reserving WSMT table memory at [mem 0x87b1c7d8-0x87b1c7ff]
[    0.011280] No NUMA configuration found
[    0.011280] Faking a node at [mem 0x0000000000000000-0x000000086effffff]
[    0.011285] NODE_DATA(0) allocated [mem 0x86efd52c0-0x86effffff]
[    0.011421] Zone ranges:
[    0.011421]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
[    0.011422]   DMA32    [mem 0x0000000001000000-0x00000000ffffffff]
[    0.011423]   Normal   [mem 0x0000000100000000-0x000000086effffff]
[    0.011424]   Device   empty
[    0.011424] Movable zone start for each node
[    0.011425] Early memory node ranges
[    0.011426]   node   0: [mem 0x0000000000001000-0x0000000000057fff]
[    0.011427]   node   0: [mem 0x0000000000059000-0x000000000009dfff]
[    0.011427]   node   0: [mem 0x0000000000100000-0x0000000087ad8fff]
[    0.011428]   node   0: [mem 0x0000000087b1d000-0x0000000087efafff]
[    0.011428]   node   0: [mem 0x0000000087efd000-0x000000008f002fff]
[    0.011429]   node   0: [mem 0x000000008fbff000-0x000000008fbfffff]
[    0.011429]   node   0: [mem 0x0000000100000000-0x000000086effffff]
[    0.011432] Initmem setup node 0 [mem 0x0000000000001000-0x000000086effffff]
[    0.011435] On node 0, zone DMA: 1 pages in unavailable ranges
[    0.011436] On node 0, zone DMA: 1 pages in unavailable ranges
[    0.011451] On node 0, zone DMA: 98 pages in unavailable ranges
[    0.013835] On node 0, zone DMA32: 68 pages in unavailable ranges
[    0.013957] On node 0, zone DMA32: 2 pages in unavailable ranges
[    0.013977] On node 0, zone DMA32: 3068 pages in unavailable ranges
[    0.047765] On node 0, zone Normal: 1024 pages in unavailable ranges
[    0.047791] On node 0, zone Normal: 4096 pages in unavailable ranges
[    0.047945] ACPI: PM-Timer IO Port: 0x1808
[    0.047950] ACPI: LAPIC_NMI (acpi_id[0x01] high edge lint[0x1])
[    0.047951] ACPI: LAPIC_NMI (acpi_id[0x02] high edge lint[0x1])
[    0.047952] ACPI: LAPIC_NMI (acpi_id[0x03] high edge lint[0x1])
[    0.047952] ACPI: LAPIC_NMI (acpi_id[0x04] high edge lint[0x1])
[    0.047953] ACPI: LAPIC_NMI (acpi_id[0x05] high edge lint[0x1])
[    0.047953] ACPI: LAPIC_NMI (acpi_id[0x06] high edge lint[0x1])
[    0.047953] ACPI: LAPIC_NMI (acpi_id[0x07] high edge lint[0x1])
[    0.047954] ACPI: LAPIC_NMI (acpi_id[0x08] high edge lint[0x1])
[    0.047979] IOAPIC[0]: apic_id 2, version 32, address 0xfec00000, GSI 0-119
[    0.047980] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
[    0.047982] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)
[    0.047984] ACPI: Using ACPI (MADT) for SMP configuration information
[    0.047985] ACPI: HPET id: 0x8086a201 base: 0xfed00000
[    0.047989] e820: update [mem 0x89bfc000-0x89c3dfff] usable ==> reserved
[    0.047998] TSC deadline timer available
[    0.048001] CPU topo: Max. logical packages:   1
[    0.048001] CPU topo: Max. logical dies:       1
[    0.048002] CPU topo: Max. dies per package:   1
[    0.048004] CPU topo: Max. threads per core:   2
[    0.048005] CPU topo: Num. cores per package:     4
[    0.048005] CPU topo: Num. threads per package:   8
[    0.048005] CPU topo: Allowing 8 present CPUs plus 0 hotplug CPUs
[    0.048017] PM: hibernation: Registered nosave memory: [mem 0x00000000-0x00000fff]
[    0.048018] PM: hibernation: Registered nosave memory: [mem 0x00058000-0x00058fff]
[    0.048020] PM: hibernation: Registered nosave memory: [mem 0x0009e000-0x000fffff]
[    0.048020] PM: hibernation: Registered nosave memory: [mem 0x86be3000-0x86be3fff]
[    0.048021] PM: hibernation: Registered nosave memory: [mem 0x86bf3000-0x86bf3fff]
[    0.048022] PM: hibernation: Registered nosave memory: [mem 0x86bf4000-0x86bf4fff]
[    0.048023] PM: hibernation: Registered nosave memory: [mem 0x86c10000-0x86c10fff]
[    0.048024] PM: hibernation: Registered nosave memory: [mem 0x87ad9000-0x87b1cfff]
[    0.048025] PM: hibernation: Registered nosave memory: [mem 0x87efb000-0x87efbfff]
[    0.048025] PM: hibernation: Registered nosave memory: [mem 0x87efc000-0x87efcfff]
[    0.048026] PM: hibernation: Registered nosave memory: [mem 0x89bfc000-0x89c3dfff]
[    0.048027] PM: hibernation: Registered nosave memory: [mem 0x89d22000-0x89d22fff]
[    0.048028] PM: hibernation: Registered nosave memory: [mem 0x8f003000-0x8f49ffff]
[    0.048028] PM: hibernation: Registered nosave memory: [mem 0x8f4a0000-0x8f4d3fff]
[    0.048029] PM: hibernation: Registered nosave memory: [mem 0x8f4d4000-0x8f544fff]
[    0.048029] PM: hibernation: Registered nosave memory: [mem 0x8f545000-0x8fbfefff]
[    0.048030] PM: hibernation: Registered nosave memory: [mem 0x8fc00000-0x8fffffff]
[    0.048031] PM: hibernation: Registered nosave memory: [mem 0x90000000-0xfdffffff]
[    0.048031] PM: hibernation: Registered nosave memory: [mem 0xfe000000-0xfe010fff]
[    0.048031] PM: hibernation: Registered nosave memory: [mem 0xfe011000-0xfebfffff]
[    0.048032] PM: hibernation: Registered nosave memory: [mem 0xfec00000-0xfec00fff]
[    0.048032] PM: hibernation: Registered nosave memory: [mem 0xfec01000-0xfecfffff]
[    0.048032] PM: hibernation: Registered nosave memory: [mem 0xfed00000-0xfed00fff]
[    0.048033] PM: hibernation: Registered nosave memory: [mem 0xfed01000-0xfedfffff]
[    0.048033] PM: hibernation: Registered nosave memory: [mem 0xfee00000-0xfee00fff]
[    0.048033] PM: hibernation: Registered nosave memory: [mem 0xfee01000-0xffffffff]
[    0.048034] [mem 0x90000000-0xfdffffff] available for PCI devices
[    0.048035] Booting paravirtualized kernel on bare hardware
[    0.048036] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1910969940391419 ns
[    0.052072] setup_percpu: NR_CPUS:8192 nr_cpumask_bits:8 nr_cpu_ids:8 nr_node_ids:1
[    0.052447] percpu: Embedded 67 pages/cpu s237568 r8192 d28672 u524288
[    0.052452] pcpu-alloc: s237568 r8192 d28672 u524288 alloc=1*2097152
[    0.052453] pcpu-alloc: [0] 0 1 2 3 [0] 4 5 6 7 
[    0.052466] Kernel command line: initrd=\7fb887b1d7f44e9d993f12e5d6b5967d\6.14.0-rc4-bisect-01301-g0747acf33112\initramfs-6.14.0-rc4-bisect-01301-g0747acf33112.img initrd=\7fb887b1d7f44e9d993f12e5d6b5967d\6.14.0-rc4-bisect-01301-g0747acf33112\initrd root=PARTUUID=89e4eb30-832d-4824-a82b-9e5f92d79936 zswap.enabled=0 rootflags=subvol=@ rw rootfstype=btrfs systemd.machine_id=7fb887b1d7f44e9d993f12e5d6b5967d
[    0.052538] printk: log buffer data + meta data: 131072 + 458752 = 589824 bytes
[    0.054784] Dentry cache hash table entries: 4194304 (order: 13, 33554432 bytes, linear)
[    0.055920] Inode-cache hash table entries: 2097152 (order: 12, 16777216 bytes, linear)
[    0.056002] Fallback order for Node 0: 0 
[    0.056004] Built 1 zonelists, mobility grouping on.  Total pages: 8380250
[    0.056005] Policy zone: Normal
[    0.056173] mem auto-init: stack:all(zero), heap alloc:on, heap free:off
[    0.056176] software IO TLB: area num 8.
[    0.118086] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=8, Nodes=1
[    0.118102] Kernel/User page tables isolation: enabled
[    0.118124] ftrace: allocating 54936 entries in 215 pages
[    0.134205] ftrace: allocated 215 pages with 6 groups
[    0.134259] Dynamic Preempt: full
[    0.134288] rcu: Preemptible hierarchical RCU implementation.
[    0.134289] rcu: 	RCU restricting CPUs from NR_CPUS=8192 to nr_cpu_ids=8.
[    0.134289] rcu: 	RCU priority boosting: priority 1 delay 500 ms.
[    0.134290] 	Trampoline variant of Tasks RCU enabled.
[    0.134290] 	Rude variant of Tasks RCU enabled.
[    0.134291] 	Tracing variant of Tasks RCU enabled.
[    0.134291] rcu: RCU calculated value of scheduler-enlistment delay is 100 jiffies.
[    0.134292] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=8
[    0.134296] RCU Tasks: Setting shift to 3 and lim to 1 rcu_task_cb_adjust=1 rcu_task_cpu_ids=8.
[    0.134297] RCU Tasks Rude: Setting shift to 3 and lim to 1 rcu_task_cb_adjust=1 rcu_task_cpu_ids=8.
[    0.134298] RCU Tasks Trace: Setting shift to 3 and lim to 1 rcu_task_cb_adjust=1 rcu_task_cpu_ids=8.
[    0.138025] NR_IRQS: 524544, nr_irqs: 2048, preallocated irqs: 16
[    0.138221] rcu: srcu_init: Setting srcu_struct sizes based on contention.
[    0.138424] kfence: initialized - using 2097152 bytes for 255 objects at 0x(____ptrval____)-0x(____ptrval____)
[    0.138446] Console: colour dummy device 80x25
[    0.138448] printk: legacy console [tty0] enabled
[    0.138480] ACPI: Core revision 20240827
[    0.138671] clocksource: hpet: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 79635855245 ns
[    0.138736] APIC: Switch to symmetric I/O mode setup
[    0.139961] x2apic: IRQ remapping doesn't support X2APIC mode
[    0.144055] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.148710] clocksource: tsc-early: mask: 0xffffffffffffffff max_cycles: 0x3c8a615336c, max_idle_ns: 440795257976 ns
[    0.148713] Calibrating delay loop (skipped), value calculated using timer frequency.. 8400.00 BogoMIPS (lpj=4200000)
[    0.148729] x86/cpu: SGX disabled or unsupported by BIOS.
[    0.148734] CPU0: Thermal monitoring enabled (TM1)
[    0.148767] Last level iTLB entries: 4KB 64, 2MB 8, 4MB 8
[    0.148768] Last level dTLB entries: 4KB 64, 2MB 0, 4MB 0, 1GB 4
[    0.148770] process: using mwait in idle threads
[    0.148773] Spectre V1 : Mitigation: usercopy/swapgs barriers and __user pointer sanitization
[    0.148774] Spectre V2 : Mitigation: IBRS
[    0.148775] Spectre V2 : Spectre v2 / SpectreRSB mitigation: Filling RSB on context switch
[    0.148776] Spectre V2 : Spectre v2 / SpectreRSB : Filling RSB on VMEXIT
[    0.148776] RETBleed: Mitigation: IBRS
[    0.148777] Spectre V2 : mitigation: Enabling conditional Indirect Branch Prediction Barrier
[    0.148778] Spectre V2 : User space: Mitigation: STIBP via prctl
[    0.148779] Speculative Store Bypass: Mitigation: Speculative Store Bypass disabled via prctl
[    0.148783] MDS: Mitigation: Clear CPU buffers
[    0.148784] TAA: Mitigation: TSX disabled
[    0.148784] MMIO Stale Data: Mitigation: Clear CPU buffers
[    0.148787] SRBDS: Mitigation: Microcode
[    0.148792] GDS: Mitigation: Microcode
[    0.148795] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    0.148797] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
[    0.148798] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
[    0.148798] x86/fpu: Supporting XSAVE feature 0x008: 'MPX bounds registers'
[    0.148799] x86/fpu: Supporting XSAVE feature 0x010: 'MPX CSR'
[    0.148800] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
[    0.148801] x86/fpu: xstate_offset[3]:  832, xstate_sizes[3]:   64
[    0.148802] x86/fpu: xstate_offset[4]:  896, xstate_sizes[4]:   64
[    0.148803] x86/fpu: Enabled xstate features 0x1f, context size is 960 bytes, using 'compacted' format.
[    0.171421] Freeing SMP alternatives memory: 48K
[    0.171423] pid_max: default: 32768 minimum: 301
[    0.173197] LSM: initializing lsm=capability,landlock,lockdown,yama,bpf
[    0.173244] landlock: Up and running.
[    0.173246] Yama: becoming mindful.
[    0.173379] LSM support for eBPF active
[    0.173411] Mount-cache hash table entries: 65536 (order: 7, 524288 bytes, linear)
[    0.173431] Mountpoint-cache hash table entries: 65536 (order: 7, 524288 bytes, linear)
[    0.173754] smpboot: CPU0: Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz (family: 0x6, model: 0x9e, stepping: 0x9)
[    0.174813] Performance Events: PEBS fmt3+, Skylake events, 32-deep LBR, full-width counters, Intel PMU driver.
[    0.174828] ... version:                4
[    0.174829] ... bit width:              48
[    0.174829] ... generic registers:      4
[    0.174830] ... value mask:             0000ffffffffffff
[    0.174831] ... max period:             00007fffffffffff
[    0.174831] ... fixed-purpose events:   3
[    0.174832] ... event mask:             000000070000000f
[    0.174906] signal: max sigframe size: 2032
[    0.174916] Estimated ratio of average max frequency by base frequency (times 1024): 1194
[    0.176292] rcu: Hierarchical SRCU implementation.
[    0.176293] rcu: 	Max phase no-delay instances is 400.
[    0.176327] Timer migration: 1 hierarchy levels; 8 children per group; 1 crossnode level
[    0.176753] NMI watchdog: Enabled. Permanently consumes one hw-PMU counter.
[    0.176800] smp: Bringing up secondary CPUs ...
[    0.176860] smpboot: x86: Booting SMP configuration:
[    0.176861] .... node  #0, CPUs:      #1 #2 #3 #4 #5 #6 #7
[    0.180060] MDS CPU bug present and SMT on, data leak possible. See https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/mds.html for more details.
[    0.180060] MMIO Stale Data CPU bug present and SMT on, data leak possible. See https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/processor_mmio_stale_data.html for more details.
[    0.180060] smp: Brought up 1 node, 8 CPUs
[    0.180060] smpboot: Total of 8 processors activated (67200.00 BogoMIPS)
[    0.180769] Memory: 32346768K/33521000K available (19122K kernel code, 2876K rwdata, 15184K rodata, 4536K init, 5372K bss, 1160460K reserved, 0K cma-reserved)
[    0.181410] devtmpfs: initialized
[    0.181410] x86/mm: Memory block size: 128MB
[    0.182995] ACPI: PM: Registering ACPI NVS region [mem 0x87ad9000-0x87b1cfff] (278528 bytes)
[    0.182995] ACPI: PM: Registering ACPI NVS region [mem 0x87efb000-0x87efbfff] (4096 bytes)
[    0.182995] ACPI: PM: Registering ACPI NVS region [mem 0x8f4d4000-0x8f544fff] (462848 bytes)
[    0.182995] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275000 ns
[    0.182995] futex hash table entries: 2048 (order: 5, 131072 bytes, linear)
[    0.182995] pinctrl core: initialized pinctrl subsystem
[    0.182995] PM: RTC time: 04:56:41, date: 2025-06-20
[    0.183267] NET: Registered PF_NETLINK/PF_ROUTE protocol family
[    0.183806] DMA: preallocated 4096 KiB GFP_KERNEL pool for atomic allocations
[    0.183954] DMA: preallocated 4096 KiB GFP_KERNEL|GFP_DMA pool for atomic allocations
[    0.184104] DMA: preallocated 4096 KiB GFP_KERNEL|GFP_DMA32 pool for atomic allocations
[    0.184114] audit: initializing netlink subsys (disabled)
[    0.184176] audit: type=2000 audit(1750395401.042:1): state=initialized audit_enabled=0 res=1
[    0.184235] thermal_sys: Registered thermal governor 'fair_share'
[    0.184237] thermal_sys: Registered thermal governor 'bang_bang'
[    0.184237] thermal_sys: Registered thermal governor 'step_wise'
[    0.184238] thermal_sys: Registered thermal governor 'user_space'
[    0.184239] thermal_sys: Registered thermal governor 'power_allocator'
[    0.184247] cpuidle: using governor ladder
[    0.184249] cpuidle: using governor menu
[    0.184293] ACPI FADT declares the system doesn't support PCIe ASPM, so disable it
[    0.184293] acpiphp: ACPI Hot Plug PCI Controller Driver version: 0.5
[    0.184293] PCI: ECAM [mem 0xe0000000-0xefffffff] (base 0xe0000000) for domain 0000 [bus 00-ff]
[    0.184293] PCI: Using configuration type 1 for base access
[    0.184293] kprobes: kprobe jump-optimization is enabled. All kprobes are optimized if possible.
[    0.193737] HugeTLB: registered 1.00 GiB page size, pre-allocated 0 pages
[    0.193737] HugeTLB: 16380 KiB vmemmap can be freed for a 1.00 GiB page
[    0.193737] HugeTLB: registered 2.00 MiB page size, pre-allocated 0 pages
[    0.193737] HugeTLB: 28 KiB vmemmap can be freed for a 2.00 MiB page
[    0.193787] raid6: skipped pq benchmark and selected avx2x4
[    0.193787] raid6: using avx2x2 recovery algorithm
[    0.193787] fbcon: Taking over console
[    0.193787] ACPI: Added _OSI(Module Device)
[    0.193787] ACPI: Added _OSI(Processor Device)
[    0.193787] ACPI: Added _OSI(3.0 _SCP Extensions)
[    0.193788] ACPI: Added _OSI(Processor Aggregator Device)
[    0.220861] ACPI: 11 ACPI AML tables successfully acquired and loaded
[    0.226319] ACPI: Dynamic OEM Table Load:
[    0.226324] ACPI: SSDT 0xFFFF8C4E40EB2000 00081F (v02 PmRef  Cpu0Ist  00003000 INTL 20160422)
[    0.227917] ACPI: Dynamic OEM Table Load:
[    0.227921] ACPI: SSDT 0xFFFF8C4E40EBC800 00065C (v02 PmRef  ApIst    00003000 INTL 20160422)
[    0.229016] ACPI: Dynamic OEM Table Load:
[    0.229019] ACPI: SSDT 0xFFFF8C4E41765200 000197 (v02 PmRef  ApHwp    00003000 INTL 20160422)
[    0.233679] ACPI: Interpreter enabled
[    0.233703] ACPI: PM: (supports S0 S3 S4 S5)
[    0.233704] ACPI: Using IOAPIC for interrupt routing
[    0.234761] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
[    0.234762] PCI: Using E820 reservations for host bridge windows
[    0.235493] ACPI: Enabled 7 GPEs in block 00 to 7F
[    0.237380] ACPI: \_SB_.PCI0.PEG0.PG00: New power resource
[    0.237635] ACPI: \_SB_.PCI0.PEG1.PG01: New power resource
[    0.237887] ACPI: \_SB_.PCI0.PEG2.PG02: New power resource
[    0.239732] ACPI: \_SB_.PCI0.RP09.PXSX.WRST: New power resource
[    0.239955] ACPI: \_SB_.PCI0.RP10.PXSX.WRST: New power resource
[    0.240175] ACPI: \_SB_.PCI0.RP11.PXSX.WRST: New power resource
[    0.240395] ACPI: \_SB_.PCI0.RP12.PXSX.WRST: New power resource
[    0.240614] ACPI: \_SB_.PCI0.RP13.PXSX.WRST: New power resource
[    0.240838] ACPI: \_SB_.PCI0.RP01.PXSX.WRST: New power resource
[    0.241058] ACPI: \_SB_.PCI0.RP02.PXSX.WRST: New power resource
[    0.241278] ACPI: \_SB_.PCI0.RP03.PXSX.WRST: New power resource
[    0.241497] ACPI: \_SB_.PCI0.RP04.PXSX.WRST: New power resource
[    0.241718] ACPI: \_SB_.PCI0.RP05.PXSX.WRST: New power resource
[    0.241942] ACPI: \_SB_.PCI0.RP06.PXSX.WRST: New power resource
[    0.242162] ACPI: \_SB_.PCI0.RP07.PXSX.WRST: New power resource
[    0.242381] ACPI: \_SB_.PCI0.RP08.PXSX.WRST: New power resource
[    0.242601] ACPI: \_SB_.PCI0.RP17.PXSX.WRST: New power resource
[    0.242823] ACPI: \_SB_.PCI0.RP18.PXSX.WRST: New power resource
[    0.243047] ACPI: \_SB_.PCI0.RP19.PXSX.WRST: New power resource
[    0.243270] ACPI: \_SB_.PCI0.RP20.PXSX.WRST: New power resource
[    0.244214] ACPI: \_SB_.PCI0.RP14.PXSX.WRST: New power resource
[    0.244438] ACPI: \_SB_.PCI0.RP15.PXSX.WRST: New power resource
[    0.244658] ACPI: \_SB_.PCI0.RP16.PXSX.WRST: New power resource
[    0.257013] ACPI: \_TZ_.FN00: New power resource
[    0.257072] ACPI: \_TZ_.FN01: New power resource
[    0.257129] ACPI: \_TZ_.FN02: New power resource
[    0.257183] ACPI: \_TZ_.FN03: New power resource
[    0.257236] ACPI: \_TZ_.FN04: New power resource
[    0.257990] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-fe])
[    0.257995] acpi PNP0A08:00: _OSC: OS supports [ExtendedConfig ASPM ClockPM Segments MSI EDR HPX-Type3]
[    0.258079] acpi PNP0A08:00: _OSC: platform does not support [PCIeHotplug SHPCHotplug PME AER]
[    0.258232] acpi PNP0A08:00: _OSC: OS now controls [PCIeCapability LTR DPC]
[    0.258234] acpi PNP0A08:00: FADT indicates ASPM is unsupported, using BIOS configuration
[    0.258895] PCI host bridge to bus 0000:00
[    0.258898] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]
[    0.258900] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]
[    0.258902] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000fffff window]
[    0.258903] pci_bus 0000:00: root bus resource [mem 0x90000000-0xdfffffff window]
[    0.258904] pci_bus 0000:00: root bus resource [mem 0xfd000000-0xfe7fffff window]
[    0.258905] pci_bus 0000:00: root bus resource [bus 00-fe]
[    0.258964] pci 0000:00:00.0: [8086:591f] type 00 class 0x060000 conventional PCI endpoint
[    0.259030] pci 0000:00:01.0: [8086:1901] type 01 class 0x060400 PCIe Root Port
[    0.259048] pci 0000:00:01.0: PCI bridge to [bus 01]
[    0.259050] pci 0000:00:01.0:   bridge window [io  0xe000-0xefff]
[    0.259052] pci 0000:00:01.0:   bridge window [mem 0xdfa00000-0xdfafffff]
[    0.259057] pci 0000:00:01.0:   bridge window [mem 0xc0000000-0xd01fffff 64bit pref]
[    0.259077] pci 0000:00:01.0: PME# supported from D0 D3hot D3cold
[    0.259395] pci 0000:00:08.0: [8086:1911] type 00 class 0x088000 conventional PCI endpoint
[    0.259422] pci 0000:00:08.0: BAR 0 [mem 0xdfb4f000-0xdfb4ffff 64bit]
[    0.259496] pci 0000:00:14.0: [8086:a2af] type 00 class 0x0c0330 conventional PCI endpoint
[    0.259542] pci 0000:00:14.0: BAR 0 [mem 0xdfb30000-0xdfb3ffff 64bit]
[    0.259570] pci 0000:00:14.0: PME# supported from D3hot D3cold
[    0.260108] pci 0000:00:14.2: [8086:a2b1] type 00 class 0x118000 conventional PCI endpoint
[    0.260153] pci 0000:00:14.2: BAR 0 [mem 0xdfb4e000-0xdfb4efff 64bit]
[    0.260227] pci 0000:00:16.0: [8086:a2ba] type 00 class 0x078000 conventional PCI endpoint
[    0.260269] pci 0000:00:16.0: BAR 0 [mem 0xdfb4d000-0xdfb4dfff 64bit]
[    0.260296] pci 0000:00:16.0: PME# supported from D3hot
[    0.260543] pci 0000:00:17.0: [8086:a282] type 00 class 0x010601 conventional PCI endpoint
[    0.260589] pci 0000:00:17.0: BAR 0 [mem 0xdfb48000-0xdfb49fff]
[    0.260592] pci 0000:00:17.0: BAR 1 [mem 0xdfb4c000-0xdfb4c0ff]
[    0.260596] pci 0000:00:17.0: BAR 2 [io  0xf050-0xf057]
[    0.260599] pci 0000:00:17.0: BAR 3 [io  0xf040-0xf043]
[    0.260603] pci 0000:00:17.0: BAR 4 [io  0xf020-0xf03f]
[    0.260607] pci 0000:00:17.0: BAR 5 [mem 0xdfb4b000-0xdfb4b7ff]
[    0.260635] pci 0000:00:17.0: PME# supported from D3hot
[    0.260868] pci 0000:00:1b.0: [8086:a2e7] type 01 class 0x060400 PCIe Root Port
[    0.260895] pci 0000:00:1b.0: PCI bridge to [bus 02]
[    0.260945] pci 0000:00:1b.0: PME# supported from D0 D3hot D3cold
[    0.261382] pci 0000:00:1b.4: [8086:a2eb] type 01 class 0x060400 PCIe Root Port
[    0.261405] pci 0000:00:1b.4: PCI bridge to [bus 03]
[    0.261409] pci 0000:00:1b.4:   bridge window [mem 0xdf900000-0xdf9fffff]
[    0.261454] pci 0000:00:1b.4: PME# supported from D0 D3hot D3cold
[    0.261899] pci 0000:00:1d.0: [8086:a298] type 01 class 0x060400 PCIe Root Port
[    0.261923] pci 0000:00:1d.0: PCI bridge to [bus 04]
[    0.261926] pci 0000:00:1d.0:   bridge window [mem 0xdf000000-0xdf8fffff]
[    0.261934] pci 0000:00:1d.0:   bridge window [mem 0xd0400000-0xd07fffff 64bit pref]
[    0.261972] pci 0000:00:1d.0: PME# supported from D0 D3hot D3cold
[    0.262426] pci 0000:00:1f.0: [8086:a2c5] type 00 class 0x060100 conventional PCI endpoint
[    0.262714] pci 0000:00:1f.2: [8086:a2a1] type 00 class 0x058000 conventional PCI endpoint
[    0.262760] pci 0000:00:1f.2: BAR 0 [mem 0xdfb44000-0xdfb47fff]
[    0.262963] pci 0000:00:1f.3: [8086:a2f0] type 00 class 0x040300 conventional PCI endpoint
[    0.263017] pci 0000:00:1f.3: BAR 0 [mem 0xdfb40000-0xdfb43fff 64bit]
[    0.263022] pci 0000:00:1f.3: BAR 4 [mem 0xdfb20000-0xdfb2ffff 64bit]
[    0.263056] pci 0000:00:1f.3: PME# supported from D3hot D3cold
[    0.263552] pci 0000:00:1f.4: [8086:a2a3] type 00 class 0x0c0500 conventional PCI endpoint
[    0.263681] pci 0000:00:1f.4: BAR 0 [mem 0xdfb4a000-0xdfb4a0ff 64bit]
[    0.263691] pci 0000:00:1f.4: BAR 4 [io  0xf000-0xf01f]
[    0.263919] pci 0000:00:1f.6: [8086:15b8] type 00 class 0x020000 conventional PCI endpoint
[    0.263983] pci 0000:00:1f.6: BAR 0 [mem 0xdfb00000-0xdfb1ffff]
[    0.264031] pci 0000:00:1f.6: PME# supported from D0 D3hot D3cold
[    0.264250] pci 0000:01:00.0: [1002:67df] type 00 class 0x030000 PCIe Legacy Endpoint
[    0.264287] pci 0000:01:00.0: BAR 0 [mem 0xc0000000-0xcfffffff 64bit pref]
[    0.264290] pci 0000:01:00.0: BAR 2 [mem 0xd0000000-0xd01fffff 64bit pref]
[    0.264291] pci 0000:01:00.0: BAR 4 [io  0xe000-0xe0ff]
[    0.264293] pci 0000:01:00.0: BAR 5 [mem 0xdfa00000-0xdfa3ffff]
[    0.264294] pci 0000:01:00.0: ROM [mem 0xdfa40000-0xdfa5ffff pref]
[    0.264316] pci 0000:01:00.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
[    0.264349] pci 0000:01:00.0: supports D1 D2
[    0.264350] pci 0000:01:00.0: PME# supported from D1 D2 D3hot D3cold
[    0.264445] pci 0000:01:00.1: [1002:aaf0] type 00 class 0x040300 PCIe Legacy Endpoint
[    0.264479] pci 0000:01:00.1: BAR 0 [mem 0xdfa60000-0xdfa63fff 64bit]
[    0.264518] pci 0000:01:00.1: supports D1 D2
[    0.264570] pci 0000:00:01.0: PCI bridge to [bus 01]
[    0.264651] acpiphp: Slot [1] registered
[    0.264660] pci 0000:00:1b.0: PCI bridge to [bus 02]
[    0.264752] pci 0000:03:00.0: [8086:f1a8] type 00 class 0x010802 PCIe Endpoint
[    0.264812] pci 0000:03:00.0: BAR 0 [mem 0xdf900000-0xdf903fff 64bit]
[    0.265013] pci 0000:00:1b.4: PCI bridge to [bus 03]
[    0.265100] pci 0000:04:00.0: [14e4:43c3] type 00 class 0x028000 PCIe Endpoint
[    0.265153] pci 0000:04:00.0: BAR 0 [mem 0xdf800000-0xdf807fff 64bit]
[    0.265156] pci 0000:04:00.0: BAR 2 [mem 0xdf000000-0xdf7fffff 64bit]
[    0.265159] pci 0000:04:00.0: BAR 4 [mem 0xd0400000-0xd07fffff 64bit pref]
[    0.265243] pci 0000:04:00.0: supports D1 D2
[    0.265244] pci 0000:04:00.0: PME# supported from D0 D1 D2 D3hot D3cold
[    0.265613] pci 0000:00:1d.0: PCI bridge to [bus 04]
[    0.267184] ACPI: PCI: Interrupt link LNKA configured for IRQ 11
[    0.267227] ACPI: PCI: Interrupt link LNKB configured for IRQ 10
[    0.267270] ACPI: PCI: Interrupt link LNKC configured for IRQ 11
[    0.267312] ACPI: PCI: Interrupt link LNKD configured for IRQ 11
[    0.267355] ACPI: PCI: Interrupt link LNKE configured for IRQ 11
[    0.267397] ACPI: PCI: Interrupt link LNKF configured for IRQ 11
[    0.267440] ACPI: PCI: Interrupt link LNKG configured for IRQ 11
[    0.267481] ACPI: PCI: Interrupt link LNKH configured for IRQ 11
[    0.270183] iommu: Default domain type: Translated
[    0.270183] iommu: DMA domain TLB invalidation policy: lazy mode
[    0.270183] SCSI subsystem initialized
[    0.270183] libata version 3.00 loaded.
[    0.270183] ACPI: bus type USB registered
[    0.270183] usbcore: registered new interface driver usbfs
[    0.270183] usbcore: registered new interface driver hub
[    0.270183] usbcore: registered new device driver usb
[    0.270183] EDAC MC: Ver: 3.0.0
[    0.270183] efivars: Registered efivars operations
[    0.270835] NetLabel: Initializing
[    0.270836] NetLabel:  domain hash size = 128
[    0.270837] NetLabel:  protocols = UNLABELED CIPSOv4 CALIPSO
[    0.270848] NetLabel:  unlabeled traffic allowed by default
[    0.270851] mctp: management component transport protocol core
[    0.270851] NET: Registered PF_MCTP protocol family
[    0.270856] PCI: Using ACPI for IRQ routing
[    0.298613] PCI: pci_cache_line_size set to 64 bytes
[    0.298657] e820: reserve RAM buffer [mem 0x00058000-0x0005ffff]
[    0.298667] e820: reserve RAM buffer [mem 0x0009e000-0x0009ffff]
[    0.298668] e820: reserve RAM buffer [mem 0x86be3018-0x87ffffff]
[    0.298669] e820: reserve RAM buffer [mem 0x86bf4018-0x87ffffff]
[    0.298670] e820: reserve RAM buffer [mem 0x87ad9000-0x87ffffff]
[    0.298671] e820: reserve RAM buffer [mem 0x87efb000-0x87ffffff]
[    0.298672] e820: reserve RAM buffer [mem 0x89bfc000-0x8bffffff]
[    0.298672] e820: reserve RAM buffer [mem 0x89d22000-0x8bffffff]
[    0.298673] e820: reserve RAM buffer [mem 0x8f003000-0x8fffffff]
[    0.298674] e820: reserve RAM buffer [mem 0x8fc00000-0x8fffffff]
[    0.298675] e820: reserve RAM buffer [mem 0x86f000000-0x86fffffff]
[    0.298729] pci 0000:01:00.0: vgaarb: setting as boot VGA device
[    0.298729] pci 0000:01:00.0: vgaarb: bridge control possible
[    0.298729] pci 0000:01:00.0: vgaarb: VGA device added: decodes=io+mem,owns=mem,locks=none
[    0.298729] vgaarb: loaded
[    0.298751] hpet0: at MMIO 0xfed00000, IRQs 2, 8, 0, 0, 0, 0, 0, 0
[    0.298756] hpet0: 8 comparators, 64-bit 24.000000 MHz counter
[    0.300739] clocksource: Switched to clocksource tsc-early
[    0.301202] VFS: Disk quotas dquot_6.6.0
[    0.301208] VFS: Dquot-cache hash table entries: 512 (order 0, 4096 bytes)
[    0.301233] pnp: PnP ACPI init
[    0.301445] system 00:00: [io  0x0a00-0x0a0f] has been reserved
[    0.301447] system 00:00: [io  0x0a10-0x0a1f] has been reserved
[    0.301449] system 00:00: [io  0x0a20-0x0a2f] has been reserved
[    0.301450] system 00:00: [io  0x0a30-0x0a3f] has been reserved
[    0.301748] pnp 00:01: [dma 0 disabled]
[    0.301873] system 00:02: [io  0x0680-0x069f] has been reserved
[    0.301875] system 00:02: [io  0xffff] has been reserved
[    0.301876] system 00:02: [io  0xffff] has been reserved
[    0.301877] system 00:02: [io  0xffff] has been reserved
[    0.301878] system 00:02: [io  0x1800-0x18fe] has been reserved
[    0.301879] system 00:02: [io  0x164e-0x164f] has been reserved
[    0.301940] system 00:03: [io  0x0800-0x087f] has been reserved
[    0.301973] system 00:05: [io  0x1854-0x1857] has been reserved
[    0.302140] system 00:06: [mem 0xfed10000-0xfed17fff] has been reserved
[    0.302142] system 00:06: [mem 0xfed18000-0xfed18fff] has been reserved
[    0.302143] system 00:06: [mem 0xfed19000-0xfed19fff] has been reserved
[    0.302144] system 00:06: [mem 0xe0000000-0xefffffff] has been reserved
[    0.302145] system 00:06: [mem 0xfed20000-0xfed3ffff] has been reserved
[    0.302147] system 00:06: [mem 0xfed90000-0xfed93fff] has been reserved
[    0.302148] system 00:06: [mem 0xfed45000-0xfed8ffff] has been reserved
[    0.302150] system 00:06: [mem 0xff000000-0xffffffff] has been reserved
[    0.302151] system 00:06: [mem 0xfee00000-0xfeefffff] could not be reserved
[    0.302153] system 00:06: [mem 0xdffc0000-0xdffdffff] has been reserved
[    0.302180] system 00:07: [mem 0xfd000000-0xfdabffff] has been reserved
[    0.302182] system 00:07: [mem 0xfdad0000-0xfdadffff] has been reserved
[    0.302183] system 00:07: [mem 0xfdb00000-0xfdffffff] has been reserved
[    0.302184] system 00:07: [mem 0xfe000000-0xfe01ffff] could not be reserved
[    0.302185] system 00:07: [mem 0xfe036000-0xfe03bfff] has been reserved
[    0.302186] system 00:07: [mem 0xfe03d000-0xfe3fffff] has been reserved
[    0.302396] system 00:08: [io  0xff00-0xfffe] has been reserved
[    0.303260] system 00:09: [mem 0xfdaf0000-0xfdafffff] has been reserved
[    0.303262] system 00:09: [mem 0xfdae0000-0xfdaeffff] has been reserved
[    0.303263] system 00:09: [mem 0xfdac0000-0xfdacffff] has been reserved
[    0.303902] pnp: PnP ACPI: found 10 devices
[    0.309108] clocksource: acpi_pm: mask: 0xffffff max_cycles: 0xffffff, max_idle_ns: 2085701024 ns
[    0.309144] NET: Registered PF_INET protocol family
[    0.309227] IP idents hash table entries: 262144 (order: 9, 2097152 bytes, linear)
[    0.319595] tcp_listen_portaddr_hash hash table entries: 16384 (order: 6, 262144 bytes, linear)
[    0.319624] Table-perturb hash table entries: 65536 (order: 6, 262144 bytes, linear)
[    0.319682] TCP established hash table entries: 262144 (order: 9, 2097152 bytes, linear)
[    0.319876] TCP bind hash table entries: 65536 (order: 9, 2097152 bytes, linear)
[    0.320015] TCP: Hash tables configured (established 262144 bind 65536)
[    0.320083] MPTCP token hash table entries: 32768 (order: 7, 786432 bytes, linear)
[    0.320164] UDP hash table entries: 16384 (order: 8, 1048576 bytes, linear)
[    0.320262] UDP-Lite hash table entries: 16384 (order: 8, 1048576 bytes, linear)
[    0.320346] NET: Registered PF_UNIX/PF_LOCAL protocol family
[    0.320352] NET: Registered PF_XDP protocol family
[    0.320362] pci 0000:00:01.0: PCI bridge to [bus 01]
[    0.320365] pci 0000:00:01.0:   bridge window [io  0xe000-0xefff]
[    0.320377] pci 0000:00:01.0:   bridge window [mem 0xdfa00000-0xdfafffff]
[    0.320381] pci 0000:00:01.0:   bridge window [mem 0xc0000000-0xd01fffff 64bit pref]
[    0.320387] pci 0000:00:1b.0: PCI bridge to [bus 02]
[    0.320404] pci 0000:00:1b.4: PCI bridge to [bus 03]
[    0.320409] pci 0000:00:1b.4:   bridge window [mem 0xdf900000-0xdf9fffff]
[    0.320418] pci 0000:00:1d.0: PCI bridge to [bus 04]
[    0.320424] pci 0000:00:1d.0:   bridge window [mem 0xdf000000-0xdf8fffff]
[    0.320427] pci 0000:00:1d.0:   bridge window [mem 0xd0400000-0xd07fffff 64bit pref]
[    0.320435] pci_bus 0000:00: resource 4 [io  0x0000-0x0cf7 window]
[    0.320436] pci_bus 0000:00: resource 5 [io  0x0d00-0xffff window]
[    0.320437] pci_bus 0000:00: resource 6 [mem 0x000a0000-0x000fffff window]
[    0.320438] pci_bus 0000:00: resource 7 [mem 0x90000000-0xdfffffff window]
[    0.320439] pci_bus 0000:00: resource 8 [mem 0xfd000000-0xfe7fffff window]
[    0.320440] pci_bus 0000:01: resource 0 [io  0xe000-0xefff]
[    0.320441] pci_bus 0000:01: resource 1 [mem 0xdfa00000-0xdfafffff]
[    0.320442] pci_bus 0000:01: resource 2 [mem 0xc0000000-0xd01fffff 64bit pref]
[    0.320443] pci_bus 0000:03: resource 1 [mem 0xdf900000-0xdf9fffff]
[    0.320444] pci_bus 0000:04: resource 1 [mem 0xdf000000-0xdf8fffff]
[    0.320445] pci_bus 0000:04: resource 2 [mem 0xd0400000-0xd07fffff 64bit pref]
[    0.320786] pci 0000:01:00.1: D0 power state depends on 0000:01:00.0
[    0.320819] PCI: CLS 64 bytes, default 64
[    0.320861] pci 0000:00:1f.1: [8086:a2a0] type 00 class 0x058000 conventional PCI endpoint
[    0.320995] pci 0000:00:1f.1: BAR 0 [mem 0xfd000000-0xfdffffff 64bit]
[    0.321093] PCI-DMA: Using software bounce buffering for IO (SWIOTLB)
[    0.321094] software IO TLB: mapped [mem 0x0000000082be3000-0x0000000086be3000] (64MB)
[    0.321130] Unpacking initramfs...
[    0.349943] Initialise system trusted keyrings
[    0.349950] Key type blacklist registered
[    0.349984] workingset: timestamp_bits=36 max_order=23 bucket_order=0
[    0.350143] fuse: init (API version 7.42)
[    0.350193] integrity: Platform Keyring initialized
[    0.350195] integrity: Machine keyring initialized
[    0.357865] xor: automatically using best checksumming function   avx       
[    0.357869] Key type asymmetric registered
[    0.357870] Asymmetric key parser 'x509' registered
[    0.357891] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 246)
[    0.357930] io scheduler mq-deadline registered
[    0.357931] io scheduler kyber registered
[    0.357940] io scheduler bfq registered
[    0.364404] ledtrig-cpu: registered to indicate activity on CPUs
[    0.365040] shpchp: Standard Hot Plug PCI Controller Driver version: 0.4
[    0.365389] input: Sleep Button as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0C0E:00/input/input0
[    0.365404] ACPI: button: Sleep Button [SLPB]
[    0.365420] input: Power Button as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0C0C:00/input/input1
[    0.365430] ACPI: button: Power Button [PWRB]
[    0.365446] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input2
[    0.370400] ACPI: button: Power Button [PWRF]
[    0.371784] thermal LNXTHERM:00: registered as thermal_zone0
[    0.371787] ACPI: thermal: Thermal Zone [TZ00] (28 C)
[    0.371899] thermal LNXTHERM:01: registered as thermal_zone1
[    0.371900] ACPI: thermal: Thermal Zone [TZ01] (30 C)
[    0.372058] Serial: 8250/16550 driver, 32 ports, IRQ sharing enabled
[    0.372395] 00:01: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A
[    0.373758] serial8250: ttyS1 at I/O 0x2f8 (irq = 3, base_baud = 115200) is a 16550A
[    0.374917] Non-volatile memory driver v1.3
[    0.374918] Linux agpgart interface v0.103
[    0.374980] ACPI: bus type drm_connector registered
[    0.375305] ahci 0000:00:17.0: version 3.0
[    0.375471] ahci 0000:00:17.0: AHCI vers 0001.0301, 32 command slots, 6 Gbps, SATA mode
[    0.375473] ahci 0000:00:17.0: 6/6 ports implemented (port mask 0x3f)
[    0.375474] ahci 0000:00:17.0: flags: 64bit ncq sntf led clo only pio slum part ems deso sadm sds apst 
[    0.426769] scsi host0: ahci
[    0.426960] scsi host1: ahci
[    0.427097] scsi host2: ahci
[    0.427153] scsi host3: ahci
[    0.427204] scsi host4: ahci
[    0.427249] scsi host5: ahci
[    0.427268] ata1: SATA max UDMA/133 abar m2048@0xdfb4b000 port 0xdfb4b100 irq 124 lpm-pol 3
[    0.427272] ata2: SATA max UDMA/133 abar m2048@0xdfb4b000 port 0xdfb4b180 irq 124 lpm-pol 3
[    0.427273] ata3: SATA max UDMA/133 abar m2048@0xdfb4b000 port 0xdfb4b200 irq 124 lpm-pol 3
[    0.427275] ata4: SATA max UDMA/133 abar m2048@0xdfb4b000 port 0xdfb4b280 irq 124 lpm-pol 3
[    0.427276] ata5: SATA max UDMA/133 abar m2048@0xdfb4b000 port 0xdfb4b300 irq 124 lpm-pol 3
[    0.427277] ata6: SATA max UDMA/133 abar m2048@0xdfb4b000 port 0xdfb4b380 irq 124 lpm-pol 3
[    0.427474] xhci_hcd 0000:00:14.0: xHCI Host Controller
[    0.427479] xhci_hcd 0000:00:14.0: new USB bus registered, assigned bus number 1
[    0.428540] xhci_hcd 0000:00:14.0: hcc params 0x200077c1 hci version 0x100 quirks 0x0000000000009810
[    0.428727] xhci_hcd 0000:00:14.0: xHCI Host Controller
[    0.428729] xhci_hcd 0000:00:14.0: new USB bus registered, assigned bus number 2
[    0.428730] xhci_hcd 0000:00:14.0: Host supports USB 3.0 SuperSpeed
[    0.428757] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 6.14
[    0.428758] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    0.428759] usb usb1: Product: xHCI Host Controller
[    0.428760] usb usb1: Manufacturer: Linux 6.14.0-rc4-bisect-01301-g0747acf33112 xhci-hcd
[    0.428761] usb usb1: SerialNumber: 0000:00:14.0
[    0.428859] hub 1-0:1.0: USB hub found
[    0.428873] hub 1-0:1.0: 16 ports detected
[    0.430507] usb usb2: New USB device found, idVendor=1d6b, idProduct=0003, bcdDevice= 6.14
[    0.430509] usb usb2: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    0.430511] usb usb2: Product: xHCI Host Controller
[    0.430512] usb usb2: Manufacturer: Linux 6.14.0-rc4-bisect-01301-g0747acf33112 xhci-hcd
[    0.430513] usb usb2: SerialNumber: 0000:00:14.0
[    0.430590] hub 2-0:1.0: USB hub found
[    0.430601] hub 2-0:1.0: 10 ports detected
[    0.431696] usbcore: registered new interface driver usbserial_generic
[    0.431699] usbserial: USB Serial support registered for generic
[    0.431719] i8042: PNP: No PS/2 controller found.
[    0.431841] rtc_cmos 00:04: RTC can wake from S4
[    0.432503] rtc_cmos 00:04: registered as rtc0
[    0.432627] rtc_cmos 00:04: setting system clock to 2025-06-20T04:56:42 UTC (1750395402)
[    0.432645] rtc_cmos 00:04: alarms up to one month, y3k, 242 bytes nvram
[    0.432803] intel_pstate: Intel P-state driver initializing
[    0.433053] intel_pstate: Disabling energy efficiency optimization
[    0.433054] intel_pstate: HWP enabled
[    0.433314] simple-framebuffer simple-framebuffer.0: [drm] Registered 1 planes with drm panic
[    0.433315] [drm] Initialized simpledrm 1.0.0 for simple-framebuffer.0 on minor 0
[    0.434348] Console: switching to colour frame buffer device 128x48
[    0.435728] simple-framebuffer simple-framebuffer.0: [drm] fb0: simpledrmdrmfb frame buffer device
[    0.435792] hid: raw HID events driver (C) Jiri Kosina
[    0.435807] usbcore: registered new interface driver usbhid
[    0.435808] usbhid: USB HID core driver
[    0.435851] drop_monitor: Initializing network drop monitor service
[    0.435925] NET: Registered PF_INET6 protocol family
[    0.515224] Freeing initrd memory: 459528K
[    0.519177] Segment Routing with IPv6
[    0.519178] RPL Segment Routing with IPv6
[    0.519189] In-situ OAM (IOAM) with IPv6
[    0.519209] NET: Registered PF_PACKET protocol family
[    0.519619] ENERGY_PERF_BIAS: Set to 'normal', was 'performance'
[    0.519724] microcode: Current revision: 0x000000f8
[    0.519725] microcode: Updated early from: 0x0000008e
[    0.519937] IPI shorthand broadcast: enabled
[    0.521133] sched_clock: Marking stable (517001011, 3368537)->(523148761, -2779213)
[    0.521258] registered taskstats version 1
[    0.521529] Loading compiled-in X.509 certificates
[    0.525067] Loaded X.509 cert 'Build time autogenerated kernel key: 4bc75e7d0dd5f5ba4b376555b65f6dec6139cd1b'
[    0.526259] Demotion targets for Node 0: null
[    0.526363] Key type .fscrypt registered
[    0.526364] Key type fscrypt-provisioning registered
[    0.526711] Btrfs loaded, zoned=yes, fsverity=yes
[    0.526733] Key type big_key registered
[    0.527867] PM:   Magic number: 13:814:919
[    0.530638] RAS: Correctable Errors collector initialized.
[    0.539299] clk: Disabling unused clocks
[    0.539301] PM: genpd: Disabling unused power domains
[    0.669461] usb 1-2: new full-speed USB device number 2 using xhci_hcd
[    0.731733] ata5: SATA link down (SStatus 4 SControl 300)
[    0.731848] ata3: SATA link down (SStatus 4 SControl 300)
[    0.731883] ata4: SATA link down (SStatus 4 SControl 300)
[    0.739772] ata6: SATA link down (SStatus 4 SControl 300)
[    0.739873] ata2: SATA link down (SStatus 4 SControl 300)
[    0.739909] ata1: SATA link down (SStatus 4 SControl 300)
[    0.743464] Freeing unused decrypted memory: 2036K
[    0.745636] Freeing unused kernel image (initmem) memory: 4536K
[    0.745891] Write protecting the kernel read-only data: 36864k
[    0.747997] Freeing unused kernel image (text/rodata gap) memory: 1356K
[    0.749256] Freeing unused kernel image (rodata/data gap) memory: 1200K
[    0.794872] usb 1-2: New USB device found, idVendor=046d, idProduct=c24c, bcdDevice=83.00
[    0.794876] usb 1-2: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[    0.794878] usb 1-2: Product: G400s Optical Gaming Mouse
[    0.794880] usb 1-2: Manufacturer: Logitech
[    0.797254] input: Logitech G400s Optical Gaming Mouse as /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0/0003:046D:C24C.0001/input/input3
[    0.797306] hid-generic 0003:046D:C24C.0001: input,hidraw0: USB HID v1.10 Mouse [Logitech G400s Optical Gaming Mouse] on usb-0000:00:14.0-2/input0
[    0.798266] hid-generic 0003:046D:C24C.0002: hiddev96,hidraw1: USB HID v1.10 Device [Logitech G400s Optical Gaming Mouse] on usb-0000:00:14.0-2/input1
[    0.819558] x86/mm: Checked W+X mappings: passed, no W+X pages found.
[    0.819561] rodata_test: all tests were successful
[    0.819562] x86/mm: Checking user space page tables
[    0.849000] x86/mm: Checked W+X mappings: passed, no W+X pages found.
[    0.849003] Run /init as init process
[    0.849004]   with arguments:
[    0.849005]     /init
[    0.849006]   with environment:
[    0.849007]     HOME=/
[    0.849007]     TERM=linux
[    0.904483] usb 2-4: new SuperSpeed USB device number 2 using xhci_hcd
[    0.917275] usb 2-4: New USB device found, idVendor=0bc2, idProduct=ab6d, bcdDevice=17.07
[    0.917278] usb 2-4: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[    0.917279] usb 2-4: Product: One Touch w/PW
[    0.917280] usb 2-4: Manufacturer: Seagate
[    0.917281] usb 2-4: SerialNumber: 00000000NABV2AXX
[    0.933008] usbcore: registered new interface driver usb-storage
[    0.939737] scsi host6: uas
[    0.939788] usbcore: registered new interface driver uas
[    0.940145] scsi 6:0:0:0: Direct-Access     Seagate  One Touch w/PW   1707 PQ: 0 ANSI: 6
[    0.943689] sd 6:0:0:0: [sda] 7814037167 512-byte logical blocks: (4.00 TB/3.64 TiB)
[    0.943691] sd 6:0:0:0: [sda] 4096-byte physical blocks
[    0.943822] sd 6:0:0:0: [sda] Write Protect is off
[    0.943824] sd 6:0:0:0: [sda] Mode Sense: 03 00 00 00
[    0.944072] sd 6:0:0:0: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[    0.967575] sd 6:0:0:0: [sda] Preferred minimum I/O size 4096 bytes
[    0.967578] sd 6:0:0:0: [sda] Optimal transfer size 33553920 bytes not a multiple of preferred minimum block size (4096 bytes)
[    1.012620]  sda: sda1 sda2
[    1.012741] sd 6:0:0:0: [sda] Attached SCSI disk
[    1.029378] usb 1-7: new full-speed USB device number 3 using xhci_hcd
[    1.070689] nvme nvme0: pci function 0000:03:00.0
[    1.079519] nvme nvme0: 8/0/0 default/read/poll queues
[    1.083777]  nvme0n1: p1 p2
[    1.153856] usb 1-7: New USB device found, idVendor=0c45, idProduct=7638, bcdDevice= 1.05
[    1.153861] usb 1-7: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[    1.153862] usb 1-7: Product: USB DEVICE
[    1.153863] usb 1-7: Manufacturer: SONiX
[    1.155672] input: SONiX USB DEVICE as /devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7:1.0/0003:0C45:7638.0003/input/input4
[    1.246571] hid-generic 0003:0C45:7638.0003: input,hidraw2: USB HID v1.11 Keyboard [SONiX USB DEVICE] on usb-0000:00:14.0-7/input0
[    1.247941] input: SONiX USB DEVICE Keyboard as /devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7:1.1/0003:0C45:7638.0004/input/input5
[    1.298530] input: SONiX USB DEVICE as /devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7:1.1/0003:0C45:7638.0004/input/input6
[    1.298607] input: SONiX USB DEVICE Mouse as /devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7:1.1/0003:0C45:7638.0004/input/input7
[    1.298791] hid-generic 0003:0C45:7638.0004: input,hiddev97,hidraw3: USB HID v1.11 Keyboard [SONiX USB DEVICE] on usb-0000:00:14.0-7/input1
[    1.325385] tsc: Refined TSC clocksource calibration: 4199.999 MHz
[    1.325392] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x3c8a606e244, max_idle_ns: 440795282550 ns
[    1.325432] clocksource: Switched to clocksource tsc
[    1.410407] usb 1-8: new high-speed USB device number 4 using xhci_hcd
[    1.533910] usb 1-8: New USB device found, idVendor=1235, idProduct=8202, bcdDevice= 4.1b
[    1.533914] usb 1-8: New USB device strings: Mfr=1, Product=3, SerialNumber=0
[    1.533916] usb 1-8: Product: Scarlett 2i2 USB
[    1.533917] usb 1-8: Manufacturer: Focusrite
[    5.697575] [drm] amdgpu kernel modesetting enabled.
[    5.697679] amdgpu: Virtual CRAT table created for CPU
[    5.697686] amdgpu: Topology: Add CPU node
[    5.697757] amdgpu 0000:01:00.0: enabling device (0006 -> 0007)
[    5.697831] [drm] initializing kernel modesetting (POLARIS10 0x1002:0x67DF 0x1043:0x0519 0xE7).
[    5.697840] [drm] register mmio base: 0xDFA00000
[    5.697841] [drm] register mmio size: 262144
[    5.697895] amdgpu 0000:01:00.0: amdgpu: detected ip block number 0 <vi_common>
[    5.697897] amdgpu 0000:01:00.0: amdgpu: detected ip block number 1 <gmc_v8_0>
[    5.697898] amdgpu 0000:01:00.0: amdgpu: detected ip block number 2 <tonga_ih>
[    5.697899] amdgpu 0000:01:00.0: amdgpu: detected ip block number 3 <gfx_v8_0>
[    5.697900] amdgpu 0000:01:00.0: amdgpu: detected ip block number 4 <sdma_v3_0>
[    5.697901] amdgpu 0000:01:00.0: amdgpu: detected ip block number 5 <powerplay>
[    5.697902] amdgpu 0000:01:00.0: amdgpu: detected ip block number 6 <dm>
[    5.697903] amdgpu 0000:01:00.0: amdgpu: detected ip block number 7 <uvd_v6_0>
[    5.697905] amdgpu 0000:01:00.0: amdgpu: detected ip block number 8 <vce_v3_0>
[    5.697918] amdgpu 0000:01:00.0: amdgpu: Fetched VBIOS from VFCT
[    5.697920] amdgpu: ATOM BIOS: 115-D000PIL-100
[    5.698111] [drm] UVD is enabled in VM mode
[    5.698112] [drm] UVD ENC is enabled in VM mode
[    5.698113] [drm] VCE enabled in VM mode
[    5.712566] Console: switching to colour dummy device 80x25
[    5.722712] amdgpu 0000:01:00.0: vgaarb: deactivate vga console
[    5.722714] amdgpu 0000:01:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[    5.722752] [drm] vm size is 128 GB, 2 levels, block size is 10-bit, fragment size is 9-bit
[    5.722904] amdgpu 0000:01:00.0: amdgpu: VRAM: 8192M 0x000000F400000000 - 0x000000F5FFFFFFFF (8192M used)
[    5.722906] amdgpu 0000:01:00.0: amdgpu: GART: 256M 0x000000FF00000000 - 0x000000FF0FFFFFFF
[    5.722911] [drm] Detected VRAM RAM=8192M, BAR=256M
[    5.722912] [drm] RAM width 256bits GDDR5
[    5.723502] [drm] amdgpu: 8192M of VRAM memory ready
[    5.723503] [drm] amdgpu: 16029M of GTT memory ready.
[    5.723513] [drm] GART: num cpu pages 65536, num gpu pages 65536
[    5.723951] [drm] PCIE GART of 256M enabled (table at 0x000000F400300000).
[    5.724372] [drm] Chained IB support enabled!
[    5.725984] amdgpu: hwmgr_sw_init smu backed is polaris10_smu
[    5.727280] [drm] Found UVD firmware Version: 1.130 Family ID: 16
[    5.728221] [drm] Found VCE firmware Version: 53.26 Binary ID: 3
[    5.793705] [drm] Display Core v3.2.323 initialized on DCE 11.2
[    5.921130] [drm] UVD and UVD ENC initialized successfully.
[    6.022060] [drm] VCE initialized successfully.
[    6.023289] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[    6.023297] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[    6.023368] amdgpu: Virtual CRAT table created for GPU
[    6.023425] amdgpu: Topology: Add dGPU node [0x67df:0x1002]
[    6.023426] kfd kfd: amdgpu: added device 1002:67df
[    6.023435] amdgpu 0000:01:00.0: amdgpu: SE 4, SH per SE 1, CU per SH 9, active_cu_number 36
[    6.025698] amdgpu 0000:01:00.0: amdgpu: Using BOCO for runtime pm
[    6.026047] amdgpu 0000:01:00.0: [drm] Registered 6 planes with drm panic
[    6.026049] [drm] Initialized amdgpu 3.63.0 for 0000:01:00.0 on minor 1
[    6.037681] fbcon: amdgpudrmfb (fb0) is primary device
[    6.111585] Console: switching to colour frame buffer device 160x45
[    6.123467] amdgpu 0000:01:00.0: [drm] fb0: amdgpudrmfb frame buffer device
[    6.412875] BTRFS: device fsid 99c64621-2d97-4ee6-94de-4087696c5c2e devid 1 transid 882476 /dev/nvme0n1p2 (259:2) scanned by mount (292)
[    6.413444] BTRFS info (device nvme0n1p2): first mount of filesystem 99c64621-2d97-4ee6-94de-4087696c5c2e
[    6.413468] BTRFS info (device nvme0n1p2): using crc32c (crc32c-x86) checksum algorithm
[    6.413481] BTRFS info (device nvme0n1p2): using free-space-tree
[    6.666714] systemd[1]: systemd 257.6-1-arch running in system mode (+PAM +AUDIT -SELINUX -APPARMOR -IMA +IPE +SMACK +SECCOMP +GCRYPT +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBCRYPTSETUP_PLUGINS +LIBFDISK +PCRE2 +PWQUALITY +P11KIT +QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD +BPF_FRAMEWORK +BTF +XKBCOMMON +UTMP -SYSVINIT +LIBARCHIVE)
[    6.666723] systemd[1]: Detected architecture x86-64.
[    6.668211] systemd[1]: Hostname set to <archb>.
[    6.928373] systemd[1]: bpf-restrict-fs: LSM BPF program attached
[    7.195229] zram: Added device: zram0
[    7.287375] systemd[1]: /etc/systemd/system/amdgpu-metrics.service:3: Failed to add dependency on #, ignoring: Invalid argument
[    7.287382] systemd[1]: /etc/systemd/system/amdgpu-metrics.service:3: Failed to add dependency on Corrected, ignoring: Invalid argument
[    7.287386] systemd[1]: /etc/systemd/system/amdgpu-metrics.service:3: Failed to add dependency on service, ignoring: Invalid argument
[    7.287389] systemd[1]: /etc/systemd/system/amdgpu-metrics.service:3: Failed to add dependency on name, ignoring: Invalid argument
[    7.311428] systemd[1]: Queued start job for default target Graphical Interface.
[    7.330951] systemd[1]: Created slice Slice /system/dirmngr.
[    7.331841] systemd[1]: Created slice Slice /system/getty.
[    7.332158] systemd[1]: Created slice Slice /system/gpg-agent.
[    7.332476] systemd[1]: Created slice Slice /system/gpg-agent-browser.
[    7.332791] systemd[1]: Created slice Slice /system/gpg-agent-extra.
[    7.333098] systemd[1]: Created slice Slice /system/gpg-agent-ssh.
[    7.333414] systemd[1]: Created slice Slice /system/keyboxd.
[    7.333722] systemd[1]: Created slice Slice /system/modprobe.
[    7.334029] systemd[1]: Created slice Slice /system/systemd-fsck.
[    7.334340] systemd[1]: Created slice Slice /system/systemd-zram-setup.
[    7.334587] systemd[1]: Created slice User and Session Slice.
[    7.334659] systemd[1]: Started Forward Password Requests to Wall Directory Watch.
[    7.334806] systemd[1]: Set up automount Arbitrary Executable File Formats File System Automount Point.
[    7.334862] systemd[1]: Expecting device /dev/disk/by-uuid/60EC-2C28...
[    7.334896] systemd[1]: Expecting device /dev/disk/by-uuid/99c64621-2d97-4ee6-94de-4087696c5c2e...
[    7.334933] systemd[1]: Expecting device /dev/disk/by-uuid/D25B-C452...
[    7.334967] systemd[1]: Expecting device /dev/zram0...
[    7.334998] systemd[1]: Reached target Login Prompts.
[    7.335029] systemd[1]: Reached target Local Integrity Protected Volumes.
[    7.335080] systemd[1]: Reached target Slice Units.
[    7.335123] systemd[1]: Reached target Local Verity Protected Volumes.
[    7.335202] systemd[1]: Listening on Device-mapper event daemon FIFOs.
[    7.337136] systemd[1]: Listening on Process Core Dump Socket.
[    7.337557] systemd[1]: Listening on Credential Encryption/Decryption.
[    7.337660] systemd[1]: Listening on Journal Socket (/dev/log).
[    7.337755] systemd[1]: Listening on Journal Sockets.
[    7.337873] systemd[1]: Listening on Network Service Netlink Socket.
[    7.337926] systemd[1]: TPM PCR Measurements was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[    7.337935] systemd[1]: Make TPM PCR Policy was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[    7.337985] systemd[1]: Listening on udev Control Socket.
[    7.338052] systemd[1]: Listening on udev Kernel Socket.
[    7.338125] systemd[1]: Listening on User Database Manager Socket.
[    7.339776] systemd[1]: Mounting Huge Pages File System...
[    7.340650] systemd[1]: Mounting POSIX Message Queue File System...
[    7.341763] systemd[1]: Mounting Kernel Debug File System...
[    7.342686] systemd[1]: Mounting Kernel Trace File System...
[    7.344400] systemd[1]: Starting Create List of Static Device Nodes...
[    7.345915] systemd[1]: Starting Load Kernel Module configfs...
[    7.347120] systemd[1]: Starting Load Kernel Module dm_mod...
[    7.348629] systemd[1]: Starting Load Kernel Module drm...
[    7.350102] systemd[1]: Starting Load Kernel Module fuse...
[    7.351535] systemd[1]: Starting Load Kernel Module loop...
[    7.352284] systemd[1]: Clear Stale Hibernate Storage Info was skipped because of an unmet condition check (ConditionPathExists=/sys/firmware/efi/efivars/HibernateLocation-8cf2644b-4b0b-428f-9387-6d876050dc67).
[    7.353954] systemd[1]: Starting Journal Service...
[    7.356114] systemd[1]: Starting Load Kernel Modules...
[    7.358010] systemd[1]: Starting Generate network units from Kernel command line...
[    7.358653] systemd[1]: TPM PCR Machine ID Measurement was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[    7.359572] systemd[1]: Starting Remount Root and Kernel File Systems...
[    7.360225] systemd[1]: Early TPM SRK Setup was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[    7.361179] systemd[1]: Starting Load udev Rules from Credentials...
[    7.362662] systemd[1]: Starting Coldplug All udev Devices...
[    7.365798] loop: module loaded
[    7.366540] systemd[1]: Starting Virtual Console Setup...
[    7.370093] systemd[1]: Mounted Huge Pages File System.
[    7.370785] systemd[1]: Mounted POSIX Message Queue File System.
[    7.371612] systemd[1]: Mounted Kernel Debug File System.
[    7.372491] systemd[1]: Mounted Kernel Trace File System.
[    7.373477] systemd[1]: Finished Create List of Static Device Nodes.
[    7.374253] systemd[1]: modprobe@configfs.service: Deactivated successfully.
[    7.374398] systemd[1]: Finished Load Kernel Module configfs.
[    7.374414] systemd-journald[357]: Collecting audit messages is disabled.
[    7.375026] systemd[1]: modprobe@drm.service: Deactivated successfully.
[    7.375159] systemd[1]: Finished Load Kernel Module drm.
[    7.375848] systemd[1]: modprobe@fuse.service: Deactivated successfully.
[    7.375981] systemd[1]: Finished Load Kernel Module fuse.
[    7.376827] systemd[1]: modprobe@loop.service: Deactivated successfully.
[    7.376998] systemd[1]: Finished Load Kernel Module loop.
[    7.377974] systemd[1]: Finished Generate network units from Kernel command line.
[    7.379298] systemd[1]: Finished Load udev Rules from Credentials.
[    7.379939] BTRFS info (device nvme0n1p2 state M): use zstd compression, level 3
[    7.381285] systemd[1]: Finished Remount Root and Kernel File Systems.
[    7.382113] systemd[1]: Reached target Preparation for Network.
[    7.383593] systemd[1]: Mounting FUSE Control File System...
[    7.384827] systemd[1]: Mounting Kernel Configuration File System...
[    7.385302] i2c_dev: i2c /dev entries driver
[    7.385532] device-mapper: uevent: version 1.0.3
[    7.385607] device-mapper: ioctl: 4.49.0-ioctl (2025-01-17) initialised: dm-devel@lists.linux.dev
[    7.385657] systemd[1]: One time configuration for iscsi.service was skipped because of an unmet condition check (ConditionPathExists=!/etc/iscsi/initiatorname.iscsi).
[    7.386625] systemd[1]: Rebuild Hardware Database was skipped because no trigger condition checks were met.
[    7.387604] systemd[1]: Starting Load/Save OS Random Seed...
[    7.393733] Asymmetric key parser 'pkcs8' registered
[    7.397265] systemd[1]: Starting Create Static Device Nodes in /dev gracefully...
[    7.397781] systemd[1]: TPM SRK Setup was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[    7.398218] systemd[1]: modprobe@dm_mod.service: Deactivated successfully.
[    7.398347] systemd[1]: Finished Load Kernel Module dm_mod.
[    7.399067] systemd[1]: Finished Load Kernel Modules.
[    7.399733] systemd[1]: Finished Virtual Console Setup.
[    7.400448] systemd[1]: Mounted FUSE Control File System.
[    7.400862] systemd[1]: Mounted Kernel Configuration File System.
[    7.401299] systemd[1]: Repartition Root Disk was skipped because no trigger condition checks were met.
[    7.401974] systemd[1]: Starting Apply Kernel Variables...
[    7.402898] systemd[1]: Finished Load/Save OS Random Seed.
[    7.410065] systemd[1]: Finished Apply Kernel Variables.
[    7.411837] systemd[1]: Starting User Database Manager...
[    7.422543] systemd[1]: Started Journal Service.
[    7.594205] zram0: detected capacity change from 0 to 8388608
[    7.637831] Adding 4194300k swap on /dev/zram0.  Priority:100 extents:1 across:4194300k SSDsc
[    7.658751] mousedev: PS/2 mouse device common for all mice
[    7.713912] resource: resource sanity check: requesting [mem 0x00000000fdffe800-0x00000000fe0007ff], which spans more than pnp 00:07 [mem 0xfdb00000-0xfdffffff]
[    7.713918] caller get_primary_reg_base+0x4d/0xa0 [intel_pmc_core] mapping multiple BARs
[    7.713944] intel_pmc_core INT33A1:00:  initialized
[    7.730077] mc: Linux media interface: v0.10
[    7.732924] input: PC Speaker as /devices/platform/pcspkr/input/input8
[    7.734290] pps_core: LinuxPPS API ver. 1 registered
[    7.734292] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
[    7.745293] mei_me 0000:00:16.0: enabling device (0000 -> 0002)
[    7.758477] i801_smbus 0000:00:1f.4: SMBus using PCI interrupt
[    7.761275] PTP clock support registered
[    7.764516] i2c i2c-8: Successfully instantiated SPD at 0x51
[    7.765046] i2c i2c-8: Successfully instantiated SPD at 0x52
[    7.833847] iTCO_vendor_support: vendor-support=0
[    7.834079] e1000e: Intel(R) PRO/1000 Network Driver
[    7.834081] e1000e: Copyright(c) 1999 - 2015 Intel Corporation.
[    7.834291] e1000e 0000:00:1f.6: Interrupt Throttling Rate (ints/sec) set to dynamic conservative mode
[    7.835015] cfg80211: Loading compiled-in X.509 certificates for regulatory database
[    7.836385] ee1004 8-0051: 512 byte EE1004-compliant SPD EEPROM, read-only
[    7.837822] ee1004 8-0052: 512 byte EE1004-compliant SPD EEPROM, read-only
[    7.838739] Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
[    7.838842] Loaded X.509 cert 'wens: 61c038651aabdcf94bd0ac7ff06c7248db18c600'
[    7.843430] RAPL PMU: API unit is 2^-32 Joules, 3 fixed counters, 655360 ms ovfl timer
[    7.843433] RAPL PMU: hw unit of domain pp0-core 2^-14 Joules
[    7.843434] RAPL PMU: hw unit of domain package 2^-14 Joules
[    7.843434] RAPL PMU: hw unit of domain dram 2^-14 Joules
[    7.848496] iTCO_wdt iTCO_wdt: Found a Intel PCH TCO device (Version=4, TCOBASE=0x0400)
[    7.848679] iTCO_wdt iTCO_wdt: initialized. heartbeat=30 sec (nowayout=0)
[    7.853095] cryptd: max_cpu_qlen set to 1000
[    7.868341] AES CTR mode by8 optimization enabled
[    7.915558] snd_hda_intel 0000:00:1f.3: enabling device (0000 -> 0002)
[    7.915814] snd_hda_intel 0000:01:00.1: enabling device (0000 -> 0002)
[    7.915887] snd_hda_intel 0000:01:00.1: Force to non-snoop mode
[    7.927667] snd_hda_intel 0000:01:00.1: bound 0000:01:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
[    7.929177] input: HDA ATI HDMI HDMI/DP,pcm=3 as /devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card2/input9
[    7.929218] input: HDA ATI HDMI HDMI/DP,pcm=7 as /devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card2/input10
[    7.929263] input: HDA ATI HDMI HDMI/DP,pcm=8 as /devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card2/input11
[    7.929302] input: HDA ATI HDMI HDMI/DP,pcm=9 as /devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card2/input12
[    7.929340] input: HDA ATI HDMI HDMI/DP,pcm=10 as /devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card2/input13
[    7.929390] input: HDA ATI HDMI HDMI/DP,pcm=11 as /devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card2/input14
[    7.937978] usbcore: registered new interface driver snd-usb-audio
[    7.963720] snd_hda_codec_realtek hdaudioC1D0: autoconfig for ALC892: line_outs=4 (0x14/0x15/0x16/0x17/0x0) type:line
[    7.963724] snd_hda_codec_realtek hdaudioC1D0:    speaker_outs=0 (0x0/0x0/0x0/0x0/0x0)
[    7.963726] snd_hda_codec_realtek hdaudioC1D0:    hp_outs=1 (0x1b/0x0/0x0/0x0/0x0)
[    7.963727] snd_hda_codec_realtek hdaudioC1D0:    mono: mono_out=0x0
[    7.963728] snd_hda_codec_realtek hdaudioC1D0:    inputs:
[    7.963729] snd_hda_codec_realtek hdaudioC1D0:      Rear Mic=0x18
[    7.963731] snd_hda_codec_realtek hdaudioC1D0:      Front Mic=0x19
[    7.963732] snd_hda_codec_realtek hdaudioC1D0:      Line=0x1a
[    7.984696] usbcore: registered new interface driver brcmfmac
[    7.984724] brcmfmac 0000:04:00.0: enabling device (0000 -> 0002)
[    7.997709] input: HDA Intel PCH Rear Mic as /devices/pci0000:00/0000:00:1f.3/sound/card1/input15
[    7.997748] input: HDA Intel PCH Front Mic as /devices/pci0000:00/0000:00:1f.3/sound/card1/input16
[    7.997783] input: HDA Intel PCH Line as /devices/pci0000:00/0000:00:1f.3/sound/card1/input17
[    7.997817] input: HDA Intel PCH Line Out Front as /devices/pci0000:00/0000:00:1f.3/sound/card1/input18
[    7.997854] input: HDA Intel PCH Line Out Surround as /devices/pci0000:00/0000:00:1f.3/sound/card1/input19
[    7.997887] input: HDA Intel PCH Line Out CLFE as /devices/pci0000:00/0000:00:1f.3/sound/card1/input20
[    7.997919] input: HDA Intel PCH Line Out Side as /devices/pci0000:00/0000:00:1f.3/sound/card1/input21
[    7.997952] input: HDA Intel PCH Front Headphone as /devices/pci0000:00/0000:00:1f.3/sound/card1/input22
[    8.092157] intel_tcc_cooling: Programmable TCC Offset detected
[    8.093686] brcmfmac: brcmf_fw_alloc_request: using brcm/brcmfmac4366c-pcie for chip BCM4366/4
[    8.097951] brcmfmac 0000:04:00.0: Direct firmware load for brcm/brcmfmac4366c-pcie.MSI-MS-7A69.bin failed with error -2
[    8.103036] brcmfmac 0000:04:00.0: Direct firmware load for brcm/brcmfmac4366c-pcie.txt failed with error -2
[    8.103390] brcmfmac 0000:04:00.0: Direct firmware load for brcm/brcmfmac4366c-pcie.clm_blob failed with error -2
[    8.103442] brcmfmac 0000:04:00.0: Direct firmware load for brcm/brcmfmac4366c-pcie.txcap_blob failed with error -2
[    8.140246] intel_rapl_common: Found RAPL domain package
[    8.140249] intel_rapl_common: Found RAPL domain core
[    8.140251] intel_rapl_common: Found RAPL domain dram
[    8.212925] e1000e 0000:00:1f.6 0000:00:1f.6 (uninitialized): registered PHC clock
[    8.276073] e1000e 0000:00:1f.6 eth0: (PCI Express:2.5GT/s:Width x1) 4c:cc:6a:b9:92:56
[    8.276076] e1000e 0000:00:1f.6 eth0: Intel(R) PRO/1000 Network Connection
[    8.276153] e1000e 0000:00:1f.6 eth0: MAC: 12, PHY: 12, PBA No: FFFFFF-0FF
[    8.277818] e1000e 0000:00:1f.6 enp0s31f6: renamed from eth0
[    8.425897] exFAT-fs (sda2): Volume was not properly unmounted. Some data may be corrupt. Please run fsck.
[    8.426841] systemd-journald[357]: Received client request to flush runtime journal.
[    8.875249] brcmfmac: brcmf_c_process_clm_blob: no clm_blob available (err=-2), device may have limited channels available
[    8.875711] brcmfmac: brcmf_c_process_txcap_blob: no txcap_blob available (err=-2)
[    8.878555] brcmfmac: brcmf_c_preinit_dcmds: Firmware: BCM4366/4 wl0: Nov  5 2018 03:19:56 version 10.28.2 (r769115) FWID 01-d2cbb8fd
[   10.103620] NET: Registered PF_ALG protocol family
[   10.112805] nct6775: Found NCT6795D or compatible chip at 0x4e:0xa20
[   10.432344] fs-verity: sha256 using implementation "sha256-avx2"
[   11.984088] ieee80211 phy0: brcmf_p2p_send_action_frame: Unknown Frame: category 0x5, action 0x4
[   15.727076] Bluetooth: Core ver 2.22
[   15.727099] NET: Registered PF_BLUETOOTH protocol family
[   15.727100] Bluetooth: HCI device and connection manager initialized
[   15.727103] Bluetooth: HCI socket layer initialized
[   15.727105] Bluetooth: L2CAP socket layer initialized
[   15.727107] Bluetooth: SCO socket layer initialized
[   16.253058] ieee80211 phy0: brcmf_inetaddr_changed: fail to get arp ip table err:-52
[   16.298613] Loading iSCSI transport class v2.0-870.
[   16.378195] iscsi: registered transport (tcp)
[   17.164792] Initializing XFRM netlink socket
[   17.531366] docker0: port 1(veth0714ffe) entered blocking state
[   17.531384] docker0: port 1(veth0714ffe) entered disabled state
[   17.531388] veth0714ffe: entered allmulticast mode
[   17.531416] veth0714ffe: entered promiscuous mode
[   17.537229] systemd-journald[357]: Time jumped backwards, rotating.
[   17.555220] eth0: renamed from veth3abe362
[   17.555546] docker0: port 1(veth0714ffe) entered blocking state
[   17.555549] docker0: port 1(veth0714ffe) entered forwarding state
[   21.982754] nvme nvme0: using unchecked data buffer
[   22.029031] block nvme0n1: No UUID available providing old NGUID
[   25.313449] warning: `kdeconnectd' uses wireless extensions which will stop working for Wi-Fi 7 hardware; use nl80211
[ 1009.043468] ieee80211 phy0: brcmf_inetaddr_changed: fail to get arp ip table err:-52
[ 1010.371437] ieee80211 phy0: brcmf_p2p_send_action_frame: Unknown Frame: category 0x5, action 0x4
[ 1015.345795] ieee80211 phy0: brcmf_inetaddr_changed: fail to get arp ip table err:-52
[ 1354.638195] docker0: port 2(veth0e370b4) entered blocking state
[ 1354.638208] docker0: port 2(veth0e370b4) entered disabled state
[ 1354.638234] veth0e370b4: entered allmulticast mode
[ 1354.638614] veth0e370b4: entered promiscuous mode
[ 1354.907352] eth0: renamed from vethaad7476
[ 1354.908884] docker0: port 2(veth0e370b4) entered blocking state
[ 1354.908894] docker0: port 2(veth0e370b4) entered forwarding state
[ 1468.462936] BUG: kernel NULL pointer dereference, address: 0000000000000000
[ 1468.462941] #PF: supervisor instruction fetch in kernel mode
[ 1468.462942] #PF: error_code(0x0010) - not-present page
[ 1468.462943] PGD 8000000639afa067 P4D 8000000639afa067 PUD 60fd0f067 PMD 0 
[ 1468.462947] Oops: Oops: 0010 [#1] PREEMPT SMP PTI
[ 1468.462949] CPU: 3 UID: 0 PID: 17966 Comm: python3 Not tainted 6.14.0-rc4-bisect-01301-g0747acf33112 #1 c5c0e2982c78d1b98d8fb9b1675f53ea62c3f6bf
[ 1468.462952] Hardware name: MSI MS-7A69/Z270M MORTAR (MS-7A69), BIOS 1.60 06/29/2018
[ 1468.462954] RIP: 0010:0x0
[ 1468.462972] Code: Unable to access opcode bytes at 0xffffffffffffffd6.
[ 1468.462973] RSP: 0018:ffff9dd2c82ffb60 EFLAGS: 00010246
[ 1468.462975] RAX: 0000000000000000 RBX: ffff8c4e6ab06400 RCX: 0000000000000002
[ 1468.462976] RDX: 0000000000000000 RSI: 0000000000000000 RDI: ffff8c4e61a80000
[ 1468.462977] RBP: 0000000000000000 R08: 0000000000000003 R09: ffff8c4e8b7d4780
[ 1468.462978] R10: ffff8c530333aa10 R11: 000000ff00aed800 R12: ffff8c4e6ab064e8
[ 1468.462979] R13: 00000000ffffffff R14: 0000000000000000 R15: 0000000000000002
[ 1468.462980] FS:  00007f092753f6c0(0000) GS:ffff8c558eb80000(0000) knlGS:0000000000000000
[ 1468.462982] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[ 1468.462983] CR2: ffffffffffffffd6 CR3: 0000000634a78005 CR4: 00000000003726f0
[ 1468.462984] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
[ 1468.462985] DR3: 0000000000000000 DR6: 00000000fffe0ff0 DR7: 0000000000000400
[ 1468.462986] Call Trace:
[ 1468.462988]  <TASK>
[ 1468.462989]  ? __die_body.cold+0x19/0x2b
[ 1468.462993]  ? page_fault_oops+0x15e/0x310
[ 1468.462997]  ? exc_page_fault+0x81/0x1b0
[ 1468.463000]  ? asm_exc_page_fault+0x26/0x30
[ 1468.463005]  unmap_queues_cpsch+0x1d6/0x2f0 [amdgpu 34bea62c824d89c2348ab9fb9a464be99c710640]
[ 1468.463396]  execute_queues_cpsch.constprop.0+0x46/0x90 [amdgpu 34bea62c824d89c2348ab9fb9a464be99c710640]
[ 1468.463676]  create_queue_cpsch+0x3d9/0x4d0 [amdgpu 34bea62c824d89c2348ab9fb9a464be99c710640]
[ 1468.463954]  pqm_create_queue+0x1f3/0x5b0 [amdgpu 34bea62c824d89c2348ab9fb9a464be99c710640]
[ 1468.464230]  kfd_ioctl_create_queue+0x24c/0x660 [amdgpu 34bea62c824d89c2348ab9fb9a464be99c710640]
[ 1468.464503]  kfd_ioctl+0x2d2/0x4b0 [amdgpu 34bea62c824d89c2348ab9fb9a464be99c710640]
[ 1468.464774]  ? __pfx_kfd_ioctl_create_queue+0x10/0x10 [amdgpu 34bea62c824d89c2348ab9fb9a464be99c710640]
[ 1468.465047]  ? blk_finish_plug+0x26/0x40
[ 1468.465052]  __x64_sys_ioctl+0x94/0xc0
[ 1468.465055]  do_syscall_64+0x7b/0x190
[ 1468.465059]  ? irqentry_exit_to_user_mode+0x2c/0x1b0
[ 1468.465062]  entry_SYSCALL_64_after_hwframe+0x76/0x7e
[ 1468.465064] RIP: 0033:0x7f0a82f97ded
[ 1468.465073] Code: 04 25 28 00 00 00 48 89 45 c8 31 c0 48 8d 45 10 c7 45 b0 10 00 00 00 48 89 45 b8 48 8d 45 d0 48 89 45 c0 b8 10 00 00 00 0f 05 <89> c2 3d 00 f0 ff ff 77 1a 48 8b 45 c8 64 48 2b 04 25 28 00 00 00
[ 1468.465074] RSP: 002b:00007f092753b870 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
[ 1468.465076] RAX: ffffffffffffffda RBX: 0000000000000001 RCX: 00007f0a82f97ded
[ 1468.465077] RDX: 00007f092753b970 RSI: 00000000c0604b02 RDI: 0000000000000003
[ 1468.465078] RBP: 00007f092753b8c0 R08: 0000000000000001 R09: 000000000000b400
[ 1468.465080] R10: 00007f092753b970 R11: 0000000000000246 R12: 00000000c0604b02
[ 1468.465081] R13: 0000000000000003 R14: 000000003d827000 R15: 0000000000000000
[ 1468.465084]  </TASK>
[ 1468.465084] Modules linked in: xt_nat xt_tcpudp snd_seq_dummy snd_hrtimer snd_seq nf_conntrack_netlink iptable_raw veth xt_conntrack xt_MASQUERADE bridge stp llc ip6table_nat ip6table_filter ip6_tables xt_set ip_set iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype iptable_filter xfrm_user xfrm_algo iscsi_tcp libiscsi_tcp libiscsi scsi_transport_iscsi bluetooth overlay ccm algif_aead crypto_null des3_ede_x86_64 des_generic libdes algif_skcipher cmac md4 nct6775 algif_hash nct6775_core af_alg hwmon_vid brcmfmac_bca vfat fat exfat intel_rapl_msr intel_rapl_common intel_uncore_frequency intel_uncore_frequency_common intel_tcc_cooling x86_pkg_temp_thermal intel_powerclamp coretemp kvm_intel kvm snd_soc_avs snd_soc_hda_codec brcmfmac snd_hda_ext_core snd_hda_codec_realtek snd_soc_core snd_hda_codec_generic snd_hda_scodec_component snd_hda_codec_hdmi snd_compress snd_hda_intel snd_usb_audio polyval_clmulni snd_intel_dspcfg polyval_generic snd_hda_codec ghash_clmulni_intel mmc_core sha512_ssse3
[ 1468.465125]  sha1_ssse3 aesni_intel snd_hda_core snd_usbmidi_lib crypto_simd snd_ump cryptd iTCO_wdt snd_hwdep rapl intel_pmc_bxt e1000e ee1004 mei_hdcp mei_pxp iTCO_vendor_support snd_pcm intel_cstate snd_rawmidi cfg80211 snd_seq_device snd_timer ptp i2c_i801 snd intel_uncore mei_me intel_wmi_thunderbolt i2c_smbus pps_core mc pcspkr brcmutil mei mxm_wmi intel_pmc_core soundcore pmt_telemetry pmt_class joydev acpi_pad intel_vsec mousedev rfkill mac_hid pkcs8_key_parser i2c_dev dm_mod crypto_user loop nfnetlink zram 842_decompress lz4hc_compress lz4_compress 842_compress ip_tables x_tables amdgpu amdxcp i2c_algo_bit drm_ttm_helper ttm drm_exec gpu_sched drm_suballoc_helper drm_panel_backlight_quirks drm_buddy nvme drm_display_helper nvme_core sha256_ssse3 cec nvme_auth video wmi uas usb_storage
[ 1468.465165] CR2: 0000000000000000
[ 1468.465167] ---[ end trace 0000000000000000 ]---
[ 1468.465168] RIP: 0010:0x0
[ 1468.465171] Code: Unable to access opcode bytes at 0xffffffffffffffd6.
[ 1468.465172] RSP: 0018:ffff9dd2c82ffb60 EFLAGS: 00010246
[ 1468.465174] RAX: 0000000000000000 RBX: ffff8c4e6ab06400 RCX: 0000000000000002
[ 1468.465175] RDX: 0000000000000000 RSI: 0000000000000000 RDI: ffff8c4e61a80000
[ 1468.465176] RBP: 0000000000000000 R08: 0000000000000003 R09: ffff8c4e8b7d4780
[ 1468.465177] R10: ffff8c530333aa10 R11: 000000ff00aed800 R12: ffff8c4e6ab064e8
[ 1468.465178] R13: 00000000ffffffff R14: 0000000000000000 R15: 0000000000000002
[ 1468.465179] FS:  00007f092753f6c0(0000) GS:ffff8c558eb80000(0000) knlGS:0000000000000000
[ 1468.465180] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[ 1468.465181] CR2: ffffffffffffffd6 CR3: 0000000634a78005 CR4: 00000000003726f0
[ 1468.465182] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
[ 1468.465183] DR3: 0000000000000000 DR6: 00000000fffe0ff0 DR7: 0000000000000400
[ 1468.465184] note: python3[17966] exited with irqs disabled
```

---

### 评论 #7 — schung-amd (2025-07-23T16:11:58Z)

Hi @mikosenigma, sorry for the delay on this, and thanks @chboishabba for the extensive investigation! As you've seen, we don't have support for kernel version 6.15 and later yet: see https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html. I haven't tested the new ROCm 6.4.2 release with kernel 6.15 myself yet, but I don't expect it to fix this.

I don't think we currently have plans to support newer kernel versions than the current kernels for our officially supported distros, so we will always be falling behind bleeding edge. However we are aware that many users are asking for support for new and upcoming kernel versions, and hopefully we can accelerate enablement and support for new kernel versions in the future. For now I recommend falling back to a known working kernel version if ROCm is required, sorry for the inconvenience.

---

### 评论 #8 — chboishabba (2025-07-23T21:51:23Z)

@schung-amd I believe compatibility for Rx 580 was deprecated in roc 5.7.1
under lts kernel. I had passed some issues up the chain regarding kfd reset
(see above log) and doorbell issues causing whole system lockup and
eventual crash (resulting in journal corruption) which I believe are set to
be integrated into next kernel minor. I believe you will find most people
are happy to run driver versions well behind current, in order to access
newer ML software versions.

On Thu, 24 July 2025, 2:12 am schung-amd, ***@***.***> wrote:

> *schung-amd* left a comment (ROCm/ROCm#4919)
> <https://github.com/ROCm/ROCm/issues/4919#issuecomment-3109275222>
>
> Hi @mikosenigma <https://github.com/mikosenigma>, sorry for the delay on
> this, and thanks @chboishabba <https://github.com/chboishabba> for the
> extensive investigation! As you've seen, we don't have support for kernel
> version 6.15 and later yet: see
> https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html.
> I haven't tested the new ROCm 6.4.2 release with kernel 6.15 myself yet,
> but I don't expect it to fix this.
>
> I don't think we currently have plans to support newer kernel versions
> than the current kernels for our officially supported distros, so we will
> always be falling behind bleeding edge. However we are aware that many
> users are asking for support for new and upcoming kernel versions, and
> hopefully we can accelerate enablement and support for new kernel versions
> in the future. For now I recommend falling back to a known working kernel
> version if ROCm is required, sorry for the inconvenience.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4919#issuecomment-3109275222>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AGM4B3XQ7XDBDG74T75BYUL3J6X6HAVCNFSM6AAAAAB7F77V4OVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTCMBZGI3TKMRSGI>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #9 — schung-amd (2025-07-31T19:46:33Z)

Closing for now as I don't think we have mainline support planned for kernel 6.15 until the Ubuntu HWE kernel version is at or beyond that point. Please revert to a previous working kernel and/or ROCm version if you need to use ROCm.

For hardware that has been dropped from mainline support, there may be some support via TheRock (https://github.com/ROCm/TheRock, also see device wishlist at https://github.com/ROCm/ROCm/discussions/4276).

@mikosenigma For the Nobara issue specifically, if you provide some logs of failures on your system we may be able to help. We don't have mainline support for Nobara, the Fedora packages that are used on Nobara are based on a mainline ROCm release but I doubt they have been validated on Nobara or with an RDNA2 GPU. Please comment when you are able to provide more information and we can reopen this if necessary.



---
