# ComfyUI with flash-attention gives "ImportError: cannot import name 'intel' from 'triton._C.libtriton'"

> **Issue #4698**
> **状态**: closed
> **创建时间**: 2025-04-29T00:49:24Z
> **更新时间**: 2025-04-29T22:45:49Z
> **关闭时间**: 2025-04-29T22:45:48Z
> **作者**: hartmark
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4698

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Reproducing steps:

Checkout my helper script:
https://github.com/hartmark/sd-rocm/tree/flash-attention-wip

Run:
`./run-local.sh`

Output:
```
Docker instance: local-comfyui
GFX_NAME = gfx1101
venv environment already initialized. Skipping initialization steps.
====================
Requirement already satisfied: pip in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (25.1)
Reinstall ROCm torch? (y/N): y
Install ROCm version of torch
====================
Found existing installation: torch 2.8.0.dev20250418+rocm6.4
Uninstalling torch-2.8.0.dev20250418+rocm6.4:
  Successfully uninstalled torch-2.8.0.dev20250418+rocm6.4
Found existing installation: torchaudio 2.6.0.dev20250428+rocm6.3
Uninstalling torchaudio-2.6.0.dev20250428+rocm6.3:
  Successfully uninstalled torchaudio-2.6.0.dev20250428+rocm6.3
Found existing installation: torchvision 0.22.0.dev20250418+rocm6.3
Uninstalling torchvision-0.22.0.dev20250418+rocm6.3:
  Successfully uninstalled torchvision-0.22.0.dev20250418+rocm6.3
Found existing installation: safetensors 0.4.5
Uninstalling safetensors-0.4.5:
  Successfully uninstalled safetensors-0.4.5
Found existing installation: pytorch-triton 3.3.0+gitab727c40
Uninstalling pytorch-triton-3.3.0+gitab727c40:
  Successfully uninstalled pytorch-triton-3.3.0+gitab727c40
Found existing installation: triton 3.3.0
Uninstalling triton-3.3.0:
  Successfully uninstalled triton-3.3.0
Collecting triton
  Using cached triton-3.3.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (1.5 kB)
Requirement already satisfied: setuptools>=40.8.0 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from triton) (75.8.0)
Using cached triton-3.3.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (156.5 MB)
Installing collected packages: triton
Successfully installed triton-3.3.0
Looking in indexes: https://download.pytorch.org/whl/nightly/rocm6.4
Collecting torch
  Using cached https://download.pytorch.org/whl/nightly/rocm6.4/torch-2.8.0.dev20250428%2Brocm6.4-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (27 kB)
Collecting torchvision
  Using cached https://download.pytorch.org/whl/nightly/rocm6.3/torchvision-0.22.0.dev20250418%2Brocm6.3-cp312-cp312-linux_x86_64.whl.metadata (6.2 kB)
Collecting safetensors
  Using cached https://download.pytorch.org/whl/nightly/safetensors-0.4.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (434 kB)
Requirement already satisfied: triton in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (3.3.0)
Collecting pytorch_triton
  Using cached https://download.pytorch.org/whl/nightly/pytorch_triton-3.3.0%2Bgitab727c40-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (1.4 kB)
Requirement already satisfied: filelock in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (3.17.0)
Requirement already satisfied: typing-extensions>=4.10.0 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (4.12.2)
Requirement already satisfied: setuptools in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (75.8.0)
Requirement already satisfied: sympy>=1.13.3 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (1.13.3)
Requirement already satisfied: networkx in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (3.4.2)
Requirement already satisfied: jinja2 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (3.1.5)
Requirement already satisfied: fsspec in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (2024.12.0)
Requirement already satisfied: pytorch-triton-rocm==3.3.0+git96316ce5 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch) (3.3.0+git96316ce5)
Requirement already satisfied: numpy in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torchvision) (1.26.4)
Collecting torch
  Using cached https://download.pytorch.org/whl/nightly/rocm6.4/torch-2.8.0.dev20250418%2Brocm6.4-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (27 kB)
Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torchvision) (11.1.0)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from sympy>=1.13.3->torch) (1.3.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from jinja2->torch) (3.0.2)
Using cached https://download.pytorch.org/whl/nightly/rocm6.3/torchvision-0.22.0.dev20250418%2Brocm6.3-cp312-cp312-linux_x86_64.whl (3.1 MB)
Using cached https://download.pytorch.org/whl/nightly/rocm6.4/torch-2.8.0.dev20250418%2Brocm6.4-cp312-cp312-manylinux_2_28_x86_64.whl (3198.1 MB)
Using cached https://download.pytorch.org/whl/nightly/pytorch_triton-3.3.0%2Bgitab727c40-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (153.2 MB)
Installing collected packages: safetensors, pytorch_triton, torch, torchvision
Successfully installed pytorch_triton-3.3.0+gitab727c40 safetensors-0.4.5 torch-2.8.0.dev20250418+rocm6.4 torchvision-0.22.0.dev20250418+rocm6.3
Requirement already satisfied: numpy==1.26.4 in ./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (1.26.4)
Reinstall Flash Attention? (y/N): y
Setting up Flash Attention with ROCm support...
Found existing installation: flash_attn 2.7.4.post1
Uninstalling flash_attn-2.7.4.post1:
  Successfully uninstalled flash_attn-2.7.4.post1
Removing previous flash-attention directory...
Cloning flash-attention repository...
Cloning into '/home/markus/code/docker/sd-rocm/data/home-local/flash-attention'...
remote: Enumerating objects: 9567, done.
remote: Counting objects: 100% (11/11), done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 9567 (delta 4), reused 2 (delta 2), pack-reused 9556 (from 2)
Receiving objects: 100% (9567/9567), 9.24 MiB | 9.41 MiB/s, done.
Resolving deltas: 100% (7419/7419), done.
Installing flash-attention...
Obtaining file:///home/markus/code/docker/sd-rocm/data/home-local/flash-attention
  Preparing metadata (setup.py) ... done
Requirement already satisfied: torch in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from flash_attn==2.7.4.post1) (2.8.0.dev20250418+rocm6.4)
Requirement already satisfied: einops in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from flash_attn==2.7.4.post1) (0.8.0)
Requirement already satisfied: filelock in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (3.17.0)
Requirement already satisfied: typing-extensions>=4.10.0 in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (4.12.2)
Requirement already satisfied: setuptools in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (75.8.0)
Requirement already satisfied: sympy>=1.13.3 in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (1.13.3)
Requirement already satisfied: networkx in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (3.4.2)
Requirement already satisfied: jinja2 in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (3.1.5)
Requirement already satisfied: fsspec in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (2024.12.0)
Requirement already satisfied: pytorch-triton-rocm==3.3.0+git96316ce5 in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from torch->flash_attn==2.7.4.post1) (3.3.0+git96316ce5)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from sympy>=1.13.3->torch->flash_attn==2.7.4.post1) (1.3.0)
Requirement already satisfied: MarkupSafe>=2.0 in /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages (from jinja2->torch->flash_attn==2.7.4.post1) (3.0.2)
Installing collected packages: flash_attn
  DEPRECATION: Legacy editable install of flash_attn==2.7.4.post1 from file:///home/markus/code/docker/sd-rocm/data/home-local/flash-attention (setup.py develop) is deprecated. pip 25.3 will enforce this behaviour change. A possible replacement is to add a pyproject.toml or enable --use-pep517, and use setuptools >= 64. If the resulting installation is not behaving as expected, try using --config-settings editable_mode=compat. Please consult the setuptools documentation for more information. Discussion can be found at https://github.com/pypa/pip/issues/11457
  Running setup.py develop for flash_attn
Successfully installed flash_attn-2.7.4.post1
Flash Attention installation completed.
PyTorch version: 2.8.0.dev20250418+rocm6.4
Is CUDA available: True
CUDA device count: 1
CUDA device name: AMD Radeon Graphics
Already up to date.
[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** ComfyUI startup time: 2025-04-29 02:42:14.563
** Platform: Linux
** Python version: 3.12.8 (main, Jan  7 2025, 05:30:26) [GCC 14.2.1 20240910]
** Python executable: /home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/bin/python
** ComfyUI Path: /home/markus/code/docker/sd-rocm/data/home-local/comfyui
** ComfyUI Base Folder Path: /home/markus/code/docker/sd-rocm/data/home-local/comfyui
** User directory: /home/markus/code/docker/sd-rocm/data/home-local/comfyui/user
** ComfyUI-Manager config path: /home/markus/code/docker/sd-rocm/data/home-local/comfyui/user/default/ComfyUI-Manager/config.ini
** Log path: /home/markus/code/docker/sd-rocm/data/home-local/comfyui/user/comfyui.log
[ComfyUI-Manager] PyTorch is not installed

Prestartup times for custom nodes:
   1.5 seconds: /home/markus/code/docker/sd-rocm/data/home-local/comfyui/custom_nodes/ComfyUI-Manager

Checkpoint files will always be loaded safely.
Total VRAM 16368 MB, total RAM 64199 MB
pytorch version: 2.8.0.dev20250418+rocm6.4
AMD arch: gfx1100
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon Graphics : hipMallocAsync
Traceback (most recent call last):
  File "/home/markus/code/docker/sd-rocm/data/home-local/comfyui/main.py", line 137, in <module>
    import execution
  File "/home/markus/code/docker/sd-rocm/data/home-local/comfyui/execution.py", line 13, in <module>
    import nodes
  File "/home/markus/code/docker/sd-rocm/data/home-local/comfyui/nodes.py", line 22, in <module>
    import comfy.diffusers_load
  File "/home/markus/code/docker/sd-rocm/data/home-local/comfyui/comfy/diffusers_load.py", line 3, in <module>
    import comfy.sd
  File "/home/markus/code/docker/sd-rocm/data/home-local/comfyui/comfy/sd.py", line 13, in <module>
    import comfy.ldm.genmo.vae.model
  File "/home/markus/code/docker/sd-rocm/data/home-local/comfyui/comfy/ldm/genmo/vae/model.py", line 13, in <module>
    from comfy.ldm.modules.attention import optimized_attention
  File "/home/markus/code/docker/sd-rocm/data/home-local/comfyui/comfy/ldm/modules/attention.py", line 29, in <module>
    from flash_attn import flash_attn_func
  File "/home/markus/code/docker/sd-rocm/data/home-local/flash-attention/flash_attn/__init__.py", line 3, in <module>
    from flash_attn.flash_attn_interface import (
  File "/home/markus/code/docker/sd-rocm/data/home-local/flash-attention/flash_attn/flash_attn_interface.py", line 13, in <module>
    from .flash_attn_triton_amd import interface_fa as flash_attn_gpu
  File "/home/markus/code/docker/sd-rocm/data/home-local/flash-attention/flash_attn/flash_attn_triton_amd/interface_fa.py", line 3, in <module>
    from .fwd_prefill import attention_prefill_forward_triton_impl
  File "/home/markus/code/docker/sd-rocm/data/home-local/flash-attention/flash_attn/flash_attn_triton_amd/fwd_prefill.py", line 2, in <module>
    import triton
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/__init__.py", line 8, in <module>
    from .runtime import (
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/runtime/__init__.py", line 1, in <module>
    from .autotuner import (Autotuner, Config, Heuristics, autotune, heuristics)
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/runtime/autotuner.py", line 9, in <module>
    from .jit import KernelInterface
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/runtime/jit.py", line 12, in <module>
    from ..runtime.driver import driver
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/runtime/driver.py", line 1, in <module>
    from ..backends import backends
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/backends/__init__.py", line 50, in <module>
    backends = _discover_backends()
               ^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/backends/__init__.py", line 43, in _discover_backends
    compiler = _load_module(name, os.path.join(root, name, 'compiler.py'))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/backends/__init__.py", line 12, in _load_module
    spec.loader.exec_module(module)
  File "/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/backends/intel/compiler.py", line 2, in <module>
    from triton._C.libtriton import ir, passes, llvm, intel
ImportError: cannot import name 'intel' from 'triton._C.libtriton' (/home/markus/code/docker/sd-rocm/data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/_C/libtriton.so
```

---

## 评论 (2 条)

### 评论 #1 — hartmark (2025-04-29T01:42:05Z)

Got it working!!

Use this _discover_backends implementation instead in:

`./data/home-local/venv-local-comfyui-3.12/lib/python3.12/site-packages/triton/backends/__init__.py`

This is in the triton-package.

```
def _discover_backends():
    backends = dict()
    root = os.path.dirname(__file__)
    print(f"DEBUG: Looking for backends in {os.path.dirname(__file__)}")
    for name in os.listdir(root):
        if not os.path.isdir(os.path.join(root, name)):
            continue
        if name.startswith('__'):
            continue

        print(f"DEBUG: Found backend '{name}'")
        if name == 'intel':
            continue

        compiler = _load_module(name, os.path.join(root, name, 'compiler.py'))
        driver = _load_module(name, os.path.join(root, name, 'driver.py'))
        backends[name] = Backend(_find_concrete_subclasses(compiler, BaseBackend),
                                 _find_concrete_subclasses(driver, DriverBase))
    return backends
```

---

### 评论 #2 — hartmark (2025-04-29T22:45:48Z)

The issue was that the __init__.py in the backends folder iterates all subfolders of it, and I tried grepping for the linux folder in all wheels I had in my cache but none seemed to have been putting in the intel folder.

I did a complete nuke of my venv and installed all packages  from scratch, it seems to be working properly now.

---
