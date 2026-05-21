# [Issue]: ROCm on WSL and pytorch doesn't work (RX 6800)

> **Issue #3371**
> **状态**: closed
> **创建时间**: 2024-06-27T21:29:19Z
> **更新时间**: 2024-07-11T13:32:21Z
> **关闭时间**: 2024-07-09T18:07:06Z
> **作者**: avishaiDV
> **标签**: AMD Radeon RX 7900 XT, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3371

## 标签

- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Hello, I am trying to use pytorch with ROCm with the new drivers update that enables WSL 2 support.
I was manage to get everything work using the guide on the website but when I try to acctually use the GPU for pytorch it freezes and it doesn't seem to do anything as can be seen in the graph I attach here"
![image](https://github.com/ROCm/ROCm/assets/39707337/918ecd9d-647d-46b2-9783-67cbfcd5bd50)

What could be the problem?

*On the CPU it does work, no freezes

### Operating System

WSL 2 with Ubuntu

### CPU

Intel i5 12600K

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  ENABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    CPU                                
  Uuid:                    CPU-XX                             
  Marketing Name:          CPU                                
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
  Chip ID:                 0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16253276(0xf8015c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16253276(0xf8015c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Marketing Name:          AMD Radeon RX 6800                 
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        16(0x10)                           
  Queue Min Size:          4096(0x1000)                       
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L3:                      131072(0x20000) KB                 
  Chip ID:                 29631(0x73bf)                      
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1815                               
  Internal Node ID:        1                                  
  Compute Unit:            60                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 118                                
  SDMA engine uCode::      0                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16729316(0xff44e4) KB              
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

### Additional Information

_No response_

---

## 评论 (20 条)

### 评论 #1 — avishaiDV (2024-06-27T22:14:39Z)

It also happens on Docker

---

### 评论 #2 — utorque (2024-06-28T12:30:41Z)

RX 6800 isn't officially supported on Linux/WSL -> https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility.html

---

### 评论 #3 — avishaiDV (2024-06-28T12:34:43Z)

> RX 6800 isn't officially supported on Linux/WSL -> https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility.html
> 
> Btw your description says RX7900XT but title & pic says RX 6800. Also make sure you have ROCm 6.1.3 and not 6.1.0

Thank you for your response
The new driver update added support for wsl:
https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-6-1.html

I was forced to select only specific GPU and ROCm version in order to open an issue here...
It should be working with this update

---

### 评论 #4 — avishaiDV (2024-06-28T12:38:51Z)

Moreover, Pytorch does recognise my GPU, but when I am trying to use it. it doesn't work. as can be seen in the attached picture 

---

### 评论 #5 — utorque (2024-06-28T13:04:05Z)

AMD Software supports 6800, ROCm on linux/wsl do not :
![image](https://github.com/ROCm/ROCm/assets/46753758/8af47e0c-144e-4f1a-a7b6-fa31a4a783e7)
Supported hardware is described on the link I gave you before. Unfortunately, only 7900GRE/XT/XTX are supported.

---

### 评论 #6 — avishaiDV (2024-06-28T13:08:42Z)

> AMD Software supports 6800, ROCm on linux/wsl do not : ![image](https://private-user-images.githubusercontent.com/46753758/344170600-8af47e0c-144e-4f1a-a7b6-fa31a4a783e7.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTk1ODAzMTUsIm5iZiI6MTcxOTU4MDAxNSwicGF0aCI6Ii80Njc1Mzc1OC8zNDQxNzA2MDAtOGFmNDdlMGMtMTQ0ZS00ZjFhLWE3YjYtZmEzMWE0YTc4M2U3LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MjglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjI4VDEzMDY1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTMxMTNmZDJmNTAxZDk0YzBlMjljN2Y1MjcyNzc2ZWVkNGE0NjYyMzBlM2MxMzFmYTVjMTAxNzE3ZTZiZDg4NDkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.wxaYv-pA755hR4KQn6xrM8MnIKWMeOHA2SivGD6w2Bo) Supported hardware is described on the link I gave you before. Unfortunately, only 7900GRE/XT/XTX are supported.

The link you provided talks about another driver that was released a week ago, you could not install it on anything other 7900GRE/XT/XTX. This update did make the RX 6800 being shown up in WSL, the previous update didn't.
Now the RX 6800 does work with WSL 2, just as 7900GRE/XT/XTX etc.

---

### 评论 #7 — utorque (2024-06-28T13:26:12Z)

Of that I am not aware, it is then very possible. It does not change the fact that pytorch is using ROCm -not a driver, more like AMD's CUDA, its latest version now supporting WSL, to run. ROCm does not supports RX6800, so it's most likely why it freezes ?

If you follow the first link you gave me, go to the link in "[Use ROCm on Radeon GPUs](https://rocm.docs.amd.com/projects/radeon/en/latest/index.html)", you will see by scrolling to the picture that, from the Radeon family, only 7900GRE/XT/XTX are unfortunately supported. If you go to compatibility matrices, you'll find the link I provided you with before.

I suppose that the latest adrenaline update is at most a good step towards supporting more GPUs since it's now showing up.

That is all I know about this matter, if someone else can provide an alternative or anything I would love to hear it too !

---

### 评论 #8 — avishaiDV (2024-06-28T13:33:06Z)

> Of that I am not aware, it is then very possible. It does not change the fact that pytorch is using ROCm -not a driver, more like AMD's CUDA, its latest version now supporting WSL, to run. ROCm does not supports RX6800, so it's most likely why it freezes ?
> 
> If you follow the first link you gave me, go to the link in "[Use ROCm on Radeon GPUs](https://rocm.docs.amd.com/projects/radeon/en/latest/index.html)", you will see by scrolling to the picture that, from the Radeon family, only 7900GRE/XT/XTX are unfortunately supported. If you go to compatibility matrices, you'll find the link I provided you with before.
> 
> I suppose that the latest adrenaline update is at most a good step towards supporting more GPUs since it's now showing up.
> 
> That is all I know about this matter, if someone else can provide an alternative or anything I would love to hear it too !

ROCm does support RX 6800
https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html
but interestingly the supported list on linux doesn't mention all these cards, now I do notice that. werid.
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html this link is not updated to the latest driver so I am not sure, because as for now it does seems to regocnise my gpu

and if you do search online you can see that people are manage to run pytorch on linux with no problem so I assume the issue I have is WSL related, or something I did wrong
for example:
https://www.reddit.com/r/LocalLLaMA/comments/18ourt4/my_setup_for_using_rocm_with_rx_6700xt_gpu_on/

---

### 评论 #9 — CraftMaster163 (2024-06-30T04:54:51Z)

when i try to install on a 7800xt i get
ROCR: unsupported GPU
hsa api call failure at: ./sources/wsl/tools/rocminfo/rocminfo.cc:1087
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

---

### 评论 #10 — avishaiDV (2024-06-30T05:18:10Z)

> when i try to install on a 7800xt i get ROCR: unsupported GPU hsa api call failure at: ./sources/wsl/tools/rocminfo/rocminfo.cc:1087 Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

What did you try to install? I didn’t get anything like that

---

### 评论 #11 — CraftMaster163 (2024-06-30T16:50:18Z)

Well when i install the amdgpu with rocm then run rocminfo i get that

---

### 评论 #12 — CraftMaster163 (2024-07-07T06:00:11Z)

find any fix or?

---

### 评论 #13 — avishaiDV (2024-07-07T06:03:37Z)

> Well when i install the amdgpu with rocm then run rocminfo i get that

On wsl? 
use the new driver update and follow the guide here https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/howto_wsl.html

---

### 评论 #14 — utorque (2024-07-07T09:16:20Z)

On WSL the compatibility matrix hasn't changed, it's still not supported ->
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html

On Sun, Jul 7, 2024, 08:03 avishaiDV ***@***.***> wrote:

> Well when i install the amdgpu with rocm then run rocminfo i get that
>
> On wsl?
> use the new driver update and follow the guide here
> https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/howto_wsl.html
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/3371#issuecomment-2212335427>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ALEWPXTQI3PM7PVDZZ2ZTDDZLDK47AVCNFSM6AAAAABKAWQKUCVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDEMJSGMZTKNBSG4>
> .
> You are receiving this because you commented.Message ID:
> ***@***.***>
>


---

### 评论 #15 — avishaiDV (2024-07-07T09:22:35Z)

> On WSL the compatibility matrix hasn't changed, it's still not supported -> https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html
> […](#)
> On Sun, Jul 7, 2024, 08:03 avishaiDV ***@***.***> wrote: Well when i install the amdgpu with rocm then run rocminfo i get that On wsl? use the new driver update and follow the guide here https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/howto_wsl.html — Reply to this email directly, view it on GitHub <[#3371 (comment)](https://github.com/ROCm/ROCm/issues/3371#issuecomment-2212335427)>, or unsubscribe <https://github.com/notifications/unsubscribe-auth/ALEWPXTQI3PM7PVDZZ2ZTDDZLDK47AVCNFSM6AAAAABKAWQKUCVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDEMJSGMZTKNBSG4> . You are receiving this because you commented.Message ID: ***@***.***>

Interestingly it does work on native Linux even though the device isn’t listed there. Refer to the Reddit post I sent earlier. 

---

### 评论 #16 — utorque (2024-07-08T07:06:58Z)

> Interestingly it does work on native Linux even though the device isn’t listed there. Refer to the Reddit post I sent earlier.

I was about to say that it was a question of ROCm version, but on the reddit example it uses ROCm 5.6, which should support the Radeon VII only -> https://rocm.docs.amd.com/en/docs-5.6.1/release/gpu_os_support.html

So yea, I guess that compatibility matrix is not worth much, not sure whether it's a good "news" or not.

However in that example, it's a newer GPU that was used on an older ROCm. Maybe some kind of retrocompatibility allowed the GPU to work. Since this is the other way around (newer ROCm, older GPU) and ROCm 6.0 was a big update, it could straight up not work as seen here. 
At the same time gfx1030 is still supported for radeon pro so that does not seem to be an issue. 

---

### 评论 #17 — harkgill-amd (2024-07-09T18:04:13Z)

Hi @avishaiDV, the issue you are seeing with the RX 6800 is expected as it is not currently supported in the beta release of ROCm on WSL. ROCm on WSL currently supports the following GPUs as noted in the [compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html). 

- AMD Radeon RX 7900 XTX
- AMD Radeon RX 7900 XT
- AMD Radeon RX 7900 GRE
- AMD Radeon PRO W7900
- AMD Radeon PRO W7900DS
- AMD Radeon PRO W7800



---

### 评论 #18 — Nuck-TH (2024-07-11T13:27:52Z)

You should see to it that ability to override one way or another is added, otherwise this is completely useless to majority of people.

---

### 评论 #19 — avishaiDV (2024-07-11T13:30:37Z)

> You should see to it that ability to override one way or another is added, otherwise this is completely useless to majority of people.

I don't understand what do you mean

---

### 评论 #20 — avishaiDV (2024-07-11T13:31:29Z)

> Hi @avishaiDV, the issue you are seeing with the RX 6800 is expected as it is not currently supported in the beta release of ROCm on WSL. ROCm on WSL currently supports the following GPUs as noted in the [compatibility matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html).
> 
> * AMD Radeon RX 7900 XTX
> * AMD Radeon RX 7900 XT
> * AMD Radeon RX 7900 GRE
> * AMD Radeon PRO W7900
> * AMD Radeon PRO W7900DS
> * AMD Radeon PRO W7800

Thank you for the reply
Are there any plans for older GPU's to be supported?

---
