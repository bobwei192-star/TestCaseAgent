# Spurtious allocation failures

> **Issue #2480**
> **状态**: closed
> **创建时间**: 2023-09-19T13:12:53Z
> **更新时间**: 2024-04-07T18:21:43Z
> **关闭时间**: 2024-04-07T18:21:43Z
> **作者**: IMbackK
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2480

## 描述

When training with deepspeed on mI50, there seam to be random, spurious allocation falures.
```
:1:rocdevice.cpp            :1897: 9616777836 us: 4277 : [tid:0x7f2accbfe6c0] Failed creating memory
:1:memory.cpp               :347 : 9616777840 us: 4277 : [tid:0x7f2accbfe6c0] Video memory allocation failed!
:1:memory.cpp               :308 : 9616777845 us: 4277 : [tid:0x7f2accbfe6c0] Can't allocate memory size - 0x00000004 bytes!
:1:rocdevice.cpp            :2334: 9616777847 us: 4277 : [tid:0x7f2accbfe6c0] failed to create a svm hidden buffer!
:1:memory.cpp               :1501: 9616777850 us: 4277 : [tid:0x7f2accbfe6c0] Unable to allocate aligned memory
:1:rocdevice.cpp            :2134: 9616777853 us: 4278 : [tid:0x7f7fc7dff6c0] Invalid argument, pool_handle: 0x0 , max_alloc: 42
:1:hip_memory.cpp           :303 : 9616777863 us: 4277 : [tid:0x7f2accbfe6c0] Allocation failed : Device memory : required :4 | free :2314338304 | total :17163091968 
:1:rocdevice.cpp            :1897: 9616777877 us: 4278 : [tid:0x7f7fc7dff6c0] Failed creating memory
:1:memory.cpp               :347 : 9616777891 us: 4278 : [tid:0x7f7fc7dff6c0] Video memory allocation failed!
:1:memory.cpp               :308 : 9616777896 us: 4278 : [tid:0x7f7fc7dff6c0] Can't allocate memory size - 0x00000004 bytes!
:1:rocdevice.cpp            :2334: 9616777903 us: 4278 : [tid:0x7f7fc7dff6c0] failed to create a svm hidden buffer!
:1:memory.cpp               :1501: 9616777909 us: 4278 : [tid:0x7f7fc7dff6c0] Unable to allocate aligned memory
:1:hip_memory.cpp           :303 : 9616777924 us: 4278 : [tid:0x7f7fc7dff6c0] Allocation failed : Device memory : required :4 | free :3648126976 | total :17163091968 

Memory access fault by GPU node-3 (Agent handle: 0x560cdd34b960) on address (nil). Reason: Page not present or supervisor privilege.
Memory access fault by GPU node-2 (Agent handle: 0x55679c7f8630) on address (nil). Reason: Page not present or supervisor privilege.
```

It is unclear to me why we are unable to allocated 4 bytes in this instance. This problem seams to be restricted to mi50, and cant be repoduced by me on mi100, rx6800xt or mi25.

This issue is repoduceable in rocm5.5 and rocm5.6

mostly uninteresting dmesg to the page fault:

```
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:40 vmid:8 pasid:32776, for process python pid 4277 thread python pid 4277)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:40 vmid:8 pasid:32775, for process python pid 4278 thread python pid 4278)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00841051
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00841051
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x1
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python pid 4278 thread python pid 4278)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x1
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:40 vmid:8 pasid:32776, for process python pid 4277 thread python pid 4277)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:24 vmid:8 pasid:32776, for process python pid 4277 thread python pid 4277)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:40 vmid:8 pasid:32775, for process python pid 4278 thread python pid 4278)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:24 vmid:8 pasid:32776, for process python pid 4277 thread python pid 4277)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python pid 4278 thread python pid 4278)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from IH client 0x1b (UTCL2)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[Tue Sep 19 15:03:01 2023] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[Tue Sep 19 15:03:02 2023] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[Tue Sep 19 15:03:02 2023] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0

```

---

## 评论 (6 条)

### 评论 #1 — nartmada (2024-03-16T01:21:23Z)

Hi @IMbackK, apologies for the lack of response.  Do you still see this issue with latest ROCm 6.0.2?  Thanks.

---

### 评论 #2 — IMbackK (2024-03-20T20:22:01Z)

I am currently unable to retest this issue. I do still have some mi50 devices, but they are in cold storage atm, so this will take some time

---

### 评论 #3 — IMbackK (2024-03-20T20:22:44Z)

maybe @schneiderfelipe could retest this

---

### 评论 #4 — nartmada (2024-03-22T14:15:29Z)

Thank you @IMbackK.  @schneiderfelipe, please let us know if you have the test results.  Thanks.

---

### 评论 #5 — schneiderfelipe (2024-03-22T14:28:32Z)

Embarrassingly, I can't find my original issue (days have been tough). Would you mind linking that?

---

### 评论 #6 — nartmada (2024-04-07T18:21:43Z)

@IMbackK, if you don't mind, I will close this ticket for the time being.  If you still see the issue with latest ROCm, please reopen the ticket.  Thanks.

---
