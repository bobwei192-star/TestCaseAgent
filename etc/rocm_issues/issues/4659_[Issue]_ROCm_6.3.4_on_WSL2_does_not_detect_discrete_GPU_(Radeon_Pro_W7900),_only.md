# [Issue]: ROCm 6.3.4 on WSL2 does not detect discrete GPU (Radeon Pro W7900), only shows gfx1100

> **Issue #4659**
> **状态**: closed
> **创建时间**: 2025-04-19T18:11:36Z
> **更新时间**: 2025-06-13T17:19:39Z
> **关闭时间**: 2025-06-13T17:19:39Z
> **作者**: AnaCoda
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4659

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

ROCm 6.3.4 on Ubuntu 22.04 (WSL2) fails to detect my discrete GPU (AMD Radeon Pro W7900). Only one GPU shows up under `rocminfo` with the identifier `gfx1100`.

My setup includes:
- Integrated GPU: AMD Radeon Graphics (Ryzen 5 5600G)
- Discrete GPU: AMD Radeon Pro W7900

I initially assumed `gfx1100` was referring to the integrated GPU, but I later disabled the iGPU in BIOS and `gfx1100` still appeared, so I’m no longer certain what it represents. There's no mention of the W7900 anywhere in the output.

Command and output:
```bash
echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
GPU:
  Name:                    AMD Ryzen 5 5600G with Radeon Graphics
  Marketing Name:          AMD Ryzen 5 5600G with Radeon Graphics
  Name:                    gfx1100
  Marketing Name:          AMD Radeon(TM) Graphics
      Name:                    amdgcn-amd-amdhsa--gfx1100
```

It’s unclear whether `gfx1100` is tied to the iGPU, dGPU, or a generic fallback. The discrete GPU appears correctly in Windows Device Manager and works fine there.

I’m aware `rocm-smi` is unsupported on WSL2 and it shows
`ERROR:root:Driver not initialized (amdgpu not found in modules)` (probably expected).

I followed this official ROCm WSL installation guide: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/howto_wsl.html, and also tried it with Ubuntu 24.04 first which had the same behaviour.

I installed Pytorch for Radeon on WSL as well, which is able to detect `device name [0]: AMD Radeon(TM) Graphics`, and here is the output of pytorch collect_env:
```bash
$  python3 -m torch.utils.collect_env
/usr/lib/python3.10/runpy.py:126: RuntimeWarning: 'torch.utils.collect_env' found in sys.modules after import of package 'torch.utils', but prior to execution of 'torch.utils.collect_env'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
Collecting environment information...
/home/ana/.local/lib/python3.10/site-packages/torch/cuda/__init__.py:645: UserWarning: Can't initialize amdsmi - Error code: 34
  warnings.warn(f"Can't initialize amdsmi - Error code: {e.err_code}")
PyTorch version: 2.4.0+rocm6.3.4.git7cecbf6d
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.3.42134-a9a80e791

OS: Ubuntu 22.04.5 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0] (64-bit runtime)
Python platform: Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon(TM) Graphics (gfx1100)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.3.42134
MIOpen runtime version: 3.3.0
Is XNNPACK available: True

CPU:
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        48 bits physical, 48 bits virtual
Byte Order:                           Little Endian
CPU(s):                               12
On-line CPU(s) list:                  0-11
Vendor ID:                            AuthenticAMD
Model name:                           AMD Ryzen 5 5600G with Radeon Graphics
CPU family:                           25
Model:                                80
Thread(s) per core:                   2
Core(s) per socket:                   6
Socket(s):                            1
Stepping:                             0
BogoMIPS:                             7785.06
Flags:                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw topoext ibrs ibpb stibp vmmcall fsgsbase bmi1 avx2 smep bmi2 erms rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves clzero xsaveerptr arat umip vaes vpclmulqdq rdpid fsrm
Hypervisor vendor:                    Microsoft
Virtualization type:                  full
L1d cache:                            192 KiB (6 instances)
L1i cache:                            192 KiB (6 instances)
L2 cache:                             3 MiB (6 instances)
L3 cache:                             16 MiB (1 instance)
Vulnerability Gather data sampling:   Not affected
Vulnerability Itlb multihit:          Not affected
Vulnerability L1tf:                   Not affected
Vulnerability Mds:                    Not affected
Vulnerability Meltdown:               Not affected
Vulnerability Mmio stale data:        Not affected
Vulnerability Reg file data sampling: Not affected
Vulnerability Retbleed:               Not affected
Vulnerability Spec rstack overflow:   Mitigation; safe RET
Vulnerability Spec store bypass:      Vulnerable
Vulnerability Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:             Mitigation; Retpolines; IBPB conditional; IBRS_FW; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                  Not affected
Vulnerability Tsx async abort:        Not affected

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==3.0.0+rocm6.3.4.git75cc27c2
[pip3] torch==2.4.0+rocm6.3.4.git7cecbf6d
[pip3] torchaudio==2.4.0+rocm6.3.4.git69d40773
[pip3] torchvision==0.19.0+rocm6.3.4.gitfab84886
[conda] Could not collect
```
Pytorch crashes or hangs when I try to load an image model to the cuda device, which the GPU should be able to handle.

Expected behavior:
- ROCm should detect the Radeon Pro W7900 under WSL2 instead of generic gfx1100
- Pytorch should be able to load https://huggingface.co/black-forest-labs/FLUX.1-schnell onto the Radeon Pro W7900


### Operating System

Ubuntu 22.04 (WSL2)

### CPU

AMD Ryzen 5 5600G with Radeon Graphics

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
WSL environment detected. 
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
Name:                    AMD Ryzen 5 5600G with Radeon Graphics
Uuid:                    CPU-XX
Marketing Name:          AMD Ryzen 5 5600G with Radeon Graphics
Vendor Name:             CPU
Feature:                 None specified
Profile:                 FULL_PROFILE
Float Round Mode:        NEAR
Max Queue Number:        0(0x0)
Queue Min Size:          0(0x0)
Queue Max Size:          0(0x0)
Queue Type:              MULTI
Node:                    0
Device Type:             CPU
Cache Info:
  L1:                      32768(0x8000) KB
Chip ID:                 0(0x0)
Cacheline Size:          64(0x40)
Internal Node ID:        0
Compute Unit:            12
SIMDs per CU:            0
Shader Engines:          0
Shader Arrs. per Eng.:   0
Memory Properties:
  Features:              None
  Pool Info:
    Pool 1
      Segment:           GLOBAL; FLAGS: FINE GRAINED
      Size:              16313520(0xf8ecb0) KB
      Allocatable:       TRUE
      Alloc Granule:     4KB
      Alloc Alignment:   4KB
      Accessible by all: TRUE
    Pool 2
      Segment:           GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:              16313520(0xf8ecb0) KB
      Allocatable:       TRUE
      Alloc Granule:     4KB
      Alloc Alignment:   4KB
      Accessible by all: TRUE
    Pool 3
      Segment:           GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:              16313520(0xf8ecb0) KB
      Allocatable:       TRUE
      Alloc Granule:     4KB
      Alloc Alignment:   4KB
      Accessible by all: TRUE
    Pool 4
      Segment:           GLOBAL; FLAGS: COARSE GRAINED
      Size:              16313520(0xf8ecb0) KB
      Allocatable:       TRUE
      Alloc Granule:     4KB
      Alloc Alignment:   4KB
      Accessible by all: TRUE

ISA Info:
*******
Agent 2
*******
Name:                    gfx1100
Marketing Name:          AMD Radeon(TM) Graphics
Vendor Name:             AMD
Feature:                 KERNEL_DISPATCH
Profile:                 BASE_PROFILE
Float Round Mode:        NEAR
Max Queue Number:        128(0x80)
Queue Min Size:          64(0x40)
Queue Max Size:          131072(0x20000)
Queue Type:              MULTI
Node:                    1
Device Type:             GPU
Cache Info:
  L1:                      32(0x20) KB
  L2:                      6144(0x1800) KB
  L3:                      98304(0x18000) KB
Chip ID:                 29768(0x7448)
Cacheline Size:          64(0x40)
Max Clock Freq. (MHz):   1760
Internal Node ID:        1
Compute Unit:            96
SIMDs per CU:            2
Shader Engines:          6
Shader Arrs. per Eng.:   2
Coherent Host Access:    FALSE
Memory Properties:
  Features:              KERNEL_DISPATCH
  Fast F16 Operation:    TRUE
  Wavefront Size:        32(0x20)
  Workgroup Max Size:    1024(0x400)
  Workgroup Max Size per Dimension:
    x                    1024(0x400)
    y                    1024(0x400)
    z                    1024(0x400)
  Max Waves Per CU:      32(0x20)
  Max Work-item Per CU:  1024(0x400)
  Grid Max Size:         4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                    4294967295(0xffffffff)
    y                    4294967295(0xffffffff)
    z                    4294967295(0xffffffff)
  Max fbarriers/Workgrp: 32
  Packet Processor uCode:: 372
  SDMA engine uCode::    24
  IOMMU Support::        None
Pool Info:
  Pool 1
    Segment:             GLOBAL; FLAGS: COARSE GRAINED
    Size:                47093220(0x2ce95e4) KB
    Allocatable:         TRUE
    Alloc Granule:       4KB
    Alloc Recommended Granule: 2048KB
    Alloc Alignment:     4KB
    Accessible by all:   FALSE
  Pool 2
    Segment:             GLOBAL; FLAGS: EXTENDED FINE GRAINED
    Size:                47093220(0x2ce95e4) KB
    Allocatable:         TRUE
    Alloc Granule:       4KB
    Alloc Recommended Granule: 2048KB
    Alloc Alignment:     4KB
    Accessible by all:   FALSE
  Pool 3
    Segment:             GROUP
    Size:                64(0x40) KB
    Allocatable:         FALSE
    Alloc Granule:       0KB
    Alloc Alignment:     0KB
    Accessible by all:   FALSE

ISA Info:
  ISA 1
    Name:                amdgcn-amd-amdhsa--gfx1100
    Machine Models:      HSA_MACHINE_MODEL_LARGE
    Profiles:            HSA_PROFILE_BASE
    Default Rounding Mode: NEAR
    Fast f16:            TRUE
    Workgroup Max Size:  1024(0x400)
    Workgroup Max Size per Dimension:
      x                  1024(0x400)
      y                  1024(0x400)
      z                  1024(0x400)
    Grid Max Size:       4294967295(0xffffffff)
    Grid Max Size per Dimension:
      x                  4294967295(0xffffffff)
      y                  4294967295(0xffffffff)
      z                  4294967295(0xffffffff)
    FBarrier Max Size:   32

*** Done ***
```

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — komorebi-c9 (2025-04-21T09:28:57Z)

Have you solved this problem? I've had the same problem

---

### 评论 #2 — harkgill-amd (2025-04-21T18:49:07Z)

Hi @AnaCoda, gfx1100/AMD Radeon(TM) Graphics refers to the dGPU (W7900) in your system. In your case, it is being detected correctly though, it should have Marketing Name `AMD Radeon PRO W7900`. Will confirm this behaviour on my end. In the meantime, could you please provide the exact reproducer for your PyTorch crash?

EDIT: Wasn't able to reproduce the incorrect Marketing Name. Could you please also confirm if you're using the latest [AMD Software: Adrenalin Edition™ 25.3.1 for WSL2](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-25-3-1.html) driver?

---

### 评论 #3 — AnaCoda (2025-04-21T22:06:18Z)

I actually was able to fix my use case by redoing some of the Pytorch installation steps, not sure what went wrong there. However, the incorrect marketing name still shows.

I do have the driver you mentioned installed:
![Image](https://github.com/user-attachments/assets/1bce95a8-d87a-47d8-a3c3-56402fec0eb5)
AMD Software: Adrenalin Edition 25.3.1 Driver Version 24.30.31.03 for Windows® 10 and Windows® 11 (Windows Driver Store Version 32.0.13031.3015).

---

### 评论 #4 — harkgill-amd (2025-04-22T17:42:25Z)

Glad to hear PyTorch is working on your end. Could you also please provide the Device ID, Revision ID and BIOS Part Number for your GPU. You can find these in the Adrenalin Software -> Settings -> Hardware & Drivers -> Hardware Details tab.

---

### 评论 #5 — AnaCoda (2025-04-22T19:45:31Z)

Device ID
7448
Revision ID
00
BIOS Part Number
113-D7070100-138

---

### 评论 #6 — harkgill-amd (2025-04-24T19:08:52Z)

There will be a fix in an upcoming Adrenalin driver release that will address the Marketing Name discrepancy for all W7900 revisions. This discrepancy doesn't cause any functional issues on WSL so you can continue as is. I'll circle back to this issue once the fix has been released and you can give it a try on your end then.

---

### 评论 #7 — harkgill-amd (2025-05-26T14:22:23Z)

Hi @AnaCoda, could you update to the [25.3.1 adrenalin release](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-25-3-1.html) and confirm if the issue persists?

---

### 评论 #8 — harkgill-amd (2025-06-13T17:19:39Z)

@AnaCoda 25.6.1 is also now out https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-25-6-1.html. When you get a chance, please check if the issue has been resolved with the latest adrenalin release. Will close this issue out for now.

---
