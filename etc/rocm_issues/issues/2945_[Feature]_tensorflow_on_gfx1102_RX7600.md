# [Feature]: tensorflow on gfx1102 / RX7600

> **Issue #2945**
> **状态**: closed
> **创建时间**: 2024-03-06T07:13:35Z
> **更新时间**: 2024-04-05T15:23:37Z
> **关闭时间**: 2024-04-05T15:23:37Z
> **作者**: Estirp
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2945

## 描述

### Suggestion Description

On Linux, RX7600 do not seems to be supported :
```
# docker run -it --network=host --device=/dev/kfd --device=/dev/dri \
                 --ipc=host --shm-size 16G --group-add video --cap-add=SYS_PTRACE \
                 --security-opt seccomp=unconfined rocm/tensorflow:latest
tf-docker / > python
Python 3.9.18 (main, Aug 25 2023, 13:20:04)
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorflow
2024-03-06 07:00:40.549184: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (1.26.18) or chardet (3.0.4) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
>>> tensorflow.config.list_physical_devices('GPU')
2024-03-06 07:01:21.149888: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-06 07:01:26.856968: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-06 07:01:26.857151: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-06 07:01:26.857236: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2266] Ignoring visible gpu device (device: 0, name: AMD Radeon RX 7600, pci bus id: 0000:0d:00.0) with AMDGPU version : gfx1102. The supported AMDGPU versions are gfx1030gfx1100, gfx900, gfx906, gfx908, gfx90a, gfx940, gfx941, gfx942.
[]
```
(empty list of supported GPU)

Did I make a mistake ?
Is it planned ?

### Operating System

Arch Linux

### GPU

gfx1102

### ROCm Component

_No response_

---

## 评论 (8 条)

### 评论 #1 — gamunu (2024-03-10T09:37:31Z)

This looks like a bug in tensorflow library https://github.com/search?q=org%3AROCm+gfx1030gfx1100&type=issues#issue-2133438576

---

### 评论 #2 — Estirp (2024-03-10T10:31:25Z)

Indeed there looks like a bug with this typo "gfx1030gfx1100". But my card identify itself as gfx110**2** not gfx110**0**. So it is not the same problem.

I suspect the list of compatible version of tensorflow to be here : https://github.com/ROCm/xla/blob/main/xla/stream_executor/device_description.h. gfx1102 is missing in its file.

---

### 评论 #3 — paradoxnafi (2024-03-12T16:13:56Z)

I have the same issue in Arch Linux on RX7600 GPU
`
import tensorflow as tf
`
_2024-03-12 16:10:24.080485: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (1.26.18) or chardet (3.0.4) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
_
`
tf.config.list_physical_devices('GPU')
`
_2024-03-12 16:10:50.416352: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-12 16:10:50.565263: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-12 16:10:50.565317: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-12 16:10:50.565335: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2266] Ignoring visible gpu device (device: 0, name: AMD Radeon RX 7600, pci bus id: 0000:2b:00.0) with AMDGPU version : gfx1102. The supported AMDGPU versions are gfx1030gfx1100, gfx900, gfx906, gfx908, gfx90a, gfx940, gfx941, gfx942.
[]_


---

### 评论 #4 — benrichard-amd (2024-03-15T18:08:33Z)

Hi @Estirp,

Since Tensorflow was not built targeting gfx1102, one thing you can try is `export HSA_OVERRIDE_GFX_VERSION=11.0.0` in your environment to make ROCm report the device as a gfx1100.

---

### 评论 #5 — Estirp (2024-03-15T20:13:39Z)

```
>>> import tensorflow
2024-03-15 20:07:29.478342: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (1.26.18) or chardet (3.0.4) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
>>> tensorflow.config.list_physical_devices('GPU')
2024-03-15 20:07:53.778397: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-15 20:08:00.541001: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-15 20:08:00.541182: I tensorflow/compiler/xla/stream_executor/rocm/rocm_gpu_executor.cc:756] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-03-15 20:08:00.541250: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2266] Ignoring visible gpu device (device: 0, name: AMD Radeon RX 7600, pci bus id: 0000:0d:00.0) with AMDGPU version : gfx1100. The supported AMDGPU versions are gfx1030gfx1100, gfx900, gfx906, gfx908, gfx90a, gfx940, gfx941, gfx942.
[]
```
Good idea, but now it fall on the **gfx1030gfx1100** bug.

---

### 评论 #6 — gamunu (2024-03-15T20:20:11Z)

http://ml-ci.amd.com:21096/job/tensorflow/job/release-rocmfork-r214-rocm-enhanced/job/release-build-whl/206/
I've downloaded the newest build from the CI system. Let's hope the updates make their way to PyPI soon.

---

### 评论 #7 — benrichard-amd (2024-03-21T20:31:25Z)

Just to clarify the original question, Tensorflow comes built with a number of target AMD GPU architectures: gfx1030, gfx1100, gfx900 ..., etc.  If you want additional architectures, Tensorflow developers will need to add them or you will need to build Tensorflow yourself. So, this is not really an issue with ROCm, but with Tensorflow.

Alternatively you can use `export HSA_OVERRIDE_GFX_VERSION=11.0.0` mentioned above, which makes ROCm report the GPU as gfx1100. This works because the 7600 XT (gfx1102) is just a cut-down gfx1100.


---

### 评论 #8 — nartmada (2024-04-05T15:23:37Z)

Closing this ticket as the issue is with Tensorflow, not ROCm.  Thanks.

---
