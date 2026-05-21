# RuntimeError: HIP error: invalid device function - if there is a solution already existed against this issue.

> **Issue #2536**
> **状态**: closed
> **创建时间**: 2023-10-10T15:15:29Z
> **更新时间**: 2025-11-26T23:13:29Z
> **关闭时间**: 2024-07-02T14:41:14Z
> **作者**: Bear-Beer
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2536

## 描述

Server： (Inspur NF5280A6) + (2 x Milan7453) + (16Dimm * 32GB-3200) 
GPU：    83:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 22 [Radeon RX 6700/6700 XT/6750 XT / 6800M/6850M XT] (rev c1)
OS：      Centos Steam9.2， kernel：5.14.0-373.el9.x86_64
ROCm：5.7
Pytorch installation cmd：pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm5.7

[root@6700xt ~]# dkms status
amdgpu/6.2.4-1652687.el9, 5.14.0-373.el9.x86_64, x86_64: installed (original_module exists)
[root@6700xt ~]#

_ipython interaction_
```
In [1]: import torch

In [2]: torch.__version__
Out[2]: '2.2.0.dev20231010+rocm5.7'

In [3]: torch.cuda.is_available()
Out[3]: True

In [4]: torch.cuda.device_count()
Out[4]: 1

In [5]: torch.cuda.current_device()
Out[5]: 0

In [6]: torch.cuda.get_device_name(torch.cuda.current_device())
Out[6]: 'AMD Radeon RX 6700 XT'

In [7]: device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

In [8]: device
Out[8]: device(type='cuda')

In [9]: torch.rand(3, 3).to(device)
Out[9]: ---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
File /usr/local/lib/python3.9/site-packages/IPython/core/formatters.py:708, in PlainTextFormatter.__call__(self, obj)
    701 stream = StringIO()
    702 printer = pretty.RepresentationPrinter(stream, self.verbose,
    703     self.max_width, self.newline,
    704     max_seq_length=self.max_seq_length,
    705     singleton_pprinters=self.singleton_printers,
    706     type_pprinters=self.type_printers,
    707     deferred_pprinters=self.deferred_printers)
--> 708 printer.pretty(obj)
    709 printer.flush()
    710 return stream.getvalue()

File /usr/local/lib/python3.9/site-packages/IPython/lib/pretty.py:410, in RepresentationPrinter.pretty(self, obj)
    407                         return meth(obj, self, cycle)
    408                 if cls is not object \
    409                         and callable(cls.__dict__.get('__repr__')):
--> 410                     return _repr_pprint(obj, self, cycle)
    412     return _default_pprint(obj, self, cycle)
    413 finally:

File /usr/local/lib/python3.9/site-packages/IPython/lib/pretty.py:778, in _repr_pprint(obj, p, cycle)
    776 """A pprint that just redirects to the normal repr function."""
    777 # Find newlines and replace them with p.break_()
--> 778 output = repr(obj)
    779 lines = output.splitlines()
    780 with p.group():

File /usr/local/lib64/python3.9/site-packages/torch/_tensor.py:442, in Tensor.__repr__(self, tensor_contents)
    438     return handle_torch_function(
    439         Tensor.__repr__, (self,), self, tensor_contents=tensor_contents
    440     )
    441 # All strings are unicode in Python 3.
--> 442 return torch._tensor_str._str(self, tensor_contents=tensor_contents)

File /usr/local/lib64/python3.9/site-packages/torch/_tensor_str.py:664, in _str(self, tensor_contents)
    662 with torch.no_grad(), torch.utils._python_dispatch._disable_current_modes():
    663     guard = torch._C._DisableFuncTorch()
--> 664     return _str_intern(self, tensor_contents=tensor_contents)

File /usr/local/lib64/python3.9/site-packages/torch/_tensor_str.py:595, in _str_intern(inp, tensor_contents)
    593                     tensor_str = _tensor_str(self.to_dense(), indent)
    594                 else:
--> 595                     tensor_str = _tensor_str(self, indent)
    597 if self.layout != torch.strided:
    598     suffixes.append("layout=" + str(self.layout))

File /usr/local/lib64/python3.9/site-packages/torch/_tensor_str.py:347, in _tensor_str(self, indent)
    343     return _tensor_str_with_formatter(
    344         self, indent, summarize, real_formatter, imag_formatter
    345     )
    346 else:
--> 347     formatter = _Formatter(get_summarized_data(self) if summarize else self)
    348     return _tensor_str_with_formatter(self, indent, summarize, formatter)

File /usr/local/lib64/python3.9/site-packages/torch/_tensor_str.py:138, in _Formatter.__init__(self, tensor)
    134         self.max_width = max(self.max_width, len(value_str))
    136 else:
    137     nonzero_finite_vals = torch.masked_select(
--> 138         tensor_view, torch.isfinite(tensor_view) & tensor_view.ne(0)
    139     )
    141     if nonzero_finite_vals.numel() == 0:
    142         # no valid number, do nothing
    143         return

**RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.**


In [10]:
```

---

## 评论 (48 条)

### 评论 #1 — briansp2020 (2023-10-10T15:23:41Z)

Did you try?
>export PYTORCH_ROCM_ARCH="gfx1031"
export HSA_OVERRIDE_GFX_VERSION=10.3.1
export HIP_VISIBLE_DEVICES=0
export ROCM_PATH=/opt/rocm

If not, try each one separate and some combination of them.

---

### 评论 #2 — briansp2020 (2023-10-10T15:25:48Z)

Also, what CPU and motherboard are you using?

---

### 评论 #3 — Bear-Beer (2023-10-11T02:19:30Z)

Thank you for your help @briansp2020 
I am a newbie for ROCm and Pytorch, I was wondering if there are some other approaches to do the verification about HIP? 

The environment variables do not work for me. there is no difference in the result. 

I updated the other information in the description.

---

### 评论 #4 — briansp2020 (2023-10-11T03:06:30Z)

This may or may not help. But does rocminfo and rocm-smi show any information about the gpu?
If you are a beginner, it's better to stick to a supported OS. According to the documentation ([here](https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html)), Ubuntu, RHEL & SLES are supported. So, you might want to try one of them unless you have to use Centos Stream. If you have to use Centos Stream, you might want to ask for help from Centos Stream forums.

---

### 评论 #5 — Bear-Beer (2023-10-11T04:41:19Z)

Yes. rocminfo and rocm-smi are all work for me. 
```
[root@6700xt ~]# rocminfo
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD EPYC 7453 28-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7453 28-Core Processor
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
  Max Clock Freq. (MHz):   2750
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            56
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    263265012(0xfb11af4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    263265012(0xfb11af4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    263265012(0xfb11af4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    AMD EPYC 7453 28-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7453 28-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2750
  BDFID:                   0
  Internal Node ID:        1
  Compute Unit:            56
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    264193024(0xfbf4400) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    264193024(0xfbf4400) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    264193024(0xfbf4400) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 3
*******
  Name:                    gfx1031
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon RX 6700 XT
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
    L2:                      3072(0xc00) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29663(0x73df)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2855
  BDFID:                   33536
  Internal Node ID:        2
  Compute Unit:            40
  SIMDs per CU:            2
  Shader Engines:          2
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
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
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 115
  SDMA engine uCode::      80
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    12566528(0xbfc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS:
      Size:                    12566528(0xbfc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1031
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***
[root@6700xt ~]# rocm-smi


========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU  Temp (DieEdge)  AvgPwr  SCLK     MCLK   Fan  Perf  PwrCap  VRAM%  GPU%
0    36.0c           29.0W   2650Mhz  96Mhz  0%   auto  186.0W   14%   99%
====================================================================================
=============================== End of ROCm SMI Log ================================
[root@6700xt ~]#
```



---

### 评论 #6 — Bear-Beer (2023-10-11T04:46:26Z)

I found that the below codes works on my env:
```
from transformers import *
pipe = pipeline("translation", model="/home/AiModels/Helsinki-NLP/opus-mt-en-zh/")
pipe("I am Bear, Bear likes Beer")
```

But The codes failed with the same signature with GPU device
```
from transformers import *
pipe = pipeline("translation", model="/home/AiModels/Helsinki-NLP/opus-mt-en-zh/", device=0)
pipe("I am Bear, Bear likes Beer")

---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
/home/SourceCode/vscode/examples/01-pipeline/pipeline.ipynb Cell 4 line 3
      1 from transformers import *
      2 pipe = pipeline("translation", model="/home/AiModels/Helsinki-NLP/opus-mt-en-zh/", device=0)
----> 3 pipe("I am Bear, Bear likes Beer")

File /usr/local/lib/python3.9/site-packages/transformers/pipelines/text2text_generation.py:371, in TranslationPipeline.__call__(self, *args, **kwargs)
    341 def __call__(self, *args, **kwargs):
    342     r"""
    343     Translate the text(s) given as inputs.
    344 
   (...)
    369           token ids of the translation.
    370     """
--> 371     return super().__call__(*args, **kwargs)

File /usr/local/lib/python3.9/site-packages/transformers/pipelines/text2text_generation.py:167, in Text2TextGenerationPipeline.__call__(self, *args, **kwargs)
    138 def __call__(self, *args, **kwargs):
    139     r"""
    140     Generate the output text(s) using text(s) given as inputs.
    141 
   (...)
    164           ids of the generated text.
    165     """
...
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
```

---

### 评论 #7 — RawEnchilada (2023-10-21T10:27:26Z)

I am running into the same "HIP error: invalid device function" while trying to train a model.
[This ROCm test script](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533) says that everything should be working. Also environment variables are set accordingly.
Any ideas?

---

### 评论 #8 — plane714 (2023-10-26T07:33:39Z)

system:ubuntu22.04
python:3.11.5
rocm:5.7.1
torch:2.2.0+rocm5.7-cp11-cp11 version10.25
torchvision: version10.25

I download .whl from pytorch official website,and create a conda environment.
because of the dependence error,I install torch.whl without depends,and install needed dependence seperatly.


torch.cuda.is_available()=Ture

but when I create tensor,it crash.

error is same as you:

RuntimeError: HIP error: invalid device function HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect. For debugging consider passing HIP_LAUNCH_BLOCKING=1. Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.



---

### 评论 #9 — trougnouf (2023-11-02T12:33:15Z)

Some issue with Arch Linux, rocm5.7.1 and 5.7.0 (from AUR = Ubuntu package), PyTorch 2.0.1, python 3.11.5, RX 6700S.
I can reproduce with `torch.ones(2).to(torch.device(0))` or  `torch.ones(2).to(torch.device(1))`

edit: it works with `HSA_OVERRIDE_GFX_VERSION=10.3.0 python`

<details>
<summary>here is my rocminfo output:</summary>

```bash

[trougnouf@l rocm570]$ /opt/rocm/bin/rocminfo 
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 9 6900HS with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 6900HS with Radeon Graphics
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
  Max Clock Freq. (MHz):   4935                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    40277244(0x26694fc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    40277244(0x26694fc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    40277244(0x26694fc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1032                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 6700S                
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
    L1:                      16(0x10) KB                        
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 29679(0x73ef)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2435                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            28                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 109                                
  SDMA engine uCode::      76                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1032         
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 3                  
*******                  
  Name:                    gfx1035                            
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 5761(0x1681)                       
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2400                               
  BDFID:                   1792                               
  Internal Node ID:        2                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 113                                
  SDMA engine uCode::      37                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1035         
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***             
```

</details>

---

### 评论 #10 — yxsamliu (2023-11-02T13:32:08Z)

can you set env var AMD_LOG_LEVEL=3 and run the test. This will trace HIP API's and may provide more information about what causes the failure.

---

### 评论 #11 — trougnouf (2023-11-02T13:59:55Z)

> can you set env var AMD_LOG_LEVEL=3 and run the test. This will trace HIP API's and may provide more information about what causes the failure.

Yes.
`[trougnouf@l ~]$ echo "import torch; print(torch.ones(2).cuda())" > tmp/atest.py`

`[trougnouf@l ~]$ AMD_LOG_LEVEL=3 python tmp/atest.py &> tmp/hsa_default.log`: https://gist.github.com/trougnouf/d952aacf76f1630a95c4d5427abffbc4
`[trougnouf@l ~]$ AMD_LOG_LEVEL=3 HSA_OVERRIDE_GFX_VERSION=10.3.0 python tmp/atest.py &> tmp/hsa_override.log`: https://gist.github.com/trougnouf/86313c04cecad89b5cdb8ee67f1a7973

---

### 评论 #12 — yxsamliu (2023-11-02T14:45:13Z)

It seems  your devices are gfx1032 and gfx1035 but PyTorch is not compiled for them. When you use HSA_OVERRIDE_GFX_VERSION=10.3.0 you tell ROCm to report the devices as gfx1030, which is what PyTorch compiled for.

---

### 评论 #13 — Aldrog (2023-11-17T22:55:13Z)

Setting `HSA_OVERRIDE_GFX_VERSION=11.0.0` fixed this issue for me when running on gfx1100. I also have integrated graphics (reported as gfx1036 in rocminfo) which might be the reason for this bug to trigger.

UPD: it fixed `HIP error: invalid device function` and made some of the pytorch examples run successfully but others are now hanging indefinitely until a hard reboot (killing a process leaves GPU with 100% load).

---

### 评论 #14 — Cheese-shrimp (2024-01-09T16:05:48Z)




> Did you try?
> 
> > export PYTORCH_ROCM_ARCH="gfx1031"
> > export HSA_OVERRIDE_GFX_VERSION=10.3.1
> > export HIP_VISIBLE_DEVICES=0
> > export ROCM_PATH=/opt/rocm
> 
> If not, try each one separate and some combination of them.

Thanks this worked for me, I modified the following:
export PYTORCH_ROCM_ARCH="gfx1031"
export HSA_OVERRIDE_GFX_VERSION=10.3.0
My configuration is: 6750GRE 12G

---

### 评论 #15 — Dlinuigh (2024-01-22T04:26:03Z)

I solved this problem by set the environment in virtual env activate file. For it always excludes system bashrc

---

### 评论 #16 — Admyfast (2024-01-27T18:50:58Z)

Greetings, dear ones! I've been struggling with this error for a week now. Please help. Don't scold me too much, I'm just starting to get acquainted with Linux. When launching Stable Diffusion - Error text:

Traceback (most recent call last):
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/threading.py", line 973, in _bootstrap
    self._bootstrap_inner()
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
    self.run()
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/threading.py", line 953, in run
    self._target(*self._args, **self._kwargs)
  File "/home/sd/stable-diffusion-webui/modules/initialize.py", line 147, in load_model
    shared.sd_model  # noqa: B018
  File "/home/sd/stable-diffusion-webui/modules/shared_items.py", line 128, in sd_model
    return modules.sd_models.model_data.get_sd_model()
  File "/home/sd/stable-diffusion-webui/modules/sd_models.py", line 531, in get_sd_model
    load_model()
  File "/home/sd/stable-diffusion-webui/modules/sd_models.py", line 658, in load_model
    load_model_weights(sd_model, checkpoint_info, state_dict, timer)
  File "/home/sd/stable-diffusion-webui/modules/sd_models.py", line 385, in load_model_weights
    model.float()
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/site-packages/lightning_fabric/utilities/device_dtype_mixin.py", line 88, in float
    return super().float()
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/site-packages/torch/nn/modules/module.py", line 992, in float
    return self._apply(lambda t: t.float() if t.is_floating_point() else t)
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/site-packages/torch/nn/modules/module.py", line 810, in _apply
    module._apply(fn)
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/site-packages/torch/nn/modules/module.py", line 810, in _apply
    module._apply(fn)
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/site-packages/torch/nn/modules/module.py", line 810, in _apply
    module._apply(fn)
  [Previous line repeated 1 more time]
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/site-packages/torch/nn/modules/module.py", line 833, in _apply
    param_applied = fn(param)
  File "/home/sd/miniconda3/envs/amd/lib/python3.10/site-packages/torch/nn/modules/module.py", line 992, in <lambda>
    return self._apply(lambda t: t.float() if t.is_floating_point() else t)
RuntimeError: HIP error: the operation cannot be performed in the present state
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

#################################################

Now I’ll show you what I have installed:
1.Operating System:
  x86_64
  DISTRIB_ID=Ubuntu
  DISTRIB_RELEASE=22.04
  DISTRIB_CODENAME=jammy
  DISTRIB_DESCRIPTION="Ubuntu 22.04.3 LTS"
  PRETTY_NAME="Ubuntu 22.04.3 LTS"
___________________________________

2. Core:
  Linux 6.2.0-26-generic #26~22.04.1-Ubuntu 
  
3. File settings "~/.bashrc"
  export HIP_LAUNCH_BLOCKING=1
  export HIP_VISIBLE_DEVICES=0
  export PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:512
  
4. Launch through the minikonda virtual environment:
  HSA_OVERRIDE_GFX_VERSION=10.3.0 python3 launch.py --listen --enable-insecure-extension-access --opt-sdp-attention --no-half-vae 
  
 
3. ROCk module is loaded
  =====================    
  HSA System Attributes    
  =====================    
  Runtime Version:         1.1
  System Timestamp Freq.:  1000.000000MHz
  Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
  Machine Model:           LARGE                              
  System Endianness:       LITTLE                             
  Mwaitx:                  DISABLED
  DMAbuf Support:          YES
  
  ==========               
  HSA Agents               
  ==========               
  *******                  
  Agent 1                  
  *******                  
    Name:                    AMD A8-5600K APU with Radeon(tm) HD Graphics
    Uuid:                    CPU-XX                             
    Marketing Name:          AMD A8-5600K APU with Radeon(tm) HD Graphics
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
      L1:                      16384(0x4000) KB                   
    Chip ID:                 0(0x0)                             
    ASIC Revision:           0(0x0)                             
    Cacheline Size:          64(0x40)                           
    Max Clock Freq. (MHz):   3600                               
    BDFID:                   0                                  
    Internal Node ID:        0                                  
    Compute Unit:            4                                  
    SIMDs per CU:            0                                  
    Shader Engines:          0                                  
    Shader Arrs. per Eng.:   0                                  
    WatchPts on Addr. Ranges:1                                  
    Features:                None
    Pool Info:               
      Pool 1                   
        Segment:                 GLOBAL; FLAGS: FINE GRAINED        
        Size:                    32819336(0x1f4c888) KB             
        Allocatable:             TRUE                               
        Alloc Granule:           4KB                                
        Alloc Alignment:         4KB                                
        Accessible by all:       TRUE                               
      Pool 2                   
        Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
        Size:                    32819336(0x1f4c888) KB             
        Allocatable:             TRUE                               
        Alloc Granule:           4KB                                
        Alloc Alignment:         4KB                                
        Accessible by all:       TRUE                               
      Pool 3                   
        Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
        Size:                    32819336(0x1f4c888) KB             
        Allocatable:             TRUE                               
        Alloc Granule:           4KB                                
        Alloc Alignment:         4KB                                
        Accessible by all:       TRUE                               
    ISA Info:                
  *******                  
  Agent 2                  
  *******                  
    Name:                    gfx1030                            
    Uuid:                    GPU-3f336d78b9266872               
    Marketing Name:          AMD Radeon RX 6800 XT              
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
      L1:                      16(0x10) KB                        
      L2:                      4096(0x1000) KB                    
      L3:                      131072(0x20000) KB                 
    Chip ID:                 29631(0x73bf)                      
    ASIC Revision:           1(0x1)                             
    Cacheline Size:          64(0x40)                           
    Max Clock Freq. (MHz):   2575                               
    BDFID:                   768                                
    Internal Node ID:        1                                  
    Compute Unit:            72                                 
    SIMDs per CU:            2                                  
    Shader Engines:          4                                  
    Shader Arrs. per Eng.:   2                                  
    WatchPts on Addr. Ranges:4                                  
    Coherent Host Access:    FALSE                              
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
      x                        4294967295(0xffffffff)             
      y                        4294967295(0xffffffff)             
      z                        4294967295(0xffffffff)             
    Max fbarriers/Workgrp:   32                                 
    Packet Processor uCode:: 116                                
    SDMA engine uCode::      83                                 
    IOMMU Support::          None                               
    Pool Info:               
      Pool 1                   
        Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
        Size:                    16760832(0xffc000) KB              
        Allocatable:             TRUE                               
        Alloc Granule:           4KB                                
        Alloc Alignment:         4KB                                
        Accessible by all:       FALSE                              
      Pool 2                   
        Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
        Size:                    16760832(0xffc000) KB              
        Allocatable:             TRUE                               
        Alloc Granule:           4KB                                
        Alloc Alignment:         4KB                                
        Accessible by all:       FALSE                              
      Pool 3                   
        Segment:                 GROUP                              
        Size:                    64(0x40) KB                        
        Allocatable:             FALSE                              
        Alloc Granule:           0KB                                
        Alloc Alignment:         0KB                                
        Accessible by all:       FALSE                              
    ISA Info:                
      ISA 1                    
        Name:                    amdgcn-amd-amdhsa--gfx1030         
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
          x                        4294967295(0xffffffff)             
          y                        4294967295(0xffffffff)             
          z                        4294967295(0xffffffff)             
        FBarrier Max Size:       32                                 
  *** Done ***




---

### 评论 #17 — cgmb (2024-02-01T19:52:12Z)

@Admyfast, I believe that the ROCm minimum system requirements include PCIe 3.0 or greater. I'm not sure if that's the cause of your problem, but that's one thing that stood out to me when looking at your logs.

You may also want to set  [`ROCR_VISIBLE_DEVICES`](https://rocm.docs.amd.com/en/docs-6.0.2/conceptual/gpu-isolation.html#rocr-visible-devices) to hide the integrated graphics from the ROCm stack.

---

### 评论 #18 — plane714 (2024-02-28T13:41:20Z)

I tried rocm5.7 at 2023.10, and gave up because I counld't solve HIP error: invalid device function.Recently, I installed ubuntu22.04.04 and rocm6.0.2.I can run stable diffusion webui successfully on my 6700xt. However, when I excuted pytorch code, I still met HIP error: invalid device function.    

P.S.I have added code in terminal as follows
export PYTORCH_ROCM_ARCH="gfx1031"
export HSA_OVERRIDE_GFX_VERSION=10.3.1
export HIP_VISIBLE_DEVICES=0
export ROCM_PATH=/opt/rocm

God,who can help me!!! I don't hope switching to nvidia graphic card is my final solution.

---

### 评论 #19 — cocoderss (2024-03-02T10:10:12Z)

> God,who can help me!!! I don't hope switching to nvidia graphic card is my final solution.

AMD hyped up all the AI base about ROCm being a serious solution and competitor to CUDA, the reality is, it's far from the truth. I go from one issue to another, each step is a minor victory but then you hit another blockade, which is frustrating. Truth of the matter, ROCm is not production ready. 


---

### 评论 #20 — Lumpus99 (2024-03-11T20:05:12Z)

> I solved this problem by set the environment in virtual env activate file. For it always excludes system bashrc

This solved the issue for me. For anyone using Pycharm, try adding the environment variables to Pycharm. Here's a link explaining how to do this:
https://stackoverflow.com/questions/42708389/how-to-set-environment-variables-in-pycharm

---

### 评论 #21 — supersonictw (2024-03-28T12:15:49Z)

Just need to put

```py
from os import putenv
putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0")
```

on the top of your codes.

It's dirty, but it's working.

![codes](https://github.com/ROCm/ROCm/assets/13705584/c3e96b08-f82a-4e8c-8031-df562a2d0820)

The reason might be your interpreter runtime didn't use your system variables.

Force to inject `HSA_OVERRIDE_GFX_VERSION` on the runtime, it will work.

---

### 评论 #22 — plane714 (2024-03-30T13:23:18Z)

> The reason might be your interpreter runtime didn't use your system variables.\n\nForce to inject HSA_OVERRIDE_GFX_VERSION on the runtime, it will work.

I've changed my graphics card, but the method you proposed I haven't used before. I used to add environment variables to .bashrc. Are you using the 6700xt as well? If anyone succeeds, can you tell me, thank you!

---

### 评论 #23 — supersonictw (2024-03-30T23:23:13Z)

> I've changed my graphics card, but the method you proposed I haven't used before. I used to add environment variables to .bashrc. Are you using the 6700xt as well? If anyone succeeds, can you tell me, thank you!

![lspci -v -m](https://github.com/ROCm/ROCm/assets/13705584/74a53977-201a-484f-a71b-c16b7545a09f)

![lspci -v -m](https://github.com/ROCm/ROCm/assets/13705584/afc9cee1-044e-4b2d-8537-6eff467dc897)

Yes. I bought several rx6700xt cards used for running deep learning training.
The method is working on the cards.

`.bashrc` might be not working because not all applications use `bash` as its shell, and some even ignore the variables of global environment just like `Jupyter on VScode`.

You can find config for the application to set the variable, or just to put the variable on your codes. Stupid but it's working.

---

### 评论 #24 — simaotwx (2024-04-19T07:54:04Z)

> > God,who can help me!!! I don't hope switching to nvidia graphic card is my final solution.
> 
> AMD hyped up all the AI base about ROCm being a serious solution and competitor to CUDA, the reality is, it's far from the truth. I go from one issue to another, each step is a minor victory but then you hit another blockade, which is frustrating. Truth of the matter, ROCm is not production ready.

I think it's less about ROCm and more about everything being made to work on CUDA and now there are layers to make it work with ROCm, somehow.

---

### 评论 #25 — almereyda (2024-04-19T10:03:28Z)

The shim for running CUDA workloads on ROCm is available at [vosen/ZLUDA](https://github.com/vosen/ZLUDA/).

---

### 评论 #26 — simaotwx (2024-04-19T10:07:44Z)

> The shim for running CUDA workloads on ROCm is available at [vosen/ZLUDA](https://github.com/vosen/ZLUDA/).

Last time I tried it did not work at all. IIRC whatever I was trying to do was still checking for NVIDIA card availability and thus refusing to work. This stuff should be more vendor agnostic and not rely on proprietary commercial solutions.

---

### 评论 #27 — supersonictw (2024-04-19T19:10:22Z)

> I was trying to do was still checking for NVIDIA card availability and thus refusing to work.

What's the application you tried to use with ZLUDA?

---

### 评论 #28 — dangarciahe (2024-05-20T14:43:18Z)

`**RuntimeError: HIP error: invalid device function`

I had the same error when doing anything other than creating integers and sending them to the GPU on my 6700 XT. 

The solution was just to restart the PC, not sure why (both drivers and ROCm were already installed, only PyTorch was new). A thing worth trying if you get the error.

I still need to define global variables:

> export PYTORCH_ROCM_ARCH="gfx1031"
export HSA_OVERRIDE_GFX_VERSION=10.3.1
export HIP_VISIBLE_DEVICES=0
export ROCM_PATH=/opt/rocm

---

### 评论 #29 — supersonictw (2024-05-20T14:49:07Z)

> The solution was just to restart the PC, not sure why (both drivers and ROCm were already installed, only PyTorch was new). A thing worth trying if you get the error.

The problem might because `HSA_OVERRIDE_GFX_VERSION=10.3.0` wasn't defined before loading HIP Runtime.
So the library couldn't recognize your rx6700xt ISA is the same as `gfx1030`.

---

### 评论 #30 — dangarciahe (2024-05-20T14:58:53Z)

> The problem might because `HSA_OVERRIDE_GFX_VERSION=10.3.0` wasn't defined before loading HIP Runtime. So the library couldn't recognize your rx6700xt ISA is the same as `gfx1030`.

I manually defined the variable before calling any PyTorch stuff. Shouldn't it already be defined before loading HIP runtime? In any case, I'm adding manually-defined global variables to previous answer.

---

### 评论 #31 — supersonictw (2024-05-20T15:07:26Z)

In fact, some interpreter might ignore the system environment variables,
so it's required to make sure the `HSA_OVERRIDE_GFX_VERSION=10.3.0` is defined.

For example, while using `pytorch` with `ipython`, `vscode's jupyter` or `jupyter notebook`:

```py
from os import putenv
putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0") # The line must be defined before importing torch.

import torch # OK. The HIP Runtime of PyTorch can recognize your ISA.
import torch.nn as nn
```

---

### 评论 #32 — dangarciahe (2024-05-20T15:16:51Z)

Yeah, that's exactly what I did in my `Jupyter Lab` environment (restarting kernel, etc.), so I guess it is still unclear why the issue solved itself by restarting the PC after installing PyTorch. 

As a note, I also tried running pure Python, adding the variables via export, with the same result.  

---

### 评论 #33 — spirosbond (2024-06-01T15:33:33Z)

Thank you all. This is a very helpful thread. I also managed to run my script on my AMD Radeon RX 7700S on EndeavourOS (Arch) by running:
`HSA_OVERRIDE_GFX_VERSION=11.0.0 python script.py`

My rocminfo and script are attached.
Feel free to use my script to test performance difference between CPU and GPU with torch.
[rocm_cuda_test.zip](https://github.com/user-attachments/files/15522324/rocm_cuda_test.zip)


---

### 评论 #34 — Argyraspides (2024-06-10T13:58:04Z)

@supersonictw's fix worked for me:

![image](https://github.com/ROCm/ROCm/assets/95353936/5c144529-288b-4133-b81e-cdf88adf6764)

At last! Training with my Ryzen 5 5600X took about 1 hour. My 6700XT brought this down to just under 2 minutes. Great stuff.

---

### 评论 #35 — ppanchad-amd (2024-06-18T20:17:18Z)

@Bear-Beer Please confirm if we can close this ticket. Thanks!

---

### 评论 #36 — s34296216 (2024-07-01T07:40:57Z)

@supersonictw  Thank you very much for the solution! 
It works for my 6700xt.

---

### 评论 #37 — supersonictw (2024-09-15T03:19:27Z)

> P.S.I have added code in terminal as follows export PYTORCH_ROCM_ARCH="gfx1031" export HSA_OVERRIDE_GFX_VERSION=10.3.1 export HIP_VISIBLE_DEVICES=0 export ROCM_PATH=/opt/rocm

@plane714 @dangarciahe 

Oops! I notice you're trying to define `HSA_OVERRIDE_GFX_VERSION=10.3.1`.

But actually, the variable **must to be** `HSA_OVERRIDE_GFX_VERSION=10.3.0`.

Anyway, hoping you get well, with any computing device.

---

### 评论 #38 — gabriel-peracio (2024-10-14T21:33:06Z)

> Did you try?
> 
> > export PYTORCH_ROCM_ARCH="gfx1031"
> > export HSA_OVERRIDE_GFX_VERSION=10.3.1
> > export HIP_VISIBLE_DEVICES=0
> > export ROCM_PATH=/opt/rocm
> 
> If not, try each one separate and some combination of them.

This bricked my install

---

### 评论 #39 — supersonictw (2024-10-15T01:41:04Z)

> This bricked my install

Please use `HSA_OVERRIDE_GFX_VERSION=10.3.0` instead.

![ROCm on RX6700XT](https://github.com/user-attachments/assets/54f5a3ab-eb61-4f08-99dc-cb6076a0cdbc)
![ROCm on RX6700XT](https://github.com/user-attachments/assets/b07b1ac3-8dde-4149-b2a9-bf3e6525f9b9)
![ROCm on RX6700XT](https://github.com/user-attachments/assets/9b14ad83-8f5a-4210-a609-520cef525a01)

---

### 评论 #40 — iHad168 (2024-10-16T03:23:07Z)

> 只需要放
> 
> ```python
> from os import putenv
> putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0")
> ```
> 
> 在你的程式碼的頂部。
> 
> 它很髒，但它正在工作。
> 
> ![程式碼](https://private-user-images.githubusercontent.com/13705584/317721805-c3e96b08-f82a-4e8c-8031-df562a2d0820.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjkwNDA0NjAsIm5iZiI6MTcyOTA0MDE2MCwicGF0aCI6Ii8xMzcwNTU4NC8zMTc3MjE4MDUtYzNlOTZiMDgtZjgyYS00ZThjLTgwMzEtZGY1NjJhMmQwODIwLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEwMTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMDE2VDAwNTYwMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTFiYzIwMDkyZDdkYTAxNGIxMWY5YTc0NmY4YWRkOWExMDU4OTJhZjZiYmRkNzEzYWUwZjg0ODQ4Zjg4ODM3ZjMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.vVDbQhS1xTYX39X6hRohmuXVvEc5w4gIYypkVAXHNKI)
> 
> The reason might be your interpreter runtime didn't use your system variables.
> 
> Force to inject `HSA_OVERRIDE_GFX_VERSION` on the runtime, it will work.

I success in `Arch Linux` use
`export HSA_OVERRIDE_GFX_VERSION=10.3.0`
`/home/<username>/StabilityMatrix/StabilityMatrix.AppImage`

Thank you



---

### 评论 #41 — supersonictw (2024-10-16T03:54:04Z)

> I success in `Arch Linux` use
> 
> `export HSA_OVERRIDE_GFX_VERSION=10.3.0`
> 
> `/home/<username>/StabilityMatrix/StabilityMatrix.AppImage`
> 
> Thank you

恭喜 不客氣 🎊
You're welcome

---

### 评论 #42 — definitelyuncertain (2024-11-21T07:24:52Z)

I had to use `HSA_OVERRIDE_GFX_VERSION=10.3.0` on my RX6600 XT (Arch) too. With both the pre-built `2.5.1 + RoCM 6.2` wheel from pip, as well as `2.6.0` built from source (git main).

This is despite my GPU being detected as `gfx1032`. And when building from source, I also had to set `PYTORCH_ROCM_ARCH="gfx1030"`, otherwise I'd get the same error as OP.

Funnily enough, it did work for integer tensors without the above fix. When I tried anything floating-point though, it would crash with an error like here: https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/11942

---

### 评论 #43 — afsara-ben (2024-12-04T20:35:05Z)

   ```
 import torch
!export TORCH_USE_HIP_DSA=1
from os import putenv
putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
# device = torch.cuda.get_device_name(0)
try:
    x = torch.rand((100, 100), device=device)
    print("GPU tensor creation successful.")
except RuntimeError as e:
    print(f"Error: {e}")
```
I did the mentioned steps but i am still getting error

> Error: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


---

### 评论 #44 — zeusshy (2024-12-18T05:07:42Z)

> Just need to put只需要把
> 
> ```python
> from os import putenv
> putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0")
> ```
> 
> on the top of your codes.在您的代码顶部。
> 
> It's dirty, but it's working.它很脏，但它正在工作。
> 
> ![codes](https://private-user-images.githubusercontent.com/13705584/317721805-c3e96b08-f82a-4e8c-8031-df562a2d0820.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ0OTg2NzQsIm5iZiI6MTczNDQ5ODM3NCwicGF0aCI6Ii8xMzcwNTU4NC8zMTc3MjE4MDUtYzNlOTZiMDgtZjgyYS00ZThjLTgwMzEtZGY1NjJhMmQwODIwLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjE4VDA1MDYxNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTkwMzNhYWU0NjZiZTNjZWE3MTQ5N2RjZGZhYjAwYjJkNDNhYzE5OWI3Njc5MjU5NWMzN2VhY2Q3MTQ4YTZlZmUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.3DkpHj8u0dRqK4uRELkbgD9hMprY4affQjTZjTEPl1I)
> 
> The reason might be your interpreter runtime didn't use your system variables.原因可能是您的解释器运行时没有使用您的系统变量。
> 
> Force to inject `HSA_OVERRIDE_GFX_VERSION` on the runtime, it will work.强制注入 `HSA_OVERRIDE_GFX_VERSION` 运行时，它将起作用。

yes，it‘s useful for me，I run a program is transunet，device is 6750Gre12G。THANK YOU！！！

---

### 评论 #45 — supersonictw (2024-12-18T05:21:39Z)

@afsara-ben 
> I did the mentioned steps but i am still getting error

Oh nono. Don't let "putenv" work after "import pytorch".

I said:

> Just need to put

> ```py
> from os import putenv
> putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0")
> ```

> on the top of your codes.

It **must** be on the top of your codes.

```py
from os import putenv
putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0")

!export TORCH_USE_HIP_DSA=1 # every env variable should be defined before importing modules
import torch # pytorch will know your ISA is 10.3.0, because it will fetch the global variable in module when it's loading (once, at first importing)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
# device = torch.cuda.get_device_name(0)
try:
 x = torch.rand((100, 100), device=device)
 print("GPU tensor creation successful.")
except RuntimeError as e:
 print(f"Error: {e}")
```

Please note, `HSA_OVERRIDE_GFX_VERSION=10.3.0` only works on RDNA2.
For RDNA3, please use `HSA_OVERRIDE_GFX_VERSION=11.0.0` instead.

---

### 评论 #46 — Karl-Han (2025-05-15T03:13:45Z)

I encountered similar problem, but the above solution with just changing the environment variables doesn't help. 

In addition, I logged with detailed log, and it turns out like https://github.com/ROCm/ROCm/issues/4208#issuecomment-2596303334

Host setup:
- Ubuntu 24.04.2 LTS
- gfx906
- /opt/rocm-6.3.2

I tried the following ways:
- use default `rocm/pytorch:latest` and `rocm/pytorch:rocm6.3_ubuntu24.04_py3.12_pytorch_release_2.4.0`
- set the `GFX_ARCH=gfx906 ROCM_VERSION=6.3.2 HSA_OVERRIDE_GFX_VERSION=9.0.6 HIP_VISIBLE_DEVICES=0 ROCM_PATH=/opt/rocm` (for sure they are in different lines)

Here are my solutions:
- just install pytorch at host and it works perfectly fine, but may not be a good idea.
- Use docker and follow [wheel package](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-a-wheels-package). Attached my version of Dockerfile and the testing command: `docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri/renderD128 --name test --group-add 44 --group-add 993 --ipc=host --shm-size 8G -it --rm rocm-pytorch:latest python -c "import torch; print(torch.ones(2).cuda())"`

```Dockerfile
# based on https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html

# Step 1: Use ROCm 6.3.2 base image
FROM rocm/dev-ubuntu-24.04:6.3.2

ENV GFX_ARCH=gfx906
ENV ROCM_VERSION=6.3.2
ENV HSA_OVERRIDE_GFX_VERSION=9.0.6
ENV HIP_VISIBLE_DEVICES=0
ENV ROCM_PATH=/opt/rocm

# Step 2: Install apt dependencies and clean up
RUN apt update \
    && apt install -y \
    libjpeg-dev \
    python3-dev python3-pip python-is-python3 \
    wget \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Step 3: Install Python wheel and setuptools, then install nightly ROCm PyTorch wheels
RUN pip3 install --break-system-packages wheel setuptools \
    && pip3 install --no-cache-dir --break-system-packages --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.3/ \
    && rm -rf ~/.cache/pip

# Step 4: Download install_kdb_files_for_pytorch_wheels.sh script
# Step 5: Export environment variables and run KDB install script
RUN wget https://raw.githubusercontent.com/wiki/ROCm/pytorch/files/install_kdb_files_for_pytorch_wheels.sh\
    && chmod +x install_kdb_files_for_pytorch_wheels.sh \
    && ./install_kdb_files_for_pytorch_wheels.sh \
    && rm ./install_kdb_files_for_pytorch_wheels.sh

# Default command to open Python for testing
CMD ["/bin/sh", "-c"]
```

---

### 评论 #47 — fgdfgfthgr-fox (2025-05-28T12:23:55Z)

Same issue as above, which I think might be due to another issue that's different from what other people in this thread has encountered... 

---

### 评论 #48 — koolara (2025-06-11T18:22:13Z)

> [@afsara-ben](https://github.com/afsara-ben)
> 
> > I did the mentioned steps but i am still getting error
> 
> Oh nono. Don't let "putenv" work after "import pytorch".
> 
> I said:
> 
> > Just need to put
> 
> > from os import putenv
> > putenv("HSA_OVERRIDE_GFX_VERSION", "10.3.0")
`HSA_OVERRIDE_GFX_VERSION=11.0.0` instead.

THANK YOU! I was using  
`env_export="export HIP_VISIBLE_DEVICES=1,2"`
in my start.sh script, but your 
`from os import putenv
putenv("HIP_VISIBLE_DEVICES","1,2")`
works

---
