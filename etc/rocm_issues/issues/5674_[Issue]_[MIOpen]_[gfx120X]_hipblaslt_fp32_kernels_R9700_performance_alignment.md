# [Issue]: [MIOpen] [gfx120X] hipblaslt fp32 kernels R9700 performance alignment

> **Issue #5674**
> **状态**: open
> **创建时间**: 2025-11-17T21:40:29Z
> **更新时间**: 2026-05-01T22:54:59Z
> **作者**: briansp2020
> **标签**: status: triage, project: miopen
> **URL**: https://github.com/ROCm/ROCm/issues/5674

## 标签

- **status: triage** (颜色: #585dd7)
- **project: miopen** (颜色: #962619)

## 负责人

- tcgu-amd

## 描述

### Problem Description

PyTorch performance on Radeon AI Pro R9700 is very poor. I ran a simple benchmark that utilize fastai library and it is 4 times slower than 7900XTX. I was expecting it to be faster than 7900XTX when it is properly optimized (Am I wrong?). It seems RDNA4 is not very well supported in ROCm yet and I'm wondering when the full support will be released. It is "Radeon AI Pro". It should have proper optimized ROCm support...

### Operating System

NAME="Ubuntu" VERSION="24.04.3 LTS (Noble Numbat)"

### CPU

AMD Ryzen 9 9900X 12-Core Processor

### GPU

AMD Radeon AI PRO R9700

### ROCm Version

ROCm7.1

### ROCm Component

_No response_

### Steps to Reproduce

Pull latest ROCm7.1 pytorch docker and run it.
```
docker pull rocm/pytorch:rocm7.1_ubuntu22.04_py3.10_pytorch_release_2.8.0
drun --name pt rocm/pytorch:rocm7.1_ubuntu22.04_py3.10_pytorch_release_2.8.0
```
Inside the docker, install fastai from source and run the test script.
```
cd
git clone https://github.com/fastai/fastai
pip install -e "fastai[dev]"
python quickstart.py
```
The output 
```
# python /pwd/Download/quickstart.py
/opt/venv/lib/python3.10/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon AI PRO R9700
/opt/venv/lib/python3.10/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/venv/lib/python3.10/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
Downloading: "https://download.pytorch.org/models/convnext_small-0c510722.pth" to /root/.cache/torch/hub/checkpoints/convnext_small-0c510722.pth
100%|████████████████████████████████████████████████████████████████████████████████| 192M/192M [00:03<00:00, 57.6MB/s]
epoch     train_loss  valid_loss  error_rate  time
0         0.112140    0.006432    0.002030    02:38
epoch     train_loss  valid_loss  error_rate  time
0         0.013685    0.000191    0.000000    03:57
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    ██████████| 100.00% [105070592/105067061 00:03<00:00]
0         0.466363    0.403699    0.818920  03:24
epoch     train_loss  valid_loss  accuracy  time
0         0.290314    0.258281    0.895560  07:00
1         0.231377    0.200506    0.921240  06:50
```
It's very slow compared to 7900XTX (not the same version. But its performance has not improved much since I ran the test on 7900XTX)
```
(pt) root@rocm:~# python tmp/quickstart.py
/root/pt/lib/python3.10/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/root/pt/lib/python3.10/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.117716    0.001144    0.000677    00:35
epoch     train_loss  valid_loss  error_rate  time
0         0.013864    0.000865    0.000677    00:48
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.464525    0.385803    0.827080  01:09
epoch     train_loss  valid_loss  accuracy  time
0         0.289083    0.221270    0.913160  02:03
1         0.228864    0.199963    0.922200  02:04
```
The test script quickstart.py
```
from fastai.vision.all import *
from fastai.text.all import *
from fastai.collab import *
from fastai.tabular.all import *

if torch.cuda.is_available():
    print("CUDA is available! PyTorch can use your GPU.")
    print(f"Number of GPUs available: {torch.cuda.device_count()}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. PyTorch will use the CPU.")

path = untar_data(URLs.PETS)/'images'

def is_cat(x): return x[0].isupper()
dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path), valid_pct=0.2, seed=42,
    label_func=is_cat, item_tfms=Resize(224))

learn = vision_learner(dls, convnext_small, metrics=error_rate)
learn.fine_tune(1)


print("Training text processing model")
dls = TextDataLoaders.from_folder(untar_data(URLs.IMDB), valid='test')
learn = text_classifier_learner(dls, AWD_LSTM, drop_mult=0.5, metrics=accuracy)
learn.fine_tune(2, 1e-2)
learn.predict("I really liked that movie!")
```





### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

#  /opt/rocm/bin/rocminfo --support
ROCk module version 6.16.6 is loaded
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
  Name:                    AMD Ryzen 9 9900X 12-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 9900X 12-Core Processor
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
  Max Clock Freq. (MHz):   5662
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65488328(0x3e745c8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65488328(0x3e745c8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65488328(0x3e745c8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65488328(0x3e745c8) KB
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
  Uuid:                    GPU-b84b4aa8c7598291
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
  BDFID:                   768
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
  Packet Processor uCode:: 108
  SDMA engine uCode::      662
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

## 评论 (29 条)

### 评论 #1 — tcgu-amd (2025-11-19T17:05:23Z)

Hi @briansp2020, thanks for reaching out. I am sorry that you are experiencing performance issues with gfx12. This has been a known issue due to the lack of MIOpen support for some kernel sizes on gfx12. The good news is, we have just merged winograd support https://github.com/ROCm/rocm-libraries/commit/cb28fbde5c90c0bee176d6e05d8641f5c8f30ccd a few weeks ago, and it should be available within the next few ROCm updates (you could also give it a try from [The Rock nightly builds](https://github.com/ROCm/TheRock/blob/main/RELEASES.md)). Hopefully that will help greatly improve the performance on gfx12 for convolution operations..

---

### 评论 #2 — briansp2020 (2025-11-23T02:33:48Z)

@tcgu-amd Thanks for your reply. Do you know when the PyTorch nightly build will be updated? When I try installing the pytorch built using TheRock, I get 1015 date version.

```
root@rocm:~# python -m venv .venv
source .venv/bin/activate
(.venv) root@rocm:~# python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/ \
  --pre torch torchaudio torchvision
Looking in indexes: https://rocm.nightlies.amd.com/v2/gfx120X-all/
Collecting torch
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/torch-2.10.0a0%2Brocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (225.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 225.3/225.3 MB 25.3 MB/s eta 0:00:00
Collecting torchaudio
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/torchaudio-2.8.0a0%2Brocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (491 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 491.4/491.4 kB 2.4 MB/s eta 0:00:00
Collecting torchvision
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/torchvision-0.25.0a0%2Brocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (1.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 8.3 MB/s eta 0:00:00
Collecting filelock (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/filelock-3.19.1-py3-none-any.whl (15 kB)
Collecting typing-extensions>=4.10.0 (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/typing_extensions-4.14.1-py3-none-any.whl (43 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 43.9/43.9 kB 7.6 MB/s eta 0:00:00
Collecting setuptools (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/setuptools-80.9.0-py3-none-any.whl (1.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 28.5 MB/s eta 0:00:00
Collecting sympy>=1.13.3 (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/sympy-1.14.0-py3-none-any.whl (6.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 39.5 MB/s eta 0:00:00
Collecting networkx>=2.5.1 (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/networkx-3.5-py3-none-any.whl (2.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 26.4 MB/s eta 0:00:00
Collecting jinja2 (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/jinja2-3.1.6-py3-none-any.whl (134 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.9/134.9 kB 3.1 MB/s eta 0:00:00
Collecting fsspec>=0.8.5 (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/fsspec-2025.7.0-py3-none-any.whl (199 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 199.6/199.6 kB 4.7 MB/s eta 0:00:00
Collecting rocm==7.10.0a20251015 (from rocm[libraries]==7.10.0a20251015->torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/rocm-7.10.0a20251015.tar.gz (14 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting pytorch-triton-rocm==3.5.0+gitd0444d76.rocm7.10.0a20251015 (from torch)
  Downloading https://rocm.nightlies.amd.com/v2/gfx120X-all/pytorch_triton_rocm-3.5.0%2Bgitd0444d76.rocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (317.1 MB)
     ━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━ 104.9/317.1 MB 59.0 MB/s eta 0:00:04
```

---

### 评论 #3 — tcgu-amd (2025-11-24T17:32:07Z)

Hi @briansp2020 Yes we are trying our best to fix the Linux torch wheel release pipeline. We have a super issue keeping track of the progress here https://github.com/ROCm/TheRock/issues/2156. Hopefully it will get fixed soon..

---

### 评论 #4 — stellaraccident (2025-12-12T13:16:14Z)

@ROCm/rocm-genies this is a big problem. Can you please ping me internally as I've got a team rolling off another project who I'd like to have grind on this for some weeks and make sure that this pro card is in good shape holistically. I'd also like to make sure that gaps are closed so that the same performance is achieved on both Linux and Windows (fix the windows ck issues once and for all).

---

### 评论 #5 — tcgu-amd (2025-12-12T17:53:42Z)

Hi @briansp2020 I took another look using a more stable wheel from the rock v2-staging, and it does look like the performance issue is still persisting. As mentioned, we will begin a full-scale investigation into this issue and git it fixed soon. Thanks! 

---

### 评论 #6 — tcgu-amd (2025-12-12T20:17:20Z)

It appears that the issue is still with MIOpen not enabling advanced kernels for gfx12 even in the latest wheels

Testing with `MIOPEN_LOG_LEVEL=7 MIOPEN_FIND_MODE=1 python quickstart.py 2>&1 | tee log.txt && grep Success ./log.txt`   
on gfx1201 with `torch-2.9.1+rocm7.11.0a20251212`

```
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvBwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvBwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvBwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvBwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvBwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvBwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvBwd: Success.
```

While on gfx1100 with even the early `torch-2.9.0a0+rocm7.0.0rc20250903` we get

```
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvBinWinogradRxSf3x2: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvBinWinogradRxSf2x3: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] GemmFwdRest: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvBinWinogradRxSf3x2: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvBinWinogradRxSf2x3g1: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] GemmFwdRest: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvBinWinogradRxSf3x2: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvBinWinogradRxSf2x3: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] ConvDirectNaiveConvFwd: Success.
MIOpen(HIP): Info2 [SearchForAllSolutions] GemmFwdRest: Success.
```
This is likely what causes the performance discrepancy.



---

### 评论 #7 — briansp2020 (2025-12-13T15:01:15Z)

Is anyone having performance issues with ROCm 7 and 7900XTX ? I was excited about 7.10 release supporting 7900XTX. So, I tried it with fresh install of Ubuntu Server 24.04 / ROCm 7.10 /7900XTX and its performance is horrible. I don't know if https://github.com/ROCm/ROCm/issues/5725 is related... Also, I get "WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status" When I run rocm-smi command

```
(.venv) root@rocm:~# rocm-smi


WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

=========================================== ROCm System Management Interface ===========================================
===================================================== Concise Info =====================================================
Device  Node  IDs              Temp    Power   Partitions          SCLK     MCLK     Fan     Perf  PwrCap  VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Avg)   (Mem, Compute, ID)
========================================================================================================================
0       1     0x744c,   47413  68.0°C  267.0W  N/A, N/A, 0         2661Mhz  1249Mhz  35.69%  high  291.0W  53%    100%
========================================================================================================================
================================================= End of ROCm SMI Log ==================================================
```

---

### 评论 #8 — stellaraccident (2025-12-13T16:39:24Z)

@ROCm/rocm-genies 

---

### 评论 #9 — briansp2020 (2025-12-14T18:24:30Z)

I just ran ROCm 6.4.6 Pytorch 2.7.1 vs ROCm 7.1 Pytorch 2.9.1 vs ROCm 7.1.1 Pytorch 2.7.1 using 7900XTX. Though ROCm6 version is still a bit slower than what I have gotten before, it still seems reasonable. ROCm7 versions just seem broken. Since this is RDNA3 issue, should I create a new issue? Or it this what https://github.com/ROCm/ROCm/issues/5725 is?

```
docker pull rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

~~~ Set up stuff ~~~

root@rocm:~# python /pwd/Downloads/quickstart.py
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
Downloading: "https://download.pytorch.org/models/convnext_small-0c510722.pth" to /root/.cache/torch/hub/checkpoints/convnext_small-0c510722.pth
100%|████████████████████████████████████████████████████████████████████████████████| 192M/192M [00:06<00:00, 29.4MB/s]
epoch     train_loss  valid_loss  error_rate  time
0         0.106292    0.000386    0.000000    00:42
epoch     train_loss  valid_loss  error_rate  time
0         0.010347    0.001300    0.000677    00:47
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    ██████████| 100.00% [105070592/105067061 00:03<00:00]
0         0.463733    0.416764    0.809560  01:10
epoch     train_loss  valid_loss  accuracy  time
0         0.289708    0.224006    0.910560  02:20
1         0.232052    0.204900    0.919240  02:10
```

```
docker pull rocm/pytorch:rocm7.1_ubuntu24.04_py3.12_pytorch_release_2.9.1

~~~ Set up stuff ~~~

root@rocm:~# python /pwd/Downloads/quickstart.py
/opt/venv/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
Downloading: "https://download.pytorch.org/models/convnext_small-0c510722.pth" to /root/.cache/torch/hub/checkpoints/convnext_small-0c510722.pth
100%|████████████████████████████████████████████████████████████████████████████████| 192M/192M [00:03<00:00, 59.5MB/s]
epoch     train_loss  valid_loss  error_rate  time
0         0.107739    0.000934    0.000000    02:10
epoch     train_loss  valid_loss  error_rate  time
0         0.011863    0.000084    0.000000    03:22
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    ██████████| 100.00% [105070592/105067061 00:03<00:00]
0         0.471562    0.391713    0.823120  01:12
epoch     train_loss  valid_loss  accuracy  time
0         0.287767    0.225610    0.910240  03:03
1         0.243133    0.205940    0.918840  02:51
```

```
docker pull rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1

~~~ Set up stuff ~~~

root@rocm:~# python /pwd/Downloads/quickstart.py
/opt/venv/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
Downloading: "https://download.pytorch.org/models/convnext_small-0c510722.pth" to /root/.cache/torch/hub/checkpoints/convnext_small-0c510722.pth
100%|████████████████████████████████████████████████████████████████████████████████| 192M/192M [00:04<00:00, 42.1MB/s]
epoch     train_loss  valid_loss  error_rate  time
0         0.106990    0.000616    0.000000    01:09
epoch     train_loss  valid_loss  error_rate  time
0         0.018354    0.000858    0.000677    02:06
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    ██████████| 100.00% [105070592/105067061 00:03<00:00]
0         0.459786    0.402556    0.816560  01:13
epoch     train_loss  valid_loss  accuracy  time
0         0.290600    0.229142    0.909240  03:02
1         0.223527    0.198819    0.922480  02:50
```

---

### 评论 #10 — tcgu-amd (2025-12-15T15:00:47Z)

Hi @briansp2020 is your issue related to https://github.com/ROCm/TheRock/issues/2485?

---

### 评论 #11 — k-artem (2025-12-15T15:11:27Z)

@briansp2020  @tcgu-amd performance on gfx12x should be aligned after/with https://github.com/ROCm/rocm-libraries/pull/3000/

---

### 评论 #12 — briansp2020 (2025-12-15T19:48:26Z)

@tcgu-amd I think it is the same issue.

[rocm6.4.4_pt2.7.1.log](https://github.com/user-attachments/files/24174337/rocm6.4.4_pt2.7.1.log)

[rocm7.1.1_pt2.7.1.log](https://github.com/user-attachments/files/24174339/rocm7.1.1_pt2.7.1.log)

---

### 评论 #13 — tcgu-amd (2025-12-16T16:26:27Z)

@briansp2020 Yes I was able to confirm the regression as well. Trying to bisect to what caused it. Thank you for your patience! 

---

### 评论 #14 — tcgu-amd (2025-12-17T20:35:26Z)

@briansp2020 Please check https://github.com/ROCm/TheRock/issues/2485 for a workaround for the rocm7 gfx11 regression. This thread will continue to be used for keeping track of gfx12 performance. Thanks :)

---

### 评论 #15 — briansp2020 (2025-12-18T07:31:47Z)

@tcgu-amd The workaround helps. With the workaround, rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1 matches ROCm 6.6.4 in image processing and is faster than without the work around. But the text processing is still slow. I'll put comments in [#2485](https://github.com/ROCm/TheRock/issues/2485).

```
root@rocm:~# PYTORCH_MIOPEN_SUGGEST_NHWC=0 python /pwd/Downloads/quickstart.py
/opt/venv/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.113572    0.000550    0.000000    00:32
epoch     train_loss  valid_loss  error_rate  time
0         0.021682    0.003351    0.001353    00:45
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.463307    0.410007    0.814280  01:09
epoch     train_loss  valid_loss  accuracy  time
0         0.301669    0.253234    0.897920  02:53
1         0.234085    0.203753    0.919200  02:50
```

---

### 评论 #16 — tcgu-amd (2025-12-18T19:24:22Z)

Hi @briansp2020, that's strange -- I wasn't observing a servere discrepancy between text workloads even without the workaround. The latest log you posted, was that with the workaround? Because it looks fairly close to what I see as well for both ROCm 6 and 7. 

Edit: This is what I see for ROCm 6

```
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XT
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.461101    0.393705    0.822920  01:08
epoch     train_loss  valid_loss  accuracy  time
0         0.298112    0.230675    0.908520  02:57
1         0.220497    0.207637    0.919600  02:51
```

And this is what I see for ROCm 7 without workaround
```
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XT
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.475451    0.410122    0.820000  01:10
epoch     train_loss  valid_loss  accuracy  time
0         0.280661    0.344886    0.838160  02:57
1         0.229918    0.198162    0.923200  02:50
```

---

### 评论 #17 — briansp2020 (2025-12-18T20:08:11Z)

@tcgu-amd Is that from your own run?
What I posted in https://github.com/ROCm/ROCm/issues/5674#issuecomment-3651787218 show 
```
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    ██████████| 100.00% [105070592/105067061 00:03<00:00]
0         0.463733    0.416764    0.809560  01:10
epoch     train_loss  valid_loss  accuracy  time
0         0.289708    0.224006    0.910560  02:20
1         0.232052    0.204900    0.919240  02:10
```
which is somewhat faster than what you posted.

It's still slower than what I have gotten in the past (shown in the original post https://github.com/ROCm/ROCm/issues/5674#issue-3635183217). With the workaround, image processing time is the fastest I've seen. 

---

### 评论 #18 — tcgu-amd (2025-12-18T22:03:10Z)

@briansp2020 What is your MIOPEN_FIND_MODE? Can you try with 2 and 5 respectively to see if that makes a difference? Maybe try a few more runs and see what's the statistic deviance? So far I am not spotting anything suspicious from the logs and the performance is consistent on my end.. 

---

### 评论 #19 — briansp2020 (2025-12-19T03:31:14Z)

@tcgu-amd 
As shown below, on my machine, text processing is 50% slower when using ROCm 7.1.1 compared to 6.4.4

```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

~~~

$ docker exec -it pt6 bash
root@rocm:/var/lib/jenkins# cd
root@rocm:~# MIOPEN_FIND_MODE=2 python /pwd/Downloads/quickstart.py
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.107538    0.000951    0.000000    00:31
epoch     train_loss  valid_loss  error_rate  time
0         0.018633    0.001369    0.000677    00:44
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.463629    0.382270    0.829080  01:07
epoch     train_loss  valid_loss  accuracy  time
0         0.291448    0.282395    0.880840  02:09
1         0.233027    0.202903    0.921520  02:09
root@rocm:~# MIOPEN_FIND_MODE=5 python /pwd/Downloads/quickstart.py
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.129428    0.001074    0.000000    00:32
epoch     train_loss  valid_loss  error_rate  time
0         0.022352    0.000108    0.000000    00:45
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.469608    0.403388    0.820000  01:09
epoch     train_loss  valid_loss  accuracy  time
0         0.300587    0.233531    0.907080  02:12
1         0.227644    0.203419    0.921680  02:13
```

```
rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1

~~~

$ docker exec -it pt711 bash
root@rocm:/# cd
root@rocm:~# MIOPEN_FIND_MODE=2  PYTORCH_MIOPEN_SUGGEST_NHWC=0 python /pwd/Downloads/quickstart.py
/opt/venv/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.118251    0.002238    0.001353    00:31
epoch     train_loss  valid_loss  error_rate  time
0         0.025084    0.000868    0.000677    00:43
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.465843    0.393329    0.823880  01:07
epoch     train_loss  valid_loss  accuracy  time
0         0.290815    0.224406    0.911360  02:50
1         0.225136    0.203422    0.921000  02:47
root@rocm:~# MIOPEN_FIND_MODE=5  PYTORCH_MIOPEN_SUGGEST_NHWC=0 python /pwd/Downloads/quickstart.py
/opt/venv/lib/python3.12/site-packages/apex/transformer/functional/fused_rope.py:54: UserWarning: Using the native apex kernel for RoPE.
  warnings.warn("Using the native apex kernel for RoPE.", UserWarning)
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.106928    0.000485    0.000000    00:31
epoch     train_loss  valid_loss  error_rate  time
0         0.013304    0.001048    0.000677    00:43
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.473756    0.397804    0.822240  01:07
epoch     train_loss  valid_loss  accuracy  time
0         0.290113    0.240782    0.905840  02:49
1         0.233494    0.203330    0.920600  02:47
root@rocm:~#
```


---

### 评论 #20 — tcgu-amd (2025-12-19T21:08:14Z)

@briansp2020 Good news: I was able to reproduce the performance issue with the official Pytorch + ROCm 6.4 release. I think this is quite an independent issue from the other one so I'm going to open a new issue to track this. Let's move the discussion there. Thanks! 

---

### 评论 #21 — Nem404 (2025-12-23T20:46:01Z)

> I'd also like to make sure that gaps are closed so that the same performance is achieved on both Linux and Windows (fix the windows ck issues once and for all).

That would be great



---

### 评论 #22 — idhamari (2026-01-05T19:52:36Z)

I think I have the same issue. I tried training a simple CNN model using R9700 vs RTX2080Ti, the old RTX is 3x faster.  Moreover, the GPU and amd-smi keep hanging from time to time, so I have to restart the machine.  

---

### 评论 #23 — sascharo (2026-01-24T15:45:31Z)

> I think I have the same issue. I tried training a simple CNN model using R9700 vs RTX2080Ti, the old RTX is 3x faster.  Moreover, the GPU and amd-smi keep hanging from time to time, so I have to restart the machine.  

Has this been resolved already?

---

### 评论 #24 — tcgu-amd (2026-01-27T15:44:44Z)

@sascharo Unfortunately R9700 performance still is not aligned with other Radeon architectures. We are looking at that right now. Thanks! 

---

### 评论 #25 — piotrp88 (2026-03-18T10:58:59Z)

Is there any update? I'm waiting for a new R9700 but am wondering if I made the right decision ordering it and also if this bug will be resolved. Thanks for your great effort

---

### 评论 #26 — k-artem (2026-03-18T16:29:18Z)

Update regarding convolution ops (image processing in quickstart.py): we have updated layout settings in pytorch https://github.com/pytorch/pytorch/pull/170780/changes, so in case of usage upstream pytorch no need to set `PYTORCH_MIOPEN_SUGGEST_NHWC=0` explicitly. 
Reminder: using NHWC layout leads to fallback in suboptimal convolution kernels (naive) that are very slow. 

---

### 评论 #27 — k-artem (2026-03-27T10:25:50Z)

Regarding  text processing -> https://github.com/ROCm/ROCm/issues/5805#issuecomment-4141615579

---

### 评论 #28 — tcgu-amd (2026-04-14T15:11:34Z)

Hi all, just an update, the performance hit seems to be due to untuned fp32 kernels on gfx12, especially for the larger problem sizes encountered in the reproducer (on smaller dimensions the performances appear to be similar between tuned and untuned). After tuning, some of the affected kernels gained up to 10x speed improvements (~2 TFLOPs to 19TFLOPS).  The updated kernels will be merged and included in the nightly release soon. Thanks! 

---

### 评论 #29 — briansp2020 (2026-05-01T22:54:59Z)

Any updates? I just tried  https://rocm.nightlies.amd.com/v2-staging/gfx120X-all/torch-2.11.0%2Brocm7.13.0a20260501-cp312-cp312-linux_x86_64.whl and the result is below. It's much better. But I was expecting R9700 to be better than 7900XTX. Using LMStudio on windows (which uses Vulcan), R9700 performs as well as 7900XTX. So, R9700 performance should double from what I got today at least. Is R9700 expected to be faster than 7900XTX when both are properly optimized?

Also, what does the "MIOpen(HIP): Warning [ParseAndLoadDb] File is unreadable: "/root/.venv/lib/python3.12/site-packages/_rocm_sdk_libraries_gfx120X_all/share/miopen/db/gfx1201_32.HIP.fdb.txt"" mean?

```
# python /pwd/Downloads/quickstart.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon AI PRO R9700
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
Epoch 1/1 : |------------------------------------------------------------| 0.00% [0/92 00:00<?]MIOpen(HIP): Warning [ParseAndLoadDb] File is unreadable: "/root/.venv/lib/python3.12/site-packages/_rocm_sdk_libraries_gfx120X_all/share/miopen/db/gfx1201_32.HIP.fdb.txt"
0         0.113136    0.003694    0.001353    00:53
epoch     train_loss  valid_loss  error_rate  time
0         0.017555    0.000213    0.000000    01:07
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.468677    0.388410    0.826880  01:59
epoch     train_loss  valid_loss  accuracy  time
0         0.290031    0.254693    0.890800  03:57
1         0.237254    0.205123    0.920240  03:21
```

---
