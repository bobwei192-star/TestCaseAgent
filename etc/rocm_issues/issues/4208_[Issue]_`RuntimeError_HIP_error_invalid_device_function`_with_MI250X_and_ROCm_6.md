# [Issue]: `RuntimeError: HIP error: invalid device function` with MI250X and ROCm 6.2.1

> **Issue #4208**
> **状态**: closed
> **创建时间**: 2024-12-30T16:51:49Z
> **更新时间**: 2025-01-21T14:12:50Z
> **关闭时间**: 2025-01-21T14:12:48Z
> **作者**: segeljakt
> **标签**: Under Investigation, ROCm 6.2.1, 1x AMD Instinct MI250X
> **URL**: https://github.com/ROCm/ROCm/issues/4208

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.1** (颜色: #ededed)
- **1x AMD Instinct MI250X** (颜色: #ededed)

## 描述

### Problem Description

I am trying to use ROCm with Pytorch for model inference and have setup a small Resnet18 script to see if things work. I am running a Singularity container on a single node in a Slurm cluster, where each node is equipped with a MI250X GPU. When running, I get a `RuntimeError: HIP error: invalid device function`:

```
Traceback (most recent call last):
  File "<string>", line 22, in <module>
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 465, in _fn
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torchvision/models/resnet.py", line 285, in forward
    return self._forward_impl(x)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torchvision/models/resnet.py", line 269, in _forward_impl
    x = self.bn1(x)
        ^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/nn/modules/batchnorm.py", line 173, in forward
    self.num_batches_tracked.add_(1)  # type: ignore[has-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

srun: Received task exit notification for 1 task of StepId=8934739.0 (status=0x0100).
srun: error: nid005414: task 0: Exited with exit code 1
srun: Terminating StepId=8934739.0
```

I have tried the proposed solutions in https://github.com/ROCm/ROCm/issues/2536 and export `HSA_OVERRIDE_GFX_VERSION=9.0.10`, but still get the same error. Is there another solution, or some way to debug this error?

### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

AMD EPYC 7742 64-Core Processor

### GPU

1x AMD Instinct MI250X

### ROCm Version

ROCm 6.2.1

### ROCm Component

_No response_

### Steps to Reproduce

This is the script I used for running Pytorch and ROCm:

```
#!/bin/bash
#SBATCH --job-name=AISPECS
#SBATCH --output=results/output%j
#SBATCH --error=results/error%j
#SBATCH --account=project_XXX
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=64G
#SBATCH --partition=standard-g

srun --verbose \
  singularity exec \
  --env PYTORCH_ROCM_ARCH="gfx90a" \
  --bind "./wheelhouse:/opt/wheelhouse" \
  aispecs-docker-eval-amd.sif \
  bash -c "/opt/aispecs-venv/bin/python3 -c \"

import torch
import amdsmi

# Check installation
amdsmi.amdsmi_init()
print('amdsmi:          ', amdsmi.amdsmi_get_processor_handles())
print('CUDA built:      ', torch.backends.cuda.is_built())
print('CUDA available:  ', torch.cuda.is_available())
print('cuDNN enabled:   ', torch.backends.cudnn.enabled)
print('cuDNN available: ', torch.backends.cudnn.is_available())
print('cuDNN version:   ', torch.backends.cudnn.version())
print('Torch Compiler Backends: ', torch.compiler.list_backends())
print('Flash Attention available: ', torch.backends.cuda.flash_sdp_enabled())
import torchvision.models as models
import torch._dynamo
torch._dynamo.config.suppress_errors = True

model = models.resnet18().cuda()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
compiled_model = torch.compile(model, backend='inductor')
x = torch.randn(16, 3, 224, 224).cuda()
optimizer.zero_grad()
out = compiled_model(x)
out.sum().backward()
optimizer.step()
\""
```

I get this stdout-output:

```
amdsmi:           [c_void_p(12949680)]
CUDA built:       True
CUDA available:   True
cuDNN enabled:    True
cuDNN available:  True
cuDNN version:    3002000
Torch Compiler Backends:  ['cudagraphs', 'inductor', 'onnxrt', 'openxla', 'tvm']
Flash Attention available:  True
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
^[[37mROCk module version 6.3.6 is loaded^[[0m
=====================
HSA System Attributes
=====================
Runtime Version:         1.14
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
  Name:                    AMD EPYC 7A53 64-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7A53 64-Core Processor
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
  Max Clock Freq. (MHz):   2000
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
      Size:                    131295136(0x7d367a0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131295136(0x7d367a0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    131295136(0x7d367a0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    AMD EPYC 7A53 64-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7A53 64-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2000
  BDFID:                   0
  Internal Node ID:        1
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
      Size:                    132111288(0x7dfdbb8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132111288(0x7dfdbb8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    132111288(0x7dfdbb8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 3
*******
  Name:                    AMD EPYC 7A53 64-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7A53 64-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    2
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2000
  BDFID:                   0
  Internal Node ID:        2
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
      Size:                    132111292(0x7dfdbbc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132111292(0x7dfdbbc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    132111292(0x7dfdbbc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 4
*******
  Name:                    AMD EPYC 7A53 64-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7A53 64-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    3
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2000
  BDFID:                   0
  Internal Node ID:        3
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
      Size:                    132056244(0x7df04b4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132056244(0x7df04b4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    132056244(0x7df04b4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 5
*******
  Name:                    gfx90a
  Uuid:                    GPU-a543f05567cbe736
  Marketing Name:          AMD Instinct MI250X
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    4
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 29704(0x7408)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1700
  BDFID:                   53504
  Internal Node ID:        4
  Compute Unit:            110
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    TRUE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    2048(0x800)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 78
  SDMA engine uCode::      8
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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

This gist https://gist.github.com/segeljakt/d854cf6cc8f11a8e268d69542167a6f4 contains:
* The output when running with `AMD_SERIALIZE_KERNEL=3`
* The Dockerfile I used to build the wheels for Pytorch:
* The Dockerfile that I later converted to Singularity to run Pytorch with ROCm.

---

## 评论 (19 条)

### 评论 #1 — ppanchad-amd (2024-12-30T18:29:59Z)

Hi @segeljakt. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — tcgu-amd (2024-12-30T21:15:49Z)

Hi @segeljakt, thanks for reaching out! We will try to reproduce this error on our side. Meanwhile, could you please run `export AMD_LOG_LEVEL=4` before running your test and show us the outputs right before the error? Thanks! 

---

### 评论 #3 — tcgu-amd (2024-12-30T21:35:10Z)

A couple other things might be able to help with debugging:
- Would it be possible to try the pre-built wheels instead of custom wheels?
- Might also help to try out a simple torch script first -- does `AMD_LOG_LEVEL=5 python3 -c "import torch; a=torch.randn(3).to('cuda'); print(a)` work?

Thanks!

---

### 评论 #4 — segeljakt (2025-01-02T12:47:01Z)

I tried running `AMD_LOG_LEVEL=5 python3 -c "import torch; a=torch.randn(3).to('cuda'); print(a)`, the output before the error is:

```
...
:1:hip_fatbin.cpp           :117 : 8802962845 us: [pid:19349 tid:0x14dec9d33080] Missing CO for these ISAs - 
:1:hip_fatbin.cpp           :120 : 8802962848 us: [pid:19349 tid:0x14dec9d33080]      amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
:3:hip_platform.cpp         :715 : 8802962852 us: [pid:19349 tid:0x14dec9d33080] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
:1:hip_fatbin.cpp           :276 : 8803012584 us: [pid:19349 tid:0x14dec9d33080] Cannot find CO in the bundle /opt/rocm-6.2.1/lib/libMIOpen.so.1.0.60201 for ISA: amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
:1:hip_fatbin.cpp           :117 : 8803012597 us: [pid:19349 tid:0x14dec9d33080] Missing CO for these ISAs - 
:1:hip_fatbin.cpp           :120 : 8803012602 us: [pid:19349 tid:0x14dec9d33080]      amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
:3:hip_platform.cpp         :715 : 8803012609 us: [pid:19349 tid:0x14dec9d33080] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
:1:hip_fatbin.cpp           :276 : 8803043953 us: [pid:19349 tid:0x14dec9d33080] Cannot find CO in the bundle /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_hip.so for ISA: amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
:1:hip_fatbin.cpp           :117 : 8803043959 us: [pid:19349 tid:0x14dec9d33080] Missing CO for these ISAs - 
:1:hip_fatbin.cpp           :120 : 8803043961 us: [pid:19349 tid:0x14dec9d33080]      amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
:3:hip_platform.cpp         :715 : 8803043965 us: [pid:19349 tid:0x14dec9d33080] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
:3:hip_device_runtime.cpp   :651 : 8803083943 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDeviceCount ( 0x7ffe02542c60 ) [0m
:3:hip_device_runtime.cpp   :653 : 8803083951 us: [pid:19349 tid:0x14dec9d33080] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :651 : 8803083978 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDeviceCount ( 0x7ffe02542c98 ) [0m
:3:hip_device_runtime.cpp   :653 : 8803083981 us: [pid:19349 tid:0x14dec9d33080] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803083992 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe0254288c ) [0m
:3:hip_device_runtime.cpp   :644 : 8803083994 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :651 : 8803084004 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDeviceCount ( 0x7ffe025427d4 ) [0m
:3:hip_device_runtime.cpp   :653 : 8803084007 us: [pid:19349 tid:0x14dec9d33080] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_context.cpp          :342 : 8803084882 us: [pid:19349 tid:0x14dec9d33080] [32m hipDevicePrimaryCtxGetState ( 0, 0x7ffe02542888, 0x7ffe0254288c ) [0m
:3:hip_context.cpp          :356 : 8803084890 us: [pid:19349 tid:0x14dec9d33080] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803084896 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe025428ac ) [0m
:3:hip_device_runtime.cpp   :644 : 8803084899 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_context.cpp          :342 : 8803084902 us: [pid:19349 tid:0x14dec9d33080] [32m hipDevicePrimaryCtxGetState ( 0, 0x7ffe025428a8, 0x7ffe025428ac ) [0m
:3:hip_context.cpp          :356 : 8803084906 us: [pid:19349 tid:0x14dec9d33080] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803084912 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe0254284c ) [0m
:3:hip_device_runtime.cpp   :644 : 8803084915 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_context.cpp          :342 : 8803084918 us: [pid:19349 tid:0x14dec9d33080] [32m hipDevicePrimaryCtxGetState ( 0, 0x7ffe02542848, 0x7ffe0254284c ) [0m
:3:hip_context.cpp          :356 : 8803084921 us: [pid:19349 tid:0x14dec9d33080] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803100009 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02542f44 ) [0m
:3:hip_device_runtime.cpp   :644 : 8803100016 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803100072 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02542144 ) [0m
:3:hip_device_runtime.cpp   :644 : 8803100075 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803100079 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02542024 ) [0m
:3:hip_device_runtime.cpp   :644 : 8803100081 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803100093 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02541ddc ) [0m
:3:hip_device_runtime.cpp   :644 : 8803100095 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_stream.cpp           :293 : 8803100102 us: [pid:19349 tid:0x14dec9d33080] [32m hipDeviceGetStreamPriorityRange ( 0x7ffe02541d88, 0x7ffe02541d8c ) [0m
:3:hip_stream.cpp           :301 : 8803100106 us: [pid:19349 tid:0x14dec9d33080] hipDeviceGetStreamPriorityRange: Returned hipSuccess : 
:3:hip_error.cpp            :36  : 8803100117 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetLastError (  ) [0m
:3:hip_device_runtime.cpp   :636 : 8803100123 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe025416ec ) [0m
:3:hip_device_runtime.cpp   :644 : 8803100125 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_graph.cpp            :866 : 8803100133 us: [pid:19349 tid:0x14dec9d33080] [32m hipStreamIsCapturing ( stream:<null>, 0x7ffe02541958 ) [0m
:3:hip_graph.cpp            :867 : 8803100137 us: [pid:19349 tid:0x14dec9d33080] hipStreamIsCapturing: Returned hipSuccess : 
:3:hip_memory.cpp           :615 : 8803100149 us: [pid:19349 tid:0x14dec9d33080] [32m hipMalloc ( 0x7ffe02541950, 2097152 ) [0m
:4:rocdevice.cpp            :2379: 8803100465 us: [pid:19349 tid:0x14dec9d33080] Allocate hsa device memory 0x14dc00200000, size 0x200000
:3:rocdevice.cpp            :2418: 8803100471 us: [pid:19349 tid:0x14dec9d33080] Device=0x7bda130, freeMem_ = 0xffee00000
:3:hip_memory.cpp           :617 : 8803100475 us: [pid:19349 tid:0x14dec9d33080] hipMalloc: Returned hipSuccess : 0x14dc00200000: duration: 326 us
:3:hip_device_runtime.cpp   :666 : 8803100489 us: [pid:19349 tid:0x14dec9d33080] [32m hipSetDevice ( 0 ) [0m
:3:hip_device_runtime.cpp   :670 : 8803100492 us: [pid:19349 tid:0x14dec9d33080] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :666 : 8803100495 us: [pid:19349 tid:0x14dec9d33080] [32m hipSetDevice ( 0 ) [0m
:3:hip_device_runtime.cpp   :670 : 8803100497 us: [pid:19349 tid:0x14dec9d33080] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803139293 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02542044 ) [0m
:3:hip_device_runtime.cpp   :644 : 8803139303 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8803139311 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02541e5c ) [0m
:3:hip_device_runtime.cpp   :644 : 8803139316 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :701 : 8803139344 us: [pid:19349 tid:0x14dec9d33080] [32m hipMemcpyWithStream ( 0x14dc00200000, 0x3ae1000, 12, hipMemcpyHostToDevice, stream:<null> ) [0m
:3:rocdevice.cpp            :3026: 8803146899 us: [pid:19349 tid:0x14dec9d33080] Number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:3:rocdevice.cpp            :3104: 8803163569 us: [pid:19349 tid:0x14dec9d33080] Created SWq=0x14dd04c94000 to map on HWq=0x14dbfb600000 with size 16384 with priority 1, cooperative: 0
:3:rocdevice.cpp            :3197: 8803163584 us: [pid:19349 tid:0x14dec9d33080] acquireQueue refCount: 0x14dbfb600000 (1)
:4:rocdevice.cpp            :2221: 8803163926 us: [pid:19349 tid:0x14dec9d33080] Allocate hsa host memory 0x14dbfb400000, size 0x100000, numa_node = 0
:3:devprogram.cpp           :2648: 8805702314 us: [pid:19349 tid:0x14dec9d33080] Using Code Object V5.
:4:command.cpp              :347 : 8805703504 us: [pid:19349 tid:0x14dec9d33080] Command (CopyHostToDevice) enqueued: 0x7f693a0
:4:rocblit.cpp              :832 : 8805703954 us: [pid:19349 tid:0x14dec9d33080] HSA Async Copy staged H2D dst=0x14dc00200000, src=0x14dc00800000, size=12, completion_signal=0x14dd011ff700
:4:rocvirtual.cpp           :571 : 8805703960 us: [pid:19349 tid:0x14dec9d33080] Host wait on completion_signal=0x14dd011ff700
:3:rocvirtual.hpp           :66  : 8805703963 us: [pid:19349 tid:0x14dec9d33080] Host active wait for Signal = (0x14dd011ff700) for -1 ns
:4:command.cpp              :287 : 8805703969 us: [pid:19349 tid:0x14dec9d33080] Queue marker to command queue: 0x76ca820
:4:command.cpp              :347 : 8805703971 us: [pid:19349 tid:0x14dec9d33080] Command (InternalMarker) enqueued: 0x88802e0
:4:command.cpp              :177 : 8805703974 us: [pid:19349 tid:0x14dec9d33080] Command 0x7f693a0 complete
:4:command.cpp              :171 : 8805703977 us: [pid:19349 tid:0x14dec9d33080] Command 0x88802e0 complete (Wall: 8805703976, CPU: 0, GPU: 0 us)
:4:command.cpp              :251 : 8805703980 us: [pid:19349 tid:0x14dec9d33080] Waiting for event 0x7f693a0 to complete, current status 0
:4:command.cpp              :266 : 8805703983 us: [pid:19349 tid:0x14dec9d33080] Event 0x7f693a0 wait completed
:3:hip_memory.cpp           :712 : 8805703987 us: [pid:19349 tid:0x14dec9d33080] hipMemcpyWithStream: Returned hipSuccess : : duration: 2564643 us
:3:hip_device_runtime.cpp   :666 : 8805703996 us: [pid:19349 tid:0x14dec9d33080] [32m hipSetDevice ( 0 ) [0m
:3:hip_device_runtime.cpp   :670 : 8805703999 us: [pid:19349 tid:0x14dec9d33080] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8805714220 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe025421d4 ) [0m
:3:hip_device_runtime.cpp   :644 : 8805714227 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8805714233 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe025420e4 ) [0m
:3:hip_device_runtime.cpp   :644 : 8805714235 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8805714241 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02541d1c ) [0m
:3:hip_device_runtime.cpp   :644 : 8805714243 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :666 : 8805714248 us: [pid:19349 tid:0x14dec9d33080] [32m hipSetDevice ( 0 ) [0m
:3:hip_device_runtime.cpp   :670 : 8805714251 us: [pid:19349 tid:0x14dec9d33080] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :666 : 8805714254 us: [pid:19349 tid:0x14dec9d33080] [32m hipSetDevice ( 0 ) [0m
:3:hip_device_runtime.cpp   :670 : 8805714256 us: [pid:19349 tid:0x14dec9d33080] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8805726264 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02542434 ) [0m
:3:hip_device_runtime.cpp   :644 : 8805726269 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8805779838 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02541ae0 ) [0m
:3:hip_device_runtime.cpp   :644 : 8805779848 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8805779855 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe025417dc ) [0m
:3:hip_device_runtime.cpp   :644 : 8805779859 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :666 : 8805779876 us: [pid:19349 tid:0x14dec9d33080] [32m hipSetDevice ( 0 ) [0m
:3:hip_device_runtime.cpp   :670 : 8805779880 us: [pid:19349 tid:0x14dec9d33080] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :636 : 8805779899 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetDevice ( 0x7ffe02541b7c ) [0m
:3:hip_device_runtime.cpp   :644 : 8805779903 us: [pid:19349 tid:0x14dec9d33080] hipGetDevice: Returned hipSuccess : 
:3:hip_platform.cpp         :225 : 8805779914 us: [pid:19349 tid:0x14dec9d33080] [32m __hipPushCallConfiguration ( {1,1,1}, {256,1,1}, 0, stream:<null> ) [0m
:3:hip_platform.cpp         :229 : 8805779921 us: [pid:19349 tid:0x14dec9d33080] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :234 : 8805779933 us: [pid:19349 tid:0x14dec9d33080] [32m __hipPopCallConfiguration ( {0,0,1}, {3156237404,5342,1}, 0x7ffe02541de8, 0x7ffe02541dd8 ) [0m
:3:hip_platform.cpp         :243 : 8805779939 us: [pid:19349 tid:0x14dec9d33080] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :677 : 8805779959 us: [pid:19349 tid:0x14dec9d33080] [32m hipLaunchKernel ( 0x14debac11408, {1,1,1}, {256,1,1}, 0x7ffe02541e00, 0, stream:<null> ) [0m
:3:hip_module.cpp           :678 : 8805779969 us: [pid:19349 tid:0x14dec9d33080] hipLaunchKernel: Returned hipErrorInvalidDeviceFunction : 
:3:hip_error.cpp            :36  : 8805779975 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetLastError (  ) [0m
:3:hip_error.cpp            :36  : 8805779980 us: [pid:19349 tid:0x14dec9d33080] [32m hipGetLastError (  ) [0m
:3:hip_device_runtime.cpp   :666 : 8806102235 us: [pid:19349 tid:0x14dec9d33080] [32m hipSetDevice ( 0 ) [0m
:3:hip_device_runtime.cpp   :670 : 8806102244 us: [pid:19349 tid:0x14dec9d33080] hipSetDevice: Returned hipSuccess : 
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor.py", line 523, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 708, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 625, in _str_intern
    tensor_str = _tensor_str(self, indent)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 357, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 146, in __init__
    tensor_view, torch.isfinite(tensor_view) & tensor_view.ne(0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

It looks like I get `Missing CO for these ISAs` and `init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules`.

The complete output is here: https://gist.github.com/segeljakt/086784abd89201730aaab4437663e938.

My project requires compiling most software packages from source, but I will see if the prebuilt packages work.

---

### 评论 #5 — tcgu-amd (2025-01-02T17:04:41Z)

@segeljakt Thanks for the update! Based on your output, I suspect there might be a library linkage issue. I am not sure about the content of the .sif file that was used to run the container on singularity, but if the --rocm flag was used to run singularity, then one possibility might be how singularity sets up the container. Based on [their docs](https://docs.sylabs.io/guides/3.5/user-guide/gpu.html#amd-gpus-rocm), it seems singularity will:

- Locate and bind the basic ROCm libraries from the host into the container, so that they are available to the container, and match the kernel GPU driver on the host.

- Set the LD_LIBRARY_PATH inside the container so that the bound-in version of the ROCm libraries are used by application run inside the container.

I would check to see if `libamdhip64.so` inside the torch lib folder (usually found at `./env/lib/python3.x/site-packages/torch/lib/`) in your container is a symbolic link pointing to `/opt/rocm/lib/libamdhip64.so`. If it is, then I would try to make sure singularity does not replace the libraries under /opt/rocm/lib. If that is not possible, I would try to replace the symbolic links under the torch lib folder with actual copies of the libraries as a step in the container build process. This is just to make sure that torch is using the libraries it was built with. 

I will continue to investigate on my end in the meantime. Hope this helps!

Thanks!  

---

### 评论 #6 — segeljakt (2025-01-03T13:19:55Z)

Thank you for the response. So far I have been running Singularity without the `--rocm` flag. When running it with the `--rocm` flag. I have debugged a bit and it looks like `LD_LIBRARY_PATH` was not set. Also, `./env/lib/python3.12/site-packages/torch/lib/libamdhip64.so` did not exist. I am currently rebuilding and will let you know what happens. Strangely the image worked before I converted it from Docker to Singularity. Maybe something in the conversion caused the error.

---

### 评论 #7 — tcgu-amd (2025-01-03T14:49:44Z)

Thanks for the update! Sorry for the confusion, I should probably clarify that that `./env` path would be the folder to the virtual environment, in your case it should be `/opt/aispecs-venv`. If you still cannot find `libamdhip64.so` in `/opt/aispecs-venv/python3.12/site-packages/torch/lib/libamdhip64.so`, I would check in `ldd /opt/aispecs-venv/lib/python3.12/site-packages/torch/_C.cpython-312-x86_64-linux-gnu.so |  grep hip`, and see if the `libamdhip64.so` or a similar file is in the outputs.

> So far I have been running Singularity without the --rocm flag. Strangely the image worked before I converted it from Docker to Singularity. Maybe something in the conversion caused the error.

Got it. In this case I would double check to see if `/dev/dri` and `/dev/kfd` are properly mapped. You can refer to the docker command in our [PyTorch Docker docs](https://rocm.docs.amd.com/projects/install-on-linux/en/develop/install/3rd-party/pytorch-install.html) for reference. 

>I have debugged a bit and it looks like LD_LIBRARY_PATH was not set

That should be okay. However, it might help to ensure proper library linkage. You can try to follow our [ROCm Post Installation Instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/post-install.html) to configuring linkage. 

> I am currently rebuilding and will let you know what happens.

Sounds great! Thanks! 

---

### 评论 #8 — tcgu-amd (2025-01-13T19:56:54Z)

Hi @segeljakt, just wondering if there has been any updates? Thanks! 

---

### 评论 #9 — segeljakt (2025-01-15T13:42:45Z)

Hi, sorry for the late response.

> If you still cannot find libamdhip64.so in /opt/aispecs-venv/python3.12/site-packages/torch/lib/libamdhip64.so, I would check in ldd /opt/aispecs-venv/lib/python3.12/site-packages/torch/_C.cpython-312-x86_64-linux-gnu.so |  grep hip, and see if the libamdhip64.so or a similar file is in the outputs.

I checked the image for the files, and they seem to be present:

```sh
$ singularity build --sandbox sandbox_dir image.sif
$ singularity shell --writable sandbox_dir
Singularity> ldd /opt/aispecs-venv/lib/python3.12/site-packages/torch/_C.cpython-312-x86_64-linux-gnu.so |  grep hip
	libtorch_hip.so => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_hip.so (0x00007f38f74c2000)
	libc10_hip.so => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libc10_hip.so (0x00007f38f7384000)
	libamdhip64.so.6 => /opt/rocm-6.2.1/lib/libamdhip64.so.6 (0x00007f389fc91000)
	libhiprtc.so.6 => /opt/rocm-6.2.1/lib/libhiprtc.so.6 (0x00007f389f4a2000)
	libhipblaslt.so.0 => /opt/rocm-6.2.1/lib/libhipblaslt.so.0 (0x00007f389ece1000)
	libhipblas.so.2 => /opt/rocm-6.2.1/lib/libhipblas.so.2 (0x00007f389ebc6000)
	libhipfft.so.0 => /opt/rocm-6.2.1/lib/libhipfft.so.0 (0x00007f389ebb3000)
	libhiprand.so.1 => /opt/rocm-6.2.1/lib/libhiprand.so.1 (0x00007f389ebad000)
	libhipsparse.so.1 => /opt/rocm-6.2.1/lib/libhipsparse.so.1 (0x00007f389eb70000)
	libhipsolver.so.0 => /opt/rocm-6.2.1/lib/libhipsolver.so.0 (0x00007f389eb2c000)
```

Just to be sure, I tried to create the symbolic link manually:

```
Singularity> ln -s /opt/rocm-6.2.1/lib/libamdhip64.so /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libamdhip64.so
Singularity> exit
$ singularity build new_image.sif sandbox_dir
```

Then, I tried to run again, but I got errors like this:

```sh
:1:hip_fatbin.cpp           :276 : 4225160549692 us: [pid:53107 tid:0x14aadb53f080] Cannot find CO in the bundle /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_hip.so for ISA: amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
:1:hip_fatbin.cpp           :117 : 4225160549705 us: [pid:53107 tid:0x14aadb53f080] Missing CO for these ISAs -
:1:hip_fatbin.cpp           :120 : 4225160549709 us: [pid:53107 tid:0x14aadb53f080]      amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
:3:hip_platform.cpp         :715 : 4225160549715 us: [pid:53107 tid:0x14aadb53f080] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
```

> Got it. In this case I would double check to see if /dev/dri and /dev/kfd are properly mapped. You can refer to the docker command in our [PyTorch Docker docs](https://rocm.docs.amd.com/projects/install-on-linux/en/develop/install/3rd-party/pytorch-install.html) for reference.

I tried to run Singularity with `singularity exec --bind=/dev/kfd --bind=/dev/dri new_image.sif`, but then got a message that there are no available HIP GPUs:

```
:3:hip_error.cpp            :36  : 4225965443347 us: [pid:74171 tid:0x148146f97300] hipGetLastError: Returned hipErrorNoDevice :
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 319, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No HIP GPUs are available
```

I think the GPU access is somehow handled by the HPC cluster, since the GPUs are not directly accessible by the host.

I also tried to run without Singularity, but I failed due to a mismatch in glibc versions. The host has version 2.31 but 2.34 appears to be required for ROCM 6.2.1. I will try to investigate some more into alternative solutions.

---

### 评论 #10 — tcgu-amd (2025-01-15T15:05:45Z)

> I checked the image for the files, and they seem to be present:
> 
> $ singularity build --sandbox sandbox_dir image.sif
> $ singularity shell --writable sandbox_dir
> Singularity> ldd /opt/aispecs-venv/lib/python3.12/site-packages/torch/_C.cpython-312-x86_64-linux-gnu.so |  grep hip
> 	libtorch_hip.so => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_hip.so (0x00007f38f74c2000)
> 	libc10_hip.so => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libc10_hip.so (0x00007f38f7384000)
> 	libamdhip64.so.6 => /opt/rocm-6.2.1/lib/libamdhip64.so.6 (0x00007f389fc91000)
> 	libhiprtc.so.6 => /opt/rocm-6.2.1/lib/libhiprtc.so.6 (0x00007f389f4a2000)
> 	libhipblaslt.so.0 => /opt/rocm-6.2.1/lib/libhipblaslt.so.0 (0x00007f389ece1000)
> 	libhipblas.so.2 => /opt/rocm-6.2.1/lib/libhipblas.so.2 (0x00007f389ebc6000)
> 	libhipfft.so.0 => /opt/rocm-6.2.1/lib/libhipfft.so.0 (0x00007f389ebb3000)
> 	libhiprand.so.1 => /opt/rocm-6.2.1/lib/libhiprand.so.1 (0x00007f389ebad000)
> 	libhipsparse.so.1 => /opt/rocm-6.2.1/lib/libhipsparse.so.1 (0x00007f389eb70000)
> 	libhipsolver.so.0 => /opt/rocm-6.2.1/lib/libhipsolver.so.0 (0x00007f389eb2c000)

This makes sense. Since you compiled torch from ground up, these libraries are symbolic links against the shared libraries under /opt/rocm. The problem with this is that if by chance any of the system libraries get replaced (for example, by singularity), Pytroch will break. 

I am wondering if you could replace these libraries with hard copies in the build process? This would be similar to how the pre-built Pytorch wheels are packaged. This way, torch won't be dependent on the system library versions. 

> Then, I tried to run again, but I got errors like this:
> 
> :1:hip_fatbin.cpp           :276 : 4225160549692 us: [pid:53107 tid:0x14aadb53f080] Cannot find CO in the bundle /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_hip.so for ISA: amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
> :1:hip_fatbin.cpp           :117 : 4225160549705 us: [pid:53107 tid:0x14aadb53f080] Missing CO for these ISAs -
> :1:hip_fatbin.cpp           :120 : 4225160549709 us: [pid:53107 tid:0x14aadb53f080]      amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
> :3:hip_platform.cpp         :715 : 42251

> 60549715 us: [pid:53107 tid:0x14aadb53f080] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules

Is this the end of the log? Because the missing CO warnings are actually quite common and sometimes can be ignored. Generally, the  breaking error would be presented by the end of the log.

> I tried to run Singularity with singularity exec --bind=/dev/kfd --bind=/dev/dri new_image.sif, but then got a message that there are no available HIP GPUs:
> 
> :3:hip_error.cpp            :36  : 4225965443347 us: [pid:74171 tid:0x148146f97300] hipGetLastError: Returned hipErrorNoDevice :
> Traceback (most recent call last):
>   File "<string>", line 1, in <module>
>   File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 319, in _lazy_init
>     torch._C._cuda_init()
> RuntimeError: No HIP GPUs are available
> I think the GPU access is somehow handled by the HPC cluster, since the GPUs are not directly accessible by the host.

This is very interesting. So it was originally working on Singularity without any additional commands, but when you tried to manually bind devices it stopped working. I think this confirms that Singularity was doing something automatically under the hood  specifically for ROCm, which might be what is causing the issue.

> I also tried to run without Singularity, but I failed due to a mismatch in glibc versions. The host has version 2.31 but 2.34 appears to be required for ROCM 6.2.1. I will try to investigate some more into alternative solutions.

Sounds good. Thanks!


---

### 评论 #11 — segeljakt (2025-01-15T15:49:22Z)

> Is this the end of the log? Because the missing CO warnings are actually quite common and sometimes can be ignored. Generally, the breaking error would be presented by the end of the log.

Oops, sorry, I forgot to scroll down. Eventually I get this:

```
...

:3:hip_module.cpp           :678 : 795019406319 us: [pid:3785  tid:0x1546faa1c080] hipLaunchKernel: Returned hipErrorInvalidDeviceFunction :
:3:hip_error.cpp            :36  : 795019406322 us: [pid:3785  tid:0x1546faa1c080] ^[[32m hipGetLastError (  ) ^[[0m
:3:hip_error.cpp            :36  : 795019406325 us: [pid:3785  tid:0x1546faa1c080] ^[[32m hipGetLastError (  ) ^[[0m
:3:hip_device_runtime.cpp   :666 : 795019737313 us: [pid:3785  tid:0x1546faa1c080] ^[[32m hipSetDevice ( 0 ) ^[[0m
:3:hip_device_runtime.cpp   :670 : 795019737325 us: [pid:3785  tid:0x1546faa1c080] hipSetDevice: Returned hipSuccess :
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor.py", line 523, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 708, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 625, in _str_intern
    tensor_str = _tensor_str(self, indent)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 357, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 146, in __init__
    tensor_view, torch.isfinite(tensor_view) & tensor_view.ne(0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
:3:hip_device_runtime.cpp   :620 : 795019938111 us: [pid:3785  tid:0x1546faa1c080] ^[[32m hipDeviceSynchronize (  ) ^[[0m
:4:commandqueue.cpp         :147 : 795019938128 us: [pid:3785  tid:0x1546faa1c080] HW Event not ready, awaiting completion instead
:4:commandqueue.cpp         :163 : 795019938135 us: [pid:3785  tid:0x1546faa1c080] All commands finished
:3:hip_device_runtime.cpp   :624 : 795019938141 us: [pid:3785  tid:0x1546faa1c080] hipDeviceSynchronize: Returned hipSuccess :
:3:hip_device_runtime.cpp   :620 : 795019939958 us: [pid:3785  tid:0x1546faa1c080] ^[[32m hipDeviceSynchronize (  ) ^[[0m

...

:3:hip_device_runtime.cpp   :620 : 795020310218 us: [pid:3785  tid:0x1546faa1c080] ^[[32m hipDeviceSynchronize (  ) ^[[0m
:3:hip_device_runtime.cpp   :624 : 795020310220 us: [pid:3785  tid:0x1546faa1c080] hipDeviceSynchronize: Returned hipSuccess :
:1:hip_fatbin.cpp           :91  : 795020310225 us: [pid:3785  tid:0x1546faa1c080] All Unique FDs are closed
:4:command.cpp              :347 : 795020310308 us: [pid:3785  tid:0x1546faa1c080] Command (Marker) enqueued: 0x709c200
:3:rocvirtual.cpp           :475 : 795020310323 us: [pid:3785  tid:0x1546faa1c080] Set Handler: handle(0x154531dff680), timestamp(0x886ab90)
:4:rocvirtual.cpp           :1076: 795020310577 us: [pid:3785  tid:0x1546faa1c080] SWq=0x154535a96000, HWq=0x154430400000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x154531dff680
:4:command.cpp              :251 : 795020310583 us: [pid:3785  tid:0x1546faa1c080] Waiting for event 0x709c200 to complete, current status 2
:3:rocvirtual.cpp           :222 : 795020310650 us: [pid:3785  tid:0x1544307ff6c0] Handler: value(0), timestamp(0x7099890), handle(0x154531dff680)
:4:command.cpp              :171 : 795020310657 us: [pid:3785  tid:0x1544307ff6c0] Command 0x709c200 complete (Wall: 795020310656, CPU: 0, GPU: 343 us)
:4:command.cpp              :266 : 795020310657 us: [pid:3785  tid:0x1546faa1c080] Event 0x709c200 wait completed
:4:rocdevice.cpp            :2395: 795020310856 us: [pid:3785  tid:0x1546faa1c080] Free hsa memory 0x154430200000
:4:rocdevice.cpp            :2395: 795020310862 us: [pid:3785  tid:0x1546faa1c080] Free hsa memory (nil)
:3:rocdevice.cpp            :3209: 795020310866 us: [pid:3785  tid:0x1546faa1c080] releaseQueue refCount:0x154430400000 (0)
:4:runtime.cpp              :93  : 795020310885 us: [pid:3785  tid:0x1546faa1c080] tearDown
:4:rocdevice.cpp            :2395: 795020311185 us: [pid:3785  tid:0x1546faa1c080] Free hsa memory 0x154430c00000
:4:rocdevice.cpp            :2395: 795020311212 us: [pid:3785  tid:0x1546faa1c080] Free hsa memory 0x154538596000
:3:rocdevice.cpp            :285 : 795020311217 us: [pid:3785  tid:0x1546faa1c080] Deleting hardware queue 0x154430400000 with refCount 0
:4:rocdevice.cpp            :2395: 795020316259 us: [pid:3785  tid:0x1546faa1c080] Free hsa memory 0x154431200000
:4:rocdevice.cpp            :2395: 795020316331 us: [pid:3785  tid:0x1546faa1c080] Free hsa memory 0x154431400000
srun: Received task exit notification for 1 task of StepId=9127631.0 (status=0x0100).
srun: error: nid005142: task 0: Exited with exit code 1
srun: Terminating StepId=9127631.0
```

> This makes sense. Since you compiled torch from ground up, these libraries are symbolic links against the shared libraries under /opt/rocm. The problem with this is that if by chance any of the system libraries get replaced (for example, by singularity), Pytroch will break.

> I am wondering if you could replace these libraries with hard copies in the build process? This would be similar to how the pre-built Pytorch wheels are packaged. This way, torch won't be dependent on the system library versions.

Hmm ok, I will take a look.

---

### 评论 #12 — segeljakt (2025-01-16T10:10:55Z)

Hmm, I tried to make hard copies for the shared libraries. It now looks like this:

```
Singularity> ldd /opt/aispecs-venv/lib/python3.12/site-packages/torch/_C.cpython-312-x86_64-linux-gnu.so
	linux-vdso.so.1 (0x00007ffc7bff9000)
	libtorch_python.so           => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_python.so (0x00007f7c20200000)
	libtorch.so                  => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch.so (0x00007f7c21664000)
	libshm.so                    => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libshm.so (0x00007f7c2165a000)
	libroctx64.so.4              => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libroctx64.so.4 (0x00007f7c21655000)
	libtorch_cpu.so              => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_cpu.so (0x00007f7c12c00000)
	libtorch_hip.so              => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libtorch_hip.so (0x00007f7c07800000)
	libc10_hip.so                => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libc10_hip.so (0x00007f7c076c2000)
	libMIOpen.so.1               => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libMIOpen.so.1 (0x00007f7bb1600000)
	libamdhip64.so.6             => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libamdhip64.so.6 (0x00007f7bafe00000)
	libc10.so                    => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libc10.so (0x00007f7bb1504000)
	libstdc++.so.6               => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f7bafa00000)
	libgcc_s.so.1                => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f7c21619000)
	libc.so.6                    => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7baf600000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f7c21670000)
	libm.so.6                    => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f7bafd17000)
	libgomp.so.1                 => /lib/x86_64-linux-gnu/libgomp.so.1 (0x00007f7c215c1000)
	libhiprtc.so.6               => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhiprtc.so.6 (0x00007f7baf918000)
	libhipblaslt.so.0            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhipblaslt.so.0 (0x00007f7baee00000)
	libhipblas.so.2              => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhipblas.so.2 (0x00007f7baece5000)
	libhipfft.so.0               => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhipfft.so.0 (0x00007f7c215ae000)
	libhiprand.so.1              => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhiprand.so.1 (0x00007f7c215a6000)
	libhipsparse.so.1            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhipsparse.so.1 (0x00007f7c201c3000)
	libhipsolver.so.0            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhipsolver.so.0 (0x00007f7c12bbe000)
	libaotriton_v2.so            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libaotriton_v2.so (0x00007f7bac400000)
	librccl.so.1                 => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librccl.so.1 (0x00007f7b72600000)
	libzstd.so.1                 => /lib/x86_64-linux-gnu/libzstd.so.1 (0x00007f7bb144a000)
	libamd_comgr.so.2            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libamd_comgr.so.2 (0x00007f7b69a00000)
	librocm-core.so.1            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocm-core.so.1 (0x00007f7c201be000)
	librocblas.so.4              => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocblas.so.4 (0x00007f7b27000000)
	librocprofiler-register.so.0 => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocprofiler-register.so.0 (0x00007f7c12b39000)
	libhsa-runtime64.so.1        => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/libhsa-runtime64.so.1 (0x00007f7b26c00000)
	libnuma.so.1                 => /lib/x86_64-linux-gnu/libnuma.so.1 (0x00007f7c12b2b000)
	librocsolver.so.0            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocsolver.so.0 (0x00007f7abf600000)
	librocfft.so.0               => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocfft.so.0 (0x00007f7abec00000)
	librocrand.so.1              => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocrand.so.1 (0x00007f7ab5800000)
	librocsparse.so.1            => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocsparse.so.1 (0x00007f7a5fa00000)
	libsuitesparseconfig.so.7    => /lib/x86_64-linux-gnu/libsuitesparseconfig.so.7 (0x00007f7c12b26000)
	libcholmod.so.5              => /lib/x86_64-linux-gnu/libcholmod.so.5 (0x00007f7ab5641000)
	librocm_smi64.so.7           => /opt/aispecs-venv/lib/python3.12/site-packages/torch/lib/librocm_smi64.so.7 (0x00007f7b724ca000)
	libz.so.1                    => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f7bafcfb000)
	libtinfo.so.6                => /lib/x86_64-linux-gnu/libtinfo.so.6 (0x00007f7bafcc7000)
	libelf.so.1                  => /lib/x86_64-linux-gnu/libelf.so.1 (0x00007f7bafca9000)
	libdrm.so.2                  => /opt/amdgpu/lib/x86_64-linux-gnu/libdrm.so.2 (0x00007f7bafc90000)
	libdrm_amdgpu.so.1           => /opt/amdgpu/lib/x86_64-linux-gnu/libdrm_amdgpu.so.1 (0x00007f7bafc81000)
	libamd.so.3                  => /lib/x86_64-linux-gnu/libamd.so.3 (0x00007f7c076b5000)
	libcolamd.so.3               => /lib/x86_64-linux-gnu/libcolamd.so.3 (0x00007f7bb1441000)
	libcamd.so.3                 => /lib/x86_64-linux-gnu/libcamd.so.3 (0x00007f7baf90d000)
	libccolamd.so.3              => /lib/x86_64-linux-gnu/libccolamd.so.3 (0x00007f7baf901000)
	liblapack.so.3               => /lib/x86_64-linux-gnu/liblapack.so.3 (0x00007f7a5f200000)
	libblas.so.3                 => /lib/x86_64-linux-gnu/libblas.so.3 (0x00007f7baf85a000)
	libgfortran.so.5             => /lib/x86_64-linux-gnu/libgfortran.so.5 (0x00007f7a5ee00000)
```

I bundled everything except what was under `/lib/x86_64-linux-gnu/` and `/opt/amdgpu/lib/x86_64-linux-gnu/`. It appears however that I still get the same error:


```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor.py", line 523, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 708, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 625, in _str_intern
    tensor_str = _tensor_str(self, indent)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 357, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 146, in __init__
    tensor_view, torch.isfinite(tensor_view) & tensor_view.ne(0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

I will try to bundle the rest of the libraries and see what happens.

---

### 评论 #13 — segeljakt (2025-01-16T11:08:36Z)

> This is very interesting. So it was originally working on Singularity without any additional commands, but when you tried to manually bind devices it stopped working. I think this confirms that Singularity was doing something automatically under the hood specifically for ROCm, which might be what is causing the issue.

Hmm, I think it could also be Slurm doing something. Slurm provides the GPUs to the host, and then the host runs Singularity. For example, with:

```
$ cat script.sh

#!/bin/bash
#SBATCH --job-name=AISPECS
#SBATCH --output=/users/segeljak/results/AISPECS.o%j
#SBATCH --error=/users/segeljak/results/AISPECS.e%j
#SBATCH --account=project_xxx
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=64G
#SBATCH --partition=standard-g

srun --verbose \
  singularity exec \
  /users/segeljak/aispecs-docker-eval-amd.sif \
  bash -c "source /opt/aispecs-venv/bin/activate;
           AMD_SERIALIZE_KERNEL=3 AMD_LOG_LEVEL=5 python -c \"import torch; a=torch.randn(3).to('cuda'); print(a)\""

$ sbatch script.sh
```

The gpus become accessible in the command passed to `srun`. I don't know exactly how singularity binds them though. It could be that Singularity requires passing the `--rocm` flag, but then I get the wrong ROCm version.

I just found out that the HPC cluster also supports `podman`. I'll see if I can get the container running on it.

---

### 评论 #14 — segeljakt (2025-01-16T17:25:54Z)

After some debugging, we realised that the issue is Torch-related. We were able to compile and successfully run the `hello.hip` example from https://github.com/ROCm/rocm-examples.

Some other notes that we found out:
* `/dev/dri` and `/dev/kfd` are mapped correctly
* Our successful Hello World run was without `--rocm`, which caused conflicts with library versions due to updated `LD_LIBRARY_PATH`.

Having confirmed that we are able to execute on the GPU, we narrowed down our investigation to Torch. When running this script inside Singularity/Slurm:

```sh
TORCH_LOGS='+dynamo,+inductor' AMD_SERIALIZE_KERNEL=3 AMD_LOG_LEVEL=6 python -c 'import torch; a=torch.randn(3).to("cuda"); print(a)'
```

We get this error output:

```
:3:hip_device_runtime.cpp   :636 : 22940633542 us: [pid:119992 tid:0x147c2d16c080] ^[[32m hipGetDevice ( 0x7ffd71ebcf9c ) ^[[0m
:3:hip_device_runtime.cpp   :644 : 22940633545 us: [pid:119992 tid:0x147c2d16c080] hipGetDevice: Returned hipSuccess :
:3:hip_platform.cpp         :225 : 22940633552 us: [pid:119992 tid:0x147c2d16c080] ^[[32m __hipPushCallConfiguration ( {1,1,1}, {256,1,1}, 0, stream:<null> ) ^[[0m
:3:hip_platform.cpp         :229 : 22940633557 us: [pid:119992 tid:0x147c2d16c080] __hipPushCallConfiguration: Returned hipSuccess :
:3:hip_platform.cpp         :234 : 22940633564 us: [pid:119992 tid:0x147c2d16c080] ^[[32m __hipPopCallConfiguration ( {0,0,1}, {526642268,5244,1}, 0x7ffd71ebd208, 0x7ffd71ebd1f8 ) ^[[0m
:3:hip_platform.cpp         :243 : 22940633568 us: [pid:119992 tid:0x147c2d16c080] __hipPopCallConfiguration: Returned hipSuccess :
:3:hip_module.cpp           :677 : 22940633577 us: [pid:119992 tid:0x147c2d16c080] ^[[32m hipLaunchKernel ( 0x147c1e04a408, {1,1,1}, {256,1,1}, 0x7ffd71ebd220, 0, stream:<null> ) ^[[0m
:3:hip_module.cpp           :678 : 22940633583 us: [pid:119992 tid:0x147c2d16c080] hipLaunchKernel: Returned hipErrorInvalidDeviceFunction :
:3:hip_error.cpp            :36  : 22940633587 us: [pid:119992 tid:0x147c2d16c080] ^[[32m hipGetLastError (  ) ^[[0m
:3:hip_error.cpp            :36  : 22940633590 us: [pid:119992 tid:0x147c2d16c080] ^[[32m hipGetLastError (  ) ^[[0m
:3:hip_device_runtime.cpp   :666 : 22940946670 us: [pid:119992 tid:0x147c2d16c080] ^[[32m hipSetDevice ( 0 ) ^[[0m
:3:hip_device_runtime.cpp   :670 : 22940946679 us: [pid:119992 tid:0x147c2d16c080] hipSetDevice: Returned hipSuccess :
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor.py", line 523, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 708, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 625, in _str_intern
    tensor_str = _tensor_str(self, indent)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 357, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/aispecs-venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 146, in __init__
    tensor_view, torch.isfinite(tensor_view) & tensor_view.ne(0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

:3:hip_device_runtime.cpp   :620 : 22941140321 us: [pid:119992 tid:0x147c2d16c080] ^[[32m hipDeviceSynchronize (  ) ^[[0m
:4:commandqueue.cpp         :147 : 22941140336 us: [pid:119992 tid:0x147c2d16c080] HW Event not ready, awaiting completion instead
:4:commandqueue.cpp         :163 : 22941140344 us: [pid:119992 tid:0x147c2d16c080] All commands finished
:3:hip_device_runtime.cpp   :624 : 22941140348 us: [pid:119992 tid:0x147c2d16c080] hipDeviceSynchronize: Returned hipSuccess :
:3:hip_device_runtime.cpp   :620 : 22941142298 us: [pid:119992 tid:0x147c2d16c080] ^[[32m hipDeviceSynchronize (  ) ^[[0m
:3
```

We are using Torch version 2.5.1 (https://github.com/pytorch/pytorch/commit/a8d6afb511a69687bbb2b7e88a3cf67917e1697e). We have tried to compile with several environment variables (e.g., `HSA_OVERRIDE_GFX_VERSION`, `TORCH_BLAS_PREFER_HIPBLASLT`) with no success.

When we compile Torch, we have previously specified `PYTORCH_ROCM_ARCH=gfx90a`. We are considering to re-compile our image. We are considering if our choice of `PYTORCH_ROCM_ARCH` caused the problem. Should we specify `PYTORCH_ROCM_ARCH=gfx90a:sramecc+:xnack-` instead, or leave the flag unset? Also, where can we find more information about `HSA_OVERRIDE_GFX_VERSION` and its relation to the AMD GPU architecture (e.g., gfx90a)?

---

### 评论 #15 — tcgu-amd (2025-01-16T18:11:37Z)

@segeljakt Thanks for the update!

> Also, where can we find more information about HSA_OVERRIDE_GFX_VERSION and its relation to the AMD GPU architecture (e.g., gfx90a)?

 Unfortunately, we do not have official document for HSA_OVERRIDE_GFX_VERSION (since it should be needed for officially supported devices). That's being said, gfx90a is well tested and you shouldn't really  need HSA_OVERRIDE_GFX_VERSION in this case, especially if hip already works. 

---

### 评论 #16 — tcgu-amd (2025-01-16T18:59:25Z)

> When we compile Torch, we have previously specified PYTORCH_ROCM_ARCH=gfx90a. We are considering to re-compile our image. We are considering if our choice of PYTORCH_ROCM_ARCH caused the problem. Should we specify PYTORCH_ROCM_ARCH=gfx90a:sramecc+:xnack- instead, or leave the flag unset?

I think `PYTORCH_ROCM_ARCH=gfx90a` is the right way to set the flag, and the flag should be set for compilation. I will try to investigate a bit more to see if I can find anything else that might be breaking your compilation. Thanks!

---

### 评论 #17 — tcgu-amd (2025-01-16T20:08:12Z)

@segeljakt, just noticed in the line you are using to build wheel, you have

```
PYTORCH_ROCM_ARCH=$GPU_VERSION USE_KINETO=0 USE_ROCTRACER=0 pip3 --verbose wheel --use-pep517 --no-deps -w "$AISPECS_WHEEL_DIR" --no-build-isolation -e .
```
The -e makes pip build in editable mode, which results in it creating symbolic links instead of properly saving the libraries to site packages. Typically this is not used in conjunction with building wheels I think. I would try removing this flag. 

---

### 评论 #18 — segeljakt (2025-01-21T13:47:45Z)

I rebuilt without the `-e` flag, and it started working! Thank you for the help. Also, I noticed that the HPC cluster was running Singularity with version 4.1.3, but I had 4.2.1, so I downgraded. I am not sure which one of these things made it work, but I might try to reproduce it later. Feel free to close this issue.

---

### 评论 #19 — tcgu-amd (2025-01-21T14:12:48Z)

@segeljakt Glad to hear it is working! I will be closing this issue then. Thanks!

---
