# [Issue]: Memory access fault by GPU node-2 (Agent handle: 0x5640a8bb1980) on address 0x7feea09c5000. Reason: Page not present or supervisor privilege.

> **Issue #2804**
> **状态**: closed
> **创建时间**: 2024-01-12T21:34:41Z
> **更新时间**: 2024-09-17T17:48:08Z
> **关闭时间**: 2024-09-17T13:45:03Z
> **作者**: nix-wolf
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2804

## 描述

###LOOK TO MY LAST COMMENT
I do believe those will be the outputs you need, and might be more useful

### Problem Description

Happens after running about 6-10 iterations of any of the latter python scripts, essentially if im doing something with the gpu i figure it is only a matter of time before it throws, i havent tested it but im guessing there is likely possiblity, Ive tried quite a few things as well. I know that inherently this may not be a rocm issue, but i think w.e is going on with the gpu is in your ballpark of knowing how to fix.

```
Memory access fault by GPU node-2 (Agent handle: 0x5640a8bb1980) on address 0x7feea09c5000. Reason: Page not present or supervisor privilege.

Unable to open /dev/kfd read-write: Invalid argument
admin is member of render group
```

Note: I have been running this setup for over a week now testing and carrying on and before I did what I did, i had generated 200 images roughly, with no issues at all and all the images were good. 

### Operating System

Fedora 39 && CentOS 7

### CPU

AMD Ryzen Threadripper 1900X 8-Core Processor

### GPU

AMD Radeon RX 6750

### Other

Docker

### ROCm Version

ROCm 5.6.0

### ROCm Component

ROCm

### Steps to Reproduce

cmds are in additional information

1. run docker: this happens in a fresh container aswell, installed as supplied
2. login as user, run script, any of them after the initial point of this issue happen
3. after the script is running and through...(6-10 iterations? i realized thats about how many it would have been at when i ran the cmd) a few iterations, in another tty run ```sudo docker attach```

What have I done since, and during:

After This happened it locked up both ttys, but they were joined, i could type and the stdio of both seemed to have been linked. typed in one is showed on the other,  with formatting, ie, enter, table, etc all seem to work, i hit ctrl-c a bunch of times and ^C showed up on both. 

I went back to the host sytem and tried to kill the container, which didnt work
I tried to kill docker, and it also would work
**nothing fancy here docker image kill <id> && systemctl stop docker

when i tried to run rocminfo thats where the kfd error came from

this is when i figured there was something stuck in memory and maybe a reboot would be enough to get it to free up, so i from a terminal restarted. The computer froze at some point in the shutdown, resulting in a hard boot. It came back just fine, I started docker all the same ways as supplied, logged in, enter the python env, and ran the script, but now I was getting those dreaded out of memory issues. which i wasnt getting before. given i had run this several hundred times. 

after messing around with it, trying to change cmd line args, and the script, i decided maybe a proper reboot would be enough, the gpus are visable, rocminfo is working, torch and cuda and see the gpus, so i rebooted, without failure in the shutdown

**the system wont shut down after this happens

the issue presisted there after, eventually i figured out that if i run the base script, it seems that my OOM issues go away and i can run all three scripts, but after they are ran 6-10 times the Fault Error Happens.

after that i sout help online to find a mention on here about 

```
export HCC_SERIALIZE_KERNEL=0x3
export HCC_SERIALIZE_COPY=0x3
export HIP_TRACE_API=0x2
[then re-run your application]

More tips are listed here: https://rocm-documentation.readthedocs.io/en/latest/Other_Solutions/Other-Solutions.html
```
OH WAIT i never tried it after i got the system stable only after the issue happens.(going to do this after i post this)

but there wont even run... it cant find ANY gpus(there are two and the second one still does register properly on rocm-smi, this is after the error as I have managed to get things to close out and be killed without rebooting

![Screenshot](https://github.com/ROCm/ROCm/assets/32893554/bed3af67-0de7-44a4-bc35-0b20bfb166d6)

The next step was a complete reinstall of the docker setup on centos, again supplied in additional
only to produce the same issues(minus OOM) everything works mint for abotu 6-10 iterations then it faults


I will be trying my scripts here before long targetting my second gpu and see if the issues are on both gpus are just one(i was only using one at the time this started)

I will also run the suggestion from the other post with a stable system and see if that does anything and will post the results

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
  Name:                    AMD Ryzen Threadripper 1900X 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper 1900X 8-Core Processor
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
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    41029664(0x2721020) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    41029664(0x2721020) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    41029664(0x2721020) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD Ryzen Threadripper 1900X 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper 1900X 8-Core Processor
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
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    41262736(0x2759e90) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    41262736(0x2759e90) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    41262736(0x2759e90) KB             
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
  Marketing Name:          AMD Radeon RX 6750 XT              
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
  Max Clock Freq. (MHz):   2880                               
  BDFID:                   2816                               
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
*******                  
Agent 4                  
*******                  
  Name:                    gfx1031                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 6750 XT              
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      3072(0xc00) KB                     
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29663(0x73df)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2880                               
  BDFID:                   17408                              
  Internal Node ID:        3                                  
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
```

### Additional Information

```
echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";

OS:
NAME="Fedora Linux"
VERSION="39 (Thirty Nine)"
```

```
echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;

CPU: 
model name	: AMD Ryzen Threadripper 1900X 8-Core Processor
```

```
GPU:
  Name:                    AMD Ryzen Threadripper 1900X 8-Core Processor
  Marketing Name:          AMD Ryzen Threadripper 1900X 8-Core Processor
  Name:                    AMD Ryzen Threadripper 1900X 8-Core Processor
  Marketing Name:          AMD Ryzen Threadripper 1900X 8-Core Processor
  Name:                    gfx1031                            
  Marketing Name:          AMD Radeon RX 6750 XT              
      Name:                    amdgcn-amd-amdhsa--gfx1031         
  Name:                    gfx1031                            
  Marketing Name:          AMD Radeon RX 6750 XT              
      Name:                    amdgcn-amd-amdhsa--gfx1031 

```


Commands Run on a Base Docker File with the docker cmd to start container & to run script
```
yum update -y
sudo yum install --nogpgcheck https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-$(rpm -E %rhel).noarch.rpm
yum install -y rocm-info make gcc openssl-devel bzip2-devel libffi-devel sudo python-virtualenv conda

curl -O https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
tar -xf Python-3.8.10.tgz 
rm !$
mv Python-3.8.10 /opt
cd /opt/Python-3.8.10

./configure --enable-optimizations
make altinstall

useradd -m admin
usermod -aG wheel admin
usermod -aG video admin
passwd admin

su - admin

conda create --name pytorch-env python=3.8.10
conda activate pytorch-env

conda install -c conda-forge cudatoolkit=11.3
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm5.6/

python -c 'import torch; print(torch.cuda.is_available())'
python -c 'import torch; print(torch.cuda.device_count())'

########################################################################
### This is for sd-xl ^^^ above is just for pytorch-rocm
#########################################################################
yum install mesa-libGLw
pip install --upgrade --upgrade-strategy only-if-needed accelerate transformers diffusers einops pytorch_lightning omegaconf opencv-python

#run my script (gc)
garbage_collection_threshold:0.6,max_split_size_mb:256
PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:128 HSA_OVERRIDE_GFX_VERSION=10.3.0 python script.py

########################################################################
### Docker stuff
#########################################################################

##starts container from image(with opens)
sudo docker run -it --mount type=bind,source=./stable-diffusion-xl-base-1.0,target=/home/admin/sd-xl-1.0 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host <image_id>
```

Python Script Running at failure
```
import torch
import random
import gc
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image
from pathlib import Path
from datetime import datetime
import os

generator = torch.Generator("cuda")
generator.seed()
pipe = StableDiffusionXLPipeline.from_pretrained(
    "./", torch_dtype=torch.float16
)

refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "./",
    torch_dtype=torch.float16,
    text_encoder_2=pipe.text_encoder_2,
    vae=pipe.vae,
    variant="fp16"
)

img_name = "some_set"

prompt = "something"
prompt_2 = "something else"
n1 = "something negitive"
n2 = "something else negitive"

pipe.enable_model_cpu_offload()
refiner.enable_model_cpu_offload()

print("GENERATING PICTUREs:___________________________________________________________________________")
for i in range(200):
    print(f'IMAGE:{i}; ________________________________________________________________________START::')

    image = pipe(
        prompt, prompt_2, negitive_prompt=n1, negitive_prompt_2=n2, guidance_scale=9.5,
        num_inference_steps=50, denoising_end=0.6, output_type="latent", generator=generator
    ).images

    image = refiner(prompt, prompt_2, negitive_prompt=n1, negitive_prompt_2=n2, image=image,
        num_inference_steps=50, denoising_start=0.6).images
    
    dir = f'../{img_name}'
    if not os.path.exists(f'{dir}'):
        os.makedirs(f'{dir}')

    now = datetime.now()
    time_stamp = now.strftime("%m_%d_%Y_%H_%M_%S")
    image[0].save(f'../{img_name}/{img_name}{time_stamp}.png')

    torch.cuda.empty_cache()
    gc.collect()    

    print(f'IMAGE:{i}; ________________________________________________________________________END::')

```

Basic Sdxl Pipeline script
```
import torch
import gc
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image

pipe = StableDiffusionXLPipeline.from_pretrained(
    "./", torch_dtype=torch.float16
)

refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "./",
    torch_dtype=torch.float16,
    text_encoder_2=pipe.text_encoder_2,
    vae=pipe.vae,
    variant="fp16"
)

pipe.enable_model_cpu_offload()
refiner.enable_model_cpu_offload()

prompt = "a photo of an astronaut riding a horse on mars, photo realistic, 4k"
prompt_2 = ""
n1 = "bad quality, cartoon, painting, blurry, blurry faces"
n2 = ""

image = pipe(prompt, prompt_2, negitive_prompt=n1, negitive_prompt_2=n2, guidance_scale=9.5, num_inference_steps=50).images[0]

image.save("../img.png")

```

Basic Base+Refiner Pipeline
```
import torch
import gc
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image

pipe = StableDiffusionXLPipeline.from_pretrained(
    "./", torch_dtype=torch.float16
)

refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "./",
    torch_dtype=torch.float16,
    text_encoder_2=pipe.text_encoder_2,
    vae=pipe.vae,
    variant="fp16"
)

pipe.enable_model_cpu_offload()
refiner.enable_model_cpu_offload()

prompt = "a photo of an astronaut riding a horse on mars, photo realistic, 4k"
prompt_2 = ""
n1 = "bad quality, cartoon, painting, blurry, blurry faces"
n2 = ""

image = pipe(prompt, prompt_2, negitive_prompt=n1, negitive_prompt_2=n2, guidance_scale=9.5, num_inference_steps=50, denoising_end=0.8, output_type="latent").images

image = refiner(prompt, prompt_2, negitive_prompt=n1, negitive_prompt_2=n2, image=image, num_inference_steps=50, denoising_start=0.8).images[0]

image.save("../img.png")

```

---

## 评论 (42 条)

### 评论 #1 — nix-wolf (2024-01-12T22:30:17Z)

Using to target the second gpu
```
CUDA_VISIBLE_DEVICES=1 PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:128 HSA_OVERRIDE_GFX_VERSION=10.3.0 python script.py
```
seems to be currently workin

![Screen](https://github.com/ROCm/ROCm/assets/32893554/7346ff2a-290a-4915-8e5f-8afd51db62de)

![Screenshq](https://github.com/ROCm/ROCm/assets/32893554/e0cbd60c-e970-47bb-8b32-7f88c9477e83)

just found this again though even though i havent been using that gpu, the other ran things fine..... im going to try running it again and see if the other gpu keeps working but here

![a](https://github.com/ROCm/ROCm/assets/32893554/a13baa54-52ac-4507-9132-b55f3e6c39d3)

nvm spoke to soon

---

### 评论 #2 — nix-wolf (2024-01-12T22:35:34Z)

![dsa](https://github.com/ROCm/ROCm/assets/32893554/919d2364-d29d-47af-a8a6-0b54836d38a5)

THIS DID FAIL WITHOUT PRODUCING THE ERROR, its quietly just... left the room

---

### 评论 #3 — nix-wolf (2024-01-12T23:27:47Z)

After reboot

After starting the container from checkpoint, logging into admin, start py-env
(the basic script)
```
HIP_TRACE_API=0x2 HCC_SERIALIZE_COPY=0x3 HCC_SERIALIZE_KERNEL=0x3 CUDA_VISIBLE_DEVICES=1 PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:128 HSA_OVERRIDE_GFX_VERSION=10.3.0 python t.py
```
Succeeded
(second script witha  refiner pipe)
```
HIP_TRACE_API=0x2 HCC_SERIALIZE_COPY=0x3 HCC_SERIALIZE_KERNEL=0x3 CUDA_VISIBLE_DEVICES=1 PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:128 HSA_OVERRIDE_GFX_VERSION=10.3.0 python r.py
```
Succeeded
(full script)
```
HIP_TRACE_API=0x2 HCC_SERIALIZE_COPY=0x3 HCC_SERIALIZE_KERNEL=0x3 CUDA_VISIBLE_DEVICES=1 PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:128 HSA_OVERRIDE_GFX_VERSION=10.3.0 python gen_image_gpu2.py
```
Succeeded
Lastly will run this on the first gpu with the last command

it locked up in the first cycle will

![qwe2](https://github.com/ROCm/ROCm/assets/32893554/821094dd-f159-42aa-aa90-da65e59add6a)


![qwe1](https://github.com/ROCm/ROCm/assets/32893554/1b06cfe1-5e56-4ceb-bee9-7ea9ce562873)

![qwe](https://github.com/ROCm/ROCm/assets/32893554/335f9a56-b990-4768-a96b-75dfbff5c17d)

once it full crashed if it does ill post the results



---

### 评论 #4 — nix-wolf (2024-01-13T20:39:51Z)

So since playing with this a bunch i have got it a little bit further but im still getting the memory access fault on node-2

What I have done is, 
I realized i didnt have amdgpu or rocm installed in docker just on the host, so i installed this
21.50 && 5.6, this caused the node-2 fault error to not come up once, it would just hang and the gpu would crash out. 

but this gave me the ability to docker attach while process is running(on both gpus) without it locking, this is the orginal thing i did that cause the issue on gpu0, as i have been able to run 30 loops in one go on my second gpu multi times without it causing the first gpu to fail. 

after review of some things, i decided to upgrade to 5.7.1 on the docker container, and the py-torch nightly wheel, since i had 5.6 installed in the python-env, and subsiquently this is why i installed that version on the system. since this upgrade i got the fault to reappear on gpu0 AND the system doesnt hang, it aborted(core dumped) but with the latter flags nothing come from it. so i guess maybe ill have to set them in the enviroment via export instead of just adding it to the command line? or is there something else im missing here. 

now, the process doesnt hang, and the gpu still crashes,

I also have tried --gpureset to bring back the gpu, and never had no luck only reboots bring it back

Heres is the return from dmesg incase there is something important this looks a lot better then the dmesg results form prior to installing 5.7.1 fyi, annd the faults seem to be here
```
  19.839611] igb 0000:05:00.0 enp5s0: igb: enp5s0 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: RX/TX
[  361.175687] systemd-journald[800]: /var/log/journal/334a3d572b6144d889c71bdef17c45e2/user-1000.journal: Journal file uses a different sequence number ID, rotating.
[  369.114787] bridge: filtering via arp/ip/ip6tables is no longer available by default. Update your scripts to load br_netfilter if you need this.
[  369.117465] Bridge firewalling registered
[  384.483249] docker0: port 1(veth20ee75b) entered blocking state
[  384.483256] docker0: port 1(veth20ee75b) entered disabled state
[  384.483290] veth20ee75b: entered allmulticast mode
[  384.483351] veth20ee75b: entered promiscuous mode
[  384.668550] eth0: renamed from veth2ee07df
[  384.678715] docker0: port 1(veth20ee75b) entered blocking state
[  384.678721] docker0: port 1(veth20ee75b) entered forwarding state
[  496.996975] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  496.997001] [drm] PSP is resuming...
[  497.064760] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[  497.164759] amdgpu 0000:0b:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  497.178446] amdgpu 0000:0b:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  497.178449] amdgpu 0000:0b:00.0: amdgpu: SMU is resuming...
[  497.178453] amdgpu 0000:0b:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[  497.178457] amdgpu 0000:0b:00.0: amdgpu: SMU driver if version not matched
[  497.188226] amdgpu 0000:0b:00.0: amdgpu: SMU is resumed successfully!
[  497.189543] [drm] DMUB hardware initialized: version=0x02020020
[  497.214670] [drm] kiq ring mec 2 pipe 1 q 0
[  497.219355] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  497.219561] [drm] JPEG decode initialized successfully.
[  497.219582] amdgpu 0000:0b:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  497.219584] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  497.219586] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  497.219588] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  497.219590] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  497.219591] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  497.219593] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  497.219595] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  497.219596] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  497.219598] amdgpu 0000:0b:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  497.219600] amdgpu 0000:0b:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  497.219602] amdgpu 0000:0b:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  497.219603] amdgpu 0000:0b:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  497.219605] amdgpu 0000:0b:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  497.219606] amdgpu 0000:0b:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  497.219608] amdgpu 0000:0b:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  497.222492] amdgpu 0000:0b:00.0: [drm] Cannot find any crtc or sizes
[  497.416029] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  497.416050] [drm] PSP is resuming...
[  497.483548] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[  497.584755] amdgpu 0000:44:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  497.598548] amdgpu 0000:44:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  497.598550] amdgpu 0000:44:00.0: amdgpu: SMU is resuming...
[  497.598554] amdgpu 0000:44:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[  497.598558] amdgpu 0000:44:00.0: amdgpu: SMU driver if version not matched
[  497.607936] amdgpu 0000:44:00.0: amdgpu: SMU is resumed successfully!
[  497.609237] [drm] DMUB hardware initialized: version=0x02020020
[  497.634764] [drm] kiq ring mec 2 pipe 1 q 0
[  497.639265] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  497.639762] [drm] JPEG decode initialized successfully.
[  497.639782] amdgpu 0000:44:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  497.639784] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  497.639785] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  497.639787] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  497.639789] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  497.639790] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  497.639792] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  497.639794] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  497.639795] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  497.639797] amdgpu 0000:44:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  497.639799] amdgpu 0000:44:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  497.639800] amdgpu 0000:44:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  497.639802] amdgpu 0000:44:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  497.639804] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  497.639805] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  497.639807] amdgpu 0000:44:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  497.643130] amdgpu 0000:44:00.0: [drm] Cannot find any crtc or sizes
[  562.602013] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  562.602039] [drm] PSP is resuming...
[  562.669769] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[  562.770767] amdgpu 0000:0b:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  562.784351] amdgpu 0000:0b:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  562.784355] amdgpu 0000:0b:00.0: amdgpu: SMU is resuming...
[  562.784359] amdgpu 0000:0b:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[  562.784363] amdgpu 0000:0b:00.0: amdgpu: SMU driver if version not matched
[  562.794629] amdgpu 0000:0b:00.0: amdgpu: SMU is resumed successfully!
[  562.795944] [drm] DMUB hardware initialized: version=0x02020020
[  562.820965] [drm] kiq ring mec 2 pipe 1 q 0
[  562.825506] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  562.825651] [drm] JPEG decode initialized successfully.
[  562.825672] amdgpu 0000:0b:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  562.825674] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  562.825676] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  562.825678] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  562.825679] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  562.825681] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  562.825683] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  562.825684] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  562.825686] amdgpu 0000:0b:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  562.825687] amdgpu 0000:0b:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  562.825689] amdgpu 0000:0b:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  562.825691] amdgpu 0000:0b:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  562.825693] amdgpu 0000:0b:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  562.825694] amdgpu 0000:0b:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  562.825696] amdgpu 0000:0b:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  562.825697] amdgpu 0000:0b:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  562.829502] amdgpu 0000:0b:00.0: [drm] Cannot find any crtc or sizes
[  563.006647] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  563.006666] [drm] PSP is resuming...
[  563.074246] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[  563.175350] amdgpu 0000:44:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  563.188995] amdgpu 0000:44:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  563.188997] amdgpu 0000:44:00.0: amdgpu: SMU is resuming...
[  563.189001] amdgpu 0000:44:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[  563.189005] amdgpu 0000:44:00.0: amdgpu: SMU driver if version not matched
[  563.199714] amdgpu 0000:44:00.0: amdgpu: SMU is resumed successfully!
[  563.201010] [drm] DMUB hardware initialized: version=0x02020020
[  563.226214] [drm] kiq ring mec 2 pipe 1 q 0
[  563.230622] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  563.230786] [drm] JPEG decode initialized successfully.
[  563.230806] amdgpu 0000:44:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  563.230808] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  563.230810] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  563.230811] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  563.230813] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  563.230815] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  563.230816] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  563.230818] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  563.230820] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  563.230821] amdgpu 0000:44:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  563.230823] amdgpu 0000:44:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  563.230825] amdgpu 0000:44:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  563.230826] amdgpu 0000:44:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  563.230828] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  563.230830] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  563.230831] amdgpu 0000:44:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  563.233770] amdgpu 0000:44:00.0: [drm] Cannot find any crtc or sizes
[  575.645976] amdgpu 0000:0b:00.0: Using 44-bit DMA addresses
[  629.844070] gmc_v10_0_process_interrupt: 41 callbacks suppressed
[  629.844077] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844087] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f5279bab000 from client 0x1b (UTCL2)
[  629.844091] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844094] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844098] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844100] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844103] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844106] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844108] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844115] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844120] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f52897c0000 from client 0x1b (UTCL2)
[  629.844124] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844127] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844130] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844132] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844135] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844137] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844140] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844144] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844149] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f527983d000 from client 0x1b (UTCL2)
[  629.844153] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844156] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844159] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844161] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844164] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844166] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844169] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844173] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844178] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f52897ae000 from client 0x1b (UTCL2)
[  629.844181] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844184] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844187] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844190] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844192] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844195] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844197] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844201] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844206] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f527989a000 from client 0x1b (UTCL2)
[  629.844209] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844212] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844215] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844218] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844220] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844223] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844225] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844229] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844234] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f52798a0000 from client 0x1b (UTCL2)
[  629.844237] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844240] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844243] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844245] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844248] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844251] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844253] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844257] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844262] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f52799b7000 from client 0x1b (UTCL2)
[  629.844265] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844268] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844271] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844273] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844276] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844278] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844281] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844285] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844290] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f5279827000 from client 0x1b (UTCL2)
[  629.844293] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844296] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844298] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844301] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844304] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844306] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844309] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844312] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844317] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f52b97a4000 from client 0x1b (UTCL2)
[  629.844321] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844323] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844326] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844329] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844331] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844334] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844336] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.844340] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770, for process python pid 1796 thread python pid 1796)
[  629.844345] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f52b97af000 from client 0x1b (UTCL2)
[  629.844348] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0xFFFFFFFF
[  629.844351] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: unknown (0x1ff)
[  629.844354] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  629.844356] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x7
[  629.844359] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xf
[  629.844361] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  629.844364] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  629.918602] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.041587] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.164331] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.287072] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.409746] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.532437] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.655121] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.778313] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  630.901365] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  631.099700] amdgpu 0000:0b:00.0: amdgpu: wait for kiq fence error: 0.
[  638.844262] amdgpu: qcm fence wait loop timeout expired
[  638.844265] amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[  638.844325] amdgpu 0000:0b:00.0: amdgpu: GPU reset begin!
[  638.844647] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:41 param:0x00000000 message:DisallowGfxOff?
[  638.844654] amdgpu 0000:0b:00.0: amdgpu: Failed to disable gfxoff!
[  639.214337] amdgpu 0000:0b:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring kiq_0.2.1.0 test failed (-110)
[  639.214608] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* KGQ disable failed
[  639.389325] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[  639.389637] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:7 param:0x00000000 message:DisableAllSmuFeatures?
[  639.389640] amdgpu 0000:0b:00.0: amdgpu: Failed to disable smu features.
[  639.389642] amdgpu 0000:0b:00.0: amdgpu: Fail to disable dpm features!
[  639.389644] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <smu> failed -121
[  639.389876] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 00000000ebe5336b; ring_buffer_end = 00000000b0f8223e; write_frame = 000000007d11fba2
[  639.390130] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
[  639.390387] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate hdcp ta
[  639.390639] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[  639.391896] amdgpu 0000:0b:00.0: amdgpu: MODE1 reset
[  639.391899] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset
[  639.392485] amdgpu 0000:0b:00.0: amdgpu: GPU smu mode1 reset
[  639.392487] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:48 param:0x00000000 message:Mode1Reset?
[  639.392489] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset failed
[  639.392491] amdgpu 0000:0b:00.0: amdgpu: ASIC reset failed with error, -121 for drm dev, 0000:0b:00.0
[  649.968075] amdgpu 0000:0b:00.0: amdgpu: GPU reset succeeded, trying to resume
[  649.968210] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  649.968330] [drm] VRAM is lost due to GPU reset!
[  649.968333] [drm] PSP is resuming...
[  650.160197] [drm:psp_hw_start [amdgpu]] *ERROR* PSP create ring failed!
[  650.160459] [drm:psp_resume [amdgpu]] *ERROR* PSP resume failed
[  650.160703] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[  650.160935] amdgpu 0000:0b:00.0: amdgpu: GPU reset(1) failed
[  650.161112] [drm] Skip scheduling IBs!
[  650.161127] [drm] Skip scheduling IBs!
[  650.164451] [drm] Skip scheduling IBs!
[  650.164458] [drm] Skip scheduling IBs!
[  659.161269] amdgpu: qcm fence wait loop timeout expired
[  659.161272] amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[  659.161299] snd_hda_intel 0000:0b:00.1: Unable to change power state from D3hot to D0, device inaccessible
[  659.164916] [drm] Skip scheduling IBs!
[  659.164928] [drm] Skip scheduling IBs!
[  659.169157] [drm] Skip scheduling IBs!
[  659.169162] [drm] Skip scheduling IBs!
[  659.173786] [drm] Skip scheduling IBs!
[  659.173791] [drm] Skip scheduling IBs!
[  659.178155] [drm] Skip scheduling IBs!
[  659.178159] [drm] Skip scheduling IBs!
[  659.182197] [drm] Skip scheduling IBs!
[  659.182202] [drm] Skip scheduling IBs!
[  659.182229] [drm] Skip scheduling IBs!
[  659.182232] [drm] Skip scheduling IBs!
[  659.182243] [drm] Skip scheduling IBs!
[  659.182246] [drm] Skip scheduling IBs!
[  659.182249] [drm] Skip scheduling IBs!
[  659.182251] [drm] Skip scheduling IBs!
[  659.186826] [drm] Skip scheduling IBs!
[  659.186831] [drm] Skip scheduling IBs!
[  659.193453] [drm] Skip scheduling IBs!
[  659.193460] [drm] Skip scheduling IBs!
[  659.197826] [drm] Skip scheduling IBs!
[  659.197831] [drm] Skip scheduling IBs!
[  659.202086] [drm] Skip scheduling IBs!
[  659.202091] [drm] Skip scheduling IBs!
[  659.225760] [drm] Skip scheduling IBs!
[  659.225774] [drm] Skip scheduling IBs!
[  659.230165] [drm] Skip scheduling IBs!
[  659.230169] [drm] Skip scheduling IBs!
[  659.234387] [drm] Skip scheduling IBs!
[  659.234393] [drm] Skip scheduling IBs!
[  659.234563] [drm] Skip scheduling IBs!
[  659.234565] [drm] Skip scheduling IBs!
[  659.234582] [drm] Skip scheduling IBs!
[  659.234585] [drm] Skip scheduling IBs!
[  659.325103] snd_hda_intel 0000:0b:00.1: CORB reset timeout#2, CORBRP = 65535
[  659.325114] amdgpu 0000:0b:00.0: amdgpu: GPU reset end with ret = -62
[  659.325117] amdgpu 0000:0b:00.0: amdgpu: GPU reset begin!
[  659.806654] amdgpu 0000:0b:00.0: amdgpu: Failed to disallow df cstate
[  713.395581] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  713.395603] [drm] PSP is resuming...
[  713.463226] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[  713.564390] amdgpu 0000:44:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  713.578035] amdgpu 0000:44:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  713.578039] amdgpu 0000:44:00.0: amdgpu: SMU is resuming...
[  713.578043] amdgpu 0000:44:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[  713.578047] amdgpu 0000:44:00.0: amdgpu: SMU driver if version not matched
[  713.589654] amdgpu 0000:44:00.0: amdgpu: SMU is resumed successfully!
[  713.590952] [drm] DMUB hardware initialized: version=0x02020020
[  713.616876] [drm] kiq ring mec 2 pipe 1 q 0
[  713.621555] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  713.621702] [drm] JPEG decode initialized successfully.
[  713.621722] amdgpu 0000:44:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  713.621724] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  713.621726] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  713.621728] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  713.621730] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  713.621732] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  713.621734] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  713.621735] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  713.621737] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  713.621739] amdgpu 0000:44:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  713.621741] amdgpu 0000:44:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  713.621742] amdgpu 0000:44:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  713.621744] amdgpu 0000:44:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  713.621746] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  713.621748] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  713.621749] amdgpu 0000:44:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  713.624862] amdgpu 0000:44:00.0: [drm] Cannot find any crtc or sizes
[  719.560290] [drm] evicting device resources failed
[  737.642599] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  737.642620] [drm] PSP is resuming...
[  737.710224] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[  737.810388] amdgpu 0000:44:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  737.824032] amdgpu 0000:44:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  737.824037] amdgpu 0000:44:00.0: amdgpu: SMU is resuming...
[  737.824040] amdgpu 0000:44:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[  737.824044] amdgpu 0000:44:00.0: amdgpu: SMU driver if version not matched
[  737.833990] amdgpu 0000:44:00.0: amdgpu: SMU is resumed successfully!
[  737.835289] [drm] DMUB hardware initialized: version=0x02020020
[  737.860320] [drm] kiq ring mec 2 pipe 1 q 0
[  737.865389] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  737.865683] [drm] JPEG decode initialized successfully.
[  737.865703] amdgpu 0000:44:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  737.865706] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  737.865708] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  737.865710] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  737.865712] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  737.865714] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  737.865716] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  737.865717] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  737.865719] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  737.865721] amdgpu 0000:44:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  737.865723] amdgpu 0000:44:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  737.865725] amdgpu 0000:44:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  737.865726] amdgpu 0000:44:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  737.865728] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  737.865730] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  737.865731] amdgpu 0000:44:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  737.869921] amdgpu 0000:44:00.0: [drm] Cannot find any crtc or sizes
[ 1154.831892] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[ 1154.831915] [drm] PSP is resuming...
[ 1154.899599] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[ 1155.000597] amdgpu 0000:44:00.0: amdgpu: RAS: optional ras ta ucode is not available
[ 1155.014286] amdgpu 0000:44:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[ 1155.014289] amdgpu 0000:44:00.0: amdgpu: SMU is resuming...
[ 1155.014294] amdgpu 0000:44:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[ 1155.014297] amdgpu 0000:44:00.0: amdgpu: SMU driver if version not matched
[ 1155.025088] amdgpu 0000:44:00.0: amdgpu: SMU is resumed successfully!
[ 1155.026392] [drm] DMUB hardware initialized: version=0x02020020
[ 1155.051720] [drm] kiq ring mec 2 pipe 1 q 0
[ 1155.056111] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[ 1155.056294] [drm] JPEG decode initialized successfully.
[ 1155.056314] amdgpu 0000:44:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 1155.056316] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 1155.056318] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 1155.056320] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[ 1155.056322] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[ 1155.056324] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[ 1155.056325] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[ 1155.056327] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[ 1155.056329] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[ 1155.056330] amdgpu 0000:44:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[ 1155.056332] amdgpu 0000:44:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 1155.056334] amdgpu 0000:44:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[ 1155.056335] amdgpu 0000:44:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[ 1155.056337] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[ 1155.056339] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[ 1155.056340] amdgpu 0000:44:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[ 1155.059212] amdgpu 0000:44:00.0: [drm] Cannot find any crtc or sizes
```

---

### 评论 #5 — nix-wolf (2024-01-14T00:08:01Z)

I upgraded the Docker Container to rocm 6, and the python env to 5.7 revleaing these errors, i was able to run the scripts on both gpus, one several times with no issues (other then OOM but thats not what im concerned about direct), i hit rocm-smi just to check the stats on the gpu and it crashed the first gpu again, not the second

```
 4727.652056] amdgpu 0000:0b:00.0: [drm] Cannot find any crtc or sizes
[ 4727.833859] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[ 4727.833878] [drm] PSP is resuming...
[ 4727.901608] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[ 4728.001698] amdgpu 0000:44:00.0: amdgpu: RAS: optional ras ta ucode is not available
[ 4728.015298] amdgpu 0000:44:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[ 4728.015302] amdgpu 0000:44:00.0: amdgpu: SMU is resuming...
[ 4728.015306] amdgpu 0000:44:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[ 4728.015310] amdgpu 0000:44:00.0: amdgpu: SMU driver if version not matched
[ 4728.027522] amdgpu 0000:44:00.0: amdgpu: SMU is resumed successfully!
[ 4728.028819] [drm] DMUB hardware initialized: version=0x02020020
[ 4728.053834] [drm] kiq ring mec 2 pipe 1 q 0
[ 4728.058805] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[ 4728.059145] [drm] JPEG decode initialized successfully.
[ 4728.059165] amdgpu 0000:44:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 4728.059168] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 4728.059170] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 4728.059172] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[ 4728.059174] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[ 4728.059176] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[ 4728.059177] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[ 4728.059179] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[ 4728.059181] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[ 4728.059183] amdgpu 0000:44:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[ 4728.059184] amdgpu 0000:44:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 4728.059186] amdgpu 0000:44:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[ 4728.059188] amdgpu 0000:44:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[ 4728.059189] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[ 4728.059191] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[ 4728.059193] amdgpu 0000:44:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[ 4728.062704] amdgpu 0000:44:00.0: [drm] Cannot find any crtc or sizes
[ 4736.783974] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:40 param:0x00000000 message:AllowGfxOff?
[ 4736.783983] amdgpu 0000:0b:00.0: amdgpu: Failed to enable gfxoff!
[ 4737.284827] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 4737.284835] amdgpu 0000:0b:00.0: amdgpu: Failed to export SMU metrics table!
[ 4737.284990] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 4737.284994] amdgpu 0000:0b:00.0: amdgpu: Failed to export SMU metrics table!
[ 4737.289317] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 4737.289322] amdgpu 0000:0b:00.0: amdgpu: Failed to export SMU metrics table!
[ 4737.289387] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 4737.289390] amdgpu 0000:0b:00.0: amdgpu: Failed to export SMU metrics table!
[ 4737.289599] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:13 param:0x00000000 message:GetEnabledSmuFeaturesHigh?
[ 4737.289603] amdgpu 0000:0b:00.0: amdgpu: Failed to retrieve enabled ppfeatures!
[ 4737.289630] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:13 param:0x00000000 message:GetEnabledSmuFeaturesHigh?
[ 4737.289633] amdgpu 0000:0b:00.0: amdgpu: Failed to retrieve enabled ppfeatures!
[ 4737.289677] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 4737.289680] amdgpu 0000:0b:00.0: amdgpu: Failed to export SMU metrics table!
[ 4737.289764] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 4737.289767] amdgpu 0000:0b:00.0: amdgpu: Failed to export SMU metrics table!
[ 4746.079958] amdgpu: qcm fence wait loop timeout expired
[ 4746.079963] amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[ 4746.079966] amdgpu: Failed to evict process queues
[ 4746.080004] amdgpu 0000:0b:00.0: amdgpu: GPU reset begin!
[ 4746.449293] amdgpu 0000:0b:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring kiq_0.2.1.0 test failed (-110)
[ 4746.449562] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* KGQ disable failed
[ 4746.623619] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[ 4746.623943] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:7 param:0x00000000 message:DisableAllSmuFeatures?
[ 4746.623947] amdgpu 0000:0b:00.0: amdgpu: Failed to disable smu features.
[ 4746.623950] amdgpu 0000:0b:00.0: amdgpu: Fail to disable dpm features!
[ 4746.623952] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <smu> failed -121
[ 4746.624198] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 00000000b8f9896b; ring_buffer_end = 00000000e1253f89; write_frame = 0000000011badcda
[ 4746.624456] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
[ 4746.624712] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate hdcp ta
[ 4746.624973] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[ 4746.626236] amdgpu 0000:0b:00.0: amdgpu: MODE1 reset
[ 4746.626239] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset
[ 4746.626817] amdgpu 0000:0b:00.0: amdgpu: GPU smu mode1 reset
[ 4746.626819] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:48 param:0x00000000 message:Mode1Reset?
[ 4746.626822] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset failed
[ 4746.626823] amdgpu 0000:0b:00.0: amdgpu: ASIC reset failed with error, -121 for drm dev, 0000:0b:00.0
[ 4757.193919] amdgpu 0000:0b:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 4757.194048] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[ 4757.194111] [drm] VRAM is lost due to GPU reset!
[ 4757.194112] [drm] PSP is resuming...
[ 4757.387630] [drm:psp_hw_start [amdgpu]] *ERROR* PSP create ring failed!
[ 4757.387906] [drm:psp_resume [amdgpu]] *ERROR* PSP resume failed
[ 4757.388159] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[ 4757.388394] amdgpu 0000:0b:00.0: amdgpu: GPU reset(1) failed
[ 4766.388969] amdgpu: qcm fence wait loop timeout expired
[ 4766.388971] amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[ 4766.388999] snd_hda_intel 0000:0b:00.1: Unable to change power state from D3hot to D0, device inaccessible
[ 4766.552810] snd_hda_intel 0000:0b:00.1: CORB reset timeout#2, CORBRP = 65535
[ 4766.552822] amdgpu 0000:0b:00.0: amdgpu: GPU reset end with ret = -62
[ 4766.552825] amdgpu 0000:0b:00.0: amdgpu: GPU reset begin!
[ 4767.033794] amdgpu 0000:0b:00.0: amdgpu: Failed to disallow df cstate
```

---

### 评论 #6 — nix-wolf (2024-01-14T01:43:43Z)

Isolated the acctual hand/crash, i did see this in the other one but i figured some of that, least from my research. I have been still getting the second gpu to run things successfully, still gpu one thats failing. THIS TIME it failed with the fans on full tilt 

this was with amdgpu22.2, rocm6(docker) && rocm5.7 py-env still just getting OOM issues on gpu 2 but program finishs and exits just fine..
```
[ 5662.665041] amdgpu: qcm fence wait loop timeout expired
[ 5662.665046] amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[ 5662.665049] amdgpu: Failed to evict process queues
[ 5662.667089] amdgpu 0000:0b:00.0: amdgpu: GPU reset begin!
[ 5662.667367] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:41 param:0x00000000 message:DisallowGfxOff?
[ 5662.667375] amdgpu 0000:0b:00.0: amdgpu: Failed to disable gfxoff!
[ 5663.035357] amdgpu 0000:0b:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring kiq_0.2.1.0 test failed (-110)
[ 5663.035621] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* KGQ disable failed
[ 5663.208959] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[ 5663.209276] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:7 param:0x00000000 message:DisableAllSmuFeatures?
[ 5663.209280] amdgpu 0000:0b:00.0: amdgpu: Failed to disable smu features.
[ 5663.209283] amdgpu 0000:0b:00.0: amdgpu: Fail to disable dpm features!
[ 5663.209284] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <smu> failed -121
[ 5663.209516] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 00000000516e3879; ring_buffer_end = 0000000052123b2f; write_frame = 0000000078035dff
[ 5663.209771] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
[ 5663.210024] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate hdcp ta
[ 5663.210281] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[ 5663.211538] amdgpu 0000:0b:00.0: amdgpu: MODE1 reset
[ 5663.211542] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset
[ 5663.212130] amdgpu 0000:0b:00.0: amdgpu: GPU smu mode1 reset
[ 5663.212133] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:48 param:0x00000000 message:Mode1Reset?
[ 5663.212136] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset failed
[ 5663.212138] amdgpu 0000:0b:00.0: amdgpu: ASIC reset failed with error, -121 for drm dev, 0000:0b:00.0
```

i do believe in my search so far i have come across a bunch  of stuff in old email lists (2018) in regards to mode1reset and smu, also another thing i noticed(not with these versions of the software the first run with 6.0&&5.7 rocm with amdgpu 21.5) was that rocm-smi would cause the crash if it was called while it was doing something, if i didnt call it to check what everything was, it would run and exit properly... i did notice some similar things in the orginal software setup, but i had a hunch there was an association as sometimes it would be fine, and sometimes it would fail right as id run it. but seemingly its more apparent now


---

### 评论 #7 — nix-wolf (2024-01-14T03:01:55Z)

Rebuilt the container from scratch with amdgpu 22.40, and rocm6.0 with pytorch2.1.3 and rocm5.7 and with running the commands listed above, i was able to get through a basic pipe to image generation with no fail, and no OOM issues, was offloading to cpu but only reserver 1.5 gb which acctually look significantly better then before since prior i even had issues with it OOM on a basic pipe. BUT i was able to produce the outputs from the enviroment variables. at least im pretty sure i was able to cause i had not seen them before in all my runs of this, it all kicked out to dmesg, and there is a lot of info here. this is the extracted important stuff the rest is stuff ive been staring at for days. hopefully this helps you guys track down the issue when you get around to looking.

in this case it was the first gpu still causing the entire thing to crash, but i was acctually running everything on the second gpu specifically, given that ive known that it will still crash. i also find it interesting from my last post that the base first 20 lines was more or less exactly what was posted.

```
 2168.276740] amdgpu 0000:0b:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring kiq_0.2.1.0 test failed (-110)
[ 2168.277009] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* KGQ disable failed
[ 2168.448670] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[ 2168.450050] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:13 param:0x00000000 message:GetEnabledSmuFeaturesHigh?
[ 2168.450054] amdgpu 0000:0b:00.0: amdgpu: Failed to retrieve enabled ppfeatures!
[ 2168.450056] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:7 param:0x00000000 message:DisableAllSmuFeatures?
[ 2168.450058] amdgpu 0000:0b:00.0: amdgpu: Failed to disable smu features.
[ 2168.450060] amdgpu 0000:0b:00.0: amdgpu: Fail to disable dpm features!
[ 2168.450061] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <smu> failed -121
[ 2168.450287] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 0000000078fc582b; ring_buffer_end = 00000000a7f8d166; write_frame = 000000005a019303
[ 2168.450529] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
[ 2168.450768] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate hdcp ta
[ 2168.451011] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[ 2168.452274] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:13 param:0x00000000 message:GetEnabledSmuFeaturesHigh?
[ 2168.452277] amdgpu 0000:0b:00.0: amdgpu: Failed to retrieve enabled ppfeatures!
[ 2168.452875] amdgpu 0000:0b:00.0: Unable to change power state from D0 to D3hot, device inaccessible
[ 2168.453478] pcieport 0000:0a:00.0: Unable to change power state from D0 to D3hot, device inaccessible
[ 2168.454065] pcieport 0000:09:00.0: Unable to change power state from D0 to D3hot, device inaccessible
[ 2319.763665] pcieport 0000:09:00.0: Unable to change power state from D3cold to D0, device inaccessible
[ 2319.764574] pcieport 0000:0a:00.0: Unable to change power state from D3cold to D0, device inaccessible
[ 2322.098459] amdgpu 0000:0b:00.0: not ready 1023ms after resume; waiting
[ 2323.186462] amdgpu 0000:0b:00.0: not ready 2047ms after resume; waiting
[ 2325.298469] amdgpu 0000:0b:00.0: not ready 4095ms after resume; waiting
[ 2329.906485] amdgpu 0000:0b:00.0: not ready 8191ms after resume; waiting
[ 2338.610508] amdgpu 0000:0b:00.0: not ready 16383ms after resume; waiting
[ 2355.506556] amdgpu 0000:0b:00.0: not ready 32767ms after resume; waiting
[ 2388.786666] amdgpu 0000:0b:00.0: not ready 65535ms after resume; giving up
[ 2388.786693] amdgpu 0000:0b:00.0: Unable to change power state from D3cold to D0, device inaccessible
[ 2399.320469] [drm:gmc_v10_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for VM flush hub: 0!
[ 2399.467311] [drm:gmc_v10_0_flush_vm_hub.constprop.0 [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[ 2399.613790] [drm:gmc_v10_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for VM flush hub: 8!
[ 2399.761364] [drm:gmc_v10_0_flush_vm_hub.constprop.0 [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[ 2399.908433] [drm:gmc_v10_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for VM flush hub: 8!
[ 2400.054825] [drm:gmc_v10_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for VM flush hub: 0!
[ 2400.055073] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[ 2400.055112] [drm] PSP is resuming...
[ 2400.095407] [drm] reserve 0xa00000 from 0x82fd000000 for PSP TMR
[ 2400.095473] amdgpu 0000:0b:00.0: amdgpu: RAS: optional ras ta ucode is not available
[ 2400.095615] ------------[ cut here ]------------
[ 2400.095616] WARNING: CPU: 5 PID: 2010 at drivers/gpu/drm/amd/amdgpu/amdgpu_object.c:444 amdgpu_bo_free_kernel+0xf9/0x120 [amdgpu]
[ 2400.095858] Modules linked in: veth xt_conntrack xt_MASQUERADE nf_conntrack_netlink xt_addrtype nft_compat br_netfilter bridge stp llc overlay nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nf_tables nfnetlink sunrpc snd_hda_codec_realtek snd_hda_codec_generic intel_rapl_msr snd_hda_codec_hdmi intel_rapl_common edac_mce_amd snd_hda_intel snd_intel_dspcfg snd_intel_sdw_acpi kvm_amd snd_hda_codec vfat fat snd_hda_core kvm asus_wmi_sensors snd_hwdep irqbypass eeepc_wmi asus_wmi snd_pcm ledtrig_audio rapl sparse_keymap platform_profile rfkill snd_timer wmi_bmof mxm_wmi snd acpi_cpufreq soundcore k10temp i2c_piix4 gpio_amdpt joydev gpio_generic loop zram xfs amdgpu crct10dif_pclmul crc32_pclmul drm_ttm_helper crc32c_intel polyval_clmulni ttm polyval_generic video drm_exec drm_suballoc_helper ghash_clmulni_intel amdxcp drm_buddy sha512_ssse3 nvme gpu_sched sha256_ssse3 igb nvme_core sha1_ssse3
[ 2400.095939]  drm_display_helper dca nvme_common cec ccp sp5100_tco i2c_algo_bit wmi scsi_dh_rdac scsi_dh_emc scsi_dh_alua ip6_tables ip_tables dm_multipath fuse
[ 2400.095957] CPU: 5 PID: 2010 Comm: python Not tainted 6.6.9-200.fc39.x86_64 #1
[ 2400.095960] Hardware name: System manufacturer System Product Name/PRIME X399-A, BIOS 1203 10/09/2019
[ 2400.095962] RIP: 0010:amdgpu_bo_free_kernel+0xf9/0x120 [amdgpu]
[ 2400.096193] Code: 00 00 00 4d 85 e4 74 08 49 c7 04 24 00 00 00 00 48 85 ed 74 08 48 c7 45 00 00 00 00 00 5b 5d 41 5c 41 5d 41 5e e9 b7 31 8e ca <0f> 0b e9 3b ff ff ff 3d 00 fe ff ff 74 b3 49 8b be 20 11 ff ff 4c
[ 2400.096195] RSP: 0018:ffffc90014d8b8a8 EFLAGS: 00010202
[ 2400.096197] RAX: ffff88810f888000 RBX: ffff8881138bf2b8 RCX: 00000082fec03000
[ 2400.096199] RDX: ffff8881138bf2c8 RSI: ffff8881138bf2c0 RDI: ffff8881138bf2b8
[ 2400.096201] RBP: ffff8881138bf2c8 R08: ffff8881138bf2f8 R09: a7442cf7d8701f6c
[ 2400.096202] R10: 41861e9f03a4a8d6 R11: d039246902ac74e7 R12: ffff8881138bf2c0
[ 2400.096203] R13: ffff888103f6e000 R14: ffff88811388eee0 R15: ffff88810f888000
[ 2400.096205] FS:  00007f6e08dbf740(0000) GS:ffff889456c40000(0000) knlGS:0000000000000000
[ 2400.096207] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[ 2400.096208] CR2: 0000555cc894f508 CR3: 0000000e5bcf2000 CR4: 00000000003506e0
[ 2400.096210] Call Trace:
[ 2400.096213]  <TASK>
[ 2400.096215]  ? amdgpu_bo_free_kernel+0xf9/0x120 [amdgpu]
[ 2400.096445]  ? __warn+0x81/0x130
[ 2400.096452]  ? amdgpu_bo_free_kernel+0xf9/0x120 [amdgpu]
[ 2400.096691]  ? report_bug+0x171/0x1a0
[ 2400.096699]  ? handle_bug+0x3c/0x80
[ 2400.096703]  ? exc_invalid_op+0x17/0x70
[ 2400.096705]  ? asm_exc_invalid_op+0x1a/0x20
[ 2400.096712]  ? amdgpu_bo_free_kernel+0xf9/0x120 [amdgpu]
[ 2400.096946]  psp_rap_initialize+0x171/0x1e0 [amdgpu]
[ 2400.097198]  psp_resume+0x15b/0x260 [amdgpu]
[ 2400.097447]  amdgpu_device_fw_loading+0x7c/0x150 [amdgpu]
[ 2400.097680]  amdgpu_device_resume+0x96/0x2b0 [amdgpu]
[ 2400.097906]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2400.097912]  amdgpu_pmops_runtime_resume+0x82/0xf0 [amdgpu]
[ 2400.098137]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2400.098139]  __rpm_callback+0x44/0x170
[ 2400.098144]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2400.098147]  rpm_callback+0x5d/0x70
[ 2400.098150]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2400.098152]  rpm_resume+0x56e/0x7b0
[ 2400.098154]  ? __flush_work.isra.0+0x1aa/0x280
[ 2400.098160]  __pm_runtime_resume+0x4b/0x80
[ 2400.098163]  amdgpu_driver_open_kms+0x50/0x270 [amdgpu]
[ 2400.098391]  drm_file_alloc+0x1b7/0x260
[ 2400.098396]  drm_open_helper+0x7e/0x150
[ 2400.098400]  drm_open+0x7f/0x140
[ 2400.098403]  drm_stub_open+0xae/0xe0
[ 2400.098408]  chrdev_open+0xce/0x250
[ 2400.098413]  ? __pfx_chrdev_open+0x10/0x10
[ 2400.098416]  do_dentry_open+0x203/0x4f0
[ 2400.098420]  path_openat+0xafe/0x1160
[ 2400.098426]  ? __mod_memcg_lruvec_state+0x4e/0xa0
[ 2400.098430]  ? __mod_lruvec_page_state+0x99/0x130
[ 2400.098434]  do_filp_open+0xb3/0x160
[ 2400.098442]  do_sys_openat2+0xab/0xe0
[ 2400.098446]  __x64_sys_open+0x59/0xa0
[ 2400.098450]  do_syscall_64+0x60/0x90
[ 2400.098456]  ? srso_return_thunk+0x5/0x10
[ 2400.098459]  ? __count_memcg_events+0x42/0x90
[ 2400.098462]  ? srso_return_thunk+0x5/0x10
[ 2400.098464]  ? count_memcg_events.constprop.0+0x1a/0x30
[ 2400.098467]  ? srso_return_thunk+0x5/0x10
[ 2400.098469]  ? handle_mm_fault+0xa2/0x360
[ 2400.098473]  ? srso_return_thunk+0x5/0x10
[ 2400.098474]  ? do_user_addr_fault+0x30f/0x660
[ 2400.098479]  ? srso_return_thunk+0x5/0x10
[ 2400.098481]  ? exc_page_fault+0x7f/0x180
[ 2400.098484]  entry_SYSCALL_64_after_hwframe+0x6e/0xd8
[ 2400.098488] RIP: 0033:0x7f6e08295efd
[ 2400.098510] Code: c5 20 00 00 75 10 b8 02 00 00 00 0f 05 48 3d 01 f0 ff ff 73 31 c3 48 83 ec 08 e8 4e f5 ff ff 48 89 04 24 b8 02 00 00 00 0f 05 <48> 8b 3c 24 48 89 c2 e8 97 f5 ff ff 48 89 d0 48 83 c4 08 48 3d 01
[ 2400.098512] RSP: 002b:00007ffdf4cd6750 EFLAGS: 00000293 ORIG_RAX: 0000000000000002
[ 2400.098515] RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007f6e08295efd
[ 2400.098517] RDX: 00007ffdf4cd6783 RSI: 0000000000080002 RDI: 00007ffdf4cd6770
[ 2400.098518] RBP: 0000000000000000 R08: 00007f6e0803b3e0 R09: 00007f6e07f062cd
[ 2400.098520] R10: 00007f6d59a0751e R11: 0000000000000293 R12: 00007f6d59d86d40
[ 2400.098521] R13: 00007ffdf4cd6770 R14: 00007ffdf4cd6834 R15: 0000555cceb9d8dc
[ 2400.098526]  </TASK>
[ 2400.098527] ---[ end trace 0000000000000000 ]---
[ 2400.098542] amdgpu 0000:0b:00.0: amdgpu: RAP TA initialize fail (0) status -1.
[ 2400.098544] amdgpu 0000:0b:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[ 2400.098547] amdgpu 0000:0b:00.0: amdgpu: SMU is resuming...
[ 2400.098550] amdgpu 0000:0b:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413b00 (65.59.0)
[ 2400.098554] amdgpu 0000:0b:00.0: amdgpu: SMU driver if version not matched
[ 2400.098558] amdgpu 0000:0b:00.0: amdgpu: dpm has been disabled
[ 2400.098564] amdgpu 0000:0b:00.0: amdgpu: SMU is resumed successfully!
[ 2400.098600] [drm] DMUB unsupported on ASIC
[ 2405.349865] ------------[ cut here ]------------
[ 2405.349867] WARNING: CPU: 5 PID: 2010 at drivers/gpu/drm/amd/amdgpu/../display/dc/dcn20/dcn20_hubbub.c:566 hubbub2_get_dchub_ref_freq+0xa0/0xc0 [amdgpu]
[ 2405.350174] Modules linked in: veth xt_conntrack xt_MASQUERADE nf_conntrack_netlink xt_addrtype nft_compat br_netfilter bridge stp llc overlay nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nf_tables nfnetlink sunrpc snd_hda_codec_realtek snd_hda_codec_generic intel_rapl_msr snd_hda_codec_hdmi intel_rapl_common edac_mce_amd snd_hda_intel snd_intel_dspcfg snd_intel_sdw_acpi kvm_amd snd_hda_codec vfat fat snd_hda_core kvm asus_wmi_sensors snd_hwdep irqbypass eeepc_wmi asus_wmi snd_pcm ledtrig_audio rapl sparse_keymap platform_profile rfkill snd_timer wmi_bmof mxm_wmi snd acpi_cpufreq soundcore k10temp i2c_piix4 gpio_amdpt joydev gpio_generic loop zram xfs amdgpu crct10dif_pclmul crc32_pclmul drm_ttm_helper crc32c_intel polyval_clmulni ttm polyval_generic video drm_exec drm_suballoc_helper ghash_clmulni_intel amdxcp drm_buddy sha512_ssse3 nvme gpu_sched sha256_ssse3 igb nvme_core sha1_ssse3
[ 2405.350243]  drm_display_helper dca nvme_common cec ccp sp5100_tco i2c_algo_bit wmi scsi_dh_rdac scsi_dh_emc scsi_dh_alua ip6_tables ip_tables dm_multipath fuse
[ 2405.350256] CPU: 5 PID: 2010 Comm: python Tainted: G        W          6.6.9-200.fc39.x86_64 #1
[ 2405.350259] Hardware name: System manufacturer System Product Name/PRIME X399-A, BIOS 1203 10/09/2019
[ 2405.350260] RIP: 0010:hubbub2_get_dchub_ref_freq+0xa0/0xc0 [amdgpu]
[ 2405.350542] Code: 83 c0 63 ff ff 3d 20 4e 00 00 77 22 89 5d 00 48 8b 44 24 08 65 48 2b 04 25 28 00 00 00 75 24 48 83 c4 10 5b 5d e9 00 a2 4a ca <0f> 0b eb de 0f 0b eb da d1 eb 8d 83 c0 63 ff ff 3d 20 4e 00 00 76
[ 2405.350543] RSP: 0018:ffffc90014d8b7e0 EFLAGS: 00010246
[ 2405.350546] RAX: 0000000000001000 RBX: 00000000000186a0 RCX: 0000000000000000
[ 2405.350547] RDX: ffffc90014d8b7e4 RSI: 00000000000039df RDI: ffff888113880000
[ 2405.350549] RBP: ffff888111f52ba0 R08: ffffc90014d8b7e0 R09: 000000000000000c
[ 2405.350550] R10: 0000000000000500 R11: ffff88947fdfdfe8 R12: ffff888111f52800
[ 2405.350552] R13: ffff8881049f9e00 R14: ffff888111f52c68 R15: ffff88810f888000
[ 2405.350554] FS:  00007f6e08dbf740(0000) GS:ffff889456c40000(0000) knlGS:0000000000000000
[ 2405.350556] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[ 2405.350557] CR2: 0000555cc894f508 CR3: 0000000e5bcf2000 CR4: 00000000003506e0
[ 2405.350559] Call Trace:
[ 2405.350562]  <TASK>
[ 2405.350563]  ? hubbub2_get_dchub_ref_freq+0xa0/0xc0 [amdgpu]
[ 2405.350852]  ? __warn+0x81/0x130
[ 2405.350856]  ? hubbub2_get_dchub_ref_freq+0xa0/0xc0 [amdgpu]
[ 2405.351138]  ? report_bug+0x171/0x1a0
[ 2405.351144]  ? handle_bug+0x3c/0x80
[ 2405.351147]  ? exc_invalid_op+0x17/0x70
[ 2405.351149]  ? asm_exc_invalid_op+0x1a/0x20
[ 2405.351156]  ? hubbub2_get_dchub_ref_freq+0xa0/0xc0 [amdgpu]
[ 2405.351438]  dcn30_init_hw+0x180/0x740 [amdgpu]
[ 2405.351720]  dc_set_power_state+0xf4/0x140 [amdgpu]
[ 2405.351987]  dm_resume+0xe5/0x850 [amdgpu]
[ 2405.352277]  ? srso_return_thunk+0x5/0x10
[ 2405.352280]  ? _dev_info+0x79/0xa0
[ 2405.352288]  amdgpu_device_ip_resume_phase2+0x52/0xc0 [amdgpu]
[ 2405.352514]  amdgpu_device_resume+0xa4/0x2b0 [amdgpu]
[ 2405.352747]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2405.352752]  amdgpu_pmops_runtime_resume+0x82/0xf0 [amdgpu]
[ 2405.352978]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2405.352981]  __rpm_callback+0x44/0x170
[ 2405.352985]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2405.352988]  rpm_callback+0x5d/0x70
[ 2405.352990]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[ 2405.352993]  rpm_resume+0x56e/0x7b0
[ 2405.352995]  ? __flush_work.isra.0+0x1aa/0x280
[ 2405.353000]  __pm_runtime_resume+0x4b/0x80
[ 2405.353003]  amdgpu_driver_open_kms+0x50/0x270 [amdgpu]
[ 2405.353232]  drm_file_alloc+0x1b7/0x260
[ 2405.353238]  drm_open_helper+0x7e/0x150
[ 2405.353241]  drm_open+0x7f/0x140
[ 2405.353244]  drm_stub_open+0xae/0xe0
[ 2405.353249]  chrdev_open+0xce/0x250
[ 2405.353253]  ? __pfx_chrdev_open+0x10/0x10
[ 2405.353256]  do_dentry_open+0x203/0x4f0
[ 2405.353260]  path_openat+0xafe/0x1160
[ 2405.353265]  ? __mod_memcg_lruvec_state+0x4e/0xa0
[ 2405.353269]  ? __mod_lruvec_page_state+0x99/0x130
[ 2405.353273]  do_filp_open+0xb3/0x160
[ 2405.353281]  do_sys_openat2+0xab/0xe0
[ 2405.353285]  __x64_sys_open+0x59/0xa0
[ 2405.353289]  do_syscall_64+0x60/0x90
[ 2405.353294]  ? srso_return_thunk+0x5/0x10
[ 2405.353296]  ? __count_memcg_events+0x42/0x90
[ 2405.353298]  ? srso_return_thunk+0x5/0x10
[ 2405.353300]  ? count_memcg_events.constprop.0+0x1a/0x30
[ 2405.353303]  ? srso_return_thunk+0x5/0x10
[ 2405.353305]  ? handle_mm_fault+0xa2/0x360
[ 2405.353309]  ? srso_return_thunk+0x5/0x10
[ 2405.353310]  ? do_user_addr_fault+0x30f/0x660
[ 2405.353314]  ? srso_return_thunk+0x5/0x10
[ 2405.353316]  ? exc_page_fault+0x7f/0x180
[ 2405.353319]  entry_SYSCALL_64_after_hwframe+0x6e/0xd8
[ 2405.353322] RIP: 0033:0x7f6e08295efd
[ 2405.353331] Code: c5 20 00 00 75 10 b8 02 00 00 00 0f 05 48 3d 01 f0 ff ff 73 31 c3 48 83 ec 08 e8 4e f5 ff ff 48 89 04 24 b8 02 00 00 00 0f 05 <48> 8b 3c 24 48 89 c2 e8 97 f5 ff ff 48 89 d0 48 83 c4 08 48 3d 01
[ 2405.353333] RSP: 002b:00007ffdf4cd6750 EFLAGS: 00000293 ORIG_RAX: 0000000000000002
[ 2405.353335] RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007f6e08295efd
[ 2405.353337] RDX: 00007ffdf4cd6783 RSI: 0000000000080002 RDI: 00007ffdf4cd6770
[ 2405.353338] RBP: 0000000000000000 R08: 00007f6e0803b3e0 R09: 00007f6e07f062cd
[ 2405.353340] R10: 00007f6d59a0751e R11: 0000000000000293 R12: 00007f6d59d86d40
[ 2405.353341] R13: 00007ffdf4cd6770 R14: 00007ffdf4cd6834 R15: 0000555cceb9d8dc
[ 2405.353346]  </TASK>
[ 2405.353347] ---[ end trace 0000000000000000 ]---
[ 2405.354857] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dpp_pg_control line:450
[ 2405.356343] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_hubp_pg_control line:524
[ 2405.357837] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dpp_pg_control line:458
[ 2405.359324] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_hubp_pg_control line:532
[ 2405.360817] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dpp_pg_control line:466
[ 2405.362302] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_hubp_pg_control line:540
[ 2405.363795] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dpp_pg_control line:474
[ 2405.365282] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_hubp_pg_control line:548
[ 2405.366778] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dpp_pg_control line:482
[ 2405.368260] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_hubp_pg_control line:556
[ 2405.369762] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dsc_pg_control line:379
[ 2405.371244] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dsc_pg_control line:387
[ 2405.372737] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dsc_pg_control line:395
[ 2405.374217] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dsc_pg_control line:403
[ 2405.375711] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dsc_pg_control line:411
[ 2405.377194] [drm] REG_WAIT timeout 1us * 1000 tries - dcn20_dsc_pg_control line:419
[ 2406.573303] amdgpu 0000:0b:00.0: amdgpu: rlc autoload: gc ucode autoload timeout
[ 2406.573307] [drm:amdgpu_device_ip_resume_phase2 [amdgpu]] *ERROR* resume of IP block <gfx_v10_0> failed -110
[ 2406.573537] amdgpu 0000:0b:00.0: amdgpu: amdgpu_device_ip_resume failed (-110).

```

---

### 评论 #8 — nix-wolf (2024-01-14T09:08:25Z)

I have run this now twice successfully on the first gpu in this configuration, i added AMD_LOG_LEVEL=4

give that the latter issues, when i have researched them are associated to gpu resets, or similar issues that have arose from gpus going to sleep  and not waking up properly, i wonder if the logging level at lvl 4 is circumventing the issue. I am piping this all to a log file, and sifting through this now and found this right at the top. two things also to note that the gpu is using a SIGNIFICANT amount less ram running this stuff in this configuration. as prior to this it would run 7.5gb, and crash with OOM trying to finalize the image created before sending it back for saving @ 4.5 gb (cause ive seen those numbers 100 times. now its only running 1.5gb.

but to note, im using gfx1030, but have a the 6750xt i believe is gfx1031
```
:1:hip_code_object.cpp      :516 : 1349537983 us: [pid:224   tid:0x7ff81ad1d740] hipErrorNoBinaryForGpu: Unable to find code object for all current devices!
:1:hip_code_object.cpp      :517 : 1349537997 us: [pid:224   tid:0x7ff81ad1d740]   Devices:
:1:hip_code_object.cpp      :520 : 1349538005 us: [pid:224   tid:0x7ff81ad1d740]     amdgcn-amd-amdhsa--gfx1030 - [Not Found]
:1:hip_code_object.cpp      :524 : 1349538008 us: [pid:224   tid:0x7ff81ad1d740]   Bundled Code Objects:
:1:hip_code_object.cpp      :540 : 1349538011 us: [pid:224   tid:0x7ff81ad1d740]     host-x86_64-unknown-linux-- - [Unsupported]
:1:hip_code_object.cpp      :538 : 1349538014 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack+]
:1:hip_code_object.cpp      :538 : 1349538017 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack-]
:1:hip_code_object.cpp      :538 : 1349538020 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx940:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx940:xnack+]
:1:hip_code_object.cpp      :538 : 1349538023 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx940:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx940:xnack-]
:1:hip_code_object.cpp      :538 : 1349538025 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx941:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx941:xnack+]
:1:hip_code_object.cpp      :538 : 1349538028 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx941:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx941:xnack-]
:1:hip_code_object.cpp      :538 : 1349538031 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx942:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx942:xnack+]
:1:hip_code_object.cpp      :538 : 1349538034 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx942:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx942:xnack-]
:1:hip_code_object.cpp      :544 : 1349538037 us: [pid:224   tid:0x7ff81ad1d740] hipErrorNoBinaryForGpu: Unable to find code object for all current devices! - 209
:1:hip_fatbin.cpp           :274 : 1349538040 us: [pid:224   tid:0x7ff81ad1d740] hipErrorNoBinaryForGpu: Couldn't find binary for ptr: 0xa7861000
:3:hip_platform.cpp         :672 : 1349538047 us: [pid:224   tid:0x7ff81ad1d740] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules

```

... nope false positive after running it a few more times and looking through stuff i realized only one gpu was on the system... apparently the other gpu died, accept i did check in the fresh install the cuda devices and there was two... so. as for no errors. but now that i have all this logging and kernel kick back stuff working mint. i should be able to find the answers...

and those answers, well she isnt bricked... i switched it to the next pice slot, 399x has 3 pcie full width busses and she is alive again!!! *fingers crossed?* 

---

### 评论 #9 — nix-wolf (2024-01-14T10:20:27Z)

```
[  869.722284] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  869.722428] [drm] JPEG decode initialized successfully.
[  869.722447] amdgpu 0000:44:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  869.722450] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  869.722452] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  869.722454] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  869.722456] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  869.722457] amdgpu 0000:44:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  869.722459] amdgpu 0000:44:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  869.722461] amdgpu 0000:44:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  869.722463] amdgpu 0000:44:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  869.722464] amdgpu 0000:44:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  869.722466] amdgpu 0000:44:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  869.722468] amdgpu 0000:44:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  869.722470] amdgpu 0000:44:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  869.722471] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  869.722473] amdgpu 0000:44:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  869.722475] amdgpu 0000:44:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  869.725447] amdgpu 0000:44:00.0: [drm] Cannot find any crtc or sizes
[  893.676492] gmc_v10_0_process_interrupt: 39 callbacks suppressed
[  893.676503] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32770, for process python pid 1991 thread python pid 1991)
[  893.676515] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00007f595b709000 from client 0x1b (UTCL2)
[  893.676521] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841050
[  893.676525] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  893.676529] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  893.676532] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  893.676535] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
[  893.676538] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  893.676541] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x1
[  893.676552] amdgpu 0000:0b:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:88 vmid:8 pasid:32770, for process python pid 1991 thread python pid 1991)
[  893.676558] amdgpu 0000:0b:00.0: amdgpu:   in page starting at address 0x00005e5e080c4000 from client 0x1b (UTCL2)
[  893.676563] amdgpu 0000:0b:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x008012B0
[  893.676566] amdgpu 0000:0b:00.0: amdgpu: 	 Faulty UTCL2 client ID: SQC (inst) (0x9)
[  893.676570] amdgpu 0000:0b:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  893.676572] amdgpu 0000:0b:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  893.676575] amdgpu 0000:0b:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xb
[  893.676578] amdgpu 0000:0b:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  893.676581] amdgpu 0000:0b:00.0: amdgpu: 	 RW: 0x0
[  902.677264] amdgpu: qcm fence wait loop timeout expired
[  902.677270] amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[  902.677319] amdgpu 0000:0b:00.0: amdgpu: GPU reset begin!
[  902.677566] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:41 param:0x00000000 message:DisallowGfxOff?
[  902.677575] amdgpu 0000:0b:00.0: amdgpu: Failed to disable gfxoff!
[  903.028604] amdgpu 0000:0b:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring kiq_0.2.1.0 test failed (-110)
[  903.028919] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* KGQ disable failed
[  903.197832] [drm:gfx_v10_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[  903.198169] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:7 param:0x00000000 message:DisableAllSmuFeatures?
[  903.198178] amdgpu 0000:0b:00.0: amdgpu: Failed to disable smu features.
[  903.198182] amdgpu 0000:0b:00.0: amdgpu: Fail to disable dpm features!
[  903.198185] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <smu> failed -121
[  903.198657] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 000000004ce49734; ring_buffer_end = 00000000c2f9e444; write_frame = 000000003419c927
[  903.199172] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
[  903.199692] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate hdcp ta
[  903.200204] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[  903.201665] amdgpu 0000:0b:00.0: amdgpu: MODE1 reset
[  903.201668] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset
[  903.202212] amdgpu 0000:0b:00.0: amdgpu: GPU smu mode1 reset
[  903.202214] amdgpu 0000:0b:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:48 param:0x00000000 message:Mode1Reset?
[  903.202218] amdgpu 0000:0b:00.0: amdgpu: GPU mode1 reset failed
[  903.202220] amdgpu 0000:0b:00.0: amdgpu: ASIC reset failed with error, -121 for drm dev, 0000:0b:00.0
[  913.744467] amdgpu 0000:0b:00.0: amdgpu: GPU reset succeeded, trying to resume
[  913.744588] [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
[  913.744689] [drm] VRAM is lost due to GPU reset!
[  913.744690] [drm] PSP is resuming...
[  913.933341] [drm:psp_hw_start [amdgpu]] *ERROR* PSP create ring failed!
[  913.933635] [drm:psp_resume [amdgpu]] *ERROR* PSP resume failed
[  913.933878] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[  913.934109] amdgpu 0000:0b:00.0: amdgpu: GPU reset(1) failed
[  913.934188] [drm] Skip scheduling IBs!
[  913.934194] [drm] Skip scheduling IBs!
[  913.935374] amdgpu: sq_intr: error, se 1, data 0x100000, sa 1, priv 1, wave_id 0, simd_id 1, wgp_id 1, err_type 2
[  913.935391] amdgpu: sq_intr: error, se 1, data 0x80000, sa 1, priv 1, wave_id 0, simd_id 3, wgp_id 1, err_type 1
[  913.935401] amdgpu: sq_intr: error, se 1, data 0x80000, sa 1, priv 1, wave_id 0, simd_id 2, wgp_id 1, err_type 1
[  922.934301] amdgpu: qcm fence wait loop timeout expired
[  922.934308] amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[  922.934344] snd_hda_intel 0000:0b:00.1: Unable to change power state from D3hot to D0, device inaccessible
[  922.934351] amdgpu: sq_intr: error, se 1, data 0x80000, sa 1, priv 1, wave_id 1, simd_id 1, wgp_id 1, err_type 1
[  922.934366] amdgpu: sq_intr: error, se 1, data 0x80000, sa 1, priv 1, wave_id 1, simd_id 2, wgp_id 1, err_type 1
[  922.934375] amdgpu: sq_intr: error, se 1, data 0x100000, sa 0, priv 1, wave_id 3, simd_id 2, wgp_id 3, err_type 2
[  922.934384] amdgpu: sq_intr: error, se 1, data 0x100000, sa 0, priv 1, wave_id 3, simd_id 1, wgp_id 3, err_type 2
[  922.934392] amdgpu: sq_intr: error, se 1, data 0x100000, sa 0, priv 1, wave_id 3, simd_id 2, wgp_id 0, err_type 2
[  922.934401] amdgpu: sq_intr: error, se 1, data 0x100000, sa 0, priv 1, wave_id 1, simd_id 3, wgp_id 0, err_type 2
[  922.934409] amdgpu: sq_intr: error, se 0, data 0x80000, sa 1, priv 1, wave_id 0, simd_id 0, wgp_id 3, err_type 1
[  923.098113] snd_hda_intel 0000:0b:00.1: CORB reset timeout#2, CORBRP = 65535
[  923.098129] amdgpu 0000:0b:00.0: amdgpu: GPU reset end with ret = -62
[  923.098132] amdgpu 0000:0b:00.0: amdgpu: GPU reset begin!
[  923.574217] amdgpu 0000:0b:00.0: amdgpu: Failed to disallow df cstate
```

```
:4:rocvirtual.cpp           :888 : 0893897953 us: [pid:110   tid:0x7f5fe9669740] HWq=0x7f5c16600000, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[16384, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x7f5c101260c0, kernarg_address=0x7f5c15603200, completion_signal=0x0
:3:hip_module.cpp           :679 : 0893897958 us: [pid:110   tid:0x7f5fe9669740] hipLaunchKernel: Returned hipSuccess : 
:3:hip_error.cpp            :27  : 0893897962 us: [pid:110   tid:0x7f5fe9669740]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :561 : 0893897967 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893897970 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893897983 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275c6c ) 
:3:hip_device_runtime.cpp   :539 : 0893897986 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893897990 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275b54 ) 
:3:hip_device_runtime.cpp   :539 : 0893897993 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893897997 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc772759d4 ) 
:3:hip_device_runtime.cpp   :539 : 0893898006 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :561 : 0893898015 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898019 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898026 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275a5c ) 
:3:hip_device_runtime.cpp   :539 : 0893898029 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_platform.cpp         :193 : 0893898038 us: [pid:110   tid:0x7f5fe9669740]  __hipPushCallConfiguration ( {64,1,1}, {256,1,1}, 0, stream:<null> ) 
:3:hip_platform.cpp         :197 : 0893898042 us: [pid:110   tid:0x7f5fe9669740] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :202 : 0893898052 us: [pid:110   tid:0x7f5fe9669740]  __hipPopCallConfiguration ( {256,0,1999068128}, {0,0,0}, 0x7ffc77275ac0, 0x7ffc77275aa8 ) 
:3:hip_platform.cpp         :211 : 0893898055 us: [pid:110   tid:0x7f5fe9669740] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :678 : 0893898063 us: [pid:110   tid:0x7f5fe9669740]  hipLaunchKernel ( 0x7f5fcd2e7ea8, {64,1,1}, {256,1,1}, 0x7ffc77275b20, 0, stream:<null> ) 
:4:command.cpp              :349 : 0893898069 us: [pid:110   tid:0x7f5fe9669740] Command (KernelExecution) enqueued: 0x5575aa07db10
:3:rocvirtual.cpp           :783 : 0893898072 us: [pid:110   tid:0x7f5fe9669740] Arg0:   = val:4575657221408489472
:3:rocvirtual.cpp           :783 : 0893898076 us: [pid:110   tid:0x7f5fe9669740] Arg1:   = val:1690312211794231296
:3:rocvirtual.cpp           :783 : 0893898079 us: [pid:110   tid:0x7f5fe9669740] Arg2:   = val:140033507275264
:3:rocvirtual.cpp           :2897: 0893898083 us: [pid:110   tid:0x7f5fe9669740] ShaderName : _ZN2at6native6modern18elementwise_kernelINS0_15CUDAFunctor_addIN3c104HalfEEENS_6detail5ArrayIPcLi3EEEEEviT_T0_
:4:rocvirtual.cpp           :888 : 0893898089 us: [pid:110   tid:0x7f5fe9669740] HWq=0x7f5c16600000, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[16384, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x7f5c09237d80, kernarg_address=0x7f5c15603280, completion_signal=0x0
:3:hip_module.cpp           :679 : 0893898094 us: [pid:110   tid:0x7f5fe9669740] hipLaunchKernel: Returned hipSuccess : 
:3:hip_error.cpp            :27  : 0893898097 us: [pid:110   tid:0x7f5fe9669740]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :561 : 0893898101 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898104 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898142 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc772756b4 ) 
:3:hip_device_runtime.cpp   :539 : 0893898147 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898153 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc772755e4 ) 
:3:hip_device_runtime.cpp   :539 : 0893898157 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898162 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275474 ) 
:3:hip_device_runtime.cpp   :539 : 0893898166 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :561 : 0893898174 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898178 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :561 : 0893898183 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898188 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898197 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc772753f4 ) 
:3:hip_device_runtime.cpp   :539 : 0893898200 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898205 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77274efc ) 
:3:hip_device_runtime.cpp   :539 : 0893898208 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_platform.cpp         :193 : 0893898215 us: [pid:110   tid:0x7f5fe9669740]  __hipPushCallConfiguration ( {128,1,1}, {512,1,1}, 0, stream:<null> ) 
:3:hip_platform.cpp         :197 : 0893898219 us: [pid:110   tid:0x7f5fe9669740] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :202 : 0893898228 us: [pid:110   tid:0x7f5fe9669740]  __hipPopCallConfiguration ( {0,0,0}, {0,0,0}, 0x7ffc77274f50, 0x7ffc77274f38 ) 
:3:hip_platform.cpp         :211 : 0893898232 us: [pid:110   tid:0x7f5fe9669740] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :678 : 0893898241 us: [pid:110   tid:0x7f5fe9669740]  hipLaunchKernel ( 0x7f5fcd2f0ea0, {128,1,1}, {512,1,1}, 0x7ffc77275250, 0, stream:<null> ) 
:4:command.cpp              :349 : 0893898248 us: [pid:110   tid:0x7f5fe9669740] Command (KernelExecution) enqueued: 0x5575aa07dd70
:3:rocvirtual.cpp           :783 : 0893898252 us: [pid:110   tid:0x7f5fe9669740] Arg0:   = val:65536
:3:rocvirtual.cpp           :783 : 0893898257 us: [pid:110   tid:0x7f5fe9669740] Arg1:   = val:140028086470656
:3:rocvirtual.cpp           :2897: 0893898261 us: [pid:110   tid:0x7f5fe9669740] ShaderName : _ZN2at6native6legacy18elementwise_kernelILi512ELi1EZNS0_15gpu_kernel_implIZZZNS0_23direct_copy_kernel_cudaERNS_18TensorIteratorBaseEENKUlvE0_clEvENKUlvE5_clEvEUlfE_EEvS5_RKT_EUliE_EEviT1_
:4:rocvirtual.cpp           :888 : 0893898265 us: [pid:110   tid:0x7f5fe9669740] HWq=0x7f5c16600000, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[65536, 1, 1], workgroup=[512, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x7f5c182a4f00, kernarg_address=0x7f5c15603300, completion_signal=0x0
:3:hip_module.cpp           :679 : 0893898271 us: [pid:110   tid:0x7f5fe9669740] hipLaunchKernel: Returned hipSuccess : 
:3:hip_error.cpp            :27  : 0893898274 us: [pid:110   tid:0x7f5fe9669740]  hipGetLastError (  ) 
:3:hip_error.cpp            :27  : 0893898278 us: [pid:110   tid:0x7f5fe9669740]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :561 : 0893898282 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898285 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898294 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77276274 ) 
:3:hip_device_runtime.cpp   :539 : 0893898298 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :561 : 0893898312 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898315 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898333 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275a7c ) 
:3:hip_device_runtime.cpp   :539 : 0893898337 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898341 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275964 ) 
:3:hip_device_runtime.cpp   :539 : 0893898344 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898348 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc772757e4 ) 
:3:hip_device_runtime.cpp   :539 : 0893898351 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :561 : 0893898357 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898361 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898369 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc7727595c ) 
:3:hip_device_runtime.cpp   :539 : 0893898372 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_platform.cpp         :193 : 0893898381 us: [pid:110   tid:0x7f5fe9669740]  __hipPushCallConfiguration ( {1,1,1}, {128,1,1}, 0, stream:<null> ) 
:3:hip_platform.cpp         :197 : 0893898384 us: [pid:110   tid:0x7f5fe9669740] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :202 : 0893898392 us: [pid:110   tid:0x7f5fe9669740]  __hipPopCallConfiguration ( {2594745289,32607,2595127560}, {0,0,0}, 0x7ffc772759a0, 0x7ffc77275998 ) 
:3:hip_platform.cpp         :211 : 0893898395 us: [pid:110   tid:0x7f5fe9669740] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :678 : 0893898404 us: [pid:110   tid:0x7f5fe9669740]  hipLaunchKernel ( 0x7f5fcd2f0a20, {1,1,1}, {128,1,1}, 0x7ffc772759d0, 0, stream:<null> ) 
:4:command.cpp              :349 : 0893898413 us: [pid:110   tid:0x7f5fe9669740] Command (KernelExecution) enqueued: 0x5575aa07dfd0
:3:rocvirtual.cpp           :783 : 0893898417 us: [pid:110   tid:0x7f5fe9669740] Arg0:   = val:1
:3:rocvirtual.cpp           :783 : 0893898421 us: [pid:110   tid:0x7f5fe9669740] Arg1:   = val:0
:3:rocvirtual.cpp           :2897: 0893898424 us: [pid:110   tid:0x7f5fe9669740] ShaderName : _ZN2at6native6legacy18elementwise_kernelILi128ELi4EZNS0_15gpu_kernel_implIZNS0_21compare_scalar_kernelIfEEvRNS_18TensorIteratorBaseENS0_12_GLOBAL__N_16OpTypeET_EUlfE_EEvS6_RKS9_EUliE2_EEviT1_
:4:rocvirtual.cpp           :888 : 0893898430 us: [pid:110   tid:0x7f5fe9669740] HWq=0x7f5c16600000, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[128, 1, 1], workgroup=[128, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x7f5c1b91ea00, kernarg_address=0x7f5c15603380, completion_signal=0x0
:3:hip_module.cpp           :679 : 0893898435 us: [pid:110   tid:0x7f5fe9669740] hipLaunchKernel: Returned hipSuccess : 
:3:hip_error.cpp            :27  : 0893898439 us: [pid:110   tid:0x7f5fe9669740]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :561 : 0893898444 us: [pid:110   tid:0x7f5fe9669740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0893898448 us: [pid:110   tid:0x7f5fe9669740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898462 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275dd4 ) 
:3:hip_device_runtime.cpp   :539 : 0893898466 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0893898472 us: [pid:110   tid:0x7f5fe9669740]  hipGetDevice ( 0x7ffc77275d7c ) 
:3:hip_device_runtime.cpp   :539 : 0893898476 us: [pid:110   tid:0x7f5fe9669740] hipGetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :652 : 0893898486 us: [pid:110   tid:0x7f5fe9669740]  hipMemcpyWithStream ( 0x7ffc77275db0, 0x7f5ad41ffe00, 1, hipMemcpyDeviceToHost, stream:<null> ) 
:4:command.cpp              :349 : 0893898499 us: [pid:110   tid:0x7f5fe9669740] Command (CopyDeviceToHost) enqueued: 0x5575aa07e230
:4:rocvirtual.cpp           :1026: 0893898509 us: [pid:110   tid:0x7f5fe9669740] HWq=0x7f5c16600000, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x7f5e48603a80
:4:rocvirtual.cpp           :554 : 0893898514 us: [pid:110   tid:0x7f5fe9669740] Host wait on completion_signal=0x7f5e48603a80
:3:rocvirtual.hpp           :67  : 0893898519 us: [pid:110   tid:0x7f5fe9669740] Host active wait for Signal = (0x7f5e48603a80) for -1 ns
Memory access fault by GPU node-2 (Agent handle: 0x55758de73200) on address 0x7f595b709000. Reason: Page not present or supervisor privilege.
```

Gotcha

---

### 评论 #10 — nix-wolf (2024-01-14T20:57:01Z)

I've done a bit more research about this

```
:1:hip_code_object.cpp      :516 : 1349537983 us: [pid:224   tid:0x7ff81ad1d740] hipErrorNoBinaryForGpu: Unable to find code object for all current devices!
:1:hip_code_object.cpp      :517 : 1349537997 us: [pid:224   tid:0x7ff81ad1d740]   Devices:
:1:hip_code_object.cpp      :520 : 1349538005 us: [pid:224   tid:0x7ff81ad1d740]     amdgcn-amd-amdhsa--gfx1030 - [Not Found]
```

and im not sure what to do, I've pulled the card from the system and are currently running my latest set of configurations and its working great will no issues, I also dont have to use, cpu offload, nor clear_cache, for this since in this configuration it seems to have sorted out all of my OOM issues, i looked into llvm and compiling the stuff for the gpus, but without some direction that seems like a deep rabbit hole. 

I also do understand that specifically my kernel 6.6 fedora 39 isnt supported, and the 6750xt isnt supported, but I dont think other then saying "compile this with this flag" or "heres this file, and youll  need to change a line in one of N files" would be more then enough for me to at least to tie it in. GIVEN that from the documentation the 1030 and 1031 are basically identical and that i also have generated 100s of pictures already under multi different configurations, I dont think im to far away from it being stable. considering the fact this is a very "edge case" senario. that is running docker attch without amdgpu/roc, installed to the system in the docker container, as after i had done all this and couldnt replicate the issue under other circumstances, I tried just running 'docker attach' and it didnt crash out. Hell maybe i need to reflash the bios on this other card cause when I did it, it somehow offset and wrote to a space it ussually doesnt? i dunno. 

Thanks for your time, and I hopefully await a favorable response. 

---

### 评论 #11 — KnairWang (2024-05-27T19:02:12Z)

TL;DR. try set the environment variable.
`HSA_OVERRIDE_GFX_VERSION`
It should match the GPU card `gfx` version.

---

I met similar issue on Archlinux, with ROCm packages at version 6.0.2-2 [arch linux package](https://archlinux.org/packages/extra/x86_64/rocm-core/), AMD GPU 7900XTX.

I was working with pytorch 2.3.0 and below is simple code to reproduce this issue. Actually it is part of diffusers scheduler.
```python
import numpy as np
import torch

sigmas = np.array([14.614647, 4.081731, 1.612887,
                  0.6932054, 0.], dtype=np.float32)
print("1", torch.from_numpy(sigmas))
print("cpu", torch.from_numpy(sigmas).to(device="cpu"))
print("rocm/cuda", torch.from_numpy(sigmas).to(device="cuda:0"))
print('done')
```
When it runs to the line `to(device="cuda:0")`, it either raises same error or hangs there while the GPU loading full with no VRAM used by program at all.

Finally I found this [github issue](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/11900) and I trid set environment variable
```
HSA_OVERRIDE_GFX_VERSION=11.0.0
```
And it works.

---

To find the correct version, there are many ways.
For example:
```
> rocminfo | rg gfx -A 2

  Name:                    gfx1100                            
  Uuid:                    GPU-3f5064323fff6f1f               
  Marketing Name:          AMD Radeon RX 7900 XTX             
--
      Name:                    amdgcn-amd-amdhsa--gfx1100         
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
--
  Name:                    gfx1036                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
--
      Name:                    amdgcn-amd-amdhsa--gfx1036         
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE  
```
Then my 7900XTX version is 1100 => 11.0.0. And the CPU-integreted-graphics version is 1036 => 10.3.6


---

### 评论 #12 — AphidGit (2024-07-05T20:46:43Z)

I've been having the same problem with rocm 6.0.2. 

For me, HSA_OVERRIDE_GFX_VERSION has no effect. 
I briefly (for about half a second) had my GPU turn my screen into random green splodges (literal memory corruption of the frame buffer). 

Shouldn't this be a _serious_ security issue given that it's apparently writing to random memory?

Edit; example kernel log: 

``` 
[ 1057.150630] amdgpu 0000:43:00.0: amdgpu: PSP is resuming...
[ 1057.221242] amdgpu 0000:43:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[ 1057.365921] amdgpu 0000:43:00.0: amdgpu: RAP: optional rap ta ucode is not available
[ 1057.365927] amdgpu 0000:43:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[ 1057.365931] amdgpu 0000:43:00.0: amdgpu: SMU is resuming...
[ 1057.365935] amdgpu 0000:43:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7d00 (78.125.0)
[ 1057.365940] amdgpu 0000:43:00.0: amdgpu: SMU driver if version not matched
[ 1057.511711] amdgpu 0000:43:00.0: amdgpu: SMU is resumed successfully!
[ 1057.513766] [drm] DMUB hardware initialized: version=0x07002A00
[ 1057.738341] [drm] kiq ring mec 3 pipe 1 q 0
[ 1057.744657] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[ 1057.744844] amdgpu 0000:43:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[ 1057.745330] amdgpu 0000:43:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 1057.745333] amdgpu 0000:43:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 1057.745336] amdgpu 0000:43:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 1057.745338] amdgpu 0000:43:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 1057.745340] amdgpu 0000:43:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 1057.745342] amdgpu 0000:43:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 1057.745344] amdgpu 0000:43:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 1057.745346] amdgpu 0000:43:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 1057.745349] amdgpu 0000:43:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 1057.745351] amdgpu 0000:43:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 1057.745353] amdgpu 0000:43:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[ 1057.745355] amdgpu 0000:43:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 1057.745357] amdgpu 0000:43:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[ 1057.745359] amdgpu 0000:43:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[ 1057.745361] amdgpu 0000:43:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[ 1057.748657] amdgpu 0000:43:00.0: amdgpu: recover vram bo from shadow start
[ 1057.755648] amdgpu 0000:43:00.0: amdgpu: recover vram bo from shadow done
[ 1057.755668] amdgpu 0000:43:00.0: amdgpu: GPU reset(3) succeeded!
[ 1138.300841] amdgpu 0000:43:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32778)
[ 1138.300851] amdgpu 0000:43:00.0: amdgpu:  in process python3 pid 6924 thread python3 pid 6924)
[ 1138.300855] amdgpu 0000:43:00.0: amdgpu:   in page starting at address 0x0000790f54a00000 from client 10
[ 1138.300860] amdgpu 0000:43:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00901031
[ 1138.300863] amdgpu 0000:43:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[ 1138.300866] amdgpu 0000:43:00.0: amdgpu:      MORE_FAULTS: 0x1
[ 1138.300869] amdgpu 0000:43:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1138.300871] amdgpu 0000:43:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[ 1138.300874] amdgpu 0000:43:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1138.300877] amdgpu 0000:43:00.0: amdgpu:      RW: 0x0
[ 1138.300884] amdgpu 0000:43:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32778)
[ 1138.300889] amdgpu 0000:43:00.0: amdgpu:  in process python3 pid 6924 thread python3 pid 6924)
[ 1138.300892] amdgpu 0000:43:00.0: amdgpu:   in page starting at address 0x0000790f54a00000 from client 10
[ 1138.300895] amdgpu 0000:43:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 1138.300898] amdgpu 0000:43:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[ 1138.300901] amdgpu 0000:43:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 1138.300904] amdgpu 0000:43:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1138.300906] amdgpu 0000:43:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[ 1138.300909] amdgpu 0000:43:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1138.300911] amdgpu 0000:43:00.0: amdgpu:      RW: 0x0
[ 1138.300919] amdgpu 0000:43:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32778)
[ 1138.300923] amdgpu 0000:43:00.0: amdgpu:  in process python3 pid 6924 thread python3 pid 6924)
[ 1138.300927] amdgpu 0000:43:00.0: amdgpu:   in page starting at address 0x0000790f54a00000 from client 10
[ 1138.300930] amdgpu 0000:43:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 1138.300932] amdgpu 0000:43:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[ 1138.300935] amdgpu 0000:43:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 1138.300938] amdgpu 0000:43:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1138.300940] amdgpu 0000:43:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[ 1138.300943] amdgpu 0000:43:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1138.300945] amdgpu 0000:43:00.0: amdgpu:      RW: 0x0
[ 1138.300952] amdgpu 0000:43:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32778)
[ 1138.300956] amdgpu 0000:43:00.0: amdgpu:  in process python3 pid 6924 thread python3 pid 6924)
[ 1138.300959] amdgpu 0000:43:00.0: amdgpu:   in page starting at address 0x0000790f54a00000 from client 10
[ 1138.300962] amdgpu 0000:43:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 1138.300965] amdgpu 0000:43:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[ 1138.300968] amdgpu 0000:43:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 1138.300970] amdgpu 0000:43:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1138.300973] amdgpu 0000:43:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[ 1138.300975] amdgpu 0000:43:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1138.300978] amdgpu 0000:43:00.0: amdgpu:      RW: 0x0
[ 1138.300985] amdgpu 0000:43:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32778)
[ 1138.300989] amdgpu 0000:43:00.0: amdgpu:  in process python3 pid 6924 thread python3 pid 6924)
[ 1138.300993] amdgpu 0000:43:00.0: amdgpu:   in page starting at address 0x0000790f54a00000 from client 10
[ 1138.300996] amdgpu 0000:43:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 1138.300998] amdgpu 0000:43:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[ 1138.301001] amdgpu 0000:43:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 1138.301004] amdgpu 0000:43:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1138.301006] amdgpu 0000:43:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[ 1138.301009] amdgpu 0000:43:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1138.301011] amdgpu 0000:43:00.0: amdgpu:      RW: 0x0
[ 1138.301019] amdgpu 0000:43:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32778)
[ 1138.301022] amdgpu 0000:43:00.0: amdgpu:  in process python3 pid 6924 thread python3 pid 6924)
[ 1138.301026] amdgpu 0000:43:00.0: amdgpu:   in page starting at address 0x0000790f54a00000 from client 10
[ 1138.301029] amdgpu 0000:43:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 1138.301031] amdgpu 0000:43:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[ 1138.301034] amdgpu 0000:43:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 1138.301037] amdgpu 0000:43:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1138.301039] amdgpu 0000:43:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[ 1138.301042] amdgpu 0000:43:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1138.301044] amdgpu 0000:43:00.0: amdgpu:      RW: 0x0
[ 1138.426043] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1138.426383] amdgpu 0000:43:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[ 1138.426386] amdgpu 0000:43:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 1138.426390] amdgpu 0000:43:00.0: amdgpu: Failed to evict queue 1
[ 1138.426408] print_sq_intr_info_error: 182 callbacks suppressed
[ 1138.426409] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426417] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426422] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426427] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426433] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426438] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426443] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426447] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426453] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426458] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[ 1138.426570] amdgpu 0000:43:00.0: amdgpu: GPU reset begin!
[ 1138.822887] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1138.823195] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1138.945304] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1138.945581] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1139.067895] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1139.068185] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1139.190536] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1139.190828] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1139.313181] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1139.313453] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1139.435800] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1139.436091] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1139.561866] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1139.562336] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1139.695998] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1139.696466] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1139.830120] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 1139.830589] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 1140.071684] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gf
``` 

Seems like it's overwriting its own protected memory and barfing on that. Here's a stack trace; 

``` 
int: You are currently not seeing messages from other users and the system.
      Users in groups 'adm', 'systemd-journal', 'wheel' can see all messages.
      Pass -q to turn off this notice.
           PID: 6924 (pt_main_thread)
           UID: 1000 ***
           GID: 1000 (***)
        Signal: 6 (ABRT)
     Timestamp: Fri 2024-07-05 23:05:06 CEST (24min ago)
  Command Line: python3 -u launch.py
    Executable: /usr/bin/python3.10
 Control Group: /user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.konsole@***.service
          Unit: user@1000.service
     User Unit: app-org.kde.konsole@***.service
         Slice: user-1000.slice
     Owner UID: 1000 ***
       Boot ID: ***
    Machine ID: ***
      Hostname: ***
       Storage: /var/lib/systemd/coredump/core.pt_main_thread.1000.***.6924.1720213506000000.zst (present)
  Size on Disk: 385.5M
       Message: Process 6924 (pt_main_thread) of user 1000 dumped core.
                
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module /tmp/miopen-interim-hsaco-9492-9737-f3c8-b889/file (deleted) without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module /tmp/miopen-interim-hsaco-87fc-7813-cf2a-1c93/file (deleted) without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module [dso] without build-id.
                Module libz.4e87b236.so.1 without build-id.
                Module librocsparse.so without build-id.
                Module librocrand.so without build-id.
                Module librocfft.so without build-id.
                Module librocsolver.so without build-id.
                Module librocblas.so without build-id.
                Module libmagma.so without build-id.
                Module librccl.so without build-id.
                Module libhiprand.so without build-id.
                Module libhipfft.so without build-id.
                Module libhipblaslt.so without build-id.
                Module libMIOpen.so without build-id.
                Stack trace of thread 6987:
                #0  0x00007913798a8e44 n/a (libc.so.6 + 0x94e44)
                #1  0x0000791379850a30 raise (libc.so.6 + 0x3ca30)
                #2  0x00007913798384c3 abort (libc.so.6 + 0x244c3)
                #3  0x000079129246e7cb _ZN4rocr4core7Runtime14VMFaultHandlerElPv (libhsa-runtime64.so + 0x6e7cb)
                #4  0x00007912924685d9 _ZN4rocr4core7Runtime15AsyncEventsLoopEPv (libhsa-runtime64.so + 0x685d9)
                #5  0x0000791292419f57 _ZN4rocr2os16ThreadTrampolineEPv (libhsa-runtime64.so + 0x19f57)
                #6  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #7  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6993:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6924:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798ae55e n/a (libc.so.6 + 0x9a55e)
                #2  0x0000791379b19889 PyThread_acquire_lock_timed (libpython3.10.so.1.0 + 0x119889)
                #3  0x0000791379bea84f n/a (libpython3.10.so.1.0 + 0x1ea84f)
                #4  0x0000791379bea61a n/a (libpython3.10.so.1.0 + 0x1ea61a)
                #5  0x0000791379b4adde n/a (libpython3.10.so.1.0 + 0x14adde)
                #6  0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #7  0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #8  0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #9  0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #10 0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #11 0x0000791379b55355 n/a (libpython3.10.so.1.0 + 0x155355)
                #12 0x0000791379b3ab77 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13ab77)
                #13 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #14 0x0000791379b3e220 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e220)
                #15 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #16 0x0000791379b39b56 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139b56)
                #17 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #18 0x0000791379b39b56 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139b56)
                #19 0x0000791379b385b0 n/a (libpython3.10.so.1.0 + 0x1385b0)
                #20 0x0000791379be4870 PyEval_EvalCode (libpython3.10.so.1.0 + 0x1e4870)
                #21 0x0000791379bf43ed n/a (libpython3.10.so.1.0 + 0x1f43ed)
                #22 0x0000791379beff5a n/a (libpython3.10.so.1.0 + 0x1eff5a)
                #23 0x0000791379a9cc33 n/a (libpython3.10.so.1.0 + 0x9cc33)
                #24 0x0000791379a9c8ce _PyRun_SimpleFileObject (libpython3.10.so.1.0 + 0x9c8ce)
                #25 0x0000791379a9d437 _PyRun_AnyFileObject (libpython3.10.so.1.0 + 0x9d437)
                #26 0x0000791379c00b65 Py_RunMain (libpython3.10.so.1.0 + 0x200b65)
                #27 0x0000791379bd6417 Py_BytesMain (libpython3.10.so.1.0 + 0x1d6417)
                #28 0x0000791379839c88 n/a (libc.so.6 + 0x25c88)
                #29 0x0000791379839d4c __libc_start_main (libc.so.6 + 0x25d4c)
                #30 0x00005bbeb8b5d065 _start (python3.10 + 0x1065)
                
                Stack trace of thread 6991:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6994:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6992:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7000:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7007:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7003:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7018:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7017:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7523:
                #0  0x000079129245330d _ZN4rocr4core15InterruptSignal11WaitRelaxedE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x5330d)
                #1  0x000079129245317a _ZN4rocr4core15InterruptSignal11WaitAcquireE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x5317a)
                #2  0x00007912924465b9 _ZN4rocr3HSA25hsa_signal_wait_scacquireE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x465b9)
                #3  0x00007912d440acd5 _ZN9roctracer11hsa_support6detailL34hsa_signal_wait_scacquire_callbackE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libroctracer64.so + 0xacd5)
                #4  0x000079130d29d0b3 _ZN3roc13WaitForSignalILb0EEEb12hsa_signal_sbb (libamdhip64.so + 0x29d0b3)
                #5  0x000079130d293f60 _ZN3roc10VirtualGPU14HwQueueTracker16CpuWaitForSignalEPNS_15ProfilingSignalE (libamdhip64.so + 0x293f60)
                #6  0x000079130d29611f _ZN3roc10VirtualGPU21releaseGpuMemoryFenceEb (libamdhip64.so + 0x29611f)
                #7  0x000079130d297e83 _ZN3roc10VirtualGPU5flushEPN3amd7CommandEb (libamdhip64.so + 0x297e83)
                #8  0x000079130d298db5 _ZN3roc10VirtualGPU12submitMarkerERN3amd6MarkerE (libamdhip64.so + 0x298db5)
                #9  0x000079130d26a441 _ZN3amd7Command7enqueueEv (libamdhip64.so + 0x26a441)
                #10 0x000079130d26aa30 _ZN3amd5Event14notifyCmdQueueEb (libamdhip64.so + 0x26aa30)
                #11 0x000079130d26aadc _ZN3amd5Event15awaitCompletionEv (libamdhip64.so + 0x26aadc)
                #12 0x000079130d12a37b _Z10ihipMemcpyPvPKvm13hipMemcpyKindRN3hip6StreamEbb (libamdhip64.so + 0x12a37b)
                #13 0x000079130d13d258 hipMemcpyWithStream (libamdhip64.so + 0x13d258)
                #14 0x000079130fc464ec _ZZN2at6native24_local_scalar_dense_cudaERKNS_6TensorEENKUlvE_clEv (libtorch_hip.so + 0x10464ec)
                #15 0x000079130fc46250 _ZN2at6native24_local_scalar_dense_cudaERKNS_6TensorE (libtorch_hip.so + 0x1046250)
                #16 0x0000791310966b04 _ZN2at12_GLOBAL__N_112_GLOBAL__N_133wrapper_CUDA___local_scalar_denseERKNS_6TensorE (libtorch_hip.so + 0x1d66b04)
                #17 0x0000791310966bbd _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFNS_6ScalarERKN2at6TensorEEXadL_ZNS6_12_GLOBAL__N_112_GLOBAL__N_133wrapper_CUDA___local_scalar_denseES9_EEEES5_NS_4guts8typelist8typelistIJS9_EEEEESA_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES9_ (libtorch_hip.so + 0x1d66bbd)
                #18 0x0000791360a101bb _ZN2at4_ops19_local_scalar_dense10redispatchEN3c1014DispatchKeySetERKNS_6TensorE (libtorch_cpu.so + 0x28101bb)
                #19 0x000079136288c6d0 _ZN5torch8autograd12VariableType12_GLOBAL__N_119_local_scalar_denseEN3c1014DispatchKeySetERKN2at6TensorE (libtorch_cpu.so + 0x468c6d0)
                #20 0x000079136288c750 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFNS_6ScalarENS_14DispatchKeySetERKN2at6TensorEEXadL_ZN5torch8autograd12VariableType12_GLOBAL__N_119_local_scalar_denseES6_SA_EEEES5_NS_4guts8typelist8typelistIJS6_SA_EEEEESB_E4callEPNS_14OperatorKernelES6_SA_ (libtorch_cpu.so + 0x468c750)
                #21 0x0000791360ac73eb _ZN2at4_ops19_local_scalar_dense4callERKNS_6TensorE (libtorch_cpu.so + 0x28c73eb)
                #22 0x0000791360106983 _ZN2at6native4itemERKNS_6TensorE (libtorch_cpu.so + 0x1f06983)
                #23 0x00007913611cca6d _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFNS_6ScalarERKN2at6TensorEEXadL_ZNS6_12_GLOBAL__N_112_GLOBAL__N_139wrapper_CompositeImplicitAutograd__itemES9_EEEES5_NS_4guts8typelist8typelistIJS9_EEEEESA_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES9_ (libtorch_cpu.so + 0x2fcca6d)
                #24 0x000079136091651b _ZN2at4_ops4item4callERKNS_6TensorE (libtorch_cpu.so + 0x271651b)
                #25 0x00007913602b3f6a _ZN2at6native10is_nonzeroERKNS_6TensorE (libtorch_cpu.so + 0x20b3f6a)
                #26 0x0000791360a90c59 _ZN2at4_ops10is_nonzero4callERKNS_6TensorE (libtorch_cpu.so + 0x2890c59)
                #27 0x0000791376d3fa2a _ZN5torch8autogradL22THPVariable_is_nonzeroEP7_objectS2_ (libtorch_python.so + 0x53fa2a)
                #28 0x0000791376d3fc38 _ZN5torch8autogradL23THPVariable_bool_scalarEP7_objectS2_ (libtorch_python.so + 0x53fc38)
                #29 0x0000791379b4c7bc n/a (libpython3.10.so.1.0 + 0x14c7bc)
                #30 0x0000791379b956df n/a (libpython3.10.so.1.0 + 0x1956df)
                #31 0x0000791379bd32e4 n/a (libpython3.10.so.1.0 + 0x1d32e4)
                #32 0x0000791379b53262 PyObject_IsTrue (libpython3.10.so.1.0 + 0x153262)
                #33 0x0000791379b3e3ee _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e3ee)
                #34 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #35 0x0000791379b55da8 PyObject_Call (libpython3.10.so.1.0 + 0x155da8)
                #36 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #37 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #38 0x0000791379b55da8 PyObject_Call (libpython3.10.so.1.0 + 0x155da8)
                #39 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #40 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #41 0x0000791379b39b56 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139b56)
                #42 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #43 0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #44 0x0000791379b55355 n/a (libpython3.10.so.1.0 + 0x155355)
                #45 0x0000791379b3ab77 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13ab77)
                #46 0x0000791379b55355 n/a (libpython3.10.so.1.0 + 0x155355)
                #47 0x0000791379b3ab77 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13ab77)
                #48 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #49 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #50 0x0000791379b55355 n/a (libpython3.10.so.1.0 + 0x155355)
                #51 0x0000791379b39b56 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139b56)
                #52 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #53 0x0000791379b3e220 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e220)
                #54 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #55 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #56 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #57 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #58 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #59 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #60 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #61 0x0000791379be668c n/a (libpython3.10.so.1.0 + 0x1e668c)
                #62 0x0000791379af2277 n/a (libpython3.10.so.1.0 + 0xf2277)
                #63 0x0000791379b4110b n/a (libpython3.10.so.1.0 + 0x14110b)
                
                Stack trace of thread 6990:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7524:
                #0  0x0000791292453304 _ZN4rocr4core15InterruptSignal11WaitRelaxedE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x53304)
                #1  0x000079129245317a _ZN4rocr4core15InterruptSignal11WaitAcquireE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x5317a)
                #2  0x00007912924465b9 _ZN4rocr3HSA25hsa_signal_wait_scacquireE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x465b9)
                #3  0x00007912d440acd5 _ZN9roctracer11hsa_support6detailL34hsa_signal_wait_scacquire_callbackE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libroctracer64.so + 0xacd5)
                #4  0x000079130d28052b _ZNK3roc6Device14IsHwEventReadyERKN3amd5EventEb (libamdhip64.so + 0x28052b)
                #5  0x000079130d09cea7 _ZN3hip5Event11synchronizeEv (libamdhip64.so + 0x9cea7)
                #6  0x000079130d09ec04 hipEventSynchronize (libamdhip64.so + 0x9ec04)
                #7  0x0000791307c0f123 _ZNK6miopen17HIPOCKernelInvoke3runEPvm (libMIOpen.so + 0x3280f123)
                #8  0x00007913078ea5c7 n/a (libMIOpen.so + 0x324ea5c7)
                #9  0x0000791307144e32 _ZN6miopen12ConvFindCoreERKNS_15AnyInvokeParamsERNS_8DbRecordERKNS_16ExecutionContextERKNS_18ProblemDescriptionEbRKSt6vectorISt10unique_ptrINS_13SolversFinderESt14default_deleteISD_EESaISG_EE (libMIOpen.so + 0x31d44e32)
                #10 0x0000791307af74b9 n/a (libMIOpen.so + 0x326f74b9)
                #11 0x0000791307afd2c4 n/a (libMIOpen.so + 0x326fd2c4)
                #12 0x0000791307ae588b n/a (libMIOpen.so + 0x326e588b)
                #13 0x0000791307ae4c7e _ZNK6miopen21ConvolutionDescriptor20FindConvFwdAlgorithmERNS_6HandleERKNS_16TensorDescriptorEPKvS5_S7_S5_PviPiP20miopenConvAlgoPerf_tS8_mb (libMIOpen.so + 0x326e4c7e)
                #14 0x0000791306f30824 miopenFindConvolutionForwardAlgorithm (libMIOpen.so + 0x31b30824)
                #15 0x0000791310c17110 _ZN2at6native15chooseAlgorithmI24miopenConvFwdAlgorithm_tEENS0_9WorkspaceERKNS0_15ConvolutionArgsEbPT_ (libtorch_hip.so + 0x2017110)
                #16 0x0000791310c0db3f _ZN2at6native34raw_miopen_convolution_forward_outERKNS_6TensorES3_S3_N3c108ArrayRefIlEES6_S6_lbb (libtorch_hip.so + 0x200db3f)
                #17 0x0000791310c0e301 _ZN2at6native26miopen_convolution_forwardEPKcRKNS_9TensorArgES5_N3c108ArrayRefIlEES8_S8_lbb (libtorch_hip.so + 0x200e301)
                #18 0x0000791310c0e4d4 _ZN2at6native18miopen_convolutionERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefIlEESA_SA_lbb (libtorch_hip.so + 0x200e4d4)
                #19 0x000079131099eeaf _ZN2at12_GLOBAL__N_112_GLOBAL__N_132wrapper_CUDA__miopen_convolutionERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_SB_bb (libtorch_hip.so + 0x1d9eeaf)
                #20 0x00007913109a4cd7 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_SE_bbEXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_132wrapper_CUDA__miopen_convolutionES8_S8_SC_SF_SF_SF_SE_bbEEEES6_NS_4guts8typelist8typelistIJS8_S8_SC_SF_SF_SF_SE_bbEEEEESG_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES8_S8_SC_SF_SF_SF_SE_bb (libtorch_hip.so + 0x1da4cd7)
                #21 0x0000791360aa8120 _ZN2at4_ops18miopen_convolution4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_SB_bb (libtorch_cpu.so + 0x28a8120)
                #22 0x000079135fe62d69 _ZN2at6native12_convolutionERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefIlEESA_SA_bSA_lbbbb (libtorch_cpu.so + 0x1c62d69)
                #23 0x0000791360fed7bf _ZN2at12_GLOBAL__N_112_GLOBAL__N_147wrapper_CompositeExplicitAutograd___convolutionERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_bSC_SB_bbbb (libtorch_cpu.so + 0x2ded7bf)
                #24 0x0000791360ff411c _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_bSF_SE_bbbbEXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_147wrapper_CompositeExplicitAutograd___convolutionES8_S8_SC_SF_SF_SF_bSF_SE_bbbbEEEES6_NS_4guts8typelist8typelistIJS8_S8_SC_SF_SF_SF_bSF_SE_bbbbEEEEESG_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES8_S8_SC_SF_SF_SF_bSF_SE_bbbb (libtorch_cpu.so + 0x2df411c)
                #25 0x0000791360735204 _ZN2at4_ops12_convolution4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_bSC_SB_bbbb (libtorch_cpu.so + 0x2535204)
                #26 0x000079135fe55f18 _ZN2at6native11convolutionERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefIlEESA_SA_bSA_l (libtorch_cpu.so + 0x1c55f18)
                #27 0x0000791360fed05c _ZN2at12_GLOBAL__N_112_GLOBAL__N_146wrapper_CompositeExplicitAutograd__convolutionERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_bSC_SB_ (libtorch_cpu.so + 0x2ded05c)
                #28 0x0000791360ff3f88 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_bSF_SE_EXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_146wrapper_CompositeExplicitAutograd__convolutionES8_S8_SC_SF_SF_SF_bSF_SE_EEEES6_NS_4guts8typelist8typelistIJS8_S8_SC_SF_SF_SF_bSF_SE_EEEEESG_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES8_S8_SC_SF_SF_SF_bSF_SE_ (libtorch_cpu.so + 0x2df3f88)
                #29 0x00007913606f2e9b _ZN2at4_ops11convolution10redispatchEN3c1014DispatchKeySetERKNS_6TensorES6_RKSt8optionalIS4_ENS2_8ArrayRefINS2_6SymIntEEESD_SD_bSD_SC_ (libtorch_cpu.so + 0x24f2e9b)
                #30 0x00007913626fc361 _ZN5torch8autograd12VariableType12_GLOBAL__N_111convolutionEN3c1014DispatchKeySetERKN2at6TensorES8_RKSt8optionalIS6_ENS3_8ArrayRefINS3_6SymIntEEESF_SF_bSF_SE_ (libtorch_cpu.so + 0x44fc361)
                #31 0x00007913626fd2d9 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorENS_14DispatchKeySetERKS6_S9_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESG_SG_bSG_SF_EXadL_ZN5torch8autograd12VariableType12_GLOBAL__N_111convolutionES7_S9_S9_SD_SG_SG_SG_bSG_SF_EEEES6_NS_4guts8typelist8typelistIJS7_S9_S9_SD_SG_SG_SG_bSG_SF_EEEEESH_E4callEPNS_14OperatorKernelES7_S9_S9_SD_SG_SG_SG_bSG_SF_ (libtorch_cpu.so + 0x44fd2d9)
                #32 0x0000791360734004 _ZN2at4_ops11convolution4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_bSC_SB_ (libtorch_cpu.so + 0x2534004)
                #33 0x000079135fbad770 _ZN2at18convolution_symintERKNS_6TensorES2_RKSt8optionalIS0_EN3c108ArrayRefINS7_6SymIntEEESA_SA_bSA_S9_ (libtorch_cpu.so + 0x19ad770)
                #34 0x000079135fe597fb _ZN2at6native13conv2d_symintERKNS_6TensorES3_RKSt8optionalIS1_EN3c108ArrayRefINS8_6SymIntEEESB_SB_SA_ (libtorch_cpu.so + 0x1c597fb)
                #35 0x00007913611e65e3 _ZN2at12_GLOBAL__N_112_GLOBAL__N_141wrapper_CompositeImplicitAutograd__conv2dERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_SB_ (libtorch_cpu.so + 0x2fe65e3)
                #36 0x00007913611e687d _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_ENS_8ArrayRefINS_6SymIntEEESF_SF_SE_EXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_141wrapper_CompositeImplicitAutograd__conv2dES8_S8_SC_SF_SF_SF_SE_EEEES6_NS_4guts8typelist8typelistIJS8_S8_SC_SF_SF_SF_SE_EEEEESG_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES8_S8_SC_SF_SF_SF_SE_ (libtorch_cpu.so + 0x2fe687d)
                #37 0x0000791360d5987e _ZN2at4_ops6conv2d4callERKNS_6TensorES4_RKSt8optionalIS2_EN3c108ArrayRefINS9_6SymIntEEESC_SC_SB_ (libtorch_cpu.so + 0x2b5987e)
                #38 0x0000791376e8558d _ZN5torch8autogradL18THPVariable_conv2dEP7_objectS2_S2_ (libtorch_python.so + 0x68558d)
                #39 0x0000791379b49d0d n/a (libpython3.10.so.1.0 + 0x149d0d)
                #40 0x0000791379b43483 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x143483)
                #41 0x0000791379b3eacf _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13eacf)
                #42 0x0000791379b55355 n/a (libpython3.10.so.1.0 + 0x155355)
                #43 0x0000791379b3e220 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e220)
                #44 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #45 0x0000791379b3e220 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e220)
                #46 0x0000791379b385b0 n/a (libpython3.10.so.1.0 + 0x1385b0)
                #47 0x0000791379b5547b n/a (libpython3.10.so.1.0 + 0x15547b)
                #48 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #49 0x0000791379b385b0 n/a (libpython3.10.so.1.0 + 0x1385b0)
                #50 0x0000791379b5547b n/a (libpython3.10.so.1.0 + 0x15547b)
                #51 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #52 0x0000791379b426f5 _PyObject_FastCallDictTstate (libpython3.10.so.1.0 + 0x1426f5)
                #53 0x0000791379b52b76 _PyObject_Call_Prepend (libpython3.10.so.1.0 + 0x152b76)
                #54 0x0000791379c1c0ae n/a (libpython3.10.so.1.0 + 0x21c0ae)
                #55 0x0000791379b43483 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x143483)
                #56 0x0000791379b3e4f8 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e4f8)
                #57 0x0000791379b385b0 n/a (libpython3.10.so.1.0 + 0x1385b0)
                #58 0x0000791379b5547b n/a (libpython3.10.so.1.0 + 0x15547b)
                #59 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #60 0x0000791379b385b0 n/a (libpython3.10.so.1.0 + 0x1385b0)
                #61 0x0000791379b5547b n/a (libpython3.10.so.1.0 + 0x15547b)
                #62 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #63 0x0000791379b426f5 _PyObject_FastCallDictTstate (libpython3.10.so.1.0 + 0x1426f5)
                
                Stack trace of thread 6995:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6989:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6997:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6999:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7011:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7013:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7010:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7002:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7006:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7009:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7005:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7001:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6998:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7015:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7004:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7014:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7026:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910b0e2ab7f _Z9th_workerPv (interpreter.cpython-310-x86_64-linux-gnu.so + 0x24b7f)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7155:
                #0  0x00007913799278f7 __select (libc.so.6 + 0x1138f7)
                #1  0x0000791379c4ea71 n/a (libpython3.10.so.1.0 + 0x24ea71)
                #2  0x0000791379b49722 n/a (libpython3.10.so.1.0 + 0x149722)
                #3  0x0000791379b3e220 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e220)
                #4  0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #5  0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #6  0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #7  0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #8  0x0000791379b5555b n/a (libpython3.10.so.1.0 + 0x15555b)
                #9  0x0000791379c30f53 n/a (libpython3.10.so.1.0 + 0x230f53)
                #10 0x0000791379c07c64 n/a (libpython3.10.so.1.0 + 0x207c64)
                #11 0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #12 0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7029:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910b0e2ab7f _Z9th_workerPv (interpreter.cpython-310-x86_64-linux-gnu.so + 0x24b7f)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7133:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7008:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7016:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7135:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7355:
                #0  0x000079137992a380 epoll_pwait (libc.so.6 + 0x116380)
                #1  0x0000790fc9fa023d uv__io_poll (loop.cpython-310-x86_64-linux-gnu.so + 0x12d23d)
                #2  0x0000790fc9f92ea6 uv_run (loop.cpython-310-x86_64-linux-gnu.so + 0x11fea6)
                #3  0x0000790fc9f1ea83 __pyx_f_6uvloop_4loop_4Loop___run (loop.cpython-310-x86_64-linux-gnu.so + 0xaba83)
                #4  0x0000790fc9f27b16 __pyx_f_6uvloop_4loop_4Loop__run (loop.cpython-310-x86_64-linux-gnu.so + 0xb4b16)
                #5  0x0000790fc9eed3c3 __pyx_pf_6uvloop_4loop_4Loop_24run_forever (loop.cpython-310-x86_64-linux-gnu.so + 0x7a3c3)
                #6  0x0000790fc9eb9355 __Pyx_PyObject_CallMethO (loop.cpython-310-x86_64-linux-gnu.so + 0x46355)
                #7  0x0000790fc9f5228d __pyx_pf_6uvloop_4loop_4Loop_44run_until_complete (loop.cpython-310-x86_64-linux-gnu.so + 0xdf28d)
                #8  0x0000791379b5357b n/a (libpython3.10.so.1.0 + 0x15357b)
                #9  0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #10 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #11 0x0000791379b3e220 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13e220)
                #12 0x0000791379b5555b n/a (libpython3.10.so.1.0 + 0x15555b)
                #13 0x0000791379b3c5b3 _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x13c5b3)
                #14 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #15 0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #16 0x0000791379b4a1f5 _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x14a1f5)
                #17 0x0000791379b39f4a _PyEval_EvalFrameDefault (libpython3.10.so.1.0 + 0x139f4a)
                #18 0x0000791379b5555b n/a (libpython3.10.so.1.0 + 0x15555b)
                #19 0x0000791379c30f53 n/a (libpython3.10.so.1.0 + 0x230f53)
                #20 0x0000791379c07c64 n/a (libpython3.10.so.1.0 + 0x207c64)
                #21 0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #22 0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7128:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7124:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7130:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7139:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 6996:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7123:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7136:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7144:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7143:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7127:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7012:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x00007910ae7506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7145:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7138:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7132:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7147:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7122:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7125:
                #0  0x00007913798a34e9 n/a (libc.so.6 + 0x8f4e9)
                #1  0x00007913798a5ed9 pthread_cond_wait (libc.so.6 + 0x91ed9)
                #2  0x0000791033d5825b blas_thread_server (libscipy_openblas-c128ec02.so + 0x35825b)
                #3  0x00007913798a6ded n/a (libc.so.6 + 0x92ded)
                #4  0x000079137992a0dc n/a (libc.so.6 + 0x1160dc)
                
                Stack trace of thread 7356:
                #0  0x0000000000000000 n/a (n/a + 0x0)
                ELF object binary architecture: AMD x86-64
``` 











---

### 评论 #13 — nix-wolf (2024-07-05T21:22:14Z)

> I've been having the same problem with rocm 6.0.2.
> 
> For me, HSA_OVERRIDE_GFX_VERSION has no effect. I briefly (for about half a second) had my GPU turn my screen into random green splodges (literal memory corruption of the frame buffer).
> 
> Shouldn't this be a _serious_ security issue given that it's apparently writing to random memory?

Yea my issue turned out to be a bunch of little things. Software was one, making sure everything works properly in the environment is pretty big. Secondly after fighting this problem for a while what I ended up finding out was one of my power cables must have had some minor short in it. After I replaced it I haven't seen this error. I found out from trying different cards to try to isolate the issue if it was the mobo or the card itself. And eventually the cord just stopped working all together. I replaced it and haven't seen the issue since. Since then I noticed there is sometimes issues with card targeting, when using the second card explicitly, I think it's a issue with the abstraction layer working with cuda because even if you tell cuda to target the second card, it starts to use it, but then tries to write to the first card causing the memory to not exist in the second card, which was partially masked by the power cord issue. It also was my second card crashing even while using the first card, I'm guessing because there is some form of a checkin that happens or for some reason with the voltage issues with the fucked power cord it was messaging everything up. I'm still not entirely sure 100% why but for insurance on finding the issue. 

1: ensure that everything is plugged in properly, and make sure all the cords are good(maybe swap one just to check)
2: try a different pcie slot as this seemed to also change things for me
3: try the card alone in a system(headless if you can) 
4: if you have multiple cards, in a headless system, try each card alone in the system
5: if you are currently running a second card dedicated to use running rocm and your primary card is currently hooked up to your moniter, try using the bios to target the second card for your moniter, and move the card for your moniter to the second slot so then when you are running rocm, it will target the first card. 

If you are running this from a workstation and having issues I would seriously suggest that you move the cards your using to a dedicated system separately. As described in the steps above. As I said before I eventually found out that there was an issue related to cuda that it starts targeting the second card, but during the process of for some reason it forgets it's sending to, or retrieving from the second card and attempts to hit the first. I even had instances where it would work for an hour then randomly fault, but that also could have been initially related to the power cord issue. Never the less after the cord was solved I was trying to get with my gpus to work and this was the issue I had. Which I think could explain the permission issue. I haven't returned to messing with multiple gpus as my assumption is that there is some preliminary code you may need in order to manage data in and out of the gpu and what gpu it's for.

 I've been using this for a while for llm and stable diffusion without any issue BTW. And since I'm just developing things I haven't needed the second gpu, I will be returning to figure out the issue I described soon since I'm almost there. If there is a dev out there that wouldn't might clarifying thus that would be pretty sweet. 

Good luck. 

---

### 评论 #14 — nix-wolf (2024-07-05T21:34:04Z)

> TL;DR. try set the environment variable. `HSA_OVERRIDE_GFX_VERSION` It should match the GPU card `gfx` version.
> 
> I met similar issue on Archlinux, with ROCm packages at version 6.0.2-2 [arch linux package](https://archlinux.org/packages/extra/x86_64/rocm-core/), AMD GPU 7900XTX.
> 
> I was working with pytorch 2.3.0 and below is simple code to reproduce this issue. Actually it is part of diffusers scheduler.
> 
> ```python
> import numpy as np
> import torch
> 
> sigmas = np.array([14.614647, 4.081731, 1.612887,
>                   0.6932054, 0.], dtype=np.float32)
> print("1", torch.from_numpy(sigmas))
> print("cpu", torch.from_numpy(sigmas).to(device="cpu"))
> print("rocm/cuda", torch.from_numpy(sigmas).to(device="cuda:0"))
> print('done')
> ```
> 
> When it runs to the line `to(device="cuda:0")`, it either raises same error or hangs there while the GPU loading full with no VRAM used by program at all.
> 
> Finally I found this [github issue](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/11900) and I trid set environment variable
> 
> ```
> HSA_OVERRIDE_GFX_VERSION=11.0.0
> ```
> 
> And it works.
> 
> To find the correct version, there are many ways. For example:
> 
> ```
> > rocminfo | rg gfx -A 2
> 
>   Name:                    gfx1100                            
>   Uuid:                    GPU-3f5064323fff6f1f               
>   Marketing Name:          AMD Radeon RX 7900 XTX             
> --
>       Name:                    amdgcn-amd-amdhsa--gfx1100         
>       Machine Models:          HSA_MACHINE_MODEL_LARGE            
>       Profiles:                HSA_PROFILE_BASE                   
> --
>   Name:                    gfx1036                            
>   Uuid:                    GPU-XX                             
>   Marketing Name:          AMD Radeon Graphics                
> --
>       Name:                    amdgcn-amd-amdhsa--gfx1036         
>       Machine Models:          HSA_MACHINE_MODEL_LARGE            
>       Profiles:                HSA_PROFILE_BASE  
> ```
> 
> Then my 7900XTX version is 1100 => 11.0.0. And the CPU-integreted-graphics version is 1036 => 10.3.6

My issue was a little different since I was using that and it wasn't helping. I did get it working, se my last reply to the other fellow. I do think the memory error has something to with cuda and rocm getting something mixed up and accidentally targeting the wrong gpu in multi gpu setups. Be nice if a dev could confirm the possibility. In the coming weeks I might be playing with multiple gpus, and I have my notes as I can reproduce these issues. I have have switched from fedora docker and centos to rocky 9.2 and no docker and was able to reproduce these behaviours

---

### 评论 #15 — nix-wolf (2024-07-05T21:36:12Z)

Another note: it could just be related to sets of packages installed as I even build rocm myself, and built rocm pytorch and had the same issues. But it's been months since I dealt with any of this. Again. I'm fairly certain the issue comes from multiple gpu setups. If you two and concure if you are running multiple gpus and in what configuration. 

---

### 评论 #16 — AphidGit (2024-07-05T21:48:21Z)

I'm pretty sure it's not a hardware issue. I updated rocm recently to use/run LLMs, and that worked just fine. Prompt processing is also a pretty heavy load, and I was processing thousands of tokens over a dozen minutes running full power. 

It's only after updating the software stack that major problems started. However, I'll run some stress tests and see if there's anything there. I doubt it though. 

So far, furmark seems to just keep going. 

---

### 评论 #17 — nix-wolf (2024-07-05T22:27:36Z)

> I'm pretty sure it's not a hardware issue. I updated rocm recently to use/run LLMs, and that worked just fine. Prompt processing is also a pretty heavy load, and I was processing thousands of tokens over a dozen minutes running full power.
> 
> It's only after updating the software stack that major problems started. However, I'll run some stress tests and see if there's anything there. I doubt it though.
> 
> So far, furmark seems to just keep going.

Yes i agree, it's just an off issue I had. But never hurts to check. Make sure those trouble shooting boxes are filled. Is it plugged in? Is it turned on? Lol

---

### 评论 #18 — AphidGit (2024-07-06T09:41:42Z)

Are there any instructions anywhere for how to bisect this problem / use source instead of AUR package? I'd like to figure out where the issue happened because 5.7 ran stable-diffusion fine. (Though failed at doing LLM, now 6.0 runs LLMs, but fails stable diffusion).  

A simple git bisect doesn't do the trick, because there's multiple repos involved. (I have no idea where the problem is.)

Another way would be to have an instruction of how to compile the ROCM as it was on say '2024-03-03 06:58:27' or any other arbitrary date-time

---

### 评论 #19 — nix-wolf (2024-07-06T15:17:27Z)

> Are there any instructions anywhere for how to bisect this problem / use source instead of AUR package? I'd like to figure out where the issue happened because 5.7 ran stable-diffusion fine. (Though failed at doing LLM, now 6.0 runs LLMs, but fails stable diffusion).
> 
> A simple git bisect doesn't do the trick, because there's multiple repos involved. (I have no idea where the problem is.)
> 
> Another way would be to have an instruction of how to compile the ROCM as it was on say '2024-03-03 06:58:27' or any other arbitrary date-time

I did build from source once. It didn't change the issue for me. Maybe it's not in rocm at all, Since I posted all this I do believe my current stack is running everything with the most recent versions of everything. Even diffusers and transformers and pytorch. Have you tried getting it setup with the newest versions of the entire software stack? 

I'll give er a check later today if you want or can message me maybe we can link up on discord and try to get it figured out. 

Did you remove a gpu from your system and try my suggestions there for isolating the issue that way? I did believe you were running 2 correct?

---

### 评论 #20 — harkgill-amd (2024-09-06T14:57:43Z)

@nix-wolf, apologies for the lack of response. Do you still need assistance with this issue?

---

### 评论 #21 — nix-wolf (2024-09-06T15:03:29Z)

Well. I wouldn't say it's ever been formally solved it doesn't seem to be
an issue now and I have played with it and got it working, but I do believe
I can reproduce this. I'm not at home at the moment, but will be this
afternoon, and then can see if I can reproduce, it's been a while as I was
able setup it up without the issue. I'll also check my notes and give a
better response as to where I left it off

On Fri, Sep 6, 2024, 08:58 harkgill-amd ***@***.***> wrote:

> @nix-wolf <https://github.com/nix-wolf>, apologies for the lack of
> response. Do you still need assistance with this issue?
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2804#issuecomment-2334246540>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AH26U4RG5B7TFJLPMY53TVLZVG7HZAVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMZUGI2DMNJUGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #22 — harkgill-amd (2024-09-06T15:07:24Z)

Thanks! If you are able to reproduce it, please provide the steps and we will give it a try on our side as well.

---

### 评论 #23 — nix-wolf (2024-09-06T15:17:33Z)

Have you given it a try based on the steps I did before? I did it 4 or 5
times in different ways with different setups.

On Fri, Sep 6, 2024, 09:07 harkgill-amd ***@***.***> wrote:

> Thanks! If you are able to reproduce it, please provide the steps and we
> will give it a try on our side as well.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2804#issuecomment-2334266255>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AH26U4T6SHSH6UQUWLUEGODZVHAMFAVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMZUGI3DMMRVGU>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #24 — tcgu-amd (2024-09-09T20:02:32Z)

@nix-wolf Hi there! I took a look at your initial steps. Would you mind providing a bit more details regarding how you set up your system? For example, how did you install ROCm on both your host system and inside the container?

Also, just a general note, according to the official docs https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.2/how-to/docker.html, ROCm in docker relies on the ROCm kernel mode driver on the host system to function properly. Hence, a mismatch between the host ROCm version and the container ROCm version can result in some discrepancies and unexpected behaviors, which may explain some of the errors you are seeing. It might be more consistent to ensure the same ROCm version on the host, inside the container, and with corresponding supported Pytorch package. 

Thanks!

---

### 评论 #25 — nix-wolf (2024-09-10T11:18:12Z)

Hey,

I do believe if you read through the subsequent comments I made relative to
trying to figure it out this is one thing I did figure out thay I didn't
have rocm installed on the host system.

I also found that one of my gou power cables wasn't functioning properly
after messing around with it for a while untill the cord went completely
dead. So I think there was a possibility that it was associated to improper
voltage under "critical load"

Off hand I still can't remember exactly what versions, but I think I also
recorded all of this in the comments above. Including the fact I switched
from using a docker container of centos 7.3(or 9) with the host as fedora
37-39 I think, which I do believe there are some issues with running rocm
on fedora because of the glibc version, which is why I was running it in
docker in the first place, if I can recall the rationale of why I setup
this way in the first place. Eventually I ran into a problem as well that
docker wasn't abke to properly manage the fans of the gpus for some access
control reasons so I opted to shift the installation to running everything
on the host system with centos. Which I do believe doing this may have
fixed my issue in part, but also could have been where i discovered my
power cable was faulty. Given the centos was coming to end of life I
eventually shifter to rocky 9 and I think I have generated 4 or 5k images
and even run LLM. I also do believe I am using the newest version of
everything.

If I'm also not mistaken (which is a separate issue) the problems í was
having, or which I'm pretty í may have had idea of how to fix(but can't
really recall) was that in my system that disptaches the scripts to be run
on the gpus, when á gpu is busy and being used, it targets, or if I run it
on the second gpu it crashes, and hangs throwing this error, and the reason
why from my research is that there is an issue with rocm's amd cuda's
communication to each gpu, and initially the program targets the second gpu
loads in all the models, starts working, and defaults to trying to
send/fetch data from the wrong gpu, result in access violation. Now, I must
apologize, I've been very busy with work as I'm working in oilfield
transportation, and work very long hours, and haven't had time as of yet to
sit down.

If one would be interested in a test, which shouldn't take long. Using
Rocky 9.2, and 2 6750xt 12gb, just run any pytorch functions in a long
running loop so that it uses at least more then half the gpu ram. And
target the second gpu, or use any of the scripts with the associated models
in above examples.

On a final note, curiously enough, I wonder if the issue is calling cuda.to()
without telling it everytime to target the second gpu may have been the
problem, I do believe that the scripts where using a variable, but I may
have missed using it in one spot.

When I do get around to this, I will toss the scripts into a git repo, so
they can be reviewed, I have had this working on one gpu for a while and my
scripts have gotta much larger then these.

Thanks again for the prompt responses, hope this at least can give you some
things to try while i find the time to sit and spend a few hours of time in
thus for you guys,

Nix




On Mon, Sep 9, 2024, 14:02 Tim Gu ***@***.***> wrote:

> @nix-wolf <https://github.com/nix-wolf> Hi there! I took a look at your
> initial steps. Would you mind providing a bit more details regarding how
> you set up your system? For example, how did you install ROCm on both your
> host system and inside the container?
>
> Also, just a general note, according to the official docs
> https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.2/how-to/docker.html,
> ROCm in docker relies on the ROCm kernel mode driver on the host system to
> function properly. Hence, a mismatch between the host ROCm version and the
> container ROCm version can result in some discrepancies and unexpected
> behaviors, which may explain some of the errors you are seeing. It might be
> more consistent to ensure the same ROCm version on the host, inside the
> container, and with corresponding supported Pytorch package.
>
> Thanks!
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2804#issuecomment-2338976485>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AH26U4QBZ6TSQQXBWX4GXSDZVX5G5AVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMZYHE3TMNBYGU>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #26 — tcgu-amd (2024-09-11T20:41:20Z)

> Hey, I do believe if you read through the subsequent comments I made relative to trying to figure it out this is one thing I did figure out thay I didn't have rocm installed on the host system. I also found that one of my gou power cables wasn't functioning properly after messing around with it for a while untill the cord went completely dead. So I think there was a possibility that it was associated to improper voltage under "critical load" Off hand I still can't remember exactly what versions, but I think I also recorded all of this in the comments above. Including the fact I switched from using a docker container of centos 7.3(or 9) with the host as fedora 37-39 I think, which I do believe there are some issues with running rocm on fedora because of the glibc version, which is why I was running it in docker in the first place, if I can recall the rationale of why I setup this way in the first place. Eventually I ran into a problem as well that docker wasn't abke to properly manage the fans of the gpus for some access control reasons so I opted to shift the installation to running everything on the host system with centos. Which I do believe doing this may have fixed my issue in part, but also could have been where i discovered my power cable was faulty. Given the centos was coming to end of life I eventually shifter to rocky 9 and I think I have generated 4 or 5k images and even run LLM. I also do believe I am using the newest version of everything. If I'm also not mistaken (which is a separate issue) the problems í was having, or which I'm pretty í may have had idea of how to fix(but can't really recall) was that in my system that disptaches the scripts to be run on the gpus, when á gpu is busy and being used, it targets, or if I run it on the second gpu it crashes, and hangs throwing this error, and the reason why from my research is that there is an issue with rocm's amd cuda's communication to each gpu, and initially the program targets the second gpu loads in all the models, starts working, and defaults to trying to send/fetch data from the wrong gpu, result in access violation. Now, I must apologize, I've been very busy with work as I'm working in oilfield transportation, and work very long hours, and haven't had time as of yet to sit down. If one would be interested in a test, which shouldn't take long. Using Rocky 9.2, and 2 6750xt 12gb, just run any pytorch functions in a long running loop so that it uses at least more then half the gpu ram. And target the second gpu, or use any of the scripts with the associated models in above examples. On a final note, curiously enough, I wonder if the issue is calling cuda.to() without telling it everytime to target the second gpu may have been the problem, I do believe that the scripts where using a variable, but I may have missed using it in one spot. When I do get around to this, I will toss the scripts into a git repo, so they can be reviewed, I have had this working on one gpu for a while and my scripts have gotta much larger then these. Thanks again for the prompt responses, hope this at least can give you some things to try while i find the time to sit and spend a few hours of time in thus for you guys, Nix
> […](#)
> On Mon, Sep 9, 2024, 14:02 Tim Gu ***@***.***> wrote: @nix-wolf <https://github.com/nix-wolf> Hi there! I took a look at your initial steps. Would you mind providing a bit more details regarding how you set up your system? For example, how did you install ROCm on both your host system and inside the container? Also, just a general note, according to the official docs https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.2/how-to/docker.html, ROCm in docker relies on the ROCm kernel mode driver on the host system to function properly. Hence, a mismatch between the host ROCm version and the container ROCm version can result in some discrepancies and unexpected behaviors, which may explain some of the errors you are seeing. It might be more consistent to ensure the same ROCm version on the host, inside the container, and with corresponding supported Pytorch package. Thanks! — Reply to this email directly, view it on GitHub <[#2804 (comment)](https://github.com/ROCm/ROCm/issues/2804#issuecomment-2338976485)>, or unsubscribe <https://github.com/notifications/unsubscribe-auth/AH26U4QBZ6TSQQXBWX4GXSDZVX5G5AVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMZYHE3TMNBYGU> . You are receiving this because you were mentioned.Message ID: ***@***.***>

Hi @nix-wolf, thanks for the quick response! Since neither Fedora, CentOS, or RX 6750 is supported by ROCm officially, we don't have a test system readily available for it. However, we did try to reproduce your issue with a dual RX 6800 setup on a host Ubuntu 22.04 system with ROCm 6.2, using the official pytorch rocm docker image with ROCm 6.2 as well and Unbuntu 20.04. Unfortunately, everything seem to run fine with the scripts you provided. Have you considered trying the official pytorch docker image and see if that works? Thanks!

---

### 评论 #27 — nix-wolf (2024-09-12T14:33:43Z)

Hey,

Thanks for running your test, but I would like to point out the centos,
Rocky, and fedora are rhel forks, so this would be the rpm packages. So the
support version that is most like any of these is rhel 9.2. On top of that
there is significant differences between the setup of things on debian
based distributions and rpm based distributions.



And I did use the pytorch docker image for centos, that is what I was using when this initially started, now as I said I did realize I didn't have anything installed on the host, as originally I was using fedora and I had glibc compatability issues, which is why I switched to am install of centos, which worked fine (I know it's unsupported) then when the issue come back I found the faulty power wire. After replacing that everything has been good accept for using the second gpu, so through a few things and conversations with a linux sys admin I decided to switch to Rocky 9.x which is a package for package fork of Rhel 9.x since that is more supported then centos 7.3 and since centos is being discontinued, I made the switch, and have been using that for some time with no issues accept for a when I target the second device. I should have a few days off of work here and I'll try to sit down and do some tests, as I do believe it is still the same issue, the only difference now is I'm not using docker anymore, I have the steps recorded somewhere. Again. If this can be ran on "rhel 9.2" 

Please,
Nix 

On Wed, Sep 11, 2024, 14:41 Tim Gu ***@***.***> wrote:

> Hey, I do believe if you read through the subsequent comments I made
> relative to trying to figure it out this is one thing I did figure out thay
> I didn't have rocm installed on the host system. I also found that one of
> my gou power cables wasn't functioning properly after messing around with
> it for a while untill the cord went completely dead. So I think there was a
> possibility that it was associated to improper voltage under "critical
> load" Off hand I still can't remember exactly what versions, but I think I
> also recorded all of this in the comments above. Including the fact I
> switched from using a docker container of centos 7.3(or 9) with the host as
> fedora 37-39 I think, which I do believe there are some issues with running
> rocm on fedora because of the glibc version, which is why I was running it
> in docker in the first place, if I can recall the rationale of why I setup
> this way in the first place. Eventually I ran into a problem as well that
> docker wasn't abke to properly manage the fans of the gpus for some access
> control reasons so I opted to shift the installation to running everything
> on the host system with centos. Which I do believe doing this may have
> fixed my issue in part, but also could have been where i discovered my
> power cable was faulty. Given the centos was coming to end of life I
> eventually shifter to rocky 9 and I think I have generated 4 or 5k images
> and even run LLM. I also do believe I am using the newest version of
> everything. If I'm also not mistaken (which is a separate issue) the
> problems í was having, or which I'm pretty í may have had idea of how to
> fix(but can't really recall) was that in my system that disptaches the
> scripts to be run on the gpus, when á gpu is busy and being used, it
> targets, or if I run it on the second gpu it crashes, and hangs throwing
> this error, and the reason why from my research is that there is an issue
> with rocm's amd cuda's communication to each gpu, and initially the program
> targets the second gpu loads in all the models, starts working, and
> defaults to trying to send/fetch data from the wrong gpu, result in access
> violation. Now, I must apologize, I've been very busy with work as I'm
> working in oilfield transportation, and work very long hours, and haven't
> had time as of yet to sit down. If one would be interested in a test, which
> shouldn't take long. Using Rocky 9.2, and 2 6750xt 12gb, just run any
> pytorch functions in a long running loop so that it uses at least more then
> half the gpu ram. And target the second gpu, or use any of the scripts with
> the associated models in above examples. On a final note, curiously enough,
> I wonder if the issue is calling cuda.to() without telling it everytime
> to target the second gpu may have been the problem, I do believe that the
> scripts where using a variable, but I may have missed using it in one spot.
> When I do get around to this, I will toss the scripts into a git repo, so
> they can be reviewed, I have had this working on one gpu for a while and my
> scripts have gotta much larger then these. Thanks again for the prompt
> responses, hope this at least can give you some things to try while i find
> the time to sit and spend a few hours of time in thus for you guys, Nix
> … <#m_2145545405755822034_>
> On Mon, Sep 9, 2024, 14:02 Tim Gu *@*.*> wrote: @nix-wolf
> <https://github.com/nix-wolf> https://github.com/nix-wolf
> <https://github.com/nix-wolf> Hi there! I took a look at your initial
> steps. Would you mind providing a bit more details regarding how you set up
> your system? For example, how did you install ROCm on both your host system
> and inside the container? Also, just a general note, according to the
> official docs
> https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.2/how-to/docker.html
> <https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.2/how-to/docker.html>,
> ROCm in docker relies on the ROCm kernel mode driver on the host system to
> function properly. Hence, a mismatch between the host ROCm version and the
> container ROCm version can result in some discrepancies and unexpected
> behaviors, which may explain some of the errors you are seeing. It might be
> more consistent to ensure the same ROCm version on the host, inside the
> container, and with corresponding supported Pytorch package. Thanks! —
> Reply to this email directly, view it on GitHub <#2804 (comment)
> <https://github.com/ROCm/ROCm/issues/2804#issuecomment-2338976485>>, or
> unsubscribe
> https://github.com/notifications/unsubscribe-auth/AH26U4QBZ6TSQQXBWX4GXSDZVX5G5AVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMZYHE3TMNBYGU
> <https://github.com/notifications/unsubscribe-auth/AH26U4QBZ6TSQQXBWX4GXSDZVX5G5AVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMZYHE3TMNBYGU>
> . You are receiving this because you were mentioned.Message ID: @.*>
>
> Hi @nix-wolf <https://github.com/nix-wolf>, thanks for the quick
> response! Since neither Fedora, CentOS, or RX 6750 is supported by ROCm
> officially, we don't have a test system readily available for it. However,
> we did try to reproduce your issue with a dual RX 6800 setup on a host
> Ubuntu 22.04 system using the official pytorch rocm docker image.
> Unfortunately, everything seem to run fine with the scripts you provided.
> Have you considered trying the official pytorch docker image and see if
> that works? Thanks!
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2804#issuecomment-2344662963>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AH26U4RNA2X2X5OATZOURLLZWCTIPAVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGNBUGY3DEOJWGM>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #28 — tcgu-amd (2024-09-12T20:14:54Z)

@nix-wolf Thanks for the additional information! We were able to successfully reproduce your issue on RHEL 9.3 + ROCM 6.2 with the official docker pytorch image for CentOS+Rocm6.1. We are using two 6800 cards with gfx1030, so the issue likely isn't with your set up. We will investigate further and keep you posted on the updates. Thanks!

---

### 评论 #29 — nix-wolf (2024-09-12T20:16:51Z)

Yes!!!! Super cool! Thanks for the update I will patiently wait!

On Thu, Sep 12, 2024, 14:15 Tim Gu ***@***.***> wrote:

> @nix-wolf <https://github.com/nix-wolf> Thanks for the additional
> information! We were able to successfully reproduce your issue on RHEL 9.3
> + ROCM 6.2 with the official docker pytorch image for CentOS+Rocm6.1. We
> are using two 6800 cards with gfx1030, so the issue likely isn't with your
> set up. We will investigate further and keep you posted on the updates.
> Thanks!
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2804#issuecomment-2347156429>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AH26U4UTMAMHU7GLEP2S5T3ZWHY5LAVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGNBXGE2TMNBSHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #30 — tcgu-amd (2024-09-13T21:21:49Z)

Hi @nix-wolf, a brief update here: It seemed like the error was fairly transient. While I was able to get it in the first run,  I did not get it on the second run and it generated all 200 images without any problems. Not quite sure what I was doing differently but I will try running some work load on GPU1 as well and see what I get. 

On a side note, it does seem like https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#release-known-issues suggest that there's some known issues with ROCm version 6.1 on Radeon cards, especially with multiple work loads. This might explain why the official Ubuntu docker image was doing fine because it had ROCm 6.2. I will verify if 6.2 had any changes to address these issues (might require some digging, not sure if I can find anything but fingers crossed). 

If you have time, please try to see if you can reproduce the issue on 6.2 docker with 6.2 kernel driver on the host if possible. It can help isolate the root cause.

Thanks!

---

### 评论 #31 — nix-wolf (2024-09-14T18:02:39Z)

> Hi @nix-wolf, a brief update here: It seemed like the error was fairly transient. While I was able to get it in the first run, I did not get it on the second run and it generated all 200 images without any problems. Not quite sure what I was doing differently but I will try running some work load on GPU1 as well and see what I get.
> 
> On a side note, it does seem like https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#release-known-issues suggest that there's some known issues with ROCm version 6.1 on Radeon cards, especially with multiple work loads. This might explain why the official Ubuntu docker image was doing fine because it had ROCm 6.2. I will verify if 6.2 had any changes to address these issues (might require some digging, not sure if I can find anything but fingers crossed).
> 
> If you have time, please try to see if you can reproduce the issue on 6.2 docker with 6.2 kernel driver on the host if possible. It can help isolate the root cause.
> 
> Thanks!

Hey, so couple things. 

I'm running everything just on the system. And without docker. I'm using rocm 6.0, I will upgrade tonight to 6.2, and retest the scripts. 

Now when targeting the second gpu using these scripts, you must add "to the line" pipe=*.to("cuda:1") unless there is another way you are isolating it? If so what are you doing to get it to target the second gpu? 

As for known issues it doesn't seem to be that any of this are specifically effectiving my use case. I'm running this on a headless system, no monitors, and I remotely login, and run the scripts or, I hit it from a website I've made, but I do it from another system, so when at idle both gpus are not being used at all. I'm not doing anything more then 2 so it's not massive multiple unit processing. As I'm not even abke to run something against the second card. I'm also not using automatic 1111 webui, I'm just using some basic processes creating stuff from a discord bot, which literally just runs the scripts and returns the image name that's referenced to display the image. I plan to make my own web interface but this portion, running it without issues from cmdline is the first step and when it's stable I'll extent it to a proper web interface. So still these known issues... really don't apply. 

If it observed using rocm-smi when using the .to() of the pipe declaration is does use and offload the information to the selected gpu, but when the second is being used it locks right up. 

I have a little bit of work to do here, and have a lot to record for a follow up, but I think this is a separate issue at this point. As, I think there interjection prior about versioning mismatches being the possible cause of the access issue maybe be along the correct lines. There was also a few other things that transpired. 

Though I am using currently 6.0 on the host and 5.7 in the python env, with no issues generally, unless I use the second gpu, but then it just locks up. 

So: I should probably do what?

-set debugging flags in current setup and see if I can get some information
-try raising python env pytorch rocm v6.0 to align  with system version and retest, if issue exists, re run with debugging and record
-try raising both system rocm and python env rocm to 6.2 and rerun, if not successful rerun with debugging and record

And I mean by debugging as the stuff above, with loglevel changes and other flags I did prior, and pipe it somewhere? 

I just want to confirm that these are the steps I should probably take, maybe a little more long winded, but the information could be invaluable, then im understanding what exactly is going on, esspetially if the issue continues. The reason why I say that is, when you initially tried it, it reproduced, and then you haven't been able to since, when reviewing my posts I had this happen dozens of times everything would seem fine then randomly fail out, requiring entire system reboots. 

I don't think what is going on even now, locked process requiring call to kill system process, is that much different because I have debugged it before and the locking is it trying to send or retrieve data from the wrong gpu, which all in all does fit the description given, "access violation" which can be seen above is itnis writing to protected space, ie. The wrong gpu. 

Now furthermore for what I recall, the reason why I have used mismatched version of rocm, and pytorch-rocm, is that OOM issue. Currently with 6.0 system and 5.7 in Python env I can run the base+pipe, (the first script) with out cpu offload, and it doesn't throw OOM errors even when ot shows ot nearly allocated the entire cards worth of space to the process. Thus could also be resolved with the newest versions. 

And my apologies for the long winded responses í think out loud sometimes and write while I do it. 

---

### 评论 #32 — nix-wolf (2024-09-15T04:06:20Z)

> Hi @nix-wolf, a brief update here: It seemed like the error was fairly transient. While I was able to get it in the first run, I did not get it on the second run and it generated all 200 images without any problems. Not quite sure what I was doing differently but I will try running some work load on GPU1 as well and see what I get.
> 
> On a side note, it does seem like https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#release-known-issues suggest that there's some known issues with ROCm version 6.1 on Radeon cards, especially with multiple work loads. This might explain why the official Ubuntu docker image was doing fine because it had ROCm 6.2. I will verify if 6.2 had any changes to address these issues (might require some digging, not sure if I can find anything but fingers crossed).
> 
> If you have time, please try to see if you can reproduce the issue on 6.2 docker with 6.2 kernel driver on the host if possible. It can help isolate the root cause.
> 
> Thanks!

upgrades to 6.2 on the system, with still running 5.7 in python env seemed to have fixed the problem. so im able ot target and use both of them now. thank you. i did record a bunch of information and logs about the entire process, and basically it kept running into an issue where it just couldnt seem to figure out what gpu to send and recieve data from, like it would have everything loaded into the second gpu, then it would hang waiting for a response from the first gpu, for what ever reason. seems that it would, if i messed around, not have the functions required to be able to do some stuff? anyways, working now, just gotta clean up some code and run some more tests of running them both at the same time in seperatedly started processes, then we will see what i get figured out for running one process against both. Cheers!

---

### 评论 #33 — nix-wolf (2024-09-15T04:53:26Z)

This is running both at the same time from seperate processes, and without using cpu offloading, and no OOM issues. 

though i did find if you are using offload to cpu, it seems that it switches back to using the first gpu(possibly the reason why it was having issues before with trying to send things to the first gpu), but that is likely something to do with diffusers/pytorch rather then rocm, but, it doesnt matter since i dont need to use anything on the cpu anyways!

![image](https://github.com/user-attachments/assets/6a4ab93f-9398-4f17-b6f5-79dfa344fc68)

also for a note, as you can see in the image, that the fan isnt running on the second gpu, ive had issues with the fans kicking in, and out, pretty much the entire time and have to use 'incron' and write to a file the system is watching that triggers running the fan, now i have to add the second gpu fan to it since i wasnt using it before, not a big deal but just something to note that, there is something going on on RHEL based distro, even in 6.2 that isnt allowing the fans to operate properly, im guessing its a permission based thing, since thats what i seemed like to me, to note, when I write to a file, that i have ownership off, the root user is watching for changes and it then setting the fan speed from its place, they do kick down automatically when the process is done running, but... not sure what is going on there and i do think that is a rocm issue. 

anddd spoke to soon, OOM issue came back after it went for the second iteration, not a biggie, and not likely an issue with rocm, ill fiddle with it and get it working ethier way.

---

### 评论 #34 — tcgu-amd (2024-09-16T13:46:11Z)

>Now when targeting the second gpu using these scripts, you must add "to the line" pipe=*.to("cuda:1") unless there is another way you are isolating it? If so what are you doing to get it to target the second gpu?

Interesting. I was simply using the CUDA_VISIBLE_DEVICES env variable to isolate gpu. I will try this to see if anything changes. If it does then the problem is probably with a discrepancy with the ROCm CUDA interfacing layer.

>upgrades to 6.2 on the system, with still running 5.7 in python env seemed to have fixed the problem. so im able ot target and use both of them now.

Glad to hear! So it does seem like an issue specific for ROCm 6.1. I will see if we can find/add to a list of know issues. 

>Also for a note, as you can see in the image, that the fan isnt running on the second gpu, ive had issues with the fans kicking in, and out,

Interesting. It does seem like the fan is perfectly functional on our system running RHEL. Might be due to a subtle incompatibility between the kernel driver and the W6750 card? 

---

### 评论 #35 — nix-wolf (2024-09-16T14:26:43Z)

> > Now when targeting the second gpu using these scripts, you must add "to the line" pipe=*.to("cuda:1") unless there is another way you are isolating it? If so what are you doing to get it to target the second gpu?
> 
> Interesting. I was simply using the CUDA_VISIBLE_DEVICES env variable to isolate gpu. I will try this to see if anything changes. If it does then the problem is probably with a discrepancy with the ROCm CUDA interfacing layer.

I forgot about that one! Now,  what would be the preferred method here? If in the environment your controlling the visible devices, and you want to use the other card st the same time, I could come run another process making only the first one visible and this isn't going to run into issues? Programmatically & pragmatically in the interest of parrelelism, with gpu computing on amd cards, even if I were to not be using pytorch, would I not want to control that from within the running process in order to manage your pool of gpu resources? Or rather would this logically just be 2 separate ways one could be managing the resources from enviroment level, or from process level. I have been figuring that the best way for me to manage my OOM issues would be by creating a managing system that keeps track of used resources, and then using both the gpus cooperatively. But as you said rocm doesn't do this very well, is this because internally it's not manging it and therefore it's up to the implmentor to decide how they want to? 


> > Also for a note, as you can see in the image, that the fan isnt running on the second gpu, ive had issues with the fans kicking in, and out,
> 
> Interesting. It does seem like the fan is perfectly functional on our system running RHEL. Might be due to a subtle incompatibility between the kernel driver and the W6750 card?

Maybe, but given the technical specs between the 6700, and the 6750 the hardware is identical if I'm not mistaken, it just is a naturally overclocked 6700 essentially. If you go back to my post from Jan 14th, about there being nohipbinaryforgpu, maybe it has something to do with that? I haven't checked with the 6.2 installation if when running loglevel 4 if that still comes up, but I suspectd that because 1031 is the actual architecture is the system not generating the bytecode for the gpu at installation since no "1030" exists in the system? Or am I suppose to generate this myself? If so how am I to ensure I have the hip binary for 1030? 

My apologies for subsequent questioning, if in fact it is bothersome, I'm a curious wonderer. 

---

### 评论 #36 — tcgu-amd (2024-09-16T19:26:14Z)

@nix-wolf No worries! Happy to answer your questions. Regarding your first question, running with CUDA_VISIBLE_DEVICES isolates the GPU at the ROCm runtime layer for the particular process i.e. python in your case. Hence, you won't be able to target the other GPU in this case from within python, which runs above the runtime layer. If you are looking for memory flexibility, then I think targeting GPUs from within Python would be the way to do it. 

For your second question, on a second thought, I think if you have been able to run sdxl workloads with 1031, then the driver for ROCm is working. However, I have no idea why the fans won't work. They should be controlled via amdgpu driver, which would be available for your card. There could be a lot of potential issue that affects the fan speed, from BIOS to kernel configurations. I would check your power management options on your system. It is *probably* not a direct problem with ROCm. 

---

### 评论 #37 — nix-wolf (2024-09-16T19:39:38Z)

@tcgu-amd for long running multi-threaded processes yea that's what I expect, from within. From the one instance I am spawning off processes from a webservice so it would be easy to just isolate the gpus using that. On the other side I was going to play with loading in segments and handling more of a specific layer, the shift it to the second gpu with the second layer, then offload back to the system. I also was going to play with more just strictly mathematical operations opposed to AI workloads, but I would like to handle that in c++ since that's where I have most of that code written. Ethier way good to know. I appreciate it. 

Well... it's not using ethier of them to 1030, nor 1031. As I said if you look at those posts with quoted runtime information it specifically says this

```
:1:hip_code_object.cpp      :516 : 1349537983 us: [pid:224   tid:0x7ff81ad1d740] hipErrorNoBinaryForGpu: Unable to find code object for all current devices!
:1:hip_code_object.cpp      :517 : 1349537997 us: [pid:224   tid:0x7ff81ad1d740]   Devices:
:1:hip_code_object.cpp      :520 : 1349538005 us: [pid:224   tid:0x7ff81ad1d740]     amdgcn-amd-amdhsa--gfx1030 - [Not Found]
:1:hip_code_object.cpp      :524 : 1349538008 us: [pid:224   tid:0x7ff81ad1d740]   Bundled Code Objects:
:1:hip_code_object.cpp      :540 : 1349538011 us: [pid:224   tid:0x7ff81ad1d740]     host-x86_64-unknown-linux-- - [Unsupported]
:1:hip_code_object.cpp      :538 : 1349538014 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack+]
:1:hip_code_object.cpp      :538 : 1349538017 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx90a:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx90a:xnack-]
:1:hip_code_object.cpp      :538 : 1349538020 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx940:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx940:xnack+]
:1:hip_code_object.cpp      :538 : 1349538023 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx940:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx940:xnack-]
:1:hip_code_object.cpp      :538 : 1349538025 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx941:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx941:xnack+]
:1:hip_code_object.cpp      :538 : 1349538028 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx941:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx941:xnack-]
:1:hip_code_object.cpp      :538 : 1349538031 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx942:xnack+ - [code object targetID is amdgcn-amd-amdhsa--gfx942:xnack+]
:1:hip_code_object.cpp      :538 : 1349538034 us: [pid:224   tid:0x7ff81ad1d740]     hipv4-amdgcn-amd-amdhsa--gfx942:xnack- - [code object targetID is amdgcn-amd-amdhsa--gfx942:xnack-]
:1:hip_code_object.cpp      :544 : 1349538037 us: [pid:224   tid:0x7ff81ad1d740] hipErrorNoBinaryForGpu: Unable to find code object for all current devices! - 209
:1:hip_fatbin.cpp           :274 : 1349538040 us: [pid:224   tid:0x7ff81ad1d740] hipErrorNoBinaryForGpu: Couldn't find binary for ptr: 0xa7861000
:3:hip_platform.cpp         :672 : 1349538047 us: [pid:224   tid:0x7ff81ad1d740] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
```

Since I'm forcing 1030, in the environment variable, and it cannot find its just running it anyways, but cannot find 1030, but it also doesn't have 1031 ethier. 

I have poked around about compiling them myself but... the docs are crazy sparse and there really isn't much information kicking around about this. 

---

### 评论 #38 — tcgu-amd (2024-09-16T21:44:33Z)

@nix-wolf Is this the result from running it with HSA_OVERRIDE_GFX_VERSION=10.3.0? 

Also, if you want to build for a specific architecture, you can try set it here https://github.com/ROCm/ROCm/blob/6695142803f60b08692bdd7625d8047477035282/README.md?plain=1#L132. 

But building ROCm generally takes quite long, so be prepared. For starters, you can try to only build and install dkms on the host system. 

By the way, I notice we have diverged to quite a different topic? Would you consider the original issue resolved by upgrading to 6.2? If so I will mark this issue closed but we can continue the discussion if you like!

---

### 评论 #39 — nix-wolf (2024-09-17T01:29:57Z)

@tcgu-amd 

Yes this is what happens when running that, it's if I don't run it with thay specific export then I do believe cuda cannot see the cards at all. As the solution to not being able to see the cards for me was that, but I do believe there is also other operating issues, I haven't don't it in a while but when I setup my server with the webservice every once in a while I forget to export the override and it spits out some, "no cuda devices available" error.  I have built it before, I have a decent work station 5950x and 64gb of ram with 2 nvme 1tb in raid 10, so haha. I'm sure it won't take any longer then the unreal engine from source to compile. Though I think things brings forth an entirely different set of questions about the packaging of rocm. Since the repo is something you guys supply it is your choice for what it comes Bundled with. Why exactly is the base repository not including all supported architectures? At least where the byte code is concerned. Given the way the repos are structured... supported or not, could there be a possibility of an effort to included externally installable packages for each set of bytecode for each architecture? They are their own seperately compiled thing, and is on the system it's own file... the practical implementation to effectively add this to the rocm repository... should be relatively trival, just the compile time, and ensuring that each seperate package installs the architectures bytecode to the proper system location. If I'm not mistaken from my research prior, it has something to do with using llvm to compile the architecture bytecode?(it has been some months so I definitely could be mistaken here) That is doing it without compiling the entire rocm source with ALL archs then pulling the files out. As I do believe I attempted this prior to my 5950x upgrade(from a 3950x) and it was a lengthy task. Also from a service side, offering the extension in the repo for installation would be very nice. I'd be more then happy to do the work if you could point me in the direction of manually compiling the gpu byte code(to save me some time).

I think it's sort of inconclusive. Because I haven't had the issue for some time, I had solved it a while back while running 6.0, and 5.7, after shifting itnto the host from docker. And the issue I was left with was the locking up using the second gpu, and then this where the bytecode doesn't exist. I also had a bad power cable on one gpu, and after switching that it seemed to have stopped for me. I was pretty certain that was my issue, as after everything seemed to work, but the above issues, but then you were abke to reproduce it. I think the greater question here is. Given that this error seems to come up for numerous different things on different systems, not very often but it does, is why. Since it seems to not be a specific thing.

so the issue that was solved by the upgrade to 6.2 was the second gpu locking up when attemping to use it. that is certain. as for the access fault, im not sure, specifically what it was, as you created it with a docker setup, then fixed it with the upgrade. so maybe it was more specific to that. as i made the switch to having it on the host instead of docker. I only was using docker because of the glibc issues with fedora, so the assertion that not having rocm on the host being the primary cause i think is reasonable. now that im on a system that can install it to the host running rocky, I dont know if i recall having issues. even though I know prior to switching as I said as long as i didnt attempt to  run anythingon the second gpu with fedora as the host i wouldnt have any issues, and i think there was a time i just left the gpu out of the server. then I wanted to try again and thats when I think i installed centos to it instead of fedora, then switched to rocky. I would say its entirely up to you if you wish to close to this, and what to decide the solution as. I think the most important take away here for any people finding their way here having this issue will be making sure, that their compatiable versions are used, and that host, and container are at least running the same. and of course sometimes just double check your power cables HAHA. the second thing aswell is there is a pretty good, tutorial on setting this stuff up from fresh install(which seems to be a lacking thing out there) with some examples of code of getting it to work with stable diffusion as I have set it up myself using this, a few dozen times now. LOL

---

### 评论 #40 — tcgu-amd (2024-09-17T13:45:03Z)

Okay. I think I will be closing this issue for now, as I think its getting any longer without being closed probably will not help anyone who came in looking for a solution/work around to the problem in the title anymore.. 

> Since the repo is something you guys supply it is your choice for what it comes Bundled with. Why exactly is the base repository not including all supported architectures

Shipping ROCm for an architecture is generally a complex process that involves engineering, business, and QA, so it is not exactly simple to add everything to the repo. *In most cases*, as long as your card is fairly new, it should work with ROCm, even if it is not supported. It is just that we are not sure it will be stable because a) ROCm wasn't designed with this particular architecture in mind, and/or b) we did not do QA's for it so we don't know if anything will go wrong, hence we can't add it to the main repo...

---

### 评论 #41 — nix-wolf (2024-09-17T13:58:56Z)

Ok.

So what exactly is the purpose of the bytecode anyways? Obviously things
work fine without, and as you stated the focus of rocm isn't to be
architecture specific, which is just logically good programming. So
compiling for an architecture gives what advantages? Would it help things
like the OOM errors because the system is abke to better logically to
allocate resources?

On Tue, Sep 17, 2024, 07:45 Tim Gu ***@***.***> wrote:

> Okay. I think I will be closing this issue for now, as I think its getting
> any longer without being closed probably will not help anyone who came in
> looking for a solution/work around to the problem in the title anymore..
>
> Since the repo is something you guys supply it is your choice for what it
> comes Bundled with. Why exactly is the base repository not including all
> supported architectures
>
> Shipping ROCm for an architecture is generally a complex process that
> involves engineering, business, and QA, so it is not exactly simple to add
> everything to the repo. *In most cases*, unless your card is fairly new,
> it should work with ROCm, even if it is not supported. It is just that we
> are not sure it will be stable because a) ROCm wasn't designed with this
> particular architecture in mind, and/or b) we did not do QA's for it so we
> don't know if anything will go wrong, hence we can't add it to the main
> repo...
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2804#issuecomment-2355860680>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AH26U4QFNTW54WQKUOOT2W3ZXAW7NAVCNFSM6AAAAABBYXRKNOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGNJVHA3DANRYGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #42 — tcgu-amd (2024-09-17T17:47:44Z)

> So what exactly is the purpose of the bytecode anyways? Obviously things
work fine without, and as you stated the focus of rocm isn't to be
architecture specific, which is just logically good programming. So
compiling for an architecture gives what advantages? Would it help things
like the OOM errors because the system is abke to better logically to
allocate resources?

Different architectures can result in different interfaces or even instruction sets at the hardware level. Performance optimization is also often architecture specific. AMD is constantly upgrading the hardware with new technology and ROCm's updates partially reflect that. 

---
