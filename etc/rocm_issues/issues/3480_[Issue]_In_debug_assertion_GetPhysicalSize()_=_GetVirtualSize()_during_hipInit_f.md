# [Issue]: In debug assertion GetPhysicalSize() <= GetVirtualSize() during hipInit fails

> **Issue #3480**
> **状态**: closed
> **创建时间**: 2024-07-31T16:03:51Z
> **更新时间**: 2024-08-02T20:12:53Z
> **关闭时间**: 2024-08-02T20:12:53Z
> **作者**: sogartar
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3480

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

In a debug build get this assertion failure during initialization with `hipInit`.

```
thread #1, name = 'iree-run-module', stop reason = signal SIGABRT
    frame #6: 0x00007ffff7a8fe96 libc.so.6`__GI___assert_fail(assertion="GetPhysicalSize() <= GetVirtualSize()", file="/src/ROCR-Runtime/src/core/runtime/amd_memory_region.cpp", line=165, function="rocr::AMD::MemoryRegion::MemoryRegion(bool, bool, bool, bool, rocr::core::Agent*, const HsaMemoryProperties&)") at assert.c:101:3
    frame #7: 0x00007fffed0f7d3a libhsa-runtime64.so.1`rocr::AMD::MemoryRegion::MemoryRegion(this=0x0000555555e42e10, fine_grain=true, kernarg=false, full_profile=false, extended_scope_fine_grain=false, owner=0x0000555555e42c20, mem_props=0x00007fffffffc580) at amd_memory_region.cpp:165:3
    frame #8: 0x00007fffed0c3914 libhsa-runtime64.so.1`rocr::AMD::CpuAgent::InitRegionList(this=0x0000555555e42c20) at amd_cpu_agent.cpp:88:77
    frame #9: 0x00007fffed0c35fa libhsa-runtime64.so.1`rocr::AMD::CpuAgent::CpuAgent(this=0x0000555555e42c20, node=0, node_props=0x00007fffffffc7d0) at amd_cpu_agent.cpp:58:17
    frame #10: 0x00007fffed1095c8 libhsa-runtime64.so.1`rocr::AMD::DiscoverCpu(node_id=0, node_prop=0x00007fffffffc7d0) at amd_topology.cpp:111:50
    frame #11: 0x00007fffed10a23b libhsa-runtime64.so.1`rocr::AMD::BuildTopology() at amd_topology.cpp:325:38
    frame #12: 0x00007fffed10a81f libhsa-runtime64.so.1`rocr::AMD::Load() at amd_topology.cpp:408:16
    frame #13: 0x00007fffed14da53 libhsa-runtime64.so.1`rocr::core::Runtime::Load(this=0x00005555558b2490) at runtime.cpp:1848:17
    frame #14: 0x00007fffed1457e3 libhsa-runtime64.so.1`rocr::core::Runtime::Acquire() at runtime.cpp:138:51
    frame #15: 0x00007fffed11129a libhsa-runtime64.so.1`rocr::HSA::hsa_init() at hsa.cpp:206:52
    frame #16: 0x00007fffed1b81e2 libhsa-runtime64.so.1`::hsa_init() at hsa_table_interface.cpp:70:35
    frame #17: 0x00007ffff61aab62 libamdhip64.so`roc::Device::init() at rocdevice.cpp:476:20
    frame #18: 0x00007ffff6124ec2 libamdhip64.so`amd::Device::init() at device.cpp:488:28
    frame #19: 0x00007ffff619d02d libamdhip64.so`amd::Runtime::init() at runtime.cpp:75:56
    frame #20: 0x00007ffff5e5c9f4 libamdhip64.so`hip::init(status=0x00007fffffffcf3f) at hip_context.cpp:45:26
    frame #21: 0x00007ffff5e7344c libamdhip64.so`void std::__invoke_impl<void, void (&)(bool*), bool*>((null)=__invoke_other @ 0x00007fffffffcda0, __f=0x00007ffff5e5c978, (null)=0x00007fffffffcf40) at invoke.h:61:36
    frame #22: 0x00007ffff5e723c4 libamdhip64.so`std::__invoke_result<void (&)(bool*), bool*>::type std::__invoke<void (&)(bool*), bool*>(__fn=0x00007ffff5e5c978, (null)=0x00007fffffffcf40) at invoke.h:96:40
    frame #23: 0x00007ffff5e70736 libamdhip64.so`void std::call_once<void (&)(bool*), bool*>(__closure=(0x00007ffff5e5c978, 0x00007fffffffcf40))(bool*), bool*&&)::'lambda'()::operator()() const at mutex:776:17
    frame #24: 0x00007ffff5e723f7 libamdhip64.so`std::once_flag::_Prepare_execution::_Prepare_execution<void std::call_once<void (&)(bool*), bool*>(std::once_flag&, void (&)(bool*), bool*&&)::'lambda'()>(__closure=())(bool*))::'lambda'()::operator()() const at mutex:712:64
    frame #25: 0x00007ffff5e7240c libamdhip64.so`std::once_flag::_Prepare_execution::_Prepare_execution<void std::call_once<void (&)(bool*), bool*>(std::once_flag&, void (&)(bool*), bool*&&)::'lambda'()>(void (&)(bool*))::'lambda'()::_FUN() at mutex:712:16
    frame #26: 0x00007ffff7aefee8 libc.so.6`__pthread_once_slow at pthread_once.c:116:7
    frame #27: 0x00007ffff5e6eb60 libamdhip64.so`__gthread_once(__once=0x00007ffff7a41d80, __func=(libstdc++.so.6`__once_proxy)) at gthr-default.h:700:35
    frame #28: 0x00007ffff5e7079e libamdhip64.so`void std::call_once<void (&)(bool*), bool*>(__once=0x00007ffff7a41d80, __f=0x00007ffff5e5c978, (null)=0x00007fffffffcf40) at mutex:783:35
    frame #29: 0x00007ffff5e5d1ba libamdhip64.so`hip::hipInit(flags=0) at hip_context.cpp:137:3
    frame #30: 0x00007ffff60f8299 libamdhip64.so`hipInit(flags=0) at hip_table_interface.cpp:813:87
```

### Operating System

Ubuntu 22.04.2

### CPU

AMD EPYC 9454 48-Core Processor

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIP

### Steps to Reproduce

I followed the [build instructions](https://github.com/ROCm/ROCm/tree/62dd3820a2db180885306b3546cc9dfd82c787dc?tab=readme-ov-file#build-rocm-from-source) from the main readme page for `ROCM_VERSION=6.1.2`.

To build the HIP runtime in debug I used this command inside the docker container.
```
RELEASE_FLAG="" \
    make -f ROCm/tools/rocm-build/ROCm.mk -j ${NPROC:-$(nproc)} T_hip_on_rocclr
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-07-31T17:33:44Z)

@sogartar Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — jamesxu2 (2024-08-02T20:12:53Z)

Hello @sogartar , this is a known issue for systems with >1TB of memory. The assert was removed in the newly released ROCm 6.2 (see [this commit](https://github.com/ROCm/ROCR-Runtime/pull/226/commits/1d1b8456c3530e7b464f6d74ed0baa2b28345126#)) and you should no longer run into this issue once you update ROCm.

---
