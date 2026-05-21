# [Issue]: Illegal memory access torch.AcceleratorError: HIP error: an illegal memory access `hipErrorIllegalAddress'

> **Issue #5742**
> **状态**: closed
> **创建时间**: 2025-12-04T23:29:41Z
> **更新时间**: 2026-02-11T15:28:58Z
> **关闭时间**: 2026-02-11T15:28:58Z
> **作者**: FR-Mister-T
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5742

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- zichguan-amd

## 描述

### Problem Description

Hello,

I'm running into this error in regular basis (comfyui ubuntu). 
I believe that it the fact I'm juggling between 2 simple workflow
1 ollama vision model (qwen 3vl and gemma3) 
1 Inference wf, using netayume lumina 2 model


# ComfyUI Error Report
## Error Details
- **Node ID:** 25
- **Node Type:** KSampler
- **Exception Type:** torch.AcceleratorError
- **Exception Message:** HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


## Stack Trace
```
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 515, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 329, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 303, in _async_map_node_over_list
    await process_inputs(input_dict, i)

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 291, in process_inputs
    result = f(**inputs)

  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1538, in sample
    return common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)

  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 131, in KSampler_sample
    return orig_fn(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1163, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 149, in sample
    return orig_fn(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1053, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1035, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 997, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 114, in KSAMPLER_sample
    return orig_fn(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 212, in sample_euler_ancestral
    return sample_euler_ancestral_RF(model, x, sigmas, extra_args, callback, disable, eta, s_noise, noise_sampler)

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 246, in sample_euler_ancestral_RF
    if sigmas[i + 1] == 0:
       ^^^^^^^^^^^^^^^^^^

```
## System Information
- **ComfyUI Version:** 0.3.76
- **Arguments:** main.py
- **OS:** linux
- **Python Version:** 3.13.10 (main, Dec  3 2025, 08:59:02) [GCC 13.3.0]
- **Embedded Python:** false
- **PyTorch Version:** 2.10.0.dev20251124+rocm7.1
## Devices

- **Name:** cuda:0 AMD Radeon AI PRO R9700 : native
  - **Type:** cuda
  - **VRAM Total:** 34208743424
  - **VRAM Free:** 34131148800
  - **Torch VRAM Total:** 0
  - **Torch VRAM Free:** 0

## Logs
```
2025-12-04T23:43:13.640095 - [92m[rgthree-comfy] Loaded 48 magnificent nodes. 🎉[0m2025-12-04T23:43:13.640111 - 
2025-12-04T23:43:13.640126 - 
2025-12-04T23:43:13.640158 - [33m[rgthree-comfy] ComfyUI's new Node 2.0 rendering may be incompatible with some rgthree-comfy nodes and features, breaking some rendering as well as losing the ability to access a node's properties (a vital part of many nodes). It also appears to run MUCH more slowly spiking CPU usage and causing jankiness and unresponsiveness, especially with large workflows. Personally I am not planning to use the new Nodes 2.0 and, unfortunately, am not able to invest the time to investigate and overhaul rgthree-comfy where needed. If you have issues when Nodes 2.0 is enabled, I'd urge you to switch it off as well and join me in hoping ComfyUI is not planning to deprecate the existing, stable canvas rendering all together.
[0m2025-12-04T23:43:13.640175 - 
2025-12-04T23:43:13.644630 - --------------------- Jake Upgrade Nodes ---------------------2025-12-04T23:43:13.644659 - 
2025-12-04T23:43:13.644822 - 🔶 Version 2.3.142025-12-04T23:43:13.644842 - 
2025-12-04T23:43:13.645267 - 🔶 Config file loaded successfully2025-12-04T23:43:13.645288 - 
2025-12-04T23:43:13.645333 - 🔶 Using standard version of RandomPrompter2025-12-04T23:43:13.645350 - 
2025-12-04T23:43:13.653082 - 🔶 All main modules loaded2025-12-04T23:43:13.653111 - 
2025-12-04T23:43:13.653129 - 🔶 No deprecated nodes loaded2025-12-04T23:43:13.653144 - 
2025-12-04T23:43:13.653606 - 🔶 Total nodes: 1042025-12-04T23:43:13.653628 - 
2025-12-04T23:43:13.653644 - --------------------------------------------------------------2025-12-04T23:43:13.653657 - 
2025-12-04T23:43:13.655457 - AMD GPU Monitor thread started2025-12-04T23:43:13.655490 - 
2025-12-04T23:43:13.655712 - Using AMD SMI tool: /opt/rocm/bin/rocm-smi2025-12-04T23:43:13.655818 - AMD GPU Monitor: Web directory set to /home/zeuss194/COMFY/ComfyUI/custom_nodes/amdgpumonitor/web2025-12-04T23:43:13.655846 - 
2025-12-04T23:43:13.655952 - 
2025-12-04T23:43:13.658290 - [MultiGPU Core Patching] Patching mm.soft_empty_cache for Comprehensive Memory Management (VRAM + CPU + Store Pruning)
2025-12-04T23:43:13.659407 - [MultiGPU Core Patching] Patching mm.get_torch_device, mm.text_encoder_device, mm.unet_offload_device
2025-12-04T23:43:13.659615 - [MultiGPU DEBUG] Initial current_device: cuda:0
2025-12-04T23:43:13.659766 - [MultiGPU DEBUG] Initial current_text_encoder_device: cuda:0
2025-12-04T23:43:13.659905 - [MultiGPU DEBUG] Initial current_unet_offload_device: cpu
2025-12-04T23:43:13.662389 - [MultiGPU] Initiating custom_node Registration. . .
2025-12-04T23:43:13.662549 - -----------------------------------------------
2025-12-04T23:43:13.662705 - custom_node                   Found     Nodes
2025-12-04T23:43:13.662845 - -----------------------------------------------
2025-12-04T23:43:13.663481 - ComfyUI-LTXVideo                  N         0
2025-12-04T23:43:13.663652 - ComfyUI-Florence2                 Y         2
2025-12-04T23:43:13.663801 - ComfyUI_bitsandbytes_NF4          N         0
2025-12-04T23:43:13.663946 - x-flux-comfyui                    N         0
2025-12-04T23:43:13.664094 - ComfyUI-MMAudio                   N         0
2025-12-04T23:43:13.664238 - ComfyUI-GGUF                      Y        18
2025-12-04T23:43:13.664379 - PuLID_ComfyUI                     N         0
2025-12-04T23:43:13.664521 - ComfyUI-WanVideoWrapper           N         0
2025-12-04T23:43:13.664673 - -----------------------------------------------
2025-12-04T23:43:13.664855 - [MultiGPU] Registration complete. Final mappings: CheckpointLoaderAdvancedMultiGPU, CheckpointLoaderAdvancedDisTorch2MultiGPU, UNetLoaderLP, UNETLoaderMultiGPU, VAELoaderMultiGPU, CLIPLoaderMultiGPU, DualCLIPLoaderMultiGPU, TripleCLIPLoaderMultiGPU, QuadrupleCLIPLoaderMultiGPU, CLIPVisionLoaderMultiGPU, CheckpointLoaderSimpleMultiGPU, ControlNetLoaderMultiGPU, DiffusersLoaderMultiGPU, DiffControlNetLoaderMultiGPU, UNETLoaderDisTorch2MultiGPU, VAELoaderDisTorch2MultiGPU, CLIPLoaderDisTorch2MultiGPU, DualCLIPLoaderDisTorch2MultiGPU, TripleCLIPLoaderDisTorch2MultiGPU, QuadrupleCLIPLoaderDisTorch2MultiGPU, CLIPVisionLoaderDisTorch2MultiGPU, CheckpointLoaderSimpleDisTorch2MultiGPU, ControlNetLoaderDisTorch2MultiGPU, DiffusersLoaderDisTorch2MultiGPU, DiffControlNetLoaderDisTorch2MultiGPU, Florence2ModelLoaderMultiGPU, DownloadAndLoadFlorence2ModelMultiGPU, UnetLoaderGGUFDisTorchMultiGPU, UnetLoaderGGUFAdvancedDisTorchMultiGPU, CLIPLoaderGGUFDisTorchMultiGPU, DualCLIPLoaderGGUFDisTorchMultiGPU, TripleCLIPLoaderGGUFDisTorchMultiGPU, QuadrupleCLIPLoaderGGUFDisTorchMultiGPU, UnetLoaderGGUFDisTorch2MultiGPU, UnetLoaderGGUFAdvancedDisTorch2MultiGPU, CLIPLoaderGGUFDisTorch2MultiGPU, DualCLIPLoaderGGUFDisTorch2MultiGPU, TripleCLIPLoaderGGUFDisTorch2MultiGPU, QuadrupleCLIPLoaderGGUFDisTorch2MultiGPU, UnetLoaderGGUFMultiGPU, UnetLoaderGGUFAdvancedMultiGPU, CLIPLoaderGGUFMultiGPU, DualCLIPLoaderGGUFMultiGPU, TripleCLIPLoaderGGUFMultiGPU, QuadrupleCLIPLoaderGGUFMultiGPU
2025-12-04T23:43:13.667088 - [36;20m[/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux] | INFO -> Using ckpts path: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts[0m
2025-12-04T23:43:13.667284 - [36;20m[/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux] | INFO -> Using symlinks: False[0m
2025-12-04T23:43:13.667458 - [36;20m[/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux] | INFO -> Using ort providers: ['CUDAExecutionProvider', 'DirectMLExecutionProvider', 'OpenVINOExecutionProvider', 'ROCMExecutionProvider', 'CPUExecutionProvider', 'CoreMLExecutionProvider'][0m
2025-12-04T23:43:14.156403 - [34mWAS Node Suite: [0mOpenCV Python FFMPEG support is enabled[0m2025-12-04T23:43:14.156492 - 
2025-12-04T23:43:14.156648 - [34mWAS Node Suite [93mWarning: [0m`ffmpeg_bin_path` is not set in `/home/zeuss194/COMFY/ComfyUI/custom_nodes/was-ns/was_suite_config.json` config file. Will attempt to use system ffmpeg binaries if available.[0m2025-12-04T23:43:14.156704 - 
2025-12-04T23:43:14.482627 - [34mWAS Node Suite: [0mFinished.[0m [32mLoaded[0m [0m220[0m [32mnodes successfully.[0m2025-12-04T23:43:14.482711 - 
2025-12-04T23:43:14.482815 - 
	[3m[93m"Art is not a thing; it is a way."[0m[3m - Elbert Hubbard[0m
2025-12-04T23:43:14.482888 - 
2025-12-04T23:43:14.913553 - [34m[ComfyUI-Easy-Use] server: [0mv1.3.4 [92mLoaded[0m2025-12-04T23:43:14.913595 - 
2025-12-04T23:43:14.913612 - [34m[ComfyUI-Easy-Use] web root: [0m/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Easy-Use/web_version/v2 [92mLoaded[0m2025-12-04T23:43:14.913625 - 
2025-12-04T23:43:14.916837 - Traceback (most recent call last):
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 2149, in load_custom_node
    module_spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "<frozen importlib._bootstrap_external>", line 1023, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI_MIGraphX/__init__.py", line 1, in <module>
    from .migraphx_compile_sd3 import CompileDiffusersMIGraphX
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI_MIGraphX/migraphx_compile_sd3.py", line 4, in <module>
    from .migraphx_utils import load_MGX_transformer_model
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI_MIGraphX/migraphx_utils.py", line 8, in <module>
    import migraphx as mgx
ModuleNotFoundError: No module named 'migraphx'

2025-12-04T23:43:14.917075 - Cannot import /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI_MIGraphX module for custom nodes: No module named 'migraphx'
2025-12-04T23:43:14.917994 - ComfyUI-GGUF: Allowing full torch compile
2025-12-04T23:43:14.921497 - [92mEclipse: [0mVersion: 1.0.61[0m2025-12-04T23:43:14.921524 - 
2025-12-04T23:43:14.922655 - ComfyUI-GGUF: Allowing full torch compile
2025-12-04T23:43:14.923283 - [92mEclipse: [0m[GGUF Wrapper] ✓ GGUF components imported successfully[0m2025-12-04T23:43:14.923307 - 
2025-12-04T23:43:14.923335 - [92mEclipse: [0m[GGUF Wrapper] Module loaded. GGUF available: True[0m2025-12-04T23:43:14.923349 - 
2025-12-04T23:43:14.923934 - [92mEclipse [93mWarning: [0m[Nunchaku Wrapper] Nunchaku package not available: No module named 'nunchaku'[0m2025-12-04T23:43:14.923957 - 
2025-12-04T23:43:15.053435 - /home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/timm/models/layers/__init__.py:48: FutureWarning: Importing from timm.models.layers is deprecated, please import via timm.layers
  warnings.warn(f"Importing from {__name__} is deprecated, please import via timm.layers", FutureWarning)
2025-12-04T23:43:15.057323 - [92mEclipse: [0m[Florence-2 Wrapper] ✓ Custom Florence-2 classes imported successfully[0m2025-12-04T23:43:15.057352 - 
2025-12-04T23:43:15.059584 - [92mEclipse: [0m[SmartLM] Loaded 9 QwenVL prompts, 15 Florence-2 tasks[0m2025-12-04T23:43:15.059609 - 
2025-12-04T23:43:15.059709 - [92mEclipse: [0m[SmartLM] Loaded LLM few-shot training examples[0m2025-12-04T23:43:15.059725 - 
2025-12-04T23:43:15.061229 - [92mEclipse: [0m[SmartLM] Found 36 model templates[0m2025-12-04T23:43:15.061251 - 
2025-12-04T23:43:15.061283 - [92mEclipse: [0m[SmartLM] Transformers version: 4.57.1[0m2025-12-04T23:43:15.061298 - 
2025-12-04T23:43:15.078281 - [92mEclipse: [0m[SmartLM] llama-cpp-python version: 0.3.16[0m2025-12-04T23:43:15.078314 - 
2025-12-04T23:43:15.103795 - [92mEclipse: [0m[Wildcard] Loading wildcards from: /home/zeuss194/COMFY/ComfyUI/models/wildcards[0m2025-12-04T23:43:15.103827 - 
2025-12-04T23:43:15.109475 - [92mEclipse: [0m[Wildcard] Loaded 107 wildcard groups[0m2025-12-04T23:43:15.109504 - 
2025-12-04T23:43:15.109551 - [92mEclipse: [0m[Wildcard] Registered server endpoints[0m2025-12-04T23:43:15.109575 - 
2025-12-04T23:43:15.109596 - [92mEclipse: [0m[Wildcard] Server endpoints and prompt handler initialized successfully[0m2025-12-04T23:43:15.109609 - 
2025-12-04T23:43:15.213875 - [34m[ComfyUI-RMBG][0m v[93m2.9.4[0m | [93m33 nodes[0m [92mLoaded[0m2025-12-04T23:43:15.213911 - 
2025-12-04T23:43:15.215378 - ### Loading: ComfyUI-Impact-Subpack (V1.3.5)
2025-12-04T23:43:15.216238 - [Impact Pack/Subpack] Using folder_paths to determine whitelist path: /home/zeuss194/COMFY/ComfyUI/user/default/ComfyUI-Impact-Subpack/model-whitelist.txt
2025-12-04T23:43:15.216323 - [Impact Pack/Subpack] Ensured whitelist directory exists: /home/zeuss194/COMFY/ComfyUI/user/default/ComfyUI-Impact-Subpack
2025-12-04T23:43:15.216404 - [Impact Pack/Subpack] Loaded 0 model(s) from whitelist: /home/zeuss194/COMFY/ComfyUI/user/default/ComfyUI-Impact-Subpack/model-whitelist.txt
2025-12-04T23:43:15.255254 - [Impact Subpack] ultralytics_bbox: /home/zeuss194/COMFY/ComfyUI/models/ultralytics/bbox
2025-12-04T23:43:15.255354 - [Impact Subpack] ultralytics_segm: /home/zeuss194/COMFY/ComfyUI/models/ultralytics/segm
2025-12-04T23:43:15.286713 - 
----------------------------------------------------------------------2025-12-04T23:43:15.286745 - 
2025-12-04T23:43:15.286761 - [ComfyUI-Manager] NOTICE: Legacy backup exists2025-12-04T23:43:15.286774 - 
2025-12-04T23:43:15.286788 -   - Your old Manager data was backed up to:2025-12-04T23:43:15.286800 - 
2025-12-04T23:43:15.286813 -       /home/zeuss194/COMFY/ComfyUI/user/__manager/.legacy-manager-backup2025-12-04T23:43:15.286826 - 
2025-12-04T23:43:15.286839 -   - Please verify and remove it when no longer needed.2025-12-04T23:43:15.286851 - 
2025-12-04T23:43:15.286863 - ----------------------------------------------------------------------
2025-12-04T23:43:15.286875 - 
2025-12-04T23:43:15.287080 - ### Loading: ComfyUI-Manager (V3.38.1)
2025-12-04T23:43:15.287512 - [ComfyUI-Manager] network_mode: public
2025-12-04T23:43:15.336147 - ### ComfyUI Version: v0.3.76-24-g3c845622 | Released on '2025-12-04'
2025-12-04T23:43:15.379808 - 
[36mEfficiency Nodes:[0m Attempting to add Control Net options to the 'HiRes-Fix Script' Node (comfyui_controlnet_aux add-on)...[92mSuccess![0m2025-12-04T23:43:15.379844 - 
2025-12-04T23:43:15.385502 - 
Import times for custom nodes:
2025-12-04T23:43:15.385720 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/websocket_image_save.py
2025-12-04T23:43:15.385799 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Lotus
2025-12-04T23:43:15.385847 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-lora-auto-trigger-words
2025-12-04T23:43:15.385891 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-tcd-sampler
2025-12-04T23:43:15.385936 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-lama-remover
2025-12-04T23:43:15.385981 -    0.0 seconds (IMPORT FAILED): /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI_MIGraphX
2025-12-04T23:43:15.386036 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/cg-use-everywhere
2025-12-04T23:43:15.386086 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/amdgpumonitor
2025-12-04T23:43:15.386134 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-inpaint-cropandstitch
2025-12-04T23:43:15.386182 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-inpaint-nodes
2025-12-04T23:43:15.386229 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF
2025-12-04T23:43:15.386272 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-custom-scripts
2025-12-04T23:43:15.386314 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/eacloudnodes
2025-12-04T23:43:15.386356 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-MultiGPU
2025-12-04T23:43:15.386396 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/rgthree-comfy
2025-12-04T23:43:15.386439 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-jakeupgrade
2025-12-04T23:43:15.386490 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux
2025-12-04T23:43:15.386531 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_ipadapter_plus
2025-12-04T23:43:15.386579 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/efficiency-nodes-comfyui
2025-12-04T23:43:15.386624 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-impact-subpack
2025-12-04T23:43:15.386664 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes
2025-12-04T23:43:15.386704 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-manager
2025-12-04T23:43:15.386744 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-rmbg
2025-12-04T23:43:15.386783 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Crystools
2025-12-04T23:43:15.386828 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-impact-pack
2025-12-04T23:43:15.386868 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-ollama
2025-12-04T23:43:15.386908 -    0.2 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI_Eclipse
2025-12-04T23:43:15.386947 -    0.2 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-florence2
2025-12-04T23:43:15.386987 -    0.4 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Easy-Use
2025-12-04T23:43:15.387027 -    0.8 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/was-ns
2025-12-04T23:43:15.387067 -    2.2 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-MiniMax-Remover
2025-12-04T23:43:15.387107 - 
2025-12-04T23:43:15.526519 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/model-list.json
2025-12-04T23:43:15.528047 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/alter-list.json
2025-12-04T23:43:15.579603 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/github-stats.json
2025-12-04T23:43:15.659011 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json
2025-12-04T23:43:15.741002 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/extension-node-map.json
2025-12-04T23:43:15.755271 - Context impl SQLiteImpl.
2025-12-04T23:43:15.755372 - Will assume non-transactional DDL.
2025-12-04T23:43:15.756128 - No target revision found.
2025-12-04T23:43:15.791237 - Starting server

2025-12-04T23:43:15.791513 - To see the GUI go to: http://127.0.0.1:8188
2025-12-04T23:43:18.774926 - FETCH ComfyRegistry Data: 5/1102025-12-04T23:43:18.774969 - 
2025-12-04T23:43:22.065523 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-04T23:43:22.102815 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/clipspace.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-04T23:43:22.104725 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/buttonGroup.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-04T23:43:22.109466 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/widgetInputs.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-04T23:43:22.178765 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/groupNode.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-04T23:43:22.296939 - FETCH ComfyRegistry Data: 10/1102025-12-04T23:43:22.309461 - 
2025-12-04T23:43:24.357134 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/button.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-04T23:43:25.794628 - FETCH ComfyRegistry Data: 15/1102025-12-04T23:43:25.794665 - 
2025-12-04T23:43:29.268033 - FETCH ComfyRegistry Data: 20/1102025-12-04T23:43:29.268077 - 
2025-12-04T23:43:32.786385 - FETCH ComfyRegistry Data: 25/1102025-12-04T23:43:32.786454 - 
2025-12-04T23:43:36.324238 - FETCH ComfyRegistry Data: 30/1102025-12-04T23:43:36.324284 - 
2025-12-04T23:43:39.811853 - FETCH ComfyRegistry Data: 35/1102025-12-04T23:43:39.811894 - 
2025-12-04T23:43:43.677686 - FETCH ComfyRegistry Data: 40/1102025-12-04T23:43:43.677727 - 
2025-12-04T23:43:47.159253 - FETCH ComfyRegistry Data: 45/1102025-12-04T23:43:47.159288 - 
2025-12-04T23:43:50.658209 - FETCH ComfyRegistry Data: 50/1102025-12-04T23:43:50.658296 - 
2025-12-04T23:43:54.158474 - FETCH ComfyRegistry Data: 55/1102025-12-04T23:43:54.158513 - 
2025-12-04T23:43:57.661130 - FETCH ComfyRegistry Data: 60/1102025-12-04T23:43:57.661178 - 
2025-12-04T23:44:01.145582 - FETCH ComfyRegistry Data: 65/1102025-12-04T23:44:01.145640 - 
2025-12-04T23:44:04.717306 - FETCH ComfyRegistry Data: 70/1102025-12-04T23:44:04.717363 - 
2025-12-04T23:44:08.245924 - FETCH ComfyRegistry Data: 75/1102025-12-04T23:44:08.245974 - 
2025-12-04T23:44:11.785822 - FETCH ComfyRegistry Data: 80/1102025-12-04T23:44:11.785859 - 
2025-12-04T23:44:15.342950 - FETCH ComfyRegistry Data: 85/1102025-12-04T23:44:15.343001 - 
2025-12-04T23:44:18.864385 - FETCH ComfyRegistry Data: 90/1102025-12-04T23:44:18.864423 - 
2025-12-04T23:44:22.386377 - FETCH ComfyRegistry Data: 95/1102025-12-04T23:44:22.386417 - 
2025-12-04T23:44:25.883610 - FETCH ComfyRegistry Data: 100/1102025-12-04T23:44:25.883653 - 
2025-12-04T23:44:29.416927 - FETCH ComfyRegistry Data: 105/1102025-12-04T23:44:29.416978 - 
2025-12-04T23:44:33.258603 - FETCH ComfyRegistry Data: 110/1102025-12-04T23:44:33.258682 - 
2025-12-04T23:44:33.759016 - FETCH ComfyRegistry Data [DONE]2025-12-04T23:44:33.759120 - 
2025-12-04T23:44:33.886504 - [ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
2025-12-04T23:44:33.912708 - FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json2025-12-04T23:44:33.912747 - 2025-12-04T23:44:34.041768 -  [DONE]2025-12-04T23:44:34.041828 - 
2025-12-04T23:44:34.089582 - [ComfyUI-Manager] All startup tasks have been completed.
2025-12-04T23:47:28.129740 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-04T23:50:51.219278 - got prompt
2025-12-04T23:50:51.264318 - model weight dtype torch.bfloat16, manual cast: None
2025-12-04T23:50:51.264869 - model_type FLOW
2025-12-04T23:50:53.855705 - Using split attention in VAE
2025-12-04T23:50:53.856767 - Using split attention in VAE
2025-12-04T23:50:54.120507 - VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
2025-12-04T23:50:54.121952 - [MultiGPU Core Patching] text_encoder_device_patched returning device: cuda:0 (current_text_encoder_device=cuda:0)
2025-12-04T23:50:54.434369 - Requested to load LuminaTEModel_
2025-12-04T23:50:54.847547 - loaded completely; 95367431640625005117571072.00 MB usable, 4986.46 MB loaded, full load: True
2025-12-04T23:50:54.975150 - CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cuda:0, dtype: torch.float16
2025-12-04T23:51:00.429155 - Requested to load Lumina2
2025-12-04T23:51:01.949179 - loaded completely; 25851.34 MB usable, 4977.74 MB loaded, full load: True
2025-12-04T23:51:27.257570 - 
 90%|█████████████████████████████████████▊    | 27/30 [00:25<00:02,  1.11it/s]2025-12-04T23:51:27.564100 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-04T23:51:29.988391 - 
100%|██████████████████████████████████████████| 30/30 [00:27<00:00,  1.10it/s]2025-12-04T23:51:29.988647 - 
100%|██████████████████████████████████████████| 30/30 [00:27<00:00,  1.07it/s]2025-12-04T23:51:29.988672 - 
2025-12-04T23:51:29.989548 - Requested to load AutoencodingEngine
2025-12-04T23:51:30.032870 - loaded completely; 8795.91 MB usable, 159.87 MB loaded, full load: True
2025-12-04T23:51:32.382763 - Prompt executed in 41.16 seconds
2025-12-04T23:52:49.917612 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-04T23:53:23.124755 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-04T23:53:55.494875 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-04T23:54:42.255635 - got prompt
2025-12-04T23:55:11.113465 - 
100%|██████████████████████████████████████████| 30/30 [00:27<00:00,  1.09it/s]2025-12-04T23:55:11.113750 - 
100%|██████████████████████████████████████████| 30/30 [00:27<00:00,  1.10it/s]2025-12-04T23:55:11.113789 - 
2025-12-04T23:55:12.962738 - Prompt executed in 30.70 seconds
2025-12-04T23:57:01.419997 - got prompt
2025-12-04T23:57:30.362470 - 
100%|██████████████████████████████████████████| 30/30 [00:27<00:00,  1.09it/s]2025-12-04T23:57:30.362709 - 
100%|██████████████████████████████████████████| 30/30 [00:27<00:00,  1.10it/s]2025-12-04T23:57:30.362732 - 
2025-12-04T23:57:32.117629 - Prompt executed in 30.69 seconds
2025-12-05T00:02:17.139691 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-05T00:02:30.746038 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-05T00:03:52.870989 - got prompt
2025-12-05T00:04:20.722095 - 
100%|██████████████████████████████████████████| 30/30 [00:26<00:00,  1.10it/s]2025-12-05T00:04:20.722289 - 
100%|██████████████████████████████████████████| 30/30 [00:26<00:00,  1.11it/s]2025-12-05T00:04:20.722318 - 
2025-12-05T00:04:22.429421 - Prompt executed in 29.56 seconds
2025-12-05T00:04:31.042022 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-05T00:04:46.502490 - HTTP Request: GET http://127.0.0.1:11434/api/tags "HTTP/1.1 200 OK"
2025-12-05T00:08:25.603179 - got prompt
2025-12-05T00:08:37.922229 - HTTP Request: POST http://127.0.0.1:11434/api/generate "HTTP/1.1 200 OK"
2025-12-05T00:08:37.923273 - Prompt executed in 12.32 seconds
2025-12-05T00:09:59.520261 - got prompt
2025-12-05T00:10:04.568945 - HTTP Request: POST http://127.0.0.1:11434/api/generate "HTTP/1.1 200 OK"
2025-12-05T00:10:04.570240 - Prompt executed in 5.05 seconds
2025-12-05T00:11:57.175907 - got prompt
2025-12-05T00:12:11.075943 - HTTP Request: POST http://127.0.0.1:11434/api/generate "HTTP/1.1 200 OK"
2025-12-05T00:12:11.076997 - Prompt executed in 13.90 seconds
2025-12-05T00:13:13.638066 - got prompt
2025-12-05T00:13:13.687168 - model weight dtype torch.bfloat16, manual cast: None
2025-12-05T00:13:13.687502 - model_type FLOW
2025-12-05T00:13:16.212092 - Using split attention in VAE
2025-12-05T00:13:16.213302 - Using split attention in VAE
2025-12-05T00:13:16.400293 - VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
2025-12-05T00:13:16.401872 - [MultiGPU Core Patching] text_encoder_device_patched returning device: cuda:0 (current_text_encoder_device=cuda:0)
2025-12-05T00:13:16.689225 - Requested to load LuminaTEModel_
2025-12-05T00:13:16.700958 - loaded completely; 95367431640625005117571072.00 MB usable, 4986.46 MB loaded, full load: True
2025-12-05T00:13:16.703343 - CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cuda:0, dtype: torch.float16
2025-12-05T00:13:20.046260 - Requested to load Lumina2
2025-12-05T00:13:21.433125 - loaded completely; 25679.34 MB usable, 4977.74 MB loaded, full load: True
2025-12-05T00:13:47.814901 - 
100%|██████████████████████████████████████████| 30/30 [00:26<00:00,  1.13it/s]2025-12-05T00:13:47.815125 - 
100%|██████████████████████████████████████████| 30/30 [00:26<00:00,  1.14it/s]2025-12-05T00:13:47.815153 - 
2025-12-05T00:13:47.816123 - Requested to load AutoencodingEngine
2025-12-05T00:13:47.853524 - loaded completely; 8770.71 MB usable, 159.87 MB loaded, full load: True
2025-12-05T00:13:49.593847 - Prompt executed in 35.95 seconds
2025-12-05T00:14:16.940779 - got prompt
2025-12-05T00:14:34.199483 - 
 63%|██████████████████████████▌               | 19/30 [00:16<00:09,  1.11it/s]2025-12-05T00:14:34.567014 - /home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py:246: UserWarning: HIP warning: an illegal memory access was encountered (Triggered internally at /pytorch/aten/src/ATen/hip/impl/HIPGuardImplMasqueradingAsCUDA.h:83.)
  if sigmas[i + 1] == 0:
2025-12-05T00:14:34.567328 - 
 63%|██████████████████████████▌               | 19/30 [00:17<00:10,  1.10it/s]2025-12-05T00:14:34.567365 - 
2025-12-05T00:14:34.574847 - !!! Exception during processing !!! HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

2025-12-05T00:14:34.579477 - Traceback (most recent call last):
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 515, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 329, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 303, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 291, in process_inputs
    result = f(**inputs)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1538, in sample
    return common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 131, in KSampler_sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1163, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 149, in sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1053, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1035, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 997, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 114, in KSAMPLER_sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 212, in sample_euler_ancestral
    return sample_euler_ancestral_RF(model, x, sigmas, extra_args, callback, disable, eta, s_noise, noise_sampler)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 246, in sample_euler_ancestral_RF
    if sigmas[i + 1] == 0:
       ^^^^^^^^^^^^^^^^^^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


2025-12-05T00:14:34.583952 - Prompt executed in 17.64 seconds
2025-12-05T00:14:35.027900 - Exception in thread 2025-12-05T00:14:35.027961 - Thread-5 (prompt_worker)
```
## Attached Workflow

```

## Additional Context
(Please add any additional context or steps to reproduce the error here)
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU: 
model name	: Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz
GPU:
  Name:                    Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz
  Marketing Name:          Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz
  Name:                    gfx1201                            
  Marketing Name:          AMD Radeon AI PRO R9700            
      Name:                    amdgcn-amd-amdhsa--gfx1201         
      Name:                    amdgcn-amd-amdhsa--gfx12-generic 

### Operating System

NAME="Ubuntu" VERSION="24.04.3 LTS (Noble Numbat)"

### CPU

CPU:  model name	: Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz

### GPU

GPU:   Name:                    Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz   Marketing Name:          Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz   Name:                    gfx1201                               Marketing Name:          AMD Radeon AI PRO R9700                   Name:                    amdgcn-amd-amdhsa--gfx1201                Name:                    amdgcn-amd-amdhsa--gfx12-generic 

### ROCm Version

7.1.1

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz
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
  Max Clock Freq. (MHz):   4500                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65419284(0x3e63814) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65419284(0x3e63814) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65419284(0x3e63814) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65419284(0x3e63814) KB             
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
  Uuid:                    GPU-5c5383ed20b3fc7d               
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
  BDFID:                   26368                              
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

## 评论 (9 条)

### 评论 #1 — zichguan-amd (2025-12-15T21:28:01Z)

Hi @FR-Mister-T, can you provide the workflows/steps to reproduce the error and does the issue happen with any other models/workflows?

---

### 评论 #2 — FR-Mister-T (2025-12-20T22:01:53Z)

Hello,

This also happen once every 4 or 5 gen with wan2.2 first / lastimage workflow available in comfyui template area , the only modification i've done is that I'm using comfyui_multigpu node for loading "gguf" models instead of the fp8 models.

video_wan2_2_14B_flf2v

Traceback (most recent call last):
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 516, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 330, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 304, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 292, in process_inputs
    result = f(**inputs)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1572, in sample
    return common_ksampler(model, noise_seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise, disable_noise=disable_noise, start_step=start_at_step, last_step=end_at_step, force_full_denoise=force_full_denoise)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 131, in KSampler_sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1163, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 149, in sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1053, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1035, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 997, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 114, in KSAMPLER_sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 199, in sample_euler
    denoised = model(x, sigma_hat * s_in, **extra_args)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 401, in __call__
    out = self.inner_model(x, sigma, model_options=model_options, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 953, in __call__
    return self.outer_predict_noise(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 960, in outer_predict_noise
    ).execute(x, timestep, model_options, seed)
      ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 963, in predict_noise
    return sampling_function(self.inner_model, x, timestep, self.conds.get("negative", None), self.conds.get("positive", None), self.cfg, model_options=model_options, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 189, in sampling_function
    out = orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 381, in sampling_function
    out = calc_cond_batch(model, conds, x, timestep, model_options)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 206, in calc_cond_batch
    return _calc_cond_batch_outer(model, conds, x_in, timestep, model_options)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 214, in _calc_cond_batch_outer
    return executor.execute(model, conds, x_in, timestep, model_options)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 326, in _calc_cond_batch
    output = model.apply_model(input_x, timestep_, **c).chunk(batch_chunks)
             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_base.py", line 162, in apply_model
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ...<2 lines>...
        comfy.patcher_extension.get_all_wrappers(comfy.patcher_extension.WrappersMP.APPLY_MODEL, transformer_options)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ).execute(x, t, c_concat, c_crossattn, control, transformer_options, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_base.py", line 204, in _apply_model
    model_output = self.diffusion_model(xc, t, context=context, control=control, transformer_options=transformer_options, **extra_conds)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 630, in forward
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ...<2 lines>...
        comfy.patcher_extension.get_all_wrappers(comfy.patcher_extension.WrappersMP.DIFFUSION_MODEL, transformer_options)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ).execute(x, timestep, context, clip_fea, time_dim_concat, transformer_options, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 650, in _forward
    return self.forward_orig(x, timestep, context, clip_fea=clip_fea, freqs=freqs, transformer_options=transformer_options, **kwargs)[:, :, :t, :h, :w]
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 583, in forward_orig
    x = block(x, e=e0, freqs=freqs, context=context, context_img_len=context_img_len, transformer_options=transformer_options)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 245, in forward
    y = self.ffn(torch.addcmul(repeat_e(e[3], x), self.norm2(x), 1 + repeat_e(e[4], x)))
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/container.py", line 253, in forward
    input = module(input)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ops.py", line 164, in forward
    return self.forward_comfy_cast_weights(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 215, in forward_comfy_cast_weights
    out = self.forward_ggml_cast_weights(input, *args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 243, in forward_ggml_cast_weights
    weight, bias = self.cast_bias_weight(input)
                   ~~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 209, in cast_bias_weight
    weight = s.get_weight(s.weight.to(device), dtype)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 186, in get_weight
    weight = comfy.lora.calculate_weight(patch_list, weight, key)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/lora.py", line 391, in calculate_weight
    output = v.calculate_weight(weight, key, strength, strength_model, offset, function, intermediate_dtype, original_weights)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/weight_adapter/lora.py", line 162, in calculate_weight
    mat1 = comfy.model_management.cast_to_device(
        v[0], weight.device, intermediate_dtype
    )
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py", line 1113, in cast_to_device
    return cast_to(tensor, dtype=dtype, device=device, non_blocking=non_blocking, copy=copy)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py", line 1108, in cast_to
    r.copy_(weight, non_blocking=non_blocking)
    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.



---

### 评论 #3 — FR-Mister-T (2025-12-21T04:02:48Z)


# ComfyUI Error Report
## Error Details
- **Node ID:** 87
- **Node Type:** KSamplerAdvanced
- **Exception Type:** torch.AcceleratorError
- **Exception Message:** HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


## Stack Trace
```
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 516, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 330, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 304, in _async_map_node_over_list
    await process_inputs(input_dict, i)

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 292, in process_inputs
    result = f(**inputs)

  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1572, in sample
    return common_ksampler(model, noise_seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise, disable_noise=disable_noise, start_step=start_at_step, last_step=end_at_step, force_full_denoise=force_full_denoise)

  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 131, in KSampler_sample
    return orig_fn(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1178, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 149, in sample
    return orig_fn(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1068, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1050, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 994, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 114, in KSAMPLER_sample
    return orig_fn(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 199, in sample_euler
    denoised = model(x, sigma_hat * s_in, **extra_args)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 401, in __call__
    out = self.inner_model(x, sigma, model_options=model_options, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 953, in __call__
    return self.outer_predict_noise(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 960, in outer_predict_noise
    ).execute(x, timestep, model_options, seed)
      ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 963, in predict_noise
    return sampling_function(self.inner_model, x, timestep, self.conds.get("negative", None), self.conds.get("positive", None), self.cfg, model_options=model_options, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 189, in sampling_function
    out = orig_fn(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 381, in sampling_function
    out = calc_cond_batch(model, conds, x, timestep, model_options)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 206, in calc_cond_batch
    return _calc_cond_batch_outer(model, conds, x_in, timestep, model_options)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 214, in _calc_cond_batch_outer
    return executor.execute(model, conds, x_in, timestep, model_options)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 326, in _calc_cond_batch
    output = model.apply_model(input_x, timestep_, **c).chunk(batch_chunks)
             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_base.py", line 162, in apply_model
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ...<2 lines>...
        comfy.patcher_extension.get_all_wrappers(comfy.patcher_extension.WrappersMP.APPLY_MODEL, transformer_options)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ).execute(x, t, c_concat, c_crossattn, control, transformer_options, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_base.py", line 204, in _apply_model
    model_output = self.diffusion_model(xc, t, context=context, control=control, transformer_options=transformer_options, **extra_conds)

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 630, in forward
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ...<2 lines>...
        comfy.patcher_extension.get_all_wrappers(comfy.patcher_extension.WrappersMP.DIFFUSION_MODEL, transformer_options)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ).execute(x, timestep, context, clip_fea, time_dim_concat, transformer_options, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 650, in _forward
    return self.forward_orig(x, timestep, context, clip_fea=clip_fea, freqs=freqs, transformer_options=transformer_options, **kwargs)[:, :, :t, :h, :w]
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 583, in forward_orig
    x = block(x, e=e0, freqs=freqs, context=context, context_img_len=context_img_len, transformer_options=transformer_options)

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 244, in forward
    x = x + self.cross_attn(self.norm3(x), context, context_img_len=context_img_len, transformer_options=transformer_options)
            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 103, in forward
    k = self.norm_k(self.k(context))
                    ~~~~~~^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/ops.py", line 164, in forward
    return self.forward_comfy_cast_weights(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 215, in forward_comfy_cast_weights
    out = self.forward_ggml_cast_weights(input, *args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 243, in forward_ggml_cast_weights
    weight, bias = self.cast_bias_weight(input)
                   ~~~~~~~~~~~~~~~~~~~~~^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 209, in cast_bias_weight
    weight = s.get_weight(s.weight.to(device), dtype)

  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 186, in get_weight
    weight = comfy.lora.calculate_weight(patch_list, weight, key)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/lora.py", line 391, in calculate_weight
    output = v.calculate_weight(weight, key, strength, strength_model, offset, function, intermediate_dtype, original_weights)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/weight_adapter/lora.py", line 165, in calculate_weight
    mat2 = comfy.model_management.cast_to_device(
        v[1], weight.device, intermediate_dtype
    )

  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py", line 1113, in cast_to_device
    return cast_to(tensor, dtype=dtype, device=device, non_blocking=non_blocking, copy=copy)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py", line 1108, in cast_to
    r.copy_(weight, non_blocking=non_blocking)
    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```
## System Information
- **ComfyUI Version:** 0.5.1
- **Arguments:** main.py
- **OS:** linux
- **Python Version:** 3.13.11 (main, Dec  6 2025, 08:52:52) [GCC 13.3.0]
- **Embedded Python:** false
- **PyTorch Version:** 2.11.0.dev20251219+rocm7.1
## Devices

- **Name:** cuda:0 AMD Radeon AI PRO R9700 : native
  - **Type:** cuda
  - **VRAM Total:** 34208743424
  - **VRAM Free:** 34131148800
  - **Torch VRAM Total:** 0
  - **Torch VRAM Free:** 0

## Logs
```
2025-12-21T05:01:17.416014 - lora key not loaded: diffusion_model.blocks.10.cross_attn.v_img.diff_b
2025-12-21T05:01:17.416039 - lora key not loaded: diffusion_model.blocks.10.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.416064 - lora key not loaded: diffusion_model.blocks.10.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.416091 - lora key not loaded: diffusion_model.blocks.11.cross_attn.k_img.diff_b
2025-12-21T05:01:17.416115 - lora key not loaded: diffusion_model.blocks.11.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.416141 - lora key not loaded: diffusion_model.blocks.11.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.416171 - lora key not loaded: diffusion_model.blocks.11.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.416198 - lora key not loaded: diffusion_model.blocks.11.cross_attn.v_img.diff_b
2025-12-21T05:01:17.416223 - lora key not loaded: diffusion_model.blocks.11.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.416248 - lora key not loaded: diffusion_model.blocks.11.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.416276 - lora key not loaded: diffusion_model.blocks.12.cross_attn.k_img.diff_b
2025-12-21T05:01:17.416300 - lora key not loaded: diffusion_model.blocks.12.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.416325 - lora key not loaded: diffusion_model.blocks.12.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.416349 - lora key not loaded: diffusion_model.blocks.12.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.416374 - lora key not loaded: diffusion_model.blocks.12.cross_attn.v_img.diff_b
2025-12-21T05:01:17.416399 - lora key not loaded: diffusion_model.blocks.12.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.416423 - lora key not loaded: diffusion_model.blocks.12.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.416449 - lora key not loaded: diffusion_model.blocks.13.cross_attn.k_img.diff_b
2025-12-21T05:01:17.416474 - lora key not loaded: diffusion_model.blocks.13.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.416498 - lora key not loaded: diffusion_model.blocks.13.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.416523 - lora key not loaded: diffusion_model.blocks.13.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.416547 - lora key not loaded: diffusion_model.blocks.13.cross_attn.v_img.diff_b
2025-12-21T05:01:17.416572 - lora key not loaded: diffusion_model.blocks.13.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.416596 - lora key not loaded: diffusion_model.blocks.13.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.416622 - lora key not loaded: diffusion_model.blocks.14.cross_attn.k_img.diff_b
2025-12-21T05:01:17.416646 - lora key not loaded: diffusion_model.blocks.14.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.416670 - lora key not loaded: diffusion_model.blocks.14.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.416694 - lora key not loaded: diffusion_model.blocks.14.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.416720 - lora key not loaded: diffusion_model.blocks.14.cross_attn.v_img.diff_b
2025-12-21T05:01:17.416744 - lora key not loaded: diffusion_model.blocks.14.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.416768 - lora key not loaded: diffusion_model.blocks.14.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.416794 - lora key not loaded: diffusion_model.blocks.15.cross_attn.k_img.diff_b
2025-12-21T05:01:17.416823 - lora key not loaded: diffusion_model.blocks.15.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.416848 - lora key not loaded: diffusion_model.blocks.15.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.416872 - lora key not loaded: diffusion_model.blocks.15.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.416897 - lora key not loaded: diffusion_model.blocks.15.cross_attn.v_img.diff_b
2025-12-21T05:01:17.416924 - lora key not loaded: diffusion_model.blocks.15.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.416948 - lora key not loaded: diffusion_model.blocks.15.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.416974 - lora key not loaded: diffusion_model.blocks.16.cross_attn.k_img.diff_b
2025-12-21T05:01:17.416998 - lora key not loaded: diffusion_model.blocks.16.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.417023 - lora key not loaded: diffusion_model.blocks.16.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.417047 - lora key not loaded: diffusion_model.blocks.16.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.417072 - lora key not loaded: diffusion_model.blocks.16.cross_attn.v_img.diff_b
2025-12-21T05:01:17.417096 - lora key not loaded: diffusion_model.blocks.16.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.417121 - lora key not loaded: diffusion_model.blocks.16.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.417147 - lora key not loaded: diffusion_model.blocks.17.cross_attn.k_img.diff_b
2025-12-21T05:01:17.417176 - lora key not loaded: diffusion_model.blocks.17.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.417203 - lora key not loaded: diffusion_model.blocks.17.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.417228 - lora key not loaded: diffusion_model.blocks.17.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.417253 - lora key not loaded: diffusion_model.blocks.17.cross_attn.v_img.diff_b
2025-12-21T05:01:17.417277 - lora key not loaded: diffusion_model.blocks.17.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.417302 - lora key not loaded: diffusion_model.blocks.17.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.417329 - lora key not loaded: diffusion_model.blocks.18.cross_attn.k_img.diff_b
2025-12-21T05:01:17.417353 - lora key not loaded: diffusion_model.blocks.18.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.417378 - lora key not loaded: diffusion_model.blocks.18.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.417403 - lora key not loaded: diffusion_model.blocks.18.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.417429 - lora key not loaded: diffusion_model.blocks.18.cross_attn.v_img.diff_b
2025-12-21T05:01:17.417453 - lora key not loaded: diffusion_model.blocks.18.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.417478 - lora key not loaded: diffusion_model.blocks.18.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.417505 - lora key not loaded: diffusion_model.blocks.19.cross_attn.k_img.diff_b
2025-12-21T05:01:17.417530 - lora key not loaded: diffusion_model.blocks.19.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.417555 - lora key not loaded: diffusion_model.blocks.19.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.417579 - lora key not loaded: diffusion_model.blocks.19.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.417605 - lora key not loaded: diffusion_model.blocks.19.cross_attn.v_img.diff_b
2025-12-21T05:01:17.417630 - lora key not loaded: diffusion_model.blocks.19.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.417655 - lora key not loaded: diffusion_model.blocks.19.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.417682 - lora key not loaded: diffusion_model.blocks.2.cross_attn.k_img.diff_b
2025-12-21T05:01:17.417706 - lora key not loaded: diffusion_model.blocks.2.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.417731 - lora key not loaded: diffusion_model.blocks.2.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.417756 - lora key not loaded: diffusion_model.blocks.2.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.417781 - lora key not loaded: diffusion_model.blocks.2.cross_attn.v_img.diff_b
2025-12-21T05:01:17.417806 - lora key not loaded: diffusion_model.blocks.2.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.417834 - lora key not loaded: diffusion_model.blocks.2.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.417861 - lora key not loaded: diffusion_model.blocks.20.cross_attn.k_img.diff_b
2025-12-21T05:01:17.417885 - lora key not loaded: diffusion_model.blocks.20.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.417910 - lora key not loaded: diffusion_model.blocks.20.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.417935 - lora key not loaded: diffusion_model.blocks.20.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.417960 - lora key not loaded: diffusion_model.blocks.20.cross_attn.v_img.diff_b
2025-12-21T05:01:17.417985 - lora key not loaded: diffusion_model.blocks.20.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.418010 - lora key not loaded: diffusion_model.blocks.20.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.418036 - lora key not loaded: diffusion_model.blocks.21.cross_attn.k_img.diff_b
2025-12-21T05:01:17.418061 - lora key not loaded: diffusion_model.blocks.21.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.418085 - lora key not loaded: diffusion_model.blocks.21.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.418110 - lora key not loaded: diffusion_model.blocks.21.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.418135 - lora key not loaded: diffusion_model.blocks.21.cross_attn.v_img.diff_b
2025-12-21T05:01:17.418160 - lora key not loaded: diffusion_model.blocks.21.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.418191 - lora key not loaded: diffusion_model.blocks.21.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.418218 - lora key not loaded: diffusion_model.blocks.22.cross_attn.k_img.diff_b
2025-12-21T05:01:17.418242 - lora key not loaded: diffusion_model.blocks.22.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.418267 - lora key not loaded: diffusion_model.blocks.22.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.418292 - lora key not loaded: diffusion_model.blocks.22.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.418317 - lora key not loaded: diffusion_model.blocks.22.cross_attn.v_img.diff_b
2025-12-21T05:01:17.418342 - lora key not loaded: diffusion_model.blocks.22.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.418367 - lora key not loaded: diffusion_model.blocks.22.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.418394 - lora key not loaded: diffusion_model.blocks.23.cross_attn.k_img.diff_b
2025-12-21T05:01:17.418418 - lora key not loaded: diffusion_model.blocks.23.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.418444 - lora key not loaded: diffusion_model.blocks.23.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.418468 - lora key not loaded: diffusion_model.blocks.23.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.418493 - lora key not loaded: diffusion_model.blocks.23.cross_attn.v_img.diff_b
2025-12-21T05:01:17.418517 - lora key not loaded: diffusion_model.blocks.23.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.418541 - lora key not loaded: diffusion_model.blocks.23.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.418568 - lora key not loaded: diffusion_model.blocks.24.cross_attn.k_img.diff_b
2025-12-21T05:01:17.418594 - lora key not loaded: diffusion_model.blocks.24.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.418618 - lora key not loaded: diffusion_model.blocks.24.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.418643 - lora key not loaded: diffusion_model.blocks.24.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.418669 - lora key not loaded: diffusion_model.blocks.24.cross_attn.v_img.diff_b
2025-12-21T05:01:17.418694 - lora key not loaded: diffusion_model.blocks.24.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.418718 - lora key not loaded: diffusion_model.blocks.24.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.418745 - lora key not loaded: diffusion_model.blocks.25.cross_attn.k_img.diff_b
2025-12-21T05:01:17.418769 - lora key not loaded: diffusion_model.blocks.25.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.418794 - lora key not loaded: diffusion_model.blocks.25.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.418819 - lora key not loaded: diffusion_model.blocks.25.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.418848 - lora key not loaded: diffusion_model.blocks.25.cross_attn.v_img.diff_b
2025-12-21T05:01:17.418874 - lora key not loaded: diffusion_model.blocks.25.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.418899 - lora key not loaded: diffusion_model.blocks.25.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.418927 - lora key not loaded: diffusion_model.blocks.26.cross_attn.k_img.diff_b
2025-12-21T05:01:17.418951 - lora key not loaded: diffusion_model.blocks.26.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.418976 - lora key not loaded: diffusion_model.blocks.26.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.419001 - lora key not loaded: diffusion_model.blocks.26.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.419026 - lora key not loaded: diffusion_model.blocks.26.cross_attn.v_img.diff_b
2025-12-21T05:01:17.419051 - lora key not loaded: diffusion_model.blocks.26.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.419075 - lora key not loaded: diffusion_model.blocks.26.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.419101 - lora key not loaded: diffusion_model.blocks.27.cross_attn.k_img.diff_b
2025-12-21T05:01:17.419126 - lora key not loaded: diffusion_model.blocks.27.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.419151 - lora key not loaded: diffusion_model.blocks.27.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.419181 - lora key not loaded: diffusion_model.blocks.27.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.419207 - lora key not loaded: diffusion_model.blocks.27.cross_attn.v_img.diff_b
2025-12-21T05:01:17.419232 - lora key not loaded: diffusion_model.blocks.27.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.419256 - lora key not loaded: diffusion_model.blocks.27.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.419283 - lora key not loaded: diffusion_model.blocks.28.cross_attn.k_img.diff_b
2025-12-21T05:01:17.419307 - lora key not loaded: diffusion_model.blocks.28.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.419331 - lora key not loaded: diffusion_model.blocks.28.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.419356 - lora key not loaded: diffusion_model.blocks.28.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.419381 - lora key not loaded: diffusion_model.blocks.28.cross_attn.v_img.diff_b
2025-12-21T05:01:17.419405 - lora key not loaded: diffusion_model.blocks.28.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.419429 - lora key not loaded: diffusion_model.blocks.28.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.419455 - lora key not loaded: diffusion_model.blocks.29.cross_attn.k_img.diff_b
2025-12-21T05:01:17.419479 - lora key not loaded: diffusion_model.blocks.29.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.419503 - lora key not loaded: diffusion_model.blocks.29.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.419526 - lora key not loaded: diffusion_model.blocks.29.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.419551 - lora key not loaded: diffusion_model.blocks.29.cross_attn.v_img.diff_b
2025-12-21T05:01:17.419575 - lora key not loaded: diffusion_model.blocks.29.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.419598 - lora key not loaded: diffusion_model.blocks.29.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.419624 - lora key not loaded: diffusion_model.blocks.3.cross_attn.k_img.diff_b
2025-12-21T05:01:17.419648 - lora key not loaded: diffusion_model.blocks.3.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.419672 - lora key not loaded: diffusion_model.blocks.3.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.419696 - lora key not loaded: diffusion_model.blocks.3.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.419721 - lora key not loaded: diffusion_model.blocks.3.cross_attn.v_img.diff_b
2025-12-21T05:01:17.419745 - lora key not loaded: diffusion_model.blocks.3.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.419770 - lora key not loaded: diffusion_model.blocks.3.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.419796 - lora key not loaded: diffusion_model.blocks.30.cross_attn.k_img.diff_b
2025-12-21T05:01:17.419821 - lora key not loaded: diffusion_model.blocks.30.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.419850 - lora key not loaded: diffusion_model.blocks.30.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.419875 - lora key not loaded: diffusion_model.blocks.30.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.419901 - lora key not loaded: diffusion_model.blocks.30.cross_attn.v_img.diff_b
2025-12-21T05:01:17.419925 - lora key not loaded: diffusion_model.blocks.30.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.419950 - lora key not loaded: diffusion_model.blocks.30.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.419977 - lora key not loaded: diffusion_model.blocks.31.cross_attn.k_img.diff_b
2025-12-21T05:01:17.420002 - lora key not loaded: diffusion_model.blocks.31.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.420027 - lora key not loaded: diffusion_model.blocks.31.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.420051 - lora key not loaded: diffusion_model.blocks.31.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.420076 - lora key not loaded: diffusion_model.blocks.31.cross_attn.v_img.diff_b
2025-12-21T05:01:17.420100 - lora key not loaded: diffusion_model.blocks.31.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.420125 - lora key not loaded: diffusion_model.blocks.31.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.420152 - lora key not loaded: diffusion_model.blocks.32.cross_attn.k_img.diff_b
2025-12-21T05:01:17.420183 - lora key not loaded: diffusion_model.blocks.32.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.420207 - lora key not loaded: diffusion_model.blocks.32.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.420232 - lora key not loaded: diffusion_model.blocks.32.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.420258 - lora key not loaded: diffusion_model.blocks.32.cross_attn.v_img.diff_b
2025-12-21T05:01:17.420283 - lora key not loaded: diffusion_model.blocks.32.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.420308 - lora key not loaded: diffusion_model.blocks.32.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.420334 - lora key not loaded: diffusion_model.blocks.33.cross_attn.k_img.diff_b
2025-12-21T05:01:17.420358 - lora key not loaded: diffusion_model.blocks.33.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.420382 - lora key not loaded: diffusion_model.blocks.33.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.420407 - lora key not loaded: diffusion_model.blocks.33.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.420432 - lora key not loaded: diffusion_model.blocks.33.cross_attn.v_img.diff_b
2025-12-21T05:01:17.420457 - lora key not loaded: diffusion_model.blocks.33.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.420482 - lora key not loaded: diffusion_model.blocks.33.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.420508 - lora key not loaded: diffusion_model.blocks.34.cross_attn.k_img.diff_b
2025-12-21T05:01:17.420533 - lora key not loaded: diffusion_model.blocks.34.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.420559 - lora key not loaded: diffusion_model.blocks.34.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.420584 - lora key not loaded: diffusion_model.blocks.34.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.420609 - lora key not loaded: diffusion_model.blocks.34.cross_attn.v_img.diff_b
2025-12-21T05:01:17.420634 - lora key not loaded: diffusion_model.blocks.34.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.420658 - lora key not loaded: diffusion_model.blocks.34.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.420684 - lora key not loaded: diffusion_model.blocks.35.cross_attn.k_img.diff_b
2025-12-21T05:01:17.420709 - lora key not loaded: diffusion_model.blocks.35.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.420733 - lora key not loaded: diffusion_model.blocks.35.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.420758 - lora key not loaded: diffusion_model.blocks.35.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.420784 - lora key not loaded: diffusion_model.blocks.35.cross_attn.v_img.diff_b
2025-12-21T05:01:17.420808 - lora key not loaded: diffusion_model.blocks.35.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.420833 - lora key not loaded: diffusion_model.blocks.35.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.420863 - lora key not loaded: diffusion_model.blocks.36.cross_attn.k_img.diff_b
2025-12-21T05:01:17.420888 - lora key not loaded: diffusion_model.blocks.36.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.420913 - lora key not loaded: diffusion_model.blocks.36.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.420937 - lora key not loaded: diffusion_model.blocks.36.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.420962 - lora key not loaded: diffusion_model.blocks.36.cross_attn.v_img.diff_b
2025-12-21T05:01:17.420987 - lora key not loaded: diffusion_model.blocks.36.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.421011 - lora key not loaded: diffusion_model.blocks.36.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.421037 - lora key not loaded: diffusion_model.blocks.37.cross_attn.k_img.diff_b
2025-12-21T05:01:17.421062 - lora key not loaded: diffusion_model.blocks.37.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.421086 - lora key not loaded: diffusion_model.blocks.37.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.421110 - lora key not loaded: diffusion_model.blocks.37.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.421135 - lora key not loaded: diffusion_model.blocks.37.cross_attn.v_img.diff_b
2025-12-21T05:01:17.421160 - lora key not loaded: diffusion_model.blocks.37.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.421191 - lora key not loaded: diffusion_model.blocks.37.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.421218 - lora key not loaded: diffusion_model.blocks.38.cross_attn.k_img.diff_b
2025-12-21T05:01:17.421243 - lora key not loaded: diffusion_model.blocks.38.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.421267 - lora key not loaded: diffusion_model.blocks.38.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.421291 - lora key not loaded: diffusion_model.blocks.38.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.421316 - lora key not loaded: diffusion_model.blocks.38.cross_attn.v_img.diff_b
2025-12-21T05:01:17.421341 - lora key not loaded: diffusion_model.blocks.38.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.421365 - lora key not loaded: diffusion_model.blocks.38.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.421391 - lora key not loaded: diffusion_model.blocks.39.cross_attn.k_img.diff_b
2025-12-21T05:01:17.421415 - lora key not loaded: diffusion_model.blocks.39.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.421439 - lora key not loaded: diffusion_model.blocks.39.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.421463 - lora key not loaded: diffusion_model.blocks.39.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.421488 - lora key not loaded: diffusion_model.blocks.39.cross_attn.v_img.diff_b
2025-12-21T05:01:17.421512 - lora key not loaded: diffusion_model.blocks.39.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.421537 - lora key not loaded: diffusion_model.blocks.39.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.421564 - lora key not loaded: diffusion_model.blocks.4.cross_attn.k_img.diff_b
2025-12-21T05:01:17.421588 - lora key not loaded: diffusion_model.blocks.4.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.421613 - lora key not loaded: diffusion_model.blocks.4.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.421638 - lora key not loaded: diffusion_model.blocks.4.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.421664 - lora key not loaded: diffusion_model.blocks.4.cross_attn.v_img.diff_b
2025-12-21T05:01:17.421689 - lora key not loaded: diffusion_model.blocks.4.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.421713 - lora key not loaded: diffusion_model.blocks.4.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.421740 - lora key not loaded: diffusion_model.blocks.5.cross_attn.k_img.diff_b
2025-12-21T05:01:17.421765 - lora key not loaded: diffusion_model.blocks.5.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.421790 - lora key not loaded: diffusion_model.blocks.5.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.421815 - lora key not loaded: diffusion_model.blocks.5.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.421841 - lora key not loaded: diffusion_model.blocks.5.cross_attn.v_img.diff_b
2025-12-21T05:01:17.421869 - lora key not loaded: diffusion_model.blocks.5.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.421894 - lora key not loaded: diffusion_model.blocks.5.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.421921 - lora key not loaded: diffusion_model.blocks.6.cross_attn.k_img.diff_b
2025-12-21T05:01:17.421946 - lora key not loaded: diffusion_model.blocks.6.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.421970 - lora key not loaded: diffusion_model.blocks.6.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.421994 - lora key not loaded: diffusion_model.blocks.6.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.422019 - lora key not loaded: diffusion_model.blocks.6.cross_attn.v_img.diff_b
2025-12-21T05:01:17.422043 - lora key not loaded: diffusion_model.blocks.6.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.422067 - lora key not loaded: diffusion_model.blocks.6.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.422093 - lora key not loaded: diffusion_model.blocks.7.cross_attn.k_img.diff_b
2025-12-21T05:01:17.422117 - lora key not loaded: diffusion_model.blocks.7.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.422142 - lora key not loaded: diffusion_model.blocks.7.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.422171 - lora key not loaded: diffusion_model.blocks.7.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.422198 - lora key not loaded: diffusion_model.blocks.7.cross_attn.v_img.diff_b
2025-12-21T05:01:17.422222 - lora key not loaded: diffusion_model.blocks.7.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.422246 - lora key not loaded: diffusion_model.blocks.7.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.422272 - lora key not loaded: diffusion_model.blocks.8.cross_attn.k_img.diff_b
2025-12-21T05:01:17.422296 - lora key not loaded: diffusion_model.blocks.8.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.422320 - lora key not loaded: diffusion_model.blocks.8.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.422344 - lora key not loaded: diffusion_model.blocks.8.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.422369 - lora key not loaded: diffusion_model.blocks.8.cross_attn.v_img.diff_b
2025-12-21T05:01:17.422393 - lora key not loaded: diffusion_model.blocks.8.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.422417 - lora key not loaded: diffusion_model.blocks.8.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.422442 - lora key not loaded: diffusion_model.blocks.9.cross_attn.k_img.diff_b
2025-12-21T05:01:17.422466 - lora key not loaded: diffusion_model.blocks.9.cross_attn.k_img.lora_down.weight
2025-12-21T05:01:17.422490 - lora key not loaded: diffusion_model.blocks.9.cross_attn.k_img.lora_up.weight
2025-12-21T05:01:17.422514 - lora key not loaded: diffusion_model.blocks.9.cross_attn.norm_k_img.diff
2025-12-21T05:01:17.422539 - lora key not loaded: diffusion_model.blocks.9.cross_attn.v_img.diff_b
2025-12-21T05:01:17.422563 - lora key not loaded: diffusion_model.blocks.9.cross_attn.v_img.lora_down.weight
2025-12-21T05:01:17.422587 - lora key not loaded: diffusion_model.blocks.9.cross_attn.v_img.lora_up.weight
2025-12-21T05:01:17.422612 - lora key not loaded: diffusion_model.img_emb.proj.0.diff
2025-12-21T05:01:17.422636 - lora key not loaded: diffusion_model.img_emb.proj.0.diff_b
2025-12-21T05:01:17.422661 - lora key not loaded: diffusion_model.img_emb.proj.1.diff_b
2025-12-21T05:01:17.422685 - lora key not loaded: diffusion_model.img_emb.proj.1.lora_down.weight
2025-12-21T05:01:17.422709 - lora key not loaded: diffusion_model.img_emb.proj.1.lora_up.weight
2025-12-21T05:01:17.422734 - lora key not loaded: diffusion_model.img_emb.proj.3.diff_b
2025-12-21T05:01:17.422758 - lora key not loaded: diffusion_model.img_emb.proj.3.lora_down.weight
2025-12-21T05:01:17.422783 - lora key not loaded: diffusion_model.img_emb.proj.3.lora_up.weight
2025-12-21T05:01:17.422807 - lora key not loaded: diffusion_model.img_emb.proj.4.diff
2025-12-21T05:01:17.422831 - lora key not loaded: diffusion_model.img_emb.proj.4.diff_b
2025-12-21T05:01:17.451863 - Requested to load WAN21
2025-12-21T05:01:40.735186 - loaded completely; 23030.70 MB usable, 14825.47 MB loaded, full load: True
2025-12-21T05:01:40.787279 - 
  0%|                                                     | 0/2 [00:00<?, ?it/s]2025-12-21T05:01:44.383888 - /home/zeuss194/COMFY/ComfyUI/comfy/model_management.py:1108: UserWarning: HIP warning: an illegal memory access was encountered (Triggered internally at /pytorch/aten/src/ATen/hip/impl/HIPGuardImplMasqueradingAsCUDA.h:83.)
  r.copy_(weight, non_blocking=non_blocking)
2025-12-21T05:01:44.384971 - 
  0%|                                                     | 0/2 [00:03<?, ?it/s]2025-12-21T05:01:44.385018 - 
2025-12-21T05:01:44.445149 - !!! Exception during processing !!! HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

2025-12-21T05:01:44.460241 - Traceback (most recent call last):
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 516, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 330, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 304, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 292, in process_inputs
    result = f(**inputs)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1572, in sample
    return common_ksampler(model, noise_seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise, disable_noise=disable_noise, start_step=start_at_step, last_step=end_at_step, force_full_denoise=force_full_denoise)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 131, in KSampler_sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1178, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 149, in sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1068, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1050, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 994, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 114, in KSAMPLER_sample
    return orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 199, in sample_euler
    denoised = model(x, sigma_hat * s_in, **extra_args)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 401, in __call__
    out = self.inner_model(x, sigma, model_options=model_options, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 953, in __call__
    return self.outer_predict_noise(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 960, in outer_predict_noise
    ).execute(x, timestep, model_options, seed)
      ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 963, in predict_noise
    return sampling_function(self.inner_model, x, timestep, self.conds.get("negative", None), self.conds.get("positive", None), self.cfg, model_options=model_options, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_smznodes/smZNodes.py", line 189, in sampling_function
    out = orig_fn(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 381, in sampling_function
    out = calc_cond_batch(model, conds, x, timestep, model_options)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 206, in calc_cond_batch
    return _calc_cond_batch_outer(model, conds, x_in, timestep, model_options)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 214, in _calc_cond_batch_outer
    return executor.execute(model, conds, x_in, timestep, model_options)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 326, in _calc_cond_batch
    output = model.apply_model(input_x, timestep_, **c).chunk(batch_chunks)
             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_base.py", line 162, in apply_model
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ...<2 lines>...
        comfy.patcher_extension.get_all_wrappers(comfy.patcher_extension.WrappersMP.APPLY_MODEL, transformer_options)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ).execute(x, t, c_concat, c_crossattn, control, transformer_options, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_base.py", line 204, in _apply_model
    model_output = self.diffusion_model(xc, t, context=context, control=control, transformer_options=transformer_options, **extra_conds)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 630, in forward
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ...<2 lines>...
        comfy.patcher_extension.get_all_wrappers(comfy.patcher_extension.WrappersMP.DIFFUSION_MODEL, transformer_options)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ).execute(x, timestep, context, clip_fea, time_dim_concat, transformer_options, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 650, in _forward
    return self.forward_orig(x, timestep, context, clip_fea=clip_fea, freqs=freqs, transformer_options=transformer_options, **kwargs)[:, :, :t, :h, :w]
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 583, in forward_orig
    x = block(x, e=e0, freqs=freqs, context=context, context_img_len=context_img_len, transformer_options=transformer_options)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 244, in forward
    x = x + self.cross_attn(self.norm3(x), context, context_img_len=context_img_len, transformer_options=transformer_options)
            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ldm/wan/model.py", line 103, in forward
    k = self.norm_k(self.k(context))
                    ~~~~~~^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1780, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/nn/modules/module.py", line 1791, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/ops.py", line 164, in forward
    return self.forward_comfy_cast_weights(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 215, in forward_comfy_cast_weights
    out = self.forward_ggml_cast_weights(input, *args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 243, in forward_ggml_cast_weights
    weight, bias = self.cast_bias_weight(input)
                   ~~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 209, in cast_bias_weight
    weight = s.get_weight(s.weight.to(device), dtype)
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF/ops.py", line 186, in get_weight
    weight = comfy.lora.calculate_weight(patch_list, weight, key)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/lora.py", line 391, in calculate_weight
    output = v.calculate_weight(weight, key, strength, strength_model, offset, function, intermediate_dtype, original_weights)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/weight_adapter/lora.py", line 165, in calculate_weight
    mat2 = comfy.model_management.cast_to_device(
        v[1], weight.device, intermediate_dtype
    )
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py", line 1113, in cast_to_device
    return cast_to(tensor, dtype=dtype, device=device, non_blocking=non_blocking, copy=copy)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py", line 1108, in cast_to
    r.copy_(weight, non_blocking=non_blocking)
    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


2025-12-21T05:01:44.469315 - Prompt executed in 151.78 seconds
2025-12-21T05:01:45.677513 - Exception in thread 2025-12-21T05:01:45.677741 - Thread-5 (prompt_worker)2025-12-21T05:01:45.677860 - :
2025-12-21T05:01:45.686898 - Traceback (most recent call last):
2025-12-21T05:01:45.686997 - 2025-12-21T05:01:45.689733 -   File [35m"/usr/lib/python3.13/threading.py"[0m, line [35m1044[0m, in [35m_bootstrap_inner[0m
    [31mself.run[0m[1;31m()[0m
    [31m~~~~~~~~[0m[1;31m^^[0m
2025-12-21T05:01:45.689813 - 2025-12-21T05:01:45.689882 -   File [35m"/usr/lib/python3.13/threading.py"[0m, line [35m995[0m, in [35mrun[0m
    [31mself._target[0m[1;31m(*self._args, **self._kwargs)[0m
    [31m~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
2025-12-21T05:01:45.689936 - 2025-12-21T05:01:45.690003 -   File [35m"/home/zeuss194/COMFY/ComfyUI/main.py"[0m, line [35m270[0m, in [35mprompt_worker[0m
    [31mcomfy.model_management.soft_empty_cache[0m[1;31m()[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^[0m
2025-12-21T05:01:45.690054 - 2025-12-21T05:01:45.690121 -   File [35m"/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-MultiGPU/device_utils.py"[0m, line [35m258[0m, in [35msoft_empty_cache_distorch2_patched[0m
    [31moriginal_soft_empty_cache[0m[1;31m(force)[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^[0m
2025-12-21T05:01:45.690171 - 2025-12-21T05:01:45.690216 -   File [35m"/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py"[0m, line [35m1523[0m, in [35msoft_empty_cache[0m
    [31mtorch.cuda.empty_cache[0m[1;31m()[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^[0m
2025-12-21T05:01:45.690255 - 2025-12-21T05:01:45.690299 -   File [35m"/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/cuda/memory.py"[0m, line [35m280[0m, in [35mempty_cache[0m
    [31mtorch._C._cuda_emptyCache[0m[1;31m()[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^[0m
2025-12-21T05:01:45.690349 - 2025-12-21T05:01:45.690429 - [1;35mtorch.AcceleratorError[0m: [35mHIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
[0m
2025-12-21T05:01:45.690474 - 
```
## Attached Workflow
Please make sure that workflow does not contain any sensitive information such as API keys or passwords.
```
Workflow too large. Please manually upload the workflow from local file system.
```

## Additional Context
(Please add any additional context or steps to reproduce the error here)


---

### 评论 #4 — FR-Mister-T (2025-12-22T00:46:02Z)

**WF .json is avaialble at the bottom of this post**

Even on a simple SDXL worflow after about 12 gen, The same kind of issue arise.
I've try to install a different version of pytorch rocm based on official ROCm documentation (https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html)
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1.1/torch-2.9.1%2Brocm7.1.1.lw.git351ff442-cp313-cp313-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1.1/torchvision-0.24.0%2Brocm7.1.1.gitb919bd0c-cp313-cp313-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1.1/triton-3.5.1%2Brocm7.1.1.gita272dfa8-cp313-cp313-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1.1/torchaudio-2.9.0%2Brocm7.1.1.gite3c6ee2b-cp313-cp313-linux_x86_64.whl
pip3 uninstall torch torchvision triton torchaudio
pip3 install torch-2.9.1+rocm7.1.1.lw.git351ff442-cp313-cp313-linux_x86_64.whl torchvision-0.24.0+rocm7.1.1.gitb919bd0c-cp313-cp313-linux_x86_64.whl torchaudio-2.9.0+rocm7.1.1.gite3c6ee2b-cp313-cp313-linux_x86_64.whl triton-3.5.1+rocm7.1.1.gita272dfa8-cp313-cp313-linux_x86_64.whl


# ComfyUI Error Report
## Error Details
- **Node ID:** 37
- **Node Type:** KSampler
- **Exception Type:** torch.AcceleratorError
- **Exception Message:** HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


## Stack Trace
```
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 516, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 330, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 304, in _async_map_node_over_list
    await process_inputs(input_dict, i)

  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 292, in process_inputs
    result = f(**inputs)

  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1538, in sample
    return common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)

  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1178, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1068, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1050, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 994, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)

  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
    return func(*args, **kwargs)

  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 220, in sample_euler_ancestral
    sigma_down, sigma_up = get_ancestral_step(sigmas[i], sigmas[i + 1], eta=eta)
                           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 70, in get_ancestral_step
    sigma_up = min(sigma_to, eta * (sigma_to ** 2 * (sigma_from ** 2 - sigma_to ** 2) / sigma_from ** 2) ** 0.5)

```
## System Information
- **ComfyUI Version:** 0.5.1
- **Arguments:** main.py
- **OS:** linux
- **Python Version:** 3.13.11 (main, Dec  6 2025, 08:52:52) [GCC 13.3.0]
- **Embedded Python:** false
- **PyTorch Version:** 2.9.1+rocm7.1.1.git351ff442
## Devices

- **Name:** cuda:0 AMD Radeon AI PRO R9700 : native
  - **Type:** cuda
  - **VRAM Total:** 34208743424
  - **VRAM Free:** 34131148800
  - **Torch VRAM Total:** 0
  - **Torch VRAM Free:** 0

## Logs
```
2025-12-22T01:51:07.381129 - Checkpoint files will always be loaded safely.
2025-12-22T01:51:07.515436 - Total VRAM 32624 MB, total RAM 63886 MB
2025-12-22T01:51:07.515548 - pytorch version: 2.9.1+rocm7.1.1.git351ff442
2025-12-22T01:51:07.515811 - Set: torch.backends.cudnn.enabled = False for better AMD performance.
2025-12-22T01:51:07.515864 - AMD arch: gfx1201
2025-12-22T01:51:07.515905 - ROCm version: (7, 1)
2025-12-22T01:51:07.516050 - Set vram state to: NORMAL_VRAM
2025-12-22T01:51:07.516119 - Device: cuda:0 AMD Radeon AI PRO R9700 : native
2025-12-22T01:51:07.516339 - Enabled pinned memory 60691.0
2025-12-22T01:51:08.305956 - Using pytorch attention
2025-12-22T01:51:09.495815 - Python version: 3.13.11 (main, Dec  6 2025, 08:52:52) [GCC 13.3.0]
2025-12-22T01:51:09.495935 - ComfyUI version: 0.5.1
2025-12-22T01:51:09.498670 - ComfyUI frontend version: 1.34.9
2025-12-22T01:51:09.499231 - [Prompt Server] web root: /home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/comfyui_frontend_package/static
2025-12-22T01:51:09.855344 - Total VRAM 32624 MB, total RAM 63886 MB
2025-12-22T01:51:09.855459 - pytorch version: 2.9.1+rocm7.1.1.git351ff442
2025-12-22T01:51:09.855683 - Set: torch.backends.cudnn.enabled = False for better AMD performance.
2025-12-22T01:51:09.855742 - AMD arch: gfx1201
2025-12-22T01:51:09.855780 - ROCm version: (7, 1)
2025-12-22T01:51:09.855853 - Set vram state to: NORMAL_VRAM
2025-12-22T01:51:09.855917 - Device: cuda:0 AMD Radeon AI PRO R9700 : native
2025-12-22T01:51:09.856086 - Enabled pinned memory 60691.0
2025-12-22T01:51:10.529017 - ### Loading: ComfyUI-Impact-Pack (V8.28)
2025-12-22T01:51:10.652106 - [Impact Pack] Wildcard total size (0.00 MB) is within cache limit (50.00 MB). Using full cache mode.
2025-12-22T01:51:10.654169 - [Impact Pack] Wildcards loading done.
2025-12-22T01:51:14.398834 - [Crystools [0;32mINFO[0m] Crystools version: 1.27.4
2025-12-22T01:51:14.418156 - [Crystools [0;32mINFO[0m] Platform release: 6.14.0-37-generic
2025-12-22T01:51:14.418227 - [Crystools [0;32mINFO[0m] JETSON: Not detected.
2025-12-22T01:51:14.420362 - [Crystools [0;32mINFO[0m] CPU: Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz - Arch: x86_64 - OS: Linux 6.14.0-37-generic
2025-12-22T01:51:14.421864 - /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Crystools/general/gpu.py:67: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml
2025-12-22T01:51:14.427464 - [Crystools [0;31mERROR[0m] Could not init pynvml (NVIDIA). NVML Shared Library Not Found
2025-12-22T01:51:14.427628 - [Crystools [0;33mWARNING[0m] No GPU monitoring libraries available.
2025-12-22T01:51:14.434281 - [VibeVoice] Using embedded VibeVoice (MIT licensed)
2025-12-22T01:51:14.753227 - [VibeVoice] VibeVoice nodes registered successfully
2025-12-22T01:51:15.155217 - Warning: Could not load sageattention: No module named 'sageattention'
2025-12-22T01:51:15.155340 - sageattention package is not installed, sageattention will not be available
2025-12-22T01:51:15.270362 - 
2025-12-22T01:51:15.270463 - [92m[rgthree-comfy] Loaded 48 epic nodes. 🎉[0m2025-12-22T01:51:15.270495 - 
2025-12-22T01:51:15.270532 - 
2025-12-22T01:51:15.270567 - [33m[rgthree-comfy] ComfyUI's new Node 2.0 rendering may be incompatible with some rgthree-comfy nodes and features, breaking some rendering as well as losing the ability to access a node's properties (a vital part of many nodes). It also appears to run MUCH more slowly spiking CPU usage and causing jankiness and unresponsiveness, especially with large workflows. Personally I am not planning to use the new Nodes 2.0 and, unfortunately, am not able to invest the time to investigate and overhaul rgthree-comfy where needed. If you have issues when Nodes 2.0 is enabled, I'd urge you to switch it off as well and join me in hoping ComfyUI is not planning to deprecate the existing, stable canvas rendering all together.
[0m2025-12-22T01:51:15.270594 - 
2025-12-22T01:51:15.278195 - --------------------- Jake Upgrade Nodes ---------------------2025-12-22T01:51:15.278259 - 
2025-12-22T01:51:15.278467 - 🔶 Version 2.3.142025-12-22T01:51:15.278512 - 
2025-12-22T01:51:15.279009 - 🔶 Config file loaded successfully2025-12-22T01:51:15.279053 - 
2025-12-22T01:51:15.279113 - 🔶 Using standard version of RandomPrompter2025-12-22T01:51:15.279142 - 
2025-12-22T01:51:15.286909 - 🔶 All main modules loaded2025-12-22T01:51:15.286959 - 
2025-12-22T01:51:15.286992 - 🔶 No deprecated nodes loaded2025-12-22T01:51:15.287018 - 
2025-12-22T01:51:15.287464 - 🔶 Total nodes: 1042025-12-22T01:51:15.287508 - 
2025-12-22T01:51:15.287540 - --------------------------------------------------------------2025-12-22T01:51:15.287564 - 
2025-12-22T01:51:15.289604 - AMD GPU Monitor thread started2025-12-22T01:51:15.289656 - 
2025-12-22T01:51:15.289884 - Using AMD SMI tool: /opt/rocm/bin/rocm-smi2025-12-22T01:51:15.290058 - AMD GPU Monitor: Web directory set to /home/zeuss194/COMFY/ComfyUI/custom_nodes/amdgpumonitor/web2025-12-22T01:51:15.290119 - 
2025-12-22T01:51:15.290807 - 
2025-12-22T01:51:15.292591 - [MultiGPU Core Patching] Patching mm.soft_empty_cache for Comprehensive Memory Management (VRAM + CPU + Store Pruning)
2025-12-22T01:51:15.293552 - [MultiGPU Core Patching] Patching mm.get_torch_device, mm.text_encoder_device, mm.unet_offload_device
2025-12-22T01:51:15.293785 - [MultiGPU DEBUG] Initial current_device: cuda:0
2025-12-22T01:51:15.293961 - [MultiGPU DEBUG] Initial current_text_encoder_device: cuda:0
2025-12-22T01:51:15.294129 - [MultiGPU DEBUG] Initial current_unet_offload_device: cpu
2025-12-22T01:51:15.296420 - [MultiGPU] Initiating custom_node Registration. . .
2025-12-22T01:51:15.296623 - -----------------------------------------------
2025-12-22T01:51:15.296794 - custom_node                   Found     Nodes
2025-12-22T01:51:15.296955 - -----------------------------------------------
2025-12-22T01:51:15.297848 - ComfyUI-LTXVideo                  N         0
2025-12-22T01:51:15.298037 - ComfyUI-Florence2                 Y         2
2025-12-22T01:51:15.298206 - ComfyUI_bitsandbytes_NF4          N         0
2025-12-22T01:51:15.298372 - x-flux-comfyui                    N         0
2025-12-22T01:51:15.298549 - ComfyUI-MMAudio                   N         0
2025-12-22T01:51:15.298724 - ComfyUI-GGUF                      Y        18
2025-12-22T01:51:15.298889 - PuLID_ComfyUI                     N         0
2025-12-22T01:51:15.299052 - ComfyUI-WanVideoWrapper           Y        20
2025-12-22T01:51:15.299213 - -----------------------------------------------
2025-12-22T01:51:15.299429 - [MultiGPU] Registration complete. Final mappings: CheckpointLoaderAdvancedMultiGPU, CheckpointLoaderAdvancedDisTorch2MultiGPU, UNetLoaderLP, UNETLoaderMultiGPU, VAELoaderMultiGPU, CLIPLoaderMultiGPU, DualCLIPLoaderMultiGPU, TripleCLIPLoaderMultiGPU, QuadrupleCLIPLoaderMultiGPU, CLIPVisionLoaderMultiGPU, CheckpointLoaderSimpleMultiGPU, ControlNetLoaderMultiGPU, DiffusersLoaderMultiGPU, DiffControlNetLoaderMultiGPU, UNETLoaderDisTorch2MultiGPU, VAELoaderDisTorch2MultiGPU, CLIPLoaderDisTorch2MultiGPU, DualCLIPLoaderDisTorch2MultiGPU, TripleCLIPLoaderDisTorch2MultiGPU, QuadrupleCLIPLoaderDisTorch2MultiGPU, CLIPVisionLoaderDisTorch2MultiGPU, CheckpointLoaderSimpleDisTorch2MultiGPU, ControlNetLoaderDisTorch2MultiGPU, DiffusersLoaderDisTorch2MultiGPU, DiffControlNetLoaderDisTorch2MultiGPU, Florence2ModelLoaderMultiGPU, DownloadAndLoadFlorence2ModelMultiGPU, UnetLoaderGGUFDisTorchMultiGPU, UnetLoaderGGUFAdvancedDisTorchMultiGPU, CLIPLoaderGGUFDisTorchMultiGPU, DualCLIPLoaderGGUFDisTorchMultiGPU, TripleCLIPLoaderGGUFDisTorchMultiGPU, QuadrupleCLIPLoaderGGUFDisTorchMultiGPU, UnetLoaderGGUFDisTorch2MultiGPU, UnetLoaderGGUFAdvancedDisTorch2MultiGPU, CLIPLoaderGGUFDisTorch2MultiGPU, DualCLIPLoaderGGUFDisTorch2MultiGPU, TripleCLIPLoaderGGUFDisTorch2MultiGPU, QuadrupleCLIPLoaderGGUFDisTorch2MultiGPU, UnetLoaderGGUFMultiGPU, UnetLoaderGGUFAdvancedMultiGPU, CLIPLoaderGGUFMultiGPU, DualCLIPLoaderGGUFMultiGPU, TripleCLIPLoaderGGUFMultiGPU, QuadrupleCLIPLoaderGGUFMultiGPU, LoadWanVideoT5TextEncoderMultiGPU, WanVideoTextEncodeMultiGPU, WanVideoTextEncodeCachedMultiGPU, WanVideoTextEncodeSingleMultiGPU, WanVideoVAELoaderMultiGPU, WanVideoTinyVAELoaderMultiGPU, WanVideoBlockSwapMultiGPU, WanVideoImageToVideoEncodeMultiGPU, WanVideoDecodeMultiGPU, WanVideoModelLoaderMultiGPU, WanVideoSamplerMultiGPU, WanVideoVACEEncodeMultiGPU, WanVideoEncodeMultiGPU, LoadWanVideoClipTextEncoderMultiGPU, WanVideoClipVisionEncodeMultiGPU, WanVideoControlnetLoaderMultiGPU, FantasyTalkingModelLoaderMultiGPU, Wav2VecModelLoaderMultiGPU, WanVideoUni3C_ControlnetLoaderMultiGPU, DownloadAndLoadWav2VecModelMultiGPU
2025-12-22T01:51:15.302317 - [36;20m[/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux] | INFO -> Using ckpts path: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts[0m
2025-12-22T01:51:15.302657 - [36;20m[/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux] | INFO -> Using symlinks: False[0m
2025-12-22T01:51:15.302974 - [36;20m[/home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux] | INFO -> Using ort providers: ['CUDAExecutionProvider', 'DirectMLExecutionProvider', 'OpenVINOExecutionProvider', 'ROCMExecutionProvider', 'CPUExecutionProvider', 'CoreMLExecutionProvider'][0m
2025-12-22T01:51:15.322534 - Traceback (most recent call last):
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 2149, in load_custom_node
    module_spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "<frozen importlib._bootstrap_external>", line 1023, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/was-ns/__init__.py", line 1, in <module>
    from .WAS_Node_Suite import NODE_CLASS_MAPPINGS
  File "/home/zeuss194/COMFY/ComfyUI/custom_nodes/was-ns/WAS_Node_Suite.py", line 44, in <module>
    from numba import jit
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/numba/__init__.py", line 59, in <module>
    _ensure_critical_deps()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/numba/__init__.py", line 45, in _ensure_critical_deps
    raise ImportError(msg)
ImportError: Numba needs NumPy 2.3 or less. Got NumPy 2.4.

2025-12-22T01:51:15.322790 - Cannot import /home/zeuss194/COMFY/ComfyUI/custom_nodes/was-ns module for custom nodes: Numba needs NumPy 2.3 or less. Got NumPy 2.4.
2025-12-22T01:51:15.410520 - [34m[ComfyUI-Easy-Use] server: [0mv1.3.4 [92mLoaded[0m2025-12-22T01:51:15.410592 - 
2025-12-22T01:51:15.410624 - [34m[ComfyUI-Easy-Use] web root: [0m/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Easy-Use/web_version/v2 [92mLoaded[0m2025-12-22T01:51:15.410649 - 
2025-12-22T01:51:15.413410 - ComfyUI-GGUF: Allowing full torch compile
2025-12-22T01:51:15.416838 - [92mEclipse: [0mVersion: 1.0.63[0m2025-12-22T01:51:15.416895 - 
2025-12-22T01:51:15.417946 - ComfyUI-GGUF: Allowing full torch compile
2025-12-22T01:51:15.418543 - [92mEclipse: [0m[GGUF Wrapper] ✓ GGUF components imported successfully[0m2025-12-22T01:51:15.418589 - 
2025-12-22T01:51:15.418629 - [92mEclipse: [0m[GGUF Wrapper] Module loaded. GGUF available: True[0m2025-12-22T01:51:15.418655 - 
2025-12-22T01:51:15.419280 - [92mEclipse [93mWarning: [0m[Nunchaku Wrapper] Nunchaku package not available: No module named 'nunchaku'[0m2025-12-22T01:51:15.419322 - 
2025-12-22T01:51:15.424404 - /home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/timm/models/layers/__init__.py:48: FutureWarning: Importing from timm.models.layers is deprecated, please import via timm.layers
  warnings.warn(f"Importing from {__name__} is deprecated, please import via timm.layers", FutureWarning)
2025-12-22T01:51:15.428558 - [92mEclipse: [0m[Florence-2 Wrapper] ✓ Custom Florence-2 classes imported successfully[0m2025-12-22T01:51:15.428611 - 
2025-12-22T01:51:15.431215 - [92mEclipse: [0m[SmartLM] Loaded 9 QwenVL prompts, 15 Florence-2 tasks[0m2025-12-22T01:51:15.431301 - 
2025-12-22T01:51:15.431532 - [92mEclipse: [0m[SmartLM] Loaded LLM few-shot training examples[0m2025-12-22T01:51:15.431567 - 
2025-12-22T01:51:15.433072 - [92mEclipse: [0m[SmartLM] Found 36 model templates[0m2025-12-22T01:51:15.433115 - 
2025-12-22T01:51:15.433152 - [92mEclipse: [0m[SmartLM] Transformers version: 4.57.3[0m2025-12-22T01:51:15.433178 - 
2025-12-22T01:51:15.450537 - [92mEclipse: [0m[SmartLM] llama-cpp-python version: 0.3.16[0m2025-12-22T01:51:15.450605 - 
2025-12-22T01:51:15.475483 - [92mEclipse: [0m[Wildcard] Loading wildcards from: /home/zeuss194/COMFY/ComfyUI/models/wildcards[0m2025-12-22T01:51:15.475566 - 
2025-12-22T01:51:15.480924 - [92mEclipse: [0m[Wildcard] Loaded 107 wildcard groups[0m2025-12-22T01:51:15.480997 - 
2025-12-22T01:51:15.481055 - [92mEclipse: [0m[Wildcard] Registered server endpoints[0m2025-12-22T01:51:15.481086 - 
2025-12-22T01:51:15.481130 - [92mEclipse: [0m[Wildcard] Server endpoints and prompt handler initialized successfully[0m2025-12-22T01:51:15.481155 - 
2025-12-22T01:51:15.481183 - [92mEclipse: [0m[SmartLM] Server endpoints initialized successfully[0m2025-12-22T01:51:15.481206 - 
2025-12-22T01:51:15.562036 - [34m[ComfyUI-RMBG][0m v[93m2.9.6[0m | [93m33 nodes[0m [92mLoaded[0m2025-12-22T01:51:15.562105 - 
2025-12-22T01:51:15.563525 - ### Loading: ComfyUI-Impact-Subpack (V1.3.5)
2025-12-22T01:51:15.564367 - [Impact Pack/Subpack] Using folder_paths to determine whitelist path: /home/zeuss194/COMFY/ComfyUI/user/default/ComfyUI-Impact-Subpack/model-whitelist.txt
2025-12-22T01:51:15.564455 - [Impact Pack/Subpack] Ensured whitelist directory exists: /home/zeuss194/COMFY/ComfyUI/user/default/ComfyUI-Impact-Subpack
2025-12-22T01:51:15.564544 - [Impact Pack/Subpack] Loaded 0 model(s) from whitelist: /home/zeuss194/COMFY/ComfyUI/user/default/ComfyUI-Impact-Subpack/model-whitelist.txt
2025-12-22T01:51:15.601844 - [Impact Subpack] ultralytics_bbox: /home/zeuss194/COMFY/ComfyUI/models/ultralytics/bbox
2025-12-22T01:51:15.601945 - [Impact Subpack] ultralytics_segm: /home/zeuss194/COMFY/ComfyUI/models/ultralytics/segm
2025-12-22T01:51:15.610299 - ### Loading: ComfyUI-Manager (V3.39)
2025-12-22T01:51:15.610814 - [ComfyUI-Manager] network_mode: public
2025-12-22T01:51:15.610945 - [ComfyUI-Manager] ComfyUI per-queue preview override detected (PR #11261). Manager's preview method feature is disabled. Use ComfyUI's --preview-method CLI option or 'Settings > Execution > Live preview method'.
2025-12-22T01:51:15.660993 - ### ComfyUI Version: v0.5.1-22-g807538fe | Released on '2025-12-20'
2025-12-22T01:51:15.700729 - 
[36mEfficiency Nodes:[0m Attempting to add Control Net options to the 'HiRes-Fix Script' Node (comfyui_controlnet_aux add-on)...[92mSuccess![0m2025-12-22T01:51:15.700794 - 
2025-12-22T01:51:15.704186 - 
Import times for custom nodes:
2025-12-22T01:51:15.704283 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/websocket_image_save.py
2025-12-22T01:51:15.704325 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Lotus
2025-12-22T01:51:15.704361 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-tcd-sampler
2025-12-22T01:51:15.704400 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-lora-auto-trigger-words
2025-12-22T01:51:15.704430 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-lama-remover
2025-12-22T01:51:15.704460 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/cg-use-everywhere
2025-12-22T01:51:15.704487 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/eacloudnodes
2025-12-22T01:51:15.704522 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/amdgpumonitor
2025-12-22T01:51:15.704552 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-inpaint-cropandstitch
2025-12-22T01:51:15.704579 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-GGUF
2025-12-22T01:51:15.704606 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-inpaint-nodes
2025-12-22T01:51:15.704632 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-custom-scripts
2025-12-22T01:51:15.704658 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/openrouter_node
2025-12-22T01:51:15.704695 -    0.0 seconds (IMPORT FAILED): /home/zeuss194/COMFY/ComfyUI/custom_nodes/was-ns
2025-12-22T01:51:15.704727 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/rgthree-comfy
2025-12-22T01:51:15.704753 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-MultiGPU
2025-12-22T01:51:15.704784 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_ipadapter_plus
2025-12-22T01:51:15.704811 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui_controlnet_aux
2025-12-22T01:51:15.704838 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-jakeupgrade
2025-12-22T01:51:15.704864 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/efficiency-nodes-comfyui
2025-12-22T01:51:15.704891 -    0.0 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-impact-subpack
2025-12-22T01:51:15.704917 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-manager
2025-12-22T01:51:15.704943 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI_Eclipse
2025-12-22T01:51:15.705018 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-rmbg
2025-12-22T01:51:15.705048 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Easy-Use
2025-12-22T01:51:15.705075 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-Crystools
2025-12-22T01:51:15.705101 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-impact-pack
2025-12-22T01:51:15.705128 -    0.1 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-ollama
2025-12-22T01:51:15.705154 -    0.2 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/comfyui-florence2
2025-12-22T01:51:15.705183 -    0.3 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/VibeVoice-ComfyUI
2025-12-22T01:51:15.705267 -    0.5 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-WanVideoWrapper
2025-12-22T01:51:15.705294 -    3.3 seconds: /home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-MiniMax-Remover
2025-12-22T01:51:15.705321 - 
2025-12-22T01:51:15.735730 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/alter-list.json
2025-12-22T01:51:15.816023 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/model-list.json
2025-12-22T01:51:15.865055 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/github-stats.json
2025-12-22T01:51:15.955030 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/extension-node-map.json
2025-12-22T01:51:16.030726 - [ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json
2025-12-22T01:51:16.063711 - Context impl SQLiteImpl.
2025-12-22T01:51:16.063821 - Will assume non-transactional DDL.
2025-12-22T01:51:16.064577 - No target revision found.
2025-12-22T01:51:16.099101 - Starting server

2025-12-22T01:51:16.099377 - To see the GUI go to: http://127.0.0.1:8188
2025-12-22T01:51:19.056791 - FETCH ComfyRegistry Data: 5/1142025-12-22T01:51:19.056875 - 
2025-12-22T01:51:22.480743 - FETCH ComfyRegistry Data: 10/1142025-12-22T01:51:22.480826 - 
2025-12-22T01:51:25.900140 - FETCH ComfyRegistry Data: 15/1142025-12-22T01:51:25.900223 - 
2025-12-22T01:51:29.318004 - FETCH ComfyRegistry Data: 20/1142025-12-22T01:51:29.318165 - 
2025-12-22T01:51:32.774008 - FETCH ComfyRegistry Data: 25/1142025-12-22T01:51:32.774078 - 
2025-12-22T01:51:36.228008 - FETCH ComfyRegistry Data: 30/1142025-12-22T01:51:36.228130 - 
2025-12-22T01:51:39.687445 - FETCH ComfyRegistry Data: 35/1142025-12-22T01:51:39.687557 - 
2025-12-22T01:51:43.098242 - FETCH ComfyRegistry Data: 40/1142025-12-22T01:51:43.098408 - 
2025-12-22T01:51:46.531638 - FETCH ComfyRegistry Data: 45/1142025-12-22T01:51:46.531713 - 
2025-12-22T01:51:50.624182 - FETCH ComfyRegistry Data: 50/1142025-12-22T01:51:50.624255 - 
2025-12-22T01:51:54.062631 - FETCH ComfyRegistry Data: 55/1142025-12-22T01:51:54.062705 - 
2025-12-22T01:51:57.829030 - FETCH ComfyRegistry Data: 60/1142025-12-22T01:51:57.829585 - 
2025-12-22T01:51:58.017665 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-22T01:51:58.041638 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/clipspace.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-22T01:51:58.053983 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/buttonGroup.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-22T01:51:58.107680 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/groupNode.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-22T01:51:58.285616 - [VibeVoice] Found 4 VibeVoice model(s) available
2025-12-22T01:51:58.285843 - [VibeVoice] No LoRA adapters found in ComfyUI/models/vibevoice/loras
2025-12-22T01:52:00.083408 - [DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/button.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
2025-12-22T01:52:01.273487 - FETCH ComfyRegistry Data: 65/1142025-12-22T01:52:01.273663 - 
2025-12-22T01:52:05.103124 - FETCH ComfyRegistry Data: 70/1142025-12-22T01:52:05.103196 - 
2025-12-22T01:52:08.546485 - FETCH ComfyRegistry Data: 75/1142025-12-22T01:52:08.546578 - 
2025-12-22T01:52:11.999845 - FETCH ComfyRegistry Data: 80/1142025-12-22T01:52:11.999926 - 
2025-12-22T01:52:15.451463 - FETCH ComfyRegistry Data: 85/1142025-12-22T01:52:15.451601 - 
2025-12-22T01:52:16.456691 - got prompt
2025-12-22T01:52:16.621487 - model weight dtype torch.float16, manual cast: None
2025-12-22T01:52:16.622370 - model_type EPS
2025-12-22T01:52:18.904539 - FETCH ComfyRegistry Data: 90/1142025-12-22T01:52:18.904618 - 
2025-12-22T01:52:19.295577 - Using split attention in VAE
2025-12-22T01:52:19.297623 - Using split attention in VAE
2025-12-22T01:52:19.575614 - VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
2025-12-22T01:52:19.581762 - [MultiGPU Core Patching] text_encoder_device_patched returning device: cuda:0 (current_text_encoder_device=cuda:0)
2025-12-22T01:52:20.642069 - Requested to load SDXLClipModel
2025-12-22T01:52:20.671442 - loaded completely; 95367431640625005117571072.00 MB usable, 1560.80 MB loaded, full load: True
2025-12-22T01:52:20.675917 - CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cuda:0, dtype: torch.float16
2025-12-22T01:52:20.949966 - [1m[36m[EasyUse] Load LORA:[0m InstantSuccubus_V2_XL_ILL_fuka.safetensors: model=1.000, clip=1.000, LBW=None, A=None, B=None2025-12-22T01:52:20.950070 - 
2025-12-22T01:52:21.618086 - [1m[36m[EasyUse] Load LORA:[0m Breasts gravity slider IXLQ5_alpha16.0_rank32_full_last.safetensors: model=-1.000, clip=-1.000, LBW=None, A=None, B=None2025-12-22T01:52:21.618159 - 
2025-12-22T01:52:21.747916 - Requested to load SDXLClipModel
2025-12-22T01:52:22.489341 - FETCH ComfyRegistry Data: 95/1142025-12-22T01:52:22.489465 - 
2025-12-22T01:52:22.798890 - loaded completely; 31177.30 MB usable, 1560.80 MB loaded, full load: True
2025-12-22T01:52:23.318829 - warning, embedding:lazypos,fuka, masterpiece, best quality, amazing quality, detailed, newest, 1girl, solo, horns, mountainous_horizon,blue jacket,open jacket,taut_clothes,  hood up, looking at viewer, jeans, bangs, collared_shirt, blunt bangs, gloves, grey hair,modest smile, does not exist, ignoring
2025-12-22T01:52:23.320183 - warning, embedding:lazypos,fuka, masterpiece, best quality, amazing quality, detailed, newest, 1girl, solo, horns, mountainous_horizon,blue jacket,open jacket,taut_clothes,  hood up, looking at viewer, jeans, bangs, collared_shirt, blunt bangs, gloves, grey hair,modest smile, does not exist, ignoring
2025-12-22T01:52:23.397458 - Requested to load SDXL
2025-12-22T01:52:25.024266 - loaded completely; 29443.00 MB usable, 4897.05 MB loaded, full load: True
2025-12-22T01:52:25.302688 - 
  0%|                                                    | 0/20 [00:00<?, ?it/s]2025-12-22T01:52:25.937414 - FETCH ComfyRegistry Data: 100/1142025-12-22T01:52:25.937524 - 
2025-12-22T01:52:30.037097 - 
 90%|██████████████████████████████████████▋    | 18/20 [00:04<00:00,  4.56it/s]2025-12-22T01:52:30.256380 - FETCH ComfyRegistry Data: 105/1142025-12-22T01:52:30.256475 - 
2025-12-22T01:52:30.474634 - 
100%|███████████████████████████████████████████| 20/20 [00:05<00:00,  4.57it/s]2025-12-22T01:52:30.474870 - 
100%|███████████████████████████████████████████| 20/20 [00:05<00:00,  3.87it/s]2025-12-22T01:52:30.474911 - 
2025-12-22T01:52:30.475589 - Requested to load AutoencoderKL
2025-12-22T01:52:30.538800 - loaded completely; 13643.84 MB usable, 159.56 MB loaded, full load: True
2025-12-22T01:52:33.081864 - 0 models unloaded.
2025-12-22T01:52:33.895247 - Requested to load SDXL
2025-12-22T01:52:34.126873 - FETCH ComfyRegistry Data: 110/1142025-12-22T01:52:34.126948 - 
2025-12-22T01:52:35.140316 - loaded completely; 30390.55 MB usable, 4897.05 MB loaded, full load: True
2025-12-22T01:52:36.270032 - 
  5%|██▏                                         | 1/20 [00:01<00:21,  1.11s/it]2025-12-22T01:52:37.375299 - FETCH ComfyRegistry Data [DONE]2025-12-22T01:52:37.375485 - 
2025-12-22T01:52:37.392828 - 
 10%|████▍                                       | 2/20 [00:02<00:20,  1.12s/it]2025-12-22T01:52:37.534651 - [ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
2025-12-22T01:52:37.566204 - FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json2025-12-22T01:52:37.566294 - 2025-12-22T01:52:37.682050 -  [DONE]2025-12-22T01:52:37.682164 - 
2025-12-22T01:52:37.738964 - [ComfyUI-Manager] All startup tasks have been completed.
2025-12-22T01:52:41.863437 - 
 30%|█████████████▏                              | 6/20 [00:06<00:15,  1.12s/it]2025-12-22T01:52:42.356713 - /home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py:70: UserWarning: HIP warning: an illegal memory access was encountered (Triggered internally at /pytorch/aten/src/ATen/hip/impl/HIPGuardImplMasqueradingAsCUDA.h:83.)
  sigma_up = min(sigma_to, eta * (sigma_to ** 2 * (sigma_from ** 2 - sigma_to ** 2) / sigma_from ** 2) ** 0.5)
2025-12-22T01:52:42.357023 - 
 30%|█████████████▏                              | 6/20 [00:07<00:16,  1.20s/it]2025-12-22T01:52:42.357066 - 
2025-12-22T01:52:42.360455 - !!! Exception during processing !!! HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

2025-12-22T01:52:42.363251 - Traceback (most recent call last):
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 516, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 330, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 304, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/home/zeuss194/COMFY/ComfyUI/execution.py", line 292, in process_inputs
    result = f(**inputs)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1538, in sample
    return common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
  File "/home/zeuss194/COMFY/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1178, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1068, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 1050, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 994, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)
  File "/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
    return func(*args, **kwargs)
  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 220, in sample_euler_ancestral
    sigma_down, sigma_up = get_ancestral_step(sigmas[i], sigmas[i + 1], eta=eta)
                           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zeuss194/COMFY/ComfyUI/comfy/k_diffusion/sampling.py", line 70, in get_ancestral_step
    sigma_up = min(sigma_to, eta * (sigma_to ** 2 * (sigma_from ** 2 - sigma_to ** 2) / sigma_from ** 2) ** 0.5)
torch.AcceleratorError: HIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


2025-12-22T01:52:42.366046 - Prompt executed in 25.90 seconds
2025-12-22T01:52:42.870696 - Exception in thread 2025-12-22T01:52:42.870781 - Thread-5 (prompt_worker)2025-12-22T01:52:42.870815 - :
2025-12-22T01:52:42.872269 - Traceback (most recent call last):
2025-12-22T01:52:42.872329 - 2025-12-22T01:52:42.872856 -   File [35m"/usr/lib/python3.13/threading.py"[0m, line [35m1044[0m, in [35m_bootstrap_inner[0m
    [31mself.run[0m[1;31m()[0m
    [31m~~~~~~~~[0m[1;31m^^[0m
2025-12-22T01:52:42.872989 - 2025-12-22T01:52:42.873025 -   File [35m"/usr/lib/python3.13/threading.py"[0m, line [35m995[0m, in [35mrun[0m
    [31mself._target[0m[1;31m(*self._args, **self._kwargs)[0m
    [31m~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
2025-12-22T01:52:42.873097 - 2025-12-22T01:52:42.873130 -   File [35m"/home/zeuss194/COMFY/ComfyUI/main.py"[0m, line [35m270[0m, in [35mprompt_worker[0m
    [31mcomfy.model_management.soft_empty_cache[0m[1;31m()[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^[0m
2025-12-22T01:52:42.873261 - 2025-12-22T01:52:42.873319 -   File [35m"/home/zeuss194/COMFY/ComfyUI/custom_nodes/ComfyUI-MultiGPU/device_utils.py"[0m, line [35m258[0m, in [35msoft_empty_cache_distorch2_patched[0m
    [31moriginal_soft_empty_cache[0m[1;31m(force)[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^[0m
2025-12-22T01:52:42.873395 - 2025-12-22T01:52:42.873432 -   File [35m"/home/zeuss194/COMFY/ComfyUI/comfy/model_management.py"[0m, line [35m1523[0m, in [35msoft_empty_cache[0m
    [31mtorch.cuda.empty_cache[0m[1;31m()[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^[0m
2025-12-22T01:52:42.873458 - 2025-12-22T01:52:42.873488 -   File [35m"/home/zeuss194/COMFY/ComfyUI/Comfyenv313/lib/python3.13/site-packages/torch/cuda/memory.py"[0m, line [35m224[0m, in [35mempty_cache[0m
    [31mtorch._C._cuda_emptyCache[0m[1;31m()[0m
    [31m~~~~~~~~~~~~~~~~~~~~~~~~~[0m[1;31m^^[0m
2025-12-22T01:52:42.873525 - 2025-12-22T01:52:42.873566 - [1;35mtorch.AcceleratorError[0m: [35mHIP error: an illegal memory access was encountered
Search for `hipErrorIllegalAddress' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__HIPRT__TYPES.html for more information.
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
[0m
2025-12-22T01:52:42.873593 - 
```
## Attached Workflow
Please make sure that workflow does not contain any sensitive information such as API keys or passwords.
```
Workflow too large. Please manually upload the workflow from local file system.
```

## Additional Context
After dumping errors logs in claude, beside asking me to reinstall an outdated rocm... he also gave me this answer

Your Options
Option 1: Report Bug to PyTorch (Recommended)
This needs to be fixed upstream. Report it here:
https://github.com/pytorch/pytorch/issues
Include:

GPU: AMD Radeon AI PRO R9700 (gfx1201)
PyTorch: 2.9.1+rocm7.1.1.git351ff442
Issue: tensor.copy_() with non_blocking=True causes illegal memory access
Reproducible: Happens intermittently during SDXL generation in ComfyUI


[fus3Adu.json](https://github.com/user-attachments/files/24282315/fus3Adu.json)




---

### 评论 #5 — zichguan-amd (2025-12-22T23:21:14Z)

Hi @FR-Mister-T, thanks for the additional information. So far, I cannot repro the issue using the provided workflow on 7900XTX + ROCm 7.1.1 + torch 2.10.0.dev20251210+rocm7.1. I ran the workload for about 45 times with no error.

However, this seems to be the same issue as https://github.com/ROCm/ROCm/issues/5245 and https://github.com/ROCm/TheRock/issues/1795, you can try some workarounds like https://github.com/ROCm/TheRock/issues/1795#issuecomment-3519877539.

---

### 评论 #6 — FR-Mister-T (2026-01-03T01:21:10Z)

Hello,

I manage to get back to a stable working environment (for rx9700 pro ai) using both "amdgpu.cwsr_enable=0" in kernel boot arg

and using the following pytorch/rocm package (whl)

wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.0.2/torch-2.9.1.dev20251204%2Brocm7.0.2.git351ff442-cp313-cp313-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.0.2/torchvision-0.24.0%2Brocm7.0.2.gitb919bd0c-cp313-cp313-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.0.2/torchaudio-2.9.0%2Brocm7.0.2.gite3c6ee2b-cp313-cp313-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.0.2/triton-3.5.1%2Brocm7.0.2.gita272dfa8-cp313-cp313-linux_x86_64.whl



---

### 评论 #7 — zichguan-amd (2026-01-05T14:32:15Z)

Great, then it's the same kernel issue, please monitor the parent issue for resolution.

---

### 评论 #8 — fjankovi (2026-02-11T09:40:47Z)

@zichguan-amd Can this be closed now? The related issues are all resolved in ROCm 7.2

---

### 评论 #9 — zichguan-amd (2026-02-11T15:28:58Z)

Yes, closing as completed

---
