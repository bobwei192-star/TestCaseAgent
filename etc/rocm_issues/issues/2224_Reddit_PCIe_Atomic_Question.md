# Reddit PCIe Atomic Question

> **Issue #2224**
> **状态**: closed
> **创建时间**: 2023-06-06T13:36:45Z
> **更新时间**: 2024-08-20T20:16:33Z
> **关闭时间**: 2024-08-20T20:16:32Z
> **作者**: saadrahim
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2224

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- MathiasMagnus

## 描述

Answer question from reddit on PCIe Atomic requirements at https://www.reddit.com/r/ROCm/comments/141ehjb/does_rocm_still_require_atomic_ops/

---

## 评论 (5 条)

### 评论 #1 — MathiasMagnus (2023-06-07T10:22:51Z)

[Responded](https://www.reddit.com/r/ROCm/comments/141ehjb/comment/jn8j4n9/?utm_source=reddit&utm_medium=web2x&context=3)

---

### 评论 #2 — nadvornik (2023-06-07T12:05:33Z)

So this is no longer true?

"Beginning with ROCm 1.8, GFX9 GPUs (such as Vega 10) no longer require PCIe atomics. We have similarly made more options available for many PCIe lanes. GFX9 GPUs can now be run on CPUs without PCIe atomics and on older PCIe generations, such as PCIe 2.0. This is not supported on GPUs below GFX9, e.g. GFX8 cards in the Fiji and Polaris families."

https://docs.amd.com/bundle/AMD_ROCm_Release_Notes_v4.5/page/Hardware_and_Software_Support.html

This is probably the same issue as https://github.com/RadeonOpenCompute/ROCm/issues/2156


---

### 评论 #3 — nadvornik (2023-06-07T12:10:49Z)

Now GFX9 devices without PCIe atomics are accepted by rocminfo. I think that only GFX8 devices are rejected.

---

### 评论 #4 — DGdev91 (2023-10-06T00:14:55Z)

It wasn't needed until rocm 5.2, then 5.3 put the requirement back.
In the docs it's mentioned as a requirement here https://docs.amd.com/en/latest/release/gpu_os_support.html#cpu-support

Recently it was introduced a workaround in rocm 5.7 https://docs.amd.com/en/latest/release.html#non-hostcall-hip-printf
It's been discussed here https://github.com/pytorch/pytorch/issues/103973

---

### 评论 #5 — harkgill-amd (2024-08-20T20:16:32Z)

As of ROCm 6.2, a PCIe Gen 3 Enabled CPU with PCIe atomics support is required to run ROCm. To check if your system supports PCIe atomics, run the following command
```
grep flags /sys/class/kfd/kfd/topology/nodes/*/io_links/0/properties
```
If the command returns a `1` for your GPU device, the system configuration does in fact support PCIe atomics.

For more information on how ROCm uses PCIe atomics, please visit the documentation [here](https://rocm.docs.amd.com/en/latest/conceptual/More-about-how-ROCm-uses-PCIe-Atomics.html). I will close out this ticket as the original question on reddit has also been answered.

---
