# [Issue]: torch.compile kills the entire system on ROCm 7.0.2 Strix Halo / gfx1151

> **Issue #5572**
> **状态**: closed
> **创建时间**: 2025-10-25T06:23:24Z
> **更新时间**: 2025-10-28T05:13:24Z
> **关闭时间**: 2025-10-28T05:13:24Z
> **作者**: alanzjl
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5572

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- taylding-amd

## 描述

### Problem Description

Running `torch.compile` freezes the entire system without much output. Minimum code to reproduce:
```
import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(1024, 512)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 10)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)

model = SimpleModel().to("cuda")
compiled_model = torch.compile(model)
x = torch.randn(32, 1024, device="cuda")
output = compiled_model(x)
```

It's a freshly installed Ubuntu 24.04.3 and I followed [this](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html) when installing torch. Verified that other torch functionalities seem to be working (quantization, sdpa, etc). 

Ran inth the same issue either with the wheel version of torch or the one installed from pytorch foundation's `--index-url https://download.pytorch.org/whl/nightly/rocm7.0`

Note that this seems to run fine inside the official docker from `rocm/pytorch:latest`

### Operating System

Ubuntu 24.04.3

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

Radeon 8060S / gfx1151

### ROCm Version

ROCm 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32490760(0x1efc508) KB
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
  Packet Processor uCode:: 31
  SDMA engine uCode::      14
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    100663296(0x6000000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    100663296(0x6000000) KB
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
*******
Agent 3
*******
  Name:                    aie2
  Uuid:                    AIE-XX
  Marketing Name:          AIE-ML
  Vendor Name:             AMD
  Feature:                 AGENT_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        1(0x1)
  Queue Min Size:          64(0x40)
  Queue Max Size:          64(0x40)
  Queue Type:              SINGLE
  Node:                    0
  Device Type:             DSP
  Cache Info:
    L2:                      2048(0x800) KB
    L3:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          0(0x0)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            0
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:0
  Memory Properties:
  Features:                AGENT_DISPATCH
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65536(0x10000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
```

### Additional Information

I have tried a few different versions of torch available under https://repo.radeon.com/rocm/manylinux/rocm-rel-7.0.2/, none of the 2.8.0 cp312 versions work:

`torch-2.8.0+gitc497508-cp312-cp312-linux_x86_64.whl` (the one recommended by the doc) - freeze
`torch-2.8.0+rocm7.0.2.lw.git245bf6ed-cp312-cp312-linux_x86_64.whl` - `Bus error (core dumped)` as soon as I `import torch` but does not freeze the system. This is also the version of torch used inside the official docker.
`torch-2.8.0+rocm7.0.2.lw.git2cd73af9-cp312-cp312-linux_x86_64.whl` - freeze

Further information:
It seems using ROCm & PyTorch from the rock suffers from the same issue. I use
```
python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  "rocm[libraries,devel]"
python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  --pre torch torchaudio torchvision
```
to install torch. 

It also seems like the issue might be related to garbage collecting & cleaning, because I do not have trouble running anything with the compiled model, but as soon as the script (that has a torch.compile in it) quits, the whole system then freezes. 

---

## 评论 (2 条)

### 评论 #1 — ianbmacdonald (2025-10-27T17:13:32Z)

Here is what my gfx1151 looks like on current nightly.  Included my pyproject.toml so you can reproduce with exact versions.  I added a few prints to give your test script some output. 

```toml
imac@ai2:~/src/torch_test$ cat pyproject.toml 
[project]
name = "torch-test"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "torch==2.10.0.dev20251026+rocm7.0",
    "torchaudio==2.10.0.dev20251027+rocm7.0",
    "torchvision==0.25.0.dev20251027+rocm7.0",
]

[tool.uv]
index-strategy = "unsafe-best-match"
prerelease = "allow"

[tool.uv.sources]
torch = { index = "rocm7_nightly" }
torchvision = { index = "rocm7_nightly" }
torchaudio = { index = "rocm7_nightly" }

[[tool.uv.index]]
name = "rocm7_nightly"
url = "https://download.pytorch.org/whl/nightly/rocm7.0/"
explicit = true

[[tool.uv.index]]
url = "https://pypi.org/simple"
default = true
```
```
imac@ai2:~/src/torch_test$ uv sync
Resolved 16 packages in 0.68ms
Audited 15 packages in 0.11ms
imac@ai2:~/src/torch_test$ cat torchtest.py 
import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(1024, 512)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 10)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)

model = SimpleModel().to("cuda")
compiled_model = torch.compile(model)
x = torch.randn(32, 1024, device="cuda")
output = compiled_model(x)
print(output)
print(output.shape)
print(output.dtype)
imac@ai2:~/src/torch_test$ uv run torchtest.py 
/home/imac/src/torch_test/.venv/lib/python3.12/site-packages/torch/backends/cuda/__init__.py:156: UserWarning: Please use the new API settings to control TF32 behavior, such as torch.backends.cudnn.conv.fp32_precision = 'tf32' or torch.backends.cuda.matmul.fp32_precision = 'ieee'. Old settings, e.g, torch.backends.cuda.matmul.allow_tf32 = True, torch.backends.cudnn.allow_tf32 = True, allowTF32CuDNN() and allowTF32CuBLAS() will be deprecated after Pytorch 2.9. Please see https://pytorch.org/docs/main/notes/cuda.html#tensorfloat-32-tf32-on-ampere-and-later-devices (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:45.)
  return torch._C._get_cublas_allow_tf32()
tensor([[ 6.5762e-02,  1.5439e-01, -1.1478e-01,  8.1730e-02,  5.3856e-02,
          2.7238e-02, -6.7762e-02, -1.2996e-01,  5.8994e-02, -1.4284e-01],
        [-2.6799e-02,  2.0264e-01, -9.4467e-02,  1.3220e-01,  7.9573e-02,
         -5.8219e-02,  7.2774e-02,  3.3511e-02,  1.5536e-01, -1.4916e-01],
        [ 1.0079e-01,  1.8892e-01, -8.0515e-02,  9.9253e-02,  1.5798e-03,
          2.4254e-02, -4.4816e-02, -8.9536e-02,  2.8274e-02, -1.6714e-01],
        [ 1.1779e-01,  1.1473e-01,  2.5151e-02,  1.9665e-01,  5.0305e-02,
          2.2384e-02,  8.3206e-03,  7.3306e-02,  6.4078e-02, -9.2343e-02],
        [ 1.9245e-01,  1.2617e-01,  2.3980e-02,  1.5622e-01,  1.6763e-02,
          2.0473e-02, -6.9792e-02, -2.6658e-02,  1.2733e-01, -1.3403e-01],
        [ 5.2701e-02,  2.1132e-01, -5.2165e-02,  7.1050e-02,  6.5061e-02,
          4.6235e-02, -1.4713e-01, -3.6006e-02,  6.8957e-02, -2.3512e-01],
        [ 1.6164e-01,  6.3277e-02, -1.1899e-01,  7.1796e-02,  4.6104e-02,
         -7.2900e-02, -9.8361e-02, -3.3366e-02,  9.9989e-02, -1.3675e-01],
        [ 1.4340e-01,  7.7123e-02,  4.6052e-02,  5.9692e-02,  3.7773e-02,
         -8.5651e-02,  4.4397e-02, -1.1667e-01,  9.6574e-02, -1.6888e-01],
        [ 1.9885e-01,  2.1578e-01,  2.3812e-02,  1.4661e-01,  8.6583e-02,
         -4.0772e-02,  1.3449e-01,  1.4957e-02,  1.4389e-01, -1.3485e-01],
        [ 1.5177e-01,  1.2498e-01, -2.8762e-02,  1.4527e-01, -7.7732e-03,
          3.5742e-02,  4.8716e-02, -9.3242e-03,  1.2400e-01, -1.5015e-01],
        [-5.6235e-02,  1.1436e-01,  4.1761e-02, -2.1950e-02,  1.7553e-01,
         -3.6280e-02, -8.3722e-02,  1.3342e-02,  1.1332e-01, -2.4967e-01],
        [ 5.9493e-02,  2.1191e-01,  2.7063e-03, -2.6575e-02,  9.7377e-02,
          5.1304e-03, -4.8369e-02, -1.4827e-02,  1.2557e-01, -3.4190e-02],
        [ 4.0450e-02,  3.8502e-02,  7.2767e-02,  6.4133e-02, -1.4194e-02,
         -1.5026e-01,  1.0225e-01, -7.6118e-02,  9.1655e-03, -1.6010e-02],
        [ 2.0958e-01,  2.0927e-01, -5.8360e-02,  1.3826e-01,  1.6780e-01,
         -1.0983e-01, -1.3367e-01, -2.0612e-01,  1.0694e-01, -1.7018e-01],
        [ 1.1445e-01,  2.2956e-01, -4.7523e-02,  6.3310e-02,  7.9797e-02,
         -6.2739e-02, -7.3015e-02, -9.7777e-02,  1.5346e-01, -1.2929e-01],
        [ 1.5204e-02,  1.8202e-01,  7.0367e-02,  7.1238e-02,  1.6889e-01,
         -2.7072e-02,  7.0854e-02, -5.0113e-02,  2.5537e-01, -1.8711e-01],
        [ 1.2417e-01,  2.4147e-01, -6.4199e-02,  8.2951e-02,  6.4273e-02,
         -3.9714e-02, -2.3923e-03,  7.6862e-04,  9.7152e-02, -3.3717e-02],
        [ 4.9307e-02,  1.5692e-01, -6.2149e-02,  1.1254e-01,  7.0803e-02,
          7.7197e-02, -7.0317e-02, -1.1529e-02, -1.8619e-02, -6.6711e-02],
        [ 1.5558e-01,  7.0840e-02,  2.0199e-02,  3.2558e-02,  1.0768e-01,
         -2.9454e-03,  8.5863e-02, -9.9760e-02, -1.5239e-02, -1.3533e-01],
        [ 1.1768e-01,  1.2193e-01, -4.3500e-02,  9.0851e-02,  2.8055e-01,
          2.8010e-05,  6.7279e-02,  3.1275e-02,  1.8993e-01, -7.4686e-02],
        [ 7.4325e-02,  1.2317e-01, -9.4551e-03,  1.6123e-01,  1.3787e-01,
         -3.5115e-02, -2.0199e-01,  5.7272e-02,  1.3675e-01, -2.4369e-01],
        [ 8.2679e-02,  6.6216e-02, -2.6638e-02, -5.4862e-02,  6.3609e-02,
          2.7951e-02,  1.7355e-02,  1.5382e-02, -7.9325e-03, -8.4051e-02],
        [ 1.2584e-01,  1.6117e-02, -1.8815e-01,  1.6500e-01,  1.7704e-02,
          7.9055e-03,  3.2405e-02,  2.2358e-02, -3.3813e-02, -1.9024e-01],
        [ 1.2273e-01,  2.1551e-01,  7.3745e-02,  1.6990e-01, -1.1175e-01,
         -1.5813e-01,  4.1632e-02, -8.4818e-02,  1.7144e-01, -1.3286e-01],
        [ 1.6016e-01,  5.7064e-02, -3.4912e-02,  1.2586e-01,  7.4126e-02,
         -1.0453e-01, -2.3339e-03,  2.1938e-02,  2.6636e-07, -1.5242e-01],
        [ 2.0856e-03,  1.8384e-01, -3.2151e-02,  4.2367e-02,  6.5098e-02,
          1.2883e-02,  4.6198e-02, -5.1154e-02,  1.7699e-02, -5.2769e-02],
        [ 1.2284e-01,  5.2053e-02, -5.9736e-02,  1.5981e-01,  3.9465e-02,
          8.5232e-02,  3.3466e-02, -3.9580e-02,  7.0915e-02, -1.7659e-01],
        [ 7.5482e-02,  1.7943e-01, -6.7826e-02, -1.6800e-02,  1.0691e-02,
         -1.4504e-01,  1.6237e-01, -5.9961e-02,  2.1511e-02, -1.4620e-01],
        [ 3.2251e-02,  4.9527e-02, -5.7025e-02, -1.7555e-03,  8.8909e-02,
         -3.8895e-02,  6.7017e-02,  5.0322e-02,  1.0433e-01, -5.5490e-02],
        [ 1.4356e-01,  1.1996e-01,  3.5028e-02,  7.8523e-02,  1.8268e-01,
         -4.9650e-02, -1.2952e-02,  4.4574e-03,  1.2353e-01, -1.2297e-01],
        [ 1.4628e-01,  2.0551e-01, -1.3292e-01,  1.6841e-01,  1.9830e-02,
         -1.2051e-01,  1.3825e-01, -2.8077e-02,  1.4799e-02, -7.2122e-02],
        [ 2.3677e-01,  1.5166e-01,  4.5092e-03,  1.0294e-01,  4.5592e-02,
         -5.5536e-02,  7.1891e-02,  5.4516e-02, -9.4224e-03, -1.7145e-01]],
       device='cuda:0', grad_fn=<CompiledFunctionBackward>)
torch.Size([32, 10])
torch.float32
imac@ai2:~/src/torch_test$ amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.0.2+39589fda      amdgpu version: Linuxver ROCm version: 7.0.2    |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0    AMD Radeon Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A              161/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
imac@ai2:~/src/torch_test$ sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
```


---

### 评论 #2 — alanzjl (2025-10-28T05:13:24Z)

thanks @ianbmacdonald! I confirm the issue now went away when I switched to 2.10 nightly. So it's probably safe to conclude that what I had was an issue with the 2.8.0 release. 

For whoever that might also be interested, I had to also add `pytorch-triton-rocm` to `tool.uv.sources` in pyproject.toml because it also has to be from the nightly index.

---
