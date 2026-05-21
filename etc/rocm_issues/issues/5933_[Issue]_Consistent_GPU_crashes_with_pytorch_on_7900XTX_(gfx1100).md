# [Issue]: Consistent GPU crashes with pytorch on 7900XTX (gfx1100)

> **Issue #5933**
> **状态**: open
> **创建时间**: 2026-02-05T13:51:22Z
> **更新时间**: 2026-03-04T20:47:22Z
> **作者**: leuchthelp
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5933

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

Consistent GPU crashes when running code inside [rocm/pytorch:latest](https://hub.docker.com/r/rocm/pytorch) container. (was not tested outside of container)

Code to reproduce and please see `dmesg` output below. 

This might very well be because of my limited understanding of proper `pytorch`, `transfomers` etiquette. However it is currently keeping me from learning the proper way. 

The proper implementation and example code follow the [transformers guide on how to use paddle-ocr](https://huggingface.co/docs/transformers/model_doc/paddleocr_vl?usage=AutoModel#batched-inference) exactly, including set parameters.

The goal was to create a pipeline which can take images containing text of arbitrary sizes (height, width), batch them up (goal was: 16-64 images) and have the model perform batched inference on them. The images usually include just a single sentence in binary colors (text:black, background: white). Multiple `CPUWorkers` gather the images and queue them towards a single `GPUWorker` which then performs the inference once the batch is sufficiently large. 

The example code does not reflect that behavior, just represents a presumed minimum viable example to crash the Desktop and GPU.

I assumed it might be my GPU clock speed, which can exceed 3020MHz - so I tried limited it naively with [CoreCtrl](https://gitlab.com/corectrl/corectrl) using the  `Powermode=Advanced` and then `Power Profile=Compute` which held the `GPU Clock` at just 568Mhz (also the same in `nvtop`, `amd-smi` and `rocm-smi`), but could still get it to crash consistently. 

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 7900X 12-Core Processor

### GPU

Radeon RX 7900 XTX - gfx1100 

### ROCm Version

ROCm version: 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

- Install Ubuntu fresh
- Install [Rocm for Radeon products](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html)
- Install docker
- Run [pytorch container](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html)

Happens much faster with higher `batchsize` (`>=8`). 

The code creates a `PaddlePaddle/PaddleOCR-VL` with `flash_attention_2`, creates a batch of 8 images and tries to analyze text inside. (in this case just random noise for easier reproduction, but does not matter)

```
from transformers import AutoModelForCausalLM, AutoProcessor
from copy import deepcopy
from PIL import Image
import numpy as np
import torch


def main():
    # Model setup
    torch_device        = "cuda"
    model_name          = "PaddlePaddle/PaddleOCR-VL"
    attn_implementation = "flash_attention_2"

    model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            dtype=torch.bfloat16,
            attn_implementation=attn_implementation, 
        ).to(device=torch_device).eval()
    processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True, use_fast=True)


    # Batch setup
    batch = []
    batch_size = 8
    task = "ocr"
    prompts = {
        "ocr": "OCR:",
    }
    message_template = [
                {"role": "user",         
                 "content": [
                        {"type": "image", "image": None},
                        {"type": "text", "text": prompts[task]},
                    ]
                }
            ]

    for _ in range(0, batch_size):
        height  = np.random.randint(24, 180)
        width   = np.random.randint(24, 180)
        a       = np.random.rand(height, width, 3) * 255
        image   = Image.fromarray(a.astype('uint8')).convert('RGB')

        message = deepcopy(message_template)
        message[0]["content"][0]["image"] = image
        batch.append(message)


    # Input setup
    inputs = processor.apply_chat_template(
            batch, 
            add_generation_prompt=True,
	        tokenize=True,
	        return_dict=True,
	        return_tensors="pt",
            padding=True,
            padding_side='left',
        ).to(torch_device)
    
    with torch.inference_mode():
            out = model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=False,
                use_cache=True
            )

    generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, out)]
    texts = processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)



if __name__ == "__main__":
    main()
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen 9 7900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7900X 12-Core Processor
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
  Max Clock Freq. (MHz):   5911                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32566780(0x1f0edfc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32566780(0x1f0edfc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32566780(0x1f0edfc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32566780(0x1f0edfc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-029a3387f47e439f               
  Marketing Name:          Radeon RX 7900 XTX                 
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
    L2:                      6144(0x1800) KB                    
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2431                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 602                                
  SDMA engine uCode::      27                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1100         
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
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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

`dmesg` output:
[one crash isolated.txt](https://github.com/user-attachments/files/25097627/one.crash.isolated.txt)
[multi-crashes.txt](https://github.com/user-attachments/files/25097628/multi-crashes.txt)


---

## 评论 (12 条)

### 评论 #1 — lucbruni-amd (2026-02-17T19:46:47Z)

Hi @leuchthelp, thanks for the detailed report and `dmesg` logs.

I couldn't reproduce this on a similar setup (Radeon RX 7900 XT / `gfx1100`, ROCm 7.2.0, `rocm/pytorch:latest` container) and was unable to reproduce the crash with `batch_size=8` and `batch_size=64`, running the script multiple times.

Could you share your Flash Attention installation method? For `gfx1100` (RDNA3), you need to use the Triton backend (see [here](https://github.com/ROCm/flash-attention?tab=readme-ov-file#amd-rocm-support)). Please also provide your `pip list` output for more information. Here's mine:

```
# pip list
Package                  Version
------------------------ ------------------------------
annotated-doc            0.0.4
annotated-types          0.7.0
anyio                    4.12.1
apex                     1.9.0+rocm7.2.0.gite37ed124
certifi                  2026.1.4
charset-normalizer       3.4.4
click                    8.3.1
contourpy                1.3.3
cxxfilt                  0.3.0
cycler                   0.12.1
einops                   0.8.2
filelock                 3.20.3
flash_attn               2.8.3
fonttools                4.61.1
fsspec                   2026.1.0
h11                      0.16.0
hf-xet                   1.2.0
httpcore                 1.0.9
httpx                    0.28.1
huggingface_hub          0.36.2
hypothesis               6.150.2
idna                     3.11
importlib_metadata       8.7.1
iniconfig                2.3.0
Jinja2                   3.1.6
kiwisolver               1.4.9
markdown-it-py           4.0.0
MarkupSafe               3.0.3
matplotlib               3.10.8
mdurl                    0.1.2
mpmath                   1.3.0
networkx                 3.6.1
ninja                    1.13.0
numpy                    2.4.1
packaging                26.0
pandas                   3.0.0
pillow                   12.1.0
pip                      26.0.1
pluggy                   1.6.0
protobuf                 6.33.5
psutil                   7.2.2
pydantic                 2.12.5
pydantic_core            2.41.5
Pygments                 2.19.2
pyparsing                3.3.2
pytest                   9.0.2
python-dateutil          2.9.0.post0
PyYAML                   6.0.3
regex                    2026.1.15
requests                 2.32.5
rich                     14.3.2
safetensors              0.7.0
scipy                    1.17.0
sentencepiece            0.2.1
setuptools               80.10.1
shellingham              1.5.4
six                      1.17.0
sortedcontainers         2.4.0
sympy                    1.14.0
tokenizers               0.22.2
torch                    2.9.1+rocm7.2.0.lw.git7e1940d4
torchaudio               2.9.0+rocm7.2.0.gite3c6ee2b
torchvision              0.24.0+rocm7.2.0.gitb919bd0c
tqdm                     4.67.1
transformer_engine       2.4.0
transformer_engine_rocm  2.4.0
transformer_engine_torch 2.4.0
transformers             4.57.6
triton                   3.5.1+rocm7.2.0.gita272dfa8
typer                    0.24.0
typer-slim               0.24.0
typing_extensions        4.15.0
typing-inspection        0.4.2
urllib3                  2.6.3
zipp                     3.23.0
```

Note that `flash_attn` was acquired from the [ROCm fork](https://github.com/ROCm/flash-attention?tab=readme-ov-file#triton-backend), and since this Docker container ships with `Triton` already, my steps were:

```
git clone https://github.com/ROCm/flash-attention.git
cd flash-attention
export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
pip install . --no-build-isolation
python paddle.py
```

If this is satisfied and the crash still happens, let's investigate further.

---

### 评论 #2 — leuchthelp (2026-02-17T20:57:45Z)

First up thank you very much for the follow-up. I will try to provide the requested information as accurately as possible.

Interesting that it did work for you, so your device was able to process all `8` or `64`  in one go, correct? Maybe it is a hardware issue on my side (?).

> Could you share your Flash Attention installation method? 

Ahh I forgot to mention in the original that I was setting `"FLASH_ATTENTION_TRITON_AMD_ENABLE" = "TRUE"` within the devcontainer globally which is why I did not need to add `os.environ["FLASH_ATTENTION_TRITON_AMD_ENABLE"] = "TRUE"` in the script and so forgot to add it to the reproductions script. Sorry about that, would have answered at least some of the questions right away.

I installed Flash Attention following the instructions on their [Github under "Trition Backend"](https://github.com/Dao-AILab/flash-attention#triton-backend). I did not clone the ROCm fork, as I did not know it existed. However, the instructions appear the same (?). I will try to run my project with the ROCm fork just for parity though it is some commits behind the original `master`.

```console
git clone https://github.com/Dao-AILab/flash-attention.git
cd flash-attention
FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" python setup.py install
```

For development I am running a Devcontainer following their Setup-Guide as well:

```Dockerfile
FROM rocm/pytorch:latest

//Other project setup

ENV FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
RUN . /opt/venv/bin/activate
RUN git clone https://github.com/Dao-AILab/flash-attention &&\ 
    cd flash-attention &&\
    python setup.py install
```


Here is the requested output of `pip list`
```console
pip list
Package            Version
------------------ ------------------------------
apex               1.9.0+rocm7.2.0.gite37ed124
bcp47              0.1.0
bitmath            1.3.3.1
certifi            2026.1.4
chardet            5.2.0
charset-normalizer 3.4.4
colorama           0.4.6
contourpy          1.3.3
cxxfilt            0.3.0
cycler             0.12.1
einops             0.8.2
filelock           3.20.3
flash_attn         2.8.3
fonttools          4.61.1
fsspec             2026.1.0
hf-xet             1.2.0
huggingface-hub    0.36.0
hypothesis         6.150.2
idna               3.11
iniconfig          2.3.0
Jinja2             3.1.6
kiwisolver         1.4.9
langcodes          3.5.1
markdown-it-py     4.0.0
MarkupSafe         3.0.3
matplotlib         3.10.8
mdurl              0.1.2
mpmath             1.3.0
msgspec            0.20.0
networkx           3.6.1
ninja              1.13.0
numpy              2.4.1
packaging          26.0
pandas             3.0.0
pillow             12.1.0
pip                26.0
pluggy             1.6.0
protobuf           6.33.5
Pygments           2.19.2
pymkv2             2.2.0.post1
pyparsing          3.3.2
pysrt              1.1.2
pytesseract        0.3.13
pytest             9.0.2
python-dateutil    2.9.0.post0
python-iso639      2026.1.31
PyYAML             6.0.3
regex              2026.1.15
requests           2.32.5
rich               14.3.1
safetensors        0.7.0
scipy              1.17.0
sentencepiece      0.2.1
setuptools         80.10.1
six                1.17.0
sortedcontainers   2.4.0
sympy              1.14.0
tokenizers         0.22.2
torch              2.9.1+rocm7.2.0.lw.git7e1940d4
torchaudio         2.9.0+rocm7.2.0.gite3c6ee2b
torchvision        0.24.0+rocm7.2.0.gitb919bd0c
tqdm               4.67.1
transformers       4.57.6
triton             3.5.1+rocm7.2.0.gita272dfa8
typing_extensions  4.15.0
urllib3            2.6.3
```

---

### 评论 #3 — leuchthelp (2026-02-17T21:14:38Z)

I was just able to crash my GPU again with `batchsize=64`, this time with the official ROCm fork of flash attention at heart.

Dmesg output is attached.

Also if you want to reconstruct the entire Container I will include both my `devcontainer.json` and `Dockerfile` for the devcontainer in full.

[26648 615536 workqueue.txt](https://github.com/user-attachments/files/25374348/26648.615536.workqueue.txt)

[devcontainer.json](https://github.com/user-attachments/files/25374361/devcontainer.json)
```json
{
  "name": "Custom ROCm PyTorch Dev",
  "build": { "dockerfile": "Dockerfile" },

  "runArgs": [
    "--cap-add=SYS_PTRACE",
    "--security-opt=seccomp=unconfined",
    "--device=/dev/kfd",
    "--device=/dev/dri",
    "--group-add=video",
    "--ipc=host",
    "--shm-size=8G"
  ],

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  }
}
```

Dockerfile
```Dockerfile
FROM rocm/pytorch:latest


RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8
RUN update-locale
RUN apt-get update && apt-get install -y tesseract-ocr mkvtoolnix 

RUN pip install --upgrade pip
RUN pip install pymkv2 pytesseract pysrt pillow rich langcodes colorama einops transformers==4.57.6 protobuf sentencepiece

ENV FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
RUN . /opt/venv/bin/activate
RUN git clone https://github.com/ROCm/flash-attention.git &&\ 
    cd flash-attention &&\
    python setup.py install
```

If you want the original Dockerfile with which I submitted the initial issue simply swap the ROCm fork for the official flash attention repository in the `git clone` line. Everything else stayed entirely the same.


---

### 评论 #4 — lucbruni-amd (2026-02-18T20:50:40Z)

Thanks @leuchthelp - doesn't look like the Flash Attention sourcing is the issue. I'll investigate further and get back to you.

---

### 评论 #5 — lucbruni-amd (2026-03-02T21:08:27Z)

Hi @leuchthelp, I am still unable to reproduce this with the exact setup in your most recent comment. Could you upload your full `dmesg` log from boot until the end of the run (where it crashes)? I'd like to see more information such as VBIOS version. There's a chance this is firmware-related.

---

### 评论 #6 — leuchthelp (2026-03-02T23:31:20Z)

@lucbruni-amd full dmesg [here](https://github.com/user-attachments/files/25698035/0.318857.IP.idents.hash.txt) from proper testing run

had `Overdrive` enabled in this second run, from testing with `LACT` to limit GPU frequency: [LACT Run 2 crashes](https://github.com/user-attachments/files/25697812/0.688286.usb.usb2.Manufacturer.txt)

I also sometimes have `nvtop` open, dunno if this could be related. I have also observed another hard crash, this time GPU-ring while trying to copy the `dmesg` output. This type of crash did not occur before and did not happen while actually running the `reproduce.py`. Thought I would include it for good measure.

[additional](https://github.com/user-attachments/files/25697853/429.088222.amdgpu.0000.txt)

Thank you again for still trying to work on the issue, even if you cannot reproduce it. Getting a feeling this could actually be a hardware issue on my end.

---

### 评论 #7 — lucbruni-amd (2026-03-03T18:28:03Z)

Thanks for the additional info. Could you also (while running the script) share your `rocm-smi -a` output? What method did you use to enable Overdrive? At what clock speeds were you able to reproduce the crash?

---

### 评论 #8 — leuchthelp (2026-03-03T21:27:41Z)

Ok just to clarify a few things, to align the record and ensure information is accurate: 

1. The original crash report was submitted with NO overdrive enabled. The `dmesg` logs captured all had `Overdrive` disabled. Just the most recent one accidentally had `Overdrive` enabled so I thought I would mark them as such to differentiate them.

Since I observed my GPU spiking to about 3030 MHz in [nvtop](https://thedocs.io/nvtop/), I suspect it might be helpful to limit GPU clock and tried doing so by 2 means: 

First: [CoreCtrl](https://gitlab.com/corectrl/corectrl) and
Second: [LACT](https://github.com/ilya-zlobintsev/LACT) 

With [LACT](https://github.com/ilya-zlobintsev/LACT) to enable `clockspeed` & `voltage` control `Overdrive` needs to be enabled. The tool provides an integrated option to enabled `Overdrive` for the user. Once installed it actively prompts the user if they want to enabled it. [Here is the relevant page from LACT WIKI on how it achieves that](https://github.com/ilya-zlobintsev/LACT/wiki/Overclocking-(AMD)).
Once enabled I set just the `Maximum GPU Clock` in [LACT](https://github.com/ilya-zlobintsev/LACT) to about 2650 MHz and could still get my GPU to crash.

However decreasing the GPU clock did not solve the issue as I had originally assumed.

I can provide additional testing with `Overdrive` enabled if need be.

2. The output of `rocm-smi -a` is provided below - `Overdrive` was left disabled and the GPU completely without control of `LACT` or similar software, i.e. all things baseline:

[crash rocm-smi -a, no overdrive](https://github.com/user-attachments/files/25726306/text.txt)

Gathered with a simple script to repeatedly run `rocm-smi -a`. Also records time-stamps. Crash happened at about `09:00:01 pm`, line `41783` in the `.txt` or the `128` call recorded. 

Receives `Error when calling libdrm` and comes back the very next call to `rocm-smi -a` with `sclk` now at 16Mhz. 

Afterwards the pattern repeats a couple of times, likely when the GPU becomes `wedged` as reported in `dmesg` and resets.

[dmesg](https://github.com/user-attachments/files/25726448/1421.194967.amdgpu.0000.txt) for cross reference.

One thing I have observed multiple times is my `mclk` effectively staying locked at `96` Mhz which always seemed suspiciously low for this type of workload.

In my full project where I set the `batchsize` to `1` currently and run this task heavily parallelized I can achieve `mclk` usually at like `1249` Mhz and `sclk` at `2930-2970` Mhz. However there are short dips to `mclk 96` Mhz when my `sclk` spikes to above `3000` Mhz. Hence my initial assumption that this could also be related to unstable clocks.

---

### 评论 #9 — lucbruni-amd (2026-03-04T16:24:14Z)

Thanks once again @leuchthelp for the comprehensive info. Could you try your luck in running the workload again after forcing high `mclk`? You can do this with `sudo amd-smi set -l high` (then observing an increase in `mclk`) and undo with `sudo amd-smi set -l auto`. You can view the documentation for that [here](https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html#amd-smi-set).

---

### 评论 #10 — leuchthelp (2026-03-04T18:02:13Z)

Ah I see, I had previously read up on those option, but was not sure with which to fiddle, if at all, hence then trying to use `LACT` instead to get the GPU into a more compatible performance profile.

Setting the profile to `high` does seem to help with the issue. It is now much harder for me to get it to crash with the `reproduce.py` provided. I can still make it crash, though out of the 15 runs I did, it only happened once.

However, if I increase the load by running my original project and increasing the `batchsize` to 4 or 8 form 1 it happens again, still less frequently overall. More specifically when I started doing more different tasks i.e. opening `firefox`, opening additional terminals or similar. I can observe micro stutters as well, though that would be expected given the load.

For context, the full project starts 4 GPU workers total, 2 for OCR, 2 for language recognition. OCR output is send to the language recognition workers. Each then handling `batchsize` images at a time. Reducing the total GPU workers to 2, i.e. 1 OCR, 1 language recognition further decreases the rate of occurrence though still more frequent than with `reproduce.py`

`rocm-smi -a` output and `dmesg` attached. This time line `90559` or the `259`th call.

[rocm-smi -a, no overdrive, set -l high](https://github.com/user-attachments/files/25747757/text.txt)

[dmesg, no overdrive, set -l high](https://github.com/user-attachments/files/25747839/2535.029925.amdgpu.0000.txt)



---

### 评论 #11 — leuchthelp (2026-03-04T18:21:57Z)

Small update: While doing more consecutive testing runs I have encountered a crash with my full project, 2 GPU workers and `batchsize` of 4 after like 15 minutes of it running smoothly. 

This time the ring reset did not happen and all that was reported to `dmesg` was:

```console
[ 4972.438521] amdgpu 0000:03:00.0: amdgpu: [drm] REG_WAIT timeout 1us * 100 tries - dcn32_program_compbuf_size line:147
```

---

### 评论 #12 — lucbruni-amd (2026-03-04T20:47:22Z)

>More specifically when I started doing more different tasks i.e. opening firefox, opening additional terminals or similar. I can observe micro stutters as well, though that would be expected given the load.

This seems consistent with the logs from [26648 615536 workqueue.txt](https://github.com/user-attachments/files/25374348/26648.615536.workqueue.txt).

```
[26648.615536] workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 259 times, consider switching to WQ_UNBOUND
[27109.508307] amdgpu 0000:03:00.0: amdgpu: Dumping IP State
[27109.509387] amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
[27109.509430] amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[27109.509431] amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[27109.509433] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 timeout, signaled seq=7091, emitted seq=7093
[27109.509437] amdgpu 0000:03:00.0: amdgpu:  Process firefox pid 5437 thread firefox:cs0 pid 5590
[27109.509439] amdgpu 0000:03:00.0: amdgpu: Starting comp_1.1.1 ring reset
```

I've raised this issue internally with the firmware team, I'll post updates here when I have them. Thanks for your patience thus far.

---
