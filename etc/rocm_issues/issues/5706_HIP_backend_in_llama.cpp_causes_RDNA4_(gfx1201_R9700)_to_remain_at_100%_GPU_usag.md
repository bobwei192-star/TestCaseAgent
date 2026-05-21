# HIP backend in llama.cpp causes RDNA4 (gfx1201 / R9700) to remain at 100% GPU usage after idle

> **Issue #5706**
> **状态**: closed
> **创建时间**: 2025-11-27T06:29:45Z
> **更新时间**: 2026-05-12T05:49:13Z
> **关闭时间**: 2026-03-18T16:22:35Z
> **作者**: tamascode
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5706

## 负责人

- tcgu-amd

## 描述

### Problem Description

Using llama.cpp with the HIP backend on an RDNA4 system (three Radeon AI PRO R9700 / gfx1201 GPUs) causes all GPUs to enter a permanent non-idle state immediately when the HIP runtime initializes.

The GPUs remain at elevated clocks / power and never return to idle until the llama-server process fully exits, even when no inference is running.

The Vulkan backend does not exhibit this issue and idles correctly.

This appears to be a HIP queue initialization / teardown bug or HSA runtime issue specific to RDNA4 (gfx1201) under ROCm 7.1.1.

System Information
CPU:
  Name:                    AMD Ryzen Threadripper 2950X 16-Core Processor
  Marketing Name:          AMD Ryzen Threadripper 2950X 16-Core Processor

GPUs:
  GPU 0:
    Name:                  gfx1201
    Marketing Name:        AMD Radeon AI PRO R9700
      Supported Targets:
        amdgcn-amd-amdhsa--gfx1201
        amdgcn-amd-amdhsa--gfx12-generic

  GPU 1:
    Name:                  gfx1201
    Marketing Name:        AMD Radeon AI PRO R9700
      Supported Targets:
        amdgcn-amd-amdhsa--gfx1201
        amdgcn-amd-amdhsa--gfx12-generic

  GPU 2:
    Name:                  gfx1201
    Marketing Name:        AMD Radeon AI PRO R9700
      Supported Targets:
        amdgcn-amd-amdhsa--gfx1201
        amdgcn-amd-amdhsa--gfx12-generic

ROCm / HIP Version Information
HIP Version:
  hipconfig --version:
    7.1.52802-26aae437f6

HIP Compiler:
  hipcc --version:
    HIP version: 7.1.52802-26aae437f6
    AMD clang version 20.0.0git (roc-7.1.1)
    InstalledDir: /opt/rocm-7.1.1/lib/llvm/bin

ROCm Runtime:
  Runtime Version:      1.18
  Runtime Ext Version:  1.14

ROCm Installation Path:
  /opt/rocm-7.1.1

AMDGPU Kernel Driver:
  Driver version:       6.12.12

GPU Architecture Detection
gfx1201
  amdgcn-amd-amdhsa--gfx1201
  amdgcn-amd-amdhsa--gfx12-generic
gfx1201
  amdgcn-amd-amdhsa--gfx1201
  amdgcn-amd-amdhsa--gfx12-generic
gfx1201
  amdgcn-amd-amdhsa--gfx1201
  amdgcn-amd-amdhsa--gfx12-generic

llama.cpp Version
Repository: https://github.com/ggerganov/llama.cpp
Commit: e509411cf142807c947b53b340d2d5594ce38120
Backend: HIP

HIP Build Configuration (CMake)
-DGGML_HIP=ON
-DGGML_HIPBLAS=ON
-DGGML_HIP_UMA=ON
-DGGML_VULKAN=OFF
-DGGML_CUDA=OFF
-DGGML_METAL=OFF
-DAMDGPU_TARGETS=gfx1201
-DCMAKE_BUILD_TYPE=Release

Reproduction Steps

Build llama.cpp with the HIP backend:

cmake -S . -B build \
  -DGGML_HIP=ON \
  -DGGML_HIPBLAS=ON \
  -DGGML_HIP_UMA=ON \
  -DAMDGPU_TARGETS=gfx1201 \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build --config Release -- -j16


Start the server without running inference:

export HIP_VISIBLE_DEVICES=0,1,2

./bin/llama-server \
  -m <model>.gguf \
  --tensor-split 0.30,0.35,0.35 \
  -b 256 \
  -ub 128 \
  -t 16


Immediately after startup (before any prompt is processed), check the GPU state:

rocm-smi --showuse --showclocks --showpower



### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen Threadripper 2950X 16-Core Processor

### GPU

3X R9700

### ROCm Version

ROCM 7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

Reproduction Steps

Build llama.cpp with the HIP backend:

cmake -S . -B build \
  -DGGML_HIP=ON \
  -DGGML_HIPBLAS=ON \
  -DGGML_HIP_UMA=ON \
  -DAMDGPU_TARGETS=gfx1201 \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build --config Release -- -j16


Start the server without running inference:

export HIP_VISIBLE_DEVICES=0,1,2

./bin/llama-server \
  -m <model>.gguf \
  --tensor-split 0.30,0.35,0.35 \
  -b 256 \
  -ub 128 \
  -t 16


Immediately after startup (before any prompt is processed), check the GPU state:

rocm-smi --showuse --showclocks --showpower

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support


ROCk module version 6.12.12 is loaded
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
  Name:                    AMD Ryzen Threadripper 2950X 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen Threadripper 2950X 16-Core Processor
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
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3500
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
      Size:                    131736912(0x7da2550) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131736912(0x7da2550) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131736912(0x7da2550) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    131736912(0x7da2550) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1201
  Uuid:                    GPU-122f60a0a7d06c96
  Marketing Name:          AMD Radeon AI PRO R9700
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
    L2:                      8192(0x2000) KB
    L3:                      65536(0x10000) KB
  Chip ID:                 30033(0x7551)
  ASIC Revision:           1(0x1)
  Cacheline Size:          256(0x100)
  Max Clock Freq. (MHz):   2350
  BDFID:                   2560
  Internal Node ID:        1
  Compute Unit:            64
  SIMDs per CU:            2
  Shader Engines:          4
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
  Packet Processor uCode:: 1012
  SDMA engine uCode::      838
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33406976(0x1fdc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1201
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic
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
*******
Agent 3
*******
  Name:                    gfx1201
  Uuid:                    GPU-3919877325193652
  Marketing Name:          AMD Radeon AI PRO R9700
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    2
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      8192(0x2000) KB
    L3:                      65536(0x10000) KB
  Chip ID:                 30033(0x7551)
  ASIC Revision:           1(0x1)
  Cacheline Size:          256(0x100)
  Max Clock Freq. (MHz):   2350
  BDFID:                   3328
  Internal Node ID:        2
  Compute Unit:            64
  SIMDs per CU:            2
  Shader Engines:          4
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
  Packet Processor uCode:: 1012
  SDMA engine uCode::      838
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33406976(0x1fdc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1201
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic
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
*******
Agent 4
*******
  Name:                    gfx1201
  Uuid:                    GPU-b206404c71c2dfec
  Marketing Name:          AMD Radeon AI PRO R9700
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    3
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      8192(0x2000) KB
    L3:                      65536(0x10000) KB
  Chip ID:                 30033(0x7551)
  ASIC Revision:           1(0x1)
  Cacheline Size:          256(0x100)
  Max Clock Freq. (MHz):   2350
  BDFID:                   17664
  Internal Node ID:        3
  Compute Unit:            64
  SIMDs per CU:            2
  Shader Engines:          4
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
  Packet Processor uCode:: 1012
  SDMA engine uCode::      838
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33406976(0x1fdc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1201
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic
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

## 评论 (34 条)

### 评论 #1 — tcgu-amd (2025-11-28T16:36:02Z)

Hi @tamascode Thanks for reporting the bug. Was able to successfully reproduce this. Will look into this immediately. Thanks! 

---

### 评论 #2 — tamascode (2025-11-28T19:38:30Z)

@tcgu-amd thanks for getting on this so quickly. 

---

### 评论 #3 — tamascode (2026-01-01T20:55:00Z)

Is there an ETA on this bug?


---

### 评论 #4 — tcgu-amd (2026-01-02T16:24:55Z)

Hi @tamascode, sorry not yet -- holiday season has been going slow with people taking vacations. Will update you soon once we have a fix available. Thanks! 

---

### 评论 #5 — tamascode (2026-01-22T00:15:36Z)

Did this get fixed in 7.2?


---

### 评论 #6 — tcgu-amd (2026-01-22T00:23:56Z)

@tamascode No unfortunately. Currently the issue seems to be part of MES and the fix will be available through the linux kernel/dkms if that is indeed the case. (It has actually been quite tricky to track down the root cause so far, sorry about the delay)

---

### 评论 #7 — tamascode (2026-01-22T20:29:20Z)

@tcgu-amd thanks for the update.  Currently I am using the Vulkan backend. 
BTW,  I did try 7.2 but that showed some major slowdown on top of the GPU usage issue described in this ticket. 

---

### 评论 #8 — tcgu-amd (2026-01-22T20:33:37Z)

@tamascode Sorry to hear that. We will be investigating the performance with gfx12 as well. Will keep you updated. Thanks! 

---

### 评论 #9 — meven3000 (2026-01-23T01:47:07Z)

Here is some info, the issue is not specific to llama.cpp. based on my diag so far this is realted to kernel dkms.

This occurs with all ROCM 7x versions (not sure about 6x) onm Ubuntu server 24.04.

Changes MES only brings it down from 100% to 91%.

using VLLM sleep  commands has no effect, only disabling the process/container works.

Kinda needs a hot fix or something, it's certainly not a good bug. I forgot to shutdown the container one night, battery drained 50Kw in the morning... also can't say its good for the cards either given the heat.




echo "==================== GPU HARDWARE ===================="
lspci | grep -E "VGA|Display|3D"
echo

echo "==================== DRM DEVICE MAPPING ===================="
for d in /sys/class/drm/card*/device; do
  echo "== $d =="
  cat $d/uevent | egrep 'DRIVER=|PCI_SLOT_NAME=' || true
done
echo

echo "==================== AMDGPU DRIVER ===================="
dkms status | grep -i amdgpu || echo "No amdgpu DKMS entry"
echo
modinfo amdgpu | egrep 'version:|filename:|srcversion:' || true
echo

echo "==================== ROCm / SMI ===================="
rocm-smi --version || true
echo
amd-smi --version || true
echo

echo "==================== GPU METRICS (IDLE STATE) ===================="
sudo amd-smi metric --gpu 0 --json | head -n 40
echo
sudo amd-smi metric --gpu 1 --json | head -n 40
echo

echo "==================== GPU POWER / UTIL ===================="
sudo amd-smi
echo

echo "==================== GPU PROCESS LIST ===================="
sudo amd-smi process --json
echo

echo "==================== RUNTIME POWER MANAGEMENT ===================="
for d in /sys/class/drm/card*/device; do
  echo "== $d =="
  cat $d/power/control 2>/dev/null || true
  cat $d/power/runtime_status 2>/dev/null || true
  cat $d/power/runtime_suspended_time 2>/dev/null || true
done
echo

echo "==================== KERNEL CMDLINE ===================="
cat /proc/cmdline
echo
==================== SYSTEM ====================
Fri Jan 23 01:42:36 AM UTC 2026

Linux localai2 6.8.0-90-generic #91-Ubuntu SMP PREEMPT_DYNAMIC Tue Nov 18 14:14:30 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux

No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.3 LTS
Release:        24.04
Codename:       noble

==================== GPU HARDWARE ====================
03:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Device 7551 (rev c0)
43:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Device 7551 (rev c0)
c6:00.0 VGA compatible controller: ASPEED Technology, Inc. ASPEED Graphics Family (rev 52)

==================== DRM DEVICE MAPPING ====================
== /sys/class/drm/card0/device ==
DRIVER=ast
PCI_SLOT_NAME=0000:c6:00.0
== /sys/class/drm/card0-VGA-1/device ==
== /sys/class/drm/card0-Virtual-1/device ==
== /sys/class/drm/card1/device ==
DRIVER=amdgpu
PCI_SLOT_NAME=0000:03:00.0
== /sys/class/drm/card1-DP-1/device ==
== /sys/class/drm/card1-DP-2/device ==
== /sys/class/drm/card1-DP-3/device ==
== /sys/class/drm/card1-DP-4/device ==
== /sys/class/drm/card1-Writeback-1/device ==
== /sys/class/drm/card2/device ==
DRIVER=amdgpu
PCI_SLOT_NAME=0000:43:00.0
== /sys/class/drm/card2-DP-5/device ==
== /sys/class/drm/card2-DP-6/device ==
== /sys/class/drm/card2-DP-7/device ==
== /sys/class/drm/card2-DP-8/device ==
== /sys/class/drm/card2-Writeback-2/device ==

==================== AMDGPU DRIVER ====================
amdgpu/6.16.6-2255209.24.04, 6.8.0-88-generic, x86_64: installed (Original modules exist)
amdgpu/6.16.6-2255209.24.04, 6.8.0-90-generic, x86_64: installed (Original modules exist)

filename:       /lib/modules/6.8.0-90-generic/updates/dkms/amdgpu.ko.zst
version:        6.16.6
srcversion:     00374535C9131B51512F32A

==================== ROCm / SMI ====================
ROCM-SMI version: 4.0.0+fc0010cf6a
ROCM-SMI-LIB version: 7.8.0

amdsmi_cli_exceptions.AmdSmiInvalidSubcommandException: AMD-SMI Command '--version' is invalid. Must receive valid AMD-SMI Command first. Run 'amd-smi -h' for more info. Error code: -10

==================== GPU METRICS (IDLE STATE) ====================
{
    "gpu_data": [
        {
            "gpu": 0,
            "usage": {
                "gfx_activity": {
                    "value": 100,
                    "unit": "%"
                },
                "umc_activity": {
                    "value": 0,
                    "unit": "%"
                },
                "mm_activity": {
                    "value": 0,
                    "unit": "%"
                },
                "vcn_activity": [
                    {
                        "value": 0,
                        "unit": "%"
                    },
                    "N/A",
                    "N/A",
                    "N/A"
                ],
                "jpeg_activity": [
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",

{
    "gpu_data": [
        {
            "gpu": 1,
            "usage": {
                "gfx_activity": {
                    "value": 100,
                    "unit": "%"
                },
                "umc_activity": {
                    "value": 0,
                    "unit": "%"
                },
                "mm_activity": {
                    "value": 0,
                    "unit": "%"
                },
                "vcn_activity": [
                    {
                        "value": 0,
                        "unit": "%"
                    },
                    "N/A",
                    "N/A",
                    "N/A"
                ],
                "jpeg_activity": [
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",

==================== GPU POWER / UTIL ====================
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.1+fc0010cf6a    amdgpu version: 6.16.6   ROCm version: 7.2.0    |
| VBIOS version: 00158742                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:03:00.0 ...Radeon AI PRO R9700 | 1 %      79 °C   0           103/300 W |
|   0       0     N/A             N/A | 100 %   38.82           29777/32624 MB |
|-------------------------------------+----------------------------------------|
| 0000:43:00.0 ...Radeon AI PRO R9700 | 0 %      80 °C   0            92/300 W |
|   1       1     N/A             N/A | 100 %   40.0 %          29777/32624 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|    0     213534  python3.12             5.9 MB   54.7 KB      0.0 B  N/A     |
|    0     213890  python3.12             5.9 MB   54.7 KB      0.0 B  N/A     |
|    0     213952  python3.12             7.9 MB   19.6 GB    20.1 GB  N/A     |
|    0     213953  python3.12             7.9 MB   19.1 GB      0.0 B  N/A     |
|    1     213534  python3.12             5.9 MB   54.7 KB      0.0 B  N/A     |
|    1     213890  python3.12             5.9 MB   54.7 KB      0.0 B  N/A     |
|    1     213952  python3.12             7.9 MB   19.6 GB    20.1 GB  N/A     |
|    1     213953  python3.12             7.9 MB   19.1 GB      0.0 B  N/A     |
+------------------------------------------------------------------------------+

==================== GPU PROCESS LIST ====================
[
    {
        "gpu": 0,
        "process_list": [
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213534,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 6180000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 56000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 0,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            },
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213890,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 6180000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 56000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 0,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            },
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213952,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 8268000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 21008920000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 21589852160,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            },
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213953,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 8244000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 20503796000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 0,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            }
        ]
    },
    {
        "gpu": 1,
        "process_list": [
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213534,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 6180000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 56000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 0,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            },
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213890,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 6180000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 56000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 0,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            },
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213952,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 8268000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 21008920000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 21589852160,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            },
            {
                "process_info": {
                    "name": "/usr/bin/python3.12",
                    "pid": 213953,
                    "memory_usage": {
                        "gtt_mem": {
                            "value": 8244000,
                            "unit": "B"
                        },
                        "cpu_mem": {
                            "value": 0,
                            "unit": "B"
                        },
                        "vram_mem": {
                            "value": 20503796000,
                            "unit": "B"
                        }
                    },
                    "mem_usage": {
                        "value": 0,
                        "unit": "B"
                    },
                    "usage": {
                        "gfx": {
                            "value": 0,
                            "unit": "ns"
                        },
                        "enc": {
                            "value": 0,
                            "unit": "ns"
                        }
                    },
                    "cu_occupancy": "N/A",
                    "evicted_time": {
                        "value": 0,
                        "unit": "ms"
                    }
                }
            }
        ]
    }
]

==================== RUNTIME POWER MANAGEMENT ====================
== /sys/class/drm/card0/device ==
on
active
0
== /sys/class/drm/card0-VGA-1/device ==
auto
unsupported
0
== /sys/class/drm/card0-Virtual-1/device ==
auto
unsupported
0
== /sys/class/drm/card1/device ==
auto
active
0
== /sys/class/drm/card1-DP-1/device ==
auto
unsupported
0
== /sys/class/drm/card1-DP-2/device ==
auto
unsupported
0
== /sys/class/drm/card1-DP-3/device ==
auto
unsupported
0
== /sys/class/drm/card1-DP-4/device ==
auto
unsupported
0
== /sys/class/drm/card1-Writeback-1/device ==
auto
unsupported
0
== /sys/class/drm/card2/device ==
auto
active
0
== /sys/class/drm/card2-DP-5/device ==
auto
unsupported
0
== /sys/class/drm/card2-DP-6/device ==
auto
unsupported
0
== /sys/class/drm/card2-DP-7/device ==
auto
unsupported
0
== /sys/class/drm/card2-DP-8/device ==
auto
unsupported
0
== /sys/class/drm/card2-Writeback-2/device ==
auto
unsupported
0

==================== KERNEL CMDLINE ====================
BOOT_IMAGE=/vmlinuz-6.8.0-90-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro modprobe.blacklist=nouveau amd_iommu=on iommu=pt amdgpu.mes=0

---

### 评论 #10 — tamascode (2026-01-28T03:19:22Z)

@meven3000. This problem does not show up on LLama.cpp with Vulkan  but it is about 50% of the speed compared to llama.cpp with ROCM. 

---

### 评论 #11 — Expro (2026-01-28T17:07:58Z)

Cannot agree here (I have 4x R9700 setup). It show's up on llama.cpp + ROCm, but does not shows up in llama.cpp + Vulkan, and Vulkan shows about same performance level (faster tk, but slower pp).

---

### 评论 #12 — tamascode (2026-01-28T19:36:05Z)

@Expro I think I may not have explained this clearly before, so let me restate it.

My system has 3× Radeon AI Pro R9700 (RDNA4 / gfx1201) GPUs.
When running llama.cpp with the Vulkan backend, I do not see this issue. GPU usage drops normally when the server is idle.

However, when running llama.cpp with the HIP/ROCm backend, the GPUs remain stuck at ~100% utilization even when idle. 

Using --split-mode layers on the llama.cpp server does improve performance:
- Prompt processing increased from ~450 to ~900
- Performance degradation over long contexts is much slower

Current setup:
Model: Qwen3-Next (Q4, v-cache)
Context: 250K tokens
GPUs: 3× R9700 (gfx1201)
Vulkan backend: works correctly
HIP/ROCm backend: stuck at 100% usage when idle

@tcgu-amd , @meven3000 I also tested downgrading the kernel to 6.6 (from 6.8), but the issue persists, so this does not appear to be kernel-related.

---

### 评论 #13 — Expro (2026-01-29T09:41:12Z)

Clear. Additional observation: vLLM exibits same issue (100% GPU on non workload as long as ROCm is initialized) so it's not llama.cpp issue, it's ROCm issue.

---

### 评论 #14 — tamascode (2026-02-05T17:43:49Z)

@tcgu-amd , checking if any progress has been made on this bug or any workarounds exist. 



---

### 评论 #15 — tcgu-amd (2026-02-17T15:12:16Z)

Hi @tamascode, yes we have been making progress internal, and this is issue is still being actively investigated.

---

### 评论 #16 — tcgu-amd (2026-03-04T15:17:33Z)

Hi @tamascode, just an update, we have found the cause to be part of the MES firmware and patched it. It will still take a bit before it makes to release. Once it does, updating the MES firmware will be able to fix it. 

~~Fortunately, this bug has negligible performance/power impact. Even when the GPU appears to be stuck at 100%, usage, the power consumption should remain at the level of idling. There shouldn't be significant impact to the actual workload.~~

I will be monitoring the status of the MES patch release and update once more after it gets released. 

Thanks!!

---

### 评论 #17 — Expro (2026-03-04T15:29:51Z)

@tcgu-amd on contrary, this bug causes serious power usage issues - idle GPU with usage stuck at 100% reports 100W / GPU without any workload. I have 4x R9700 setup that shows that quite visibly.

---

### 评论 #18 — tcgu-amd (2026-03-04T15:53:06Z)

> [@tcgu-amd](https://github.com/tcgu-amd) on contrary, this bug causes serious power usage issues - idle GPU with usage stuck at 100% reports 100W / GPU without any workload. I have 4x R9700 setup that shows that quite visibly.

Interesting, perhaps it has to do with a different test workload being used internally. Thanks for the report! 

---

### 评论 #19 — Expro (2026-03-04T15:57:13Z)

If you want to see that yourself - launch vLLM on R9700. vLLM initializes ROCm, then mulls over content of model file with CPU / RAM for 30 sec before it does anything meaningful on GPU. And yet, as soon as ROCm is initialized but not used (model not yet loaded, caches not allocated etc) it still sits on 100% and report 100W/GPU power usage.

---

### 评论 #20 — tamascode (2026-03-06T05:25:49Z)

Hello @tcgu-amd ,  thanks for the update.  I am glad the issue has been resolved.  I will test it as soon as it has been merged.  Thanks again for fixing this. 

---

### 评论 #21 — tcgu-amd (2026-03-18T16:22:35Z)

Hi @tamascode, I will be closing this issue since it is now tested and merged. Please feel free to follow up if you require further assistance. Thanks! 

---

### 评论 #22 — mamama1 (2026-04-02T00:51:40Z)

> Hi [@tamascode](https://github.com/tamascode), I will be closing this issue since it is now tested and merged. Please feel free to follow up if you require further assistance. Thanks!

Hi,

shouldn't this be fixed in 6.18.20? I'm undervolting and underclocking - hence I only see 30W but usually the card is idling at 11W (before inference). Using Qwen3.5-35B-A3B-Q4_K_M.

```
========================================== ROCm System Management Interface ==========================================
==================================================== Concise Info ====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK     MCLK   Fan    Perf    PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                      
======================================================================================================================
0       1     0x7551,   8001   45.0°C  31.0W  N/A, N/A, 0         2324Mhz  96Mhz  29.8%  manual  210.0W  76%    100%  
======================================================================================================================
================================================ End of ROCm SMI Log =================================================
root@ai02:/home/user# uname -r
6.18.20-061820-generic

```

Thanks

---

### 评论 #23 — meven3000 (2026-04-02T01:03:00Z)

Thanks tcgu-amd, can confirm this is working on draft compile with kernel 6.8 and also on the newer 6.17 kernel.

---

### 评论 #24 — mamama1 (2026-04-02T01:09:35Z)

It is weird, i even manually updated amd firmware... but still the 100% GPU usage is there, + 30W idle consumption instead of 11W.

 ```
uname -r
6.18.20-061820-generic

cat /sys/kernel/debug/dri/0/amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b9a
PFP feature version: 29, firmware version: 0x00000bea
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000c44
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3804948, firmware version: 0x003a0f14
ASD feature version: 553648371, firmware version: 0x210000f3
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x17000046
TA DTM feature version: 0x00000000, firmware version: 0x12000019
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684c00 (104.76.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x09109018
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x0a000400
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x00000081
MES feature version: 1, firmware version: 0x00000081
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 115-G287BP00-100

[    9.892554] amdgpu 0000:01:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000033, smu fw program = 0, smu fw version = 0x00684c00 (104.76.0)
[    9.892558] amdgpu 0000:01:00.0: amdgpu: SMU driver if version not matched
[    9.919618] amdgpu 0000:01:00.0: amdgpu: SMU is initialized successfully! 
```

---

### 评论 #25 — meven3000 (2026-04-02T03:41:38Z)

Not sure if kernel 6.18 works, 6.8 and 6.17 worked for me.

6.17 was only just supported of 7.2.1.

Had tried ubuntu 25.05 at one point and getting this work correctly was a pain, even trying to change to an official supported kernel build was causes issues. I would suggest using general LTS Linux os.

---

### 评论 #26 — mamama1 (2026-04-02T16:53:16Z)

> Not sure if kernel 6.18 works, 6.8 and 6.17 worked for me.
> 
> 6.17 was only just supported of 7.2.1.
> 
> Had tried ubuntu 25.05 at one point and getting this work correctly was a pain, even trying to change to an official supported kernel build was causes issues. I would suggest using general LTS Linux os.

heh. on 6.8 i wasn't even able to init the gpu (within a VM with gpu passthrough):
 ```
[    7.285612] [drm] amdgpu kernel modesetting enabled.
[    7.285755] amdgpu: Virtual CRAT table created for CPU
[    7.285771] amdgpu: Topology: Add CPU node
[    7.286287] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x7551 0x1043:0x0626 0xC0).
[    7.286302] [drm] register mmio base: 0x82000000
[    7.286303] [drm] register mmio size: 524288
[    7.291718] amdgpu 0000:01:00.0: amdgpu: Fatal error during GPU init
[    7.291722] amdgpu 0000:01:00.0: amdgpu: amdgpu: finishing device.
[    7.292763] amdgpu: probe of 0000:01:00.0 failed with error -22 
```

in 6.17 i have the same issue (24.04 LTS HWE Kernel):
```
========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU  Temp (DieEdge)  AvgPwr  SCLK     MCLK   Fan    Perf    PwrCap  VRAM%  GPU%
0    47.0c           30.0W   2317Mhz  96Mhz  29.8%  manual  210.0W   71%   100%
====================================================================================
=============================== End of ROCm SMI Log ================================
root@ai01:/home/user# uname -r
6.17.0-20-generic

in the container:
rocm-core/now 7.2.0.70200-43~24.04 amd64 [installed,local]
```

do i need rocm 7.2.1 in the container?

edit: with rocm 7.2.1 and kernel 6.17.0-20 (6.17.13), GPU utilization is at 100% and power usage at 30W as soon as the container is up, without having run any inference at all.
i'm out of ideas.

---

### 评论 #27 — tamascode (2026-04-02T22:45:36Z)

@mamama1 I tried 7.2.1 but the GPU usage is still 100% on the following OS version. 

Linux aiplane1 6.17.0-20-generic #20~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Mar 19 01:28:37 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

I also updated the firmware but the version that go installed does not have the change. 


---

### 评论 #28 — mamama1 (2026-04-02T22:49:33Z)

> [@mamama1](https://github.com/mamama1) I tried 7.2.1 but the GPU usage is still 100% on the following OS version.
> 
> Linux aiplane1 6.17.0-20-generic [#20](https://github.com/ROCm/ROCm/pull/20)~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Mar 19 01:28:37 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
> 
> I also updated the firmware but the version that go installed does not have the change.

i just discovered that while rocm gave me 40-70 token/s with Qwen3.5-35B-A3B-Q4_K_M.gguf on llama.cpp, depending on whether I was downclocking or not, the llama.cpp vulkan version gives me 74 token/s with that model when underclocked and downvolted at 120W(!!!) and 98 token/s when unthrottled at full 300W TDP.

on top of that, the bug is gone where the CPU doesn't idle down properly in idle. as soon as the model stops spinning, gpu load is at 0% and power usage at 10W.

so far, I can't see any downsides of using vulkan over rocm. :-O

---

### 评论 #29 — tamascode (2026-04-03T16:31:37Z)

@mamama1 Yeah, llama.cpp has put a lot of work into improving Vulkan support, and it works very well with up to 2 GPUs. Multi-GPU support should be much faster under ROCm, but at the moment ROCm seems broken for multi-GPU use in llama.cpp, or there is some issue with ROCm itself, because it crashes whenever I try to run llama.cpp with more than 1 GPU.

---

### 评论 #30 — zedbytes (2026-04-12T18:58:01Z)

> > [@mamama1](https://github.com/mamama1) I tried 7.2.1 but the GPU usage is still 100% on the following OS version.
> > Linux aiplane1 6.17.0-20-generic [#20](https://github.com/ROCm/ROCm/pull/20)~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Mar 19 01:28:37 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
> > I also updated the firmware but the version that go installed does not have the change.
> 
> i just discovered that while rocm gave me 40-70 token/s with Qwen3.5-35B-A3B-Q4_K_M.gguf on llama.cpp, depending on whether I was downclocking or not, the llama.cpp vulkan version gives me 74 token/s with that model when underclocked and downvolted at 120W(!!!) and 98 token/s when unthrottled at full 300W TDP.
> 
> on top of that, the bug is gone where the CPU doesn't idle down properly in idle. as soon as the model stops spinning, gpu load is at 0% and power usage at 10W.
> 
> so far, I can't see any downsides of using vulkan over rocm. :-O

we get some insane numbers on qwen 3.5 using vulken mesa 26 and llamacpp on ubuntu
my set up is dual R9700 

https://github.com/ggml-org/llama.cpp/discussions/21043

---

### 评论 #31 — tamascode (2026-04-16T00:47:53Z)

BTW I run the cards at 260W which keeps their fans under 50% at 72F room temperature. 


---

### 评论 #32 — interconnectedMe (2026-05-11T23:25:54Z)

my single R9700 is using ~90W with a model loaded, not working.
any plans for an update on this?

Additional reproduction on single Radeon AI PRO R9700.

## Host

- OS: Ubuntu 24.04.4 LTS / noble
- Kernel: `6.17.0-23-generic`
- Kernel build: `#23~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Tue Apr 14 16:11:48 UTC`
- GPU: AMD Radeon AI PRO R9700
- GFX: `gfx1201`
- Device ID: `0x7551`
- VBIOS: `113-R9700AT-F40`
- AMDGPU DKMS: `amdgpu/6.16.13-2278356.24.04`
- Loaded amdgpu module: `/lib/modules/6.17.0-23-generic/updates/dkms/amdgpu.ko`
- ROCk module: `6.16.13`
- HSA runtime: `Runtime Version 1.18`, `Runtime Ext Version 1.15`
- Host ROCm core: `7.2.0.70200-43~24.04`
- Host HIP runtime: `7.2.26015.70200-43~24.04`
- `linux-firmware`: `20240318.git3b128b60-0ubuntu2.27`

## Firmware from `rocm-smi --showfwinfo`

- MES firmware: `0x00000084`
- MES KIQ firmware: `0x00000084`
- ME firmware: `2880`
- MEC firmware: `3200`
- PFP firmware: `2950`
- SMC firmware: `00.104.75.00`

## llama.cpp

- Image: `ghcr.io/ggml-org/llama.cpp:server-rocm`
- Image digest: `ghcr.io/ggml-org/llama.cpp@sha256:5adb6536e9b8a202ff9172cfffa5a0b390f97df2a5c2e4a8d8e2381e288b2e05`
- Image created: `2026-04-21T06:25:49.88960845Z`
- llama.cpp version: `8864 (ff6b1062a)`
- Build: `built with GNU 13.3.0 for Linux x86_64`
- Container HIP version: `7.2.53211-e1a6bc5663amdgcn`
- Container ROCm core: `7.2.1.70201-81~24.04`

## Repro command shape

Running `llama-server` through Docker ROCm backend:

```bash
docker run --rm --name r9700-llamacpp-qwen36-35b-a3b-apex-i-compact-kv-f16 \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --ipc=host \
  --shm-size 16G \
  -p 8002:8080 \
  -v /srv/models:/srv/models:ro \
  ghcr.io/ggml-org/llama.cpp:server-rocm \
  --model /srv/models/manual/gguf/mudler/Qwen3.6-35B-A3B-APEX-GGUF/Qwen3.6-35B-A3B-APEX-I-Compact.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  --ctx-size 65536 \
  --gpu-layers all \
  --flash-attn on \
  --cache-type-k f16 \
  --cache-type-v f16 \
  --batch-size 2048 \
  --ubatch-size 512 \
  --threads 8 \
  --threads-batch 12 \
  --parallel 1 \
  --cont-batching \
  --jinja \
  --reasoning off \
  --metrics


Observed behavior
Immediately after startup, before inference:

rocm-smi reports GPU use: 100%
Power: around 78W to 87W
VRAM used by llama-server: about 19.18 GB
llama.cpp metrics show:
prompt tokens: 0
generated tokens: 0
active requests: 0
deferred requests: 0
After stopping llama-server:

GPU use drops to around 3%
Power drops to around 14W to 16W
VRAM drops back to baseline
Also tested:

Docker pause: process pauses, but GPU still reports 100% and elevated power.
llama.cpp --sleep-idle-seconds 20: /props reports "is_sleeping": true and VRAM drops to about 0.48GB, but GPU still reports 100% and around 81W.
So this still reproduces the idle-busy / elevated idle power issue on R9700 with MES firmware 0x84.

---

### 评论 #33 — meven3000 (2026-05-11T23:50:28Z)

try add "--no-warmup" see if the issue still occurs.

secondary.
Also, try --no-mmap.

Also try drop your 65536 to say 8192 to test, if llama.cpp ends of transferring layers from CPU memory to GPU memory due to vram being tight then your GPU will also stay at 100%

As far as i've seen this issue is resolved, its more to do with variations of llama.cpp config or vllm config are applied.

for vllm if using 2x GPUs for instance you must set export GPU_MAX_HW_QUEUES=2 otherwise you will also see 100% GPU



---

### 评论 #34 — interconnectedMe (2026-05-12T05:49:13Z)

Thanks @meven3000 

Down at 19W now ;-)

Tested the suggested variants. Summary: `GPU_MAX_HW_QUEUES=1` fixes the idle-busy symptom here; `--no-warmup`, `--no-mmap`, and reducing ctx do not.

Image:

- `ghcr.io/ggml-org/llama.cpp:server-rocm`
- digest: `sha256:5adb6536e9b8a202ff9172cfffa5a0b390f97df2a5c2e4a8d8e2381e288b2e05`
- created: `2026-04-21T06:25:49.88960845Z`
- llama.cpp build: `b8864-ff6b1062a`

Measured after startup, before any inference. `/metrics` showed:

- `llamacpp:prompt_tokens_total 0`
- `llamacpp:tokens_predicted_total 0`
- `llamacpp:requests_processing 0`
- `llamacpp:requests_deferred 0`

| Variant | GPU_MAX_HW_QUEUES | ctx | GPU use | Power | VRAM |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | unset | 65536 | 100% | 95 W | 56% / 19.18 GB |
| `--no-warmup` | unset | 65536 | 100% | 94 W | 56% / 19.18 GB |
| `--no-warmup --no-mmap` | unset | 65536 | 100% | 93 W | 56% / 19.18 GB |
| `--no-warmup --no-mmap` | unset | 8192 | 100% | 92 W | 53% / 18.01 GB |
| baseline | 1 | 65536 | 3% | 22 W | 56% / 19.15 GB |
| `--no-warmup` | 1 | 65536 | 3% | 22 W | 56% / 19.15 GB |
| `--no-warmup --no-mmap` | 1 | 65536 | 3% | 21 W | 56% / 19.15 GB |
| `--no-warmup --no-mmap` | 1 | 8192 | 3% | 21 W | 53% / 17.98 GB |

After stopping `llama-server`, the GPU returned to about 3% use and 21-23 W with llama VRAM released.

So for this single R9700 repro, the important variable appears to be HIP hardware queue count, not warmup, mmap, or 64K context pressure. The working Docker change is:

```bash
-e GPU_MAX_HW_QUEUES=1


> try add "--no-warmup" see if the issue still occurs.
> 
> secondary. Also, try --no-mmap.
> 
> Also try drop your 65536 to say 8192 to test, if llama.cpp ends of transferring layers from CPU memory to GPU memory due to vram being tight then your GPU will also stay at 100%
> 
> As far as i've seen this issue is resolved, its more to do with variations of llama.cpp config or vllm config are applied.
> 
> for vllm if using 2x GPUs for instance you must set export GPU_MAX_HW_QUEUES=2 otherwise you will also see 100% GPU



---
