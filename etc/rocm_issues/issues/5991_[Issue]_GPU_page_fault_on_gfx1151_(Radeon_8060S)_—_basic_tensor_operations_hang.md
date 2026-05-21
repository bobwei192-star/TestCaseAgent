# [Issue]: GPU page fault on gfx1151 (Radeon 8060S) — basic tensor operations hang

> **Issue #5991**
> **状态**: closed
> **创建时间**: 2026-02-24T02:46:40Z
> **更新时间**: 2026-03-20T05:16:24Z
> **关闭时间**: 2026-03-20T05:16:24Z
> **作者**: naveenjafer
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5991

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

### Problem Description

Basic PyTorch GPU operations (e.g. `torch.randn` on device, `torch.matmul`) cause the process to **hang indefinitely** on an AMD Radeon 8060S (`gfx1151`) GPU. The kernel log (`dmesg`) reports a **GFX Hub page fault** originating from the Command Processor Frontend (CPF), with walker, mapping, and permission errors.

PyTorch reports `gfx1151` in `torch.cuda.get_arch_list()`, the device is detected, and `torch.cuda.get_device_name()` returns the correct name. The fault occurs only when actual GPU compute is dispatched.

## Environment

| Component | Version |
|---|---|
| **PyTorch** | `2.11.0a0+rocm7.11.0a20260106` (nightly) |
| **GPU** | AMD Radeon 8060S Graphics (Device ID `0x1586`, SKU `STRXLGEN`) |
| **GPU Architecture** | `gfx1151` |
| **CPU** | AMD Ryzen AI MAX+ 395 w/ Radeon 8060S |
| **OS** | Ubuntu 24.04.4 LTS (Noble Numbat) |
| **Kernel** | `6.17.0-1011-oem` |
| **Python** | 3.12.3 |
| **amdgpu-install** | `30.30.0.0.30300000-2278356.24.04` |
| **rocminfo gfx targets** | `amdgcn-amd-amdhsa--gfx1151`, `amdgcn-amd-amdhsa--gfx11-generic` |
| **`torch.cuda.get_arch_list()`** | `['gfx1151']` |
| **`torch.cuda.is_available()`** | `True` |
| **`torch.cuda.get_device_name(0)`** | `Radeon 8060S Graphics` |


## To Reproduce

```python
import torch

device = torch.device("cuda:0")
a = torch.randn(1000, 1000, device=device)  # <-- hangs here
b = torch.randn(1000, 1000, device=device)
c = torch.matmul(a, b)
print(c[0][0].item())
```

Run with:
```bash
python3 main.py
```

The process hangs. No Python exception is raised.

## `dmesg` output (kernel log)

```
[  121.670431] gmc_v11_0_process_interrupt: 159 callbacks suppressed
[  121.670441] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32771)
[  121.670456] amdgpu 0000:c1:00.0: amdgpu:  Process python3 pid 4075 thread python3 pid 4075
[  121.670461] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007ecfa00bc000 from client 10
[  121.670466] amdgpu 0000:c1:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[  121.670468] amdgpu 0000:c1:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPF (0x4)
[  121.670471] amdgpu 0000:c1:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  121.670473] amdgpu 0000:c1:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[  121.670475] amdgpu 0000:c1:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  121.670478] amdgpu 0000:c1:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  121.670478] amdgpu 0000:c1:00.0: amdgpu: 	 RW: 0x0
```

## Analysis

- `torch.cuda.get_arch_list()` **does** include `gfx1151`, so PyTorch appears to have been built with gfx1151 support.
- The device is correctly detected and named.
- However, when any actual GPU kernel is dispatched (even a simple `torch.randn` on device), the GPU's Command Processor Frontend triggers a page fault with walker and mapping errors, suggesting the compiled GPU ISA is invalid or incompatible with the hardware.


## Expected behavior

`torch.randn(1000, 1000, device="cuda:0")` should allocate and populate a tensor on the GPU without hanging or causing a page fault.

## Other notes 
I have tried with both ROCm nightly (Rock) and a stable 7.2 using the documentation here (https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html), I encounter the same error.

### Operating System

 Ubuntu 24.04.4 LTS (Noble Numbat)

### CPU

AMD Ryzen AI MAX+ 395 w/ Radeon 8060S 

### GPU

AMD Radeon 8060S Graphics (Device ID `0x1586`, SKU `STRXLGEN`) 

### ROCm Version

7.2 and the nightly builds from the rock, tested on pytorch -  `2.11.0a0+rocm7.11.0a20260106` (nightly)

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — chejh-amd (2026-02-24T08:36:33Z)

This looks like a gfx1151 (Radeon 8060S) ROCm/driver bug rather than a PyTorch script issue, since even a minimal `torch.randn` call causes a GFX Hub page fault from CPF on a properly detected device; reproducing with a simple HIP sample and a standard supported kernel, would you please provide full dmesg logs, may help the ROCm team root‑cause it.

---

### 评论 #2 — amd-nicknick (2026-02-25T10:37:48Z)

@naveenjafer, are you using the amdgpu dkms by any chance? You should not use that, instead just use the OEM kernel + inbox drivers.

---

### 评论 #3 — naveenjafer (2026-03-03T05:26:24Z)

@amd-nicknick No, I am not using dkms. The instructions in https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#configure-shared-memory are what I followed to the T. 

I came across this thread #5724 and I may be on ox83, could that be an issue? 

`cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES` produces 
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000083

llama.cpp was working as of a couple months back with ROCm 7.1 https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb, I can't seem to remember what may have changed. Possibly the kernel version? 

I am currently on 6.17.0-1011-oem on Ubuntu 24.04 


---

### 评论 #4 — naveenjafer (2026-03-03T05:55:11Z)

@amd-nicknick Using the fix suggested here - https://github.com/ROCm/ROCm/issues/5590#issuecomment-3537889505, I was able to get the simple torch test case to pass. Is this the recommended way? As much as the basic torch test case works, the llama.cpp serves that were working earlier now seg fault 

`[  616.542343] llama-server[15547]: segfault at 34 ip 000076895244e2a4 sp 00007ffd79f420e0 error 4 in libhsa-runtime64.so.1.18.70100[4e2a4,76895241d000+132000] likely on CPU 6 (core 6, socket 0)`


---

### 评论 #5 — amd-nicknick (2026-03-04T10:30:34Z)

Hi @naveenjafer, I'm guessing you have leftover packages that provided the 0x83 FW. That FW is broken.
Check for residual packages:
```
dpkg -S /lib/firmware/amdgpu/gc_11_5_1_mes1.bin.zst
# If the output is amdgpu-dkms-firmware, remove it with apt autoremove --purge
```
For the suggestion in #5590, I assume you've applied the `cwsr_enable=0` boot flag. This flag is necessary until a new kernel is used (6.18-rc6+)

---

### 评论 #6 — amd-nicknick (2026-03-16T07:35:41Z)

Hi @naveenjafer, any updates you could share with me? A quick note on cwsr_enable flag: We have upstreamed a kernel change that defaults to disabling the CWSR feature. However, it would still take a while to trickle down to distros. My suggestions is again to keep the flag until kernel 6.18-rc6+ with new ROCm versions.

---

### 评论 #7 — amd-nicknick (2026-03-20T05:16:24Z)

Closing this issue due to inactivity. Please feel free to reopen if you are still encountering the same issue. Thanks!

---
