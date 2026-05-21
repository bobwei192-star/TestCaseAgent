# [Issue]: Memory access fault by GPU node-1 (Agent handle: 0x5de975b3cc80) on address 0x799bfc063000

> **Issue #5051**
> **状态**: open
> **创建时间**: 2025-07-16T06:21:56Z
> **更新时间**: 2026-05-18T01:19:04Z
> **作者**: prasannamahato
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5051

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

ROCm error"Memory access fault by GPU node-1 (Agent handle: 0x5de975b3cc80) on address 0x799bfc063000. Reason: Page not present or supervisor privilege." while training a ai model 

### Operating System

22.04.05

### CPU

Ryzen 7 7700x

### GPU

rx 9070 xt

### ROCm Version

6.4.1

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information
The problem is solved , the problem was secure boot.

---

## 评论 (42 条)

### 评论 #1 — Orangestar12 (2025-07-16T22:19:52Z)

Getting the same result when VAE Decoding a latent 3D mesh generated with Hunyuan3D via comfyui-hunyuan3dwrapper & Flash VDM, ~~though I'm on ROCm 6.3 rather than 6.4~~ Different memory address, obviously, but it consistently crashes and core dumps.

EDIT: Tested on ROCm 6.4 nightly. Same result.

CPU: AMD Ryzen 5 3600 (12) @ 4.208GHz
GPU: AMD ATI RX 9070/9070 XT

Monitoring RAM and VRAM with `htop` and `radeontop` show that RAM, CPU and graphics pipe aren't maxing out, or at least not in unexpected ways.

```
Loading model from /mnt/Speedy Speed Boy/ComfyUI/models/diffusion_models/hunyuan3d-dit-v2.safetensors
image shape torch.Size([1, 3, 518, 518])
guidance:  None
Diffusion Sampling:: 100%|██████|50/50 [01:23<00:00,  1.66s/it]
latents shape:  torch.Size([1, 3072, 64])
Allocated memory: memory=2.458 GB
Max allocated memory: max_memory=5.617 GB
Max reserved memory: max_reserved=8.473 GB
FlashVDM Volume Decoding: 100%|██████| 32/32 [00:00<00:00, 454.24it/s]
Memory access fault by GPU node-1 (Agent handle: 0x55db7833c9a0) on address 0x7f2c228fa000. Reason: Page not present or supervisor privilege.
```

Attempting to cancel execution results in

```
GPU core dump created: gpucore.30336
```

Faster way to debug this than trying to train a whole model on the 9070 XT.

---

### 评论 #2 — ppanchad-amd (2025-07-17T14:20:33Z)

Hi @prasannamahato. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — zichguan-amd (2025-07-31T18:10:26Z)

I'm not able to repro the memory fault but I'm running into an issue I think from hy3d side. This is with 9070XT ROCm 6.4.2 + PyTorch nightly 2.9.0.dev20250723+rocm6.4 running hy3d_example_01
```
Diffusion Sampling:: 100%|████████████████████████████████████████████████████████████████████████████████| 50/50 [00:14<00:00,  3.55it/s]
latents shape:  torch.Size([1, 3072, 64])
Allocated memory: memory=2.503 GB
Max allocated memory: max_memory=4.688 GB
Max reserved memory: max_reserved=4.878 GB
FlashVDM Volume Decoding: 100%|███████████████████████████████████████████████████████████████████████████| 32/32 [00:00<00:00, 46.99it/s]
/home/rocm/ComfyUI/custom_nodes/ComfyUI-Hunyuan3DWrapper/hy3dgen/shapegen/models/autoencoders/volume_decoders.py:82: UserWarning: Using a non-tuple sequence for multidimensional indexing is deprecated and will be changed in pytorch 2.9; use x[tuple(seq)] instead of x[seq]. In pytorch 2.9 this will be interpreted as tensor index, x[torch.tensor(seq)], which will result either in an error or a different result (Triggered internally at /pytorch/torch/csrc/autograd/python_variable_indexing.cpp:309.)
  sliced = padded[slice_dims]
MC Surface Extractor
Traceback (most recent call last):
  File "/home/rocm/ComfyUI/custom_nodes/ComfyUI-Hunyuan3DWrapper/hy3dgen/shapegen/models/autoencoders/surface_extractors.py", line 54, in __call__
    vertices, faces = self.run(grid_logits[i], **kwargs)
  File "/home/rocm/ComfyUI/custom_nodes/ComfyUI-Hunyuan3DWrapper/hy3dgen/shapegen/models/autoencoders/surface_extractors.py", line 70, in run
    vertices, faces, normals, _ = measure.marching_cubes(
  File "/home/rocm/ComfyUI/venv/lib/python3.10/site-packages/skimage/measure/_marching_cubes_lewiner.py", line 139, in marching_cubes
    return _marching_cubes_lewiner(
  File "/home/rocm/ComfyUI/venv/lib/python3.10/site-packages/skimage/measure/_marching_cubes_lewiner.py", line 206, in _marching_cubes_lewiner
    raise RuntimeError('No surface found at the given iso value.')
RuntimeError: No surface found at the given iso value.
!!! Exception during processing !!! 'NoneType' object has no attribute 'mesh_f'
Traceback (most recent call last):
  File "/home/rocm/ComfyUI/execution.py", line 427, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb)
  File "/home/rocm/ComfyUI/execution.py", line 270, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb)
  File "/home/rocm/ComfyUI/execution.py", line 244, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/home/rocm/ComfyUI/execution.py", line 232, in process_inputs
    result = f(**inputs)
  File "/home/rocm/ComfyUI/custom_nodes/ComfyUI-Hunyuan3DWrapper/nodes.py", line 1401, in process
    outputs.mesh_f = outputs.mesh_f[:, ::-1]
AttributeError: 'NoneType' object has no attribute 'mesh_f'
```

---

### 评论 #4 — Umio-Yasuno (2025-08-13T07:23:05Z)

This also happens randomly in my environment with ROCm (TheRock 7.0.0rc20250810) + ComfyUI + pytorch (2.7.1+rocm7.0.0rc20250811) + RX 9060 XT 16GB (gfx1200, overrided gfx1201).  
It never happened with ROCm 6.4.1 + pytorch 2.8 .

However, ROCm (TheRock 7.0.0rc20250810) + pytorch (2.7.1+rocm7.0.0rc20250811) can generate images 2 to 3 times faster than ROCm 6.4.1 + pytorch 2.8.

```
:3:hip_module.cpp           :550 : 38724080984 us: [pid:92169 tid: 0x7fcd43d616c0] [32m hipExtModuleLaunchKernel ( 0x0x7fcb18a10cc0, 2560, 31, 1, 128, 1, 1, 0, stream:<null>, char array:<null>, 0x7fcd43d59f60, event:0, event:0, 0 ) [0m
:4:command.cpp              :357 : 38724080987 us: [pid:92169 tid: 0x7fcd43d616c0] Command (KernelExecution) enqueued: 0x7fc9f8d60710 to queue: 0x7fc9eecf54f0
:3:rocvirtual.cpp           :883 : 38724080989 us: [pid:92169 tid: 0x7fcd43d616c0] Arg0:  Gemm info = val:0x1 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724080990 us: [pid:92169 tid: 0x7fcd43d616c0] Arg1:  kernel info0 = val:0x2200001 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724080991 us: [pid:92169 tid: 0x7fcd43d616c0] Arg2:  kernel info1 = val:0x4010008 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724080992 us: [pid:92169 tid: 0x7fcd43d616c0] Arg3:  numWG = val:0x14 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724080993 us: [pid:92169 tid: 0x7fcd43d616c0] Arg4:  SizesFree0 = val:0x500 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724080994 us: [pid:92169 tid: 0x7fcd43d616c0] Arg5:  SizesFree1 = val:0x7b8 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724080995 us: [pid:92169 tid: 0x7fcd43d616c0] Arg6:  SizesFree2 = val:0x1 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724080996 us: [pid:92169 tid: 0x7fcd43d616c0] Arg7:  SizesSum0 = val:0x500 (size:0x4)
:3:rocvirtual.cpp           :790 : 38724080997 us: [pid:92169 tid: 0x7fcd43d616c0] Arg8:  D = ptr:0x7fcb1d600000 obj:[0x7fcb1d600000-0x7fcb1fe00000]
:3:rocvirtual.cpp           :790 : 38724080999 us: [pid:92169 tid: 0x7fcd43d616c0] Arg9:  C = ptr:0x7fcb1d600000 obj:[0x7fcb1d600000-0x7fcb1fe00000]
:3:rocvirtual.cpp           :790 : 38724081001 us: [pid:92169 tid: 0x7fcd43d616c0] Arg10:  A = ptr:0x7fcb1f612000 obj:[0x7fcb1d600000-0x7fcb1fe00000]
:3:rocvirtual.cpp           :790 : 38724081003 us: [pid:92169 tid: 0x7fcd43d616c0] Arg11:  B = ptr:0x7fcb1f13f000 obj:[0x7fcb1d600000-0x7fcb1fe00000]
:3:rocvirtual.cpp           :883 : 38724081004 us: [pid:92169 tid: 0x7fcd43d616c0] Arg12:  strideD0 = val:0x500 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081005 us: [pid:92169 tid: 0x7fcd43d616c0] Arg13:  strideD1 = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081006 us: [pid:92169 tid: 0x7fcd43d616c0] Arg14:  strideC0 = val:0x500 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081007 us: [pid:92169 tid: 0x7fcd43d616c0] Arg15:  strideC1 = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081009 us: [pid:92169 tid: 0x7fcd43d616c0] Arg16:  strideA0 = val:0x500 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081010 us: [pid:92169 tid: 0x7fcd43d616c0] Arg17:  strideA1 = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081011 us: [pid:92169 tid: 0x7fcd43d616c0] Arg18:  strideB0 = val:0x500 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081012 us: [pid:92169 tid: 0x7fcd43d616c0] Arg19:  strideB1 = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081013 us: [pid:92169 tid: 0x7fcd43d616c0] Arg20:  alpha = val:0x3f800000 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081014 us: [pid:92169 tid: 0x7fcd43d616c0] Arg21:  beta = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :774 : 38724081015 us: [pid:92169 tid: 0x7fcd43d616c0] Arg22:  AddressScaleAlphaVec = ptr:(nil) 
:3:rocvirtual.cpp           :774 : 38724081017 us: [pid:92169 tid: 0x7fcd43d616c0] Arg23:  bias = ptr:(nil) 
:3:rocvirtual.cpp           :883 : 38724081018 us: [pid:92169 tid: 0x7fcd43d616c0] Arg24:  biasType = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081019 us: [pid:92169 tid: 0x7fcd43d616c0] Arg25:  StrideBias = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081020 us: [pid:92169 tid: 0x7fcd43d616c0] Arg26:  activationAlpha = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081021 us: [pid:92169 tid: 0x7fcd43d616c0] Arg27:  activationBeta = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :883 : 38724081022 us: [pid:92169 tid: 0x7fcd43d616c0] Arg28:  activationType = val:0x0 (size:0x4)
:3:rocvirtual.cpp           :3344: 38724081023 us: [pid:92169 tid: 0x7fcd43d616c0] ShaderName : Cijk_Alik_Bljk_HHS_BH_Bias_HA_S_SAV_UserArgs_MT64x64x32_MI16x16x1_SN_LDSB0_AFC1_AFEM1_AFEM1_ASEM1_CLR0_CADS0_DTVA0_DTVB1_EPS1_FDSI0_GRPM1_GRVWA8_GRVWB8_GSUAMB_GLS0_ISA1201_IU1_K1_LBSPPA128_LBSPPB0_LBSPPM0_LPA16_LPB0_LPM0_LRVW8_LWPMn1_MIAV1_MIWT2_2_MO40_NTn1_NTA0_NTB0_NTC0_NTD0_NTM0_NEPBS0_NLCA1_NLCB2_ONLL1_PGR1_PLR1_PKA0_SIA3_SS0_SPO0_SRVW0_SSO0_SVW8_SK0_SKXCCM0_TLDS2_ULSGRO0_USL1_UIOFGRO0_USFGROn1_VSn1_VWA1_VWB1_WSGRA0_WSGRB0_WS32_WG32_4_1
:3:rocvirtual.cpp           :3542: 38724081024 us: [pid:92169 tid: 0x7fcd43d616c0] KernargSegmentByteSize = 144 KernargSegmentAlignment = 256
:4:rocvirtual.cpp           :1076: 38724081026 us: [pid:92169 tid: 0x7fcd43d616c0] SWq=0x7fcf2a564000, HWq=0x7fcbe4200000, id=1, Dispatch Header = 0x1502 (type=2, barrier=1, acquire=2, release=2), setup=3, grid=[2560, 31, 1], workgroup=[128, 1, 1], private_seg_size=0, group_seg_size=13312, kernel_obj=0x7fcbc5532bc0, kernarg_address=0x7fcbdc200000, completion_signal=0x0, correlation_id=0, rptr=2085755, wptr=2085755
:4:commandqueue.cpp         :183 : 38724081027 us: [pid:92169 tid: 0x7fcd43d616c0] Marker queued to 0x7fc9eecf54f0 for finish
:4:command.cpp              :357 : 38724081028 us: [pid:92169 tid: 0x7fcd43d616c0] Command (InternalMarker) enqueued: 0x7fc9f0145e40 to queue: 0x7fc9eecf54f0
:3:rocvirtual.cpp           :551 : 38724081031 us: [pid:92169 tid: 0x7fcd43d616c0] Set Handler: handle(0x7fced23fca00), timestamp(0x7fc9f0a77f90)
:4:rocvirtual.cpp           :1260: 38724081033 us: [pid:92169 tid: 0x7fcd43d616c0] SWq=0x7fcf2a564000, HWq=0x7fcbe4200000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7fced23fca00, rptr=2085755, wptr=2085756
:1:rocdevice.cpp            :3434: 38724086971 us: [pid:92169 tid: 0x7fced21ff6c0] Memory Fault Error
```

---

### 评论 #5 — GowthamKudupudi (2025-09-02T15:03:58Z)

i don't have this issue with the main user(uid 1000), if i run the gpu application with another user which is part of all groups same as main user, i face this issue.

---

### 评论 #6 — Lonceg (2025-09-24T15:51:58Z)

Seems like the same issue as I keep getting with ROCm 7.0.0 Docker Image here https://github.com/ROCm/ROCm/issues/5405

---

### 评论 #7 — Umio-Yasuno (2025-10-19T23:38:49Z)

~I found that setting `HSA_DISABLE_FRAGMENT_ALLOCATOR=1` or `PYTORCH_NO_HIP_MEMORY_CACHING=1` (but slightly reduced performance) resolves the memory access error.~
~It may be more stable not to set `PYTORCH_ALLOC_CONF=expandable_segments:True`.~

---

### 评论 #8 — Orangestar12 (2025-11-05T23:20:25Z)

> ~I found that setting `HSA_DISABLE_FRAGMENT_ALLOCATOR=1` or `PYTORCH_NO_HIP_MEMORY_CACHING=1` (but slightly reduced performance) resolves the memory access error.~ ~It may be more stable not to set `PYTORCH_ALLOC_CONF=expandable_segments:True`.~

~You edited this to cross it out, but I can confirm `PYTORCH_NO_HIP_MEMORY_CACHING=1` does solve the problem - though with a \~17% speed penalty. Given the name of the option, it should be obvious why.~

Ok, apparently not. I was testing for a full week just to make sure and it suddenly popped up right after I made this comment. :V

---

### 评论 #9 — scrapes (2025-11-29T12:12:11Z)

> i don't have this issue with the main user(uid 1000), if i run the gpu application with another user which is part of all groups same as main user, i face this issue.

Using the jax rocm docker image (rocm 7.1.1)  i couldnt Train more than 2 Epochs before encountering this problem.
Setting the user and group of the container to 1000:1000 (main uid and gid) i did not encounter this problem once while doing multipile training sessions over around 15h summed up.

GPU used was a 9070 xt

Kernel:  `6.17.9-2-cachyos`

---

### 评论 #10 — Umio-Yasuno (2025-12-06T05:09:11Z)

Is `amdgpu.cwsr_enable=0` the solution?

https://github.com/ROCm/ROCm/issues/4846#issuecomment-3617170494

---

### 评论 #11 — alshdavid (2025-12-06T11:58:53Z)

This happens to me on ComfyUI on Linux randomly when too many images are generated in sequence. This also appears to happen every time I try to generate a video

---

### 评论 #12 — prasannamahato (2025-12-12T16:50:58Z)

the problem is solved the cause is secure boot , disable it and it works perfectly then. 

---

### 评论 #13 — Umio-Yasuno (2025-12-12T20:07:04Z)

My conclusion: This issue is caused by a mismatch between the hardware scheduling mode and CWSR (compute wave store and resume) support.
It can be resolved by using hipblaslt with https://github.com/ROCm/rocm-libraries/commit/29b74681771a7da911faee1e38c1d6d90826023c applied, a [patched](https://lists.freedesktop.org/archives/amd-gfx/2025-December/134755.html) Linux kernel, or disabling CWSR with `amdgpu.cwsr_enable=0` .

https://github.com/ROCm/rocm-libraries/issues/3211
https://github.com/ROCm/rocm-libraries/commit/29b74681771a7da911faee1e38c1d6d90826023c
https://lists.freedesktop.org/archives/amd-gfx/2025-December/134755.html

---

### 评论 #14 — GuardianLiarus (2026-01-03T16:19:46Z)

Facing the same issue, i'm running Python 3.14.2 as well as Pytorch nightly with rocm7.1

---

### 评论 #15 — alexheretic (2026-01-09T19:06:11Z)

I'm seeing these occur now for some reason, maybe related to new kernel code (in `6.18.3`)? Happens for example during VAE encode.

```
Memory access fault by GPU node-1 (Agent handle: 0x55f8b54eec30) on address 0x7f2a53193000. Reason: Page not present or supervisor privilege.
```

### System
Linux using comfyui
```
Total VRAM 16368 MB, total RAM 64217 MB
pytorch version: 2.10.0.dev20251206+rocm7.1
AMD arch: gfx1100 
```

>  or disabling CWSR with amdgpu.cwsr_enable=0 .

Note: I'm running with `amdgpu.cwsr_enable=0` (confirmed in my `/proc/cmdline`) but it is not stopping this happening.

<details>
<summary>journal logs</summary>

```
Jan 09 18:55:45 alexpc kernel: gmc_v11_0_process_interrupt: 632 callbacks suppressed
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc systemd-coredump[134090]: Process 91762 (python) of user 60105 terminated abnormally with signal 6/ABRT, processing...
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc systemd[1]: Started Process Core Dump (PID 134090/UID 0).
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318b000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801A31
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:          Faulty UTCL2 client ID: SDMA0 (0xd)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:          MORE_FAULTS: 0x1
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:          WALKER_ERROR: 0x0
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:          MAPPING_ERROR: 0x0
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:          RW: 0x0
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318b000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318b000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318b000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318c000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318c000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318b000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318c000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318c000 from client 10
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32792)
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:  Process python pid 91762 thread python pid 91762
Jan 09 18:55:45 alexpc kernel: amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f2a5318d000 from client 10
```

```
Jan 09 18:57:12 alexpc systemd-coredump[134091]: [🡕] Process 91762 (python) of user 60105 dumped core.
                                                 
                                                 Module /dev/zero (deleted) without build-id.
                                                 ...
                                                 Module /dev/zero (deleted) without build-id.
                                                 Module libsharpyuv.817afaaa.so.0 without build-id.
                                                 Module libz.db8a765a.so.1 without build-id.
                                                 Module libwebp.efd97cc6.so.7 without build-id.
                                                 Module libjpeg.2394f5ee.so.8 without build-id.
                                                 Module libpng16.c2d532b4.so.16 without build-id.
                                                 Module librocroller.so without build-id.
                                                 Module libmagma.so without build-id.
                                                 Stack trace of thread 91764:
                                                 #0  0x00007f2ed709890c n/a (libc.so.6 + 0x9890c)
                                                 #1  0x00007f2ed703e3a0 raise (libc.so.6 + 0x3e3a0)
                                                 #2  0x00007f2ed702557a abort (libc.so.6 + 0x2557a)
                                                 #3  0x00007f2db948d33f _ZN4rocr4core7Runtime14VMFaultHandlerElPv (libhsa-runtime64.so + 0x8d33f)
                                                 #4  0x00007f2db948c0b3 _ZN4rocr4core7Runtime15AsyncEventsLoopEPv (libhsa-runtime64.so + 0x8c0b3)
                                                 #5  0x00007f2db94332cd _ZN4rocr2os16ThreadTrampolineEPv (libhsa-runtime64.so + 0x332cd)
                                                 #6  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #7  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91762:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70931b4 n/a (libc.so.6 + 0x931b4)
                                                 #3  0x00007f2ed711acb5 epoll_wait (libc.so.6 + 0x11acb5)
                                                 #4  0x00007f2ed6621981 n/a (select.cpython-313-x86_64-linux-gnu.so + 0x2981)
                                                 #5  0x00007f2ed757483d _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17483d)
                                                 #6  0x00007f2ed7648b59 PyEval_EvalCode (libpython3.13.so.1.0 + 0x248b59)
                                                 #7  0x00007f2ed768956c n/a (libpython3.13.so.1.0 + 0x28956c)
                                                 #8  0x00007f2ed768618d n/a (libpython3.13.so.1.0 + 0x28618d)
                                                 #9  0x00007f2ed76828f8 n/a (libpython3.13.so.1.0 + 0x2828f8)
                                                 #10 0x00007f2ed7682522 n/a (libpython3.13.so.1.0 + 0x282522)
                                                 #11 0x00007f2ed7682323 n/a (libpython3.13.so.1.0 + 0x282323)
                                                 #12 0x00007f2ed7680991 Py_RunMain (libpython3.13.so.1.0 + 0x280991)
                                                 #13 0x00007f2ed7635beb Py_BytesMain (libpython3.13.so.1.0 + 0x235beb)
                                                 #14 0x00007f2ed7027635 n/a (libc.so.6 + 0x27635)
                                                 #15 0x00007f2ed70276e9 __libc_start_main (libc.so.6 + 0x276e9)
                                                 #16 0x000055f8a72ba045 _start (/usr/bin/python3.13 + 0x1045)
                                                 
                                                 Stack trace of thread 91779:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed7095e9e pthread_cond_wait (libc.so.6 + 0x95e9e)
                                                 #4  0x00007f2c63637c7b blas_thread_server (libscipy_openblas-b75cc656.so + 0x437c7b)
                                                 #5  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #6  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)

                                                 Stack trace of thread 91812:
                                                 #0  0x00007f2db94620f6 _ZN4rocr4core14BusyWaitSignal11WaitRelaxedE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x620f6)
                                                 #1  0x00007f2db9461dea _ZN4rocr4core14BusyWaitSignal11WaitAcquireE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x61dea)
                                                 #2  0x00007f2db9465931 _ZN4rocr3HSA25hsa_signal_wait_scacquireE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x65931)
                                                 #3  0x00007f2ed177c61c _ZN9roctracer11hsa_support6detailL34hsa_signal_wait_scacquire_callbackE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libroctracer64.so + 0x1161c)
                                                 #4  0x00007f2e367d73ea _ZN3amd3roc13WaitForSignalE12hsa_signal_sbb (libamdhip64.so + 0x3d73ea)
                                                 #5  0x00007f2e367e177a _ZN3amd3roc10VirtualGPU14HwQueueTracker16CpuWaitForSignalEPNS0_15ProfilingSignalE (libamdhip64.so + 0x3e177a)
                                                 #6  0x00007f2e367e44de _ZN3amd3roc10VirtualGPU21releaseGpuMemoryFenceEb (libamdhip64.so + 0x3e44de)
                                                 #7  0x00007f2e367eaa0c _ZN3amd3roc10VirtualGPU12submitMarkerERNS_6MarkerE (libamdhip64.so + 0x3eaa0c)
                                                 #8  0x00007f2e367b4946 _ZN3amd7Command7enqueueEv (libamdhip64.so + 0x3b4946)
                                                 #9  0x00007f2e367b7640 _ZN3amd9HostQueue6finishEb (libamdhip64.so + 0x3b7640)
                                                 #10 0x00007f2e36482cbe _ZN3hip6Device14SyncAllStreamsEbb (libamdhip64.so + 0x82cbe)
                                                 #11 0x00007f2e3658afbc _ZN3hip8ihipFreeEPv (libamdhip64.so + 0x18afbc)
                                                 #12 0x00007f2e36592940 _ZN3hip7hipFreeEPv (libamdhip64.so + 0x192940)
                                                 #13 0x00007f2ed34b2a24 _ZN3c103hip19HIPCachingAllocator6NativeL15uncached_deleteEPv (libc10_hip.so + 0x19a24)
                                                 #14 0x00007f2ea3bb3e76 _ZN2at6native40raw_miopen_convolution_forward_out_32bitERKNS_6TensorES3_S3_N3c108ArrayRefIlEES6_S6_lbbb (libtorch_hip.so + 0x2fb3e76)
                                                 #15 0x00007f2ea3baeef3 _ZN2at6native30miopen_convolution_forward_outERNS_9TensorArgEPKcRKS1_S6_N3c108ArrayRefIlEES9_S9_lbbb (libtorch_hip.so + 0x2faeef3)
                                                 #16 0x00007f2ea3baf287 _ZN2at6native18miopen_convolutionERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefIlEESA_SA_lbb (libtorch_hip.so + 0x2faf287)
                                                 #17 0x00007f2ea391690a _ZN2at12_GLOBAL__N_112_GLOBAL__N_132wrapper_CUDA__miopen_convolutionERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_SB_bb (libtorch_hip.so + 0x2d1690a)
                                                 #18 0x00007f2ea394077e _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_SE_bbEXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_132wrapper_CUDA__miopen_convolutionES8_S8_>
                                                 #19 0x00007f2ebe8c85c7 _ZN2at4_ops18miopen_convolution4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_SB_bb (libtorch_cpu.so + 0x2cc85c7)
                                                 #20 0x00007f2ebdb074cf _ZN2at6native12_convolutionERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefIlEESA_SA_bSA_lbbbb (libtorch_cpu.so + 0x1f074cf)
                                                 #21 0x00007f2ebeec0d60 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_bSF_SE_bbbbEXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_147wrapper_CompositeExplicitAutograd>
                                                 #22 0x00007f2ebe516c64 _ZN2at4_ops12_convolution4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_bSC_SB_bbbb (libtorch_cpu.so + 0x2916c64)
                                                 #23 0x00007f2ebdb00846 _ZN2at6native11convolutionERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefIlEESA_SA_bSA_l (libtorch_cpu.so + 0x1f00846)
                                                 #24 0x00007f2ebeec08c5 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_bSF_SE_EXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_146wrapper_CompositeExplicitAutograd__co>
                                                 #25 0x00007f2ebe514049 _ZN2at4_ops11convolution4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_bSC_SB_ (libtorch_cpu.so + 0x2914049)
                                                 #26 0x00007f2ebdb0bb60 _ZN2at6native13conv3d_symintERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefINS8_6SymIntEEESB_SB_SA_ (libtorch_cpu.so + 0x1f0bb60)
                                                 #27 0x00007f2ebeff659e _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_SE_EXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_141wrapper_CompositeImplicitAutograd__conv3d>
                                                 #28 0x00007f2ebea63d4d _ZN2at4_ops6conv3d4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_SB_ (libtorch_cpu.so + 0x2e63d4d)
                                                 #29 0x00007f2ed1e80f9d _ZN5torch8autogradL18THPVariable_conv3dEP7_objectS2_S2_ (libtorch_python.so + 0x680f9d)
                                                 #30 0x00007f2ed7594c9d n/a (libpython3.13.so.1.0 + 0x194c9d)
                                                 #31 0x00007f2ed75611db _PyObject_MakeTpCall (libpython3.13.so.1.0 + 0x1611db)
                                                 #32 0x00007f2ed7572676 _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x172676)
                                                 #33 0x00007f2ed75ce575 n/a (libpython3.13.so.1.0 + 0x1ce575)
                                                 #34 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #35 0x00007f2ed75ce575 n/a (libpython3.13.so.1.0 + 0x1ce575)
                                                 #36 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #37 0x00007f2ed75ce575 n/a (libpython3.13.so.1.0 + 0x1ce575)
                                                 #38 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #39 0x00007f2ed75ce575 n/a (libpython3.13.so.1.0 + 0x1ce575)
                                                 #40 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #41 0x00007f2ed7646b01 n/a (libpython3.13.so.1.0 + 0x246b01)
                                                 #42 0x00007f2ed769920f n/a (libpython3.13.so.1.0 + 0x29920f)
                                                 #43 0x00007f2ed75611db _PyObject_MakeTpCall (libpython3.13.so.1.0 + 0x1611db)
                                                 #44 0x00007f2ed7572676 _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x172676)
                                                 #45 0x00007f2ed75ce6c3 n/a (libpython3.13.so.1.0 + 0x1ce6c3)
                                                 #46 0x00007f2ed76569d6 n/a (libpython3.13.so.1.0 + 0x2569d6)
                                                 #47 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #48 0x00007f2ed75ce6c3 n/a (libpython3.13.so.1.0 + 0x1ce6c3)
                                                 #49 0x00007f2ed76569d6 n/a (libpython3.13.so.1.0 + 0x2569d6)
                                                 #50 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #51 0x00007f2ed7646b79 n/a (libpython3.13.so.1.0 + 0x246b79)
                                                 #52 0x00007f2ed769920f n/a (libpython3.13.so.1.0 + 0x29920f)
                                                 #53 0x00007f2ed75611db _PyObject_MakeTpCall (libpython3.13.so.1.0 + 0x1611db)
                                                 #54 0x00007f2ed757b769 _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17b769)
                                                 #55 0x00007f2ed75ce6c3 n/a (libpython3.13.so.1.0 + 0x1ce6c3)
                                                 #56 0x00007f2ed76569d6 n/a (libpython3.13.so.1.0 + 0x2569d6)
                                                 #57 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #58 0x00007f2ed75ce6c3 n/a (libpython3.13.so.1.0 + 0x1ce6c3)
                                                 #59 0x00007f2ed76569d6 n/a (libpython3.13.so.1.0 + 0x2569d6)
                                                 #60 0x00007f2ed757582f _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17582f)
                                                 #61 0x00007f2ed765d80d n/a (libpython3.13.so.1.0 + 0x25d80d)
                                                 #62 0x00007f2ed65c77d5 n/a (_asyncio.cpython-313-x86_64-linux-gnu.so + 0x57d5)
                                                 #63 0x00007f2ed65c8eb5 n/a (_asyncio.cpython-313-x86_64-linux-gnu.so + 0x6eb5)

                                                 Stack trace of thread 91962:
                                                 #0  0x00007f2ed321de66 gomp_barrier_wait_end (libgomp.so + 0x1de66)
                                                 #1  0x00007f2ed321b498 gomp_thread_start (libgomp.so + 0x1b498)
                                                 #2  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #3  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91964:
                                                 #0  0x00007f2ed321de66 gomp_barrier_wait_end (libgomp.so + 0x1de66)
                                                 #1  0x00007f2ed321b498 gomp_thread_start (libgomp.so + 0x1b498)
                                                 #2  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #3  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91965:
                                                 #0  0x00007f2ed321de6d gomp_barrier_wait_end (libgomp.so + 0x1de6d)
                                                 #1  0x00007f2ed321b498 gomp_thread_start (libgomp.so + 0x1b498)
                                                 #2  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #3  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91778:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed7095e9e pthread_cond_wait (libc.so.6 + 0x95e9e)
                                                 #4  0x00007f2c63637c7b blas_thread_server (libscipy_openblas-b75cc656.so + 0x437c7b)
                                                 #5  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #6  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91968:
                                                 #0  0x00007f2ed321de66 gomp_barrier_wait_end (libgomp.so + 0x1de66)
                                                 #1  0x00007f2ed321b498 gomp_thread_start (libgomp.so + 0x1b498)
                                                 #2  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #3  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91963:
                                                 #0  0x00007f2ed321de66 gomp_barrier_wait_end (libgomp.so + 0x1de66)
                                                 #1  0x00007f2ed321b498 gomp_thread_start (libgomp.so + 0x1b498)
                                                 #2  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #3  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91780:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed7095e9e pthread_cond_wait (libc.so.6 + 0x95e9e)
                                                 #4  0x00007f2c63637c7b blas_thread_server (libscipy_openblas-b75cc656.so + 0x437c7b)
                                                 #5  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #6  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91967:
                                                 #0  0x00007f2ed321de66 gomp_barrier_wait_end (libgomp.so + 0x1de66)
                                                 #1  0x00007f2ed321b498 gomp_thread_start (libgomp.so + 0x1b498)
                                                 #2  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #3  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91777:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed7095e9e pthread_cond_wait (libc.so.6 + 0x95e9e)
                                                 #4  0x00007f2c63637c7b blas_thread_server (libscipy_openblas-b75cc656.so + 0x437c7b)
                                                 #5  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #6  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)

                                                 Stack trace of thread 91977:
                                                 #0  0x00007f2ed711670d ioctl (libc.so.6 + 0x11670d)
                                                 #1  0x00007f2db9528730 hsakmt_ioctl (libhsa-runtime64.so + 0x128730)
                                                 #2  0x00007f2db951f4e3 hsaKmtWaitOnMultipleEvents_Ext (libhsa-runtime64.so + 0x11f4e3)
                                                 #3  0x00007f2db948bc73 _ZN4rocr4core7Runtime15AsyncEventsLoopEPv (libhsa-runtime64.so + 0x8bc73)
                                                 #4  0x00007f2db94332cd _ZN4rocr2os16ThreadTrampolineEPv (libhsa-runtime64.so + 0x332cd)
                                                 #5  0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #6  0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91994:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed709e1f6 n/a (libc.so.6 + 0x9e1f6)
                                                 #4  0x00007f2ed76cb115 _PySemaphore_Wait (libpython3.13.so.1.0 + 0x2cb115)
                                                 #5  0x00007f2ed76cafad _PyParkingLot_Park (libpython3.13.so.1.0 + 0x2cafad)
                                                 #6  0x00007f2ed76a8ec7 n/a (libpython3.13.so.1.0 + 0x2a8ec7)
                                                 #7  0x00007f2ed76a8d77 n/a (libpython3.13.so.1.0 + 0x2a8d77)
                                                 #8  0x00007f2ed759a3f2 n/a (libpython3.13.so.1.0 + 0x19a3f2)
                                                 #9  0x00007f2ed756364d PyObject_Vectorcall (libpython3.13.so.1.0 + 0x16364d)
                                                 #10 0x00007f2ed7572676 _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x172676)
                                                 #11 0x00007f2ed75ce3bc n/a (libpython3.13.so.1.0 + 0x1ce3bc)
                                                 #12 0x00007f2ed76cb1d8 n/a (libpython3.13.so.1.0 + 0x2cb1d8)
                                                 #13 0x00007f2ed76cb15c n/a (libpython3.13.so.1.0 + 0x2cb15c)
                                                 #14 0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #15 0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 91996:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed709ef08 n/a (libc.so.6 + 0x9ef08)
                                                 #4  0x00007f2ed76cb0ad _PySemaphore_Wait (libpython3.13.so.1.0 + 0x2cb0ad)
                                                 #5  0x00007f2ed76cafad _PyParkingLot_Park (libpython3.13.so.1.0 + 0x2cafad)
                                                 #6  0x00007f2ed38084b8 n/a (_queue.cpython-313-x86_64-linux-gnu.so + 0x14b8)
                                                 #7  0x00007f2ed380861a n/a (_queue.cpython-313-x86_64-linux-gnu.so + 0x161a)
                                                 #8  0x00007f2ed75e6573 n/a (libpython3.13.so.1.0 + 0x1e6573)
                                                 #9  0x00007f2ed756364d PyObject_Vectorcall (libpython3.13.so.1.0 + 0x16364d)
                                                 #10 0x00007f2ed757b769 _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17b769)
                                                 #11 0x00007f2ed75ce3bc n/a (libpython3.13.so.1.0 + 0x1ce3bc)
                                                 #12 0x00007f2ed76cb1d8 n/a (libpython3.13.so.1.0 + 0x2cb1d8)
                                                 #13 0x00007f2ed76cb15c n/a (libpython3.13.so.1.0 + 0x2cb15c)
                                                 #14 0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #15 0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 
                                                 Stack trace of thread 92160:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed709e1f6 n/a (libc.so.6 + 0x9e1f6)
                                                 #4  0x00007f2ed76cb115 _PySemaphore_Wait (libpython3.13.so.1.0 + 0x2cb115)
                                                 #5  0x00007f2ed76cafad _PyParkingLot_Park (libpython3.13.so.1.0 + 0x2cafad)
                                                 #6  0x00007f2ed76a8ec7 n/a (libpython3.13.so.1.0 + 0x2a8ec7)
                                                 #7  0x00007f2ed76a8d77 n/a (libpython3.13.so.1.0 + 0x2a8d77)
                                                 #8  0x00007f2ed759a3f2 n/a (libpython3.13.so.1.0 + 0x19a3f2)
                                                 #9  0x00007f2ed756364d PyObject_Vectorcall (libpython3.13.so.1.0 + 0x16364d)
                                                 #10 0x00007f2ed7572676 _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x172676)
                                                 #11 0x00007f2ed75ce3bc n/a (libpython3.13.so.1.0 + 0x1ce3bc)
                                                 #12 0x00007f2ed76cb1d8 n/a (libpython3.13.so.1.0 + 0x2cb1d8)
                                                 #13 0x00007f2ed76cb15c n/a (libpython3.13.so.1.0 + 0x2cb15c)
                                                 #14 0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #15 0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)

                                                 Stack trace of thread 130827:
                                                 #0  0x00007f2ed709f002 n/a (libc.so.6 + 0x9f002)
                                                 #1  0x00007f2ed709316c n/a (libc.so.6 + 0x9316c)
                                                 #2  0x00007f2ed70937dc n/a (libc.so.6 + 0x937dc)
                                                 #3  0x00007f2ed709ef08 n/a (libc.so.6 + 0x9ef08)
                                                 #4  0x00007f2ed76cb0ad _PySemaphore_Wait (libpython3.13.so.1.0 + 0x2cb0ad)
                                                 #5  0x00007f2ed76cafad _PyParkingLot_Park (libpython3.13.so.1.0 + 0x2cafad)
                                                 #6  0x00007f2ed38084b8 n/a (_queue.cpython-313-x86_64-linux-gnu.so + 0x14b8)
                                                 #7  0x00007f2ed380861a n/a (_queue.cpython-313-x86_64-linux-gnu.so + 0x161a)
                                                 #8  0x00007f2ed75e6573 n/a (libpython3.13.so.1.0 + 0x1e6573)
                                                 #9  0x00007f2ed756364d PyObject_Vectorcall (libpython3.13.so.1.0 + 0x16364d)
                                                 #10 0x00007f2ed757b769 _PyEval_EvalFrameDefault (libpython3.13.so.1.0 + 0x17b769)
                                                 #11 0x00007f2ed75ce3bc n/a (libpython3.13.so.1.0 + 0x1ce3bc)
                                                 #12 0x00007f2ed76cb1d8 n/a (libpython3.13.so.1.0 + 0x2cb1d8)
                                                 #13 0x00007f2ed76cb15c n/a (libpython3.13.so.1.0 + 0x2cb15c)
                                                 #14 0x00007f2ed709698b n/a (libc.so.6 + 0x9698b)
                                                 #15 0x00007f2ed711a9cc n/a (libc.so.6 + 0x11a9cc)
                                                 ELF object binary architecture: AMD x86-64
```
</details>


---

### 评论 #16 — alexheretic (2026-01-11T01:17:29Z)

I saw no issues after reverting to Linux `6.18.3` -> `6.17.9`. So this does suggest a fairly recent kernel bug is causing this.

---

### 评论 #17 — zichguan-amd (2026-01-16T17:06:24Z)

It's probably this FW issue https://github.com/ROCm/ROCm/issues/5724, should be fixed now in latest package.

---

### 评论 #18 — alexheretic (2026-01-16T21:46:22Z)

> It's probably this FW issue https://github.com/ROCm/ROCm/issues/5724, should be fixed now in latest package.

Doesn't seem so. I re-tested with linux `6.18.5.arch1-1`, linux-firmware-amdgpu `20260110-1` and still can reproduce the issue whereas rolling back to `6.17.9` I cannot.

Details: https://github.com/ROCm/amdgpu/issues/204#issuecomment-3761929985

---

### 评论 #19 — superm1 (2026-01-17T05:20:37Z)

> Doesn't seem so. I re-tested with linux 6.18.5.arch1-1, linux-firmware-amdgpu 20260110-1 and still can reproduce the issue whereas rolling back to 6.17.9 I cannot.

Either move to nightlies or add this patch to your ROCm build: https://github.com/ROCm/rocm-systems/commit/09ba45b3f43ec333a84a0ca178fcd1e3ea9400a9

---

### 评论 #20 — alexheretic (2026-01-17T15:43:19Z)

> Either move to nightlies or add this patch to your ROCm build: https://github.com/ROCm/rocm-systems/commit/09ba45b3f43ec333a84a0ca178fcd1e3ea9400a9

That patch seems to be for gfx1151 which I don't have.

I am currently using the pytorch nightlies, the latest reproduction was with `2.11.0.dev20260110+rocm7.1`. Note: The _rocm_ nightlies at https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ don't seem to have been updated recently so I haven't been using them.

---

### 评论 #21 — alexheretic (2026-01-17T15:58:56Z)

> The rocm nightlies at https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ don't seem to have been updated recently

hmm maybe available at https://rocm.nightlies.amd.com/v2/gfx110X-all now? I can see some newer versions there, I'll try them...

---

### 评论 #22 — superm1 (2026-01-17T16:37:31Z)

> That patch seems to be for gfx1151 which I don't have.

Ah sorry about that.

---

### 评论 #23 — alexheretic (2026-01-17T17:04:16Z)

> hmm maybe available at https://rocm.nightlies.amd.com/v2/gfx110X-all now? I can see some newer versions there, I'll try them...

Still occurs on latest gfx110X-all nightly (torch `2.11.0a0+rocm7.11.0a20260117`) with `6.18.5.arch1-1`. I kinda expect it to be a kernel bug anyway since I see no issues on `6.17.9`.

---

### 评论 #24 — TomatoLoli (2026-01-19T23:03:52Z)

My comfyui setup was a couple months behind and after doing a fresh pull and fresh install of the pip packages nothing worked past a few generations with the error reported by OP. Using an AMD RX9070xt

I tried rocm 7.1, rocm 7.0, rocm6.3, rocm6.4. With no joy on both kernels ~6.12 and 6.18.6

I also tried the setting amdgpu.cwsr_enable=0 and amdgpu.cwsr_enable=1 with no joy. 

What solved this for me with ComfyUI on OpenSuse TW was switching to the LTS kernel 6.12.x and using the launch options `python main.py --use-quad-cross-attention --disable-smart-memory --cache-none`

I think the kernel downgrade might be unnecessary but I’ve been smashing my head against this for a week and its working now. Hope that helps!

---

### 评论 #25 — crmne (2026-01-21T23:22:30Z)

Tested on Arch Linux with AMD Ryzen AI 9 HX 370 / Radeon 890M (gfx1150). Kernels tried: 6.18.3, 6.12-lts, and 6.17.9 from archive: no change.

ROCm OpenCL crashes with "Memory access fault by GPU node-1 (Reason: Page not present or supervisor privilege)" in clinfo and apps.

Tried ROCm 7.1.1 (Arch repo) and TheRock 7.10 via rocm-gfx1150-bin (owns /opt/rocm); same fault.

Kernel params tried: `amdgpu.cwsr_enable=0` and `amdgpu.gpu_recovery=0` (no improvement).

Still hitting memory access faults with ROCm and Rusticl on gfx1150.

---

### 评论 #26 — shssoichiro (2026-01-22T00:19:15Z)

Can anyone confirm if this (and the other 8 duplicate issues) are fixed with ROCm 7.2?

---

### 评论 #27 — crmne (2026-01-22T09:36:05Z)

Update: fixed for me with linux-firmware 20260110 on Arch. The package to apply this is the AUR linux-firmware-git package; my patch pins it to tag 20260110 (the patch itself is NOT in AUR). Gist with PKGBUILD/.SRCINFO changes: https://gist.github.com/crmne/a4958cd66e3d22a02ccada1e27ee3a76

---

### 评论 #28 — leuchthelp (2026-01-22T17:49:09Z)

Still seeing it with gfx1100 (7900 XTX) on Ubuntu 24.04.3 with rocm `Version: 7.2.0.70200-43~24.04` installed on host, inside `rocm/pytorch:latest` container, which should be `rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.9.1` in my case.

---

### 评论 #29 — zichguan-amd (2026-01-22T18:05:21Z)

For gfx1100 on ubuntu, @leuchthelp do you have [dkms](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#amdgpu-driver-installation) installed? It's mostly a driver/firmware issue. There were a few firmware issues that could cause this error, which mostly impacted gfx1151 and should be fixed now. Another reason I've seen is that some in-box drivers are too old/not yet compatible with ROCm and requires `amdgpu-dkms` to work. ubuntu 22.04.5 needs dkms, and I've also seen some reports on ubuntu 24.04.3.

---

### 评论 #30 — leuchthelp (2026-01-22T18:22:50Z)

@zichguan-amd I do, setup a completely fresh install of Ubuntu 24.04.3 (host) just hours earlier, following the quickstart-guide from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html -> into docker install -> into running `rocm/pytorch` on docker following https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html

edit:

To add to this, I'm trying to run [deepseek-ai/DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR#vllm) via vllm using this exact example.

---

### 评论 #31 — superm1 (2026-01-22T19:03:10Z)

Just to be clear- this is the correct URL for Radeon and Ryzen: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/index.html

---

### 评论 #32 — Orangestar12 (2026-01-22T19:06:47Z)

I haven't posted in a while, but the issue has disappeared for me. I don't know if I'm just mitigating the problem heavily or I've actually solved the problem.

On Arch Linux, Kernel 6.18.5-zen1-1-zen
AMD Radeon RX 9070 XT

First, I installed `gfx1200`
```
yay -S rocm-gfx120x-bin
```

Then, in my startup script for comfyui, I do the following:

1. Turn off SDDM
I try to maximize the memory available prior to starting the app just in case. I access the webui through a second device, so this won't be a solution for someone who needs to run a webui and the server on the same device.
```
systemctl stop sddm
```

2. Reset the GPU with `rocm-smi`
```
rocm-smi --gpureset --device 0
```

3. Disable GPU core dumps
Obviously don't do this if you need the dumps, but they tend to pile up.
```
export AMD_SERIALIZE_KERNEL=0
export ROCM_DEBUG=0
```

This seems to have solved the problem for me. I never get a memory access fault if I make sure these operations are done in order.

---

### 评论 #33 — leuchthelp (2026-01-22T19:23:10Z)

> Just to be clear- this is the correct URL for Radeon and Ryzen: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/index.html

Correct, went there after reading the note about "using rocm with radeon" - just to clarify

Went with docker container install after, instead of bare-metal like would be instructed next with the [radeon docs](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html) purely for convenience reasons

---

### 评论 #34 — GuardianLiarus (2026-01-31T10:06:42Z)

In case that can help any diagnosis, i have found that using `--fp32-vae` with comfyui has completely stopped the issue from happening, albeit the VAE Decoding being slower now.

I'd like to mention:

1. Using different Python versions changed nothing for me
2. Using different ROCM versions from pytorch.org and therock nightlies changed nothing
3. Using different Kernel versions didn't change anything
4. Waiting for the AMD firmware updates didn't change anything either.

When not using `--fp32-vae`  i noticed that queuing a lot of jobs was what tend to make the error trigger, it was way less likely if things were done one by one.


---

### 评论 #35 — r4dm (2026-02-02T12:25:29Z)

> Is `amdgpu.cwsr_enable=0` the solution?
> 
> [#4846 (comment)](https://github.com/ROCm/ROCm/issues/4846#issuecomment-3617170494)

it works! (strix halo)

---

### 评论 #36 — chrisb123 (2026-02-11T21:54:33Z)

I'm still experiencing this same issue.
debian 6.12.69+deb13-amd64
romc 7.2
amdgpu-30.30
tried amdgpu.cwsr_enable=0

---

### 评论 #37 — jyggen (2026-02-17T15:20:41Z)

I can confirm that using `--fp32-vae` in ComfyUI resolves the issue for me. Without it I run into `[Memory access fault by GPU node-1` errors after a couple of workflow runs. I haven't tried a similar setting in sdnext yet, but I had the same issue there so the error is not exclusive to ComfyUI. I've tried `amdgpu.cwsr_enable=0` as well without success.

Radeon RX 9070 XT on Linux 6.18.9-arch-2.

system packages:
```
linux-firmware-amdgpu 20260110-1
mesa 1:25.3.5-1
rocm-cmake 7.2.0-1
rocm-core 7.2.0-2
rocm-device-libs 2:7.2.0-1
rocm-hip-runtime 7.2.0-1
rocminfo 7.2.0-1
rocm-language-runtime 7.2.0-1
rocm-llvm 2:7.2.0-1
rocm-smi-lib 7.2.0-1
```
python packages:
```
rocm-7.12.0a20260212
rocm-sdk-core-7.12.0a20260212
rocm-sdk-libraries-gfx120X-all-7.12.0a20260212
torch-2.9.1+rocm7.12.0a20260212
torchaudio-2.9.0+rocm7.12.0a20260212
torchvision-0.24.0+rocm7.12.0a20260212
triton-3.5.1+rocm7.12.0a20260212
```



---

### 评论 #38 — c0rb4c (2026-02-18T17:23:06Z)

For me adding "--disable-smart-memory" solves absolutely everything whichever is the workflow. Don't know what it does exactly but not one single crash on my Radeon AI Pro R9700 since then.

---

### 评论 #39 — jyggen (2026-02-18T17:50:34Z)

Yes, `--disable-smart-memory` seems to work great as well but without the slowdown seen with `--fp32-vae`. Thanks!

---

### 评论 #40 — TomatoLoli (2026-04-05T03:55:03Z)

Installing this resolved the problem for me. 

https://download.pytorch.org/whl/rocm7.2

---

### 评论 #41 — GuardianLiarus (2026-04-08T18:37:50Z)

> Installing this resolved the problem for me.
> 
> https://download.pytorch.org/whl/rocm7.2

I can also confirm it seems to be fixed in the 7.2 stable release ! 

No `--fp32-vae` or `--disable-smart-memory` needed

---

### 评论 #42 — leucome (2026-05-18T01:19:04Z)

This started to happen for me even with pytorch rocm7.2 and Linux kernel 7.   Also began after updating from an older installation.


---
