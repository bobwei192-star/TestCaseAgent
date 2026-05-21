# [Issue]: Strix Halo (gfx1151) gives segfault on any VRAM access with torch nightly package

> **Issue #5853**
> **状态**: closed
> **创建时间**: 2026-01-15T03:34:20Z
> **更新时间**: 2026-03-17T15:38:29Z
> **关闭时间**: 2026-03-17T15:38:28Z
> **作者**: chaserhkj
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5853

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

I don't know if there is anything wrong with my setup, but on my Strix Halo platform any ROCm VRAM access seems to consistently give me segfault with the torch nightly package. Nightly package from [TheRock](https://github.com/ROCm/TheRock/blob/main/RELEASES.md) seems to work fine though. My problem is that I hope to use pre-built binary version of llama.cpp container images to host LLMs, and they just fail the similar way - upon VRAM allocation throwing out a segfault. While I could build llama.cpp myself with the rock package I would say ideally I just want the prebuilt binary to work.

See below for more details

### Operating System

Arch Linux (rolling)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

Radeon 8060S

### ROCm Version

ROCm 7.1.0

### ROCm Component

_No response_

### Steps to Reproduce

test.py:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device: {torch.cuda.get_device_name(0)}")
x = torch.tensor([1.0, 2.0, 3.0]).cuda()
y = torch.tensor([1.0, 2.0, 3.0]).cuda()
print(x + y)
```

With torch nightly version:
```
$ uv venv --python 3.12 venv-multi-bin
$ source venv-multi-bin/bin/activate
$ uv pip install --index-url https://download.pytorch.org/whl/nightly/rocm7.1 torch
$ uv run python test.py
/var/home/hkj/venv-multi-bin/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:307: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
CUDA available: True
Device: AMD Radeon 8060S
Segmentation fault
```
Similar faults happen when I attempt to run any other workloads with other frameworks like llama.cpp, etc. I inspected the dumped cores they seemed to fault at the same point.

With the rock package:
```
$ uv venv --python 3.12 venv-gfx1151-only
$ source venv-gfx1151-only/bin/activate
$ uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ torch
$ uv run python test.py
/var/home/hkj/venv-gfx1151-only/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:279: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /__w/TheRock/TheRock/external-builds/pytorch/pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
CUDA available: True
Device: Radeon 8060S Graphics
tensor([2., 4., 6.], device='cuda:0')
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

The above test is done bare metal. I can only run "rocminfo" from a container, but the container is the base for the prebuilt llama.cpp binaries I tested that exhibited similar faults so I guess it is still applicable:
```
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5187
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
      Size:                    130488832(0x7c71a00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130488832(0x7c71a00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    130488832(0x7c71a00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    130488832(0x7c71a00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1151
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon Graphics
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
    L2:                      2048(0x800) KB
    L3:                      32768(0x8000) KB
  Chip ID:                 5510(0x1586)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2900
  BDFID:                   50432
  Internal Node ID:        1
  Compute Unit:            40
  SIMDs per CU:            2
  Shader Engines:          2
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
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
  Packet Processor uCode:: 32
  SDMA engine uCode::      17
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    125829120(0x7800000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    125829120(0x7800000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1151
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
```

### Additional Information

I have:

```
$ cat /etc/modprobe.d/uma-allocation.conf
# Maximize GTT for LLM usage on 128GB UMA system
options ttm pages_limit=31457280
options ttm page_pool_size=15728640
$ sudo dmesg | grep GTT
[    5.721182] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 122880M of GTT memory ready.
```

I tried setting 
```
HSA_OVERRIDE_GFX_VERSION=11.0.0
HSA_OVERRIDE_GFX_VERSION=11.5.0
HSA_OVERRIDE_GFX_VERSION=11.5.1
```
None worked.

I tried running with `AMD_LOG_LEVEL=5 HSA_ENABLE_DEBUG=1 HSAKMT_DEBUG_LEVEL=7` and got these outputs before segfault:
```
/var/home/hkj/venv/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:307: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
udmabuf is not enabled
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
SVM alignment default order is 9.acquiring VM for 11ba using 8
Initialized unreserved SVM apertures: 0x200000 - 0x7fffffffffff
mem_handle_aperture start 0x2800000000000, mem_handle_aperture limit 0x3000000000000
SVM alignment default order is 9.acquiring VM for 11ba using 8
Initialized unreserved SVM apertures: 0x200000 - 0x7fffffffffff
mem_handle_aperture start 0x2800000000000, mem_handle_aperture limit 0x3000000000000
[hsaKmtMapMemoryToGPU] address 0x7ff827f00000
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x7ff6bc600000 flags 0x20040 size 0x200000 node_id 0
numa_node_id is out range: numa_node_id 0, num_node 1
[hsaKmtAllocMemoryAlign] node 0 address 0x7ff6bc600000 size 2097152 from host
[hsaKmtMapMemoryToGPUNodes] address 0x7ff6bc600000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x7ff5bbc00000 size 4294967296 from scratch
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x7ff827f0c000 flags 0x821040 size 0x1000 node_id 0
numa_node_id is out range: numa_node_id 0, num_node 1
[hsaKmtAllocMemoryAlign] node 0 address 0x7ff827f0c000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x7ff827f0c000 number of nodes 1
:3:rocdevice.cpp            :420 : 6744385914 us: [pid:25927 tid: 0x7ff8286d8740] Initalizing runtime stack, Enumerated GPU agents = 1
:3:rocdevice.cpp            :187 : 6744385940 us: [pid:25927 tid: 0x7ff8286d8740] Numa selects cpu agent[0]=0x29d97290(fine=0x29dacc00,coarse=0x297b2ba0) for gpu agent=0x297b3980 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :277 : 6744385948 us: [pid:25927 tid: 0x7ff8286d8740] Using dev kernel arg wa = 0
:3:comgrctx.cpp             :127 : 6744385981 us: [pid:25927 tid: 0x7ff8286d8740] Loaded COMGR library version 3.0.
[hsaKmtGetTileConfig] node 1
:3:rocdevice.cpp            :1590: 6744386159 us: [pid:25927 tid: 0x7ff8286d8740] addressableNumVGPRs=256, totalNumVGPRs=1536, vGPRAllocGranule=24, availableRegistersPerCU_=196608
:3:rocdevice.cpp            :1604: 6744386168 us: [pid:25927 tid: 0x7ff8286d8740] imageSupport=1
:3:rocdevice.cpp            :1635: 6744386171 us: [pid:25927 tid: 0x7ff8286d8740] Gfx Major/Minor/Stepping: 11/5/1
:3:rocdevice.cpp            :1637: 6744386173 us: [pid:25927 tid: 0x7ff8286d8740] HMM support: 1, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1639: 6744386175 us: [pid:25927 tid: 0x7ff8286d8740] Max SDMA Read Mask: 0x1, Max SDMA Write Mask: 0x1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x7ff5bae00000 flags 0x2040 size 0x400000 node_id 0
numa_node_id is out range: numa_node_id 0, num_node 1
[hsaKmtAllocMemoryAlign] node 0 address 0x7ff5bae00000 size 4194304 from host
:4:rocdevice.cpp            :2007: 6744386887 us: [pid:25927 tid: 0x7ff8286d8740] Allocate hsa host memory 0x7ff5bae00000, size 0x400000, numa_node = 0, mem_seg = 0
[hsaKmtQueryPointerInfo] pointer 0x7ff5bae00000
[hsaKmtMapMemoryToGPUNodes] address 0x7ff5bae00000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x7ff827f0a000 flags 0x40 size 0x1000 node_id 0
numa_node_id is out range: numa_node_id 0, num_node 1
[hsaKmtAllocMemoryAlign] node 0 address 0x7ff827f0a000 size 4096 from host
:4:rocdevice.cpp            :2007: 6744386967 us: [pid:25927 tid: 0x7ff8286d8740] Allocate hsa host memory 0x7ff827f0a000, size 0x38, numa_node = 0, mem_seg = 1
[hsaKmtQueryPointerInfo] pointer 0x7ff827f0a000
[hsaKmtMapMemoryToGPUNodes] address 0x7ff827f0a000 number of nodes 1
:3:hip_context.cpp          :60  : 6744386983 us: [pid:25927 tid: 0x7ff8286d8740] HIP Version: 7.1.52802.26aae437f6, Direct Dispatch: 1
:3:os_posix.cpp             :961 : 6744386994 us: [pid:25927 tid: 0x7ff8286d8740] HIP Library Path: /var/home/hkj/venv/lib/python3.12/site-packages/torch/lib/libamdhip64.so
:3:hip_device_runtime.cpp   :703 : 6744399665 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDeviceCount ( 0x7ffeb78ca13c )
:3:hip_device_runtime.cpp   :705 : 6744399672 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDeviceCount: Returned hipSuccess :
CUDA available: True
:3:hip_device_runtime.cpp   :703 : 6744399774 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDeviceCount ( 0x7ffeb78ca0f0 )
:3:hip_device_runtime.cpp   :705 : 6744399777 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDeviceCount: Returned hipSuccess :
:3:hip_device.cpp           :659 : 6744399790 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevicePropertiesR0600 ( 0x2a38a160, 0 )
:3:hip_device.cpp           :661 : 6744399796 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevicePropertiesR0600: Returned hipSuccess :
:3:hip_device_runtime.cpp   :703 : 6744399806 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDeviceCount ( 0x7ffeb78c9f9c )
:3:hip_device_runtime.cpp   :705 : 6744399809 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDeviceCount: Returned hipSuccess :
:3:hip_device_runtime.cpp   :703 : 6744399840 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDeviceCount ( 0x7ff74c46afa4 )
:3:hip_device_runtime.cpp   :705 : 6744399843 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDeviceCount: Returned hipSuccess :
:3:hip_device.cpp           :659 : 6744399847 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevicePropertiesR0600 ( 0x7ffeb78c9bd8, 0 )
:3:hip_device.cpp           :661 : 6744399849 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevicePropertiesR0600: Returned hipSuccess :
:3:hip_device_runtime.cpp   :687 : 6744399871 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c9d0c )
:3:hip_device_runtime.cpp   :699 : 6744399875 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :365 : 6744400132 us: [pid:25927 tid: 0x7ff8286d8740]  hipDevicePrimaryCtxGetState ( 0, 0x7ffeb78c9d24, 0x7ffeb78c9d28 )
:3:hip_context.cpp          :379 : 6744400137 us: [pid:25927 tid: 0x7ff8286d8740] hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :687 : 6744400140 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c9d0c )
:3:hip_device_runtime.cpp   :699 : 6744400142 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :365 : 6744400145 us: [pid:25927 tid: 0x7ff8286d8740]  hipDevicePrimaryCtxGetState ( 0, 0x7ffeb78c9d24, 0x7ffeb78c9d28 )
:3:hip_context.cpp          :379 : 6744400146 us: [pid:25927 tid: 0x7ff8286d8740] hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :687 : 6744400154 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c9efc )
:3:hip_device_runtime.cpp   :699 : 6744400158 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :365 : 6744400162 us: [pid:25927 tid: 0x7ff8286d8740]  hipDevicePrimaryCtxGetState ( 0, 0x7ffeb78c9f14, 0x7ffeb78c9f18 )
:3:hip_context.cpp          :379 : 6744400168 us: [pid:25927 tid: 0x7ff8286d8740] hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device.cpp           :659 : 6744400644 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevicePropertiesR0600 ( 0x7ffeb78c9830, 0 )
:3:hip_device.cpp           :661 : 6744400650 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevicePropertiesR0600: Returned hipSuccess :
Device: AMD Radeon 8060S
:3:hip_device_runtime.cpp   :687 : 6744400848 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c9e74 )
:3:hip_device_runtime.cpp   :699 : 6744400852 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :687 : 6744400890 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c9094 )
:3:hip_device_runtime.cpp   :699 : 6744400894 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :687 : 6744400898 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c8f54 )
:3:hip_device_runtime.cpp   :699 : 6744400902 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :687 : 6744400909 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c8ddc )
:3:hip_device_runtime.cpp   :699 : 6744400912 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_stream.cpp           :316 : 6744400919 us: [pid:25927 tid: 0x7ff8286d8740]  hipDeviceGetStreamPriorityRange ( 0x7ffeb78c8d90, 0x7ffeb78c8db0 )
:3:hip_stream.cpp           :324 : 6744400924 us: [pid:25927 tid: 0x7ff8286d8740] hipDeviceGetStreamPriorityRange: Returned hipSuccess :
:3:hip_error.cpp            :34  : 6744400939 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetLastError (  )
:3:hip_device_runtime.cpp   :687 : 6744400943 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c85bc )
:3:hip_device_runtime.cpp   :699 : 6744400945 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1075: 6744400954 us: [pid:25927 tid: 0x7ff8286d8740]  hipStreamIsCapturing ( char array:<null>, 0x7ffeb78c8820 )
:3:hip_graph.cpp            :1076: 6744400958 us: [pid:25927 tid: 0x7ff8286d8740] hipStreamIsCapturing: Returned hipSuccess :
:3:hip_memory.cpp           :759 : 6744400968 us: [pid:25927 tid: 0x7ff8286d8740]  hipMalloc ( 0x7ffeb78c8900, 2097152 )
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x7ff5baa00000 size 2097152 from device
[hsaKmtMapMemoryToGPUNodes] address 0x7ff5baa00000 number of nodes 1
:4:rocdevice.cpp            :2186: 6744401102 us: [pid:25927 tid: 0x7ff8286d8740] Allocate hsa device memory 0x7ff5baa00000, size 0x200000, hsa_mem_flags 0x0h
:3:rocdevice.cpp            :2226: 6744401106 us: [pid:25927 tid: 0x7ff8286d8740] Device=0x29fe6170, freeMem_ = 0x1dffe00000
:3:hip_memory.cpp           :761 : 6744401112 us: [pid:25927 tid: 0x7ff8286d8740] hipMalloc: Returned hipSuccess : 0x7ff5baa00000: duration: 144 us
:3:hip_device_runtime.cpp   :773 : 6744401131 us: [pid:25927 tid: 0x7ff8286d8740]  hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :778 : 6744401134 us: [pid:25927 tid: 0x7ff8286d8740] hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :773 : 6744401137 us: [pid:25927 tid: 0x7ff8286d8740]  hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :778 : 6744401139 us: [pid:25927 tid: 0x7ff8286d8740] hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :687 : 6744401180 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c8d34 )
:3:hip_device_runtime.cpp   :699 : 6744401183 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :687 : 6744401185 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c8b6c )
:3:hip_device_runtime.cpp   :699 : 6744401187 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :365 : 6744401191 us: [pid:25927 tid: 0x7ff8286d8740]  hipDevicePrimaryCtxGetState ( 0, 0x7ffeb78c8b84, 0x7ffeb78c8b88 )
:3:hip_context.cpp          :379 : 6744401195 us: [pid:25927 tid: 0x7ff8286d8740] hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :687 : 6744401199 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c8b4c )
:3:hip_device_runtime.cpp   :699 : 6744401202 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1075: 6744401207 us: [pid:25927 tid: 0x7ff8286d8740]  hipStreamIsCapturing ( char array:<null>, 0x7ffeb78c8d70 )
:3:hip_graph.cpp            :1076: 6744401212 us: [pid:25927 tid: 0x7ff8286d8740] hipStreamIsCapturing: Returned hipSuccess :
:3:hip_device_runtime.cpp   :687 : 6744401216 us: [pid:25927 tid: 0x7ff8286d8740]  hipGetDevice ( 0x7ffeb78c8b4c )
:3:hip_device_runtime.cpp   :699 : 6744401218 us: [pid:25927 tid: 0x7ff8286d8740] hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2045: 6744401228 us: [pid:25927 tid: 0x7ff8286d8740]  hipStreamGetCaptureInfo ( char array:<null>, 0x7ffeb78c8d3c, char array:<null> )
:3:hip_graph.cpp            :2046: 6744401231 us: [pid:25927 tid: 0x7ff8286d8740] hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :809 : 6744401245 us: [pid:25927 tid: 0x7ff8286d8740]  hipMemcpyWithStream ( 0x7ff5baa00000, 0x2a3a4c40, 12, hipMemcpyHostToDevice, char array:<null> )
:5:hip_device.cpp           :35  : 6744401248 us: [pid:25927 tid: 0x7ff8286d8740] NullStream (nil), wait 1
:3:rocdevice.cpp            :2871: 6744401254 us: [pid:25927 tid: 0x7ff8286d8740] Number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x7ff827efe000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x7ff827efe000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x7ff827efc000 flags 0x21040 size 0x1000 node_id 0
numa_node_id is out range: numa_node_id 0, num_node 1
[hsaKmtAllocMemoryAlign] node 0 address 0x7ff827efc000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x7ff827efc000 number of nodes 1
[hsaKmtMapMemoryToGPUNodes] address 0x7ff827efa000 number of nodes 1
Allocating VRAM for EOP
[hsaKmtMapMemoryToGPUNodes] address 0x7ff827ef8000 number of nodes 1
Allocating GTT for CWSR
hsaKmtSVMSetAttr: address 0x0x7ff5b9c00000 size 0xd56000
[hsaKmtUnmapMemoryToGPU] address 0x7ff827ef8000
[hsaKmtFreeMemory] address 0x7ff827ef8000
[hsaKmtUnmapMemoryToGPU] address 0x7ff827efa000
[hsaKmtFreeMemory] address 0x7ff827efa000
[hsaKmtUnmapMemoryToGPU] address 0x7ff827efe000
[hsaKmtFreeMemory] address 0x7ff827efe000
[hsaKmtUnmapMemoryToGPU] address 0x7ff827efc000
[hsaKmtFreeMemory] address 0x7ff827efc000
```

---

## 评论 (12 条)

### 评论 #1 — lucbruni-amd (2026-01-19T19:07:57Z)

Hi @chaserhkj,

Thanks for reporting this issue and providing comprehensive info - that's very helpful.

I've tested the following three installations on `gfx1151` and `Ubuntu 24.04`:

```
# TheRock nightly
$pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ torch torchaudio torchvision
...
Successfully installed MarkupSafe-3.0.2 filelock-3.19.1 fsspec-2025.7.0 jinja2-3.1.6 mpmath-1.3.0 networkx-3.5 numpy-2.3.2 pillow-11.3.0 rocm-7.11.0a20260113 rocm-sdk-core-7.11.0a20260113 rocm-sdk-libraries-gfx1151-7.11.0a20260113 setuptools-80.9.0 sympy-1.14.0 torch-2.9.1+rocm7.11.0a20260113 torchaudio-2.9.0+rocm7.11.0a20260113 torchvision-0.24.0+rocm7.11.0a20260113 triton-3.5.1+rocm7.11.0a20260113 typing-extensions-4.14.1
$python test.py
CUDA available: True
Device: Radeon 8060S Graphics
tensor([2., 4., 6.], device='cuda:0')
# Consistent with your result other than the Numpy warning
```

```
# Your command for upstream wheels
$pip install --index-url https://download.pytorch.org/whl/nightly/rocm7.1 torch
...
Successfully installed MarkupSafe-3.0.2 filelock-3.20.3 fsspec-2026.1.0 jinja2-3.1.6 mpmath-1.3.0 networkx-3.6.1 setuptools-78.1.0 sympy-1.14.0 torch-2.11.0.dev20260119+rocm7.1 triton-rocm-3.6.0+git9844da95 typing-extensions-4.15.0
$python test.py
.venv-torch/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:307: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
CUDA available: True
Device: AMD Radeon 8060S
tensor([2., 4., 6.], device='cuda:0')
# Reproduces the /opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory issue, Numpy warning, but not the segmentation fault
```

```
# Pytorch install command
$pip install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/rocm7.1
...
Successfully installed MarkupSafe-3.0.2 filelock-3.20.3 fsspec-2026.1.0 jinja2-3.1.6 mpmath-1.3.0 networkx-3.6.1 numpy-2.4.1 pillow-12.1.0 setuptools-78.1.0 sympy-1.14.0 torch-2.11.0.dev20260118+rocm7.1 torchvision-0.25.0.dev20260119+rocm7.1 triton-rocm-3.6.0+git9844da95 typing-extensions-4.15.0
$python test.py
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
CUDA available: True
Device: AMD Radeon 8060S
tensor([2., 4., 6.], device='cuda:0')
# No Numpy warning, but no segmentation fault still
```

Now, I understand you are on Arch and there also going to be some environmental differences, so I will continue from my end to try and reproduce the segmentation fault. Thanks for your patience.

Edit: added installed versions

---

### 评论 #2 — lucbruni-amd (2026-01-21T19:16:08Z)

Tested this with the `archlinux:latest` image and also failed to reproduce the segmentation fault:

```
(venv) # uv pip install --index-url https://download.pytorch.org/whl/nightly/rocm7.1 torch
Using Python 3.12.12 environment at: venv
Resolved 11 packages in 1.37s
Prepared 11 packages in 3m 17s
Installed 11 packages in 342ms
 + filelock==3.20.3
 + fsspec==2026.1.0
 + jinja2==3.1.6
 + markupsafe==3.0.2
 + mpmath==1.3.0
 + networkx==3.6.1
 + setuptools==78.1.0
 + sympy==1.14.0
 + torch==2.11.0.dev20260121+rocm7.1
 + triton-rocm==3.6.0+git9844da95
 + typing-extensions==4.15.0
(venv) # uv run python test.py
.../venv/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:307: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
/opt/amdgpu/share/libdrm/amdgpu.ids: No such file or directory
CUDA available: True
Device: AMD Radeon 8060S
tensor([2., 4., 6.], device='cuda:0')
```

Mind you, these are slightly newer wheels - could you re-test with nightlies from at least January 18th as my above test was also successful. Thanks!

---

### 评论 #3 — wingrunr21 (2026-01-21T22:38:32Z)

I'm seeing the same thing via the current `rocm/vllm-dev:nightly` image on an Arch Linux host. Repro steps:

Put `test.py` from the original post in a working directory and run the following:

```bash
docker run -it -v ./test.py:/app/test.py --rm --runtime=amd -e AMD_VISIBLE_DEVICES=1 --entrypoint /bin/bash rocm/vllm-dev:nightly --login
/usr/bin/python test.py
```

Note that you need to run this via an interactive shell as it does seem using `python` as the entry point does not trigger the segfault.

I've set `AMD_VISIBLE_DEVICES=1` here as I also have an R9700 installed in this system (which doesn't segfault).

---

### 评论 #4 — chaserhkj (2026-01-21T23:06:43Z)

I tested using `docker.io/archlinux/archlinux` distrobox (this is slightly newer than archlinux:latest) and latest wheels but still get the segfault.

I thought to find out where exactly the segfault is happening from the core dumps, but I don't have access to the debugging symbols of the rocm libraries used by the pytorch nightly build. The backtrace, however, could be extracted and de-mangled successfully to reveal the backtrace function names:

```
$ coredumpctl info -1 | c++filt
           PID: 232272 (python)
           UID: 1000 (hkj)
           GID: 1000 (hkj)
        Signal: 11 (SEGV)
     Timestamp: Wed 2026-01-21 17:49:35 EST (7min ago)
  Command Line: venv/bin/python test.py
    Executable: /var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12
 Control Group: /user.slice/user-1000.slice/user@1000.service/user.slice/libpod-61c33ba9015c89c1ee11707007fadc0eec7647318470edf92e19e51a839c9494.scope/container
          Unit: user@1000.service
     User Unit: libpod-61c33ba9015c89c1ee11707007fadc0eec7647318470edf92e19e51a839c9494.scope
         Slice: user-1000.slice
     Owner UID: 1000 (hkj)
       Boot ID: e7e3a8f5c38d48d2ab051ab8a9e21d8e
    Machine ID: 54ef86789777438d8f8097c762a330ce
      Hostname: 61c33ba9015c
       Storage: /var/lib/systemd/coredump/core.python.1000.e7e3a8f5c38d48d2ab051ab8a9e21d8e.232272.1769035775000000.zst (present)
  Size on Disk: 41.3M
       Message: Process 232272 (python) of user 1000 dumped core.

                Module /var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 without build-id.
                Module librocroller.so without build-id.
                Module libmagma.so without build-id.
                Stack trace of thread 1:
                #0  0x00007f9541645a70 rocr::AMD::GpuAgent::ReleaseQueueMainScratch(rocr::AMD::ScratchCache::ScratchInfo&) (libhsa-runtime64.so + 0x45a70)
                #1  0x00007f9541620021 rocr::AMD::GpuAgent::QueueCreate(unsigned long, unsigned int, unsigned long, void (*)(hsa_status_t, hsa_queue_s*, void*), void*, unsigned int, unsigned int, rocr::core::Queue**) [clone .cold] (libhsa-runtime64.so + 0x20021)
                #2  0x00007f9541648add rocr::AMD::GpuAgent::CreateInterceptibleQueue(void (*)(hsa_status_t, hsa_queue_s*, void*), void*, unsigned int) (libhsa-runtime64.so + 0x48add)
                #3  0x00007f9541648b79 std::_Function_handler<rocr::core::Queue* (), rocr::AMD::GpuAgent::InitDma()::{lambda(_HSA_QUEUE_PRIORITY)#1}>::_M_invoke(std::_Any_data const&) (libhsa-runtime64.so + 0x48b79)
                #4  0x00007f954164f475 rocr::AMD::GpuAgent::QueueCreate(unsigned long, unsigned int, unsigned long, void (*)(hsa_status_t, hsa_queue_s*, void*), void*, unsigned int, unsigned int, rocr::core::Queue**) (libhsa-runtime64.so + 0x4f475)
                #5  0x00007f9541664a52 rocr::HSA::hsa_queue_create(hsa_agent_s, unsigned int, unsigned int, void (*)(hsa_status_t, hsa_queue_s*, void*), void*, unsigned int, unsigned int, hsa_queue_s**) (libhsa-runtime64.so + 0x64a52)
                #6  0x00007f96737512b3 roctracer::hsa_support::detail::hsa_queue_create_callback(hsa_agent_s, unsigned int, unsigned int, void (*)(hsa_status_t, hsa_queue_s*, void*), void*, unsigned int, unsigned int, hsa_queue_s**) (libroctracer64.so + 0x132b3)
                #7  0x00007f95d5dd3b72 amd::roc::Device::acquireQueue(unsigned int, bool, std::vector<unsigned int, std::allocator<unsigned int> > const&, amd::CommandQueue::Priority, bool) (libamdhip64.so + 0x3d3b72)
                #8  0x00007f95d5deb7bc amd::roc::VirtualGPU::create() (libamdhip64.so + 0x3eb7bc)
                #9  0x00007f95d5dceabd amd::roc::Device::createVirtualDevice(amd::CommandQueue*) (libamdhip64.so + 0x3ceabd)
                #10 0x00007f95d5db67c0 amd::HostQueue::HostQueue(amd::Context&, amd::Device&, unsigned long, unsigned int, amd::CommandQueue::Priority, std::vector<unsigned int, std::allocator<unsigned int> > const&) (libamdhip64.so + 0x3b67c0)
                #11 0x00007f95d5cd2e08 hip::Stream::Stream(hip::Device*, hip::Stream::Priority, unsigned int, bool, std::vector<unsigned int, std::allocator<unsigned int> > const&, hipStreamCaptureStatus) (libamdhip64.so + 0x2d2e08)
                #12 0x00007f95d5a8be0c hip::Device::NullStream(bool) (libamdhip64.so + 0x8be0c)
                #13 0x00007f95d5bd8985 hip::hipMemcpyWithStream(void*, void const*, unsigned long, hipMemcpyKind, ihipStream_t*) (libamdhip64.so + 0x1d8985)
                #14 0x00007f96416a1412 c10::hip::memcpy_and_sync(void*, void const*, long, hipMemcpyKind, ihipStream_t*) (libtorch_hip.so + 0x14a1412)
                #15 0x00007f96416673e0 at::native::copy_kernel_cuda(at::TensorIterator&, bool) (libtorch_hip.so + 0x14673e0)
                #16 0x00007f965f96a574 at::native::copy_impl(at::Tensor&, at::Tensor const&, bool) [clone .isra.0] (libtorch_cpu.so + 0x1f6a574)
                #17 0x00007f965f96bd8c at::native::copy_(at::Tensor&, at::Tensor const&, bool) (libtorch_cpu.so + 0x1f6bd8c)
                #18 0x00007f96607e73c9 at::_ops::copy_::call(at::Tensor&, at::Tensor const&, bool) (libtorch_cpu.so + 0x2de73c9)
                #19 0x00007f965fce3a79 at::native::_to_copy(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x22e3a79)
                #20 0x00007f9660cccacd c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd___to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x32ccacd)
                #21 0x00007f9660253ca8 at::_ops::_to_copy::redispatch(c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x2853ca8)
                #22 0x00007f9660a243ed c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>), &at::(anonymous namespace)::_to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x30243ed)
                #23 0x00007f9660253ca8 at::_ops::_to_copy::redispatch(c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x2853ca8)
                #24 0x00007f9662b7f157 torch::autograd::VariableType::(anonymous namespace)::_to_copy(c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x517f157)
                #25 0x00007f9662b7f7c0 c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>), &torch::autograd::VariableType::(anonymous namespace)::_to_copy>, at::Tensor, c10::guts::typelist::typelist<c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x517f7c0)
                #26 0x00007f96602faac3 at::_ops::_to_copy::call(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x28faac3)
                #27 0x00007f965fcce497 at::native::to(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x22ce497)
                #28 0x00007f9660e02bb3 c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeImplicitAutograd_dtype_layout_to>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x3402bb3)
                #29 0x00007f96604c39e8 at::_ops::to_dtype_layout::call(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>) (libtorch_cpu.so + 0x2ac39e8)
                #30 0x00007f9673cb3173 torch::autograd::dispatch_to(at::Tensor const&, c10::Device, bool, bool, std::optional<c10::MemoryFormat>) (libtorch_python.so + 0x4b3173)
                #31 0x00007f9673d2a645 torch::autograd::THPVariable_cuda(_object*, _object*, _object*) (libtorch_python.so + 0x52a645)
                #32 0x00000000016425b4 method_vectorcall_VARARGS_KEYWORDS.llvm.13312062049805101343 (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x12435b4)
                #33 0x0000000001615fa6 _PyEval_EvalFrameDefault (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x1216fa6)
                #34 0x0000000001685f22 PyEval_EvalCode (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x1286f22)
                #35 0x00000000016acb82 run_mod.llvm.14141341423068999323 (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x12adb82)
                #36 0x00000000017ba3d3 pyrun_file (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x13bb3d3)
                #37 0x00000000017ba158 _PyRun_SimpleFileObject (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x13bb158)
                #38 0x00000000017ba010 _PyRun_AnyFileObject (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x13bb010)
                #39 0x00000000017b9f4a pymain_run_file_obj (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x13baf4a)
                #40 0x00000000017b9e5e pymain_run_file (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x13bae5e)
                #41 0x000000000174e5bb Py_RunMain (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x134f5bb)
                #42 0x0000000001755aba pymain_main.llvm.8350030150739882507 (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x1356aba)
                #43 0x00000000017558ad main (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x13568ad)
                #44 0x00007f9675cc4635 n/a (libc.so.6 + 0x27635)
                #45 0x00007f9675cc46e9 __libc_start_main (libc.so.6 + 0x276e9)
                #46 0x0000000001797069 _start (/var/home/hkj/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin/python3.12 + 0x1398069)

                Stack trace of thread 2:
                #0  0x00007f9675db374d ioctl (libc.so.6 + 0x11674d)
                #1  0x00007f9541729020 hsakmt_ioctl (libhsa-runtime64.so + 0x129020)
                #2  0x00007f954171fdc3 hsaKmtWaitOnMultipleEvents_Ext (libhsa-runtime64.so + 0x11fdc3)
                #3  0x00007f95416ae799 rocr::core::Signal::WaitAnyExceptions(unsigned int, hsa_signal_s const*, hsa_signal_condition_t const*, long const*, long*) (libhsa-runtime64.so + 0xae799)
                #4  0x00007f954168b648 rocr::core::Runtime::AsyncEventsLoop(void*) (libhsa-runtime64.so + 0x8b648)
                #5  0x00007f95416333cd rocr::os::ThreadTrampoline(void*) (libhsa-runtime64.so + 0x333cd)
                #6  0x00007f9675d3398b n/a (libc.so.6 + 0x9698b)
                #7  0x00007f9675db7a0c n/a (libc.so.6 + 0x11aa0c)
                ELF object binary architecture: AMD x86-64
```
Library versions:
```
$ uv pip list
Using Python 3.12.12 environment at: venv
Package           Version
----------------- --------------------------
filelock          3.20.3
fsspec            2026.1.0
jinja2            3.1.6
markupsafe        3.0.2
mpmath            1.3.0
networkx          3.6.1
setuptools        78.1.0
sympy             1.14.0
torch             2.11.0.dev20260121+rocm7.1
triton-rocm       3.6.0+git9844da95
typing-extensions 4.15.0
```

Anyone who has access to the debugging symbols of the above library should be able to convert the addresses (libhsa-runtime64.so + 0x45a70) back to source code LOC locations by
```
addr2line -e path/to/libhsa-runtime64.so/debug/symbol/file 0x45a70
```

---

### 评论 #5 — lucbruni-amd (2026-01-22T14:59:27Z)

Thanks @wingrunr21 & @chaserhkj for the additional info. I'll look into this.

---

### 评论 #6 — lucbruni-amd (2026-01-28T18:22:45Z)

@chaserhkj, @wingrunr21: this is a known issue, see [here](https://github.com/ROCm/TheRock/issues/2991#issuecomment-3768808325). There are many version incompatibilities with Strix Halo at the moment. You may benefit from the ROCm 7.2 pre-built binaries. See installation instructions for Pytorch [here](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html). Thanks for your patience.

---

### 评论 #7 — wingrunr21 (2026-01-28T19:01:07Z)

ok. vllm right now does not support > 7.0 from either official or AMD sources. llama.cpp is on 7.0 via official channels. The Lemonade-SDK build works with an upgraded kernel though.  

---

### 评论 #8 — lucbruni-amd (2026-01-28T19:08:40Z)

I see. I suppose the alternative would be applying the corresponding kernel patches which I see you've done. We apologize for these inconveniences and this is being actively addressed.

---

### 评论 #9 — wingrunr21 (2026-01-28T19:22:50Z)

The kernel patches are insufficient, yes? you still need rocm7.2 or a build from TheRock to not trigger the segfault (at least, that seems to be the behavior I'm noticing).

---

### 评论 #10 — lucbruni-amd (2026-01-28T19:26:37Z)

The table also mentions ROCm 6.4 which may satisfy your vLLM use case, although the status is unstable.

---

### 评论 #11 — visorcraft (2026-02-15T17:06:36Z)

Still an issue as of February 2026 on Fedora 43 with ROCm 6.4 (Fedora repos) and the kyuz0 `rocm-7rc-rocwmma` distrobox container.

**Hardware:** GMKtec EVO-X2, Ryzen AI Max+ 395, 128 GB LPDDR5X-8000, Fedora 43, kernel 6.18.9

**What works:**
- ROCm 6.4 HIP (Fedora `hipblas-6.4.0`, `hip-runtime-amd-6.4.43484`) — runs llama.cpp llama-bench successfully, pp512=575 t/s, tg128=37.6 t/s on Qwen3-Coder-Next 80B-A3B Q4_K_M
- Vulkan RADV (Mesa) — our primary backend, 42.7 t/s tg128

**What segfaults:**
- kyuz0's `rocm-7rc-rocwmma` container (`docker.io/kyuz0/amd-strix-halo-toolboxes:rocm-7rc-rocwmma`) — segfaults immediately on model load in llama-bench. This is the only container that has a working rocWMMA build for gfx1151 (the WMMA FA kernels compile successfully), but the runtime crashes before any inference can happen.

This blocks the ROCWMMA flash attention path on Strix Halo, which is reportedly the key optimization for large-context performance. We documented the full investigation at https://github.com/visorcraft/strix-halo-llm-perf

---

### 评论 #12 — lucbruni-amd (2026-03-02T21:18:30Z)

@visorcraft, see the following [documentation](https://rocm.docs.amd.com/en/latest/how-to/system-optimization/strixhalo.html#required-kernel-version) which we've added recently. Your use-case seems to fall under the "Generic Distro >= 6.18.4" column. I've pulled the image in question:

```
# cat /opt/rocm-7.0/.info/version
7.9.0
```

This combination in the table is listed as unsupported with your host kernel. You would need a stable and supported combination according to the table to guarantee a way around this - otherwise you can try out some of the other kernel versions warranting an unstable setup with ROCm 7.9.0. I'll leave this issue open for now for discourse.

---
