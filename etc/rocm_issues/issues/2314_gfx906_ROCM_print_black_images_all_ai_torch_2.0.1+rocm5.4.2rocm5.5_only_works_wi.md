# gfx906 ROCM print black images all ai torch: 2.0.1+rocm5.4.2/rocm5.5 only works with torch=1.13.0+rocm5.2

> **Issue #2314**
> **状态**: closed
> **创建时间**: 2023-07-04T00:54:12Z
> **更新时间**: 2023-09-25T20:34:04Z
> **关闭时间**: 2023-09-25T20:34:03Z
> **作者**: KEDI103
> **标签**: application:pytorch, aimodel:stablediffusion
> **URL**: https://github.com/ROCm/ROCm/issues/2314

## 标签

- **application:pytorch** (颜色: #bfdadc)
- **aimodel:stablediffusion** (颜色: #c2e0c6)

## 描述

Let me summary my problem ( full of it in github links I open multi of them but can't get answer or fix)
I tried my gfx906 Radeon VII card with webui and invoke ai its working with torch==1.13.0+rocm5.2 but with torch==2.0.1+rocm5.4.2 I just got problem as black render. But it work with lots people but in my case I couldn't work it in my case.

Here my history of this:
https://github.com/pytorch/pytorch/issues/103973
https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/9206
https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/10873

At this point I am stuck with out dated pytorch.
Also my card still in rocm support list but my card
https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html

I tried with
directly from rocm https://rocm.docs.amd.com/ 5.5.1/5.6 both of them failed
from https://www.amd.com/en/support/linux-drivers Radeon™ Pro Software for Enterprise on Ubuntu 22.04.1 Installer Revision Number 23.Q1 Release Date 4/27/2023 (Also there is no Ubuntu 22.04.2 and I am using Ubuntu 22.04.2)

python: 3.10.6
working version:
pip install torch==1.13.0+rocm5.2 torchvision==0.14.0+rocm5.2 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/rocm5.2
Not working
pip install torch==2.0.1+rocm5.4.2 torchvision==0.15.2+rocm5.4.2 --index-url https://download.pytorch.org/whl/rocm5.4.2
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm5.5

```
bcansin@BCANSINSMAINUBUNTU:~$ apt show rocm-libs -a
Package: rocm-libs
Version: 5.6.0.50600-67~22.04
Priority: optional
Section: devel
Maintainer: ROCm Libs Support <rocm-libs.support@amd.com>
Installed-Size: 13,3 kB
Depends: hipblas (= 1.0.0.50600-67~22.04), hipblaslt (= 0.2.0.50600-67~22.04), hipfft (= 1.0.12.50600-67~22.04), hipsolver (= 1.8.0.50600-67~22.04), hipsparse (= 2.3.6.50600-67~22.04), miopen-hip (= 2.20.0.50600-67~22.04), rccl (= 2.16.5.50600-67~22.04), rocalution (= 2.1.9.50600-67~22.04), rocblas (= 3.0.0.50600-67~22.04), rocfft (= 1.0.23.50600-67~22.04), rocrand (= 2.10.17.50600-67~22.04), rocsolver (= 3.22.0.50600-67~22.04), rocsparse (= 2.5.2.50600-67~22.04), rocm-core (= 5.6.0.50600-67~22.04), hipblas-dev (= 1.0.0.50600-67~22.04), hipblaslt-dev (= 0.2.0.50600-67~22.04), hipcub-dev (= 2.13.1.50600-67~22.04), hipfft-dev (= 1.0.12.50600-67~22.04), hipsolver-dev (= 1.8.0.50600-67~22.04), hipsparse-dev (= 2.3.6.50600-67~22.04), miopen-hip-dev (= 2.20.0.50600-67~22.04), rccl-dev (= 2.16.5.50600-67~22.04), rocalution-dev (= 2.1.9.50600-67~22.04), rocblas-dev (= 3.0.0.50600-67~22.04), rocfft-dev (= 1.0.23.50600-67~22.04), rocprim-dev (= 2.13.0.50600-67~22.04), rocrand-dev (= 2.10.17.50600-67~22.04), rocsolver-dev (= 3.22.0.50600-67~22.04), rocsparse-dev (= 2.5.2.50600-67~22.04), rocthrust-dev (= 2.18.0.50600-67~22.04), rocwmma-dev (= 1.1.0.50600-67~22.04)
Homepage: https://github.com/RadeonOpenCompute/ROCm
Download-Size: 1.010 B
APT-Sources: https://repo.radeon.com/rocm/apt/5.6 jammy/main amd64 Packages
Description: Radeon Open Compute (ROCm) Runtime software stack

bcansin@BCANSINSMAINUBUNTU:~$ rocminfo
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD FX(tm)-9590 Eight-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD FX(tm)-9590 Eight-Core Processor
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
  Max Clock Freq. (MHz):   4700                               
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
      Size:                    32757548(0x1f3d72c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32757548(0x1f3d72c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32757548(0x1f3d72c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx906                             
  Uuid:                    GPU-be60788172fd5d3e               
  Marketing Name:          AMD Radeon VII                     
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
    L2:                      8192(0x2000) KB                    
  Chip ID:                 26287(0x66af)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1801                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            60                                 
  SIMDs per CU:            4                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
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

---

## 评论 (23 条)

### 评论 #1 — stalkerg (2023-08-01T03:49:48Z)

As I understand, your AMD FX does not support atomics on PCIe, it should work fine on modern systems. 

---

### 评论 #2 — xuhuisheng (2023-08-01T06:20:53Z)

It weired that torch 2.0.1 required PCIe-atomics when torch 1.13 dont required on same card.

---

### 评论 #3 — KEDI103 (2023-08-01T18:39:30Z)

So is that my CPU not GPU problem all the time?

---

### 评论 #4 — xuhuisheng (2023-08-01T23:55:55Z)

My 3rd gen intel cpu may have same lacking pcie -atomics problem.
It weired that Rocm already said there is no longer required pcie-atomics feature for gfx9.
But I think my cpu is really old, so i just buy a 4th gen cpu and going to test my gfx906.
In this week i may received cpu and mother board to test it.

---

### 评论 #5 — KEDI103 (2023-08-02T00:13:16Z)

> My 3rd gen intel cpu may have same lacking pcie -atomics problem. It weired that Rocm already said there is no longer required pcie-atomics feature for gfx9. But I think my cpu is really old, so i just buy a 4th gen cpu and going to test my gfx906. In this week i may received cpu and mother board to test it.

Thats great I am waiting for your test.  Also I glad people reply to my problem because this problem waste my tons of time and starting get hopeless.

---

### 评论 #6 — stalkerg (2023-08-02T03:35:09Z)

> It weired that torch 2.0.1 required PCIe-atomics when torch 1.13 dont required on same card.

it's a good question, but I definitely remember such drama with PCIe atomics. Basically, this is why they drop gfx8 support. 
https://rocmdocs.amd.com/en/latest/understand/More-about-how-ROCm-uses-PCIe-Atomics.html



---

### 评论 #7 — xuhuisheng (2023-08-02T07:26:26Z)

@stalkerg 
Yes, they just drop gfx8 to dust.

But I can run llama-4bit with gfx8 on myself compiled pytoch-2.0, which gfx906 always report wrong results.
At the same time, gfx8 cannot support MAGA, so I cannot execute gptq on gfx8.

Now I have to run quantize llama-7b on gfx906, and copy it to gfx8 to inference. HaHa. Wish my 4th gen motherboard arrived this week. So I can run this steps on one PC.

---

### 评论 #8 — xuhuisheng (2023-08-03T03:32:39Z)

My mistake. gfx803 cannot run properly on ROCm-5.6 either. I have to rollback to ROCm-5.5 to run pytorch-2.0.

And because of hurrican effect, I don't know when could get my new motherboard.
😭 

---

### 评论 #9 — xuhuisheng (2023-08-18T00:24:28Z)

Bad news.
I bought another b85 motherboard, gfx906 cannot run properly with pytorch-2.x on i5 4750 and b85 motherboard.
I am afraid it is not PCIe Atomic related error.

I will find time to do more test.

---

### 评论 #10 — stalkerg (2023-08-18T03:06:24Z)

What exactly do you run? Maybe I can test it on my Vega56.

---

### 评论 #11 — xuhuisheng (2023-08-18T04:59:38Z)

![image](https://github.com/RadeonOpenCompute/ROCm/assets/1118508/cf5c66c9-5eca-47af-a794-140242a202d3)
pytorch-2.0.1 example mnist, always result accuracy 1%.

https://download.pytorch.org/whl/nightly/rocm5.6/torch-2.1.0.dev20230817%2Brocm5.6-cp310-cp310-linux_x86_64.whl

While mnist get right result on torch-1.13.1 and gfx906. 

---

### 评论 #12 — KEDI103 (2023-08-18T16:25:50Z)

> Bad news. I bought another b85 motherboard, gfx906 cannot run properly with pytorch-2.x on i5 4750 and b85 motherboard. I am afraid it is not PCIe Atomic related error.
> 
> I will find time to do more test.

I just can't build new pc or buy new parts right now I am waiting for new cpu and gpus to release. And while waiting is impossible to get not black images with gfx906 with pytorch 2 with my setup am I cursed to use pytorch 1 until the new pc.

Also after all of this rocm things I decided to leave AMD to Nvidia. Before this happend I was thinking AMD workstation cards now thinking nvidia. And its sad to leave AMD since 2005 I always buy AMD gpu and cpus.(I bought 4 laptops 4 destops maybe more devices inculude AMD and suggest to my every friend) 

gfx906 made me so much suffer. I really want my wasted time back. %100 regret to buy AMD instead of Nvidia because of gfx906 rocm support.

---

### 评论 #13 — xuhuisheng (2023-08-21T12:23:13Z)

@KEDI103 @stalkerg 
I had a mistake that I plug the gfx906 to the second pcie socket except first pcie socket. All we know that only first socket of PCIe support PCIe atomic operation. So I plug the gfx906 to the first socket of PCIe, the error of mnist had gone. I had released and going to find time do more tests, just like SD and llama with pytorch-2.0.


```
Train Epoch: 14 [56960/60000 (95%)]     Loss: 0.052591
Train Epoch: 14 [57600/60000 (96%)]     Loss: 0.001324
Train Epoch: 14 [58240/60000 (97%)]     Loss: 0.027882
Train Epoch: 14 [58880/60000 (98%)]     Loss: 0.006072
Train Epoch: 14 [59520/60000 (99%)]     Loss: 0.002215

Test set: Average loss: 0.0267, Accuracy: 9916/10000 (99%)

```

Wish me luck.  :D

---

### 评论 #14 — stalkerg (2023-08-21T14:12:04Z)

@xuhuisheng LOL it's a surprise! I also find this ticket #910 seems like a really common issue, but I can't find it in the documentation or so... is it means if I have 4 cards, only the first one can really work? 

---

### 评论 #15 — KEDI103 (2023-08-21T14:22:53Z)

> @KEDI103 @stalkerg I had a mistake that I plug the gfx906 to the second pcie socket except first pcie socket. All we know that only first socket of PCIe support PCIe atomic operation. So I plug the gfx906 to the first socket of PCIe, the error of mnist had gone. I had released and going to find time do more tests, just like SD and llama with pytorch-2.0.
> 
> ```
> Train Epoch: 14 [56960/60000 (95%)]     Loss: 0.052591
> Train Epoch: 14 [57600/60000 (96%)]     Loss: 0.001324
> Train Epoch: 14 [58240/60000 (97%)]     Loss: 0.027882
> Train Epoch: 14 [58880/60000 (98%)]     Loss: 0.006072
> Train Epoch: 14 [59520/60000 (99%)]     Loss: 0.002215
> 
> Test set: Average loss: 0.0267, Accuracy: 9916/10000 (99%)
> ```
> 
> Wish me luck. :D



> @xuhuisheng LOL it's a surprise! I also find this ticket #910 seems like a really common issue, but I can't find it in the documentation or so... is it means if I have 4 cards, only the first one can really work?

so I am nona try this on my unsupported radeon vii gfx906
https://community.amd.com/t5/gaming/how-to-running-optimized-automatic1111-stable-diffusion-webui-on/ba-p/625585
if this not work too just give up and wait to next release of professinal cards but probally gona be nvidia if amd not made cheaper useable ( not like gfx906 dissater awfull thing ) lets see.

---

### 评论 #16 — KEDI103 (2023-08-21T20:47:35Z)

> so I am nona try this on my unsupported radeon vii gfx906 https://community.amd.com/t5/gaming/how-to-running-optimized-automatic1111-stable-diffusion-webui-on/ba-p/625585 if this not work too just give up and wait to next release of professinal cards but probally gona be nvidia if amd not made cheaper useable ( not like gfx906 dissater awfull thing ) lets see.

never mind this is most awfull pointless thing I have ever tried and they said x9,9 incarese are they okey...? This thing wasted so much time and my dispointment so indescribable.
- Linux pytorch 1.13 even nailed this one. can't even generate at 1280x720 
- so low options 
- you need covent models to optimazition ones...
- tons of unneed steps + it their problems.
and more etc...
why AMD can't make things right like nvidia cuda why rocm ultra suck and make us suffer so much....

---

### 评论 #17 — xuhuisheng (2023-08-22T06:56:15Z)

gfx906 with torch: 2.1.0.dev20230820+rocm5.6.

* [OK] stable diffusion
* [OK] exllama + llama2 4bit gptq

Seems all we need is PCIe Atomic Feature.

---

### 评论 #18 — xuhuisheng (2023-08-22T07:18:58Z)

> @xuhuisheng LOL it's a surprise! I also find this ticket #910 seems like a really common issue, but I can't find it in the documentation or so... is it means if I have 4 cards, only the first one can really work?

Actually, I cannot say anything about the PCIe Atomic. Years before who said: Oh, you are using an OLD card named gfx803, RX580, and this card is too old to get any official support, We suggest you buy a new card, likes gfx900, gfx906, which wont require PCIe Atomic feature, even they can run properly on PCI 2.0.

Then I bought a gfx906 , although this gfx906 is not a new card. And half a year later, they said gfx906 requred PCIe Atomic feature，too, If your cpu or motherboard cannot support PCIe Atomi feature, you cannot upgrade torch-2.x.

Haha~

I didn't test Xeon platform yet, so I am not sure if xeon platform, likes x99, can support more than one PCIe socket for PCIe Atomic feature. But It looks like if we used Core serial, Only the first socket of PCIe connect CPU directly, and only the first socket of PCIe can support Atomic Feature.

BTW: years before, I really beg ROCm team to show me a way to workaround PCIe Atomic Feature for gfx803, no-one reply anything about it. Only somebody from phononix said the PCIe Atomic Feature requirement is hardcoding in firmware, Even ROCm is opensource. there is noway to custom firmeware. It is the dead end.



---

### 评论 #19 — stalkerg (2023-08-23T07:12:35Z)

Yeah, maybe somebody like John Bridgman can clarify this. 

PS rusticl even not use amdkfd now and it's working good ) unfortunately pytorch doesn't support opencl. 

---

### 评论 #20 — KEDI103 (2023-08-23T16:20:35Z)

> > @xuhuisheng LOL it's a surprise! I also find this ticket #910 seems like a really common issue, but I can't find it in the documentation or so... is it means if I have 4 cards, only the first one can really work?
> 
> Actually, I cannot say anything about the PCIe Atomic. Years before who said: Oh, you are using an OLD card named gfx803, RX580, and this card is too old to get any official support, We suggest you buy a new card, likes gfx900, gfx906, which wont require PCIe Atomic feature, even they can run properly on PCI 2.0.
> 
> Then I bought a gfx906 , although this gfx906 is not a new card. And half a year later, they said gfx906 requred PCIe Atomic feature，too, If your cpu or motherboard cannot support PCIe Atomi feature, you cannot upgrade torch-2.x.
> 
> Haha~
> 
> I didn't test Xeon platform yet, so I am not sure if xeon platform, likes x99, can support more than one PCIe socket for PCIe Atomic feature. But It looks like if we used Core serial, Only the first socket of PCIe connect CPU directly, and only the first socket of PCIe can support Atomic Feature.
> 
> BTW: years before, I really beg ROCm team to show me a way to workaround PCIe Atomic Feature for gfx803, no-one reply anything about it. Only somebody from phononix said the PCIe Atomic Feature requirement is hardcoding in firmware, Even ROCm is opensource. there is noway to custom firmeware. It is the dead end.

Here if you install dev ROCm 5.6 to AUTOMATIC1111 its open but when you tried to gen BOOM this happend... well thank you for ROCm team and Pytorch team broke everything after 
`pip install torch==1.13.1+rocm5.2 torchvision==0.14.1+rocm5.2 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/rocm5.2`

I am just angry at this point.

torch: 2.1.0.dev20230822+rocm5.6

```
*** Error completing request
*** Arguments: ('task(06wwmzeaj9eyez8)', 'miku', '', [], 20, 'Euler a', 1, 1, 7, 512, 512, False, 0.7, 2, 'Latent', 0, 0, 0, 'Use same checkpoint', 'Use same sampler', '', '', [], <gradio.routes.Request object at 0x7f531b2c4ac0>, 0, False, '', 0.8, -1, False, -1, 0, 0, 0, 0.9, 5, '0.0001', False, 'None', '', 0.1, False, False, '', 0, False, 7, 100, 'Constant', 0, 'Constant', 0, 4, True, 'MEAN', 'AD', 1, <scripts.controlnet_ui.controlnet_ui_group.UiControlNetUnit object at 0x7f531f48feb0>, <scripts.controlnet_ui.controlnet_ui_group.UiControlNetUnit object at 0x7f531f48fe20>, <scripts.controlnet_ui.controlnet_ui_group.UiControlNetUnit object at 0x7f531b2d66e0>, <scripts.controlnet_ui.controlnet_ui_group.UiControlNetUnit object at 0x7f531b2d5e40>, '', None, ['artist', 'character', 'species', 'general'], '', 'Reset form', 'Generate', '', '', False, False, 3, 0, False, False, 0, False, False, None, None, '', '', '', '', 'Auto rename', {'label': 'Upload avatars config'}, 'Open outputs directory', 'Export to WebUI style', True, {'label': 'Presets'}, {'label': 'QC preview'}, '', [], 'Select', 'QC scan', 'Show pics', None, False, False, 'positive', 'comma', 0, False, False, '', 1, '', [], 0, '', [], 0, '', [], True, False, False, False, 0, False, None, None, False, None, None, False, None, None, False, None, None, False, 50) {}
    Traceback (most recent call last):
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/call_queue.py", line 57, in f
        res = list(func(*args, **kwargs))
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/call_queue.py", line 36, in f
        res = func(*args, **kwargs)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/txt2img.py", line 55, in txt2img
        processed = processing.process_images(p)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/processing.py", line 722, in process_images
        res = process_images_inner(p)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/extensions/sd-webui-controlnet/scripts/batch_hijack.py", line 42, in processing_process_images_hijack
        return getattr(processing, '__controlnet_original_process_images_inner')(p, *args, **kwargs)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/processing.py", line 783, in process_images_inner
        model_hijack.embedding_db.load_textual_inversion_embeddings()
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/textual_inversion/textual_inversion.py", line 255, in load_textual_inversion_embeddings
        self.expected_shape = self.get_expected_shape()
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/textual_inversion/textual_inversion.py", line 154, in get_expected_shape
        vec = shared.sd_model.cond_stage_model.encode_embedding_init_text(",", 1)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/modules/sd_hijack_clip.py", line 339, in encode_embedding_init_text
        embedded = embedding_layer.token_embedding.wrapped(ids.to(embedding_layer.token_embedding.wrapped.weight.device)).squeeze(0)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/sparse.py", line 162, in forward
        return F.embedding(
      File "/media/b_cansin/ai/ai/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/functional.py", line 2233, in embedding
        return torch.embedding(weight, input, padding_idx, scale_grad_by_freq, sparse)
    RuntimeError: HIP error: the operation cannot be performed in the present state
    HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
    For debugging consider passing HIP_LAUNCH_BLOCKING=1.
    Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


---

```

---

### 评论 #21 — KEDI103 (2023-08-23T17:10:18Z)

@xuhuisheng 
Also from AMD ( I suprised I thought they playing dead ) labeled needs reproduction I suggest type yours too 
https://github.com/pytorch/pytorch/issues/103973


---

### 评论 #22 — xuhuisheng (2023-08-24T00:31:18Z)

@KEDI103 
OK. I will go to show him how to reproduce.

---

### 评论 #23 — hongxiayang (2023-09-25T20:33:44Z)

This is a duplicated issue with upstream pytorch issue: https://github.com/pytorch/pytorch/issues/103973..
I will close this one. 


---
