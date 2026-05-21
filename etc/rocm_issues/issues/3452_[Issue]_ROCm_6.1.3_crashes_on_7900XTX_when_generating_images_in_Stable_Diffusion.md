# [Issue]: ROCm 6.1.3 crashes on 7900XTX when generating images in Stable Diffusion

> **Issue #3452**
> **状态**: closed
> **创建时间**: 2024-07-23T18:01:38Z
> **更新时间**: 2024-08-06T15:09:37Z
> **关闭时间**: 2024-08-06T15:09:37Z
> **作者**: matoro
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3452

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

As requested in https://github.com/ROCm/ROCm/issues/3265 , I'm opening this separate issue since the recommendations listed there did not resolve the issue.

I am running this in an Ubuntu container, but the host and thus kernel is Gentoo.  Kernel is `6.9.9-gentoo-dist`.

Attempting to generate images in Stable Diffusion crashes the card.  The graphical session is recoverable by remotely killing and restarting the X server.

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 3950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

Followed the exact steps as specified in https://github.com/ROCm/ROCm/issues/3265#issuecomment-2245358795

Installed ROCm 6.1.3:
```
$ cat /etc/apt/sources.list.d/rocm.list 
deb [arch=amd64] https://repo.radeon.com/rocm/apt/6.1.3/ jammy main
$ dpkg-query --list '*rocm*'
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                   Version                      Architecture Description
+++-======================-============================-============-===========================================================
ii  rocm                   6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) software stack meta package
ii  rocm-cmake             0.12.0.60103-122~22.04       amd64        rocm-cmake built using CMake
ii  rocm-core              6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-dbgapi            0.71.0.60103-122~22.04       amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent       2.0.3.60103-122~22.04        amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-developer-tools   6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs       1.0.0.60103-122~22.04        amd64        Radeon Open Compute - device libraries
ii  rocm-gdb               14.1.60103-122~22.04         amd64        ROCgdb
ii  rocm-hip-libraries     6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime       6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev   6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-sdk           6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime  6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm              17.0.0.24193.60103-122~22.04 amd64        ROCm core compiler
ii  rocm-ml-libraries      6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ml-sdk            6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
un  rocm-ocl-icd           <none>                       <none>       (no description available)
ii  rocm-opencl            2.0.0.60103-122~22.04        amd64        clr built using CMake
ii  rocm-opencl-dev        2.0.0.60103-122~22.04        amd64        clr built using CMake
ii  rocm-opencl-icd-loader 1.2.60103-122~22.04          amd64        OpenCL-ICD-Loader built using CMake
ii  rocm-opencl-runtime    6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl-sdk        6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp-sdk        6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
un  rocm-smi               <none>                       <none>       (no description available)
ii  rocm-smi-lib           7.2.0.60103-122~22.04        amd64        AMD System Management libraries
ii  rocm-utils             6.1.3.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocminfo               1.0.0.60103-122~22.04        amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool
```

Clone stable diffusion repo.  Make changes as specified:
```
$ grep -E "^[^#]" webui-user.sh
export COMMANDLINE_ARGS="--no-half-vae --opt-sdp-attention"
export TORCH_COMMAND="pip install https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torch-2.1.2%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torchvision-0.16.1%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/pytorch_triton_rocm-2.1.0%2Brocm6.1.3.4d510c3a44-cp310-cp310-linux_x86_64.whl"
export TORCH_BLAS_PREFER_HIPBLASLT=0
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export PYTORCH_ROCM_ARCH=gfx1100
export HIP_VISIBLE_DEVICES=0
export PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512
```

Run and attempt to generate an image.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.13
Runtime Ext Version:     1.4
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
  Name:                    AMD Ryzen 9 3950X 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 3950X 16-Core Processor
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
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65750464(0x3eb45c0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65750464(0x3eb45c0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65750464(0x3eb45c0) KB
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
  Uuid:                    GPU-5fc6ddc1dd71ff02
  Marketing Name:
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
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2304
  BDFID:                   3328
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
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
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 202
  SDMA engine uCode::      21
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***
```

### Additional Information

Stable Diffusion reports:
```
Model loaded in 2.7s (load weights from disk: 0.8s, create model: 0.3s, apply weights to model: 1.3s, calculate empty prompt: 0.2s).
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 20/20 [00:01<00:00, 17.95it/s]
Memory access fault by GPU node-1 (Agent handle: 0x55ac14d27600) on address 0x7f9587e00000. Reason: Page not present or supervisor privilege.s]
./webui.sh: line 304:  4388 Aborted                 "${python_cmd}" -u "${LAUNCH_SCRIPT}" "$@"
```

The following errors are emitted from the kernel:

```
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32783)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:  in process python pid 25698 thread python pid 25698)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:   in page starting at address 0x00007f9587e00000 from client 10
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MORE_FAULTS: 0x1
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          RW: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32783)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:  in process python pid 25698 thread python pid 25698)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:   in page starting at address 0x00007f9587e00000 from client 10
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          RW: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32783)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:  in process python pid 25698 thread python pid 25698)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:   in page starting at address 0x00007f9587e00000 from client 10
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          RW: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32783)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:  in process python pid 25698 thread python pid 25698)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:   in page starting at address 0x00007f9587e00000 from client 10
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          RW: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32783)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:  in process python pid 25698 thread python pid 25698)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:   in page starting at address 0x00007f9587e00000 from client 10
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          RW: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32783)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:  in process python pid 25698 thread python pid 25698)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:   in page starting at address 0x00007f9587e00000 from client 10
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu:          RW: 0x0
[Tue Jul 23 13:49:25 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: Failed to evict queue 1
[Tue Jul 23 13:49:25 2024] print_sq_intr_info_error: 182 callbacks suppressed
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: GPU reset begin!
[Tue Jul 23 13:49:25 2024] amdgpu 0000:0d:00.0: amdgpu: Failed to remove queue 0
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=14
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:26 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:27 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:27 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:27 2024] [drm:amdgpu_debugfs_mes_event_log_init [amdgpu]] *ERROR* MES failed to response msg=3
[Tue Jul 23 13:49:27 2024] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Tue Jul 23 13:49:27 2024] [drm:gfx_v9_4_2_set_power_brake_sequence [amdgpu]] *ERROR* failed to halt cp gfx
[Tue Jul 23 13:49:27 2024] amdgpu 0000:0d:00.0: amdgpu: MODE1 reset
[Tue Jul 23 13:49:27 2024] amdgpu 0000:0d:00.0: amdgpu: GPU mode1 reset
[Tue Jul 23 13:49:27 2024] amdgpu 0000:0d:00.0: amdgpu: GPU smu mode1 reset
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: GPU reset succeeded, trying to resume
[Tue Jul 23 13:49:28 2024] [drm] PCIE GART of 512M enabled (table at 0x0000008001300000).
[Tue Jul 23 13:49:28 2024] [drm] VRAM is lost due to GPU reset!
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: PSP is resuming...
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: RAP: optional rap ta ucode is not available
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: SMU is resuming...
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7e00 (78.126.0)
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: SMU driver if version not matched
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: SMU is resumed successfully!
[Tue Jul 23 13:49:28 2024] [drm] DMUB hardware initialized: version=0x07002A00
[Tue Jul 23 13:49:28 2024] [drm] kiq ring mec 3 pipe 1 q 0
[Tue Jul 23 13:49:28 2024] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: [drm:jpeg_v2_0_dec_ring_emit_ib [amdgpu]] JPEG decode initialized successfully.
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: recover vram bo from shadow start
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: recover vram bo from shadow done
[Tue Jul 23 13:49:28 2024] amdgpu 0000:0d:00.0: amdgpu: GPU reset(3) succeeded!
```

---

## 评论 (16 条)

### 评论 #1 — ppanchad-amd (2024-07-24T15:47:48Z)

@matoro Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2024-07-24T20:16:28Z)

Hi @matoro, thanks for the detailed issue report. I can confirm that I was able to reproduce your issue in some specific cases and am currently investigating. I'll detail my process so far.

Your output from `dpkg-query --list '*rocm*'` matches mine, so there does not appear to be an issue with ROCm component versions. In order to arrive at as similar a configuration as possible, I first uninstalled torch, torchvision, and triton to make sure I'm pulling the same versions as you, then applied your script
```
grep -E "^[^#]" webui-user.sh
export COMMANDLINE_ARGS="--no-half-vae --opt-sdp-attention"
export TORCH_COMMAND="pip install https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torch-2.1.2%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torchvision-0.16.1%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/pytorch_triton_rocm-2.1.0%2Brocm6.1.3.4d510c3a44-cp310-cp310-linux_x86_64.whl"
export TORCH_BLAS_PREFER_HIPBLASLT=0
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export PYTORCH_ROCM_ARCH=gfx1100
export HIP_VISIBLE_DEVICES=0
export PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512
```
to set the environment variables and ran webui.sh. I was able to generate a crash in this configuration.

There are two things I'd like to suggest for now. One is to try running Stable Diffusion with --listen, and accessing the webui from another machine on your network; when I did this I was able to repeatedly generate images without crashing. By default you can access the headless web UI through <the host machine's IP>:7860. 

The other suggestion I have is to try setting up a venv before setting the environment variables and running Stable Diffusion as per https://are-we-gfx1100-yet.github.io/post/a1111-webui/; if you're already doing this and didn't specify or I missed it, I apologize. However, this was inconsistent for me when using a local web UI (i.e. not using the --listen flag); it worked fine multiple times, then I crashed with a local web UI outside of a venv, and following that crash when I went back into the venv to invoke the local web UI again I crashed. This might be due to some corruption that occurs following a crash, or it may just be inconsistent; I'll have to test it further.

Thanks again for your detailed report, there are several reports of Stable Diffusion crashes on the 7900XTX and other cards that we haven't been able to address and you've brought us one step closer to a solution. Let me know if either of my suggestions help you in the short term so we can narrow down the root cause. If neither of these help, I'll try to reproduce your Ubuntu-inside-Gentoo configuration.

---

### 评论 #3 — matoro (2024-07-24T20:32:30Z)

> Hi @matoro, thanks for the detailed issue report. I can confirm that I was able to reproduce your issue in some specific cases and am currently investigating. I'll detail my process so far.
> 
> Your output from `dpkg-query --list '*rocm*'` matches mine, so there does not appear to be an issue with ROCm component versions. In order to arrive at as similar a configuration as possible, I first uninstalled torch, torchvision, and triton to make sure I'm pulling the same versions as you, then applied your script
> 
> ```
> grep -E "^[^#]" webui-user.sh
> export COMMANDLINE_ARGS="--no-half-vae --opt-sdp-attention"
> export TORCH_COMMAND="pip install https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torch-2.1.2%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torchvision-0.16.1%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/pytorch_triton_rocm-2.1.0%2Brocm6.1.3.4d510c3a44-cp310-cp310-linux_x86_64.whl"
> export TORCH_BLAS_PREFER_HIPBLASLT=0
> export HSA_OVERRIDE_GFX_VERSION=11.0.0
> export PYTORCH_ROCM_ARCH=gfx1100
> export HIP_VISIBLE_DEVICES=0
> export PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512
> ```
> 
> to set the environment variables and ran webui.sh. I was able to generate a crash in this configuration.
> 
> There are two things I'd like to suggest for now. One is to try running Stable Diffusion with --listen, and accessing the webui from another machine on your network; when I did this I was able to repeatedly generate images without crashing. By default you can access the headless web UI through <the host machine's IP>:7860.
> 
> The other suggestion I have is to try setting up a venv before setting the environment variables and running Stable Diffusion as per https://are-we-gfx1100-yet.github.io/post/a1111-webui/; if you're already doing this and didn't specify or I missed it, I apologize. However, this was inconsistent for me when using a local web UI (i.e. not using the --listen flag); it worked fine multiple times, then I crashed with a local web UI outside of a venv, and following that crash when I went back into the venv to invoke the local web UI again I crashed. This might be due to some corruption that occurs following a crash, or it may just be inconsistent; I'll have to test it further.
> 
> Thanks again for your detailed report, there are several reports of Stable Diffusion crashes on the 7900XTX and other cards that we haven't been able to address and you've brought us one step closer to a solution. Let me know if either of my suggestions help you in the short term so we can narrow down the root cause. If neither of these help, I'll try to reproduce your Ubuntu-inside-Gentoo configuration.

Hey, thanks so much for looking at it.

First off, stable-diffusion already installs everything to a venv by default.  I don't install anything outside of a venv.

Secondly that snippet wasn't supposed to be a script for setting the environment variables, it was supposed to be demonstrating that I had them set in `webui-user.sh`, which `webui.sh` sources on startup.  That regex simply prints out all lines which are not commented out.  If you do the same thing, then `grep -E "^[^#]" webui-user.sh` should print the same list of `exports`.  That way, you won't have to set those variables every time you run, and you can tweak them before restarting stable-diffusion.

---

### 评论 #4 — matoro (2024-07-24T23:15:16Z)

For posterity's sake, I just tried accessing the UI remotely using `--listen`, and it still crashed my card.  I can't imagine that has anything to do with it.

Besides - if stock stable-diffusion crashes at all, that is a problem.  If the output looks the same, both on the terminal and in `dmesg`, then it's probably the same issue.  Or are you saying that you observed crashes, but with different symptoms?

---

### 评论 #5 — schung-amd (2024-07-25T14:03:46Z)

Hi, thanks for the quick response.

You're correct that Stable Diffusion installs and runs in a venv by default. The behaviour I experienced locally was that manually starting the venv before running fixed the crashes. However, frustratingly, so far today I am unable to reproduce any crashes with --no-half-vae enabled, regardless of manual venv or --listen flag. Running without --no-half-vae still crashes with the same dmesg output you're observing, but as you're crashing with this flag this doesn't seem to be causing your issue.

The next step on my end is to attempt reproduction inside a container in order to match your configuration better. This may be delayed a bit, but I'll update you when I have it set up. In the meantime, can you post the full output from running webui.sh? Also, I apologize if this seems redundant, but just to cover all the bases make sure the environment variables are actually being set and that the correct versions of torch, torchvision, and triton are installed.

I agree that stock Stable Diffusion crashing is an issue, the hope is that finding a consistent workaround will point toward the root cause.

---

### 评论 #6 — matoro (2024-07-25T14:43:27Z)

Sure, here is the complete output when running and then attempting to generate an image.  I do not change any settings or put anything in the prompt.

```
$ ./webui.sh

################################################################
Install script for stable-diffusion + Web UI
Tested on Debian 11 (Bullseye), Fedora 34+ and openSUSE Leap 15.4 or newer.
################################################################

################################################################
Running on matoro user
################################################################

################################################################
Repo already cloned, using it as install directory
################################################################

################################################################
Create and activate python venv
################################################################

################################################################
Launching launch.py...
################################################################
glibc version is 2.35
Check TCMalloc: libtcmalloc_minimal.so.4
libtcmalloc_minimal.so.4 is linked with libc.so,execute LD_PRELOAD=/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4
Python 3.10.12 (main, Mar 22 2024, 16:50:05) [GCC 11.4.0]
Version: v1.9.4-295-g9f5a98d5
Commit hash: 9f5a98d5766b4ac233d916fe8b02ea16b8b2c259
Launching Web UI with arguments: --no-half-vae --opt-sdp-attention
no module 'xformers'. Processing without...
no module 'xformers'. Processing without...
No module 'xformers'. Proceeding without it.
Loading weights [6ce0161689] from /var/tmp/stable-diffusion-webui/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors
Running on local URL:  http://127.0.0.1:7860

To create a public link, set `share=True` in `launch()`.
Startup time: 6.3s (prepare environment: 1.5s, import torch: 1.7s, import gradio: 0.5s, setup paths: 1.5s, other imports: 0.3s, load scripts: 0.3s, create ui: 0.4s).
Creating model from config: /var/tmp/stable-diffusion-webui/configs/v1-inference.yaml
/var/tmp/stable-diffusion-webui/venv/lib/python3.10/site-packages/huggingface_hub/file_download.py:1150: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
Applying attention optimization: sdp... done.
Model loaded in 2.2s (load weights from disk: 0.5s, create model: 0.3s, apply weights to model: 1.1s, calculate empty prompt: 0.2s).
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 20/20 [00:01<00:00, 17.96it/s]
Memory access fault by GPU node-1 (Agent handle: 0x563187d2e580) on address 0x7fe6b8600000. Reason: Page not present or supervisor privilege.s]
./webui.sh: line 304:  1142 Aborted                 "${python_cmd}" -u "${LAUNCH_SCRIPT}" "$@"
```

Here are the complete contents of my `webui-user.sh`:
```
$ cat webui-user.sh
#!/bin/bash
#########################################################
# Uncomment and change the variables below to your need:#
#########################################################

# Install directory without trailing slash
#install_dir="/home/$(whoami)"

# Name of the subdirectory
#clone_dir="stable-diffusion-webui"

# Commandline arguments for webui.py, for example: export COMMANDLINE_ARGS="--medvram --opt-split-attention"
export COMMANDLINE_ARGS="--no-half-vae --opt-sdp-attention"

# python3 executable
#python_cmd="python3"

# git executable
#export GIT="git"

# python3 venv without trailing slash (defaults to ${install_dir}/${clone_dir}/venv)
#venv_dir="venv"

# script to launch to start the app
#export LAUNCH_SCRIPT="launch.py"

# install command for torch
#export TORCH_COMMAND="pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1"
export TORCH_COMMAND="pip install https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torch-2.1.2%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/torchvision-0.16.1%2Brocm6.1.3-cp310-cp310-linux_x86_64.whl https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/pytorch_triton_rocm-2.1.0%2Brocm6.1.3.4d510c3a44-cp310-cp310-linux_x86_64.whl"

# Requirements file to use for stable-diffusion-webui
#export REQS_FILE="requirements_versions.txt"

# Fixed git repos
#export K_DIFFUSION_PACKAGE=""
#export GFPGAN_PACKAGE=""

# Fixed git commits
#export STABLE_DIFFUSION_COMMIT_HASH=""
#export CODEFORMER_COMMIT_HASH=""
#export BLIP_COMMIT_HASH=""

# Uncomment to enable accelerated launch
#export ACCELERATE="True"

# Uncomment to disable TCMalloc
#export NO_TCMALLOC="True"

export TORCH_BLAS_PREFER_HIPBLASLT=0
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export PYTORCH_ROCM_ARCH=gfx1100
export HIP_VISIBLE_DEVICES=0
export PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512

###########################################
```

---

### 评论 #7 — waheedi (2024-07-28T14:48:20Z)

i had similar crashes before, but on a different gfx version, when it reaches the final rendering before it renders the image the graphic card goes into limbo, the problem for my case was overheating, I tried adjust voltage/clocks in my case and the issue disappeared without changing any packages. But it could be a different scenario on your case, it would be helpful if you try to run again with a higher AMD_LOG_LEVEL=1 OR 2 to see whats going on.

---

### 评论 #8 — matoro (2024-07-28T16:26:32Z)

> i had similar crashes before, but on a different gfx version, when it reaches the final rendering before it renders the image the graphic card goes into limbo, the problem for my case was overheating, I tried adjust voltage/clocks in my case and the issue disappeared without changing any packages. But it could be a different scenario on your case, it would be helpful if you try to run again with a higher AMD_LOG_LEVEL=1 OR 2 to see whats going on.

Sure, here's a log of the issue with `AMD_LOG_LEVEL=2` set:  [out.log](https://github.com/user-attachments/files/16404490/out.log)

I wouldn't expect it to be overheating-related, because I am using completely stock settings on my card with no overclocking, and further I am watching temps the entire time and never see it break 60C.  And I am not using anything intense, I am observing the crash while generating a single 512x512 image with stock settings on SD.  What settings did you change exactly?

---

### 评论 #9 — waheedi (2024-07-28T17:00:49Z)

I think you can also try level 3, that would output a lot more stuff, but its always interesting to see more traces, but I think these missing functions are not the real cause for you, but it may be good some good guy have a look into that  :)

What kernel version do you currently run? it may be related to the amdgpu kernel driver

> I wouldn't expect it to be overheating-related, because I am using completely stock settings on my card with no overclocking, and further I am watching temps the entire time and never see it break 60C. And I am not using anything intense, I am observing the crash while generating a single 512x512 image with stock settings on SD. What settings did you change exactly?

overheating can happen in a glimpse of a second and it may not be a real over heat but a hysteresis either hardware or software related (also monitor per second the status use `rocm-smi` ), for me down clocking the voltage and memory clock have helped maintain a consistent stable output. 
 
i dont think that pruned model is more than 4 GB in size and that image generation should not take more than 2GB so in total you are using around 5-7GB so that out of memory is just a crashing procedure (maybe wrong address translation or any similar memory related issue) and not really an out of memory issue. but also driver related, rocm related, pytorch, etc all possibilities are open.

 



---

### 评论 #10 — matoro (2024-07-28T19:31:42Z)

> I think you can also try level 3, that would output a lot more stuff, but its always interesting to see more traces, but I think these missing functions are not the real cause for you, but it may be good some good guy have a look into that :)


Sure, the log was too large to upload to github so [here is a log capture taken with `AMD_LOG_LEVEL=3`](https://synapse.matoro.tk/_matrix/media/v3/download/synapse.matoro.tk/APSCqDTlKprJVINkEJKIMXxH?allow_redirect=true).  I noticed also that this had some c++-mangled names in it, so I ran it through `c++filt` as well.

> What kernel version do you currently run? it may be related to the amdgpu kernel driver

This most recent attempt is on kernel 6.10.2.  I have never been able to successfully generate an image or text on my card with any settings on any kernel.  Using it for compute in any capacity instantly causes this crash.

> > I wouldn't expect it to be overheating-related, because I am using completely stock settings on my card with no overclocking, and further I am watching temps the entire time and never see it break 60C. And I am not using anything intense, I am observing the crash while generating a single 512x512 image with stock settings on SD. What settings did you change exactly?
> 
> overheating can happen in a glimpse of a second and it may not be a real over heat but a hysteresis either hardware or software related (also monitor per second the status use `rocm-smi` ), for me down clocking the voltage and memory clock have helped maintain a consistent stable output.

Can you share exactly what settings you used?  I'm just tired of randomly flipping settings only to get the same results over and over.

> i dont think that pruned model is more than 4 GB in size and that image generation should not take more than 2GB so in total you are using around 5-7GB so that out of memory is just a crashing procedure (maybe wrong address translation or any similar memory related issue) and not really an out of memory issue. but also driver related, rocm related, pytorch, etc all possibilities are open.

I am using the exact ROCm packages and pytorch packages that were specified by @schung-amd , an AMD employee, in https://github.com/ROCm/ROCm/issues/3265#issuecomment-2245358795 .  I can't imagine how this could be any closer to textbook at least from the userspace side.

---

### 评论 #11 — waheedi (2024-07-28T19:49:24Z)

> Sure, the log was too large to upload to github so [here is a log capture taken with `AMD_LOG_LEVEL=3`](https://synapse.matoro.tk/_matrix/media/v3/download/synapse.matoro.tk/APSCqDTlKprJVINkEJKIMXxH?allow_redirect=true). I noticed also that this had some c++-mangled names in it, so I ran it through `c++filt` as well.

I think the card goes into limbo and its not any more an accessible resource at the point where it says out of memory or privileges. what does rocm-smi reports after its dead, does it actually have the card listed with all its correct parameters values, like temp, vram etc?

I saw that you wrote the card remains functional after the crash but is it really functional or its just have a framebuffer capability and not ROCm, or it can start the script without any problem and then crashes at 20/20?

> This most recent attempt is on kernel 6.10.2. I have never been able to successfully generate an image or text on my card with any settings on any kernel. Using it for compute in any capacity instantly causes this crash.

So basically you tried earlier versions like 6.4? 

> Can you share exactly what settings you used? I'm just tired of randomly flipping settings only to get the same results over and over.

I actually did not understand which settings should I share :), the kernel parameters settings, or the DF parameters settings or which settings? also regarding kernel parameters are using any?



---

### 评论 #12 — matoro (2024-07-28T21:23:30Z)

> > Sure, the log was too large to upload to github so [here is a log capture taken with `AMD_LOG_LEVEL=3`](https://synapse.matoro.tk/_matrix/media/v3/download/synapse.matoro.tk/APSCqDTlKprJVINkEJKIMXxH?allow_redirect=true). I noticed also that this had some c++-mangled names in it, so I ran it through `c++filt` as well.
> 
> I think the card goes into limbo and its not any more an accessible resource at the point where it says out of memory or privileges. what does rocm-smi reports after its dead, does it actually have the card listed with all its correct parameters values, like temp, vram etc?
> 
> I saw that you wrote the card remains functional after the crash but is it really functional or its just have a framebuffer capability and not ROCm, or it can start the script without any problem and then crashes at 20/20?

Yes, as soon as the driver resets the card (after the line that says `amdgpu: GPU reset(3) succeeded!`) then it resumes being fully functional, except that the Xorg session freezes.  It continues displaying a frozen image of whatever was on screen at the time of the crash.  If I ssh in and kill the Xorg session and start a new one, the new session is fully functional.

> > This most recent attempt is on kernel 6.10.2. I have never been able to successfully generate an image or text on my card with any settings on any kernel. Using it for compute in any capacity instantly causes this crash.
> 
> So basically you tried earlier versions like 6.4?

I've periodically tried this at least once on all major kernel releases since support was added, which is a pretty recent version.  I don't think 7900XTX was supported as far back as kernel 6.4.  Regardless, I've tried on 6.9 and 6.10 at least in this thread.

> > Can you share exactly what settings you used? I'm just tired of randomly flipping settings only to get the same results over and over.
> 
> I actually did not understand which settings should I share :), the kernel parameters settings, or the DF parameters settings or which settings? also regarding kernel parameters are using any?

My full kernel command line is:
```
ro debug amd_iommu=pt pcie_acs_override=downstream rd.driver.pre=vfio-pci mitigations=off transparent_hugepage=never rcu_nocbs=8-15,24-31 nohz_full=8-15,24-31 clocksource=tsc acpi_enforce_resources=lax amdgpu.ppfeaturemask=0xffffffff amdgpu.mcbp=0
```

Some of those are related to running virtual machines - since my 7900XTX does not work for compute, I pass through an NVIDIA card to a virtual machine.  The last two items especially (`amdgpu.ppfeaturemask=0xffffffff amdgpu.mcbp=0`) were recommended by other users who reported that it solved their problems, but neither of them has worked for me.

You said earlier:
> for me down clocking the voltage and memory clock have helped maintain a consistent stable output.
That is what I am looking for.  Can you please specify what voltage and memory clock you set?

---

### 评论 #13 — waheedi (2024-07-28T21:38:34Z)

sure, the voltages and clocks can be adjusted using normal cat and echo command lines on the sys/fs files, here is a repo that does that in a nice script, thanks to this guy:) https://github.com/sibradzic/amdgpu-clocks if you need the actual values for the clock and voltages then my numbers are not going to help you because they are not for RX7900X but what you can do, is look into the current table and try to down it by a factor of 10%

The boot params looks good, and I think just for a temporary test, which is not really good (because it disables the dynamic power management of the card) but try it to see if that also crashes `amdgpu.dpm=0`  
I recommend removing the rest of the params except the ppfeaturemask and amd_iommu to make sure nothing is causing out of control behavior which is mostly not the case.



---

### 评论 #14 — smirgol (2024-08-05T17:14:44Z)

Just wanted to chime in and confirm that I'm having the same issue (again). It used to work, but suddenly when I tried to use Stable Diffusion again at a later time, it had stopped working and is crashing my X11 session (again), which I'm unable to recover without a reboot.  

I say again, because it really likes to break out of a sudden every now and then. I then somehow manage to get it back to a working state after a while and lots of fiddling and try&error, only for it to break again at a later time for whatever reason. It's super fragile somehow, which is frustrating because I don't know why. :|


syslog: same as OP,
GPU: same as OP
OS: Ubuntu 22.04.4 LTS
Kernel: 6.9.9
ROCm: both 6.1.2 and 6.2

### Packages:
```
ii  rocm-core                                                   6.2.0.60200-66~22.04                                    amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                                            1.0.0.60200-66~22.04                                    amd64        Radeon Open Compute - device libraries
ii  rocm-llvm                                                   18.0.0.24292.60200-66~22.04                             amd64        ROCm core compiler
ii  rocm-smi-lib                                                7.3.0.60200-66~22.04                                    amd64        AMD System Management libraries
ii  rocminfo                                                    1.0.0.60200-66~22.04                                    amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool

ii  amdgpu-core                                                 1:6.2.60200-2009582.22.04                               all          Core meta package for unified amdgpu driver.
ii  amdgpu-install                                              6.2.60200-2009582.22.04                                 all          AMDGPU driver repository and installer
ii  libdrm-amdgpu-amdgpu1:amd64                                 1:2.4.120.60200-2009582.22.04                           amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm-amdgpu-common                                        1.0.0.60200-2009582.22.04                               all          List of AMD/ATI cards' device IDs, revision IDs and marketing names
ii  libdrm-amdgpu-dev:amd64                                     1:2.4.120.60200-2009582.22.04                           amd64        Userspace interface to kernel DRM services -- development files
ii  libdrm-amdgpu-radeon1:amd64                                 1:2.4.120.60200-2009582.22.04                           amd64        Userspace interface to radeon-specific kernel DRM services -- runtime
ii  libdrm-amdgpu1:amd64                                        2.4.120-1~kisak~j                                       amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm-amdgpu1:i386                                         2.4.120-1~kisak~j                                       i386         Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm2-amdgpu:amd64                                        1:2.4.120.60200-2009582.22.04                           amd64        Userspace interface to kernel DRM services -- runtime
ii  ricks-amdgpu-utils                                          3.6.0-2                                                 all          transitional package
ii  xserver-xorg-video-amdgpu                                   22.0.0-1ubuntu0.2                                       amd64        X.Org X server -- AMDGPU display driver
```

### ENV
```
export PATH="/opt/rocm/bin:$PATH"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/rocm/lib/"
export ROCM_VERSION=6.2
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export HCC_AMDGPU_TARGET=gfx1100
export GPU_MAX_HW_QUEUES=1
export TORCH_BLAS_PREFER_HIPBLASLT=0
```

### pip list | grep torch  (from within venv)
```
open-clip-torch              2.20.0
pytorch-lightning            1.9.4
pytorch-triton-rocm          3.0.0+01cbe5045a
torch                        2.5.0.dev20240616+rocm6.1
torchaudio                   2.4.0.dev20240616+rocm6.1
torchcrepe                   0.0.20
torchdiffeq                  0.2.3
torchfcpe                    0.0.4
torchmetrics                 1.2.0
torchsde                     0.2.6
torchvision                  0.19.0.dev20240616+rocm6.1
```

### GRUB
```
quiet splash amdgpu.ppfeaturemask=0xfff7ffff amd_iommu=on iommu=pt
```

### automatic1111 start line
```
PYTORCH_HIP_ALLOC_CONF=max_split_size_mb:128 ./webui-my.sh --opt-split-attention --api --no-half-vae
```
Note: `webui-my.sh` is a copy of an older version of the original start script, where I've modified it to detect my GPU properly


### EDIT:

I've tried a fresh install of automatic1111 and this one did not crash, but it used different options than I do:
```
--precision full --no-half
```

With these it does not crash and I remember that I had to use `--no-half` quite a while ago to not make it crash, but later at some point I could drop it without issues. Looks like I now again need this option.

Anyways, with this line it no longer crashes on my existing installation of automatic1111:
```
PYTORCH_HIP_ALLOC_CONF=max_split_size_mb:128 ./webui-my.sh --opt-split-attention --api --no-half-vae --precision full --no-half
```
The rest stays as described above. I'll see how it goes, at least it doesn't crash immediately now, which I'd call progress. :)


---

### 评论 #15 — matoro (2024-08-06T02:39:03Z)

Thank you for this, the above was enough to finally get a session where I was able to generate images.

After I confirmed that it was successfully stable, I tried to reduce the options one-by-one to come up with a set of options which would reliably reproduce the problem.  However, what I found out instead is that the issue is not reproducible on-demand.  Some option sets would crash, so I would remove an option and try again, get no crash, then go back to the one that originally showed it and get no crash.  At least I did observe that if it crashed, it would do so on the first image generation.  If it generated a single image and didn't crash, then generating further images regardless of model would also not crash.

I was able to at one point completely empty my `COMMANDLINE_ARGS` variable and not get a crash.  The best option seems to be as above:
```
export COMMANDLINE_ARGS="--opt-split-attention --no-half-vae --precision full --no-half"
```
as I never got a crash on this configuration.  Unfortunately, seems that since the problem is intermittent when changing options, and the same sets of options do not always trigger it, it might be hard to track down.

Additionally there's no guarantee that it's not a stateful issue, where switching the options itself is what triggers the problem.

---

### 评论 #16 — schung-amd (2024-08-06T14:09:47Z)

Thanks for following up on this, I'm glad you were able to get things working. @smirgol I noticed you're on ROCm 6.2 now; out of curiosity, do you crash without `--no-half` on ROCm 6.1.x, or is this behavior new to ROCm 6.2? Our internal reproduction of the crash on ROCm 6.1.3 was fixed with `--no-half-vae` alone, but I wonder if we were just "fortunate" in not requiring `--no-half` for some reason, and in retrospect requiring both makes sense as both are related to FP16 support. Stable Diffusion crashes on the 7900XTX have been reported from time to time and we've had a hard time reproducing the crashes internally, so this is a good data point.

Looking at the A1111 repo, it seems like both `--no-half` and `--no-half-vae` are known to be necessary on some AMD cards (e.g. https://github.com/vladmandic/automatic/discussions/1041, also see `--no-half` requirement stated for some AMD cards in https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs), but it appears these flags were automatically set at some point and are no longer, so some of the intermittent nature of this issue might be due to A1111 version differences. 

@matoro If the issue appears to be solved on your end after a while, please close this issue, or I'll close this if I don't hear any further issues by the end of the week; but feel free to reopen or make a new issue if you start experiencing these crashes again. It seems like half precision is a common pain point for Stable Diffusion configurations in general, and I don't know if an internal solution is possible.

---
