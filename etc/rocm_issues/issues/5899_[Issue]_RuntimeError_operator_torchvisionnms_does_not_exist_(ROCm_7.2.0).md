# [Issue]: RuntimeError: operator torchvision::nms does not exist (ROCm 7.2.0)

> **Issue #5899**
> **状态**: closed
> **创建时间**: 2026-01-24T05:35:13Z
> **更新时间**: 2026-01-26T22:13:30Z
> **关闭时间**: 2026-01-26T22:13:30Z
> **作者**: osirisOfGit
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5899

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Hello!
Upgraded my ROCm to 7.2.0 today from 7.1.1 - followed uninstall steps, followed by install, but now running into the below when running [ComfyUI](https://github.com/Comfy-Org/ComfyUI) (currently on 0.10.0 but wasn't working on 0.9.2 either). Reporting here as the error is originating from an interaction between torch and torchvision

```
Traceback (most recent call last):
  File "/mnt/mydrive/Coding/../models/comfy-ui/ComfyUI/main.py", line 178, in <module>
    import execution
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/execution.py", line 16, in <module>
    from latent_preview import set_preview_method
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/latent_preview.py", line 5, in <module>
    from comfy.sd import VAE
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/comfy/sd.py", line 11, in <module>
    from .ldm.cascade.stage_c_coder import StageC_coder
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/comfy/ldm/cascade/stage_c_coder.py", line 19, in <module>
    import torchvision
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torchvision/__init__.py", line 10, in <module>
    from torchvision import _meta_registrations, datasets, io, models, ops, transforms, utils  # usort:skip
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torchvision/_meta_registrations.py", line 163, in <module>
    @torch.library.register_fake("torchvision::nms")
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torch/library.py", line 1062, in register
    use_lib._register_fake(
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torch/library.py", line 210, in _register_fake
    handle = entry.fake_impl.register(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torch/_library/fake_impl.py", line 50, in register
    if torch._C._dispatch_has_kernel_for_dispatch_key(self.qualname, "Meta"):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: operator torchvision::nms does not exist
```

<details>
<summary> Complete section </summary>

```
source $CODING_HOME/../models/comfy-ui/venv-linux/bin/activate && python3 $CODING_HOME/../models/comfy-ui/ComfyUI/main.py --use-pytorch-cross-attention --preview-method auto

[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** ComfyUI startup time: 2026-01-23 23:15:24.626
** Platform: Linux
** Python version: 3.12.3 (main, Jan  8 2026, 11:30:50) [GCC 13.3.0]
** Python executable: /mnt/mydrive/models/comfy-ui/venv-linux/bin/python3
** ComfyUI Path: /mnt/mydrive/models/comfy-ui/ComfyUI
** ComfyUI Base Folder Path: /mnt/mydrive/models/comfy-ui/ComfyUI
** User directory: /mnt/mydrive/models/comfy-ui/ComfyUI/user
** ComfyUI-Manager config path: /mnt/mydrive/models/comfy-ui/ComfyUI/user/__manager/config.ini
** Log path: /mnt/mydrive/models/comfy-ui/ComfyUI/user/comfyui.log

Prestartup times for custom nodes:
   0.9 seconds: /mnt/mydrive/models/comfy-ui/ComfyUI/custom_nodes/comfyui-manager

Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 61897 MB
pytorch version: 2.9.1+rocm7.2.0.git7e1940d4
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1201
ROCm version: (7, 2)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Using async weight offloading with 2 streams
Enabled pinned memory 58802.0
Found comfy_kitchen backend eager: {'available': True, 'disabled': False, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Found comfy_kitchen backend cuda: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Found comfy_kitchen backend triton: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Traceback (most recent call last):
  File "/mnt/mydrive/Coding/../models/comfy-ui/ComfyUI/main.py", line 178, in <module>
    import execution
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/execution.py", line 16, in <module>
    from latent_preview import set_preview_method
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/latent_preview.py", line 5, in <module>
    from comfy.sd import VAE
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/comfy/sd.py", line 11, in <module>
    from .ldm.cascade.stage_c_coder import StageC_coder
  File "/mnt/mydrive/models/comfy-ui/ComfyUI/comfy/ldm/cascade/stage_c_coder.py", line 19, in <module>
    import torchvision
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torchvision/__init__.py", line 10, in <module>
    from torchvision import _meta_registrations, datasets, io, models, ops, transforms, utils  # usort:skip
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torchvision/_meta_registrations.py", line 163, in <module>
    @torch.library.register_fake("torchvision::nms")
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torch/library.py", line 1062, in register
    use_lib._register_fake(
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torch/library.py", line 210, in _register_fake
    handle = entry.fake_impl.register(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/mydrive/models/comfy-ui/venv-linux/lib/python3.12/site-packages/torch/_library/fake_impl.py", line 50, in register
    if torch._C._dispatch_has_kernel_for_dispatch_key(self.qualname, "Meta"):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: operator torchvision::nms does not exist
```

</details>

I followed the following sections on https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/howto_native_linux.html (non-docker instructions on each): 

1. ROCm
1. PyTorch
1. ONNX
1. Triton
1. MIGraphX

All the validation steps are providing the expected output, except for ONNX:

```
❯ python3 -c "import onnxruntime as ort; print(ort.get_available_providers())"
['MIGraphXExecutionProvider', 'CPUExecutionProvider']
```

Unsure if this is related.

<details>
<summary> Installed PIP Packages </summary>

```
❯ pip list 
Package                                Version
-------------------------------------- ------------------------------
aiofiles                               24.1.0
aiohappyeyeballs                       2.6.1
aiohttp                                3.13.3
aiohttp_socks                          0.11.0
aiosignal                              1.4.0
alembic                                1.18.1
annotated-types                        0.7.0
attrs                                  25.4.0
av                                     16.1.0
certifi                                2026.1.4
cffi                                   2.0.0
chardet                                5.2.0
charset-normalizer                     3.4.4
click                                  8.3.1
coloredlogs                            15.0.1
comfy-kitchen                          0.2.7
comfyui-embedded-docs                  0.4.0
comfyui_frontend_package               1.36.14
comfyui_workflow_templates             0.8.14
comfyui-workflow-templates-core        0.3.100
comfyui-workflow-templates-media-api   0.3.44
comfyui-workflow-templates-media-image 0.3.66
comfyui-workflow-templates-media-other 0.3.87
comfyui-workflow-templates-media-video 0.3.39
contourpy                              1.3.3
cryptography                           46.0.3
cycler                                 0.12.1
einops                                 0.8.1
filelock                               3.20.3
flatbuffers                            25.12.19
fonttools                              4.61.1
frozenlist                             1.8.0
fsspec                                 2026.1.0
gitdb                                  4.0.12
GitPython                              3.1.46
greenlet                               3.3.1
h11                                    0.16.0
h2                                     4.3.0
hf-xet                                 1.2.0
hpack                                  4.1.0
huggingface-hub                        0.36.0
humanfriendly                          10.0
hyperframe                             6.1.0
idna                                   3.11
Jinja2                                 3.1.6
jsonschema                             4.26.0
jsonschema-specifications              2025.9.1
kiwisolver                             1.4.9
kornia                                 0.8.2
kornia_rs                              0.1.10
Mako                                   1.3.10
markdown-it-py                         4.0.0
MarkupSafe                             3.0.3
matplotlib                             3.10.8
matrix-nio                             0.25.2
mdurl                                  0.1.2
mpmath                                 1.3.0
multidict                              6.7.0
networkx                               3.6.1
numpy                                  1.26.4
onnxruntime-migraphx                   1.23.2
packaging                              26.0
pandas                                 3.0.0
pillow                                 12.1.0
pip                                    25.3
propcache                              0.4.1
protobuf                               6.33.4
psutil                                 7.2.1
pycparser                              3.0
pycryptodome                           3.23.0
pydantic                               2.12.5
pydantic_core                          2.41.5
pydantic-settings                      2.12.0
PyGithub                               2.8.1
Pygments                               2.19.2
PyJWT                                  2.10.1
PyNaCl                                 1.6.2
pyparsing                              3.3.2
python-dateutil                        2.9.0.post0
python-dotenv                          1.2.1
python-socks                           2.8.0
PyYAML                                 6.0.3
referencing                            0.37.0
regex                                  2026.1.15
requests                               2.32.5
rich                                   14.2.0
rpds-py                                0.30.0
safetensors                            0.7.0
scipy                                  1.17.0
sentencepiece                          0.2.1
setuptools                             80.10.1
shellingham                            1.5.4
six                                    1.17.0
smmap                                  5.0.2
spandrel                               0.4.1
SQLAlchemy                             2.0.46
sympy                                  1.14.0
tabulate                               0.9.0
tokenizers                             0.22.2
toml                                   0.10.2
torch                                  2.9.1+rocm7.2.0.lw.git7e1940d4
torch_migraphx                         1.1
torchaudio                             2.9.0+rocm7.2.0.gite3c6ee2b
torchsde                               0.2.6
torchvision                            0.25.0+rocm7.2.0.gitaa35ca19
tqdm                                   4.67.1
trampoline                             0.1.2
transformers                           4.57.6
triton                                 3.5.1+rocm7.2.0.gita272dfa8
typer                                  0.21.1
typing_extensions                      4.15.0
typing-inspection                      0.4.2
unpaddedbase64                         2.1.0
urllib3                                2.6.3
uv                                     0.9.26
wheel                                  0.46.3
yarl                                   1.22.0
```

(I manually downgraded numpy for better compatibility with a variety of Comfy customNodes, but the error was happening using the default version too)

</details>

Let me know if there's any more information i can provide, or if i should take my report elsewhere. Thanks in advance

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 7 9800X3D 8-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
❯ /opt/rocm/bin/rocminfo --support
ROCk module version 6.16.13 is loaded
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

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 9800X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 9800X3D 8-Core Processor
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5271                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    63382676(0x3c72494) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    63382676(0x3c72494) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    63382676(0x3c72494) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    63382676(0x3c72494) KB             
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
  Uuid:                    GPU-ce1b043aff2a2d99               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2520                               
  BDFID:                   768                                
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
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5056(0x13c0)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   31744                              
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
  Packet Processor uCode:: 121                                
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31691336(0x1e39248) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31691336(0x1e39248) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic 
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
```

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — osirisOfGit (2026-01-24T06:05:18Z)

oh, and i did end up purging and recreating my venv during setup - i had it in the comfyUI repo dir originally, so i had to delete it and recreate it a level up, so there shouldn't be any litter in it

---

### 评论 #2 — techbotgoku (2026-01-24T08:00:29Z)

https://github.com/ROCm/ROCm/issues/5897#issuecomment-3794164361

I'm guessing you installed from [Install PyTorch for ROCm](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html ).

If yes, I think there are issues with pytorch-0.25.0

Fix:

1. Uninstall torchvision:
```
pip3 uninstall torchvision
```

2. Download and install tochvision compatible with rocm 7.2
```
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchvision-0.24.0%2Brocm7.2.0.gitb919bd0c-cp312-cp312-linux_x86_64.whl
pip3 install torchvision-0.24.0+rocm7.2.0.gitb919bd0c-cp312-cp312-linux_x86_64.whl
```

---

### 评论 #3 — osirisOfGit (2026-01-24T16:46:54Z)

That worked!! Thanks a ton - should i close this issue in favour of the other one?

---

### 评论 #4 — rafavcc (2026-01-25T18:51:00Z)

Great solution! I got this error too. We should warn @AMDGithubSCIMAdmin ?

---

### 评论 #5 — harkgill-amd (2026-01-26T15:57:45Z)

Hey @osirisOfGit and @techbotgoku, thanks for the report and subsequent workaround! 

Will dig a little deeper into what's going wrong with `torchvision-0.25.0` but we should have some changes in by the end of day to make sure users don't get blocked by this going forward.

---

### 评论 #6 — harkgill-amd (2026-01-26T22:13:30Z)

https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html#option-a-pytorch-via-pip-installation has been updated to correctly point to the `torchvision-0.24.0` wheels. Thanks again for the help on this one!

---
