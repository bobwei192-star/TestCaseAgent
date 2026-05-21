# [Issue]: Soft lockup when having high vram usage

> **Issue #3580**
> **状态**: closed
> **创建时间**: 2024-08-14T00:05:49Z
> **更新时间**: 2025-07-01T21:59:55Z
> **关闭时间**: 2025-07-01T21:59:55Z
> **作者**: hartmark
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3580

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

I have AMD Radeon RX 7800 XT 16 GB, I couldn't select it in the list.

I'm having problem with soft locks when generating stable diffusion images. I need to restart lightdm or do a sysrq-r,e,i to kill all processes.

### Operating System

Arch Linux

### CPU

AMD Ryzen 9 5900X 12-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

I'm running ComfyUI in a docker container. I have created a repo for the docker compose script. You can use this to reproduce the problem.
1. clone https://github.com/hartmark/sd-rocm
2. download absolutereality model at https://civitai.com/models/81458/absolutereality and save it at `data/checkpoints`
3. Startup the docker container with `docker-compose up`
4. Wait until ComfyUI have started
5. Go to ComfyUI at http://localhost
6. Load this workflow and run
[workflow.json](https://github.com/user-attachments/files/16606555/workflow.json)


It crashes on the first VAE decode

If I generate a smaller image like 1024x1024 or lower It will sometimes generate the whole workflow or fail on the second KSampler



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
Runtime Ext Version:     1.6
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
  Name:                    AMD Ryzen 9 5900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5900X 12-Core Processor
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
  Max Clock Freq. (MHz):   3700                               
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
      Size:                    32767952(0x1f3ffd0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32767952(0x1f3ffd0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32767952(0x1f3ffd0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1101                            
  Uuid:                    GPU-8e404be42e45fb92               
  Marketing Name:          AMD Radeon RX 7800 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29822(0x747e)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2169                               
  BDFID:                   2560                               
  Internal Node ID:        1                                  
  Compute Unit:            60                                 
  SIMDs per CU:            2                                  
  Shader Engines:          3                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 222                                
  SDMA engine uCode::      22                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1101         
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

### Additional Information

I have previous filed an bug at AMDGPU project but I think the issue is something ROCm related.
https://gitlab.freedesktop.org/drm/amd/-/issues/3548

---

## 评论 (60 条)

### 评论 #1 — 2eQTu (2024-08-14T00:34:54Z)

FYI to AMD folks, the POC issue bot assigned the wrong label for hardware.   Per output above, submitter is talking about an "AMD Radeon RX 7800 XT" , but no such label exists and the bot assigned "AMD Radeon RX 7900 XT" instead.

---

### 评论 #2 — harkgill-amd (2024-08-19T15:10:01Z)

Hi @hartmark, thank you for providing the steps to reproduce. We will try to reproduce the issue internally and investigate it from there. 

---

### 评论 #3 — hartmark (2024-08-19T15:22:34Z)

> Hi @hartmark, thank you for providing the steps to reproduce. We will try to reproduce the issue internally and investigate it from there.

Cool, just poke me if you need more details regarding my setup.

---

### 评论 #4 — hartmark (2024-08-20T22:18:17Z)

I have noticed that this is also a certain way to reproduce the issue:
https://github.com/ROCm/ROCm/issues/2196#issuecomment-2295441030

---

### 评论 #5 — hartmark (2024-08-23T15:06:44Z)

I saw that ROCm 6.2 python torch libraries have been released so I have updated my docker-compose.repo.

I also may have found a workaround for the lockups, ComfyUI released a --reserve-vram flag and setting it to 6.0 seems to fixed my issue with random lockups.
`--reserve-vram 6`

https://github.com/comfyanonymous/ComfyUI/commit/045377ea893d0703e515d87f891936784cb2f5de

Even though I have set reserve limit to 6GB I have almost all gpu memory used
![image](https://github.com/user-attachments/assets/81be86f4-6337-4df5-b4d5-531fef61965f)

This is my full ComfyUI startup-line for reference:
`PYTORCH_HIP_ALLOC_CONF=expandable_segments:True python main.py --listen 0.0.0.0 --port 80 --use-split-cross-attention --front-end-version Comfy-Org/ComfyUI_frontend@latest --reserve-vram 6`

---

### 评论 #6 — hartmark (2024-08-23T15:20:15Z)

I may have been to quick to hope for success. After the KSampler step completed it was on "VAE decode" for ages and after a while I got a lockup but it seems python libs was unhappy.

See attached journalctrl log
[journalctl.txt](https://github.com/user-attachments/files/16730667/journalctl.txt)


---

### 评论 #7 — hartmark (2024-08-23T15:50:21Z)

I have tested some more and it seems that ComfyUI just gets out of memory now and doesn't try to use system ram to continue.

I have tried using --lowvram and still get no system ram used.

---

### 评论 #8 — hartmark (2024-08-24T01:29:16Z)

It seems I still have problems where my whole computer locks up, not even altgr-rei can make me recover and there's nothing in the kernel log.

---

### 评论 #9 — alexxu-amd (2024-08-26T21:20:26Z)

Hi @hartmark ,
Thank you for your patience. For the past few days, we've been attempting to reproduce this issue with various configurations. Just an update that we are able to reproduce this issue. The lockup can happen during the KSampler step or the VAE step when generating a 2048 * 2048 image. So far, it seems `--no-half-vae` flag from the webui does help with the VAE lockup, but the system could still encounter the lockup during KSampler. We will investigate further and keep you updated.

---

### 评论 #10 — hartmark (2024-08-26T21:39:18Z)

> Hi @hartmark , Thank you for your patience. For the past few days, we've been attempting to reproduce this issue with various configurations. Just an update that we are able to reproduce this issue. The lockup can happen during the KSampler step or the VAE step when generating a 2048 * 2048 image. So far, it seems `--no-half-vae` flag from the webui does help with the VAE lockup, but the system could still encounter the lockup during KSampler. We will investigate further and keep you updated.

Hmm, it seems there is no --no-half-vae

```
stable-diffusion-comfyui-1  | usage: main.py [-h] [--listen [IP]] [--port PORT] [--tls-keyfile TLS_KEYFILE]
stable-diffusion-comfyui-1  |                [--tls-certfile TLS_CERTFILE] [--enable-cors-header [ORIGIN]]
stable-diffusion-comfyui-1  |                [--max-upload-size MAX_UPLOAD_SIZE]
stable-diffusion-comfyui-1  |                [--extra-model-paths-config PATH [PATH ...]]
stable-diffusion-comfyui-1  |                [--output-directory OUTPUT_DIRECTORY]
stable-diffusion-comfyui-1  |                [--temp-directory TEMP_DIRECTORY]
stable-diffusion-comfyui-1  |                [--input-directory INPUT_DIRECTORY] [--auto-launch]
stable-diffusion-comfyui-1  |                [--disable-auto-launch] [--cuda-device DEVICE_ID]
stable-diffusion-comfyui-1  |                [--cuda-malloc | --disable-cuda-malloc]
stable-diffusion-comfyui-1  |                [--force-fp32 | --force-fp16]
stable-diffusion-comfyui-1  |                [--bf16-unet | --fp16-unet | --fp8_e4m3fn-unet | --fp8_e5m2-unet]
stable-diffusion-comfyui-1  |                [--fp16-vae | --fp32-vae | --bf16-vae] [--cpu-vae]
stable-diffusion-comfyui-1  |                [--fp8_e4m3fn-text-enc | --fp8_e5m2-text-enc | --fp16-text-enc | --fp32-text-enc]
stable-diffusion-comfyui-1  |                [--force-channels-last] [--directml [DIRECTML_DEVICE]]
stable-diffusion-comfyui-1  |                [--disable-ipex-optimize]
stable-diffusion-comfyui-1  |                [--preview-method [none,auto,latent2rgb,taesd]]
stable-diffusion-comfyui-1  |                [--cache-classic | --cache-lru CACHE_LRU]
stable-diffusion-comfyui-1  |                [--use-split-cross-attention | --use-quad-cross-attention | --use-pytorch-cross-attention]
stable-diffusion-comfyui-1  |                [--disable-xformers]
stable-diffusion-comfyui-1  |                [--force-upcast-attention | --dont-upcast-attention]
stable-diffusion-comfyui-1  |                [--gpu-only | --highvram | --normalvram | --lowvram | --novram | --cpu]
stable-diffusion-comfyui-1  |                [--reserve-vram RESERVE_VRAM]
stable-diffusion-comfyui-1  |                [--default-hashing-function {md5,sha1,sha256,sha512}]
stable-diffusion-comfyui-1  |                [--disable-smart-memory] [--deterministic] [--fast]
stable-diffusion-comfyui-1  |                [--dont-print-server] [--quick-test-for-ci]
stable-diffusion-comfyui-1  |                [--windows-standalone-build] [--disable-metadata]
stable-diffusion-comfyui-1  |                [--disable-all-custom-nodes] [--multi-user] [--verbose]
stable-diffusion-comfyui-1  |                [--front-end-version FRONT_END_VERSION]
stable-diffusion-comfyui-1  |                [--front-end-root FRONT_END_ROOT]
stable-diffusion-comfyui-1  | main.py: error: unrecognized arguments: --no-half-vae
```


---

### 评论 #11 — alexxu-amd (2024-08-27T13:22:53Z)

The `--no-half-vae` flag is for the webui. So in this case, it is added to your startup-webui.sh file:
`python3 launch.py --skip-python-version-check --enable-insecure-extension-access --listen --port 81 --api --precision full --no-half --no-half-vae`

---

### 评论 #12 — hartmark (2024-08-27T13:28:39Z)

> The `--no-half-vae` flag is for the webui. So in this case, it is added to your startup-webui.sh file: `python3 launch.py --skip-python-version-check --enable-insecure-extension-access --listen --port 81 --api --precision full --no-half --no-half-vae`

Aha, I'm mostly using comfyUI, is there any workaround for it as well?

---

### 评论 #13 — schung-amd (2024-08-28T16:47:54Z)

At a glance, I believe the equivalent flags here are `--force-fp32` and `--fp32-vae`.

---

### 评论 #14 — hartmark (2024-08-31T01:38:30Z)

> At a glance, I believe the equivalent flags here are `--force-fp32` and `--fp32-vae`.

These flags seems to have helped the stability. It took around 10 minutes to get the KSampler finished but the Decode VAE step was taking forever, I aborted after 30 minutes. Good thing is that it didn't crash consistently after just a few seconds.

However, if I run this workflow it does crash consistently again.
https://github.com/ROCm/ROCm/issues/3580#issuecomment-2299857204
I got it to work with setting just 512x512 and added `--lowvram --reserve-vram 3` and also switched to use flux GGUF  G5_1.

Is there any more logging I can enable or make the debugging easier to pinpoint the issue?

---

### 评论 #15 — gongdao123 (2024-09-25T09:59:06Z)

My case was using vLLM, if I set gpu_memory_utilization above 0.95.
Will very easily trigger GPU hang when doing inferencing

---

### 评论 #16 — hartmark (2024-10-14T00:34:01Z)

> Is there any more logging I can enable or make the debugging easier to pinpoint the issue?

Any news about this issue and is there any debugging I can do?


---

### 评论 #17 — schung-amd (2024-10-15T20:53:27Z)

Hi @hartmark, sorry for the delay, I've taken a look at this. I couldn't get ComfyUI to run using your Docker (I suspect due to torch versions), so I installed ComfyUI and its dependencies natively instead. Regarding torch package versions, I recommend using wheels from repo.radeon.com instead of the nightly builds. In this case, for ROCm 6.2.1, I used torch wheels from https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/, specifically torch 2.3.0+rocm-6.2.0, pytorch-triton 2.3.0+rocm-6.2.0, and torchvision 0.18.0+rocm6.2.0, and also specified numpy==1.26.4 as these wheels are incompatible with later numpy versions. Similar instructions for ROCm 6.2.3 can be found at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html.

I'm able to complete the workflow in your original post without `--force-fp32` and `--fp32-vae` without crashing. My system is on Arch with the torch versions stated above, ROCm 6.2.1 via `opencl-amd` and `opencl-amd-dev`, and Python 3.10 on a 7900XTX. When you refer to a soft lockup, how long have you waited for the workflow to finish? It takes about 5 minutes on the 7900XTX, but the peak VRAM usage is above 21GB which exceeds what the 7800XT has, which would likely result in a longer runtime.

---

### 评论 #18 — hartmark (2024-10-16T00:06:41Z)

What errors do you get when running my docker container?

I tried to install the wheels you linked.
```
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/pytorch_triton_rocm-2.3.0%2Brocm6.2.0.1540b42334-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/onnxruntime_rocm-1.18.0-cp39-cp39-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/pytorch_triton_rocm-2.3.0%2Brocm6.2.0.1540b42334-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/torch-2.3.0%2Brocm6.2.0-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2/torchvision-0.18.0%2Brocm6.2.0-cp310-cp310-linux_x86_64.whl
find *.whl | xargs pip3 install
```
But I get this error:
`ERROR: onnxruntime_rocm-1.18.0-cp39-cp39-linux_x86_64.whl is not a supported wheel on this platform.`


About the soft lockups:
Before I was getting that the whole system froze and I could only switch to a virtual terminal. But that was on X11 using xfce. I have migrated over to Kde Plasma on Wayland and now the system doesn't seem to freeze any more, but it becomes very sluggish and slow. I haven't tried the workflow for a while because even simple generations using flux with 512x512 with control net seems to take a while to generate.

---

### 评论 #19 — schung-amd (2024-10-16T13:25:17Z)

> What errors do you get when running my docker container?

I can start the docker and access the UI, but the workflow fails almost immediately with 
```
CLIPTextEncode
Attempting to use hipBLASLt on a unsupported architecture!
```

> I tried to install the wheels you linked.
...
But I get this error:
ERROR: onnxruntime_rocm-1.18.0-cp39-cp39-linux_x86_64.whl is not a supported wheel on this platform.

You can probably skip the onnx runtime wheel in that repo, in my experience it's mainly torch, torchvision, and triton that matter. I think the error is complaining about python version, as that wheel is for 3.9 and the others are for 3.10.

---

### 评论 #20 — sohaibnd (2024-10-22T19:25:43Z)

Hi @hartmark, I was able to reproduce your issue on Arch (kernel version 6.11.1) with a 7800XT and the **original** repro steps you provided (no flags added other than what is already present in your setup scripts). Based on the error I am seeing in the journalctl log (`kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!`), I suspect this could be a driver regression. Can you try downgrading your kernel to 6.8.2 and check if the issue is still present?

---

### 评论 #21 — hartmark (2024-10-23T22:15:45Z)

> > What errors do you get when running my docker container?
> 
> I can start the docker and access the UI, but the workflow fails almost immediately with
> 
> ```
> CLIPTextEncode
> Attempting to use hipBLASLt on a unsupported architecture!
> ```
> 
> > I tried to install the wheels you linked.
> > ...
> > But I get this error:
> > ERROR: onnxruntime_rocm-1.18.0-cp39-cp39-linux_x86_64.whl is not a supported wheel on this platform.
> 
> You can probably skip the onnx runtime wheel in that repo, in my experience it's mainly torch, torchvision, and triton that matter. I think the error is complaining about python version, as that wheel is for 3.9 and the others are for 3.10.

I tried again without any luck.

```
(venv-comfyui) (base) root@96e6cd1ccc18:~# rm onnxruntime_rocm-1.18.0-cp39-cp39-linux_x86_64.whl 
(venv-comfyui) (base) root@96e6cd1ccc18:~# find *.whl | xargs pip3 install
ERROR: pytorch_triton_rocm-2.3.0+rocm6.2.0.1540b42334-cp310-cp310-linux_x86_64.whl is not a supported wheel on this platform.
(venv-comfyui) (base) root@96e6cd1ccc18:~# python --version
Python 3.12.4
(venv-comfyui) (base) root@96e6cd1ccc18:~# ls *.whl
pytorch_triton_rocm-2.3.0+rocm6.2.0.1540b42334-cp310-cp310-linux_x86_64.whl  torchvision-0.18.0+rocm6.2.0-cp310-cp310-linux_x86_64.whl
torch-2.3.0+rocm6.2.0-cp310-cp310-linux_x86_64.whl
```

About your warning, try add this line before starting comfyui:
`export TORCH_BLAS_PREFER_HIPBLASLT=0`

See this thread:
https://github.com/pytorch/pytorch/issues/138067#issuecomment-2423237687


---

### 评论 #22 — hartmark (2024-10-23T22:28:16Z)

Update, I get the same error as @schung-amd now "Attempting to use hipBLASLt on a unsupported architecture!"

Even with the export, I found further down in the thread that there was some issues and adding this instead works:
export DISABLE_ADDMM_CUDA_LT=1



---

### 评论 #23 — sohaibnd (2024-10-23T22:30:35Z)

> Update, I get the same error as @schung-amd now "Attempting to use hipBLASLt on a unsupported architecture!"
> 
> Even with the export, I found further down in the thread that there was some issues and adding this instead works: export DISABLE_ADDMM_CUDA_LT=1

@hartmark How are you running it right now?



---

### 评论 #24 — schung-amd (2024-10-23T22:35:05Z)

> (venv-comfyui) (base) root@96e6cd1ccc18:~# python --version
> Python 3.12.4

Those wheels need python 3.10, I think that should resolve this error.

---

### 评论 #25 — hartmark (2024-10-23T22:41:10Z)

> > Update, I get the same error as @schung-amd now "Attempting to use hipBLASLt on a unsupported architecture!"
> > Even with the export, I found further down in the thread that there was some issues and adding this instead works: export DISABLE_ADDMM_CUDA_LT=1
> 
> @hartmark How are you running it right now?

I connected to my docker container and removed torch and installed latest:
1. sudo docker exec -ti sd-rocm-stable-diffusion-comfyui-1
2. cd
3. /opt/conda/bin/python3 -m venv "venv-$DOCKER_INSTANCE"
4. source "venv-$DOCKER_INSTANCE/bin/activate"
5. pip3 uninstall torch torchaudio torchvision safetensors pytorch_triton -y
6. pip3 install --pre \
        torch torchaudio torchvision safetensors \
        --index-url https://download.pytorch.org/whl/nightly/rocm6.2 \
        --root-user-action=ignore

Then I just restarted the docker compose and my killing workflow seems to still be running now after some initial testing of other workflows.

---

### 评论 #26 — sohaibnd (2024-10-23T23:01:22Z)

> Hi @hartmark, I was able to reproduce your issue on Arch (kernel version 6.11.1) with a 7800XT and the **original** repro steps you provided (no flags added other than what is already present in your setup scripts). Based on the error I am seeing in the journalctl log (`kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!`), I suspect this could be a driver regression. Can you try downgrading your kernel to 6.8.2 and check if the issue is still present?

Alright, have you tried the suggestion above to downgrade the kernel?

Also, as @schung-amd suggested above, please try using the pytorch wheels from repo.radeon.com instead of the nightly builds.


---

### 评论 #27 — hartmark (2024-10-23T23:05:22Z)

I get new behavior and error now on my killing workflow.

Every step up before "VAE decode" the system is responsive and the GPU is spinning up fans but besides that no issues.

When entering "VAE decode" I get that the computer is sluggish, it's like the monitor gets stuck 4-5 seconds once per 20-30 seconds.

Then after like 6-7 minutes I got a black screen and the GPU hang error and I needed to do alt-gr-r,e,i to reboot kde plasma.

This is what I get from journalctl:
[journalctl.log](https://github.com/user-attachments/files/17499013/journalctl.log)

It seems the GPU hang recovery was unsuccessful

---

### 评论 #28 — hartmark (2024-10-23T23:10:37Z)

> Alright, have you tried the suggestion above to downgrade the kernel?

Not yet, I was going to try once again and see how it behaved with new pytorch and comfyui as they move quite fast with new code.

I will also try using python 3.10 and install the wheels, are they more stable? It seems everything in ROCm space is quite fast moving so I guess any random time in the nightly is as stable as any manually tagged release version. Correct me if I'm wrong.

---

### 评论 #29 — sohaibnd (2024-10-23T23:10:45Z)

> > > Update, I get the same error as @schung-amd now "Attempting to use hipBLASLt on a unsupported architecture!"
> > > Even with the export, I found further down in the thread that there was some issues and adding this instead works: export DISABLE_ADDMM_CUDA_LT=1
> > 
> > 
> > @hartmark How are you running it right now?
> 
> I connected to my docker container and removed torch and installed latest:
> 
> 1. sudo docker exec -ti sd-rocm-stable-diffusion-comfyui-1
> 2. cd
> 3. /opt/conda/bin/python3 -m venv "venv-$DOCKER_INSTANCE"
> 4. source "venv-$DOCKER_INSTANCE/bin/activate"
> 5. pip3 uninstall torch torchaudio torchvision safetensors pytorch_triton -y
> 6. pip3 install --pre 
>    torch torchaudio torchvision safetensors 
>    --index-url https://download.pytorch.org/whl/nightly/rocm6.2 
>    --root-user-action=ignore
> 
> Then I just restarted the docker compose and my killing workflow seems to still be running now after some initial testing of other workflows.

This is after following these steps correct? and can you please provide your kernel version?

---

### 评论 #30 — hartmark (2024-10-23T23:12:38Z)

> > > > Update, I get the same error as @schung-amd now "Attempting to use hipBLASLt on a unsupported architecture!"
> > > > Even with the export, I found further down in the thread that there was some issues and adding this instead works: export DISABLE_ADDMM_CUDA_LT=1
> > > 
> > > 
> > > @hartmark How are you running it right now?
> > 
> > 
> > I connected to my docker container and removed torch and installed latest:
> > 
> > 1. sudo docker exec -ti sd-rocm-stable-diffusion-comfyui-1
> > 2. cd
> > 3. /opt/conda/bin/python3 -m venv "venv-$DOCKER_INSTANCE"
> > 4. source "venv-$DOCKER_INSTANCE/bin/activate"
> > 5. pip3 uninstall torch torchaudio torchvision safetensors pytorch_triton -y
> > 6. pip3 install --pre
> >    torch torchaudio torchvision safetensors
> >    --index-url https://download.pytorch.org/whl/nightly/rocm6.2
> >    --root-user-action=ignore
> > 
> > Then I just restarted the docker compose and my killing workflow seems to still be running now after some initial testing of other workflows.
> 
> This is after following these steps correct? and can you please provide your kernel version?

yes, just do the commands in a new command window and then ctrl-c the docker compose command and start it again so it boots up with the latest pytorch

```
markus@bernard ~ % uname -a
Linux bernard 6.11.4-arch2-1 #1 SMP PREEMPT_DYNAMIC Sun, 20 Oct 2024 18:20:12 +0000 x86_64 GNU/Linux

```

---

### 评论 #31 — hartmark (2024-10-23T23:23:29Z)

I have downgraded to 6.8.2 now and running the workflow again. I have also pushed the fix with DISABLE_ADDMM_CUDA_LT=1

Now I get the python to get killed without pulling the whole desktop with it.

This is the log from docker:

```
stable-diffusion-comfyui-1  | loaded completely 0.0 1639.406135559082 True
100%|██████████| 20/20 [03:05<00:00,  9.25s/it]
stable-diffusion-comfyui-1  | Requested to load AutoencoderKL
stable-diffusion-comfyui-1  | Loading 1 new model
stable-diffusion-comfyui-1  | loaded completely 0.0 319.11416244506836 True
stable-diffusion-comfyui-1  | HW Exception by GPU node-1 (Agent handle: 0x83dc630) reason :GPU Hang
stable-diffusion-webui-1    | HW Exception by GPU node-1 (Agent handle: 0x8bfc900) reason :GPU Hang
stable-diffusion-webui-1    | /conf/startup-webui.sh: line 30:    24 Aborted                 (core dumped) python3 launch.py --skip-python-version-check --enable-insecure-extension-access --listen --port 81 --api --precision full --no-half --no-half-vae
stable-diffusion-comfyui-1  | /conf/startup-comfyui.sh: line 43:    24 Aborted                 (core dumped) python main.py --listen 0.0.0.0 --port 80 --front-end-version Comfy-Org/ComfyUI_frontend@latest --reserve-vram 6
```

journalctl:
[journalctl_linux6.8.2.log](https://github.com/user-attachments/files/17499092/journalctl_linux6.8.2.log)

```
% uname -a
Linux bernard 6.8.2-arch2-1 #1 SMP PREEMPT_DYNAMIC Thu, 28 Mar 2024 17:06:35 +0000 x86_64 GNU/Linux
```

The hang happens on VAE decode.

---

### 评论 #32 — schung-amd (2024-10-23T23:28:24Z)

> I will also try using python 3.10 and install the wheels, are they more stable? It seems everything in ROCm space is quite fast moving so I guess any random time in the nightly is as stable as any manually tagged release version. Correct me if I'm wrong.

Those wheels are significantly more stable than the nightly builds, I think the 6.2 wheels have been there since August. The ROCm on Radeon docs (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html) 
 have this to say:

> Important! AMD recommends proceeding with ROCm WHLs available at repo.radeon.com. The ROCm WHLs available at PyTorch.org are not tested extensively by AMD as the WHLs change regularly when the nightly builds are updated.

No guarantees this will help with your issue, but in my experience falling back to these wheels when pytorch-related issues arise has been effective.

---

### 评论 #33 — hartmark (2024-10-24T00:00:01Z)

> > I will also try using python 3.10 and install the wheels, are they more stable? It seems everything in ROCm space is quite fast moving so I guess any random time in the nightly is as stable as any manually tagged release version. Correct me if I'm wrong.
> 
> Those wheels are significantly more stable than the nightly builds, I think the 6.2 wheels have been there since August. The ROCm on Radeon docs (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html) have this to say:
> 
> > Important! AMD recommends proceeding with ROCm WHLs available at repo.radeon.com. The ROCm WHLs available at PyTorch.org are not tested extensively by AMD as the WHLs change regularly when the nightly builds are updated.
> 
> No guarantees this will help with your issue, but in my experience falling back to these wheels when pytorch-related issues arise has been effective.

Alright, I'll try  get python 3.10 installed but it seems to be missing in the rocm-docker image.

My docker compose uses this image:
`rocm/pytorch:latest`

---

### 评论 #34 — hartmark (2024-10-24T00:14:11Z)

I tried installing python 3.10 in my docker with this guide:
https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/

But I get an error when trying to install packages. It seems SSL is missing.
```

(venv-comfyui) (base) root@96e6cd1ccc18:~# find *.whl | xargs pip3 install
WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
Processing ./pytorch_triton_rocm-2.3.0+rocm6.2.0.1540b42334-cp310-cp310-linux_x86_64.whl
Processing ./torch-2.3.0+rocm6.2.0-cp310-cp310-linux_x86_64.whl
Processing ./torchvision-0.18.0+rocm6.2.0-cp310-cp310-linux_x86_64.whl
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/filelock/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/filelock/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/filelock/

```

---

### 评论 #35 — hartmark (2024-10-24T00:47:30Z)

I got python installed by using pyenv. I have however an issue  that **torchaudio** is missing, its required for ComfyUI, I cannot see it in  the release folder:
 https://repo.radeon.com/rocm/manylinux/

edit: **safetensors** is also missing

---

### 评论 #36 — hartmark (2024-10-24T01:11:02Z)

I was able to get it up and running now with python 3.10 and stable 6.2 release. I have pushed my changes to the docker repo.

I'm getting the same error as with the nighty ROCm.

```
stable-diffusion-comfyui-1  | HW Exception by GPU node-1 (Agent handle: 0x625f4a09de50) reason :GPU Hang
stable-diffusion-webui-1    | HW Exception by GPU node-1 (Agent handle: 0x90aee00) reason :GPU Hang
stable-diffusion-webui-1    | /conf/startup-webui.sh: line 30:    24 Aborted                 (core dumped) python3 launch.py --skip-python-version-check --enable-insecure-extension-access --listen --port 81 --api --precision full --no-half --no-half-vae
stable-diffusion-comfyui-1  | /conf/startup-comfyui.sh: line 43:    24 Aborted                 (core dumped) python main.py --listen 0.0.0.0 --port 80 --front-end-version Comfy-Org/ComfyUI_frontend@latest --reserve-vram 6
```


---

### 评论 #37 — hartmark (2024-10-24T01:24:31Z)

One workaround seems to use the tiled VAE decode:
![image](https://github.com/user-attachments/assets/e0334b94-7993-461c-93db-a1fdba9dd38b)

Now I'm able to run the workflow and get even the second image generated.

---

### 评论 #38 — schung-amd (2024-10-24T13:29:34Z)

Glad to hear it's working now. Interestingly, when I ran a larger image size it already had an automatic fallback to tiled VAE decode due to lack of VRAM, so I wonder if there's a missing or broken check somewhere. For now, you can try to reduce your VRAM consumption by running without `--force-fp32` and `--fp32-vae`; it's still not clear to me when these flags are necessary for stability, but I was able to get the workflow to run without the flags using the stable torch wheels.

---

### 评论 #39 — hartmark (2024-10-24T13:43:50Z)

> Glad to hear it's working now. Interestingly, when I ran a larger image size it already had an automatic fallback to tiled VAE decode due to lack of VRAM, so I wonder if there's a missing or broken check somewhere. For now, you can try to reduce your VRAM consumption by running without `--force-fp32` and `--fp32-vae`; it's still not clear to me when these flags are necessary for stability, but I was able to get the workflow to run without the flags using the stable torch wheels.

I was already running without those flags because they didn't change so much in stability for me.

Is there any proper fix for the GPU hang in the works at AMD? It seems that the error is something in ROCm that triggering GPU hang.

Then there's a regression in linux kernel because the GPU hang takes down the whole desktop on linux kernel after version 6.8.2.

---

### 评论 #40 — sohaibnd (2024-10-24T13:46:30Z)

> One workaround seems to use the tiled VAE decode: ![image](https://private-user-images.githubusercontent.com/12826053/379509413-e0334b94-7993-461c-93db-a1fdba9dd38b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mjk3NzcxODAsIm5iZiI6MTcyOTc3Njg4MCwicGF0aCI6Ii8xMjgyNjA1My8zNzk1MDk0MTMtZTAzMzRiOTQtNzk5My00NjFjLTkzZGItYTFmZGJhOWRkMzhiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEwMjQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMDI0VDEzMzQ0MFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWU2MzlhNmM5MGQ3MGUwYjkxYTVmODMzMWY1YmQ0OTdmNzQxZDU3NTZjZGFmNDhhNTJlZjBhODVkY2E5ZDZjNjAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.47ffcNjDaMEUfTZ1L1fCxYG22E5bzCVAyctB3cDjOUY)
> 
> Now I'm able to run the workflow and get even the second image generated.

That's good to hear, is this on kernel 6.8.2 still?

---

### 评论 #41 — hartmark (2024-10-24T13:51:38Z)

> > One workaround seems to use the tiled VAE decode: ![image](https://private-user-images.githubusercontent.com/12826053/379509413-e0334b94-7993-461c-93db-a1fdba9dd38b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mjk3NzcxODAsIm5iZiI6MTcyOTc3Njg4MCwicGF0aCI6Ii8xMjgyNjA1My8zNzk1MDk0MTMtZTAzMzRiOTQtNzk5My00NjFjLTkzZGItYTFmZGJhOWRkMzhiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEwMjQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMDI0VDEzMzQ0MFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWU2MzlhNmM5MGQ3MGUwYjkxYTVmODMzMWY1YmQ0OTdmNzQxZDU3NTZjZGFmNDhhNTJlZjBhODVkY2E5ZDZjNjAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.47ffcNjDaMEUfTZ1L1fCxYG22E5bzCVAyctB3cDjOUY)
> > Now I'm able to run the workflow and get even the second image generated.
> 
> That's good to hear, is this on kernel 6.8.2 still?

Aye, this is on 6.8.2, I'll try jump back to latest again and retry how it works using VAE decode (tiling)

I have added an issue at ComfyUI aswell for a feature request to always force tiling if possible.


---

### 评论 #42 — sohaibnd (2024-10-24T13:57:08Z)

> > Glad to hear it's working now. Interestingly, when I ran a larger image size it already had an automatic fallback to tiled VAE decode due to lack of VRAM, so I wonder if there's a missing or broken check somewhere. For now, you can try to reduce your VRAM consumption by running without `--force-fp32` and `--fp32-vae`; it's still not clear to me when these flags are necessary for stability, but I was able to get the workflow to run without the flags using the stable torch wheels.
> 
> I was already running without those flags because they didn't change so much in stability for me.
> 
> Is there any proper fix for the GPU hang in the works at AMD? It seems that the error is something in ROCm that triggering GPU hang.
> 
> Then there's a regression in linux kernel because the GPU hang takes down the whole desktop on linux kernel after version 6.8.2.

Yes, we're currently investigating the GPU hang on 6.8.2 and the system freeze/crash on later kernel versions that you have observed. However, you should note that the 7800XT is not in the list of supported GPUs ([source](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus)), neither are kernel versions above 6.8 ([source](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems)), so there are bound to be issues (in this case with using pytorch) one way or another.

---

### 评论 #43 — hartmark (2024-10-25T11:13:25Z)

> Yes, we're currently investigating the GPU hang on 6.8.2 and the system freeze/crash on later kernel versions that you have observed. However, you should note that the 7800XT is not in the list of supported GPUs ([source](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus)), neither are kernel versions above 6.8 ([source](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems)), so there are bound to be issues (in this case with using pytorch) one way or another.

I understand that you don't support my card (which is a shame for a card costing 5-600$ really)

Thing is that it seems that the issue is mainly due to vram being fully used and GTT is being used.

My qualified guess is that 7900XT will also fail the workflow in this issue if the resolution is bumped up a bit.

Do you have any links to the GPU hang on 6.8.2 and the system freeze/crash on later kernels? Or is all work done behind doors at AMD?

---

### 评论 #44 — sohaibnd (2024-11-05T17:31:56Z)

Hi @hartmark, the issue is being investigated internally. Can you check if the out-of-memory issue (`kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!`) can still be reproduced on kernel 6.11.1 with the stable python wheels you are using from repo.radeon.com? I am still getting the lockup but no longer seeing this out-of-memory error message.

---

### 评论 #45 — hartmark (2024-11-06T23:45:34Z)

I'm on this now:

```
% uname -a
Linux bernard 6.11.6-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 01 Nov 2024 03:30:41 +0000 x86_64 GNU/Linux
```

I get the same GPU hang as I stated here.
https://github.com/ROCm/ROCm/issues/3580#issuecomment-2433715980

I seem to not get this any more though:
`kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!)`

I guess I can remove **--reserve-vram 6** now atleast.

---

### 评论 #46 — hartmark (2024-11-07T00:25:04Z)

I think I have pinpointed that it's the VAE decode that is the culprit.

I have created a new workflow loading an 2048x2048 pixel image, VAE encode it into latent space, upscale latent space by 7, then VAE decode back again to a new image.

You can download VAE from here (put in models/vae folder):
https://huggingface.co/StableDiffusionVN/Flux/blob/main/Vae/flux_vae.safetensors

[Load BIG image VAE encode-decode.json](https://github.com/user-attachments/files/17654451/Load.BIG.image.VAE.encode-decode.json)
![2048x2048](https://github.com/user-attachments/assets/26656963-42cb-44bb-8f5b-83fe7e851e64)

Now I get the same issue with that the desktop is sluggish and stutters with updates. And after a while I got just a blank screen for a second and then it resumed working again. I got this in the journal:

`nov 07 01:10:05 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring gfx_0.0.0 timeout, but soft recovered`

ComfyUI threw out this so it has to do with memory usage:
`stable-diffusion-comfyui-1  | Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.`


---

### 评论 #47 — hartmark (2024-11-07T00:45:12Z)

I tried the new workflow again and got GPU hang once more like I did in comment 3580

just poke me if there is anything else I can test or if you need any more information.

journal:
```
nov 07 01:36:56 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=3295304, emitted seq=3295306
nov 07 01:36:56 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Process information: process plasmashell pid 84232 thread plasmashel:cs0 pid 84261
nov 07 01:36:56 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: GPU reset begin!
nov 07 01:36:56 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Failed to evict queue 3
nov 07 01:36:56 bernard kernel: amdgpu: Failed to suspend process 0x8015
nov 07 01:36:56 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Failed to evict queue 3
nov 07 01:36:56 bernard kernel: amdgpu: Failed to suspend process 0x8017
nov 07 01:36:56 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 2 for dev 4946
nov 07 01:36:56 bernard systemd-coredump[91686]: Process 87058 (pt_main_thread) of user 0 terminated abnormally with signal 6/ABRT, processing...
nov 07 01:36:56 bernard systemd-coredump[91687]: Process 87062 (python3) of user 0 terminated abnormally with signal 6/ABRT, processing...
nov 07 01:36:56 bernard systemd[1]: Started Process Core Dump (PID 91686/UID 0).
nov 07 01:36:56 bernard systemd[1]: Started Process Core Dump (PID 91687/UID 0).
nov 07 01:36:56 bernard systemd[1]: Started Pass systemd-coredump journal entries to relevant user for potential DrKonqi handling.
nov 07 01:36:56 bernard systemd[1]: Started Pass systemd-coredump journal entries to relevant user for potential DrKonqi handling.
nov 07 01:36:58 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
nov 07 01:36:58 bernard kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
nov 07 01:36:59 bernard kernel: [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Dumping IP State
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Dumping IP State Completed
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: MODE1 reset
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: GPU mode1 reset
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: GPU smu mode1 reset
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: GPU reset succeeded, trying to resume
nov 07 01:36:59 bernard kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
nov 07 01:36:59 bernard kernel: [drm] VRAM is lost due to GPU reset!
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: PSP is resuming...
nov 07 01:36:59 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: reserve 0xa700000 from 0x83e0000000 for PSP TMR
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: RAP: optional rap ta ucode is not available
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: SMU is resuming...
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x00505100 (80.81.0)
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: SMU driver if version not matched
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: SMU is resumed successfully!
nov 07 01:37:00 bernard kernel: [drm] DMUB hardware initialized: version=0x07002A00
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
nov 07 01:37:00 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: recover vram bo from shadow start

```

---

### 评论 #48 — hartmark (2024-12-08T01:43:55Z)

> I'm on this now:
> 
> ```
> % uname -a
> Linux bernard 6.11.6-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 01 Nov 2024 03:30:41 +0000 x86_64 GNU/Linux
> ```
> 
> I get the same GPU hang as I stated here. [#3580 (comment)](https://github.com/ROCm/ROCm/issues/3580#issuecomment-2433715980)
> 
> I seem to not get this any more though: `kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!)`
> 
> I guess I can remove **--reserve-vram 6** now atleast.

I'm still getting " *ERROR* Not enough memory for command submission!)`" on latest kernel.

Currently on:
`Linux bernard 6.12.1-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 22 Nov 2024 16:04:27 +0000 x86_64 GNU/Linux`

Is there any news from internal bug-tracker from AMD about the hang issue?

---

### 评论 #49 — sohaibnd (2024-12-09T15:18:01Z)

Hi @hartmark, can you try installing ROCm on Ubuntu 24.04 (or another supported OS) and running on that? I was able to run the workflow on Ubuntu 24.04 with a 7800XT without any issues.

---

### 评论 #50 — hartmark (2024-12-11T00:59:36Z)

> Hi @hartmark, can you try installing ROCm on Ubuntu 24.04 (or another supported OS) and running on that? I was able to run the workflow on Ubuntu 24.04 with a 7800XT without any issues.

What workflow did you try? It would be quite time intensive to reinstall ubuntu on my machine.

I just tried https://github.com/ROCm/ROCm/issues/3580#issuecomment-2461073403
and still get crashes on my archlinux. I'm on kernel 6.12.3, there is 6.12.4 out that I can check.

What kernel does Ubuntu 24.04 use? And what python and ROCm version are you using?

This is the journal log, can it be something with wayland? I'm using KDE plasma:
```
dec 11 01:44:12 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Dumping IP State
dec 11 01:44:12 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Dumping IP State Completed
dec 11 01:44:12 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=404675, emitted seq=404677
dec 11 01:44:12 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Process information: process kwin_wayland pid 1107 thread kwin_wayla:cs0 pid 1157
dec 11 01:44:13 bernard baloo_file_extractor[3466]: Invalid encoding. Ignoring "/home/markus/filen-live/Documents/OSCAR_Data/Profiles/Markus/ResMed_2320342>
dec 11 01:44:13 bernard baloo_file_extractor[3466]: kf.baloo: "/home/markus/filen-live/Documents/OSCAR_Data/Profiles/Markus/ResMed_23203426107/Backup/DATAL>
dec 11 01:44:13 bernard baloo_file_extractor[3466]: kf.baloo: "/home/markus/filen-live/Documents/OSCAR_Data/Profiles/Markus/ResMed_23203426107/Backup/DATAL>
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: MES failed to respond to msg=RESET
dec 11 01:44:14 bernard kernel: [drm:amdgpu_mes_reset_legacy_queue [amdgpu]] *ERROR* failed to reset legacy queue
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: GPU reset begin!
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Failed to evict queue 3
dec 11 01:44:14 bernard kernel: amdgpu: Failed to suspend process 0x8029
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: Failed to evict queue 3
dec 11 01:44:14 bernard kernel: amdgpu: Failed to suspend process 0x8005
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 2 for dev 4946
dec 11 01:44:14 bernard systemd-coredump[31002]: Process 28038 (python) of user 0 terminated abnormally with signal 6/ABRT, processing...
dec 11 01:44:14 bernard systemd-coredump[31001]: Process 28033 (python3) of user 0 terminated abnormally with signal 6/ABRT, processing...
dec 11 01:44:14 bernard systemd[1]: Started Process Core Dump (PID 31002/UID 0).
dec 11 01:44:14 bernard systemd[1]: Started Process Core Dump (PID 31001/UID 0).
dec 11 01:44:14 bernard systemd[1]: Started Pass systemd-coredump journal entries to relevant user for potential DrKonqi handling.
dec 11 01:44:14 bernard systemd[1]: Started Pass systemd-coredump journal entries to relevant user for potential DrKonqi handling.
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: MODE1 reset
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: GPU mode1 reset
dec 11 01:44:14 bernard kernel: amdgpu 0000:0a:00.0: amdgpu: GPU smu mode1 reset

```

---

### 评论 #51 — sohaibnd (2024-12-11T20:01:32Z)

> ### Steps to Reproduce
> I'm running ComfyUI in a docker container. I have created a repo for the docker compose script. You can use this to reproduce the problem.
> 
> 1. clone https://github.com/hartmark/sd-rocm
> 2. download absolutereality model at https://civitai.com/models/81458/absolutereality and save it at `data/checkpoints`
> 3. Startup the docker container with `docker-compose up`
> 4. Wait until ComfyUI have started
> 5. Go to ComfyUI at http://localhost
> 6. Load this workflow and run
>    [workflow.json](https://github.com/user-attachments/files/16606555/workflow.json)

I just followed your original steps to reproduce on Ubuntu 24.04 (which uses kernel 6.8) but it works without a docker container too (I tried it with ROCm 6.2.4+python 3.12+pytorch 2.5.1). Since it works on Ubuntu, the issue is something specific to arch, which is unsupported.




---

### 评论 #52 — hartmark (2024-12-12T02:19:33Z)

> > ### Steps to Reproduce
> > I'm running ComfyUI in a docker container. I have created a repo for the docker compose script. You can use this to reproduce the problem.
> > 
> > 1. clone https://github.com/hartmark/sd-rocm
> > 2. download absolutereality model at https://civitai.com/models/81458/absolutereality and save it at `data/checkpoints`
> > 3. Startup the docker container with `docker-compose up`
> > 4. Wait until ComfyUI have started
> > 5. Go to ComfyUI at http://localhost
> > 6. Load this workflow and run
> >    [workflow.json](https://github.com/user-attachments/files/16606555/workflow.json)
> 
> I just followed your original steps to reproduce on Ubuntu 24.04 (which uses kernel 6.8) but it works without a docker container too (I tried it with ROCm 6.2.4+python 3.12+pytorch 2.5.1). Since it works on Ubuntu, the issue is something specific to arch, which is unsupported.

That one is sometimes successful for me too, I needed to rerun a few times sometimes.

Then I found a more reliably way to crash:
https://github.com/ROCm/ROCm/issues/3580#issuecomment-2461073403

How does that workflow work for you?

---

### 评论 #53 — sohaibnd (2024-12-12T17:27:15Z)

I don't get a crash but VAE decode fails due to insufficient VRAM for this workflow. 
![image](https://github.com/user-attachments/assets/78baf31e-6f6c-4fda-bdf7-6bcad48ded4e)

Trying with a smaller image (1536*1536) works. 




---

### 评论 #54 — hartmark (2024-12-12T19:38:10Z)

> I don't get a crash but VAE decode fails due to insufficient VRAM for this workflow. ![image](https://private-user-images.githubusercontent.com/181746774/395232185-78baf31e-6f6c-4fda-bdf7-6bcad48ded4e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQwMzE5ODYsIm5iZiI6MTczNDAzMTY4NiwicGF0aCI6Ii8xODE3NDY3NzQvMzk1MjMyMTg1LTc4YmFmMzFlLTZmNmMtNGZkYS1iZGY3LTZiY2FkNDhkZWQ0ZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQxMjEyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTIxMlQxOTI4MDZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hZTVlNjU1ODg3MjUxMmFkMWVlMGU3NmIzOTc5YTExZjI5ODhlNjQwMTJkNDlkOWUzZDk1ZDVhNzI5ZjEzYTZlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.cDfPPpoIw99coxYPZuBK53v_6d1PvkjU3Bbl3lR2lcY)
> 
> Trying with a smaller image (1536*1536) works.

I have a theory that when OOM occurs in getting the crashes. Shouldn't the system ram be used instead of getting OOM?

I read in the thread that @schung-amd was on arch Linux. How are you running ComfyUI?

---

### 评论 #55 — sohaibnd (2024-12-18T21:18:44Z)

> Shouldn't the system ram be used instead of getting OOM?

System memory does not automatically get used if you run out of VRAM. It may be possible to move some parts of the model or data to system memory and back to the GPU when needed, but this would have to be done manually in comfyui and would incur data transfer overhead.

> I have a theory that when OOM occurs in getting the crashes. 

That's a plausible theory, but unfortunately there won't be any fix for this as Arch is an unsupported distribution. As mentioned before, you can try using Ubuntu (or another supported OS) for your workload to not experience any crashes, and make use of  tiled VAE decode to address out of memory issues. If you want to keep looking into this and share your findings, feel free to do so and I can move this issue to discussions. Otherwise, I can close this issue.



---

### 评论 #56 — hartmark (2024-12-18T21:51:33Z)

> System memory does not automatically get used if you run out of VRAM. It may be possible to move some parts of the model or data to system memory and back to the GPU when needed, but this would have to be done manually in comfyui and would incur data transfer overhead.

How does one build such solution?


> That's a plausible theory, but unfortunately there won't be any fix for this as Arch is an unsupported distribution. As mentioned before, you can try using Ubuntu (or another supported OS) for your workload to not experience any crashes, and make use of tiled VAE decode to address out of memory issues. If you want to keep looking into this and share your findings, feel free to do so and I can move this issue to discussions. Otherwise, I can close this issue.

My 7800xt has 16GV cram, does your have the same?

7800xt is also not supported so we're already out of bounds here. But I hope AMD will redouble their efforts in AI to break Nvidia dominance.

I hope we can keep this issue open here and would love to even try help out trying any bleeding edge kernels or and exotic fixes for ease the task for AMD to build the best software for our excellent hardware.

I'll see what time I'll get to explore how it behaves in Ubuntu. I think I will try have one netboot image I can customise.



---

### 评论 #57 — sleppyrobot (2025-01-19T04:40:08Z)

This problem is especially bad when trying to use video models, I discovered a work around for Linux, should work on RDNA3
https://github.com/comfyanonymous/ComfyUI/issues/5759#issuecomment-2600591113

---

### 评论 #58 — hartmark (2025-01-28T00:21:49Z)

I haven't ran so much lately, but it seems to be more stable now and doesn't crash as often as before.

I think perhaps ComfyUI have solved some memory leakage because I still get occasionally GPU hang when getting out of vram.

There's a flag to use cpu for VAE decode if you get issues in the future.
https://github.com/comfyanonymous/ComfyUI/issues/5759#issuecomment-2603156947



---

### 评论 #59 — darren-amd (2025-06-25T15:54:58Z)

Hi @hartmark,

Were you able to give this a try on Ubuntu? I can move this thread to discussions if you'd like to keep it open for collaboration, thanks!

---

### 评论 #60 — hartmark (2025-07-01T21:59:55Z)

> Hi [@hartmark](https://github.com/hartmark),
> 
> Were you able to give this a try on Ubuntu? I can move this thread to discussions if you'd like to keep it open for collaboration, thanks!

I haven't been doing so much AI-stuff lately.

It seems that the workflows I get error on wouldn't work anyway on a supported environment as you guys reported it getting out of memory messages.

I have gotten a bit discouraged to continue exploring AI with my GPU as it seems the more advanced workflows requires more than 16GB vram and I'm not in the position of getting any other hardware to overcome vram-limitations.

I hope that in the future the tooling will be better to support less vram and fallback transparently to ram if needed to continue.

We can close this issue and if I have any other issues I'll post them.

---
