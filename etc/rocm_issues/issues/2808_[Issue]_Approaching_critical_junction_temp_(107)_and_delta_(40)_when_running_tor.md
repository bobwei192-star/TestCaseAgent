# [Issue]: Approaching critical junction temp (>107) and delta (>40) when running torch to train models with large dimensions

> **Issue #2808**
> **状态**: closed
> **创建时间**: 2024-01-16T15:46:55Z
> **更新时间**: 2024-06-20T00:20:17Z
> **关闭时间**: 2024-06-20T00:20:17Z
> **作者**: brownbat
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2808

## 描述

### Problem Description

While experimenting with hyperparameters on LSTMs, models with large hidden dimensions (512+) steadily increase GPU junction temperature to near critical levels on a Radeon 7900 XTX.

Welcome any confirmation if anyone else has encountered similar issues.

Keywords: overheating, thermal, heat, temp

### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 5 5500

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

I can consistently reproduce this by running this [LSTM factory](https://github.com/brownbat/cipher_classifier_factory) to generate models and specifying hidden dimensions of 512 or 1024 or similar.

The specific model training code can be found in the [train_LSTM.py](https://github.com/brownbat/cipher_classifier_factory/blob/main/train_lstm.py) module. The model class is fairly boilerplate, with def train_model(data, hyperparams) at [ln200+](https://github.com/brownbat/cipher_classifier_factory/blob/490a21ddc25496b3077385b9b8a49a4452860ffd/train_lstm.py#L200C1-L200C36) detailing the training loop, which could be used to distill this into a toy program for reproducibility.

For system setup I'm using the pytorch [packaged installation](https://pytorch.org/get-started/locally/) whl for either stable (rocm5.6) or nightly (rocm5.7).

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen 5 5500                   
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5500                   
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
  Max Clock Freq. (MHz):   4267                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16148332(0xf6676c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16148332(0xf6676c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16148332(0xf6676c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-3a625686c8030680               
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      19                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***  

### Additional Information

I'm using conky to measure temperatures and load and it reports CPU remains at near 0% usage while GPU goes to 99% while training. At lower dimensions, the GPU goes to 99% but plateaus at a significantly lower temperature, which to me suggests an issue with cooling or throttling specific to VRAM management.

/etc/conky/conky.conf
...
${color grey}CPU Usage:$color $cpu% ${cpubar 4}
${color grey}Processes:$color $processes  ${color grey}Running:$color $running_processes

${color grey}GPU Usage: ${execi 10 /usr/local/bin/gpu_usage.sh}% ${execibar 4 /usr/local/bin/gpu_usage.sh}
${color grey}GPU Junction Temp: ${execi 10 sensors | grep 'junction' | awk '{print $2, $3}'}
${color grey}GPU Edge Temp: ${execi 10 sensors | grep 'edge' | awk '{print $2, $3}'}
...

---

## 评论 (10 条)

### 评论 #1 — brownbat (2024-01-16T15:55:57Z)

Please label "won't fix" or simply "yudkowsky" if melting any commercially available GPUs that attempt to train large models has been included as a feature for AI safety purposes. 😅

---

### 评论 #2 — preda (2024-01-23T10:41:28Z)

What you see may be the normal default behavior of the GPU. It works like this: the GPU goes as fast as it can (i.e. high "sclk", i.e. the frequency of the compute core), the fan does spin up but within limits (i.e. the fan may remain below 100% in order to keep noise down), and the temperature raises. When the temperature starts approaching the critial temp, the sclk is lowered in order to reduce the power consumption, and the temperature stops increasing (i.e. becomes stable at a high value) while the workload is sustained.

To mitigate, I force a lower sclk level. The GPU does not run as fast, but it does maintain a lower temperature with the fan at about 50%. This also reduces the power use of the GPU significantly.


---

### 评论 #3 — FeepingCreature (2024-03-31T10:04:52Z)

Cannot reproduce, unfortunately, on 6.7.11 with rocm 6.0.2 with my Sapphire 7900 XTX Vapor 24G.

Steps taken:

- clone repo
- install dependencies
- patch `run_basic_tests` to have `'hidden_dim': 1024`
- run basic tests for three epochs while observing `sensors`

Highest temps I saw were 81°C junction, 72°C memory.

Note that at lower `hidden_dim`, the GPU isn't even fully busy (`sudo radeontop -c`): are you sure your cooling setup is up to the task? Critical junction temp sounds like a heatjam to me, I've had issues with this on stock fans. Check if your case is getting hot. Alternately, try setting casefans to max in the BIOS.

---

### 评论 #4 — brownbat (2024-04-01T02:06:25Z)

Thanks for taking a look @FeepingCreature, really appreciate it. I don't think the run_basic_tests should trigger this.

## How to Reproduce

I should definitely clarify the steps to reproduce, re-reading my post it's not clear, sorry.

Basically: 

1. Pull the repo.
2. Install requirements.txt
3. Run researcher.py (no modification needed as of the version on 1 April)
4. Wait ~8-10 epochs for crash

run_basic_tests only has 10k samples and only three epochs, that probably just isn't aggressive enough for a crash. In researcher.py I'm using 100k samples and getting to around 8 epochs. If you re-pull and run researcher.py without modifications for 8-10 epochs it should be set up to crash without editing any code. 

[Note: if you previously pulled it and didn't clean it, you may need to delete data/pending_experiments.json to run it cleanly for the first time, that will store queued experiments and run them first.]

That is about an hour of training. I know that is a lot to ask anybody to see this to failure.

## Cooling

I've tried a few different fan orientations including an open case without any noticeable difference so far. I was definitely concerned about system cooling originally, so before posting this I adjusted the case setup a few times without much luck. I'm still open to the possibility of changing cooling further, but I'm not too hopeful at this point. Currently I have two thermaltake fans for intake at the front of the case with two stock bequiet! fans in the rear and top to push the air out, all 120mm. I have an extra 140 noctua sitting around, maybe I could go up to 5 fans, I struggled to squeeze that in here though. Case is mostly empty and I think my cable management is pretty clean, it's routed below the board so shouldn't be even touching airflow. CPU and RAM are close but the GPU is below those and has a pretty good gap on all sides.

## Changing settings [optional]

You shouldn't need to do this at all. But if you want to dig in and play with different settings here's how:

At the top of researcher.py after the imports and comment block ~L62, there's a variable set: default_params. You can adjust parameters there. It's currently: 

```python
default_params = {
    'ciphers': [_get_cipher_names()],
    'num_samples': [100000],
    'sample_length': [500],
    'epochs': [30],
    'num_layers': [128],
    'batch_size': [32],
    'embedding_dim': [32],
    'hidden_dim': [1024],
    'dropout_rate': [0.2],
    'learning_rate': [0.002]
}
```

OR -- you can just add a .json file at \data\pending_experiments.json and populate it with a list of the experiments you want to run in order, ie

```
[{"data_params": {"ciphers": ["english", "caesar", "vigenere", "beaufort", "autokey", "random_noise", "playfair", "bifid", "fractionated_morse", "columnar_transposition"], "num_samples": 100000, "sample_length": 500}, "hyperparams": {"epochs": 30, "num_layers": 128, "batch_size": 32, "embedding_dim": 32, "hidden_dim": 1024, "dropout_rate": 0.2, "learning_rate": 0.002}, "experiment_id": "exp_1"}]
```

One small gotcha, it will run whatever is in pending_experiments.json first, and the default_params appends experiments to the end of pending_experiments, so FIFO. So if you are rapidly testing different settings you need to delete pending_experiments or clear it out to make sure you're running the experiment you specified in default_params immediately.


## Thank you

Thanks again for taking a look, really appreciate it even if it ends up a sanity check and something purely local with my setup, or I just need to RMA the card. Would really like to be able to run longer training runs though.

---

### 评论 #5 — brownbat (2024-04-01T02:16:54Z)

Thanks @preda 

> To mitigate, I force a lower sclk level. The GPU does not run as fast, but it does maintain a lower temperature with the fan at about 50%. This also reduces the power use of the GPU significantly.

Oh interesting, happy to underclock as a test. What's the best way to lower sclk on Ubuntu 22.04?

ChatGPT recommends I create
/etc/modprobe.d/amdgpu.conf
and in it set:
options amdgpu si_dpm_perf_levels="sclk:xxx"

Is there a more direct way to do this through a radeon utility or is that basically the right approach?

---

### 评论 #6 — FeepingCreature (2024-04-01T13:21:00Z)

Alright, I have it running now. We'll see in an hour.

Note that this card needs *seriously a lot a lot* of cooling. Before I got my current fan setup, I had the case open *and* a stationary fan pointed directly at it. Now I'm running four case fans, two in, two out, _each_ 3.6W, and they can just about keep up with the heat output. Four "quiet" fans at 1W per were *definitely not* sufficient.

edit: Seriously, check if the top of your case is getting hot. That's where all the heat accumulates if you have lack of airflow. If you have sufficient airflow, it should be at most warm.

edit: Epoch 2, 83C/76C
edit: Epoch 3, 85C/76C
edit: Epoch 4, 85C/76C
edit: Epoch 5: 84C/76C
edit: Epoch 6: 81C/76C
edit: Epoch 7: 85C/76C
edit: Epoch 8: 83C/76C

(Each entry is junction/memory)

---

### 评论 #7 — brownbat (2024-04-02T00:45:53Z)

Ok that's impressive, I'm going to town on cooling.

I went to 5 fans and even fed one 3w from the aio header so it was basically screaming and pushing a lot of cool air, noticeably dramatic. I was stable at a junction of 91, down about 10 degrees. The card is a bit cursed because its exhaust fans point down instead of up into the air channel, and the hottest part by feel is the edge of the radiator, not the top or bottom.

But still, 91 should be ok, so I felt good. Then got a crash at 91 degrees right at the end of epoch 1. So it's either overheating away from the sensor, or... maybe there's a power issue? (though this is my second psu I've tested), or... I don't know. Bad card, rma?

---

### 评论 #8 — FeepingCreature (2024-04-02T06:08:45Z)

I'm getting crashes with Stable Diffusion that have nothing to do with temperature. The Linux driver is definitely not the most stable piece of software. Try checking if there's already a bug filed for the specific crash message?

---

### 评论 #9 — ppanchad-amd (2024-06-19T18:20:01Z)

@brownbat Can you please close this ticket since it's not a ROCm related issue and perhaps open a ticket under discussion, if needed? Thanks!

---

### 评论 #10 — brownbat (2024-06-20T00:20:11Z)

I'm still unclear about root cause, but really appreciate the suggestions. I'll do a full rebuild next month and hopefully that does it. Will close for now and if I see it again I'll work on a toy program that triggers it more reliably across builds. Thanks all.

---
