# [Issue]: 7900xtx poor performance after upgrade to rocm7.1.1

> **Issue #5725**
> **状态**: closed
> **创建时间**: 2025-11-29T16:26:57Z
> **更新时间**: 2026-04-07T04:45:48Z
> **关闭时间**: 2026-04-07T04:45:48Z
> **作者**: TheRainstorm
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5725

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- amd-nicknick

## 描述

### Problem Description

I'm experiencing a major performance degradation on my RX 7900 XTX when running a PyTorch performance [benchmark](https://github.com/zzc0721/torch-performance-test-data) with ROCm 7.1.1, compared to the performance on ROCm 6.4.

Key Observations:

- **Counter-intuitive Clock Speeds**: With ROCm 7.1.1, the SCLK correctly boosts to 2.8-2.9 GHz during the test. However, with the better-performing ROCm 6.4, the SCLK only reaches 2.1 GHz. Higher clocks are resulting in lower performance.
- **rocblas Library Size Discrepancy**: The rocblas library bundled with the PyTorch environment for ROCm 6.4 is significantly larger than the system-wide rocblas library provided by ROCm 7.1.1.

```shell
➜  ~ ls -lSh /home/xxx/miniconda3/envs/rocm6/lib/python3.13/site-packages/torch/lib/rocblas/library | grep gfx1100 |wc -l
96
➜  ~ ls -lhS /opt/rocm-7.1.1/lib/rocblas/library/ | grep gfx1100 |wc -l
96
➜  ~ du -sh /home/xxx/miniconda3/envs/rocm6/lib/python3.13/site-packages/torch/lib/rocblas/library
3.3G    /home/yfy/miniconda3/envs/rocm6/lib/python3.13/site-packages/torch/lib/rocblas/library
➜  ~ du -sh /opt/rocm-7.1.1/lib/rocblas/library/
651M    /opt/rocm-7.1.1/lib/rocblas/library/
```

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 5950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 7.1.1

### ROCm Component

rocBLAS

### Steps to Reproduce

1. install rocm 7.1.1 and AMD driver according: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html

2. create conda py13 env and install pytorch using wheel package

```shell
pip3 install https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1.1/triton-3.5.1%2Brocm7.1.1.gita272dfa8-cp313-cp313-linux_x86_64.whl
pip3 install https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1.1/torch-2.9.1%2Brocm7.1.1.lw.git351ff442-cp313-cp313-linux_x86_64.whl
pip3 install https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1.1/torchvision-0.24.0%2Brocm7.1.1.gitb919bd0c-cp313-cp313-linux_x86_64.whl
```

OR just using pytorch docker image `rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.9.1`

3. run performance testing

```shell
git clone https://github.com/zzc0721/torch-performance-test-data

python test.py
```

4. get abnormal performance

e.g
```
2.9.1+rocm7.1.1.git351ff442
FP32: 3.35 TFLOPS | TF32: 3.30 TFLOPS | FP16: 79.16 TFLOPS | BF16: 79.98 TFLOPS
```

with rocm6.4
```
2.9.1+rocm6.4
FP32: 26.68 TFLOPS | TF32: 26.05 TFLOPS | FP16: 105.22 TFLOPS | BF16: 102.08 TFLOPS
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.14
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
    L1:                      65536(0x10000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            32
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    49301900(0x2f0498c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49301900(0x2f0498c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49301900(0x2f0498c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    49301900(0x2f0498c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1100
  Uuid:                    GPU-a56d387a32cf2cbb
  Marketing Name:          Radeon RX 7900 XTX
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
  Chip ID:                 29772(0x744c)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2526
  BDFID:                   512
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 602
  SDMA engine uCode::      27
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1100
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*** Done ***


### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — TheRainstorm (2025-11-29T16:31:42Z)

To rule out an installation error, I have reinstalled the amdgpu driver and ROCm stack multiple times. I have tested both official installation procedures outlined in the ROCm documentation, but the outcome remains the same. The methods attempted include:

- Package Manager Installation: Following the official [ROCm Quick start installation guide](https://rocm.docs.amd.com/en/latest/deploy/linux/quick_start.html).
- amdgpu-install Script: Following the guide for [installing Radeon software with ROCm](https://rocm.docs.amd.com/en/latest/deploy/linux/install_radeon.html).

---

### 评论 #2 — ianbmacdonald (2025-12-02T17:10:55Z)

Just to verify this, I fired up an old .venv on ROCm 7.1.1 and here is what your script produced on my Debian 13 instance using slightly older pytorch (2.9.0) .   

```
$ uv pip list
Package                           Version
--------------------------------- ----------------------------
...
torch                             2.9.0+git44352d7
torchaudio                        2.9.0+eaa9e4e
torchvision                       0.24.0+7a9db90
triton                            3.5.0
...

```

```
测试设备: AMD Radeon RX 7900 XTX
显存大小: 24.0 GB

Python版本: 3.12.12 (main, Oct 14 2025, 21:25:31) [Clang 20.1.4 ]
PyTorch版本: 2.9.0+git44352d7
...
📊 性能数据摘要：
设备：AMD Radeon RX 7900 XTX
FP32: 26.12 TFLOPS | TF32: 26.28 TFLOPS | FP16: 101.29 TFLOPS | BF16: 96.57 TFLOPS
```

```
$ amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.0+021c61fc      amdgpu version: Linuxver ROCm version: 7.1.1    |
| VBIOS version: 022.001.002.031.000001                                        |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:03:00.0 AMD Radeon RX 7900 XTX | 2 %      36 °C   0            23/327 W |
|   0       0     N/A             N/A | 4 %      0.0 %             40/24560 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
$ dpkg -l | grep rocm
ii  rocm                                 7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) software stack meta package
ii  rocm-cmake                           0.14.0.70101-38~24.04                amd64        rocm-cmake built using CMake
ii  rocm-core                            7.1.1.70101-38~24.04                 amd64        ROCm Runtime software stack
ii  rocm-dbgapi                          0.77.4.70101-38~24.04                amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent                     2.1.0.70101-38~24.04                 amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-developer-tools                 7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                     1.0.0.70101-38~24.04                 amd64        Radeon Open Compute - device libraries
ii  rocm-gdb                             16.3.70101-38~24.04                  amd64        ROCgdb
ii  rocm-hip                             7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime                     7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev                 7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime                7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm                            20.0.0.25444.70101-38~24.04          amd64        ROCm core compiler
ii  rocm-opencl                          2.0.0.70101-38~24.04                 amd64        clr built using CMake
ii  rocm-opencl-dev                      2.0.0.70101-38~24.04                 amd64        clr built using CMake
ii  rocm-opencl-sdk                      7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp                          7.1.1.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
ii  rocm-smi-lib                         7.8.0.70101-38~24.04                 amd64        AMD System Management libraries
ii  rocminfo                             1.0.0.70101-38~24.04                 amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool
```
Now, just for kicks, I pulled the same wheels as you, and sure enough, with no change in ENVs, I see this:
```
📊 性能数据摘要：
设备：AMD Radeon RX 7900 XTX
FP32: 3.36 TFLOPS | TF32: 3.15 TFLOPS | FP16: 76.92 TFLOPS | BF16: 77.18 TFLOPS
```

It seems pretty clear those wheels are probably the issue.  Likely conservative and compatible 'any-linux'.  I actually don't use that repo at all, as it isn't indexed, so it can't really be used for reproducable builds easily anyways.   

If you want to build your own, the exact .venv I used was from this issue: https://github.com/ROCm/aiter/issues/900#issuecomment-3523554029

Or pull a matched set from indexed wheels from one of the other indexed repos, like pytorch Rocm7.1 nightly, which seems to produce the results you are looking for. 
```
$ bumprocm.py --index rocm71_nightly --python-tag cp313
bumprocm v1.13.1
[info] probing ROCm package index: https://download.pytorch.org/whl/nightly/rocm7.1/ (hardware-agnostic index)
[debug] torch: scanned 130 links, matched 38 wheels
[debug] torchvision: scanned 168 links, matched 48 wheels
[debug] torchaudio: scanned 168 links, matched 48 wheels
Selected build (PRIMARY by newest date):
  date:  20251124
  torch:           2.10.0.dev20251123+rocm7.1
  torchvision:     0.25.0.dev20251124+rocm7.1
  torchaudio:      2.10.0.dev20251124+rocm7.1

--dry-run mode. Use --write to apply changes to pyproject.toml.

Copy/paste install command (PRIMARY):
  uv add --index rocm71_nightly=https://download.pytorch.org/whl/nightly/rocm7.1/ --index-strategy unsafe-best-match --prerelease allow "torch==2.10.0.dev20251123+rocm7.1" "torchvision==0.25.0.dev20251124+rocm7.1" "torchaudio==2.10.0.dev20251124+rocm7.1"

$ uv init --python=3.13
Initialized project `test`

$ uv add --index rocm71_nightly=https://download.pytorch.org/whl/nightly/rocm7.1/ --index-strategy unsafe-best-match --prerelease allow "torch==2.10.0.dev20251123+rocm7.1" "torchvision==0.25.0.dev20251124+rocm7.1" "torchaudio==2.10.0.dev20251124+rocm7.1"
Using CPython 3.13.5 interpreter at: /usr/bin/python3.13
Creating virtual environment at: .venv
Resolved 16 packages in 544ms
Prepared 15 packages in 1m 33s
Installed 15 packages in 1.50s
 + filelock==3.20.0
 + fsspec==2025.10.0
 + jinja2==3.1.6
 + markupsafe==3.0.3
 + mpmath==1.3.0
 + networkx==3.6
 + numpy==2.3.5
 + pillow==12.0.0
 + pytorch-triton-rocm==3.5.1+gitbfeb0668
 + setuptools==80.9.0
 + sympy==1.14.0
 + torch==2.10.0.dev20251123+rocm7.1
 + torchaudio==2.10.0.dev20251124+rocm7.1
 + torchvision==0.25.0.dev20251124+rocm7.1
 + typing-extensions==4.15.0

$ git clone https://github.com/zzc0721/torch-performance-test-data
Cloning into 'torch-performance-test-data'...
remote: Enumerating objects: 309, done.
remote: Counting objects: 100% (125/125), done.
remote: Compressing objects: 100% (101/101), done.
remote: Total 309 (delta 79), reused 29 (delta 24), pack-reused 184 (from 2)
Receiving objects: 100% (309/309), 146.64 KiB | 4.19 MiB/s, done.
Resolving deltas: 100% (160/160), done.

$ source .venv/bin/activate
(test) $ cd torch-performance-test-data/

(test) $ python test.py 
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
测试设备: AMD Radeon Graphics
显存大小: 24.0 GB

Python版本: 3.13.5 (main, Jun 25 2025, 18:55:22) [GCC 14.2.0]
PyTorch版本: 2.10.0.dev20251123+rocm7.1

当前 TF32 设置:
  matmul.allow_tf32 = False
  cudnn.allow_tf32 = True

PyTorch 当前不支持 FP8 E4M3FN，跳过该项测试
  原因: "addmm_cuda" not implemented for 'Float8_e4m3fn'

[FP32] 已设置 TF32 = False

测试 FP32:
  完成 5 个尺寸测试

[TF32] 已设置 TF32 = True

测试 TF32:
  完成 5 个尺寸测试

测试 FP16:
  完成 5 个尺寸测试

测试 BF16:
  完成 5 个尺寸测试

============================================================
性能总结:
FP32         最大算力:   26.10 TFLOPS @ 4096x4096
TF32         最大算力:   26.29 TFLOPS @ 4096x4096
FP16         最大算力:   99.97 TFLOPS @ 4096x4096
BF16         最大算力:   97.26 TFLOPS @ 8192x8192
============================================================

============================================================
🎉 测试完成！

📊 性能数据摘要：
设备：AMD Radeon Graphics
FP32: 26.10 TFLOPS | TF32: 26.29 TFLOPS | FP16: 99.97 TFLOPS | BF16: 97.26 TFLOPS

🔗 提交数据请点击以下链接：
https://github.com/zzc0721/torch-performance-test-data/issues/new?title=%E6%96%B0%E5%A2%9E%E6%80%A7%E8%83%BD%E6%95%B0%E6%8D%AE%EF%BC%9AAMD%20Radeon%20Graphics&body=%23%23%20%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF%0A-%20%E8%AE%BE%E5%A4%87%E5%90%8D%E7%A7%B0%EF%BC%9AAMD%20Radeon%20Graphics%0A-%20Python%E7%89%88%E6%9C%AC%EF%BC%9Apy3135%0A-%20PyTorch%E7%89%88%E6%9C%AC%EF%BC%9Atorch2100dev20251123rocm71%0A%0A%23%23%20%E6%80%A7%E8%83%BD%E6%95%B0%E6%8D%AE%0A%60%60%60%0A%7C%20AMD%20Radeon%20Graphics%20%7C%2026.10%20%7C%2026.29%20%7C%2099.97%20%7C%2097.26%20%7C%20%2A%2A%E8%AF%B7%E5%A1%AB%E5%86%99note%2A%2A%20%7C%20%2A%2A%E8%AF%B7%E5%A1%AB%E5%86%99contributor%2A%2A%20%7C%0A%60%60%60%0A%0A%0A%23%23%20%E8%AF%A6%E7%BB%86%E6%80%A7%E8%83%BD%E6%95%B0%E6%8D%AE%0A%60%60%60%0A%0AFP32%3A%0A%20%201024x1024%3A%208.83%20TFLOPS%0A%20%202048x2048%3A%2023.48%20TFLOPS%0A%20%204096x4096%3A%2026.10%20TFLOPS%0A%20%208192x8192%3A%2025.19%20TFLOPS%0A%20%2010240x10240%3A%2025.17%20TFLOPS%0A%0ATF32%3A%0A%20%201024x1024%3A%2015.16%20TFLOPS%0A%20%202048x2048%3A%2024.22%20TFLOPS%0A%20%204096x4096%3A%2026.29%20TFLOPS%0A%20%208192x8192%3A%2025.17%20TFLOPS%0A%20%2010240x10240%3A%2025.14%20TFLOPS%0A%0AFP16%3A%0A%20%201024x1024%3A%2025.50%20TFLOPS%0A%20%202048x2048%3A%2065.07%20TFLOPS%0A%20%204096x4096%3A%2099.97%20TFLOPS%0A%20%208192x8192%3A%2095.07%20TFLOPS%0A%20%2010240x10240%3A%2092.27%20TFLOPS%0A%0ABF16%3A%0A%20%201024x1024%3A%2025.00%20TFLOPS%0A%20%202048x2048%3A%2058.73%20TFLOPS%0A%20%204096x4096%3A%2093.72%20TFLOPS%0A%20%208192x8192%3A%2097.26%20TFLOPS%0A%20%2010240x10240%3A%2090.90%20TFLOPS%0A%60%60%60%0A%0A%0A%23%23%20%E5%A1%AB%E5%86%99%E8%AF%B4%E6%98%8E%0A1.%20%2A%2Anote%E5%88%97%2A%2A%EF%BC%9A%E8%AF%B7%E5%A1%AB%E5%86%99%E6%B5%8B%E8%AF%95%E7%8E%AF%E5%A2%83%EF%BC%8C%E5%8C%85%E5%90%AB%E4%BB%A5%E4%B8%8B%E5%85%B3%E9%94%AE%E5%AD%97%E4%BC%9A%E8%87%AA%E5%8A%A8%E5%BD%92%E7%B1%BB%EF%BC%9A%0A%20%20%20-%20%60GCP%60%20%28GCP%E4%BA%91%E5%AE%9E%E4%BE%8B%29%0A%20%20%20-%20%60%E5%AE%9E%E4%BD%93%E6%9C%BA%60%20%28%E7%89%A9%E7%90%86%E6%9C%BA%E5%99%A8%29%0A%20%20%20-%20%60%E7%AC%94%E8%AE%B0%E6%9C%AC%60%20%28%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91%29%0A%20%20%20-%20%60docker%60%20%28Docker%E5%AE%B9%E5%99%A8%29%0A%20%20%20-%20%60%E4%BC%98%E4%BA%91%E6%99%BA%E7%AE%97%60%20%28%E4%BC%98%E4%BA%91%E6%99%BA%E7%AE%97%E5%B9%B3%E5%8F%B0%29%0A%20%20%20-%20%60%E6%99%BA%E7%AE%97%E4%BA%91%E6%89%89%60%20%28%E6%99%BA%E7%AE%97%E4%BA%91%E6%89%89%E5%B9%B3%E5%8F%B0%29%0A%0A2.%20%2A%2Acontributor%E5%88%97%2A%2A%EF%BC%9A%E6%A0%BC%E5%BC%8F%E4%B8%BA%20%60%5B%E7%94%A8%E6%88%B7%E5%90%8D%5D%28https%3A//github.com/%E7%94%A8%E6%88%B7%E5%90%8D%29%60%EF%BC%8C%E4%B8%8D%E5%A1%AB%E9%BB%98%E8%AE%A4%E4%BD%A0%E8%87%AA%E5%B7%B1%0A%0A%E6%84%9F%E8%B0%A2%E6%82%A8%E7%9A%84%E8%B4%A1%E7%8C%AE%EF%BC%81

============================================================
💡 提示：
1. 点击链接会自动填充设备信息和性能数据
2. 请在issue中填写note（测试环境）和contributor信息
3. 包含特定关键字的note将被自动归类

```

---

### 评论 #3 — liaowenqi123 (2025-12-14T17:08:15Z)

I encountered a similar problem as yours. The result when running it in WSL2 was(float32):
```
Python path: /home/liao/AMDROCm/.venv/bin/python
PyTorch path: /home/liao/AMDROCm/.venv/lib/python3.10/site-packages/torch/__init__.py
PyTorch version: 2.6.0+rocm6.4.2.git76481f7c
ROCm availability: True
Device name: AMD Radeon RX 7900 XTX
Number of Devices: 1
Average Elapsed Time: 0.0959 s
Performance: 22.40 TFLOPS
```
However, the result when running on Windows is as follows.
```
Python path: C:\Users\admin\AppData\Local\Programs\Python\ Python311\pythonw.exe
PyTorch path: C:\Users\admin\AppData\Local\Programs\Python\Python311\Lib\site-packages\torch_init_.py
PyTorch version: 2.9.1+rocm7.10.0
ROCm availability: True
Device name: AMD Radeon RX 7900 XTX
Number of Devices: 1
Average Elapsed Time: 1.4329 s
Performance: 1.50 TFLOPS
```

But if you change it to float16:
```
WSL:
Python Path: /home/liao/AMDROCm/.venv/bin/python
PyTorch Path: /home/liao/AMDROCm/.venv/lib/python3.10/site-packages/torch/__init__.py
PyTorch Version: 2.6.0+rocm6.4.2.git76481f7c
ROCm Available: True
Device Name: AMD Radeon RX 7900 XTX
Number of Devices: 1
Average Elapsed Time: 0.0249 s
Performance: 86.32 TFLOPS

Windows:
Python Path: C:\Users\admin\AppData\Local\Programs\Python\Python311\pythonw.exe
PyTorch Path: C:\Users\admin\AppData\Local\Programs\Python\Python311\Lib\site-packages\torch\__init__.py
PyTorch Version: 2.9.1+rocm7.10.0
ROCm Available: True
Device Name: AMD Radeon RX 7900 XTX
Number of Devices: 1
Average Elapsed Time: 0.0306 s
Performance: 70.17 TFLOPS
```



---

### 评论 #4 — slojosic-amd (2025-12-16T12:02:35Z)

This issue will be fixed by reverting preferred Torch BLAS backend to rocBLAS instead of hipBLASLt for all RDNA3 and RDNA3.5 targets: https://github.com/ROCm/pytorch/pull/2876

---
