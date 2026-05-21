# Unable to run with 7900 xtx

> **Issue #2746**
> **状态**: closed
> **创建时间**: 2023-12-18T08:58:53Z
> **更新时间**: 2024-03-31T15:10:44Z
> **关闭时间**: 2024-03-31T15:10:44Z
> **作者**: AlfredTallMountain
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2746

## 描述

Hi I've tried every combination possible of rocm and pytorch
(with docker, without, from sources, 5.6, 5.7, with env variables, ...)
but all that I get is 100% CPU forever of immediate segfault.

This is on fresh ubuntu 22.04.

amdgpu-install has all the 'usecases', rocminfo and rocm-smi do work,
steam is able to run 3d accelerated games
and on windows the card works (tried stable diffusion, shark ai, directml)

Did anyone here have more luck ?


---

## 评论 (28 条)

### 评论 #1 — terryrankine (2023-12-18T09:30:31Z)

The MOST luck i have had to date.... is.....

ROCm 6.0
with the vm_update kernel flag
and im getting pretty reasonable runs (more than 30mins of processing above 16gb used on the xtx.)

however - i get second monitor digital garbage (imagine bad refreshes) pretty often.

I have been tryin since rocm 5.4.... I feel your pain.

`GRUB_CMDLINE_LINUX="amd_iommu=on iommu=pt fsck.mode=force amdgpu.vm_update_mode=3"`

as you can see - i force file system checks cos it crashes way to often....

```
terryr@theblob:~$ rocminfo 
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
  Name:                    AMD Ryzen 5 3600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 3600X 6-Core Processor 
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
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98783216(0x5e34ff0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98783216(0x5e34ff0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98783216(0x5e34ff0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-f4b3a217836b48ac               
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
  BDFID:                   12032                              
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
```

```
Linux theblob 6.2.0-39-generic #40~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 16 10:53:04 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

```
terryr@theblob:~$ lsmod | grep amd
edac_mce_amd           45056  0
kvm_amd               204800  0
ccp                   131072  1 kvm_amd
kvm                  1347584  1 kvm_amd
amdgpu              16470016  11
amddrm_ttm_helper      16384  1 amdgpu
amdttm                106496  2 amdgpu,amddrm_ttm_helper
amddrm_buddy           20480  1 amdgpu
amdxcp                 16384  1 amdgpu
amd_sched              61440  1 amdgpu
amdkcl                 45056  3 amd_sched,amdttm,amdgpu
drm_display_helper    212992  1 amdgpu
drm_kms_helper        249856  4 drm_display_helper,amdgpu
drm                   700416  17 drm_kms_helper,amd_sched,amdttm,drm_display_helper,amdgpu,amddrm_buddy,amdkcl,amddrm_ttm_helper,amdxcp
i2c_algo_bit           16384  1 amdgpu
video                  73728  1 amdgpu
```



---

### 评论 #2 — AlfredTallMountain (2023-12-18T09:37:36Z)

thanks for the info.
I guess that the consensus is that it's not production ready and it's better to wait ?

---

### 评论 #3 — terryrankine (2023-12-18T09:40:14Z)

The only way it gets there is is we somehow help them see the bugs.....


Not one has said run this trace tool and we will find it yet..... So just
log what you can.....

On Mon, 18 Dec 2023, 5:37 pm AlfredTallMountain, ***@***.***>
wrote:

> thanks for the info.
> I guess that the consensus is that it's not production ready and it's
> better to wait ?
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2746#issuecomment-1859942473>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AAKWX5DMTLKJ3MFPSCWLH3LYKAFGVAVCNFSM6AAAAABAZFHQ7OVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTQNJZHE2DENBXGM>
> .
> You are receiving this because you commented.Message ID:
> ***@***.***>
>


---

### 评论 #4 — AlfredTallMountain (2023-12-18T09:42:08Z)

I'm happy to help, I can easily reproduce the segfault
(by just using the 'official' docker)

do you happen to know how to trace / collect info ?

---

### 评论 #5 — terryrankine (2023-12-18T13:26:54Z)

here is  the journey so far.... since i started trying.... https://github.com/ROCm/ROCm/issues/2689


---

### 评论 #6 — briansp2020 (2023-12-18T13:31:53Z)

You need to install the nightly build. Try installing it with the following command.
>pip3 install --pre --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm5.7

Also, I had better luck with the 5-series kernel. Ubuntu server installs kernel 5.15 instead of 6.2 that Ubuntu desktop uses, though I have not tested the 6-series kernel with ROCm6 yet.

---

### 评论 #7 — AlfredTallMountain (2023-12-18T14:55:27Z)

> here is the journey so far.... since i started trying.... #2689

I see no reply from the rocm devs.
Are they usually reading / reacting ?

---

### 评论 #8 — nartmada (2024-01-11T05:15:08Z)

@AlfredTallMountain, sorry for the delay in responding.  Can you please share your repro steps ?  We will try to repro your issue here at AMD.  Thanks.

---

### 评论 #9 — AlfredTallMountain (2024-01-11T05:28:20Z)

@nartmada sorry for not updating this thread, I then managed to get the stack working
(tested with whisper and stablediffusion)
the solution was to disable the igpu (of the 7800X3D cpu)

this is clearly stated on your documentation here: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html
but i'm blind.

by the way, do you happen to know when rocm 6 will be picked up by pytorch ?
by the way x 2, are you aware of any performance boost between rocm 6 and rocm 5.6 ?

Thanks

---

### 评论 #10 — terryrankine (2024-01-11T05:45:56Z)

> @AlfredTallMountain, sorry for the delay in responding. Can you please share your repro steps ? We will try to repro your issue here at AMD. Thanks.

There are a few of us who got 'further' but there is still a large memory bug out there - you can make the driver die pretty reliabliy with you are using >20Gb VRAM (but not exceeding it) within about 15-20 mins.

[@Veryunstablerice 
](https://github.com/VeryUnstableRice) should be able to confirm.

https://github.com/ROCm/ROCm/issues/2689

---

### 评论 #11 — terryrankine (2024-01-11T05:47:19Z)

chrome + stablediffusion - just crashed in under 12mins....

`terryr@theblob:~$ uptime
 13:46:13 up 12 min,  1 user,  load average: 1.43, 1.14, 0.72
`

Happy to run whatever tooling you like for bug reports.

---

### 评论 #12 — nartmada (2024-01-12T16:30:35Z)

> @nartmada sorry for not updating this thread, I then managed to get the stack working (tested with whisper and stablediffusion) the solution was to disable the igpu (of the 7800X3D cpu)
> 
> this is clearly stated on your documentation here: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html but i'm blind.
> 
> by the way, do you happen to know when rocm 6 will be picked up by pytorch ? by the way x 2, are you aware of any performance boost between rocm 6 and rocm 5.6 ?
> 
> Thanks

@AlfredTallMountain, let me reach out to the internal team regarding your 2 questions.  Thanks.

---

### 评论 #13 — nartmada (2024-01-12T16:33:13Z)

> > @AlfredTallMountain, sorry for the delay in responding. Can you please share your repro steps ? We will try to repro your issue here at AMD. Thanks.
> 
> There are a few of us who got 'further' but there is still a large memory bug out there - you can make the driver die pretty reliabliy with you are using >20Gb VRAM (but not exceeding it) within about 15-20 mins.
> 
> [@Veryunstablerice ](https://github.com/VeryUnstableRice) should be able to confirm.
> 
> #2689

Thanks @terryrankine.  I will reach out to the internal team and ask for guidance to debug the memory issue.

---

### 评论 #14 — terryrankine (2024-01-17T00:39:35Z)

where did you get to with this?

On Sat, 13 Jan 2024 at 00:33, Adam Tran - AMD ***@***.***>
wrote:

> @AlfredTallMountain <https://github.com/AlfredTallMountain>, sorry for
> the delay in responding. Can you please share your repro steps ? We will
> try to repro your issue here at AMD. Thanks.
>
> There are a few of us who got 'further' but there is still a large memory
> bug out there - you can make the driver die pretty reliabliy with you are
> using >20Gb VRAM (but not exceeding it) within about 15-20 mins.
>
> @Veryunstablerice <https://github.com/VeryUnstableRice> should be able to
> confirm.
>
> #2689 <https://github.com/ROCm/ROCm/issues/2689>
>
> Thanks @terryrankine <https://github.com/terryrankine>. I will reach out
> to the internal team and ask for guidance to debug the memory issue.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2746#issuecomment-1889611720>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AAKWX5HNBUZVTEJIWUOGFOTYOFQVJAVCNFSM6AAAAABAZFHQ7OVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTQOBZGYYTCNZSGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #15 — nartmada (2024-01-17T03:21:52Z)

Hi @terryrankine, sorry for the delay in getting back.  For the issue with "... >20Gb VRAM", #2689 has a similar signature to one of the internal issues which got fixed recently.  The fix should be included in the next ROCm release 6.0.1 (target date late Jan 2024).  For the 2 pytorch related questions, I am still waiting for internal team to get back to me.  

---

### 评论 #16 — nartmada (2024-01-22T22:59:24Z)

@terryrankine, @AlfredTallMountain, regarding the pytorch questions:

Do you happen to know when rocm 6 will be picked up pytorch?
-ETA probably another week.  We are in process of doing this, but we have hit an issue related to permission.

Are you aware of any performance boost between rocm 6 and rocm 5.6 ?
-There is optimization done throughout the ROCm stack.  So, in generally there is definitely performance improvement between ROCm 5.6 to ROCm 6.0.

Also, pytorch + ROCm 6.0 nightly wheel are available:  https://download.pytorch.org/whl/nightly/torch/
It can be used by any community user to try ROCm 6.0.

Hope I have answered your questions.  


---

### 评论 #17 — terryrankine (2024-01-23T23:24:09Z)

the new packages are in the repo now.

6.0.1 packages released - instructions not up dated - but if you are here - you can probably work it out....

https://repo.radeon.com/amdgpu-install/6.0.1/
https://repo.radeon.com/rocm/apt/6.0.1/

good luck

---

### 评论 #18 — AlfredTallMountain (2024-01-24T03:02:32Z)

Terry thanks for the update.
I've tried a 'before and after' and I don't see a perf difference
but probably something in the whisper and stable-diffusion packages is still using rocm 5.7

---

### 评论 #19 — AlfredTallMountain (2024-01-24T03:22:00Z)

I'm unable to upgrade torch, torchaudio and torchvision
I've tried:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
(and nightly)

```
test@linux:~$ pip list|grep -i torch
pytorch-triton-rocm                   2.2.0+dafe145982
torch                                 2.3.0.dev20240123+rocm5.7
torchaudio                            2.2.0.dev20240123+rocm5.7
torchvision                           0.18.0.dev20240123+rocm5.7


---

### 评论 #20 — terryrankine (2024-01-24T06:18:54Z)

[image: image.png]

not sure how the management of deps are organised - but they exist


On Wed, 24 Jan 2024 at 11:22, AlfredTallMountain ***@***.***>
wrote:

> I'm unable to upgrade torch, torchaudio and torchvision
> I've tried:
> pip3 install torch torchvision torchaudio --index-url
> https://download.pytorch.org/whl/rocm6.0
> (and nightly)
>
> ***@***.***:~$ pip list|grep -i torch
> pytorch-triton-rocm                   2.2.0+dafe145982
> torch                                 2.3.0.dev20240123+rocm5.7
> torchaudio                            2.2.0.dev20240123+rocm5.7
> torchvision                           0.18.0.dev20240123+rocm5.7
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2746#issuecomment-1907290519>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AAKWX5CKEJD6WDUY5YQMV3TYQB46FAVCNFSM6AAAAABAZFHQ7OVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTSMBXGI4TANJRHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #21 — terryrankine (2024-01-24T07:12:56Z)

although maybe they are not building everything in rocm 6....

https://github.com/pytorch/pytorch/pull/117433

i can see torch in 6, but no torchbision etc

also i get some errors on actually running something with the rocm6 whl....
so stay tuned.

> Message ID: ***@***.***>
>>
>


---

### 评论 #22 — dominusbelial (2024-02-02T02:47:37Z)

This is not good, I have the 2 greatest GPUs from AMD and both are basically useless for any kind of AI work. I'm selling my w7900 and going for a A100.

---

### 评论 #23 — terryrankine (2024-02-02T03:08:26Z)

so.....

I was able to build torch, torchvision, and torch audio against 6.0.1, and install into the venv for stablediffusion, and then change the stable diffusion code (imports now in different locations) and then.... it ran.....

but the building torchvision and torch audio instructions are bad - but there was instructions for building torch against rocm


So - i will load it up with a big memory model and then see what happens....

#back soon



---

### 评论 #24 — nartmada (2024-02-02T03:26:20Z)

rocm6.0.2 is available at https://rocm.docs.amd.com/en/latest/.  Please give it a try.  Thanks. 

---

### 评论 #25 — dominusbelial (2024-02-16T12:54:28Z)

This is actually looking great, I have comfy UI working and python code using cuda stuff is also working great, I had to re arrenge my GPUs and prefix all my commands to target it and now I can run pytorch example repo whiteout issues.

---

### 评论 #26 — terryrankine (2024-02-17T06:13:46Z)

6.0.2 building against pytorch is working for me - closed my ticket - https://github.com/ROCm/ROCm/issues/2689

---

### 评论 #27 — nartmada (2024-03-22T15:44:10Z)

Apologies for not following up in past few weeks.  Have all the concerns/issues listed in this ticket been fixed?  Thanks.

---

### 评论 #28 — nartmada (2024-03-31T15:10:44Z)

Closing the ticket.  Please re-open if you are still observing concerns/issues listed in this ticket.  Thanks.

---
