# Linux AMD Ryzen AI 9 HX 370 w/ Radeon 890M gfx1150

> **Issue #5108**
> **状态**: closed
> **创建时间**: 2025-07-28T05:26:12Z
> **更新时间**: 2026-01-26T15:01:29Z
> **关闭时间**: 2025-10-21T18:24:48Z
> **作者**: matthiasch
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5108

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

Why is the gfx1150 not supported on Linux (kernel 6.14)?

After realizing that pytorch ROCm does not support this device, I thought I might "just" build it from source. But that just made me realize that there is no support in ANY of the AMD software libraries for this GPU!

In the newest version 6.4.2 there seems to be support for the gfx1151, but not for the gfx1150 (incl.  beta 7) .

When can we see this happening? Or, if not, why?

Thank you.

---

## 评论 (30 条)

### 评论 #1 — schung-amd (2025-07-28T15:22:41Z)

Hi @matthiasch, sorry for the inconvenience. From my understanding, with gfx1150 and gfx1151 we took the approach of enabling some ROCm components in native Windows first, presumably because there was a focus on Windows-based Strix and Strix Halo laptops; this has caused a lot of confusion and pain for Linux and WSL users as well as those needing Pytorch support. 

This is not intended to be the long-term situation, and we are working on it, but I don't have a firm timeline for this to be done. We're aware that this has been in an unacceptable state for too long now and have been adding fuel to the fire to try to accelerate this. No guarantees, and Strix might lag a bit behind Strix Halo, but I expect support by the end of the year (ideally sooner as we try to accelerate).

In the meanwhile, I recommend getting in contact with some of the AMDers and community members working on TheRock in the AMD Developer Community Discord: https://discord.com/invite/amd-dev. They've done great work bridging the gap for gfx1151 so far and can probably help with gfx1150. We may be blocked by enablement of math libraries at the moment though, but I think there should be some enablement coming in the next few months.

---

### 评论 #2 — AbelVM (2025-08-10T11:13:50Z)

Nothing changed with kernel 6.16 + ROCm 6.4.3

---

### 评论 #3 — AbelVM (2025-08-12T08:17:13Z)

Good news with kernel 6.16 + [ROCm 7.0 RC1](https://rocm.docs.amd.com/en/docs-7.0-rc1/preview/install/rocm.html)

```
ROCk module is loaded

=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:                    AMD Ryzen AI 9 HX 370 w/ Radeon 890M
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen AI 9 HX 370 w/ Radeon 890M
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
  Max Clock Freq. (MHz):   5157                               
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
      Size:                    95599392(0x5b2bb20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    95599392(0x5b2bb20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    95599392(0x5b2bb20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    95599392(0x5b2bb20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1150                            
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
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
  Chip ID:                 5390(0x150e)                       
  ASIC Revision:           4(0x4)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 29                                 
  SDMA engine uCode::      11                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    47799696(0x2d95d90) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    47799696(0x2d95d90) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1150         
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
*******                  
Agent 3                  
*******                  
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
  Vendor Name:             AMD                                
  Feature:                 AGENT_DISPATCH                     
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        1(0x1)                             
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          64(0x40)                           
  Queue Type:              SINGLE                             
  Node:                    0                                  
  Device Type:             DSP                                
  Cache Info:              
    L2:                      2048(0x800) KB                     
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          0(0x0)                             
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            0                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:0                                  
  Memory Properties:       
  Features:                AGENT_DISPATCH
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    95599392(0x5b2bb20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536(0x10000) KB                  
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    95599392(0x5b2bb20) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done *** 
```

---

### 评论 #4 — matthiasch (2025-08-12T08:25:34Z)

What is the good news about it? AFAIK this release still does not support gfx1150 as a target device.
I get the same output with Ubuntu 24.04 6.14 + amdgpu-dkms

---

### 评论 #5 — AbelVM (2025-08-12T08:28:23Z)

I only got the CPU agent before; now I get the GPU and NPU agents too

---

### 评论 #6 — matthiasch (2025-08-12T08:35:08Z)

I had that from the start, but that will not help you. The toolkit can not compile for this target, i.e., you can not compile pytorch for this device.
For the NPU the situations is unfortunately even worse. The 1.4 release was useless, and recently they started releasing  for Windows only... https://ryzenai.docs.amd.com/en/latest/inst.html

You can try HSA_OVERRIDE_GFX_VERSION=11.0.2 but it is not so reliable. When I did some pytorch testing with the kernel driver that comes with Ubuntu 24.04 it produces wrong results. Updating using the amdgpu-dkms package seems to work at the moment, but I am not sure how much you can trust it...

---

### 评论 #7 — AbelVM (2025-08-12T08:57:54Z)

Hmmm, starting with kernel 6.14, you shouldn't need the DKMS package, as it includes everything

---

### 评论 #8 — matthiasch (2025-08-12T11:25:25Z)

@AbelVM Did you read?? Wrong computations when not using amdgpu-dkms.

---

### 评论 #9 — AbelVM (2025-08-12T11:46:40Z)

@matthiasch Not only I did read, I also applied comprehension. My point still stands.

Save your rudeness for the people who bear you. 


---

### 评论 #10 — matthiasch (2025-08-12T11:53:33Z)

@AbelVM trying to let people know to be careful with the drivers included in the (Ubuntu) kernel and using HSA_OVERRIDE_GFX_VERSION.
Good luck to you.


---

### 评论 #11 — Juarrow (2025-09-10T18:45:35Z)

To me this is a bummer...

Got the new device today and will return it tomorrow as this is not acceptable.

---

### 评论 #12 — schung-amd (2025-09-10T20:04:59Z)

I'm expecting official support in an upcoming ROCm release, hopefully later this month; unfortunately timelines are still not firm enough to communicate (a process I hope we will be able to improve on in the future) so I can't guarantee anything. Obviously support has been lacking for far too long already, but this should be amended soon.

---

### 评论 #13 — matthiasch (2025-09-11T01:12:19Z)

> I'm expecting official support in an upcoming ROCm release

@schung-amd Can you point to the info in one of the repos where it shows that the HIP compiler will support gfx1150 as a target in the next release? I think I checked the 7.0 beta (docker image), and there was no support.

> To me this is a bummer...
> 
> Got the new device today and will return it tomorrow as this is not acceptable.

@Juarrow I was also surprised that more than one year after the hardware release, there is still no real support (besides some workarounds). I was a long time NVIDIA user, but switched to this device because the hardware looked appealing to me. With NVIDIA this wouldn't have happened, I always had a great out-of-the-box experience. I know I repeat myself, but... one (!) year ago the hardware was announced...

---

### 评论 #14 — onofreiciuc (2025-09-18T19:47:18Z)

gfx1150 added on ROCm/Rock roadmap 
  https://github.com/ROCm/TheRock/commit/7dff9eefe0deb78274c56fcebc586ece326c2fb7

the issues are from 
 March  https://github.com/ROCm/TheRock/issues/150 
 June https://github.com/ROCm/TheRock/issues/844

---

### 评论 #15 — CochainComplex (2025-09-24T17:20:50Z)

..mh I'm just about to buy one. This is a potential deal breaker. 

---

### 评论 #16 — harkgill-amd (2025-10-14T20:32:16Z)

Our latest [ROCm 7.0.2](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.0.2/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html#rocm-7-0-2) release includes support for gfx1150 on Linux. Windows is lagging a bit behind but also has support for the APU with [ROCm 6.4.4 ](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.0.2/docs/compatibility/compatibilityryz/windows/windows_compatibility.html).

---

### 评论 #17 — jammsen (2025-10-18T16:50:22Z)

> Our latest [ROCm 7.0.2](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.0.2/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html#rocm-7-0-2) release includes support for gfx1150 on Linux. Windows is lagging a bit behind but also has support for the APU with [ROCm 6.4.4 ](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.0.2/docs/compatibility/compatibilityryz/windows/windows_compatibility.html).

Hey @harkgill-amd - Thanks for the update and the work, could you please upgrade the Roadmap for the support of AMD Ryzen AI 9 HX 370 / gfx1150 ?

---

### 评论 #18 — CochainComplex (2025-10-21T13:02:38Z)

> Our latest [ROCm 7.0.2](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.0.2/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html#rocm-7-0-2) release includes support for gfx1150 on Linux. Windows is lagging a bit behind but also has support for the APU with [ROCm 6.4.4 ](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.0.2/docs/compatibility/compatibilityryz/windows/windows_compatibility.html).

thx for the update. Sounds great. I have ordered it....now I hope for the XDNA2 support on Linux but this is a different piece of software. Sometimes its hard to love AMD no offense 

---

### 评论 #19 — Juarrow (2025-10-21T17:49:46Z)

 Does anyone here get decent performance with this? I tried it with comfy and - in my setup - it works, but it's abysmal. Could be my setup though.

---

### 评论 #20 — harkgill-amd (2025-10-21T18:24:48Z)

@jammsen, could you please point me to the roadmap you're referring to?

@Juarrow, could you please file a separate issue highlighting your ComfyUI workflow and the results you're seeing? Just want to make sure there's nothing out of the ordinary going on.

To wrap up this thread, I'd like to highlight that both 7.0.2 and 6.4.4 are still considered [pre-releases](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/index.html#use-rocm-on-radeon-and-ryzen), there are some teething issues [documented](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/limitations/limitationsryz.html#release) as we begin to support these new SKUs. We're hoping to address these in future releases and any issues reported against the pre-release will help us do so. Thanks again for all your patience and support!



---

### 评论 #21 — jammsen (2025-10-21T18:41:08Z)

> [@jammsen](https://github.com/jammsen), could you please point me to the roadmap you're referring to?

https://github.com/ROCm/TheRock/blob/main/ROADMAP.md?plain=1#L40 - You said its released so shouldnt there be in line 40 and 64 be an update?



---

### 评论 #22 — andypiper (2025-10-22T09:53:51Z)

> Does anyone here get decent performance with this? I tried it with comfy and - in my setup - it works, but it's abysmal. Could be my setup though.

I am getting between 1.4x to 2x performance over CPU usage with Whisper when using the gfx1150 GPU, FWIW. That said I have 12 cores of CPU, so that's a very decent chunk of compute in the first place.

---

### 评论 #23 — Juarrow (2025-10-26T18:25:12Z)

> > Does anyone here get decent performance with this? I tried it with comfy and - in my setup - it works, but it's abysmal. Could be my setup though.
> 
> I am getting between 1.4x to 2x performance over CPU usage with Whisper when using the gfx1150 GPU, FWIW. That said I have 12 cores of CPU, so that's a very decent chunk of compute in the first place.

What does that mean in terms of it/s?

Do you mind sharing how you set it up? @andypiper 

---

### 评论 #24 — jammsen (2025-10-26T19:51:10Z)

> > Does anyone here get decent performance with this? I tried it with comfy and - in my setup - it works, but it's abysmal. Could be my setup though.
> 
> I am getting between 1.4x to 2x performance over CPU usage with Whisper when using the gfx1150 GPU, FWIW. That said I have 12 cores of CPU, so that's a very decent chunk of compute in the first place.

@andypiper how did you install and configure it? Whats your setup and your Hardware-Setup?

---

### 评论 #25 — andypiper (2025-10-26T19:59:58Z)

Something like this, I didn't make specific notes so this is from shell history.

Framework 13 with Ryzen AI 9 HX 370 mainboard.
Fedora 43 pre-release.

ROCM installed from the AMD repo https://repo.radeon.com/amdgpu-install/7.0.2/rhel/10/amdgpu-install-7.0.2.70002-1.el10.noarch.rpm

`sudo amdgpu-install -y --usecase=rocm,graphics --no-dkms` 
(NB may need to modify the amdgpu-install script as it does not play nicely with dnf5 by default, but I think I only needed to change the remove command, so probably will be fine for an install... it looks like I may have some older things installed from Fedora 43 as well)

```
$ rpm -qa | rg rocm
rocm-llvm-filesystem-19-14.rocm6.4.2.fc43.x86_64
rocm-omp-6.4.2-2.fc43.x86_64
rocm-runtime-6.4.2-2.fc43.x86_64
rocm-comgr-19-14.rocm6.4.2.fc43.x86_64
rocm-smi-6.4.3-1.fc43.x86_64
rocm-clinfo-6.4.2-2.fc43.x86_64
rocm-rpm-macros-6.4.2-1.fc43.noarch
rocm-rpm-macros-modules-6.4.2-1.fc43.noarch
rocm-core-7.0.2.70002-56.el10.x86_64
rocm-llvm-20.0.0.25385.70002-56.el10.x86_64
rocm-device-libs-1.0.0.70002-56.el10.x86_64
rocm-dbgapi-0.77.4.70002-56.el10.x86_64
rocm-smi-lib-7.8.0.70002-56.el10.x86_64
rocm-cmake-0.14.0.70002-56.el10.x86_64
rocminfo-1.0.0.70002-56.el10.x86_64
rocm-language-runtime-7.0.2.70002-56.el10.x86_64
rocm-hip-runtime-7.0.2.70002-56.el10.x86_64
rocm-opencl-2.0.0.70002-56.el10.x86_64
rocm-hip-runtime-devel-7.0.2.70002-56.el10.x86_64
rocm-opencl-devel-2.0.0.70002-56.el10.x86_64
rocm-opencl-sdk-7.0.2.70002-56.el10.x86_64
rocm-openmp-7.0.2.70002-56.el10.x86_64
rocm-debug-agent-2.1.0.70002-56.el10.x86_64
rocm-gdb-16.3.70002-56.el10.x86_64
rocm-developer-tools-7.0.2.70002-56.el10.x86_64
rocm-hip-7.0.2.70002-56.el10.x86_64
rocm-7.0.2.70002-56.el10.x86_64
```

I have Python 3.13.1 installed via pyenv.

`pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm7.0`

At this point:
```
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"}')"
CUDA available: True
Device: AMD Radeon 890M Graphics
```



---

### 评论 #26 — jammsen (2025-10-26T21:43:42Z)

Thanks for sharing @andypiper 

---

### 评论 #27 — Juarrow (2025-10-27T17:39:23Z)

@andypiper thanks a lot. I'll give it a try and then open an issue as suggested by @harkgill-amd if it does not get better.

Been also trying my luck with 7.10 (nightlies), but can't get it to work.

---

### 评论 #28 — jammsen (2025-11-09T18:38:24Z)

> Something like this, I didn't make specific notes so this is from shell history.
> 
> Framework 13 with Ryzen AI 9 HX 370 mainboard. Fedora 43 pre-release.
> 
> ROCM installed from the AMD repo https://repo.radeon.com/amdgpu-install/7.0.2/rhel/10/amdgpu-install-7.0.2.70002-1.el10.noarch.rpm
> 
> `sudo amdgpu-install -y --usecase=rocm,graphics --no-dkms` (NB may need to modify the amdgpu-install script as it does not play nicely with dnf5 by default, but I think I only needed to change the remove command, so probably will be fine for an install... it looks like I may have some older things installed from Fedora 43 as well)
> 
> ```
> $ rpm -qa | rg rocm
> rocm-llvm-filesystem-19-14.rocm6.4.2.fc43.x86_64
> rocm-omp-6.4.2-2.fc43.x86_64
> rocm-runtime-6.4.2-2.fc43.x86_64
> rocm-comgr-19-14.rocm6.4.2.fc43.x86_64
> rocm-smi-6.4.3-1.fc43.x86_64
> rocm-clinfo-6.4.2-2.fc43.x86_64
> rocm-rpm-macros-6.4.2-1.fc43.noarch
> rocm-rpm-macros-modules-6.4.2-1.fc43.noarch
> rocm-core-7.0.2.70002-56.el10.x86_64
> rocm-llvm-20.0.0.25385.70002-56.el10.x86_64
> rocm-device-libs-1.0.0.70002-56.el10.x86_64
> rocm-dbgapi-0.77.4.70002-56.el10.x86_64
> rocm-smi-lib-7.8.0.70002-56.el10.x86_64
> rocm-cmake-0.14.0.70002-56.el10.x86_64
> rocminfo-1.0.0.70002-56.el10.x86_64
> rocm-language-runtime-7.0.2.70002-56.el10.x86_64
> rocm-hip-runtime-7.0.2.70002-56.el10.x86_64
> rocm-opencl-2.0.0.70002-56.el10.x86_64
> rocm-hip-runtime-devel-7.0.2.70002-56.el10.x86_64
> rocm-opencl-devel-2.0.0.70002-56.el10.x86_64
> rocm-opencl-sdk-7.0.2.70002-56.el10.x86_64
> rocm-openmp-7.0.2.70002-56.el10.x86_64
> rocm-debug-agent-2.1.0.70002-56.el10.x86_64
> rocm-gdb-16.3.70002-56.el10.x86_64
> rocm-developer-tools-7.0.2.70002-56.el10.x86_64
> rocm-hip-7.0.2.70002-56.el10.x86_64
> rocm-7.0.2.70002-56.el10.x86_64
> ```
> 
> I have Python 3.13.1 installed via pyenv.
> 
> `pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm7.0`
> 
> At this point:
> 
> ```
> python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"}')"
> CUDA available: True
> Device: AMD Radeon 890M Graphics
> ```

My Proxmox9 + LXC + Docker solution 👍 
https://github.com/jammsen/proxmox-setup-scripts

---

### 评论 #29 — Goldlionren (2025-11-11T00:44:52Z)

I just put my case here: I make my HX370 (AMD 890M,gfx1150) running ComfyUI sucessfully by using Rocm 6.4.4 with Pytorch 2.8 in Python 3.12 env:
Total VRAM 44920 MB, total RAM 32405 MB
pytorch version: 2.8.0a0+gitfc14c65
Set: torch.backends.cudnn.enabled = False for better AMD performance.
AMD arch: gfx1150
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon(TM) 890M Graphics : native
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
Python version: 3.12.12 | packaged by conda-forge | (main, Oct 22 2025, 23:13:34) [MSC v.1944 64 bit (AMD64)]
ComfyUI version: 0.3.67
ComfyUI frontend version: 1.28.8
[Prompt Server] web root: C:\Users\James\miniforge3\envs\rocm-win\Lib\site-packages\comfyui_frontend_package\static
Note: NumExpr detected 24 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 16.
NumExpr defaulting to 16 threads.
[Crystools INFO] Crystools version: 1.27.4
[Crystools INFO] Platform release: 11
[Crystools INFO] JETSON: Not detected.
[Crystools INFO] CPU: AMD Ryzen AI 9 HX PRO 370 w/ Radeon 890M - Arch: AMD64 - OS: Windows 11
[Crystools INFO] pynvml (NVIDIA) initialized.
[Crystools INFO] GPU/s:
[Crystools INFO] 0) AMD Radeon(TM) 890M Graphics
[Crystools INFO] NVIDIA Driver: AMD Driver: Unknown

There are some small warnings, but working well. Compared with Zluda version, it is more stable but a little bit slower as there is no sage attention supported on Rocm version which Zluda supported.

The only issue I can found is that the right click will auto start AMD software app sometime, it is strange.

Hopefully, it can be fixed in the future release and also please try to support Pytorch2.9+ soon.

Thanks,




---

### 评论 #30 — ncw2k69 (2026-01-26T15:01:28Z)

this works for me https://github.com/ncw2k69/linux/blob/main/rocm.md if anyone interested

---
