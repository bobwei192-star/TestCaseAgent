# [Issue]: HIP error: an illegal memory access was encountered, hipErrorIllegalAddress (on RX 6700 XT, ROCm 7.2)

> **Issue #6003**
> **状态**: open
> **创建时间**: 2026-02-26T09:52:15Z
> **更新时间**: 2026-04-01T16:48:17Z
> **作者**: pkrasicki
> **标签**: Under Investigation, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6003

## 标签

- **Under Investigation** (颜色: #0052cc)
- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

I keep getting memory related crashes in ComfyUI (and PyTorch in general). It's been happening since at least ROCm 7.0. It's random and unpredictable, I don't know of any consistent way to reproduce it. Sometimes it will happen after long usage, sometimes right away, sometimes it doesn't happen at all.

I'm currently using ROCm 7.2, I installed the following packages:
```
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torch-2.9.1%2Brocm7.2.0.lw.git7e1940d4-cp313-cp313-linux_x86_64.whl
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchvision-0.24.0%2Brocm7.2.0.gitb919bd0c-cp313-cp313-linux_x86_64.whl
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/triton-3.5.1%2Brocm7.2.0.gita272dfa8-cp313-cp313-linux_x86_64.whl
https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchaudio-2.9.0%2Brocm7.2.0.gite3c6ee2b-cp313-cp313-linux_x86_64.whl
```

Previously I used official builds from PyTorch and the issue happened there too.

Full ComfyUI log (I only removed some logs from custom nodes to make it more readable):
```
$ HSA_OVERRIDE_GFX_VERSION=10.3.0 python main.py

[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** Platform: Linux
** Python version: 3.13.5 (main, Jun 25 2025, 18:55:22) [GCC 14.2.0]
** Python executable: /mnt/AI/ComfyUI/env/bin/python
** ComfyUI Path: /mnt/AI/ComfyUI
** ComfyUI Base Folder Path: /mnt/AI/ComfyUI
** User directory: /mnt/AI/ComfyUI/user
** ComfyUI-Manager config path: /mnt/AI/ComfyUI/user/__manager/config.ini
** Log path: /mnt/AI/ComfyUI/user/comfyui.log

Checkpoint files will always be loaded safely.
Found comfy_kitchen backend cuda: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Found comfy_kitchen backend triton: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Found comfy_kitchen backend eager: {'available': True, 'disabled': False, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Total VRAM 12272 MB, total RAM 28026 MB
pytorch version: 2.9.1+rocm7.2.0.git7e1940d4
AMD arch: gfx1030
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 6700 XT : native
Using async weight offloading with 2 streams
Enabled pinned memory 26624.0
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
Python version: 3.13.5 (main, Jun 25 2025, 18:55:22) [GCC 14.2.0]
ComfyUI version: 0.13.0
ComfyUI frontend version: 1.38.13
[Prompt Server] web root: /mnt/AI/ComfyUI/env/lib/python3.13/site-packages/comfyui_frontend_package/static
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
ComfyUI-GGUF: Allowing full torch compile
Context impl SQLiteImpl.
Will assume non-transactional DDL.
Assets scan(roots=['models']) completed in 0.502s (created=0, skipped_existing=674, orphans_pruned=0, total_seen=747)
Starting server
To see the GUI go to: http://127.0.0.1:8188
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/groupNode.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/widgetInputs.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/button.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/buttonGroup.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.float32
Found quantization metadata version 1
Using MixedPrecisionOps for text encoder
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load Flux2TEModel_
loaded completely; 10800.80 MB usable, 8263.34 MB loaded, full load: True
gguf qtypes: F32 (80), Q8_0 (112), BF16 (9)
model weight dtype torch.float16, manual cast: None
model_type FLUX
Requested to load Flux2
!!! Exception during processing !!! HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

Traceback (most recent call last):
  File "/mnt/AI/ComfyUI/execution.py", line 530, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/execution.py", line 334, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/custom_nodes/ComfyUI-Lora-Manager/py/metadata_collector/metadata_hook.py", line 168, in async_map_node_over_list_with_metadata
    results = await original_map_node_over_list(
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
    )
    ^
  File "/mnt/AI/ComfyUI/execution.py", line 308, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/mnt/AI/ComfyUI/execution.py", line 296, in process_inputs
    result = f(**inputs)
  File "/mnt/AI/ComfyUI/comfy_api/internal/__init__.py", line 149, in wrapped_func
    return method(locked_class, **inputs)
  File "/mnt/AI/ComfyUI/comfy_api/latest/_io.py", line 1710, in EXECUTE_NORMALIZED
    to_return = cls.execute(*args, **kwargs)
  File "/mnt/AI/ComfyUI/comfy_extras/nodes_custom_sampler.py", line 963, in execute
    samples = guider.sample(noise.generate_noise(latent), latent_image, sampler, sigmas, denoise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=noise.seed)
  File "/mnt/AI/ComfyUI/comfy/samplers.py", line 1049, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/mnt/AI/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/samplers.py", line 983, in outer_sample
    self.inner_model, self.conds, self.loaded_models = comfy.sampler_helpers.prepare_sampling(self.model_patcher, noise.shape, self.conds, self.model_options)
                                                       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/sampler_helpers.py", line 130, in prepare_sampling
    return executor.execute(model, noise_shape, conds, model_options=model_options, force_full_load=force_full_load)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/sampler_helpers.py", line 138, in _prepare_sampling
    comfy.model_management.load_models_gpu([model] + models, memory_required=memory_required + inference_memory, minimum_memory_required=minimum_memory_required + inference_memory, force_full_load=force_full_load)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 716, in load_models_gpu
    free_memory(total_memory_required[device] * 1.1 + extra_mem, device, for_dynamic=free_for_dynamic, ram_required=total_ram_required[device])
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 635, in free_memory
    if memory_to_free > 0 and current_loaded_models[i].model_unload(memory_to_free):
                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 551, in model_unload
    self.model.detach(unpatch_weights)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_patcher.py", line 1021, in detach
    self.unpatch_model(self.offload_device, unpatch_weights=unpatch_all)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/comfy/model_patcher.py", line 886, in unpatch_model
    self.model.to(device_to)
    ~~~~~~~~~~~~~^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1371, in to
    return self._apply(convert)
           ~~~~~~~~~~~^^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  [Previous line repeated 4 more times]
  File "/mnt/AI/ComfyUI/comfy/ops.py", line 914, in _apply
    self.register_parameter(key, torch.nn.Parameter(fn(param), requires_grad=False))
                                                    ~~^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1357, in convert
    return t.to(
           ~~~~^
        device,
        ^^^^^^^
        dtype if t.is_floating_point() or t.is_complex() else None,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        non_blocking,
        ^^^^^^^^^^^^^
    )
    ^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


Prompt executed in 94.48 seconds
Exception in thread Thread-2 (prompt_worker):
Traceback (most recent call last):
  File "/usr/lib/python3.13/threading.py", line 1043, in _bootstrap_inner
    self.run()
    ~~~~~~~~^^
  File "/usr/lib/python3.13/threading.py", line 994, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/main.py", line 302, in prompt_worker
    comfy.model_management.soft_empty_cache()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/mnt/AI/ComfyUI/comfy/model_management.py", line 1702, in soft_empty_cache
    torch.cuda.synchronize()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/__init__.py", line 1082, in synchronize
    with torch.cuda.device(device):
         ~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/__init__.py", line 529, in __init__
    self.idx = _get_device_index(device, optional=True)
               ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/_utils.py", line 373, in _get_device_index
    return _torch_get_device_index(device, optional, allow_cpu)
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 870, in _get_device_index
    device_idx = _get_current_device_index()
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 807, in _get_current_device_index
    return _get_device_attr(lambda m: m.current_device())
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 792, in _get_device_attr
    return get_member(torch.cuda)
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/_utils.py", line 807, in <lambda>
    return _get_device_attr(lambda m: m.current_device())
                                      ~~~~~~~~~~~~~~~~^^
  File "/mnt/AI/ComfyUI/env/lib/python3.13/site-packages/torch/cuda/__init__.py", line 1070, in current_device
    return torch._C._cuda_getDevice()
           ~~~~~~~~~~~~~~~~~~~~~~~~^^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

### Operating System

Debian 13

### CPU

Intel i5-4690K

### GPU

RX 6700 XT

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

It happens with different workflows and different models. There isn't a simple, consistent way to reproduce it.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

I set the `HSA_OVERRIDE_GFX_VERSION=10.3.0` environment variable, since it's the only way for RX 6700 XT to work in ROCm. It works fine, except for the occasional random crashes.

I've heard that setting some kernel parameter might fix those crashes, but I didn't try it, because I don't understand what it does or what the downsides are.

I have ROCm 7.1 from AMD's repo installed on my system, but PyTorch uses its own version (ROCm 7.2 in this case), so it shouldn't matter here.

---

## 评论 (7 条)

### 评论 #1 — tcgu-amd (2026-02-26T20:23:17Z)

HI @pkrasicki! Thanks for opening the issue! The other illegal memory access issue was caused by hipblaslt's expert scheduling mode, which could be temporarily fixed by disabling cwsr via `amdgpu.cwsr_enable=0`. CWSR(compute wave store and resume) allows the GPU to preempt shader execution in the middle of a compute wave. Disabling it helps avoid the scheduling conflict. Albeit the downside is that it changes the program serialization and might introduce performance loss. Please feel free to give it a try and see if it helps with your problem at all. If not, then this could be an independent issue. Thanks! 

---

### 评论 #2 — chejh-amd (2026-03-02T06:52:31Z)

Hi @pkrasicki How about disabling amdgpu.cwsr_enable=0, did it work?

---

### 评论 #3 — xuzhen (2026-03-05T17:15:19Z)

I've also encountered this issue on my system. The torch, torchaudio, torchvision and triton-rocm packages were downloaded from https://download.pytorch.org/whl/test/
<details>

```
Total VRAM 24560 MB, total RAM 64242 MB
pytorch version: 2.11.0+rocm7.2
AMD arch: gfx1100
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 Radeon RX 7900 XTX : native
Using async weight offloading with 2 streams
Enabled pinned memory 61029.0
Using pytorch attention
Python version: 3.13.12 (main, Feb  4 2026, 15:06:39) [GCC 15.2.0]
ComfyUI version: 0.15.1
ComfyUI frontend version: 1.39.19

......

terminate called after throwing an instance of 'c10::AcceleratorError'
  what():  CUDA error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Device-side assertion tracking was not enabled by user.
Exception raised from SetDevice at /pytorch/c10/hip/HIPFunctions.cpp:334 (most recent call first):
frame #0: c10::Error::Error(c10::SourceLocation, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >) + 0x98 (0x7f390a0f9648 in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libc10.so)
frame #1: <unknown function> + 0x4bf9a (0x7f3980147f9a in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libc10_hip.so)
frame #2: c10::cuda::c10_cuda_check_implementation(int, char const*, char const*, unsigned int, bool) + 0x1fd (0x7f3980147afd in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libc10_hip.so)
frame #3: c10::cuda::SetDevice(signed char, bool) + 0x9a (0x7f3980148bfa in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libc10_hip.so)
frame #4: <unknown function> + 0x34d8987 (0x7f3983742987 in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_hip.so)
frame #5: <unknown function> + 0x3599ad5 (0x7f3983803ad5 in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_hip.so)
frame #6: <unknown function> + 0xdd6bcb (0x7f3981040bcb in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_hip.so)
frame #7: at::_ops::bmm::call(at::Tensor const&, at::Tensor const&) + 0x19e (0x7f39a251fc3e in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_cpu.so)
frame #8: <unknown function> + 0x2090a7b (0x7f39a176fa7b in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_cpu.so)
frame #9: at::native::matmul(at::Tensor const&, at::Tensor const&) + 0x40 (0x7f39a17705d0 in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_cpu.so)
frame #10: <unknown function> + 0x34164b0 (0x7f39a2af54b0 in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_cpu.so)
frame #11: at::_ops::matmul::call(at::Tensor const&, at::Tensor const&) + 0x19e (0x7f39a267564e in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_cpu.so)
frame #12: <unknown function> + 0x4f4dc9 (0x7f39b5845dc9 in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_python.so)
frame #13: <unknown function> + 0x4f4e77 (0x7f39b5845e77 in /media/ComfyUI/venv/lib/python3.13/site-packages/torch/lib/libtorch_python.so)
frame #14: python3() [0x59ed7b]
frame #15: python3() [0x652212]
frame #16: python3() [0x4d6e0e]
frame #17: python3() [0x5cc0cb]
<omitting python frames>
frame #19: python3() [0x5dd0a7]
frame #21: python3() [0x5dd0a7]
frame #23: python3() [0x6a967b]
frame #24: python3() [0x64191d]
frame #27: python3() [0x5dd0a7]
frame #29: python3() [0x5dd0a7]
frame #31: python3() [0x6a967b]
frame #32: python3() [0x64191d]
frame #35: python3() [0x5dd0a7]
frame #37: python3() [0x5dd0a7]
frame #39: python3() [0x6a967b]
frame #40: python3() [0x64191d]
frame #43: python3() [0x5dd11c]
frame #44: python3() [0x5baa3f]
frame #46: python3() [0x6ba3c6]
frame #47: <unknown function> + 0x9848 (0x7f39baa2e848 in /usr/lib/python3.13/lib-dynload/_asyncio.cpython-313-x86_64-linux-gnu.so)
frame #48: <unknown function> + 0x96e6 (0x7f39baa2e6e6 in /usr/lib/python3.13/lib-dynload/_asyncio.cpython-313-x86_64-linux-gnu.so)
frame #50: python3() [0x715774]
frame #51: python3() [0x58add0]
frame #53: python3() [0x5dd01a]
frame #54: python3() [0x6f6330]
frame #55: python3() [0x69e188]
frame #56: <unknown function> + 0x95469 (0x7f39bbbd4469 in /usr/lib/x86_64-linux-gnu/libc.so.6)
frame #57: <unknown function> + 0x113cf8 (0x7f39bbc52cf8 in /usr/lib/x86_64-linux-gnu/libc.so.6)
```
</details>


The `dmesg` shows some page fault errors
<details>

```
[  402.306415] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306423] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306427] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2bf000 from client 10
[  402.306430] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306433] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306436] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306439] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306442] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306445] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306447] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306454] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306457] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306461] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2b0000 from client 10
[  402.306464] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306466] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306469] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306472] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306474] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306477] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306479] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306487] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306490] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306493] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2b9000 from client 10
[  402.306496] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306499] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306502] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306504] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306507] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306509] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306512] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306518] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306521] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306524] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2b6000 from client 10
[  402.306527] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306530] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306532] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306535] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306537] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306540] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306542] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306548] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306552] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306555] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2c8000 from client 10
[  402.306557] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306560] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306563] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306565] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306568] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306570] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306573] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306579] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306582] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306585] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2e3000 from client 10
[  402.306589] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306592] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306595] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306597] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306600] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306602] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306606] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306614] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306617] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306620] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2b3000 from client 10
[  402.306623] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306627] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306630] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306632] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306635] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306637] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306640] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306646] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306649] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306652] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae280000 from client 10
[  402.306655] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306658] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306660] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306663] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306665] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306668] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306670] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306676] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306680] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306683] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2c2000 from client 10
[  402.306686] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306688] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306694] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306696] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306699] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306701] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306704] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.306710] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32772)
[  402.306713] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 4010 thread python3 pid 4010
[  402.306716] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f32ae2dd000 from client 10
[  402.306719] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  402.306722] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  402.306724] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  402.306727] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  402.306729] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  402.306732] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  402.306734] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  402.309423] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  402.309435] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  402.309442] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  402.309448] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[  402.309456] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  402.309461] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  402.309467] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  402.309475] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  402.309482] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[  402.309488] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
```
</details>


With amdgpu.cwsr_enable=0, It became WORSE: the whole desktop environment crashed. Additional GPU reset errors appeared in `dmesg`
<details>

```
[  738.639536] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639544] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639548] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08c8f000 from client 10
[  738.639552] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639555] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639559] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639562] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639564] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639567] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639570] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639577] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639581] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639586] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08c80000 from client 10
[  738.639589] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639592] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639595] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639598] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639600] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639603] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639606] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639612] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639616] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639619] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08c89000 from client 10
[  738.639622] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639625] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639628] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639630] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639633] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639636] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639638] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639644] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639648] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639651] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08c86000 from client 10
[  738.639654] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639657] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639660] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639663] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639665] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639668] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639671] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639677] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639680] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639684] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08ce0000 from client 10
[  738.639687] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639689] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639692] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639695] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639698] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639700] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639703] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639709] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639713] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639716] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08c83000 from client 10
[  738.639719] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639722] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639725] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639727] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639732] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639734] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639737] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639743] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639747] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639750] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08ce9000 from client 10
[  738.639753] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639756] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639758] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639764] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639766] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639769] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639773] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639779] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639785] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639789] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08c95000 from client 10
[  738.639792] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639794] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639797] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639804] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639806] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639809] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639812] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639818] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639823] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639826] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08ce3000 from client 10
[  738.639829] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639833] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639836] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639841] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639844] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639847] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639849] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  738.639855] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775)
[  738.639859] amdgpu 0000:2f:00.0: amdgpu:  Process python3 pid 28912 thread python3 pid 28912
[  738.639862] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00007f8e08c9b000 from client 10
[  738.639865] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  738.639868] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  738.639871] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  738.639873] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  738.639876] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  738.639879] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  738.639881] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[  740.639966] amdgpu 0000:2f:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  740.639975] amdgpu 0000:2f:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[  740.639978] amdgpu 0000:2f:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  740.639983] amdgpu 0000:2f:00.0: amdgpu: Failed to evict queue 1
[  740.639988] amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!. Source:  3
[  740.639991] print_sq_intr_info_error: 1190 callbacks suppressed
[  740.639993] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640006] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640012] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640019] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640025] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640031] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640037] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640042] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640048] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640055] amdgpu 0000:2f:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[  740.640476] amdgpu 0000:2f:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 34301
[  740.640508] amdgpu 0000:2f:00.0: amdgpu: Dumping IP State
[  740.641636] amdgpu 0000:2f:00.0: amdgpu: Dumping IP State Completed
[  742.771441] amdgpu 0000:2f:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  742.771449] amdgpu 0000:2f:00.0: amdgpu: failed to unmap legacy queue
[  743.010523] [drm:gfx_v11_0_cp_gfx_enable.isra.0 [amdgpu]] *ERROR* failed to halt cp gfx
[  743.059033] amdgpu 0000:2f:00.0: amdgpu: MODE1 reset
[  743.059037] amdgpu 0000:2f:00.0: amdgpu: GPU mode1 reset
[  743.059096] amdgpu 0000:2f:00.0: amdgpu: GPU smu mode1 reset
[  743.560997] amdgpu 0000:2f:00.0: amdgpu: GPU reset succeeded, trying to resume
[  743.561110] [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
[  743.561148] amdgpu 0000:2f:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[  743.561150] amdgpu 0000:2f:00.0: amdgpu: [drm] Check your /sys/class/drm/card0/device/devcoredump/data
[  743.561153] amdgpu 0000:2f:00.0: amdgpu: VRAM is lost due to GPU reset!
[  743.561155] amdgpu 0000:2f:00.0: amdgpu: PSP is resuming...
[  743.631620] amdgpu 0000:2f:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[  743.781019] amdgpu 0000:2f:00.0: amdgpu: RAP: optional rap ta ucode is not available
[  743.781022] amdgpu 0000:2f:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[  743.781025] amdgpu 0000:2f:00.0: amdgpu: SMU is resuming...
[  743.781030] amdgpu 0000:2f:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8300 (78.131.0)
[  743.781035] amdgpu 0000:2f:00.0: amdgpu: SMU driver if version not matched
[  743.931411] amdgpu 0000:2f:00.0: amdgpu: SMU is resumed successfully!
[  743.944480] amdgpu 0000:2f:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002F00
[  743.996837] amdgpu 0000:2f:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  743.996842] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  743.996844] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  743.996847] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  743.996849] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  743.996851] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  743.996853] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  743.996856] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  743.996858] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  743.996860] amdgpu 0000:2f:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  743.996863] amdgpu 0000:2f:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  743.996865] amdgpu 0000:2f:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  743.996868] amdgpu 0000:2f:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[  743.996870] amdgpu 0000:2f:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[  743.996872] amdgpu 0000:2f:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[  744.001244] amdgpu 0000:2f:00.0: amdgpu: GPU reset(2) succeeded!
[  744.015134] amdgpu 0000:2f:00.0: [drm] device wedged, but recovered through reset
```
</details>

I found that the problem was caused by an environment variable `PYTORCH_TUNABLEOP_ENABLED=1` I had set for ROCM 6.x. After removing that variable, ROCM 7.x no longer produces the hipErrorIllegalAddress error.

---

### 评论 #4 — spot94 (2026-03-11T05:31:12Z)

I have the same issue, it appears in workflows with **IPAdapter** nodes.
OS: Kubuntu 25.10 (kernel 6.18)
ROCm 7.1.1
GPU: RX 6700XT

Disabling `PYTORCH_TUNABLEOP_ENABLED` is solving the issue

---

### 评论 #5 — tcgu-amd (2026-03-27T19:22:42Z)

Hi @pkrasicki @spot94  @xuzhen , can you verify if the issue still exists on the latest ROCm 7.2.1 with the latest amdgpu-dkms? Thanks! 

---

### 评论 #6 — xuzhen (2026-03-29T12:01:29Z)

@tcgu-amd  tried the wheels from https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2.1/, still the same error with `PYTORCH_TUNABLEOP_ENABLED=1`.

<details>

```
Total VRAM 24560 MB, total RAM 64242 MB
pytorch version: 2.9.1+rocm7.2.1.gitff65f5bc
AMD arch: gfx1100
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 7900 XTX : native
Using async weight offloading with 2 streams
Enabled pinned memory 61029.0
Using pytorch attention
Python version: 3.13.12 (main, Feb  4 2026, 15:06:39) [GCC 15.2.0]
ComfyUI version: 0.17.0
comfy-aimdo version: 0.2.12
comfy-kitchen version: 0.2.8

......

/media/ComfyUI/venv/lib/python3.13/site-packages/segment_anything/modeling/image_encoder.py:231: UserWarning: HIP warning: an illegal memory access was encountered (Triggered internally at /pytorch/aten/src/ATen/hip/impl/HIPGuardImplMasqueradingAsCUDA.h:83.)
  attn = (q * self.scale) @ k.transpose(-2, -1)
!!! Exception during processing !!! HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

Traceback (most recent call last):
  File "/run/media/ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact/core.py", line 884, in make_sam_mask
    detected_masks = sam_obj.predict(image, points, plabs, dilated_bbox, threshold)
  File "/run/media/ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact/core.py", line 634, in predict
    predictor.set_image(image, "RGB")
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/segment_anything/predictor.py", line 60, in set_image
    self.set_torch_image(input_image_torch, image.shape[:2])
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
    return func(*args, **kwargs)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/segment_anything/predictor.py", line 89, in set_torch_image
    self.features = self.model.image_encoder(input_image)
                    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
    return forward_call(*args, **kwargs)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/segment_anything/modeling/image_encoder.py", line 112, in forward
    x = blk(x)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
    return forward_call(*args, **kwargs)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/segment_anything/modeling/image_encoder.py", line 174, in forward
    x = self.attn(x)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
    return forward_call(*args, **kwargs)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/segment_anything/modeling/image_encoder.py", line 231, in forward
    attn = (q * self.scale) @ k.transpose(-2, -1)
           ~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/run/media/ComfyUI/execution.py", line 525, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/media/ComfyUI/execution.py", line 334, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/media/ComfyUI/execution.py", line 308, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/run/media/ComfyUI/execution.py", line 296, in process_inputs
    result = f(**inputs)
  File "/run/media/ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact/impact_pack.py", line 876, in doit
    enhanced_img, cropped_enhanced, cropped_enhanced_alpha, mask, cnet_pil_list = FaceDetailer.enhance_face(
                                                                                  ~~~~~~~~~~~~~~~~~~~~~~~~~^
        single_image.unsqueeze(0), model, clip, vae, guide_size, guide_size_for, max_size, seed + i, steps, cfg, sampler_name, scheduler,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
        cycle=cycle, inpaint_model=inpaint_model, noise_mask_feather=noise_mask_feather, scheduler_func_opt=scheduler_func_opt,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        tiled_encode=tiled_encode, tiled_decode=tiled_decode)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/media/ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact/impact_pack.py", line 813, in enhance_face
    sam_mask = core.make_sam_mask(sam_model_opt, segs, image, sam_detection_hint, sam_dilation,
                                  sam_threshold, sam_bbox_expansion, sam_mask_hint_threshold,
                                  sam_mask_hint_use_negative, )
  File "/run/media/ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact/core.py", line 891, in make_sam_mask
    sam_obj.release_device()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/run/media/ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact/core.py", line 630, in release_device
    self.model.to(device="cpu")
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1371, in to
    return self._apply(convert)
           ~~~~~~~~~~~^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 930, in _apply
    module._apply(fn)
    ~~~~~~~~~~~~~^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 957, in _apply
    param_applied = fn(param)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1357, in convert
    return t.to(
           ~~~~^
        device,
        ^^^^^^^
        dtype if t.is_floating_point() or t.is_complex() else None,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        non_blocking,
        ^^^^^^^^^^^^^
    )
    ^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


Prompt executed in 97.12 seconds
Exception in thread Thread-4 (prompt_worker):
Traceback (most recent call last):
  File "/usr/lib/python3.13/threading.py", line 1044, in _bootstrap_inner
    self.run()
    ~~~~~~~~^^
  File "/usr/lib/python3.13/threading.py", line 995, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/media/ComfyUI/./main.py", line 316, in prompt_worker
    comfy.model_management.soft_empty_cache()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/run/media/ComfyUI/comfy/model_management.py", line 1778, in soft_empty_cache
    torch.cuda.synchronize()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/cuda/__init__.py", line 1082, in synchronize
    with torch.cuda.device(device):
         ~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/cuda/__init__.py", line 529, in __init__
    self.idx = _get_device_index(device, optional=True)
               ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/cuda/_utils.py", line 373, in _get_device_index
    return _torch_get_device_index(device, optional, allow_cpu)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/_utils.py", line 870, in _get_device_index
    device_idx = _get_current_device_index()
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/_utils.py", line 807, in _get_current_device_index
    return _get_device_attr(lambda m: m.current_device())
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/_utils.py", line 792, in _get_device_attr
    return get_member(torch.cuda)
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/_utils.py", line 807, in <lambda>
    return _get_device_attr(lambda m: m.current_device())
                                      ~~~~~~~~~~~~~~~~^^
  File "/media/ComfyUI/venv/lib/python3.13/site-packages/torch/cuda/__init__.py", line 1070, in current_device
    return torch._C._cuda_getDevice()
           ~~~~~~~~~~~~~~~~~~~~~~~~^^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```
</details>


---

### 评论 #7 — Penguin-Guru (2026-03-31T02:32:37Z)

I'm not sure if the issue I encountered is the same as this one but I was able to resolve a similar problem by forcing pip to update all the relevant dependencies. The parameter is `--force-reinstall`.

I will include the full command for reference, but the value of `--index-url` varies depending on the G.P.U. model/family. The value I used was selected from the options [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-pytorch-python-packages).

`python -s -m pip install --force-reinstall --pre torch torchaudio torchvision --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all --no-cache-dir`

---
