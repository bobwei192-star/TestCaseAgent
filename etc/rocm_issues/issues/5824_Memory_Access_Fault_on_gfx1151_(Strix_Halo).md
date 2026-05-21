# Memory Access Fault on gfx1151 (Strix Halo)

> **Issue #5824**
> **状态**: closed
> **创建时间**: 2025-12-29T18:48:26Z
> **更新时间**: 2026-01-26T03:21:06Z
> **关闭时间**: 2026-01-23T09:25:17Z
> **作者**: adamskrodzki
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5824

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

# AMD ROCm Bug Report: Memory Access Fault on gfx1151 (Strix Halo)

## Summary

Basic PyTorch GPU memory operations crash with "Memory access fault by GPU node-1" on AMD Radeon 8060S (gfx1151 / Strix Halo). Even the simplest possible GPU tensor creation fails.

## Minimal Reproducer

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")  # True
print(f"Device: {torch.cuda.get_device_name(0)}")      # AMD Radeon 8060S
x = torch.tensor([1.0, 2.0, 3.0]).cuda()               # CRASHES HERE
```

**Environment variables used:**
```bash
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 HSA_OVERRIDE_GFX_VERSION=11.0.0 python test.py
```

## Error Output

```
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
CUDA available: True
Device: AMD Radeon 8060S
Memory access fault by GPU node-1 (Agent handle: 0x1b376c50) on address 0x7f762a667000. Reason: Page not present or supervisor privilege.
Aborted (core dumped)
```

## System Information

### Hardware
- **CPU**: AMD Ryzen AI Max+ 395 (Strix Halo)
- **GPU**: AMD Radeon 8060S (gfx1151)
- **RAM**: 128GB (32GB CPU / 96GB GPU unified memory)

### Software Versions
- **OS**: Nobara Linux 43 (Fedora-based)
- **Kernel**: 6.17.8-200.nobara.fc43.x86_64
- **linux-firmware**: 20250808-1.fc42
- **ROCm Runtime**: 6.3.1-4.fc42
- **ROCm Core**: 6.3.1-2.fc42
- **PyTorch**: 2.9.1+rocm6.3

### Kernel Boot Parameters
```
amd_iommu=off ttm.pages_limit=25165824 ttm.page_pool_size=25165824
```

### ROCm Packages Installed
```
rocm-runtime-6.3.1-4.fc42.x86_64
rocm-core-6.3.1-2.fc42.x86_64
rocm-hip-6.3.1-4.fc42.x86_64
rocm-opencl-6.3.1-4.fc42.x86_64
rocm-smi-6.3.1-3.fc42.x86_64
rocm-device-libs-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-libs-18-37.rocm6.3.1.fc42.x86_64
rocm-comgr-18-37.rocm6.3.1.fc42.x86_64
```

## What I've Tried

| Configuration | Result |
|--------------|--------|
| linux-firmware 20251125 | Crash |
| linux-firmware 20250808 | Crash |
| Kernel 6.18.2 | Crash |
| Kernel 6.17.8 | Crash |
| ROCm 7.1.1 (via Docker) | Crash |
| ROCm 6.3.1 | Crash |
| amdgpu.cwsr_enable=0 | Crash |
| amd_iommu=off | Crash |
| ttm.pages_limit=25165824 | Crash |
| HSA_OVERRIDE_GFX_VERSION=11.0.0 | Crash |
| HSA_OVERRIDE_GFX_VERSION=11.0.3 | Crash |

## Additional Information

### GPU Detection Works
```bash
$ amd-smi
GPU-Name: Radeon 8060S Graphics
Mem-Usage: 874/98304 MB
```

### GTT Memory is Correct
```bash
$ sudo dmesg | grep -i "gtt memory"
amdgpu: 98304M of GTT memory ready.
```

### Previously Working
This configuration was working on **December 18, 2025**. The issue started after a system update on **December 29, 2025** which upgraded 1510+ packages including ROCm 6.3.1 → 7.1.1 and linux-firmware. Downgrading did not restore functionality.

## Expected Behavior

Simple tensor operations should work on gfx1151 GPU without memory access faults.

## Actual Behavior

Any GPU memory operation triggers "Memory access fault by GPU node-1" with "Page not present or supervisor privilege" error.

## Related Issues

- https://github.com/ROCm/ROCm/issues/5616 (Strix Point memory issues)
- AMD Strix Halo gfx1151 is a newer variant that may have similar issues

## Contact

Please let me know if you need any additional diagnostic information.


---

## 评论 (11 条)

### 评论 #1 — amd-nicknick (2025-12-31T06:27:01Z)

@adamskrodzki, please use TheRock nighlies for Strix Halo, you could use the prebuilt wheels:
https://github.com/ROCm/TheRock/blob/main/RELEASES.md#torch-for-gfx1151

Also, **do not** use the variable `HSA_OVERRIDE_GFX_VERSION`, and do not disable IOMMU.

---

### 评论 #2 — adamskrodzki (2025-12-31T12:32:32Z)

Thank you for the suggestion. Provided I've run everything correctly I installed TheRock nightlies as advised

````
# Uninstall current PyTorch
pip uninstall torch torchvision torchaudio pytorch-triton-rocm -y

# Install from TheRock nightlies for gfx1151
pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch torchaudio torchvision

# Update GRUB and reboot
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo reboot
````

To validate my installation I've run following script:

````
# 1. Environment variables (should all be empty/unset)
echo "HSA_OVERRIDE_GFX_VERSION=$HSA_OVERRIDE_GFX_VERSION"
echo "TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=$TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL"
echo "AMD_IFACE=$AMD_IFACE"

# 2. Kernel cmdline (should NOT have amd_iommu=off)
cat /proc/cmdline

# 3. PyTorch version (should be from TheRock, e.g., 2.10+therock or similar)
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'HIP: {torch.version.hip}')"

# 4. Check pip source of torch
pip show torch | grep -E "Name|Version|Location"

# 5. System ROCm packages
rpm -qa | grep -i rocm

# 6. Kernel and firmware
uname -r
rpm -qa | grep linux-firmware

# 7. GPU info
python -c "import torch; print(torch.cuda.get_device_name(0))"

````

That resulted in following output:

````
HSA_OVERRIDE_GFX_VERSION=
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=
AMD_IFACE=
BOOT_IMAGE=(hd0,gpt5)/vmlinuz-6.17.8-200.nobara.fc43.x86_64 root=UUID=5f2126d7-c671-43f5-8d0e-f8569fbcb951 ro rootflags=subvol=@ quiet splash ttm.pages_limit=25165824 ttm.page_pool_size=25165824
PyTorch: 2.10.0a0+rocm7.10.0a20251015
HIP: 7.1.25413-7721681424
Name: torch
Version: 2.10.0a0+rocm7.10.0a20251015
Location: /home/adam/.pyenv/versions/3.11.9/lib/python3.11/site-packages
perl-FCGI-ProcManager-0.28-26.fc43.noarch
rocm-rpm-macros-7.1.0-3.fc43.noarch
rocm-clinfo-7.1.1-1.fc43.x86_64
rocm-cmake-7.1.0-1.fc43.noarch
rocminfo-7.1.0-1.fc43.x86_64
rocm-comgr-18-37.rocm6.3.1.fc42.x86_64
rocm-runtime-6.3.1-4.fc42.x86_64
rocm-llvm-filesystem-18-37.rocm6.3.1.fc42.x86_64
rocm-libc++-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-libs-18-37.rocm6.3.1.fc42.x86_64
rocm-clang-libs-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-static-18-37.rocm6.3.1.fc42.x86_64
rocm-lld-18-37.rocm6.3.1.fc42.x86_64
rocm-libc++-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-runtime-devel-6.3.1-4.fc42.x86_64
rocm-clang-runtime-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-clang-18-37.rocm6.3.1.fc42.x86_64
rocm-clang-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-device-libs-18-37.rocm6.3.1.fc42.x86_64
hipcc-18-37.rocm6.3.1.fc42.x86_64
rocm-hip-6.3.1-4.fc42.x86_64
rocm-comgr-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-hip-devel-6.3.1-4.fc42.x86_64
rocm-opencl-6.3.1-4.fc42.x86_64
rocm-smi-6.3.1-3.fc42.x86_64
rocm-core-6.3.1-2.fc42.x86_64
6.17.8-200.nobara.fc43.x86_64
linux-firmware-whence-20250808-1.fc42.noarch
linux-firmware-20250808-1.fc42.noarch
Radeon 8060S Graphics
````



running reproducer results in following error:

````

CUDA available: True
Device: Radeon 8060S Graphics
Memory access fault by GPU node-1 (Agent handle: 0x8415330) on address 0x7f870141a000. Reason: Page not present or supervisor privilege.
````



I would appreciate any and all further help. Please let me know if I installed something incorrectly.

---

### 评论 #3 — adamskrodzki (2026-01-03T16:32:49Z)

Also feel free to suggest any debug scripts / linux commands that I can run on my computer that will help you identify what an issue is.

---

### 评论 #4 — bondwell79 (2026-01-04T09:23:01Z)

Check another thread: https://github.com/ROCm/ROCm/issues/5724 (same error)

---

### 评论 #5 — amd-nicknick (2026-01-08T07:07:49Z)

@adamskrodzki, could you check the MES FW you're currently using?
Check the output of `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info`


---

### 评论 #6 — Kortyburns (2026-01-11T07:44:45Z)

@adamskrodzki I had the same issue. The fix was to update the AMD FW (usr/lib/firmware/amd...). I don't remember well (because i tried soo many different things), so please find below the summary of the solution, as summarized by LLM:

-------
"Forward-Fix" Firmware (Dec 4, 2025)
The default Fedora package (`20251125`) contains a GFX1151 regression. The solution is to manually hotfix the firmware blobs from the upstream Linux tree.
- **Commit**: `amdgpu: update GC 11.5.1 firmware` (Dec 4, 2025)
- **Target Files**: `/usr/lib/firmware/amdgpu/gc_11_5_1_*`
- **Effect**: Reverts MES to `0x80`, resolving `GCVM_L2_PROTECTION_FAULT`.

Using the last FW version, the memory access issues were gone, resulting a fine tune from 18hours (CPU) into 10min (GPU)

HTH

---

### 评论 #7 — amd-nicknick (2026-01-15T09:49:25Z)

@Kortyburns, I just checked Fedora has promoted a new FW package `linux-firmware-20260110-1`, there should be no need to manually revert the firmware now. Could you please try updating the package with dnf and give it a try? Thanks!
@adamskrodzki, pinging you again to see if you're still reproducing the issue?

---

### 评论 #8 — amd-nicknick (2026-01-23T09:25:17Z)

Closing this issue for now due to inactivity, if you are still facing the same issue, please reopen this issue and attach latest information. Thanks!

---

### 评论 #9 — adamskrodzki (2026-01-23T11:55:16Z)

Sorry for lack of response, 
I took advice and checked 
#5724 

and when I downgraded 
https://github.com/ROCm/ROCm/issues/5724#issuecomment-3708369843

It worked, 

Today I've tried to update to latest kernel and firmware and rocm

my current versions are:

vmlinuz-6.18.6-200.nobara.fc43.x86_64
linux-firmware-20260110-1.fc43.noarch

Script from the top causes  "Segmentation fault"

It may be due to ROCm being on 7.1.1 I cauldn't install ROCm 7.2 on Fedora 

keep seing

Status code: 404 for https://repo.radeon.com/rocm/yum/7.2.0/main/repodata/repomd.xml (IP: 95.101.116.92) - https://repo.radeon.com/rocm/yum


@amd-nicknick 


---

### 评论 #10 — adamskrodzki (2026-01-23T17:01:53Z)

````
HSA_OVERRIDE_GFX_VERSION=11.5.1
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
AMD_IFACE=
BOOT_IMAGE=(hd0,gpt5)/vmlinuz-6.18.6-200.nobara.fc43.x86_64 root=UUID=5f2126d7-c671-43f5-8d0e-f8569fbcb951 ro rootflags=subvol=@ quiet splash ttm.pages_limit=25165824 ttm.page_pool_size=25165824 amdgpu.cwsr_enable=0
PyTorch: 2.10.0a0+rocm7.10.0a20251015
HIP: 7.1.25413-7721681424
Name: torch
Version: 2.10.0a0+rocm7.10.0a20251015
Location: /home/adam/.pyenv/versions/3.11.9/lib/python3.11/site-packages
perl-FCGI-ProcManager-0.28-26.fc43.noarch
6.18.6-200.nobara.fc43.x86_64
linux-firmware-whence-20260110-1.fc43.noarch
amd-gpu-firmware-20260110-1.fc43.noarch
intel-gpu-firmware-20260110-1.fc43.noarch
linux-firmware-20260110-1.fc43.noarch
nvidia-gpu-firmware-20260110-1.fc43.noarch
[sudo] password for adam: 
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
Radeon 8060S Graphics
````
those are my current versions

---

### 评论 #11 — amd-nicknick (2026-01-26T03:21:06Z)

Hi @adamskrodzki, the ROCm 7.2 track (the legacy release track) does not support Fedora officially, so the 404 you're seeing is expected for yum, as we're no longer updating that package list.

You could check the docs to find the supported configuration matrix:
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/native_linux/native_linux_compatibility.html

If you'd like to stick on Fedora, we also build manylinux wheels for PyTorch, available for 7.2 here: https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/
Alternatively, you could use the latest TheRock nightlies if you encounter any problems.
https://github.com/ROCm/TheRock/blob/main/RELEASES.md

---
