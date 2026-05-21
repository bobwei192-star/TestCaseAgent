# [Issue]: RDNA3 HIP Memory Pool Fragmentation causes massive slowdown on Windows after VRAM-heavy workload

> **Issue #6007**
> **状态**: open
> **创建时间**: 2026-02-28T10:28:31Z
> **更新时间**: 2026-04-17T19:12:00Z
> **作者**: ReinerBforartists
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6007

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

(Get-WmiObject Win32_OperatingSystem).Version

After GPU heavy operation a ComfyUI workflow works significantly slower. 

After running a large VRAM-intensive HIP application (e.g., LM Studio) and closing it, subsequent HIP workloads (e.g., ComfyUI with PyTorch-HIP) experience massive slowdown.  I have now to reboot the system to be able to continue. At one point it even slows down in ComfyUI. But with loading a large LLM in LM Studio it is faster to reproduce:

Fresh boot ComfyUI: Zimage ~1 s, Qwen Image ~3 s per KSampler step
After VRAM-heavy app: Zimage ~25 s, Qwen Image ~45 s per KSampler step
GPU utilization: 100 % during slowdown
Dedicated GPU memory: ~31.4 / 32 GB
Total GPU memory: ~53.5 / 62.8 GB
Shared GPU memory: ~22.2 / 30.8 GB
Power state: normal (full GPU clocks)

This indicates that GPU memory pool is fragmented or memory residency is not properly cleared, causing allocations to spill to system RAM.

### Operating System

Windows 11 Pro 25H2

### CPU

AMD Ryzen 9 9900X

### GPU

AMD Radeon AI Pro 32 Gb

### ROCm Version

7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

Boot Windows
Run ComfyUI → generate image (fast, 1–3 s)
Close ComfyUI
Run a VRAM-heavy HIP application (LM Studio, full model load)
Close HIP application
Run ComfyUI image workflow again → extreme slowdown observed

ComfyUI workflows to reproduce the problem:

[comfyui workflows.zip](https://github.com/user-attachments/files/25620560/comfyui.workflows.zip)

Be aware of this AMD related bug. Create a directory on D:\a\ComfyUI, and copy over the python_embedded folder from the ComfyUI portable. 

https://github.com/Comfy-Org/ComfyUI/issues/11546



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

![Image](https://github.com/user-attachments/assets/95394962-2d06-451f-9571-931f9126335d)

![Image](https://github.com/user-attachments/assets/51680387-f923-4485-8ce8-168466cb64cd)

![Image](https://github.com/user-attachments/assets/fbb75df7-ef4c-4a8c-8ca8-3f5c66ba68cb)

Maybe related issue, has also to do with a massive slowdown at a second run.

https://github.com/Comfy-Org/ComfyUI/issues/12672

Comfy log of a slow generation, which produced the images in three seconds after a fresh boot:
```

G:\comfyamd\ComfyUI_windows_portable>set HIP_PRINT_ENV=1

G:\comfyamd\ComfyUI_windows_portable>set HIP_TRACE_API=1

G:\comfyamd\ComfyUI_windows_portable>set PYTORCH_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512

G:\comfyamd\ComfyUI_windows_portable>.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --disable-pinned-memory --use-split-cross-attention
G:\comfyamd\ComfyUI_windows_portable\python_embeded\Lib\site-packages\requests\__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (6.0.0.post1)/charset_normalizer (3.4.4) doesn't match a supported version!
  warnings.warn(
[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** ComfyUI startup time: 2026-02-28 11:04:48.383
** Platform: Windows
** Python version: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
** Python executable: G:\comfyamd\ComfyUI_windows_portable\python_embeded\python.exe
** ComfyUI Path: G:\comfyamd\ComfyUI_windows_portable\ComfyUI
** ComfyUI Base Folder Path: G:\comfyamd\ComfyUI_windows_portable\ComfyUI
** User directory: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\user
** ComfyUI-Manager config path: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\user\default\ComfyUI-Manager\config.ini
** Log path: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\user\comfyui.log

Prestartup times for custom nodes:
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\rgthree-comfy
   6.8 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Manager

Found comfy_kitchen backend cuda: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Found comfy_kitchen backend triton: {'available': False, 'disabled': True, 'unavailable_reason': "ImportError: No module named 'triton'", 'capabilities': []}
Found comfy_kitchen backend eager: {'available': True, 'disabled': False, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Checkpoint files will always be loaded safely.
Total VRAM 32624 MB, total RAM 63140 MB
pytorch version: 2.9.1+rocmsdk20260116
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1201
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon AI PRO R9700 : native
Using async weight offloading with 2 streams
Using split optimization for attention
Python version: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
ComfyUI version: 0.15.0
ComfyUI frontend version: 1.39.16
[Prompt Server] web root: G:\comfyamd\ComfyUI_windows_portable\python_embeded\Lib\site-packages\comfyui_frontend_package\static
Traceback (most recent call last):
  File "G:\comfyamd\ComfyUI_windows_portable\ComfyUI\nodes.py", line 2224, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "G:\comfyamd\ComfyUI_windows_portable\ComfyUI\comfy_extras\nodes_glsl.py", line 64, in <module>
    _check_opengl_availability()
  File "G:\comfyamd\ComfyUI_windows_portable\ComfyUI\comfy_extras\nodes_glsl.py", line 35, in _check_opengl_availability
    raise RuntimeError(
RuntimeError: OpenGL dependencies not available.
Please install the updated requirements.txt file by running:
G:\comfyamd\ComfyUI_windows_portable\python_embeded\python.exe -s -m pip install -r G:\comfyamd\ComfyUI_windows_portable\ComfyUI\requirements.txt
If you are on the portable package you can run: update\update_comfyui.bat to solve this problem.


Cannot import G:\comfyamd\ComfyUI_windows_portable\ComfyUI\comfy_extras\nodes_glsl.py module for custom nodes: OpenGL dependencies not available.
Please install the updated requirements.txt file by running:
G:\comfyamd\ComfyUI_windows_portable\python_embeded\python.exe -s -m pip install -r G:\comfyamd\ComfyUI_windows_portable\ComfyUI\requirements.txt
If you are on the portable package you can run: update\update_comfyui.bat to solve this problem.

ComfyUI-FreeMemory nodes loaded: Image, Latent, Model, CLIP, and String versions available.
ComfyUI-GGUF: Allowing full torch compile
### Loading: ComfyUI-Impact-Pack (V8.28.2)
[Impact Pack] Wildcard total size (0.00 MB) is within cache limit (50.00 MB). Using full cache mode.
[Impact Pack] Wildcards loading done.
### Loading: ComfyUI-Manager (V3.37.1)
[ComfyUI-Manager] network_mode: public
### ComfyUI Revision: 150 [b874bd2b] *DETACHED | Released on '2026-02-24'
Error loading module AILab_QwenVL: cannot import name 'AutoModelForVision2Seq' from 'transformers' (G:\comfyamd\ComfyUI_windows_portable\python_embeded\Lib\site-packages\transformers\__init__.py)
Error loading module AILab_QwenVL_GGUF_PromptEnhancer: No module named 'llama_cpp'
Error loading module AILab_QwenVL_PromptEnhancer: cannot import name 'ATTENTION_MODES' from 'AILab_QwenVL' (G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-QwenVL\AILab_QwenVL.py)
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/model-list.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/alter-list.json
Note: NumExpr detected 24 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 16.
NumExpr defaulting to 16 threads.
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/github-stats.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/extension-node-map.json
FizzleDorf Custom Nodes: Loaded

     ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗    ██████╗ ███╗   ██╗
     ██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║   ██╔═══██╗████╗  ██║
     ██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║   ██║   ██║██╔██╗ ██║
     ██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║   ██║   ██║██║╚██╗██║
     ██║  ██║   ██║   ██║  ██║██║ ╚████║   ╚██████╔╝██║ ╚████║
     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═══╝
████████╗██╗  ██╗███████╗   ██╗███╗   ██╗███████╗██╗██████╗ ███████╗
╚══██╔══╝██║  ██║██╔════╝   ██║████╗  ██║██╔════╝██║██╔══██╗██╔════╝
   ██║   ███████║█████╗     ██║██╔██╗ ██║███████╗██║██║  ██║█████╗
   ██║   ██╔══██║██╔══╝     ██║██║╚██╗██║╚════██║██║██║  ██║██╔══╝
   ██║   ██║  ██║███████╗   ██║██║ ╚████║███████║██║██████╔╝███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═════╝ ╚══════╝

             ⚡ R Y A N   O N   T H E   I N S I D E ⚡


[RyanOnTheInside] Copying extension file: widget_hotkey.js
[RyanOnTheInside] Failed to load .nodes.masks.temporal_masks: No module named 'pymunk'
[RyanOnTheInside] Failed to load .nodes.masks.optical_flow_masks: No module named 'pymunk'
[RyanOnTheInside] Failed to load .nodes.masks.particle_system_masks: No module named 'pymunk'
[RyanOnTheInside] Failed to load .nodes.masks.flex_masks: No module named 'pymunk'
Checking for AdvancedLivePortrait at: None
Checking for Advanced-ControlNet at: None
Checking for AnimateDiff-Evolved at: None
ComfyUI-AdvancedLivePortrait not found. FlexExpressionEditor will not be available. Install ComfyUI-AdvancedLivePortrait and restart ComfyUI.
ComfyUI-Advanced-ControlNet not found. Advanced-ControlNet feature nodes will not be available. Install ComfyUI-Advanced-ControlNet and restart ComfyUI.
ComfyUI-AnimateDiff-Evolved not found. AnimateDiff feature nodes will not be available. Install ComfyUI-AnimateDiff-Evolved and restart ComfyUI.
[comfyui_ryanontheinside.acestep] [ACE-Step Patches] Patched resolve_areas_and_cond_masks_multidim for 1D latent support
[comfyui_ryanontheinside.acestep] [ACE-Step Patches] Patched comfy.utils.reshape_mask for 1D latent support
[Crystools ERROR] pynvml is not installed. No module named 'pynvml'
[Crystools WARNING] No GPU monitoring libraries available.

[rgthree-comfy] Loaded 48 fantastic nodes. 🎉

[rgthree-comfy] ComfyUI's new Node 2.0 rendering may be incompatible with some rgthree-comfy nodes and features, breaking some rendering as well as losing the ability to access a node's properties (a vital part of many nodes). It also appears to run MUCH more slowly spiking CPU usage and causing jankiness and unresponsiveness, especially with large workflows. Personally I am not planning to use the new Nodes 2.0 and, unfortunately, am not able to invest the time to investigate and overhaul rgthree-comfy where needed. If you have issues when Nodes 2.0 is enabled, I'd urge you to switch it off as well and join me in hoping ComfyUI is not planning to deprecate the existing, stable canvas rendering all together.

Error: modelscope not installed. Please run: pip install modelscope

Import times for custom nodes:
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\websocket_image_save.py
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\HeartMuLa_ComfyUI
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-simple-prompt-batcher
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\z-image-turbo
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui_auto_prompt_schedule
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-FreeMemory
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-VFI
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\Crystools-MonitorOnly
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyMath
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Custom-Scripts
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-frame-interpolation
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\Derfuu_ComfyUI_ModdedNodes
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-QwenVL
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\rgthree-comfy
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-GGUF
   0.0 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-VideoHelperSuite
   0.1 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-LTXVideo
   0.2 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI_FizzNodes
   0.2 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-levelpixel
   0.2 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Impact-Pack
   0.4 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui_ryanonyheinside
   0.5 seconds: G:\comfyamd\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Manager

WARNING: some comfy_extras/ nodes did not import correctly. This may be because they are missing some dependencies.

IMPORT FAILED: nodes_glsl.py

This issue might be caused by new missing dependencies added the last time you updated ComfyUI.
Please run the update script: update/update_comfyui.bat

Context impl SQLiteImpl.
Will assume non-transactional DDL.
Assets scan(roots=['models']) completed in 0.015s (created=0, skipped_existing=65, orphans_pruned=0, total_seen=65)
Starting server

To see the GUI go to: http://127.0.0.1:8188
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/clipspace.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/groupNode.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/widgetInputs.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/button.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/buttonGroup.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Found quantization metadata version 1
Using MixedPrecisionOps for text encoder
Requested to load QwenImageTEModel_
loaded completely;  7910.28 MB loaded, full load: True
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cuda:0, dtype: torch.float16
[Prompt Batcher] 📋 Batching 10 prompts:
[Prompt Batcher]   1. modern interior, A singer wearing headphones, singing into a...
[Prompt Batcher]   2. modern interior, A handful of fans in streetwear — some film...
[Prompt Batcher]   3. modern interior, A waitress in simple black attire walks slo...
[Prompt Batcher]   4. modern interior, The singer wearing headphones, singing into...
[Prompt Batcher]   5. modern interior, A fan in streetwear lies flat on the wooden...
[Prompt Batcher]   6. modern interior, A waitress carrying a tray of ceramic mugs ...
[Prompt Batcher]   7. modern interior, The producer behind the laptop, surrounded ...
[Prompt Batcher]   8. modern interior, A fan in streetwear sits cross-legged near ...
[Prompt Batcher]   9. modern interior, The singer wearing headphones, now off-mic ...
[Prompt Batcher]   10. modern interior, The rooftop is silent now — the singer wear...
model weight dtype torch.float8_e4m3fn, manual cast: torch.bfloat16
model_type FLUX
Requested to load QwenImage
Unloaded partially: 3180.03 MB freed, 4730.25 MB remains loaded, 453.25 MB buffer reserved, lowvram patches: 0
loaded completely; 24392.90 MB usable, 19483.95 MB loaded, full load: True
 50%|██████████████████████████████████████████                                          | 2/4 [00:24<00:28, 14.14s/it]FETCH ComfyRegistry Data [DONE]
[ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json [DONE]
[ComfyUI-Manager] All startup tasks have been completed.
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:45<00:00, 11.35s/it]
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:41<00:00, 10.33s/it]
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:41<00:00, 10.28s/it]
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:40<00:00, 10.17s/it]
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:42<00:00, 10.56s/it]
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:41<00:00, 10.45s/it]
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:41<00:00, 10.48s/it]
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:41<00:00, 10.32s/it]
  0%|                                                                                            | 0/4 [00:00<?, ?it/s]




```


---

## 评论 (20 条)

### 评论 #1 — ReinerBforartists (2026-03-01T17:17:21Z)

May i add that this is for me a showstopper bug? The speed slowdown makes ComfyUI useless for me for image generation.

---

### 评论 #2 — schung-amd (2026-03-04T17:17:55Z)

Hi @ReinerBforartists, thanks for the report. I was able to reproduce this with a 7900XTX following these steps:

1. Run the ComfyUI Qwen workload you provided, observe ~1it/s
2. Close ComfyUI, launch LM Studio
3. Load a large model which requires shared memory usage (did not test with smaller models), submit a few prompts
4. Close LM Studio, relaunch ComfyUI
5. Rerun Qwen workload, observe >1m per iteration

A few notes:
- After closing LM Studio, task manager was still showing a large amount of VRAM usage
- ComfyUI had a KSampler crash after which most of the resident VRAM usage was cleared (but this did not help with the performance)
- I had to reduce the image size on the post-LM Studio runs, otherwise the ComfyUI backend was crashing. About 6GB of VRAM usage was still resident post-LM Studio and post-crash, which may be the cause of this.

I'll take a look. From what I'm seeing my initial suspicion is that LM Studio is not properly clearing its memory usage on closing, and that ComfyUI is not seeing or respecting the current memory usage when pinning memory; these issues might or might not be on our end, I'll have to do a deeper dive to isolate the root cause.

---

### 评论 #3 — schung-amd (2026-03-04T20:26:09Z)

The LM Studio lingering memory usage can be avoided/worked around by loading the LLM with "Try mmap()" disabled; see https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1198. After doing this the memory is freed appropriately on closing LM Studio and there is no performance degradation in subsequent ComfyUI usage.

Are you seeing this issue with workloads other than LM Studio?

---

### 评论 #4 — schung-amd (2026-03-05T00:36:20Z)

Oddly I can no longer reproduce this after installing the ROCm backend for LM Studio (I realized my initial repros used the default Vulkan backend) and rebooting. As such I don't think this is on the ROCm end, but will reinstall everything and try to repro again.

---

### 评论 #5 — ReinerBforartists (2026-03-05T06:40:46Z)

> The LM Studio lingering memory usage can be avoided/worked around by loading the LLM with "Try mmap()" disabled; see [lmstudio-ai/lmstudio-bug-tracker#1198](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1198). After doing this the memory is freed appropriately on closing LM Studio and there is no performance degradation in subsequent ComfyUI usage.
> 
> Are you seeing this issue with workloads other than LM Studio?

No. But i have no other software occupying the vram this heavily. And thanks for the workaround. I will have a look if i can reproduce the fix here.

---

### 评论 #6 — ReinerBforartists (2026-03-05T07:20:39Z)

I tried, and turning off try mmap has no effect here. I currently use LM Studio 0.4.6.

Looking forward if you can repo it again. I still can in case this is of help.

---

### 评论 #7 — schung-amd (2026-03-05T15:40:36Z)

What model are you loading into LM Studio, and are you loading with the default settings? What version of Adrenalin are you on? Does this happen with both the Vulkan and ROCm backends for LM Studio?

---

### 评论 #8 — ReinerBforartists (2026-03-05T16:53:39Z)

It depends. For this test it was Qwen 3.5-35-a3b. It has 20 gb. See first screenshot in the issue.

> Does this happen with both the Vulkan and ROCm backends for LM Studio?

Good question, where do i switch that? I use the defaults. The runtime says GGUF Vulkan llama.cpp (Windows)

`[
  {
    "modelCompatibilityType": "gguf",
    "runtime": {
      "hardwareSurveyResult": {
        "compatibility": {
          "status": "Compatible"
        },
        "cpuSurveyResult": {
          "result": {
            "code": "Success",
            "message": ""
          },
          "cpuInfo": {
            "name": "AMD Ryzen 9 9900X 12-Core Processor            ",
            "architecture": "x86_64",
            "supportedInstructionSetExtensions": [
              "AVX",
              "AVX2"
            ]
          }
        },
        "memoryInfo": {
          "ramCapacity": 66206793728,
          "vramCapacity": 34208743424,
          "totalMemory": 100415537152
        },
        "gpuSurveyResult": {
          "result": {
            "code": "Success",
            "message": ""
          },
          "gpuInfo": [
            {
              "name": "AMD Radeon AI PRO R9700",
              "deviceId": 0,
              "totalMemoryCapacityBytes": 67312091136,
              "dedicatedMemoryCapacityBytes": 34208743424,
              "integrationType": "Discrete",
              "detectionPlatform": "Vulkan",
              "detectionPlatformVersion": "1.3.283",
              "otherInfo": {
                "deviceLUIDValid": "true",
                "deviceLUID": "e1f8000000000000",
                "deviceUUID": "00000000030000000000000000000000",
                "driverID": "1",
                "driverName": "AMD proprietary driver",
                "driverInfo": "26.2.2 (LLPC)",
                "vendorID": "4098"
              }
            },
            {
              "name": "AMD Radeon(TM) Graphics",
              "deviceId": 1,
              "totalMemoryCapacityBytes": 35250831360,
              "dedicatedMemoryCapacityBytes": 23590076416,
              "integrationType": "Integrated",
              "detectionPlatform": "Vulkan",
              "detectionPlatformVersion": "1.3.283",
              "otherInfo": {
                "deviceLUIDValid": "true",
                "deviceLUID": "1c1e010000000000",
                "deviceUUID": "000000000f0000000000000000000000",
                "driverID": "1",
                "driverName": "AMD proprietary driver",
                "driverInfo": "26.2.2 (AMD proprietary shader compiler)",
                "vendorID": "4098"
              }
            }
          ]
        }
      }
    }
  }
]`

![Image](https://github.com/user-attachments/assets/edb6a27d-193e-4a99-bd6e-2dd892939d5a)

![Image](https://github.com/user-attachments/assets/cfc6b4d3-48c5-4f94-b2da-7755c2aed7ab)




---

### 评论 #9 — ReinerBforartists (2026-03-06T11:34:04Z)

EDIT, just checked again, at Windows there is no ROCm runtime available. Just Vulkan. At Linux i have ROCm available. But it does not load any model then anymore. And this issue is about Windows.

![Image](https://github.com/user-attachments/assets/3e28cacc-6016-4f41-b74b-375ac212edb3)

---

### 评论 #10 — schung-amd (2026-03-06T16:05:45Z)

Yeah I realized the ROCm llama.cpp backend appears to be missing on Windows with the 9700 (and probably other RDNA4 cards?)... it's there for the 7900XTX so I assume support is missing in LM Studio and/or llama.cpp for that card. I swapped the hardware in my test system to be closer to yours, but I still couldn't repro with the Vulkan v2.5.1 backend and a 9700 with Adrenalin driver version 26.1.1. From your output I think you're on 26.2.2, can you try downgrading to 26.1.1? Meanwhile I'll see if I can get a repro with 26.2.2.

---

### 评论 #11 — schung-amd (2026-03-06T18:31:04Z)

Tried 26.2.2, still could not repro. Noticed some differences in your ComfyUI logs and the default settings. Is there a reason you're disabling pinned memory? I also only have installed what is required by your Qwen workflow, and don't have any of the additional custom nodes installed, although I don't think they would cause issues here if they're not being used.

---

### 评论 #12 — ReinerBforartists (2026-03-07T06:53:21Z)

Pinned memory is a cuda feature. It does nothing for an AMD card, requires more vram and i was told that it can even cause errors. So to turn it off is one of the common tips that you can find when using an AMD card.

For the driver i am stuck to what Adrenalin offers me. And yes i am at 216.2.2, the newest version. I don't see a way to downgrade. Or do you mean to install the old Adrenalin version?

My start parameters in the bat are currently 

set PYTORCH_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --disable-pinned-memory --use-split-cross-attention --cache-none 

--cache none is from the experiments.

Another interesting question is why you could reproduce it with the first try and not with the second try. What has changed?

And you need a bit patience. I did another test today just to rule out that the problem is meanwhile fixed.  I run the newest LM Studio version here, 0.4.6. And loading LM Studio once before starting comfyui did not lead to the degradation. The second use of LM Studio then did. And my qwen image generation went down from 3 seconds to 45 seconds again.

Mh, in LM Studio you could try to use the maxium context length for the model and chat with it a bit. This requires more vram then. I run definitely faster into the problem that way.

![Image](https://github.com/user-attachments/assets/c88ea985-9495-4215-b510-55b3b34a539e)


---

### 评论 #13 — mikecolins (2026-03-07T07:41:27Z)

Ran into the exact same issue, was driving me nuts. AMD version 26.2.2 on windows 11. I was using Qwen Image Edit model (AIO) about 20gb in size, so quite at the limit of my XTX card. Would consistently slow down after first image edit beyond a fresh restart even prior to using LM Studio in my workflow. In fact, I introduced a prompt expander because I wanted to reduce the generation attempts due to horrible turnaround time.

On the same setup I switched to flux1-kontext and now it is consistently working to properly load/unload and not constantly dump everything into the ram. Flux now keeps the generation timing pretty consistent and decently quick despite the higher step count. Tried all kinds of things in starting comfyUI, but nothing worked to fix it for Qwen Image Edit. Just adding my comfy startup log in case it helps tracking down why this may be happening. (some of the experimentation stuff like reserving vram still in there but makes no difference so shouldn't hurt):

comfy-aimdo failed to load: Could not find module 'C:\Users\x\Documents\ComfyUI\.venv\Lib\site-packages\comfy_aimdo\aimdo.dll' (or one of its dependencies). Try using the full path with constructor syntax.
NOTE: comfy-aimdo is currently only support for Nvidia GPUs
Setting output directory to: C:\Users\x\Documents\ComfyUI\output
Setting input directory to: C:\Users\x\Documents\ComfyUI\input
Setting user directory to: C:\Users\x\Documents\ComfyUI\user
[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** ComfyUI startup time: 2026-03-07 16:50:44.173
** Platform: Windows
** Python version: 3.12.11 (main, Aug 18 2025, 19:17:54) [MSC v.1944 64 bit (AMD64)]
** Python executable: C:\Users\x\Documents\ComfyUI\.venv\Scripts\python.exe
** ComfyUI Path: C:\Users\x\AppData\Local\Programs\ComfyUI\resources\ComfyUI
** ComfyUI Base Folder Path: C:\Users\x\AppData\Local\Programs\ComfyUI\resources\ComfyUI
** User directory: C:\Users\x\Documents\ComfyUI\user
** ComfyUI-Manager config path: C:\Users\x\Documents\ComfyUI\user\__manager\config.ini
** Log path: C:\Users\x\Documents\ComfyUI\user\comfyui.log

Prestartup times for custom nodes:
   0.0 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\comfyui-easy-use
  12.0 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\ComfyUI-Manager

Found comfy_kitchen backend cuda: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Found comfy_kitchen backend triton: {'available': False, 'disabled': True, 'unavailable_reason': "ImportError: No module named 'triton'", 'capabilities': []}
Found comfy_kitchen backend eager: {'available': True, 'disabled': False, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Checkpoint files will always be loaded safely.
Total VRAM 24560 MB, total RAM 32610 MB
pytorch version: 2.9.1+rocmsdk20260116
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1100
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 7900 XTX : native
Using async weight offloading with 2 streams
Enabled pinned memory 14674.0
Using pytorch attention
Python version: 3.12.11 (main, Aug 18 2025, 19:17:54) [MSC v.1944 64 bit (AMD64)]
ComfyUI version: 0.16.3
[Prompt Server] web root: C:\Users\x\AppData\Local\Programs\ComfyUI\resources\ComfyUI\web_custom_versions\desktop_app
[ComfyUI-Easy-Use] server: v1.3.6 Loaded
[ComfyUI-Easy-Use] web root: C:\Users\x\Documents\ComfyUI\custom_nodes\comfyui-easy-use\web_version/v2 Loaded
ComfyUI-GGUF: Allowing full torch compile
### Loading: ComfyUI-Impact-Pack (V8.28.2)
[Impact Pack] Wildcard total size (0.00 MB) is within cache limit (50.00 MB). Using full cache mode.
### Loading: ComfyUI-Impact-Subpack (V1.3.5)
[Impact Pack/Subpack] Using folder_paths to determine whitelist path: C:\Users\x\Documents\ComfyUI\user\default\ComfyUI-Impact-Subpack\model-whitelist.txt
[Impact Pack/Subpack] Ensured whitelist directory exists: C:\Users\x\Documents\ComfyUI\user\default\ComfyUI-Impact-Subpack
[Impact Pack] Wildcards loading done.
[Impact Pack/Subpack] Loaded 0 model(s) from whitelist: C:\Users\x\Documents\ComfyUI\user\default\ComfyUI-Impact-Subpack\model-whitelist.txt
[Impact Subpack] ultralytics_bbox: C:\Users\x\Documents\ComfyUI\models\ultralytics\bbox
[Impact Subpack] ultralytics_segm: C:\Users\x\Documents\ComfyUI\models\ultralytics\segm
### Loading: ComfyUI-Manager (V3.39.2)
[ComfyUI-Manager] network_mode: public
[ComfyUI-Manager] ComfyUI per-queue preview override detected (PR #11261). Manager's preview method feature is disabled. Use ComfyUI's --preview-method CLI option or 'Settings > Execution > Live preview method'.
### ComfyUI Revision: UNKNOWN (The currently installed ComfyUI is not a Git repository)

Import times for custom nodes:
   0.0 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\qweneditutils
   0.0 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\comfyui-unload-model
   0.0 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\ComfyUI-GGUF
   0.0 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\video_prompter
   0.0 seconds: C:\Users\xh\Documents\ComfyUI\custom_nodes\ComfyUI-Manager
   0.1 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\comfyui-impact-subpack
   0.2 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\comfyui-impact-pack
   4.8 seconds: C:\Users\x\Documents\ComfyUI\custom_nodes\comfyui-easy-use

[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/alter-list.json
Context impl SQLiteImpl.
Will assume non-transactional DDL.
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/model-list.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/github-stats.json
Assets scan(roots=['models']) completed in 0.061s (created=0, skipped_existing=68, orphans_pruned=0, total_seen=68)
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/extension-node-map.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json
Starting server

To see the GUI go to: http://127.0.0.1:8188
FETCH ComfyRegistry Data: 5/128
FETCH ComfyRegistry Data: 10/128
FETCH ComfyRegistry Data: 15/128
FETCH ComfyRegistry Data: 20/128
FETCH ComfyRegistry Data: 25/128
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/clipspace.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /extensions/core/groupNode.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/buttonGroup.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
[DEPRECATION WARNING] Detected import of deprecated legacy API: /scripts/ui/components/button.js. This is likely caused by a custom node extension using outdated APIs. Please update your extensions or contact the extension author for an updated version.
FETCH ComfyRegistry Data: 30/128
FETCH ComfyRegistry Data: 35/128
got prompt
got prompt
got prompt
got prompt
got prompt
FETCH ComfyRegistry Data: 40/128
FETCH ComfyRegistry Data: 45/128
FETCH ComfyRegistry Data: 50/128
FETCH ComfyRegistry Data: 55/128
FETCH ComfyRegistry Data: 60/128
FETCH ComfyRegistry Data: 65/128
FETCH ComfyRegistry Data: 70/128
FETCH ComfyRegistry Data: 75/128
FETCH ComfyRegistry Data: 80/128
FETCH ComfyRegistry Data: 85/128
FETCH ComfyRegistry Data: 90/128
FETCH ComfyRegistry Data: 95/128
FETCH ComfyRegistry Data: 100/128
FETCH ComfyRegistry Data: 105/128
FETCH ComfyRegistry Data: 110/128
[LLM Backend] LM Studio response keys: ['id', 'object', 'created', 'model', 'choices', 'usage', 'stats', 'system_fingerprint']
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Requested to load AutoencodingEngine
loaded completely; 9764.51 MB usable, 159.87 MB loaded, full load: True
FETCH ComfyRegistry Data: 115/128
FETCH ComfyRegistry Data: 120/128
clip missing: ['text_projection.weight']
Requested to load FluxClipModel_
loaded completely;  9609.86 MB loaded, full load: True
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cuda:0, dtype: torch.float16
FETCH ComfyRegistry Data: 125/128
model weight dtype torch.float8_e4m3fn, manual cast: torch.bfloat16
model_type FLUX
FETCH ComfyRegistry Data [DONE]
[ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes



---

### 评论 #14 — ReinerBforartists (2026-03-07T07:47:58Z)

> On the same setup I switched to flux1-kontext and now it is consistently working to properly load/unload and not constantly dump everything into the ram. 

Interesting observation. Thanks. I can reproduce the problem wiht Qwen Image and Z-Image. Flux deals different with the VAE from what i know. Lemme test ...

EDIT; ah i need to download the weights first. Might take a few moments ...

---

### 评论 #15 — ReinerBforartists (2026-03-07T11:02:16Z)

Observation from Linux. When i close LM Studio immediately, then the model does not unload, and remains in VRam. The Vram remains occpupied. 98 zo 99%. When i first eject the model, and then close LM Studio, then the Vram gets freed. It goes down to 1%. But something is then blocking. At Linux i cannot load the model in LM Studio again. At Windows i can. I tried then at Windows, and unloading the model also here frees the Vram. And image generation in Comfy is now back to normal speed.

So, this part is a LM Studio bug. I will report it to LM Studio.

But we should not focus on LM Studio here. It's just the quickest way for me to reproduce the problem right now, to demonstrate the problem. LM Studio is closed. The Vram should simply not be occupied anymore when the software that uses the Vram is closed, no matter what software was active. And i get the same issue after only using ComfyUI for a while, like confirmed by mikecolins. It just takes a bit longer.

---

### 评论 #16 — mikecolins (2026-03-07T17:36:18Z)

Awesome, thank you for reproducing the issue so quickly. Did you by any chance find a workaround how to free up the VRAM again once it happens on windows? Got to admit, I would like an easier way to get full speed with qwen image edit again than restarting PC. 

---

### 评论 #17 — ReinerBforartists (2026-03-07T19:19:45Z)

Unfortunately not,. sorry. Once the Vram is occupied by the LLM and LM Studio is closed only reboot is left. And it is as told not a fix for this issue. It is just a quick way to reproduce the underlying problem. As told, i can, as you, run into the slow state with just ComfyUI alone. It just takes a bit longer then.

EDIT. hah i just noticed a thing. Reload LM Studio, load the model again, then eject. This frees the Vram.

---

### 评论 #18 — schung-amd (2026-04-17T18:12:19Z)

Sorry for the delay on this, I was still unable to repro this but we have some VRAM allocation-related fixes in an upcoming Adrenalin driver release which I'm hoping will help. I'll update when that's available.

---

### 评论 #19 — ReinerBforartists (2026-04-17T18:16:00Z)

Thanks for not forgetting about the issue. 

Use LM Studio, load a model, watch the drop. It's really LM Studio not unloading its models. And then the ram is of course occupied and not longer available for ComfyUI. I can see this here in the task manager.

Curious enough i had the same experience by using an LLM inside of ComfyUI. The model did not unload after closing the workflow. And different from LM Studio there was no way to unload it afterwards neither. I had to reboot.

---

### 评论 #20 — schung-amd (2026-04-17T19:12:00Z)

Yeah the one time I did repro it was clearly an LM Studio unloading issue, but didn't see it again. Will revisit that first once the new driver is available. I was never able to repro with other workflow interruptions, but we have seen a possibly related issue where loading multiple models simultaneously can lead to excessive VRAM usage in some scenarios.

---
