# [Issue]: ROCm 6.4 -> ROCm 7.1 GEMM fp32 kernel regression

> **Issue #5805**
> **状态**: open
> **创建时间**: 2025-12-19T21:14:24Z
> **更新时间**: 2026-04-20T13:55:57Z
> **作者**: tcgu-amd
> **标签**: Under Investigation, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5805

## 标签

- **Under Investigation** (颜色: #0052cc)
- **status: assessed** (颜色: #e6d813)

## 负责人

- tcgu-amd

## 描述

### Problem Description

This is forked from https://github.com/ROCm/ROCm/issues/5674#issuecomment-3668793386. Opened on behalf of @briansp2020

rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1 text processing is slow. 

Performance of ROCm 7.1

````
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

Performance of ROCm 6.4
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

### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen 9 9900X 12-Core Processor

### GPU

AMD Radeon AI PRO R9700

### ROCm Version

7.1

### ROCm Component

_No response_

### Steps to Reproduce

docker pull rocm/pytorch:rocm7.1_ubuntu22.04_py3.10_pytorch_release_2.8.0
drun --name pt rocm/pytorch:rocm7.1_ubuntu22.04_py3.10_pytorch_release_2.8.0

cd
git clone https://github.com/fastai/fastai
pip install -e "fastai[dev]"
python quickstart.py

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

/opt/rocm/bin/rocminfo --support
ROCk module version 6.16.6 is loaded
HSA System Attributes
Runtime Version: 1.18
Runtime Ext Version: 1.14
System Timestamp Freq.: 1000.000000MHz
Sig. Max Wait Duration: 18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model: LARGE
System Endianness: LITTLE
Mwaitx: DISABLED
XNACK enabled: NO
DMAbuf Support: YES
VMM Support: YES

==========
HSA Agents
Agent 1

Name: AMD Ryzen 9 9900X 12-Core Processor
Uuid: CPU-XX
Marketing Name: AMD Ryzen 9 9900X 12-Core Processor
Vendor Name: CPU
Feature: None specified
Profile: FULL_PROFILE
Float Round Mode: NEAR
Max Queue Number: 0(0x0)
Queue Min Size: 0(0x0)
Queue Max Size: 0(0x0)
Queue Type: MULTI
Node: 0
Device Type: CPU
Cache Info:
L1: 49152(0xc000) KB
Chip ID: 0(0x0)
ASIC Revision: 0(0x0)
Cacheline Size: 64(0x40)
Max Clock Freq. (MHz): 5662
BDFID: 0
Internal Node ID: 0
Compute Unit: 24
SIMDs per CU: 0
Shader Engines: 0
Shader Arrs. per Eng.: 0
WatchPts on Addr. Ranges:1
Memory Properties:
Features: None
Pool Info:
Pool 1
Segment: GLOBAL; FLAGS: FINE GRAINED
Size: 65488328(0x3e745c8) KB
Allocatable: TRUE
Alloc Granule: 4KB
Alloc Recommended Granule:4KB
Alloc Alignment: 4KB
Accessible by all: TRUE
Pool 2
Segment: GLOBAL; FLAGS: EXTENDED FINE GRAINED
Size: 65488328(0x3e745c8) KB
Allocatable: TRUE
Alloc Granule: 4KB
Alloc Recommended Granule:4KB
Alloc Alignment: 4KB
Accessible by all: TRUE
Pool 3
Segment: GLOBAL; FLAGS: KERNARG, FINE GRAINED
Size: 65488328(0x3e745c8) KB
Allocatable: TRUE
Alloc Granule: 4KB
Alloc Recommended Granule:4KB
Alloc Alignment: 4KB
Accessible by all: TRUE
Pool 4
Segment: GLOBAL; FLAGS: COARSE GRAINED
Size: 65488328(0x3e745c8) KB
Allocatable: TRUE
Alloc Granule: 4KB
Alloc Recommended Granule:4KB
Alloc Alignment: 4KB
Accessible by all: TRUE
ISA Info:

Agent 2

Name: gfx1201
Uuid: GPU-b84b4aa8c7598291
Marketing Name: AMD Radeon AI PRO R9700
Vendor Name: AMD
Feature: KERNEL_DISPATCH
Profile: BASE_PROFILE
Float Round Mode: NEAR
Max Queue Number: 128(0x80)
Queue Min Size: 64(0x40)
Queue Max Size: 131072(0x20000)
Queue Type: MULTI
Node: 1
Device Type: GPU
Cache Info:
L1: 32(0x20) KB
L2: 8192(0x2000) KB
L3: 65536(0x10000) KB
Chip ID: 30033(0x7551)
ASIC Revision: 1(0x1)
Cacheline Size: 256(0x100)
Max Clock Freq. (MHz): 2350
BDFID: 768
Internal Node ID: 1
Compute Unit: 64
SIMDs per CU: 2
Shader Engines: 4
Shader Arrs. per Eng.: 2
WatchPts on Addr. Ranges:4
Coherent Host Access: FALSE
Memory Properties:
Features: KERNEL_DISPATCH
Fast F16 Operation: TRUE
Wavefront Size: 32(0x20)
Workgroup Max Size: 1024(0x400)
Workgroup Max Size per Dimension:
x 1024(0x400)
y 1024(0x400)
z 1024(0x400)
Max Waves Per CU: 32(0x20)
Max Work-item Per CU: 1024(0x400)
Grid Max Size: 4294967295(0xffffffff)
Grid Max Size per Dimension:
x 2147483647(0x7fffffff)
y 65535(0xffff)
z 65535(0xffff)
Max fbarriers/Workgrp: 32
Packet Processor uCode:: 108
SDMA engine uCode:: 662
IOMMU Support:: None
Pool Info:
Pool 1
Segment: GLOBAL; FLAGS: COARSE GRAINED
Size: 33406976(0x1fdc000) KB
Allocatable: TRUE
Alloc Granule: 4KB
Alloc Recommended Granule:2048KB
Alloc Alignment: 4KB
Accessible by all: FALSE
Pool 2
Segment: GROUP
Size: 64(0x40) KB
Allocatable: FALSE
Alloc Granule: 0KB
Alloc Recommended Granule:0KB
Alloc Alignment: 0KB
Accessible by all: FALSE
ISA Info:
ISA 1
Name: amdgcn-amd-amdhsa--gfx1201
Machine Models: HSA_MACHINE_MODEL_LARGE
Profiles: HSA_PROFILE_BASE
Default Rounding Mode: NEAR
Default Rounding Mode: NEAR
Fast f16: TRUE
Workgroup Max Size: 1024(0x400)
Workgroup Max Size per Dimension:
x 1024(0x400)
y 1024(0x400)
z 1024(0x400)
Grid Max Size: 4294967295(0xffffffff)
Grid Max Size per Dimension:
x 2147483647(0x7fffffff)
y 65535(0xffff)
z 65535(0xffff)
FBarrier Max Size: 32
ISA 2
Name: amdgcn-amd-amdhsa--gfx12-generic
Machine Models: HSA_MACHINE_MODEL_LARGE
Profiles: HSA_PROFILE_BASE
Default Rounding Mode: NEAR
Default Rounding Mode: NEAR
Fast f16: TRUE
Workgroup Max Size: 1024(0x400)
Workgroup Max Size per Dimension:
x 1024(0x400)
y 1024(0x400)
z 1024(0x400)
Grid Max Size: 4294967295(0xffffffff)
Grid Max Size per Dimension:
x 2147483647(0x7fffffff)
y 65535(0xffff)
z 65535(0xffff)
FBarrier Max Size: 32
*** Done ***

### Additional Information

_No response_

---

## 评论 (44 条)

### 评论 #1 — tcgu-amd (2025-12-23T20:24:22Z)

@briansp2020 Here's some updates:

Did some profiling, and here's the time MIOpen spent on each API call for 

ROCm 6.4:
```
API Call                                           Total Time (ms) Calls    Avg (ms)
-------------------------------------------------------------------------------------
miopenDestroyTensorDescriptor                      106727.163      8392239  0.013
miopenCreateRNNDescriptor                          105051.669      57147    1.838
miopenCreateTensorDescriptor                       11229.078       8392239  0.001
miopenSetTensorDescriptor                          8507.687        7661007  0.001
miopenGetRNNWorkspaceSize                          1689.364        45702    0.037
miopenGetRNNLayerParamSize                         426.523         365616   0.001
miopenGetRNNLayerBiasSize                          403.353         365616   0.001
miopenGetRNNLayerParamOffset                       379.875         365616   0.001
miopenGetRNNLayerBiasOffset                        375.462         365616   0.001
miopenSetRNNDescriptor                             99.948          57147    0.002
miopenRNNForwardInference                          76.938          16374    0.005
miopenGetRNNTrainingReserveSize                    76.659          17883    0.004
miopenDestroyRNNDescriptor                         59.355          57147    0.001
miopenRNNBackwardData                              56.610          11445    0.005
miopenRNNForwardTraining                           54.024          17883    0.003
miopenGetRNNParamsSize                             40.405          34257    0.001
miopenRNNBackwardWeights                           23.135          11445    **0.002**
```

ROCm 7.11
```
miopenCreateRNNDescriptor                          181940.865      57204    3.181
miopenDestroyTensorDescriptor                      106274.183      8394966  0.013
miopenCreateTensorDescriptor                       11242.422       8394966  0.001
miopenSetTensorDescriptor                          8197.064        7663062  0.001
miopenGetRNNWorkspaceSize                          1317.702        45744    0.029
miopenGetRNNLayerParamSize                         427.945         365952   0.001
miopenGetRNNLayerBiasSize                          417.622         365952   0.001
miopenGetRNNLayerParamOffset                       381.440         365952   0.001
miopenGetRNNLayerBiasOffset                        376.665         365952   0.001
miopenSetRNNDescriptor                             99.261          57204    0.002
miopenGetRNNTrainingReserveSize                    77.038          17910    0.004
miopenRNNForwardInference                          76.947          16374    0.005
miopenDestroyRNNDescriptor                         60.406          57204    0.001
miopenRNNBackwardData                              58.699          11460    0.005
miopenRNNForwardTraining                           54.521          17910    0.003
miopenGetRNNParamsSize                             45.786          34284    0.001
miopenRNNBackwardWeights                           23.135          11460    0.002
```

As you can see, the main contributor in runtime is miopenCreateRNNDescriptor, which increased by 70%. I suspect this is due to the newly introduced dynamic optimization code. Can you try to see if setting `MIOPEN_RNN_DYNAMIC_FORCE=0` helps in anyway? Thanks! 

---

### 评论 #2 — tcgu-amd (2026-01-08T17:26:39Z)

Hi, I will be closing this issue due to inactivity. Please feel free ping me if further assistance is needed. Thanks! 

---

### 评论 #3 — briansp2020 (2026-01-08T18:55:32Z)

Is this resolved? I'm still waiting for the fix...


---

### 评论 #4 — tcgu-amd (2026-01-08T19:00:46Z)

HI @briansp2020, happy new year! Did you try with MIOPEN_RNN_DYNAMIC_FORCE=0? So far, based on what I have seen this didn't look like a bug, rather a side effect of using a more advanced solution optimization algorithm on training a relatively small RNN model (given the fact that the overhead of creating RNN descriptor is by far the bigger contributor in runtime both before/after the change). On a larger model this shouldn't be as significant of an issue and should result in a performance gain instead. 

---

### 评论 #5 — briansp2020 (2026-01-08T21:11:33Z)

Hi @tcgu-amd , happy new year to you as well!
MIOPEN_RNN_DYNAMIC_FORCE=0 does not seem to make a difference...

```
rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1


MIOPEN_FIND_MODE=5  PYTORCH_MIOPEN_SUGGEST_NHWC=0 python /pwd/Downloads/quickstart.py
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
0         0.115563    0.000416    0.000000    00:32
epoch     train_loss  valid_loss  error_rate  time
0         0.011584    0.000404    0.000000    00:43
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.458454    0.399951    0.820000  01:07
epoch     train_loss  valid_loss  accuracy  time
0         0.305108    0.232605    0.905760  02:49
1         0.235795    0.201710    0.921040  02:45


MIOPEN_FIND_MODE=5  PYTORCH_MIOPEN_SUGGEST_NHWC=0  MIOPEN_RNN_DYNAMIC_FORCE=0 python /pwd/Downloads/quickst
art.py
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
0         0.118545    0.000980    0.000000    00:31
epoch     train_loss  valid_loss  error_rate  time
0         0.015005    0.000052    0.000000    00:44
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.460033    0.393837    0.824160  01:08
epoch     train_loss  valid_loss  accuracy  time
0         0.297583    0.234970    0.903680  02:50
1         0.248170    0.206763    0.919280  02:47
```


---

### 评论 #6 — briansp2020 (2026-01-08T21:12:55Z)

Just tried 7.10 and PYTORCH_MIOPEN_SUGGEST_NHWC=0 workaround does not seem to work any more. Image stuff is slow again...

```
(.venv) root@rocm:~# MIOPEN_FIND_MODE=5  PYTORCH_MIOPEN_SUGGEST_NHWC=0  MIOPEN_RNN_DYNAMIC_FORCE=0 python /pwd/Downloads/quickstart.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.112476    0.000906    0.000000    01:34
epoch     train_loss  valid_loss  error_rate  time
0         0.017625    0.001031    0.000677    02:06
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.463619    0.394835    0.822840  01:11
epoch     train_loss  valid_loss  accuracy  time
0         0.292603    0.234902    0.906720  02:56
1         0.233250    0.202328    0.921280  02:51
```

---

### 评论 #7 — tcgu-amd (2026-01-08T21:15:09Z)

> Just tried 7.10 and PYTORCH_MIOPEN_SUGGEST_NHWC=0 workaround does not seem to work any more. Image stuff is slow again...
> 
> ```
> (.venv) root@rocm:~# MIOPEN_FIND_MODE=5  PYTORCH_MIOPEN_SUGGEST_NHWC=0  MIOPEN_RNN_DYNAMIC_FORCE=0 python /pwd/Downloads/quickstart.py
> CUDA is available! PyTorch can use your GPU.
> Number of GPUs available: 1
> GPU Name: AMD Radeon RX 7900 XTX
> /root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
>   warnings.warn(
> /root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
>   warnings.warn(msg)
> epoch     train_loss  valid_loss  error_rate  time
> 0         0.112476    0.000906    0.000000    01:34
> epoch     train_loss  valid_loss  error_rate  time
> 0         0.017625    0.001031    0.000677    02:06
> Training text processing model
> epoch     train_loss  valid_loss  accuracy  time
> 0         0.463619    0.394835    0.822840  01:11
> epoch     train_loss  valid_loss  accuracy  time
> 0         0.292603    0.234902    0.906720  02:56
> 1         0.233250    0.202328    0.921280  02:51
> ```

Interesting...Was it the same venv or did you install a new one? 

---

### 评论 #8 — briansp2020 (2026-01-08T21:32:01Z)

I just installed today. I think the files in https://repo.amd.com/rocm/whl/ has changed since the initial release. I remember that [gfx120X-all](https://repo.amd.com/rocm/whl/gfx120X-all/) subdirectory did not exist when I first checked out the directory.

Are you guys preparing to release new build using TheRock? 

---

### 评论 #9 — tcgu-amd (2026-01-08T21:34:31Z)

@briansp2020 Okay so you installed ROCm from the official repo, not the ROCK? From where did you install the torch wheels? 

---

### 评论 #10 — briansp2020 (2026-01-08T21:55:22Z)

I just did the following in my rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1 docker image today. I thought that was what I'm supposed to do to install TheRock. What do you mean by "installed ROCm from the official repo, not the ROCK?" I was just following the instructions from https://rocm.docs.amd.com/en/7.10.0-preview/install/rocm.html

```
python -m venv .venv
source .venv/bin/activate
python -m pip install --index-url https://repo.amd.com/rocm/whl/gfx110X-dgpu/ "rocm[libraries,devel]"
rocminfo
amd-smi version
python -m pip install --index-url https://repo.amd.com/rocm/whl/gfx110X-dgpu/ torch torchvision torchaudio
```


Along with the additional directory appearing in https://repo.amd.com/rocm/whl, the output of rocminfo does not match the example output of the documentation, which is why I suspected that files have been changed. Running rocminfo on my PC shows "Runtime Ext Version:     1.15" as shown below. The documentation shows 1.14.

```
(.venv) root@rocm:~# rocminfo
ROCk module version 6.16.6 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.15
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES
~~~
```

Unlike ROCm repo on https://repo.radeon.com/, I can't see the dates of the files on https://repo.amd.com/rocm/whl. So, I can't tell for sure whether the files have changed for sure.

---

### 评论 #11 — tcgu-amd (2026-01-09T19:06:14Z)

Right, no worries! It is kind of confusing right now because there are 3 channels from where you can install torch+rocm. Typically TheRock releases through the nightlies channel, then there's the official channels from AMD and Pytorch. I just wanted to make sure I am on the same page regarding which version you are using. I have been using TheRock releases from the nightlies by the way. I am gonna try to see if I can reproduce the issue with the offical AMD version which seems to be what you are using.

By the way thanks for catching the docs error. We will get it updated!

---

### 评论 #12 — briansp2020 (2026-01-09T19:27:48Z)

How do I install from TheRock nightly release? Is there a documentation describing the steps?

---

### 评论 #13 — tcgu-amd (2026-01-09T19:40:25Z)

@briansp2020 yes of course. Please see this page for details https://github.com/ROCm/TheRock/blob/main/RELEASES.md

---

### 评论 #14 — briansp2020 (2026-01-09T20:06:06Z)

Ok. The instruction was in the document.  But the workaround no longer seems to work with the nightly... I removed .venv and installed nightly again and I get the following.
BTW, nightly installs torch 2.11. So, I needed to update fastai/setting.ini and remove torch version upper limit.

```
(.venv) root@rocm:~# MIOPEN_FIND_MODE=5  PYTORCH_MIOPEN_SUGGEST_NHWC=0  MIOPEN_RNN_DYNAMIC_FORCE=0 python /pwd/Downloads/quickstart.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.121374    0.001729    0.000677    01:03
epoch     train_loss  valid_loss  error_rate  time
0         0.013823    0.001234    0.000677    01:18
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.465913    0.413062    0.811720  01:09
epoch     train_loss  valid_loss  accuracy  time
0         0.290088    0.252294    0.898360  02:53
1         0.240169    0.201879    0.921880  02:49
```

---

### 评论 #15 — tcgu-amd (2026-01-09T20:51:47Z)

@briansp2020 Thanks! Yeah there are other torch+rocm combinations available from index [rocm.nightlies.amd.com/v2-staging/gfx110X-all](https://rocm.nightlies.amd.com/v2-staging/gfx110X-all). For example if you want to install the latest nightly build today for torch2.9+rocm7.11 you can use python -m pip install --index-url https://rocm.nightlies.amd.com/v2-staging/gfx110X-all torch==2.9.1+rocm7.11.0a20260109 torchvision==0.24.0+rocm7.11.0a20260109 torchaudio==2.9.1+rocm7.11.0a20260109 (This is mainly for developer testing purposes so is not in the instructions)

By the way, can you try running with MIOPEN_ENABLE_LOGGING_CMD=1, then in the logs, grep for NHWC/nhwc and see if there's any results both with and without the PYTORCH_MIOPEN_SUGGEST_NHWC=0 var? This will ultimately confirm if the env vars have effects or not. Thanks! 

---

### 评论 #16 — briansp2020 (2026-01-09T22:25:57Z)

Using nightly build,

```
(.venv) root@rocm:~# MIOPEN_ENABLE_LOGGING_CMD=1 MIOPEN_FIND_MODE=5  python /pwd/Downloads/quickstart.py >& NHWC__.log
(.venv) root@rocm:~# MIOPEN_ENABLE_LOGGING_CMD=1 MIOPEN_FIND_MODE=5  PYTORCH_MIOPEN_SUGGEST_NHWC=0 python /pwd/Downloads/quickstart.py >& NHWC_0.log
```

[NHWC__.log](https://github.com/user-attachments/files/24536370/NHWC__.log)
[NHWC_0.log](https://github.com/user-attachments/files/24536369/NHWC_0.log)

---

### 评论 #17 — tcgu-amd (2026-01-12T19:09:10Z)

@briansp2020 Thanks for the confirmation! Yeah so in both cases the NHWC has been turned off by default, which means the performance degradation is likely caused by other reasons. 

I did find something puzzling though -- I tried rerun the reproducer with torch-2.9+ROCm6.4 installed from the official PyTorch source (since TheRock releases does not go that far back), and also see the slower performance numbers now. If you have the chance, would you be able to let me know if you see the same thing on your side as well? 

---

### 评论 #18 — briansp2020 (2026-01-12T21:29:43Z)

Looking at the result below, it seems some went wrong with the image stuff went going from PyTorch 2.7.1 to 2.9.1 and the text stuff when going from ROCm 6 to ROCm7.

PyTorch from the docker hub
```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

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
epoch     train_loss  valid_loss  error_rate  time
0         0.106654    0.000779    0.000677    00:32
epoch     train_loss  valid_loss  error_rate  time
0         0.021216    0.005605    0.000677    00:45
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.469877    0.403338    0.817240  01:08
epoch     train_loss  valid_loss  accuracy  time
0         0.290214    0.228511    0.909600  02:14
1         0.244349    0.203322    0.920640  02:10
```

Installed 2.9.1 in the same docker
```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python -m venv .venv
root@rocm:~# source .venv/bin/activate
((.venv) ) root@rocm:~# pip3 install torch torchvision --index-url https://download.pytorch.org/whl/rocm6.4
((.venv) ) root@rocm:~# pip install -e "fastai[dev]"
~~~
((.venv) ) root@rocm:~# python /pwd/Downloads/quickstart.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/root/.venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.117098    0.002021    0.001353    01:06
epoch     train_loss  valid_loss  error_rate  time
0         0.013265    0.000227    0.000000    01:20
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.456002    0.398176    0.820160  01:10
epoch     train_loss  valid_loss  accuracy  time
0         0.290643    0.226509    0.910400  02:15
1         0.237398    0.205041    0.920600  02:14
```

---

### 评论 #19 — tcgu-amd (2026-01-12T21:32:42Z)

@briansp2020, thanks! That's good, we have isolated what's going on to PyTorch specifically. I will try 2.7.1 and report back. 

---

### 评论 #20 — tcgu-amd (2026-01-14T18:49:50Z)

Hi @briansp2020, so after bit of debugging, I think I have tracked down the issue to the linear layer performance. I created this simple test script to see what's the performance on torch 2.9.1 versus torch 2.7.1

```
import torch
import torch.nn.functional as F

# Test the exact same tensor shapes as your hook output
input1 = torch.randn(64, 14, 14, 384, device='cuda', requires_grad=True)
weight1 = torch.randn(1000, 384, device='cuda')
bias1 = torch.randn(1000, device='cuda')

input2 = torch.randn(64, 14, 14, 1536, device='cuda', requires_grad=True)
weight2 = torch.randn(1000, 1536, device='cuda')
bias2 = torch.randn(1000, device='cuda')

# Test without torch.compile
torch._dynamo.config.suppress_errors = True

print("Testing linear operations...")
with torch.profiler.profile() as prof:
    for _ in range(100):
        out1 = F.linear(input1, weight1, bias1)
        out2 = F.linear(input2, weight2, bias2)

print(prof.key_averages().table(sort_by="cuda_time_total"))
```
So the problem is with hipDeviceSynchronize, which looks like this on 2.9.1
`hipDeviceSynchronize        97.96%        1.536s`

and this on 2.7.1
`hipDeviceSynchronize        66.44%     248.776ms`

Which is quite puzzling because both are using the same rocm 7.11. I will be diving into the python/rocm interface layer to see if any change from 2.9.1 might have caused this. 

---

### 评论 #21 — tcgu-amd (2026-01-16T16:48:56Z)

Hi @briansp2020, can you try running with the reproducer again with `DISABLE_ADDMM_CUDA_LT=1`?

So I have found out that the slow down came from the addmm kernel, which the newer python version forces selection from hipblaslt. That causes the slow down. The env variable above should disable that change. 

Please let me know if that works. Thanks! 

---

### 评论 #22 — tcgu-amd (2026-01-16T19:43:54Z)

Just to summarize the finding so far,

After profiling most of the performance issue seem to come from the Linear layers. 

Here's the amount of time each part of the model spends with pytorch 2.7.1+rocm7.11

<img width="592" height="95" alt="Image" src="https://github.com/user-attachments/assets/c9f4690a-e63f-4dbe-8961-a7811de8ca37" />

Heres the same result with pytorch2.9.1 + rocm 7.11

<img width="607" height="91" alt="Image" src="https://github.com/user-attachments/assets/ab73129b-baa2-4b1c-805d-dbf3e8599420" />

With a simple test 
```
import torch
import torch.nn.functional as F

import torch.cuda.tunable
# Test the exact same tensor shapes as your hook output
input1 = torch.randn(64, 14, 14, 384, device='cuda', requires_grad=True)
weight1 = torch.randn(1000, 384, device='cuda')
bias1 = torch.randn(1000, device='cuda')

# Test without torch.compile
torch._dynamo.config.suppress_errors = True

print("Testing linear operations...")
with torch.profiler.profile(
    # activiies=[torch.profiler.ProfilerActivity.CUDA],
    # record_shapes=True,
    # with_stack=True,
    # profile_memory=True
) as prof:
    for _ in range(100):
        out1 = F.linear(input1, weight1, bias1)

print(prof.key_averages().table(sort_by="cuda_time_total"))
```
to break down the runtime of a single Linear layer we have the following distribution for 2.7.1

<img width="2362" height="676" alt="Image" src="https://github.com/user-attachments/assets/4403e754-d6af-4862-be0f-3853d31dc6a9" />

for 2.9.1:

<img width="2368" height="612" alt="Image" src="https://github.com/user-attachments/assets/e8e01347-d366-4c7d-ad2f-c8ad0a35d2b8" />

As we can see, 2.7.1 and 2.9.1 seems to be choosing different kernels. In particular, 2.9.1 seems to be using hipblaslt as the backend. More details on how backend is selected for ADDMM can be found here https://github.com/pytorch/pytorch/blob/83506e5107bc8789615cebbc7eee1c8ddf1f4d90/aten/src/ATen/native/cuda/Blas.cpp.

After setting env var `DISABLE_ADDMM_CUDA_LT=1` to disable hipblaslt, we can see the performance of 2.9.1 is now close to that of 2.7.1

<img width="2363" height="672" alt="Image" src="https://github.com/user-attachments/assets/75b8ad14-56d2-4610-9e7d-50ef35631e7f" />

Running the original reproducer with the env var set on 2.9.1 is now

<img width="650" height="122" alt="Image" src="https://github.com/user-attachments/assets/10d97bb9-c8d1-49a1-b010-89d95452b042" />

---

### 评论 #23 — briansp2020 (2026-01-16T21:59:55Z)

Ok. DISABLE_ADDMM_CUDA_LT=1 seems to resolve performance issue in image related stuff for both pytorch 2.9.1 and 2.11.0a0+rocm7.11.0a20260109 nightly.

Did you figure out what's causing slowdown in text processing that happens when running ROCM 7+

---

### 评论 #24 — tcgu-amd (2026-01-16T22:10:22Z)

> Ok. DISABLE_ADDMM_CUDA_LT=1 seems to resolve performance issue in image related stuff for both pytorch 2.9.1 and 2.11.0a0+rocm7.11.0a20260109 nightly.
> 
> Did you figure out what's causing slowdown in text processing that happens when running ROCM 7+

Awesome! No the text processing one is still in investigation...

---

### 评论 #25 — tcgu-amd (2026-01-20T17:18:56Z)

Hi @briansp2020, I been struggling a little bit. So far I have tried 2.9+7.11, 2.7+7.11, 2.9 + 6.4, 2.7+6.4, and all of them seem to have the same slower performance numbers. I don't really know why I can't reproduce the run time you are seeing...

Can you try running this script and show me the results? Thanks!

```
from fastai.vision.all import *
from fastai.text.all import *
from fastai.collab import *
from fastai.tabular.all import *


import torch
torch.backends.cudnn.enabled=False
if torch.cuda.is_available():
    print("CUDA is available! PyTorch can use your GPU.")
    print(f"Number of GPUs available: {torch.cuda.device_count()}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. PyTorch will use the CPU.")


import time
import torch
from collections import defaultdict

class SimpleProfiler:
    def __init__(self, model):
        self.model = model
        self.times = defaultdict(list)
        self.original_forwards = {}

    def __enter__(self):
        self._wrap_all_modules(self.model)
        return self

    def _wrap_all_modules(self, module, prefix=""):
        # Get module type and name
        module_type = module.__class__.__name__
        module_name = f"{module_type}:{prefix}" if prefix else module_type

        # Only wrap if it has a forward method and isn't a container
        if hasattr(module, 'forward') and module_type not in ['ModuleList', 'Sequential']:
            original_forward = module.forward
            self.original_forwards[module] = original_forward

            def timed_forward(*args, **kwargs):
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                start = time.time()
                result = original_forward(*args, **kwargs)
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                elapsed = time.time() - start

                self.times[module_name].append(elapsed)
                return result

            module.forward = timed_forward

        # Recursively wrap children
        for name, child in module.named_children():
            child_prefix = f"{prefix}.{name}" if prefix else name
            self._wrap_all_modules(child, child_prefix)

    def __exit__(self, *args):
        # Restore all original forward methods
        for module, original_forward in self.original_forwards.items():
            module.forward = original_forward

    def summary(self):
        print("\n" + "="*70)
        print(f"{'Module':<40} {'Total(ms)':>15} {'Calls':>10}")
        print("="*70)

        # Sort by total time
        sorted_times = sorted(
            [(name, sum(times)*1000, len(times)) for name, times in self.times.items()],
            key=lambda x: x[1],
            reverse=True
        )

        total_time = sum(total for _, total, _ in sorted_times)

        for name, total_ms, calls in sorted_times:
            percentage = (total_ms / total_time * 100) if total_time > 0 else 0
            print(f"{name:<40} {total_ms:>15.3f} {calls:>10} ({percentage:>5.1f}%)")

        print("="*70)
        print(f"{'TOTAL':<40} {total_time:>15.3f}")

print("Training text processing model")
dls = TextDataLoaders.from_folder(untar_data(URLs.IMDB), valid='test')
learn = text_classifier_learner(dls, AWD_LSTM, drop_mult=0.5, metrics=accuracy)
with SimpleProfiler(learn) as prof:
    learn.fine_tune(2, 1e-2)
prof.summary()
learn.predict("I really liked that movie!")
``` 

---

### 评论 #26 — briansp2020 (2026-01-22T03:11:39Z)

I just ran my script and yours on rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1 & rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1. Relevant output below. Full output attached. Each scripts were run 2 times since the first runs are usually slower.

BTW, I upgraded the kernel modules to 7.2. So, even though I'm using the same docker image as before, the setup is slightly different. I don't think it matters though.

Just noticed that your script has "torch.backends.cudnn.enabled=False". I'm running your script again with the line commented out. Will report the result soon.

```
rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python /pwd/Downloads/quickstart.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/venv/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.111695    0.001465    0.000677    01:08
epoch     train_loss  valid_loss  error_rate  time
0         0.011377    0.002479    0.000677    02:05
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.464019    0.388568    0.827200  01:10
epoch     train_loss  valid_loss  accuracy  time
0         0.296903    0.229999    0.907760  02:57
1         0.257182    0.203736    0.920200  02:52

root@rocm:~# python /pwd/Downloads/reproduce.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.466178    0.390924    0.827600  01:44
epoch     train_loss  valid_loss  accuracy  time
0         0.285804    0.248698    0.894640  03:22
1         0.239210    0.200639    0.921760  03:23

======================================================================
Module                                         Total(ms)      Calls
======================================================================
SentenceEncoder:0                             315294.264       2343 ( 25.2%)
AWD_LSTM:0.module                             313438.121      11397 ( 25.0%)
WeightDropout:0.module.rnns.1                 139969.831      11397 ( 11.2%)
LSTM:0.module.rnns.1.module                   139011.662      11397 ( 11.1%)
WeightDropout:0.module.rnns.0                  94958.773      11397 (  7.6%)
LSTM:0.module.rnns.0.module                    93980.278      11397 (  7.5%)
WeightDropout:0.module.rnns.2                  74529.836      11397 (  6.0%)
LSTM:0.module.rnns.2.module                    74002.286      11397 (  5.9%)
EmbeddingDropout:0.module.encoder_dp            2012.062      11397 (  0.2%)
PoolingLinearClassifier:1                       1834.465       2343 (  0.1%)
LinBnDrop:1.layers.0                             605.594       2343 (  0.0%)
RNNDropout:0.module.hidden_dps.0                 418.545      11397 (  0.0%)
RNNDropout:0.module.hidden_dps.1                 416.625      11397 (  0.0%)
RNNDropout:0.module.input_dp                     288.867      11397 (  0.0%)
Linear:1.layers.0.2                              275.025       2343 (  0.0%)
LinBnDrop:1.layers.1                             262.272       2343 (  0.0%)
BatchNorm1d:1.layers.0.0                         149.028       2343 (  0.0%)
BatchNorm1d:1.layers.1.0                         103.796       2343 (  0.0%)
Linear:1.layers.1.2                               87.494       2343 (  0.0%)
ReLU:1.layers.0.3                                 81.589       2343 (  0.0%)
Dropout:1.layers.0.1                              45.761       2343 (  0.0%)
Dropout:1.layers.1.1                              35.985       2343 (  0.0%)
======================================================================
TOTAL                                        1251802.159
```

[rocm711_pytorch271.log](https://github.com/user-attachments/files/24784852/rocm711_pytorch271.log)

```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python /pwd/Downloads/quickstart.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.122361    0.000476    0.000000    00:33
epoch     train_loss  valid_loss  error_rate  time
0         0.026743    0.000337    0.000000    00:46
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.467524    0.428242    0.797360  01:10
epoch     train_loss  valid_loss  accuracy  time
0         0.299340    0.236283    0.906560  02:14
1         0.228708    0.200251    0.923040  02:14

root@rocm:~# python /pwd/Downloads/reproduce.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.461173    0.415904    0.809880  01:42
epoch     train_loss  valid_loss  accuracy  time
0         0.303722    0.267476    0.887120  03:21
1         0.236491    0.204611    0.919840  03:23

======================================================================
Module                                         Total(ms)      Calls
======================================================================
SentenceEncoder:0                             313640.511       2343 ( 25.2%)
AWD_LSTM:0.module                             311916.346      11419 ( 25.0%)
WeightDropout:0.module.rnns.1                 138871.381      11419 ( 11.1%)
LSTM:0.module.rnns.1.module                   137916.850      11419 ( 11.1%)
WeightDropout:0.module.rnns.0                  94404.715      11419 (  7.6%)
LSTM:0.module.rnns.0.module                    93424.136      11419 (  7.5%)
WeightDropout:0.module.rnns.2                  74665.608      11419 (  6.0%)
LSTM:0.module.rnns.2.module                    74177.720      11419 (  6.0%)
EmbeddingDropout:0.module.encoder_dp            2016.337      11419 (  0.2%)
PoolingLinearClassifier:1                       1862.211       2343 (  0.1%)
LinBnDrop:1.layers.0                             593.724       2343 (  0.0%)
RNNDropout:0.module.hidden_dps.0                 417.844      11419 (  0.0%)
RNNDropout:0.module.hidden_dps.1                 413.707      11419 (  0.0%)
RNNDropout:0.module.input_dp                     287.224      11419 (  0.0%)
Linear:1.layers.0.2                              272.791       2343 (  0.0%)
LinBnDrop:1.layers.1                             267.971       2343 (  0.0%)
BatchNorm1d:1.layers.0.0                         139.503       2343 (  0.0%)
BatchNorm1d:1.layers.1.0                         100.221       2343 (  0.0%)
Linear:1.layers.1.2                               91.719       2343 (  0.0%)
ReLU:1.layers.0.3                                 75.868       2343 (  0.0%)
Dropout:1.layers.0.1                              48.012       2343 (  0.0%)
Dropout:1.layers.1.1                              37.995       2343 (  0.0%)
======================================================================
TOTAL                                        1245642.393
```

[rocm644_pytorch271.log](https://github.com/user-attachments/files/24784853/rocm644_pytorch271.log)

---

### 评论 #27 — briansp2020 (2026-01-22T03:29:31Z)

Hope this helps. It's weird that the time reported by the profiler is the same even though the time reported by fastai library is different. Maybe not all the function calls are profiled?
Let me know if you want me to try anything else.

```
rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python /pwd/Downloads/reproduce.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.459417    0.398543    0.819720  01:10
epoch     train_loss  valid_loss  accuracy  time
0         0.296214    0.253523    0.892040  02:56
1         0.234967    0.198465    0.923080  02:52

======================================================================
Module                                         Total(ms)      Calls
======================================================================
SentenceEncoder:0                             208642.544       2343 ( 25.3%)
AWD_LSTM:0.module                             206890.602      11407 ( 25.1%)
WeightDropout:0.module.rnns.1                  95963.323      11407 ( 11.6%)
LSTM:0.module.rnns.1.module                    95019.337      11407 ( 11.5%)
WeightDropout:0.module.rnns.0                  81599.547      11407 (  9.9%)
LSTM:0.module.rnns.0.module                    80661.362      11407 (  9.8%)
WeightDropout:0.module.rnns.2                  25331.700      11407 (  3.1%)
LSTM:0.module.rnns.2.module                    24811.330      11407 (  3.0%)
EmbeddingDropout:0.module.encoder_dp            2021.228      11407 (  0.2%)
PoolingLinearClassifier:1                       1723.838       2343 (  0.2%)
LinBnDrop:1.layers.0                             571.825       2343 (  0.1%)
RNNDropout:0.module.hidden_dps.0                 430.478      11407 (  0.1%)
RNNDropout:0.module.hidden_dps.1                 425.017      11407 (  0.1%)
RNNDropout:0.module.input_dp                     289.652      11407 (  0.0%)
Linear:1.layers.0.2                              272.857       2343 (  0.0%)
LinBnDrop:1.layers.1                             243.664       2343 (  0.0%)
BatchNorm1d:1.layers.0.0                         132.930       2343 (  0.0%)
BatchNorm1d:1.layers.1.0                          93.959       2343 (  0.0%)
Linear:1.layers.1.2                               82.592       2343 (  0.0%)
ReLU:1.layers.0.3                                 73.409       2343 (  0.0%)
Dropout:1.layers.0.1                              45.302       2343 (  0.0%)
Dropout:1.layers.1.1                              35.391       2343 (  0.0%)
======================================================================
TOTAL                                         825361.888
```

```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python /pwd/Downloads/reproduce.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.457415    0.403787    0.817720  01:09
epoch     train_loss  valid_loss  accuracy  time
0         0.284956    0.263510    0.883040  02:11
1         0.225485    0.208444    0.918760  02:12

======================================================================
Module                                         Total(ms)      Calls
======================================================================
SentenceEncoder:0                             205833.566       2343 ( 25.3%)
AWD_LSTM:0.module                             204241.467      11402 ( 25.1%)
WeightDropout:0.module.rnns.1                  94414.400      11402 ( 11.6%)
LSTM:0.module.rnns.1.module                    93476.140      11402 ( 11.5%)
WeightDropout:0.module.rnns.0                  80780.934      11402 (  9.9%)
LSTM:0.module.rnns.0.module                    79827.059      11402 (  9.8%)
WeightDropout:0.module.rnns.2                  25143.936      11402 (  3.1%)
LSTM:0.module.rnns.2.module                    24634.223      11402 (  3.0%)
EmbeddingDropout:0.module.encoder_dp            2046.004      11402 (  0.3%)
PoolingLinearClassifier:1                       1759.634       2343 (  0.2%)
LinBnDrop:1.layers.0                             562.588       2343 (  0.1%)
RNNDropout:0.module.hidden_dps.0                 414.766      11402 (  0.1%)
RNNDropout:0.module.hidden_dps.1                 408.275      11402 (  0.1%)
RNNDropout:0.module.input_dp                     289.293      11402 (  0.0%)
Linear:1.layers.0.2                              269.768       2343 (  0.0%)
LinBnDrop:1.layers.1                             251.399       2343 (  0.0%)
BatchNorm1d:1.layers.0.0                         126.483       2343 (  0.0%)
BatchNorm1d:1.layers.1.0                          94.426       2343 (  0.0%)
Linear:1.layers.1.2                               86.116       2343 (  0.0%)
ReLU:1.layers.0.3                                 69.293       2343 (  0.0%)
Dropout:1.layers.0.1                              47.124       2343 (  0.0%)
Dropout:1.layers.1.1                              36.928       2343 (  0.0%)
======================================================================
TOTAL                                         814813.821
```

---

### 评论 #28 — tcgu-amd (2026-01-22T17:32:04Z)

@briansp2020 Hmm that's some really interesting results. The profiler scripts I wrote wraps around each module so it should have caught everything module wise. If there's any additional overhead then perhaps it came from somewhere else? 

---

### 评论 #29 — shdwchn10 (2026-01-22T22:49:58Z)

Hi! I noticed bad performance on 7900XTX in Comfy UI with [this Wan workflow](https://github.com/kijai/ComfyUI-WanVideoWrapper) and found this issue.

My test setup:
- Almalinux 10 podman rootless containers with ROCm 7.2.0 (from AMD repo)
- host Fedora 43
- kernel 6.18.5

Tested pytorch versions: 2.7.1, 2.8.0 and 2.9.1. Python WHLs from https://repo.radeon.com/rocm/manylinux/

Exact versions:
```
# 2.9.1
torch-2.9.1+rocm7.2.0.lw.git7e1940d4-cp312-cp312-linux_x86_64.whl
torchvision-0.24.0+rocm7.2.0.gitb919bd0c-cp312-cp312-linux_x86_64.whl
triton-3.5.1+rocm7.2.0.gita272dfa8-cp312-cp312-linux_x86_64.whl
torchaudio-2.9.0+rocm7.2.0.gite3c6ee2b-cp312-cp312-linux_x86_64.whl
# 2.8.0
torch-2.8.0+rocm7.2.0.lw.gitbf943426-cp312-cp312-linux_x86_64.whl
torchvision-0.23.0+rocm7.2.0.git824e8c87-cp312-cp312-linux_x86_64.whl
triton-3.4.0+rocm7.2.0.git0cace8d2-cp312-cp312-linux_x86_64.whl
torchaudio-2.8.0+rocm7.2.0.git6e1c7fe9-cp312-cp312-linux_x86_64.whl
# 2.7.1
torch-2.7.1+rocm7.2.0.lw.git262e50d5-cp312-cp312-linux_x86_64.whl
torchvision-0.22.1+rocm7.2.0.git59a3e1f9-cp312-cp312-linux_x86_64.whl
triton-3.3.1+rocm7.2.0.git28a7371e-cp312-cp312-linux_x86_64.whl
torchaudio-2.7.1+rocm7.2.0.git95c61b41-cp312-cp312-linux_x86_64.whl
```

Test results:

2.7.1
```
# python quickstart.py                                                                                
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
epoch     train_loss  valid_loss  error_rate  time    
0         0.111150    0.000474    0.000000    00:30                                                                                                     
epoch     train_loss  valid_loss  error_rate  time    
0         0.011026    0.002171    0.001353    00:42                                                                                                     
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    
0         0.474352    0.420004    0.807320  01:05                                                                                                         
epoch     train_loss  valid_loss  accuracy  time    
0         0.294236    0.225080    0.911440  02:40                                                                                                         
1         0.251551    0.201922    0.921640  02:39

# python reproduce.py 
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    
0         0.463609    0.392159    0.824600  01:34                                                                                                         
epoch     train_loss  valid_loss  accuracy  time    
0         0.293628    0.234241    0.908640  03:06                                                                                                         
1         0.230213    0.203654    0.920360  03:06                                                                                                         

======================================================================
Module                                         Total(ms)      Calls
======================================================================
SentenceEncoder:0                             279604.174       2343 ( 25.2%)
AWD_LSTM:0.module                             277617.702      11439 ( 25.1%)
WeightDropout:0.module.rnns.1                 122915.052      11439 ( 11.1%)
LSTM:0.module.rnns.1.module                   121906.449      11439 ( 11.0%)
WeightDropout:0.module.rnns.0                  84593.525      11439 (  7.6%)
LSTM:0.module.rnns.0.module                    83573.007      11439 (  7.5%)
WeightDropout:0.module.rnns.2                  65506.721      11439 (  5.9%)
LSTM:0.module.rnns.2.module                    64890.282      11439 (  5.9%)
EmbeddingDropout:0.module.encoder_dp            2107.413      11439 (  0.2%)
PoolingLinearClassifier:1                       1906.501       2343 (  0.2%)
LinBnDrop:1.layers.0                             615.312       2343 (  0.1%)
RNNDropout:0.module.hidden_dps.1                 490.268      11439 (  0.0%)
RNNDropout:0.module.hidden_dps.0                 486.016      11439 (  0.0%)
RNNDropout:0.module.input_dp                     314.092      11439 (  0.0%)
LinBnDrop:1.layers.1                             313.472       2343 (  0.0%)
Linear:1.layers.0.2                              258.012       2343 (  0.0%)
BatchNorm1d:1.layers.0.0                         149.714       2343 (  0.0%)
BatchNorm1d:1.layers.1.0                         117.068       2343 (  0.0%)
Linear:1.layers.1.2                              105.350       2343 (  0.0%)
ReLU:1.layers.0.3                                 85.085       2343 (  0.0%)
Dropout:1.layers.0.1                              49.682       2343 (  0.0%)
Dropout:1.layers.1.1                              43.344       2343 (  0.0%)
======================================================================
TOTAL                                        1107648.242
```

2.8.0
```
# python quickstart.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
epoch     train_loss  valid_loss  error_rate  time    
0         0.113108    0.000661    0.000000    01:12                                                                                                     
epoch     train_loss  valid_loss  error_rate  time    
0         0.013208    0.002179    0.000677    01:16                                                                                                     
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    
0         0.467827    0.405800    0.816120  01:08                                                                                                         
epoch     train_loss  valid_loss  accuracy  time    
0         0.295399    0.228146    0.907440  02:58                                                                                                         
1         0.231875    0.204652    0.919360  02:44

# python reproduce.py 
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    
0         0.466128    0.396319    0.821840  01:35                                                                                                         
epoch     train_loss  valid_loss  accuracy  time    
0         0.298856    0.257947    0.897400  03:07                                                                                                         
1         0.224143    0.203870    0.920240  03:07                                                                                                         

======================================================================
Module                                         Total(ms)      Calls
======================================================================
SentenceEncoder:0                             281993.509       2343 ( 25.2%)
AWD_LSTM:0.module                             279888.278      11418 ( 25.1%)
WeightDropout:0.module.rnns.1                 123663.322      11418 ( 11.1%)
LSTM:0.module.rnns.1.module                   122649.973      11418 ( 11.0%)
WeightDropout:0.module.rnns.0                  85177.778      11418 (  7.6%)
LSTM:0.module.rnns.0.module                    84135.468      11418 (  7.5%)
WeightDropout:0.module.rnns.2                  66460.831      11418 (  5.9%)
LSTM:0.module.rnns.2.module                    65844.120      11418 (  5.9%)
PoolingLinearClassifier:1                       2099.974       2343 (  0.2%)
EmbeddingDropout:0.module.encoder_dp            2035.417      11418 (  0.2%)
LinBnDrop:1.layers.0                             677.685       2343 (  0.1%)
RNNDropout:0.module.hidden_dps.1                 493.426      11418 (  0.0%)
RNNDropout:0.module.hidden_dps.0                 490.031      11418 (  0.0%)
RNNDropout:0.module.input_dp                     332.535      11418 (  0.0%)
LinBnDrop:1.layers.1                             322.659       2343 (  0.0%)
Linear:1.layers.0.2                              263.825       2343 (  0.0%)
BatchNorm1d:1.layers.0.0                         172.369       2343 (  0.0%)
BatchNorm1d:1.layers.1.0                         120.232       2343 (  0.0%)
ReLU:1.layers.0.3                                112.775       2343 (  0.0%)
Linear:1.layers.1.2                              107.726       2343 (  0.0%)
Dropout:1.layers.0.1                              52.115       2343 (  0.0%)
Dropout:1.layers.1.1                              45.048       2343 (  0.0%)
======================================================================
TOTAL                                        1117139.098
```

2.9.1
```
# python quickstart.py 
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
epoch     train_loss  valid_loss  error_rate  time    
0         0.113565    0.003304    0.002030    01:10                                                                                                     
epoch     train_loss  valid_loss  error_rate  time    
0         0.015539    0.004178    0.001353    01:15                                                                                                     
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    
0         0.464574    0.395773    0.819200  01:07                                                                                                         
epoch     train_loss  valid_loss  accuracy  time    
0         0.293715    0.241127    0.902040  02:59                                                                                                         
1         0.228030    0.203988    0.920440  02:47

# python reproduce.py 
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: AMD Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time    
0         0.471113    0.396306    0.825320  01:35                                                                                                         
epoch     train_loss  valid_loss  accuracy  time    
0         0.302817    0.233473    0.906120  03:08                                                                                                         
1         0.233061    0.199446    0.922560  03:07                                                                                                         

======================================================================
Module                                         Total(ms)      Calls
======================================================================
SentenceEncoder:0                             282509.896       2343 ( 25.2%)
AWD_LSTM:0.module                             280314.492      11422 ( 25.0%)
WeightDropout:0.module.rnns.1                 123918.614      11422 ( 11.1%)
LSTM:0.module.rnns.1.module                   122884.383      11422 ( 11.0%)
WeightDropout:0.module.rnns.0                  85458.984      11422 (  7.6%)
LSTM:0.module.rnns.0.module                    84411.713      11422 (  7.5%)
WeightDropout:0.module.rnns.2                  66345.020      11422 (  5.9%)
LSTM:0.module.rnns.2.module                    65702.344      11422 (  5.9%)
PoolingLinearClassifier:1                       2451.952       2343 (  0.2%)
EmbeddingDropout:0.module.encoder_dp            2078.821      11422 (  0.2%)
LinBnDrop:1.layers.0                             803.930       2343 (  0.1%)
RNNDropout:0.module.hidden_dps.1                 494.787      11422 (  0.0%)
RNNDropout:0.module.hidden_dps.0                 487.017      11422 (  0.0%)
RNNDropout:0.module.input_dp                     320.238      11422 (  0.0%)
LinBnDrop:1.layers.1                             317.087       2343 (  0.0%)
Linear:1.layers.0.2                              259.652       2343 (  0.0%)
BatchNorm1d:1.layers.0.0                         219.194       2343 (  0.0%)
ReLU:1.layers.0.3                                200.061       2343 (  0.0%)
BatchNorm1d:1.layers.1.0                         118.594       2343 (  0.0%)
Linear:1.layers.1.2                              106.973       2343 (  0.0%)
Dropout:1.layers.0.1                              50.628       2343 (  0.0%)
Dropout:1.layers.1.1                              43.487       2343 (  0.0%)
======================================================================
TOTAL                                        1119497.865
```

I'm ready to do more tests if needed

---

### 评论 #30 — tcgu-amd (2026-01-23T15:04:23Z)

Hi @shdwchn10 did you try the workaround mentioned earlier in the thread so far? i.e. `DISABLE_ADDMM_CUDA_LT=1` and `TORCH_MIOPEN_SUGGEST_NHCW=0`?  These resolved the regression issues for the CV model. Currently the effort has been on investigating the LSTM performance different which I highly doubt is related to WAN performance. 

---

### 评论 #31 — tcgu-amd (2026-01-23T20:23:37Z)

Hi @briansp2020, can you try running this one on 2.7.1+6.4.4?

```
from fastai.vision.all import *
from fastai.text.all import *
from fastai.collab import *
from fastai.tabular.all import *


import torch
torch.backends.cudnn.enabled=False
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

with torch.profiler.profile() as prof:
    learn.fine_tune(1)

print(prof.key_averages().table(sort_by="cuda_time_total"))
```
Sorry for asking so much, this bug has been really elusive...

---

### 评论 #32 — briansp2020 (2026-01-23T20:43:30Z)

@tcgu-amd I'm more than happy to help. 
Are we back to trouble shooting the issue with image processing?

```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1 

bsp2020@rocm:~$ docker exec -it pt6 bash
root@rocm:/var/lib/jenkins# cd
root@rocm:~# python /pwd/Downloads/reproduce2.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ConvNeXt_Small_Weights.IMAGENET1K_V1`. You can also use `weights=ConvNeXt_Small_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
epoch     train_loss  valid_loss  error_rate  time
0         0.117965    0.003566    0.001353    00:24
epoch     train_loss  valid_loss  error_rate  time
0         0.011261    0.000964    0.000677    00:38
[W123 20:39:33.992599336 collection.cpp:1110] Warning: ROCTracer produced duplicate flow start: 1 (function operator())
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                                   Name    Self CPU %      Self CPU   CPU total %     CPU total  CPU time avg     Self CUDA   Self CUDA %    CUDA total  CUDA time avg    # of Calls
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                           aten::linear         0.01%      11.440ms         0.37%     333.587ms      19.431us       0.000us         0.00%        7.429s     432.724us         17168
                                            aten::addmm         0.21%     195.153ms         0.29%     266.440ms      15.951us        7.419s        24.51%        7.419s     444.128us         16704
    autograd::engine::evaluate_function: AddmmBackward0         0.02%      22.394ms         0.26%     241.640ms      18.240us       0.000us         0.00%        7.033s     530.901us         13248
                                               aten::mm         0.29%     264.177ms         0.35%     318.474ms      15.114us        6.721s        22.20%        6.721s     318.950us         21072
                                         AddmmBackward0         0.01%      13.229ms         0.20%     184.075ms      13.895us       0.000us         0.00%        6.692s     505.157us         13248
autograd::engine::evaluate_function: ConvolutionBack...         0.02%      17.749ms         8.75%        7.981s       1.098ms       0.000us         0.00%        5.155s     709.330us          7268
                                   ConvolutionBackward0         0.01%       4.626ms         8.71%        7.944s       1.093ms       0.000us         0.00%        4.794s     659.599us          7268
                             aten::convolution_backward         0.04%      35.972ms         8.70%        7.939s       1.092ms        3.446s        11.38%        4.794s     659.599us          7268
                                     aten::_convolution         0.02%      14.588ms         0.82%     748.933ms      80.704us       0.000us         0.00%        4.136s     445.728us          9280
                                           aten::conv2d         0.00%       4.443ms         0.84%     768.711ms      82.835us       0.000us         0.00%        4.136s     445.658us          9280
                                      aten::convolution         0.01%      12.869ms         0.84%     763.606ms      82.285us       0.000us         0.00%        4.136s     445.658us          9280
Cijk_Alik_Bljk_SB_MT128x256x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us        3.030s        10.01%        3.030s     711.714us          4257
Cijk_Alik_Bljk_SB_MT128x256x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us        2.846s         9.40%        2.846s     607.625us          4683
                                aten::_conv_depthwise2d         0.03%      23.830ms         0.05%      41.247ms       4.939us        2.467s         8.15%        2.467s     295.392us          8352
void at::native::(anonymous namespace)::conv_depthwi...         0.00%       0.000us         0.00%       0.000us       0.000us        2.467s         8.15%        2.467s     479.516us          5145
void at::native::(anonymous namespace)::conv_depthwi...         0.00%       0.000us         0.00%       0.000us       0.000us        2.214s         7.31%        2.214s     521.137us          4248
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us        2.083s         6.88%        2.083s      63.921us         32588
Cijk_Ailk_Bljk_SB_MT128x128x8_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us        2.013s         6.65%        2.013s     568.505us          3540
Cijk_Ailk_Bljk_SB_MT128x64x8_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us        1.940s         6.41%        1.940s     608.919us          3186
                                            aten::copy_        47.70%       43.516s        47.71%       43.532s       1.084ms        1.655s         5.47%        1.655s      41.228us         40154
     autograd::engine::evaluate_function: GeluBackward0         0.01%       9.175ms         0.04%      34.363ms       5.188us       0.000us         0.00%        1.562s     235.772us          6624
                                          GeluBackward0         0.00%       3.404ms         0.03%      23.922ms       3.611us       0.000us         0.00%        1.562s     235.772us          6624
                                    aten::gelu_backward         0.02%      18.439ms         0.02%      20.019ms       3.022us        1.562s         5.16%        1.562s     235.772us          6624
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us        1.562s         5.16%        1.562s     367.645us          4248
                                            aten::clone         0.02%      13.780ms         0.15%     136.322ms       3.769us       0.000us         0.00%        1.553s      42.928us         36168
                                       aten::contiguous         0.01%       7.399ms         0.15%     139.747ms       3.949us       0.000us         0.00%        1.542s      43.573us         35384
                                      aten::thnn_conv2d         0.00%     765.687us         0.72%     655.604ms     706.470us       0.000us         0.00%        1.253s       1.350ms           928
                             aten::_slow_conv2d_forward         0.49%     451.151ms         0.72%     654.710ms     705.507us        1.227s         4.05%        1.253s       1.350ms           928
                                       aten::layer_norm         0.00%       3.517ms         0.13%     120.341ms      12.968us       0.000us         0.00%        1.244s     134.069us          9280
                                aten::native_layer_norm         0.05%      44.848ms         0.13%     116.332ms      12.536us     919.348ms         3.04%        1.244s     134.069us          9280
void at::native::(anonymous namespace)::conv_depthwi...         0.00%       0.000us         0.00%       0.000us       0.000us        1.232s         4.07%        1.232s       1.317ms           936
                               hipExtModuleLaunchKernel         2.38%        2.170s         2.40%        2.188s      24.456us       0.000us         0.00%        1.127s      12.593us         89488
autograd::engine::evaluate_function: NativeLayerNorm...         0.02%      19.356ms         0.16%     147.834ms      20.086us       0.000us         0.00%        1.103s     149.868us          7360
                               NativeLayerNormBackward0         0.01%       5.731ms         0.14%     125.968ms      17.115us       0.000us         0.00%        1.103s     149.868us          7360
                       aten::native_layer_norm_backward         0.06%      52.724ms         0.13%     119.431ms      16.227us     766.804ms         2.53%        1.103s     149.868us          7360
                                             aten::gelu         0.03%      29.386ms         0.04%      36.477ms       4.368us     985.524ms         3.26%     985.524ms     117.999us          8352
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us     985.524ms         3.26%     985.524ms     191.550us          5145
void at::native::(anonymous namespace)::vectorized_l...         0.00%       0.000us         0.00%       0.000us       0.000us     919.348ms         3.04%     919.348ms     160.810us          5717
                            aten::_slow_conv2d_backward         8.47%        7.730s         8.58%        7.830s      12.159ms     844.438ms         2.79%     879.813ms       1.366ms           644
                                             aten::add_         0.23%     205.288ms         0.24%     216.138ms       2.294us     734.516ms         2.43%     734.516ms       7.797us         94210
                                              aten::mul         0.10%      90.965ms         0.11%     102.312ms       3.273us     674.817ms         2.23%     674.817ms      21.584us         31264
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us     611.057ms         2.02%     611.057ms      34.401us         17763
Cijk_Ailk_Bljk_SB_MT64x64x32_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us     454.331ms         1.50%     454.331ms       1.283ms           354
                                              aten::sum         0.08%      75.413ms         0.09%      80.245ms       5.893us     414.112ms         1.37%     414.112ms      30.414us         13616
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us     408.050ms         1.35%     408.050ms      10.587us         38541
Cijk_Alik_Bljk_SB_MT128x256x8_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us     406.730ms         1.34%     406.730ms     954.764us           426
Cijk_Ailk_Bjlk_SB_MT128x64x16_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us     406.195ms         1.34%     406.195ms     578.626us           702
void at::native::reduce_kernel<128, 4, at::native::R...         0.00%       0.000us         0.00%       0.000us       0.000us     396.989ms         1.31%     396.989ms     108.289us          3666
Cijk_Ailk_Bjlk_SB_MT128x64x8_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us     395.157ms         1.31%     395.157ms     562.902us           702
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us     385.538ms         1.27%     385.538ms      86.833us          4440
      autograd::engine::evaluate_function: MulBackward0         0.02%      18.643ms         0.11%     104.654ms       8.011us       0.000us         0.00%     382.055ms      29.245us         13064
Cijk_Ailk_Bjlk_SB_MT16x16x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us     367.789ms         1.22%     367.789ms       2.358ms           156
Cijk_Alik_Bljk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us     361.018ms         1.19%     361.018ms     847.460us           426
                                           MulBackward0         0.01%       6.372ms         0.06%      53.618ms       4.104us       0.000us         0.00%     350.155ms      26.803us         13064
Cijk_Ailk_Bljk_SB_MT128x64x8_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us     345.137ms         1.14%     345.137ms      37.952us          9094
Cijk_Ailk_Bljk_SB_MT32x16x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us     340.676ms         1.13%     340.676ms      37.499us          9085
Cijk_Ailk_Bljk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us     326.926ms         1.08%     326.926ms      35.950us          9094
void at::native::(anonymous namespace)::cuComputePar...         0.00%       0.000us         0.00%       0.000us       0.000us     302.922ms         1.00%     302.922ms      64.178us          4720
Cijk_Alik_Bljk_SB_MT128x256x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us     271.203ms         0.90%     271.203ms     636.626us           426
Cijk_Ailk_Bljk_SB_MT128x256x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us     251.361ms         0.83%     251.361ms     710.060us           354
void at::native::(anonymous namespace)::layer_norm_g...         0.00%       0.000us         0.00%       0.000us       0.000us     230.229ms         0.76%     230.229ms      62.939us          3658
void at::native::(anonymous namespace)::cuComputeGra...         0.00%       0.000us         0.00%       0.000us       0.000us     220.821ms         0.73%     220.821ms     227.650us           970
void at::native::col2im_kernel<float, float>(long, f...         0.00%       0.000us         0.00%       0.000us       0.000us     201.765ms         0.67%     201.765ms       8.906us         22656
Cijk_Ailk_Bljk_SB_MT128x64x8_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us     200.975ms         0.66%     200.975ms     567.725us           354
Cijk_Ailk_Bljk_SB_MT256x64x8_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us     196.737ms         0.65%     196.737ms     555.753us           354
Cijk_Ailk_Bjlk_SB_MT32x32x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us     193.527ms         0.64%     193.527ms       1.241ms           156
Cijk_Ailk_Bljk_SB_MT128x128x8_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us     192.502ms         0.64%     192.502ms     543.792us           354
void at::native::im2col_kernel<float>(long, float co...         0.00%       0.000us         0.00%       0.000us       0.000us     172.248ms         0.57%     172.248ms       4.004us         43024
Cijk_Ailk_Bjlk_SB_MT32x16x32_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us     164.628ms         0.54%     164.628ms      21.799us          7552
                                    hipMemcpyWithStream        29.25%       26.686s        29.33%       26.762s      33.286ms       0.000us         0.00%     152.209ms     189.315us           804
Cijk_Ailk_Bjlk_SB_MT64x32x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us     128.730ms         0.43%     128.730ms      17.046us          7552
Cijk_Alik_Bljk_SB_MT128x128x8_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us     101.484ms         0.34%     101.484ms      60.988us          1664
Cijk_Alik_Bljk_SB_MT16x16x32_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us      97.712ms         0.32%      97.712ms      58.721us          1664
Cijk_Ailk_Bjlk_SB_MT32x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us      88.527ms         0.29%      88.527ms      11.722us          7552
                                             aten::mul_         0.22%     198.252ms         0.23%     209.889ms       2.245us      86.391ms         0.29%      86.391ms       0.924us         93472
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      86.391ms         0.29%      86.391ms       2.279us         37900
                                              aten::add         0.15%     135.079ms         0.16%     142.012ms       3.492us      85.380ms         0.28%      85.380ms       2.099us         40668
                                               aten::to         0.00%       2.101ms        47.64%       43.461s      11.621ms       0.000us         0.00%      68.527ms      18.323us          3740
                                         aten::_to_copy         0.01%       4.727ms        47.63%       43.459s      16.754ms       0.000us         0.00%      68.527ms      26.418us          2594
Cijk_Ailk_Bljk_SB_MT128x64x8_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us      68.432ms         0.23%      68.432ms       7.525us          9094
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      63.761ms         0.21%      63.761ms      74.313us           858
                              aten::adaptive_max_pool2d         0.00%       3.175ms         0.00%       4.196ms      18.088us      58.978ms         0.19%      61.445ms     264.848us           232
                           Memcpy HtoD (Host -> Device)         0.00%       0.000us         0.00%       0.000us       0.000us      59.219ms         0.20%      59.219ms      92.820us           638
void at::native::(anonymous namespace)::adaptivemaxp...         0.00%       0.000us         0.00%       0.000us       0.000us      58.978ms         0.19%      58.978ms     415.340us           142
                        torch::autograd::AccumulateGrad         0.03%      25.992ms         0.13%     114.457ms       2.880us       0.000us         0.00%      42.634ms       1.073us         39744
autograd::engine::evaluate_function: torch::autograd...         0.03%      29.738ms         0.16%     147.053ms       3.700us       0.000us         0.00%      42.626ms       1.073us         39744
Cijk_Ailk_Bjlk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us      41.900ms         0.14%      41.900ms     537.174us            78
Cijk_Ailk_Bjlk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us      41.779ms         0.14%      41.779ms     535.624us            78
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      41.601ms         0.14%      41.601ms       1.961us         21213
                                         aten::addcdiv_         0.09%      81.560ms         0.09%      86.463ms       2.175us      36.623ms         0.12%      36.623ms       0.921us         39744
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      36.623ms         0.12%      36.623ms       2.166us         16908
                                         aten::addcmul_         0.10%      90.935ms         0.10%      95.732ms       2.409us      28.498ms         0.09%      28.498ms       0.717us         39744
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      28.498ms         0.09%      28.498ms       1.685us         16908
                                              aten::div         5.24%        4.780s         5.26%        4.798s     117.735us      27.391ms         0.09%      28.465ms       0.698us         40756
                                             aten::sqrt         0.10%      90.476ms         0.11%     104.664ms       2.633us      28.166ms         0.09%      28.166ms       0.709us         39744
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      28.166ms         0.09%      28.166ms       1.666us         16908
                                            aten::fill_         0.16%     142.165ms         0.16%     143.306ms       3.405us      27.864ms         0.09%      27.864ms       0.662us         42084
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      27.864ms         0.09%      27.864ms       1.519us         18348
                                            aten::zero_         0.02%      16.424ms         0.17%     155.164ms       3.736us       0.000us         0.00%      27.581ms       0.664us         41528
                                        hipLaunchKernel         2.12%        1.933s         2.15%        1.966s       5.453us       0.000us         0.00%      26.671ms       0.074us        360516
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
Self CPU time total: 91.236s
Self CUDA time total: 30.270s

```


---

### 评论 #33 — tcgu-amd (2026-01-23T21:27:23Z)

@briansp2020 Sorry I accidentally sent the wrong script... No we are not back to vision. 

```
from fastai.vision.all import *
from fastai.text.all import *
from fastai.collab import *
from fastai.tabular.all import *


import torch
torch.backends.cudnn.enabled=False
if torch.cuda.is_available():
    print("CUDA is available! PyTorch can use your GPU.")
    print(f"Number of GPUs available: {torch.cuda.device_count()}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. PyTorch will use the CPU.")

path = untar_data(URLs.PETS)/'images'

print("Training text processing model")
dls = TextDataLoaders.from_folder(untar_data(URLs.IMDB), valid='test')
learn = text_classifier_learner(dls, AWD_LSTM, drop_mult=0.5, metrics=accuracy)
with torch.profiler.profile() as prof:
    learn.fine_tune(2, 1e-2)
learn.predict("I really liked that movie!")
print(prof.key_averages().table(sort_by="cuda_time_total"))
```
Can you give this one a try instead? 

---

### 评论 #34 — briansp2020 (2026-01-23T23:56:33Z)

The script keeps crashing... Is torch profiler known to be flaky or should I suspect my hardware has a problem? I was able to run it once before. But after rebooting my machine, it isn't generating the profile summary...
Also, I noticed that cudnn is disabled. Is this intentional?

```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

bsp2020@rocm:~$ docker exec -it pt6 bash
root@rocm:/var/lib/jenkins# cd
root@rocm:~# cat /pwd/Downloads/profile_fastai_text.py
from fastai.vision.all import *
from fastai.text.all import *
from fastai.collab import *
from fastai.tabular.all import *


import torch
torch.backends.cudnn.enabled=False
if torch.cuda.is_available():
    print("CUDA is available! PyTorch can use your GPU.")
    print(f"Number of GPUs available: {torch.cuda.device_count()}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. PyTorch will use the CPU.")

path = untar_data(URLs.PETS)/'images'

print("Training text processing model")
dls = TextDataLoaders.from_folder(untar_data(URLs.IMDB), valid='test')
learn = text_classifier_learner(dls, AWD_LSTM, drop_mult=0.5, metrics=accuracy)
with torch.profiler.profile() as prof:
    learn.fine_tune(2, 1e-2)
learn.predict("I really liked that movie!")
print(prof.key_averages().table(sort_by="cuda_time_total"))
root@rocm:~# python /pwd/Downloads/profile_fastai_text.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.464369    0.404515    0.817360  01:39
epoch     train_loss  valid_loss  accuracy  time
0         0.296480    0.239009    0.902400  03:25
1         0.232641    0.203910    0.920800  03:31
Killed
root@rocm:~#
```

---

### 评论 #35 — briansp2020 (2026-01-24T01:54:58Z)

Enabling the cudnn (MIOpen) allows the profiler to finish.

```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python /pwd/Downloads/profile_fastai_text.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.464369    0.396223    0.819920  01:11
epoch     train_loss  valid_loss  accuracy  time
0         0.286062    0.220390    0.912040  02:16
1         0.236459    0.202951    0.919400  02:18
[W124 01:45:40.691498451 collection.cpp:1110] Warning: ROCTracer produced duplicate flow start: 2 (function operator())
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                                   Name    Self CPU %      Self CPU   CPU total %     CPU total  CPU time avg     Self CUDA   Self CUDA %    CUDA total  CUDA time avg    # of Calls
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                             aten::lstm         0.02%      69.409ms        21.47%       74.304s       2.167ms       0.000us         0.00%        8.950s     261.041us         34284
                                       aten::miopen_rnn        20.66%       71.522s        21.44%       74.207s       2.164ms        8.734s        93.32%        8.950s     261.041us         34284
Cijk_Alik_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us        5.570s        59.51%        5.570s      80.954us         68800
Cijk_Alik_Bljk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us     797.583ms         8.52%     797.583ms       1.511ms           528
Cijk_Alik_Bljk_SB_MT32x8x8_SN_1LDSB0_APM1_ABV0_ACED0...         0.00%       0.000us         0.00%       0.000us       0.000us     481.573ms         5.15%     481.573ms      38.643us         12462
Cijk_Alik_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us     455.784ms         4.87%     455.784ms      13.404us         34003
Cijk_Alik_Bljk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us     322.226ms         3.44%     322.226ms     631.815us           510
                                       LSTMFwdHidUpdate         0.00%       0.000us         0.00%       0.000us       0.000us     311.045ms         3.32%     311.045ms       2.553us        121812
Cijk_Alik_Bljk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us     290.958ms         3.11%     290.958ms     595.007us           489
                                         Op2dTensorLite         0.00%       0.000us         0.00%       0.000us       0.000us     187.945ms         2.01%     187.945ms      50.360us          3732
                                              aten::mul         0.07%     241.972ms         0.07%     252.542ms       5.043us     155.772ms         1.66%     155.772ms       3.111us         50074
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us     155.327ms         1.66%     155.327ms      62.506us          2485
                                    hipMemcpyWithStream         1.86%        6.431s         1.87%        6.476s       5.898ms       0.000us         0.00%     144.273ms     131.397us          1098
                                SubTensorOpWithScalar1d         0.00%       0.000us         0.00%       0.000us       0.000us     140.816ms         1.50%     140.816ms      25.155us          5598
                                              aten::cat         0.28%     973.636ms         0.28%     979.508ms       5.041us     128.168ms         1.37%     128.168ms       0.660us        194292
                                            aten::copy_        26.60%       92.059s        26.60%       92.065s     344.888us     109.412ms         1.17%     109.412ms       0.410us        266942
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us     100.924ms         1.08%     100.924ms      26.255us          3844
                         Memcpy DtoD (Device -> Device)         0.00%       0.000us         0.00%       0.000us       0.000us      85.639ms         0.92%      85.639ms       8.966us          9552
                                          aten::dropout         0.01%      19.037ms         0.06%     196.211ms       8.682us       0.000us         0.00%      80.514ms       3.563us         22599
                                   aten::native_dropout         0.03%     112.414ms         0.05%     177.034ms       8.741us      80.514ms         0.86%      80.514ms       3.975us         20253
void at::native::(anonymous namespace)::fused_dropou...         0.00%       0.000us         0.00%       0.000us       0.000us      80.514ms         0.86%      80.514ms      38.524us          2090
Cijk_Alik_Bljk_SB_MT32x8x8_SN_1LDSB0_APM1_ABV0_ACED0...         0.00%       0.000us         0.00%       0.000us       0.000us      63.804ms         0.68%      63.804ms      10.163us          6278
                             SubTensorOpWithSubTensor2d         0.00%       0.000us         0.00%       0.000us       0.000us      62.056ms         0.66%      62.056ms      11.550us          5373
                                            aten::fill_         0.09%     309.733ms         0.09%     313.866ms       2.646us      36.617ms         0.39%      36.617ms       0.309us        118641
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      36.617ms         0.39%      36.617ms       8.918us          4106
                                            aten::zero_         0.02%      60.511ms         0.11%     369.544ms       3.210us       0.000us         0.00%      36.389ms       0.316us        115127
                                            aten::clone         0.02%      70.708ms         0.13%     446.019ms       5.826us       0.000us         0.00%      33.777ms       0.441us         76561
Cijk_Alik_Bljk_SB_MT128x256x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us      21.126ms         0.23%      21.126ms     660.198us            32
                                      aten::masked_fill         0.01%      17.401ms         0.02%      83.962ms      13.443us       0.000us         0.00%      21.016ms       3.365us          6246
                                        aten::embedding         0.01%      37.630ms         0.09%     310.249ms      27.148us       0.000us         0.00%      14.588ms       1.277us         11428
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us      13.570ms         0.14%      13.570ms       3.636us          3732
                                               aten::to         0.01%      22.911ms        26.46%       91.585s       1.682ms       0.000us         0.00%      13.565ms       0.249us         54463
                                         aten::_to_copy         0.01%      35.264ms        26.45%       91.562s       2.268ms       0.000us         0.00%      13.565ms       0.336us         40369
                                               aten::mm         0.12%     418.391ms         0.14%     495.014ms      52.852us      13.381ms         0.14%      13.381ms       1.429us          9366
                                     aten::index_select         0.02%      65.402ms         0.04%     148.875ms      13.027us      10.984ms         0.12%      10.984ms       0.961us         11428
void at::native::(anonymous namespace)::indexSelectL...         0.00%       0.000us         0.00%       0.000us       0.000us      10.975ms         0.12%      10.975ms      17.673us           621
                                              aten::pow         0.01%      37.900ms         0.01%      45.570ms      11.685us      10.520ms         0.11%      10.520ms       2.697us          3900
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      10.520ms         0.11%      10.520ms      46.964us           224
                                     aten::masked_fill_         0.01%      24.200ms         0.01%      27.895ms       4.466us      10.226ms         0.11%      10.226ms       1.637us          6246
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us      10.226ms         0.11%      10.226ms      45.651us           224
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us      10.055ms         0.11%      10.055ms      60.574us           166
                                       aten::bernoulli_         0.04%     132.622ms         0.04%     138.604ms       5.803us       9.667ms         0.10%       9.667ms       0.405us         23884
void at::native::(anonymous namespace)::distribution...         0.00%       0.000us         0.00%       0.000us       0.000us       9.667ms         0.10%       9.667ms       3.885us          2488
                                             aten::mean         0.02%      59.234ms         0.02%      63.056ms      10.660us       8.907ms         0.10%       9.470ms       1.601us          5915
                                              aten::sum         0.03%     116.220ms         0.04%     125.168ms       6.764us       9.104ms         0.10%       9.401ms       0.508us         18504
                           Memcpy HtoD (Host -> Device)         0.00%       0.000us         0.00%       0.000us       0.000us       8.999ms         0.10%       8.999ms      24.791us           363
                                           aten::linear         0.00%       5.151ms         0.04%     132.542ms      28.285us       0.000us         0.00%       8.915ms       1.903us          4686
                                           aten::matmul         0.00%       3.673ms         0.03%     114.425ms      24.419us       0.000us         0.00%       8.915ms       1.903us          4686
void at::native::reduce_kernel<512, 1, at::native::R...         0.00%       0.000us         0.00%       0.000us       0.000us       8.228ms         0.09%       8.228ms      24.489us           336
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us       8.069ms         0.09%       8.069ms      13.793us           585
                                       aten::contiguous         0.00%      11.178ms         0.05%     176.102ms       5.674us       0.000us         0.00%       8.041ms       0.259us         31035
Cijk_Alik_Bljk_SB_MT128x64x16_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us       7.894ms         0.08%       7.894ms      70.485us           112
                                              aten::sub         0.01%      45.655ms         0.01%      49.479ms       4.696us       6.153ms         0.07%       6.153ms       0.584us         10536
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       6.022ms         0.06%       6.022ms       1.906us          3160
                                             aten::div_         0.04%     133.224ms         0.04%     137.960ms       5.108us       5.592ms         0.06%       5.592ms       0.207us         27007
void at::native::reduce_kernel<512, 1, at::native::R...         0.00%       0.000us         0.00%       0.000us       0.000us       5.568ms         0.06%       5.568ms       6.582us           846
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us       5.563ms         0.06%       5.563ms      49.673us           112
Cijk_Alik_Bljk_SB_MT16x16x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us       5.398ms         0.06%       5.398ms      14.870us           363
                                              aten::max         0.01%      32.157ms         0.01%      34.472ms       7.361us       5.164ms         0.06%       5.164ms       1.103us          4683
void at::native::reduce_kernel<128, 4, at::native::R...         0.00%       0.000us         0.00%       0.000us       0.000us       5.164ms         0.06%       5.164ms      46.111us           112
       autograd::engine::evaluate_function: MmBackward0         0.00%       5.419ms         0.12%     407.936ms     174.332us       0.000us         0.00%       4.466ms       1.908us          2340
                                            MmBackward0         0.00%       7.569ms         0.12%     402.485ms     172.002us       0.000us         0.00%       4.466ms       1.908us          2340
Cijk_Alik_Bljk_SB_MT128x128x8_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us       4.215ms         0.05%       4.215ms     162.110us            26
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us       3.610ms         0.04%       3.610ms       6.191us           583
                                          aten::reshape         0.01%      33.759ms         0.04%     127.335ms       7.049us       0.000us         0.00%       3.600ms       0.199us         18064
void at::native::reduce_kernel<128, 4, at::native::R...         0.00%       0.000us         0.00%       0.000us       0.000us       3.535ms         0.04%       3.535ms      31.564us           112
                                             aten::add_         0.06%     221.084ms         0.06%     221.232ms       2.588us       3.479ms         0.04%       3.479ms       0.041us         85469
Cijk_Alik_Bljk_SB_MT128x128x8_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us       3.341ms         0.04%       3.341ms      92.816us            36
Cijk_Alik_Bljk_SB_MT128x256x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us       3.043ms         0.03%       3.043ms     253.571us            12
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       3.030ms         0.03%       3.030ms       1.940us          1562
Cijk_Alik_Bljk_SB_MT128x256x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us       2.998ms         0.03%       2.998ms     428.248us             7
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       2.970ms         0.03%       2.970ms       1.657us          1792
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us       2.761ms         0.03%       2.761ms       5.814us           475
                                       aten::batch_norm         0.00%       5.208ms         0.03%     116.374ms      24.834us       0.000us         0.00%       2.730ms       0.583us          4686
                           aten::_batch_norm_impl_index         0.00%       9.005ms         0.03%     111.160ms      23.722us       0.000us         0.00%       2.730ms       0.583us          4686
                                aten::native_batch_norm         0.02%      70.383ms         0.03%      99.066ms      21.141us       2.730ms         0.03%       2.730ms       0.583us          4686
Cijk_Alik_Bljk_SB_MT128x128x16_SN_1LDSB0_APM1_ABV0_A...         0.00%       0.000us         0.00%       0.000us       0.000us       2.669ms         0.03%       2.669ms     133.453us            20
                                             aten::mul_         0.03%     113.660ms         0.03%     113.741ms       2.430us       2.530ms         0.03%       2.530ms       0.054us         46800
                                               aten::ne         0.03%      87.383ms         0.03%      87.710ms       7.675us       2.435ms         0.03%       2.435ms       0.213us         11428
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us       2.435ms         0.03%       2.435ms       3.915us           622
void at::native::elementwise_kernel<512, 1, at::nati...         0.00%       0.000us         0.00%       0.000us       0.000us       2.430ms         0.03%       2.430ms       3.307us           735
                                        aten::new_zeros         0.00%      16.713ms         0.03%     120.318ms       5.897us       0.000us         0.00%       2.348ms       0.115us         20403
Cijk_Alik_Bljk_SB_MT128x128x8_SN_1LDSB0_APM1_ABV0_AC...         0.00%       0.000us         0.00%       0.000us       0.000us       1.982ms         0.02%       1.982ms     180.177us            11
                                        hipLaunchKernel         0.07%     252.939ms         0.07%     255.140ms       6.921us       0.000us         0.00%       1.812ms       0.049us         36866
Cijk_Alik_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us       1.769ms         0.02%       1.769ms      40.212us            44
Cijk_Ailk_Bljk_SB_MT128x64x8_SN_1LDSB0_APM1_ABV0_ACE...         0.00%       0.000us         0.00%       0.000us       0.000us       1.728ms         0.02%       1.728ms      15.426us           112
autograd::engine::evaluate_function: torch::autograd...         0.00%      16.436ms         0.02%      75.402ms       4.394us       0.000us         0.00%       1.540ms       0.090us         17160
                        torch::autograd::AccumulateGrad         0.01%      18.221ms         0.02%      58.913ms       3.433us       0.000us         0.00%       1.540ms       0.090us         17160
                                            aten::index         0.01%      42.050ms         4.84%       16.756s       7.152ms       1.269ms         0.01%       1.518ms       0.648us          2343
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us       1.497ms         0.02%       1.497ms      13.482us           111
                                             aten::item         0.00%      11.975ms        34.29%      118.700s       4.265ms       0.000us         0.00%       1.461ms       0.053us         27830
                              aten::_local_scalar_dense        34.28%      118.655s        34.29%      118.687s       4.265ms       1.461ms         0.02%       1.461ms       0.053us         27830
autograd::engine::evaluate_function: NativeBatchNorm...         0.00%       6.364ms         0.01%      41.801ms      17.864us       0.000us         0.00%       1.399ms       0.598us          2340
                               NativeBatchNormBackward0         0.00%       3.519ms         0.01%      35.402ms      15.129us       0.000us         0.00%       1.399ms       0.598us          2340
                       aten::native_batch_norm_backward         0.01%      22.330ms         0.01%      31.847ms      13.610us       1.399ms         0.01%       1.399ms       0.598us          2340
                                         aten::addcmul_         0.02%      53.740ms         0.02%      53.778ms       3.134us       1.395ms         0.01%       1.395ms       0.081us         17160
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       1.395ms         0.01%       1.395ms       2.076us           672
                                         aten::addcdiv_         0.01%      40.756ms         0.01%      40.785ms       2.377us       1.342ms         0.01%       1.342ms       0.078us         17160
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       1.342ms         0.01%       1.342ms       1.997us           672
void at::native::index_elementwise_kernel<128, 4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       1.269ms         0.01%       1.269ms      11.330us           112
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
Self CPU time total: 346.145s
Self CUDA time total: 9.359s
```

---

### 评论 #36 — briansp2020 (2026-01-24T05:00:08Z)

Ran the profiler with cudnn enabled. The only big thing that stands out is aten::copy_. It is much slower in 7.1.1 compared to 6.4.4. It is about 72s slower and that difference is pretty close to the total time difference.
Hope this helps.

```
rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python /pwd/Downloads/profile_fastai_text.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.462429    0.399084    0.819240  01:09
epoch     train_loss  valid_loss  accuracy  time
0         0.300151    0.227894    0.908240  02:13
1         0.232843    0.202197    0.920800  02:15
[W124 04:30:08.735920979 collection.cpp:1110] Warning: ROCTracer produced duplicate flow start: 2 (function operator())
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                                   Name    Self CPU %      Self CPU   CPU total %     CPU total  CPU time avg     Self CUDA   Self CUDA %    CUDA total  CUDA time avg    # of Calls
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                       aten::lift_fresh         0.00%      10.910us         0.00%      10.910us       1.364us       0.000us         0.00%       0.000us       0.000us             8
                                               aten::to         0.01%      21.286ms        26.81%       88.463s       1.625ms       0.000us         0.00%      14.405ms       0.265us         54439
                                         aten::_to_copy         0.01%      48.970ms        26.80%       88.441s       2.192ms       0.000us         0.00%      14.405ms       0.357us         40345
                                    aten::empty_strided         0.04%     129.541ms         0.04%     131.055ms       1.123us       0.000us         0.00%       0.000us       0.000us        116676
                                            aten::copy_        26.69%       88.076s        26.95%       88.934s     333.567us     110.349ms         1.18%     110.349ms       0.414us        266614
                                               aten::ge         0.00%      29.075us         0.00%      38.612us       9.653us       0.000us         0.00%       0.000us       0.000us             4
                                              aten::all         0.00%      29.858us         0.00%      38.282us       9.570us       0.000us         0.00%       0.000us       0.000us             4
                                       aten::as_strided         0.07%     225.415ms         0.07%     225.415ms       0.201us       0.000us         0.00%       0.000us       0.000us       1119254
                                            aten::fill_         0.09%     306.192ms         0.10%     314.114ms       2.652us      36.418ms         0.39%      36.418ms       0.308us        118429
                                       aten::is_nonzero         0.00%       1.231ms         0.00%       3.428ms       1.462us       0.000us         0.00%       0.000us       0.000us          2344
                                             aten::item         0.00%      13.709ms        34.36%      113.393s       4.078ms       0.000us         0.00%       1.494ms       0.054us         27806
                              aten::_local_scalar_dense        32.65%      107.744s        34.36%      113.379s       4.078ms       1.494ms         0.02%       1.494ms       0.054us         27806
                                           aten::cumsum         0.00%      20.639us         0.00%      20.969us       5.242us       0.000us         0.00%       0.000us       0.000us             4
                                            aten::empty         0.15%     508.908ms         0.15%     509.441ms       0.729us       0.000us         0.00%       0.000us       0.000us        699069
                                          aten::detach_         0.00%       6.078ms         0.00%       7.786ms       0.454us       0.000us         0.00%       0.000us       0.000us         17164
                                                detach_         0.00%       1.709ms         0.00%       1.709ms       0.100us       0.000us         0.00%       0.000us       0.000us         17164
                                   hipStreamIsCapturing         0.00%     913.921us         0.00%     913.921us       0.099us       0.000us         0.00%       0.000us       0.000us          9190
                                              hipMalloc         0.00%       2.318ms         0.00%       2.318ms      79.926us       0.000us         0.00%       0.000us       0.000us            29
                                    hipMemcpyWithStream         1.96%        6.478s         1.96%        6.478s       5.784ms       0.000us         0.00%       0.000us       0.000us          1120
                           Memcpy HtoD (Host -> Device)         0.00%       0.000us         0.00%       0.000us       0.000us       9.766ms         0.10%       9.766ms      25.634us           381
                aten::_has_compatible_shallow_copy_type         0.00%       8.368us         0.00%       8.368us       0.091us       0.000us         0.00%       0.000us       0.000us            92
                                            aten::clone         0.02%      69.536ms         0.13%     440.860ms       5.759us       0.000us         0.00%      34.468ms       0.450us         76545
                                         hipMemcpyAsync         0.00%      12.332ms         0.00%      12.332ms       1.371us       0.000us         0.00%       0.000us       0.000us          8998
                         Memcpy DtoD (Device -> Device)         0.00%       0.000us         0.00%       0.000us       0.000us      85.758ms         0.92%      85.758ms       8.928us          9606
                                        aten::new_zeros         0.00%      14.242ms         0.03%     113.641ms       5.589us       0.000us         0.00%       2.190ms       0.108us         20333
                                        aten::new_empty         0.01%      20.685ms         0.02%      74.049ms       1.678us       0.000us         0.00%       0.000us       0.000us         44121
                                            aten::zero_         0.02%      57.325ms         0.11%     367.680ms       3.200us       0.000us         0.00%      36.184ms       0.315us        114915
                                        hipLaunchKernel         0.08%     254.944ms         0.08%     254.944ms       6.830us       0.000us         0.00%       0.000us       0.000us         37329
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      36.418ms         0.39%      36.418ms       8.904us          4090
                                          aten::random_         0.00%      65.823us         0.00%      65.823us      10.971us       0.000us         0.00%       0.000us       0.000us             6
enumerate(DataLoader)#_MultiProcessingDataLoaderIter...         0.60%        1.970s         0.60%        1.990s     847.180us       0.000us         0.00%       0.000us       0.000us          2349
                                             aten::set_         0.02%      57.993ms         0.02%      57.993ms       0.310us       0.000us         0.00%       0.000us       0.000us        187242
                                            aten::alias         0.01%      40.005ms         0.01%      40.005ms       0.669us       0.000us         0.00%       0.000us       0.000us         59835
                                               aten::le         0.00%      10.301ms         0.01%      16.849ms       7.200us       0.000us         0.00%       0.000us       0.000us          2340
                                          aten::nonzero         0.00%       9.536ms         0.00%      12.546ms       5.361us       0.000us         0.00%       0.000us       0.000us          2340
                                      aten::as_strided_         0.02%      55.260ms         0.02%      55.260ms       1.152us       0.000us         0.00%       0.000us       0.000us         47979
                                              aten::max         0.01%      28.261ms         0.01%      32.569ms       6.955us       5.097ms         0.05%       5.097ms       1.088us          4683
                                               aten::gt         0.00%       4.200ms         0.00%       4.200ms       1.795us       0.000us         0.00%       0.000us       0.000us          2340
                                           aten::select         0.03%      98.417ms         0.04%     124.876ms       0.942us       0.000us         0.00%       0.000us       0.000us        132556
                                             aten::rsub         0.00%       8.432ms         0.01%      37.005ms       7.902us       0.000us         0.00%     343.924us       0.073us          4683
                                              aten::sub         0.01%      38.470ms         0.01%      48.902ms       4.641us       6.319ms         0.07%       6.319ms       0.600us         10536
                                              aten::add         0.01%      48.340ms         0.01%      48.975ms       2.511us       1.205ms         0.01%       1.205ms       0.062us         19506
                                              aten::div         0.03%     102.650ms         0.03%     110.082ms       4.551us       1.128ms         0.01%       1.128ms       0.047us         24189
                                               aten::eq         0.01%      26.704ms         0.01%      35.487ms      10.093us     562.325us         0.01%     562.325us       0.160us          3516
                                            aten::slice         0.11%     352.571ms         0.15%     495.791ms       0.610us       0.000us         0.00%       0.000us       0.000us        812123
                                               aten::ne         0.03%      86.942ms         0.03%      88.226ms       7.736us       2.379ms         0.03%       2.379ms       0.209us         11404
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us     562.325us         0.01%     562.325us       4.725us           119
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us       2.379ms         0.03%       2.379ms       3.837us           620
                                              aten::sum         0.03%     115.482ms         0.04%     124.641ms       6.762us       8.974ms         0.10%       8.974ms       0.487us         18433
void at::native::elementwise_kernel<512, 1, at::nati...         0.00%       0.000us         0.00%       0.000us       0.000us       2.399ms         0.03%       2.399ms       3.238us           741
                                          hipHostMalloc         0.00%      62.978us         0.00%      62.978us      62.978us       0.000us         0.00%       0.000us       0.000us             1
void at::native::reduce_kernel<512, 1, at::native::R...         0.00%       0.000us         0.00%       0.000us       0.000us       5.522ms         0.06%       5.522ms       6.451us           856
                                       aten::bernoulli_         0.04%     125.275ms         0.04%     135.184ms       5.683us       9.300ms         0.10%       9.300ms       0.391us         23788
                                             aten::div_         0.04%     127.658ms         0.04%     134.916ms       5.013us       5.713ms         0.06%       5.713ms       0.212us         26911
void at::native::(anonymous namespace)::distribution...         0.00%       0.000us         0.00%       0.000us       0.000us       9.300ms         0.10%       9.300ms       3.750us          2480
                                              aten::mul         0.07%     233.945ms         0.07%     246.903ms       4.943us     156.526ms         1.68%     156.526ms       3.134us         49950
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       6.178ms         0.07%       6.178ms       1.938us          3188
                                        aten::embedding         0.01%      37.623ms         0.09%     305.436ms      26.783us       0.000us         0.00%      14.692ms       1.288us         11404
                                          aten::reshape         0.01%      32.901ms         0.04%     124.720ms       6.914us       0.000us         0.00%       3.557ms       0.197us         18040
                                             aten::view         0.02%      54.941ms         0.02%      54.941ms       0.291us       0.000us         0.00%       0.000us       0.000us        188782
                                     aten::index_select         0.02%      59.883ms         0.04%     145.892ms      12.793us      11.134ms         0.12%      11.134ms       0.976us         11404
                                          aten::resize_         0.01%      28.191ms         0.01%      28.191ms       0.429us       0.000us         0.00%       0.000us       0.000us         65757
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us     156.067ms         1.67%     156.067ms      63.159us          2471
                                          aten::dropout         0.01%      18.998ms         0.06%     193.978ms       8.611us       0.000us         0.00%      79.692ms       3.538us         22527
                                   aten::native_dropout         0.03%     109.488ms         0.05%     174.981ms       8.671us      79.692ms         0.85%      79.692ms       3.949us         20181
                                       aten::empty_like         0.02%      61.861ms         0.06%     196.085ms       1.366us       0.000us         0.00%       0.000us       0.000us        143529
void at::native::(anonymous namespace)::indexSelectL...         0.00%       0.000us         0.00%       0.000us       0.000us      11.113ms         0.12%      11.113ms      18.041us           616
void at::native::(anonymous namespace)::fused_dropou...         0.00%       0.000us         0.00%       0.000us       0.000us      79.692ms         0.85%      79.692ms      38.021us          2096
                                             aten::lstm         0.02%      70.667ms        22.42%       73.994s       2.163ms       0.000us         0.00%        8.914s     260.550us         34212
                              aten::cudnn_is_acceptable         0.00%       6.657ms         0.00%       6.657ms       0.195us       0.000us         0.00%       0.000us       0.000us         34212
                                       aten::miopen_rnn        21.60%       71.283s        22.40%       73.897s       2.160ms        8.700s        93.30%        8.914s     260.550us         34212
                                        aten::transpose         0.02%      65.384ms         0.03%     102.049ms       0.917us       0.000us         0.00%       0.000us       0.000us        111249
                                                hipInit         0.00%       0.351us         0.00%       0.351us       0.351us       0.000us         0.00%       0.000us       0.000us             1
                            hipGetDevicePropertiesR0600         0.01%      33.298ms         0.01%      33.298ms       0.132us       0.000us         0.00%       0.000us       0.000us        251786
                                              hipMemset         0.00%      17.954us         0.00%      17.954us       8.977us       0.000us         0.00%       0.000us       0.000us             2
                                        Memset (Device)         0.00%       0.000us         0.00%       0.000us       0.000us     781.365us         0.01%     781.365us       3.283us           238
                                            aten::chunk         0.02%      61.130ms         0.26%     855.763ms       4.688us       0.000us         0.00%       0.000us       0.000us        182556
                                            aten::split         0.05%     161.925ms         0.24%     794.633ms       4.353us       0.000us         0.00%       0.000us       0.000us        182556
                                           aten::narrow         0.08%     249.762ms         0.19%     643.208ms       0.873us       0.000us         0.00%       0.000us       0.000us        737151
                                              aten::cat         0.28%     939.592ms         0.29%     966.062ms       4.984us     127.109ms         1.36%     127.109ms       0.656us        193850
                                          aten::view_as         0.01%      35.977ms         0.02%      63.789ms       0.466us       0.000us         0.00%       0.000us       0.000us        136848
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us     100.503ms         1.08%     100.503ms      26.186us          3838
                                  hipDeviceGetAttribute         0.01%      19.291ms         0.01%      19.291ms       0.158us       0.000us         0.00%       0.000us       0.000us        121835
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us      13.385ms         0.14%      13.385ms       3.598us          3720
                                      hipModuleLoadData         0.04%     135.303ms         0.04%     135.303ms       4.832ms       0.000us         0.00%       0.000us       0.000us            28
                               hipExtModuleLaunchKernel         0.07%     232.758ms         0.07%     232.758ms       0.891us       0.000us         0.00%       0.000us       0.000us        261094
                                SubTensorOpWithScalar1d         0.00%       0.000us         0.00%       0.000us       0.000us     149.467ms         1.60%     149.467ms      26.786us          5580
Cijk_Alik_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us       1.391ms         0.01%       1.391ms      39.730us            35
                                         Op2dTensorLite         0.00%       0.000us         0.00%       0.000us       0.000us     196.625ms         2.11%     196.625ms      52.856us          3720
Cijk_Alik_Bljk_SB_MT32x8x8_SN_1LDSB0_APM1_ABV0_ACED0...         0.00%       0.000us         0.00%       0.000us       0.000us     319.657ms         3.43%     319.657ms      38.018us          8408
                                       LSTMFwdHidUpdate         0.00%       0.000us         0.00%       0.000us       0.000us     306.852ms         3.29%     306.852ms       2.523us        121634
                                       aten::transpose_         0.01%      37.115ms         0.03%      90.080ms       1.974us       0.000us         0.00%       0.000us       0.000us         45639
                             SubTensorOpWithSubTensor1d         0.00%       0.000us         0.00%       0.000us       0.000us     261.531us         0.00%     261.531us       1.384us           189
                             SubTensorOpWithSubTensor2d         0.00%       0.000us         0.00%       0.000us       0.000us      64.145ms         0.69%      64.145ms      11.905us          5388
Cijk_Alik_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us        5.678s        60.89%        5.678s      78.066us         72729
Cijk_Alik_Bljk_SB_MT32x8x8_SN_1LDSB0_APM1_ABV0_ACED0...         0.00%       0.000us         0.00%       0.000us       0.000us      42.501ms         0.46%      42.501ms      10.026us          4239
                                           aten::detach         0.01%      24.633ms         0.02%      58.301ms       0.810us       0.000us         0.00%       0.000us       0.000us         71959
                                                 detach         0.01%      33.668ms         0.01%      33.668ms       0.468us       0.000us         0.00%       0.000us       0.000us         71959
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us       2.122ms         0.02%       2.122ms       5.570us           381
                                     aten::_unsafe_view         0.00%       7.213ms         0.00%       7.213ms       0.645us       0.000us         0.00%       0.000us       0.000us         11175
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
Self CPU time total: 329.968s
Self CUDA time total: 9.325s
```

```
rocm/pytorch:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.7.1

root@rocm:~# python /pwd/Downloads/profile_fastai_text.py
CUDA is available! PyTorch can use your GPU.
Number of GPUs available: 1
GPU Name: Radeon RX 7900 XTX
Training text processing model
epoch     train_loss  valid_loss  accuracy  time
0         0.476104    0.425152    0.804680  01:09
epoch     train_loss  valid_loss  accuracy  time
0         0.304068    0.255384    0.895600  02:54
1         0.236443    0.205498    0.918760  02:53
[W124 04:04:47.850070327 collection.cpp:1110] Warning: ROCTracer produced duplicate flow start: 2 (function operator())
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                                   Name    Self CPU %      Self CPU   CPU total %     CPU total  CPU time avg     Self CUDA   Self CUDA %    CUDA total  CUDA time avg    # of Calls
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
                                       aten::lift_fresh         0.00%      13.354us         0.00%      13.354us       1.669us       0.000us         0.00%       0.000us       0.000us             8
                                               aten::to        -0.01%  -28654.039us        38.60%      159.671s       2.933ms       0.000us         0.00%       8.735ms       0.160us         54436
                                         aten::_to_copy        -0.01%  -35718.294us        38.59%      159.631s       3.957ms       0.000us         0.00%       8.735ms       0.217us         40342
                                    aten::empty_strided         0.04%     147.701ms         0.04%     150.489ms       1.290us       0.000us         0.00%       0.000us       0.000us        116655
                                            aten::copy_        38.67%      159.951s        38.72%      160.138s     600.605us      14.988ms         2.95%      14.988ms       0.056us        266627
                                               aten::ge         0.00%      30.897us         0.00%      38.382us       9.595us       0.000us         0.00%       0.000us       0.000us             4
                                              aten::all         0.00%      29.035us         0.00%      36.417us       9.104us       0.000us         0.00%       0.000us       0.000us             4
                                       aten::as_strided         0.06%     238.570ms         0.06%     238.570ms       0.213us       0.000us         0.00%       0.000us       0.000us       1119976
                                            aten::fill_         0.11%     464.775ms         0.11%     471.950ms       3.979us       2.796ms         0.55%       2.796ms       0.024us        118623
                                       aten::is_nonzero         0.00%       1.445ms         0.00%       3.763ms       1.605us       0.000us         0.00%       0.000us       0.000us          2344
                                             aten::item        -0.15%  -612143.741us        27.75%      114.791s       4.129ms       0.000us         0.00%     174.954us       0.006us         27803
                              aten::_local_scalar_dense        26.98%      111.591s        27.75%      114.777s       4.128ms     174.954us         0.03%     174.954us       0.006us         27803
                                           aten::cumsum         0.00%      18.564us         0.00%      18.885us       4.721us       0.000us         0.00%       0.000us       0.000us             4
                                            aten::empty         0.12%     500.107ms         0.12%     500.706ms       0.716us       0.000us         0.00%       0.000us       0.000us        699550
                                          aten::detach_         0.00%       9.293ms         0.00%      10.778ms       0.628us       0.000us         0.00%       0.000us       0.000us         17164
                                                detach_         0.00%       1.485ms         0.00%       1.485ms       0.087us       0.000us         0.00%       0.000us       0.000us         17164
                                   hipStreamIsCapturing         0.00%       1.212ms         0.00%       1.212ms       0.094us       0.000us         0.00%       0.000us       0.000us         12924
                                              hipMalloc         0.00%       3.521ms         0.00%       3.521ms     121.413us       0.000us         0.00%       0.000us       0.000us            29
                                    hipMemcpyWithStream         2.29%        9.489s         2.29%        9.489s       6.238ms       0.000us         0.00%       0.000us       0.000us          1521
                           Memcpy HtoD (Host -> Device)         0.00%       0.000us         0.00%       0.000us       0.000us       8.538ms         1.68%       8.538ms     304.914us            28
                aten::_has_compatible_shallow_copy_type         0.00%       6.070us         0.00%       6.070us       0.066us       0.000us         0.00%       0.000us       0.000us            92
                                            aten::clone         0.02%      66.124ms         0.11%     441.776ms       5.768us       0.000us         0.00%       1.565ms       0.020us         76597
                                         hipMemcpyAsync         0.00%      18.286ms         0.00%      18.306ms       1.460us       0.000us         0.00%       0.000us       0.000us         12539
                         Memcpy DtoD (Device -> Device)         0.00%       0.000us         0.00%       0.000us       0.000us       5.931ms         1.17%       5.931ms       9.536us           622
                                        aten::new_zeros         0.00%      15.445ms         0.06%     260.594ms      12.752us       0.000us         0.00%     204.466us       0.010us         20436
                                        aten::new_empty         0.00%      19.512ms         0.02%      75.537ms       1.709us       0.000us         0.00%       0.000us       0.000us         44212
                                            aten::zero_         0.01%      55.640ms         0.13%     523.096ms       4.544us       0.000us         0.00%       2.796ms       0.024us        115109
                                        hipLaunchKernel         0.08%     343.933ms         0.08%     345.388ms       6.727us       0.000us         0.00%       0.000us       0.000us         51347
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us       2.796ms         0.55%       2.796ms      11.798us           237
                                          aten::random_         0.00%      75.372us         0.00%      75.372us      12.562us       0.000us         0.00%       0.000us       0.000us             6
enumerate(DataLoader)#_MultiProcessingDataLoaderIter...         0.54%        2.247s         0.55%        2.268s     965.698us       0.000us         0.00%       0.000us       0.000us          2349
                                             aten::set_         0.01%      55.811ms         0.01%      55.811ms       0.298us       0.000us         0.00%       0.000us       0.000us        187326
                                            aten::alias         0.01%      36.774ms         0.01%      36.774ms       0.615us       0.000us         0.00%       0.000us       0.000us         59835
                                               aten::le         0.00%      10.853ms         0.00%      17.741ms       7.582us       0.000us         0.00%       0.000us       0.000us          2340
                                          aten::nonzero         0.00%       9.876ms         0.00%      12.931ms       5.526us       0.000us         0.00%       0.000us       0.000us          2340
                                      aten::as_strided_         0.01%      51.915ms         0.01%      51.915ms       1.082us       0.000us         0.00%       0.000us       0.000us         48000
                                              aten::max         0.01%      29.990ms         0.01%      37.925ms       8.098us     227.521us         0.04%     227.521us       0.049us          4683
                                               aten::gt         0.00%       4.655ms         0.00%       4.655ms       1.989us       0.000us         0.00%       0.000us       0.000us          2340
                                           aten::select         0.03%     105.096ms         0.03%     132.334ms       0.998us       0.000us         0.00%       0.000us       0.000us        132655
                                             aten::rsub         0.00%       8.609ms         0.01%      60.226ms      12.860us       0.000us         0.00%      10.119us       0.002us          4683
                                              aten::sub         0.01%      42.625ms         0.02%      74.352ms       7.057us      13.438us         0.00%      13.438us       0.001us         10536
                                              aten::add         0.02%      85.242ms         0.02%      85.344ms       4.375us       0.000us         0.00%       0.000us       0.000us         19506
                                              aten::div         0.03%     134.739ms         0.03%     143.462ms       5.931us       0.000us         0.00%       0.000us       0.000us         24189
                                               aten::eq         0.01%      29.375ms         0.01%      46.020ms      13.089us      14.679us         0.00%      14.679us       0.004us          3516
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us      14.679us         0.00%      14.679us      14.679us             1
                                            aten::slice         0.10%     428.713ms         0.14%     584.196ms       0.719us       0.000us         0.00%       0.000us       0.000us        812608
                                               aten::ne         0.02%      87.405ms         0.02%      87.905ms       7.710us     168.113us         0.03%     168.113us       0.015us         11401
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us     168.113us         0.03%     168.113us       3.577us            47
void at::native::elementwise_kernel<512, 1, at::nati...         0.00%       0.000us         0.00%       0.000us       0.000us     178.914us         0.04%     178.914us       3.727us            48
                                              aten::sum         0.04%     181.968ms         0.05%     194.449ms      10.485us     567.993us         0.11%     567.993us       0.031us         18545
void at::native::reduce_kernel<512, 1, at::native::R...         0.00%       0.000us         0.00%       0.000us       0.000us     370.032us         0.07%     370.032us       7.552us            49
                                          hipHostMalloc         0.00%      40.385us         0.00%      40.385us      40.385us       0.000us         0.00%       0.000us       0.000us             1
                                       aten::bernoulli_         0.03%     122.963ms         0.03%     131.281ms       5.522us     674.340us         0.13%     674.340us       0.028us         23776
void at::native::(anonymous namespace)::distribution...         0.00%       0.000us         0.00%       0.000us       0.000us     674.340us         0.13%     674.340us       3.587us           188
                                             aten::div_         0.03%     133.941ms         0.03%     142.856ms       5.311us     390.375us         0.08%     390.375us       0.015us         26899
void at::native::vectorized_elementwise_kernel<4, at...         0.00%       0.000us         0.00%       0.000us       0.000us     385.096us         0.08%     385.096us       2.048us           188
                                              aten::mul         0.06%     239.784ms         0.06%     253.049ms       5.063us      11.304ms         2.22%      11.304ms       0.226us         49978
void at::native::elementwise_kernel_manual_unroll<12...         0.00%       0.000us         0.00%       0.000us       0.000us      11.304ms         2.22%      11.304ms      60.128us           188
                                        aten::embedding         0.01%      35.207ms         0.07%     279.058ms      24.477us       0.000us         0.00%     619.486us       0.054us         11401
                                          aten::reshape         0.01%      29.380ms         0.03%     112.916ms       6.260us       0.000us         0.00%     141.689us       0.008us         18037
                                             aten::view         0.01%      57.409ms         0.01%      57.409ms       0.304us       0.000us         0.00%       0.000us       0.000us        188803
                                     aten::index_select         0.01%      61.550ms         0.03%     133.925ms      11.747us     477.797us         0.09%     477.797us       0.042us         11401
                                          aten::resize_         0.01%      26.720ms         0.01%      26.720ms       0.406us       0.000us         0.00%       0.000us       0.000us         65881
void at::native::(anonymous namespace)::indexSelectL...         0.00%       0.000us         0.00%       0.000us       0.000us     477.797us         0.09%     477.797us      10.166us            47
                                          aten::dropout         0.00%      15.729ms         0.05%     199.571ms       8.863us       0.000us         0.00%       5.857ms       0.260us         22518
                                   aten::native_dropout         0.03%     113.008ms         0.04%     182.577ms       9.051us       5.857ms         1.15%       5.857ms       0.290us         20172
                                       aten::empty_like         0.02%      63.096ms         0.05%     199.529ms       1.389us       0.000us         0.00%       0.000us       0.000us        143667
void at::native::(anonymous namespace)::fused_dropou...         0.00%       0.000us         0.00%       0.000us       0.000us       5.857ms         1.15%       5.857ms      41.245us           142
                                             aten::lstm         0.02%      66.447ms        18.03%       74.559s       2.180ms       0.000us         0.00%     476.390ms      13.928us         34203
                              aten::cudnn_is_acceptable         0.00%       6.562ms         0.00%       6.562ms       0.192us       0.000us         0.00%       0.000us       0.000us         34203
                                       aten::miopen_rnn        17.32%       71.643s        18.00%       74.469s       2.177ms     459.831ms        90.50%     476.390ms      13.928us         34203
                                        aten::transpose         0.02%      67.222ms         0.02%     100.033ms       0.898us       0.000us         0.00%       0.000us       0.000us        111390
                                                hipInit         0.00%       0.471us         0.00%       0.471us       0.471us       0.000us         0.00%       0.000us       0.000us             1
                            hipGetDevicePropertiesR0600         0.01%      46.596ms         0.01%      46.596ms       0.131us       0.000us         0.00%       0.000us       0.000us        355996
                                              hipMemset         0.00%      19.216us         0.00%      19.216us       9.608us       0.000us         0.00%       0.000us       0.000us             2
                                        Memset (Device)         0.00%       0.000us         0.00%       0.000us       0.000us      61.880us         0.01%      61.880us      30.940us             2
                                            aten::chunk         0.01%      59.127ms         0.22%     900.437ms       4.930us       0.000us         0.00%       0.000us       0.000us        182640
                                            aten::split         0.04%     151.630ms         0.20%     841.309ms       4.606us       0.000us         0.00%       0.000us       0.000us        182640
                                           aten::narrow         0.06%     241.415ms         0.17%     699.808ms       0.949us       0.000us         0.00%       0.000us       0.000us        737513
                                              aten::cat         0.23%     948.046ms         0.23%     954.811ms       4.921us       9.778ms         1.92%       9.778ms       0.050us        194037
                                          aten::view_as         0.01%      32.860ms         0.02%      64.882ms       0.474us       0.000us         0.00%       0.000us       0.000us        136812
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us       7.949ms         1.56%       7.949ms      28.090us           283
                                  hipDeviceGetAttribute         0.01%      26.213ms         0.01%      26.213ms       0.152us       0.000us         0.00%       0.000us       0.000us        172297
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us     990.208us         0.19%     990.208us       3.511us           282
                                      hipModuleLoadData         0.04%     171.243ms         0.04%     171.243ms       6.116ms       0.000us         0.00%       0.000us       0.000us            28
                               hipExtModuleLaunchKernel         0.07%     309.490ms         0.07%     309.492ms       0.838us       0.000us         0.00%       0.000us       0.000us        369154
                                SubTensorOpWithScalar1d         0.00%       0.000us         0.00%       0.000us       0.000us       5.222ms         1.03%       5.222ms      12.344us           423
Cijk_Alik_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us     653.033us         0.13%     653.033us      43.536us            15
                                         Op2dTensorLite         0.00%       0.000us         0.00%       0.000us       0.000us       7.135ms         1.40%       7.135ms      25.303us           282
Cijk_Alik_Bljk_SB_MT32x8x8_SN_1LDSB0_APM1_ABV0_ACED0...         0.00%       0.000us         0.00%       0.000us       0.000us     152.606ms        30.03%     152.606ms      34.794us          4386
                                       LSTMFwdHidUpdate         0.00%       0.000us         0.00%       0.000us       0.000us      21.413ms         4.21%      21.413ms       2.134us         10035
                                       aten::transpose_         0.01%      37.042ms         0.02%      86.576ms       1.896us       0.000us         0.00%       0.000us       0.000us         45660
                             SubTensorOpWithSubTensor1d         0.00%       0.000us         0.00%       0.000us       0.000us     129.472us         0.03%     129.472us       1.439us            90
                             SubTensorOpWithSubTensor2d         0.00%       0.000us         0.00%       0.000us       0.000us       2.404ms         0.47%       2.404ms       7.219us           333
Cijk_Alik_Bljk_SB_MT64x64x8_SN_1LDSB0_APM1_ABV0_ACED...         0.00%       0.000us         0.00%       0.000us       0.000us     180.993ms        35.62%     180.993ms      78.048us          2319
Cijk_Alik_Bljk_SB_MT32x8x8_SN_1LDSB0_APM1_ABV0_ACED0...         0.00%       0.000us         0.00%       0.000us       0.000us      21.498ms         4.23%      21.498ms       9.736us          2208
                                           aten::detach         0.01%      21.376ms         0.01%      53.606ms       0.745us       0.000us         0.00%       0.000us       0.000us         71941
                                                 detach         0.01%      32.230ms         0.01%      32.230ms       0.448us       0.000us         0.00%       0.000us       0.000us         71941
void at::native::(anonymous namespace)::CatArrayBatc...         0.00%       0.000us         0.00%       0.000us       0.000us     383.572us         0.08%     383.572us       5.327us            72
                                     aten::_unsafe_view         0.00%       7.275ms         0.00%       7.275ms       0.651us       0.000us         0.00%       0.000us       0.000us         11176
-------------------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------  ------------
Self CPU time total: 413.622s
Self CUDA time total: 508.099ms
```

---

### 评论 #37 — reneleonhardt (2026-01-24T11:20:31Z)

Is it possible to add ROCm 7.2 to the benchmark matrix?
https://www.phoronix.com/news/AMD-ROCm-7.2-Released

---

### 评论 #38 — tcgu-amd (2026-01-26T17:31:08Z)

Hi @reneleonhardt, thanks for the suggestion!

> Is it possible to add ROCm 7.2 to the benchmark matrix? https://www.phoronix.com/news/AMD-ROCm-7.2-Released

I don't think 7.2 fixed this particular issue, so it probably won't make that much of a difference. But yeah, once we figure out a potential workaround, we can bench 7.2 with it to see how it would affect performance. Thanks! 

---

### 评论 #39 — reneleonhardt (2026-01-26T21:36:47Z)

You're welcome! And the never ending stream continues, pytorch 2.10 has been released too finally with Python 3.14 support 😄

---

### 评论 #40 — tcgu-amd (2026-01-26T21:51:15Z)

@briansp2020, thanks for your results and observations, that helped a lot. So I did some detailed profiling on the memory copy behavior and here's the results

<img width="2217" height="648" alt="Image" src="https://github.com/user-attachments/assets/4dd21f58-b115-4ebf-be90-f23ec2443829" />

The issue seems to be that there's many more calls to hipMemcpyWithStream than the actual MEMORY_COPY_HOST_TO_DEVICE calls, and the overall overhead is much more significant that the actual memory copy operation itself. 

I will have to dig deeper to see why that's the case. 

By the way, I obtained the results via the following command 

`rocprofv3 --memory-copy-trace --hip-runtime-trace --summary-groups 'MEMORY_COPY|HIP_API'  --  python quickstart.py`

I modified quickstart.py to only run the text processing part for 1 epoch. 

You can give it a try if you are interested, but it does take a while for results to be aggregated. 

Thanks! 

---

### 评论 #41 — briansp2020 (2026-01-27T01:00:28Z)

I tried it on rocm 6.4.4, 7.1.1 and 7.2.
7.1.1 generates a lot of warnings. 7.2, though less than 7.1.1, still generates a lot of warnings. 
Comparing the output, number of calls did not change between rocm 6 & 7. It just seems like hipMemcpyWithStream just got slower. Looking through the changes made to hipMemcpyWithStream, this commit https://github.com/ROCm/rocm-systems/commit/b69f832430536e7a916ca6088357f492dda22edc that added check for StreamCaptureOngoing is slowing it down? 

Since I don't understand the reason why the check was added, I think I'll stop here. Hope you guys can release the fix soon and implement CI test that will catch these performance regressions going forward.




---

### 评论 #42 — tcgu-amd (2026-02-06T16:26:10Z)

@briansp2020 sorry for not updating for a while. I tried patching out the new check in hipMemcpyWithStream as you suggested, but unfortunately this didn't seem to have a lot of effects on the overall performance. I will be investigating further and updating you. Thanks! 

---

### 评论 #43 — tcgu-amd (2026-02-23T15:08:15Z)

Hi @briansp2020, just an update. After some investigation, it seems like that hipmemcpy might not be the root of the problem. The kernels used by rocblas actually changed between 6.4.4 and 7.0.0. After doing a library swap it seems like once we switch the roblas library in 7.0 to 6.4 the regression disappears. 

---

### 评论 #44 — k-artem (2026-03-27T10:23:24Z)

As @tcgu-amd mentioned, the root cause is that rocBLAS uses a different set of GEMM kernels (inside MIOpen’s RNN API that uses in example) in ROCm 7.x. The suboptimal performance of FP32 GEMM kernels is a known issue, and improvements are planned in hipBLASLt. We’ll update this issue once those changes land.

---
