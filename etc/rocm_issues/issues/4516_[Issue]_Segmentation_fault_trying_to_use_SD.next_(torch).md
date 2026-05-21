# [Issue]: Segmentation fault trying to use SD.next (torch)

> **Issue #4516**
> **状态**: closed
> **创建时间**: 2025-03-20T11:00:45Z
> **更新时间**: 2025-04-28T14:41:09Z
> **关闭时间**: 2025-04-23T15:49:00Z
> **作者**: mcondarelli
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4516

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am trying to use `SD.next` with standard Torch implementation.
My `webui-user.sh` contains just:
```
mcon@ikea:~/LLaMaConda/SD.next/sdnext$ cat webui-user.sh 
TORCH_COMMAND="torch==2.4.1+rocm6.1 torchvision==0.19.1+rocm6.1 --index-url https://download.pytorch.org/whl/rocm6.1"
```
I try to start `SD.next`as:
```
HSA_OVERRIDE_GFX_VERSION=11.0.0 PYTORCH_ROCM_ARCH=gfx1100 GPU_DRIVER=rocm AMD_LOG_LEVEL=7 ./webui.sh --debug --use-rocm
```
This bombs with (full log in attach):
```
...
:3:hip_device_runtime.cpp   :636 : 339330727986 us: [pid:723435 tid:0x7eacacbe3140]  hipGetDevice ( 0x7ffd2b25908c ) 
:3:hip_device_runtime.cpp   :644 : 339330727989 us: [pid:723435 tid:0x7eacacbe3140] hipGetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :701 : 339330727995 us: [pid:723435 tid:0x7eacacbe3140]  hipMemcpyWithStream ( 0x7ea883000000, 0x39961840, 8, hipMemcpyHostToDevice, stream:<null> ) 
:3:rocdevice.cpp            :3030: 339330728010 us: [pid:723435 tid:0x7eacacbe3140] Number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:4:command.cpp              :348 : 339330765136 us: [pid:723435 tid:0x7eacacbe3140] Command (CopyHostToDevice) enqueued: 0x398b2490
Segmentation fault (core dumped)
```

[sdnext.log](https://github.com/user-attachments/files/19363520/sdnext.log)

### Operating System

OS: NAME="Linux Mint" VERSION="22.1 (Xia)"

### CPU

CPU:  model name	: AMD Ryzen 9 5950X 16-Core Processor

### GPU

GPU:    Name:                    gfx1102                               Marketing Name:          AMD Radeon™ RX 7600 XT                  Name:                    amdgcn-amd-amdhsa--gfx1102         

### ROCm Version

rocm-6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

```
git clone https://github.com/vladmandic/sdnext.git
cd sdnext
echo 'TORCH_COMMAND="torch==2.4.1+rocm6.1 torchvision==0.19.1+rocm6.1 --index-url https://download.pytorch.org/whl/rocm6.1"' >webui-user.sh
HSA_OVERRIDE_GFX_VERSION=11.0.0 PYTORCH_ROCM_ARCH=gfx1100 GPU_DRIVER=rocm AMD_LOG_LEVEL=7 ./webui.sh --debug --use-rocm
```
NOTE: the `TORCH_COMMAND` line is what was advised by `SD.next` developers (see [this](https://github.com/vladmandic/sdnext/issues/3833)) but I get similar output also with other versions including the latest one.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
mcon@ikea:~/LLaMaConda/SD.next/sdnext$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.10.5 is loaded
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
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
  Max Clock Freq. (MHz):   3400                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65762040(0x3eb72f8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65762040(0x3eb72f8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65762040(0x3eb72f8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65762040(0x3eb72f8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon™ RX 7600 XT           
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2493                               
  BDFID:                   11520                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 412                                
  SDMA engine uCode::      21                                 
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
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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

_No response_

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2025-03-20T14:02:28Z)

Hi @mcondarelli. Internal ticket has been created for investigating this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-04-23T15:49:00Z)

Hi @mcondarelli, sorry for the delayed response, and thank you for reaching out to us. I read through your other posts https://github.com/vladmandic/sdnext/issues/3833 and https://github.com/ROCm/ROCm/issues/4358. As my colleague mentioned, getting FP16 to work with gfx1102 requires more than just HSA_OVERRIDE_GFX_VERSION=11.0.0 due to hardware limitations. There's currently a long-term effort internally for supporting generic GPU targets, but it is not clear how long this will take to propagate to high-level frameworks such as PyTorch. 

Until then, there is little I can help from our side regarding this issue unfortunately. I think it would probably be much easier to see if SDNext can be made to work with PyTorch 2.3.1, as it is the latest version supported by ROCm 5.7. There might always be methods to force FP32 mode, but it might require some hacking around the source code of SDNext. 

I will be closing this issue for now, but please feel free to post more follow-up questions. I will try my best to help.

Thanks! 


---

### 评论 #3 — mcondarelli (2025-04-23T19:42:55Z)

Problem is it's almost (?) impossible to install ROCm 5.7.x on any modern computer.
It doesn't compile from source and precompiled binaries won't run on modern versions of glibc.
What you are effectively saying is: "you made a huge mistake buying Radeon".

---

### 评论 #4 — tcgu-amd (2025-04-23T20:23:18Z)

I understand your frustration, and I am truly sorry regarding you experience with our product. We have received many feedbacks regarding the limited ROCm support on consumer line GPUs, and we have been working on expanding that as we speak right now.  

> Problem is it's almost (?) impossible to install ROCm 5.7.x on any modern computer. It doesn't compile from source and precompiled binaries won't run on modern versions of glibc. What you are effectively saying is: "you made a huge mistake buying Radeon".

Just in case, have you gave https://rocm.docs.amd.com/en/docs-5.7.0/deploy/linux/quick_start.html as try? This page is not longer easy to access, so I am linking it in case you haven't come across it before. I tried it ubuntu 22.04 and it appears to be still working. 

Sorry again about your trouble, and thank you for feedbacks! 

---

### 评论 #5 — mcondarelli (2025-04-24T08:19:26Z)

Will that work with Containerization and "modern" host (which means a more recent  `amdgpu` driver on host?
Unfortunately installing Ubuntu 22.04 on bare metal is not advisable for many reasons.
I you confirm I can use a Doccker/Incus/LXD container with recent drivers I will surely give it a spin (but I seem to recall it failed for some reason).

---

### 评论 #6 — tcgu-amd (2025-04-24T15:28:11Z)

> Will that work with Containerization and "modern" host (which means a more recent `amdgpu` driver on host? Unfortunately installing Ubuntu 22.04 on bare metal is not advisable for many reasons. I you confirm I can use a Doccker/Incus/LXD container with recent drivers I will surely give it a spin (but I seem to recall it failed for some reason.

I see, thanks for the additional context! Using a [ROCm 5.7 docker image](https://hub.docker.com/layers/rocm/dev-ubuntu-22.04/5.7-complete/images/sha256-868bc21c236b0177d1a4aca64771b8a6d2b7c20f3244554e75c11e791d6a2857?context=explore) should work with recent versions of amdgpu. However, the problem is actually with `amdgpu-dkms`, which needs to be installed on the host in order for the docker container to work. This package is usually installed along ROCm and is considered to be a part of the stack. Typically, we recommend keeping the versions of amdgpu-dkms consistent with the containerized ROCm (e.g. amdgpu-dkms installed from ROCm 5.7 installer on the host for docker image with ROCm 5.7.)

The best and most consistent way to get this to work is to install ROCm 5.7 amdgpu-dkms on a host running one of the supported systems (i.e. ubuntu 22.04, RHEL9.2, SLES 15.5). If that doesn't work, systems that derives from these supported systems (e.g. mint for Ubuntu, fedora for RHEL) could be worth a try as well. 

Alternatively, sometimes mismatching amdgpu-dkms and ROCm versions can work as well, especially when the versions are not too far apart. The oldest ROCm for Ubuntu 22.04 is 6.2, so I would [give that a try](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.2.0/install/quick-start.html) (you only need the `sudo apt install amdgpu-dkms` at the end there).

> Unfortunately installing Ubuntu 22.04 on bare metal is not advisable for many reasons.

I am curious, would you mine sharing the reasons? It helps us determine how to expand our support for other linux versions in the future.

Hope this helps,
Thanks

---

### 评论 #7 — mcondarelli (2025-04-27T14:31:45Z)

I will try to use a docker machine with Ubuntu 22.04/ROCm5.7 on my Ubuntu 24.04 server.
Problem with downgrading to 22.04 on bare metal are twofold:
- current kernel (vital component for amdgpu-dkms) will live only to August 2025, than it will have to be replaced (with lk 6.5, if memory serves)
- this server is used for other tasks besides running ROCm (mainly for development) and not al environments run on U22,04.

In general breaking previously working stuff is not seen as a very good programming practice.

IFF I understand the problem right it seems someone "enhanced" the Float16 kernel using more hardware registers than available on my GPU.
Providing a version with the old "less optimized" kernel doesn't look like a very daunting task, especially so if choice can be done at compile-time (of course the "right way" to do this is auto choosing the best kernel at runtime, but that is not really needed in most cases, including mine).

---

### 评论 #8 — tcgu-amd (2025-04-28T14:41:08Z)

@mcondarelli Thank you for the explanation. I understand that switching baremetal OS is often not a viable option, and I really feel your pain. We have received a lot of feedbacks regarding compatibility issues for ROCm and we are working very hard on improving that. 

A bit of a background:

ROCm is in its current state because kernels are directly compiled to GPU ISAs, then bundled together within ROCm. This contrasts with CUDA which compiles code to an intermediate representation i.e. PTX.  In other words, to keep backwards compatibility, we must compile the entirety of ROCm for all GPUs released up to date for every new version, which is not really feasible for us. Due to this, we can only keep a more managable "sliding window" of a set of more recent GPUs. This also means that to extract the best performance out of ROCm, we often have to manually optimize kernels for each GPU. 

Usually, ISAs in the same series/generation of GPUs are very similar, that's why using HSA_OVERRIDE_GFX_VERSION command can often work as a "hack" to allow ROCm to run on unsupported hardware. Unfortunately, despite being similar, there are still differences, which means this hack won't work all the time in cases such as yours. 

With this in mind, what you said in your comment

> Providing a version with the old "less optimized" kernel doesn't look like a very daunting task, especially so if choice can be done at compile-time (of course the "right way" to do this is auto choosing the best kernel at runtime, but that is not really needed in most cases, including mine).

may not look like much work for this particular case. However, from our perspective, it is not a decision for one kernel, but for all older versions of kernels in ROCm. If we were to keep these, we would have to compile them for GPUs on which they are already obsolete. This might not be as trivial and it would appear, and it bloats the already huge binary size. At this point, we would essentially be going our extra way trying to "support" hardware that were decided to be beyond our capability to support. A line has to be drawn somewhere, and unfortunately, this is wouldn't be within it. 

***There's still hope***,

Now, we have realized that the current model is not really sustainable, and there are a couple pieces of work-in-progress within ROCm that can potentially improve the situation. First, there's an ongoing effort to use more generic ISAs in various ROCm components to improve compatibility. However, the result of this shift will not be immediate, but will gradually show up in future releases. For shorter term, there's an effort trying to create a [generic build platform](https://github.com/ROCm/TheRock) for ROCm that allows users to build ROCm (relatively) easily for a significantly expanded set of hardware. Finally, there is also an effort in [shifting from directly compiling to ISAs to using SPIR-V](https://rocm.docs.amd.com/projects/llvm-project/en/develop/conceptual/spirv.html), an AMD GPU target agnostic intermediate representation that could hugely expand our support capability. 

Sorry for the rather long write-up, and sorry for not being able to offer more substantial help. If you are interested in trying your luck compiling for gfx1102, I would suggest giving https://github.com/ROCm/TheRock a try.

I hope this at least provided some insights regarding the current and the future situations of ROCm.

Thanks and best of luck!

---
