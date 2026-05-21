# [Issue]: PyTorch LSTM/RNNs very slow in ROCm

> **Issue #4677**
> **状态**: closed
> **创建时间**: 2025-04-23T22:50:21Z
> **更新时间**: 2025-05-21T19:42:02Z
> **关闭时间**: 2025-05-21T19:42:01Z
> **作者**: ZDisket
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4677

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

When running LSTM, the speed is extremely slow compared to an equivalent, or even _much lesser_ NVIDIA GPU. Discovered while trying to train a reimplementation of Tacotron 2. Asked o3 to make me an LSTM speed test script and tested it in 

### RTX 3080 Ti, Win10
```
PS C:\Users\REDACTED\Internal Docs\Code-Proj> python .\lstm_speed_test.py
Using device: cuda
C:\Users\REDACTED\AppData\Local\Programs\Python\Python39\lib\site-packages\torch\onnx\_internal\_beartype.py:35: UserWarning: unhashable type: 'list'
  warnings.warn(f"{e}")
C:\Users\REDACTED\AppData\Local\Programs\Python\Python39\lib\site-packages\onnxscript\function_libs\torch_lib\graph_building.py:23: UserWarning: unhashable type: 'list'
  from onnxscript._internal import param_manipulation, runtime_typing
Dataset size: 50000  |  Steps/epoch: 196  |  Total params: 0.06 M
Epoch  1 ▸ 1.261s  (0.0064s / step, 39,779 seq/s)
Epoch  2 ▸ 1.091s  (0.0056s / step, 45,976 seq/s)
Epoch  3 ▸ 1.043s  (0.0053s / step, 48,114 seq/s)
Epoch  4 ▸ 1.060s  (0.0054s / step, 47,347 seq/s)
Epoch  5 ▸ 1.110s  (0.0057s / step, 45,212 seq/s)

Finished 5 epochs (250,000 sequences) in 5.57s → 44,916 sequences/s overall.
```

### MI300X, Ubuntu
```
root@enc1-gpuvm013:/var/lib/jenkins# python lstm_speed_test.py 
/var/lib/jenkins/lstm_speed_test.py:120: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
  scaler = torch.cuda.amp.GradScaler(enabled=args.amp)
Using device: cuda
Dataset size: 50000  |  Steps/epoch: 196  |  Total params: 0.06 M
/var/lib/jenkins/lstm_speed_test.py:65: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  with torch.cuda.amp.autocast(args.amp), torch.no_grad():
/var/lib/jenkins/lstm_speed_test.py:79: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  with torch.cuda.amp.autocast(args.amp):
Epoch  1 ▸ 10.382s  (0.0530s / step, 4,833 seq/s)
Epoch  2 ▸ 3.525s  (0.0180s / step, 14,233 seq/s)
Epoch  3 ▸ 3.619s  (0.0185s / step, 13,864 seq/s)
Epoch  4 ▸ 3.654s  (0.0186s / step, 13,731 seq/s)
Epoch  5 ▸ 3.841s  (0.0196s / step, 13,063 seq/s)

Finished 5 epochs (250,000 sequences) in 25.02s → 9,991 sequences/s overall.
```
To investigate further, I ran the profiler on both* and printed the 30 most latency consuming ops after finishing the passes
### CUDA
![Image](https://github.com/user-attachments/assets/b8562699-3d6d-4775-9f98-caced80e2021)
### ROCm
![Image](https://github.com/user-attachments/assets/ca0f7dff-6386-414e-9551-8e73446ee41c)

My observation is that PyTorch w/CUDA ships with a dedicated CuDNN kernel for RNNs, while ROCm does everything naively. 

*: The MI300X machine has ROCm 6.4 and enabling the profiler on that one made the backwards pass error out. So the profiler image is from another with a 7900XTX w/ ROCm 6.3 - which gets a similar speed in the benchmark.

### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

Intel(R) Xeon(R) Platinum 8470

### GPU

AMD Instinct MI300X VF

### ROCm Version

ROCm 6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Acquire pytorch-rocm docker image
2. Grab [this script](https://drive.google.com/file/d/1DyhQV_Y_zaMQhXLkaOfibR4OJxLwBRsL/view?usp=drive_link)
3. `python lstm_speed_test.py`


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    Intel(R) Xeon(R) Platinum 8470     
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) Platinum 8470     
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
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            13                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    230893620(0xdc32834) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    230893620(0xdc32834) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    230893620(0xdc32834) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    230893620(0xdc32834) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-f91d9f93a2e6d19d               
  Marketing Name:          AMD Instinct MI300X VF             
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
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29877(0x74b5)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   1280                               
  Internal Node ID:        1                                  
  Compute Unit:            304                                
  SIMDs per CU:            4                                  
  Shader Engines:          32                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 177                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    200998912(0xbfb0000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    200998912(0xbfb0000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    200998912(0xbfb0000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
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

Using JupyterLab and [this docker image](https://hub.docker.com/layers/rocm/pytorch/rocm6.4_ubuntu22.04_py3.10_pytorch_release_2.6.0/images/sha256-130536fdfceb374626a7bcb8d00b9d796ddfc3115677d51229e5b852d96b5ef4)

---

## 评论 (12 条)

### 评论 #1 — ppanchad-amd (2025-04-24T14:25:15Z)

Hi @ZDisket. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-04-24T20:10:02Z)

Hi @ZDisket, thanks for the reproducer. I can't quite reproduce the 3.5x increase in time/epoch, I'm seeing ~1.8s per epoch on MI300X. One possible factor here is that the reproducer workload is tiny and the MI300 is not being fully utilized; I can speed this up to ~0.5s per epoch with `--batch_size 32768`.

Can you see how much you can speed up performance on the 3080 by increasing the batch size? Also, can you run larger models on the 3080 and report the time/epoch? Not sure how big of a model will fit on the 3080, but increasing `--hidden_size` by a factor of 2 until it no longer fits would be helpful.


---

### 评论 #3 — ZDisket (2025-04-24T20:30:00Z)

> Hi [@ZDisket](https://github.com/ZDisket), thanks for the reproducer. I can't quite reproduce the 3.5x increase in time/epoch, I'm seeing ~1.8s per epoch on MI300X. One possible factor here is that the reproducer workload is tiny and the MI300 is not being fully utilized; I can speed this up to ~0.5s per epoch with `--batch_size 32768`.
> 
> Can you see how much you can speed up performance on the 3080 by increasing the batch size? Also, can you run larger models on the 3080 and report the time/epoch? Not sure how big of a model will fit on the 3080, but increasing `--hidden_size` by a factor of 2 until it no longer fits would be helpful.

At `--hidden_size 512` the 3080 Ti still beats the MI300X at 15.97s → 15,659 sequences/s overall., versus the MI300's 18.98s → 13,172 sequences/s overall.

At `--hidden_size 2048` the MI300X scores 2,364 sequences/s overall, versus the 3080 Ti's 1,500 sequences/s, beating it.
at 4096 training doesn't advance on the 3080

It's important to note that the 3080 Ti is a last-last gen gaming GPU from NVIDIA, versus AMD's current gen datacenter-tier offering. A more apples-to-apples comparison would be versus H100, unfortunately I don't have access to one.

---

### 评论 #4 — schung-amd (2025-04-24T20:37:44Z)

Thanks for the datapoints. Can you step up the batch size on the 3080 by factors of 2 and see how much faster it can get?

> A more apples-to-apples comparison would be versus H100, unfortunately I don't have access to one.

That's true, but having poor speed compared to the 3080 is an issue anyway; just trying to narrow down some potential factors that might be obscuring the real performance gap.

---

### 评论 #5 — ZDisket (2025-04-24T20:46:23Z)

>Can you step up the batch size on the 3080 by factors of 2 and see how much faster it can get?

Sure. 3080 Ti, all hidden size=512, batch size:

512:

```
Dataset size: 50000  |  Steps/epoch: 98  |  Total params: 3.22 M
Epoch  1 ▸ 2.840s  (0.0290s / step, 17,670 seq/s)
Epoch  2 ▸ 2.779s  (0.0284s / step, 18,055 seq/s)
Epoch  3 ▸ 3.029s  (0.0309s / step, 16,563 seq/s)
Epoch  4 ▸ 2.875s  (0.0293s / step, 17,451 seq/s)
Epoch  5 ▸ 2.879s  (0.0294s / step, 17,426 seq/s)

Finished 5 epochs (250,000 sequences) in 14.40s → 17,357 sequences/s overall.
```

1024:
```
Dataset size: 50000  |  Steps/epoch: 49  |  Total params: 3.22 M
Epoch  1 ▸ 2.792s  (0.0570s / step, 17,971 seq/s)
Epoch  2 ▸ 2.911s  (0.0594s / step, 17,236 seq/s)
Epoch  3 ▸ 2.658s  (0.0543s / step, 18,874 seq/s)
Epoch  4 ▸ 2.639s  (0.0539s / step, 19,013 seq/s)
Epoch  5 ▸ 2.619s  (0.0535s / step, 19,156 seq/s)

Finished 5 epochs (250,000 sequences) in 13.62s → 18,355 sequences/s overall.
```
2048:

```
Dataset size: 50000  |  Steps/epoch: 25  |  Total params: 3.22 M
Epoch  1 ▸ 3.059s  (0.1224s / step, 16,738 seq/s)
Epoch  2 ▸ 2.772s  (0.1109s / step, 18,467 seq/s)
Epoch  3 ▸ 2.721s  (0.1089s / step, 18,814 seq/s)
Epoch  4 ▸ 2.633s  (0.1053s / step, 19,446 seq/s)
Epoch  5 ▸ 2.631s  (0.1052s / step, 19,464 seq/s)

Finished 5 epochs (250,000 sequences) in 13.82s → 18,093 sequences/s overall.
```
Higher = OOM




---

### 评论 #6 — schung-amd (2025-04-25T19:26:53Z)

Thanks. I did a bit of profiling, seems like there's a lot of overhead coming from DataLoader. Since the model is small it would probably be faster to load all of it onto the GPU beforehand rather than transfer from pinned host memory every iteration. Increasing the batch size to utilize more of the MI300 hardware provides a significant performance gain, but may result in more epochs required so there's a tradeoff to consider. IMO the comparison to a 3080 with a tiny model like this is not too meaningful, as we can't get close to fully utilizing the MI300 without a very large batch size, but as you say we don't have an apples-to-apples comparison with an NVIDIA accelerator to see where real performance gaps might lie.

It's also not clear to me why the performance I'm seeing on MI300 and 7900XTX is significantly better than what's reported here (although still worse than the reported 3080 performance); could be due to a difference in environment (CPU, your VM, etc.).

---

### 评论 #7 — ZDisket (2025-04-26T18:31:15Z)

> could be due to a difference in environment (CPU, your VM, etc.)

what CPU do your 7900XTX and MI300 envs have?

---

### 评论 #8 — schung-amd (2025-04-28T14:21:15Z)

Can't check the MI300 at the moment, but the 7900XTX system has a 5995WX.

edit: The MI300X system has an EPYC 9454.

---

### 评论 #9 — ZDisket (2025-04-29T22:00:03Z)

@schung-amd Okay, I've investigated further. There is a lot of latency coming from the dataloader. [I've made a new version of the repro](https://drive.google.com/file/d/1gWVqBBv46Rth-AiQPc_Gu5Xf4bCYu3Yl/view?usp=sharing) that only starts the per-epoch count _after_ all tensors are moved to device, so it only counts how much time it takes to do the GPU operations.

On my 3080Ti: (no args)

```
Dataset size: 50000  |  Steps/epoch: 196  |  Total params: 0.06 M
Epoch  1 ▸ 0.003s  (0.0000s / step, 15,463,034 seq/s)
Epoch  2 ▸ 0.004s  (0.0000s / step, 13,610,004 seq/s)
Epoch  3 ▸ 0.002s  (0.0000s / step, 20,155,051 seq/s)
Epoch  4 ▸ 0.004s  (0.0000s / step, 13,044,247 seq/s)
Epoch  5 ▸ 0.003s  (0.0000s / step, 14,515,578 seq/s)

Finished 5 epochs (250,000 sequences) in 5.25s → 47,664 sequences/s overall.

Total GPU time: 0.01672s, -> 0.00334 avg per epoch
```
MI300X, no args:
```
Dataset size: 50000  |  Steps/epoch: 196  |  Total params: 0.06 M
Epoch  1 ▸ 0.018s  (0.0001s / step, 2,722,709 seq/s)
Epoch  2 ▸ 0.010s  (0.0000s / step, 5,244,167 seq/s)
Epoch  3 ▸ 0.010s  (0.0001s / step, 4,811,502 seq/s)
Epoch  4 ▸ 0.011s  (0.0001s / step, 4,596,212 seq/s)
Epoch  5 ▸ 0.010s  (0.0001s / step, 4,779,342 seq/s)

Finished 5 epochs (250,000 sequences) in 19.24s → 12,996 sequences/s overall.

Total GPU time: 0.05984s, -> 0.01197 avg per epoch
```

3080Ti, hidden_size=512, batch_size=512

```
Dataset size: 50000  |  Steps/epoch: 98  |  Total params: 3.22 M
Epoch  1 ▸ 0.633s  (0.0065s / step, 79,243 seq/s)
Epoch  2 ▸ 0.596s  (0.0061s / step, 84,155 seq/s)
Epoch  3 ▸ 0.591s  (0.0060s / step, 84,960 seq/s)
Epoch  4 ▸ 0.586s  (0.0060s / step, 85,653 seq/s)
Epoch  5 ▸ 0.681s  (0.0069s / step, 73,734 seq/s)

Finished 5 epochs (250,000 sequences) in 16.17s → 15,464 sequences/s overall.

Total GPU time: 3.08631s, -> 0.61726 avg per epoch
```

MI300X, same args as above

```
Dataset size: 50000  |  Steps/epoch: 98  |  Total params: 3.22 M
Epoch  1 ▸ 0.013s  (0.0001s / step, 3,943,792 seq/s)
Epoch  2 ▸ 0.012s  (0.0001s / step, 4,082,086 seq/s)
Epoch  3 ▸ 0.017s  (0.0002s / step, 2,981,101 seq/s)
Epoch  4 ▸ 0.012s  (0.0001s / step, 4,021,734 seq/s)
Epoch  5 ▸ 0.015s  (0.0002s / step, 3,288,930 seq/s)

Finished 5 epochs (250,000 sequences) in 10.73s → 23,304 sequences/s overall.

Total GPU time: 0.06958s, -> 0.01392 avg per epoch
```

Now the MI300X more handily beats the 3080Ti, although as noted this is an unfair comparison. Also I'll have to compare `nn.LSTMCell`

---

### 评论 #10 — schung-amd (2025-04-30T14:24:18Z)

@ZDisket Great, that's a good idea; as you say this is still not an apples-to-apples comparison, but gives a better sense of the compute performance. Hopefully a similar approach (i.e. transferring as much data as possible onto the GPU at once to avoid DataLoader overhead) is effective in increasing the performance of your real workload.

---

### 评论 #11 — schung-amd (2025-05-15T14:54:56Z)

@ZDisket Have you had a chance to test `nn.LSTMCell`, and/or do you need additional guidance on this? Otherwise I'd like to close this issue for now, as I don't think we can make any further conclusions about performance without an apples-to-apples comparison with another accelerator.

---

### 评论 #12 — schung-amd (2025-05-21T19:42:01Z)

Closing for now, feel free to comment if you see poor results for your real workload or need further guidance on this and we can reopen if necessary.

---
